# P08-stock-supply-01 — P08 · Stock & Supply (1 of 2)

**10 screens · 52 operations · 37 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `APPROVAL_ACT, LEDGER_APPROVE, LEDGER_POST, LEDGER_VIEW, PROCUREMENT_MANAGE, PROCUREMENT_RECEIVE, PROCUREMENT_REQUEST, PROCUREMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `BO-049` | Stock Levels | B–D | 18 | 23 | 6 | 34 | 2 | 4 | — | notStarted (generated) |
| `BO-050` | Stock Position & Valuation | B–D | 0 | 12 | 5 | 12 | 2 | 4 | — | notStarted (generated) |
| `BO-051` | Purchase Orders | B–D | 22 | 14 | 6 | 12 | 1 | 4 | — | notStarted (generated) |
| `BO-052` | Goods Receipt | B–D | 19 | 19 | 6 | 12 | 1 | 0 | — | notStarted (generated) |
| `BO-078` | Requisitions | B–D | 23 | 26 | 6 | 16 | 3 | 0 | — | notStarted (generated) |
| `BO-079` | Stock Count | B–D | 28 | 18 | 6 | 8 | 0 | 4 | — | notStarted (generated) |
| `BO-080` | Stock Transfers | B–D | 18 | 12 | 6 | 8 | 2 | 4 | — | notStarted (generated) |
| `BO-081` | Inventory Items | A | 33 | 18 | 6 | 33 | 2 | 4 | — | notStarted (generated) |
| `BO-082` | Stock Movements | B–D | 14 | 16 | 6 | 18 | 0 | 4 | — | notStarted (generated) |
| `BO-083` | Suppliers | B–D | 36 | 13 | 6 | 7 | 1 | 4 | — | notStarted (generated) |

## Thin screens in this batch

**BO-050 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-049` Stock Levels

