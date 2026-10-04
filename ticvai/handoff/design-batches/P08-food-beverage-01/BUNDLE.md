# P08-food-beverage-01 — P08 · Food & Beverage

**8 screens · 40 operations · 47 schemas · 10 permissions**

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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `APPROVAL_REQUEST, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_OWN, REPORT_VIEW_VENUE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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

### Food, Beverage & Retail

Food & beverage, retail, rentals, inventory and procurement across the till (P04), the kitchen display (P15), the staff app (P06), Venue Management (P08), the guest web and app (P01/P02), the kiosk (P05) and the CMS (P13). COUNTER SERVICE (F108): the cashier takes the order on the Food & Drink board from the outlet's menu in force (sections in the outlet's order, option groups attached to the item), sends it to the kitchen, and only then charges — send to kitchen, then charge, for every POS F&B order (R261, upheld against the v2 frame by POSV2-4). The kitchen ticket is on the rail while the card is in the guest's hand; an unpaid sent order is cancelled while ordered or accepted and voided with a reason after (R125(3), R091(5)); the guest gets an order number, and the customer-facing status board (numbers only) is the kitchen display's KIT-007, mirrored on the till's queue (POSV2-7). TABLE SERVICE (F29, F80, F94): a party is seated with its covers, orders across the visit, courses are fired by the pass (DI-333, DI-407), the bill is printed and settled at the end and split by amount, covers, category, item or seat (DI-106); the client's table statuses are Available → Ordered → Table closed → Reserved with no cleaning status (DI-336); moving and merging tables stay on the staff app until after r2 (POSV2-8). GUEST ORDERING (F11, F48): a guest inside the venue orders in the app or web for pickup or delivery to a seat or a scanned location (DI-288, DI-291); F&B and retail are optional licensed modules completed inside TICVAI (DI-505), kept simple (DI-1091); no food without an admission ticket (DI-292); table reservations and the waitlist do not go through the cart and a dining deposit is a venue option, off by default (DI-1048, DI-1049, R077). KITCHEN (P15, F83, F88): TICVAI's own display on commodity screens (19 September, replacing the 31 July "integration point only", DI-077); one kitchen ticket per preparation station from the outlet's routing rules with a fallback display (DI-323); a fired timer counts up and resets per course, not shown for quick service (DI-334); displays are assigned to stations and filter by course, with no station-load tile in r1 (R277). 86 takes an item off sale on every till and guest menu immediately (R110(c)); guests always see "Sold out", never a missing dish. RETAIL (F17, F34, F51): scan and sell through the same cart, charge and payment as tickets and food (DI-795), one cart, one receipt and one QR per guest (DI-293); system stock per venue gates the sale (DI-294); returns by receipt or order number only in r1 (R139(c)), refund to the original tender with a reason code and note (DI-796, DI-797); Shop & Drop is paid online and collected on the way out (R236), a merchandise reservation lasts to the end of the visit day (R169, R215). TILL MONEY (F32, F73, F74, F87): the float is counted by denomination with note images and typed quantities (DI-775, DI-776, R229) while the hardware checks itself (DI-778); the close is a …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Send to kitchen | Put the order on the kitchen rail. On the till it always comes before Charge. | Fire, Fire order, Submit order, kitchen fires on payment | R261 / POSV2-4 / F108 step 3 |
| Charge | The till's single tender step (Payment, POS-005); the button reads "Charge AED 110.25". | Checkout (on staff screens), Pay now | F108 step 4 / screens/P04-point-of-sale.yaml#POS-021 |
| Fire / Hold (a course) | Kitchen-pass words for releasing or holding the next course of a table, and the "fired" timer. | using "fire" for sending an order from the till | DI-333 / DI-334 / DI-407 |
| Kitchen ticket | The slip on the kitchen display, one per preparation station. | Order (on the kitchen display), KOT | R210 |
| Ready · Served · Collected · Delivered | How an order reaches the guest; a server marks Served, a counter Collected, a runner Delivered (with the location). | Done, Complete, Bumped (as a status) | R125 / contracts/satellite/fnb.yaml#recordOrderHandover |
| Recall (kitchen) / Recall held sale (till) | Bring a mis-bumped kitchen ticket back to the rail; separately, bring a held cart back into a sale. Never "Recall" alone where both could apply. | Undo bump, Restore | contracts/satellite/fnb.yaml#recallKitchenTicket / POSV2-6 |
| Unavailable (86) / Sold out | Staff screens say "Unavailable" and may add "86"; guest screens say "Sold out". Immediate everywhere. | Out of stock (for food), Disabled, Hidden | R110 / contracts/satellite/fnb.yaml#getGuestMenu |
| Order type | Dine-in · Quick service · Takeaway · Delivery, chosen in the cart. | Service mode, Fulfilment source (on the till) | DI-789 / contracts/satellite/fnb.yaml#/components/schemas/ServiceMode |
| Covers | The number of guests at a table, entered when seating; drives split-by-covers. | Pax (except as a small suffix on the floor plan), Heads | DI-104 / contracts/satellite/fnb.yaml#openTableVisit |
| Vacant · Seated · Ordered · Bill requested · Table closed · … | Table statuses on every floor plan (till and staff app); "Table closed" is the client's word for after payment. | Cleaning, Needs clearing, Dirty | DI-336 / DI-792 |
| Till · Cash drawer | Staff copy may say "till" for the workstation; the cash drawer is the deposit box. | Terminal id as a heading, Deposit box (on staff screens) | R156 |
| Float · Count · Blind count · Variance | The opening float; the denomination count; the closing count made without seeing the expected cash; counted minus expected. | Expected in drawer, Discrepancy, Error | R080 / POSV2-3 |
| Cash out · Cash in · Safe drop | Taking cash out of the drawer mid-shift, adding change, and a supervisor moving cash to the safe with the cashier as witness. | Lift, Withdrawal (as button labels) | DI-274 / contracts/spine/shift.yaml#createCashMovement / … |
| Menu item · Merchandise item · Inventory item · SKU | The scoped product words; SKU is a variant's code, Product stays the sellable thing. | SKU as the item's name, Article | R131 |
| Stock on hand · Allocated · Available | Available is on hand minus allocated. | Inventory (as a number), Free stock | R171 / DI-361 |
| Requisition · Purchase order · Goods receipt · Transfer · … | The procurement and stock words, in that flow. | GRN as the only label, Indent | DI-341 / DI-348 / DI-362 / DI-363 |
| Shop & Drop | Bought and paid now, collected on the way out. | Click & collect | R236 |
| Check-out (rental) · Return (rental) | Handing equipment to the guest and taking it back. On the same screens payment is "Charge" or "Pay". | Checkout (for a handover), Check-in (for a return) | DI-758 / DI-765 |
| Deposit hold · Release · Capture | A refundable deposit held, given back in full, or partly kept for damage with the rest released. | Charge deposit, Refund deposit | DI-752 / R127 |
| Extension · Swap · Overdue · Late fee | The active-rental words; a quick swap restarts the clock, a late swap earns a free extension. | Renewal, Exchange (for a swap) | DI-761 / DI-762 / DI-764 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-020` | F&B Order Management | A | 25 | 25 | 6 | 15 | 0 | 1 | — | notStarted (generated) |
| `BO-021` | Order Search | A | 5 | 40 | 5 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-045` | Menu Management | A | 68 | 75 | 6 | 15 | 3 | 2 | — | notStarted (generated) |
| `BO-046` | Kitchen Display | C | 8 | 14 | 6 | 7 | 0 | 3 | — | notStarted (generated) |
| `BO-104` | Food & Beverage | A | 1 | 12 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-134` | Kitchen & Preparation Stations | C | 15 | 16 | 6 | 1 | 1 | 6 | — | notStarted (generated) |
| `BO-135` | Order Routing & KDS/Printer Rules | C | 7 | 7 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-136` | F&B Global Settings & Controls | A | 84 | 5 | 6 | 17 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-021, BO-135 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-020` F&B Order Management

**Take, amend and route an F&B order from the back office — and see what the kitchen is working on.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | Block A · task VM-BO-020 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW`, `SCOPE_VIEW` (1 operate, 2 read); in the flows as guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listFnbOrders` reads the population and `getFnbOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `orderId` (deepLink), `ticketId` (deepLink) · cold entry: An order opened from a list or a link. A kitchen ticket opened from the rail. |
| Route | `/fnb/fnb-order-management` |

**What the spec says about it.** Restored 20 August when the P15 build was rolled back. **Named `Timed Entry Rules` and carrying eleven F&B order operations.** Timed entry is an admission profile; this is the order desk. The client board calls it *Active Order Management & Fulfilment Journey*. **Purpose corrected 24 August.** The screen was renamed *F&B Order Management* and its purpose still read *"Control how early and how late a ticket admits"* — **timed entry, on a screen whose every operation is `fnb`.** A rename that moves the label and leaves the sentence is worse than no rename: the name is what a reader scans and the purpose is what they trust.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Station set-up and item routing are configuration owned by Kitchen & Preparation Stations, and the back office has no tender step, so a quick-service order … Removed 2 October 2026 (CHG-WIR-008): Station set-up and item routing are configuration owned by Kitchen & Preparation Stations, and the back office has no tender step, so a quick-service order … Removed 2 October 2026 (CHG-WIR-008): Station set-up and item routing are configuration owned by Kitchen & Preparation Stations, and the back office has no tender step, so a quick-service order …

**From the Food, Beverage & Retail process.** The back-office order desk for an outlet manager or F&B supervisor: every live F&B order across the outlets the user may see, in the nine-state lifecycle, with the few acts a back office legitimately takes on an order (accept or refuse a guest order, cancel within the rules, move a kitchen ticket to the top, amend lines the kitchen has not started). Orders are taken and charged at the till (send to kitchen, then charge), not here. The one thing to get right is the cancel/void boundary: for each order the screen must show which act is available before anyone clicks it — refuse (ordered), cancel with void authority (accepted), or void in Order Corrections (in preparation onward).

**Fixed on main** (the package already carries these; draw what it says): Filters are text fields for "Outlet id", "Table visit id" and "Status", and the three tables are titled "Every F&B order", "Every kitchen … (CHG-SBO-008); "Save kitchen stations" (setKitchenStations) and the kitchen-station table (listKitchenStations) are on the order desk. (CHG-WIR-008); "Create F&B order" (createFnbOrder) and the purpose "Take, amend and route an F&B order from the back office". (CHG-WIR-008); The cancel dialog says that once accepted "the reason comes from the void reason list (guestChangedMind, enteredInError, itemUnavailable … (CHG-SBO-008); The no-access state names the permission key ORDER_VIEW (the same pattern on every screen in this part). (CHG-SBO-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which outlets accept guest orders automatically, and where is that configured?** → Drawn default stands (answer: "Default / recommended accepted"): Show Accept only on orders still in Ordered; no outlet setting is drawn (no contract field exists for "automatic where the outlet is configured"). *(decided by Chinmay, 2026-10-02; DEC-028 / CHG-NOTE-004)*
- **Outlet-level visibility (an outlet manager sees only their outlet) — how is it implemented?** → Drawn default stands (answer: "Default / recommended accepted"): The outlet filter lists only outlets the user's grants reach; no extra control. *(decided by Chinmay, 2026-10-02; DEC-029 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `Outlet.id` |
| Status | select | optional | — | Ordered · Accepted · In preparation · Ready · Served · Collected · Delivered · Cancelled · Refunded | — | The order statuses in words, as chips; free text matched nothing. | `FnbOrder.status` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listFnbOrders` ?outletId |
| Table visit | picker: choose a table visit | — | — | `listFnbOrders` ?tableVisitId |
| Status | select | — | Ordered · Accepted · In preparation · Ready · Served · Collected · Delivered · Cancelled · Refunded | `listFnbOrders` ?status |
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |
| Course | number field | — | min 1 | `listKitchenTickets` ?course |
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

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

**Form: Prioritise kitchen ticket** (modal, opened by *Prioritise kitchen ticket*; *Prioritise kitchen ticket* calls `prioritiseKitchenTicket`, *Cancel* sends nothing)

