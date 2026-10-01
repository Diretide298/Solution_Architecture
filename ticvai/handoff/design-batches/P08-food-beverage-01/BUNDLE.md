# P08-food-beverage-01 — P08 · Food & Beverage

**8 screens · 34 operations · 40 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-020` | F&B Order Management | B–D | 50 | 44 | 6 | 20 | 0 | 1 | — | notStarted (generated) |
| `BO-021` | Order Search | B–D | 5 | 6 | 5 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-045` | Menu Management | A | 57 | 25 | 6 | 6 | 3 | 2 | — | notStarted (generated) |
| `BO-046` | Kitchen Display | B–D | 17 | 35 | 6 | 8 | 0 | 3 | — | notStarted (generated) |
| `BO-104` | Food & Beverage | B–D | 12 | 31 | 6 | 20 | 0 | 0 | — | notStarted (generated) |
| `BO-134` | Kitchen & Preparation Stations | B–D | 11 | 16 | 6 | 1 | 1 | 6 | — | notStarted (generated) |
| `BO-135` | Order Routing & KDS/Printer Rules | B–D | 12 | 28 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-136` | F&B Global Settings & Controls | A | 87 | 29 | 6 | 27 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-021 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-020` F&B Order Management

**Take, amend and route an F&B order from the back office — and see what the kitchen is working on.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 operate, 2 read, 1 configure); in the flows as guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listFnbOrders` reads the population and `getFnbOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `orderId` (deepLink), `ticketId` (deepLink) · cold entry: An order opened from a list or a link. A kitchen ticket opened from the rail. |
| Route | `/fnb/bo-020` |

**What the spec says about it.** Restored 20 August when the P15 build was rolled back. **Named `Timed Entry Rules` and carrying eleven F&B order operations.** Timed entry is an admission profile; this is the order desk. The client board calls it *Active Order Management & Fulfilment Journey*. **Purpose corrected 24 August.** The screen was renamed *F&B Order Management* and its purpose still read *"Control how early and how late a ticket admits"* — **timed entry, on a screen whose every operation is `fnb`.** A rename that moves the label and leaves the sentence is worse than no rename: the name is what a reader scans and the purpose is what they trust.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listFnbOrders`. | `listFnbOrders` ?outletId |
| Table visit id | picker: choose a table visit (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?tableVisitId=` to `listFnbOrders`. | `listFnbOrders` ?tableVisitId |
| Status | select | optional | — | Ordered · Accepted · In preparation · Ready · Served · Collected · Delivered · Cancelled · Refunded | — | Sends `?status=` to `listFnbOrders`. | `listFnbOrders` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listKitchenStations` ?outletId |
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |
| Course | number field | — | min 1 | `listKitchenTickets` ?course |

**Form: Accept F&B order** (modal, opened by *Accept F&B order*; *Accept F&B order* calls `acceptFnbOrder`, *Cancel* sends nothing)

**Collects what `acceptFnbOrder` sends before it is called.** Required: `recordedAt`. Optional: `estimatedReadyAt`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Estimated ready at `estimatedReadyAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `acceptFnbOrder` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `acceptFnbOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `acceptFnbOrder` body |

Errors to draw in the form: 409 Already accepted, cancelled, or the outlet has stopped taking orders

**Form: Save kitchen ticket status** (modal, opened by *Save kitchen ticket status*; *Save kitchen ticket status* calls `setKitchenTicketStatus`, *Cancel* sends nothing)

**Collects what `setKitchenTicketStatus` sends before it is called.** Required: `status`, `recordedAt`. Optional: `lineIds`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | — | `setKitchenTicketStatus` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Advance specific lines. Omit for the whole ticket. | `setKitchenTicketStatus` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setKitchenTicketStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setKitchenTicketStatus` body |

Errors to draw in the form: 409 The move is not one of the four above. Names the ticket's current status.

**Form: Amend F&B order** (modal, opened by *Amend F&B order*; *Amend F&B order* calls `amendFnbOrder`, *Cancel* sends nothing)

**Collects what `amendFnbOrder` sends before it is called.** Nothing in the body is required. Optional: `addLines`, `removeLineIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `amendFnbOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `amendFnbOrder` body |
| Menu item `addLines[].menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `amendFnbOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `amendFnbOrder` body |
| Modifier options `addLines[].modifierOptionIds` | multi-picker: choose modifier options | optional | — | — | — | — | `amendFnbOrder` body |
| Note `addLines[].note` | text area | optional | — | max length 200 | — | Free text to the kitchen. Allergy notes belong here and are surfaced prominently. | `amendFnbOrder` body |
| Seat number `addLines[].seatNumber` | number field | optional | — | — | — | Which cover ordered it. Drives split-by-covers accurately. | `amendFnbOrder` body |
| Course `addLines[].course` | number field | optional | — | — | — | Course grouping, so the kitchen fires in sequence. | `amendFnbOrder` body |
| Redeem entitlement `addLines[].redeemEntitlementId` | text field | optional | — | An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is … | — | A meal combo redeemed at the till or by a scan (29 September, MOB-4; applied 30 September). | `amendFnbOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `amendFnbOrder` body |

Errors to draw in the form: 409 A targeted line is already `inPreparation` or served. Names the lines in `lineIds`, and `suggestedOperation` is `voidOrder` (audit R125 (4)).; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

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

**Form: Prioritise kitchen ticket** (modal, opened by *Prioritise kitchen ticket*; *Prioritise kitchen ticket* calls `prioritiseKitchenTicket`, *Cancel* sends nothing)

**Collects what `prioritiseKitchenTicket` sends before it is called.** Required: `reason`. Optional: `priority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `prioritiseKitchenTicket` body |
| Priority `priority` | stepper or slider | optional | 100 | min 0; max 100 | — | Absent means the top of the queue (decided 28 September, audit R125 (2)): the ticket takes the highest priority on the rail. | `prioritiseKitchenTicket` body |

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

