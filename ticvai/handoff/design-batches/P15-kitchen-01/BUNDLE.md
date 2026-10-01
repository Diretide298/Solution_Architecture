# P15-kitchen-01 — P15 · Kitchen

**10 screens · 27 operations · 28 schemas · 8 permissions**

Platform P15 Kitchen Display · ships as **venue-pos** ·
staff audience · kiosk ·
offline-capable

## Who this is for

**staff on kiosk.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `INCIDENT_REPORT, INCIDENT_VIEW, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **16 of these operations work offline**: chaseStation, fireCourse, getFnbOrder, getHaccpStatus, holdCourse, list86Events, listKitchenStations, listKitchenTickets
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `KIT-001` | Kitchen Operations Command Center | A | 2 | 63 | 6 | 6 | 1 | 3 | — | notStarted (generated) |
| `KIT-002` | Kitchen Display System (KDS) | A | 19 | 27 | 6 | 6 | 2 | 3 | — | notStarted (generated) |
| `KIT-003` | Order Firing & Course Management | A | 22 | 0 | 6 | 4 | 3 | 0 | — | notStarted (generated) |
| `KIT-004` | Active Order Management & Fulfilment Journey | A | 2 | 41 | 6 | 8 | 1 | 6 | — | notStarted (generated) |
| `KIT-005` | Kitchen Station Workload & Dynamic Routing | A | 11 | 16 | 6 | 4 | 1 | 6 | — | notStarted (generated) |
| `KIT-006` | Expeditor & Order Assembly | A | 11 | 27 | 6 | 6 | 0 | 0 | — | notStarted (generated) |
| `KIT-007` | Guest Collection, Buzzer & Digital Notification | A | 7 | 47 | 6 | 7 | 2 | 0 | — | notStarted (generated) |
| `KIT-008` | Exceptions, Re-Fire & Unavailable Items | A | 18 | 14 | 6 | 4 | 0 | 0 | — | notStarted (generated) |
| `KIT-009` | SLA, Priority & Service Rules | A | 76 | 0 | 5 | 18 | 0 | 0 | — | notStarted (generated) |
| `KIT-010` | Kitchen Performance, AI & Operational Optimization | A | 3 | 1 | 6 | 1 | 0 | 3 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `KIT-001` Kitchen Operations Command Center

**Kitchen Operations Command Center — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18156 (APP-POS-KIT-001) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | commandCentre (touchLarge density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/kitchen-operations-command-center` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3a` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **`wireframe.status` corrected 25 August.** When these screens were repointed from the client pack to their own board on 24 August, the status stayed `designed` — **which claimed a client had drawn a board this package generated.** `derivedFrom` keeps the pack frame, which is where the design came from; `status` describes the file being pointed at, and those are different facts. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3a`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen Operations Command Center* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |
| Status | select | optional | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | Sends `?status=` to `listKitchenTickets`. | `listKitchenTickets` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Outlet | picker: choose an outlet | — | — | `listKitchenStations` ?outletId |
| Outlet | picker: choose an outlet | — | — | `listFnbOrders` ?outletId |
| Table visit | picker: choose a table visit | — | — | `listFnbOrders` ?tableVisitId |
| Status | select | — | Ordered · Accepted · In preparation · Ready · Served · Collected · Delivered · Cancelled · Refunded | `listFnbOrders` ?status |

#### Outputs: what the screen shows and produces

**Shown**