**Know what is on the shelf and what is on order.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure); in the flows as storekeeper |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listStockLocations` reads the population and `getStockPositions` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `itemId` (deepLink) · cold entry: An item opened from the catalogue. |
| Route | `/venue-operations/stock-levels` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): F&B Stock & Operations Command Center; Outlet Stock & Ingredient Availability. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): "Save item availability" (the F&B 86 operation) acts on a menu item, not a stock item, and has its own screen (BO-140) (R254, R110; design-notes correction …

**From the Food, Beverage & Retail process.** Stock Levels answers "what is on the shelf, and where" for one venue: on hand, allocated and available, by item and by stock location, valued where the user may see value. It is the storekeeper's start screen (F92 step 1) and the place a short store raises a transfer (F35 step 1). The one thing to get right is that available is on hand minus allocated, and a negative position is shown as negative, never hidden or clamped to zero.

**Known correction pending (do not draw the wrong version)**

- **The main list is "Every stock location" (location rows with id, code, parent id, active). Stock positions sit only in a side panel.** Why: The screen's purpose is what is on the shelf. Positions are the list; locations are a filter (tree). Raw id columns leak plumbing. *(source: screens/P08-venue-back-office.yaml#BO-049 / R254; Food, Beverage & Retail)*
- **"No results" is declared as never shown because the location list takes no filter.** Why: Stock positions do take filters (location, item, include zero), so a filter that matches nothing is a real state. *(source: contracts/satellite/inventory.yaml#getStockPositions; Food, Beverage & Retail)*
- **The first-run state offers "Create stock transfer".** Why: With no items or locations there is nothing to transfer. First run should point to setting up locations and items (BO-081). *(source: designer default; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): "Save item availability" (the F&B 86 operation, setItemAvailability) is the primary button. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The client's command centre asks for "low-stock / critical / out-of-stock". The contract has only "below reorder point" and zero. What makes an item "critical"?** → Drawn default accepted: Draw two flags, "Below reorder point" and "Out of stock". No "Critical" badge until it is defined. *(decided by Chinmay, 2026-10-02; DEC-284 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Does Allocated include merchandise held for collection and online orders awaiting pickup or shipment, or only inventory stock reservations?** → Drawn default accepted: Draw Allocated as one number, with a tooltip "Reserved for orders and collections". *(decided by Chinmay, 2026-10-02; DEC-285 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |
| As at | date picker | — | — | `getStockValuation` ?asAt |
| Location | picker: choose a location | — | — | `getStockValuation` ?locationId |

**Form: Create stock transfer** (modal, opened by *Create stock transfer*; *Create stock transfer* calls `createStockTransfer`, *Cancel* sends nothing)

**Collects what `createStockTransfer` sends before it is called.** Required: `id`, `fromLocationId`, `toLocationId`, `lines`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| From location `fromLocationId` | picker: choose a from location | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| To location `toLocationId` | picker: choose a to location | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createStockTransfer` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `createStockTransfer` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `createStockTransfer` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `createStockTransfer` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockTransfer` body |

Errors to draw in the form: 409 Insufficient stock at the source

**Form: Create stock movement** (modal, opened by *Create stock movement*; *Create stock movement* calls `createStockMovement`, *Cancel* sends nothing)

**Collects what `createStockMovement` sends before it is called.** Required: `id`, `itemId`, `locationId`, `kind`, `quantity`, `recordedAt`. Optional: `unit`, `reason`, `costCenterId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createStockMovement` body |
| Item `itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createStockMovement` body |
| Location `locationId` | picker: choose a location | required | — | — | shows names, sends the id | — | `createStockMovement` body |
| Kind `kind` | select | required | — | Receipt · Issue · Sale depletion · Waste · Adjustment in · Adjustment out · Transfer out · Transfer in · Count gain · Count loss · Supplier return · Production | — | The kind decides the direction (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` (the finished item entering stock; the … | `createStockMovement` body |
| Quantity `quantity` | number field | required | — | more than 0 | — | Always positive. The `kind` decides whether it adds or removes stock, not the sign (decided 28 September, audit R171). | `createStockMovement` body |
| Unit `unit` | text field | optional | — | — | — | — | `createStockMovement` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required for `adjustmentIn`, `adjustmentOut` and `waste` (decided 28 September, audit R171); adjustments are reported separately. | `createStockMovement` body |
| Cost center `costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | — | `createStockMovement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockMovement` body |

Errors to draw in the form: 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock, and the item does not permit negative balances

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Location**: A tree picker over the venue's stock locations, following the warehouse hierarchy (for example Main Store > Food Store > Cold Room). Choosing a parent includes its children. Default is "All locations". Never a text field for an id. *(source: DI-345 / contracts/satellite/inventory.yaml#/components/schemas/StockLocation)*
- **Item search**: Name, SKU or barcode, with scan support on a device that has a scanner. Sends the chosen item as the item filter. *(source: contracts/satellite/inventory.yaml#lookupInventoryItem / DI-233)*
- **Show zero stock**: Off by default. On, it lists items with nothing on hand at the location (the out-of-stock check). *(source: contracts/satellite/inventory.yaml#getStockPositions / DI-340)*

#### Outputs: what the screen shows and produces

**Shown**

**Every stock location** (data table, from `listStockLocations`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Main store, Sub store, Kitchen, Bar, Retail floor, Cellar… | — |
| Is active | yes / no (icon or chip) | — |

**The selected stock location** (detail panel, from `listStockLocations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Main store, Sub store, Kitchen, Bar, Retail floor, Cellar… | — |
| Parent location | the name it points at, never the id | — |
| Is active | yes / no (icon or chip) | — |

**The stock valuation** (detail panel, from `getStockValuation`)

| Shows | Format | Notes |
|---|---|---|
| As at | 1 Oct 2026 | — |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| By location | list or chips (count when long) | — |
| By category | list or chips (count when long) | — |

**The stock position** (detail panel, from `getStockPositions`)

| Shows | Format | Notes |
|---|---|---|
| Item name | text | — |
| SKU | text | — |
| Location name | text | — |
| On hand | 1,234.5 | — |
| Allocated | 1,234.5 | Reserved for orders: the quantity under an active stock reservation for an order (decided 28 September, audit R171). |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Last counted at | 1 Oct 2026, 14:30 | — |
| Last movement at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create stock transfer (secondary button) | `createStockTransfer` POST `/stock-transfers` | CreateStockTransferRequest | StockTransfer | 409 Insufficient stock at the source | opens modal first |
| Create stock movement (secondary button) | `createStockMovement` POST `/stock-movements` | CreateStockMovementRequest | StockMovement | 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock, and the item does not permit negative balances | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Stock table (the main list)**: One row per item and location: item name, SKU, location, On hand, Allocated, Available, unit, value, last counted, last movement. Show Available most prominently, because it is what a sale or an issue can still draw on. Label the three numbers "On hand", "Allocated" and "Available", never "Inventory". Sort by Available ascending so problems come first. *(source: R171 / DI-361 / contracts/satellite/inventory.yaml#/components/schemas/StockPosition)*
- **Negative positions**: Shown with a minus sign and an alert colour, for example "-4 pcs". Never shown as 0. A position that cannot go negative hides an oversell that already happened. *(source: F35 step 6)*
- **Low / out of stock flags**: "Below reorder point" when the item's flag is set. "Out of stock" when on hand is zero or less. These are the client's command-centre indicators. *(source: DI-340 / DI-345 / contracts/satellite/inventory.yaml#/components/schemas/InventoryItem)*
- **Stock value panel**: Total value as at today, by location and by category, in AED with 2 decimals. Visible only to users who hold the ledger-view right. For others the value column and panel are absent (not zero). Valued by each item's own costing method, so the panel carries the note "Valued at each item's costing method (weighted average or FIFO)". *(source: contracts/satellite/inventory.yaml#getStockValuation / DI-344)*
- **In transit**: Stock dispatched on a transfer and not yet received belongs to neither location. Show it as a separate "In transit" line in the value panel, so the totals reconcile. *(source: contracts/satellite/inventory.yaml#createStockTransfer)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Transfer stock**: Opens the transfer form with the selected item and its location prefilled as the source (Stock Transfers, BO-080, owns the full form). The server refuses with "Not enough stock at <location>" when the source is short. Success shows the transfer number and the item as "In transit". *(source: F35 step 1 / contracts/satellite/inventory.yaml#createStockTransfer)*
- **Adjust stock**: Opens the adjustment form (Stock Movements, BO-082, owns it): Adjustment in, Adjustment out, Waste or Issue, with a positive quantity and a required reason. The list refreshes with the new balance. *(source: R171 / contracts/satellite/inventory.yaml#createStockMovement)*
- **Open item / Count this item**: Row links to the item record (BO-081) and to Stock Count (BO-079) to start a spot count on that item. *(source: F92 step 1 / F35 step 8)*

**Data it reads**: `getStockPositions` (onLoad, Stock on hand by item and location); `getStockValuation` (onLoad, Stock value by location and category); `listStockLocations` (onLoad, List stock locations)

**Where the user goes next**

- → `BO-082` Stock Movements: *The four orders are sourced from another store instead*; calls `createStockMovement`
- → `BO-079` Stock Count: *Stock Count*
- → `BO-080` Stock Transfers: *Stock Transfers*; carries `transferId`
- → `EMP-065` Receiving: *The delivery arrives*; carries `transferId`
- → `BO-081` Inventory Items: *Inventory Items*; carries `itemId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stock levels list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stock levels untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stock levels yet. Offers Create stock transfer (`createStockTransfer`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listStockLocations` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires to show this screen, and names that permission (the screen's other reads need `LEDGER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createStockTransfer` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock at the source; 409 Insufficient stock, and the item does not permit negative balances |

#### Edge cases to draw

- **The user has stock rights but not the ledger-view right**: Quantities show and value is hidden. This is a partial-access state, not an error. The no-access state applies only when stock positions themselves are refused. *(source: contracts/satellite/inventory.yaml#getStockValuation / contracts/satellite/inventory.yaml#getStockPositions)*
- **Online orders already took stock that a delivery was expected to cover (oversell)**: The position goes negative and the row says so. Nothing on this screen refuses it. Resolution is a transfer from another store, or a refund recorded as an oversell. *(source: F35 step 5 / F35 step 6)*
- **Offline device**: Positions read from cache with a "Last updated hh:mm" stamp. Adjustments are not offered offline, because stock depletion is real time. *(source: contracts/satellite/inventory.yaml#getStockPositions / contracts/satellite/inventory.yaml#createStockMovement)*

#### Consistency with other screens

- Match `EMP-062`: The same three numbers with the same labels, in the same order (On hand · Allocated · Available).
- Match `POS-023`: Available here is what the till and web shop sell against. A sale is gated on system stock per venue, not physical stock.
- Match `BO-050`: The value panel and BO-050 use one valuation read. Same figures, same "as at" date.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
locations:
- Main Store
- Main Store > Food Store
- Main Store > Beverage Store
- Oasis Bistro Kitchen
- Pool Bar
- Marina Bay Retail Floor
rows:
- item: Coca-Cola 330 ml can
  sku: BEV-CC-330
  location: Pool Bar
  onHand: 182
  allocated: 0
  available: 182
  unit: can
  value: AED 345.80
- item: Full-cream milk 2 L
  sku: DRY-MLK-2L
  location: Oasis Bistro Kitchen
  onHand: 6
  allocated: 0
  available: 6
  unit: bottle
  flag: Below reorder point
- item: Aqua Park logo T-shirt, green, M
  sku: TSH-AQP-GRN-M
  location: Marina Bay Retail Floor
  onHand: 3
  allocated: 7
  available: -4
  unit: pcs
  flag: Negative
valuation:
  asAt: '2026-10-14'
  total: AED 412,906.35
  inTransit: AED 3,120.00
```

#### Permissions

- `getStockPositions` → `PRODUCT_VIEW` (read) · staff
- `getStockValuation` → `LEDGER_VIEW` (read) · staff
- `createStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff
- `createStockMovement` → `PRODUCT_CONFIGURE` (configure) · staff
- `listStockLocations` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires to show this screen, and names that permission (the screen's other reads need `LEDGER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createStockTransfer` …

#### Requirements it meets

34 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.9 | The system should allow multi-store retailing where the stores are connected with the inventory information of other stores. This should allow the guests to order items which are out of stock in the … | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 4.4.14 | Support multiple warehouses, stores, kiosks, stock rooms, and inventory locations with centralized visibility. | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 4.4.25 | Maintain one inventory source across POS, B2C, B2B, Mobile App, Kiosks, APIs, and future channels with real-time synchronization. | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 15.1.9 | Real-Time Inventory Tracking - System shall track inventory levels in real time. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.10 | Multi-Location Inventory - System shall support inventory across multiple locations. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.11 | Multi-Warehouse Inventory - System shall support multiple warehouses. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.12 | Available Stock Tracking - System shall track available stock. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.13 | Reserved Stock Tracking - System shall track reserved inventory. | Inventory Management | CONTRACTED | `getStockPositions` |
| 18.7.1 | Inventory Lookup - Users shall view inventory availability. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.2 | Stock Count - Users shall perform stock counts. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.3 | Inventory Transfers - Users shall execute inventory transfers. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.4 | Goods Receipt - Users shall record goods receipt transactions. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| … 22 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Warehouse/location structure is a customisable hierarchy (e.g. main warehouse → food warehouse → beverage warehouse), with stock received centrally or directly at an outlet/kitchen for fast-moving perishables. Expiry is tracked at batch/date level; reorder alerts notify staff at a minimum threshold. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-345)*
- F&B Stock Command Center shows stock value, low-stock/critical/out-of-stock items and recipe-based ingredient consumption. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-340)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-049` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 5.dc.html#fnb-5a`, `FnB Board 5.dc.html#fnb-5b`, `Retail Board 4.dc.html#ret-4a`, `Retail Board 4.dc.html#ret-4h`, `Inventory Board 1.dc.html#inv-7`, `Inventory Board 1.dc.html#inv-9`
- Flow F35 *Stock arrives short and an oversell is resolved*, step 1: The store is short. A transfer is raised against a store that has it. → **`findNearbyStock` was the board's word and `listStockLocations` is the operation.** A transfer moves stock between locations; a requisition asks a supplier.
- Flow F35 *Stock arrives short and an oversell is resolved*, step 5: The website has already sold four of the damaged units. → **An oversell, and it is nobody's mistake.** The stock was committed against a delivery that was in transit and arrived broken — **allocation against expected stock is what makes online selling …
- Flow F35 *Stock arrives short and an oversell is resolved*, step 6: The stock goes negative and stays negative. → **A movement is written either way.** A stock level that refuses to go negative is a stock level that hides what happened — the same rule F33 applies to an offline oversell.
- Flow F92 *Store stock is watched, replenished and reconciled*, step 1: Stock Levels. → **Drawn by the client as RET-4A.**
- Flow F35 branch at step 5 (high): when No other store has the line., **The orders are refunded, and the reason is recorded as an oversell rather than a cancellation.** A venue that logs both the same way cannot tell a supply failure from a change of mind.
- Flow F35 branch at step 6 (high): when The negative position crosses the venue's write-off threshold., Routes through `createApprovalRequest`. **One approval mechanism, different subjects** — the same path a stock write-off, a menu repricing and a till variance all take.
- Flow F92 branch at step 1 (medium): when A step is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` decides — the journey is shorter, not broken.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create stock transfer, Create stock movement.
- [ ] Every transition is wired: `BO-082`, `BO-079`, `BO-080`, `EMP-065`, `BO-081`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-050` Stock Position & Valuation

**Count the shelf and account for the difference.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_VIEW`, `PRODUCT_VIEW` (2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getStockPositions` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/stock-count` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Named `Stock Count` and carrying `getStockPositions` and `getStockValuation`** — two screens with one name, while `BO-079 Stock Count` holds the actual counting operations. Renamed 20 August; the operations were right.

**From the Food, Beverage & Retail process.** Stock Position & Valuation is the finance-facing view of stock: what the venue's stock is worth on a date, by location and by category, under each item's costing method (weighted average or FIFO). It is read-only. The one thing to get right is that it is a valuation report, not a counting screen. The current definition is half renamed from "Stock Count".

**Known correction pending (do not draw the wrong version)**

- **The route is /venue-operations/stock-count and the component StockCountDetail.tsx. The purpose reads "Count the shelf and account for the difference". The pattern is a single-record status tracker.** Why: The 20 August rename stopped at the name. Stock counting is BO-079. This screen is a read-only valuation report, so it needs a valuation route and component name, a valuation purpose and a report pattern. *(source: screens/P08-venue-back-office.yaml#BO-050; Food, Beverage & Retail)*
- **The no-access state names only the stock-view permission.** Why: Valuation needs the ledger-view permission. A user with only stock view sees a broken page rather than an explanation. *(source: contracts/satellite/inventory.yaml#getStockValuation; Food, Beverage & Retail)*
- **The client asked for a breakdown by department and sub-department. The valuation returns only by location and by category.** Why: Department is not a valuation dimension in the contract. *(source: DI-342 / contracts/satellite/inventory.yaml#/components/schemas/StockValuation; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Item costing offers four methods (weighted average, FIFO, standard cost, last purchase price). The workshop agreed weighted average and FIFO. Should the other two be offered?** → Drawn default accepted: The note names weighted average and FIFO only. The item form (BO-081) offers those two. *(decided by Chinmay, 2026-10-02; DEC-286 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |
| As at | date picker | — | — | `getStockValuation` ?asAt |
| Location | picker: choose a location | — | — | `getStockValuation` ?locationId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **As at**: A date. Default today. A past date gives the value on that date (served from the reporting replica, so allow for a short lag). *(source: contracts/satellite/inventory.yaml#getStockValuation)*
- **Location**: Tree picker as on Stock Levels; default all locations. *(source: DI-345)*

#### Outputs: what the screen shows and produces

**Shown**

**The stock position** (detail panel, from `getStockPositions`)

| Shows | Format | Notes |
|---|---|---|
| Item name | text | — |
| SKU | text | — |
| Location name | text | — |
| On hand | 1,234.5 | — |
| Allocated | 1,234.5 | Reserved for orders: the quantity under an active stock reservation for an order (decided 28 September, audit R171). |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Last counted at | 1 Oct 2026, 14:30 | — |
| Last movement at | 1 Oct 2026, 14:30 | — |

**The stock valuation** (detail panel, from `getStockValuation`)

| Shows | Format | Notes |
|---|---|---|
| As at | 1 Oct 2026 | — |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| By location | list or chips (count when long) | — |
| By category | list or chips (count when long) | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Headline**: Total stock value in AED with 2 decimals, the as-at date, and the item count. Out-of-stock item count beside it. *(source: DI-342 / contracts/satellite/inventory.yaml#/components/schemas/StockValuation)*
- **Breakdown**: Two tables: by location (value and item count) and by category (value). Sort by value, highest first. A bar per row is enough; no pie chart. *(source: DI-342 / DI-041)*
- **Costing method note**: One line under the headline: "Each item is valued at its own costing method: weighted average or FIFO." Name the method on the item rows when drilling in (from the item master). *(source: DI-344 / contracts/satellite/inventory.yaml#/components/schemas/CostingMethod)*

**Data it reads**: `getStockPositions` (onLoad, Stock on hand by item and location); `getStockValuation` (onLoad, Stock value by location and category)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stock position valuation, read by `getStockPositions`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stock position valuation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stock position valuation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **User can see stock but not ledger value**: The valuation needs the ledger-view right. Without it, say "Stock value is visible to finance roles", and link to Stock Levels for quantities. *(source: contracts/satellite/inventory.yaml#getStockValuation)*
- **As-at date before the venue's first stock movement**: Show zero value with "No stock recorded on this date", not an error. *(source: designer default)*

#### Consistency with other screens

- Match `BO-049`: Same valuation read and same totals as the Stock Levels value panel.
- Match `BO-081`: The costing method shown per item is the one set (and locked) on the item master.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asAt: '2026-10-31'
total: AED 412,906.35
itemCount: 1284
outOfStock: 37
byLocation:
- location: Main Store
  value: AED 198,440.10
  items: 612
- location: Oasis Bistro Kitchen
  value: AED 41,215.75
  items: 188
- location: Marina Bay Retail Floor
  value: AED 96,780.00
  items: 341
byCategory:
- category: Beverages
  value: AED 88,302.40
- category: Apparel
  value: AED 71,950.00
```

#### Permissions

- `getStockPositions` → `PRODUCT_VIEW` (read) · staff
- `getStockValuation` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.9 | The system should allow multi-store retailing where the stores are connected with the inventory information of other stores. This should allow the guests to order items which are out of stock in the … | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 4.4.14 | Support multiple warehouses, stores, kiosks, stock rooms, and inventory locations with centralized visibility. | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 4.4.25 | Maintain one inventory source across POS, B2C, B2B, Mobile App, Kiosks, APIs, and future channels with real-time synchronization. | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 15.1.9 | Real-Time Inventory Tracking - System shall track inventory levels in real time. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.10 | Multi-Location Inventory - System shall support inventory across multiple locations. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.11 | Multi-Warehouse Inventory - System shall support multiple warehouses. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.12 | Available Stock Tracking - System shall track available stock. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.13 | Reserved Stock Tracking - System shall track reserved inventory. | Inventory Management | CONTRACTED | `getStockPositions` |
| 18.7.1 | Inventory Lookup - Users shall view inventory availability. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.2 | Stock Count - Users shall perform stock counts. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.3 | Inventory Transfers - Users shall execute inventory transfers. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.4 | Goods Receipt - Users shall record goods receipt transactions. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The system must support both Weighted Average and FIFO costing methods for inventory valuation. *(agreed · MoM 18 Aug 2026, 4.11 Inventory & Procurement; 5. Key Decisions · DI-344)*
- Inventory & Procurement covers both F&B and Retail: total inventory value, item counts and out-of-stock items, broken down by department/sub-department. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-342)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-050` · status **notStarted** · provenance generated
- Client design-board frames: `Inventory Board 3.dc.html#inv-3h`, `Inventory Board 7.dc.html#inv-7d`

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-050?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-051` Purchase Orders

**Order more of what is running out.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PROCUREMENT_MANAGE`, `PROCUREMENT_VIEW` (1 configure, 1 read); in the flows as storekeeper |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPurchaseOrders` reads the population and `getPurchaseOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `purchaseOrderId` (deepLink) · cold entry: **A staff link opened cold resolves the purchase order or says plainly that it is gone.** Without `purchaseOrderId` the list opens. **The scope is resolved … |
| Route | `/venue-operations/purchase-orders` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. **Rebound 28 September to the inventory purchase-order operations** (decided 28 September, audit R254): it carried 13 sales-order operations (`listOrders`, `voidOrder`, `holdOrder` and the rest), attached by name resemblance as BO-070 was, and none of them orders stock. It now lists, raises, sends, acknowledges, cancels and short-closes purchase orders; receiving is BO-052. Guards are the procurement permissions (audit R091 (4)), and cancel and close-short may answer 202 pending a finance approver (audit R144).

**From the Food, Beverage & Retail process.** Purchase Orders is where the buyer turns an approved requisition and its chosen quotation into an order, sends it, records the supplier's acknowledgement, and later cancels it or closes it short. The one thing to get right is the chain: no order without an approved requisition and a selected quotation, with the price taken from the quotation and changed only with a reason. Cancelling or short-closing goes to a finance approver.

**Known correction pending (do not draw the wrong version)**

- **PO types do not match the agreed decision. The client agreed three types: Regular (item, quantity, price), Contract (pre-agreed fixed price for a period, picked up automatically on later orders) and Service (non-inventory items and services). The contract's PurchaseOrder.kind is standard / blanket …** Why: Regular maps to standard. Contract maps only partly to blanket plus release: the supplier contract record has no price lines, so nothing can "auto-pick" a contract price. Service has no counterpart: every PO line needs an inventory item and every receipt adds stock. rfqAward is a sourcing origin, not a type, because every standard order already needs a quotation. Also, the create request has no … *(source: DI-348 / TRACKER Workshops/Actions row 91 / contracts/satellite/inventory.yaml#/components/schemas/PurchaseOrder / contracts/satellite/inventory.yaml#/components/schemas/CreatePurchaseOrderRequest / …; Food, Beverage & Retail)*
- **The list shows a match-status column (matched / price variance / quantity variance) and the order has a supplier invoice reference, but no operation records a supplier invoice or sets the match status.** Why: Three-way match has only two legs. The column would always be empty. Hide it until an invoice-capture operation exists, or add one. *(source: contracts/satellite/inventory.yaml#/components/schemas/PurchaseOrder; Food, Beverage & Retail)*
- **The order is "still ours to change" while Raised, but no operation updates a raised order.** Why: A wrong line on a raised order can only be fixed by cancelling (which may need finance approval) and raising again. *(source: contracts/satellite/inventory.yaml#sendPurchaseOrder; Food, Beverage & Retail)*
- **The filters are text fields "Status" and "Supplier id". The list shows approvalRequestId as a column.** Why: These leak plumbing. Use status chips, a supplier picker and a "Pending approval" badge. *(source: screens/P08-venue-back-office.yaml#BO-051; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How does "Send to supplier" reach the supplier: an emailed PDF from TICVAI, or a status change after the buyer sends it themselves?** → Drawn default accepted: Draw "Send" as emailing a PDF to the supplier's contact email, with a "Download PDF" secondary action. *(decided by Chinmay, 2026-10-02; DEC-287 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Is the proposed PO number format PO-<venue code>-<six-digit sequence> accepted?** → Drawn default accepted: Use PO-AQP-000214 in all mock-ups. *(decided by Chinmay, 2026-10-02; DEC-288 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Raised · Sent · Acknowledged · Partially received · Received · Closed short · Cancelled | — | Sends `?status=` to `listPurchaseOrders`. | `listPurchaseOrders` ?status |
| Supplier id | picker: choose a supplier (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?supplierId=` to `listPurchaseOrders`. | `listPurchaseOrders` ?supplierId |

**Form: Create purchase order** (modal, opened by *Create purchase order*; *Create purchase order* calls `createPurchaseOrder`, *Cancel* sends nothing)

**Collects what `createPurchaseOrder` sends before it is called.** Required: `id`, `requisitionId`, `supplierId`, `quotationId`, `lines`, `expectedDelivery`. Optional: `deliverToLocationId`, `note`. **Each line's `unitPrice` is prefilled from the selected quotation**; if the user changes it, the line asks for `priceOverrideReason`, which the server requires (400) whenever the price differs from the quotation (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createPurchaseOrder` body |
| Kind `kind` | radio group | optional | Standard | Standard · Blanket · Release · Rfq award; `standard` needs `requisitionId` and `quotationId` (409 `requisition-required` without them); `blanket` and `rfqAward` are raised without a requisition; `release` names `blanketParentId`. | — | Which order this is (CHG-RUL-004). `standard` needs `requisitionId` and `quotationId` (409 `requisition-required` without them); `blanket` and `rfqAward` are raised without a … | `createPurchaseOrder` body |
| Requisition `requisitionId` | picker: choose a requisition | optional | — | — | shows names, sends the id | Required for a `standard` order; omitted for a blanket order, an RFQ award or a release. | `createPurchaseOrder` body |
| Supplier `supplierId` | picker: choose a supplier | required | — | — | shows names, sends the id | — | `createPurchaseOrder` body |
| Quotation `quotationId` | picker: choose a quotation | optional | — | — | shows names, sends the id | Required for a `standard` order and an `rfqAward` (the winning quotation). | `createPurchaseOrder` body |
| Rfq `rfqId` | picker: choose a rfq | optional | — | — | shows names, sends the id | For an `rfqAward`, the quotation round it awards. | `createPurchaseOrder` body |
| Blanket parent `blanketParentId` | picker: choose a blanket parent | optional | — | — | shows names, sends the id | For a `release`, the open blanket order it draws against. | `createPurchaseOrder` body |
| Contract price valid until `contractPriceValidUntil` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | For a `blanket` order, the last day its prices hold. | `createPurchaseOrder` body |
| Deliver to location `deliverToLocationId` | picker: choose a deliver to location | optional | — | — | shows names, sends the id | — | `createPurchaseOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createPurchaseOrder` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createPurchaseOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `createPurchaseOrder` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `createPurchaseOrder` body |
| Unit price `lines[].unitPrice` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Omitted, the selected quotation line's price. Editable with a reason (decided 28 September, audit R171). | `createPurchaseOrder` body |
| Price override reason `lines[].priceOverrideReason` | text area | optional | — | max length 500; Required when `unitPrice` differs from the quotation line (audit R171). | — | Required when `unitPrice` differs from the quotation line (audit R171). | `createPurchaseOrder` body |
| Expected delivery `expectedDelivery` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createPurchaseOrder` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `createPurchaseOrder` body |

Errors to draw in the form: 400 A line price differs from the selected quotation with no `priceOverrideReason` (audit R171).; 409 A `standard` order with no approved requisition or no quotation (`requisition-required`), a quotation that does not match the requisition or the RFQ …

**Form: Acknowledge purchase order** (modal, opened by *Acknowledge purchase order*; *Acknowledge purchase order* calls `acknowledgePurchaseOrder`, *Cancel* sends nothing)

**Collects what `acknowledgePurchaseOrder` sends before it is called.** Required: `supplierReference`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Supplier reference `supplierReference` | text field | required | — | — | — | Kept as `PurchaseOrder.supplierReference`; the time is `acknowledgedAt`. | `acknowledgePurchaseOrder` body |

Errors to draw in the form: 409 Not in a state that permits this

**Sent by *Cancel purchase order*** (`cancelPurchaseOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Kept as `PurchaseOrder.cancelReason`. | `cancelPurchaseOrder` body |

**Sent by *Close purchase order short*** (`closePurchaseOrderShort`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | Kept as `PurchaseOrder.closeShortReason`. | `closePurchaseOrderShort` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Requisition**: Picker limited to approved requisitions of this venue (number, department, required-by date, estimated total). It is the first field and drives the rest. *(source: contracts/satellite/inventory.yaml#createPurchaseOrder / DI-348)*
- **Quotation**: Picker of the quotations recorded for that requisition, showing supplier, total, lead time and validity. "Lowest total" and "Shortest lead time" badges as in the comparison. Choosing one sets the supplier, which is read-only on the order. *(source: contracts/satellite/inventory.yaml#compareQuotations / R171)*
- **Lines**: Prefilled from the quotation: item, quantity, unit, unit price. Quantity may be lowered, not raised beyond the approved quantity. If the unit price is changed, the line shows the quoted price beside it and asks for a price reason inline. Without the reason the order cannot be raised. *(source: R171 / contracts/satellite/inventory.yaml#/components/schemas/CreatePurchaseOrderRequest)*
- **Deliver to**: Location picker. Default is the venue's main store. Choosing an outlet kitchen is allowed for fast-moving perishables received directly. *(source: DI-345 / contracts/satellite/inventory.yaml#/components/schemas/PurchaseOrder)*
- **Expected delivery**: Date, required, not in the past. It is the date supplier on-time performance is measured against. *(source: contracts/satellite/inventory.yaml#createPurchaseOrder / contracts/satellite/reporting.yaml#getSupplierPerformance)*
- **Status filter / Supplier filter**: Status as chips (see outputs). Supplier as a searchable picker of the tenant's suppliers. Not text fields. *(source: contracts/satellite/inventory.yaml#listPurchaseOrders)*

#### Outputs: what the screen shows and produces

**Shown**

**Every purchase order** (data table, from `listPurchaseOrders`): A row with `approvalRequestId` set shows *pending approval* (audit R144).

| Shows | Format | Notes |
|---|---|---|
| Purchase order number | text | Per venue, in sequence (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for … |
| Supplier name | text | — |
| Kind | chip: Standard, Blanket, Release, Rfq award | BL-159. A blanket order is a price and a commitment, not a delivery. |
| Status | chip: Raised, Sent, Acknowledged, Partially received, Received, Closed short… | — |
| Match status | chip: Unmatched, Matched, Price variance, Quantity variance, Both variance | The variance kinds are separated because they have different owners — a price variance is a buyer's problem and a quantity variance is a … |
| Approval request | the name it points at, never the id | The pending approval request raised by `cancelPurchaseOrder` or `closePurchaseOrderShort` (kinds `purchaseOrderCancel` … |

**The selected purchase order** (detail panel, from `getPurchaseOrder`)

| Shows | Format | Notes |
|---|---|---|
| Purchase order number | text | Per venue, in sequence (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for … |
| Supplier name | text | — |
| Kind | chip: Standard, Blanket, Release, Rfq award | BL-159. A blanket order is a price and a commitment, not a delivery. |
| Contract price valid until | 1 Oct 2026 | — |
| Match status | chip: Unmatched, Matched, Price variance, Quantity variance, Both variance | The variance kinds are separated because they have different owners — a price variance is a buyer's problem and a quantity variance is a … |
| Status | chip: Raised, Sent, Acknowledged, Partially received, Received, Closed short… | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create purchase order (primary button) | `createPurchaseOrder` POST `/purchase-orders` | CreatePurchaseOrderRequest | PurchaseOrder | 400 A line price differs from the selected quotation with no `priceOverrideReason` (audit R171).; 409 A `standard` order with no approved requisition or no quotation (`requisition-required`), a quotation that does not … | gated `PROCUREMENT_MANAGE`; opens modal first |
| Send purchase order (secondary button) | `sendPurchaseOrder` POST `/purchase-orders/{purchaseOrderId}/send` | — | PurchaseOrder | 409 Not in a state that permits this, or the order waits for its approval under the PO approval matrix (`po-approval-pending`; CHG-RUL-004). | gated `PROCUREMENT_MANAGE` |
| Acknowledge purchase order (secondary button) | `acknowledgePurchaseOrder` POST `/purchase-orders/{purchaseOrderId}/acknowledge` | inline | PurchaseOrder | 409 Not in a state that permits this | gated `PROCUREMENT_MANAGE`; opens modal first |
| Cancel purchase order (destructive button) | `cancelPurchaseOrder` POST `/purchase-orders/{purchaseOrderId}/cancel` | inline | PurchaseOrder | 409 The order is not `raised` or `sent`. | gated `PROCUREMENT_MANAGE` |
| Close purchase order short (destructive button) | `closePurchaseOrderShort` POST `/purchase-orders/{purchaseOrderId}/close-short` | inline | PurchaseOrder | 409 Not in a state that permits this | gated `PROCUREMENT_MANAGE` |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Order list**: Columns: PO number (e.g. PO-AQP-000214), supplier, type, status, expected delivery, total (AED incl. 5% VAT), received progress ("12 of 20 lines"). A row awaiting a finance decision shows a "Pending approval" badge beside its status ("Cancellation pending approval" or "Close-short pending approval"). Never an approval id. *(source: R144 / R171 / contracts/satellite/inventory.yaml#/components/schemas/PurchaseOrder)*
- **Status labels**: Raised (not yet sent, still editable by us), Sent, Acknowledged, Partly received, Received, Closed short, Cancelled. Use exactly these words. *(source: contracts/satellite/inventory.yaml#/components/schemas/PurchaseOrderStatus / contracts/satellite/inventory.yaml#sendPurchaseOrder)*
- **Order detail**: Header: supplier, supplier's reference (once acknowledged), deliver-to, requisition number (linked), quotation (linked to the comparison). Lines: item, ordered, received, outstanding, unit price, quoted price (struck through with the reason, when overridden), line total. Footer: subtotal, VAT 5%, total. *(source: contracts/satellite/inventory.yaml#getPurchaseOrder)*
- **Printable / sendable order**: A clean PO document (venue legal name, TRN, supplier, lines, VAT, total, delivery address and date) for sending. *(source: designer default)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Raise purchase order**: Creates the order in Raised with its number assigned by the server (per venue, in sequence). Refused when the requisition is not approved or the quotation does not belong to it. Say which, and offer the requisition. *(source: R171 / contracts/satellite/inventory.yaml#createPurchaseOrder)*
- **Send to supplier**: Confirm "Send PO-AQP-000214 to Gulf Fresh Dairy LLC? After sending, the order can no longer be changed." The status becomes Sent. *(source: contracts/satellite/inventory.yaml#sendPurchaseOrder)*
- **Record acknowledgement**: Asks for the supplier's own order reference. Optional in practice: goods often arrive without one. It feeds supplier performance. *(source: contracts/satellite/inventory.yaml#acknowledgePurchaseOrder)*
- **Cancel order**: Only for Raised or Sent orders. Asks for a reason (at least 3 characters) and names the order, the supplier and the value not yet received. If finance approval is needed, the order stays as it is with "Cancellation pending approval". It cancels when the finance approver agrees, and the requester can never approve it. A partly received order offers "Close short" instead. *(source: R144 / contracts/satellite/inventory.yaml#cancelPurchaseOrder)*
- **Close short**: For a partly received order. Asks for a reason and names the balance that will no longer be expected. It goes to a finance approver ("Close-short pending approval"). Closing writes off a committed cost. *(source: R144 / contracts/satellite/inventory.yaml#closePurchaseOrderShort)*

**Data it reads**: `listPurchaseOrders` (onLoad, List purchase orders)

**Where the user goes next**

- → `BO-052` Goods Receipt: *Receive against this order*; carries `purchaseOrderId`

**What opens over it**

- confirmDialog *Cancel purchase order*: **Names what `cancelPurchaseOrder` changes and what it leaves alone**, in the consequence rather than the verb: the order number, the supplier and the value not yet received. **Collects what `cancelPurchaseOrder` sends before it is called.** Required: `reason`. **It may answer 202 pending a finance …
- confirmDialog *Close purchase order short*: **Names what `closePurchaseOrderShort` changes and what it leaves alone**, in the consequence rather than the verb: the balance that will no longer be expected. **Collects what `closePurchaseOrderShort` sends before it is called.** Required: `reason`. **It may answer 202 pending a finance …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The purchase orders list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the purchase orders untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No purchase orders yet. Offers Create purchase order (`createPurchaseOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and supplierId, and the purchase orders are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PROCUREMENT_VIEW`, which `listPurchaseOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_MANAGE` for `createPurchaseOrder`, `sendPurchaseOrder`, `acknowledgePurchaseOrder`, `cancelPurchaseOrder` and 1 more. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A line price differs from the selected quotation with no `priceOverrideReason` (audit R171).; 409 A `standard` order with no approved requisition or no quotation (`requisition-required`), a quotation that does not match the requisition or the RFQ …; 409 Not in a state that permits this; 409 Not in a state that permits this, or the order waits for its approval under the PO approval matrix … |

#### Edge cases to draw

- **Supplier put on hold after the quotation was recorded**: A supplier on hold stops appearing in new orders. Show the quotation as not selectable, with "Supplier on hold". *(source: contracts/satellite/inventory.yaml#updateSupplier)*
- **Quotation expired (valid-until passed)**: Show it as expired in the picker. Raising against it is the buyer's call; show the warning. *(source: contracts/satellite/inventory.yaml#/components/schemas/CreateQuotationRequest)*
- **Approval request rejected by finance**: The badge clears and the order is unchanged. Show the approver's note in the order history. *(source: R144)*
- **Minimum order value**: If the order total is below the supplier's minimum order value, warn before raising. The contract does not refuse it. *(source: contracts/satellite/inventory.yaml#/components/schemas/Supplier)*

#### Consistency with other screens

- Match `BO-078`: The requisition, its approved quantities and its quotation comparison come from Requisitions. "Raise purchase order" on an approved requisition opens this form prefilled.
- Match `BO-052`: Received and outstanding quantities update from goods receipts. The same status words are used on both screens.
- Match `BO-084`: Cancel and close-short approvals appear in the finance approver's queue there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- number: PO-AQP-000214
  supplier: Gulf Fresh Dairy LLC
  type: Regular
  status: Sent
  expectedDelivery: '2026-10-16'
  deliverTo: Oasis Bistro Kitchen
  lines:
  - item: Full-cream milk 2 L
    ordered: 60
    unit: bottle
    unitPrice: AED 12.50
    lineTotal: AED 750.00
  - item: Greek yoghurt 1 kg
    ordered: 24
    unit: tub
    unitPrice: AED 18.75
    quoted: AED 17.90
    priceReason: Supplier price increase from 1 Oct, confirmed by email
    lineTotal: AED 450.00
  subtotal: AED 1,200.00
  vat: AED 60.00
  total: AED 1,260.00
- number: PO-AQP-000209
  supplier: Emirates Beverage Trading LLC
  status: Partly received
  badge: Close-short pending approval
  total: AED 8,412.60
```

#### Permissions

- `listPurchaseOrders` → `PROCUREMENT_VIEW` (read) · staff
- `getPurchaseOrder` → `PROCUREMENT_VIEW` (read) · staff
- `createPurchaseOrder` → `PROCUREMENT_MANAGE` (configure) · staff
- `sendPurchaseOrder` → `PROCUREMENT_MANAGE` (configure) · staff
- `acknowledgePurchaseOrder` → `PROCUREMENT_MANAGE` (configure) · staff
- `cancelPurchaseOrder` → `PROCUREMENT_MANAGE` (configure) · staff
- `closePurchaseOrderShort` → `PROCUREMENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PROCUREMENT_VIEW`, which `listPurchaseOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_MANAGE` for `createPurchaseOrder`, `sendPurchaseOrder`, `acknowledgePurchaseOrder`, `cancelPurchaseOrder` and 1 more.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 15.1.14 | On-Order Stock Tracking - System shall track inventory on purchase orders. | Inventory Management | CONTRACTED | `getPurchaseOrder` |
| 4.4.18 | Support creation, approval, tracking, and management of supplier purchase orders. | Bundles and Promotions | CONTRACTED | `createPurchaseOrder` |
| 4.4.19 | Support inventory receiving, partial deliveries, discrepancy management, and automatic stock updates. | Bundles and Promotions | CONTRACTED | `createPurchaseOrder` |
| 4.5.8 | Convert approved requisitions into supplier purchase orders. | Bundles and Promotions | CONTRACTED | `createPurchaseOrder` |
| 15.3.10 | Purchase Orders - System shall support purchase orders. | Inventory Management | CONTRACTED | `createPurchaseOrder` |
| 15.3.13 | Goods Receipt Notes - System shall support GRNs. | Inventory Management | CONTRACTED | `createPurchaseOrder` |
| 15.3.14 | Purchase Receipt Validation - System shall validate received purchases. | Inventory Management | CONTRACTED | `createPurchaseOrder` |
| 4.5.33 | Manage supplier invoices. | Bundles and Promotions | CONTRACTED | data `PurchaseOrder` |
| 15.3.7 | Request for Quotation - System shall support RFQs. | Inventory Management | CONTRACTED | data `PurchaseOrder` |
| 15.3.11 | Blanket Purchase Orders - System shall support blanket purchase orders. | Inventory Management | CONTRACTED | data `PurchaseOrder` |
| 15.3.12 | Contract Purchasing - System shall support contract purchasing. | Inventory Management | CONTRACTED | data `PurchaseOrder` |
| 15.3.15 | Three-Way Matching - System shall support PO, GRN and invoice matching. | Inventory Management | CONTRACTED | data `PurchaseOrder` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Flow is Purchase Request → Approval → Purchase Order, with RFQ to compare prices from multiple suppliers. Three PO types: Regular (item/quantity/price entry), Contract (pre-agreed fixed price for a period, auto-picked on later orders) and Service (non-inventory items/services). *(agreed · MoM 18 Aug 2026, 4.13 Supplier & Purchase Order Management; 5. Key Decisions · DI-348)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-051` · status **notStarted** · provenance generated
- Client design-board frames: `Inventory Board 5.dc.html#inv-5a`, `Inventory Board 5.dc.html#inv-5h`, `Inventory Board 5.dc.html#inv-5j`
- Flow F76 *Stock is counted, requested, transferred and received*, step 5: Goods Receipt. → **Drawn by the client as RET-4E.** 7 operations on this step.
- Flow F92 *Store stock is watched, replenished and reconciled*, step 5: Goods Receipt. → **Drawn by the client as RET-4E.**

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create purchase order, Send purchase order, Acknowledge purchase order, Cancel purchase order, Close purchase order short.
- [ ] Every transition is wired: `BO-052`.
- [ ] Every gated control is gated: `PROCUREMENT_MANAGE`, `PROCUREMENT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-052` Goods Receipt

**Book in what actually arrived.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PROCUREMENT_RECEIVE`, `PROCUREMENT_VIEW` (1 operate, 1 read); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPurchaseOrders` reads the population and `getPurchaseOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `purchaseOrderId` (deepLink), `receiptId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/goods-receipt` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Pulled to Wave 2 (CF-101). Requisitions are Wave 1 and receipt was Wave 3 — **the end of the chain arriving two waves after the start.** **Cross-platform navigation removed 24 August**: EMP-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): The purchase-order lifecycle belongs to BO-051 and the transfer actions to BO-080; F76 step 5 and F92 step 5 attached them here before BO-051 existed in the … Removed 2 October 2026 (CHG-WIR-008): The purchase-order lifecycle belongs to BO-051 and the transfer actions to BO-080; F76 step 5 and F92 step 5 attached them here before BO-051 existed in the … Removed 2 October 2026 (CHG-WIR-008): The purchase-order lifecycle belongs to BO-051 and the transfer actions to BO-080; F76 step 5 and F92 step 5 attached them here before BO-051 existed in the …

**From the Food, Beverage & Retail process.** Goods Receipt is where the storekeeper books in what actually arrived against a purchase order. Partial deliveries are normal. Batch and expiry are captured per line. Over-delivery beyond the tolerance is refused, and damaged or wrong goods are rejected by receipt line. The one thing to get right is that a receipt records what arrived, line by line and batch by batch. It is not a confirmation of the order. The screen must not also be the purchase-order and transfer screen it currently is.

**Known correction pending (do not draw the wrong version)**

- **The rejection reasons are a fixed list.** Why: The client asked for a user-defined reason list that can be extended in the backend without development. *(source: DI-363 / contracts/satellite/inventory.yaml#rejectReceivedGoods; Food, Beverage & Retail)*
- **The filters are text fields "Status" and "Supplier id". Both tables show every raw column (ids, scope path, journal id).** Why: These leak plumbing. *(source: screens/P08-venue-back-office.yaml#BO-052; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The screen carries the purchase-order lifecycle (raise, send, acknowledge, cancel, close short) and the transfer actions (close transfer … (CHG-WIR-008); F35 step 4 receives the remainder of a stock transfer with createGoodsReceipt. F15 branch at 4 answers a short delivery with … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the over-receipt tolerance of 5% accepted as the tenant default?** → Drawn default accepted: Show "Up to <outstanding + 5%>". *(decided by Chinmay, 2026-10-02; DEC-289 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Raised · Sent · Acknowledged · Partially received · Received · Closed short · Cancelled | — | Sends `?status=` to `listPurchaseOrders`. | `listPurchaseOrders` ?status |
| Supplier id | picker: choose a supplier (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?supplierId=` to `listPurchaseOrders`. | `listPurchaseOrders` ?supplierId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Purchase order | picker: choose a purchase order | — | — | `listGoodsReceipts` ?purchaseOrderId |

**Form: Create goods receipt** (modal, opened by *Create goods receipt*; *Create goods receipt* calls `createGoodsReceipt`, *Cancel* sends nothing)

**Collects what `createGoodsReceipt` sends before it is called.** Required: `id`, `purchaseOrderId`, `locationId`, `lines`, `recordedAt`. Optional: `deliveryNoteReference`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createGoodsReceipt` body |
| Purchase order `purchaseOrderId` | picker: choose a purchase order | required | — | — | shows names, sends the id | — | `createGoodsReceipt` body |
| Location `locationId` | picker: choose a location | required | — | — | shows names, sends the id | — | `createGoodsReceipt` body |
| Delivery note reference `deliveryNoteReference` | text field | optional | — | max length 128 | — | — | `createGoodsReceipt` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createGoodsReceipt` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createGoodsReceipt` body |
| Received quantity `lines[].receivedQuantity` | number field | required | — | min 0 | — | — | `createGoodsReceipt` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `createGoodsReceipt` body |
| Batch number `lines[].batchNumber` | text field | optional | — | max length 64 | — | — | `createGoodsReceipt` body |
| Expiry date `lines[].expiryDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Required for perishable items. | `createGoodsReceipt` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | — | `createGoodsReceipt` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGoodsReceipt` body |

Errors to draw in the form: 409 Over-receipt beyond `VenueSettings.inventory.overReceiptTolerancePercent` (proposed default 5, audit R094), or the purchase order is closed

**Sent by *Reject received goods*** (`rejectReceivedGoods`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `rejectReceivedGoods` body |
| Line `lines[].lineId` | picker: choose a line | required | — | — | shows names, sends the id | `GoodsReceipt.lines[].lineId`, the batch or expiry line rejected (audit R171). | `rejectReceivedGoods` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `rejectReceivedGoods` body |
| Reason `reason` | select | required | — | Damaged · Wrong item · Quality failure · Short dated · Over delivery · Other | — | `other` requires `note` (decided 28 September, audit R222). | `rejectReceivedGoods` body |
| Note `note` | text area | optional | — | max length 1000 | — | Required, at least 3 characters, when `reason` is `other` (audit R222). | `rejectReceivedGoods` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Purchase order**: Chosen from "Expected deliveries": orders that are Sent, Acknowledged or Partly received for this venue, soonest expected first. Searchable by PO number, supplier or delivery note. *(source: contracts/satellite/inventory.yaml#listPurchaseOrders / contracts/satellite/inventory.yaml#createGoodsReceipt)*
- **Receive into**: Location picker. Defaults to the order's deliver-to location. *(source: DI-345 / contracts/satellite/inventory.yaml#/components/schemas/CreateGoodsReceiptRequest)*
- **Delivery note number**: Optional, up to 128 characters. Printed on the supplier's delivery note. *(source: contracts/satellite/inventory.yaml#/components/schemas/CreateGoodsReceiptRequest)*
- **Received quantity (per line)**: Blank by default, with a "Receive as ordered" shortcut per line and for all lines. Show ordered, already received and outstanding beside it. The maximum allowed is outstanding plus the venue's over-receipt tolerance (proposed 5%). Show the limit, e.g. "Up to 63". *(source: R094 / contracts/satellite/inventory.yaml#createGoodsReceipt)*
- **Batch and expiry (per line)**: Batch number up to 64 characters. The expiry date is required for perishable items (flagged on the item master). One order line can be split into several batch lines ("Add batch"), because one item can arrive on two batches with two expiry dates. *(source: R171 / DI-345 / contracts/satellite/inventory.yaml#/components/schemas/CreateGoodsReceiptRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Every purchase order** (data table, from `listPurchaseOrders`)

| Shows | Format | Notes |
|---|---|---|
| Purchase order number | text | Per venue, in sequence (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for … |
| Supplier name | text | — |
| Kind | chip: Standard, Blanket, Release, Rfq award | BL-159. A blanket order is a price and a commitment, not a delivery. |
| Contract price valid until | 1 Oct 2026 | — |
| Match status | chip: Unmatched, Matched, Price variance, Quantity variance, Both variance | The variance kinds are separated because they have different owners — a price variance is a buyer's problem and a quantity variance is a … |
| Status | chip: Raised, Sent, Acknowledged, Partially received, Received, Closed short… | — |

**Every goods receipt** (data table, from `listGoodsReceipts`)

| Shows | Format | Notes |
|---|---|---|
| Receipt number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152), e.g. |
| Delivery note reference | text | — |
| Total value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | — |

**The selected purchase order** (detail panel, from `getPurchaseOrder`)

| Shows | Format | Notes |
|---|---|---|
| Purchase order number | text | Per venue, in sequence (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for … |
| Supplier name | text | — |
| Kind | chip: Standard, Blanket, Release, Rfq award | BL-159. A blanket order is a price and a commitment, not a delivery. |
| Contract price valid until | 1 Oct 2026 | — |
| Match status | chip: Unmatched, Matched, Price variance, Quantity variance, Both variance | The variance kinds are separated because they have different owners — a price variance is a buyer's problem and a quantity variance is a … |
| Status | chip: Raised, Sent, Acknowledged, Partially received, Received, Closed short… | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create goods receipt (primary button) | `createGoodsReceipt` POST `/goods-receipts` | CreateGoodsReceiptRequest | GoodsReceipt | 409 Over-receipt beyond `VenueSettings.inventory.overReceiptTolerancePercent` (proposed default 5, audit R094), or the purchase order is closed | gated `PROCUREMENT_RECEIVE`; opens modal first; produces a document or message: Receive goods against a purchase order |
| Reject received goods (destructive button) | `rejectReceivedGoods` POST `/goods-receipts/{receiptId}/reject` | inline | GoodsReceipt | 400 `reason` is `other` with no `note` (audit R222).; 409 A line rejects more than was received and not already rejected on it, or names a `lineId` the receipt does not hold (audit R171) | gated `PROCUREMENT_RECEIVE` |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Receipt confirmation**: Receipt number (venue prefix plus sequence, e.g. AQP-GR-000431), lines received, total value, and "Stock updated". "Accrual posted" shows as text, never as a journal id. The order's status moves to Partly received or Received. *(source: R152 / contracts/satellite/inventory.yaml#/components/schemas/GoodsReceipt)*
- **Receipt history**: Per order: each receipt with date, receiver, delivery note, lines, rejected quantities with reasons. *(source: contracts/satellite/inventory.yaml#listGoodsReceipts)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Post receipt**: Adds stock and creates the accrual. Refused for over-receipt beyond the tolerance. Name the line and the maximum. Refused if the order was closed meanwhile. *(source: R094 / contracts/satellite/inventory.yaml#createGoodsReceipt)*
- **Reject lines**: Pick receipt lines (each batch or expiry line), the quantity rejected and a reason: Damaged, Wrong item, Quality failure, Short-dated, Over-delivery, Other. Other requires a note of at least 3 characters. The rejection reverses the stock and raises a supplier return. The dialog names the receipt and the lines. *(source: R171 / R222 / contracts/satellite/inventory.yaml#rejectReceivedGoods)*

**Data it reads**: `listPurchaseOrders` (onLoad, List purchase orders); `listGoodsReceipts` (onLoad, List goods receipts)

**Where the user goes next**

- → `EMP-005` Task detail: *The technician resumes*
- → `BO-049` Stock Levels: *The website has already sold four of the damaged units*; carries `itemId`

**What opens over it**

- confirmDialog *Reject received goods*: **Names what `rejectReceivedGoods` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted. **Collects what `rejectReceivedGoods` sends before it is called.** Required: `lines` — each a receipt …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The goods receipt list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the goods receipt untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No goods receipt yet. Offers Create goods receipt (`createGoodsReceipt`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, supplierId and the goods receipt are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PROCUREMENT_VIEW`, which `listPurchaseOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_RECEIVE` for `createGoodsReceipt`, `rejectReceivedGoods`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `reason` is `other` with no `note` (audit R222).; 409 A line rejects more than was received and not already rejected on it, or names a `lineId` the receipt does not hold (audit R171); 409 Over-receipt beyond `VenueSettings.inventory.overReceiptTolerancePercent` (proposed default 5, audit R094), or the purchase order is closed |

#### Edge cases to draw

- **A chilled or frozen delivery arrives warm**: The temperature is recorded before the receipt is posted, and the delivery is refused at the door. On the handheld this is Receiving (EMP-065). Here, show the cold-chain reading on the receipt if one was taken. *(source: F28 step 1 / contracts/satellite/fnb.yaml#logColdChain)*
- **The same item arrives on two batches**: Two receipt lines for one order line. A rejection can name one batch and leave the other. *(source: R171)*
- **Partial delivery and the rest will never come**: The order stays Partly received. Link to Purchase Orders to close it short (finance approval). *(source: R144 / contracts/satellite/inventory.yaml#closePurchaseOrderShort)*

#### Consistency with other screens

- Match `EMP-065`: The same receipt form in handheld layout: same fields, same reasons, same tolerance message. The handheld is where most receipts happen.
- Match `BO-051`: Same status words. Order lifecycle actions (send, cancel, close short) live only on Purchase Orders.
- Match `BO-083`: Rejections and lateness feed supplier performance (on time in full, rejection reasons).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order: PO-AQP-000214 · Gulf Fresh Dairy LLC · expected 16 Oct 2026
deliveryNote: GFD-DN-778120
receivedAt: 2026-10-16 07:42 GST
lines:
- item: Full-cream milk 2 L
  ordered: 60
  received: 36
  batch: L2610A
  expiry: '2026-10-23'
- item: Full-cream milk 2 L
  ordered: (same line)
  received: 24
  batch: L2610B
  expiry: '2026-10-24'
- item: Greek yoghurt 1 kg
  ordered: 24
  received: 20
  rejected: 4
  reason: Damaged
receiptNumber: AQP-GR-000431
totalValue: AED 1,125.00
```

#### Permissions

- `createGoodsReceipt` → `PROCUREMENT_RECEIVE` (operate) · staff
- `listPurchaseOrders` → `PROCUREMENT_VIEW` (read) · staff
- `getPurchaseOrder` → `PROCUREMENT_VIEW` (read) · staff
- `listGoodsReceipts` → `PROCUREMENT_VIEW` (read) · staff
- `rejectReceivedGoods` → `PROCUREMENT_RECEIVE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PROCUREMENT_VIEW`, which `listPurchaseOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_RECEIVE` for `createGoodsReceipt`, `rejectReceivedGoods`.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.5.10 | Receive inventory against purchase orders. | Bundles and Promotions | CONTRACTED | `createGoodsReceipt` |
| 4.5.30 | Receive goods against purchase orders. | Bundles and Promotions | CONTRACTED | `createGoodsReceipt` |
| 4.5.32 | Support partial deliveries. | Bundles and Promotions | CONTRACTED | `createGoodsReceipt` |
| 15.2.5 | Purchase Receiving - System shall support receiving operations. | Inventory Management | CONTRACTED | `createGoodsReceipt` |
| 15.2.6 | Receiving Validation - System shall validate received goods. | Inventory Management | CONTRACTED | `createGoodsReceipt` |
| 15.2.7 | Receiving Discrepancy Management - System shall manage receiving discrepancies. | Inventory Management | CONTRACTED | `createGoodsReceipt` |
| 15.1.14 | On-Order Stock Tracking - System shall track inventory on purchase orders. | Inventory Management | CONTRACTED | `getPurchaseOrder` |
| 4.5.33 | Manage supplier invoices. | Bundles and Promotions | CONTRACTED | data `PurchaseOrder` |
| 15.3.7 | Request for Quotation - System shall support RFQs. | Inventory Management | CONTRACTED | data `PurchaseOrder` |
| 15.3.11 | Blanket Purchase Orders - System shall support blanket purchase orders. | Inventory Management | CONTRACTED | data `PurchaseOrder` |
| 15.3.12 | Contract Purchasing - System shall support contract purchasing. | Inventory Management | CONTRACTED | data `PurchaseOrder` |
| 15.3.15 | Three-Way Matching - System shall support PO, GRN and invoice matching. | Inventory Management | CONTRACTED | data `PurchaseOrder` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Warehouse/location structure is a customisable hierarchy (e.g. main warehouse → food warehouse → beverage warehouse), with stock received centrally or directly at an outlet/kitchen for fast-moving perishables. Expiry is tracked at batch/date level; reorder alerts notify staff at a minimum threshold. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-345)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-052` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 4.dc.html#ret-4e`, `Inventory Board 6.dc.html#inv-6a`, `Inventory Board 6.dc.html#inv-6b`, `Inventory Board 6.dc.html#inv-6c`, `Inventory Board 6.dc.html#inv-6d`, `Inventory Board 6.dc.html#inv-6e`
- Flow F15 *A part is needed and ordered*, step 4: The goods arrive and are received → Stock rises at the venue
- Flow F15 branch at step 4 (requiresStaff): when The delivery is short, `closeTransferShort` or a partial receipt. **The difference is a discrepancy to investigate, not a silent adjustment.**
- Flow F15 branch at step 4 (requiresStaff): when The wrong part arrived, Received and rejected as a separate movement. The work order stays blocked and the requisition is raised again.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create goods receipt, Reject received goods.
- [ ] Every transition is wired: `EMP-005`, `BO-049`.
- [ ] Every gated control is gated: `PROCUREMENT_RECEIVE`, `PROCUREMENT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-078` Requisitions

**Raise, track and approve a request to buy something.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 1 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_ACT`, `PROCUREMENT_REQUEST`, `PROCUREMENT_VIEW`, `PRODUCT_VIEW` (2 operate, 2 read); in the flows as storekeeper, technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `approveRequisition` decides items that `listRequisitions` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `requisitionId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/inventory/requisitions` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 2 board screen(s): Requisition & Smart Replenishment; Store Inventory & Replenishment Configuration. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Retail board operations wired 24 August.**

**From the Food, Beverage & Retail process.** Requisitions is the purchase request: a department asks to buy, its head approves, returns or rejects it, quotations are compared, and the approved request becomes a purchase order. It serves two people: the requester (raise, track, answer questions) and the approver (decide). The one thing to get right is that the approver is never the requester, and approval may only lower quantities, never raise them.

**Known correction pending (do not draw the wrong version)**

- **A requisition can only become a supplier purchase. The client also uses requisitions for outlets replenishing from the central warehouse, and for inter-store requests approved before a transfer. Flow F35 says "a requisition asks a supplier". Transfers have no approval state.** Why: Internal replenishment has no model. Either the requisition gets a fulfilment type (buy from a supplier / transfer from a store) that ends in a transfer, or transfers get a request-and-approve step. *(source: DI-341 / DI-362 / F35 step 1 / contracts/satellite/inventory.yaml#/components/schemas/Requisition / contracts/satellite/inventory.yaml#/components/schemas/TransferStatus; Food, Beverage & Retail)*
- **The approval of a requisition exists twice: approveRequisition on this screen (F76) and the generic approval queue on BO-084 (F15 step 3). Also, approveRequisition's decision allows rejected and returnedForInfo, which duplicate rejectRequisition and returnRequisition.** Why: One approval path per request, and one way to reject. Otherwise a request can be decided in two places. *(source: F15 step 3 / F76 step 3 / contracts/satellite/inventory.yaml#approveRequisition; Food, Beverage & Retail)*
- **F15 step 2 raises a requisition "against the work order" so the job and the purchase find each other. The request has no work-order field.** Why: The link the flow promises cannot be stored. *(source: F15 step 2 / contracts/satellite/inventory.yaml#/components/schemas/CreateRequisitionRequest; Food, Beverage & Retail)*
- **The status "draft" exists, but nothing creates or submits a draft. Creating raises the request straight into approval, and suggestions are not drafts.** Why: The client expects below-par-level stock to create a draft request for review. Today that state cannot be reached. *(source: DI-234 / contracts/satellite/inventory.yaml#/components/schemas/RequisitionStatus; Food, Beverage & Retail)*
- **The first-run state "offers no create action". The filters are text fields "Status" and "Raised by principal id". An "Every stock location" table is on the screen. There is no exit to Purchase Orders.** Why: The purpose includes raising requests. Locations are only a picker for suggestions. The approved request's next step is BO-051. *(source: screens/P08-venue-back-office.yaml#BO-078 / R251; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should internal replenishment (outlet from warehouse, store to store) go through requisitions with approval, or through transfers with an approval step?** → Drawn default accepted: Draw supplier purchase only. Mark internal replenishment as pending. *(decided by Chinmay, 2026-10-02; DEC-290 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **What is the requisition number format?** → Drawn default accepted: REQ-<venue code>-<six-digit sequence>, as an example only. *(decided by Chinmay, 2026-10-02; DEC-291 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · Pending approval · Approved · Rejected · Returned for info · Ordered · Closed · Cancelled | — | Sends `?status=` to `listRequisitions`. | `listRequisitions` ?status |
| Raised by principal id | picker: choose a raised by principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?raisedByPrincipalId=` to `listRequisitions`. | `listRequisitions` ?raisedByPrincipalId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getSuggestedRequisitions` ?locationId |

**Form: Create requisition** (modal, opened by *Create requisition*; *Create requisition* calls `createRequisition`, *Cancel* sends nothing)

**Collects what `createRequisition` sends before it is called.** Required: `id`, `venueId`, `lines`, `requiredBy`. Optional: `departmentId`, `costCenterId`, `justification`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createRequisition` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createRequisition` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `createRequisition` body |
| Cost center `costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | — | `createRequisition` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createRequisition` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createRequisition` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `createRequisition` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `createRequisition` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | — | `createRequisition` body |
| Required by `requiredBy` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createRequisition` body |
| Justification `justification` | text area | optional | — | max length 1000 | — | — | `createRequisition` body |

Errors to draw in the form: 400 Validation failed

**Form: Decide requisition** (modal, opened by *Decide requisition*; *Send decision* calls `approveRequisition`, *Cancel* sends nothing)

**Collects the decision `approveRequisition` sends** (decided by Chinmay, 3 October 2026 (CHG-SPF-010)): `decision` is approve, reject or return; a reject or a return names its reason in `note`, which the form will not send empty. Optional: `amendedLines` (approve only). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approved · Rejected · Returned for info | — | — | `approveRequisition` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `approveRequisition` body |
| Amended lines `amendedLines` | repeatable rows | optional | — | — | — | — | `approveRequisition` body |
| Line `amendedLines[].lineId` | text field | optional | — | — | — | — | `approveRequisition` body |
| Approved quantity `amendedLines[].approvedQuantity` | number field | optional | — | min 0 | — | — | `approveRequisition` body |

Errors to draw in the form: 400 An amended quantity exceeds the requested quantity; 403 Authenticated but not permitted at the requested scope; 409 The requisition is not `pendingApproval`, or the caller raised it — the state model's guard is that the approver is not the requester

**Form: Save requisition lines** (modal, opened by *Save requisition lines*; *Save requisition lines* calls `updateRequisitionLines`, *Cancel* sends nothing)

**Collects what `updateRequisitionLines` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | — | — | — | `updateRequisitionLines` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `updateRequisitionLines` body |
| Quantity `lines[].quantity` | number field | required | — | — | — | — | `updateRequisitionLines` body |
| Reason `lines[].reason` | text area | optional | — | — | — | Why the quantity differs from the suggestion. Kept on the line. | `updateRequisitionLines` body |

Errors to draw in the form: 409 Already approved: the requisition is `approved`, `ordered` or `closed` (audit R171), or it is `rejected` or `cancelled`.

**Sent by *Cancel requisition*** (`cancelRequisition`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | Kept as `Requisition.cancelReason`. | `cancelRequisition` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Lines**: Item picker (inventory items), quantity, unit. Units offer the item's base unit and purchase unit ("can" or "case of 24"). When the request came from a suggestion, the suggested quantity stays visible beside the requested one. A different quantity asks for a short reason. *(source: DI-343 / contracts/satellite/inventory.yaml#updateRequisitionLines / contracts/satellite/inventory.yaml#/components/schemas/Requisition)*
- **Required by**: Date, required, today or later. *(source: contracts/satellite/inventory.yaml#/components/schemas/CreateRequisitionRequest)*
- **Department / cost centre**: Pickers. Department defaults to the requester's own. The cost centre is what finance books it to. *(source: contracts/satellite/inventory.yaml#/components/schemas/CreateRequisitionRequest)*
- **Justification**: Optional, up to 1,000 characters. It is what the approver reads first. *(source: contracts/satellite/inventory.yaml#/components/schemas/CreateRequisitionRequest)*
- **Approver's amended quantity**: On approval each line can be lowered, never raised above the requested quantity. Enforce it in the field (the maximum is the requested quantity). *(source: contracts/satellite/inventory.yaml#approveRequisition)*
- **Filters**: Status chips, plus "Raised by me" / "Waiting for my decision" tabs. Never a "Raised by principal id" text field. *(source: contracts/satellite/inventory.yaml#listRequisitions)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listRequisitions`)

| Shows | Format | Notes |
|---|---|---|
| Requisition number | text | — |
| Status | chip: Draft, Pending approval, Approved, Rejected, Returned for info, Ordered… | — |
| Estimated total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approval note | text | — |
| Required by | 1 Oct 2026 | — |
| Approved at | 1 Oct 2026, 14:30 | — |

**Every stock location** (data table, from `listStockLocations`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Main store, Sub store, Kitchen, Bar, Retail floor, Cellar… | — |
| Is active | yes / no (icon or chip) | — |

**The selected requisition** (detail panel, from `listRequisitions`)

| Shows | Format | Notes |
|---|---|---|
| Requisition number | text | — |
| Justification | text | — |
| Status | chip: Draft, Pending approval, Approved, Rejected, Returned for info, Ordered… | — |
| Lines | list or chips (count when long) | — |
| Estimated total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approval note | text | — |
| Approved at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |

**The requisition suggestion** (detail panel, from `getSuggestedRequisitions`)

| Shows | Format | Notes |
|---|---|---|
| Item name | text | — |
| SKU | text | — |
| On hand | 1,234.5 | — |
| Reorder point | 1,234.5 | — |
| Par level | 1,234.5 | — |
| Suggested quantity | 1,234.5 | — |
| Average daily consumption | 1,234.5 | — |
| Days of cover remaining | 1,234.5 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create requisition (primary button) | `createRequisition` POST `/requisitions` | CreateRequisitionRequest | Requisition | 400 Validation failed | gated `PROCUREMENT_REQUEST`; opens modal first |
| Decide requisition (secondary button) | `approveRequisition` POST `/requisitions/{requisitionId}/approve` | inline | Requisition | 400 An amended quantity exceeds the requested quantity; 403 Authenticated but not permitted at the requested scope; 409 The requisition is not `pendingApproval`, or the caller raised it — the state model's guard is that … | gated `APPROVAL_ACT`; opens modal first |
| Cancel requisition (destructive button) | `cancelRequisition` POST `/requisitions/{requisitionId}/cancel` | inline | Requisition | 409 Not in a state that permits this | gated `PROCUREMENT_REQUEST` |
| Compare quotations (secondary button) | `compareQuotations` GET `/requisitions/{requisitionId}/quotations` | — | QuotationComparison | — | gated `PROCUREMENT_VIEW` |
| Save requisition lines (secondary button) | `updateRequisitionLines` PUT `/requisitions/{requisitionId}/lines` | inline | Requisition | 409 Already approved: the requisition is `approved`, `ordered` or `closed` (audit R171), or it is `rejected` or `cancelled`. | gated `PROCUREMENT_REQUEST`; opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Two tabs**: "Waiting for my decision" (pending approval, not raised by me; an empty tab is the good outcome) and "Requests" (everything for the venue, filterable). The empty decision tab says "Nothing waiting for you". *(source: screens/P08-venue-back-office.yaml#BO-078)*
- **Status labels**: Pending approval, Approved, Returned for information, Rejected, Ordered, Closed, Cancelled. A returned request shows the approver's question prominently to the requester. A rejected one shows the reason and offers "Copy to new request". *(source: contracts/satellite/inventory.yaml#/components/schemas/RequisitionStatus / contracts/satellite/inventory.yaml#rejectRequisition / contracts/satellite/inventory.yaml#returnRequisition)*
- **Suggestions panel**: "Below reorder point" items for a chosen location: on hand, reorder point, par level, average daily use, days of cover left, suggested quantity, preferred supplier, lead time. Sort by days of cover ascending. A suggestion is a draft for a person to review and is never raised automatically. *(source: DI-234 / contracts/satellite/inventory.yaml#getSuggestedRequisitions)*
- **Quotation comparison**: Side by side per supplier: total, lead time, valid until, and per line unit prices with the lowest per line highlighted. Badges "Lowest total" and "Shortest lead time". The cheapest total is not always the cheapest line. *(source: contracts/satellite/inventory.yaml#compareQuotations / DI-348)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **New request**: Raises the request straight into Pending approval. It shows in the approver's tab. *(source: contracts/satellite/inventory.yaml#createRequisition)*
- **Create from suggestions**: Opens a new request prefilled with the selected suggestions. The suggested quantities are kept beside any change. *(source: contracts/satellite/inventory.yaml#getSuggestedRequisitions / contracts/satellite/inventory.yaml#updateRequisitionLines)*
- **Edit lines**: Allowed until approval. After approval it is refused, and the message says a new request is needed. *(source: R171 / contracts/satellite/inventory.yaml#updateRequisitionLines)*
- **Approve · Return with a question · Reject**: Three distinct buttons for the approver. Return asks a question and Reject asks a reason. The buttons are hidden on a request the user raised; the server refuses it anyway. *(source: contracts/satellite/inventory.yaml#approveRequisition / contracts/satellite/inventory.yaml#returnRequisition / contracts/satellite/inventory.yaml#rejectRequisition)*
- **Cancel request**: Requester only, with a reason. The confirmation names the request number and its estimated total. *(source: contracts/satellite/inventory.yaml#cancelRequisition)*
- **Record quotation · Compare · Raise purchase order**: On an approved request: record supplier quotes against it, compare them, select one, then "Raise purchase order", which opens BO-051 prefilled. *(source: DI-348 / contracts/satellite/inventory.yaml#recordQuotation / contracts/satellite/inventory.yaml#createPurchaseOrder)*

**Data it reads**: `listRequisitions` (onLoad, List requisitions); `getSuggestedRequisitions` (onLoad, Draft requisitions from reorder points); `listStockLocations` (onLoad, List stock locations)

**Where the user goes next**

- → `BO-080` Stock Transfers: *Stock Transfers*
- → `BO-084` Approval Inbox: *A manager approves it*; calls `createRequisition`
- → `BO-079` Stock Count: *Stock Count*
- → `BO-081` Inventory Items: *Inventory Items*; carries `itemId`

**What opens over it**

- confirmDialog *Cancel requisition*: **Names what `cancelRequisition` changes and what it leaves alone**, in the consequence rather than the verb. A requisitions this affects should be identified in the dialog, not just counted. **Collects what `cancelRequisition` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The requisitions list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the requisitions untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, raisedByPrincipalId and the requisitions are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PROCUREMENT_VIEW`, which `listRequisitions` requires to show this screen, and names that permission (the screen's other reads need `PRODUCT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_ACT` for `approveRequisition`, `rejectRequisition` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An amended quantity exceeds the requested quantity; 400 Validation failed; 409 Already approved: the requisition is `approved`, `ordered` or `closed` (audit R171), or it is `rejected` or `cancelled`.; 409 Not in a state that permits this |

#### Edge cases to draw

- **No supplier is set up for an item**: The request can be approved but cannot become an order. Show "No supplier for <item>" with a link to Suppliers. *(source: F15 step 2)*
- **Offline (handheld or weak signal)**: Raising and editing a request queue offline. Approving, rejecting and returning need a connection. *(source: contracts/satellite/inventory.yaml#createRequisition / contracts/satellite/inventory.yaml#approveRequisition)*

#### Consistency with other screens

- Match `EMP-063`: Same request form and status words in handheld layout.
- Match `BO-051`: "Raise purchase order" carries the requisition and the selected quotation.
- Match `BO-083`: Quotations recorded on Suppliers appear in this comparison, and the reverse.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- number: REQ-AQP-000118
  department: Oasis Bistro (F&B)
  raisedBy: Priya Nair
  requiredBy: '2026-10-18'
  status: Pending approval
  lines:
  - item: Full-cream milk 2 L
    suggested: 72
    requested: 60
    unit: bottle
    reason: Weekend menu change, less demand
  - item: Greek yoghurt 1 kg
    requested: 24
    unit: tub
  estimatedTotal: AED 1,180.00
  justification: Weekly dairy replenishment for Oasis Bistro dinner service
- number: REQ-AQP-000117
  department: Marina Bay Store
  raisedBy: Omar Ziad
  status: Returned for information
  question: Why 300 T-shirts in size S when last month sold 40?
```

#### Permissions

- `listRequisitions` → `PROCUREMENT_VIEW` (read) · staff
- `createRequisition` → `PROCUREMENT_REQUEST` (operate) · staff
- `approveRequisition` → `APPROVAL_ACT` (operate) · staff
- `cancelRequisition` → `PROCUREMENT_REQUEST` (operate) · staff
- `getSuggestedRequisitions` → `PROCUREMENT_VIEW` (read) · staff
- `compareQuotations` → `PROCUREMENT_VIEW` (read) · staff
- `listStockLocations` → `PRODUCT_VIEW` (read) · staff
- `updateRequisitionLines` → `PROCUREMENT_REQUEST` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PROCUREMENT_VIEW`, which `listRequisitions` requires to show this screen, and names that permission (the screen's other reads need `PRODUCT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `APPROVAL_ACT` for `approveRequisition`, `rejectRequisition` …

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.30 | Allow inventory replenishment requests via mobile app. | Bundles and Promotions | CONTRACTED | `createRequisition` |
| 4.6.32 | Perform inventory counts through mobile devices. | Bundles and Promotions | CONTRACTED | `createRequisition` |
| 15.3.4 | Purchase Requests - System shall support purchase requests. | Inventory Management | CONTRACTED | `createRequisition` |
| 15.3.5 | Purchase Requisitions - System shall support purchase requisitions. | Inventory Management | CONTRACTED | `createRequisition` |
| 15.3.6 | Purchase Approval Workflows - System shall support procurement approvals. | Inventory Management | CONTRACTED | `createRequisition` |
| 17.6.5 | Procurement Request Generation - System shall generate procurement requests from maintenance requirements. | Maintenance & Safety Management | CONTRACTED | `createRequisition` |
| 4.5.6 | The system should allow to maintain par stocks and raise requestion automatically if the stock level reaches minimum | Bundles and Promotions | CONTRACTED | `getSuggestedRequisitions` |
| 4.5.7 | Create purchase requisitions based on stock requirements. | Bundles and Promotions | CONTRACTED | `getSuggestedRequisitions` |
| 4.5.34 | Automated reorder suggestions. | Bundles and Promotions | CONTRACTED | `getSuggestedRequisitions` |
| 4.5.27 | Able to make quotations | Bundles and Promotions | CONTRACTED | `compareQuotations` |
| 4.5.28 | Supplier Quotation Comparions | Bundles and Promotions | CONTRACTED | `compareQuotations` |
| 15.3.8 | Supplier Quotation Collection - System shall support supplier quotations. | Inventory Management | CONTRACTED | `compareQuotations` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Flow is Purchase Request → Approval → Purchase Order, with RFQ to compare prices from multiple suppliers. Three PO types: Regular (item/quantity/price entry), Contract (pre-agreed fixed price for a period, auto-picked on later orders) and Service (non-inventory items/services). *(agreed · MoM 18 Aug 2026, 4.13 Supplier & Purchase Order Management; 5. Key Decisions · DI-348)*
- Production execution & batch management shows planned vs. actual vs. yield quantity and batch losses; wastage/spoilage must be recorded per item. Outlets raise requisitions to replenish from the central warehouse. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-341)*
- Requisitions raised in the app flow to department-head approval then purchasing; stock falling below a par level (e.g. 100 units) auto-creates a draft requisition for review and confirmation. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-234)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-078` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 5.dc.html#fnb-5f`, `Retail Board 4.dc.html#ret-4c`, `Retail Board 4.dc.html#ret-4k`, `Inventory Board 4.dc.html#inv-4a`, `Inventory Board 4.dc.html#inv-4e`, `Inventory Board 4.dc.html#inv-4f`
- Flow F15 *A part is needed and ordered*, step 2: Raises a requisition against the work order → Linked, so the job and the purchase find each other
- Flow F76 *Stock is counted, requested, transferred and received*, step 3: Requisitions. → **Drawn by the client as RET-4C.** 9 operations on this step.
- Flow F92 *Store stock is watched, replenished and reconciled*, step 3: Requisitions. → **Drawn by the client as RET-4C.**
- Flow F15 branch at step 2 (requiresStaff): when No supplier is set up for the part, Blocks. `BO-083` — a requisition naming a supplier nobody has onboarded cannot become a purchase order.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-078?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create requisition, Decide requisition, Cancel requisition, Compare quotations, Save requisition lines.
- [ ] Every transition is wired: `BO-080`, `BO-084`, `BO-079`, `BO-081`.
- [ ] Every gated control is gated: `APPROVAL_ACT`, `PROCUREMENT_REQUEST`, `PROCUREMENT_VIEW`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-079` Stock Count

**Count what is there, blind, and resolve the variance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 1 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_POST`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 operate, 1 configure, 1 read); in the flows as storekeeper |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listStockCounts` reads the population and `getCountVariance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `countId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/inventory/stock-count` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 1 board screen(s): Stock Count, Reconciliation & Variance. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Blind counting (decided 28 September, audit R110)**: while a count is open or counting the screen shows the pre-filled item list with a blank count and no expected quantity or variance; variance appears only after submission.

**From the Food, Beverage & Retail process.** Stock Count is the supervisor's side of counting: start a full, cycle or spot count at a location, watch progress, review the variance once counting is submitted, send lines back for recount, and post. Counting itself mostly happens on the handheld (EMP-066). The one thing to get right is blindness. While a count is open or counting, nobody sees the expected quantity or the variance. Variance appears only after submission, and then never as zero by default.

**Known correction pending (do not draw the wrong version)**

- **Two counting APIs exist side by side. The inventory one (submit counted quantities; recount the whole count with a supervisor PIN) and the F&B one (enter a line; send lines back for recount with no PIN). Flow F30 uses the F&B pair.** Why: The decision says a stock recount needs a supervisor's step-up on the same device. The line recount in F30 has none. One counting model should be chosen, and the recount should carry the step-up. *(source: R144 / F30 step 5 / contracts/satellite/fnb.yaml#requestRecount / contracts/satellite/inventory.yaml#recountStockCount; Food, Beverage & Retail)*
- **No operation ends counting. Statuses go Open → Counting → Closed → Variance review → Posted, but nothing moves a count from Counting to Closed. Variance is "hidden until the count is submitted".** Why: The moment variance is revealed has no action behind it. Draw a "Finish counting" step; the contract needs the operation. *(source: R110 / contracts/satellite/inventory.yaml#/components/schemas/CountStatus; Food, Beverage & Retail)*
- **Posting above the approval amount answers 409 "approval is required". F30's branch says it routes through an approval request.** Why: Other approvals (PO cancel) return a pending state with the request attached. Here the post just fails and nothing raises the approval. *(source: F30 step 4 / contracts/satellite/inventory.yaml#postStockCount; Food, Beverage & Retail)*
- **The first-run state offers "Request recount". The location filter is a "Location id" text field. The status filter is a text field.** Why: First run should offer "Start count". Filters are pickers. *(source: screens/P08-venue-back-office.yaml#BO-079; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which counting API is the build target, the inventory one or the F&B one?** → Drawn default accepted: Draw per-line entry and per-line recount (F30), with the supervisor PIN on recount. *(decided by Chinmay, 2026-10-02; DEC-292 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Are a 2% line tolerance and an AED 1,000.00 posting approval amount accepted?** → Drawn default accepted: Use them in mock-ups. *(decided by Chinmay, 2026-10-02; DEC-293 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Location id | picker: choose a location (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?locationId=` to `listStockCounts`. | `listStockCounts` ?locationId |
| Status | select | optional | — | Open · Counting · Closed · Variance pending · Posted · Cancelled | — | Sends `?status=` to `listStockCounts`. | `listStockCounts` ?status |

**Form: Start stock count** (modal, opened by *Start stock count*; *Start stock count* calls `startStockCount`, *Cancel* sends nothing)

**Collects what `startStockCount` sends before it is called.** Required: `id`, `locationId`, `kind`. Optional: `categoryIds`, `isBlind`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `startStockCount` body |
| Location `locationId` | picker: choose a location | required | — | — | shows names, sends the id | — | `startStockCount` body |
| Kind `kind` | segmented control | required | — | Full · Cycle · Spot | — | — | `startStockCount` body |
| Categorys `categoryIds` | multi-picker: choose categorys | optional | — | — | — | For cycle counts — restrict to these categories. | `startStockCount` body |
| Is blind `isBlind` | toggle | optional | on | — | — | Expected quantities withheld from the counting device. Defaults true because a counter who can see the figure reconciles to it rather than to the shelf. | `startStockCount` body |

Errors to draw in the form: 409 A count is already open for this location

**Form: Post stock count** (modal, opened by *Post stock count*; *Post stock count* calls `postStockCount`, *Cancel* sends nothing)

**Collects what `postStockCount` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 1000 | — | — | `postStockCount` body |

Errors to draw in the form: 409 Unreviewed variance lines remain, or approval is required

**Form: Recount stock count** (modal, opened by *Recount stock count*; *Recount stock count* calls `recountStockCount`, *Cancel* sends nothing)

**Collects what `recountStockCount` sends before it is called.** Required: `reason` and `supervisorStepUp` — a supervisor enters their staff PIN on this device (`principalId`, `credential`); a refused PIN is 403 supervisor-step-up-refused (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | Kept as `StockCount.recountReason`. | `recountStockCount` body |
| Supervisor step up `supervisorStepUp` | group | required | — | — | — | A supervisor signs the act in place, on the device making the call (decided 28 September, audit R144). | `recountStockCount` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `recountStockCount` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `recountStockCount` body |

Errors to draw in the form: 403 The supervisor step-up failed (audit R144). The PIN did not verify, or the principal does not hold `LEDGER_APPROVE` at this venue.; 409 Not in a state that permits this

**Form: Submit counted quantities** (modal, opened by *Submit counted quantities*; *Submit counted quantities* calls `submitCountLines`, *Cancel* sends nothing)

**Collects what `submitCountLines` sends before it is called.** Required: `lines` (each `itemId`, `countedQuantity`, `recordedAt`; optional `unit`, `note`). The item list is pre-filled from on-hand stock with the count blank, and **no expected quantity or variance is shown** (decided 28 September, audit R110). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1; at most 500 | — | — | `submitCountLines` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `submitCountLines` body |
| Counted quantity `lines[].countedQuantity` | number field | required | — | min 0 | — | — | `submitCountLines` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `submitCountLines` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | — | `submitCountLines` body |
| Recorded at `lines[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `submitCountLines` body |

**Form: Enter count line** (modal, opened by *Enter count line*; *Enter count line* calls `enterCountLine`, *Cancel* sends nothing)

**Collects what `enterCountLine` sends before it is called.** Required: `recordedAt`, `itemId`, `countedQuantity`. Optional: `locationId`, `uom`, `batchId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time the line was counted. The second entry for a line replaces the first in this order. | `enterCountLine` body |
| Item `itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `enterCountLine` body |
| Location `locationId` | picker: choose a location | optional | — | — | shows names, sends the id | — | `enterCountLine` body |
| Counted quantity `countedQuantity` | number field | required | — | — | — | — | `enterCountLine` body |
| UOM `uom` | text field | optional | — | — | — | — | `enterCountLine` body |
| Batch `batchId` | picker: choose a batch | optional | — | — | shows names, sends the id | — | `enterCountLine` body |
| Note `note` | text area | optional | — | — | — | — | `enterCountLine` body |

**Form: Request recount** (modal, opened by *Request recount*; *Request recount* calls `requestRecount`, *Cancel* sends nothing)

**Collects what `requestRecount` sends before it is called.** Required: `lineIds`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lineIds` | multi-picker: choose lines | required | — | — | — | — | `requestRecount` body |
| Reason `reason` | text area | optional | — | — | — | — | `requestRecount` body |

**Sent by *Cancel stock count*** (`cancelStockCount`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | Kept as `StockCount.cancelReason`. | `cancelStockCount` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Location**: Location tree picker. Only one open count per location; locations with an open count show "Count in progress". *(source: contracts/satellite/inventory.yaml#startStockCount)*
- **Count type**: Full (everything at the location), Cycle (chosen categories, on rota) or Spot (a few items, e.g. after a damaged delivery). Cycle asks for categories. *(source: contracts/satellite/inventory.yaml#/components/schemas/StartStockCountRequest / F35 step 8)*
- **Blind count**: On by default. Turning it off asks for confirmation ("Counters will see expected quantities"). *(source: R110 / contracts/satellite/inventory.yaml#/components/schemas/StartStockCountRequest)*
- **Recount reason and supervisor PIN**: Sending a whole count back needs a reason and a supervisor's PIN entered on this device. A refused PIN changes nothing. *(source: R144 / contracts/satellite/inventory.yaml#recountStockCount)*

#### Outputs: what the screen shows and produces

**Shown**

**Every stock count** (data table, from `listStockCounts`): **Variance columns stay blank while a count is `open` or `counting`** (decided 28 September, audit R110) — they fill only once the count is submitted.

| Shows | Format | Notes |
|---|---|---|
| Location name | text | — |
| Kind | text | — |
| Status | chip: Open, Counting, Closed, Variance pending, Posted, Cancelled | — |
| Line count | 1,234 | — |
| Counted count | 1,234 | — |
| Variance line count | 1,234 | — |

**The selected stock count** (detail panel, from `listStockCounts`)

| Shows | Format | Notes |
|---|---|---|
| Location name | text | — |
| Kind | text | — |
| Status | chip: Open, Counting, Closed, Variance pending, Posted, Cancelled | — |
| Line count | 1,234 | — |
| Counted count | 1,234 | — |
| Variance line count | 1,234 | — |
| Variance value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Started at | 1 Oct 2026, 14:30 | — |

**The count variance** (detail panel, from `getCountVariance`): **Called only after the count is submitted** (decided 28 September, audit R110). While the count is `open` or `counting` the server answers 409 and the panel reads *Variance appears once the count is submitted* — never a zero.

| Shows | Format | Notes |
|---|---|---|
| Count | the name it points at, never the id | — |
| Total variance value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Exception count | 1,234 | Lines beyond `VenueSettings.inventory.countVarianceTolerancePercent` (proposed default 2 per cent, audit R094), requiring review before … |
| Lines | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Start stock count (primary button) | `startStockCount` POST `/stock-counts` | StartStockCountRequest | StockCount | 409 A count is already open for this location | opens modal first |
| Post stock count (secondary button) | `postStockCount` POST `/stock-counts/{countId}/post` | inline | StockCount | 409 Unreviewed variance lines remain, or approval is required | opens modal first |
| Recount stock count (secondary button) | `recountStockCount` POST `/stock-counts/{countId}/recount` | inline | StockCount | 403 The supervisor step-up failed (audit R144). The PIN did not verify, or the principal does not hold `LEDGER_APPROVE` at this venue.; 409 Not in a state that permits this | step-up: pin (Sends a submitted count back, discarding its variance; a supervisor signs it in place (audit R144).); opens modal first |
| Cancel stock count (destructive button) | `cancelStockCount` POST `/stock-counts/{countId}/cancel` | inline | StockCount | 409 Not in a state that permits this | — |
| Submit counted quantities (secondary button) | `submitCountLines` POST `/stock-counts/{countId}/lines` | inline | inline | — | opens modal first |
| Enter count line (secondary button) | `enterCountLine` POST `/fnb-stock-counts/{countId}/lines` | inline | inline | — | opens modal first |
| Request recount (secondary button) | `requestRecount` POST `/fnb-stock-counts/{countId}/recount` | inline | RecountResult | — | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Count list**: Location, type (Full / Cycle / Spot), status, progress "38 of 46 lines counted", started by, started at. Variance columns are blank (not zero) while Open or Counting. Status words: Open, Counting, Closed, Variance review, Posted, Cancelled. *(source: R110 / contracts/satellite/inventory.yaml#/components/schemas/StockCount)*
- **Variance review**: After submission: per line expected, counted, variance (quantity and %), variance value, times counted, note. Lines beyond the tolerance (proposed 2%) are flagged "Review" and sorted first. Header: total variance value (AED, signed) and the number of exceptions. Before submission the panel reads "Variance appears once the count is submitted". *(source: R110 / R094 / contracts/satellite/inventory.yaml#getCountVariance)*
- **Clean count warning**: A count with no variance at all is shown with a gentle prompt, "No differences found. Check every line was counted", rather than as a success. *(source: F30 step 4)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Start count**: Creates the count with one line per item that has stock at the location (filtered by category for a cycle count). The count is blank. Refused if a count is already open there. *(source: R171 / contracts/satellite/inventory.yaml#startStockCount)*
- **Send lines for recount**: Select lines and give a reason. Those lines reopen on the handheld. The original figure is kept beside the recount. *(source: F30 step 5 / F30 step 6 / contracts/satellite/fnb.yaml#requestRecount)*
- **Post count**: Writes Count gain / Count loss movements for every variance and posts the value. Refused while any exception line is unreviewed. Above the venue's approval amount (proposed AED 1,000.00 total variance) it needs approval. Show "Waiting for approval" rather than an error. *(source: R094 / R171 / contracts/satellite/inventory.yaml#postStockCount / F30 step 4)*
- **Cancel count**: Only before counting starts, with a reason. Once lines are counted the count must be finished or recounted. Hide Cancel then. *(source: contracts/satellite/inventory.yaml#cancelStockCount)*

**Data it reads**: `listStockCounts` (onLoad, List stock counts)

**Where the user goes next**

- → `BO-049` Stock Levels: *Stock Levels*; carries `itemId`
- → `BO-078` Requisitions: *Requisitions*
- → `BO-080` Stock Transfers: *Stock Transfers*
- → `BO-081` Inventory Items: *Inventory Items*; carries `itemId`
- → `BO-137` Recipe Consumption & Theoretical Inventory: *The variance feeds theoretical-against-actual*; carries `countId`; calls `postStockCount`
- → `EMP-066` Stock Count & Cycle Count Management: *The lines are recounted and re-entered*; carries `countId`; calls `requestRecount`

**What opens over it**

- confirmDialog *Cancel stock count*: **Names what `cancelStockCount` changes and what it leaves alone**, in the consequence rather than the verb. A stock count this affects should be identified in the dialog, not just counted. **Collects what `cancelStockCount` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stock count list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stock count untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stock count yet. Offers Request recount (`requestRecount`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on locationId, status and the stock count are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listStockCounts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `recountStockCount`; `LEDGER_POST` for `postStockCount`; `PRODUCT_CONFIGURE` for `startStockCount`, `cancelStockCount` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A count is already open for this location; 409 Count is still open.; 409 Not in a state that permits this; 409 Unreviewed variance lines remain, or approval is required |

#### Edge cases to draw

- **Stock moved during the count (a sale, a transfer)**: Variance uses the expected quantity snapshotted when each line was entered, not the current one. Say so in the variance header ("Expected = system quantity when each line was counted"). *(source: F30 step 7 / contracts/satellite/inventory.yaml#/components/schemas/CountLine)*
- **Counter is offline in a cellar**: Lines queue on the handheld and the count stays Counting. Progress here updates when they sync. *(source: F30 step 2)*

#### Consistency with other screens

- Match `EMP-066`: Same count, same line order, same status words. The handheld enters and this screen reviews and posts.
- Match `BO-082`: Posted variances appear in the movement ledger as Count gain / Count loss, linked to the count.
- Match `BO-137`: Posted variance feeds theoretical-against-actual for F&B.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
count:
  location: Oasis Bistro Kitchen
  type: Cycle
  categories:
  - Dairy
  - Beverages
  blind: true
  status: Variance review
  lines: 46
  counted: 46
  startedBy: Khalid Al Mansoori
  startedAt: 2026-10-20 06:15 GST
variance:
  total: -AED 412.75
  exceptions: 3
  lines:
  - item: Full-cream milk 2 L
    expected: 18
    counted: 12
    variance: -6
    pct: -33.3%
    value: -AED 75.00
    flag: Review
  - item: Coca-Cola 330 ml can
    expected: 240
    counted: 238
    variance: -2
    pct: -0.8%
    value: -AED 3.80
```

#### Permissions

- `listStockCounts` → `PRODUCT_VIEW` (read) · staff
- `startStockCount` → `PRODUCT_CONFIGURE` (configure) · staff
- `postStockCount` → `LEDGER_POST` (operate) · staff
- `recountStockCount` → `LEDGER_APPROVE` (operate) · staff · step-up pin
- `cancelStockCount` → `PRODUCT_CONFIGURE` (configure) · staff
- `submitCountLines` → `PRODUCT_CONFIGURE` (configure) · staff
- `getCountVariance` → `PRODUCT_VIEW` (read) · staff
- `enterCountLine` → `PRODUCT_CONFIGURE` (configure) · staff
- `requestRecount` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listStockCounts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `recountStockCount`; `LEDGER_POST` for `postStockCount`; `PRODUCT_CONFIGURE` for `startStockCount`, `cancelStockCount` …

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.16 | Support physical inventory counts, cycle counts, stock corrections, damaged goods handling, and inventory reconciliation. | Bundles and Promotions | CONTRACTED | `startStockCount` |
| 4.5.15 | Perform periodic inventory counts. | Bundles and Promotions | CONTRACTED | `postStockCount` |
| 4.5.16 | Adjust inventory levels with audit tracking. | Bundles and Promotions | CONTRACTED | `postStockCount` |
| 15.1.24 | Physical Stock Count - System shall support physical inventory counts. | Inventory Management | CONTRACTED | `postStockCount` |
| 15.1.25 | Cycle Count Management - System shall support cycle counting. | Inventory Management | CONTRACTED | `postStockCount` |
| 15.1.26 | Stock Reconciliation - System shall support stock reconciliation. | Inventory Management | CONTRACTED | `postStockCount` |
| 15.1.27 | Variance Reporting - System shall provide stock variance reporting. | Inventory Management | CONTRACTED | `postStockCount` |
| 6.1.21 | The system should be able to generate discrepancy report generated prior to making an inventory adjustment. | Retail POS | CONTRACTED | `getCountVariance` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-079` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 5.dc.html#fnb-5h`, `Retail Board 4.dc.html#ret-4f`, `Inventory Board 3.dc.html#inv-3a`, `Inventory Board 3.dc.html#inv-3d`, `Inventory Board 3.dc.html#inv-3e`, `Inventory Board 3.dc.html#inv-3f`
- Flow F30 *A count is entered, varied and posted*, step 4: The supervisor reviews the variance. → Variance by line and by value. **A count with no variance is a count somebody did not do** — real shelves are never exactly right, and a clean sheet is the first thing a stocktaker queries.
- Flow F30 *A count is entered, varied and posted*, step 5: Three lines look wrong. They send them back. → **Scoped to lines, not the whole count.** Recounting four items is an hour; recounting a cellar is a shift, and a model that only offers the second gets neither.
- Flow F30 *A count is entered, varied and posted*, step 7: The supervisor accepts and posts. → **Movements are written, not levels.** `inventory.stock_level` is derived — four operations wrote it directly until 20 August, and **a stored level and a movement ledger that disagree is a stock …
- Flow F35 *Stock arrives short and an oversell is resolved*, step 8: A cycle count on that line is triggered to confirm the position. → **The count closes the loop.** Theoretical against actual after a damaged delivery, a negative position and two transfers — **and if it still disagrees, the problem was never the delivery.**
- Flow F76 *Stock is counted, requested, transferred and received*, step 1: Stock Count. → **Drawn by the client as RET-4F.** 3 operations on this step.
- Flow F30 branch at step 4 (high): when The variance is above the venue's write-off threshold., Routes through `createApprovalRequest` before it can post. **One approval mechanism, not one per thing approved** — CF-132 settled that, and a write-off is an approval request with a different …
- Flow F30 branch at step 7 (high): when Stock moved between entry and post — a sale, a transfer, a waste record., **The snapshotted theoretical is used, not the current one.** The count measures what was on the shelf when somebody looked at it; **re-deriving at post time would silently absorb the movement into …
- Flow F35 branch at step 8 (low): when The count agrees with the adjusted position., **The loop closes and nothing else happens.** Worth stating as an outcome, because a chain this long with a clean ending is the case a venue needs to be able to reach.
- Flow F76 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-079?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Start stock count, Post stock count, Recount stock count, Cancel stock count, Submit counted quantities, Enter count line, Request recount.
- [ ] Every transition is wired: `BO-049`, `BO-078`, `BO-080`, `BO-081`, `BO-137`, `EMP-066`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `LEDGER_POST`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-080` Stock Transfers

**Move stock between venues, and receive what arrives. Shows inbound and outbound transfers for the venue (decided 28 September, audit R183).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 operate, 1 configure, 1 read); in the flows as storekeeper |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listStockTransfers` reads the population and `getStockTransfer` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `transferId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/inventory/stock-transfers` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 1 board screen(s): Transfers, Distribution & Outlet Receiving. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Retail board operations wired 24 August.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Transfers are received with Receive; a goods receipt needs a supplier purchase order and was attached by resemblance (R254; design-notes correction fnb-retail …

**From the Food, Beverage & Retail process.** Stock Transfers moves stock between any two stock locations: outlet to outlet, warehouse to outlet, outlet to warehouse, and between venues. It shows both outbound and inbound transfers for the venue. Dispatch takes stock out at once and puts it in transit; the receiving store confirms what arrived. The one thing to get right is that a difference between sent and received stays visible at both ends until someone closes it short, with a reason and a supervisor PIN.

**Known correction pending (do not draw the wrong version)**

- **A transfer has no request or approval step. createStockTransfer dispatches immediately. The client and matrix say "transfer with approval workflow".** Why: An outlet cannot ask the warehouse for stock and wait for approval. The person with the stock simply sends it. *(source: DI-362 / MATRIX 4.5.5 / MATRIX 4.5.14 / contracts/satellite/inventory.yaml#/components/schemas/TransferStatus; Food, Beverage & Retail)*
- **The transfer statuses include both "dispatched" and "inTransit", and "cancelled", but no operation cancels a transfer.** Why: Two words for one state goes against the simplicity principle (no granular dispatch statuses). A status no operation reaches is dead. Draw one "In transit" state and no Cancel. *(source: DI-346 / contracts/satellite/inventory.yaml#/components/schemas/TransferStatus; Food, Beverage & Retail)*
- **The table shows fromVenueId, toVenueId and scopePath columns, and the status filter is a text field.** Why: These leak plumbing. Show venue names and a direction badge. *(source: screens/P08-venue-back-office.yaml#BO-080; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): "Create goods receipt" is an action on this screen. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Closing a transfer short with a supervisor PIN (rather than an approval request) was proposed by the coordinator. The R144 decision did not name this act.** → Drawn default accepted: Draw the supervisor PIN on the same device. *(decided by Chinmay, 2026-10-02; DEC-294 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **What is the transfer number format?** → Drawn default accepted: TRF-<venue code>-<six-digit sequence>, as an example only. *(decided by Chinmay, 2026-10-02; DEC-295 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | radio group | optional | — | Dispatched · In transit · Received · Partially received · Cancelled | — | Sends `?status=` to `listStockTransfers`. | `listStockTransfers` ?status |

**Form: Create stock transfer** (modal, opened by *Create stock transfer*; *Create stock transfer* calls `createStockTransfer`, *Cancel* sends nothing)

**Collects what `createStockTransfer` sends before it is called.** Required: `id`, `fromLocationId`, `toLocationId`, `lines`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| From location `fromLocationId` | picker: choose a from location | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| To location `toLocationId` | picker: choose a to location | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createStockTransfer` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `createStockTransfer` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `createStockTransfer` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `createStockTransfer` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockTransfer` body |

Errors to draw in the form: 409 Insufficient stock at the source

**Form: Receive stock transfer** (modal, opened by *Receive stock transfer*; *Receive stock transfer* calls `receiveStockTransfer`, *Cancel* sends nothing)

**Collects what `receiveStockTransfer` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `receiveStockTransfer` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `receiveStockTransfer` body |
| Received quantity `lines[].receivedQuantity` | number field | required | — | min 0 | — | — | `receiveStockTransfer` body |
| Discrepancy reason `lines[].discrepancyReason` | text area | optional | — | max length 500 | — | — | `receiveStockTransfer` body |

Errors to draw in the form: 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short

**Sent by *Close transfer short*** (`closeTransferShort`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | Kept as `StockTransfer.closeShortReason`. | `closeTransferShort` body |
| Supervisor step up `supervisorStepUp` | group | required | — | — | — | A supervisor signs the act in place, on the device making the call (decided 28 September, audit R144). | `closeTransferShort` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `closeTransferShort` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `closeTransferShort` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **From / To**: Location pickers. From defaults to a location at this venue. To may be at another venue of the tenant, and the picker groups locations by venue. From and To cannot be the same. *(source: DI-362 / DI-294 / R183 / contracts/satellite/inventory.yaml#/components/schemas/CreateStockTransferRequest)*
- **Lines**: Item (scan or search), quantity and unit. Show available at the source beside each line; a quantity above it is refused by the server. *(source: contracts/satellite/inventory.yaml#createStockTransfer)*
- **Received quantity (receiving)**: Per line, blank with "Received as sent" shortcut. The difference from the dispatched quantity is shown live as a discrepancy. *(source: contracts/satellite/inventory.yaml#receiveStockTransfer)*
- **Close-short reason and supervisor PIN**: Reason required. A supervisor with stock-approval rights enters their PIN on this device. *(source: R144 / contracts/satellite/inventory.yaml#closeTransferShort)*

#### Outputs: what the screen shows and produces

**Shown**

**Every stock transfer** (data table, from `listStockTransfers`): **Inbound and outbound** (decided 28 September, audit R183) — the list holds every transfer whose source or destination is this venue; each row is marked outbound (`fromVenueId` is this venue) or inbound (`toVenueId` is this venue), and the direction is a filter.

| Shows | Format | Notes |
|---|---|---|
| Transfer number | text | — |
| Status | chip: Dispatched, In transit, Received, Partially received, Cancelled | — |
| Dispatched at | 1 Oct 2026, 14:30 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| From venue | the name it points at, never the id | The venue of `fromLocationId`. Set by the server (audit R183). |
| To venue | the name it points at, never the id | The venue of `toLocationId`. Set by the server (audit R183). |

**The stock transfer** (detail panel, from `getStockTransfer`)

| Shows | Format | Notes |
|---|---|---|
| Transfer number | text | — |
| Status | chip: Dispatched, In transit, Received, Partially received, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Dispatched at | 1 Oct 2026, 14:30 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Close short reason | text | Why the balance was written off, from `closeTransferShort`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create stock transfer (primary button) | `createStockTransfer` POST `/stock-transfers` | CreateStockTransferRequest | StockTransfer | 409 Insufficient stock at the source | opens modal first |
| Receive stock transfer (secondary button) | `receiveStockTransfer` POST `/stock-transfers/{transferId}/receive` | inline | StockTransfer | 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short | opens modal first |
| Close transfer short (destructive button) | `closeTransferShort` POST `/stock-transfers/{transferId}/close-short` | inline | StockTransfer | 403 The supervisor step-up failed (audit R144). The PIN did not verify, or the principal does not hold `LEDGER_APPROVE` at this venue.; 409 Not in a state that permits this | step-up: pin (Writes off stock in transit; a supervisor signs it in place (proposed by the coordinator, client to confirm, audit …) |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Transfer list**: Direction badge (Outbound / Inbound), transfer number, from, to (venue name shown when different), lines, dispatched at, status. Direction is a filter tab: All · Outbound · Inbound. Status words: In transit, Partly received, Received, Closed short, Cancelled. *(source: R183 / contracts/satellite/inventory.yaml#listStockTransfers / DI-346)*
- **Transfer manifest**: What was sent, what arrived, what is missing, per line, plus the cold-chain reading where one was taken. Discrepancies sit with the transfer, not on another screen. *(source: contracts/satellite/inventory.yaml#getStockTransfer)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Send stock (create transfer)**: Dispatches at once. The source decreases and the quantity is "In transit". Refused with "Not enough stock at <location>" when short. *(source: contracts/satellite/inventory.yaml#createStockTransfer)*
- **Receive**: Offered only on inbound transfers that are In transit or Partly received. Received quantities may differ; the difference is recorded against both locations. *(source: R183 / contracts/satellite/inventory.yaml#receiveStockTransfer)*
- **Close short**: Writes off the balance that will not arrive, with a reason and a supervisor PIN. A wrong PIN changes nothing. *(source: R144 / contracts/satellite/inventory.yaml#closeTransferShort)*

**Data it reads**: `listStockTransfers` (onLoad, Inbound and outbound transfers for this venue (decided 28 …)

**Where the user goes next**

- → `BO-078` Requisitions: *Requisitions*
- → `BO-079` Stock Count: *Stock Count*
- → `BO-081` Inventory Items: *Inventory Items*; carries `itemId`
- → `BO-052` Goods Receipt: *Goods Receipt*
- → `BO-051` Purchase Orders: *Goods Receipt*
- → `BO-049` Stock Levels: *The website has already sold four of the damaged units*; carries `itemId`

**What opens over it**

- confirmDialog *Close transfer short*: **Names what `closeTransferShort` changes and what it leaves alone**, in the consequence rather than the verb. A stock transfers this affects should be identified in the dialog, not just counted. **Collects what `closeTransferShort` sends before it is called.** Required: `reason` and …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stock transfers list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stock transfers untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stock transfers yet. Offers Create stock transfer (`createStockTransfer`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the stock transfers are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listStockTransfers` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `closeTransferShort`; `PRODUCT_CONFIGURE` for `createStockTransfer`, `receiveStockTransfer`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient stock at the source; 409 Not in a state that permits this; 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short |

#### Edge cases to draw

- **Damage found only after the cases are opened**: The transfer is received in full, and the damage is a separate adjustment with a damage reason. The claim against the sending store is a separate conversation. *(source: F35 step 3)*
- **Transfer between two venues**: Both venues see it. The sending venue cannot receive it and the receiving venue cannot dispatch it. *(source: R183)*

#### Consistency with other screens

- Match `EMP-064`: Same transfer form, statuses and manifest on the handheld.
- Match `EMP-065`: Receiving a transfer at the door uses the same manifest and the same discrepancy wording.
- Match `BO-049`: In-transit stock appears in valuation as its own line.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- number: TRF-AQP-000087
  direction: Outbound
  from: Main Store
  to: Marina Bay Retail Floor
  status: In transit
  dispatchedAt: 2026-10-21 09:10 GST
  lines:
  - item: Aqua Park logo T-shirt, green, M
    sent: 24
- number: TRF-WWD-000031
  direction: Inbound
  from: Wild Wadi Store (other venue)
  to: Main Store
  status: Partly received
  lines:
  - item: Kids swim goggles, blue
    sent: 100
    received: 92
    missing: 8
```

#### Permissions

- `listStockTransfers` → `PRODUCT_VIEW` (read) · staff
- `createStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff
- `receiveStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff
- `closeTransferShort` → `LEDGER_APPROVE` (operate) · staff · step-up pin
- `getStockTransfer` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listStockTransfers` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `closeTransferShort`; `PRODUCT_CONFIGURE` for `createStockTransfer`, `receiveStockTransfer`.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.15 | Support stock transfers between stores and warehouses including approval workflows, shipment tracking, receiving confirmation, and audit logs. | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 4.5.5 | The system should provide ability to transfer stocks to another store with a approval level | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 4.5.14 | Transfer inventory between locations with approval workflows. | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 15.1.15 | In-Transit Inventory Tracking - System shall track inventory in transit. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.16 | Internal Transfers - System shall support internal transfers. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.17 | Replenishment Management - System shall support warehouse replenishment. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.5.3 | Inter-Venue Transfers - System shall support inter-venue transfers. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.15 | Shipment Tracking - System shall support shipment tracking. | Inventory Management | CONTRACTED | `receiveStockTransfer` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Outlets raise inter-store requisitions subject to an approval workflow before transfer; stock can be transferred between any two stores (outlet-to-outlet, warehouse-to-outlet, outlet-to-warehouse). *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-362)*
- Stock is centralised per venue across web, app, kiosk and POS and not shared across venues; sale is gated by the system-recorded stock (an outlet with no system stock cannot sell even if physically present); inter-venue stock transfer moves stock. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-294)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-080` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 4.dc.html#ret-4d`, `Inventory Board 3.dc.html#inv-3b`, `Inventory Board 3.dc.html#inv-3c`
- Flow F35 *Stock arrives short and an oversell is resolved*, step 4: The rest is received and the transfer closes short. → **Closing short records that the balance will not arrive** — which is the claim. The board called it `raiseTransferClaim`; the contract calls it what it is.
- Flow F35 *Stock arrives short and an oversell is resolved*, step 7: The four orders are sourced from another store instead. → **Sourced rather than cancelled.** A guest who ordered and paid does not care which store it came from, and **cancelling is the outcome a venue reaches when it cannot see the alternative.**
- Flow F76 *Stock is counted, requested, transferred and received*, step 4: Stock Transfers. → **Drawn by the client as RET-4D.** 2 operations on this step.
- Flow F92 *Store stock is watched, replenished and reconciled*, step 4: Stock Transfers. → **Drawn by the client as RET-4D.**

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-080?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create stock transfer, Receive stock transfer, Close transfer short.
- [ ] Every transition is wired: `BO-078`, `BO-079`, `BO-081`, `BO-052`, `BO-051`, `BO-049`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-081` Inventory Items

**What the venue stocks, and where.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 1 · needs the `inventory` module |
| Block | Block A · task APP-SETUP-BO-081 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as storekeeper |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listInventoryItems` reads the population and `getInventoryItem` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `itemId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/inventory/inventory-items` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

**From the Food, Beverage & Retail process.** Inventory Items is the item master: what the venue stocks, in which unit, how it is bought, how it is costed, when it needs reordering, and where it can be held (the location hierarchy). The one thing to get right is which fields lock once stock has moved. Base unit and costing method cannot change after the first movement, and the form must show this before someone tries.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Only one purchase unit and factor per item. The client's examples need several conversions ("1 carton = 24 pieces"; "1 case = 2 litres = 2,000 ml"). (CHG-SBO-005)
- The item master has no "item type" and no status beyond active. (CHG-SBO-005)
- The update operation cannot change barcode, purchase unit, factor, perishable, shelf life or allow-negative-stock. (CHG-SBO-005)
- Stock locations can be created but never renamed, moved in the tree or deactivated. "Transit" is offered as a kind a user can create. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The filters are text fields "Venue id" and "Category id". An "Every stock location" table with raw columns sits beside the item table. (CHG-SBO-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Offer only weighted average and FIFO (agreed), or also standard cost and last purchase price (in the contract)?** → Drawn default stands (answer: "Default / recommended accepted"): Two options. *(decided by Chinmay, 2026-10-02; DEC-041 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Category | picker: choose a category | optional | — | — | shows names, sends the id | A pick list of categories by name; the venue comes from the session. | `InventoryItem.categoryId` |
| Below reorder point | toggle | optional | — | — | — | Sends `?belowReorderPoint=` to `listInventoryItems`. | `listInventoryItems` ?belowReorderPoint |
| Search | text field | optional | — | min length 1; max length 200 | — | Sends `?search=` to `listInventoryItems`. | `listInventoryItems` ?search |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listInventoryItems` ?categoryId |

**Form: Create inventory item** (modal, opened by *Create inventory item*; *Create inventory item* calls `createInventoryItem`, *Cancel* sends nothing)

**Collects what `createInventoryItem` sends before it is called.** Required: `sku`, `name`, `venueId`, `baseUnit`, `costingMethod`. Optional: `barcode`, `categoryId`, `purchaseUnit`, `purchaseUnitFactor`, `reorderPoint`, `reorderQuantity`, `parLevel`, `preferredSupplierId`, `allowNegativeStock`, `isPerishable`, `shelfLifeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| SKU `sku` | text field | required | — | max length 64 | — | — | `createInventoryItem` body |
| Barcode `barcode` | text field | optional | — | max length 128 | — | — | `createInventoryItem` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createInventoryItem` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createInventoryItem` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createInventoryItem` body |
| Base unit `baseUnit` | text field | required | — | — | — | The unit stock is held in. Immutable once movements exist. | `createInventoryItem` body |
| Purchase unit `purchaseUnit` | text field | optional | — | — | — | How the supplier sells it — a case of 24 against a base unit of one. | `createInventoryItem` body |
| Purchase unit factor `purchaseUnitFactor` | number field | optional | 1 | min 0 | — | — | `createInventoryItem` body |
| Costing method `costingMethod` | radio group | required | — | Weighted average · Fifo · Standard cost · Last purchase price | — | Fixed at item creation. Immutable once movements exist. | `createInventoryItem` body |
| Reorder point `reorderPoint` | number field | optional | — | min 0 | — | — | `createInventoryItem` body |
| Reorder quantity `reorderQuantity` | number field | optional | — | min 0 | — | — | `createInventoryItem` body |
| Par level `parLevel` | number field | optional | — | min 0 | — | — | `createInventoryItem` body |
| Preferred supplier `preferredSupplierId` | picker: choose a preferred supplier | optional | — | — | shows names, sends the id | — | `createInventoryItem` body |
| Allow negative stock `allowNegativeStock` | toggle | optional | off | — | — | True permits issue beyond on-hand. Occasionally needed at a bar mid-service; dangerous everywhere else. | `createInventoryItem` body |
| Is perishable `isPerishable` | toggle | optional | off | — | — | — | `createInventoryItem` body |
| Shelf life days `shelfLifeDays` | number field (days) | optional | — | — | — | — | `createInventoryItem` body |

Errors to draw in the form: 400 Validation failed; 409 SKU already in use in this venue

**Form: Save inventory item** (modal, opened by *Save inventory item*; *Save inventory item* calls `updateInventoryItem`, *Cancel* sends nothing)

**Collects what `updateInventoryItem` sends before it is called.** Nothing in the body is required. Optional: `name`, `categoryId`, `reorderPoint`, `reorderQuantity`, `parLevel`, `preferredSupplierId`, `isActive`, `costingMethod`, `baseUnit`. **Category and preferred supplier can be cleared** — each picker has a *None* choice that sends `null` (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateInventoryItem` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | Null clears the category (decided 28 September, audit R171). | `updateInventoryItem` body |
| Reorder point `reorderPoint` | number field | optional | — | min 0 | — | — | `updateInventoryItem` body |
| Reorder quantity `reorderQuantity` | number field | optional | — | min 0 | — | — | `updateInventoryItem` body |
| Par level `parLevel` | number field | optional | — | min 0 | — | — | `updateInventoryItem` body |
| Preferred supplier `preferredSupplierId` | picker: choose a preferred supplier | optional | — | — | shows names, sends the id | Null clears the preferred supplier (decided 28 September, audit R171). | `updateInventoryItem` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateInventoryItem` body |
| Costing method `costingMethod` | radio group | optional | — | Weighted average · Fifo · Standard cost · Last purchase price | — | Fixed at item creation. Immutable once movements exist. | `updateInventoryItem` body |
| Base unit `baseUnit` | text field | optional | — | — | — | Changeable only while `hasMovements` is false; the 409 below is the refusal once it is true. | `updateInventoryItem` body |

Errors to draw in the form: 409 Attempt to change costing method or base unit after movements exist

**Form: Create stock location** (modal, opened by *Create stock location*; *Create stock location* calls `createStockLocation`, *Cancel* sends nothing)

**Collects what `createStockLocation` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`. Optional: `parentLocationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createStockLocation` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createStockLocation` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createStockLocation` body |
| Kind `kind` | select | required | — | Main store · Sub store · Kitchen · Bar · Retail floor · Cellar · Transit | — | — | `createStockLocation` body |
| Parent location `parentLocationId` | picker: choose a parent location | optional | — | — | shows names, sends the id | — | `createStockLocation` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Base unit**: The unit stock is held and counted in (piece, can, bottle, kg, litre, ml). Required. Locked with a lock icon and "Used in stock movements, cannot change" once the item has movements. *(source: contracts/satellite/inventory.yaml#/components/schemas/InventoryItem / contracts/satellite/inventory.yaml#updateInventoryItem)*
- **Purchase unit and factor**: How the supplier sells it, written as a sentence the user completes: "1 [case] = [24] [can]". Default factor 1. *(source: DI-343 / contracts/satellite/inventory.yaml#/components/schemas/CreateInventoryItemRequest)*
- **Costing method**: Weighted average or FIFO. Required at creation. Locked once the item has movements, with the reason shown. *(source: DI-344 / contracts/satellite/inventory.yaml#createInventoryItem)*
- **Reorder point / Reorder quantity / Par level**: Helper text: reorder point is when to reorder, reorder quantity is how much a suggestion orders, and par level is the level to top up to. All three are in the base unit. Reorder alerts and suggested requisitions run from them. *(source: DI-345 / DI-234 / contracts/satellite/inventory.yaml#getSuggestedRequisitions)*
- **Preferred supplier**: Picker of the tenant's active suppliers. Suppliers on hold are not offered. Can be cleared with "None". *(source: R171 / R183 / contracts/satellite/inventory.yaml#updateInventoryItem)*
- **Perishable and shelf life**: Perishable off by default. On, "Shelf life (days)" shows, and every goods receipt of this item needs an expiry date. *(source: DI-345 / contracts/satellite/inventory.yaml#/components/schemas/CreateGoodsReceiptRequest)*
- **Allow negative stock**: Off by default. Turning it on shows "Only for bar items mid-service. Issues can exceed what is recorded on hand." *(source: contracts/satellite/inventory.yaml#/components/schemas/CreateInventoryItemRequest)*
- **Kit components**: For a retail bundle sold as one item: components and the quantity per kit. A component cannot itself be a kit, and an item with its own movements cannot become one. Kit availability is "fewest whole kits the components make". *(source: MATRIX 4.4.20 / contracts/satellite/inventory.yaml#setInventoryKitDefinition)*
- **Stock location (setup)**: Code, name, kind (Main store, Sub-store, Kitchen, Bar, Retail floor, Cellar) and parent location. Shown as an editable tree on its own "Locations" tab. *(source: DI-345 / contracts/satellite/inventory.yaml#createStockLocation)*

#### Outputs: what the screen shows and produces

**Shown**

**Items** (data table, from `listInventoryItems`)

| Shows | Format | Notes |
|---|---|---|
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Costing method | chip: Weighted average, Fifo, Standard cost, Last purchase price | Fixed at item creation. Immutable once movements exist. |
| Reorder quantity | 1,234.5 | — |
| Par level | 1,234.5 | — |

**Stock locations** (tree nav, from `listStockLocations`): On its own tab, as a tree (parent and children), not a raw table beside the items.

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Main store, Sub store, Kitchen, Bar, Retail floor, Cellar… | — |
| Is active | yes / no (icon or chip) | — |

**The selected inventory** (detail panel, from `getInventoryItem`)

| Shows | Format | Notes |
|---|---|---|
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Base unit | text | The unit stock is held in. Immutable once movements exist. |
| Purchase unit | text | How the supplier sells it — a case of 24 against a base unit of one. |
| Costing method | chip: Weighted average, Fifo, Standard cost, Last purchase price | Fixed at item creation. Immutable once movements exist. |
| Reorder quantity | 1,234.5 | — |
| Par level | 1,234.5 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create inventory item (primary button) | `createInventoryItem` POST `/inventory-items` | CreateInventoryItemRequest | InventoryItem | 400 Validation failed; 409 SKU already in use in this venue | opens modal first |
| Save inventory item (secondary button) | `updateInventoryItem` PATCH `/inventory-items/{itemId}` | inline | InventoryItem | 409 Attempt to change costing method or base unit after movements exist | opens modal first |
| Lookup inventory item (secondary button) | `lookupInventoryItem` GET `/inventory-items/lookup` | — | InventoryItem | 400 Neither barcode nor SKU supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Create stock location (secondary button) | `createStockLocation` POST `/stock-locations` | inline | StockLocation | — | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Item list**: Name, SKU, category, base unit, purchase unit ("case of 24"), costing method, on hand (all locations), reorder point, and a "Below reorder point" badge. Filters: category, below reorder point, search (name, SKU, barcode), scan. *(source: contracts/satellite/inventory.yaml#listInventoryItems)*
- **Item detail**: Stock by location (on hand, allocated, available), on order, in transit, average cost and last purchase price (AED), and an "In use since <date>, base unit and costing method locked" note when it has movements. *(source: contracts/satellite/inventory.yaml#getInventoryItem)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Add item**: Refused when the SKU is already used in this venue. The SKU field shows the error. *(source: contracts/satellite/inventory.yaml#createInventoryItem)*
- **Save changes**: Changing a locked field is refused. The form never offers it once locked, so the refusal should not normally be reached. *(source: contracts/satellite/inventory.yaml#updateInventoryItem)*
- **Add location**: Adds a node to the location tree under the chosen parent. *(source: contracts/satellite/inventory.yaml#createStockLocation)*

**Data it reads**: `listInventoryItems` (onLoad, List inventory items); `listStockLocations` (onLoad, List stock locations); `getInventoryKitDefinition` (onLoad, Show kit components)

**Where the user goes next**

- → `BO-078` Requisitions: *Requisitions*
- → `BO-079` Stock Count: *Stock Count*
- → `BO-080` Stock Transfers: *Stock Transfers*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory items list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory items untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory items yet. Offers Create inventory item (`createInventoryItem`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, categoryId, belowReorderPoint, search and the inventory items are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listInventoryItems` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createInventoryItem`, `updateInventoryItem`, `createStockLocation`, `setInventoryKitDefinition`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither barcode nor SKU supplied; 400 Validation failed; 409 Attempt to change costing method or base unit after movements exist; 409 SKU already in use in this venue |

#### Edge cases to draw

- **Item deactivated while stock is on hand**: Warn "<n> still on hand at <locations>". Deactivation does not remove stock. *(source: designer default)*
- **Scan with no signal in a store room**: Item lookup by barcode works offline from cache. *(source: contracts/satellite/inventory.yaml#lookupInventoryItem)*

#### Consistency with other screens

- Match `BO-048`: A merchandise item links to an inventory item from this master. Retail and F&B share one item master.
- Match `BO-078`: The units offered on a requisition line are this item's base and purchase units.
- Match `BO-052`: The perishable flag here makes expiry mandatory at receipt.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
items:
- name: Coca-Cola 330 ml can
  sku: BEV-CC-330
  category: Beverages
  baseUnit: can
  purchase: 1 case = 24 can
  costing: Weighted average
  reorderPoint: 240
  reorderQuantity: 480
  parLevel: 720
  preferredSupplier: Emirates Beverage Trading LLC
  averageCost: AED 1.90
- name: Full-cream milk 2 L
  sku: DRY-MLK-2L
  category: Dairy
  baseUnit: bottle
  purchase: 1 crate = 6 bottle
  costing: FIFO
  perishable: true
  shelfLifeDays: 7
  preferredSupplier: Gulf Fresh Dairy LLC
- name: Beach day kit (towel + goggles + pouch)
  sku: KIT-BCH-01
  kit:
  - component: Beach towel, blue
    qty: 1
  - component: Kids swim goggles, blue
    qty: 1
  - component: Waterproof phone pouch
    qty: 1
locations:
- Main Store (main store)
- '  Food Store (sub-store)'
- '    Cold Room (sub-store)'
- '  Beverage Store (sub-store)'
- Oasis Bistro Kitchen (kitchen)
- Pool Bar (bar)
- Marina Bay Retail Floor (retail floor)
```

#### Permissions

- `listInventoryItems` → `PRODUCT_VIEW` (read) · staff
- `getInventoryItem` → `PRODUCT_VIEW` (read) · staff
- `createInventoryItem` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateInventoryItem` → `PRODUCT_CONFIGURE` (configure) · staff
- `lookupInventoryItem` → `PRODUCT_VIEW` (read) · staff
- `listStockLocations` → `PRODUCT_VIEW` (read) · staff
- `createStockLocation` → `PRODUCT_CONFIGURE` (configure) · staff
- `getInventoryKitDefinition` → `PRODUCT_VIEW` (read) · staff
- `setInventoryKitDefinition` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listInventoryItems` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createInventoryItem`, `updateInventoryItem`, `createStockLocation`, `setInventoryKitDefinition`.

#### Requirements it meets

33 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 15.5.9 | Inventory APIs - System shall expose inventory APIs. | Inventory Management | CONTRACTED | `listInventoryItems` |
| 15.5.10 | Procurement APIs - System shall expose procurement APIs. | Inventory Management | CONTRACTED | `listInventoryItems` |
| 15.5.11 | Warehouse APIs - System shall expose warehouse APIs. | Inventory Management | CONTRACTED | `listInventoryItems` |
| 4.5.35 | FIFO, LIFO, and Weighted Average costing methods. | Bundles and Promotions | CONTRACTED | `createInventoryItem` |
| 7.4.33 | It is expected that the software can sell PLUs considered as simple items which could possibly be inventory managed. | F&B POS | CONTRACTED | `createInventoryItem` |
| 7.4.34 | Food and Beverage PLUs can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `createInventoryItem` |
| 7.4.35 | Retail PLUs can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `createInventoryItem` |
| 7.4.39 | Wristbands can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `createInventoryItem` |
| 10.1.4 | The system should be able to sync all the SKU products and Standalone SKU products from the inventory management and make it available to sell as per availability and pricing strategy. | Games & F&B Integration | CONTRACTED | `createInventoryItem` |
| 15.1.1 | Inventory Item Master - System shall support centralized inventory item management. | Inventory Management | CONTRACTED | `createInventoryItem` |
| 15.1.2 | Item Categories - System shall support inventory item categorization. | Inventory Management | CONTRACTED | `createInventoryItem` |
| 15.1.3 | SKU Management - System shall support SKU management. | Inventory Management | CONTRACTED | `createInventoryItem` |
| … 21 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Warehouse/location structure is a customisable hierarchy (e.g. main warehouse → food warehouse → beverage warehouse), with stock received centrally or directly at an outlet/kitchen for fast-moving perishables. Expiry is tracked at batch/date level; reorder alerts notify staff at a minimum threshold. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-345)*
- Item Master captures category, item type, status and unit of measurement, with pack-size conversions (e.g. 1 carton = 24 pieces; 1 case = 2 litres = 2000 ml). *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-343)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-081` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 4.dc.html#ret-4b`, `Inventory Board 1.dc.html#inv-2`, `Inventory Board 1.dc.html#inv-3`, `Inventory Board 1.dc.html#inv-4`, `Inventory Board 1.dc.html#inv-5`, `Inventory Board 2.dc.html#inv-2b`
- Flow F76 *Stock is counted, requested, transferred and received*, step 2: Inventory Items. → **Drawn by the client as RET-4B.** 7 operations on this step.
- Flow F92 *Store stock is watched, replenished and reconciled*, step 2: Inventory Items. → **Drawn by the client as RET-4B.**

#### Acceptance for the design

- [ ] Every input above is drawn (33), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-081?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create inventory item, Save inventory item, Lookup inventory item, Create stock location.
- [ ] Every transition is wired: `BO-078`, `BO-079`, `BO-080`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-082` Stock Movements

**Every movement, and why it happened.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 1 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listStockMovements` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/inventory/stock-movements` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Moved to wave 1 on 24 August.** F34 walks a retail sale and its return, which is a wave-1 journey — **a venue that can take a return and cannot disposition the item puts damaged stock back on the shelf**, and the count finds it three weeks later.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): An "Every order" table (sales orders) and "Create stock transfer" sit on the movement ledger, attached through F35 step 7; sourcing belongs with transfers … Removed 2 October 2026 (CHG-WIR-008): An "Every order" table (sales orders) and "Create stock transfer" sit on the movement ledger, attached through F35 step 7; sourcing belongs with transfers …

**From the Food, Beverage & Retail process.** Stock Movements is the ledger. Every change to stock is a movement with a kind, a reason, a person and a source: receipts, sales, transfers, counts, waste, adjustments. On hand is derived from it. It is also where a manager records a manual adjustment, issue or waste. The one thing to get right is direction. Quantity is always entered positive, and the kind decides whether stock goes up or down.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The reason is free text only (up to 500 characters). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): An "Every order" table (sales orders) and a "Create stock transfer" button sit on the ledger. (CHG-WIR-008); F34 step 8 dispositions a returned item here with a manual movement. The retail return already restocks or writes off by condition. (CHG-CLN-005); The item, location and kind filters are text fields ("Item id", "Location id", "Kind"). (CHG-SBO-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Item | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `InventoryItem.id` |
| Location | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `StockLocation.id` |
| Kind | select | optional | — | Receipt · Issue · Sale depletion · Waste · Adjustment in · Adjustment out · Transfer out · Transfer in · Count gain · Count loss · Supplier return · Production | — | Movement kinds in words, as chips. | `StockMovement.kind` |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listStockMovements`. | `listStockMovements` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listStockMovements`. | `listStockMovements` ?recordedTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Item | picker: choose an item | — | — | `listStockMovements` ?itemId |
| Location | picker: choose a location | — | — | `listStockMovements` ?locationId |
| Kind | select | — | Receipt · Issue · Sale depletion · Waste · Adjustment in · Adjustment out · Transfer out · Transfer in · Count gain · Count loss · Supplier return · Production | `listStockMovements` ?kind |
| Category | picker: choose a category | — | — | `listInventoryItems` ?categoryId |
| Below reorder point | toggle | — | — | `listInventoryItems` ?belowReorderPoint |
| Search | text field | — | min length 1; max length 200 | `listInventoryItems` ?search |

**Form: Create stock movement** (modal, opened by *Create stock movement*; *Create stock movement* calls `createStockMovement`, *Cancel* sends nothing)

**Collects what `createStockMovement` sends before it is called.** Required: `id`, `itemId`, `locationId`, `kind`, `quantity`, `recordedAt`. Optional: `unit`, `reason`, `costCenterId`. **The kind picker offers `adjustmentIn` and `adjustmentOut`** (and issue, waste, supplierReturn); the kind decides the direction, so **quantity is entered positive** and the field refuses a sign. **Reason is required for adjustmentIn, adjustmentOut and waste** — the dialog will not confirm without it and the server refuses 400 (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createStockMovement` body |
| Item `itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createStockMovement` body |
| Location `locationId` | picker: choose a location | required | — | — | shows names, sends the id | — | `createStockMovement` body |
| Kind `kind` | select | required | — | Receipt · Issue · Sale depletion · Waste · Adjustment in · Adjustment out · Transfer out · Transfer in · Count gain · Count loss · Supplier return · Production | — | The kind decides the direction (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` (the finished item entering stock; the … | `createStockMovement` body |
| Quantity `quantity` | number field | required | — | more than 0 | — | Always positive. The `kind` decides whether it adds or removes stock, not the sign (decided 28 September, audit R171). | `createStockMovement` body |
| Unit `unit` | text field | optional | — | — | — | — | `createStockMovement` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required for `adjustmentIn`, `adjustmentOut` and `waste` (decided 28 September, audit R171); adjustments are reported separately. | `createStockMovement` body |
| Cost center `costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | — | `createStockMovement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockMovement` body |

Errors to draw in the form: 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock, and the item does not permit negative balances

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Kind (manual entry)**: Offer only the kinds a person records by hand: Issue (to a cost centre), Waste, Adjustment in, Adjustment out, Return to supplier. Receipt, Sale, Transfer in/out, Count gain/loss and Production are written by their own screens and appear only in the ledger. *(source: R171 / contracts/satellite/inventory.yaml#/components/schemas/MovementKind)*
- **Quantity**: Positive number only; the field refuses a sign. Beside it, a live preview "Stock after: 42 → 36 can" in the item's unit. *(source: R171 / contracts/satellite/inventory.yaml#/components/schemas/CreateStockMovementRequest)*
- **Reason**: Required for Adjustment in, Adjustment out and Waste (up to 500 characters). Draw it as a reason list plus a note, with "Other" requiring the note. *(source: R171 / R222 / DI-363)*
- **Cost centre**: Picker, shown for Issue. It decides where the cost is booked. *(source: contracts/satellite/inventory.yaml#/components/schemas/CreateStockMovementRequest)*
- **Ledger filters**: Item (search or scan), location (tree), kind (multi-select of the words below), date range (Recorded from / to). Never id text fields. *(source: contracts/satellite/inventory.yaml#listStockMovements)*

#### Outputs: what the screen shows and produces

**Shown**

**Movements** (data table, from `listStockMovements`): `countGain` and `countLoss` rows are shown (posted by a stock count), never entered here; quantity is always positive and the kind shows the direction (decided 28 September, audit R171).

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Receipt, Issue, Sale depletion, Waste, Adjustment in, Adjustment out… | The kind decides the direction (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` … |
| Quantity | 1,234.5 | Always positive. The `kind` decides whether it adds or removes stock, not the sign (decided 28 September, audit R171). |
| Unit | text | — |
| Reason | text | Required for `adjustmentIn`, `adjustmentOut` and `waste` (decided 28 September, audit R171); adjustments are reported separately. |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Balance after | 1,234.5 | — |
| Unit cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The selected stock movement** (detail panel, from `listStockMovements`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Receipt, Issue, Sale depletion, Waste, Adjustment in, Adjustment out… | The kind decides the direction (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` … |
| Quantity | 1,234.5 | Always positive. The `kind` decides whether it adds or removes stock, not the sign (decided 28 September, audit R171). |
| Unit | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Balance after | 1,234.5 | — |
| Unit cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Source type | text | What generated it — an order, a count, a transfer. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create stock movement (primary button) | `createStockMovement` POST `/stock-movements` | CreateStockMovementRequest | StockMovement | 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock, and the item does not permit negative balances | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Ledger table**: Date and time (GST), item, location, kind in words, signed quantity derived from the kind (green +12, red -6), balance after, unit cost and total cost (AED), reason, by whom, and source as a readable link ("Sale AQP-104582", "Count 20 Oct, Oasis Bistro Kitchen", "Transfer TRF-AQP-000087"). Newest first. *(source: R171 / contracts/satellite/inventory.yaml#/components/schemas/StockMovement)*
- **Kind words**: Receipt · Issue · Sale · Waste · Adjustment in · Adjustment out · Transfer out · Transfer in · Count gain · Count loss · Return to supplier · Production. *(source: contracts/satellite/inventory.yaml#/components/schemas/MovementKind / R131)*
- **Adjustments view**: A saved filter "Adjustments and waste", because adjustments are reported separately. Frequent adjustments on one item are the shrinkage signal; sort that view by count per item. *(source: contracts/satellite/inventory.yaml#createStockMovement)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Record movement**: Writes the movement and shows the new balance. Refused when stock is insufficient and the item does not allow negative stock; say "Only 4 on hand at Pool Bar". Not available offline. *(source: contracts/satellite/inventory.yaml#createStockMovement)*

**Data it reads**: `listStockMovements` (onLoad, The movement ledger); `listInventoryItems` (onLoad, List inventory items (the pick list)); `listStockLocations` (onLoad, List stock locations (the pick list))

**Where the user goes next**

- → `BO-079` Stock Count: *A cycle count on that line is triggered to confirm the position*
- → `BO-078` Requisitions: *Requisitions*
- → `BO-080` Stock Transfers: *Stock Transfers*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stock movements list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stock movements untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stock movements yet. Offers Create stock movement (`createStockMovement`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on itemId, locationId, kind, recordedFrom, recordedTo and the stock movements are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listStockMovements` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createStockMovement`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock, and the item does not permit negative balances |

#### Edge cases to draw

- **A returned retail item is resaleable, damaged or going back to the supplier**: The retail return already restocks or writes off by condition. This screen records only the supplier return of written-off stock. It must not restock a second time. *(source: F34 step 7 / contracts/satellite/retail.yaml#createRetailReturn)*
- **Kit sold**: The ledger shows one Sale line per component, never a line for the kit itself. *(source: contracts/satellite/inventory.yaml#setInventoryKitDefinition)*

#### Consistency with other screens

- Match `EMP-067`: The handheld's damage/loss form records the same kinds with the same reason list.
- Match `BO-139`: F&B wastage uses the same reason list and appears in this ledger as Waste.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- at: 2026-10-21 14:05 GST
  item: Coca-Cola 330 ml can
  location: Pool Bar
  kind: Sale
  qty: '-2'
  balanceAfter: 180
  source: Sale AQP-104582
- at: 2026-10-21 11:30 GST
  item: Full-cream milk 2 L
  location: Oasis Bistro Kitchen
  kind: Waste
  qty: '-3'
  reason: Spoiled, fridge door left open
  by: Fatima Al Suwaidi
  totalCost: AED 37.50
- at: 2026-10-20 18:40 GST
  item: Full-cream milk 2 L
  location: Oasis Bistro Kitchen
  kind: Count loss
  qty: '-6'
  source: Count 20 Oct, Oasis Bistro Kitchen
```

#### Permissions

- `listStockMovements` → `PRODUCT_VIEW` (read) · staff
- `createStockMovement` → `PRODUCT_CONFIGURE` (configure) · staff
- `listInventoryItems` → `PRODUCT_VIEW` (read) · staff
- `listStockLocations` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listStockMovements` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createStockMovement`.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.13 | Maintain real-time inventory balances and automatically update stock after sales, returns, transfers, adjustments, and goods receipt transactions. | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 4.5.1 | The system should be able to sync all the products and associated information from the inventory management on real-time or timed intervals, to be able to scan/search for the product and complete the … | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 4.5.2 | The system should be able to sync all the product sale and return products between POS and inventory in order to push data back to inventory management tools to manage re-order levels. | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 15.1.16 | Damaged Inventory Tracking - System shall track damaged inventory. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.17 | Goods Receipt - System shall support inventory receipt transactions. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.18 | Inventory Adjustments - System shall support stock adjustments. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.19 | Stock Consumption - System shall record stock consumption. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.20 | Return to Stock - System shall support stock returns. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.21 | Write-Off Management - System shall support inventory write-offs. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.22 | Inventory Movement History - System shall maintain inventory movement history. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.23 | Inventory Audit Trail - System shall maintain inventory audit logs. | Inventory Management | CONTRACTED | `createStockMovement` |
| 17.6.4 | Maintenance Inventory Integration - System shall integrate with inventory management. | Maintenance & Safety Management | CONTRACTED | `createStockMovement` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-082` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 4.dc.html#ret-4g`, `Inventory Board 1.dc.html#inv-8`, `Inventory Board 2.dc.html#inv-2j`

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-082?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create stock movement.
- [ ] Every transition is wired: `BO-079`, `BO-078`, `BO-080`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-083` Suppliers

**Who we buy from, and what they quoted. Suppliers are the tenant's; a venue sees them read-only and records quotations (decided 28 September, audit R183).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `inventory` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PROCUREMENT_MANAGE`, `PROCUREMENT_VIEW`, `REPORT_VIEW_VENUE` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSuppliers` reads the population and `getSupplierPerformance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `supplierId` (deepLink), `contractId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/inventory/suppliers` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Retail board operations wired 24 August.**

**Known gaps.** **`getSupplierPerformance` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.

**From the Food, Beverage & Retail process.** Suppliers is the tenant's supplier master, read-only at venue level, together with what each supplier quoted, their contracts and their performance. The one thing to get right is ownership. Suppliers are created and edited at tenant level. A venue user sees them read-only and records quotations against them for the venue.

**Known correction pending (do not draw the wrong version)**

- **The supplier has no category (F&B, retail, engineering), no linked item categories and no compliance documents.** Why: The client's supplier master and the matrix ("Supplier master with classification") need them, and spend by category depends on them. *(source: DI-347 / MATRIX 15.3.1; Food, Beverage & Retail)*
- **The update request names the field "paymentTermDays" and takes a "contacts" array. The supplier record has "paymentTermsDays" and flat contact fields. Create takes both "isActive" and "status".** Why: The names mismatch and the duplicated active flag will drift. *(source: contracts/satellite/inventory.yaml#updateSupplier / contracts/satellite/inventory.yaml#/components/schemas/Supplier; Food, Beverage & Retail)*
- **The supplier contract carries validity and terms but no prices or items.** Why: The agreed Contract PO type picks a pre-agreed price automatically on later orders. Without price lines nothing can be picked. *(source: DI-348 / contracts/satellite/inventory.yaml#/components/schemas/InventorySupplierContract; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Navigation exits to Stock Count and Stock Transfers. (CHG-WIR-009).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Supplier | picker: choose a supplier | — | — | `listSupplierContracts` ?supplierId |
| Status | radio group | — | Draft · Active · Expired · Terminated | `listSupplierContracts` ?status |
| Expiring before | date picker | — | — | `listSupplierContracts` ?expiringBefore |

**Form: Create supplier** (modal, opened by *Create supplier*; *Create supplier* calls `createSupplier`, *Cancel* sends nothing)

**Collects what `createSupplier` sends before it is called.** Required: `id`, `code`, `name`. Optional: `contactName`, `contactEmail`, `contactPhone`, `taxRegistrationNumber`, `paymentTermsDays`, `leadTimeDays`, `currency`, `accountId`, `isActive`, `status`, `statusReason`, `minimumOrderValue` and 1 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createSupplier` body |
| Code `code` | text field | required | — | max length 64 | — | Unique per tenant (decided 28 September, audit R108). | `createSupplier` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createSupplier` body |
| Contact name `contactName` | text field | optional | — | — | — | — | `createSupplier` body |
| Contact email `contactEmail` | text field | optional | — | — | — | — | `createSupplier` body |
| Contact phone `contactPhone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `createSupplier` body |
| Tax registration number `taxRegistrationNumber` | text field | optional | — | — | — | — | `createSupplier` body |
| Payment terms days `paymentTermsDays` | number field (days) | optional | — | — | — | — | `createSupplier` body |
| Lead time days `leadTimeDays` | number field (days) | optional | — | — | — | — | `createSupplier` body |
| Currency `currency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | — | `createSupplier` body |
| Account `accountId` | picker: choose an account | optional | — | — | shows names, sends the id | — | `createSupplier` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createSupplier` body |
| Status `status` | radio group | optional | — | Active · On hold · Suspended · Terminated | — | Set by `updateSupplier`. A supplier on hold stops appearing in requisitions and purchase orders while its history stays intact. | `createSupplier` body |
| Status reason `statusReason` | text field | optional | — | — | — | — | `createSupplier` body |
| Minimum order value `minimumOrderValue` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createSupplier` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `createSupplier` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Record quotation** (modal, opened by *Record quotation*; *Record quotation* calls `recordQuotation`, *Cancel* sends nothing)

**Collects what `recordQuotation` sends before it is called.** Required: `requisitionId`, `lines`, `validUntil`. Optional: `reference`, `leadTimeDays`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Requisition `requisitionId` | picker: choose a requisition | required | — | — | shows names, sends the id | — | `recordQuotation` body |
| Reference `reference` | text field | optional | — | max length 128 | — | — | `recordQuotation` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `recordQuotation` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `recordQuotation` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `recordQuotation` body |
| Unit price `lines[].unitPrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `recordQuotation` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `recordQuotation` body |
| Lead time days `leadTimeDays` | number field (days) | optional | — | — | — | — | `recordQuotation` body |
| Valid until `validUntil` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `recordQuotation` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `recordQuotation` body |

**Form: Save supplier** (modal, opened by *Save supplier*; *Save supplier* calls `updateSupplier`, *Cancel* sends nothing)

**Collects what `updateSupplier` sends before it is called.** Nothing in the body is required. Optional: `name`, `status`, `statusReason`, `paymentTermDays`, `leadTimeDays`, `minimumOrderValue`, `contacts`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | — | — | — | `updateSupplier` body |
| Status `status` | radio group | optional | — | Active · On hold · Suspended · Terminated | — | — | `updateSupplier` body |
| Status reason `statusReason` | text field | optional | — | — | — | — | `updateSupplier` body |
| Payment term days `paymentTermDays` | number field (days) | optional | — | — | — | — | `updateSupplier` body |
| Lead time days `leadTimeDays` | number field (days) | optional | — | — | — | — | `updateSupplier` body |
| Minimum order value `minimumOrderValue` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateSupplier` body |
| Contacts `contacts` | repeatable rows | optional | — | — | — | — | `updateSupplier` body |
| Name `contacts[].name` | text field | optional | — | — | — | — | `updateSupplier` body |
| Email `contacts[].email` | text field | optional | — | — | — | — | `updateSupplier` body |
| Phone `contacts[].phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `updateSupplier` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Supplier details (tenant scope)**: Code (unique in the tenant), name, contact, TRN (tax registration number), currency (ISO, default AED), payment terms in days, lead time in days, minimum order value. At venue scope every field is read-only and the edit button is absent. *(source: R183 / R108 / contracts/satellite/inventory.yaml#createSupplier)*
- **Status**: Active, On hold, Suspended, Terminated, with a reason when not active. On hold stops the supplier appearing in new requisitions and orders; history stays. *(source: contracts/satellite/inventory.yaml#updateSupplier)*
- **Quotation**: Recorded against an approved request: supplier's reference, lines (item, quantity, unit price), lead time, valid until (required). Chosen from the request side (BO-078) or here with a request picker. *(source: R183 / contracts/satellite/inventory.yaml#recordQuotation)*
- **Supplier contract**: Number (unique per supplier), name, valid from / to, currency, payment terms, signed document. Created as Draft, or Active when the signed document is attached. *(source: contracts/satellite/inventory.yaml#createSupplierContract)*

#### Outputs: what the screen shows and produces

**Shown**

**Every supplier** (data table, from `listSuppliers`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Unique per tenant (decided 28 September, audit R108). |
| Name | text | — |
| Contact name | text | — |
| Contact email | text | — |
| Contact phone | +971 50 123 4567 | — |
| Tax registration number | text | — |

**Supplier performance** (detail panel, from `getSupplierPerformance`): Shows `ordersPlaced`, `onTimeInFullPercent`, `averageDaysLate`, `shortDeliveryPercent`, `rejectionPercent`, `rejectionReasons`, `priceVariancePercent` from `getSupplierPerformance`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Orders placed | 1,234 | — |
| On time in full percent | 1,234.5 | — |
| Average days late | 1,234.5 | — |
| Short delivery percent | 1,234.5 | — |
| Rejection percent | 1,234.5 | — |
| Rejection reasons | grouped details | Rejected receipt lines counted by rejection reason, keyed by the reason. Sourced from the reason recorded against each rejected goods … |
| Price variance percent | 1,234.5 | Quoted against invoiced. The number that finds a supplier quietly raising prices, which no delivery record shows. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create supplier (primary button) | `createSupplier` POST `/suppliers` | Supplier | Supplier | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | gated `PROCUREMENT_MANAGE`; opens modal first |
| Record quotation (secondary button) | `recordQuotation` POST `/suppliers/{supplierId}/quotations` | CreateQuotationRequest | Quotation | — | gated `PROCUREMENT_MANAGE`; opens modal first |
| Save supplier (secondary button) | `updateSupplier` PUT `/suppliers/{supplierId}` | inline | Supplier | — | gated `PROCUREMENT_MANAGE`; opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Supplier list**: Code, name, status badge, currency, payment terms, lead time, active contracts count. No raw account or id columns. *(source: contracts/satellite/inventory.yaml#listSuppliers)*
- **Performance scorecard**: For a chosen period: orders placed, on time in full %, average days late, short delivery %, rejection % with reasons, price variance % (quoted vs invoiced). OTIF is the headline number. *(source: DI-347 / R158 / contracts/satellite/reporting.yaml#getSupplierPerformance)*
- **Contracts tab**: Contracts sorted by expiry. "Expiring within 30 days" highlighted, because someone has to renew them. *(source: contracts/satellite/inventory.yaml#listSupplierContracts)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Add supplier / Save supplier**: Tenant scope only. A duplicate code is refused, and the code field says so. *(source: R183 / R108)*
- **End contract**: Terminate with a reason. A terminated or expired contract is never reopened; renewal is a new contract. *(source: contracts/satellite/inventory.yaml#updateSupplierContract)*

**Data it reads**: `listSuppliers` (onLoad, List suppliers); `listSupplierContracts` (onLoad, Supplier contracts list)

**Where the user goes next**

- → `BO-078` Requisitions: *Requisitions*; carries `requisitionId`
- → `BO-007` Product Directory: *The new range becomes products in the directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The suppliers list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the suppliers untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No suppliers yet. At tenant scope offers Create supplier (`createSupplier`); at venue scope says suppliers are set up by the tenant (audit R183). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSuppliers` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PROCUREMENT_VIEW`, which `listSuppliers` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_MANAGE` for `createSupplier`, `recordQuotation`, `updateSupplier`, `createSupplierContract` and 1 more; `REPORT_VIEW_VENUE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 The contract is `terminated` or `expired`; a renewal is a new contract.; 422 `validTo` before `validFrom`, or `active` without a `documentReference`. |

#### Edge cases to draw

- **Venue user with no suppliers set up**: Says "Suppliers are set up by your head office" rather than offering to add one. *(source: R183 / screens/P08-venue-back-office.yaml#BO-083)*

#### Consistency with other screens

- Match `BO-078`: Quotations recorded here appear in the request's comparison.
- Match `BO-052`: Receipts and rejections there feed this scorecard.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- code: SUP-0042
  name: Gulf Fresh Dairy LLC
  status: Active
  currency: AED
  paymentTermsDays: 30
  leadTimeDays: 2
  otif: 91.4%
  rejection: 2.1% (Damaged, Short-dated)
- code: SUP-0057
  name: Desert Rose Merchandise FZE
  status: On hold
  statusReason: Trade licence renewal pending
  currency: AED
- code: SUP-0063
  name: Emirates Beverage Trading LLC
  contract:
    number: EBT-2026-07
    validFrom: '2026-01-01'
    validTo: '2026-12-31'
    paymentTermsDays: 45
```

#### Permissions

- `listSuppliers` → `PROCUREMENT_VIEW` (read) · staff
- `createSupplier` → `PROCUREMENT_MANAGE` (configure) · staff
- `recordQuotation` → `PROCUREMENT_MANAGE` (configure) · staff
- `updateSupplier` → `PROCUREMENT_MANAGE` (configure) · staff
- `getSupplierPerformance` → `REPORT_VIEW_VENUE` (operate) · staff
- `listSupplierContracts` → `PROCUREMENT_VIEW` (read) · staff
- `createSupplierContract` → `PROCUREMENT_MANAGE` (configure) · staff
- `updateSupplierContract` → `PROCUREMENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PROCUREMENT_VIEW`, which `listSuppliers` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_MANAGE` for `createSupplier`, `recordQuotation`, `updateSupplier`, `createSupplierContract` and 1 more; `REPORT_VIEW_VENUE` for …

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.5.9 | Manage supplier profiles, contracts and delivery information. | Bundles and Promotions | CONTRACTED | `createSupplier` |
| 4.5.29 | Manage supplier contracts and pricing. | Bundles and Promotions | CONTRACTED | `createSupplier` |
| 15.3.1 | Supplier Master - System shall support supplier management. | Inventory Management | CONTRACTED | `createSupplier` |
| 15.3.2 | Supplier Classification - System shall support supplier classification. | Inventory Management | CONTRACTED | `createSupplier` |
| 4.5.11 | Maintain supplier-specific pricing catalogs. | Bundles and Promotions | CONTRACTED | `recordQuotation` |
| 15.3.3 | Supplier Performance Tracking - System shall track supplier performance. | Inventory Management | CONTRACTED | `getSupplierPerformance` |
| 15.3.17 | Supplier Performance Reports - System shall provide supplier reports. | Inventory Management | CONTRACTED | `getSupplierPerformance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Suppliers are categorised (F&B, retail, engineering, etc.); the Supplier Master holds details, linked item categories, compliance documents and performance scorecards. Spend analysis shows category-, supplier- and contract-wise spend. *(client request · MoM 18 Aug 2026, 4.13 Supplier & Purchase Order Management · DI-347)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-083` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 2.dc.html#ret-2g`, `Inventory Board 4.dc.html#inv-4b`, `Inventory Board 4.dc.html#inv-4c`, `Inventory Board 4.dc.html#inv-4d`, `Inventory Board 7.dc.html#inv-7f`
- Flow F78 *A supplier is set up and a catalogue is priced and published*, step 1: The supplier is found or set up, and its quotation recorded. → **Suppliers are the tenant's; a venue records the quotation** (audit R183). The quoted price is what a purchase order line later prefills.
- Flow F78 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.

#### Acceptance for the design

- [ ] Every input above is drawn (36), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-083?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create supplier, Record quotation, Save supplier.
- [ ] Every transition is wired: `BO-078`, `BO-007`.
- [ ] Every gated control is gated: `PROCUREMENT_MANAGE`, `PROCUREMENT_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

### In P08 · Stock & Supply

- Decision: do NOT implement every granular warehouse status (put-away, picking, packing, dispatching, etc.); keep day-to-day workflows simple and fast for end users. This principle guides UI/UX and workflow design across inventory and warehouse operations. *(agreed · MoM 18 Aug 2026, 4.12 Simplification Principle — Guiding Decision · DI-346)*
- Decision: F&B configuration (menus, recipes, costing, inventory) is managed at outlet level, and Retail follows the same segregation. Venue-owned homogeneous outlets (e.g. popcorn/ice-cream booths) may be set up centrally once and applied across outlets, but the model stays outlet-level. *(agreed · MoM 18 Aug 2026, 4.5 Outlet-Level vs. Venue-Level Configuration — Key Discussion · DI-330)*

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acknowledgePurchaseOrder": {"method":"POST","path":"/purchase-orders/{purchaseOrderId}/acknowledge","contract":"inventory","summary":"Record the supplier acknowledgement","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PurchaseOrder"},
"approveRequisition": {"method":"POST","path":"/requisitions/{requisitionId}/approve","contract":"inventory","summary":"Approve, reject or return a requisition","permission":"APPROVAL_ACT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Requisition"},
"cancelPurchaseOrder": {"method":"POST","path":"/purchase-orders/{purchaseOrderId}/cancel","contract":"inventory","summary":"Cancel a purchase order","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PurchaseOrder"},
"cancelRequisition": {"method":"POST","path":"/requisitions/{requisitionId}/cancel","contract":"inventory","summary":"Cancel a requisition","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Requisition"},
"cancelStockCount": {"method":"POST","path":"/stock-counts/{countId}/cancel","contract":"inventory","summary":"Abandon a count","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StockCount"},
"closePurchaseOrderShort": {"method":"POST","path":"/purchase-orders/{purchaseOrderId}/close-short","contract":"inventory","summary":"Close an order accepting the balance will not arrive","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PurchaseOrder"},
"closeTransferShort": {"method":"POST","path":"/stock-transfers/{transferId}/close-short","contract":"inventory","summary":"Close a transfer accepting the balance will not arrive","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StockTransfer"},
"compareQuotations": {"method":"GET","path":"/requisitions/{requisitionId}/quotations","contract":"inventory","summary":"Compare quotations for a requisition","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"QuotationComparison"},
"createGoodsReceipt": {"method":"POST","path":"/goods-receipts","contract":"inventory","summary":"Receive goods against a purchase order","permission":"PROCUREMENT_RECEIVE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGoodsReceiptRequest","responds":"GoodsReceipt"},
"createInventoryItem": {"method":"POST","path":"/inventory-items","contract":"inventory","summary":"Create an inventory item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateInventoryItemRequest","responds":"InventoryItem"},
"createPurchaseOrder": {"method":"POST","path":"/purchase-orders","contract":"inventory","summary":"Raise a purchase order","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePurchaseOrderRequest","responds":"PurchaseOrder"},
"createRequisition": {"method":"POST","path":"/requisitions","contract":"inventory","summary":"Raise a requisition","permission":"PROCUREMENT_REQUEST","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRequisitionRequest","responds":"Requisition"},
"createStockLocation": {"method":"POST","path":"/stock-locations","contract":"inventory","summary":"Create a stock location","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StockLocation"},
"createStockMovement": {"method":"POST","path":"/stock-movements","contract":"inventory","summary":"Record an issue, return or adjustment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateStockMovementRequest","responds":"StockMovement"},
"createStockTransfer": {"method":"POST","path":"/stock-transfers","contract":"inventory","summary":"Send stock to another location","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateStockTransferRequest","responds":"StockTransfer"},
"createSupplier": {"method":"POST","path":"/suppliers","contract":"inventory","summary":"Create a supplier","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Supplier","responds":"Supplier"},
"createSupplierContract": {"method":"POST","path":"/suppliers/{supplierId}/contracts","contract":"inventory","summary":"Record a purchasing contract with a supplier","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventorySupplierContract"},
"enterCountLine": {"method":"POST","path":"/fnb-stock-counts/{countId}/lines","contract":"fnb","summary":"What was actually on the shelf","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getCountVariance": {"method":"GET","path":"/stock-counts/{countId}/variance","contract":"inventory","summary":"Variance between counted and expected","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CountVariance"},
"getInventoryItem": {"method":"GET","path":"/inventory-items/{itemId}","contract":"inventory","summary":"Read an item with stock position","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"InventoryItem"},
"getInventoryKitDefinition": {"method":"GET","path":"/inventory-items/{itemId}/kit-definition","contract":"inventory","summary":"The components a kit item is made of","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"InventoryKitDefinition"},
"getPurchaseOrder": {"method":"GET","path":"/purchase-orders/{purchaseOrderId}","contract":"inventory","summary":"Read a purchase order with receipt progress","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PurchaseOrder"},
"getStockPositions": {"method":"GET","path":"/stock","contract":"inventory","summary":"Stock on hand by item and location","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locationId","in":"query","required":null},{"name":"itemId","in":"query","required":null},{"name":"includeZero","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getStockTransfer": {"method":"GET","path":"/stock-transfers/{transferId}","contract":"inventory","summary":"One transfer, its manifest and where it is","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"StockTransfer"},
"getStockValuation": {"method":"GET","path":"/stock/valuation","contract":"inventory","summary":"Stock value by location and category","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"asAt","in":"query","required":null},{"name":"locationId","in":"query","required":null}],"requestBody":null,"responds":"StockValuation"},
"getSuggestedRequisitions": {"method":"GET","path":"/requisitions/suggested","contract":"inventory","summary":"Draft requisitions from reorder points","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locationId","in":"query","required":null}],"requestBody":null,"responds":null},
"getSupplierPerformance": {"method":"GET","path":"/suppliers/{supplierId}/performance","contract":"reporting","summary":"On-time, in-full, and what was rejected","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":null},
"listGoodsReceipts": {"method":"GET","path":"/goods-receipts","contract":"inventory","summary":"List goods receipts","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"purchaseOrderId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInventoryItems": {"method":"GET","path":"/inventory-items","contract":"inventory","summary":"List inventory items","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"belowReorderPoint","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPurchaseOrders": {"method":"GET","path":"/purchase-orders","contract":"inventory","summary":"List purchase orders","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"supplierId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRequisitions": {"method":"GET","path":"/requisitions","contract":"inventory","summary":"List requisitions","permission":"PROCUREMENT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"raisedByPrincipalId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockCounts": {"method":"GET","path":"/stock-counts","contract":"inventory","summary":"List stock counts","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockLocations": {"method":"GET","path":"/stock-locations","contract":"inventory","summary":"List stock locations","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockMovements": {"method":"GET","path":"/stock-movements","contract":"inventory","summary":"The movement ledger","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"itemId","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockTransfers": {"method":"GET","path":"/stock-transfers","contract":"inventory","summary":"List transfers","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSupplierContracts": {"method":"GET","path":"/supplier-contracts","contract":"inventory","summary":"Supplier contracts, by supplier, status or expiry","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"supplierId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringBefore","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSuppliers": {"method":"GET","path":"/suppliers","contract":"inventory","summary":"List suppliers","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupInventoryItem": {"method":"GET","path":"/inventory-items/lookup","contract":"inventory","summary":"Look up by barcode or SKU","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"barcode","in":"query","required":null},{"name":"sku","in":"query","required":null}],"requestBody":null,"responds":"InventoryItem"},
"postStockCount": {"method":"POST","path":"/stock-counts/{countId}/post","contract":"inventory","summary":"Post a count and adjust stock","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StockCount"},
"receiveStockTransfer": {"method":"POST","path":"/stock-transfers/{transferId}/receive","contract":"inventory","summary":"Receive a transfer","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StockTransfer"},
"recordQuotation": {"method":"POST","path":"/suppliers/{supplierId}/quotations","contract":"inventory","summary":"Record a supplier quotation","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateQuotationRequest","responds":"Quotation"},
"recountStockCount": {"method":"POST","path":"/stock-counts/{countId}/recount","contract":"inventory","summary":"Send a count back to be recounted","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StockCount"},
"rejectReceivedGoods": {"method":"POST","path":"/goods-receipts/{receiptId}/reject","contract":"inventory","summary":"Reject received goods","permission":"PROCUREMENT_RECEIVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GoodsReceipt"},
"requestRecount": {"method":"POST","path":"/fnb-stock-counts/{countId}/recount","contract":"fnb","summary":"Send a line back to be counted again","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecountResult"},
"sendPurchaseOrder": {"method":"POST","path":"/purchase-orders/{purchaseOrderId}/send","contract":"inventory","summary":"Issue the order to the supplier","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PurchaseOrder"},
"setInventoryKitDefinition": {"method":"PUT","path":"/inventory-items/{itemId}/kit-definition","contract":"inventory","summary":"Make an item a kit of other stocked items","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"InventoryKitDefinition","responds":"InventoryKitDefinition"},
"startStockCount": {"method":"POST","path":"/stock-counts","contract":"inventory","summary":"Start a stock count","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StartStockCountRequest","responds":"StockCount"},
"submitCountLines": {"method":"POST","path":"/stock-counts/{countId}/lines","contract":"inventory","summary":"Submit counted quantities","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateInventoryItem": {"method":"PATCH","path":"/inventory-items/{itemId}","contract":"inventory","summary":"Amend an item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryItem"},
"updateRequisitionLines": {"method":"PUT","path":"/requisitions/{requisitionId}/lines","contract":"inventory","summary":"Change what an outlet is asking for, before it is approved","permission":"PROCUREMENT_REQUEST","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Requisition"},
"updateSupplier": {"method":"PUT","path":"/suppliers/{supplierId}","contract":"inventory","summary":"Change terms, or stop buying from them","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Supplier"},
"updateSupplierContract": {"method":"PATCH","path":"/supplier-contracts/{contractId}","contract":"inventory","summary":"Extend, activate or end a supplier contract","permission":"PROCUREMENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventorySupplierContract"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CostingMethod": {"type":"string","description":"Fixed at item creation. Immutable once movements exist.","enum":["weightedAverage","fifo","standardCost","lastPurchasePrice"]},
"CountStatus": {"type":"string","enum":["open","counting","closed","variancePending","posted","cancelled"]},
"CountVariance": {"x-ticvai-persistence":"none — computed at close","type":"object","required":["countId","totalVarianceValue","lines"],"properties":{"countId":{"type":"string","format":"uuid"},"totalVarianceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exceptionCount":{"type":"integer","description":"Lines beyond `VenueSettings.inventory.countVarianceTolerancePercent` (proposed default 2 per cent, audit R094), requiring review before posting."},"lines":{"type":"array","items":{"type":"object","required":["itemId","expectedQuantity","countedQuantity","variance","isException"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"expectedQuantity":{"type":"number"},"countedQuantity":{"type":"number"},"variance":{"type":"number"},"variancePercentage":{"type":"number"},"varianceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isException":{"type":"boolean"},"recountCount":{"type":"integer","description":"A line counted several times is itself a finding."},"note":{"type":"string","nullable":true}}}}}},
"CreateGoodsReceiptRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","purchaseOrderId","locationId","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"purchaseOrderId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"deliveryNoteReference":{"type":"string","maxLength":128},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","receivedQuantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"receivedQuantity":{"type":"number","minimum":0},"unit":{"type":"string"},"batchNumber":{"type":"string","maxLength":64},"expiryDate":{"type":"string","format":"date","description":"Required for perishable items."},"note":{"type":"string","maxLength":200}}}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateInventoryItemRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["sku","name","venueId","baseUnit","costingMethod"],"properties":{"sku":{"type":"string","maxLength":64},"barcode":{"type":"string","maxLength":128},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"baseUnit":{"type":"string","description":"The unit stock is held in. Immutable once movements exist."},"purchaseUnit":{"type":"string","description":"How the supplier sells it — a case of 24 against a base unit of one."},"purchaseUnitFactor":{"type":"number","minimum":0,"default":1},"costingMethod":{"$ref":"#/components/schemas/CostingMethod"},"reorderPoint":{"type":"number","minimum":0},"reorderQuantity":{"type":"number","minimum":0},"parLevel":{"type":"number","minimum":0},"preferredSupplierId":{"type":"string","format":"uuid"},"allowNegativeStock":{"type":"boolean","default":false,"description":"True permits issue beyond on-hand. Occasionally needed at a bar mid-service; dangerous everywhere else.\n"},"isPerishable":{"type":"boolean","default":false},"shelfLifeDays":{"type":"integer","nullable":true}}},
"CreatePurchaseOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","supplierId","lines","expectedDelivery"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["standard","blanket","release","rfqAward"],"default":"standard","description":"**Which order this is** (CHG-RUL-004). `standard` needs `requisitionId` and `quotationId` (409 `requisition-required` without them); `blanket` and `rfqAward` are raised without a requisition; `release` names `blanketParentId`. Every kind goes through the PO approval matrix."},"requisitionId":{"type":"string","format":"uuid","nullable":true,"description":"Required for a `standard` order; omitted for a blanket order, an RFQ award or a release."},"supplierId":{"type":"string","format":"uuid"},"quotationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for a `standard` order and an `rfqAward` (the winning quotation)."},"rfqId":{"type":"string","format":"uuid","nullable":true,"description":"For an `rfqAward`, the quotation round it awards."},"blanketParentId":{"type":"string","format":"uuid","nullable":true,"description":"For a `release`, the open blanket order it draws against."},"contractPriceValidUntil":{"type":"string","format":"date","nullable":true,"description":"For a `blanket` order, the last day its prices hold."},"deliverToLocationId":{"type":"string","format":"uuid"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"},"unitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Omitted, the selected quotation line's price. **Editable with a reason** (decided 28 September, audit R171).\n"},"priceOverrideReason":{"type":"string","maxLength":500,"nullable":true,"description":"Required when `unitPrice` differs from the quotation line (audit R171)."}}}},"expectedDelivery":{"type":"string","format":"date"},"note":{"type":"string","maxLength":1000}}},
"CreateQuotationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["requisitionId","lines","validUntil"],"properties":{"requisitionId":{"type":"string","format":"uuid"},"reference":{"type":"string","maxLength":128},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","unitPrice","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"unit":{"type":"string"}}}},"leadTimeDays":{"type":"integer"},"validUntil":{"type":"string","format":"date"},"note":{"type":"string","maxLength":1000}}},
"CreateRequisitionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","venueId","lines","requiredBy"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid"},"costCenterId":{"type":"string","format":"uuid"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"},"note":{"type":"string","maxLength":200}}}},"requiredBy":{"type":"string","format":"date"},"justification":{"type":"string","maxLength":1000}}},
"CreateStockMovementRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","itemId","locationId","kind","quantity","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MovementKind"},"quantity":{"type":"number","exclusiveMinimum":0,"description":"Always positive. **The `kind` decides whether it adds or removes stock**, not the sign (decided 28 September, audit R171).\n"},"unit":{"type":"string"},"reason":{"type":"string","maxLength":500,"description":"**Required for `adjustmentIn`, `adjustmentOut` and `waste`** (decided 28 September, audit R171); adjustments are reported separately.\n"},"costCenterId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateStockTransferRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","fromLocationId","toLocationId","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"fromLocationId":{"type":"string","format":"uuid"},"toLocationId":{"type":"string","format":"uuid"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"}}}},"note":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"GoodsReceipt": {"x-ticvai-persistence":"inventory.goods_receipt + inventory.goods_receipt_line","type":"object","required":["id","receiptNumber","purchaseOrderId","locationId","lines","receivedByPrincipalId","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"receiptNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152), e.g. `MAR-GR-000431`. Not gapless; only tax invoices are gapless, per legal entity. A receipt recorded offline takes the next number from the range its device holds in reserve.\n"},"purchaseOrderId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"deliveryNoteReference":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string","format":"uuid","readOnly":true,"description":"One batch or expiry line of the receipt. What `rejectReceivedGoods` addresses (decided 28 September, audit R171).\n"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"orderedQuantity":{"type":"number"},"receivedQuantity":{"type":"number"},"rejectedQuantity":{"type":"number"},"batchNumber":{"type":"string","nullable":true},"expiryDate":{"type":"string","format":"date","nullable":true},"unitCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"totalValue":{"x-ticvai-column":"net_value_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"receivedByPrincipalId":{"type":"string","format":"uuid"},"journalEntryId":{"type":"string","nullable":true,"description":"The accrual the supplier invoice will later match against."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"InventoryItem": {"x-ticvai-persistence":"inventory.item","allOf":[{"$ref":"#/components/schemas/CreateInventoryItemRequest"},{"type":"object","required":["id","onHand","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"onHand":{"type":"number","description":"Derived from movements. Not directly editable."},"onOrder":{"type":"number"},"inTransit":{"type":"number"},"available":{"type":"number","description":"On-hand minus allocated, where allocated is stock reserved for orders (decided 28 September, audit R171)."},"averageCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lastPurchasePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isBelowReorderPoint":{"type":"boolean"},"hasMovements":{"type":"boolean","description":"True locks costing method and base unit."},"isActive":{"type":"boolean"}}}]},
"InventoryKitComponent": {"x-ticvai-persistence":"inventory.kit_component","type":"object","description":"4.4.20. One component of a kit and the quantity one kit consumes.","required":["componentItemId","quantity"],"properties":{"kitItemId":{"type":"string","format":"uuid","readOnly":true},"componentItemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","exclusiveMinimum":0},"unit":{"type":"string","nullable":true,"description":"The component's base unit where omitted."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the kit item's venue scope."}}},
"InventoryKitDefinition": {"x-ticvai-persistence":"none — composed of the item's inventory.kit_component rows","type":"object","description":"4.4.20. Also the `setInventoryKitDefinition` body.","required":["components"],"properties":{"kitItemId":{"type":"string","format":"uuid","readOnly":true},"components":{"type":"array","items":{"$ref":"#/components/schemas/InventoryKitComponent"}}}},
"InventorySupplierContract": {"type":"object","x-ticvai-persistence":"inventory.supplier_contract","description":"**Taken from the backend workbook, 20 September.** Stores purchasing agreements, validity dates, and commercial terms agreed with a supplier.","required":["supplierId","number","name","validFrom","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"supplierId":{"type":"string","format":"uuid"},"number":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date","nullable":true},"currencyCode":{"type":"string","maxLength":10,"nullable":true},"paymentTermsDays":{"type":"integer","nullable":true},"documentReference":{"type":"string","maxLength":500,"nullable":true},"status":{"type":"string","maxLength":30,"enum":["draft","active","expired","terminated"],"description":"Written by `createSupplierContract` and `updateSupplierContract`; `expired` is set by the server once `validTo` has passed (29 September, writers pass)."},"statusReason":{"type":"string","maxLength":500,"nullable":true},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"}}},
"LocationKind": {"type":"string","enum":["mainStore","subStore","kitchen","bar","retailFloor","cellar","transit"]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"MovementKind": {"type":"string","description":"**The kind decides the direction** (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` (the finished item entering stock; the ingredients leave as `issue`). Out: `issue`, `saleDepletion`, `waste`, `adjustmentOut`, `transferOut`, `countLoss`, `supplierReturn`. `adjustment` and `countAdjustment` were split into an in and an out kind so that no kind has two directions.\n","enum":["receipt","issue","saleDepletion","waste","adjustmentIn","adjustmentOut","transferOut","transferIn","countGain","countLoss","supplierReturn","production"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PurchaseOrder": {"x-ticvai-persistence":"inventory.purchase_order + inventory.purchase_order_line","type":"object","required":["id","purchaseOrderNumber","supplierId","status","lines","total","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"purchaseOrderNumber":{"type":"string","readOnly":true,"description":"**Per venue, in sequence** (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for an order with no venue. Proposed format `PO-<venue code>-<sequence, six digits>`, client to correct.\n"},"requisitionId":{"type":"string","format":"uuid","nullable":true,"description":"Null on a blanket order or an RFQ award, which are raised without one."},"quotationId":{"type":"string","format":"uuid","nullable":true,"description":"The quotation selected when the order was raised (`createPurchaseOrder` requires it). **The link that shows the comparison was made**, which `rfqId` alone does not."},"supplierId":{"type":"string","format":"uuid"},"supplierName":{"type":"string"},"kind":{"type":"string","enum":["standard","blanket","release","rfqAward"],"default":"standard","description":"BL-159. **A blanket order is a price and a commitment, not a delivery.** Releases draw against it, and modelling each release as its own purchase order loses the contract that makes the price valid.\n"},"blanketParentId":{"type":"string","format":"uuid","nullable":true,"description":"The blanket order this release draws against — another purchase order, so the same id type."},"contractPriceValidUntil":{"type":"string","format":"date","nullable":true},"rfqId":{"type":"string","format":"uuid","nullable":true,"description":"Where this order came from a quotation round. **Keeping the link is what lets a venue show it took the best of three**, which is usually the procurement rule rather than a preference.\n"},"supplierInvoiceRef":{"type":"string","nullable":true,"description":"BL-123. **Purchase orders and goods receipts both existed — the third leg did not.** A three-way match with two legs is a two-way match, and it is the supplier invoice that carries the price nobody has checked yet.\n"},"matchStatus":{"type":"string","nullable":true,"enum":["unmatched","matched","priceVariance","quantityVariance","bothVariance"],"description":"**The variance kinds are separated because they have different owners** — a price variance is a buyer's problem and a quantity variance is a receiving one.\n"},"status":{"$ref":"#/components/schemas/PurchaseOrderStatus"},"deliverToLocationId":{"type":"string","format":"uuid","nullable":true,"description":"**Scoped 31 August.** A purchase order is raised by somebody, for somewhere, and carried neither. `requisitionId` reaches a venue through a join, but **a purchase order raised without a requisition — a blanket order, an RFQ award — had no scope at all**, so nothing could answer *whose budget is this* without guessing.\n\n**`deliverToLocationId` is separate from `venueId` on purpose.** A tenant buying centrally and delivering to three venues is one order and three destinations; collapsing them would force one order per venue and lose the volume the tenant negotiated for."},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"orderedQuantity":{"type":"number"},"receivedQuantity":{"type":"number"},"outstandingQuantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"The selected quotation line's price, kept beside `unitPrice` (audit R171)."},"priceOverrideReason":{"type":"string","nullable":true,"description":"Why `unitPrice` differs from `quotedUnitPrice` (audit R171)."},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expectedDelivery":{"type":"string","format":"date"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"supplierReference":{"type":"string","nullable":true,"description":"The supplier's own order reference, from `acknowledgePurchaseOrder`."},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Null is the supplier performance figure** — goods arriving against an order never acknowledged."},"closeShortReason":{"type":"string","nullable":true,"description":"Why the balance was written off, from `closePurchaseOrderShort`."},"cancelReason":{"type":"string","nullable":true,"description":"From `cancelPurchaseOrder`."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The pending approval request raised by `cancelPurchaseOrder` or `closePurchaseOrderShort` (kinds `purchaseOrderCancel`, `purchaseOrderShortClose`; audit R144). Null when none is open."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Which venue is buying. **Null on a tenant-level order** — see `deliverToLocationId`."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Present on every order regardless of whether a venue is named, because a tenant-level order still belongs to a tenant."}}},
"PurchaseOrderStatus": {"type":"string","enum":["raised","sent","acknowledged","partiallyReceived","received","closedShort","cancelled"]},
"Quotation": {"x-ticvai-persistence":"inventory.quotation + inventory.quotation_line","allOf":[{"$ref":"#/components/schemas/CreateQuotationRequest"},{"type":"object","required":["id","supplierId","total","receivedAt"],"properties":{"id":{"type":"string","format":"uuid"},"supplierId":{"type":"string","format":"uuid"},"supplierName":{"type":"string"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"isSelected":{"type":"boolean"},"receivedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","description":"The partition key. A quotation is sought by somebody and the scope says who, the venue that recorded it, against a tenant supplier (audit R183)."}}}]},
"QuotationComparison": {"x-ticvai-persistence":"none — computed","type":"object","required":["requisitionId","quotations","lowestTotalSupplierId"],"properties":{"requisitionId":{"type":"string","format":"uuid"},"quotations":{"type":"array","items":{"$ref":"#/components/schemas/Quotation"}},"lowestTotalSupplierId":{"type":"string","format":"uuid","nullable":true},"shortestLeadTimeSupplierId":{"type":"string","format":"uuid","nullable":true},"byLine":{"type":"array","description":"Per-line comparison. The cheapest total is not always the cheapest line.","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"prices":{"type":"array","items":{"type":"object","properties":{"supplierId":{"type":"string","format":"uuid"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isLowest":{"type":"boolean"}}}}}}}}},
"RecountResult": {"type":"object","x-ticvai-persistence":"none — response shape","description":"The lines `requestRecount` reopened.","required":["countId","reopenedLineIds"],"properties":{"countId":{"type":"string","format":"uuid"},"reopenedLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","nullable":true}}},
"Requisition": {"x-ticvai-persistence":"inventory.requisition + inventory.requisition_line","type":"object","required":["id","requisitionNumber","venueId","status","lines","raisedByPrincipalId","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"requisitionNumber":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"costCenterId":{"type":"string","format":"uuid","nullable":true},"justification":{"type":"string","nullable":true},"status":{"$ref":"#/components/schemas/RequisitionStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"requestedQuantity":{"type":"number"},"suggestedQuantity":{"type":"number","nullable":true,"description":"**Kept, never overwritten** (`updateRequisitionLines`). Null on a line nobody suggested.\n"},"approvedQuantity":{"type":"number","nullable":true},"orderedQuantity":{"type":"number","nullable":true},"unit":{"type":"string"},"reason":{"type":"string","nullable":true,"description":"Why the requested quantity differs from the suggestion."},"note":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"estimatedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvalNote":{"type":"string","nullable":true},"requiredBy":{"type":"string","format":"date"},"createdAt":{"type":"string","format":"date-time"},"approvedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true,"description":"From `rejectRequisition`. What the requester reads before copying it into a new draft."},"rejectedAt":{"type":"string","format":"date-time","nullable":true},"returnQuestion":{"type":"string","nullable":true,"description":"From `returnRequisition`. What the requester must answer before resubmitting."},"returnedAt":{"type":"string","format":"date-time","nullable":true},"cancelReason":{"type":"string","nullable":true,"description":"From `cancelRequisition`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true}}},
"RequisitionStatus": {"type":"string","enum":["draft","pendingApproval","approved","rejected","returnedForInfo","ordered","closed","cancelled"]},
"RequisitionSuggestion": {"x-ticvai-persistence":"none — computed","type":"object","required":["itemId","onHand","reorderPoint","suggestedQuantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"onHand":{"type":"number"},"reorderPoint":{"type":"number"},"parLevel":{"type":"number"},"suggestedQuantity":{"type":"number"},"averageDailyConsumption":{"type":"number"},"daysOfCoverRemaining":{"type":"number"},"preferredSupplierId":{"type":"string","format":"uuid","nullable":true},"leadTimeDays":{"type":"integer","nullable":true}}},
"StartStockCountRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","locationId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["full","cycle","spot"]},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"For cycle counts — restrict to these categories."},"isBlind":{"type":"boolean","default":true,"description":"Expected quantities withheld from the counting device. Defaults true because a counter who can see the figure reconciles to it rather than to the shelf. **The expected quantity and the variance stay hidden until the count is submitted** (decided 28 September, audit R110).\n"}}},
"StockCount": {"x-ticvai-persistence":"inventory.count + inventory.count_line","type":"object","required":["id","locationId","kind","status","isBlind","lineCount","countedCount","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"locationName":{"type":"string"},"kind":{"type":"string"},"status":{"$ref":"#/components/schemas/CountStatus"},"isBlind":{"type":"boolean"},"lineCount":{"type":"integer"},"countedCount":{"type":"integer"},"varianceLineCount":{"type":"integer"},"varianceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"startedByPrincipalId":{"type":"string","format":"uuid"},"postedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"journalEntryId":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"postedAt":{"type":"string","format":"date-time","nullable":true},"recountReason":{"type":"string","nullable":true,"description":"Why the count was last sent back by `recountStockCount`."},"recountSignedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor whose step-up sent the count back last (audit R144)."},"cancelReason":{"type":"string","nullable":true,"description":"Why it was abandoned, from `cancelStockCount`."}}},
"StockLocation": {"x-ticvai-persistence":"inventory.location","type":"object","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/LocationKind"},"parentLocationId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"}}},
"StockMovement": {"x-ticvai-persistence":"inventory.movement","allOf":[{"$ref":"#/components/schemas/CreateStockMovementRequest"},{"type":"object","required":["balanceAfter","principalId","createdAt"],"properties":{"balanceAfter":{"type":"number"},"unitCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"x-ticvai-column":"net_cost_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"principalId":{"type":"string","format":"uuid"},"sourceType":{"type":"string","nullable":true,"description":"What generated it — an order, a count, a transfer."},"sourceId":{"type":"string","nullable":true},"journalEntryId":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]},
"StockPosition": {"x-ticvai-persistence":"none — derived from movements","type":"object","required":["itemId","locationId","onHand","unit"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"locationId":{"type":"string","format":"uuid"},"locationName":{"type":"string"},"onHand":{"type":"number"},"allocated":{"type":"number","description":"**Reserved for orders**: the quantity under an active stock reservation for an order (decided 28 September, audit R171). A transfer is not allocation: dispatched stock has already left on-hand and sits in transit.\n"},"available":{"type":"number","description":"**On-hand minus allocated** (decided 28 September, audit R171). What can still be sold or issued.\n"},"unit":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lastCountedAt":{"type":"string","format":"date-time","nullable":true},"lastMovementAt":{"type":"string","format":"date-time","nullable":true}}},
"StockTransfer": {"x-ticvai-persistence":"inventory.transfer + inventory.transfer_line","type":"object","required":["id","fromLocationId","toLocationId","status","lines","dispatchedAt"],"properties":{"id":{"type":"string","format":"uuid"},"transferNumber":{"type":"string"},"fromLocationId":{"type":"string","format":"uuid"},"toLocationId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/TransferStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"dispatchedQuantity":{"type":"number"},"receivedQuantity":{"type":"number","nullable":true},"discrepancy":{"type":"number","nullable":true},"discrepancyReason":{"type":"string","nullable":true}}}},"dispatchedByPrincipalId":{"type":"string","format":"uuid"},"receivedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"dispatchedAt":{"type":"string","format":"date-time"},"receivedAt":{"type":"string","format":"date-time","nullable":true},"closeShortReason":{"type":"string","nullable":true,"description":"Why the balance was written off, from `closeTransferShort`."},"closeShortSignedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor whose step-up closed the transfer short (audit R144)."},"fromVenueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue of `fromLocationId`. Set by the server (audit R183)."},"toVenueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue of `toLocationId`. Set by the server (audit R183)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). `fromLocationId` and `toLocationId` give the endpoints; **this gives the owner**, the source venue's scope.\n\n**Both venues see a transfer between them** (decided 28 September, audit R183). It used to sit at the tenant above both, where neither venue could see it. The row is owned at the source venue and `toScopePath` admits the destination venue too."},"toScopePath":{"type":"string","readOnly":true,"description":"The destination venue's scope. Row-level security admits a caller whose scope matches `scopePath` or `toScopePath`, so both venues read the transfer (decided 28 September, audit R183).\n"}}},
"StockValuation": {"x-ticvai-persistence":"none — computed","type":"object","required":["asAt","total","byLocation"],"properties":{"asAt":{"type":"string","format":"date"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"byLocation":{"type":"array","items":{"type":"object","properties":{"locationId":{"type":"string","format":"uuid"},"locationName":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"itemCount":{"type":"integer"}}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"categoryName":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"Supplier": {"x-ticvai-persistence":"inventory.supplier","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64,"x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108).\n"},"name":{"type":"string","maxLength":200},"contactName":{"type":"string","nullable":true},"contactEmail":{"type":"string","nullable":true},"contactPhone":{"type":"string","nullable":true},"taxRegistrationNumber":{"type":"string","nullable":true},"paymentTermsDays":{"type":"integer","nullable":true},"leadTimeDays":{"type":"integer","nullable":true},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"accountId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"},"status":{"type":"string","enum":["active","onHold","suspended","terminated"],"description":"Set by `updateSupplier`. **A supplier on hold stops appearing in requisitions and purchase orders while its history stays intact.**"},"statusReason":{"type":"string","nullable":true},"minimumOrderValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.** Suppliers are owned at tenant and venues quote against them (decided 28 September, audit R183)."}}},
"TransferStatus": {"type":"string","enum":["dispatched","inTransit","received","partiallyReceived","cancelled"]}
}
```
