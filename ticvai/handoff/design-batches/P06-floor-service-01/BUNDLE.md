# P06-floor-service-01 — P06 · Floor Service

**10 screens · 38 operations · 43 schemas · 6 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **22 of these operations work offline**: addGuestNote, compItem, createFnbOrder, createPayment, fireCourse, getBill, getTableMap, getTableVisit
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
| `EMP-051` | Restaurant Service Command Center | B–D | 3 | 41 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `EMP-052` | Floor Plan & Table Map | B–D | 11 | 3 | 5 | 2 | 6 | 1 | — | notStarted (generated) |
| `EMP-053` | Table & Seating Configuration | B–D | 17 | 0 | 5 | 1 | 1 | 6 | — | notStarted (generated) |
| `EMP-054` | Reservation Calendar & Timeline | B–D | 3 | 46 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-055` | Create / Edit Reservation | B–D | 32 | 0 | 5 | 4 | 2 | 0 | — | notStarted (generated) |
| `EMP-056` | Walk-In & Waitlist Management | B–D | 21 | 0 | 5 | 7 | 1 | 0 | — | notStarted (generated) |
| `EMP-057` | Guest Profile & Dining History | B–D | 13 | 33 | 6 | 8 | 2 | 0 | — | notStarted (generated) |
| `EMP-058` | Live Table & Service Management | B–D | 74 | 15 | 5 | 17 | 4 | 1 | — | notStarted (generated) |
| `EMP-059` | Table Order, Bill & Payment Management | B–D | 51 | 8 | 5 | 16 | 2 | 1 | — | notStarted (generated) |
| `EMP-060` | Reservation & Table Performance | B–D | 3 | 29 | 6 | 1 | 0 | 1 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-051` Restaurant Service Command Center

**Restaurant Service Command Center — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listTableReservations` reads the population and `getTableMap` reads one of them — list, select, act |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/restaurant-service-command-center` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4a`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Restaurant Service Command Center* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listTableReservations`. | `listTableReservations` ?outletId |
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listTableReservations`. | `listTableReservations` ?date |
| Search restaurant service command center | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listFnbOrders` ?outletId |
| Table visit | picker: choose a table visit | — | — | `listFnbOrders` ?tableVisitId |
| Status | select | — | Ordered · Accepted · In preparation · Ready · Served · Collected · Delivered · Cancelled · Refunded | `listFnbOrders` ?status |

#### Outputs: what the screen shows and produces

**Shown**