**Kitchen tickets** (metric tile, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |
| Lines | list or chips (count when long) | — |
| Line | the name it points at, never the id | — |
| Name | text | — |
| Quantity | 1,234 | — |
| Modifiers | list or chips (count when long) | — |
| Note | text | — |
| Allergens | list or chips (count when long) | — |

**Kitchen stations** (metric tile, from `listKitchenStations`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Menu items | list or chips (count when long) | Items routed to this station. |
| Display workstations | list or chips (count when long) | The kitchen displays assigned to this station (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks … |
| Display endpoint | text | The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station … |
| Is active | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Fnb orders** (metric tile, from `listFnbOrders`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Table visit | the name it points at, never the id | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Lines | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Menu item | the name it points at, never the id | — |
| Quantity | 1,234 | — |
| Modifier options | list or chips (count when long) | — |
| Note | text | Free text to the kitchen. Allergy notes belong here and are surfaced prominently. |
| Seat number | 1,234 | Which cover ordered it. Drives split-by-covers accurately. |
| Course | 1,234 | Course grouping, so the kitchen fires in sequence. |
| Redeem entitlement | text | A meal combo redeemed at the till or by a scan (29 September, MOB-4; applied 30 September). |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Unit price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Line total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales order | the name it points at, never the id | Retyped 29 September (SD-046), and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. |

**Every kitchen ticket** (data table, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bump (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue); `listKitchenStations` (onLoad, List preparation stations and their routing); `listFnbOrders` (onLoad, List F&B orders)

**Where the user goes next**

- → `KIT-002` Kitchen Display System (KDS): *Kitchen Display System (KDS)*
- → `KIT-003` Order Firing & Course Management: *Order Firing & Course Management*
- → `KIT-004` Active Order Management & Fulfilment Journey: *Active Order Management & Fulfilment Journey*; carries `orderId`
- → `KIT-005` Kitchen Station Workload & Dynamic Routing: *Kitchen Station Workload & Dynamic Routing*
- → `KIT-006` Expeditor & Order Assembly: *Expeditor & Order Assembly*
- → `KIT-007` Guest Collection, Buzzer & Digital Notification: *Guest Collection, Buzzer & Digital Notification*; carries `orderId`
- → `KIT-008` Exceptions, Re-Fire & Unavailable Items: *Exceptions, Re-Fire & Unavailable Items*
- → `KIT-009` SLA, Priority & Service Rules: *SLA, Priority & Service Rules*
- → `KIT-010` Kitchen Performance, AI & Operational Optimization: *Kitchen Performance, AI & Operational Optimization*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `listKitchenStations` → `PRODUCT_VIEW` (read) · staff
- `listFnbOrders` → `ORDER_VIEW` (read) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `ORDER_VIEW`

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.5 | The system should support usage of buzzers for notifying guests when their order is ready. A buzzer would be assigned to the guests at the time of taking their order. | Bundles and Promotions | CONTRACTED | data `KitchenTicket` |
| 5.2.3 | The system should be able to have options as Fire & forget and Hold & fire orders(modifications should including the manual time adjustment). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |
| 5.2.4 | The system should be able to have options as phased, timed, delayed ordering (used in fine dine options). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Kitchen Operations Command Center shows live order counts, items pending/firing and kitchen station status. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-332)*

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A52** Design on-seat / location-based F&B delivery: seat-linked QR codes for seated events, and physical location QR codes (e.g., per beach chair/table) for open venues, routing kitchen orders to the scanned location *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'kitchen')*

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-001` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3a`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3a`
- Flow F83 *A kitchen works a service from the rail to the exception*, step 1: Kitchen Operations Command Center. → **Drawn by the client as FNB-3A.** 3 operations on this step.
- Flow F88 *An order is assembled, collected and notified*, step 5: Kitchen Operations Command Center. → **Drawn by the client as FNB-3A.** 3 operations on this step.
- Flow F83 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (63 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump.
- [ ] Every transition is wired: `KIT-002`, `KIT-003`, `KIT-004`, `KIT-005`, `KIT-006`, `KIT-007`, `KIT-008`, `KIT-009`, `KIT-010`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-002` Kitchen Display System (KDS)

**Kitchen Display System (KDS) — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18181 (APP-POS-KIT-002) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as cashier, supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `ticketId` (KIT-002), `visitId` (deepLink) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/kitchen-display-system-kds` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **The screen the platform exists for.** Bumped, not tapped — a bump bar and a touch target sized for somebody wearing gloves. Nothing on it is more than one action deep. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Cross-platform navigation removed 24 August**: EMP-058. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3b` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen Display System (KDS)* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |
| Status | select | optional | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | Sends `?status=` to `listKitchenTickets`. | `listKitchenTickets` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |

**Form: Save kitchen ticket status** (modal, opened by *Save kitchen ticket status*; *Save kitchen ticket status* calls `setKitchenTicketStatus`, *Cancel* sends nothing)

**Collects what `setKitchenTicketStatus` sends before it is called.** Required: `status`, `recordedAt`. Optional: `lineIds`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | — | `setKitchenTicketStatus` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Advance specific lines. Omit for the whole ticket. | `setKitchenTicketStatus` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setKitchenTicketStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setKitchenTicketStatus` body |

Errors to draw in the form: 409 The move is not one of the four above. Names the ticket's current status.

**Form: Fire course** (modal, opened by *Fire course*; *Fire course* calls `fireCourse`, *Cancel* sends nothing)

**Collects what `fireCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `fireAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `fireCourse` body |
| Course `course` | number field | required | — | min 1 | — | — | `fireCourse` body |
| Fire at `fireAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | For `timed` coursing. Absent means now — a server standing at the pass is not scheduling, they are calling it. | `fireCourse` body |

**Form: Hold course** (modal, opened by *Hold course*; *Hold course* calls `holdCourse`, *Cancel* sends nothing)

**Collects what `holdCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `holdCourse` body |
| Course `course` | number field | required | — | min 1 | — | — | `holdCourse` body |
| Reason `reason` | radio group | optional | — | Table not ready · Guest request · Kitchen backed up · Awaiting previous · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `holdCourse` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `holdCourse` body |

Errors to draw in the form: 400 Validation failed

**Form: Refire item** (modal, opened by *Refire item*; *Refire item* calls `refireItem`, *Cancel* sends nothing)

**Collects what `refireItem` sends before it is called.** Required: `lineId`, `reason`, `recordedAt`. Optional: `chargeable`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Line `lineId` | picker: choose a line | required | — | — | shows names, sends the id | `KitchenTicket.lines[].lineId`. The refire is a new line carrying `refireOfLineId`. | `refireItem` body |
| Reason `reason` | select | required | — | Overcooked · Undercooked · Wrong item · Dropped · Cold · Allergy risk · Guest changed mind · Late add | — | Why a line was made again (`refireItem`). The reasons are the data. | `refireItem` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `refireItem` body |
| Chargeable `chargeable` | toggle | optional | off | — | — | False by default, and that default is the point. A refire the kitchen caused is not billable, and making it opt-in stops a busy service quietly charging for its own mistakes. | `refireItem` body |

**Form: Recall kitchen ticket** (modal, opened by *Recall kitchen ticket*; *Recall kitchen ticket* calls `recallKitchenTicket`, *Cancel* sends nothing)

**Collects what `recallKitchenTicket` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `recallKitchenTicket` body |

Errors to draw in the form: 409 Past the recall window (`VenueSettings.fnb.recallWindowMinutes`, proposed default 10, audit R094).

**Form: Notify server** (modal, opened by *Notify server*; *Notify server* calls `notifyServer`, *Cancel* sends nothing)

**Collects what `notifyServer` sends before it is called.** Nothing in the body is required. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | radio group | optional | — | Food ready · Guest waiting · Bill requested · Assistance needed · Allergy query | — | — | `notifyServer` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every kitchen ticket** (data table, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**The selected kitchen ticket** (detail panel, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |
| Lines | list or chips (count when long) | — |
| Target ready at | 1 Oct 2026, 14:30 | — |
| Elapsed seconds | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bump (primary button) | navigation or local | — | — | — | — |
| Save kitchen ticket status (primary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | works offline; gated `ORDER_MODIFY`; opens modal first; produces a document or message: Advance a kitchen ticket |
| Fire course (secondary button) | `fireCourse` POST `/kitchen-tickets/{ticketId}/fire` | inline | KitchenTicket | — | works offline; gated `ORDER_MODIFY`; opens modal first |
| Hold course (secondary button) | `holdCourse` POST `/kitchen-tickets/{ticketId}/hold` | inline | KitchenTicket | 400 Validation failed | works offline; gated `ORDER_MODIFY`; opens modal first |
| Refire item (secondary button) | `refireItem` POST `/kitchen-tickets/{ticketId}/refire` | inline | KitchenTicket | — | works offline; gated `ORDER_MODIFY`; opens modal first |
| Recall kitchen ticket (secondary button) | `recallKitchenTicket` POST `/kitchen-tickets/{ticketId}/recall` | inline | KitchenTicket | 409 Past the recall window (`VenueSettings.fnb.recallWindowMinutes`, proposed default 10, audit R094). | works offline; gated `ORDER_MODIFY`; opens modal first; produces a document or message: Bring back a ticket that was bumped by mistake |
| Notify server (secondary button) | `notifyServer` POST `/table-visits/{visitId}/notify-server` | inline | no body | — | gated `ORDER_MODIFY`; opens modal first |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*
- → `KIT-003` Order Firing & Course Management: *Order Firing & Course Management*; carries `ticketId`
- → `EMP-058` Live Table & Service Management: *Starters cleared*; carries `ticketId`, `visitId`
- → `EMP-059` Table Order, Bill & Payment Management: *The server comps the delayed dish*; carries `visitId`; calls `refireItem`
- → `POS-022` Send to Kitchen: *The guest is called and takes it*; carries `orderId`, `ticketId`; calls `setKitchenTicketStatus`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Past the recall window (`VenueSettings.fnb.recallWindowMinutes`, proposed default 10, audit R094).; 409 The move is not one of the four above. Names the ticket's current status. |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `fireCourse` → `ORDER_MODIFY` (operate) · staff
- `holdCourse` → `ORDER_MODIFY` (operate) · staff
- `refireItem` → `ORDER_MODIFY` (operate) · staff
- `recallKitchenTicket` → `ORDER_MODIFY` (operate) · staff
- `notifyServer` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `ORDER_VIEW`

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.5 | The system should support usage of buzzers for notifying guests when their order is ready. A buzzer would be assigned to the guests at the time of taking their order. | Bundles and Promotions | CONTRACTED | data `KitchenTicket` |
| 5.2.3 | The system should be able to have options as Fire & forget and Hold & fire orders(modifications should including the manual time adjustment). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |
| 5.2.4 | The system should be able to have options as phased, timed, delayed ordering (used in fine dine options). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Kitchen display lets cashier/kitchen mark orders ready, handed over or delivered, driving the guest-facing order-status board. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-794)*
- Each kitchen ticket shows a live "fired" timer counting elapsed time since the order was sent (not a countdown); it resets when a course within that ticket is completed/dished out. Not shown for quick-service outlets, which print and prepare immediately. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-334)*

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A52** Design on-seat / location-based F&B delivery: seat-linked QR codes for seated events, and physical location QR codes (e.g., per beach chair/table) for open venues, routing kitchen orders to the scanned location *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'kitchen')*

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-002` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3b`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3b`
- Flow F108 *A guest orders food at a counter and collects it*, step 5: The kitchen makes it and bumps it. → Ready. The counter sees it on the same rail.
- Flow F29 *A table is seated, coursed and split*, step 4: The kitchen makes the starters and bumps them. → **The pass calls the server rather than waiting to be noticed.** Food ready and nobody collecting it is the commonest reason a plate goes out cold.
- Flow F29 *A table is seated, coursed and split*, step 6: One main comes back wrong. The station refires it. → **`chargeable` false by default.** A refire the kitchen caused is not billable, and making it opt-in stops a busy service quietly charging for its own mistakes.
- Flow F83 *A kitchen works a service from the rail to the exception*, step 2: Kitchen Display System (KDS). → **Drawn by the client as FNB-3B.** 2 operations on this step.
- Flow F88 *An order is assembled, collected and notified*, step 2: Kitchen Display System (KDS). → **Drawn by the client as FNB-3B.** 4 operations on this step.
- Flow F29 branch at step 6 (medium): when The shift changes mid-service., `reassignServer`, and **the gratuity split follows the assignment.** A table reassigned at 8pm and closed at 10pm has two servers with a claim on it.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump, Save kitchen ticket status, Fire course, Hold course, Refire item, Recall kitchen ticket, Notify server.
- [ ] Every transition is wired: `KIT-001`, `KIT-003`, `EMP-058`, `EMP-059`, `POS-022`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-003` Order Firing & Course Management

**Order Firing & Course Management — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18182 (APP-POS-KIT-003) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE` (1 operate, 1 read, 1 configure); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | configEditor (touchLarge density): the screen declares only writes (`setKitchenTicketStatus`, `prioritiseKitchenTicket`, `fireCourse`) and no read of a population — it is settings, not a list |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `ticketId` (KIT-002), `outletId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/order-firing-course-management` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Starters before mains is the entire job of a kitchen pass.** `KitchenTicket.coursing` carries `holdAndFire`, `phased` and `timed`; without it a table gets dessert while eating its starter. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3c` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3c`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Order Firing &amp; Course Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |
| Status | text field | — | — | — | — | Required. | — |
| Recorded at | date picker | — | — | — | — | Required. | — |
| Line ids | multi select | — | — | — | — | — | — |
| Station id | text field | — | — | — | — | Filled from this display's station assignment (`KitchenStation.displayWorkstationIds`), not typed or picked (audit R277). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |

**Form: Prioritise kitchen ticket** (modal, opened by *Prioritise kitchen ticket*; *Prioritise kitchen ticket* calls `prioritiseKitchenTicket`, *Cancel* sends nothing)

**Collects what `prioritiseKitchenTicket` sends before it is called.** Required: `reason`. Optional: `priority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `prioritiseKitchenTicket` body |
| Priority `priority` | stepper or slider | optional | 100 | min 0; max 100 | — | Absent means the top of the queue (decided 28 September, audit R125 (2)): the ticket takes the highest priority on the rail. | `prioritiseKitchenTicket` body |

**Form: Fire course** (modal, opened by *Fire course*; *Fire course* calls `fireCourse`, *Cancel* sends nothing)

**Collects what `fireCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `fireAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `fireCourse` body |
| Course `course` | number field | required | — | min 1 | — | — | `fireCourse` body |
| Fire at `fireAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | For `timed` coursing. Absent means now — a server standing at the pass is not scheduling, they are calling it. | `fireCourse` body |

**Form: Hold course** (modal, opened by *Hold course*; *Hold course* calls `holdCourse`, *Cancel* sends nothing)

**Collects what `holdCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `reason`, `note`. **When the reason is Other, the note is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `holdCourse` body |
| Course `course` | number field | required | — | min 1 | — | — | `holdCourse` body |
| Reason `reason` | radio group | optional | — | Table not ready · Guest request · Kitchen backed up · Awaiting previous · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `holdCourse` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `holdCourse` body |

Errors to draw in the form: 400 Validation failed

**Form: Save course rules** (modal, opened by *Save course rules*; *Save course rules* calls `setCourseRules`, *Cancel* sends nothing)

**Collects what `setCourseRules` sends before it is called.** Nothing in the body is required. Optional: `outletId`, `defaultCoursing`, `courseNames`, `autoFireMinutes`, `serviceModeOverrides`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Default coursing `defaultCoursing` | radio group | optional | — | Fire and forget · Hold and fire · Phased · Timed · Delayed | — | How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock … | `setCourseRules` body |
| Course names `courseNames` | list of values (chips) | optional | — | — | — | — | `setCourseRules` body |
| Auto fire minutes `autoFireMinutes` | number field (minutes) | optional | — | — | — | — | `setCourseRules` body |
| Service mode overrides `serviceModeOverrides` | key and value settings | optional | — | — | — | A different default per service mode. | `setCourseRules` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Sent by *Save kitchen ticket status*** (`setKitchenTicketStatus`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | — | `setKitchenTicketStatus` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Advance specific lines. Omit for the whole ticket. | `setKitchenTicketStatus` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setKitchenTicketStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setKitchenTicketStatus` body |

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save kitchen ticket status (primary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | works offline; gated `ORDER_MODIFY`; produces a document or message: Advance a kitchen ticket |
| Prioritise kitchen ticket (secondary button) | `prioritiseKitchenTicket` POST `/kitchen/tickets/{ticketId}/prioritise` | inline | KitchenTicket | — | gated `ORDER_MODIFY`; opens modal first; produces a document or message: Move a ticket up the queue |
| Fire course (secondary button) | `fireCourse` POST `/kitchen-tickets/{ticketId}/fire` | inline | KitchenTicket | — | works offline; gated `ORDER_MODIFY`; opens modal first |
| Hold course (secondary button) | `holdCourse` POST `/kitchen-tickets/{ticketId}/hold` | inline | KitchenTicket | 400 Validation failed | works offline; gated `ORDER_MODIFY`; opens modal first |
| Save course rules (secondary button) | `setCourseRules` PUT `/outlets/{outletId}/course-rules` | CourseRules | CourseRules | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | gated `PRODUCT_CONFIGURE`; opens modal first |
| Bump (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue, filtered by course (audit R277))

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*
- → `KIT-004` Active Order Management & Fulfilment Journey: *Active Order Management & Fulfilment Journey*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic (audit R277). |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_MODIFY` gets this state naming `ORDER_MODIFY`**, the screen's `permission` and the one its fire, hold, status and prioritise actions need (the screen has no read); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The move is not one of the four above. Names the ticket's current status. |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `prioritiseKitchenTicket` → `ORDER_MODIFY` (operate) · staff
- `fireCourse` → `ORDER_MODIFY` (operate) · staff
- `holdCourse` → `ORDER_MODIFY` (operate) · staff
- `setCourseRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_MODIFY` gets this state naming `ORDER_MODIFY`**, the screen's `permission` and the one its fire, hold, status and prioritise actions need (the screen has no read); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `ORDER_MODIFY`

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.34 | Support automatic and manual prioritization of kitchen orders based on VIP guests, memberships, Fast Pass, SLA targets, group bookings, events, or supervisor override. | Bundles and Promotions | CONTRACTED | `prioritiseKitchenTicket` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The kitchen pass fires courses (starters before mains), as drawn on the F&B boards. *(agreed · client-design-boards-audit 20 Aug 2026, The finding - course firing · DI-407)*
- Each kitchen ticket shows a live "fired" timer counting elapsed time since the order was sent (not a countdown); it resets when a course within that ticket is completed/dished out. Not shown for quick-service outlets, which print and prepare immediately. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-334)*
- Course-wise ordering (mainly fine dining) groups an order by course (starters, main course, dessert) so the kitchen fires each course at the right time. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-333)*

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-003` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3c`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3c`
- Flow F83 *A kitchen works a service from the rail to the exception*, step 3: Order Firing & Course Management. → **Drawn by the client as FNB-3C.** 2 operations on this step.
- Flow F88 *An order is assembled, collected and notified*, step 3: Order Firing & Course Management. → **Drawn by the client as FNB-3C.** 4 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (400, 409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save kitchen ticket status, Prioritise kitchen ticket, Fire course, Hold course, Save course rules, Bump.
- [ ] Every transition is wired: `KIT-001`, `KIT-004`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-004` Active Order Management & Fulfilment Journey

**Active Order Management & Fulfilment Journey — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18157 (APP-POS-KIT-004) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenTickets` reads the population and `getFnbOrder` reads one of them — list, select, act |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `orderId` (KIT-002) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/active-order-management-fulfilment-journey` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3d` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |
| Status | select | optional | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | Sends `?status=` to `listKitchenTickets`. | `listKitchenTickets` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |

#### Outputs: what the screen shows and produces

**Shown**

**Every kitchen ticket** (data table, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**The selected kitchen ticket** (detail panel, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |
| Lines | list or chips (count when long) | — |
| Target ready at | 1 Oct 2026, 14:30 | — |
| Elapsed seconds | 1,234 | — |

**The F&B order** (detail panel, from `getFnbOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Table visit | the name it points at, never the id | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Lines | list or chips (count when long) | — |
| Sales order | the name it points at, never the id | Retyped 29 September (SD-046), and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Kitchen ticket | the name it points at, never the id | — |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bump (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue); `getFnbOrder` (onLoad, Read an F&B order)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*
- → `KIT-008` Exceptions, Re-Fire & Unavailable Items: *Exceptions, Re-Fire & Unavailable Items*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `getFnbOrder` → `ORDER_VIEW` (read) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `ORDER_VIEW`

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.35 | Provide end-to-end order status tracking including Ordered, Accepted, In Preparation, Ready, Served, Collected, Delivered, Cancelled, and Refunded with real-time synchronization. | Bundles and Promotions | CONTRACTED | `getFnbOrder` |
| 5.1.11 | Synchronize order statuses in real time between POS, KDS, Mobile Ordering, QR Ordering, Guest Apps, Delivery Systems, and Reporting Platforms. | F&B & Guest Management | CONTRACTED | `getFnbOrder` |
| 4.7.5 | The system should support usage of buzzers for notifying guests when their order is ready. A buzzer would be assigned to the guests at the time of taking their order. | Bundles and Promotions | CONTRACTED | data `KitchenTicket` |
| 5.2.3 | The system should be able to have options as Fire & forget and Hold & fire orders(modifications should including the manual time adjustment). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |
| 5.2.4 | The system should be able to have options as phased, timed, delayed ordering (used in fine dine options). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Kitchen display lets cashier/kitchen mark orders ready, handed over or delivered, driving the guest-facing order-status board. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-794)*

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-004` · status **notStarted** · provenance generated · **Drawn as FNB-3D in the client pack.** The pack's frame is the specification for this screen — it carries operations, states, entry params and exits, and it is better specified than anything derived …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3d`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3d`
- Flow F83 *A kitchen works a service from the rail to the exception*, step 4: Active Order Management & Fulfilment Journey. → **Drawn by the client as FNB-3D.** 2 operations on this step.
- Flow F88 *An order is assembled, collected and notified*, step 4: Active Order Management & Fulfilment Journey. → **Drawn by the client as FNB-3D.** 2 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump.
- [ ] Every transition is wired: `KIT-001`, `KIT-008`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-005` Kitchen Station Workload & Dynamic Routing

**Kitchen Station Workload & Dynamic Routing — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18158 (APP-POS-KIT-005) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure) |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenStations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/kitchen-station-workload-dynamic-routing` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Station Workload &amp; Dynamic Routing* matched at 0.89. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listKitchenStations`. | `listKitchenStations` ?outletId |
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |

**Form: Save kitchen stations** (modal, opened by *Save kitchen stations*; *Save kitchen stations* calls `setKitchenStations`, *Cancel* sends nothing)

**Collects what `setKitchenStations` sends before it is called.** Required: `stations`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Stations `stations` | repeatable rows | required | — | — | — | — | `setKitchenStations` body |
| ID `stations[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setKitchenStations` body |
| Code `stations[].code` | text field | required | — | — | — | — | `setKitchenStations` body |
| Name `stations[].name` | text field | required | — | — | — | — | `setKitchenStations` body |
| Outlet `stations[].outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | — | `setKitchenStations` body |
| Menu items `stations[].menuItemIds` | multi-picker: choose menu items | optional | — | — | — | Items routed to this station. | `setKitchenStations` body |
| Display workstations `stations[].displayWorkstationIds` | multi-picker: choose display workstations | optional | — | A workstation is assigned to at most one station; a second assignment is refused `400`. | — | The kitchen displays assigned to this station (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks after it. | `setKitchenStations` body |
| Display endpoint `stations[].displayEndpoint` | text field | optional | — | — | — | The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station, with a fallback device where the primary is … | `setKitchenStations` body |
| Is active `stations[].isActive` | toggle | optional | — | — | — | — | `setKitchenStations` body |

Errors to draw in the form: 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

#### Outputs: what the screen shows and produces

**Shown**

**Every kitchen station** (data table, from `listKitchenStations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Menu items | list or chips (count when long) | Items routed to this station. |
| Display endpoint | text | The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station … |
| Display workstations | list or chips (count when long) | The kitchen displays assigned to this station (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks … |
| Is active | yes / no (icon or chip) | — |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**The selected kitchen station** (detail panel, from `listKitchenStations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Menu items | list or chips (count when long) | Items routed to this station. |
| Display endpoint | text | The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station … |
| Display workstations | list or chips (count when long) | The kitchen displays assigned to this station (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks … |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bump (primary button) | navigation or local | — | — | — | — |
| Save kitchen stations (primary button) | `setKitchenStations` PUT `/kitchen/stations` | inline | KitchenStation[] | 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue, filtered by course (audit R277)); `listKitchenStations` (onLoad, List preparation stations and their routing)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation. |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `listKitchenStations` → `PRODUCT_VIEW` (read) · staff
- `setKitchenStations` → `PRODUCT_CONFIGURE` (configure) · staff
- `rebalanceStationLoad` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.33 | Support configurable kitchen routing rules to automatically direct orders/items to kitchen stations, printers, KDS screens, bars, dessert stations, or production areas based on product, category … | Bundles and Promotions | CONTRACTED | `setKitchenStations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Kitchens are divided into stations (grill, fryer, beverage, dessert, etc.), each mapped to specific printers or KDS devices. Routing rules decide where an item prints/displays by category or item, with a fallback station/device if the primary one is offline or faulty. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-323)*

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A52** Design on-seat / location-based F&B delivery: seat-linked QR codes for seated events, and physical location QR codes (e.g., per beach chair/table) for open venues, routing kitchen orders to the scanned location *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-005` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3e`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3e`

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump, Save kitchen stations.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-006` Expeditor & Order Assembly

**Expeditor & Order Assembly — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18183 (APP-POS-KIT-006) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `ticketId` (KIT-002), `orderId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/expeditor-order-assembly` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **No expeditor role is modelled** — this reads and sets ticket status like the KDS. Whether an expeditor needs their own state is a kitchen question rather than a contract one. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Expeditor &amp; Order Assembly* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |
| Status | select | optional | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | Sends `?status=` to `listKitchenTickets`. | `listKitchenTickets` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |

**Form: Save kitchen ticket status** (modal, opened by *Save kitchen ticket status*; *Save kitchen ticket status* calls `setKitchenTicketStatus`, *Cancel* sends nothing)

**Collects what `setKitchenTicketStatus` sends before it is called.** Required: `status`, `recordedAt`. Optional: `lineIds`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | — | `setKitchenTicketStatus` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Advance specific lines. Omit for the whole ticket. | `setKitchenTicketStatus` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setKitchenTicketStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setKitchenTicketStatus` body |

Errors to draw in the form: 409 The move is not one of the four above. Names the ticket's current status.

**Form: Chase station** (modal, opened by *Chase station*; *Chase station* calls `chaseStation`, *Cancel* sends nothing)

**Collects what `chaseStation` sends before it is called.** Required: `ticketId`, `recordedAt`. Optional: `lineId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Ticket `ticketId` | picker: choose a ticket | required | — | — | shows names, sends the id | — | `chaseStation` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | — | `chaseStation` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the chase. Becomes `KitchenException.raisedAt`. | `chaseStation` body |

**Form: Mark order collected** (modal, opened by *Mark order collected*; *Mark order collected* calls `markOrderCollected`, *Cancel* sends nothing)

**Collects what `markOrderCollected` sends before it is called.** Required: `recordedAt`. Optional: `verifiedBy`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Verified by `verifiedBy` | radio group | optional | — | Buzzer · Order number · Name · QR · None | — | — | `markOrderCollected` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the collection. Closes the ready-to-collected clock. | `markOrderCollected` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every kitchen ticket** (data table, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**The selected kitchen ticket** (detail panel, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |
| Lines | list or chips (count when long) | — |
| Target ready at | 1 Oct 2026, 14:30 | — |
| Elapsed seconds | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bump (primary button) | navigation or local | — | — | — | — |
| Save kitchen ticket status (primary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | works offline; gated `ORDER_MODIFY`; opens modal first; produces a document or message: Advance a kitchen ticket |
| Chase station (secondary button) | `chaseStation` POST `/kitchen-stations/{stationId}/chase` | inline | no body | — | works offline; gated `ORDER_MODIFY`; opens modal first |
| Mark order collected (secondary button) | `markOrderCollected` POST `/orders/{orderId}/collected` | inline | FnbOrder | — | works offline; gated `ORDER_MODIFY`; opens modal first |
| Print order label (secondary button) | `printOrderLabel` POST `/kitchen-tickets/{ticketId}/label` | — | OrderLabel | — | works offline; gated `ORDER_VIEW`; produces a document or message: A label for the bag |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*
- → `KIT-002` Kitchen Display System (KDS): *Kitchen Display System (KDS)*; carries `ticketId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The move is not one of the four above. Names the ticket's current status. |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `chaseStation` → `ORDER_MODIFY` (operate) · staff
- `markOrderCollected` → `ORDER_MODIFY` (operate) · staff
- `printOrderLabel` → `ORDER_VIEW` (read) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `ORDER_VIEW`

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.5 | The system should support usage of buzzers for notifying guests when their order is ready. A buzzer would be assigned to the guests at the time of taking their order. | Bundles and Promotions | CONTRACTED | data `KitchenTicket` |
| 5.2.3 | The system should be able to have options as Fire & forget and Hold & fire orders(modifications should including the manual time adjustment). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |
| 5.2.4 | The system should be able to have options as phased, timed, delayed ordering (used in fine dine options). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |

#### Client meeting inputs

None names this screen.

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-006` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3f`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3f`
- Flow F88 *An order is assembled, collected and notified*, step 1: Expeditor & Order Assembly. → **Drawn by the client as FNB-3F.** 3 operations on this step.
- Flow F88 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump, Save kitchen ticket status, Chase station, Mark order collected, Print order label.
- [ ] Every transition is wired: `KIT-001`, `KIT-002`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-007` Guest Collection, Buzzer & Digital Notification

**Guest Collection, Buzzer & Digital Notification — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18159 (APP-POS-KIT-007) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read) |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `orderId` (KIT-002) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/guest-collection-buzzer-digital-notification` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **`buzzerCode` exists and nothing dispatches to a physical pager.** The digital half works; the buzzer half assumes a device driver the package does not model. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3g` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **The customer-facing order status board is this screen's** (decided 1 October 2026, POS v2 decision POSV2-7, docs/registers/pos-v2-decisions.md): the board the guests read, order numbers only under Preparing and Ready for pickup, never a name. The till's Order Queue (POS-029) shows a mirror of it, not a board of its own.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |
| Status | select | optional | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | Sends `?status=` to `listKitchenTickets`. | `listKitchenTickets` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |

**Form: Record order handover** (modal, opened by *Record order handover*; *Record order handover* calls `recordOrderHandover`, *Cancel* sends nothing)

**Collects what `recordOrderHandover` sends before it is called.** Required: `outcome`, `recordedAt`. Optional: `deliveredToLocationId`, `runnerPrincipalId`, `note`. **Only the outcome that fits the order's service mode is offered**: tableService `served`; quickService or collection `collected`; delivery or roomService `delivered`, with `deliveredToLocationId` required. `guestNotFound` and `refused` are offered for every mode. Any other pairing is refused 422 `outcomeNotForServiceMode` (decided 28 September, audit R125 (1)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Served · Collected · Delivered · Guest not found · Refused | — | `served`, `collected` and `delivered` move the order to the `FnbOrderStatus` of the same name. | `recordOrderHandover` body |
| Delivered to location `deliveredToLocationId` | picker: choose a delivered to location | optional | — | — | shows names, sends the id | Required where `outcome` is `delivered` (audit R125 (1)). | `recordOrderHandover` body |
| Runner principal `runnerPrincipalId` | picker: choose a runner principal | optional | — | — | shows names, sends the id | — | `recordOrderHandover` body |
| Note `note` | text area | optional | — | max length 500 | — | Required for guestNotFound and refused. | `recordOrderHandover` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordOrderHandover` body |

Errors to draw in the form: 409 Order is not ready, or already closed; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)).

#### Outputs: what the screen shows and produces

**Shown**

**Every kitchen ticket** (data table, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Guest status board — Preparing and Ready for pickup** (card list, from `listKitchenTickets`): **Order numbers only, never a name**, in two columns, Preparing and Ready for pickup, readable from across the room. **Owned here** (decided 1 October 2026, POSV2-7); the till's Order Queue (POS-029) mirrors it. The look is the v2 build's queue status board.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |
| Lines | list or chips (count when long) | — |
| Line | the name it points at, never the id | — |
| Name | text | — |
| Quantity | 1,234 | — |
| Modifiers | list or chips (count when long) | — |
| Note | text | — |
| Allergens | list or chips (count when long) | — |

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**The selected kitchen ticket** (detail panel, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | The F&B order the ticket was created from on acceptance (`FnbOrder.id`). |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritised by principal | the name it points at, never the id | — |
| Prioritise reason | text | — |
| Lines | list or chips (count when long) | — |
| Target ready at | 1 Oct 2026, 14:30 | — |
| Elapsed seconds | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bump (primary button) | navigation or local | — | — | — | — |
| Record order handover (primary button) | `recordOrderHandover` POST `/guest-orders/{orderId}/delivery` | inline | GuestOrderStatus | 409 Order is not ready, or already closed; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)). | works offline; gated `ORDER_MODIFY`; opens modal first |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Order is not ready, or already closed; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)). |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `recordOrderHandover` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `ORDER_VIEW`

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 19.2.49 | Pickup Ordering - System shall support pickup ordering. | Guest Mobile App & Branding | CONTRACTED | `recordOrderHandover` |
| 4.7.5 | The system should support usage of buzzers for notifying guests when their order is ready. A buzzer would be assigned to the guests at the time of taking their order. | Bundles and Promotions | CONTRACTED | data `KitchenTicket` |
| 5.2.3 | The system should be able to have options as Fire & forget and Hold & fire orders(modifications should including the manual time adjustment). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |
| 5.2.4 | The system should be able to have options as phased, timed, delayed ordering (used in fine dine options). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Kitchen display lets cashier/kitchen mark orders ready, handed over or delivered, driving the guest-facing order-status board. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-794)*
- Quick-service (QSR) orders capture no pickup details: guest orders, pays, gets a receipt/order number and is notified via a KDS-driven order-status board. Takeaway/delivery do need contact and timing details. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-790)*

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-007` · status **notStarted** · provenance generated · **Drawn as FNB-3G in the client pack.** The pack's frame is the specification for this screen — it carries operations, states, entry params and exits, and it is better specified than anything derived …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3g`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3g`

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (47 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump, Record order handover.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-008` Exceptions, Re-Fire & Unavailable Items

**Exceptions, Re-Fire & Unavailable Items — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18184 (APP-POS-KIT-008) |
| Who uses it | venue staff holding `INCIDENT_REPORT`, `INCIDENT_VIEW`, `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 operate, 3 read, 1 configure); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `list86Events` reads the population and `getHaccpStatus` reads one of them — list, select, act |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `itemId` (KIT-002), `ticketId` (KIT-002), `outletId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/exceptions-re-fire-unavailable-items` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **86 is a kitchen word and a real state.** An item marked unavailable here stops selling at every till in the venue within seconds, which is the only reason to put it on a kitchen screen. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.** **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3h` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3h`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Exceptions, Re-Fire &amp; Unavailable Items* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** **`getHaccpStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `list86Events`. | `list86Events` ?from |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |

**Form: Save item availability** (modal, opened by *Save item availability*; *Save item availability* calls `setItemAvailability`, *Cancel* sends nothing)

**Collects what `setItemAvailability` sends before it is called.** Required: `isAvailable`, `recordedAt`. Optional: `reason`, `note`, `restoreAt`. **When the reason is Other, the note is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is available `isAvailable` | toggle | required | — | — | — | — | `setItemAvailability` body |
| Reason `reason` | radio group | optional | — | Sold out · Ingredient unavailable · Equipment down · Seasonal · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `setItemAvailability` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `setItemAvailability` body |
| Restore at `restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Automatic restore, typically at next service. Kept as `MenuItem.restoreAt`. | `setItemAvailability` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `setItemAvailability` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save kitchen ticket status** (modal, opened by *Save kitchen ticket status*; *Save kitchen ticket status* calls `setKitchenTicketStatus`, *Cancel* sends nothing)

**Collects what `setKitchenTicketStatus` sends before it is called.** Required: `status`, `recordedAt`. Optional: `lineIds`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | — | `setKitchenTicketStatus` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Advance specific lines. Omit for the whole ticket. | `setKitchenTicketStatus` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setKitchenTicketStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setKitchenTicketStatus` body |

Errors to draw in the form: 409 The move is not one of the four above. Names the ticket's current status.

**Form: Log kitchen exception** (modal, opened by *Log kitchen exception*; *Log kitchen exception* calls `logKitchenException`, *Cancel* sends nothing)

**Collects what `logKitchenException` sends before it is called.** Required: `kind`, `outletId`, `recordedAt`. Optional: `stationId`, `ticketId`, `durationMinutes`, `note`. **When the kind is Other, the note is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Equipment down · Item ran out · Late delivery · Staff short · Power loss · Spillage · Other | — | `chased` is not offered here — `chaseStation` records it. `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222); refused `400` without … | `logKitchenException` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | The outlet whose kitchen it happened in. Required because `stationId` may be absent. | `logKitchenException` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `logKitchenException` body |
| Ticket `ticketId` | picker: choose a ticket | optional | — | — | shows names, sends the id | The ticket it happened on, where there was one. | `logKitchenException` body |
| Duration minutes `durationMinutes` | number field (minutes) | optional | — | — | — | — | `logKitchenException` body |
| Note `note` | text area | optional | — | — | — | — | `logKitchenException` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time, not arrival time. Becomes `KitchenException.raisedAt`, so a replay after a dropped network keeps when the fryer actually went down. | `logKitchenException` body |

Errors to draw in the form: 400 Validation failed

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**Every eighty six event** (data table, from `list86Events`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Menu item | the name it points at, never the id | — |
| Off at | 1 Oct 2026, 14:30 | — |
| Back at | 1 Oct 2026, 14:30 | — |
| Reason | chip: Ran out, Quality issue, Equipment down, Supplier failure, Seasonal, Other | `other` always carries a `note` (audit R222). |
| Called by principal | the name it points at, never the id | — |
| Refused order count | 1,234 | — |

**Haccp status** (detail panel, from `getHaccpStatus`): Shows `checksDue`, `checksMissed`, `openActions`, `unsignedActions`, `oldestOpenActionAgeHours`, `lastInspectionAt` from `getHaccpStatus`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Checks due | 1,234 | — |
| Checks missed | 1,234 | — |
| Open actions | 1,234 | — |
| Unsigned actions | 1,234 | — |
| Oldest open action age hours | 1,234 | — |
| Last inspection at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save item availability (primary button) | `setItemAvailability` PUT `/menu-items/{itemId}/availability` | inline | MenuItem | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | works offline; gated `PRODUCT_CONFIGURE`; opens modal first |
| Save kitchen ticket status (secondary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | works offline; gated `ORDER_MODIFY`; opens modal first; produces a document or message: Advance a kitchen ticket |
| Log kitchen exception (secondary button) | `logKitchenException` POST `/kitchen-exceptions` | inline | KitchenException | 400 Validation failed | works offline; gated `INCIDENT_REPORT`; opens modal first |
| Bump (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue, filtered by course (audit R277)); `getHaccpStatus` (onLoad, getHaccpStatus); `list86Events` (onLoad, What came off the menu today, when, and for how long)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one `list86Events`, the population it reads, enforces (`getHaccpStatus` needs `INCIDENT_VIEW` and reaches no component yet, see `gaps`); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The move is not one of the four above. Names the ticket's current status. |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setItemAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `getHaccpStatus` → `INCIDENT_VIEW` (read) · staff
- `list86Events` → `PRODUCT_VIEW` (read) · staff
- `logKitchenException` → `INCIDENT_REPORT` (operate) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one `list86Events`, the population it reads, enforces (`getHaccpStatus` needs `INCIDENT_VIEW` and reaches no component yet, see `gaps`); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.9 | The system should be able to allow the back office to limit the sale of a particular item per day or per timeslot.(example: Happy hour time slot based sales). | Bundles and Promotions | CONTRACTED | `setItemAvailability` |

#### Client meeting inputs

None names this screen.

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-008` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3h`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3h`
- Flow F83 *A kitchen works a service from the rail to the exception*, step 5: Exceptions, Re-Fire & Unavailable Items. → **Drawn by the client as FNB-3H.** 3 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 409, 412).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save item availability, Save kitchen ticket status, Log kitchen exception, Bump.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `INCIDENT_REPORT`, `INCIDENT_VIEW`, `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-009` SLA, Priority & Service Rules

**SLA, Priority & Service Rules — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18160 (APP-POS-KIT-009) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `PRODUCT_CONFIGURE`, `TENANT_CONFIGURE` (1 operate, 2 configure) |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | configEditor (touchLarge density): the screen declares only writes (`prioritiseKitchenTicket`, `setVenueSettings`) and no read of a population — it is settings, not a list |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `outletId` (session), `ticketId` (KIT-002) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/sla-priority-service-rules` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3j` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *SLA, Priority &amp; Service Rules* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Reason | text field | — | — | — | — | Required. | — |
| Priority | number field | — | — | — | — | — | — |

**Form: Save venue settings** (modal, opened by *Save venue settings*; *Save venue settings* calls `setVenueSettings`, *Cancel* sends nothing)

**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `id`, `venueId`, `currencyCode`, `currencyScale`, `supportHours`, `quietHours`, `biometrics`, `segregatedAccess`, `alerting`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettings` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettings` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettings` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettings` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettings` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettings` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettings` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettings` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettings` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettings` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettings` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettings` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettings` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettings` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettings` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettings` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettings` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettings` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettings` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettings` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettings` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettings` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettings` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettings` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettings` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettings` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettings` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettings` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettings` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettings` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| Shift variance threshold `shiftVarianceThreshold` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. | `setVenueSettings` body |
| Catalogue `catalogue` | group | optional | — | — | — | — | `setVenueSettings` body |
| Max variants per product `catalogue.maxVariantsPerProduct` | number field | optional | 200 | min 1; max 2000 | — | Variants one product may generate from its attributes (`setProductAttributes` refuses above it). | `setVenueSettings` body |
| Waitlist offer hold minutes `catalogue.waitlistOfferHoldMinutes` | number field (minutes) | optional | 30 | min 1; max 1440 | — | How long a waitlist offer holds the released capacity for the guest it was offered to. | `setVenueSettings` body |
| Bulk price change escalation percent `catalogue.bulkPriceChangeEscalationPercent` | stepper or slider | optional | 10 | min 0; max 100; A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). | — | A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). | `setVenueSettings` body |
| Bulk price change escalation count `catalogue.bulkPriceChangeEscalationCount` | number field | optional | 50 | min 1; A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). | — | A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). | `setVenueSettings` body |
| … 27 more | | | | | | the rest are in `schemas.json` | `setVenueSettings` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender …

**Sent by *Prioritise kitchen ticket*** (`prioritiseKitchenTicket`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `prioritiseKitchenTicket` body |
| Priority `priority` | stepper or slider | optional | 100 | min 0; max 100 | — | Absent means the top of the queue (decided 28 September, audit R125 (2)): the ticket takes the highest priority on the rail. | `prioritiseKitchenTicket` body |

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Prioritise kitchen ticket (primary button) | `prioritiseKitchenTicket` POST `/kitchen/tickets/{ticketId}/prioritise` | inline | KitchenTicket | — | gated `ORDER_MODIFY`; produces a document or message: Move a ticket up the queue |
| Save venue settings (secondary button) | `setVenueSettings` PUT `/venues/{venueId}/settings` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TENANT_CONFIGURE`; opens modal first |
| Bump (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_MODIFY` gets this state naming `ORDER_MODIFY`**, the screen's `permission` and the one prioritising needs (the screen has no read); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Permissions

- `prioritiseKitchenTicket` → `ORDER_MODIFY` (operate) · staff
- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff
- `setKitchenSla` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_MODIFY` gets this state naming `ORDER_MODIFY`**, the screen's `permission` and the one prioritising needs (the screen has no read); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `ORDER_MODIFY`

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.34 | Support automatic and manual prioritization of kitchen orders based on VIP guests, memberships, Fast Pass, SLA targets, group bookings, events, or supervisor override. | Bundles and Promotions | CONTRACTED | `prioritiseKitchenTicket` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.34 | Expiry Alerts - System shall generate expiry alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 16.4.23 | Device Alerts - System shall generate device alerts. | Device Management | CONTRACTED | data `VenueSettings` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-009` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3j`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3j`

#### Acceptance for the design

- [ ] Every input above is drawn (76), with its required mark, default, format and its error state (400, 403, 404, 412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-009?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Prioritise kitchen ticket, Save venue settings, Bump.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `PRODUCT_CONFIGURE`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-010` Kitchen Performance, AI & Operational Optimization

**Kitchen Performance, AI & Operational Optimization — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18116 (APP-POS-KIT-010) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate) |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | statusTracker (touchLarge density): `getDashboard` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available offline.** `getDashboard` is an analytical read (ADR-0016) and there is nothing local to serve. The rail on KIT-001 is what survives a network loss. **Corrected 24 August**: the earlier wording described the kitchen rather than this screen, and a checker cannot tell those apart from … |
| Opens with | `venueId` (session), `stationId` (session), `dashboardId` (KIT-002) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/kitchen-performance-ai-operational-optimization` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3k` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bump (primary button) | navigation or local | — | — | — | — |
| Ask reporting question (primary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | gated `REPORT_VIEW_VENUE`; opens modal first |

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `REPORT_VIEW_VENUE` gets this state naming `REPORT_VIEW_VENUE`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. |
| Offline (`?state=offline`) | **Not available offline.** `getDashboard` is an analytical read (ADR-0016) and there is nothing local to serve. The rail on KIT-001 is what survives a network loss. **Corrected 24 August**: the earlier wording described the kitchen rather than this screen, and a checker cannot tell those apart from prose. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem) |

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `REPORT_VIEW_VENUE` gets this state naming `REPORT_VIEW_VENUE`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.

Screen guard: `REPORT_VIEW_VENUE`

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |

#### Client meeting inputs

None names this screen.

Also apply: 6 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A52** Design on-seat / location-based F&B delivery: seat-linked QR codes for seated events, and physical location QR codes (e.g., per beach chair/table) for open venues, routing kitchen orders to the scanned location *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'kitchen')*

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-010` · status **notStarted** · provenance generated · **Drawn as FNB-3K in the client pack.** The pack's frame is the specification for this screen — it carries operations, states, entry params and exits, and it is better specified than anything derived …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3k`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3k`
- ADR-0016 *— Read and write paths are separated, and routing is declared per operation* (`docs/adr/0016-read-write-separation.md`)
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (1 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump, Ask reporting question.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P15 as a whole** (2: 0 open, 2 closed). Open first; a closed row says where it went on 30 September.

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker)*

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

### Across P15 Kitchen Display

- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Allam: Softlabs need not build a full kitchen display system, only an integration point that sends order information to an existing KDS for display. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-077)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"chaseStation": {"method":"POST","path":"/kitchen-stations/{stationId}/chase","contract":"fnb","summary":"The pass asks a station where an item is","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"fireCourse": {"method":"POST","path":"/kitchen-tickets/{ticketId}/fire","contract":"fnb","summary":"Send a held course to the pass","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getFnbOrder": {"method":"GET","path":"/fnb-orders/{orderId}","contract":"fnb","summary":"Read an F&B order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"FnbOrder"},
"getHaccpStatus": {"method":"GET","path":"/food-safety/status","contract":"fnb","summary":"Where this venue stands, right now","permission":"INCIDENT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"holdCourse": {"method":"POST","path":"/kitchen-tickets/{ticketId}/hold","contract":"fnb","summary":"Stop a course going out","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"list86Events": {"method":"GET","path":"/outlets/{outletId}/86-events","contract":"fnb","summary":"What came off the menu today, when, and for how long","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFnbOrders": {"method":"GET","path":"/fnb-orders","contract":"fnb","summary":"List F&B orders","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"tableVisitId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listKitchenStations": {"method":"GET","path":"/kitchen/stations","contract":"fnb","summary":"List preparation stations and their routing","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listKitchenTickets": {"method":"GET","path":"/kitchen/tickets","contract":"fnb","summary":"Kitchen ticket queue","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"stationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"course","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"logKitchenException": {"method":"POST","path":"/kitchen-exceptions","contract":"fnb","summary":"Something went wrong that is not a refire","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenException"},
"markOrderCollected": {"method":"POST","path":"/orders/{orderId}/collected","contract":"fnb","summary":"The guest took it","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FnbOrder"},
"notifyServer": {"method":"POST","path":"/table-visits/{visitId}/notify-server","contract":"fnb","summary":"The kitchen calls the server to the pass","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"printOrderLabel": {"method":"POST","path":"/kitchen-tickets/{ticketId}/label","contract":"fnb","summary":"A label for the bag","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderLabel"},
"prioritiseKitchenTicket": {"method":"POST","path":"/kitchen/tickets/{ticketId}/prioritise","contract":"fnb","summary":"Move a ticket up the queue","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"rebalanceStationLoad": {"method":"POST","path":"/kitchen-stations/rebalance","contract":"fnb","summary":"Move work between stations mid-service","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StationRebalance","responds":"StationRebalance"},
"recallKitchenTicket": {"method":"POST","path":"/kitchen-tickets/{ticketId}/recall","contract":"fnb","summary":"Bring back a ticket that was bumped by mistake","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"recordDashboardView": {"method":"POST","path":"/dashboards/{dashboardId}/views","contract":"reporting","summary":"Record that a dashboard was opened","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"recordOrderHandover": {"method":"POST","path":"/guest-orders/{orderId}/delivery","contract":"fnb","summary":"Record that an order reached the guest","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestOrderStatus"},
"refireItem": {"method":"POST","path":"/kitchen-tickets/{ticketId}/refire","contract":"fnb","summary":"Make it again","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"setCourseRules": {"method":"PUT","path":"/outlets/{outletId}/course-rules","contract":"fnb","summary":"How this outlet courses by default","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CourseRules","responds":"CourseRules"},
"setItemAvailability": {"method":"PUT","path":"/menu-items/{itemId}/availability","contract":"fnb","summary":"Mark an item available or eighty-sixed","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"setKitchenSla": {"method":"PUT","path":"/outlets/{outletId}/kitchen-sla","contract":"fnb","summary":"How long a ticket may sit before it is late","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"KitchenSla","responds":"KitchenSla"},
"setKitchenStations": {"method":"PUT","path":"/kitchen/stations","contract":"fnb","summary":"Configure stations and item routing","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"outletId","in":"query","required":true},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenStation"},
"setKitchenTicketStatus": {"method":"PUT","path":"/kitchen/tickets/{ticketId}/status","contract":"fnb","summary":"Advance a kitchen ticket","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"setVenueSettings": {"method":"PUT","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Set support hours, quiet hours, segregated access and alerting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"CourseRules": {"type":"object","x-ticvai-persistence":"fnb.course_rule","description":"**An outlet's coursing default.** It was written to the resolution cache only, which the service model calls losable without consequence — an outlet's default vanished on a cache flush. One row per outlet.\n","properties":{"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet in the path."},"defaultCoursing":{"$ref":"#/components/schemas/CoursingPolicy"},"courseNames":{"type":"array","items":{"type":"string"}},"autoFireMinutes":{"type":"integer","nullable":true},"serviceModeOverrides":{"type":"object","description":"A different default per service mode.","propertyNames":{"$ref":"#/components/schemas/ServiceMode"},"additionalProperties":{"$ref":"#/components/schemas/CoursingPolicy"}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `outlet` scope."}}},
"CoursingPolicy": {"type":"string","description":"How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n","enum":["fireAndForget","holdAndFire","phased","timed","delayed"]},
"CreateFnbOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently."},"seatNumber":{"type":"integer","nullable":true,"description":"Which cover ordered it. Drives split-by-covers accurately."},"course":{"type":"integer","nullable":true,"description":"Course grouping, so the kitchen fires in sequence."},"redeemEntitlementId":{"type":"string","nullable":true,"x-ticvai-references":"access.entitlement","description":"**A meal combo redeemed at the till or by a scan** (29 September, MOB-4; applied 30 September). The entitlement a bundle's `fnbMenuItem` component issued (promotions `BundleComponent.componentKind: fnbMenuItem`, `menuItemId`, `redeemAtOutletIds`). The line is priced at zero against it, `menuItemId` must be the component's menu item and the outlet one of `redeemAtOutletIds` (or any outlet with the item on a live menu when that list is empty), and the entitlement is marked used in the same step through access `validateAccess` at the outlet. An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is refused the same way if it was used meanwhile."}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"EightySixEvent": {"type":"object","x-ticvai-persistence":"fnb.sold_out_item","description":"Board 5J. **`setItemAvailability` recorded the current state and not the history.** An item 86'd at 7pm on a Saturday is a lost-sales figure and a prep-planning signal, and the package kept only the flag.\n**`refusedOrderCount` is what makes it worth keeping.** *Off for ninety minutes* is a note; *off for ninety minutes and eleven guests asked for it* is a purchasing decision.\n","required":["id","menuItemId","offAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"offAt":{"type":"string","format":"date-time"},"backAt":{"type":"string","format":"date-time","nullable":true},"reason":{"type":"string","enum":["ranOut","qualityIssue","equipmentDown","supplierFailure","seasonal","other"],"description":"`other` always carries a `note` (audit R222)."},"note":{"type":"string","maxLength":500,"nullable":true,"description":"The note given with the 86. Required where the reason is `other` (audit R222)."},"calledByPrincipalId":{"type":"string","format":"uuid"},"refusedOrderCount":{"type":"integer","default":0,"readOnly":true}}},
"FnbOrder": {"x-ticvai-persistence":"fnb.service_order + fnb.service_order_line","type":"object","required":["id","orderNumber","outletId","serviceMode","status","lines","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"lines":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/CreateFnbOrderLine"},{"type":"object","properties":{"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"orders.sales_order","description":"**Retyped 29 September (SD-046)**, and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"},"updatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both offline-sync fields, and no plain updated timestamp.\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"kitchenTicketId":{"type":"string","format":"uuid","nullable":true},"kitchenTickets":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"The kitchen tickets this order created, one per station (SD-046). Returned, not stored here; they are `fnb.kitchen_ticket` rows.","items":{"$ref":"#/components/schemas/KitchenTicket"}},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"GuestOrderStatus": {"type":"object","x-ticvai-persistence":"none — projection over kitchen_ticket","required":["orderId","status","lines"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"isReadyForCollection":{"type":"boolean"},"lines":{"type":"array","description":"Per-line status. A guest waiting on one dish should see which.","items":{"type":"object","properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}}}},
"KitchenException": {"type":"object","x-ticvai-persistence":"fnb.kitchen_exception","description":"Board 3, 24 August. **Something that cost the kitchen a service and left no other trace** — equipment down, an item run out mid-ticket, a late delivery, a station short.\n`refireItem` covers a dish. **This covers the reasons a venue looking at a bad Saturday needs**, and which currently live in somebody's memory.\n","required":["id","kind","raisedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"stationId":{"type":"string","format":"uuid","nullable":true},"ticketId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["equipmentDown","itemRanOut","lateDelivery","staffShort","powerLoss","spillage","chased","other"],"description":"`other` always carries a `note` (audit R222)."},"durationMinutes":{"type":"integer","nullable":true},"raisedAt":{"type":"string","format":"date-time"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}},
"KitchenSla": {"type":"object","description":"**How long a ticket may sit, per service mode, and what pushes it up the rail** (`setKitchenSla`). The priority weights are the ones `listKitchenTickets` orders the rail by.\n","properties":{"targets":{"type":"array","items":{"type":"object","required":["serviceMode","targetMinutes"],"properties":{"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"targetMinutes":{"type":"integer","minimum":1},"warnAtPercent":{"type":"integer","default":80}}}},"priorityWeights":{"type":"object","description":"The weight of each signal the board names — age, promise time, table stage, a VIP marker.","properties":{"age":{"type":"integer","minimum":0},"targetReadyAt":{"type":"integer","minimum":0,"description":"Promise time."},"tableStage":{"type":"integer","minimum":0},"vip":{"type":"integer","minimum":0}}}}},
"KitchenStation": {"x-ticvai-persistence":"fnb.kitchen_station","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"menuItemIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Items routed to this station."},"displayWorkstationIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**The kitchen displays assigned to this station** (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks after it. Set with `setKitchenStations`. A display reads the rail for the station it is assigned to (`listKitchenTickets`). A workstation is assigned to at most one station; a second assignment is refused `400`.\n"},"displayEndpoint":{"type":"string","nullable":true,"description":"The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station, with a fallback device where the primary is down — 18 Aug minute). Absent where the station has no display assigned.\n"},"isActive":{"type":"boolean"}}},
"KitchenTicket": {"x-ticvai-persistence":"fnb.kitchen_ticket + fnb.kitchen_ticket_line","type":"object","required":["id","orderId","outletId","status","lines","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"coursing":{"allOf":[{"$ref":"#/components/schemas/CoursingPolicy"}],"nullable":true,"description":"BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"},"buzzerCode":{"type":"string","nullable":true,"description":"BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"},"priority":{"type":"integer","description":"Higher fires sooner. Raised by Fast Pass or supervisor override."},"prioritisedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"prioritiseReason":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","status"],"properties":{"lineId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"refireOfLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."},"refireReason":{"allOf":[{"$ref":"#/components/schemas/RefireReason"}],"nullable":true,"readOnly":true},"isChargeable":{"type":"boolean","nullable":true,"readOnly":true,"description":"A refire's `chargeable` flag. Null on a line that is not a refire."},"course":{"type":"integer","nullable":true},"stationId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}},"createdAt":{"type":"string","format":"date-time"},"targetReadyAt":{"type":"string","format":"date-time","nullable":true},"elapsedSeconds":{"type":"integer"}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"OrderLabel": {"type":"object","x-ticvai-persistence":"none — rendered from the kitchen ticket and its order","description":"**What goes on the bag** (`printOrderLabel`). Order number, guest name, items and **the allergen flags, which are the reason the label is rendered by the server** from the same source as the order rather than printed from whatever the client has.\n","required":["ticketId","orderNumber","lines","allergens"],"properties":{"ticketId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"guestName":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"deliveryLabel":{"type":"string","nullable":true,"description":"Where it is going, as a runner would read it."},"buzzerCode":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["name","quantity"],"properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"allergens":{"type":"array","description":"Every allergen on the order, together. Present and possibly empty — never omitted.","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RefireReason": {"type":"string","description":"Why a line was made again (`refireItem`). The reasons are the data.","enum":["overcooked","undercooked","wrongItem","dropped","cold","allergyRisk","guestChangedMind","lateAdd"]},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"ServiceMode": {"type":"string","enum":["quickService","tableService","roomService","collection","delivery"]},
"StationRebalance": {"type":"object","description":"**A temporary move of work between stations** (`rebalanceStationLoad`). Reverts at `revertAt`, or at close where that is null — a permanent change is `setKitchenStations`.\n","required":["moves"],"properties":{"moves":{"type":"array","items":{"type":"object","required":["fromStationId","toStationId"],"properties":{"fromStationId":{"type":"string","format":"uuid"},"toStationId":{"type":"string","format":"uuid"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"revertAt":{"type":"string","format":"date-time","nullable":true}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}}
}
```