**Sent by *Cancel F&B order*** (`cancelFnbOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `cancelFnbOrder` body |
| Reason `reason` | radio group | required | — | Outlet refused · Guest cancelled · Item unavailable · Too long · Error | — | — | `cancelFnbOrder` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `cancelFnbOrder` body |
| Record waste `recordWaste` | toggle | optional | — | — | — | Where preparation had started. Raises a waste movement rather than silently losing the cost. | `cancelFnbOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

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
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Kitchen ticket | the name it points at, never the id | — |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |

**Every kitchen station** (data table, from `listKitchenStations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Menu items | list or chips (count when long) | Items routed to this station. |
| Display endpoint | text | The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station … |
| Is active | yes / no (icon or chip) | — |

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

**The selected F&B order** (detail panel, from `getFnbOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Table visit | the name it points at, never the id | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Lines | list or chips (count when long) | — |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Kitchen ticket | the name it points at, never the id | — |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Accept F&B order (primary button) | `acceptFnbOrder` POST `/fnb-orders/{orderId}/accept` | inline | FnbOrder | 409 Already accepted, cancelled, or the outlet has stopped taking orders | opens modal first |
| Save kitchen ticket status (secondary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | opens modal first; produces a document or message: Advance a kitchen ticket |
| Amend F&B order (secondary button) | `amendFnbOrder` PATCH `/fnb-orders/{orderId}` | inline | FnbOrder | 409 A targeted line is already `inPreparation` or served. Names the lines in `lineIds`, and `suggestedOperation` is `voidOrder` (audit R125 (4)).; 412 The row changed since the `If-Match` version was read (SD-013). … | opens modal first |
| Cancel F&B order (destructive button) | `cancelFnbOrder` POST `/fnb-orders/{orderId}/cancel` | inline | FnbOrder | 403 The caller lacks `ORDER_MODIFY`, or the order is `accepted` and the caller lacks `ORDER_VOID` (`void-permission-required`, audit R091 (5)).; 409 Past `accepted` (audit R125 (3)). `illegalStatusTransition` where the … | — |
| Create F&B order (secondary button) | `createFnbOrder` POST `/fnb-orders` | CreateFnbOrderRequest | FnbOrder | 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here … | emits `fnb.kitchenTicketCreated`; opens modal first |
| Prioritise kitchen ticket (secondary button) | `prioritiseKitchenTicket` POST `/kitchen/tickets/{ticketId}/prioritise` | inline | KitchenTicket | — | opens modal first; produces a document or message: Move a ticket up the queue |
| Save kitchen stations (secondary button) | `setKitchenStations` PUT `/kitchen/stations` | inline | KitchenStation[] | 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `listFnbOrders` (onLoad, List F&B orders); `listKitchenStations` (onLoad, List preparation stations and their routing); `listKitchenTickets` (onLoad, Kitchen ticket queue)

**Where the user goes next**

- → `BO-104` Food & Beverage: *Food & Beverage*
- → `GST-025` F&B – Order Tracking: *Tracks the order*; carries `orderId`

**What opens over it**

- confirmDialog *Cancel F&B order*: **Names what `cancelFnbOrder` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted. **Collects what `cancelFnbOrder` sends before it is called.** Required: `recordedAt`, `reason`. Optional: `note` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order yet. Offers Create F&B order (`createFnbOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, tableVisitId, status and the order are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getFnbOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 400 Validation failed; 409 A targeted line is already `inPreparation` or served. Names the lines in `lineIds`, and `suggestedOperation` is `voidOrder` (audit R125 (4)).; 409 Already accepted, cancelled, or the outlet has stopped taking orders |

#### Permissions

- `acceptFnbOrder` → `ORDER_MODIFY` (operate) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `amendFnbOrder` → `ORDER_MODIFY` (operate) · staff
- `cancelFnbOrder` → `ORDER_MODIFY` (operate) · staff
- `createFnbOrder` → `ORDER_CREATE` (operate) · staff
- `getFnbOrder` → `ORDER_VIEW` (read) · staff
- `listFnbOrders` → `ORDER_VIEW` (read) · staff
- `listKitchenStations` → `PRODUCT_VIEW` (read) · staff
- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `prioritiseKitchenTicket` → `ORDER_MODIFY` (operate) · staff
- `setKitchenStations` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getFnbOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.6 | The system should be able to modify the count of item directly rather than having to punch the menu button multiple times. | Bundles and Promotions | CONTRACTED | `amendFnbOrder` |
| 4.6.7 | The system should be able to modify the count of combo item, The system should ask if the combo needs to be repeated or modified, rather than directly multiplying the previous selected combo.(the … | Bundles and Promotions | CONTRACTED | `amendFnbOrder` |
| 4.6.3 | The system should be able to record a cancellation/Refund to guests from the POS register using scan option of the original receipt. | Bundles and Promotions | CONTRACTED | `cancelFnbOrder` |
| 4.6.4 | The system should be able to record a Cancellation/refund from guests from the POS register using transaction ID / PNR selection option. | Bundles and Promotions | CONTRACTED | `cancelFnbOrder` |
| 4.6.5 | The system should mark the transactions associated with a cancelled or refunded order as voided to ensure balanced reporting. Inventory should be updated with wastage for the associated transaction. | Bundles and Promotions | CONTRACTED | `cancelFnbOrder` |
| 4.6.12 | The system should be able to change transaction status to refunded after the Refund transaction is posted. Refund/Negative sales to be treated as guest recovery and update inventory with wastage. | Bundles and Promotions | CONTRACTED | `cancelFnbOrder` |
| 4.6.1 | The system should be able to record a sale to guests from the POS register using menu screens/buttons. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.6.2 | The system should be able to record a sale to guests from the POS register using manual product sale option | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.9.2 | The system should have a notes section to capture special requests that modifiers don't cover, such as bespoke guest requirements. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 10.1.1 | The system should allow send special request comments/directions on the kitchen display/printers for the kitchen preparation guest requests/inputs. | Games & F&B Integration | CONTRACTED | `createFnbOrder` |
| 4.6.35 | Provide end-to-end order status tracking including Ordered, Accepted, In Preparation, Ready, Served, Collected, Delivered, Cancelled, and Refunded with real-time synchronization. | Bundles and Promotions | CONTRACTED | `getFnbOrder` |
| 5.1.11 | Synchronize order statuses in real time between POS, KDS, Mobile Ordering, QR Ordering, Guest Apps, Delivery Systems, and Reporting Platforms. | F&B & Guest Management | CONTRACTED | `getFnbOrder` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-020` · status **notStarted** · provenance generated
- Flow F11 *Guest orders food to a lounger*, step 5: Kitchen accepts and prepares → A ticket appears at the right station
- Flow F11 branch at step 5 (recoverable): when Outlet refuses the order, Past last orders, out of an ingredient, too far behind. **Refused immediately rather than after ten minutes** — `cancelFnbOrder` before acceptance needs no approval for exactly this.
- Flow F11 branch at step 5 (requiresStaff): when Item unavailable after acceptance, Partial cancellation with a refund for the line. The rest is prepared.

#### Acceptance for the design

- [ ] Every input above is drawn (50), with its required mark, default, format and its error state (400, 403, 404, 409, 412).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Accept F&B order, Save kitchen ticket status, Amend F&B order, Cancel F&B order, Create F&B order, Prioritise kitchen ticket, Save kitchen stations.
- [ ] Every transition is wired: `BO-104`, `GST-025`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-021` Order Search

**Find any order taken at this venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY` (1 operate); in the flows as cashier, guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session), `orderId` (deepLink) · cold entry: An order opened from a list or a link. |
| Route | `/fnb/bo-021` |

**What the spec says about it.** Restored 20 August when the P15 build was rolled back.

#### Inputs: what the user enters or picks

**Form: Record order handover** (modal, opened by *Record order handover*; *Record order handover* calls `recordOrderHandover`, *Cancel* sends nothing)

**Collects what `recordOrderHandover` sends before it is called.** Required: `outcome`, `recordedAt`. Optional: `deliveredToLocationId`, `runnerPrincipalId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

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

**The guest order status** (detail panel, from `getGuestOrderStatus`)

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Is ready for collection | yes / no (icon or chip) | — |
| Lines | list or chips (count when long) | Per-line status. A guest waiting on one dish should see which. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record order handover (primary button) | `recordOrderHandover` POST `/guest-orders/{orderId}/delivery` | inline | GuestOrderStatus | 409 Order is not ready, or already closed; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)). | opens modal first |

**Data it reads**: `getGuestOrderStatus` (onLoad, Track an order)

**Where the user goes next**

- → `BO-104` Food & Beverage: *Food & Beverage*
- → `POS-002` Sell — Ticket Catalogue: *Sell — Ticket Catalogue*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order search, read by `getGuestOrderStatus`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order search untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order search yet. Offers Record order handover (`recordOrderHandover`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_MODIFY`, which `recordOrderHandover` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Order is not ready, or already closed; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)). |

#### Permissions

- `recordOrderHandover` → `ORDER_MODIFY` (operate) · staff
- `getGuestOrderStatus` → no permission · guest

**A refused user sees:** Shown when the caller lacks `ORDER_MODIFY`, which `recordOrderHandover` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.49 | Pickup Ordering - System shall support pickup ordering. | Guest Mobile App & Branding | CONTRACTED | `recordOrderHandover` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-021` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 3.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 3.dc.html#ret-3a`
- Flow F11 *Guest orders food to a lounger*, step 7: Runner delivers to the lounger → Delivered, not merely served
- Flow F81 *A retail sale runs from overview to tender*, step 1: Order Search. → **Drawn by the client as RET-3A.** 2 operations on this step.
- Flow F11 branch at step 7 (requiresStaff): when Runner cannot find the guest, The guest moved. The order is held at the outlet and the guest is notified to collect — **not thrown away and not left in the sun**.
- Flow F81 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-021?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record order handover.
- [ ] Every transition is wired: `BO-104`, `POS-002`.
- [ ] Every gated control is gated: `ORDER_MODIFY`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-045` Menu Management

**Change what is on sale and what is in it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #20699 (APP-SETUP-BO-045) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as supervisor, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMenus` reads the population and `getMenu` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `menuId` (deepLink), `menuItemId` (deepLink) · cold entry: A menu opened from the list. An item opened from the menu. **Allergen verification is per item** — a menu-wide check is a job, not a screen. |
| Route | `/fnb/bo-045` |

**What the spec says about it.** Restored 20 August when the P15 build was rolled back. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listMenus`. | `listMenus` ?outletId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listMenus`. | `listMenus` ?activeAt |

**Form: Create menu** (modal, opened by *Create menu*; *Create menu* calls `createMenu`, *Cancel* sends nothing)

**Collects what `createMenu` sends before it is called.** Required: `code`, `name`, `outletId`. Optional: `availability`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createMenu` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createMenu` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createMenu` body |
| Availability `availability` | group | optional | — | — | — | When this menu is in force. Absent means always. | `createMenu` body |
| Days of week `availability.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createMenu` body |
| Start time `availability.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `createMenu` body |
| End time `availability.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `createMenu` body |
| Valid from `availability.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `createMenu` body |
| Valid to `availability.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `createMenu` body |

Errors to draw in the form: 400 Validation failed

**Form: Save menu sections** (modal, opened by *Save menu sections*; *Save menu sections* calls `setMenuSections`, *Cancel* sends nothing)

**Collects what `setMenuSections` sends before it is called.** Required: `sections`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sections `sections` | repeatable rows | required | — | — | — | — | `setMenuSections` body |
| Code `sections[].code` | text field | required | — | — | — | — | `setMenuSections` body |
| Name `sections[].name` | text field | required | — | — | — | — | `setMenuSections` body |
| Sort order `sections[].sortOrder` | number field | required | — | — | — | — | `setMenuSections` body |
| Items `sections[].items` | repeatable rows | optional | — | — | — | The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`. | `setMenuSections` body |
| ID `sections[].items[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setMenuSections` body |
| Product variant `sections[].items[].productVariantId` | picker: choose a product variant | required | — | — | shows names, sends the id | The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue. | `setMenuSections` body |
| Name `sections[].items[].name` | text field | required | — | — | — | — | `setMenuSections` body |
| Description `sections[].items[].description` | text area | optional | — | — | — | — | `setMenuSections` body |
| Price `sections[].items[].price` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setMenuSections` body |
| Sort order `sections[].items[].sortOrder` | number field | optional | — | — | — | — | `setMenuSections` body |
| Modifier groups `sections[].items[].modifierGroupIds` | multi-picker: choose modifier groups | optional | — | — | — | — | `setMenuSections` body |
| Station `sections[].items[].stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setMenuSections` body |
| Is stock tracked `sections[].items[].isStockTracked` | toggle | optional | — | Stock-tracked items cannot be sold offline. | — | True where a recipe exists. Stock-tracked items cannot be sold offline. | `setMenuSections` body |
| Is available `sections[].items[].isAvailable` | toggle | required | — | — | — | — | `setMenuSections` body |
| Unavailable reason `sections[].items[].unavailableReason` | text field | optional | — | — | — | — | `setMenuSections` body |
| Restore at `sections[].items[].restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand. | `setMenuSections` body |
| Preparation minutes `sections[].items[].preparationMinutes` | number field (minutes) | optional | — | — | — | — | `setMenuSections` body |
| Allergens `sections[].items[].allergens` | multi-select chips | optional | — | Gluten · Crustaceans · Eggs · Fish · Peanuts · Soybeans · Milk · Nuts · Celery · Mustard · Sesame · Sulphites … | — | — | `setMenuSections` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save menu** (modal, opened by *Save menu*; *Save menu* calls `updateMenu`, *Cancel* sends nothing)

**Collects what `updateMenu` sends before it is called.** Nothing in the body is required. Optional: `name`, `availability`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateMenu` body |
| Availability `availability` | group | optional | — | — | — | When this menu is in force. Absent means always. | `updateMenu` body |
| Days of week `availability.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `updateMenu` body |
| Start time `availability.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `updateMenu` body |
| End time `availability.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `updateMenu` body |
| Valid from `availability.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `updateMenu` body |
| Valid to `availability.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `updateMenu` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateMenu` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Publish menu** (modal, opened by *Publish menu*; *Publish menu* calls `publishMenu`, *Cancel* sends nothing)

**Collects what `publishMenu` sends before it is called.** Nothing in the body is required. Optional: `effectiveAt`, `channels`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Effective at `effectiveAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Absent or null publishes now. Otherwise local midnight, in the Region's time zone, of the day the menu goes live, sent as a UTC instant like every date-time. | `publishMenu` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where the version goes live. Empty means every channel the outlet sells on. | `publishMenu` body |
| Note `note` | text area | optional | — | — | — | — | `publishMenu` body |

**Form: Schedule menu publish** (modal, opened by *Schedule menu publish*; *Schedule menu publish* calls `scheduleMenuPublish`, *Cancel* sends nothing)

**Collects what `scheduleMenuPublish` sends before it is called.** Nothing in the body is required. Optional: `effectiveAt`, `cancelScheduleId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Effective at `effectiveAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Local midnight, in the Region's time zone, of the day the menu goes live, sent as a UTC instant like every date-time (for a Dubai outlet going live on 1 March … | `scheduleMenuPublish` body |
| Cancel schedule `cancelScheduleId` | picker: choose a cancel schedule | optional | — | — | shows names, sends the id | A pending schedule from `listMenuSchedules`. When set, `effectiveAt` is ignored. | `scheduleMenuPublish` body |

Errors to draw in the form: 409 A schedule already exists for that date. Names it in `existingScheduleId`.

**Form: Rollback menu** (modal, opened by *Rollback menu*; *Rollback menu* calls `rollbackMenu`, *Cancel* sends nothing)

**Collects what `rollbackMenu` sends before it is called.** Nothing in the body is required. Optional: `toVersion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To version `toVersion` | number field | optional | — | — | — | A `MenuVersion.version` from `listMenuVersions`. Absent means the version before the live one. | `rollbackMenu` body |

**Form: Apply menu actions** (modal, opened by *Apply menu actions*; *Apply menu actions* calls `applyMenuActions`, *Cancel* sends nothing)

**Collects what `applyMenuActions` sends before it is called.** Required: `actions`. Optional: `previewOnly`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Preview only `previewOnly` | toggle | optional | on | — | — | — | `applyMenuActions` body |
| Actions `actions` | repeatable rows | required | — | — | — | — | `applyMenuActions` body |
| Kind `actions[].kind` | select | optional | — | Reprice · Retire · Activate · Move section · Set availability · Set tax | — | — | `applyMenuActions` body |
| Selector `actions[].selector` | group | optional | — | — | — | Which items a bulk action touches. At least one criterion; several narrow each other. | `applyMenuActions` body |
| Menu items `actions[].selector.menuItemIds` | multi-picker: choose menu items | optional | — | — | — | — | `applyMenuActions` body |
| Section codes `actions[].selector.sectionCodes` | list of values (chips) | optional | — | — | — | `MenuSection.code` values on this menu. | `applyMenuActions` body |
| All items `actions[].selector.allItems` | toggle | optional | — | — | — | Every item on the menu. Stated rather than implied by an empty selector. | `applyMenuActions` body |
| Value `actions[].value` | group | optional | — | — | — | What the action sets. One field per kind: `reprice` takes `percentChange` or `price`; `moveSection` takes `toSectionCode`; `setAvailability` takes `isAvailable`; `setTax` takes … | `applyMenuActions` body |
| Percent change `actions[].value.percentChange` | number field (%) | optional | — | — | — | Signed. `-5` is five per cent off. | `applyMenuActions` body |
| Price `actions[].value.price` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyMenuActions` body |
| To section code `actions[].value.toSectionCode` | text field | optional | — | — | — | — | `applyMenuActions` body |
| Is available `actions[].value.isAvailable` | toggle | optional | — | — | — | — | `applyMenuActions` body |
| Tax code `actions[].value.taxCode` | text field | optional | — | — | — | A tax code from the finance tax engine. | `applyMenuActions` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every menu** (data table, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**The selected menu** (detail panel, from `getMenu`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**Last allergen verdict** (detail panel, from `verifyAllergens`): **Shows the last automatic verdict** — `matches`, `undeclared` (with `via` and `sourceRef`, shown first), `overDeclared` — from the check the server runs after every recipe, substitution or modifier change, with when it ran (decided 28 September, audit R241). **The contract records the verdict but exposes no read of it yet**, so until one exists this panel shows the result of the latest manual …

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Matches | yes / no (icon or chip) | — |
| Declared | list or chips (count when long) | — |
| Actual | list or chips (count when long) | — |
| Undeclared | list or chips (count when long) | Present in the dish and absent from the label. The dangerous direction, and the response leads with it. |
| Allergen | text | — |
| Via | chip: Ingredient, Substitution, Modifier, Shared equipment | — |
| Source ref | text | — |
| Over declared | list or chips (count when long) | Labelled and no longer present. Safe, and still worth fixing — a menu that over-declares teaches guests the labels are guesses. |
| Checked at | 1 Oct 2026, 14:30 | — |
| Trigger | chip: Manual, Recipe changed, Substitution changed, Modifier changed | What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Create menu (primary button) | `createMenu` POST `/menus` | CreateMenuRequest | Menu | 400 Validation failed | opens modal first |
| Save menu sections (secondary button) | `setMenuSections` PUT `/menus/{menuId}/sections` | inline | Menu | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save menu (secondary button) | `updateMenu` PATCH `/menus/{menuId}` | inline | Menu | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Publish menu (secondary button) | `publishMenu` POST `/menus/{menuId}/publish` | inline | MenuVersion | — | opens modal first |
| Schedule menu publish (secondary button) | `scheduleMenuPublish` POST `/menus/{menuId}/schedule` | inline | MenuSchedule | 409 A schedule already exists for that date. Names it in `existingScheduleId`. | opens modal first |
| Rollback menu (secondary button) | `rollbackMenu` POST `/menus/{menuId}/rollback` | inline | MenuVersion | — | opens modal first |
| Apply menu actions (secondary button) | `applyMenuActions` POST `/menus/{menuId}/actions` | inline | MenuActionResult | — | opens modal first |
| Re-check allergens (manual) (secondary button) | `verifyAllergens` POST `/menu-items/{menuItemId}/verify-allergens` | — | AllergenVerdict | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listMenus` (onLoad, List menus)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-104` Food & Beverage: *Food & Beverage*
- → `POS-002` Sell — Ticket Catalogue: *The till picks it up in its next catalogue bundle*; calls `publishMenu`
- → `BO-111` Ingredient Substitution, Allergen & Nutrition: *An item's recipe changed, so its allergens are re-verified*; carries `menuId`, `menuItemId`; calls `applyMenuActions`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The menu list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the menu untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No menu yet. Offers Create menu (`createMenu`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, activeAt and the menu are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Constraints are unsatisfiable — minimum exceeds available options. Told apart from the shared validation 400 by `refusedReason`.; 400 Validation failed; 409 A schedule already exists for that date. Names it in `existingScheduleId`.; 409 The group adds an allergen the item does not declare. Names both — `modifierGroupId` and `allergens` — so the venue can fix the claim or drop the group. |

#### Permissions

- `listMenus` → `PRODUCT_VIEW` (read) · staff
- `getMenu` → `PRODUCT_VIEW` (read) · staff
- `createMenu` → `PRODUCT_CONFIGURE` (configure) · staff
- `setMenuSections` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateMenu` → `PRODUCT_CONFIGURE` (configure) · staff
- `publishMenu` → `PRODUCT_CONFIGURE` (configure) · staff
- `scheduleMenuPublish` → `PRODUCT_CONFIGURE` (configure) · staff
- `rollbackMenu` → `PRODUCT_CONFIGURE` (configure) · staff
- `applyMenuActions` → `PRODUCT_CONFIGURE` (configure) · staff
- `verifyAllergens` → `PRODUCT_VIEW` (read) · staff
- `createModifierGroup` → `PRODUCT_CONFIGURE` (configure) · staff
- `attachModifierGroup` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.22 | The system should provide the option to split menu items by sections for specific locations of the outlet. For example: one menu section going to kitchen and the other going to the drink bar. The … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.3 | The system should provide the option to remotely configure visibility and placement of available menu items available for sale on POS screen. The function should be limited to only users accounts … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.4 | The system should be able to design a menu button layout page can be copied and re-used in multiple locations if the need arises | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 2.1.32 | System shall allow guests to purchase food and beverage items through self-service kiosks. The kiosk shall support menu browsing, product customization, combo meals, upsell recommendations … | Ticketing Sales | CONTRACTED | data `Menu` |
| 2.1.33 | System shall allow guests to purchase retail merchandise through self-service kiosks. The kiosk shall support product browsing, inventory validation, variant selection (size, color, style) … | Ticketing Sales | CONTRACTED | data `Menu` |
| 4.6.13 | The system should have a interface for kiosks where the guest should be able to place order via the self service option all the way till completing payments. | Bundles and Promotions | CONTRACTED | data `Menu` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Modifiers can be free or chargeable with minimum/maximum selection rules; combo meals support component selection with upgrade options at additional cost. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-328)*
- Product creation captures product name, auto-generated PLU code, category/sub-category, pricing type, inventory-tracking toggle, recipe linkage, unit of measurement and preparation time. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-327)*
- Menu & Product Command Center tracks menus, active recipes and products, and flags products without mapped recipes or with unavailable ingredients. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-325)*

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-045` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 2.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2a`, `FnB Board 2.dc.html#fnb-2b`, `FnB Board 2.dc.html#fnb-2e`, `FnB Board 2.dc.html#fnb-2j`, `FnB Board 2.dc.html#fnb-2k`
- Flow F31 *A menu is drafted, scheduled and rolled back*, step 1: The manager opens the live menu and starts a draft. → A new version in `draft`. **The live version keeps selling** — an edit that takes effect as it is typed is an edit made under pressure at 11am on a Saturday.
- Flow F31 *A menu is drafted, scheduled and rolled back*, step 2: They reprice a category rather than forty items. → **Previewed before applied, always.** The preview names how many items each action touches, because *reprice all* and *reprice all in this category* differ by four hundred dirhams a day.
- Flow F31 *A menu is drafted, scheduled and rolled back*, step 4: The draft is scheduled for Monday rather than published now. → **Takes effect at the outlet's local midnight, not the tenant's.** A venue in Dubai and one in London do not change menu at the same instant.
- Flow F31 *A menu is drafted, scheduled and rolled back*, step 5: Monday arrives. The schedule fires and the version goes live. → **The previous version stays readable**, which is what makes step 7 possible — and a price change that cannot be undone is a price change nobody makes on a Friday.
- Flow F31 *A menu is drafted, scheduled and rolled back*, step 7: The new price is wrong on eleven items. The manager rolls back. → **The restored version becomes a new version rather than deleting the bad one.** A menu history that can be edited cannot answer *what were we charging at noon*, and that is exactly what a refund …
- Flow F85 *Production is planned, costed and released*, step 5: Menu Management. → **Drawn by the client as FNB-2B.** 3 operations on this step.
- Flow F93 *A recipe changes and its allergen claim is re-verified*, step 2: Menu Management. → **Drawn by the client as FNB-2E.**
- Flow F31 branch at step 2 (medium): when The repricing crosses the venue's approval threshold., `createApprovalRequest` before publish. **The same mechanism as a stock write-off** — one approval path, different subjects.
- Flow F31 branch at step 4 (high): when A schedule already exists for that date., **Refused, with the existing schedule named.** Two publishes on one date is a race, and the loser is silently discarded — a venue with three pending changes and no way to see them is the state …
- Flow F31 branch at step 7 (high): when Orders were taken at the wrong price before the rollback., **Rolling back does not correct them.** The orders stand at what they were charged, and the correction is a refund or a goodwill comp — **a system that silently reprices settled orders is a system …

#### Acceptance for the design

- [ ] Every input above is drawn (57), with its required mark, default, format and its error state (400, 403, 404, 409, 412).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Create menu, Save menu sections, Save menu, Publish menu, Schedule menu publish, Rollback menu, Apply menu actions, Re-check allergens (manual), What publishing changes.
- [ ] Every transition is wired: `BO-008`, `BO-104`, `POS-002`, `BO-111`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-046` Kitchen Display

**Show the kitchen what to make, in order.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 operate, 2 read, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `ticketId` (deepLink) · cold entry: A kitchen ticket opened from the rail. |
| Route | `/fnb/bo-046` |

**What the spec says about it.** Restored 20 August when the P15 build was rolled back. **Retained in P08 on 20 August when the P15 build was rolled back**, and P15 now owns the kitchen display for the venue floor. **This is the back-office view of the same tickets** — a manager watching the pass from a desk, not a screen at the pass.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Station id | picker: choose a station (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?stationId=` to `listKitchenTickets`. | `listKitchenTickets` ?stationId |
| Status | select | optional | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | Sends `?status=` to `listKitchenTickets`. | `listKitchenTickets` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Course | number field | — | min 1 | `listKitchenTickets` ?course |
| Outlet | picker: choose an outlet | — | — | `listKitchenStations` ?outletId |

**Form: Save kitchen ticket status** (modal, opened by *Save kitchen ticket status*; *Save kitchen ticket status* calls `setKitchenTicketStatus`, *Cancel* sends nothing)

**Collects what `setKitchenTicketStatus` sends before it is called.** Required: `status`, `recordedAt`. Optional: `lineIds`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | — | `setKitchenTicketStatus` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Advance specific lines. Omit for the whole ticket. | `setKitchenTicketStatus` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setKitchenTicketStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setKitchenTicketStatus` body |

Errors to draw in the form: 409 The move is not one of the four above. Names the ticket's current status.

**Form: Prioritise kitchen ticket** (modal, opened by *Prioritise kitchen ticket*; *Prioritise kitchen ticket* calls `prioritiseKitchenTicket`, *Cancel* sends nothing)

**Collects what `prioritiseKitchenTicket` sends before it is called.** Required: `reason`. Optional: `priority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `prioritiseKitchenTicket` body |
| Priority `priority` | stepper or slider | optional | 100 | min 0; max 100 | — | Absent means the top of the queue (decided 28 September, audit R125 (2)): the ticket takes the highest priority on the rail. | `prioritiseKitchenTicket` body |

**Form: Save kitchen stations** (modal, opened by *Save kitchen stations*; *Save kitchen stations* calls `setKitchenStations`, *Cancel* sends nothing)

**Collects what `setKitchenStations` sends before it is called.** Required: `stations`. **Each station carries its display assignment**, `displayWorkstationIds` — the kitchen displays that show this station's rail. A display belongs to one station; assigning it to a second is refused 400. The kitchen display takes its station from this assignment rather than from a picker on the display (decided 28 September, audit R277). Dismissing sends nothing; the screen behind is unchanged.

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
| Save kitchen ticket status (primary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | opens modal first; produces a document or message: Advance a kitchen ticket |
| Prioritise kitchen ticket (secondary button) | `prioritiseKitchenTicket` POST `/kitchen/tickets/{ticketId}/prioritise` | inline | KitchenTicket | — | opens modal first; produces a document or message: Move a ticket up the queue |
| Save kitchen stations (secondary button) | `setKitchenStations` PUT `/kitchen/stations` | inline | KitchenStation[] | 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue); `listKitchenStations` (onLoad, List preparation stations and their routing)

**Where the user goes next**

- → `BO-104` Food & Beverage: *Food & Beverage*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The kitchen display list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the kitchen display untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No kitchen display yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on stationId, status and the kitchen display are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listKitchenTickets` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 409 The move is not one of the four above. Names the ticket's current status. |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `listKitchenStations` → `PRODUCT_VIEW` (read) · staff
- `prioritiseKitchenTicket` → `ORDER_MODIFY` (operate) · staff
- `setKitchenStations` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listKitchenTickets` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.34 | Support automatic and manual prioritization of kitchen orders based on VIP guests, memberships, Fast Pass, SLA targets, group bookings, events, or supervisor override. | Bundles and Promotions | CONTRACTED | `prioritiseKitchenTicket` |
| 4.6.33 | Support configurable kitchen routing rules to automatically direct orders/items to kitchen stations, printers, KDS screens, bars, dessert stations, or production areas based on product, category … | Bundles and Promotions | CONTRACTED | `setKitchenStations` |
| 4.7.5 | The system should support usage of buzzers for notifying guests when their order is ready. A buzzer would be assigned to the guests at the time of taking their order. | Bundles and Promotions | CONTRACTED | data `KitchenTicket` |
| 5.2.3 | The system should be able to have options as Fire & forget and Hold & fire orders(modifications should including the manual time adjustment). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |
| 5.2.4 | The system should be able to have options as phased, timed, delayed ordering (used in fine dine options). | F&B & Guest Management | CONTRACTED | data `KitchenTicket` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A52** Design on-seat / location-based F&B delivery: seat-linked QR codes for seated events, and physical location QR codes (e.g., per beach chair/table) for open venues, routing kitchen orders to the scanned location *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'kitchen')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-046` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 409, 412).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-046?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save kitchen ticket status, Prioritise kitchen ticket, Save kitchen stations.
- [ ] Every transition is wired: `BO-104`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-104` Food & Beverage

**Everything in food & beverage.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `REPORT_VIEW_VENUE`, `TENANT_VIEW` (1 configure, 2 read, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMenus` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/food-beverage` |

**What the spec says about it.** Section landing. **4 screens reach the entry point through here** — before 20 August they reached it through nothing. **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listMenus`. | `listMenus` ?outletId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listMenus`. | `listMenus` ?activeAt |
| Search food & beverage | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |

**Form: Create menu** (modal, opened by *Create menu*; *Create menu* calls `createMenu`, *Cancel* sends nothing)

**Collects what `createMenu` sends before it is called.** Required: `code`, `name`, `outletId`. Optional: `availability`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createMenu` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createMenu` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createMenu` body |
| Availability `availability` | group | optional | — | — | — | When this menu is in force. Absent means always. | `createMenu` body |
| Days of week `availability.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createMenu` body |
| Start time `availability.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `createMenu` body |
| End time `availability.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `createMenu` body |
| Valid from `availability.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `createMenu` body |
| Valid to `availability.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `createMenu` body |

Errors to draw in the form: 400 Validation failed

#### Outputs: what the screen shows and produces

**Shown**

**Every menu** (data table, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**Takings and admissions today** (metric tile, from `getKpiValues`): **Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Card list** (card list): 4 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).

**The selected menu** (detail panel, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |
| Published version | 1,234 | The `MenuVersion.version` live now. Null for a menu never published. |
| Published at | 1 Oct 2026, 14:30 | — |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create menu (primary button) | `createMenu` POST `/menus` | CreateMenuRequest | Menu | 400 Validation failed | opens modal first |

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `getVenueSettings` (onLoad, What is enabled here); `listMenus` (onLoad, Menus and their state)

**Where the user goes next**

- → `BO-020` F&B Order Management: *F&B Order Management*
- → `BO-021` Order Search: *Order Search*
- → `BO-045` Menu Management: *Menu Management*; carries `menuId`, `menuItemId`
- → `BO-046` Kitchen Display: *Kitchen Display*
- → `BO-134` Kitchen & Preparation Stations: *Kitchen & Preparation Stations*
- → `BO-135` Order Routing & KDS/Printer Rules: *Order Routing & KDS/Printer Rules*
- → `BO-136` F&B Global Settings & Controls: *F&B Global Settings & Controls*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in food & beverage yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for food & beverage. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `listMenus` → `PRODUCT_VIEW` (read) · staff
- `createMenu` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** You do not have permission for food & beverage. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.32 | System shall allow guests to purchase food and beverage items through self-service kiosks. The kiosk shall support menu browsing, product customization, combo meals, upsell recommendations … | Ticketing Sales | CONTRACTED | data `Menu` |
| 2.1.33 | System shall allow guests to purchase retail merchandise through self-service kiosks. The kiosk shall support product browsing, inventory validation, variant selection (size, color, style) … | Ticketing Sales | CONTRACTED | data `Menu` |
| 4.6.13 | The system should have a interface for kiosks where the guest should be able to place order via the self service option all the way till completing payments. | Bundles and Promotions | CONTRACTED | data `Menu` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-104` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-104?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create menu.
- [ ] Every transition is wired: `BO-020`, `BO-021`, `BO-045`, `BO-046`, `BO-134`, `BO-135`, `BO-136`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `REPORT_VIEW_VENUE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-134` Kitchen & Preparation Stations

**Kitchen & Preparation Stations — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW` (1 configure, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listKitchenStations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `outletId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/food-beverage/kitchen-preparation-stations` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `FnB Board 1.dc.html` frame `fnb-1h`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen &amp; Preparation Stations* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listKitchenStations`. | `listKitchenStations` ?outletId |
| Search kitchen | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

**Form: Save kitchen stations** (modal, opened by *Save kitchen stations*; *Save kitchen stations* calls `setKitchenStations`, *Cancel* sends nothing)

**Collects what `setKitchenStations` sends before it is called.** Required: `stations`. **Each station carries its display assignment**, `displayWorkstationIds` — the kitchen displays that show this station's rail. A display belongs to one station; assigning it to a second is refused 400. The kitchen display takes its station from this assignment rather than from a picker on the display (decided 28 September, audit R277). Dismissing sends nothing; the screen behind is unchanged.

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
| Save kitchen stations (primary button) | `setKitchenStations` PUT `/kitchen/stations` | inline | KitchenStation[] | 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `listKitchenStations` (onLoad, List preparation stations and their routing); `listOutlets` (onLoad, The outlets whose kitchen SLA is set (setKitchenSla is per …)

**Where the user goes next**

- → `BO-104` Food & Beverage: *Food & Beverage*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The kitchen preparation stations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the kitchen preparation stations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No kitchen preparation stations yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId and the kitchen preparation stations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listKitchenStations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation. |

#### Permissions

- `listKitchenStations` → `PRODUCT_VIEW` (read) · staff
- `setKitchenStations` → `PRODUCT_CONFIGURE` (configure) · staff
- `setKitchenSla` → `PRODUCT_CONFIGURE` (configure) · staff
- `listOutlets` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listKitchenStations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.33 | Support configurable kitchen routing rules to automatically direct orders/items to kitchen stations, printers, KDS screens, bars, dessert stations, or production areas based on product, category … | Bundles and Promotions | CONTRACTED | `setKitchenStations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Kitchens are divided into stations (grill, fryer, beverage, dessert, etc.), each mapped to specific printers or KDS devices. Routing rules decide where an item prints/displays by category or item, with a fallback station/device if the primary one is offline or faulty. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-323)*

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A52** Design on-seat / location-based F&B delivery: seat-linked QR codes for seated events, and physical location QR codes (e.g., per beach chair/table) for open venues, routing kitchen orders to the scanned location *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-134` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 1.dc.html`
- Client design-board frames: `FnB Board 1.dc.html#fnb-1h`

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-134?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save kitchen stations.
- [ ] Every transition is wired: `BO-104`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-135` Order Routing & KDS/Printer Rules

**Order Routing & KDS/Printer Rules — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listWorkstations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/food-beverage/order-routing-kds-printer-rules` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `FnB Board 1.dc.html` frame `fnb-1j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Order Routing &amp; KDS / Printer Rules* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listWorkstations`. | `listWorkstations` ?venueId |
| Sale board kind | radio group | optional | — | Ticketing · Fnb · Retail · Mixed | — | Sends `?saleBoardKind=` to `listWorkstations`. | `listWorkstations` ?saleBoardKind |
| Search order routing | search field | — | — | — | — | — | — |

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

**Every workstation** (data table, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Scope path | text | — |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point. |
| Devices | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |

**The selected workstation** (detail panel, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Scope path | text | — |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point. |
| Devices | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Time zone | text | — |
| Deployment profile | chip: Terminal local, Venue edge, Thin | How this workstation obtains catalogue and inventory (ADR-0013). - `terminalLocal` — own SQLite, leases direct from the cell. |
| Edge node | the name it points at, never the id | Present when `deploymentProfile` is `venueEdge`. |
| Health score | 1,234 | Board 1 of the client's POS set. A number a manager can sort by — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save kitchen stations (primary button) | `setKitchenStations` PUT `/kitchen/stations` | inline | KitchenStation[] | 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `listWorkstations` (onLoad, List workstations)

**Where the user goes next**

- → `BO-104` Food & Beverage: *Food & Beverage*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order routing kds list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order routing kds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order routing kds yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, saleBoardKind and the order routing kds are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listWorkstations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation. |

#### Permissions

- `setKitchenStations` → `PRODUCT_CONFIGURE` (configure) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listWorkstations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.33 | Support configurable kitchen routing rules to automatically direct orders/items to kitchen stations, printers, KDS screens, bars, dessert stations, or production areas based on product, category … | Bundles and Promotions | CONTRACTED | `setKitchenStations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Kitchens are divided into stations (grill, fryer, beverage, dessert, etc.), each mapped to specific printers or KDS devices. Routing rules decide where an item prints/displays by category or item, with a fallback station/device if the primary one is offline or faulty. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-323)*

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-135` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 1.dc.html`
- Client design-board frames: `FnB Board 1.dc.html#fnb-1j`

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403, 412).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-135?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save kitchen stations.
- [ ] Every transition is wired: `BO-104`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-136` F&B Global Settings & Controls

**F&B Global Settings & Controls — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 2 · needs the `core` module |
| Block | Block A · ticket #20702 (APP-SETUP-BO-136) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 configure, 2 read); in the flows as supervisor |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProductionRuns` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `planId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. A plan opened from the list. |
| Route | `/food-beverage/f-b-global-settings-controls` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | radio group | optional | — | Planned · In progress · Completed · Cancelled | — | Sends `?status=` to `listProductionRuns`. | `listProductionRuns` ?status |
| Location kind | segmented control | optional | — | Outlet · Commissary | — | Sends `?locationKind=` to `listProductionRuns`. | `listProductionRuns` ?locationKind |
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listProductionRuns`. | `listProductionRuns` ?from |
| Search f | search field | — | — | — | — | — | — |

**Form: Save venue settings** (modal, opened by *Save venue settings*; *Save venue settings* calls `setVenueSettings`, *Cancel* sends nothing)

**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `id`, `venueId`, `currencyCode`, `currencyScale`, `supportHours`, `quietHours`, `biometrics`, `segregatedAccess`, `alerting`, and **the configured limits** — `displayCurrencies`, the cart, resale, exchange, reschedule and reservation limits, `shiftVarianceThreshold`, and the `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue` and `reporting` groups (decided 28 September, audit R094). **A limit left empty inherits the tenant default** (null = inherit); each field shows the default it would inherit. **`fnb.foodSafetyLeadPrincipalId` is settable here** — until a food-safety …

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

**Form: Build production plan** (modal, opened by *Build production plan*; *Build production plan* calls `buildProductionPlan`, *Cancel* sends nothing)

**Collects what `buildProductionPlan` sends before it is called.** Required: `id`, `forDate`, `status`, `lines`. Optional: `outletId`, `basedOnSuggestionId`, `releasedRunIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `buildProductionPlan` body |
| Outlet `outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | — | `buildProductionPlan` body |
| For date `forDate` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | The trading day this prep list is for, in the Region's time zone. | `buildProductionPlan` body |
| Status `status` | radio group | required | — | Draft · Released · Superseded · Cancelled | — | — | `buildProductionPlan` body |
| Based on suggestion `basedOnSuggestionId` | picker: choose a based on suggestion | optional | — | — | shows names, sends the id | The forecast it started from. Kept so plan-against-forecast can be compared later — which is the label `recordSuggestionOutcome` needs. | `buildProductionPlan` body |
| Lines `lines` | repeatable rows | required | — | — | — | — | `buildProductionPlan` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `buildProductionPlan` body |
| Suggested quantity `lines[].suggestedQuantity` | number field | optional | — | — | — | — | `buildProductionPlan` body |
| Planned quantity `lines[].plannedQuantity` | number field | required | — | — | — | — | `buildProductionPlan` body |
| UOM `lines[].uom` | text field | optional | — | — | — | — | `buildProductionPlan` body |
| Station `lines[].stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `buildProductionPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every production run** (data table, from `listProductionRuns`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Recipe | the name it points at, never the id | — |
| Producing outlet | the name it points at, never the id | — |
| For outlets | list or chips (count when long) | Where it goes. A central kitchen produces for outlets that did not make it. |
| Planned quantity | 1,234.5 | — |
| Actual quantity | 1,234.5 | BL-126. Theoretical against actual is the whole point of recording this. |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, In progress, Completed, Cancelled | — |
| Variance reason | text | — |

**The selected production run** (detail panel, from `listProductionRuns`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Recipe | the name it points at, never the id | — |
| Production plan | the name it points at, never the id | The plan whose release created this run. Null for a run planned directly. |
| Producing outlet | the name it points at, never the id | — |
| For outlets | list or chips (count when long) | Where it goes. A central kitchen produces for outlets that did not make it. |
| Planned quantity | 1,234.5 | — |
| Actual quantity | 1,234.5 | BL-126. Theoretical against actual is the whole point of recording this. |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, In progress, Completed, Cancelled | — |
| Variance reason | text | — |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |
| Fnb | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Save venue settings (primary button) | `setVenueSettings` PUT `/venues/{venueId}/settings` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Build production plan (secondary button) | `buildProductionPlan` POST `/production-plans` | ProductionPlan | ProductionPlan | — | opens modal first |
| Release production plan (secondary button) | `releaseProductionPlan` POST `/production-plans/{planId}/release` | — | ProductionPlan | — | — |

**Data it reads**: `getVenueSettings` (onLoad, Operational settings for this venue); `listProductionRuns` (onLoad, What is being made, and what was)

**Where the user goes next**

- → `BO-137` Recipe Consumption & Theoretical Inventory: *Recipe Consumption & Theoretical Inventory*
- → `BO-104` Food & Beverage: *Food & Beverage*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The global settings controls list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the global settings controls untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No global settings controls yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, locationKind, from and the global settings controls are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getVenueSettings` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Permissions

- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff
- `buildProductionPlan` → `PRODUCT_CONFIGURE` (configure) · staff
- `releaseProductionPlan` → `PRODUCT_CONFIGURE` (configure) · staff
- `listProductionRuns` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getVenueSettings` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

27 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.8.14 | AI forecasts production quantities using historical demand and attendance. | Bundles and Promotions | CONTRACTED | `buildProductionPlan` |
| 4.6.36 | Compare theoretical recipe cost versus actual inventory consumption and wastage, highlighting variances and operational inefficiencies. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.7 | Manage recipe yields, shrinkage, wastage and final portions. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.12 | Plan kitchen production quantities based on expected demand. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.13 | Manage batch preparation and production runs. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.16 | Generate production sheets for kitchen operations. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.17 | Support central kitchen and commissary operations supplying multiple outlets, including production batches, transfers, yields, and planning. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.18 | Generate replenishment requests automatically based on demand forecasts, stock levels, and attendance projections. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.19 | Generate production schedules using reservations, attendance forecasts, event schedules, and inventory availability. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 5.1.10 | Manage kitchen production capacity. | F&B & Guest Management | CONTRACTED | data `ProductionRun` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| … 15 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- F&B Controls configure approval workflows globally (e.g. void approval, refund approval) based on amount thresholds and user privileges. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-324)*

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-136` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 2.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2m`, `FnB Board 2.dc.html#fnb-2n`, `FnB Board 5.dc.html#fnb-5d`
- Flow F85 *Production is planned, costed and released*, step 1: F&B Global Settings & Controls. → **Drawn by the client as FNB-2M.** 3 operations on this step.
- Flow F85 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (87), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-136?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Save venue settings, Build production plan, Release production plan.
- [ ] Every transition is wired: `BO-137`, `BO-104`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

### In P08 · Food & Beverage

- Decision: F&B configuration (menus, recipes, costing, inventory) is managed at outlet level, and Retail follows the same segregation. Venue-owned homogeneous outlets (e.g. popcorn/ice-cream booths) may be set up centrally once and applied across outlets, but the model stays outlet-level. *(agreed · MoM 18 Aug 2026, 4.5 Outlet-Level vs. Venue-Level Configuration — Key Discussion · DI-330)*
- **Open question.** F&B dashboards are role-based: the F&B Director sees all outlets, an outlet manager sees only their own outlet. Detailed design of the role-based dashboards (Director vs. outlet-level roles) is still to be finalised. *(open · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions; 6. Open Items · DI-318)*

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptFnbOrder": {"method":"POST","path":"/fnb-orders/{orderId}/accept","contract":"fnb","summary":"The outlet takes the order","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FnbOrder"},
"amendFnbOrder": {"method":"PATCH","path":"/fnb-orders/{orderId}","contract":"fnb","summary":"Amend an order before it is prepared","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FnbOrder"},
"applyMenuActions": {"method":"POST","path":"/menus/{menuId}/actions","contract":"fnb","summary":"Do the same thing to many items at once","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuActionResult"},
"attachModifierGroup": {"method":"PUT","path":"/menu-items/{menuItemId}/modifier-groups","contract":"fnb","summary":"Give an item its choices","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"buildProductionPlan": {"method":"POST","path":"/production-plans","contract":"fnb","summary":"Turn a forecast into a prep list","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductionPlan","responds":"ProductionPlan"},
"cancelFnbOrder": {"method":"POST","path":"/fnb-orders/{orderId}/cancel","contract":"fnb","summary":"Cancel an order","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FnbOrder"},
"createFnbOrder": {"method":"POST","path":"/fnb-orders","contract":"fnb","summary":"Place an F&B order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateFnbOrderRequest","responds":"FnbOrder"},
"createMenu": {"method":"POST","path":"/menus","contract":"fnb","summary":"Create a menu","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateMenuRequest","responds":"Menu"},
"createModifierGroup": {"method":"POST","path":"/modifier-groups","contract":"fnb","summary":"Create a modifier group","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifierGroup","responds":"ModifierGroup"},
"getFnbOrder": {"method":"GET","path":"/fnb-orders/{orderId}","contract":"fnb","summary":"Read an F&B order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"FnbOrder"},
"getGuestOrderStatus": {"method":"GET","path":"/guest-orders/{orderId}","contract":"fnb","summary":"Track an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestOrderStatus"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getMenu": {"method":"GET","path":"/menus/{menuId}","contract":"fnb","summary":"Read a menu with sections and items","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Menu"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listFnbOrders": {"method":"GET","path":"/fnb-orders","contract":"fnb","summary":"List F&B orders","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"tableVisitId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listKitchenStations": {"method":"GET","path":"/kitchen/stations","contract":"fnb","summary":"List preparation stations and their routing","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listKitchenTickets": {"method":"GET","path":"/kitchen/tickets","contract":"fnb","summary":"Kitchen ticket queue","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"stationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"course","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenus": {"method":"GET","path":"/menus","contract":"fnb","summary":"List menus","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutlets": {"method":"GET","path":"/outlets","contract":"tenancy","summary":"List outlets","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Outlet"},
"listProductionRuns": {"method":"GET","path":"/production-runs","contract":"fnb","summary":"What is being made, and what was","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationKind","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"prioritiseKitchenTicket": {"method":"POST","path":"/kitchen/tickets/{ticketId}/prioritise","contract":"fnb","summary":"Move a ticket up the queue","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"publishMenu": {"method":"POST","path":"/menus/{menuId}/publish","contract":"fnb","summary":"Make the draft live, now or on a date","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuVersion"},
"recordOrderHandover": {"method":"POST","path":"/guest-orders/{orderId}/delivery","contract":"fnb","summary":"Record that an order reached the guest","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestOrderStatus"},
"releaseProductionPlan": {"method":"POST","path":"/production-plans/{planId}/release","contract":"fnb","summary":"Make the plan real","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionPlan"},
"rollbackMenu": {"method":"POST","path":"/menus/{menuId}/rollback","contract":"fnb","summary":"Put the previous version back","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuVersion"},
"scheduleMenuPublish": {"method":"POST","path":"/menus/{menuId}/schedule","contract":"fnb","summary":"Publish it on a date, not now","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuSchedule"},
"setKitchenSla": {"method":"PUT","path":"/outlets/{outletId}/kitchen-sla","contract":"fnb","summary":"How long a ticket may sit before it is late","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"KitchenSla","responds":"KitchenSla"},
"setKitchenStations": {"method":"PUT","path":"/kitchen/stations","contract":"fnb","summary":"Configure stations and item routing","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"outletId","in":"query","required":true},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenStation"},
"setKitchenTicketStatus": {"method":"PUT","path":"/kitchen/tickets/{ticketId}/status","contract":"fnb","summary":"Advance a kitchen ticket","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"setMenuSections": {"method":"PUT","path":"/menus/{menuId}/sections","contract":"fnb","summary":"Set menu sections and their item ordering","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Menu"},
"setVenueSettings": {"method":"PUT","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Set support hours, quiet hours, segregated access and alerting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"updateMenu": {"method":"PATCH","path":"/menus/{menuId}","contract":"fnb","summary":"Amend a menu","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Menu"},
"verifyAllergens": {"method":"POST","path":"/menu-items/{menuItemId}/verify-allergens","contract":"fnb","summary":"Does this dish still match its claim?","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AllergenVerdict"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AllergenVerdict": {"x-ticvai-persistence":"fnb.allergen_verdict","type":"object","description":"One allergen check of one dish (decided 28 September, audit R241). Written by the server on every automatic run and by `verifyAllergens` on a manual re-check; `getAllergenVerification` reads the latest.\n","required":["menuItemId","matches","checkedAt","trigger"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"matches":{"type":"boolean"},"declared":{"type":"array","items":{"type":"string"}},"actual":{"type":"array","items":{"type":"string"}},"undeclared":{"type":"array","description":"**Present in the dish and absent from the label.** The dangerous direction, and the response leads with it.\n","items":{"type":"object","properties":{"allergen":{"type":"string"},"via":{"type":"string","enum":["ingredient","substitution","modifier","sharedEquipment"]},"sourceRef":{"type":"string"}}}},"overDeclared":{"type":"array","description":"Labelled and no longer present. **Safe, and still worth fixing** — a menu that over-declares teaches guests the labels are guesses.\n","items":{"type":"string"}},"checkedAt":{"type":"string","format":"date-time","readOnly":true},"trigger":{"type":"string","readOnly":true,"description":"What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241).","enum":["manual","recipeChanged","substitutionChanged","modifierChanged"]}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"CoursingPolicy": {"type":"string","description":"How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n","enum":["fireAndForget","holdAndFire","phased","timed","delayed"]},
"CreateFnbOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently."},"seatNumber":{"type":"integer","nullable":true,"description":"Which cover ordered it. Drives split-by-covers accurately."},"course":{"type":"integer","nullable":true,"description":"Course grouping, so the kitchen fires in sequence."},"redeemEntitlementId":{"type":"string","nullable":true,"x-ticvai-references":"access.entitlement","description":"**A meal combo redeemed at the till or by a scan** (29 September, MOB-4; applied 30 September). The entitlement a bundle's `fnbMenuItem` component issued (promotions `BundleComponent.componentKind: fnbMenuItem`, `menuItemId`, `redeemAtOutletIds`). The line is priced at zero against it, `menuItemId` must be the component's menu item and the outlet one of `redeemAtOutletIds` (or any outlet with the item on a live menu when that list is empty), and the entitlement is marked used in the same step through access `validateAccess` at the outlet. An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is refused the same way if it was used meanwhile."}}},
"CreateFnbOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","outletId","serviceMode","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true,"description":"Required for table service. Absent for quick service."},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateFnbOrderLine"}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.sales_order` this F&B order fulfils (SD-046, 29 September). A POS sale sends the order it took payment on; the commercial order is the sales order and this is its fulfilment."},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateMenuRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","outletId"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"}}},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"FnbOrder": {"x-ticvai-persistence":"fnb.service_order + fnb.service_order_line","type":"object","required":["id","orderNumber","outletId","serviceMode","status","lines","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"lines":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/CreateFnbOrderLine"},{"type":"object","properties":{"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"orders.sales_order","description":"**Retyped 29 September (SD-046)**, and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"},"updatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both offline-sync fields, and no plain updated timestamp.\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"kitchenTicketId":{"type":"string","format":"uuid","nullable":true},"kitchenTickets":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"The kitchen tickets this order created, one per station (SD-046). Returned, not stored here; they are `fnb.kitchen_ticket` rows.","items":{"$ref":"#/components/schemas/KitchenTicket"}},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"GuestOrderStatus": {"type":"object","x-ticvai-persistence":"none — projection over kitchen_ticket","required":["orderId","status","lines"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"isReadyForCollection":{"type":"boolean"},"lines":{"type":"array","description":"Per-line status. A guest waiting on one dish should see which.","items":{"type":"object","properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}}}},
"KitchenSla": {"type":"object","description":"**How long a ticket may sit, per service mode, and what pushes it up the rail** (`setKitchenSla`). The priority weights are the ones `listKitchenTickets` orders the rail by.\n","properties":{"targets":{"type":"array","items":{"type":"object","required":["serviceMode","targetMinutes"],"properties":{"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"targetMinutes":{"type":"integer","minimum":1},"warnAtPercent":{"type":"integer","default":80}}}},"priorityWeights":{"type":"object","description":"The weight of each signal the board names — age, promise time, table stage, a VIP marker.","properties":{"age":{"type":"integer","minimum":0},"targetReadyAt":{"type":"integer","minimum":0,"description":"Promise time."},"tableStage":{"type":"integer","minimum":0},"vip":{"type":"integer","minimum":0}}}}},
"KitchenStation": {"x-ticvai-persistence":"fnb.kitchen_station","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"menuItemIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Items routed to this station."},"displayWorkstationIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**The kitchen displays assigned to this station** (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks after it. Set with `setKitchenStations`. A display reads the rail for the station it is assigned to (`listKitchenTickets`). A workstation is assigned to at most one station; a second assignment is refused `400`.\n"},"displayEndpoint":{"type":"string","nullable":true,"description":"The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station, with a fallback device where the primary is down — 18 Aug minute). Absent where the station has no display assigned.\n"},"isActive":{"type":"boolean"}}},
"KitchenTicket": {"x-ticvai-persistence":"fnb.kitchen_ticket + fnb.kitchen_ticket_line","type":"object","required":["id","orderId","outletId","status","lines","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"coursing":{"allOf":[{"$ref":"#/components/schemas/CoursingPolicy"}],"nullable":true,"description":"BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"},"buzzerCode":{"type":"string","nullable":true,"description":"BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"},"priority":{"type":"integer","description":"Higher fires sooner. Raised by Fast Pass or supervisor override."},"prioritisedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"prioritiseReason":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","status"],"properties":{"lineId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"refireOfLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."},"refireReason":{"allOf":[{"$ref":"#/components/schemas/RefireReason"}],"nullable":true,"readOnly":true},"isChargeable":{"type":"boolean","nullable":true,"readOnly":true,"description":"A refire's `chargeable` flag. Null on a line that is not a refire."},"course":{"type":"integer","nullable":true},"stationId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}},"createdAt":{"type":"string","format":"date-time"},"targetReadyAt":{"type":"string","format":"date-time","nullable":true},"elapsedSeconds":{"type":"integer"}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuActionResult": {"type":"object","x-ticvai-persistence":"none — response shape","description":"**The preview, or what was applied** (`applyMenuActions`). The same shape either way, so the screen that showed the preview shows the result.\n","required":["applied","actions"],"properties":{"applied":{"type":"boolean","description":"False for a preview (`previewOnly`), true once applied."},"actions":{"type":"array","items":{"type":"object","required":["index","kind","affectedItemCount"],"properties":{"index":{"type":"integer","description":"The action's position in the request."},"kind":{"type":"string","enum":["reprice","retire","activate","moveSection","setAvailability","setTax"]},"affectedItemCount":{"type":"integer","description":"**How many items it touches** — the number the preview exists to show."},"affectedMenuItemIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"appliedAt":{"type":"string","format":"date-time","nullable":true}}},
"MenuActionSelector": {"type":"object","description":"**Which items a bulk action touches.** At least one criterion; several narrow each other. *Reprice all* and *reprice all in this section* are different selectors on purpose, and the preview says how many items each one reaches.\n","minProperties":1,"properties":{"menuItemIds":{"type":"array","items":{"type":"string","format":"uuid"}},"sectionCodes":{"type":"array","description":"`MenuSection.code` values on this menu.","items":{"type":"string"}},"allItems":{"type":"boolean","description":"Every item on the menu. Stated rather than implied by an empty selector."}}},
"MenuActionValue": {"type":"object","description":"What the action sets. **One field per kind**: `reprice` takes `percentChange` or `price`; `moveSection` takes `toSectionCode`; `setAvailability` takes `isAvailable`; `setTax` takes `taxCode`; `retire` and `activate` take none.\n","properties":{"percentChange":{"type":"number","description":"Signed. `-5` is five per cent off."},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"toSectionCode":{"type":"string"},"isAvailable":{"type":"boolean"},"taxCode":{"type":"string","description":"A tax code from the finance tax engine."}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MenuSchedule": {"type":"object","x-ticvai-persistence":"fnb.menu_schedule","description":"**A publish dated for later** (`scheduleMenuPublish`, or `publishMenu` with an `effectiveAt`). Listed by `listMenuSchedules` while `pending`, so a venue with three scheduled price changes can see them; one per menu per date.\n","required":["id","menuId","effectiveAt","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"menuId":{"type":"string","format":"uuid"},"effectiveAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["pending","applied","cancelled"]},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` that went live when the schedule fired. Null until then."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"cancelledAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"MenuVersion": {"type":"object","x-ticvai-persistence":"fnb.menu_version","description":"**One published state of a menu, kept.** `publishMenu` writes one, `rollbackMenu` writes a new one from an older one, and `listMenuVersions` reads them — the previous version stays readable, which is what makes rollback and *what were we charging at noon* possible. **A version is never edited**; a menu history that can be edited cannot answer a refund dispute.\nStatuses follow flow F31: a new version is `draft` while the live one keeps selling, `scheduled` once dated, `live`, and `superseded` when a later version goes live.\n","required":["id","menuId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"menuId":{"type":"string","format":"uuid"},"version":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","scheduled","live","superseded"]},"effectiveAt":{"type":"string","format":"date-time","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"restoredFromVersion":{"type":"integer","nullable":true,"description":"Set on a version written by `rollbackMenu` — the version it restored."},"channels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"note":{"type":"string","nullable":true},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","description":"The sections and items as published. The snapshot, not a reference to the live rows.","items":{"$ref":"#/components/schemas/MenuSection"}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"ModifierGroup": {"x-ticvai-persistence":"fnb.modifier_group + fnb.modifier_option","type":"object","description":"**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n","required":["id","code","name","minSelections","maxSelections","options"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"minSelections":{"type":"integer","minimum":0,"description":"Greater than zero makes the group required."},"maxSelections":{"type":"integer","minimum":1},"options":{"type":"array","minItems":1,"items":{"type":"object","required":["id","name","priceDelta"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isDefault":{"type":"boolean"},"isAvailable":{"type":"boolean"},"allergens":{"type":"array","description":"What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductionPlan": {"type":"object","x-ticvai-persistence":"fnb.production_plan + fnb.production_plan_line","description":"Board 2M. **Forecast demand against recipes, producing a prep list.** Built from `requestSuggestion(kind=prepPlan)` and then edited — **a forecast a chef cannot overrule is a forecast a chef ignores.**\n**A plan is not a production run and the separation is deliberate.** A plan is drafted, argued over and edited; releasing it creates the runs. **A plan that creates runs as it is drafted creates runs nobody asked for.**\n","required":["id","forDate","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"forDate":{"type":"string","format":"date","description":"The trading day this prep list is for, in the Region's time zone."},"status":{"type":"string","enum":["draft","released","superseded","cancelled"]},"basedOnSuggestionId":{"type":"string","format":"uuid","nullable":true,"description":"**The forecast it started from.** Kept so plan-against-forecast can be compared later — which is the label `recordSuggestionOutcome` needs.\n"},"lines":{"type":"array","items":{"type":"object","required":["itemId","plannedQuantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"suggestedQuantity":{"type":"number","nullable":true},"plannedQuantity":{"type":"number"},"uom":{"type":"string"},"stationId":{"type":"string","format":"uuid","nullable":true}}}},"releasedRunIds":{"type":"array","items":{"type":"string","format":"uuid"},"readOnly":true}}},
"ProductionRun": {"type":"object","x-ticvai-persistence":"fnb.production_run","description":"BL-129. **A central kitchen makes 400 portions at 6am for four outlets**, and nothing modelled that — orders consume stock and no operation produced any.\n**Production converts ingredients into a sellable item**, which is a stock movement in both directions at once, and treating it as two unrelated adjustments loses the yield.\n","required":["id","recipeId","plannedQuantity","status"],"properties":{"id":{"type":"string","format":"uuid"},"recipeId":{"type":"string","format":"uuid"},"productionPlanId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The plan whose release created this run. Null for a run planned directly."},"stationId":{"type":"string","format":"uuid","nullable":true,"description":"**The station whose prep list this run is on.** Copied from the plan line on release, where runs are grouped by station (audit R125 (7)).\n"},"producingOutletId":{"type":"string","format":"uuid"},"forOutletIds":{"type":"array","description":"**Where it goes.** A central kitchen produces for outlets that did not make it.\n","items":{"type":"string","format":"uuid"}},"plannedQuantity":{"type":"number"},"actualQuantity":{"type":"number","nullable":true,"description":"BL-126. **Theoretical against actual is the whole point of recording this.** A recipe says 400 portions from the ingredients issued; the run says how many were made, and the gap is waste, theft or a recipe that is wrong.\n"},"scheduledFor":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["planned","inProgress","completed","cancelled"]},"varianceReason":{"type":"string","nullable":true}}},
"RefireReason": {"type":"string","description":"Why a line was made again (`refireItem`). The reasons are the data.","enum":["overcooked","undercooked","wrongItem","dropped","cold","allergyRisk","guestChangedMind","lateAdd"]},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"SalesChannel": {"type":"string","description":"**Where a sale came from.** Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing.\n**Not interchangeable with the local `Channel` enums.** `catalogue.Channel` and `orders.Channel` are byte-identical duplicates of each other listing `pos, kiosk, web, mobile, b2b, ota, callCentre`; `orders.OrderChannel` lists `guestApp, guestWeb, partner, api, backOffice` on top. **Pointing the nine at a local enum would silently narrow them** — and the duplication between the two `Channel` enums is the reason a shared one existed in the first place.\n**This is the reporting dimension**: attribution, promotion eligibility and settlement all group by it, which is why it has to mean the same thing in `orders`, `catalogue`, `subscription` and `marketing-crm` rather than four things that nearly line up.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice","b2b","ota"]},
"ServiceMode": {"type":"string","enum":["quickService","tableService","roomService","collection","delivery"]},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