**Every table reservation** (data table, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Guest name | text | — |
| Contact point | text | — |
| Party size | 1,234 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Table | the name it points at, never the id | — |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |
| Group | the name it points at, never the id | 5.1.2. Several bookings managed as one party across adjacent tables. |
| Notes | text | Allergies |

**Every F&B order** (data table, from `listFnbOrders`)

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

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The selected table reservation** (detail panel, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Guest name | text | — |
| Contact point | text | — |
| Party size | 1,234 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Tables | list or chips (count when long) | The dining tables assigned to this reservation, one row each. Usually empty until seating. |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |
| Group | the name it points at, never the id | 5.1.2. Several bookings managed as one party across adjacent tables. |
| Notes | text | Allergies |
| Actual party size | 1,234 | — |
| Table visit | the name it points at, never the id | — |

**The table map** (detail panel, from `getTableMap`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Zones | list or chips (count when long) | — |
| Tables | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getTableMap` (onLoad, Table map with live state); `listTableReservations` (onLoad, Bookings for a service period); `listFnbOrders` (onLoad, List F&B orders)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The restaurant service list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the restaurant service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No restaurant service yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, date and the restaurant service are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |

#### Permissions

- `getTableMap` → `ORDER_VIEW` (read) · staff
- `listTableReservations` → `ORDER_MODIFY` (operate) · staff
- `listFnbOrders` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.1 | The system should be able to allow table reservations view for the available tables in real-time, for the guests to choose/request. | F&B & Guest Management | CONTRACTED | `getTableMap` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-051` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4a`

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-052` Floor Plan & Table Map

**Floor Plan & Table Map — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getTableMap` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/floor-plan-table-map` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Floor Plan &amp; Table Map* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search floor plan | search field | — | — | — | — | — | — |

**Form: Save table layout** (modal, opened by *Save table layout*; *Save table layout* calls `setTableLayout`, *Cancel* sends nothing)

**Collects what `setTableLayout` sends before it is called.** Required: `tables`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tables `tables` | repeatable rows | required | — | — | — | — | `setTableLayout` body |
| ID `tables[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setTableLayout` body |
| Label `tables[].label` | text field | required | — | max length 32 | — | The table code, unique per venue (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is … | `setTableLayout` body |
| Capacity `tables[].capacity` | number field | required | — | min 1 | — | — | `setTableLayout` body |
| Zone `tables[].zone` | text field | optional | — | — | — | — | `setTableLayout` body |
| Position `tables[].position` | group | optional | — | — | — | — | `setTableLayout` body |
| X `tables[].position.x` | number field | optional | — | — | — | — | `setTableLayout` body |
| Y `tables[].position.y` | number field | optional | — | — | — | — | `setTableLayout` body |
| Shape `tables[].shape` | radio group | optional | — | Round · Square · Rectangle · Booth · Bar | — | — | `setTableLayout` body |
| Is out of service `tables[].isOutOfService` | toggle | optional | off | `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | — | Damaged, or its section closed. `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | `setTableLayout` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

#### Outputs: what the screen shows and produces

**Shown**

**The table map** (detail panel, from `getTableMap`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Zones | list or chips (count when long) | — |
| Tables | list or chips (count when long) | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Save table layout (primary button) | `setTableLayout` PUT `/outlets/{outletId}/tables` | inline | TableMap | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `getTableMap` (onLoad, Table map with live state)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The floor plan table, read by `getTableMap`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the floor plan table untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No floor plan table yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |

#### Permissions

- `getTableMap` → `ORDER_VIEW` (read) · staff
- `setTableLayout` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.1 | The system should be able to allow table reservations view for the available tables in real-time, for the guests to choose/request. | F&B & Guest Management | CONTRACTED | `getTableMap` |
| 4.9.6 | The system should be able to create, modify, delete a restaurant floor plan. | Bundles and Promotions | CONTRACTED | `setTableLayout` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*
- Tables are colour-coded by status (vacant, occupied, reserved) and filterable by status. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-792)*
- Qossai asked if guests pick a specific table; Allam: table choice can be an option, but the default is the guest gives party size and the system/host allocates a table. *(agreed · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-689)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Allam: replace the dated table layout with a modern, graphical table map where two-seat and four-seat tables look visually distinct; the cashier selects a table then enters the number of covers. *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-104)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-052` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4b`

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 412).
- [ ] Every output is drawn (3 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-052?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Save table layout.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-053` Table & Seating Configuration

**Table & Seating Configuration — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`setTableLayout`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (EMP-003), `tableId` (navigation) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/table-seating-configuration` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4c`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Table &amp; Seating Configuration* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `TableDefinition.id` |
| label | text field | optional | — | max length 32 | — | The table code, unique per venue (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. | `TableDefinition.label` |
| capacity | number field | optional | — | min 1 | — | — | `TableDefinition.capacity` |
| zone | text field | optional | — | — | — | — | `TableDefinition.zone` |
| position | group | optional | — | — | — | — | `TableDefinition.position` |
| shape | radio group | optional | — | Round · Square · Rectangle · Booth · Bar | — | — | `TableDefinition.shape` |
| Search table | search field | — | — | — | — | — | — |

**Sent by *Save table layout*** (`setTableLayout`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tables `tables` | repeatable rows | required | — | — | — | — | `setTableLayout` body |
| ID `tables[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setTableLayout` body |
| Label `tables[].label` | text field | required | — | max length 32 | — | The table code, unique per venue (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is … | `setTableLayout` body |
| Capacity `tables[].capacity` | number field | required | — | min 1 | — | — | `setTableLayout` body |
| Zone `tables[].zone` | text field | optional | — | — | — | — | `setTableLayout` body |
| Position `tables[].position` | group | optional | — | — | — | — | `setTableLayout` body |
| X `tables[].position.x` | number field | optional | — | — | — | — | `setTableLayout` body |
| Y `tables[].position.y` | number field | optional | — | — | — | — | `setTableLayout` body |
| Shape `tables[].shape` | radio group | optional | — | Round · Square · Rectangle · Booth · Bar | — | — | `setTableLayout` body |
| Is out of service `tables[].isOutOfService` | toggle | optional | off | `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | — | Damaged, or its section closed. `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | `setTableLayout` body |

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Save table layout (primary button) | `setTableLayout` PUT `/outlets/{outletId}/tables` | inline | TableMap | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved table seating. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the table seating untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No table seating configured. The form opens empty and `setTableLayout` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_CONFIGURE`, which `setTableLayout` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 A visit is open on the table (names the visit), or the new `label` is already used by another table in this venue (`duplicate-code`, audit R108). |

#### Permissions

- `setTableLayout` → `PRODUCT_CONFIGURE` (configure) · staff
- `createTable` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateTable` → `PRODUCT_CONFIGURE` (configure) · staff
- `setSectionLayout` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_CONFIGURE`, which `setTableLayout` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.9.6 | The system should be able to create, modify, delete a restaurant floor plan. | Bundles and Promotions | CONTRACTED | `setTableLayout` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-053` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4c`

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-053?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Save table layout.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-054` Reservation Calendar & Timeline

**Reservation Calendar & Timeline — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listTableReservations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/reservation-calendar-timeline` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Reservation Calendar &amp; Timeline* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listTableReservations`. | `listTableReservations` ?outletId |
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listTableReservations`. | `listTableReservations` ?date |
| Search reservation calendar | search field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `listTableReservations`): Reservations by hour; agenda view on the handheld. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Guest name | text | — |
| Contact point | text | — |
| Party size | 1,234 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Tables | list or chips (count when long) | The dining tables assigned to this reservation, one row each. Usually empty until seating. |
| Reservation | the name it points at, never the id | — |
| Table | the name it points at, never the id | — |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |
| Group | the name it points at, never the id | 5.1.2. Several bookings managed as one party across adjacent tables. |
| Notes | text | Allergies |
| Actual party size | 1,234 | — |
| Table visit | the name it points at, never the id | — |
| Deposit | grouped details | The deposit this booking holds, snapshotted from `orders.DepositPolicy.dining` when it was made (decided 29 September, rev 3 REV3-8b). |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Basis | chip: Fixed per guest, Fixed per table, Percent of minimum spend | — |

**Every table reservation** (data table, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Guest name | text | — |
| Contact point | text | — |
| Party size | 1,234 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Table | the name it points at, never the id | — |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |
| Group | the name it points at, never the id | 5.1.2. Several bookings managed as one party across adjacent tables. |
| Notes | text | Allergies |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The selected table reservation** (detail panel, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Guest name | text | — |
| Contact point | text | — |
| Party size | 1,234 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Table | the name it points at, never the id | — |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |
| Group | the name it points at, never the id | 5.1.2. Several bookings managed as one party across adjacent tables. |
| Notes | text | Allergies |
| Actual party size | 1,234 | — |
| Table visit | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listTableReservations` (onLoad, Bookings for a service period)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation calendar timeline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation calendar timeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation calendar timeline yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, date and the reservation calendar timeline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |

#### Permissions

- `listTableReservations` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-054` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4d`

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_MODIFY`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-055` Create / Edit Reservation

**Create / Edit Reservation — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`createTableReservation`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/create-edit-reservation` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Create / Edit Reservation* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `TableReservation.id` |
| outletId | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `TableReservation.outletId` |
| subjectId | picker: choose a subject (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `TableReservation.subjectId` |
| guestName | text field | optional | — | — | — | — | `TableReservation.guestName` |
| contactPoint | text field | optional | — | — | — | — | `TableReservation.contactPoint` |
| partySize | number field | optional | — | min 1 | — | — | `TableReservation.partySize` |
| startsAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `TableReservation.startsAt` |
| durationMinutes | number field (minutes) | optional | — | An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | — | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | `TableReservation.durationMinutes` |
| tableIds | picker: choose a table (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `TableReservation.tables[].tableId` |
| status | select | optional | — | Awaiting deposit · Booked · Confirmed · Seated · Completed · Cancelled · No show; `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | — | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | `TableReservation.status` |
| groupId | picker: choose a group (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | 5.1.2. Several bookings managed as one party across adjacent tables. | `TableReservation.groupId` |
| notes | text area | optional | — | — | — | Allergies | `TableReservation.notes` |
| actualPartySize | number field | optional | — | — | — | — | `TableReservation.actualPartySize` |
| tableVisitId | picker: choose a table visit (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `TableReservation.tableVisitId` |
| Search create / edit reservation | search field | — | — | — | — | — | — |

**Form: Find matches for guest** (modal, opened by *Find matches for guest*; *Find matches for guest* calls `matchGuest`, *Cancel* sends nothing)

**Collects what `matchGuest` sends before it is called.** Nothing in the body is required. Optional: `name`, `phone`, `email`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | — | — | — | `matchGuest` body |
| Phone `phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `matchGuest` body |
| Email `email` | text field | optional | — | — | — | — | `matchGuest` body |

**Sent by *Create table reservation*** (`createTableReservation`; no form is declared, so these are filled from the screen or collected inline)

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

#### Outputs: what the screen shows and produces

**Shown**

**Possible existing guest** (duplicate match): **Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Possible existing guest** (duplicate match): **Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.

**Possible existing guest** (duplicate match): **Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Create table reservation (primary button) | `createTableReservation` POST `/table-reservations` | TableReservation | TableReservation | 409 No cover available for that party size at that time. The reason names the constraint — a party of eight refused when a party of two would fit … | — |
| Find matches for guest (secondary button) | `matchGuest` POST `/guests/match` | inline | inline | — | opens modal first |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved create edit reservation. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the create edit reservation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No create edit reservation configured. The form opens empty and `createTableReservation` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `GUEST_VIEW`, which `matchGuest` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No cover available for that party size at that time. The reason names the constraint — a party of eight refused when a party of two would fit … |

#### Permissions

- `createTableReservation` → no permission · guest
- `matchGuest` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `GUEST_VIEW`, which `matchGuest` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.9.10 | The system should be able to create,modify and delete new/existing reservations | Bundles and Promotions | CONTRACTED | `createTableReservation` |
| 4.9.13 | The system should be able to allow table reservations in advance according to the requirements. | Bundles and Promotions | CONTRACTED | `createTableReservation` |
| 7.5.1 | Event scheduled services such as table booking or meal delivery can be managed by the system (sales only) | F&B POS | CONTRACTED | `createTableReservation` |
| 13.3.11 | APIs shall support reservation creation, modification, cancellation, waitlists and availability checks. | Developer & API Management | CONTRACTED | `createTableReservation` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The client's FnB Board 4 draws a guest duplicate-match and merge process on reservation create/edit and the guest profile: proposed matches shown as candidates, and the merge confirmed by the user. *(agreed · design-brief-9-september 9 Sep 2026, 2 (f) duplicateMatch · DI-808)*
- Table reservation captures table selection (with system recommendations), customer details, guest count, location/outlet and an optional deposit adjusted against the final bill; walk-in and waitlist management are also supported. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-337)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-055` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4e`

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-055?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create table reservation, Find matches for guest.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-056` Walk-In & Waitlist Management

**Walk-In & Waitlist Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`joinRestaurantWaitlist`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `entryId` (navigation) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/walk-in-waitlist-management` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Walk-In &amp; Waitlist Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `RestaurantWaitlist.id` |
| outletId | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `RestaurantWaitlist.outletId` |
| subjectId | picker: choose a subject (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `RestaurantWaitlist.subjectId` |
| partySize | number field | optional | — | — | — | — | `RestaurantWaitlist.partySize` |
| quotedWaitMinutes | number field (minutes) | optional | — | — | — | — | `RestaurantWaitlist.quotedWaitMinutes` |
| seatingPreference | select | optional | — | Any · Indoor · Outdoor · Bar · Booth · High chair | — | — | `RestaurantWaitlist.seatingPreference` |
| status | select | optional | — | Waiting · Notified · Seated · Walked away · No show · Cancelled | — | — | `RestaurantWaitlist.status` |
| notifiedAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `RestaurantWaitlist.notifiedAt` |
| holdExpiresAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | How long a table waits for somebody who was called. Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a setting rather than a … | `RestaurantWaitlist.holdExpiresAt` |
| Search walk-in | search field | — | — | — | — | — | — |

**Form: Leave waitlist** (confirmDialog, opened by *Leave waitlist*; *Take them off the list* calls `leaveRestaurantWaitlist`, *Keep them* sends nothing)

**Names the party and its place in the list.** `leaveRestaurantWaitlist` ends the entry `cancelled`; a party already called releases its held table at once. Optional: `note`, why the party left (audit R073 (d)).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 300 | — | Why, where the guest or host gave a reason. Optional. | `leaveRestaurantWaitlist` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status.

**Sent by *Join restaurant waitlist*** (`joinRestaurantWaitlist`; no form is declared, so these are filled from the screen or collected inline)

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

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Join restaurant waitlist (primary button) | `joinRestaurantWaitlist` POST `/waitlist` | RestaurantWaitlist | RestaurantWaitlist | — | works offline |
| Leave waitlist (destructive button) | `leaveRestaurantWaitlist` POST `/waitlist/{entryId}/leave` | inline | RestaurantWaitlist | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status. | opens confirmDialog first |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved walk-in waitlist. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the walk-in waitlist untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No walk-in waitlist configured. The form opens empty and `joinRestaurantWaitlist` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_MODIFY`, which `joinRestaurantWaitlist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status. |

#### Permissions

- `joinRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest
- `leaveRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `ORDER_MODIFY`, which `joinRestaurantWaitlist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.9.11 | The system should be able to create,modify, delete a new/old guest to the wait list | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.14 | Allow guests to make reservations via website, mobile app, kiosk, QR code, call center, and third-party reservation channels with real-time availability. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.15 | Prevent overbooking by managing seating capacities, combined tables, reservation duration, occupancy rules, and operating schedules. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.16 | Support no-show tracking, deposits, cancellation policies, penalties, blacklists, and automated guest communications. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.17 | Provide automated waitlist management with SMS, email, WhatsApp, push notification, and mobile app alerts when tables become available. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 5.1.4 | The system should be able to provide a way for central reservations where the guest should be able to place a booking from various touchpoints. The system should provide APIs to facilitate … | F&B & Guest Management | CONTRACTED | data `RestaurantWaitlist` |
| 5.6.13 | Track no-shows and support warnings, restrictions, penalties, and future reservation controls. | F&B & Guest Management | CONTRACTED | data `RestaurantWaitlist` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Table reservation captures table selection (with system recommendations), customer details, guest count, location/outlet and an optional deposit adjusted against the final bill; walk-in and waitlist management are also supported. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-337)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-056` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4f`

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-056?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Join restaurant waitlist, Leave waitlist.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_MODIFY`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-057` Guest Profile & Dining History

**Guest Profile & Dining History — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `ORDER_VIEW` (1 configure, 2 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listOrders` reads the population and `getGuestProfile` reads one of them — list, select, act |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `subjectId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/guest-profile-dining-history` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4g`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Guest Profile &amp; Dining History* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOrders`. | `listOrders` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listOrders`. | `listOrders` ?principalId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listOrders`. | `listOrders` ?shiftId |
| Status | select | optional | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | — | Sends `?status=` to `listOrders`. | `listOrders` ?status |
| Created from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdFrom=` to `listOrders`. | `listOrders` ?createdFrom |
| Created to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdTo=` to `listOrders`. | `listOrders` ?createdTo |
| Search guest profile | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

**Form: Find matches for guest** (modal, opened by *Find matches for guest*; *Find matches for guest* calls `matchGuest`, *Cancel* sends nothing)

**Collects what `matchGuest` sends before it is called.** Nothing in the body is required. Optional: `name`, `phone`, `email`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | — | — | — | `matchGuest` body |
| Phone `phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `matchGuest` body |
| Email `email` | text field | optional | — | — | — | — | `matchGuest` body |

**Sent by *Merge guests*** (`mergeGuests`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Keep subject `keepSubjectId` | picker: choose a keep subject | required | — | — | shows names, sends the id | — | `mergeGuests` body |
| Merge subjects `mergeSubjectIds` | multi-picker: choose merge subjects | required | — | — | — | — | `mergeGuests` body |
| Reason `reason` | text area | optional | — | — | — | — | `mergeGuests` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Possible duplicates of this guest** (duplicate match): Candidates from `matchGuest`, each with the rule that matched it.

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Possible duplicates of this guest** (duplicate match): Candidates from `matchGuest`, each with the rule that matched it.

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**Possible duplicates of this guest** (duplicate match): Candidates from `matchGuest`, each with the rule that matched it.

**The guest profile** (detail panel, from `getGuestProfile`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger. |
| Display name | text | — |
| Email | text | — |
| Phone | +971 50 123 4567 | — |
| Preferred language | text | — |
| Preferred channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Guest link | text | Present where the guest is linked across cells. Marketing acts locally. |
| Tags | list or chips (count when long) | — |
| Engagement score | 1,234 | 22.2.20 and 22.2.21. `lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not. |
| Engagement tier | chip: New, Active, Occasional, Lapsing, Lapsed, Dormant | 5.3.19. Automatic classification, computed rather than assigned. |
| Lifetime value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Visit count | 1,234 | — |
| Last visit at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Merged into subject | the name it points at, never the id | Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`, which retain it as a redirect rather than deleting it. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Merge these two records (confirm dialog) | navigation or local | — | — | — | — |
| Confirm (primary button) | navigation or local | — | — | — | — |
| Merge these two records (confirm dialog) | navigation or local | — | — | — | — |
| Merge these two records (confirm dialog) | navigation or local | — | — | — | — |
| Find matches for guest (primary button) | `matchGuest` POST `/guests/match` | inline | inline | — | opens modal first |
| Merge guests (destructive button) | `mergeGuests` POST `/guests/merge` | inline | MergeResult[] | 409 A record in `mergeSubjectIds` is already merged (`alreadyMerged`), or `keepSubjectId` is among them (`sameProfile`) (MergeRefusedProblem) | — |

**Data it reads**: `getGuestProfile` (onLoad, Read a guest profile); `listOrders` (onLoad, List orders)

**What opens over it**

- confirmDialog *Merge guests*: **Names what `mergeGuests` changes and what it leaves alone**, in the consequence rather than the verb. A guest profile dining this affects should be identified in the dialog, not just counted. **Collects what `mergeGuests` sends before it is called.** Required: `keepSubjectId`, `mergeSubjectIds`. …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest profile dining list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest profile dining untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest profile dining yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the guest profile dining are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `GUEST_VIEW`, which `getGuestProfile` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A record in `mergeSubjectIds` is already merged (`alreadyMerged`), or `keepSubjectId` is among them (`sameProfile`) (MergeRefusedProblem) |

#### Permissions

- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `matchGuest` → `GUEST_VIEW` (read) · staff
- `mergeGuests` → `GUEST_MANAGE` (configure) · staff
- `addGuestNote` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `GUEST_VIEW`, which `getGuestProfile` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The client's FnB Board 4 draws a guest duplicate-match and merge process on reservation create/edit and the guest profile: proposed matches shown as candidates, and the merge confirmed by the user. *(agreed · design-brief-9-september 9 Sep 2026, 2 (f) duplicateMatch · DI-808)*
- Decision: one unified customer profile across ticketing, F&B and retail gives a 360° view of guest activity and avoids duplicates; e.g. a guest who buys tickets online and later dines is matched by name/mobile to the same profile. *(agreed · MoM 18 Aug 2026, 4.9 Unified Customer Profile · DI-339)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-057` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4g`

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-057?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Merge these two records, Confirm, Merge these two records, Merge these two records, Find matches for guest, Merge guests.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-058` Live Table & Service Management

**Live Table & Service Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE` (2 operate, 1 read, 1 configure); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`openTableVisit`, `updateTableVisit`, `mergeTableVisits`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `visitId` (EMP-003), `reservationId` (deepLink), `entryId` (deepLink), `outletId` (session), `ticketId` (deepLink) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. A booking opened from the timeline. **The … |
| Route | `/operations/live-table-service-management` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Cross-platform navigation removed 24 August**: KIT-002. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `OpenTableVisitRequest.id` |
| tableId | picker: choose a table (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `OpenTableVisitRequest.tableId` |
| covers | number field | optional | — | min 1 | — | Captured at seating because it drives split-by-covers at close. | `OpenTableVisitRequest.covers` |
| serverPrincipalId | picker: choose a server principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `OpenTableVisitRequest.serverPrincipalId` |
| subjectId | picker: choose a subject (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `OpenTableVisitRequest.subjectId` |
| recordedAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `OpenTableVisitRequest.recordedAt` |
| Search live table | search field | — | — | — | — | — | — |

**Form: Save table visit** (modal, opened by *Save table visit*; *Save table visit* calls `updateTableVisit`, *Cancel* sends nothing)

**Collects what `updateTableVisit` sends before it is called.** Required: `recordedAt`. Optional: `covers`, `tableId`, `serverPrincipalId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Covers `covers` | number field | optional | — | min 1 | — | — | `updateTableVisit` body |
| Table `tableId` | picker: choose a table | optional | — | — | shows names, sends the id | — | `updateTableVisit` body |
| Server principal `serverPrincipalId` | picker: choose a server principal | optional | — | — | shows names, sends the id | — | `updateTableVisit` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `updateTableVisit` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `updateTableVisit` body |

Errors to draw in the form: 409 Target table is occupied.

**Form: Transfer table visit** (modal, opened by *Transfer table visit*; *Transfer table visit* calls `transferTableVisit`, *Cancel* sends nothing)

**Collects what `transferTableVisit` sends before it is called.** Required: `toPrincipalId`, `reason`, `recordedAt`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `transferTableVisit` body |
| Reason `reason` | radio group | required | — | Shift change · Break · Section change · Escalation · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `transferTableVisit` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `transferTableVisit` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `transferTableVisit` body |

Errors to draw in the form: 400 Validation failed

**Form: Seat table reservation** (modal, opened by *Seat table reservation*; *Seat table reservation* calls `seatTableReservation`, *Cancel* sends nothing)

**Collects what `seatTableReservation` sends before it is called.** Required: `tableIds`, `recordedAt`. Optional: `actualPartySize`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tables `tableIds` | multi-picker: choose tables | required | — | at least 1 | — | — | `seatTableReservation` body |
| Actual party size `actualPartySize` | number field | optional | — | — | — | — | `seatTableReservation` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `seatTableReservation` body |

Errors to draw in the form: 409 The booking is not in a seatable state. Names its current status.

**Form: Save service stage** (modal, opened by *Save service stage*; *Save service stage* calls `setServiceStage`, *Cancel* sends nothing)

**Collects what `setServiceStage` sends before it is called.** Required: `recordedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `setServiceStage` body |
| Stage `stage` | select | required | — | Seated · Drinks ordered · Food ordered · Starters away · Mains away · Dessert · Coffee · Bill requested · Paying · Cleared | — | — | `setServiceStage` body |

**Form: Move table visit** (modal, opened by *Move table visit*; *Move table visit* calls `moveTableVisit`, *Cancel* sends nothing)

**Collects what `moveTableVisit` sends before it is called.** Required: `toTableId`, `recordedAt`. Optional: `reason`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To table `toTableId` | picker: choose a to table | required | — | — | shows names, sends the id | — | `moveTableVisit` body |
| Reason `reason` | radio group | optional | — | Guest request · Table fault · Party size change · Service recovery · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `moveTableVisit` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `moveTableVisit` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `moveTableVisit` body |

Errors to draw in the form: 400 Validation failed; 409 The target table is occupied. Names the visit occupying it in `occupyingVisitId`, because the next thing the server asks is *by whom*, and `suggestedOperation` …

**Form: Reassign server** (modal, opened by *Reassign server*; *Reassign server* calls `reassignServer`, *Cancel* sends nothing)

**Collects what `reassignServer` sends before it is called.** Required: `recordedAt`, `serverPrincipalId`. Optional: `splitGratuity`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `reassignServer` body |
| Server principal `serverPrincipalId` | picker: choose a server principal | required | — | — | shows names, sends the id | — | `reassignServer` body |
| Split gratuity `splitGratuity` | toggle | optional | on | — | — | — | `reassignServer` body |

**Form: Notify server** (modal, opened by *Notify server*; *Notify server* calls `notifyServer`, *Cancel* sends nothing)

**Collects what `notifyServer` sends before it is called.** Nothing in the body is required. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | radio group | optional | — | Food ready · Guest waiting · Bill requested · Assistance needed · Allergy query | — | — | `notifyServer` body |

**Form: Create F&B order** (modal, opened by *Create F&B order*; *Create F&B order* calls `createFnbOrder`, *Cancel* sends nothing)

**Collects what `createFnbOrder` sends before it is called.** Required: `id`, `outletId`, `serviceMode`, `lines`, `recordedAt`. Optional: `tableVisitId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Service mode `serviceMode` | radio group | required | — | Quick service · Table service · Room service · Collection · Delivery | — | — | `createFnbOrder` body |
| Table visit `tableVisitId` | picker: choose a table visit | optional | — | — | shows names, sends the id | Required for table service. Absent for quick service. | `createFnbOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createFnbOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Menu item `lines[].menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createFnbOrder` body |
| Modifier options `lines[].modifierOptionIds` | multi-picker: choose modifier options | optional | — | — | — | — | `createFnbOrder` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | Free text to the kitchen. Allergy notes belong here and are surfaced prominently. | `createFnbOrder` body |
| Seat number `lines[].seatNumber` | number field | optional | — | — | — | Which cover ordered it. Drives split-by-covers accurately. | `createFnbOrder` body |
| Course `lines[].course` | number field | optional | — | — | — | Course grouping, so the kitchen fires in sequence. | `createFnbOrder` body |
| Redeem entitlement `lines[].redeemEntitlementId` | text field | optional | — | An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is … | — | A meal combo redeemed at the till or by a scan (29 September, MOB-4; applied 30 September). | `createFnbOrder` body |
| Sales order `salesOrderId` | picker: choose a sales order | optional | — | — | shows names, sends the id | The `orders.sales_order` this F&B order fulfils (SD-046, 29 September). A POS sale sends the order it took payment on; the commercial order is the sales order and this is its … | `createFnbOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createFnbOrder` body |

Errors to draw in the form: 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here …

**Form: Fire course** (modal, opened by *Fire course*; *Fire course* calls `fireCourse`, *Cancel* sends nothing)

**Collects what `fireCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `fireAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `fireCourse` body |
| Course `course` | number field | required | — | min 1 | — | — | `fireCourse` body |
| Fire at `fireAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | For `timed` coursing. Absent means now — a server standing at the pass is not scheduling, they are calling it. | `fireCourse` body |

**Form: Hold course** (modal, opened by *Hold course*; *Hold course* calls `holdCourse`, *Cancel* sends nothing)

**Collects what `holdCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `reason`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `holdCourse` body |
| Course `course` | number field | required | — | min 1 | — | — | `holdCourse` body |
| Reason `reason` | radio group | optional | — | Table not ready · Guest request · Kitchen backed up · Awaiting previous · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `holdCourse` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `holdCourse` body |

Errors to draw in the form: 400 Validation failed

**Form: Save table combinations** (modal, opened by *Save table combinations*; *Save table combinations* calls `setTableCombinations`, *Cancel* sends nothing)

**Collects what `setTableCombinations` sends before it is called.** Required: `combinations`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Combinations `combinations` | repeatable rows | required | — | — | — | — | `setTableCombinations` body |
| Tables `combinations[].tableIds` | multi-picker: choose tables | required | — | at least 2 | — | — | `setTableCombinations` body |
| Combined covers `combinations[].combinedCovers` | number field | required | — | min 1 | — | — | `setTableCombinations` body |
| Setup minutes `combinations[].setupMinutes` | number field (minutes) | optional | 5 | — | — | — | `setTableCombinations` body |

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

**Form: Notify waitlist party** (modal, opened by *Notify waitlist party*; *Notify waitlist party* calls `notifyWaitlistParty`, *Cancel* sends nothing)

**Collects what `notifyWaitlistParty` sends before it is called.** Nothing in the body is required. Optional: `channel`, `holdMinutes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channel `channel` | radio group | optional | — | SMS · Whatsapp · Push · Pager · Called in person | — | — | `notifyWaitlistParty` body |
| Hold minutes `holdMinutes` | number field (minutes) | optional | 10 | — | — | — | `notifyWaitlistParty` body |

**Sent by *Open table visit*** (`openTableVisit`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `openTableVisit` body |
| Table `tableId` | picker: choose a table | required | — | — | shows names, sends the id | — | `openTableVisit` body |
| Covers `covers` | number field | required | — | min 1 | — | Captured at seating because it drives split-by-covers at close. | `openTableVisit` body |
| Server principal `serverPrincipalId` | picker: choose a server principal | optional | — | — | shows names, sends the id | — | `openTableVisit` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `openTableVisit` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `openTableVisit` body |

**Sent by *Merge table visits*** (`mergeTableVisits`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source visit `sourceVisitId` | picker: choose a source visit | required | — | — | shows names, sends the id | — | `mergeTableVisits` body |

#### Outputs: what the screen shows and produces

**Shown**

**The table visit** (detail panel, from `getTableVisit`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Table | the name it points at, never the id | — |
| Table label | text | — |
| Outlet | the name it points at, never the id | — |
| Covers | 1,234 | — |
| Status | chip: Open, Bill requested, Settled, Merged, Cancelled | — |
| Server principal | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Orders | list or chips (count when long) | — |
| Merged into visit | the name it points at, never the id | — |
| Merged from visits | list or chips (count when long) | — |
| Running total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Gratuity | AED 1,234.50 | The gratuity taken at `closeTableVisit`. Not the service charge, which is revenue (`FnbServiceChargePolicy`); this is the guest's tip, and … |
| Opened at | 1 Oct 2026, 14:30 | — |
| Closed at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Open table visit (primary button) | `openTableVisit` POST `/table-visits` | OpenTableVisitRequest | TableVisit | 409 Table already occupied. | works offline |
| Save table visit (secondary button) | `updateTableVisit` PATCH `/table-visits/{visitId}` | inline | TableVisit | 409 Target table is occupied. | works offline; opens modal first |
| Merge table visits (destructive button) | `mergeTableVisits` POST `/table-visits/{visitId}/merge` | inline | TableVisit | 409 Either visit is already closed | — |
| Transfer table visit (secondary button) | `transferTableVisit` POST `/table-visits/{visitId}/transfer` | inline | TableVisit | 400 Validation failed | works offline; opens modal first |
| Seat table reservation (secondary button) | `seatTableReservation` POST `/table-reservations/{reservationId}/seat` | inline | TableReservation | 409 The booking is not in a seatable state. Names its current status. | works offline; opens modal first |
| Save service stage (secondary button) | `setServiceStage` PUT `/table-visits/{visitId}/stage` | inline | TableVisit | — | works offline; opens modal first |
| Move table visit (secondary button) | `moveTableVisit` POST `/table-visits/{visitId}/move` | inline | TableVisit | 400 Validation failed; 409 The target table is occupied. Names the visit occupying it in `occupyingVisitId`, because the next thing the server asks is *by whom*, and `suggestedOperation` … | works offline; opens modal first |
| Reassign server (secondary button) | `reassignServer` PUT `/table-visits/{visitId}/server` | inline | TableVisit | — | works offline; opens modal first |
| Notify server (secondary button) | `notifyServer` POST `/table-visits/{visitId}/notify-server` | inline | no body | — | opens modal first |
| Create F&B order (secondary button) | `createFnbOrder` POST `/fnb-orders` | CreateFnbOrderRequest | FnbOrder | 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here … | emits `fnb.kitchenTicketCreated`; works offline; opens modal first |
| Fire course (secondary button) | `fireCourse` POST `/kitchen-tickets/{ticketId}/fire` | inline | KitchenTicket | — | works offline; opens modal first |
| Hold course (secondary button) | `holdCourse` POST `/kitchen-tickets/{ticketId}/hold` | inline | KitchenTicket | 400 Validation failed | works offline; opens modal first |
| Save table combinations (secondary button) | `setTableCombinations` PUT `/outlets/{outletId}/table-combinations` | inline | inline | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Quote wait time (secondary button) | `quoteWaitTime` POST `/waitlist/{entryId}/quote` | — | inline | — | — |
| Join restaurant waitlist (secondary button) | `joinRestaurantWaitlist` POST `/waitlist` | RestaurantWaitlist | RestaurantWaitlist | — | works offline; opens modal first |
| Notify waitlist party (secondary button) | `notifyWaitlistParty` POST `/waitlist/{entryId}/notify` | inline | RestaurantWaitlist | — | opens modal first |

**Where the user goes next**

- → `EMP-059` Table Order, Bill & Payment Management: *Food is ordered with courses*; carries `visitId`
- → `EMP-060` Reservation & Table Performance: *Reservation & Table Performance*; carries `outletId`
- → `KIT-002` Kitchen Display System (KDS): *One main comes back wrong*; carries `ticketId`, `visitId`

**What opens over it**

- confirmDialog *Merge table visits*: **Names what `mergeTableVisits` changes and what it leaves alone**, in the consequence rather than the verb. A live table service this affects should be identified in the dialog, not just counted. **Collects what `mergeTableVisits` sends before it is called.** Required: `sourceVisitId`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved live table service. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live table service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live table service configured. The form opens empty and `openTableVisit` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getTableVisit` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here …; 409 Either visit is already closed; 409 Table already occupied. |

#### Permissions

- `openTableVisit` → `ORDER_CREATE` (operate) · staff
- `updateTableVisit` → `ORDER_MODIFY` (operate) · staff
- `mergeTableVisits` → `ORDER_MODIFY` (operate) · staff
- `transferTableVisit` → `ORDER_MODIFY` (operate) · staff
- `seatTableReservation` → `ORDER_MODIFY` (operate) · staff
- `setServiceStage` → `ORDER_MODIFY` (operate) · staff
- `moveTableVisit` → `ORDER_MODIFY` (operate) · staff
- `reassignServer` → `ORDER_MODIFY` (operate) · staff
- `notifyServer` → `ORDER_MODIFY` (operate) · staff
- `createFnbOrder` → `ORDER_CREATE` (operate) · staff
- `fireCourse` → `ORDER_MODIFY` (operate) · staff
- `holdCourse` → `ORDER_MODIFY` (operate) · staff
- `setTableCombinations` → `PRODUCT_CONFIGURE` (configure) · staff
- `quoteWaitTime` → `ORDER_MODIFY` (operate) · staff
- `joinRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest
- `notifyWaitlistParty` → `ORDER_MODIFY` (operate) · staff
- `getTableVisit` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getTableVisit` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.19 | The system should be able to ensure table number and number of guests can be updated. | Bundles and Promotions | CONTRACTED | `updateTableVisit` |
| 5.1.2 | The system should be able to allow grouping of table reservations for easier order management and billing as per the guest to choice/request. | F&B & Guest Management | CONTRACTED | `mergeTableVisits` |
| 4.6.15 | The system should be able to transfer one/multiple/all checks to a different operator. | Bundles and Promotions | CONTRACTED | `transferTableVisit` |
| 4.9.7 | The system should be able to assign waiters to a table | Bundles and Promotions | CONTRACTED | `transferTableVisit` |
| 4.9.8 | The system should be able to modify waiters assignment to tables | Bundles and Promotions | CONTRACTED | `transferTableVisit` |
| 4.9.9 | The system should be able to delete waiter assignment to a table | Bundles and Promotions | CONTRACTED | `transferTableVisit` |
| 4.6.1 | The system should be able to record a sale to guests from the POS register using menu screens/buttons. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.6.2 | The system should be able to record a sale to guests from the POS register using manual product sale option | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.9.2 | The system should have a notes section to capture special requests that modifiers don't cover, such as bespoke guest requirements. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 10.1.1 | The system should allow send special request comments/directions on the kitchen display/printers for the kitchen preparation guest requests/inputs. | Games & F&B Integration | CONTRACTED | `createFnbOrder` |
| 4.9.11 | The system should be able to create,modify, delete a new/old guest to the wait list | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.14 | Allow guests to make reservations via website, mobile app, kiosk, QR code, call center, and third-party reservation channels with real-time availability. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each table has an activity log (seated, drinks ordered, food ordered, sent to kitchen, course served, etc.) and actions Add Guest, Change Server and Transfer Table. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-338)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-058` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4a`, `FnB Board 4.dc.html#fnb-4b`, `FnB Board 4.dc.html#fnb-4h`
- Flow F29 *A table is seated, coursed and split*, step 1: The host seats the booking against a table. → A visit opens on the table. **The reservation becomes a visit rather than staying a reservation** — a booking that is still a booking while people are sitting at it is a table the system thinks is …
- Flow F29 *A table is seated, coursed and split*, step 2: The server marks them seated and takes drinks. → Stage `seated`, then `drinksOrdered`. **The stage is what makes a turn time real** — a table `seated` fifty minutes and not ordered is a service problem, and open/closed cannot say so.
- Flow F29 *A table is seated, coursed and split*, step 5: Starters cleared. The server judges the table is ready and fires the mains. → **The act this whole flow exists to prove.** `KitchenTicket.coursing` carried the policy until 24 August and nothing fired anything — a venue could configure coursing and never course a table.
- Flow F80 *A table is configured, reserved, seated and billed*, step 2: Live Table & Service Management. → **Drawn by the client as FNB-4B.** 10 operations on this step.
- Flow F94 *A restaurant floor is set up before service*, step 1: Live Table & Service Management. → **Drawn by the client as FNB-4A.**
- Flow F29 branch at step 1 (low): when There is no booking — four people walk in., Enters through the waitlist instead: `joinRestaurantWaitlist`, then `quoteWaitTime`, then `notifyWaitlistParty` when a table frees. **The quote is computed, not typed** — a host guesses low under …
- Flow F29 branch at step 2 (medium): when The party is larger than the table., `setTableCombinations` says which tables push together and to what capacity. **Declared rather than inferred** — a pillar or a step means two adjacent tables do not always combine, and a host knows …
- Flow F29 branch at step 5 (low): when The table has gone quiet and is not ready for mains., `holdCourse`. **A held course keeps its place in the rail** so the kitchen can see how long it has waited — a held course nobody fires becomes a cold course nobody wants.
- Flow F94 branch at step 1 (medium): when A step is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` decides — the journey is shorter, not broken.

#### Acceptance for the design

- [ ] Every input above is drawn (74), with its required mark, default, format and its error state (400, 404, 409, 412).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-058?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Open table visit, Save table visit, Merge table visits, Transfer table visit, Seat table reservation, Save service stage, Move table visit, Reassign server, Notify server, Create F&B order, Fire course, Hold course, Save table combinations, Quote wait time, Join restaurant waitlist, Notify waitlist party.
- [ ] Every transition is wired: `EMP-059`, `EMP-060`, `KIT-002`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-059` Table Order, Bill & Payment Management

**Table Order, Bill & Payment Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW` (2 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getBill` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `visitId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/table-order-bill-payment-management` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search table order, bill | search field | — | — | — | — | — | — |

**Form: Request bill** (modal, opened by *Request bill*; *Request bill* calls `requestBill`, *Cancel* sends nothing)

**Collects what `requestBill` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `requestBill` body |

**Form: Create payment** (modal, opened by *Create payment*; *Create payment* calls `createPayment`, *Cancel* sends nothing)

**Collects what `createPayment` sends before it is called.** Required: `id`, `orderId`, `tender`, `amount`, `recordedAt`. Optional: `tenderCurrency`, `tenderAmount`, `walletAuthorisationId`, `deviceId`. Dismissing sends nothing; the screen behind is unchanged.

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

Errors to draw in the form: 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender other than card … (PaymentProblem)

**Form: Create F&B order** (modal, opened by *Create F&B order*; *Create F&B order* calls `createFnbOrder`, *Cancel* sends nothing)

**Collects what `createFnbOrder` sends before it is called.** Required: `id`, `outletId`, `serviceMode`, `lines`, `recordedAt`. Optional: `tableVisitId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Service mode `serviceMode` | radio group | required | — | Quick service · Table service · Room service · Collection · Delivery | — | — | `createFnbOrder` body |
| Table visit `tableVisitId` | picker: choose a table visit | optional | — | — | shows names, sends the id | Required for table service. Absent for quick service. | `createFnbOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createFnbOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Menu item `lines[].menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createFnbOrder` body |
| Modifier options `lines[].modifierOptionIds` | multi-picker: choose modifier options | optional | — | — | — | — | `createFnbOrder` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | Free text to the kitchen. Allergy notes belong here and are surfaced prominently. | `createFnbOrder` body |
| Seat number `lines[].seatNumber` | number field | optional | — | — | — | Which cover ordered it. Drives split-by-covers accurately. | `createFnbOrder` body |
| Course `lines[].course` | number field | optional | — | — | — | Course grouping, so the kitchen fires in sequence. | `createFnbOrder` body |
| Redeem entitlement `lines[].redeemEntitlementId` | text field | optional | — | An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is … | — | A meal combo redeemed at the till or by a scan (29 September, MOB-4; applied 30 September). | `createFnbOrder` body |
| Sales order `salesOrderId` | picker: choose a sales order | optional | — | — | shows names, sends the id | The `orders.sales_order` this F&B order fulfils (SD-046, 29 September). A POS sale sends the order it took payment on; the commercial order is the sales order and this is its … | `createFnbOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createFnbOrder` body |

Errors to draw in the form: 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here …

**Form: Split bill** (modal, opened by *Split bill*; *Split bill* calls `splitBill`, *Cancel* sends nothing)

**Collects what `splitBill` sends before it is called.** Required: `recordedAt`, `method`. Optional: `parts`, `amounts`, `lineAssignments`, `categoryAssignments`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the split (offline-capable). | `splitBill` body |
| Method `method` | radio group | required | — | By amount · By covers · By category · By line · By seat | — | — | `splitBill` body |
| Parts `parts` | number field | optional | — | min 2 | — | For `byCovers` — defaults to the visit's cover count. | `splitBill` body |
| Amounts `amounts` | repeatable rows | optional | — | — | — | For `byAmount`. Must sum to the bill total. | `splitBill` body |
| Line assignments `lineAssignments` | repeatable rows | optional | — | — | — | For `byLine` or `bySeat`. Every line must be assigned exactly once. | `splitBill` body |
| Line `lineAssignments[].lineId` | text field | required | — | — | — | — | `splitBill` body |
| Part index `lineAssignments[].partIndex` | number field | required | — | min 0 | — | — | `splitBill` body |
| Category assignments `categoryAssignments` | repeatable rows | optional | — | — | — | For `byCategory` — food to one part, beverage to another. | `splitBill` body |
| Category code `categoryAssignments[].categoryCode` | text field | required | — | — | — | — | `splitBill` body |
| Part index `categoryAssignments[].partIndex` | number field | required | — | min 0 | — | — | `splitBill` body |

Errors to draw in the form: 400 Split does not sum to the bill total, or a line is assigned twice.; 409 Visit already settled

**Form: Comp item** (modal, opened by *Comp item*; *Comp item* calls `compItem`, *Cancel* sends nothing)

**Collects what `compItem` sends before it is called.** Required: `orderLineId`, `recordedAt`, `reason`. Optional: `note`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order line `orderLineId` | picker: choose an order line | required | — | — | shows names, sends the id | An order line (`FnbOrder.lines[].id`). | `compItem` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `compItem` body |
| Reason `reason` | select | required | — | Quality issue · Wait · Wrong item · Allergy incident · Goodwill · Staff meal · Wastage · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `compItem` body |
| Note `note` | text area | optional | — | — | — | Free text. Required where the reason is `other` (audit R222). | `compItem` body |

Errors to draw in the form: 400 Validation failed

**Form: Transfer order items** (modal, opened by *Transfer order items*; *Transfer order items* calls `transferOrderItems`, *Cancel* sends nothing)

**Collects what `transferOrderItems` sends before it is called.** Required: `toVisitId`, `lineIds`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To visit `toVisitId` | picker: choose a to visit | required | — | — | shows names, sends the id | — | `transferOrderItems` body |
| Lines `lineIds` | multi-picker: choose lines | required | — | — | — | — | `transferOrderItems` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `transferOrderItems` body |

**Sent by *Close table visit*** (`closeTableVisit`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Payments `payments` | repeatable rows | required | — | at least 1 | — | — | `closeTableVisit` body |
| Sub bill `payments[].subBillId` | text field | required | — | — | — | — | `closeTableVisit` body |
| Tender `payments[].tender` | text field | required | — | — | — | — | `closeTableVisit` body |
| Amount `payments[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeTableVisit` body |
| Gratuity `gratuity` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeTableVisit` body |

#### Outputs: what the screen shows and produces

**Shown**

**The bill** (detail panel, from `getBill`)

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

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Close table visit (destructive button) | `closeTableVisit` POST `/table-visits/{visitId}/close` | inline | inline | 409 Payments do not cover the bill, or lines remain unserved (named in `lineIds`). | — |
| Create payment (secondary button) | `createPayment` POST `/payments` | CreatePaymentRequest | Payment | 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender … | emits `payment.captured`, `order.paid`; works offline; opens modal first |
| Create F&B order (secondary button) | `createFnbOrder` POST `/fnb-orders` | CreateFnbOrderRequest | FnbOrder | 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here … | emits `fnb.kitchenTicketCreated`; works offline; opens modal first |
| Split bill (secondary button) | `splitBill` POST `/table-visits/{visitId}/bill/split` | SplitBillRequest | BillSplit | 400 Split does not sum to the bill total, or a line is assigned twice.; 409 Visit already settled | works offline; opens modal first |
| Comp item (secondary button) | `compItem` POST `/table-visits/{visitId}/comp` | inline | TableVisit | 400 Validation failed | works offline; opens modal first |
| Transfer order items (secondary button) | `transferOrderItems` POST `/table-visits/{visitId}/transfer-items` | inline | TableVisit | — | works offline; opens modal first |
| Request bill (primary button) | `requestBill` POST `/table-visits/{visitId}/request-bill` | inline | TableVisit | — | works offline; opens modal first |

**Data it reads**: `getBill` (onLoad, Bill for a visit)

**Where the user goes next**

- → `EMP-058` Live Table & Service Management: *Live Table & Service Management*; carries `visitId`; calls `transferOrderItems`
- → `KIT-002` Kitchen Display System (KDS): *The kitchen makes the starters and bumps them*; carries `visitId`; calls `createFnbOrder`

**What opens over it**

- confirmDialog *Close table visit*: **Names what `closeTableVisit` changes and what it leaves alone**, in the consequence rather than the verb. A table order bill this affects should be identified in the dialog, not just counted. **Collects what `closeTableVisit` sends before it is called.** Required: `payments`. Optional: `gratuity`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The table order bill, read by `getBill`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the table order bill untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No table order bill yet. Offers Create payment (`createPayment`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getBill` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Split does not sum to the bill total, or a line is assigned twice.; 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here …; 409 Payments do not cover the bill, or lines remain unserved (named in `lineIds`). |

#### Permissions

- `closeTableVisit` → `ORDER_CREATE` (operate) · staff
- `createPayment` → `ORDER_CREATE` (operate) · staff, guest, partner
- `createFnbOrder` → `ORDER_CREATE` (operate) · staff
- `splitBill` → `ORDER_MODIFY` (operate) · staff
- `getBill` → `ORDER_VIEW` (read) · staff
- `compItem` → `ORDER_MODIFY` (operate) · staff
- `transferOrderItems` → `ORDER_MODIFY` (operate) · staff
- `requestBill` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getBill` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.23 | Payment can be done online. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.12.35 | System shall support multiple payment methods within a single transaction including cash, credit card, wallet, loyalty points, vouchers, gift cards, bank transfers, and credit balances. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.13.2 | The operator can register the payment. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.15.3 | The operator can register the payment and print the pass. | Ticketing Sales | CONTRACTED | `createPayment` |
| 4.2.6 | The system should be able to accept several currencies in one transaction (a guest pays in USD and gets the change in AED). | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.7 | The system should be accept multiple payments in one transaction. For example, there must be an option to split the payment within a group of guests | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.13 | The system should be able to support payment of one transaction with multiple payment methods. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.22 | The system shall support mixed payment scenarios using any combination of loyalty points, wallet balances, gift cards, vouchers, cash, and payment cards within the same transaction. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.6.27 | Support mobile payment for F&B and retail orders. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.6.1 | The system should be able to record a sale to guests from the POS register using menu screens/buttons. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.6.2 | The system should be able to record a sale to guests from the POS register using manual product sale option | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.9.2 | The system should have a notes section to capture special requests that modifiers don't cover, such as bespoke guest requirements. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Table/seat-level structure supports flexible bill-splitting: by amount, by number of covers, or by category (e.g. one guest pays food, another drinks). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-106)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-059` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4j`
- Flow F29 *A table is seated, coursed and split*, step 3: Food is ordered with courses. → A kitchen ticket with `coursing` set from the outlet's default. **Starters fire; mains hold.**
- Flow F29 *A table is seated, coursed and split*, step 7: The server comps the delayed dish. → **A comp is not a discount.** Different budget, and a venue that cannot tell them apart cannot tell a generous manager from a leaking till.
- Flow F29 *A table is seated, coursed and split*, step 8: The table asks to split four ways. → Four bills. **Tax and service charge recompute per bill** — a split that apportions VAT by percentage produces bills that do not sum, and the difference is a fils somebody explains.
- Flow F29 *A table is seated, coursed and split*, step 9: Each guest pays their own. → The visit closes. **Stage `cleared` releases the table to the floor plan**, and the waitlist picks it up.
- Flow F80 *A table is configured, reserved, seated and billed*, step 1: Table Order, Bill & Payment Management. → **Drawn by the client as FNB-4J.** 1 operations on this step.
- Flow F29 branch at step 8 (low): when A guest moves from the bar and their drinks should follow., `transferOrderItems` moves lines between bills. **The kitchen is not re-fired** — food already made does not get made again because the bill moved.
- Flow F80 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.

#### Acceptance for the design

- [ ] Every input above is drawn (51), with its required mark, default, format and its error state (400, 402, 404, 409).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-059?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Close table visit, Create payment, Create F&B order, Split bill, Comp item, Transfer order items, Request bill.
- [ ] Every transition is wired: `EMP-058`, `KIT-002`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-060` Reservation & Table Performance

**Reservation & Table Performance — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listTableReservations` reads the population and `getTableMap` reads one of them — list, select, act |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/reservation-table-performance` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listTableReservations`. | `listTableReservations` ?outletId |
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listTableReservations`. | `listTableReservations` ?date |
| Search reservation | search field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every table reservation** (data table, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Guest name | text | — |
| Contact point | text | — |
| Party size | 1,234 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Table | the name it points at, never the id | — |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |
| Group | the name it points at, never the id | 5.1.2. Several bookings managed as one party across adjacent tables. |
| Notes | text | Allergies |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The selected table reservation** (detail panel, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Guest name | text | — |
| Contact point | text | — |
| Party size | 1,234 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Tables | list or chips (count when long) | The dining tables assigned to this reservation, one row each. Usually empty until seating. |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |
| Group | the name it points at, never the id | 5.1.2. Several bookings managed as one party across adjacent tables. |
| Notes | text | Allergies |
| Actual party size | 1,234 | — |
| Table visit | the name it points at, never the id | — |

**The table map** (detail panel, from `getTableMap`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Zones | list or chips (count when long) | — |
| Tables | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listTableReservations` (onLoad, Bookings for a service period); `getTableMap` (onLoad, Table map with live state)

**Where the user goes next**

- → `EMP-061` Retail Inventory Command Center: *Retail Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation table performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation table performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation table performance yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, date and the reservation table performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |

#### Permissions

- `listTableReservations` → `ORDER_MODIFY` (operate) · staff
- `getTableMap` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.1 | The system should be able to allow table reservations view for the available tables in real-time, for the guests to choose/request. | F&B & Guest Management | CONTRACTED | `getTableMap` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-060` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4c`
- Flow F80 *A table is configured, reserved, seated and billed*, step 3: Reservation & Table Performance. → **Drawn by the client as FNB-4C.** 2 operations on this step.
- Flow F94 *A restaurant floor is set up before service*, step 2: Reservation & Table Performance. → **Drawn by the client as FNB-4B.**

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-060?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] Every transition is wired: `EMP-061`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P06 reference designs** (from `handoff/design-batches/apps/4-staff-app/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P06 as a whole** (3: 0 open, 3 closed). Open first; a closed row says where it went on 30 September.

- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A49** Confirm scope: deliver a lightweight standalone ticket-validation app for dedicated scanner devices, in addition to the scan/validate function embedded in the full Staff Operations App *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A71** Design an offline-first, native ticket-scanning/access-control capability (local scan storage with sync-on-reconnect) for both the dedicated scanner app and the scanning function embedded in the Employee App *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 10 Aug 2026 · workshop tracker)*

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**19 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addGuestNote": {"method":"POST","path":"/guests/{subjectId}/notes","contract":"marketing-crm","summary":"What the floor needs to know about this table","permission":"GUEST_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestNote"},
"closeTableVisit": {"method":"POST","path":"/table-visits/{visitId}/close","contract":"fnb","summary":"Settle and close a visit","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"compItem": {"method":"POST","path":"/table-visits/{visitId}/comp","contract":"fnb","summary":"Take a line off the bill, with a reason and a name","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"createFnbOrder": {"method":"POST","path":"/fnb-orders","contract":"fnb","summary":"Place an F&B order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateFnbOrderRequest","responds":"FnbOrder"},
"createPayment": {"method":"POST","path":"/payments","contract":"orders","summary":"Take a payment against an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePaymentRequest","responds":"Payment"},
"createTable": {"method":"POST","path":"/tables","contract":"fnb","summary":"A table as a thing, not an inference","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TableDefinition","responds":"TableDefinition"},
"createTableReservation": {"method":"POST","path":"/table-reservations","contract":"fnb","summary":"Book a table in advance","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TableReservation","responds":"TableReservation"},
"fireCourse": {"method":"POST","path":"/kitchen-tickets/{ticketId}/fire","contract":"fnb","summary":"Send a held course to the pass","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"getBill": {"method":"GET","path":"/table-visits/{visitId}/bill","contract":"fnb","summary":"Bill for a visit","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Bill"},
"getGuestProfile": {"method":"GET","path":"/guests/{subjectId}","contract":"marketing-crm","summary":"Read a guest profile","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestProfileDetail"},
"getTableMap": {"method":"GET","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Table map with live state","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TableMap"},
"getTableVisit": {"method":"GET","path":"/table-visits/{visitId}","contract":"fnb","summary":"Read a visit with all its orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TableVisit"},
"holdCourse": {"method":"POST","path":"/kitchen-tickets/{ticketId}/hold","contract":"fnb","summary":"Stop a course going out","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"joinRestaurantWaitlist": {"method":"POST","path":"/waitlist","contract":"fnb","summary":"Add a party to an outlet's waitlist","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RestaurantWaitlist","responds":"RestaurantWaitlist"},
"leaveRestaurantWaitlist": {"method":"POST","path":"/waitlist/{entryId}/leave","contract":"fnb","summary":"Take a party off an outlet's waitlist","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RestaurantWaitlist"},
"listFnbOrders": {"method":"GET","path":"/fnb-orders","contract":"fnb","summary":"List F&B orders","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"tableVisitId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTableReservations": {"method":"GET","path":"/table-reservations","contract":"fnb","summary":"Bookings for a service period","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"date","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"matchGuest": {"method":"POST","path":"/guests/match","contract":"marketing-crm","summary":"Is this the same person we already have?","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"mergeGuests": {"method":"POST","path":"/guests/merge","contract":"marketing-crm","summary":"Two records, one person","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MergeResult"},
"mergeTableVisits": {"method":"POST","path":"/table-visits/{visitId}/merge","contract":"fnb","summary":"Merge another visit into this one","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"moveTableVisit": {"method":"POST","path":"/table-visits/{visitId}/move","contract":"fnb","summary":"Move a party to a different table, mid-service","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"notifyServer": {"method":"POST","path":"/table-visits/{visitId}/notify-server","contract":"fnb","summary":"The kitchen calls the server to the pass","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"notifyWaitlistParty": {"method":"POST","path":"/waitlist/{entryId}/notify","contract":"fnb","summary":"Their table is ready","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RestaurantWaitlist"},
"openTableVisit": {"method":"POST","path":"/table-visits","contract":"fnb","summary":"Seat a party and open a visit","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OpenTableVisitRequest","responds":"TableVisit"},
"quoteWaitTime": {"method":"POST","path":"/waitlist/{entryId}/quote","contract":"fnb","summary":"Tell a party how long, and mean it","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"reassignServer": {"method":"PUT","path":"/table-visits/{visitId}/server","contract":"fnb","summary":"Hand a table to another server","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"requestBill": {"method":"POST","path":"/table-visits/{visitId}/request-bill","contract":"fnb","summary":"The party asked to pay","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"seatTableReservation": {"method":"POST","path":"/table-reservations/{reservationId}/seat","contract":"fnb","summary":"The party arrived and has been sat down","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableReservation"},
"setSectionLayout": {"method":"PUT","path":"/outlets/{outletId}/sections","contract":"fnb","summary":"Divide the floor into sections and give each a server","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"SectionLayout","responds":"SectionLayout"},
"setServiceStage": {"method":"PUT","path":"/table-visits/{visitId}/stage","contract":"fnb","summary":"Where this table is in its meal","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"setTableCombinations": {"method":"PUT","path":"/outlets/{outletId}/table-combinations","contract":"fnb","summary":"Which tables can be pushed together, and to what capacity","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setTableLayout": {"method":"PUT","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Configure the table layout","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableMap"},
"splitBill": {"method":"POST","path":"/table-visits/{visitId}/bill/split","contract":"fnb","summary":"Split a bill","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SplitBillRequest","responds":"BillSplit"},
"transferOrderItems": {"method":"POST","path":"/table-visits/{visitId}/transfer-items","contract":"fnb","summary":"Move items to another table's bill","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"transferTableVisit": {"method":"POST","path":"/table-visits/{visitId}/transfer","contract":"fnb","summary":"Move a check to another server","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"updateTable": {"method":"PUT","path":"/tables/{tableId}","contract":"fnb","summary":"Change what a table is","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"TableDefinition","responds":"TableDefinition"},
"updateTableVisit": {"method":"PATCH","path":"/table-visits/{visitId}","contract":"fnb","summary":"Amend covers, move table, or reassign server","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"Bill": {"x-ticvai-persistence":"none — computed from visit orders","type":"object","required":["visitId","lines","subtotal","taxAmount","total"],"properties":{"visitId":{"type":"string"},"covers":{"type":"integer"},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","lineTotal"],"properties":{"lineId":{"type":"string"},"orderId":{"type":"string"},"name":{"type":"string"},"quantity":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryCode":{"type":"string","nullable":true},"seatNumber":{"type":"integer","nullable":true}}}},"subtotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"serviceCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"BillSplit": {"x-ticvai-persistence":"fnb.bill_split + fnb.sub_bill","type":"object","required":["visitId","method","subBills"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"visitId":{"type":"string"},"method":{"$ref":"#/components/schemas/SplitMethod"},"subBills":{"type":"array","items":{"type":"object","required":["subBillId","total","status"],"properties":{"subBillId":{"type":"string"},"lineIds":{"type":"array","items":{"type":"string"}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["unpaid","paid"]}}}}}},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"CoursingPolicy": {"type":"string","description":"How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n","enum":["fireAndForget","holdAndFire","phased","timed","delayed"]},
"CreateFnbOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently."},"seatNumber":{"type":"integer","nullable":true,"description":"Which cover ordered it. Drives split-by-covers accurately."},"course":{"type":"integer","nullable":true,"description":"Course grouping, so the kitchen fires in sequence."},"redeemEntitlementId":{"type":"string","nullable":true,"x-ticvai-references":"access.entitlement","description":"**A meal combo redeemed at the till or by a scan** (29 September, MOB-4; applied 30 September). The entitlement a bundle's `fnbMenuItem` component issued (promotions `BundleComponent.componentKind: fnbMenuItem`, `menuItemId`, `redeemAtOutletIds`). The line is priced at zero against it, `menuItemId` must be the component's menu item and the outlet one of `redeemAtOutletIds` (or any outlet with the item on a live menu when that list is empty), and the entitlement is marked used in the same step through access `validateAccess` at the outlet. An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is refused the same way if it was used meanwhile."}}},
"CreateFnbOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","outletId","serviceMode","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true,"description":"Required for table service. Absent for quick service."},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateFnbOrderLine"}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.sales_order` this F&B order fulfils (SD-046, 29 September). A POS sale sends the order it took payment on; the commercial order is the sales order and this is its fulfilment."},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FnbOrder": {"x-ticvai-persistence":"fnb.service_order + fnb.service_order_line","type":"object","required":["id","orderNumber","outletId","serviceMode","status","lines","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"lines":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/CreateFnbOrderLine"},{"type":"object","properties":{"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"orders.sales_order","description":"**Retyped 29 September (SD-046)**, and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"},"updatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both offline-sync fields, and no plain updated timestamp.\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"kitchenTicketId":{"type":"string","format":"uuid","nullable":true},"kitchenTickets":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"The kitchen tickets this order created, one per station (SD-046). Returned, not stored here; they are `fnb.kitchen_ticket` rows.","items":{"$ref":"#/components/schemas/KitchenTicket"}},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"FnbReservationTable": {"type":"object","x-ticvai-persistence":"fnb.reservation_table","description":"**Taken from the backend workbook, 20 September.** Maps one or more dining tables assigned to a reservation.","required":["reservationId","tableId","createdAt"],"properties":{"reservationId":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"GuestNote": {"type":"object","x-ticvai-persistence":"marketing.guest_note","description":"A note on a guest, written by staff (`addGuestNote`). **Attributed and personal data**, and `isAllergy` keeps an allergy apart from every other kind so it surfaces on the order screen.\n","required":["id","subjectId","kind","text","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["allergy","dietary","seatingPreference","occasion","serviceRecovery","vip","general"]},"text":{"type":"string"},"isAllergy":{"type":"boolean","default":false},"visibleToServer":{"type":"boolean","default":true},"authorPrincipalId":{"type":"string","format":"uuid","readOnly":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"GuestProfileDetail": {"x-ticvai-persistence":"marketing.guest_profile","allOf":[{"$ref":"#/components/schemas/GuestProfile"},{"type":"object","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"consents":{"$ref":"#/components/schemas/ConsentState"},"loyalty":{"$ref":"#/components/schemas/LoyaltyPosition"},"openCaseCount":{"type":"integer"},"recentOrderIds":{"type":"array","items":{"type":"string"}},"membershipIds":{"type":"array","items":{"type":"string","format":"uuid"}},"notes":{"type":"string","nullable":true}}}]},
"KitchenTicket": {"x-ticvai-persistence":"fnb.kitchen_ticket + fnb.kitchen_ticket_line","type":"object","required":["id","orderId","outletId","status","lines","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"coursing":{"allOf":[{"$ref":"#/components/schemas/CoursingPolicy"}],"nullable":true,"description":"BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"},"buzzerCode":{"type":"string","nullable":true,"description":"BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"},"priority":{"type":"integer","description":"Higher fires sooner. Raised by Fast Pass or supervisor override."},"prioritisedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"prioritiseReason":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","status"],"properties":{"lineId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"refireOfLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."},"refireReason":{"allOf":[{"$ref":"#/components/schemas/RefireReason"}],"nullable":true,"readOnly":true},"isChargeable":{"type":"boolean","nullable":true,"readOnly":true,"description":"A refire's `chargeable` flag. Null on a line that is not a refire."},"course":{"type":"integer","nullable":true},"stationId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}},"createdAt":{"type":"string","format":"date-time"},"targetReadyAt":{"type":"string","format":"date-time","nullable":true},"elapsedSeconds":{"type":"integer"}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"MergeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["survivingSubjectId","absorbedSubjectId","transferred"],"properties":{"survivingSubjectId":{"type":"string","format":"uuid"},"absorbedSubjectId":{"type":"string","format":"uuid"},"transferred":{"type":"object","properties":{"orders":{"type":"integer"},"cases":{"type":"integer"},"loyaltyPoints":{"type":"integer","description":"The total points moved across every programme. The per-programme outcome is `loyaltyProgrammes`."}}},"loyaltyProgrammes":{"type":"array","description":"**One entry per loyalty programme either record belonged to (decided 28 September, audit R149).** Points are added and the higher tier is kept, per programme — a single points number cannot say which programme it belongs to.\n","items":{"type":"object","required":["programmeId","pointsAdded","resultingPoints"],"properties":{"programmeId":{"type":"string","format":"uuid"},"pointsAdded":{"type":"integer","description":"The absorbed record's balance in this programme, added to the survivor's."},"resultingPoints":{"type":"integer"},"tierKept":{"type":"string","nullable":true,"description":"The higher of the two records' tiers in this programme."}}}},"consentOutcome":{"type":"array","description":"Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n","items":{"type":"object","properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"result":{"$ref":"#/components/schemas/ConsentDecision"},"wasRestricted":{"type":"boolean"}}}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"OpenTableVisitRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","tableId","covers","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"covers":{"type":"integer","minimum":1,"description":"Captured at seating because it drives split-by-covers at close."},"serverPrincipalId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"RefireReason": {"type":"string","description":"Why a line was made again (`refireItem`). The reasons are the data.","enum":["overcooked","undercooked","wrongItem","dropped","cold","allergyRisk","guestChangedMind","lateAdd"]},
"RestaurantWaitlist": {"type":"object","x-ticvai-persistence":"fnb.waitlist_entry","description":"BL-130. **Distinct from `queue`, which is for rides.** A restaurant waitlist has a party size, a table preference and a walk-away point, and a guest who leaves is not the same as a guest who was served.\n","required":["id","outletId","partySize","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partySize":{"type":"integer"},"quotedWaitMinutes":{"type":"integer","nullable":true},"seatingPreference":{"type":"string","enum":["any","indoor","outdoor","bar","booth","highChair"],"nullable":true},"status":{"type":"string","enum":["waiting","notified","seated","walkedAway","noShow","cancelled"]},"notifiedAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time","description":"**When the party joined, on the device.** The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. Required on a join — the operation is offline-capable."},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**How long a table waits for somebody who was called.** Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a setting rather than a constant.\n"}}},
"SectionLayout": {"type":"object","description":"An outlet's floor divided into sections, each with its server (`setSectionLayout`).","required":["sections"],"properties":{"sections":{"type":"array","items":{"type":"object","required":["name","tableIds"],"properties":{"name":{"type":"string"},"tableIds":{"type":"array","items":{"type":"string","format":"uuid"}},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"servicePeriod":{"type":"string","nullable":true}}}}}},
"ServiceMode": {"type":"string","enum":["quickService","tableService","roomService","collection","delivery"]},
"SplitBillRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["method","recordedAt"],"properties":{"recordedAt":{"type":"string","format":"date-time","description":"Device time of the split (offline-capable)."},"method":{"$ref":"#/components/schemas/SplitMethod"},"parts":{"type":"integer","minimum":2,"description":"For `byCovers` — defaults to the visit's cover count."},"amounts":{"type":"array","description":"For `byAmount`. Must sum to the bill total.","items":{"$ref":"../shared/common.yaml#/components/schemas/Money"}},"lineAssignments":{"type":"array","description":"For `byLine` or `bySeat`. Every line must be assigned exactly once.","items":{"type":"object","required":["lineId","partIndex"],"properties":{"lineId":{"type":"string"},"partIndex":{"type":"integer","minimum":0}}}},"categoryAssignments":{"type":"array","description":"For `byCategory` — food to one part, beverage to another.","items":{"type":"object","required":["categoryCode","partIndex"],"properties":{"categoryCode":{"type":"string"},"partIndex":{"type":"integer","minimum":0}}}}}},
"SplitMethod": {"type":"string","enum":["byAmount","byCovers","byCategory","byLine","bySeat"]},
"TableCombination": {"type":"object","x-ticvai-persistence":"fnb.table_combination","description":"**Tables that can be pushed together, and what they seat together.** Declared by a host rather than inferred from a floor plan — a pillar, a step or a service run stops two adjacent tables combining. `setTableCombinations` writes the outlet's set.\n","required":["tableIds","combinedCovers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet in the path."},"tableIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"combinedCovers":{"type":"integer","minimum":1},"setupMinutes":{"type":"integer","default":5},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `outlet` scope."}}},
"TableDefinition": {"x-ticvai-persistence":"fnb.dining_table","type":"object","description":"A restaurant (dining) table, reserved with `createTableReservation`. Not a map-bookable `resources` table, which is a non-dining spot sold like a cabana (decided 29 September, rev 3 GAP-C2).","required":["id","label","capacity"],"properties":{"id":{"type":"string","format":"uuid"},"label":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"**The table code, unique per venue** (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. `createTable` and `updateTable` refuse a duplicate with `409` `duplicate-code`.\n"},"capacity":{"type":"integer","minimum":1},"zone":{"type":"string","nullable":true},"position":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"shape":{"type":"string","enum":["round","square","rectangle","booth","bar"]},"isOutOfService":{"type":"boolean","default":false,"description":"**Damaged, or its section closed.** `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`."}}},
"TableMap": {"x-ticvai-persistence":"none — projection","type":"object","required":["outletId","tables"],"properties":{"outletId":{"type":"string","format":"uuid"},"zones":{"type":"array","items":{"type":"string"}},"tables":{"type":"array","items":{"$ref":"#/components/schemas/TableState"}}}},
"TableReservation": {"type":"object","x-ticvai-persistence":"fnb.table_reservation","x-ticvai-retired-columns":["table_ids"],"required":["outletId","startsAt","partySize"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string"},"contactPoint":{"type":"string"},"partySize":{"type":"integer","minimum":1},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer","description":"**How long the cover is held.** An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked.\n"},"tables":{"type":"array","description":"The dining tables assigned to this reservation, one row each.\n**Usually empty until seating.** Committing a specific table at booking time refuses later bookings against a constraint that did not need to exist — that was true of the `tableIds` array this replaces and it is still true, because it is about *when* a table is assigned rather than how the assignment is stored.\n**Replaces `tableIds`, retired 20 September.** An array cannot carry per-row state, which is the same reason this merge took `entry_rule_point`, `menu_item_modifier`, `seat_block_item`, `plan_benefit`, `payment_method_config` and `tier_module` from the backend workbook. A party seated across three tables that releases one early has nowhere to say so in an array, and *\"which reservations are on table 7 tonight\"* is a GIN scan over every reservation instead of an index seek.\n","items":{"$ref":"#/components/schemas/FnbReservationTable"}},"status":{"$ref":"#/components/schemas/TableReservationStatus"},"groupId":{"type":"string","format":"uuid","nullable":true,"description":"5.1.2. Several bookings managed as one party across adjacent tables."},"notes":{"type":"string","description":"Allergies","occasion":null,"accessibility.":null},"actualPartySize":{"type":"integer","nullable":true,"readOnly":true},"tableVisitId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"deposit":{"$ref":"#/components/schemas/TableReservationDeposit"},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"TableReservationDeposit": {"type":"object","nullable":true,"readOnly":true,"x-ticvai-persistence":"fnb.table_reservation","description":"**The deposit this booking holds, snapshotted from `orders.DepositPolicy.dining` when it was made** (decided 29 September, rev 3 REV3-8b). Null where no deposit applied, which is every booking while the venue leaves `dining.enabled` false (the default). A later change to the policy does not re-price a booking already made.\n","required":["amount","basis"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","enum":["fixedPerGuest","fixedPerTable","percentOfMinimumSpend"]},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"While `awaitingDeposit`, when the held cover is released if the deposit has not been authorised. The cart lease of the deposit line (15 minutes, audit R169)."},"refundableUntil":{"type":"string","format":"date-time","nullable":true,"description":"`startsAt` less `dining.refundableUntilHours`. Cancelling before it releases the deposit in full."},"variantId":{"type":"string","format":"uuid","description":"The venue's table-deposit variant, `DepositPolicy.dining.depositVariantId`, which the client sends to `addCartLine` with this booking's id."},"cartLineId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.CartLine` carrying the deposit, once added."},"depositId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.deposit` row, once the payment is authorised."}}},
"TableReservationStatus": {"type":"string","description":"`awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`.","enum":["awaitingDeposit","booked","confirmed","seated","completed","cancelled","noShow"]},
"TableState": {"x-ticvai-persistence":"none — projection over table and visit","allOf":[{"$ref":"#/components/schemas/TableDefinition"},{"type":"object","required":["status"],"properties":{"status":{"$ref":"#/components/schemas/TableStatus"},"visitId":{"type":"string","format":"uuid","nullable":true},"covers":{"type":"integer","nullable":true},"seatedAt":{"type":"string","format":"date-time","nullable":true},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"billTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]},
"TableVisit": {"x-ticvai-persistence":"fnb.table_visit","type":"object","required":["id","tableId","outletId","covers","status","orders","openedAt"],"properties":{"id":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"covers":{"type":"integer"},"status":{"type":"string","enum":["open","billRequested","settled","merged","cancelled"]},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"orders":{"type":"array","items":{"$ref":"#/components/schemas/FnbOrder"}},"mergedIntoVisitId":{"type":"string","format":"uuid","nullable":true},"mergedFromVisitIds":{"type":"array","items":{"type":"string","format":"uuid"}},"runningTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"gratuity":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"readOnly":true,"description":"The gratuity taken at `closeTableVisit`. **Not the service charge**, which is revenue (`FnbServiceChargePolicy`); this is the guest's tip, and `reassignServer` decides who shares it."},"openedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]}
}
```