**Collects what `prioritiseKitchenTicket` sends before it is called.** Required: `reason`. Optional: `priority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `prioritiseKitchenTicket` body |
| Priority `priority` | stepper or slider | optional | 100 | min 0; max 100 | — | Absent means the top of the queue (decided 28 September, audit R125 (2)): the ticket takes the highest priority on the rail. | `prioritiseKitchenTicket` body |

**Sent by *Cancel F&B order*** (`cancelFnbOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `cancelFnbOrder` body |
| Reason `reason` | radio group | required | — | Outlet refused · Guest cancelled · Item unavailable · Too long · Error | — | — | `cancelFnbOrder` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `cancelFnbOrder` body |
| Record waste `recordWaste` | toggle | optional | — | — | — | Where preparation had started. Raises a waste movement rather than silently losing the cost. | `cancelFnbOrder` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet (filter)**: A picker of outlet names (listOutlets), never a text field for an id. Defaults to the user's own outlet when their access is restricted to one, otherwise "All outlets". F&B Director sees all outlets, an outlet manager only theirs. *(source: contracts/satellite/fnb.yaml#listFnbOrders / DI-318 / DI-331)*
- **Status (filter)**: Chips over the nine FnbOrderStatus values, grouped: Live (Ordered, Accepted, In preparation, Ready), Handed over (Served, Collected, Delivered), Cancelled, Refunded. Default is Live. The labels are the same nine words the till, kitchen display and guest app use. *(source: MATRIX 4.6.35 / MATRIX 5.1.11 / contracts/satellite/fnb.yaml#/components/schemas/FnbOrderStatus)*
- **Table (filter)**: Replaces the "Table visit id" text field. A picker of the outlet's open tables by label (T12), resolved to the visit behind it. Hidden for outlets that do not offer table service. *(source: contracts/satellite/fnb.yaml#listFnbOrders / DI-319)*
- **Cancel reason**: Required. The contract's cancel list, labelled for staff: Outlet refused (outletRefused), Guest cancelled (guestCancelled), Item unavailable (itemUnavailable), Taking too long (tooLong), Entered in error (error). Note optional, max 300 characters. "Record waste" toggle appears only when the order is Accepted (the kitchen may have started) and defaults off; it raises a waste movement instead of losing the cost. *(source: contracts/satellite/fnb.yaml#cancelFnbOrder / R125)*
- **Accept order — estimated ready time**: Optional time picker, prefilled from the outlet's delivery policy: now + ASAP collection minutes (default 25) for collection, now + ASAP delivery minutes (default 45) for delivery. Station is optional and defaults to the outlet's routing rules; recordedAt is device time and never shown. *(source: contracts/satellite/fnb.yaml#acceptFnbOrder / contracts/satellite/fnb.yaml#/components/schemas/FnbDeliveryPolicy)*
- **Move to top — reason**: Reason required, 3 to 500 characters. Position is not asked by default: leaving it empty puts the ticket at the top of the rail. An optional "place at" (1–100) sits behind a secondary control. *(source: contracts/satellite/fnb.yaml#prioritiseKitchenTicket / R125 / MATRIX 4.6.34)*
- **Amend order — lines**: Only lines the kitchen has not started can be removed or changed; lines In preparation or later are shown locked with "Already with the kitchen — void instead". Added lines follow the same modifier rules as the till. Online only. *(source: contracts/satellite/fnb.yaml#amendFnbOrder / R125)*

#### Outputs: what the screen shows and produces

**Shown**

**Orders** (data table, from `listFnbOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Lines | list or chips (count when long) | — |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |

**Kitchen tickets** (data table, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | BL-131. Starters before mains is the entire job of a kitchen pass, and the model fired everything at once. |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Prioritise reason | text | — |

**The selected F&B order** (detail panel, from `getFnbOrder`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Lines | list or chips (count when long) | — |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
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
| Prioritise kitchen ticket (secondary button) | `prioritiseKitchenTicket` POST `/kitchen/tickets/{ticketId}/prioritise` | inline | KitchenTicket | — | opens modal first; produces a document or message: Move a ticket up the queue |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Order list columns**: Order number (venue prefix + sequence, e.g. AQP-104582), Outlet, Order type, Table or location, Status badge, Items, Total (AED, 2 decimals, VAT-inclusive with "incl. VAT" in the detail), Placed (time since, GST), Estimated ready. No ids, no kitchenTicketId, no recordedAt/syncedAt columns. *(source: R152 / DI-039 / contracts/satellite/fnb.yaml#/components/schemas/FnbOrder)*
- **Order type label**: Maps ServiceMode to the till's words: tableService = Dine-in, quickService = Quick service, collection = Takeaway, delivery = Delivery, roomService = Room service. Never "Service mode". *(source: contracts/satellite/fnb.yaml#/components/schemas/ServiceMode / POSV2-4)*
- **Selected order detail**: Lines with modifiers and line notes; one kitchen ticket per preparation station with its own status (an order at the grill and the bar has two); a timeline of status changes; the sales order it fulfils as a link to Order Detail for payment and refund. A ticket moved up shows "Moved to top by Omar Ziad — VIP cabana guest". *(source: contracts/satellite/fnb.yaml#/components/schemas/FnbOrder / MATRIX 10.1.1 / MATRIX 4.6.34)*
- **Not yet synced marker**: An order whose syncedAt is empty came from a till that was offline; show "From an offline till — not yet synced" so a supervisor does not act on a stale status. *(source: contracts/satellite/fnb.yaml#createFnbOrder)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Accept**: Only on orders in Ordered that came from a guest channel (a till order at its own outlet is accepted in the same transaction). Success creates the kitchen tickets and the status becomes Accepted; 409 means already accepted, cancelled, or the outlet has stopped taking orders — say which. *(source: contracts/satellite/fnb.yaml#acceptFnbOrder / F11 step 5)*
- **Refuse**: Cancel on an Ordered order: no approval, reason "Outlet refused" preselected. The guest is told at once rather than after ten minutes. *(source: F11 step 5 / contracts/satellite/fnb.yaml#cancelFnbOrder)*
- **Cancel order (accepted)**: Destructive confirm naming the order, items and value ("Cancel AQP-104582 — 3 items, AED 96.50"). Needs void authority; without it the server answers 403 and the dialog says "Cancelling an accepted order needs void authority — ask a supervisor". Not offered from In preparation onward. *(source: R091 / R125 / contracts/satellite/fnb.yaml#cancelFnbOrder)*
- **Void (in preparation or later)**: No cancel button. Show "Void in Order Corrections" which opens the order there; the server's 409 names voidOrder as the next step. *(source: R125 / contracts/satellite/fnb.yaml#cancelFnbOrder / contracts/spine/orders.yaml#voidOrder)*
- **Move to top**: The ticket takes the highest priority on the rail and records who and why. Rail order is the server's; the screen shows tickets in the order returned and never re-sorts them. *(source: R125 / contracts/satellite/fnb.yaml#listKitchenTickets)*
- **Advance kitchen ticket**: Only the next legal move is offered (Received to Preparing, Preparing to Ready, Ready to Recalled, Recalled to Preparing). Served comes from the handover, Cancelled from cancelling the order. *(source: contracts/satellite/fnb.yaml#setKitchenTicketStatus)*

**Data it reads**: `listFnbOrders` (onLoad, List F&B orders); `listKitchenTickets` (onLoad, Kitchen ticket queue); `listOutlets` (onLoad, List outlets (the pick list))

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
| Empty, first run (`?state=emptyFirstRun`) | No order yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, tableVisitId, status and the order are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | You don't have access to F&B orders — ask your venue manager. Permission keys are never shown to the user; the screen names the access in words. **Never an empty table** — that reads as *there is no data*. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A targeted line is already `inPreparation` or served. Names the lines in `lineIds`, and `suggestedOperation` is `voidOrder` (audit R125 (4)).; 409 Already accepted, cancelled, or the outlet has stopped taking orders; 409 Past `accepted` (audit R125 (3)). `illegalStatusTransition` where the order is `inPreparation` or `ready`, naming `currentStatus` and `suggestedOperation …; 409 The move is … |

#### Edge cases to draw

- **An order with lines at several stations**: Each station's ticket has its own status; the order is Ready only when every ticket is. *(source: contracts/satellite/fnb.yaml#/components/schemas/FnbOrder)*
- **A tracked item ordered on an offline till and stock ran out meanwhile**: The replayed order is refused (trackedItemOffline); show it as an exception on the order with the line named, not a silent disappearance. *(source: contracts/satellite/fnb.yaml#createFnbOrder / R125)*
- **Item unavailable after acceptance**: Partial cancellation of that line with a refund; the rest is prepared. *(source: F11 step 5)*
- **Someone else changed the order while it was open (412)**: Re-read the order and show what changed before the amend can be retried. *(source: contracts/satellite/fnb.yaml#amendFnbOrder)*
- **Guest not found or refused at handover**: The order stays Ready with the attempt recorded; it is not closed or cancelled. *(source: contracts/satellite/fnb.yaml#recordOrderHandover / F11 step 7)*

#### Consistency with other screens

- Match `POS-022`: Same order number, status words and kitchen-ticket split as Send to Kitchen on the till.
- Match `POS-029`: The till's Order Queue shows the same live orders; the stalled-order emphasis must match.
- Match `BO-046`: Back-office Kitchen Display shows the same rail in the same server order.
- Match `BO-047`: Voids from In preparation onward happen there; the hand-off carries the order.
- Match `GST-025`: The guest tracker reads the same nine states; a status changed here is what the guest sees.
- Match `BO-135`: Stations and routing are configured there, not on the order desk.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
orders:
- number: AQP-104582
  outlet: Bite & Go quick-service counter
  type: Quick service
  status: In preparation
  items: 3
  total: AED 96.50
  placed: 12:41 GST (6 min ago)
  ready: '12:52'
- number: AQP-104590
  outlet: Oasis Bistro
  type: Dine-in
  table: T12
  covers: 4
  status: Accepted
  items: 7
  total: AED 412.00
- number: AQP-104593
  outlet: Pool Bar
  type: Delivery
  location: Cabana 12
  status: Ordered
  items: 2
  total: AED 58.00
  guest: Aisha Rahman
lines:
- Chicken shawarma wrap, no garlic
- Halloumi fries
- Fresh mint lemonade (large)
moved_to_top:
  by: Omar Ziad
  reason: VIP cabana guest, birthday cake to follow
```

#### Permissions

- `acceptFnbOrder` → `ORDER_MODIFY` (operate) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `amendFnbOrder` → `ORDER_MODIFY` (operate) · staff
- `cancelFnbOrder` → `ORDER_MODIFY` (operate) · staff
- `getFnbOrder` → `ORDER_VIEW` (read) · staff
- `listFnbOrders` → `ORDER_VIEW` (read) · staff
- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `prioritiseKitchenTicket` → `ORDER_MODIFY` (operate) · staff
- `listOutlets` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** You don't have access to F&B orders — ask your venue manager. Permission keys are never shown to the user; the screen names the access in words. **Never an empty table** — that reads as *there is no data*.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.6 | The system should be able to modify the count of item directly rather than having to punch the menu button multiple times. | Bundles and Promotions | CONTRACTED | `amendFnbOrder` |
| 4.6.7 | The system should be able to modify the count of combo item, The system should ask if the combo needs to be repeated or modified, rather than directly multiplying the previous selected combo.(the … | Bundles and Promotions | CONTRACTED | `amendFnbOrder` |
| 4.6.3 | The system should be able to record a cancellation/Refund to guests from the POS register using scan option of the original receipt. | Bundles and Promotions | CONTRACTED | `cancelFnbOrder` |
| 4.6.4 | The system should be able to record a Cancellation/refund from guests from the POS register using transaction ID / PNR selection option. | Bundles and Promotions | CONTRACTED | `cancelFnbOrder` |
| 4.6.5 | The system should mark the transactions associated with a cancelled or refunded order as voided to ensure balanced reporting. Inventory should be updated with wastage for the associated transaction. | Bundles and Promotions | CONTRACTED | `cancelFnbOrder` |
| 4.6.12 | The system should be able to change transaction status to refunded after the Refund transaction is posted. Refund/Negative sales to be treated as guest recovery and update inventory with wastage. | Bundles and Promotions | CONTRACTED | `cancelFnbOrder` |
| 4.6.35 | Provide end-to-end order status tracking including Ordered, Accepted, In Preparation, Ready, Served, Collected, Delivered, Cancelled, and Refunded with real-time synchronization. | Bundles and Promotions | CONTRACTED | `getFnbOrder` |
| 5.1.11 | Synchronize order statuses in real time between POS, KDS, Mobile Ordering, QR Ordering, Guest Apps, Delivery Systems, and Reporting Platforms. | F&B & Guest Management | CONTRACTED | `getFnbOrder` |
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.34 | Support automatic and manual prioritization of kitchen orders based on VIP guests, memberships, Fast Pass, SLA targets, group bookings, events, or supervisor override. | Bundles and Promotions | CONTRACTED | `prioritiseKitchenTicket` |
| … 3 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (403, 404, 409, 412).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Accept F&B order, Save kitchen ticket status, Amend F&B order, Cancel F&B order, Prioritise kitchen ticket.
- [ ] Every transition is wired: `BO-104`, `GST-025`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-021` Order Search

**Find any order taken at this venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | Block A · task VM-BO-021 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session), `orderId` (deepLink) · cold entry: An order opened from a list or a link. |
| Route | `/fnb/order-search` |

**What the spec says about it.** Restored 20 August when the P15 build was rolled back. **Board frame RET-3A removed 2 October 2026** (CHG-SBO-008): Retail Board 3 RET-3A is the Retail Sales & POS Command Center, a cross-store dashboard, not this order search; the designer must not draw it here.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Order Search bound only getGuestOrderStatus, a guest-audience read of one order by id, and had no search; a staff lookup is listFnbOrders (F&B) and …

**From the Food, Beverage & Retail process.** Staff look up any order at the venue by its number or receipt and see where it is — for a guest at the counter asking "where is my food?", a runner confirming a hand-over, or a supervisor checking a disputed sale. One thing to get right: it is a search first (by order number, receipt number, guest), then one order's status; today it binds only a single-order guest read with nothing to search by.

**Fixed on main** (the package already carries these; draw what it says): "Order Search" binds only getGuestOrderStatus, a guest-audience read of one order by id, and has no search input or list; its states say … (CHG-WIR-008); The board frame cited for BO-021 (Retail Board 3 RET-3A) and flow F81 step 1 are the "Retail Sales & POS Command Center" — a cross-store … (CHG-SBO-008); Navigation exits to POS-002 "Sell — Ticket Catalogue" carrying orderId (from F81). (CHG-CLN-006).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is Order Search F&B-only, or every order at the venue (tickets, retail, F&B — one cart, one receipt)?** → Drawn default stands (answer: "Default / recommended accepted"): Draw it venue-wide with a module chip on each result; F&B results open the F&B status view. *(decided by Chinmay, 2026-10-02; DEC-030 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listFnbOrders` ?outletId |
| Table visit | picker: choose a table visit | — | — | `listFnbOrders` ?tableVisitId |
| Status | select | — | Ordered · Accepted · In preparation · Ready · Served · Collected · Delivered · Cancelled · Refunded | `listFnbOrders` ?status |

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

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Search**: One box that accepts an order number (AQP-104582) or a receipt number, exact match; results list below. Returns in r1 are found by receipt or order number only, so the same identifiers must work here. *(source: R139 / R152 / contracts/satellite/retail.yaml#lookupRetailSale)*
- **Hand-over outcome**: Offer only the outcome that closes this order's type: Dine-in closes Served; Quick service and Takeaway close Collected; Delivery and Room service close Delivered and require the delivery location (prefilled from the order). "Guest not found" and "Refused" are always available and make the note required (max 500). *(source: R125 / contracts/satellite/fnb.yaml#recordOrderHandover)*

#### Outputs: what the screen shows and produces

**Shown**

**F&B orders** (data table, from `listFnbOrders`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Outlet | the name it points at, never the id | — |
| Payment timing | chip: Send first, Pay first | The outlet's payment timing when the order was placed (CHG-CSA-010), kept as a snapshot. |
| Sent to kitchen at | 1 Oct 2026, 14:30 | When the order's kitchen tickets were created. Null on a `payFirst` order not yet paid (CHG-CSA-010). |
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

**Find by receipt** (detail panel, from `lookupRetailSale`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | text | — |
| Receipt number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Order | text | The order in the Order & Payment context. Retail does not keep its own ledger. |
| Outlet | the name it points at, never the id | — |
| Shift | text | — |
| Subject | the name it points at, never the id | — |
| Lines | list or chips (count when long) | — |
| Line | text | — |
| Merchandise | the name it points at, never the id | — |
| Name | text | — |
| Quantity | 1,234 | — |
| Unit price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Line total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Serial numbers | list or chips (count when long) | — |
| Returned quantity | 1,234 | — |
| Is returnable | yes / no (icon or chip) | False once the window has passed or the line is fully returned. |
| Not returnable reason | text | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record order handover (primary button) | `recordOrderHandover` POST `/guest-orders/{orderId}/delivery` | inline | GuestOrderStatus | 409 Order is not ready, or already closed; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)). | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Order status**: The nine-state status as a stepper (Ordered, Accepted, In preparation, Ready, then Served / Collected / Delivered), with each line's kitchen status, because a guest waiting on one dish should see which. Estimated ready time shown; "Ready for collection" emphasised. *(source: contracts/satellite/fnb.yaml#getGuestOrderStatus / MATRIX 5.1.11)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Record hand-over**: Enabled only when the order is Ready. Success moves it to the closing state; 409 "not ready or already closed"; 422 "this outcome does not close a <order type> order" or "delivery needs a location". Works offline (a runner loses signal crossing the venue). *(source: contracts/satellite/fnb.yaml#recordOrderHandover / F11 step 7)*

**Data it reads**: `listFnbOrders` (onLoad, Find an F&B order taken at this venue)

**Where the user goes next**

- → `BO-104` Food & Beverage: *Food & Beverage*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order search, read by `listFnbOrders`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order search untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order search yet. Offers Record order handover (`recordOrderHandover`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listFnbOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for `recordOrderHandover`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 None of the three identifiers was sent; 409 Order is not ready, or already closed; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)). |

#### Edge cases to draw

- **Runner cannot find the guest**: Record "Guest not found" with a note; the order stays Ready, held at the outlet, guest notified to collect. *(source: F11 step 7)*
- **Tenant without the retail or F&B licence**: The search covers only licensed modules; the screen does not offer a module it cannot open. *(source: F81 step 1)*

#### Consistency with other screens

- Match `POS-030`: Sales Journal on the till finds a sale by the same identifiers; same result row layout.
- Match `KIT-007`: The order number shown on a result is the one on the guest status board.
- Match `BO-022`: An order found here opens Order Detail for payment, refund and history.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
search: AQP-104582
result:
  number: AQP-104582
  outlet: Bite & Go quick-service counter
  type: Quick service
  buzzer: '841'
  status: Ready
  ready_since: 12:53 GST
  lines:
  - Chicken shawarma wrap — ready
  - Halloumi fries — ready
  - Fresh mint lemonade — ready
handover:
  outcome: Collected
  by: Priya Nair
```

#### Permissions

- `recordOrderHandover` → `ORDER_MODIFY` (operate) · staff
- `listFnbOrders` → `ORDER_VIEW` (read) · staff
- `lookupRetailSale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listFnbOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for `recordOrderHandover`.

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
- Flow F11 *Guest orders food to a lounger*, step 7: Runner delivers to the lounger → Delivered, not merely served
- Flow F11 branch at step 7 (requiresStaff): when Runner cannot find the guest, The guest moved. The order is held at the outlet and the guest is notified to collect — **not thrown away and not left in the sun**.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-021?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record order handover.
- [ ] Every transition is wired: `BO-104`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-045` Menu Management

**Change what is on sale and what is in it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-SETUP-BO-045-REST |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW` (1 operate, 1 configure, 2 read); in the flows as supervisor, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMenus` reads the population and `getMenu` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `menuId` (deepLink), `menuItemId` (deepLink) · cold entry: A menu opened from the list. An item opened from the menu. **Allergen verification is per item** — a menu-wide check is a job, not a screen. |
| Route | `/fnb/menu-management` |

**What the spec says about it.** Restored 20 August when the P15 build was rolled back. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **BO-045 is the menu home; BO-109 is its arranging canvas (2 October 2026, CHG-SBO-008; Chinmay: duplicate screens merged as proposed).** Menu list, versions, publish, schedule, rollback, modifiers, bulk changes and allergen verdicts live here (frames fnb-2a, 2e, 2j, 2k); "Open in builder" opens BO-109 on the picked menu, which has no menu list of its own. **F&B owns its prices (decided 2 October 2026 by Chinmay, DEC-034; CHG-CSA-009):** `MenuItem.price` is F&B's own catalogue price, set per outlet, so ticketing scales on its own; the central catalogue prices tickets and single-price booths only. This screen reads F&B's catalogue, never the central one.

**From the Food, Beverage & Retail process.** The F&B manager's home for one outlet's menus: which menus the outlet has, what is live, what is a draft, what is scheduled, and the history a refund dispute asks about ("what were we charging at noon"). From here the manager reprices or retires in bulk with a preview, publishes now or for a date, rolls back, manages modifier groups, and sees each dish's allergen verdict. The one thing to get right is that the live version keeps selling while the draft is edited, and every publish says what goes live, on which tills and channels, and from when.

**Fixed on main** (the package already carries these; draw what it says): Plumbing on the screen - a text field "Outlet id", a date picker "Active at", a table "Every menu" with id, outletId, availability object … (CHG-SBO-008); The "Last allergen verdict" panel says the contract exposes no read of the automatic verdict; getAllergenVerification now exists (it names … (CHG-WIR-008); listMenuVersions and listMenuSchedules are not declared on BO-045. (CHG-WIR-008); listModifierGroups is not declared, only createModifierGroup and attachModifierGroup. (CHG-WIR-008); The approval path for a repricing above threshold (createApprovalRequest) is not on the screen. (CHG-WIR-008); BO-045 and BO-109 overlap. Both list menus, both save menu sections, and both point at the same client frame fnb-2b; BO-045 sits under the … (CHG-SBO-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where is an F&B price owned? MenuItem.price says pricing and tax come from the catalogue variant ("a menu is a presentation of the catalogue"), yet applyMenuActions reprices menu items and FNB-2J shows price changes as menu changes.** → F&B prices are owned by F&B: the F&B service has its own catalogue table (prices migrated into F&B so ticketing scales in isolation); an outlet may set its own price. The central catalogue prices tickets and single-price booths. Fix the stale MenuItem text ('pricing and tax come from the catalogue variant'); withdraw the F&B notes' correction asking to drop the menu's own price; check BO-045 and the F&B screens read F&B's catalogue. *(decided by Chinmay, 2026-10-02; DEC-034 / CHG-NOTE-004)*
- **R197 names menu publish and rollback as escalated actions, but publishMenu and rollbackMenu carry no escalated permission. Is the escalation dropped (R197's "no threshold makes sense") or still owed?** → Not answered by Chinmay: the workbook cell repeats the superseded first BO-045 price answer. The question (R197 escalation of menu publish/rollback) takes its drawn default. *(decided by Chinmay, 2026-10-02; DEC-035 / CHG-NOTE-004)*
- **Can a scheduled publish take a time of day? The contract fixes local midnight; the client's FNB-2J frame shows "Tomorrow at 06:00".** → Not answered by Chinmay: the workbook cell repeats the superseded first BO-045 price answer. The question (scheduled menu publish time of day) takes its drawn default. *(decided by Chinmay, 2026-10-02; DEC-036 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `Outlet.id` |
| In force on | date picker | — | — | — | — | Shows the menu as it stands on the chosen date: today by default, a later date to see a scheduled publish. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listMenus` ?outletId |
| Active at | date and time picker | — | — | `listMenus` ?activeAt |
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

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
| Product variant `sections[].items[].productVariantId` | picker: choose a product variant | required | — | — | shows names, sends the id | The catalogue variant this item links to, for reporting, stock and tax class only. | `setMenuSections` body |
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

**Form: Request approval** (modal, opened by *Request approval*; *Request approval* calls `createApprovalRequest`, *Cancel* sends nothing)

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

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet**: A picker of outlets by name (Oasis Bistro, Bite & Go), defaulting to the signed-in user's outlet; never a text field for an id. Menus are configured per outlet; an outlet manager sees only their own outlets, the F&B Director all of them. *(source: DI-330 / DI-331 / DI-318 / contracts/satellite/fnb.yaml#listMenus)*
- **In force at**: Replaces the generated "Active at" date picker. A segmented control "Now / Choose a day and time" that filters to menus in force then (breakfast, lunch, happy hour). Read in the outlet's Region time zone (GST for the UAE), not UTC. *(source: contracts/satellite/fnb.yaml#listMenus / contracts/satellite/fnb.yaml#/components/schemas/MenuAvailability)*
- **Service period (menu availability)**: Day chips Mon to Sun plus a start and end wall-clock time (24-hour, HH:MM) and optional valid-from and valid-to dates. Leaving it empty means "always". Show the result as a sentence ("Daily 18:00 to 23:00 from 1 Nov 2026") under the controls. *(source: contracts/satellite/fnb.yaml#/components/schemas/MenuAvailability)*
- **Menu code**: Short code, up to 64 characters, shown as a small grey label next to the name (OB-DINNER). The name (up to 200 characters) is what everybody reads. *(source: contracts/satellite/fnb.yaml#/components/schemas/CreateMenuRequest)*
- **Bulk change**: One action per row: Reprice (by percent or amount), Retire, Activate, Move to section, Set availability, Set tax; each scoped to a section or a selection of items. "Preview" is the only first button; "Apply" appears only after the preview has named how many items each action touches. *(source: contracts/satellite/fnb.yaml#applyMenuActions / contracts/satellite/fnb.yaml#/components/schemas/MenuActionResult / F31 step 2)*
- **Publish (when)**: "Now" or "On a date". A date publish takes effect at the outlet's local midnight in its Region's time zone, so the picker is a date only, never a time. One scheduled publish per menu per date. *(source: contracts/satellite/fnb.yaml#scheduleMenuPublish / F31 step 4)*
- **Publish (where)**: Channel checkboxes with people's words (Till, Kiosk, Guest app, Guest web, Call centre, Partner); none ticked means every channel the outlet sells on, and the dialog says so in words. *(source: contracts/satellite/fnb.yaml#publishMenu / contracts/shared/common.yaml#/components/schemas/SalesChannel)*
- **Roll back to**: A pick from the version history (newest first), defaulting to the version before the live one. Never a typed version number. *(source: contracts/satellite/fnb.yaml#rollbackMenu / contracts/satellite/fnb.yaml#listMenuVersions)*
- **Modifier group**: Minimum and maximum selections; a minimum above zero shows the group as Required (single-select when min = max = 1). Each option has a price change that may be 0.00 (free) or a charge. Maximum must be at least 1 and not below the minimum. *(source: contracts/satellite/fnb.yaml#createModifierGroup / DI-328 / screens/P08-venue-back-office.yaml#BO-045)*

#### Outputs: what the screen shows and produces

**Shown**

**Menus** (data table, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Is active | yes / no (icon or chip) | — |

**Last allergen verdict** (detail panel, from `getAllergenVerification`)

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

**Versions** (data table, from `listMenuVersions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Menu | the name it points at, never the id | — |
| Status | chip: Draft, Scheduled, Live, Superseded | — |
| Effective at | 1 Oct 2026, 14:30 | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Restored from version | 1,234 | Set on a version written by `rollbackMenu` — the version it restored. |
| Channels | list or chips (count when long) | — |
| Note | text | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Days of week | list or chips (count when long) | — |
| Start time | text | Wall-clock time, in the Region's time zone. |
| End time | text | Wall-clock time, in the Region's time zone. |
| Valid from | 1 Oct 2026 | Calendar day, in the Region's time zone, not UTC. |
| Valid to | 1 Oct 2026 | Calendar day, in the Region's time zone, not UTC. |
| Sections | list or chips (count when long) | The sections and items as published. The snapshot, not a reference to the live rows. |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |

**Scheduled publishes** (data table, from `listMenuSchedules`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Menu | the name it points at, never the id | — |
| Effective at | 1 Oct 2026, 14:30 | — |
| Status | chip: Pending, Applied, Cancelled | — |
| Published version | 1,234 | The `MenuVersion.version` that went live when the schedule fired. Null until then. |
| Cancelled at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Option groups** (data table, from `listModifierGroups`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Min selections | 1,234 | Greater than zero makes the group required. |
| Max selections | 1,234 | — |
| Options | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Price delta | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Is default | yes / no (icon or chip) | — |
| Is available | yes / no (icon or chip) | — |
| Allergens | list or chips (count when long) | What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and … |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The selected menu** (detail panel, from `getMenu`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
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
| Request approval (secondary button) | `createApprovalRequest` POST `/approval-requests` | CreateApprovalRequest | ApprovalRequest | 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Menu list**: One row per menu: name, outlet, service period sentence, live version ("Live v7 since 28 Oct"), and a draft indicator when there are unpublished changes. No ids, no raw sections array. *(source: contracts/satellite/fnb.yaml#/components/schemas/Menu / R254)*
- **Version and schedule status**: Version badges Draft, Scheduled, Live, Superseded; a version written by a rollback reads "Restored from v5". Pending schedules are listed pending first, then by date, each with a Cancel link. *(source: contracts/satellite/fnb.yaml#listMenuVersions / contracts/satellite/fnb.yaml#listMenuSchedules / contracts/satellite/fnb.yaml#/components/schemas/MenuSchedule)*
- **Item flags**: Each item row carries small flags the Command Center asks for - "No recipe" (item not stock-tracked), "86" (unavailable, with reason), and the allergen verdict state. Counts for the loaded menu may head the list; venue-wide attention counts are not drawn. *(source: DI-325 / R283 / contracts/satellite/fnb.yaml#/components/schemas/MenuItem)*
- **Allergen verdict**: Undeclared allergens first, in danger colour, each with where it came from (ingredient, substitution, modifier, shared equipment) and the source line; over-declared second in amber ("safe, still worth fixing"); then "Checked 14:02 after a recipe change" or "after a manual re-check". No check yet reads "Not checked yet", not an empty panel. *(source: R241 / contracts/satellite/fnb.yaml#getAllergenVerification / contracts/satellite/fnb.yaml#/components/schemas/AllergenVerdict)*
- **Prices**: In the venue currency with its own scale (AED 46.00; BHD and KWD to 3 decimals, never rounded). Bulk repricing previews show old and new price side by side. *(source: DI-306 / contracts/satellite/fnb.yaml#applyMenuActions)*
- **Who owns the price**: F&B owns its prices: the F&B service has its own catalogue table (prices were migrated into F&B so ticketing scales on its own), so the menu item's price is F&B's price, and an outlet may set its own. The central catalogue prices tickets and single-price booths only; never draw a central catalogue price beside the menu price. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Create menu**: Creates the menu for the chosen outlet with no sections. It reaches tills and guest menus only after it is published; the success message says so. *(source: contracts/satellite/fnb.yaml#createMenu)*
- **Save sections**: Saves section order and item order. The order here is the order the cashier sees on the counter till. If someone else saved first (412), say "Khalid changed this menu while you were editing - reload to see his changes" and keep the user's edits visible. *(source: contracts/satellite/fnb.yaml#setMenuSections)*
- **Preview, then Apply (bulk change)**: Preview shows per action the number of items touched and which; Apply runs the same actions and shows the same panel as the result. Never an Apply without a preview. *(source: contracts/satellite/fnb.yaml#applyMenuActions / F31 step 2)*
- **Publish now**: Confirmation names the menu, the version, the outlet and its tills, the channels, and that the current live version becomes superseded. After publish, tills pick it up with their next catalogue bundle; an offline till keeps selling the previous version until it reconnects. *(source: contracts/satellite/fnb.yaml#publishMenu / F31 step 5 / screens/P08-venue-back-office.yaml#BO-045)*
- **Schedule**: Writes a pending schedule shown in the list. A second schedule for the same date is refused and the message names the existing one with a "Cancel that schedule" link. *(source: contracts/satellite/fnb.yaml#scheduleMenuPublish / F31 step 4)*
- **Roll back**: Confirmation states that the restored version becomes a new version and that orders already taken at the wrong price stay as charged (corrections are refunds or comps, not a silent reprice). *(source: contracts/satellite/fnb.yaml#rollbackMenu / F31 step 7)*
- **Re-check allergens**: A manual re-check of one dish; the automatic check already runs after every recipe, substitution or modifier change. Updates the verdict panel with trigger "manual". *(source: R241 / contracts/satellite/fnb.yaml#verifyAllergens)*
- **Give an item its choices (attach modifier groups)**: Refused when a group adds an allergen the dish does not declare; the message names the group and the allergen and offers the two ways out - update the dish's allergen claim or remove the group. *(source: contracts/satellite/fnb.yaml#attachModifierGroup)*

**Data it reads**: `listMenus` (onLoad, List menus); `listOutlets` (onLoad, List outlets (the pick list))

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-104` Food & Beverage: *Food & Beverage*
- → `POS-002` Sell — Ticket Catalogue: *The till picks it up in its next catalogue bundle*; calls `publishMenu`
- → `BO-109` Menu Builder & POS Layout Designer: *Open in builder*; carries `menuId`
- → `BO-111` Ingredient Substitution, Allergen & Nutrition: *An item's recipe changed, so its allergens are re-verified*; carries `menuId`, `menuItemId`; calls `applyMenuActions`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The menu list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the menu untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No menu yet. Offers Create menu (`createMenu`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, activeAt and the menu are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_REQUEST` for `createApprovalRequest`; `PRODUCT_CONFIGURE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Constraints are unsatisfiable — minimum exceeds available options. Told apart from the shared validation 400 by `refusedReason`.; 400 Validation failed; 409 A schedule already exists for that date. Names it in `existingScheduleId`.; 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) |

#### Edge cases to draw

- **The repricing crosses the venue's approval threshold**: Publishing waits for approval; the change list shows which lines need approval and by whom (as FNB-2J draws), and Publish is disabled with that reason. *(source: F31 step 2 / screens/P08-venue-back-office.yaml#BO-045)*
- **A menu never published**: Shows "Never published" instead of a live version; tills do not have it. *(source: contracts/satellite/fnb.yaml#/components/schemas/Menu)*
- **A recipe is added to an item**: The item becomes stock-tracked and can no longer be sold on an offline till; the item row shows this so the manager is not surprised at the next outage. *(source: contracts/satellite/fnb.yaml#setRecipe / contracts/satellite/fnb.yaml#/components/schemas/MenuItem)*
- **Outlets in different Region time zones**: A schedule for "1 Nov" goes live at each outlet's local midnight; the confirmation states the local time ("00:00 GST, 1 Nov 2026"). *(source: contracts/satellite/fnb.yaml#scheduleMenuPublish)*

#### Consistency with other screens

- Match `BO-109`: Same menu, same sections and item order; BO-109 is the visual arranger of the draft and must not publish on its own path. See corrections for the overlap.
- Match `BO-111`: The allergen verdict panel is the same component, same wording and order (undeclared first).
- Match `BO-140`: The "86" flag and reason on an item row read exactly as on the availability screen.
- Match `POS-021`: Section order and item order saved here are the order the cashier sees on the counter till.
- Match `BO-011`: Combos (DI-328) are configured on BO-011 (createCombo, setComboSlots); a combo tile in this menu links there.
- Match `WEB-036`: Guests see an unavailable item as "Sold out", never a missing item (getGuestMenu).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro (table service, Main Hall)
menus:
- name: Dinner Menu
  code: OB-DINNER
  period: Daily 18:00 to 23:00
  live: v7 since 28 Oct 2026
  draft: 14 unpublished changes
- name: Ramadan Iftar Menu
  code: OB-IFTAR
  period: Daily 17:30 to 20:00, 1 to 30 Nov 2026
  live: never published
pendingSchedule:
  version: v8
  effective: Mon 2 Nov 2026, 00:00 GST
  by: Khalid Al Mansoori
bulkPreview: Reprice Grill & Mains +5% - 16 items, AED 92.40 a day at last week's mix
items:
- name: Lamb Ouzi
  price: AED 95.00
  flags:
  - No recipe
- name: Classic Beef Burger
  price: AED 46.00
  verdict: Undeclared soybeans via substitution (Burger Sauce supplier change)
- name: Chicken Machboos
  price: AED 58.00
  flags:
  - 86 - Ingredient unavailable, back at 18:00
modifierGroup:
  name: Cooking level
  rule: Required, choose 1
  options:
  - Medium rare 0.00
  - Medium 0.00
  - Well done 0.00
```

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
- `getAllergenVerification` → `PRODUCT_VIEW` (read) · staff
- `listMenuVersions` → `PRODUCT_VIEW` (read) · staff
- `listMenuSchedules` → `PRODUCT_VIEW` (read) · staff
- `listModifierGroups` → `PRODUCT_VIEW` (read) · staff, guest
- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `listOutlets` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_REQUEST` for `createApprovalRequest`; `PRODUCT_CONFIGURE` for …

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.22 | The system should provide the option to split menu items by sections for specific locations of the outlet. For example: one menu section going to kitchen and the other going to the drink bar. The … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.3 | The system should provide the option to remotely configure visibility and placement of available menu items available for sale on POS screen. The function should be limited to only users accounts … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.4 | The system should be able to design a menu button layout page can be copied and re-used in multiple locations if the need arises | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.8.2 | The system should be able to send the modifier data of POS menu items to manage the stocking, reporting and re-order levels within the inventory system. | Bundles and Promotions | CONTRACTED | `listModifierGroups` |
| 4.8.3 | The system should have the ability to pass the modifier data to Kitchen printers and/or kitchen display system, in order for the kitchen to include the requests in their preparations. | Bundles and Promotions | CONTRACTED | `listModifierGroups` |
| 4.9.1 | The system should have the ability to set mandatory or optional modifiers for items. | Bundles and Promotions | CONTRACTED | `listModifierGroups` |
| 4.9.5 | the system should have a separate list of modifiers which the guest can either add or remove as per their choice and the actual order could be charged to the guest. | Bundles and Promotions | CONTRACTED | `listModifierGroups` |
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| … 3 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (68), with its required mark, default, format and its error state (400, 403, 404, 409, 412).
- [ ] Every output is drawn (75 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Create menu, Save menu sections, Save menu, Publish menu, Schedule menu publish, Rollback menu, Apply menu actions, Re-check allergens (manual), What publishing changes, Request approval.
- [ ] Every transition is wired: `BO-008`, `BO-104`, `POS-002`, `BO-109`, `BO-111`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 3 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-046` Kitchen Display

**Show the kitchen what to make, in order.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | Block C · task VM-BO-046 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `ticketId` (deepLink) · cold entry: A kitchen ticket opened from the rail. |
| Route | `/fnb/kitchen-display` |

**What the spec says about it.** Restored 20 August when the P15 build was rolled back. **Retained in P08 on 20 August when the P15 build was rolled back**, and P15 now owns the kitchen display for the venue floor. **This is the back-office view of the same tickets** — a manager watching the pass from a desk, not a screen at the pass.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Station configuration (the station table and Save kitchen stations) sat on a monitoring screen; configuration lives on BO-134 (R254; design-notes correction … Removed 2 October 2026 (CHG-WIR-008): Station configuration (the station table and Save kitchen stations) sat on a monitoring screen; configuration lives on BO-134 (R254; design-notes correction …

**From the Food, Beverage & Retail process.** The back-office view of the kitchen rail: a manager or F&B supervisor watching one outlet's tickets from a desk, not the screen at the pass (that is P15). It is for seeing what is late and for owning a queue jump (prioritise, with a reason). The one thing to get right is that the rail order is the server's - priority first, then the outlet's weights - and the screen never re-sorts it by arrival or promise time.

**Known correction pending (do not draw the wrong version)**

- **"Save kitchen ticket status" is a modal collecting a status from all six values plus "recordedAt" and a station id.** Why: Only four moves are allowed (received to preparing, preparing to ready, ready to recalled, recalled to preparing); served comes from handover and cancelled from cancelling the order; recordedAt is the device's own time. Draw one next-move button. *(source: contracts/satellite/fnb.yaml#setKitchenTicketStatus; Food, Beverage & Retail)*
- **Plumbing columns and fields - "Station id" and "Status" text fields; columns id, orderId, outletId, prioritisedByPrincipalId, coursing as raw values.** Why: Users read order numbers, tables, people's names and the order-type words. *(source: screens/P08-venue-back-office.yaml#BO-046 / R254; Food, Beverage & Retail)*
- **Purpose reads "Show the kitchen what to make, in order" and emptyFirstRun reads "No kitchen display yet".** Why: The screen notes say it is the back-office view, not the kitchen's screen; an empty rail is "No open tickets", and an outlet without stations is a separate state. *(source: screens/P08-venue-back-office.yaml#BO-046; Food, Beverage & Retail)*
- **Overlap - BO-046, BO-020 (F&B Order Management) and KIT-001 (Kitchen Operations Command Center) all read the rail and prioritise tickets.** Why: Three rail views for one manager is what DI-671 asks to consolidate; propose folding BO-046 into BO-020 as its "Kitchen rail" tab. *(source: DI-671 / DI-987 / screens/P15-kitchen-display.yaml#KIT-001; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Station configuration on a monitoring screen - the table "Every kitchen station" and the "Save kitchen stations" action … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does the back office advance tickets at all, or only watch and prioritise? And with Allam's position that Softlabs need only an integration point to an existing KDS (DI-077) against the full P15 app, is a back-office rail view needed in r1?** → Drawn default stands (answer: "Watch + prioritise only"): Draw read-only rail plus Prioritise; no status moves from the back office. *(decided by Chinmay, 2026-10-02; DEC-180 / CHG-NOTE-004)*

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

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet and station**: Outlet picker, then station chips by name (Grill, Fryer, Cold, Beverage, Pastry) from the outlet's stations; "All stations" default. Never a "Station id" text field. *(source: contracts/satellite/fnb.yaml#listKitchenTickets / contracts/satellite/fnb.yaml#listKitchenStations)*
- **Status filter**: Chips New, Preparing, Ready, Recalled (received, preparing, ready, recalled); not a free-text field. *(source: contracts/satellite/fnb.yaml#/components/schemas/KitchenTicket)*
- **Course**: A course filter (Starters, Mains, Desserts by the outlet's course names) for table-service outlets only; hidden for quick service. With a course chosen, tickets show only that course's lines. *(source: R277 / contracts/satellite/fnb.yaml#listKitchenTickets / contracts/satellite/fnb.yaml#/components/schemas/CourseRules)*
- **Prioritise - reason**: Required, 3 to 500 characters ("VIP table, owner's guests"). Position defaults to the top of the queue; no number is asked for. *(source: contracts/satellite/fnb.yaml#prioritiseKitchenTicket / R125)*

#### Outputs: what the screen shows and produces

**Shown**

**Every kitchen ticket** (data table, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |

**The selected kitchen ticket** (detail panel, from `listKitchenTickets`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |
| Target ready at | 1 Oct 2026, 14:30 | — |
| Elapsed seconds | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save kitchen ticket status (primary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | opens modal first; produces a document or message: Advance a kitchen ticket |
| Prioritise kitchen ticket (secondary button) | `prioritiseKitchenTicket` POST `/kitchen/tickets/{ticketId}/prioritise` | inline | KitchenTicket | — | opens modal first; produces a document or message: Move a ticket up the queue |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Ticket card**: Order number (AQP-104582) and table label or buzzer number, order type in the vocabulary (Dine-in, Quick service, Room service, Collection, Delivery), covers when known, lines grouped by course with modifiers under each line, and the station it belongs to. *(source: contracts/satellite/fnb.yaml#/components/schemas/KitchenTicket / R210)*
- **Fired timer**: Counts up from when the order or course was sent (not a countdown), resets when a course is dished out, and is not shown for quick-service tickets. Colour turns to warning at the outlet's warn percentage of the service-mode target and to late beyond the target. *(source: DI-334 / contracts/satellite/fnb.yaml#/components/schemas/KitchenSla)*
- **Prioritised marker**: A small marker with who jumped the queue and why, on the card and in the detail. *(source: contracts/satellite/fnb.yaml#prioritiseKitchenTicket / MATRIX 4.6.34)*
- **Rail order**: Rendered exactly in the order returned; no sort control. *(source: contracts/satellite/fnb.yaml#listKitchenTickets)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Prioritise**: Moves the ticket to the top of the rail on every display of that station; recorded against the person. Success shows the ticket at its new place with the marker. *(source: contracts/satellite/fnb.yaml#prioritiseKitchenTicket / R125)*
- **Next move (Start, Mark ready, Recall)**: If the back office may advance tickets at all, only the one allowed next move is a button on the card; never a status dropdown. A refused move (409) names the ticket's current status and refreshes the card. *(source: contracts/satellite/fnb.yaml#setKitchenTicketStatus)*

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue)

**Where the user goes next**

- → `BO-104` Food & Beverage: *Food & Beverage*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The kitchen display list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the kitchen display untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No kitchen display yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on stationId, status and the kitchen display are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listKitchenTickets` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for `setKitchenTicketStatus`, `prioritiseKitchenTicket`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The move is not one of the four above. Names the ticket's current status. |

#### Edge cases to draw

- **Recall after the recall window**: After the venue's recall window (proposed 10 minutes from the bump) the act is a re-fire, not a recall; the button changes its label accordingly. *(source: contracts/spine/tenancy.yaml#/components/schemas/VenueSettings / R094)*
- **Connection lost**: The rail stays visible with "Last updated 20:14" and a reconnecting banner; actions queue only where offline-capable. *(source: contracts/satellite/fnb.yaml#listKitchenTickets / contracts/satellite/fnb.yaml#prioritiseKitchenTicket)*
- **The outlet has no stations configured**: Says "No kitchen stations set up for Oasis Bistro" with a link to Kitchen & Preparation Stations (BO-134), not "No kitchen display yet". *(source: screens/P08-venue-back-office.yaml#BO-134)*
- **An order is cancelled while its ticket is on screen**: The card shows Cancelled (struck through) for a moment and leaves the rail; cancelling is done on the order, not here. *(source: contracts/satellite/fnb.yaml#setKitchenTicketStatus / R125)*

#### Consistency with other screens

- Match `KIT-002`: Same ticket card anatomy, order type words, timer behaviour and colours as the station display.
- Match `KIT-001`: KIT-001 is the kitchen command centre in P15; BO-046 must not become a second command centre.
- Match `BO-020`: F&B Order Management also reads the rail and prioritises; see the overlap correction.
- Match `BO-134`: Station and display assignment is configured on BO-134 only.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro
tickets:
- number: AQP-104582
  table: T14
  type: Dine-in
  covers: 4
  course: Mains (course 2 of 3)
  fired: '12:40'
  station: Grill
  lines:
  - 2x Classic Beef Burger - medium rare, no pickles
  - 1x Lamb Ouzi
- number: AQP-104590
  buzzer: 841
  type: Quick service
  station: Fryer
  lines:
  - 3x Fries
  - 1x Halloumi Wrap - extra sauce
- number: AQP-104597
  table: T22
  type: Dine-in
  prioritised: Omar Ziad - VIP table, owner's guests
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `prioritiseKitchenTicket` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listKitchenTickets` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_MODIFY` for `setKitchenTicketStatus`, `prioritiseKitchenTicket`.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.34 | Support automatic and manual prioritization of kitchen orders based on VIP guests, memberships, Fast Pass, SLA targets, group bookings, events, or supervisor override. | Bundles and Promotions | CONTRACTED | `prioritiseKitchenTicket` |
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

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-046?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save kitchen ticket status, Prioritise kitchen ticket.
- [ ] Every transition is wired: `BO-104`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-104` Food & Beverage

**Everything in food & beverage.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `core` module |
| Block | Block A · task VM-BO-104 |
| Who uses it | venue staff holding `REPORT_VIEW_OWN`, `REPORT_VIEW_VENUE` (2 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMenus` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/food-beverage` |

**What the spec says about it.** Section landing. **4 screens reach the entry point through here** — before 20 August they reached it through nothing. **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Menu management (the menu table and Start a menu) belongs to BO-045, and getVenueSettings carries no module enablement (R279), so "What is enabled here" cannot … Removed 2 October 2026 (CHG-WIR-008): Menu management (the menu table and Start a menu) belongs to BO-045, and getVenueSettings carries no module enablement (R279), so "What is enabled here" cannot … Removed 2 October 2026 (CHG-WIR-008): Menu management (the menu table and Start a menu) belongs to BO-045, and getVenueSettings carries no module enablement (R279), so "What is enabled here" cannot …

**From the Food, Beverage & Retail process.** The Food & Beverage section landing in the back office: today's takings at the top, cards into every F&B screen (orders, order search, menus, kitchen display, stations, routing, global settings, outlets, outlet set-up) and a search across them. It carries no attention counts. One thing to get right: it is a hub, not a menu list — nothing on it should be a data table.

**Known correction pending (do not draw the wrong version)**

- **requiresModule core on the F&B hub.** Why: F&B is an optional licensed module; a tenant without it should not see an F&B hub. *(source: DI-505 / screens/P08-venue-back-office.yaml#BO-104; Food, Beverage & Retail)*
- **No way to F&B Outlets (BO-044, reached only from Venue Operations) or the pack's outlet set-up screens (BO-727–BO-733).** Why: Outlet configuration is the first F&B task (DI-330) and is unreachable from the F&B section. *(source: R251 / screens/P08-venue-back-office.yaml#BO-044; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The hub's content is an "Every menu" table with an "Outlet id" text field and an "Active at" date picker, a menu detail panel, and a "venue … (CHG-WIR-008); getVenueSettings is declared with purpose "What is enabled here". (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the F&B hub show F&B takings rather than venue takings, and drop admissions?** → The F&B hub shows F&B takings; admissions are dropped from it. *(decided by Chinmay, 2026-10-02; DEC-181 / CHG-NOTE-004)*
- **Is BO-104 or BO-727 (F&B Command Center) the F&B landing?** → Drawn default stands (answer: "BO-104 is the landing hub; BO-727 is a card on it"): BO-104 is the section hub; BO-727 is a card on it. *(decided by Chinmay, 2026-10-02; DEC-182 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
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
| Module | field | — | — | `getKpiValues` ?module |
| Date | date picker | — | — | `getServiceSummary` ?date |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Search food & beverage**: Finds F&B screens and settings by name (Menus, Outlets, Kitchen stations); not a record search. *(source: screens/P08-venue-back-office.yaml#BO-104)*

#### Outputs: what the screen shows and produces

**Shown**

**F&B takings** (detail panel, from `getServiceSummary`): **The F&B hub shows F&B takings; admissions are dropped from it (decided 2 October 2026 by Chinmay, DEC-181).** BO-104 is the F&B landing; the F&B Command Center (BO-727) is a card on it (DEC-182).

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | — |
| Covers | 1,234 | — |
| Tables | 1,234 | Table visits served. |
| Sales | AED 1,234.50 | Excluding VAT, as `grossSales` (CHG-FIN-007). |
| Tips | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Open tables | 1,234 | Visits still open, with their bills not yet settled. |

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

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **KPI tiles**: F&B takings today (the F&B outlets only), with movement against the previous period, from the seeded KPIs; the period is today in the venue time zone. Admissions are not on the F&B hub. *(source: R283 / contracts/satellite/reporting.yaml#getKpiValues / DI-041 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Section cards**: F&B Order Management, Order Search, Menu Management, Kitchen Display, Kitchen & Preparation Stations, Order Routing & KDS/Printer Rules, F&B Global Settings & Controls, F&B Outlets. No counts on the cards. *(source: R283 / screens/P08-venue-back-office.yaml#BO-104)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **New menu**: Opens Menu Management on a new menu (the outlet is picked there), not an inline create modal with an outlet id. *(source: screens/P08-venue-back-office.yaml#BO-045 / DI-330)*

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `getServiceSummary` (onLoad, F&B takings and service figures for the hub (DEC-181 …)

**Where the user goes next**

- → `BO-020` F&B Order Management: *F&B Order Management*
- → `BO-021` Order Search: *Order Search*
- → `BO-045` Menu Management: *Menu Management*
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

#### Edge cases to draw

- **Tenant without the F&B licence**: The section is not shown in the shell at all. *(source: DI-505)*
- **Outlet manager restricted to one outlet**: Cards open pre-filtered to their outlet; figures that cannot be outlet-scoped are labelled as venue figures. *(source: DI-318 / DI-331)*

#### Consistency with other screens

- Match `BO-100`: Same KPI tile component and wording as Venue Home and the other hubs.
- Match `BO-727`: The client pack's F&B Command Center is a second F&B landing; one must link to the other.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
- name: F&B takings today
  value: AED 48,960.00
  delta: +4.8% vs yesterday
cards:
- F&B Order Management
- Order Search
- Menu Management
- Kitchen Display
- Kitchen & Preparation Stations
- Order Routing & KDS/Printer Rules
- F&B Global Settings & Controls
- F&B Outlets
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getServiceSummary` → `REPORT_VIEW_OWN` (operate) · staff

**A refused user sees:** You do not have permission for food & beverage. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Food & Beverage, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-104` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-104?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-020`, `BO-021`, `BO-045`, `BO-046`, `BO-134`, `BO-135`, `BO-136`.
- [ ] Every gated control is gated: `REPORT_VIEW_OWN`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-134` Kitchen & Preparation Stations

**Kitchen & Preparation Stations — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 2 · needs the `fnb` module |
| Block | Block C · task VM-BO-134 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW` (1 configure, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listKitchenStations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `outletId` (session), `planId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/food-beverage/kitchen-preparation-stations` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `FnB Board 1.dc.html` frame `fnb-1h`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen &amp; Preparation Stations* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly. **One kitchen serves several outlets through a producing outlet (decided 2 October 2026 by Chinmay, DEC-188; CHG-CSA-015):** a station of a producing outlet can serve the outlets it produces for. Stations carry their printers.

**From the Food, Beverage & Retail process.** One outlet's kitchen set-up: its preparation stations (grill, fryer, cold, beverage, dessert), which kitchen displays show each station's rail (a primary and fallbacks in order), which items each station makes, and the outlet's kitchen targets per order type with the weights that order the rail (FNB-1H). The one thing to get right is the device-to-station assignment - it is how a kitchen display knows its station; there is no picker on the display.

**Known correction pending (do not draw the wrong version)**

- **A kitchen station has no printer and no category routing; displayEndpoint duplicates the newer displayWorkstationIds.** Why: DI-323 asks for stations mapped to printers or displays with routing by category or item; two device fields will disagree. *(source: DI-323 / contracts/satellite/fnb.yaml#/components/schemas/KitchenStation / TRACKER 30-Sep/Tracker row 28; Food, Beverage & Retail)*
- **Routing is held twice - KitchenStation.menuItemIds and MenuItem.stationId.** Why: An item could be routed to two stations or none depending on which is read; one must be the truth. *(source: contracts/satellite/fnb.yaml#/components/schemas/KitchenStation / contracts/satellite/fnb.yaml#/components/schemas/MenuItem / MATRIX 4.6.22; Food, Beverage & Retail)*
- **Plumbing - "Outlet id" text field, table "Every kitchen station" with id, outletId, menuItemIds and device ids as columns.** Why: Users read station names, display names and item counts. *(source: screens/P08-venue-back-office.yaml#BO-134 / R254; Food, Beverage & Retail)*
- **Kitchen targets are set on both BO-134 and KIT-009.** Why: Two writers of one setting; keep it here (back office) and show it read-only on the display side. *(source: contracts/satellite/fnb.yaml#setKitchenSla / screens/P15-kitchen-display.yaml#KIT-009; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): BO-134 and BO-135 both save stations (setKitchenStations), and the client board draws them as two tabs of one area ("Kitchens & Stations / … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are kitchen printers in the first release, and which models? The hardware list still says "decide later" for kitchen displays and printers.** → Kitchen printers are in release 1. *(decided by Chinmay, 2026-10-02; DEC-187 / CHG-NOTE-004)*
- **Can one kitchen serve several outlets (FNB-1H "Main Kitchen linked to 3 outlets") when the model is per outlet?** → One kitchen serves several outlets through a producing outlet (one kitchen outlet produces for several). *(decided by Chinmay, 2026-10-02; DEC-188 / CHG-NOTE-004)*

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
| Printer devices `stations[].printerDeviceIds` | multi-picker: choose printer devices | optional | — | — | — | The kitchen printers assigned to this station (Chinmay, 2 October, workbook Q187: kitchen printers are in release 1; CHG-CSA-014), as tenancy `RegisteredDevice` ids of kind … | `setKitchenStations` body |
| Serves outlets `stations[].servesOutletIds` | multi-picker: choose serves outlets | optional | — | — | — | A producing outlet's station serving other outlets (Chinmay, 2 October, workbook Q186 and Q188; DI-330; CHG-CSA-015). | `setKitchenStations` body |
| Is active `stations[].isActive` | toggle | optional | — | — | — | — | `setKitchenStations` body |

Errors to draw in the form: 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Print prep sheet** (modal, opened by *Print prep sheet*; *Print prep sheet* calls `printPrepSheet`, *Cancel* sends nothing)

**Collects what `printPrepSheet` sends before it is called.** Required: `target`. Optional: `stationIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target `target` | segmented control | required | — | Browser · Station printers | — | — | `printPrepSheet` body |
| Stations `stationIds` | multi-picker: choose stations | optional | — | — | — | Only these stations' parts. Empty means every station in the plan. | `printPrepSheet` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is not released yet (`plan-not-released`); a draft plan prints only to the browser.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet**: Outlet picker by name (from the outlet list); stations are always one outlet's set. A kitchen that serves several outlets is set up once, as a producing outlet that produces for the others. *(source: contracts/satellite/fnb.yaml#setKitchenStations / DI-330 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Station**: Name (Grill Station), short code (GRL), active toggle. *(source: contracts/satellite/fnb.yaml#/components/schemas/KitchenStation)*
- **Kitchen displays**: An ordered list of the outlet's kitchen display devices by their names: first is primary, the rest are fallbacks in order. A display already assigned to another station shows greyed with that station's name (assigning it twice is refused). *(source: R277 / DI-323 / contracts/satellite/fnb.yaml#/components/schemas/KitchenStation)*
- **Items made here**: Pick by section and item name from the outlet's menu; bulk "whole section" selection. *(source: contracts/satellite/fnb.yaml#/components/schemas/KitchenStation / MATRIX 4.6.33)*
- **Kitchen targets**: Per order type (Dine-in, Quick service, Room service, Collection, Delivery) a target in minutes (at least 1) and the warn point as a percent of it (default 80). *(source: contracts/satellite/fnb.yaml#setKitchenSla / contracts/satellite/fnb.yaml#/components/schemas/KitchenSla)*
- **What pushes a ticket up the rail**: Four weights (Age, Promise time, Table stage, VIP), whole numbers from 0, shown as sliders with their effect explained. *(source: contracts/satellite/fnb.yaml#setKitchenSla)*
- **Kitchen printers**: In release 1: each station has its kitchen printers beside its displays (the printer models are still to be named on the hardware list). *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

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
| Print prep sheet (secondary button) | `printPrepSheet` POST `/production-plans/{planId}/prep-sheet` | inline | PrepSheet | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is not released yet (`plan-not-released`); a draft plan prints only to the browser. | opens modal first; produces a document or message: Print a production plan's prep sheet |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Station rows**: Name, primary display and fallbacks, number of items routed, active. No live load percentage, open orders or average prep time. *(source: R277 / screens/P08-venue-back-office.yaml#BO-134)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save stations**: Saves the outlet's whole station set; displays switch to their assigned station's rail. A 412 says someone else changed the stations and offers reload. *(source: contracts/satellite/fnb.yaml#setKitchenStations)*
- **Save kitchen targets**: The new targets colour the rail and the new weights order it from the next refresh. *(source: contracts/satellite/fnb.yaml#setKitchenSla)*

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listKitchenStations` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setKitchenStations`, `setKitchenSla`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A workstation is assigned to more than one station (`displayWorkstationIds`, audit R277), or the body fails validation.; 409 The plan is not released yet (`plan-not-released`); a draft plan prints only to the browser. |

#### Edge cases to draw

- **The primary display is offline**: The next display in the list shows the station's rail; the station row shows which display is serving. *(source: DI-323 / contracts/satellite/fnb.yaml#/components/schemas/KitchenStation)*
- **A station is deactivated while items are routed to it**: Warn with the number of items that will have no station and require reassigning before save. *(source: designer default)*
- **A temporary move of work for tonight**: Not done here; "Move work for this service" links to the station workload screen (it reverts at close). *(source: contracts/satellite/fnb.yaml#rebalanceStationLoad / screens/P15-kitchen-display.yaml#KIT-005)*

#### Consistency with other screens

- Match `BO-135`: Routing rules and these stations are one configuration; see the overlap correction.
- Match `KIT-009`: KIT-009 also sets the kitchen targets (setKitchenSla); one owner, the other read-only.
- Match `KIT-002`: The display shows the station named here, with no station picker.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro
stations:
- name: Grill Station
  code: GRL
  displays:
  - Grill KDS 1 (primary)
  - Pass KDS (fallback)
  items: 18
- name: Fryer Station
  code: FRY
  displays:
  - Fryer KDS
  items: 9
- name: Cold Kitchen
  code: CLD
  displays:
  - Cold KDS
  items: 14
- name: Beverage
  code: BEV
  displays:
  - Bar KDS
  items: 28
targets:
- type: Dine-in
  minutes: 18
  warnAt: 80%
- type: Quick service
  minutes: 8
  warnAt: 75%
- type: Delivery
  minutes: 15
  warnAt: 80%
weights:
  age: 5
  promiseTime: 3
  tableStage: 2
  vip: 4
```

#### Permissions

- `listKitchenStations` → `PRODUCT_VIEW` (read) · staff
- `setKitchenStations` → `PRODUCT_CONFIGURE` (configure) · staff
- `setKitchenSla` → `PRODUCT_CONFIGURE` (configure) · staff
- `listOutlets` → `SCOPE_VIEW` (read) · staff
- `printPrepSheet` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listKitchenStations` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setKitchenStations`, `setKitchenSla`.

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

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 404, 409, 412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-134?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save kitchen stations, Print prep sheet.
- [ ] Every transition is wired: `BO-104`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-135` Order Routing & KDS/Printer Rules

**Order Routing & KDS/Printer Rules — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 2 · needs the `fnb` module |
| Block | Block C · task VM-BO-135 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listWorkstations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `outletId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/food-beverage/order-routing-kds-printer-rules` |

**What the spec says about it.** **Merged into BO-134** (decided 2 October 2026, Chinmay: fix the wrong wiring now; CHG-WIR-008). BO-134 and BO-135 both save stations (setKitchenStations) and the client board draws them as two tabs of one area ("Kitchens & Stations / Routing Rules"); merged into one "Kitchen stations & routing" screen, BO-134 (DI-987, DI-671; design-notes corrections fnb-retail BO-134, BO-135). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-134, and nothing on it is built separately. **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `FnB Board 1.dc.html` frame `fnb-1j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Order Routing &amp; KDS / Printer Rules* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Food, Beverage & Retail process.** Where each item's kitchen ticket goes: the rules that send an item to a station and its display, and what happens when that station's display is down. The client's frame draws ordered rules (product, then category, then outlet, then the kitchen default as fallback; first match wins) with a "test a ticket" check. The contract today routes per item to a station and falls back across that station's displays. The one thing to get right is that no item is ever left without a destination.

**Fixed on main** (the package already carries these; draw what it says): Built on listWorkstations - a table "Every workstation" with venueId, regionId, departmentId, scopePath, saleBoard, currency … (CHG-WIR-008); No routing-rule model - no rule priority, no category or outlet condition, no fallback station, no printers. (CHG-SBO-018); Overlap with BO-134 (same save operation, same board area). (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is per-item routing with display fallback enough for r1, or do we owe category rules and a fallback station (DI-323 is client-requested)?** → Kitchen routing: item routing plus category rules plus a fallback station (DI-323). *(decided by Chinmay, 2026-10-02; DEC-189 / CHG-NOTE-004)*
- **Where does an item with no station go - refused at Send to kitchen, or to a default station?** → Drawn default stands (answer: "A default station named per outlet"): To a default station named per outlet. *(decided by Chinmay, 2026-10-02; DEC-190 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search order routing | search field | — | — | — | — | — | — |

**Form: Save routing rules** (modal, opened by *Save routing rules*; *Save routing rules* calls `setKitchenRoutingRules`, *Cancel* sends nothing)

**Collects what `setKitchenRoutingRules` sends before it is called.** Required: `defaultStationId`. Optional: `categoryRules`, `fallbackStationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Category rules `categoryRules` | repeatable rows | optional | — | — | — | Tried in order; the first match wins. | `setKitchenRoutingRules` body |
| Match kind `categoryRules[].matchKind` | segmented control | required | — | Menu section · Product category | — | — | `setKitchenRoutingRules` body |
| Match value `categoryRules[].matchValue` | text field | required | — | — | — | A `MenuSection.code`, or a catalogue product category code. | `setKitchenRoutingRules` body |
| Station `categoryRules[].stationId` | picker: choose a station | required | — | — | shows names, sends the id | — | `setKitchenRoutingRules` body |
| Default station `defaultStationId` | picker: choose a default station | required | — | — | shows names, sends the id | Where a line that matches no item rule and no category rule goes (workbook Q190). | `setKitchenRoutingRules` body |
| Fallback station `fallbackStationId` | picker: choose a fallback station | optional | — | — | shows names, sends the id | Where a ticket goes when the station it routed to is inactive or every display assigned to it is down (DI-323). | `setKitchenRoutingRules` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 A station named is not this outlet's and does not serve it (`unknown-station`).

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Item routing**: A matrix of the outlet's menu sections and items against stations; assign a whole section at once, override single items. Every item must land on exactly one station. *(source: contracts/satellite/fnb.yaml#setKitchenStations / MATRIX 4.6.33 / DI-323)*
- **Fallback**: Per station, the order of displays to fall back to (from BO-134), and a fallback station (FNB-1J "else if station offline, route to Backup Grill Station"). *(source: DI-323 / screens/P08-venue-back-office.yaml#BO-135 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Test a ticket**: Pick items and see which station and display each would go to now, including any fallback in force. *(source: screens/P08-venue-back-office.yaml#BO-135)*
- **Category rules**: Route by category as well as by item; an item rule wins over its category's rule, and an item no rule covers goes to the outlet's default station. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Outputs: what the screen shows and produces

**Shown**

**Routing rules** (detail panel, from `getKitchenRoutingRules`): **Item routing, then category rules, then the default station, with a fallback station when one is down (decided 2 October 2026 by Chinmay, DEC-189, DI-323; DEC-190: a default station named per outlet).**

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | The outlet in the path. |
| Category rules | list or chips (count when long) | Tried in order; the first match wins. |
| Match kind | chip: Menu section, Product category | — |
| Match value | text | A `MenuSection.code`, or a catalogue product category code. |
| Station | the name it points at, never the id | — |
| Default station | the name it points at, never the id | Where a line that matches no item rule and no category rule goes (workbook Q190). |
| Fallback station | the name it points at, never the id | Where a ticket goes when the station it routed to is inactive or every display assigned to it is down (DI-323). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save routing rules (primary button) | `setKitchenRoutingRules` PUT `/outlets/{outletId}/kitchen-routing` | KitchenRoutingRules | KitchenRoutingRules | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 A station named is not this outlet's and does not serve it (`unknown-station`). | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Unrouted items**: A count and list of menu items with no station, shown first, with a "Route them" action. *(source: designer default)*
- **Routing summary**: Items per station; the station's displays with primary and fallback. *(source: contracts/satellite/fnb.yaml#/components/schemas/KitchenStation)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save routing**: Saves the outlet's stations with their items; tickets from the next order follow the new routing. *(source: contracts/satellite/fnb.yaml#setKitchenStations)*

**Data it reads**: `getKitchenRoutingRules` (onLoad, The routing rules in force (DEC-189))

**Where the user goes next**

- → `BO-104` Food & Beverage: *Food & Beverage*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order routing kds list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order routing kds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order routing kds yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, saleBoardKind and the order routing kds are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission the screen requires, and names it. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A station named is not this outlet's and does not serve it (`unknown-station`). |

#### Edge cases to draw

- **A new menu item is published with no station**: It appears under Unrouted items; until routed it goes to the outlet's default station (assumption to confirm). *(source: designer default)*
- **Tonight's grill is overloaded**: Not here - a temporary move by category is on the station workload screen and reverts at close. *(source: contracts/satellite/fnb.yaml#rebalanceStationLoad / screens/P15-kitchen-display.yaml#KIT-005)*

#### Consistency with other screens

- Match `BO-134`: Same stations and displays; propose one screen.
- Match `KIT-005`: Temporary rebalancing by category lives there; permanent routing here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro
routing:
- section: Burgers
  station: Grill Station
  items: 18
- section: Sides
  station: Fryer Station
  items: 14
- section: Beverages
  station: Beverage
  items: 28
- item: Halloumi Salad
  station: Cold Kitchen
unrouted:
- Truffle Fries
- Mango Lassi
```

#### Permissions

- `getKitchenRoutingRules` → `PRODUCT_VIEW` (read) · staff
- `setKitchenRoutingRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks the permission the screen requires, and names it. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

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

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 404, 412, 422).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-135?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save routing rules.
- [ ] Every transition is wired: `BO-104`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-136` F&B Global Settings & Controls

**F&B Global Settings & Controls — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Food & Beverage · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-SETUP-BO-136 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 configure, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProductionRuns` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `outletId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. A plan opened from the list. |
| Route | `/food-beverage/f-b-global-settings-controls` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **setVenueSettings replaces the whole settings row** (PUT; an omitted property returns to its default). The save sends the VenueSettings that getVenueSettings returned, with only this screen's group changed; nothing else is reset (CHG-FXS-003).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Production operations (build and release plan, the run list) and F85 step 1 belong to BO-112; their frames (fnb-2m, 2n, 5d) were attached to this settings screen … Removed 2 October 2026 (CHG-WIR-008): Production operations (build and release plan, the run list) and F85 step 1 belong to BO-112; their frames (fnb-2m, 2n, 5d) were attached to this settings screen … Removed 2 October 2026 (CHG-WIR-008): Production operations (build and release plan, the run list) and F85 step 1 belong to BO-112; their frames (fnb-2m, 2n, 5d) were attached to this settings screen …

**From the Food, Beverage & Retail process.** F&B policy for the venue (FNB-1K): which F&B actions need approval at which amount and by whom - voids, manual price changes, complimentary items, refunds, moving items between checks, re-opening a closed check - plus the venue's F&B limits (comp escalation amount, kitchen recall window, the food-safety lead). The client asked for F&B controls that configure approval workflows by amount thresholds and user privileges. The one thing to get right is showing, beside every value, the tenant default it inherits when left empty.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No setting holds the void, manual price change, refund, transfer or re-open approval bands; VenueSettings.fnb has only the comp escalation, recall window and food-safety lead. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Board frames fnb-2m (Production Planning & Sheets), fnb-2n (Central Kitchen & Commissary) and fnb-5d (Production Execution & Batch) are … (CHG-SBO-018); Production operations (buildProductionPlan, releaseProductionPlan, listProductionRuns with status, location kind and from filters) and F85 … (CHG-WIR-008); The whole VenueSettings record is shown and editable - id, currency scale, support hours, quiet hours, biometrics, segregated access … (CHG-SBO-018); requiresModule is "core" although the screen is F&B. (CHG-SBO-003).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **At which level is F&B policy set? DI-324 says globally, FNB-1K says tenant level with outlet overrides, and the contract has venue settings with tenant defaults (R094) and no outlet override.** → Drawn default stands (answer: "Default / recommended accepted"): Venue values with the tenant default shown; no outlet override in r1. *(decided by Chinmay, 2026-10-02; DEC-047 / CHG-NOTE-004)*
- **FNB-1K lists "86 an item - head chef approval", while R110 (c) makes 86 immediate. Does marking an item unavailable ever need approval?** → Drawn default stands (answer: "Default / recommended accepted"): No approval; 86 is immediate (R110 (c)). *(decided by Chinmay, 2026-10-02; DEC-048 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search f | search field | — | — | — | — | — | — |

**Form: Save course rules** (modal, opened by *Save course rules*; *Save course rules* calls `setCourseRules`, *Cancel* sends nothing)

**Collects what `setCourseRules` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Default coursing `defaultCoursing` | radio group | optional | — | Fire and forget · Hold and fire · Phased · Timed · Delayed | — | How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock … | `setCourseRules` body |
| Course names `courseNames` | list of values (chips) | optional | — | — | — | — | `setCourseRules` body |
| Auto fire minutes `autoFireMinutes` | number field (minutes) | optional | — | — | — | — | `setCourseRules` body |
| Service mode overrides `serviceModeOverrides` | key and value settings | optional | — | — | — | A different default per service mode. | `setCourseRules` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save venue settings** (modal, opened by *Save venue settings*; *Save venue settings* calls `setVenueSettings`, *Cancel* sends nothing)

**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `fnb`. Only the F&B group (recall window, comp escalation, table reserved lead, food-safety lead); the other venue settings are other screens'. Dismissing sends nothing; the screen behind is unchanged. **setVenueSettings replaces the whole settings row** (PUT; an omitted property returns to its default). The save sends the VenueSettings that getVenueSettings returned, with only this screen's group changed; nothing else is reset (CHG-FXS-003).

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
| Consent form `biometrics.consentFormId` | picker: choose a consent form | optional | — | Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access … | shows names, sends the id | The venue's own consent form, which every biometric capture is taken on (decided 2 October 2026, Chinmay, batch 4, BO-188: "Consent first, on the venue's consent form"; DEC-128 … | `setVenueSettings` body |
| Allow minors `biometrics.allowMinors` | toggle | optional | on | Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method. | — | Whether this venue enrols minors at all (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: "Guardian consent on the venue's form; minor age per country; the … | `setVenueSettings` body |
| Accreditation face matching `biometrics.accreditationFaceMatching` | group | optional | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables it, with applicant …; Enabling it is refused without `legalSignOffReference` … | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables … | `setVenueSettings` body |
| Is enabled `biometrics.accreditationFaceMatching.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Legal sign off reference `biometrics.accreditationFaceMatching.legalSignOffReference` | text field | optional | — | max length 200 | — | The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when. | `setVenueSettings` body |
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
| Charge currencies `chargeCurrencies` | list of values (chips) | optional | — | presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. | — | Which currencies a guest may select and pay in (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). | `setVenueSettings` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettings` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettings` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettings` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettings` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettings` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| … 34 more | | | | | | the rest are in `schemas.json` | `setVenueSettings` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender …

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Comp escalation amount**: Money in the venue currency; above it, comping a line needs the discount permission. Empty inherits the tenant default (proposed AED 100.00, client to correct). *(source: contracts/spine/tenancy.yaml#/components/schemas/VenueSettings / R197 / R094)*
- **Kitchen recall window**: Minutes after a bump during which the kitchen can still recall (0 to 60, proposed 10); after it a recall is a re-fire. *(source: contracts/spine/tenancy.yaml#/components/schemas/VenueSettings / R094)*
- **Food-safety lead**: A person picker (staff with food-safety rights). Required for escalations; while empty, escalating a corrective action is refused and the screen says so. *(source: R096 / contracts/satellite/fnb.yaml#escalateCorrectiveAction)*
- **Approval matrix**: Rows per action (Void, Manual price change, Complimentary item, Refund, Move items between checks, Re-open closed check) with amount bands and the role that approves each band. *(source: DI-324 / screens/P08-venue-back-office.yaml#BO-136)*

#### Outputs: what the screen shows and produces

**Shown**

**Load the outlet's course rules as saved** (card list, from `getCourseRules`)

| Shows | Format | Notes |
|---|---|---|
| Default coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to … |
| Course names | list or chips (count when long) | — |
| Auto fire minutes | 1,234 | — |
| Service mode overrides | grouped details | A different default per service mode. |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| Fnb | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save venue settings (primary button) | `setVenueSettings` PUT `/venues/{venueId}/settings` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save course rules (secondary button) | `setCourseRules` PUT `/outlets/{outletId}/course-rules` | CourseRules | CourseRules | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Inherited values**: "Inherits AED 100.00 (tenant default)" in grey under an empty field; a set value shows "Venue value" and a reset link. *(source: R094)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save F&B settings**: The settings save replaces the venue's whole settings record; the screen must send every non-F&B setting back unchanged (they are not shown here), or they revert to defaults. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*

**Data it reads**: `getVenueSettings` (onLoad, Operational settings for this venue); `getCourseRules` (onLoad, Load the outlet's course rules as saved)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_VIEW`, which `getVenueSettings` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setCourseRules`; `TENANT_CONFIGURE` for `setVenueSettings`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Edge cases to draw

- **No food-safety lead named**: A warning banner on this screen and on the food-safety views - "Escalations will be refused until a food-safety lead is named". *(source: R096 / contracts/spine/tenancy.yaml#/components/schemas/VenueSettings)*
- **The user lacks venue-configuration rights**: Read-only with the reason; never an empty page. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*

#### Consistency with other screens

- Match `POS-014`: The approval bands set here are what the till's supervisor step-up obeys (DI-324 scopes both).
- Match `BO-140`: The food-safety lead named here is who receives escalations from the food-safety views.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aqua Park
compEscalation: AED 100.00 (inherits tenant default)
recallWindow: 10 minutes
foodSafetyLead: Fatima Al Suwaidi
approvals:
- action: Void
  upTo: AED 50.00
  role: Supervisor
- action: Void
  above: AED 50.00
  role: Manager
- action: Complimentary item
  upTo: AED 100.00
  role: Supervisor
- action: Refund
  any: true
  role: Manager
```

#### Permissions

- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff
- `setCourseRules` → `PRODUCT_CONFIGURE` (configure) · staff
- `getCourseRules` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_VIEW`, which `getVenueSettings` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setCourseRules`; `TENANT_CONFIGURE` for `setVenueSettings`.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
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
| 16.9.58 | Device Incident Management - System shall support device incident management. | Device Management | CONTRACTED | data `VenueSettings` |
| … 5 more | | | | `traceability.json` |

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
- Client design-board frames: `FnB Board 1.dc.html#fnb-1k`

#### Acceptance for the design

- [ ] Every input above is drawn (84), with its required mark, default, format and its error state (400, 403, 404, 412, 422).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-136?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save venue settings, Save course rules.
- [ ] Every transition is wired: `BO-137`, `BO-104`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
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
"cancelFnbOrder": {"method":"POST","path":"/fnb-orders/{orderId}/cancel","contract":"fnb","summary":"Cancel an order","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FnbOrder"},
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"createMenu": {"method":"POST","path":"/menus","contract":"fnb","summary":"Create a menu","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateMenuRequest","responds":"Menu"},
"createModifierGroup": {"method":"POST","path":"/modifier-groups","contract":"fnb","summary":"Create a modifier group","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifierGroup","responds":"ModifierGroup"},
"getAllergenVerification": {"method":"GET","path":"/menu-items/{menuItemId}/allergen-verification","contract":"fnb","summary":"The last allergen verdict recorded for a dish","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AllergenVerdict"},
"getCourseRules": {"method":"GET","path":"/outlets/{outletId}/course-rules","contract":"fnb","summary":"How this outlet courses by default (read)","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CourseRules"},
"getFnbOrder": {"method":"GET","path":"/fnb-orders/{orderId}","contract":"fnb","summary":"Read an F&B order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"FnbOrder"},
"getKitchenRoutingRules": {"method":"GET","path":"/outlets/{outletId}/kitchen-routing","contract":"fnb","summary":"An outlet's kitchen routing rules","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"KitchenRoutingRules"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getMenu": {"method":"GET","path":"/menus/{menuId}","contract":"fnb","summary":"Read a menu with sections and items","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Menu"},
"getServiceSummary": {"method":"GET","path":"/service-summary","contract":"reporting","summary":"My service summary (a server without a till)","permission":"REPORT_VIEW_OWN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null}],"requestBody":null,"responds":"ServiceSummary"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listFnbOrders": {"method":"GET","path":"/fnb-orders","contract":"fnb","summary":"List F&B orders","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"tableVisitId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listKitchenStations": {"method":"GET","path":"/kitchen/stations","contract":"fnb","summary":"List preparation stations and their routing","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listKitchenTickets": {"method":"GET","path":"/kitchen/tickets","contract":"fnb","summary":"Kitchen ticket queue","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"stationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"course","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenuSchedules": {"method":"GET","path":"/menus/{menuId}/schedule","contract":"fnb","summary":"What is scheduled to go live, and when","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenuVersions": {"method":"GET","path":"/menus/{menuId}/versions","contract":"fnb","summary":"Every published version of a menu","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenus": {"method":"GET","path":"/menus","contract":"fnb","summary":"List menus","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listModifierGroups": {"method":"GET","path":"/modifier-groups","contract":"fnb","summary":"List modifier groups","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutlets": {"method":"GET","path":"/outlets","contract":"tenancy","summary":"List outlets","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Outlet"},
"lookupRetailSale": {"method":"GET","path":"/retail-sales/lookup","contract":"retail","summary":"Find a sale from a receipt","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"receiptNumber","in":"query","required":null},{"name":"orderNumber","in":"query","required":null},{"name":"receiptBarcode","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"printPrepSheet": {"method":"POST","path":"/production-plans/{planId}/prep-sheet","contract":"fnb","summary":"Print a production plan's prep sheet","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PrepSheet"},
"prioritiseKitchenTicket": {"method":"POST","path":"/kitchen/tickets/{ticketId}/prioritise","contract":"fnb","summary":"Move a ticket up the queue","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"publishMenu": {"method":"POST","path":"/menus/{menuId}/publish","contract":"fnb","summary":"Make the draft live, now or on a date","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuVersion"},
"recordOrderHandover": {"method":"POST","path":"/guest-orders/{orderId}/delivery","contract":"fnb","summary":"Record that an order reached the guest","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestOrderStatus"},
"rollbackMenu": {"method":"POST","path":"/menus/{menuId}/rollback","contract":"fnb","summary":"Put the previous version back","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuVersion"},
"scheduleMenuPublish": {"method":"POST","path":"/menus/{menuId}/schedule","contract":"fnb","summary":"Publish it on a date, not now","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuSchedule"},
"setCourseRules": {"method":"PUT","path":"/outlets/{outletId}/course-rules","contract":"fnb","summary":"How this outlet courses by default","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CourseRules","responds":"CourseRules"},
"setKitchenRoutingRules": {"method":"PUT","path":"/outlets/{outletId}/kitchen-routing","contract":"fnb","summary":"Set an outlet's category rules, default station and fallback station","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"KitchenRoutingRules","responds":"KitchenRoutingRules"},
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
"AllergenVerdict": {"x-ticvai-persistence":"fnb.allergen_verdict","type":"object","description":"One allergen check of one dish (decided 28 September, audit R241). Written by the server on every automatic run and by `verifyAllergens` on a manual re-check; `getAllergenVerification` reads the latest.\n","required":["menuItemId","matches","checkedAt","trigger"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"matches":{"type":"boolean"},"declared":{"type":"array","items":{"type":"string"}},"actual":{"type":"array","items":{"type":"string"}},"undeclared":{"type":"array","x-ticvai-persistence-column":"jsonb","description":"**Present in the dish and absent from the label.** The dangerous direction, and the response leads with it.\n","items":{"type":"object","properties":{"allergen":{"type":"string"},"via":{"type":"string","enum":["ingredient","substitution","modifier","sharedEquipment"]},"sourceRef":{"type":"string"}}}},"overDeclared":{"type":"array","description":"Labelled and no longer present. **Safe, and still worth fixing** — a menu that over-declares teaches guests the labels are guesses.\n","items":{"type":"string"}},"checkedAt":{"type":"string","format":"date-time","readOnly":true},"trigger":{"type":"string","readOnly":true,"description":"What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241).","enum":["manual","recipeChanged","substitutionChanged","modifierChanged"]}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n\n**A rota shift swap** (4 October 2026, CHG-FXC-008; Sprint 1-2 judging: `workforce.requestShiftSwap` raised a request\nwith no kind that fits). `configurationChange`, subject `shiftSwap`, `subjectContract` `workforce`, `subjectId` the\nShiftSwap id: an existing kind narrowed by `subjectTypes`, as the optional review steps above, so no kind is added.","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"CourseRules": {"type":"object","x-ticvai-persistence":"fnb.course_rule","description":"**An outlet's coursing default.** It was written to the resolution cache only, which the service model calls losable without consequence — an outlet's default vanished on a cache flush. One row per outlet.\n","properties":{"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet in the path."},"defaultCoursing":{"$ref":"#/components/schemas/CoursingPolicy"},"courseNames":{"type":"array","items":{"type":"string"}},"autoFireMinutes":{"type":"integer","nullable":true},"serviceModeOverrides":{"type":"object","description":"A different default per service mode.","propertyNames":{"$ref":"#/components/schemas/ServiceMode"},"additionalProperties":{"$ref":"#/components/schemas/CoursingPolicy"}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `outlet` scope."}}},
"CoursingPolicy": {"type":"string","description":"How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n","enum":["fireAndForget","holdAndFire","phased","timed","delayed"]},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"CreateFnbOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently."},"seatNumber":{"type":"integer","nullable":true,"description":"Which cover ordered it. Drives split-by-covers accurately."},"course":{"type":"integer","nullable":true,"description":"Course grouping, so the kitchen fires in sequence."},"redeemEntitlementId":{"type":"string","nullable":true,"x-ticvai-references":"access.entitlement","description":"**A meal combo redeemed at the till or by a scan** (29 September, MOB-4; applied 30 September). The entitlement a bundle's `fnbMenuItem` component issued (promotions `BundleComponent.componentKind: fnbMenuItem`, `menuItemId`, `redeemAtOutletIds`). The line is priced at zero against it, `menuItemId` must be the component's menu item and the outlet one of `redeemAtOutletIds` (or any outlet with the item on a live menu when that list is empty), and the entitlement is marked used in the same step through access `validateAccess` at the outlet. An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is refused the same way if it was used meanwhile."}}},
"CreateMenuRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","outletId"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"}}},
"FnbOrder": {"x-ticvai-persistence":"fnb.service_order + fnb.service_order_line","type":"object","required":["id","orderNumber","outletId","serviceMode","status","lines","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"paymentTiming":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/OutletPaymentTiming"}],"readOnly":true,"description":"The outlet's payment timing when the order was placed (CHG-CSA-010), kept as a snapshot."},"sentToKitchenAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the order's kitchen tickets were created. Null on a `payFirst` order not yet paid (CHG-CSA-010)."},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"lines":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/CreateFnbOrderLine"},{"type":"object","properties":{"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"orders.sales_order","description":"**Retyped 29 September (SD-046)**, and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"},"updatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both offline-sync fields, and no plain updated timestamp.\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"kitchenTicketId":{"type":"string","format":"uuid","nullable":true},"kitchenTickets":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"The kitchen tickets this order created, one per station (SD-046). Returned, not stored here; they are `fnb.kitchen_ticket` rows.","items":{"$ref":"#/components/schemas/KitchenTicket"}},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"GuestOrderStatus": {"type":"object","x-ticvai-persistence":"none — projection over kitchen_ticket","required":["orderId","status","lines"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"isReadyForCollection":{"type":"boolean"},"lines":{"type":"array","description":"Per-line status. A guest waiting on one dish should see which.","items":{"type":"object","properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}}}},
"KitchenRoutingRules": {"type":"object","x-ticvai-persistence":"fnb.kitchen_routing_rule","description":"**Where a line goes when its item names no station** (Chinmay, 2 October, workbook Q189 and Q190; DI-323; CHG-CSA-015). Item rules are `KitchenStation.menuItemIds`; these are the category rules, the default station and the fallback station of one outlet. One row per outlet.\n","required":["defaultStationId"],"properties":{"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet in the path."},"categoryRules":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Tried in order; the first match wins.","items":{"type":"object","required":["matchKind","matchValue","stationId"],"properties":{"matchKind":{"type":"string","enum":["menuSection","productCategory"]},"matchValue":{"type":"string","description":"A `MenuSection.code`, or a catalogue product category code."},"stationId":{"type":"string","format":"uuid"}}}},"defaultStationId":{"type":"string","format":"uuid","description":"Where a line that matches no item rule and no category rule goes (workbook Q190). Never refused for want of a station."},"fallbackStationId":{"type":"string","format":"uuid","nullable":true,"description":"Where a ticket goes when the station it routed to is inactive or every display assigned to it is down (DI-323)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `outlet` scope."}}},
"KitchenSla": {"type":"object","x-ticvai-persistence":"fnb.kitchen_sla","x-ticvai-primary-key":["outletId"],"description":"**How long a ticket may sit, per service mode, and what pushes it up the rail** (`setKitchenSla`). The priority weights are the ones `listKitchenTickets` orders the rail by.\n\n**Stored per outlet in `fnb.kitchen_sla`** (3 October 2026, CHG-R1S-005: the HLD/LLD cross-check found `setKitchenSla` wrote no table). One row per outlet; the targets and weights are held whole.\n","properties":{"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet, from the path. The row's key."},"targets":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","items":{"type":"object","required":["serviceMode","targetMinutes"],"properties":{"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"targetMinutes":{"type":"integer","minimum":1},"warnAtPercent":{"type":"integer","default":80}}}},"priorityWeights":{"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The weight of each signal the board names — age, promise time, table stage, a VIP marker.","properties":{"age":{"type":"integer","minimum":0},"targetReadyAt":{"type":"integer","minimum":0,"description":"Promise time."},"tableStage":{"type":"integer","minimum":0},"vip":{"type":"integer","minimum":0}}}}},
"KitchenStation": {"x-ticvai-persistence":"fnb.kitchen_station","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"menuItemIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Items routed to this station."},"displayWorkstationIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**The kitchen displays assigned to this station** (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks after it. Set with `setKitchenStations`. A display reads the rail for the station it is assigned to (`listKitchenTickets`). A workstation is assigned to at most one station; a second assignment is refused `400`.\n"},"displayEndpoint":{"type":"string","nullable":true,"description":"The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station, with a fallback device where the primary is down — 18 Aug minute). Absent where the station has no display assigned.\n"},"printerDeviceIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**The kitchen printers assigned to this station** (Chinmay, 2 October, workbook Q187: kitchen printers are in release 1; CHG-CSA-014), as tenancy `RegisteredDevice` ids of kind `receiptPrinter` or `labelPrinter`. A station may have printers, displays or both; a ticket for a station with printers is printed there as well as shown, and `printPrepSheet` sends the station's part of a prep sheet to them.\n"},"servesOutletIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**A producing outlet's station serving other outlets** (Chinmay, 2 October, workbook Q186 and Q188; DI-330; CHG-CSA-015). `outletId` is the producing outlet (the commissary or main kitchen); the outlets listed here route their orders to this station as if it were their own. Empty, the default, means the station serves only its own outlet.\n"},"isActive":{"type":"boolean"}}},
"KitchenTicket": {"x-ticvai-persistence":"fnb.kitchen_ticket + fnb.kitchen_ticket_line","type":"object","required":["id","orderId","outletId","status","lines","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"coursing":{"allOf":[{"$ref":"#/components/schemas/CoursingPolicy"}],"nullable":true,"description":"BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"},"buzzerCode":{"type":"string","nullable":true,"description":"BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"},"priority":{"type":"integer","description":"Higher fires sooner. Raised by Fast Pass or supervisor override."},"prioritisedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"prioritiseReason":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","status"],"properties":{"lineId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"refireOfLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."},"refireReason":{"allOf":[{"$ref":"#/components/schemas/RefireReason"}],"nullable":true,"readOnly":true},"isChargeable":{"type":"boolean","nullable":true,"readOnly":true,"description":"A refire's `chargeable` flag. Null on a line that is not a refire."},"course":{"type":"integer","nullable":true},"stationId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}},"createdAt":{"type":"string","format":"date-time"},"targetReadyAt":{"type":"string","format":"date-time","nullable":true},"elapsedSeconds":{"type":"integer"},"visitId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The table visit the ticket is for** (4 October 2026, CHG-FXC-011; KIT-002): the `{visitId}` `notifyServer` takes. Null for a counter or delivery order with no visit."}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuActionResult": {"type":"object","x-ticvai-persistence":"none — response shape","description":"**The preview, or what was applied** (`applyMenuActions`). The same shape either way, so the screen that showed the preview shows the result.\n","required":["applied","actions"],"properties":{"applied":{"type":"boolean","description":"False for a preview (`previewOnly`), true once applied."},"actions":{"type":"array","items":{"type":"object","required":["index","kind","affectedItemCount"],"properties":{"index":{"type":"integer","description":"The action's position in the request."},"kind":{"type":"string","enum":["reprice","retire","activate","moveSection","setAvailability","setTax"]},"affectedItemCount":{"type":"integer","description":"**How many items it touches** — the number the preview exists to show."},"affectedMenuItemIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"appliedAt":{"type":"string","format":"date-time","nullable":true}}},
"MenuActionSelector": {"type":"object","description":"**Which items a bulk action touches.** At least one criterion; several narrow each other. *Reprice all* and *reprice all in this section* are different selectors on purpose, and the preview says how many items each one reaches.\n","minProperties":1,"properties":{"menuItemIds":{"type":"array","items":{"type":"string","format":"uuid"}},"sectionCodes":{"type":"array","description":"`MenuSection.code` values on this menu.","items":{"type":"string"}},"allItems":{"type":"boolean","description":"Every item on the menu. Stated rather than implied by an empty selector."}}},
"MenuActionValue": {"type":"object","description":"What the action sets. **One field per kind**: `reprice` takes `percentChange` or `price`; `moveSection` takes `toSectionCode`; `setAvailability` takes `isAvailable`; `setTax` takes `taxCode`; `retire` and `activate` take none.\n","properties":{"percentChange":{"type":"number","description":"Signed. `-5` is five per cent off."},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"toSectionCode":{"type":"string"},"isAvailable":{"type":"boolean"},"taxCode":{"type":"string","description":"A tax code from the finance tax engine."}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"**The catalogue variant this item links to, for reporting, stock and tax class only. It is not where the price comes from** (Chinmay, 2 October, workbook Q34; CHG-CSA-009). F&B owns its own catalogue: F&B prices were migrated into the F&B service so ticketing scales as an isolated service (ADR-0028), and the price an outlet sells at is `price` on this item. The central catalogue prices tickets and single-price booths; it never reprices a dish. A menu belongs to one outlet, so `price` is that outlet's price, and an outlet may set its own; it changes through `updateMenu`, `setMenuSections` or `applyMenuActions` (`reprice`). Tax is computed on the order line by the tax engine. (Replaces the earlier text \"pricing and tax come from there — a menu is a presentation of the catalogue\", which was stale.)\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"dailyCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**How many portions the kitchen set for today** (`setMenuItemDailyCount`; Chinmay, 2 October, workbook Q194; CHG-CSA-017). Null means the item is not counted. Reset at the venue day start.\n"},"remainingCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**What is left of `dailyCount`** (\"6 left\" on the till and the guest menu). Each sale takes from it; **at zero the item is marked unavailable automatically**, with an `EightySixEvent` whose `source` is `dailyCount`. Null where the item is not counted.\n"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MenuSchedule": {"type":"object","x-ticvai-persistence":"fnb.menu_schedule","description":"**A publish dated for later** (`scheduleMenuPublish`, or `publishMenu` with an `effectiveAt`). Listed by `listMenuSchedules` while `pending`, so a venue with three scheduled price changes can see them; one per menu per date.\n","required":["id","menuId","effectiveAt","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"menuId":{"type":"string","format":"uuid"},"effectiveAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["pending","applied","cancelled"]},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` that went live when the schedule fired. Null until then."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"cancelledAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"MenuVersion": {"type":"object","x-ticvai-persistence":"fnb.menu_version","description":"**One published state of a menu, kept.** `publishMenu` writes one, `rollbackMenu` writes a new one from an older one, and `listMenuVersions` reads them — the previous version stays readable, which is what makes rollback and *what were we charging at noon* possible. **A version is never edited**; a menu history that can be edited cannot answer a refund dispute.\nStatuses follow flow F31: a new version is `draft` while the live one keeps selling, `scheduled` once dated, `live`, and `superseded` when a later version goes live.\n","required":["id","menuId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"menuId":{"type":"string","format":"uuid"},"version":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","scheduled","live","superseded"]},"effectiveAt":{"type":"string","format":"date-time","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"restoredFromVersion":{"type":"integer","nullable":true,"description":"Set on a version written by `rollbackMenu` — the version it restored."},"channels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"note":{"type":"string","nullable":true},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","description":"The sections and items as published. The snapshot, not a reference to the live rows.","items":{"$ref":"#/components/schemas/MenuSection"}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"ModifierGroup": {"x-ticvai-persistence":"fnb.modifier_group + fnb.modifier_option","type":"object","description":"**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n","required":["id","code","name","minSelections","maxSelections","options"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"minSelections":{"type":"integer","minimum":0,"description":"Greater than zero makes the group required."},"maxSelections":{"type":"integer","minimum":1},"options":{"type":"array","minItems":1,"items":{"type":"object","required":["id","name","priceDelta"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isDefault":{"type":"boolean"},"isAvailable":{"type":"boolean"},"allergens":{"type":"array","description":"What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."},"endsNextDay":{"type":"boolean","default":false,"description":"**A late-night window is one window past midnight** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). A bar open 23:00 to 01:00 on Friday is `day: fri`, `from: '23:00'`, `to: '01:00'`, `endsNextDay: true`: one service period, and its takings belong to Friday's trading day, not split across two days. With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours.\n"}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200,"description":"The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005)."},"nameTranslations":{"$ref":"#/components/schemas/OutletNameTranslations"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"outletType":{"allOf":[{"$ref":"#/components/schemas/OutletType"}],"nullable":true,"description":"The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail."},"departmentId":{"type":"string","format":"uuid","nullable":true,"description":"**The department the outlet belongs to** (DI-319: department, sub-department, cost centre and status; DEC-196; CHG-CSP-005): an `OrgUnit` of kind department, as `Workstation.departmentId`. The outlet itself is the sub-department, so it needs no second field.\n"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"paymentTiming":{"allOf":[{"$ref":"#/components/schemas/OutletPaymentTiming"}],"default":"sendFirst","description":"Pay first, or send to the kitchen first then pay (DEC-064; CHG-CSP-004)."},"admissionContext":{"allOf":[{"$ref":"#/components/schemas/OutletAdmissionContext"}],"default":"insideVenue","description":"Inside the venue (needs an admission ticket) or standalone (no ticket) (DEC-070; CHG-CSP-004)."},"producesForOutletIds":{"type":"array","default":[],"description":"**One kitchen serving several outlets is a producing outlet** (decided 2 October 2026, Chinmay, batch 6 set 5, BO-134: \"Yes: via a producing outlet (one kitchen outlet produces for several)\"; DEC-188; CHG-CSP-005). The outlets this one prepares food for, in the same venue. The model stays per outlet (DI-330): each outlet keeps its own menu and stations, and an order at a listed outlet may route to this outlet's kitchen stations (fnb `KitchenStation`). Empty on an outlet that only produces for itself. An outlet may not list itself, an outlet of another venue (`422 outlet-not-in-venue`), or one that lists it back.\n","items":{"type":"string","format":"uuid"}},"saleBoardId":{"type":"string","format":"uuid","nullable":true,"description":"**The till layout every till in this outlet uses, unless a till overrides it** (decided 2 October 2026, Chinmay, batch 6 set 4, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006). DI-326 puts the layout at the outlet; MATRIX 2.1.9 binds a board to a workstation. Both hold: a workstation with no board of its own (`ConfigureWorkstationRequest.saleBoardId` absent or null) uses this one, and `Workstation.saleBoardSource` says which applied.\n"},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletAdmissionContext": {"type":"string","description":"**Whether an outlet sits behind the admission gate** (decided 2 October 2026, Chinmay, batch 1, WEB-036: \"Inside the venue, a ticket is needed. A restaurant outside the venue (standalone) can sell without one\"; DEC-070; CHG-CSP-004). `insideVenue` (the default): a guest ordering food needs an admission ticket or a place inside, as DI-292 (14 August) decided. `standalone`: a restaurant outside the gate, which may sell takeaway and delivery (DI-1039) with no ticket. DI-292 is amended for standalone outlets only. The admission check itself stays in Access (ADR-0068). F&B keeps its own payment and its own receipt either way. **The canonical name** (2 October 2026, CHG-CLN-008): the field is `admissionContext` on the outlet and on F&B's guest `DiningOutlet`; common `OutletSiting` and the word \"siting\" are deprecated aliases of this.\n","enum":["insideVenue","standalone"]},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"OutletNameTranslations": {"type":"object","x-ticvai-persistence":"none — jsonb column on platform.outlet","description":"**The outlet's name in other languages, keyed by ISO 639-1 code** (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: \"Yes, where a country needs it: the local language plus English\"; DEC-031; CHG-CSP-005). `Outlet.name` stays the English name. Where the region requires a local name (`RegionSettings.localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. The same shape as catalogue's `LocalisedText` (DI-210).\n","additionalProperties":{"type":"string","maxLength":200}},
"OutletPaymentTiming": {"type":"string","description":"**When an F&B order is paid, set per outlet** (Chinmay, 2 October, workbook Q64; refines audit R261 per outlet; CHG-CSA-010). `sendFirst`, the default and R261's rule: the order goes to the kitchen, then the till charges (table service, and quick service where the venue wants the kitchen started while the guest pays). `payFirst`: the till charges before anything reaches the kitchen; an unpaid order at a `payFirst` outlet is never sent (`fnb.createFnbOrder`, `fnb.fireCourse`). Shared because the outlet (tenancy `Outlet`) holds it and F&B enforces it.\n","enum":["sendFirst","payFirst"],"default":"sendFirst"},
"OutletType": {"type":"string","description":"**How an F&B or retail outlet trades, which switches features on or off** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-729: \"Add both fields: outlet type and department (DI-319)\"; DEC-196; CHG-CSP-005). DI-319: a quick-service outlet needs no table booking, a fine-dining outlet needs a table layout. `kind` stays the physical place (a shop, a restaurant, a kiosk); this is the service model inside it. `commissary` is a producing kitchen (DEC-186, DEC-188).\n","enum":["fineDining","casualDining","quickService","coffeeShop","barLounge","foodCourt","buffet","commissary","retail"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PrepSheet": {"type":"object","x-ticvai-persistence":"none — rendered from the production plan and the template","description":"A production plan rendered through the venue's prep-sheet template (`printPrepSheet`, CHG-CSA-014).","required":["planId","sections"],"properties":{"planId":{"type":"string","format":"uuid"},"renderedAt":{"type":"string","format":"date-time"},"sections":{"type":"array","items":{"type":"object","properties":{"stationId":{"type":"string","format":"uuid","nullable":true},"title":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"item":{"type":"string"},"plannedQuantity":{"type":"number"},"suggestedQuantity":{"type":"number","nullable":true},"unit":{"type":"string"},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}}}}}},"printedTo":{"type":"array","description":"The printers each station's part was sent to (`target` `stationPrinters`).","items":{"type":"object","properties":{"stationId":{"type":"string","format":"uuid"},"deviceId":{"type":"string","format":"uuid"}}}},"notPrinted":{"type":"array","description":"Stations in the plan with no printer assigned; never silently skipped.","items":{"type":"string","format":"uuid"}}}},
"RefireReason": {"type":"string","description":"Why a line was made again (`refireItem`). The reasons are the data.","enum":["overcooked","undercooked","wrongItem","dropped","cold","allergyRisk","guestChangedMind","lateAdd"]},
"RetailSale": {"x-ticvai-persistence":"retail.sale + retail.sale_line","type":"object","required":["id","receiptNumber","orderId","outletId","lines","grossAmount","createdAt"],"properties":{"id":{"type":"string"},"receiptNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Each till holds a reserved range of the venue's sequence, so a sale made offline prints its number at once and the server accepts it on sync. **Not gapless**: an unused reserved number is skipped, not reissued. Only tax invoices are gapless, per legal entity.\n"},"orderId":{"type":"string","description":"The order in the Order & Payment context. Retail does not keep its own ledger."},"outletId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"merchandiseId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"serialNumbers":{"type":"array","items":{"type":"string"}},"returnedQuantity":{"type":"integer"},"isReturnable":{"type":"boolean","description":"False once the window has passed or the line is fully returned."},"notReturnableReason":{"type":"string","nullable":true}}}},"subtotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"net_amount"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reprintCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"}}},
"SalesChannel": {"type":"string","description":"**Where a sale came from.** Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing.\n**Not interchangeable with the local `Channel` enums.** `catalogue.Channel` and `orders.Channel` are byte-identical duplicates of each other listing `pos, kiosk, web, mobile, b2b, ota, callCentre`; `orders.OrderChannel` lists `guestApp, guestWeb, partner, api, backOffice` on top. **Pointing the nine at a local enum would silently narrow them** — and the duplication between the two `Channel` enums is the reason a shared one existed in the first place.\n**This is the reporting dimension**: attribution, promotion eligibility and settlement all group by it, which is why it has to mean the same thing in `orders`, `catalogue`, `subscription` and `marketing-crm` rather than four things that nearly line up.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice","b2b","ota"]},
"ServiceMode": {"type":"string","enum":["quickService","tableService","roomService","collection","delivery"]},
"ServiceSummary": {"x-ticvai-persistence":"none — computed from fnb.table_visit, the orders and payments on it","type":"object","description":"One server's service day (`getServiceSummary`, CHG-CSA-020).","required":["date","covers","tables"],"properties":{"date":{"type":"string","format":"date"},"covers":{"type":"integer"},"tables":{"type":"integer","description":"Table visits served."},"sales":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Excluding VAT, as `grossSales` (CHG-FIN-007)."},"tips":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openTables":{"type":"integer","description":"Visits still open, with their bills not yet settled."}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}}
}
```
