# P06-stock-on-the-floor-01 — P06 · Stock on the Floor

**10 screens · 34 operations · 38 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, ORDER_CREATE, ORDER_MODIFY, PROCUREMENT_RECEIVE, PROCUREMENT_REQUEST, PROCUREMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **14 of these operations work offline**: createGoodsReceipt, createRequisition, enterCountLine, getHaccpStatus, getStockPositions, getStockTransfer, listRequisitions, listSerialisedItems
  — and the rest do not. A surface that looks the same online and off is lying.
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

### Finance, Ledger & Tax · Reporting & Analytics

Finance and insights run underneath every sale. A sale at a till (P04), kiosk, web storefront (P01) or guest app (P02) is priced and taxed per line at the moment of sale, recorded in the venue's base currency (AED in the UAE; 2 decimals, or 3 for BHD, KWD and OMR, never rounded away), and posted to an append-only dual ledger through account mappings per money event; anything unmapped lands in suspense. Tax follows the jurisdiction's tax profile: inclusive or exclusive, compound where a tax applies on another, zero-rated or exempt with verified evidence, and computed on the discounted price by default or on the price before discount where the region requires it (Egypt). A guest may select a currency the venue charges and pay in it: the rate is locked on the order, the payment partner is asked in that currency, the ledger keeps the base amount with the rate, and a refund goes back in the currency paid (decided 2 October 2026, Chinmay); a currency shown but not charged is an approximate price. Foreign cash at a till is recorded at its base equivalent and change is given in base currency. A paid order can carry a VAT receipt (simplified tax invoice), a full tax invoice with the buyer's TRN, or a consolidated invoice for a company, each numbered without gaps and never edited; corrections are credit memos. Revenue is recognised by rule: POS-style immediate, tickets on the visit, gift cards and wallet on use, annual passes straight-line or per visit, breakage on expiry; deferred revenue is a balance that ages. Each venue's day is reconciled (POS cash, gateways, bank, wallet against the ledger, provider files matched automatically, only genuine mismatches to a person); chargebacks are defended against the bank's deadline; month end runs seven close checks and goes to a finance approver. Nothing posted is deleted: a correction is a reversal, an approver is never the preparer, and ledger approval needs a second factor. Back-office finance lives in Venue Management (P08: chart of accounts, mapping, FX, journals, recognition, reconciliation, period close, chargebacks); tax profiles, calculation validation and platform reconciliation in the TICVAI Console (P09); partner settlement in P10. Reporting is one consolidated, permission-based area (Analytics, P16): seeded standard dashboards and reports plus no-code builders over a governed business catalogue; the P08 report screens, the POS terminal day view and the kitchen performance view are scoped windows onto the same definitions and must show the same numbers. Every figure is read from a lag-tolerant reporting copy and shows its "as of" time; scope comes from the person's rights, never from a filter; AI explains and recommends but never acts, answers only within the person's role, labels forecasts, and is phase two for finance ledgers.

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Base currency | The venue's region currency; the currency every record and ledger posting is in. A guest may pay in a currency they select (where the venue charges it); the books still hold the base amount and the rate. | Home currency, Local price, Default currency | DI-211 / DI-282 / contracts/spine/orders.yaml#/components/schemas/Order |
| Pay in USD (a currency the venue charges) | The guest's selected payment currency; the card is charged in it at the rate locked on the order, and refunds go back in it. | Converted price, Approx. (for a charged currency) | contracts/spine/orders.yaml#checkoutCart / … |
| ≈ (approx.) price in USD / SAR / … | A conversion of a base-currency price for a currency the venue shows but does not charge, always next to the base price. | Converted price, USD price | DI-211 / screens/P02-guest-mobile-app.yaml#GST-044 |
| Takings | Money received in the period less refunds (cash-basis); the seeded KPI on hubs. | Revenue, Sales, Income | contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / R283 |
| Gross sales | Issued sales before discounts and refunds; whether tax is included must be stated on the tile. | Revenue, Turnover | MATRIX 6.1.78 |
| Net revenue | Gross sales less discounts less refunds, adjusted per finance policy. | Net sales, Revenue, Income | MATRIX 6.1.78 |
| Recognised revenue / Deferred revenue | Earned under the recognition rules / paid for but not yet earned. Kept distinct from sales. | Realised revenue, Unearned income, Wallet revenue | MATRIX 5.12.6 / DI-260 / contracts/spine/finance.yaml#getDeferredRevenue |
| VAT receipt | The simplified tax invoice issued on a paid order. | Receipt (when it is a tax document), Bill | contracts/spine/finance.yaml#issueTaxInvoice |
| Tax invoice / Combined tax invoice | A full invoice with the buyer's details / one invoice for several paid orders of one buyer. | Bill, Statement | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoiceType |
| Credit memo | The document that corrects an issued invoice after a refund; the invoice itself is never edited. | Credit note (until the client's tax adviser chooses "Tax credit note"), Edit invoice | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoice |
| VAT (or the jurisdiction's tax name) | Use the tax profile's own name on every surface; "Tax" only where several kinds are summed. | GST in UAE, Service charge for a tax | contracts/spine/catalogue.yaml#setTaxProfileJurisdiction |
| Price before discount | The taxable base where the jurisdiction taxes the undiscounted price. | Gross price, List tax | DI-598 |
| Post / Reverse | A journal reaches the ledger when approved and posted; a correction is a reversal, never an edit or delete. | Edit entry, Delete entry, Undo | contracts/spine/finance.yaml#reverseJournalEntry |
| Period (Open / Closing / Closed) | A fiscal period's state; closing stops postings, closed locks them. | Month locked, Frozen | contracts/spine/finance.yaml#/components/schemas/PeriodStatus |
| Variance (Over / Short) | The difference between expected and counted or recorded, always saying between which two figures. | Discrepancy, Error, Loss | DI-275 / contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation |
| Settlement / Exception / Resolve | A provider's file for a day / a line that did not match / the recorded explanation. | Payout file, Error, Close | contracts/spine/finance.yaml#/components/schemas/SettlementException |
| Chargeback | A bank-initiated reversal with an evidence deadline; not a refund. | Dispute refund, Reversal | contracts/spine/orders.yaml#/components/schemas/Chargeback |
| Report / Dashboard / Tile / KPI | A runnable, exportable, schedulable definition / a page of tiles / one visual bound to a report / a company-wide measure defined once. | Widget (outside the builder's library), Board (for a user-facing dashboard) | contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / … |
| Warning / Critical | KPI status bands set by a target's amber and red thresholds; always words plus colour. | Amber, Red (alone), Bad | contracts/satellite/reporting.yaml#/components/schemas/KpiTarget |
| As of HH:MM / Updated N sec ago | The freshness of every figure read from the reporting copy; stale shows a warning. | Live (unless refreshed), Real-time | MATRIX 8.7.22 |
| Forecast | Any projected figure, with its range; never shown as a fact. | Expected, Will be | DI-973 |
| Outlet / Workstation (till) | A sales point / the device; staff copy may say "till" for the workstation. | Store, POS (in copy), Drawer (for the device) | R156 |
| Channel | POS, Web, App, Kiosk, B2B, OTA, from one closed list. | Source, Platform | MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7 |

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
| `EMP-061` | Retail Inventory Command Center | D | 6 | 14 | 6 | 12 | 0 | 4 | — | notStarted (generated) |
| `EMP-062` | Store Stock & SKU Availability | C | 1 | 30 | 5 | 12 | 2 | 4 | — | notStarted (generated) |
| `EMP-063` | Requisition & Smart Store Replenishment | D | 18 | 21 | 6 | 9 | 2 | 0 | — | notStarted (generated) |
| `EMP-064` | Store-to-Store & Warehouse Transfers | D | 14 | 48 | 6 | 11 | 1 | 0 | — | notStarted (generated) |
| `EMP-065` | Receiving | A | 31 | 25 | 5 | 7 | 2 | 0 | — | notStarted (generated) |
| `EMP-066` | Stock Count & Cycle Count Management | D | 17 | 20 | 5 | 1 | 3 | 4 | — | notStarted (generated) |
| `EMP-067` | Damage, Loss, Shrinkage & Stock Adjustment | A | 37 | 6 | 5 | 16 | 1 | 4 | — | notStarted (generated) |
| `EMP-068` | Reservation, Allocation & Omnichannel Inventory | C | 8 | 5 | 5 | 14 | 1 | 4 | — | notStarted (generated) |
| `EMP-069` | Barcode, RFID, Serialized Stock & Traceability | D | 3 | 8 | 6 | 0 | 2 | 4 | — | notStarted (generated) |
| `EMP-070` | Inventory Exceptions, AI Replenishment & Action Center | D | 18 | 9 | 6 | 6 | 0 | 4 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-061` Retail Inventory Command Center

**Retail Inventory Command Center — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 2 · needs the `inventory` module |
| Block | Block D · task APP-STAFF-EMP-061 |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `REPORT_VIEW_VENUE` (1 read, 1 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listStockMovements` reads the population and `getStockPositions` reads one of them — list, select, act |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `alertId` (navigation), `dashboardId` (navigation) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/retail-inventory-command-center` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.**

**From the Finance, Ledger & Tax · Reporting & Analytics process.** On a handheld, a retail lead checks stock on hand, allocated and available by item and location and the latest movements, one thumb, walking. Today's takings and alerts are secondary.

**Known correction pending (do not draw the wrong version)**

- **Filters are free-text "Item id" and "Location id" fields, and a "Confirm" button has no operation.** Why: Spec leak and a dead control; an item search and a location picker are needed. *(source: screens/P06-staff-app.yaml#EMP-061; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do takings and a store manager's mobile dashboard belong on a stock screen, or in the reporting area on mobile?** → Drawn default accepted: Keep a single takings figure at the top; the dashboard lives in the reporting area. *(decided by Chinmay, 2026-10-02; DEC-361 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Item id | picker: choose an item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?itemId=` to `listStockMovements`. | `listStockMovements` ?itemId |
| Location id | picker: choose a location (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?locationId=` to `listStockMovements`. | `listStockMovements` ?locationId |
| Kind | select | optional | — | Receipt · Issue · Sale depletion · Waste · Adjustment in · Adjustment out · Transfer out · Transfer in · Count gain · Count loss · Supplier return · Production | — | Sends `?kind=` to `listStockMovements`. | `listStockMovements` ?kind |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listStockMovements`. | `listStockMovements` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listStockMovements`. | `listStockMovements` ?recordedTo |
| Search retail inventory command center | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |
| Refresh | toggle | off | — | `getDashboard` ?refresh |
| Status | radio group | — | Raised · Acknowledged · Resolved · Expired | `listAlerts` ?status |
| Severity | segmented control | — | Info · Warning · Critical | `listAlerts` ?severity |
| Workstation | picker: choose a workstation | — | — | `listAlerts` ?workstationId |
| Shift | picker: choose a shift | — | — | `listAlerts` ?shiftId |
| … 1 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Shown**

**Every stock movement** (data table, from `listStockMovements`)

| Shows | Format | Notes |
|---|---|---|
| Quantity | 1,234.5 | Always positive. The `kind` decides whether it adds or removes stock, not the sign (decided 28 September, audit R171). |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Balance after | 1,234.5 | — |
| Unit cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The selected stock movement** (detail panel, from `listStockMovements`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Receipt, Issue, Sale depletion, Waste, Adjustment in, Adjustment out… | The kind decides the direction (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` … |
| Quantity | 1,234.5 | Always positive. The `kind` decides whether it adds or removes stock, not the sign (decided 28 September, audit R171). |
| Balance after | 1,234.5 | — |
| Unit cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The stock position** (detail panel, from `getStockPositions`)

| Shows | Format | Notes |
|---|---|---|
| Item name | text | — |
| Location name | text | — |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Last counted at | 1 Oct 2026, 14:30 | — |
| Last movement at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **stock card**: Item, location, on hand, allocated, available (bold), value in base currency, last counted, last movement. *(source: MATRIX 15.1.9)*

**Data it reads**: `getStockPositions` (onLoad, Stock on hand by item and location); `listStockMovements` (onLoad, The movement ledger); `getKpiValues` (onLoad, Today's takings and revenue KPIs on the phone); `getDashboard` (onLoad, Store manager's mobile dashboard); `listAlerts` (onLoad, Daily revenue alerts (also pushed, deliverTo push))

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retail inventory list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retail inventory untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retail inventory yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on itemId, locationId, kind, recordedFrom, recordedTo and the retail inventory are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **out of coverage**: Stock from cache with "As of 10:12"; takings and alerts say "Needs connection". *(source: screens/P06-staff-app.yaml#EMP-061 / contracts/satellite/reporting.yaml#getKpiValues)*

#### Consistency with other screens

- Match `P16 ANL-006 Inventory & Waste, ANL-012 Live Operations`: Same stock and takings figures.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Shrek plush 30 cm · Motiongate Main Street Store · on hand 46 · allocated 6 · available 40 · AED 1,840.00 · counted
  28 Sep
```

#### Permissions

- `getStockPositions` → `PRODUCT_VIEW` (read) · staff
- `listStockMovements` → `PRODUCT_VIEW` (read) · staff
- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `acknowledgeAlert` → `REPORT_VIEW_VENUE` (operate) · staff

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

None names this screen.

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-061` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4d`, `FnB Board 4.dc.html#fnb-4e`
- Flow F80 *A table is configured, reserved, seated and billed*, step 4: Retail Inventory Command Center. → **Drawn by the client as FNB-4D.** 1 operations on this step.
- Flow F94 *A restaurant floor is set up before service*, step 3: Retail Inventory Command Center. → **Drawn by the client as FNB-4C.**

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-061?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-062` Store Stock & SKU Availability

**Store Stock & SKU Availability — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 2 · needs the `retail` module |
| Block | Block C · task APP-SETUP-EMP-062 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getStockPositions` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (session) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/store-stock-sku-availability` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.** **Links to EMP-067 for the reading itself** — F28 step 1 to step 2, and a due-checks list that cannot reach the recording screen is a list nobody acts on.

**Known gaps.** **`getHaccpStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. Removed 2 October 2026 (CHG-WIR-008): The client defined this screen as retail store stock and availability; the HACCP status, Log temperature and the F&B 86 toggle are other processes attached … Removed 2 October 2026 (CHG-WIR-008): The client defined this screen as retail store stock and availability; the HACCP status, Log temperature and the F&B 86 toggle are other processes attached …

**From the Food, Beverage & Retail process.** Store Stock & Availability is the shop-floor handheld lookup. A staff member scans or searches a product and sees on hand against available here (net of what is held for online orders and collections), plus stock at sibling stores, so a colleague can be sent to fetch a size rather than losing the sale. The one thing to get right is speed with one thumb: scan, see, act.

**Fixed on main** (the package already carries these; draw what it says): The screen carries the HACCP status and "Log temperature" (food safety) and the F&B 86 toggle. It requires the F&B module. (CHG-WIR-008); It reads stock positions (one record, status tracker) but not the shop-floor reads that exist for exactly this: getOutletStock ("shaped for … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do pending online purchases awaiting pickup or shipment count in Allocated?** → Drawn default stands (answer: "Default / recommended accepted"): Yes. Allocated covers everything held for an order or a collection. *(decided by Chinmay, 2026-10-02; DEC-051 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search store stock | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |
| Category | picker: choose a category | — | — | `getOutletStock` ?categoryId |
| Low stock first | toggle | on | — | `getOutletStock` ?lowStockFirst |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Scan or search**: Camera or scanner barcode first, with name search as fallback. A barcode that matches an inactive item says "Not found", the same as an unknown barcode. *(source: DI-233 / DI-361 / R215 / contracts/satellite/retail.yaml#lookupMerchandise)*

#### Outputs: what the screen shows and produces

**Shown**

**The stock position** (detail panel, from `getStockPositions`)

| Shows | Format | Notes |
|---|---|---|
| Item name | text | — |
| Location name | text | — |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Last counted at | 1 Oct 2026, 14:30 | — |
| Last movement at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Outlet stock** (data table, from `getOutletStock`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Merchandise | the name it points at, never the id | — |
| SKU | text | — |
| Name | text | — |
| Category name | text | — |
| On hand | 1,234.5 | — |
| Allocated | 1,234.5 | Held by an unexpired collection reservation. |
| Available | 1,234.5 | — |
| Is below reorder point | yes / no (icon or chip) | — |
| Last sold at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Scan an item** (detail panel, from `lookupMerchandise`)

| Shows | Format | Notes |
|---|---|---|
| Merchandise | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | The outlet whose price and stock this is: the asking workstation's outlet, or `outletId` for a caller with none (decided 28 September … |
| SKU | text | — |
| Name | text | — |
| List price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Effective price | AED 1,234.50 | After any live promotion. |
| Applied promotion code | text | — |
| On hand | 1,234.5 | — |
| Is available | yes / no (icon or chip) | — |
| Sibling outlets | list or chips (count when long) | Stock elsewhere in the venue, so a colleague can be sent. |
| Outlet | the name it points at, never the id | — |
| Outlet name | text | — |
| On hand | 1,234.5 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Result card**: Product name and variant (size/colour), price after promotion (AED), then three big numbers: On hand · Allocated · Available at this store. Below them: "Other stores", the sibling outlets with available stock, nearest first. *(source: DI-361 / R171 / contracts/satellite/retail.yaml#lookupMerchandise)*
- **Store list view**: Without a search, the store's stock with low stock first (below reorder point), filterable by category. Cards, not a table. *(source: contracts/satellite/retail.yaml#getOutletStock)*

**Data it reads**: `getStockPositions` (onLoad, Stock on hand by item and location); `getOutletStock` (onLoad, This outlet's stock, low stock first, with sibling outlets)

**Where the user goes next**

- → `EMP-067` Damage, Loss, Shrinkage & Stock Adjustment: *They read the unit and record the temperature*; carries `outletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The store stock sku, read by `getStockPositions`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the store stock sku untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No store stock sku yet. Offers no create action — this screen declares no operation that makes one. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither barcode nor SKU supplied, or a caller with no workstation sent no `outletId` (audit R215) |

#### Edge cases to draw

- **Offline**: Stock reads from cache with "Last updated hh:mm". The sibling-store check needs a connection; say so in place. *(source: contracts/satellite/inventory.yaml#getStockPositions / contracts/satellite/retail.yaml#lookupMerchandise)*
- **Available is zero or negative while items are on the shelf**: Say "All on hand is held for orders". The item cannot be sold at the till, because the sale is gated on system stock. *(source: DI-294 / DI-361)*

#### Consistency with other screens

- Match `BO-049`: Same three numbers and labels.
- Match `POS-023`: The till's price check returns the same price and sibling stock.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scan: '6291100456781'
result:
  product: Aqua Park logo T-shirt
  variant: Green / M
  price: AED 89.00
  onHand: 5
  allocated: 3
  available: 2
  otherStores:
  - store: Beach Hut
    available: 6
  - store: Main Gate Kiosk
    available: 0
```

#### Permissions

- `getStockPositions` → `PRODUCT_VIEW` (read) · staff
- `getOutletStock` → `PRODUCT_VIEW` (read) · staff
- `lookupMerchandise` → `PRODUCT_VIEW` (read) · staff, guest

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

- Store Stock & Availability: search by product to see stock-on-hand vs. available stock, factoring in pending online purchases awaiting pickup/shipment. *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-361)*
- Item lookup by name or barcode scan shows stock and availability across stores/warehouses; inventory count and goods receipt are done in the app. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-233)*

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-062` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 5.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 5.dc.html#fnb-5j`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-062?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] Every transition is wired: `EMP-067`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-063` Requisition & Smart Store Replenishment

**Requisition & Smart Store Replenishment — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 2 · needs the `inventory` module |
| Block | Block D · task APP-STAFF-EMP-063 |
| Who uses it | venue staff holding `PROCUREMENT_REQUEST`, `PROCUREMENT_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listRequisitions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `requisitionId` (navigation) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/requisition-smart-store-replenishment` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed.

**From the Food, Beverage & Retail process.** The handheld side of requisitions: an outlet manager or storekeeper sees what is running low, raises a request (from a suggestion or from scratch) and tracks its status. Approval happens in the back office. The one thing to get right is the suggestion: the suggested quantity stays visible beside what was asked for.

**Known correction pending (do not draw the wrong version)**

- **The no-access state names the stock-view permission, while listing requisitions needs the procurement-view permission. The filters are "Status" and "Raised by principal id" text fields.** Why: The wrong permission name, and plumbing on a handheld. *(source: R091 / contracts/satellite/inventory.yaml#listRequisitions; Food, Beverage & Retail)*
- **Requests to replenish from another store (inter-store requisition) cannot be raised here.** Why: The client named this screen for inter-store requisitions with approval before transfer. See the BO-078 correction. *(source: DI-362; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Only create and list are bound. The "smart replenishment" half (suggestions from reorder points) and editing lines before approval are … (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · Pending approval · Approved · Rejected · Returned for info · Ordered · Closed · Cancelled | — | Sends `?status=` to `listRequisitions`. | `listRequisitions` ?status |
| Raised by principal id | picker: choose a raised by principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?raisedByPrincipalId=` to `listRequisitions`. | `listRequisitions` ?raisedByPrincipalId |
| Search requisition | search field | — | — | — | — | — | — |

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

**Form: Edit lines** (modal, opened by *Edit lines*; *Edit lines* calls `updateRequisitionLines`, *Cancel* sends nothing)

**Collects what `updateRequisitionLines` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | — | — | — | `updateRequisitionLines` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `updateRequisitionLines` body |
| Quantity `lines[].quantity` | number field | required | — | — | — | — | `updateRequisitionLines` body |
| Reason `lines[].reason` | text area | optional | — | — | — | Why the quantity differs from the suggestion. Kept on the line. | `updateRequisitionLines` body |

Errors to draw in the form: 409 Already approved: the requisition is `approved`, `ordered` or `closed` (audit R171), or it is `rejected` or `cancelled`.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Request lines**: Scan or search items, quantity in base or purchase unit, a reason when it differs from the suggestion, required-by date. *(source: DI-234 / DI-343 / contracts/satellite/inventory.yaml#updateRequisitionLines)*

#### Outputs: what the screen shows and produces

**Shown**

**Every requisition** (data table, from `listRequisitions`)

| Shows | Format | Notes |
|---|---|---|
| Requisition number | text | — |
| Status | chip: Draft, Pending approval, Approved, Rejected, Returned for info, Ordered… | — |
| Estimated total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approved at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Suggested** (data table, from `getSuggestedRequisitions`)

| Shows | Format | Notes |
|---|---|---|
| Suggestions | list or chips (count when long) | — |
| Item | the name it points at, never the id | — |
| Item name | text | — |
| SKU | text | — |
| On hand | 1,234.5 | — |
| Reorder point | 1,234.5 | — |
| Par level | 1,234.5 | — |
| Suggested quantity | 1,234.5 | — |
| Average daily consumption | 1,234.5 | — |
| Days of cover remaining | 1,234.5 | — |
| Preferred supplier | the name it points at, never the id | — |
| Lead time days | 1,234 | — |

**The selected requisition** (detail panel, from `listRequisitions`)

| Shows | Format | Notes |
|---|---|---|
| Requisition number | text | — |
| Status | chip: Draft, Pending approval, Approved, Rejected, Returned for info, Ordered… | — |
| Lines | list or chips (count when long) | — |
| Estimated total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Approved at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Create requisition (primary button) | `createRequisition` POST `/requisitions` | CreateRequisitionRequest | Requisition | 400 Validation failed | works offline; opens modal first |
| Edit lines (secondary button) | `updateRequisitionLines` PUT `/requisitions/{requisitionId}/lines` | inline | Requisition | 409 Already approved: the requisition is `approved`, `ordered` or `closed` (audit R171), or it is `rejected` or `cancelled`. | works offline; opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **My requests**: Cards with number, status (same words as BO-078), required-by date and estimated total. "Returned for information" cards show the approver's question first. *(source: contracts/satellite/inventory.yaml#listRequisitions)*

**Data it reads**: `listRequisitions` (onLoad, List requisitions); `getSuggestedRequisitions` (onLoad, Below-par items as a draft for review)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The requisition smart store list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the requisition smart store untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No requisition smart store yet. Offers Create requisition (`createRequisition`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, raisedByPrincipalId and the requisition smart store are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PROCUREMENT_VIEW`, which `listRequisitions` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_REQUEST` for `createRequisition`, `updateRequisitionLines`. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Already approved: the requisition is `approved`, `ordered` or `closed` (audit R171), or it is `rejected` or `cancelled`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
suggestion:
  item: Coca-Cola 330 ml can
  onHand: 96
  reorderPoint: 240
  suggested: 3 case (72 can)
  daysOfCover: 1.4
request:
  number: REQ-AQP-000121
  status: Pending approval
  requiredBy: '2026-10-23'
  estimatedTotal: AED 642.00
```

#### Permissions

- `createRequisition` → `PROCUREMENT_REQUEST` (operate) · staff
- `listRequisitions` → `PROCUREMENT_VIEW` (read) · staff
- `getSuggestedRequisitions` → `PROCUREMENT_VIEW` (read) · staff
- `updateRequisitionLines` → `PROCUREMENT_REQUEST` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PROCUREMENT_VIEW`, which `listRequisitions` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_REQUEST` for `createRequisition`, `updateRequisitionLines`.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Outlets raise inter-store requisitions subject to an approval workflow before transfer; stock can be transferred between any two stores (outlet-to-outlet, warehouse-to-outlet, outlet-to-warehouse). *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-362)*
- Requisitions raised in the app flow to department-head approval then purchasing; stock falling below a par level (e.g. 100 units) auto-creates a draft requisition for review and confirmation. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-234)*

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-063` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4f`

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-063?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create requisition, Edit lines.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PROCUREMENT_REQUEST`, `PROCUREMENT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-064` Store-to-Store & Warehouse Transfers

**Store-to-Store & Warehouse Transfers — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 2 · needs the `inventory` module |
| Block | Block D · task APP-STAFF-EMP-064 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listStockLocations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `transferId` (navigation) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/store-to-store-warehouse-transfers` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed.

**From the Food, Beverage & Retail process.** The handheld side of transfers: send stock from this store to another (store to store, warehouse to store, store to warehouse), and receive what is inbound. The one thing to get right is that the receiving person sees the manifest and records what actually arrived.

**Known correction pending (do not draw the wrong version)**

- **Transfers have no approval step, although this screen is named for approved inter-store transfers.** Why: See the BO-080 correction. *(source: DI-362; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The screen lists stock locations and can only create a transfer. It has no transfer list, no manifest and no "Receive". (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search store-to-store | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Dispatched · In transit · Received · Partially received · Cancelled | `listStockTransfers` ?status |

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

**Form: Receive** (modal, opened by *Receive*; *Receive* calls `receiveStockTransfer`, *Cancel* sends nothing)

**Collects what `receiveStockTransfer` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `receiveStockTransfer` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `receiveStockTransfer` body |
| Received quantity `lines[].receivedQuantity` | number field | required | — | min 0 | — | — | `receiveStockTransfer` body |
| Discrepancy reason `lines[].discrepancyReason` | text area | optional | — | max length 500 | — | — | `receiveStockTransfer` body |

Errors to draw in the form: 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Send**: To (location picker grouped by venue), lines by scan with available-at-source shown, note. *(source: DI-362 / contracts/satellite/inventory.yaml#createStockTransfer)*

#### Outputs: what the screen shows and produces

**Shown**

**Every stock location** (data table, from `listStockLocations`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Main store, Sub store, Kitchen, Bar, Retail floor, Cellar… | — |
| Is active | yes / no (icon or chip) | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Transfers** (data table, from `listStockTransfers`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Transfer number | text | — |
| From location | the name it points at, never the id | — |
| To location | the name it points at, never the id | — |
| Status | chip: Dispatched, In transit, Received, Partially received, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Item | the name it points at, never the id | — |
| Item name | text | — |
| Dispatched quantity | 1,234.5 | — |
| Received quantity | 1,234.5 | — |
| Discrepancy | 1,234.5 | — |
| Discrepancy reason | text | — |
| Dispatched by principal | the name it points at, never the id | — |
| Received by principal | the name it points at, never the id | — |
| Dispatched at | 1 Oct 2026, 14:30 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Close short reason | text | Why the balance was written off, from `closeTransferShort`. |
| Close short signed by principal | the name it points at, never the id | The supervisor whose step-up closed the transfer short (audit R144). |
| From venue | the name it points at, never the id | The venue of `fromLocationId`. Set by the server (audit R183). |

**Manifest** (detail panel, from `getStockTransfer`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Transfer number | text | — |
| From location | the name it points at, never the id | — |
| To location | the name it points at, never the id | — |
| Status | chip: Dispatched, In transit, Received, Partially received, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Item | the name it points at, never the id | — |
| Item name | text | — |
| Dispatched quantity | 1,234.5 | — |
| Received quantity | 1,234.5 | — |
| Discrepancy | 1,234.5 | — |
| Discrepancy reason | text | — |
| Dispatched by principal | the name it points at, never the id | — |
| Received by principal | the name it points at, never the id | — |
| Dispatched at | 1 Oct 2026, 14:30 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Close short reason | text | Why the balance was written off, from `closeTransferShort`. |
| Close short signed by principal | the name it points at, never the id | The supervisor whose step-up closed the transfer short (audit R144). |
| From venue | the name it points at, never the id | The venue of `fromLocationId`. Set by the server (audit R183). |
| To venue | the name it points at, never the id | The venue of `toLocationId`. Set by the server (audit R183). |

**The selected stock location** (detail panel, from `listStockLocations`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Main store, Sub store, Kitchen, Bar, Retail floor, Cellar… | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Create stock transfer (primary button) | `createStockTransfer` POST `/stock-transfers` | CreateStockTransferRequest | StockTransfer | 409 Insufficient stock at the source | opens modal first |
| Receive (secondary button) | `receiveStockTransfer` POST `/stock-transfers/{transferId}/receive` | inline | StockTransfer | 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Transfers**: Two tabs, Outbound and Inbound, with status words as on BO-080 (In transit, Partly received, Received, Closed short). *(source: R183 / contracts/satellite/inventory.yaml#listStockTransfers)*

**Data it reads**: `listStockLocations` (onLoad, List stock locations); `listStockTransfers` (onLoad, Inbound and outbound transfers)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The store-to-store warehouse transfers list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the store-to-store warehouse transfers untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No store-to-store warehouse transfers yet. Offers Create stock transfer (`createStockTransfer`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listStockLocations` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listStockLocations` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createStockTransfer`, `receiveStockTransfer`. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient stock at the source; 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- number: TRF-AQP-000088
  from: Main Store
  to: Beach Hut
  status: In transit
  lines:
  - item: Kids swim goggles, blue
    qty: 30
  - item: Beach towel, blue
    qty: 20
```

#### Permissions

- `createStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff
- `listStockLocations` → `PRODUCT_VIEW` (read) · staff
- `listStockTransfers` → `PRODUCT_VIEW` (read) · staff
- `getStockTransfer` → `PRODUCT_VIEW` (read) · staff
- `receiveStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listStockLocations` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createStockTransfer`, `receiveStockTransfer`.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.15 | Support stock transfers between stores and warehouses including approval workflows, shipment tracking, receiving confirmation, and audit logs. | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 4.5.5 | The system should provide ability to transfer stocks to another store with a approval level | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 4.5.14 | Transfer inventory between locations with approval workflows. | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 15.1.15 | In-Transit Inventory Tracking - System shall track inventory in transit. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.16 | Internal Transfers - System shall support internal transfers. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.17 | Replenishment Management - System shall support warehouse replenishment. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.5.3 | Inter-Venue Transfers - System shall support inter-venue transfers. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 4.5.4 | The system should have the ability to record the local /in store inventory (stock management system: used for in-store stock view/management reporting) | Bundles and Promotions | CONTRACTED | `listStockLocations` |
| 4.5.13 | Manage inventory across multiple warehouses and locations. | Bundles and Promotions | CONTRACTED | `listStockLocations` |
| 10.1.5 | The system should have the ability to record the local /in store inventory( for in store stock view/management). | Games & F&B Integration | CONTRACTED | `listStockLocations` |
| 15.2.15 | Shipment Tracking - System shall support shipment tracking. | Inventory Management | CONTRACTED | `receiveStockTransfer` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Outlets raise inter-store requisitions subject to an approval workflow before transfer; stock can be transferred between any two stores (outlet-to-outlet, warehouse-to-outlet, outlet-to-warehouse). *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-362)*

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-064` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4g`

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-064?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create stock transfer, Receive.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-065` Receiving

**Receiving & Store Put-Away — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 1 · needs the `inventory` module |
| Block | Block A · task APP-SETUP-EMP-065 |
| Who uses it | venue staff holding `INCIDENT_REPORT`, `PROCUREMENT_RECEIVE`, `PROCUREMENT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 operate, 2 read, 1 configure); in the flows as storekeeper |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getStockTransfer` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `receiptId` (EMP-003), `transferId` (deepLink) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. A transfer opened from the list, or scanned … |
| Route | `/operations/receiving-store-put-away` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.** **Retitled "Receiving"** (DI-346, the simplicity principle: no put-away, picking, packing or dispatching statuses; design-notes correction fnb-retail EMP-065; CHG-SPO-018). The screen id and route are unchanged.

**From the Food, Beverage & Retail process.** Receiving is the handheld screen at the delivery door: open the expected delivery (a supplier order or an inbound transfer), read the manifest before touching the goods, record the temperature of chilled deliveries, book in what arrived line by line with batch and expiry, and refuse what is damaged. The one thing to get right is order: manifest first, temperature before posting, refusal at the door.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The rejection reasons are a fixed list. (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): The title is "Receiving & Store Put-Away". (CHG-SPO-018); The screen has no way to find the expected supplier order (no order list or read), and no "Receive" for an inbound transfer … (CHG-WIR-008); F35 step 3 rejects damaged transfer cases "at the door, before the receipt is posted" with rejectReceivedGoods. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search receiving | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Raised · Sent · Acknowledged · Partially received · Received · Closed short · Cancelled | `listPurchaseOrders` ?status |
| Supplier | picker: choose a supplier | — | — | `listPurchaseOrders` ?supplierId |

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

**Form: Log cold chain** (modal, opened by *Log cold chain*; *Log cold chain* calls `logColdChain`, *Cancel* sends nothing)

**Collects what `logColdChain` sends before it is called.** Required: `id`, `recordedAt`, `valueCelsius`, `decision`. Optional: `goodsReceiptId`, `transferId`, `thresholdCelsius`, `correctiveActionId`, `supplierClaimRaised`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `logColdChain` body |
| Goods receipt `goodsReceiptId` | picker: choose a goods receipt | optional | — | — | shows names, sends the id | — | `logColdChain` body |
| Transfer `transferId` | picker: choose a transfer | optional | — | — | shows names, sends the id | — | `logColdChain` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `logColdChain` body |
| Value celsius `valueCelsius` | number field | required | — | — | — | — | `logColdChain` body |
| Threshold celsius `thresholdCelsius` | number field | optional | — | — | — | — | `logColdChain` body |
| Decision `decision` | radio group | required | — | Accepted · Accepted with note · Partially rejected · Rejected | — | — | `logColdChain` body |
| Corrective action `correctiveActionId` | picker: choose a corrective action | optional | — | — | shows names, sends the id | — | `logColdChain` body |
| Supplier claim raised `supplierClaimRaised` | toggle | optional | off | — | — | — | `logColdChain` body |

**Form: Receive transfer** (modal, opened by *Receive transfer*; *Receive transfer* calls `receiveStockTransfer`, *Cancel* sends nothing)

**Collects what `receiveStockTransfer` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `receiveStockTransfer` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `receiveStockTransfer` body |
| Received quantity `lines[].receivedQuantity` | number field | required | — | min 0 | — | — | `receiveStockTransfer` body |
| Discrepancy reason `lines[].discrepancyReason` | text area | optional | — | max length 500 | — | — | `receiveStockTransfer` body |

Errors to draw in the form: 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short

**Sent by *Reject received goods*** (`rejectReceivedGoods`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `rejectReceivedGoods` body |
| Line `lines[].lineId` | picker: choose a line | required | — | — | shows names, sends the id | `GoodsReceipt.lines[].lineId`, the batch or expiry line rejected (audit R171). | `rejectReceivedGoods` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `rejectReceivedGoods` body |
| Reason `reason` | select | required | — | Damaged · Wrong item · Quality failure · Short dated · Over delivery · Other | — | `other` requires `note` (decided 28 September, audit R222). | `rejectReceivedGoods` body |
| Note `note` | text area | optional | — | max length 1000 | — | Required, at least 3 characters, when `reason` is `other` (audit R222). | `rejectReceivedGoods` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Delivery**: Scan the delivery note or pick from today's expected deliveries for this location: supplier orders that are sent or partly received, and inbound transfers in transit. Show supplier or sending store, reference and number of lines. *(source: F35 step 2 / contracts/satellite/inventory.yaml#getStockTransfer)*
- **Temperature (chilled and frozen)**: Reading in °C with the threshold shown, and a decision: Accept, Accept with note, Partly reject, Reject. Taken before posting. A breach opens a major corrective action automatically. *(source: F28 step 1 / R125 / contracts/satellite/fnb.yaml#logColdChain)*
- **Received quantity per line**: Big steppers; scan an item to jump to its line. "All as sent / as ordered" shortcut. The limit for a supplier order is outstanding plus the tolerance (proposed 5%). *(source: R094 / contracts/satellite/inventory.yaml#createGoodsReceipt)*
- **Batch and expiry**: Expiry required for perishable items. A date picker that defaults to empty, never to today. "Add batch" splits a line. *(source: R171 / DI-345)*
- **Rejection**: Per receipt line: quantity, reason (Damaged, Wrong item, Quality failure, Short-dated, Over-delivery, Other) and a note, required for Other. *(source: R171 / R222 / contracts/satellite/inventory.yaml#rejectReceivedGoods)*

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The stock transfer** (detail panel, from `getStockTransfer`)

| Shows | Format | Notes |
|---|---|---|
| Transfer number | text | — |
| Status | chip: Dispatched, In transit, Received, Partially received, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Dispatched at | 1 Oct 2026, 14:30 | — |
| Received at | 1 Oct 2026, 14:30 | — |

**Expected deliveries** (data table, from `listPurchaseOrders`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Purchase order number | text | Per venue, in sequence (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for … |
| Requisition | the name it points at, never the id | Null on a blanket order or an RFQ award, which are raised without one. |
| Quotation | the name it points at, never the id | The quotation selected when the order was raised (`createPurchaseOrder` requires it). |
| Supplier | the name it points at, never the id | — |
| Supplier name | text | — |
| Kind | chip: Standard, Blanket, Release, Rfq award | BL-159. A blanket order is a price and a commitment, not a delivery. |
| Blanket parent | the name it points at, never the id | The blanket order this release draws against — another purchase order, so the same id type. |
| Contract price valid until | 1 Oct 2026 | — |
| Rfq | the name it points at, never the id | Where this order came from a quotation round. Keeping the link is what lets a venue show it took the best of three, which is usually the … |
| Supplier invoice ref | text | BL-123. Purchase orders and goods receipts both existed — the third leg did not. |
| Match status | chip: Unmatched, Matched, Price variance, Quantity variance, Both variance | The variance kinds are separated because they have different owners — a price variance is a buyer's problem and a quantity variance is a … |
| Status | chip: Raised, Sent, Acknowledged, Partially received, Received, Closed short… | — |
| Deliver to location | the name it points at, never the id | Scoped 31 August. A purchase order is raised by somebody, for somewhere, and carried neither. |
| Lines | list or chips (count when long) | — |
| Line | text | — |
| Item | the name it points at, never the id | — |
| Item name | text | — |
| Ordered quantity | 1,234.5 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create goods receipt (primary button) | `createGoodsReceipt` POST `/goods-receipts` | CreateGoodsReceiptRequest | GoodsReceipt | 409 Over-receipt beyond `VenueSettings.inventory.overReceiptTolerancePercent` (proposed default 5, audit R094), or the purchase order is closed | works offline; opens modal first; produces a document or message: Receive goods against a purchase order |
| Reject received goods (destructive button) | `rejectReceivedGoods` POST `/goods-receipts/{receiptId}/reject` | inline | GoodsReceipt | 400 `reason` is `other` with no `note` (audit R222).; 409 A line rejects more than was received and not already rejected on it, or names a `lineId` the receipt does not hold (audit R171) | — |
| Log cold chain (secondary button) | `logColdChain` POST `/food-safety/cold-chain` | ColdChainEvent | ColdChainEvent | — | works offline; opens modal first |
| Receive transfer (secondary button) | `receiveStockTransfer` POST `/stock-transfers/{transferId}/receive` | inline | StockTransfer | 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short | opens modal first |
| Confirm (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Manifest**: Line by line, what is expected (ordered or sent) against what is being received. A running "Missing" count shows at the top. *(source: F35 step 2 / contracts/satellite/inventory.yaml#getStockTransfer)*
- **Done**: Receipt number (e.g. AQP-GR-000431) or "Transfer received", lines received, lines rejected, "Stock updated". If the device was offline: "Saved on this device, will sync" with the number from the device's reserved range. *(source: R152 / contracts/satellite/inventory.yaml#/components/schemas/GoodsReceipt)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Post receipt**: Adds stock. Offline-capable for supplier orders. Over-receipt is refused, naming the line and its maximum. *(source: contracts/satellite/inventory.yaml#createGoodsReceipt / R094)*
- **Reject**: Reverses the stock on the chosen lines and raises a supplier return. Needs a connection. *(source: contracts/satellite/inventory.yaml#rejectReceivedGoods)*

**Data it reads**: `getStockTransfer` (onLoad, One transfer, its manifest and where it is); `listPurchaseOrders` (onLoad, The supplier orders expected today)

**Where the user goes next**

- → `BO-052` Goods Receipt: *The rest is received and the transfer closes short*; carries `purchaseOrderId`, `receiptId`
- → `BO-080` Stock Transfers: *The rest is received and the transfer closes short*; carries `transferId`

**What opens over it**

- confirmDialog *Reject received goods*: **Names what `rejectReceivedGoods` changes and what it leaves alone**, in the consequence rather than the verb. A receiving store put-away this affects should be identified in the dialog, not just counted. **Collects what `rejectReceivedGoods` sends before it is called.** Required: `lines` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The receiving store put-away, read by `getStockTransfer`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the receiving store put-away untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No receiving store put-away yet. Offers Create goods receipt (`createGoodsReceipt`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getStockTransfer` requires to show this screen, and names that permission (the screen's other reads need `PROCUREMENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_REPORT` for `logColdChain`; `PROCUREMENT_RECEIVE` for … |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `reason` is `other` with no `note` (audit R222).; 409 A line rejects more than was received and not already rejected on it, or names a `lineId` the receipt does not hold (audit R171); 409 Over-receipt beyond `VenueSettings.inventory.overReceiptTolerancePercent` (proposed default 5, audit R094), or the purchase order is closed; 409 The transfer is not `inTransit` or `partiallyReceived` — it … |

#### Edge cases to draw

- **Offline at the loading bay**: The receipt and the temperature reading queue. Rejection waits for the connection, and the screen says "Reject when back online". *(source: contracts/satellite/inventory.yaml#createGoodsReceipt / contracts/satellite/fnb.yaml#logColdChain / contracts/satellite/inventory.yaml#rejectReceivedGoods)*
- **Damage found after opening the cases**: Received, then adjusted with a damage reason (Damage, Loss & Adjustment). It is no longer a door rejection. *(source: F35 step 3)*

#### Consistency with other screens

- Match `BO-052`: Same fields, reasons and tolerance message as the back-office receipt.
- Match `BO-080`: Same manifest and discrepancy wording for an inbound transfer.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
delivery:
  supplier: Gulf Fresh Dairy LLC
  order: PO-AQP-000214
  deliveryNote: GFD-DN-778120
  expected: 16 Oct 2026, 07:00–09:00
temperature:
  reading: 3.8 °C
  threshold: ≤ 5 °C
  decision: Accept
lines:
- item: Full-cream milk 2 L
  ordered: 60
  received: 60
  batches:
  - batch: L2610A
    expiry: '2026-10-23'
    qty: 36
  - batch: L2610B
    expiry: '2026-10-24'
    qty: 24
- item: Greek yoghurt 1 kg
  ordered: 24
  received: 24
  rejected: 4
  reason: Damaged
receiver: Khalid Al Mansoori
```

#### Permissions

- `createGoodsReceipt` → `PROCUREMENT_RECEIVE` (operate) · staff
- `rejectReceivedGoods` → `PROCUREMENT_RECEIVE` (operate) · staff
- `logColdChain` → `INCIDENT_REPORT` (operate) · staff
- `getStockTransfer` → `PRODUCT_VIEW` (read) · staff
- `listPurchaseOrders` → `PROCUREMENT_VIEW` (read) · staff
- `receiveStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getStockTransfer` requires to show this screen, and names that permission (the screen's other reads need `PROCUREMENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_REPORT` for `logColdChain`; `PROCUREMENT_RECEIVE` for …

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.5.10 | Receive inventory against purchase orders. | Bundles and Promotions | CONTRACTED | `createGoodsReceipt` |
| 4.5.30 | Receive goods against purchase orders. | Bundles and Promotions | CONTRACTED | `createGoodsReceipt` |
| 4.5.32 | Support partial deliveries. | Bundles and Promotions | CONTRACTED | `createGoodsReceipt` |
| 15.2.5 | Purchase Receiving - System shall support receiving operations. | Inventory Management | CONTRACTED | `createGoodsReceipt` |
| 15.2.6 | Receiving Validation - System shall validate received goods. | Inventory Management | CONTRACTED | `createGoodsReceipt` |
| 15.2.7 | Receiving Discrepancy Management - System shall manage receiving discrepancies. | Inventory Management | CONTRACTED | `createGoodsReceipt` |
| 15.2.15 | Shipment Tracking - System shall support shipment tracking. | Inventory Management | CONTRACTED | `receiveStockTransfer` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Receiving, stock counts (monthly/weekly/as needed) and damage/loss adjustments are supported, with a fully configurable user-defined reason list extendable in the backend without development. *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-363)*
- Item lookup by name or barcode scan shows stock and availability across stores/warehouses; inventory count and goods receipt are done in the app. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-233)*

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-065` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 5.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 5.dc.html#fnb-5g`
- Flow F35 *Stock arrives short and an oversell is resolved*, step 2: The delivery arrives. The receiver opens the manifest before touching it. → **Built 24 August because nothing read a transfer** — `createStockTransfer`, `receiveStockTransfer` and `closeTransferShort` all existed, and **the receiving store could accept a delivery it could …
- Flow F35 *Stock arrives short and an oversell is resolved*, step 3: Two cases are damaged in transit. They are rejected at the door. → **Rejected before the receipt is posted.** Once stock is received it has entered the store, and a claim against the sender needs the reading that refused it.
- Flow F35 branch at step 3 (medium): when The damage is not visible until the cases are opened., **Received, then adjusted.** `createStockMovement` with a damage reason rather than a rejection — **the transfer is closed and the claim is a separate conversation with the sending store**, which is …

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-065?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create goods receipt, Reject received goods, Log cold chain, Receive transfer, Confirm.
- [ ] Every transition is wired: `BO-052`, `BO-080`.
- [ ] Every gated control is gated: `INCIDENT_REPORT`, `PROCUREMENT_RECEIVE`, `PROCUREMENT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-066` Stock Count & Cycle Count Management

**Stock Count & Cycle Count Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 2 · needs the `inventory` module |
| Block | Block D · task APP-STAFF-EMP-066 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as storekeeper |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getCountVariance` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `countId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/stock-count-cycle-count-management` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Drawn 31 August** — `Retail Board 4.dc.html` frame `ret-4f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Stock Count &amp; Cycle Count Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): In F30, variance review, recount requests and posting are the supervisor's steps on BO-079 (steps 4, 5 and 7); a counter's device showing variance weakens the … Removed 2 October 2026 (CHG-WIR-008): In F30, variance review, recount requests and posting are the supervisor's steps on BO-079 (steps 4, 5 and 7); a counter's device showing variance weakens the … Removed 2 October 2026 (CHG-WIR-008): In F30, variance review, recount requests and posting are the supervisor's steps on BO-079 (steps 4, 5 and 7); a counter's device showing variance weakens the …

**From the Food, Beverage & Retail process.** The counter's handheld. Open the count assigned to my location, walk the shelves and enter what is there, line by line, blind, offline if needed. Recount the lines a supervisor sends back. The daily count list lives here too. The one thing to get right is that the counter never sees the expected quantity or the variance on this device.

**Known correction pending (do not draw the wrong version)**

- **Bulk RFID counting is requested but has no operation or device.** Why: Open with the client. The RFID reader is still on the hardware list. *(source: DI-365 / TRACKER 30-Sep/Tracker row 28; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The handheld carries the variance panel, "Post stock count" and "Request recount". It has no list of open counts to choose from. (CHG-WIR-008); The first-run state offers "Request recount". (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search stock count | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `listStockCounts` ?locationId |
| Status | select | — | Open · Counting · Closed · Variance pending · Posted · Cancelled | `listStockCounts` ?status |

**Form: Start stock count** (modal, opened by *Start stock count*; *Start stock count* calls `startStockCount`, *Cancel* sends nothing)

**Collects what `startStockCount` sends before it is called.** Required: `id`, `locationId`, `kind`. Optional: `categoryIds`, `isBlind` (defaults true). Starting pre-fills one line per item with stock at the location, expected snapshotted and hidden until submission (audit R110 (a)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `startStockCount` body |
| Location `locationId` | picker: choose a location | required | — | — | shows names, sends the id | — | `startStockCount` body |
| Kind `kind` | segmented control | required | — | Full · Cycle · Spot | — | — | `startStockCount` body |
| Categorys `categoryIds` | multi-picker: choose categorys | optional | — | — | — | For cycle counts — restrict to these categories. | `startStockCount` body |
| Is blind `isBlind` | toggle | optional | on | — | — | Expected quantities withheld from the counting device. Defaults true because a counter who can see the figure reconciles to it rather than to the shelf. | `startStockCount` body |

Errors to draw in the form: 409 A count is already open for this location

**Form: Enter count line** (modal, opened by *Enter count line*; *Enter count line* calls `enterCountLine`, *Cancel* sends nothing)

**Collects what `enterCountLine` sends before it is called.** Required: `recordedAt`, `itemId`, `countedQuantity`. Optional: `locationId`, `uom`, `batchId`, `note`. `enterCountLine` returns no expected quantity or variance, and the screen shows neither until the count is submitted, then reads `getCountVariance` (decided 28 September, audit R110 (a)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time the line was counted. The second entry for a line replaces the first in this order. | `enterCountLine` body |
| Item `itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `enterCountLine` body |
| Location `locationId` | picker: choose a location | optional | — | — | shows names, sends the id | — | `enterCountLine` body |
| Counted quantity `countedQuantity` | number field | required | — | — | — | — | `enterCountLine` body |
| UOM `uom` | text field | optional | — | — | — | — | `enterCountLine` body |
| Batch `batchId` | picker: choose a batch | optional | — | — | shows names, sends the id | — | `enterCountLine` body |
| Note `note` | text area | optional | — | — | — | — | `enterCountLine` body |

**Form: Save daily count** (modal, opened by *Save daily count*; *Save daily count* calls `setDailyCount`, *Cancel* sends nothing)

**Collects what `setDailyCount` sends before it is called.** Required: `itemIds`. Optional: `locationId`, `dueBy`, `postsAdjustment`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Items `itemIds` | multi-picker: choose items | required | — | — | — | — | `setDailyCount` body |
| Location `locationId` | picker: choose a location | optional | — | — | shows names, sends the id | — | `setDailyCount` body |
| Due by `dueBy` | text field | optional | — | — | — | Local time, e.g. | `setDailyCount` body |
| Posts adjustment `postsAdjustment` | toggle | optional | off | — | — | False, and it should stay false. A daily count that adjusts stock removes the variance it exists to surface. | `setDailyCount` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Count line**: Pre-filled item list (one card per item at the location) with a blank quantity. Scan to jump to an item. Unit selector (base or purchase unit). Optional batch and note. Entering a line again replaces the earlier entry. *(source: R110 / R171 / contracts/satellite/fnb.yaml#enterCountLine)*
- **Daily count list**: Choose the 20 or so items counted every day (high-value, high-variance) and the due time. "Adjust stock" stays off: a daily count is a check, not a correction. *(source: F30 step 1 / contracts/satellite/inventory.yaml#setDailyCount)*

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking. **The lines arrive pre-filled from on-hand stock** — one card per item at the location, with a blank count and no expected figure; the counter enters what is on the shelf (audit R110 (a), R171 (7)).

**Open counts** (data table, from `listStockCounts`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Location name | text | — |
| Kind | text | — |
| Status | chip: Open, Counting, Closed, Variance pending, Posted, Cancelled | — |
| Is blind | yes / no (icon or chip) | — |
| Line count | 1,234 | — |
| Counted count | 1,234 | — |
| Variance line count | 1,234 | — |
| Variance value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Started by principal | the name it points at, never the id | — |
| Posted by principal | the name it points at, never the id | — |
| Journal entry | text | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Closed at | 1 Oct 2026, 14:30 | — |
| Posted at | 1 Oct 2026, 14:30 | — |
| Recount reason | text | Why the count was last sent back by `recountStockCount`. |
| Recount signed by principal | the name it points at, never the id | The supervisor whose step-up sent the count back last (audit R144). |
| Cancel reason | text | Why it was abandoned, from `cancelStockCount`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Start stock count (primary button) | `startStockCount` POST `/stock-counts` | StartStockCountRequest | StockCount | 409 A count is already open for this location | works offline; opens modal first |
| Enter count line (secondary button) | `enterCountLine` POST `/fnb-stock-counts/{countId}/lines` | inline | inline | — | works offline; opens modal first |
| Save daily count (secondary button) | `setDailyCount` PUT `/stock-counts/daily` | inline | inline | — | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Progress**: "38 of 46 counted", and lines sent back for recount highlighted at the top with the supervisor's reason. *(source: F30 step 6 / contracts/satellite/fnb.yaml#requestRecount)*

**Data it reads**: `listStockCounts` (onLoad, The open counts to enter lines on)

**Where the user goes next**

- → `BO-079` Stock Count: *The supervisor reviews the variance*; carries `countId`; calls `enterCountLine`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stock count cycle, read by `listStockCounts`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stock count cycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stock count cycle yet. Offers Start stock count (`startStockCount`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listStockCounts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `startStockCount`, `enterCountLine`, `setDailyCount`. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A count is already open for this location |

#### Edge cases to draw

- **No signal in the cellar**: Lines save on the device and the count stays open. A small "12 lines waiting to sync" banner. *(source: F30 step 2)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
count:
  location: Main Store > Beverage Store
  type: Full
  lines: 212
  counted: 87
line:
  item: Still water 500 ml bottle
  unit: case of 24
  counted: 18 case + 7 bottle
```

#### Permissions

- `startStockCount` → `PRODUCT_CONFIGURE` (configure) · staff
- `enterCountLine` → `PRODUCT_CONFIGURE` (configure) · staff
- `setDailyCount` → `PRODUCT_CONFIGURE` (configure) · staff
- `listStockCounts` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listStockCounts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `startStockCount`, `enterCountLine`, `setDailyCount`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.16 | Support physical inventory counts, cycle counts, stock corrections, damaged goods handling, and inventory reconciliation. | Bundles and Promotions | CONTRACTED | `startStockCount` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Allam: support bulk stock-taking with handheld RFID scanners — scanning a batch of tagged items updates system quantities once verified and saved. Chinmay's focus is reconciling existing stock vs. newly scanned data. Device specs pending. *(open · MoM 19 Aug 2026, 4.6 RFID/Barcode-Based Bulk Stock Counting — Open Item · DI-365)*
- Receiving, stock counts (monthly/weekly/as needed) and damage/loss adjustments are supported, with a fully configurable user-defined reason list extendable in the backend without development. *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-363)*
- Item lookup by name or barcode scan shows stock and availability across stores/warehouses; inventory count and goods receipt are done in the app. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-233)*

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-066` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Client design-board frames: `Retail Board 4.dc.html#ret-4f`
- Flow F30 *A count is entered, varied and posted*, step 1: The storekeeper opens the count. → A count in `open`, scoped to a location and an item set. **The theoretical position is not snapshotted here** — it is captured per line, at entry.
- Flow F30 *A count is entered, varied and posted*, step 2: They count the shelf and enter each line. → **The theoretical quantity is snapshotted at entry, not at post.** Stock moves during a count, and a variance computed at post time is measured against a different number from the one the counter was …
- Flow F30 *A count is entered, varied and posted*, step 3: A line is miskeyed. They count again and re-enter it. → **The second entry replaces the first.** A counter who miskeys and re-counts is the normal case, and a model that refuses the second sends them to a supervisor to undo the first.
- Flow F30 *A count is entered, varied and posted*, step 6: The lines are recounted and re-entered. → Status `recounted`. **The original entry is kept beside the recount** — the pair is what tells a venue whether the problem was the counter or the shelf.
- Flow F30 branch at step 2 (low): when The counter is in a cellar with no signal., **Lines journal locally and the count stays open.** This is the ordinary case, not the edge — and a count that cannot be entered where the stock is, is a count entered later from a piece of paper.
- Flow F30 branch at step 1 (medium): when It is a daily count rather than a full one., Same flow, twenty lines. **`postsAdjustment` is false and should stay false** — a daily count is a check, not a correction, and one that silently adjusts stock hides the shrinkage it exists to find.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-066?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Start stock count, Enter count line, Save daily count.
- [ ] Every transition is wired: `BO-079`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-067` Damage, Loss, Shrinkage & Stock Adjustment

**Damage, Loss, Shrinkage & Stock Adjustment — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-SETUP-EMP-067 |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW`, `ORDER_MODIFY`, `PRODUCT_CONFIGURE` (2 configure, 2 operate, 1 read); in the flows as storekeeper |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`recordWaste`, `createStockMovement`, `logTemperature`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (EMP-003), `actionId` (deepLink) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. A corrective action opened from the … |
| Route | `/operations/damage-loss-shrinkage-stock-adjustment` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.**

**From the Food, Beverage & Retail process.** Damage, Loss & Adjustment on the handheld: record that something broke, spoiled, went missing or was found, with a reason, so stock stays true and shrinkage is visible. The one thing to get right is a single, quick form (item, quantity, reason, note) that writes one movement.

**Known correction pending (do not draw the wrong version)**

- **Waste can be recorded two ways: the F&B waste operation (recordWaste, gated by the order-modify permission) and an inventory movement of kind waste.** Why: Two paths for one event split the waste report. Gating waste by an order permission borrows from the wrong domain (procurement and stock got their own permissions). *(source: R091 / contracts/satellite/fnb.yaml#recordWaste / contracts/satellite/inventory.yaml#createStockMovement; Food, Beverage & Retail)*
- **The reason list is not configurable.** Why: The client asked for a user-defined reason list that can be extended without development. *(source: DI-363; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): A raw "Id" text field and a "Recorded at" date picker are on the form. "Log temperature" and "Sign corrective action" (HACCP) are on this … (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search damage, loss, shrinkage | search field | — | — | — | — | — | — |
| Id | text field | — | — | — | — | Required. | — |
| Lines | multi select | — | — | — | — | Required. | — |
| Reason | select field | — | — | — | — | Required. | — |
| Recorded at | date picker | — | — | — | — | Required. | — |
| Note | text field | — | — | — | — | — | — |

**Form: Create stock movement** (modal, opened by *Create stock movement*; *Create stock movement* calls `createStockMovement`, *Cancel* sends nothing)

**Collects what `createStockMovement` sends before it is called.** Required: `id`, `itemId`, `locationId`, `kind`, `quantity`, `recordedAt`. Optional: `unit`, `reason`, `costCenterId`. **The kind picker offers `adjustmentIn`, `adjustmentOut` and `waste`** — the kind decides the direction, so the quantity is always entered positive; `countGain` and `countLoss` are shown on movements a count posted but are not offered here. **A reason is mandatory for an adjustment or waste** (400 without one) (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Log temperature** (modal, opened by *Log temperature*; *Log temperature* calls `logTemperature`, *Cancel* sends nothing)

**Collects what `logTemperature` sends before it is called.** Required: `id`, `checkPointId`, `recordedAt`, `valueCelsius`, `outcome`. Optional: `checkPointKind`, `recordedByPrincipalId`, `minCelsius`, `maxCelsius`, `deviceReported`, `correctiveActionId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `logTemperature` body |
| Check point `checkPointId` | picker: choose a check point | required | — | — | shows names, sends the id | The unit, station or delivery being read. | `logTemperature` body |
| Check point kind `checkPointKind` | select | optional | — | Fridge · Freezer · Holding cabinet · Blast chiller · Core probe · Delivery · Display counter · Ambient | — | — | `logTemperature` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `logTemperature` body |
| Recorded by principal `recordedByPrincipalId` | picker: choose a recorded by principal | optional | — | — | shows names, sends the id | — | `logTemperature` body |
| Value celsius `valueCelsius` | number field | required | — | — | — | — | `logTemperature` body |
| Min celsius `minCelsius` | number field | optional | — | — | — | — | `logTemperature` body |
| Max celsius `maxCelsius` | number field | optional | — | — | — | — | `logTemperature` body |
| Outcome `outcome` | segmented control | required | — | In range · Out of range · Not taken; A check that did not happen is itself a finding, and a log with a gap cannot be told apart from a log nobody kept. | — | `notTaken` is a record, not an absence. A check that did not happen is itself a finding, and a log with a gap cannot be told apart from a log nobody kept. | `logTemperature` body |
| Device reported `deviceReported` | toggle | optional | off | — | — | A probe reading and a person's reading are different evidence. An inspector treats them differently and so should the record. | `logTemperature` body |
| Corrective action `correctiveActionId` | picker: choose a corrective action | optional | — | — | shows names, sends the id | — | `logTemperature` body |

**Form: Sign corrective action** (modal, opened by *Sign corrective action*; *Sign corrective action* calls `signCorrectiveAction`, *Cancel* sends nothing)

**Collects what `signCorrectiveAction` sends before it is called.** Required: `actionTaken`. Optional: `disposal`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action taken `actionTaken` | text field | required | — | — | — | — | `signCorrectiveAction` body |
| Disposal `disposal` | radio group | optional | — | None · Discarded · Reworked · Quarantined · Returned | — | — | `signCorrectiveAction` body |

Errors to draw in the form: 409 A critical finding signed by the principal who raised it (`CorrectiveAction.raisedByPrincipalId`).

**Sent by *Record waste*** (`recordWaste`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordWaste` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `recordWaste` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `recordWaste` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `recordWaste` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `recordWaste` body |
| Reason `reason` | select | required | — | Spoilage · Preparation error · Customer return · Breakage · Over production · Expired | — | — | `recordWaste` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `recordWaste` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordWaste` body |
| Photo image `photoAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Photo evidence (an `assets` media id). Required where the venue's waste-approval policy is on and the value is at or above its `photoRequiredAbove` (CHG-CSA-016); refused `422 … | `recordWaste` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Item and quantity**: Scan or search, positive quantity, unit. Direction from the choice "Remove from stock" (waste, damage, loss) or "Add to stock" (found). *(source: R171 / contracts/satellite/inventory.yaml#createStockMovement)*
- **Reason**: From the venue's reason list (e.g. Spoilage, Breakage, Expired, Preparation error, Over-production, Theft suspected, Found), with a note required for Other. *(source: DI-363 / R222 / MATRIX 4.6.31)*

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Food safety checks due** (detail panel, from `getHaccpStatus`)

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
| Record waste (primary button) | `recordWaste` POST `/outlets/{outletId}/waste` | inline | inline | 422 The waste-approval policy is on and the value needs photo evidence that was not sent (`photo-required`, CHG-CSA-016). | works offline |
| Create stock movement (secondary button) | `createStockMovement` POST `/stock-movements` | CreateStockMovementRequest | StockMovement | 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock, and the item does not permit negative balances | opens modal first |
| Log temperature (secondary button) | `logTemperature` POST `/food-safety/temperature-logs` | TemperatureLog | inline | — | works offline; opens modal first |
| Sign corrective action (secondary button) | `signCorrectiveAction` POST `/food-safety/corrective-actions/{actionId}/sign` | inline | CorrectiveAction | 409 A critical finding signed by the principal who raised it (`CorrectiveAction.raisedByPrincipalId`). | opens modal first |
| Confirm (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getHaccpStatus` (onLoad, Food-safety checks due and open findings)

**Where the user goes next**

- → `BO-044` F&B Outlets: *The venue manager reviews open and unsigned findings before service*; carries `actionId`, `outletId`; calls `signCorrectiveAction`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved damage loss shrinkage. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the damage loss shrinkage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No damage loss shrinkage configured. The form opens empty and `recordWaste` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `INCIDENT_VIEW`, which `getHaccpStatus` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `signCorrectiveAction`; `INCIDENT_REPORT` for `logTemperature`; `ORDER_MODIFY` for `recordWaste`; `PRODUCT_CONFIGURE` for … |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 A critical finding signed by the principal who raised it (`CorrectiveAction.raisedByPrincipalId`).; 409 Insufficient stock, and the item does not permit negative balances; 422 The waste-approval policy is on and the value needs photo evidence that was not sent … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- item: Wine glass 350 ml
  qty: 6
  direction: Remove
  reason: Breakage
  location: Oasis Bistro Kitchen
  by: Aisha Rahman
- item: Croissant, butter
  qty: 14
  direction: Remove
  reason: Over-production
  location: Bite & Go counter
```

#### Permissions

- `recordWaste` → `ORDER_MODIFY` (operate) · staff
- `createStockMovement` → `PRODUCT_CONFIGURE` (configure) · staff
- `logTemperature` → `INCIDENT_REPORT` (operate) · staff
- `signCorrectiveAction` → `INCIDENT_MANAGE` (configure) · staff
- `getHaccpStatus` → `INCIDENT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `INCIDENT_VIEW`, which `getHaccpStatus` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `signCorrectiveAction`; `INCIDENT_REPORT` for `logTemperature`; `ORDER_MODIFY` for `recordWaste`; `PRODUCT_CONFIGURE` for …

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.31 | Allow mobile recording of food waste and spoilage. | Bundles and Promotions | CONTRACTED | `recordWaste` |
| 4.7.2 | The system should be able to allow negative sales for various operational scenarios. | Bundles and Promotions | CONTRACTED | `recordWaste` |
| 4.7.3 | The system should allow manual recording of wastage of F&B products. | Bundles and Promotions | CONTRACTED | `recordWaste` |
| 6.1.38 | The system should be able to report on F&B wastage: 1.Wastage count 2.Value of wastage 3.Normal wastage/abnormal wastage. | Retail POS | CONTRACTED | `recordWaste` |
| 4.4.13 | Maintain real-time inventory balances and automatically update stock after sales, returns, transfers, adjustments, and goods receipt transactions. | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 4.5.1 | The system should be able to sync all the products and associated information from the inventory management on real-time or timed intervals, to be able to scan/search for the product and complete the … | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 4.5.2 | The system should be able to sync all the product sale and return products between POS and inventory in order to push data back to inventory management tools to manage re-order levels. | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 15.1.16 | Damaged Inventory Tracking - System shall track damaged inventory. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.17 | Goods Receipt - System shall support inventory receipt transactions. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.18 | Inventory Adjustments - System shall support stock adjustments. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.19 | Stock Consumption - System shall record stock consumption. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.20 | Return to Stock - System shall support stock returns. | Inventory Management | CONTRACTED | `createStockMovement` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Receiving, stock counts (monthly/weekly/as needed) and damage/loss adjustments are supported, with a fully configurable user-defined reason list extendable in the backend without development. *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-363)*

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-067` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 5.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 5.dc.html#fnb-5e`
- Flow F28 *A temperature excursion is caught and signed off*, step 1: The check falls due and appears on the storekeeper's list. → Checks due, checks missed, and open actions. **A missed check counts the same as a failed one** — a log with a gap cannot be told apart from a log nobody kept.
- Flow F28 *A temperature excursion is caught and signed off*, step 2: They read the unit and record the temperature. → In range, and the flow ends here. **This is what happens almost every time**, and the flow is written so that the ordinary path is two steps.
- Flow F28 *A temperature excursion is caught and signed off*, step 3: The reading is out of range. The platform opens a corrective action against it. → **The reading is kept, not refused.** Deleting a bad reading is the one thing an inspector looks for, and an operation that rejects it teaches a kitchen to stop taking readings.
- Flow F28 *A temperature excursion is caught and signed off*, step 4: They act — discard, rework, quarantine — and record what they did. → `open` becomes `actioned`. **Not signed yet, and this is the state most findings sit in.**
- Flow F28 *A temperature excursion is caught and signed off*, step 5: They put their name to it. → `actioned` becomes `signed`. **The signature is the record** — *discarded and reset* with nobody against it is not a corrective action.
- Flow F28 branch at step 3 (high): when The severity is critical and the person who found it is the person on shift., **Escalated rather than signed.** A supervisor signs what a cook should not, and the refusal is in the state model rather than in a policy document — `signCorrectiveAction` returns 409 with the …
- Flow F28 branch at step 2 (medium): when The check was not taken at all., Recorded as `notTaken`. **A check that did not happen is itself a finding** — the alternative is a gap, and a gap and a clean log look identical to an inspector.
- Flow F28 branch at step 1 (medium): when A delivery arrives warm rather than a scheduled check falling due., Enters at `EMP-065` through `logColdChain` instead. **The reading is taken before the receipt is posted** — once stock is received it has entered the kitchen, and a claim against a supplier needs the …
- Flow F28 branch at step 5 (low): when The device is offline when they try to sign., **The action stays `actioned` and the signature waits.** Everything else in this flow queues offline; a signature does not, because one applied against a stale finding is a signature on the wrong …

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-067?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record waste, Create stock movement, Log temperature, Sign corrective action, Confirm.
- [ ] Every transition is wired: `BO-044`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW`, `ORDER_MODIFY`, `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-068` Reservation, Allocation & Omnichannel Inventory

**Reservation, Allocation & Omnichannel Inventory — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 2 · needs the `inventory` module |
| Block | Block C · task APP-STAFF-EMP-068 |
| Who uses it | venue staff holding `ORDER_CREATE`, `PRODUCT_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getStockPositions` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (session), `reservationId` (navigation) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/reservation-allocation-omnichannel-inventory` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `Retail Board 4.dc.html` frame `ret-4h`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Reservation, Allocation &amp; Omnichannel Inventory* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-011): No read lists merchandise reservations (holds) for an outlet.

**From the Food, Beverage & Retail process.** Reservation & allocation on the handheld: hold stock for a guest to collect later today (or for a VIP), and see what is held against what is free. The one thing to get right is the hold length. A merchandise reservation runs from at least 15 minutes to no later than the end of the visit day, which is the default.

**Known correction pending (do not draw the wrong version)**

- **Allocation per sales channel ("50 units online, 50 on-site, each selling independently") is not modelled. The screen binds only the guest collection hold and stock positions.** Why: The agreed decision has no operation or field (stock reservations have no channel; the reservation source types are work order, rental, order, transfer, other). *(source: DI-364 / contracts/satellite/inventory.yaml#/components/schemas/StockReservationSourceType; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): There is no list, cancel or collect of reservations on the screen, although those operations exist. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a merchandise collection hold the same thing as an inventory stock reservation (and so counted in Allocated)?** → Drawn default accepted: Yes, it reduces Available. *(decided by Chinmay, 2026-10-02; DEC-301 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search reservation, allocation | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |

**Form: Reserve merchandise** (modal, opened by *Reserve merchandise*; *Reserve merchandise* calls `reserveMerchandise`, *Cancel* sends nothing)

**Collects what `reserveMerchandise` sends before it is called.** Required: `id`, `lines`, `expiresAt`. Optional: `subjectId`, `collectionNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `reserveMerchandise` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `reserveMerchandise` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `reserveMerchandise` body |
| Merchandise `lines[].merchandiseId` | picker: choose a merchandise | required | — | — | shows names, sends the id | — | `reserveMerchandise` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `reserveMerchandise` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | At least 15 minutes from now and no later than the close of the venue's operating day (audit R215). | `reserveMerchandise` body |
| Collection note `collectionNote` | text field | optional | — | max length 200 | — | — | `reserveMerchandise` body |

Errors to draw in the form: 400 `expiresAt` is less than 15 minutes ahead, or later than the end of the visit day (audit R215).; 409 Insufficient stock. `refusedReason` is `insufficientStock`, and `lines` names the lines short. (StockConflictProblem)

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Hold until**: Default end of today's operating day. Earliest 15 minutes from now. Shown as a time, e.g. "until 22:00 today". *(source: R169 / R215 / contracts/satellite/retail.yaml#reserveMerchandise)*
- **Guest**: Optional guest search (name or mobile). A collection note up to 200 characters. *(source: contracts/satellite/retail.yaml#reserveMerchandise)*

#### Outputs: what the screen shows and produces

**Shown**

**The stock position** (detail panel, from `getStockPositions`)

| Shows | Format | Notes |
|---|---|---|
| Item name | text | — |
| Location name | text | — |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Last counted at | 1 Oct 2026, 14:30 | — |
| Last movement at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Reserve merchandise (primary button) | `reserveMerchandise` POST `/outlets/{outletId}/reserve` | inline | MerchandiseReservation | 400 `expiresAt` is less than 15 minutes ahead, or later than the end of the visit day (audit R215).; 409 Insufficient stock. `refusedReason` is `insufficientStock`, and `lines` names the lines short. … | opens modal first |
| Collected (secondary button) | `collectMerchandiseReservation` POST `/merchandise-reservations/{reservationId}/collect` | — | inline | — | — |
| Release hold (secondary button) | `cancelMerchandiseReservation` POST `/merchandise-reservations/{reservationId}/cancel` | — | inline | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Held stock**: Reservation number, guest, items, held until, status (Reserved, Collected, Expired, Cancelled). A held item is never handed over unpaid. *(source: R236 / contracts/satellite/retail.yaml#reserveMerchandise)*

**Data it reads**: `getStockPositions` (onLoad, Stock on hand by item and location)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation allocation omnichannel, read by `getStockPositions`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation allocation omnichannel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation allocation omnichannel yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `reserveMerchandise`, `collectMerchandiseReservation`, `cancelMerchandiseReservation`. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `expiresAt` is less than 15 minutes ahead, or later than the end of the visit day (audit R215).; 409 Insufficient stock. `refusedReason` is `insufficientStock`, and `lines` names the lines short. (StockConflictProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- reservation: RSV-MBR-002118
  guest: Fatima Al Suwaidi
  items:
  - Aqua Park logo T-shirt, green, M ×2
  holdUntil: 22:00 today
  status: Reserved
```

#### Permissions

- `getStockPositions` → `PRODUCT_VIEW` (read) · staff
- `reserveMerchandise` → `ORDER_CREATE` (operate) · staff, guest
- `collectMerchandiseReservation` → `ORDER_CREATE` (operate) · staff
- `cancelMerchandiseReservation` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `reserveMerchandise`, `collectMerchandiseReservation`, `cancelMerchandiseReservation`.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: stock can be reserved/held (e.g. for a VIP customer) and allocated per sales channel (e.g. 50 units online, 50 on-site), each channel selling independently against its allocation. *(agreed · MoM 19 Aug 2026, 4.5 Inventory Management; 5. Key Decisions · DI-364)*

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-068` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Client design-board frames: `Retail Board 4.dc.html#ret-4h`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-068?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Reserve merchandise, Collected, Release hold.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_CREATE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-069` Barcode, RFID, Serialized Stock & Traceability

**Barcode, RFID, Serialized Stock & Traceability — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 2 · needs the `inventory` module |
| Block | Block D · task APP-STAFF-EMP-069 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listSerialisedItems` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/barcode-rfid-serialized-stock-traceability` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `Retail Board 4.dc.html` frame `ret-4j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Barcode, RFID, Serialized Stock &amp; Traceability* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Food, Beverage & Retail process.** Barcode, serial and traceability on the handheld: scan a barcode for price and stock, or a serial to find exactly one item (a watch at the jewellery counter, a camera returned under warranty). The one thing to get right is serial-first search.

**Known correction pending (do not draw the wrong version)**

- **RFID is in the title. No RFID operation or device exists.** Why: Bulk RFID stock-taking is an open item with the client, and the reader (Kaptur) is still on the hardware list. *(source: DI-365 / TRACKER 30-Sep/Tracker row 28; Food, Beverage & Retail)*
- **The serial and status filters are text fields, and the table is "Every serialised".** Why: Plumbing on a handheld. Use scan, then status chips. *(source: screens/P06-staff-app.yaml#EMP-069; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Serial | text field | optional | — | — | — | Sends `?serial=` to `listSerialisedItems`. | `listSerialisedItems` ?serial |
| Status | text field | optional | — | — | — | Sends `?status=` to `listSerialisedItems`. | `listSerialisedItems` ?status |
| Search barcode, rfid, serialized stock | search field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every serialised** (data table, from `listSerialisedItems`)

| Shows | Format | Notes |
|---|---|---|
| Serial | text | Unique within the item, not globally. Two manufacturers reuse serial numbers and a global constraint would refuse the second one. |
| Status | chip: In stock, Reserved, Sold, Returned, Damaged, Lost… | — |
| Warranty until | 1 Oct 2026 | — |
| Received at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The selected serialised** (detail panel, from `listSerialisedItems`)

| Shows | Format | Notes |
|---|---|---|
| Serial | text | Unique within the item, not globally. Two manufacturers reuse serial numbers and a global constraint would refuse the second one. |
| Status | chip: In stock, Reserved, Sold, Returned, Damaged, Lost… | — |
| Warranty until | 1 Oct 2026 | — |
| Received at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Lookup merchandise (primary button) | `lookupMerchandise` GET `/merchandise/lookup` | — | PriceCheck | 400 Neither barcode nor SKU supplied, or a caller with no workstation sent no `outletId` (audit R215); 404 No active item with that barcode or SKU at the outlet. An inactive item is not found (audit R215). | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Serial result**: Item, serial, status, location, warranty until, and the sale it was sold on. Several matches when one serial exists on different items. *(source: DI-406 / contracts/satellite/inventory.yaml#listSerialisedItems)*

**Data it reads**: `listSerialisedItems` (onLoad, listSerialisedItems)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The barcode rfid serialized list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the barcode rfid serialized untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No barcode rfid serialized yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on serial, status and the barcode rfid serialized are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listSerialisedItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither barcode nor SKU supplied, or a caller with no workstation sent no `outletId` (audit R215) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- scan: SW8K-2026-004417
  item: Smartwatch kids GPS, pink
  status: Sold
  warrantyUntil: '2027-10-12'
  soldOn: Sale MBR-20931
```

#### Permissions

- `listSerialisedItems` → `PRODUCT_VIEW` (read) · staff
- `lookupMerchandise` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listSerialisedItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Barcode, RFID, serialised stock and traceability: serialisation down to the individual item (e.g. a jewellery counter or high-value electronics). *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - Retail Board 4 Page 9 · DI-406)*
- **Open question.** Allam: support bulk stock-taking with handheld RFID scanners — scanning a batch of tagged items updates system quantities once verified and saved. Chinmay's focus is reconciling existing stock vs. newly scanned data. Device specs pending. *(open · MoM 19 Aug 2026, 4.6 RFID/Barcode-Based Bulk Stock Counting — Open Item · DI-365)*

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-069` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 4.dc.html`
- Client design-board frames: `Retail Board 4.dc.html#ret-4j`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-069?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Lookup merchandise.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-070` Inventory Exceptions, AI Replenishment & Action Center

**Inventory Exceptions, AI Replenishment & Action Center — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Stock on the Floor · wave 2 · needs the `analytics` module |
| Block | Block D · task APP-STAFF-EMP-070 |
| Who uses it | venue staff holding `PROCUREMENT_REQUEST`, `REPORT_VIEW_VENUE` (2 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAlerts` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Not available offline.** `listAlerts` reads the analytical replica (ADR-0016). **Corrected 24 August** — the shared "works from cache and queues what it records" wording was applied to a screen whose only operation is an analytical read. |
| Opens with | `venueId` (session), `alertId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/inventory-exceptions-ai-replenishment-action-cen` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `Inventory Board 1.dc.html` frame `inv-10` (*Inventory Exceptions, Data Quality & AI*). **Inventory Board 1 is the only one of the seven that maps onto screens this package has** — item master, categories, UoM, locations, statuses, movement history. Boards 2 to 7 draw a warehouse and procurement suite the contracts do not contain.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Inventory alerts a floor lead must act on (low stock, expiring, count variance): acknowledge it and, where stock is low, raise a requisition from the alert in two taps.

**Known correction pending (do not draw the wrong version)**

- **Filters are free-text "Workstation id", "Shift id" and "Item id"; no operation supplies the "AI replenishment" the name promises.** Why: Spec leak, and an AI label with nothing behind it. *(source: screens/P06-staff-app.yaml#EMP-070; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | radio group | optional | — | Raised · Acknowledged · Resolved · Expired | — | Sends `?status=` to `listAlerts`. | `listAlerts` ?status |
| Severity | segmented control | optional | — | Info · Warning · Critical | — | Sends `?severity=` to `listAlerts`. | `listAlerts` ?severity |
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listAlerts`. | `listAlerts` ?workstationId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listAlerts`. | `listAlerts` ?shiftId |
| Item id | picker: choose an item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?itemId=` to `listAlerts`. | `listAlerts` ?itemId |
| Search inventory exceptions, ai replenishment | search field | — | — | — | — | — | — |

**Form: Acknowledge alert** (modal, opened by *Acknowledge alert*; *Acknowledge alert* calls `acknowledgeAlert`, *Cancel* sends nothing)

**Collects what `acknowledgeAlert` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 300 | — | Stored as `Alert.acknowledgementNote`. | `acknowledgeAlert` body |

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

#### Outputs: what the screen shows and produces

**Shown**

**Every alert** (data table, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Acknowledged at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The selected alert** (detail panel, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Observed value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Acknowledged at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Acknowledge alert (primary button) | `acknowledgeAlert` POST `/alerts/{alertId}/acknowledge` | inline | Alert | — | opens modal first |
| Create requisition (secondary button) | `createRequisition` POST `/requisitions` | CreateRequisitionRequest | Requisition | 400 Validation failed | works offline; opens modal first |

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Create requisition**: Prefilled from the alert (item, location, suggested quantity to par, required by); confirmation shows the requisition number. *(source: contracts/satellite/inventory.yaml#createRequisition / MATRIX 17.6.5)*

**Data it reads**: `listAlerts` (onLoad, What is currently raised)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory exceptions replenishment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory exceptions replenishment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory exceptions replenishment yet. Offers Create requisition (`createRequisition`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, severity, workstationId, shiftId, itemId and the inventory exceptions replenishment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listAlerts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_REQUEST` for `createRequisition`. |
| Offline (`?state=offline`) | **Not available offline.** `listAlerts` reads the analytical replica (ADR-0016). **Corrected 24 August** — the shared "works from cache and queues what it records" wording was applied to a screen whose only operation is an analytical read. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `P16 ANL-018 Alerts & Exception Center`: Same alert record and acknowledgement.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Low stock · Aquaventure beach towel · Splash Shop · 8 left, par 40 · requisition 60 units by 3 Oct
```

#### Permissions

- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `acknowledgeAlert` → `REPORT_VIEW_VENUE` (operate) · staff
- `createRequisition` → `PROCUREMENT_REQUEST` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listAlerts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_REQUEST` for `createRequisition`.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.30 | Allow inventory replenishment requests via mobile app. | Bundles and Promotions | CONTRACTED | `createRequisition` |
| 4.6.32 | Perform inventory counts through mobile devices. | Bundles and Promotions | CONTRACTED | `createRequisition` |
| 15.3.4 | Purchase Requests - System shall support purchase requests. | Inventory Management | CONTRACTED | `createRequisition` |
| 15.3.5 | Purchase Requisitions - System shall support purchase requisitions. | Inventory Management | CONTRACTED | `createRequisition` |
| 15.3.6 | Purchase Approval Workflows - System shall support procurement approvals. | Inventory Management | CONTRACTED | `createRequisition` |
| 17.6.5 | Procurement Request Generation - System shall generate procurement requests from maintenance requirements. | Maintenance & Safety Management | CONTRACTED | `createRequisition` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Stock on the Floor, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-070` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Inventory Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Inventory Board 1.dc.html`
- Client design-board frames: `Inventory Board 1.dc.html#inv-10`
- ADR-0016 *— Read and write paths are separated, and routing is declared per operation* (`docs/adr/0016-read-write-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Acknowledge alert, Create requisition.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PROCUREMENT_REQUEST`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

### In P06 · Stock on the Floor

- Decision: do NOT implement every granular warehouse status (put-away, picking, packing, dispatching, etc.); keep day-to-day workflows simple and fast for end users. This principle guides UI/UX and workflow design across inventory and warehouse operations. *(agreed · MoM 18 Aug 2026, 4.12 Simplification Principle — Guiding Decision · DI-346)*

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acknowledgeAlert": {"method":"POST","path":"/alerts/{alertId}/acknowledge","contract":"reporting","summary":"Mark it seen","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Alert"},
"cancelMerchandiseReservation": {"method":"POST","path":"/merchandise-reservations/{reservationId}/cancel","contract":"retail","summary":"Release a reservation","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"collectMerchandiseReservation": {"method":"POST","path":"/merchandise-reservations/{reservationId}/collect","contract":"retail","summary":"The guest picked it up","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createGoodsReceipt": {"method":"POST","path":"/goods-receipts","contract":"inventory","summary":"Receive goods against a purchase order","permission":"PROCUREMENT_RECEIVE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGoodsReceiptRequest","responds":"GoodsReceipt"},
"createRequisition": {"method":"POST","path":"/requisitions","contract":"inventory","summary":"Raise a requisition","permission":"PROCUREMENT_REQUEST","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRequisitionRequest","responds":"Requisition"},
"createStockMovement": {"method":"POST","path":"/stock-movements","contract":"inventory","summary":"Record an issue, return or adjustment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateStockMovementRequest","responds":"StockMovement"},
"createStockTransfer": {"method":"POST","path":"/stock-transfers","contract":"inventory","summary":"Send stock to another location","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateStockTransferRequest","responds":"StockTransfer"},
"enterCountLine": {"method":"POST","path":"/fnb-stock-counts/{countId}/lines","contract":"fnb","summary":"What was actually on the shelf","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getHaccpStatus": {"method":"GET","path":"/food-safety/status","contract":"fnb","summary":"Where this venue stands, right now","permission":"INCIDENT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getOutletStock": {"method":"GET","path":"/outlets/{outletId}/stock-check","contract":"retail","summary":"Stock across an outlet","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"categoryId","in":"query","required":null},{"name":"lowStockFirst","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getStockPositions": {"method":"GET","path":"/stock","contract":"inventory","summary":"Stock on hand by item and location","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locationId","in":"query","required":null},{"name":"itemId","in":"query","required":null},{"name":"includeZero","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getStockTransfer": {"method":"GET","path":"/stock-transfers/{transferId}","contract":"inventory","summary":"One transfer, its manifest and where it is","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"StockTransfer"},
"getSuggestedRequisitions": {"method":"GET","path":"/requisitions/suggested","contract":"inventory","summary":"Draft requisitions from reorder points","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locationId","in":"query","required":null}],"requestBody":null,"responds":null},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listPurchaseOrders": {"method":"GET","path":"/purchase-orders","contract":"inventory","summary":"List purchase orders","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"supplierId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRequisitions": {"method":"GET","path":"/requisitions","contract":"inventory","summary":"List requisitions","permission":"PROCUREMENT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"raisedByPrincipalId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSerialisedItems": {"method":"GET","path":"/serialised-items","contract":"inventory","summary":"Where each individual item is","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"serial","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockCounts": {"method":"GET","path":"/stock-counts","contract":"inventory","summary":"List stock counts","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockLocations": {"method":"GET","path":"/stock-locations","contract":"inventory","summary":"List stock locations","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockMovements": {"method":"GET","path":"/stock-movements","contract":"inventory","summary":"The movement ledger","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"itemId","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockTransfers": {"method":"GET","path":"/stock-transfers","contract":"inventory","summary":"List transfers","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"logColdChain": {"method":"POST","path":"/food-safety/cold-chain","contract":"fnb","summary":"The temperature a delivery arrived at, and what was decided","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ColdChainEvent","responds":"ColdChainEvent"},
"logTemperature": {"method":"POST","path":"/food-safety/temperature-logs","contract":"fnb","summary":"Record a temperature check, in range or not","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TemperatureLog","responds":null},
"lookupMerchandise": {"method":"GET","path":"/merchandise/lookup","contract":"retail","summary":"Price and stock check by barcode","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"barcode","in":"query","required":null},{"name":"sku","in":"query","required":null},{"name":"includeSiblingOutlets","in":"query","required":null},{"name":"outletId","in":"query","required":null}],"requestBody":null,"responds":"PriceCheck"},
"receiveStockTransfer": {"method":"POST","path":"/stock-transfers/{transferId}/receive","contract":"inventory","summary":"Receive a transfer","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StockTransfer"},
"recordWaste": {"method":"POST","path":"/outlets/{outletId}/waste","contract":"fnb","summary":"Record waste","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rejectReceivedGoods": {"method":"POST","path":"/goods-receipts/{receiptId}/reject","contract":"inventory","summary":"Reject received goods","permission":"PROCUREMENT_RECEIVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GoodsReceipt"},
"reserveMerchandise": {"method":"POST","path":"/outlets/{outletId}/reserve","contract":"retail","summary":"Reserve an item for collection","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MerchandiseReservation"},
"setDailyCount": {"method":"PUT","path":"/stock-counts/daily","contract":"inventory","summary":"Which items get counted every day","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"signCorrectiveAction": {"method":"POST","path":"/food-safety/corrective-actions/{actionId}/sign","contract":"fnb","summary":"Say what was done, and put a name to it","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CorrectiveAction"},
"startStockCount": {"method":"POST","path":"/stock-counts","contract":"inventory","summary":"Start a stock count","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StartStockCountRequest","responds":"StockCount"},
"updateRequisitionLines": {"method":"PUT","path":"/requisitions/{requisitionId}/lines","contract":"inventory","summary":"Change what an outlet is asking for, before it is approved","permission":"PROCUREMENT_REQUEST","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Requisition"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"ColdChainEvent": {"type":"object","x-ticvai-persistence":"fnb.cold_chain_event","description":"Board 5G. **A delivery arriving warm is a rejection decision made at the door**, and the package had `createGoodsReceipt` with nowhere to record the temperature it arrived at.\n**The reading is taken before the receipt is posted**, not after — once stock is received it has entered the kitchen, and a claim against a supplier needs the reading that refused it.\n","required":["id","recordedAt","valueCelsius","decision"],"properties":{"id":{"type":"string","format":"uuid"},"goodsReceiptId":{"type":"string","format":"uuid","nullable":true},"transferId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"valueCelsius":{"type":"number"},"thresholdCelsius":{"type":"number"},"decision":{"type":"string","enum":["accepted","acceptedWithNote","partiallyRejected","rejected"]},"correctiveActionId":{"type":"string","format":"uuid","nullable":true},"supplierClaimRaised":{"type":"boolean","default":false}}},
"CorrectiveAction": {"type":"object","x-ticvai-persistence":"fnb.corrective_action","description":"What was done about a finding, and who signed it. **Opened automatically by an out-of-range reading or a cold-chain breach**, because an action that depends on somebody remembering to raise it is an action that is not raised.\n**Signed by a named principal, and the signature is the record.** *Discarded and reset* with nobody against it is not a corrective action.\n","required":["id","raisedAt","source","status"],"properties":{"id":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"},"raisedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who raised it, which is who may not sign it when it is critical** (`signCorrectiveAction`). Null where the action was opened automatically by a reading or a cold-chain breach."},"source":{"type":"string","enum":["temperatureExcursion","coldChainBreach","expiredStock","contamination","pestSighting","equipmentFailure","missedCheck","manual"],"description":"`missedCheck` is raised by the server when a checkpoint goes past its `checkFrequencyMinutes` with no reading (audit R125 (5))."},"sourceRef":{"type":"string","format":"uuid","nullable":true},"severity":{"type":"string","enum":["observation","minor","major","critical"],"description":"**Set by the source when the platform opens it** (decided 28 September, audit R125 (5)): an out-of-range reading or a cold-chain breach opens at `major`, a missed check at `minor`. `critical` is a person's escalation, not a default."},"actionTaken":{"type":"string","nullable":true},"disposal":{"type":"string","enum":["none","discarded","reworked","quarantined","returned"],"nullable":true},"status":{"type":"string","enum":["open","actioned","signed","escalated","closed"]},"signedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"signedAt":{"type":"string","format":"date-time","nullable":true},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**A critical finding a shift cannot close.** Escalation exists so a supervisor signs what a cook should not. Always the venue's food-safety lead at the time of escalation (`fnb.foodSafetyLeadPrincipalId`, audit R096 (9)).\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"CountStatus": {"type":"string","enum":["open","counting","closed","variancePending","posted","cancelled"]},
"CreateGoodsReceiptRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","purchaseOrderId","locationId","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"purchaseOrderId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"deliveryNoteReference":{"type":"string","maxLength":128},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","receivedQuantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"receivedQuantity":{"type":"number","minimum":0},"unit":{"type":"string"},"batchNumber":{"type":"string","maxLength":64},"expiryDate":{"type":"string","format":"date","description":"Required for perishable items."},"note":{"type":"string","maxLength":200}}}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateRequisitionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","venueId","lines","requiredBy"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid"},"costCenterId":{"type":"string","format":"uuid"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"},"note":{"type":"string","maxLength":200}}}},"requiredBy":{"type":"string","format":"date"},"justification":{"type":"string","maxLength":1000}}},
"CreateStockMovementRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","itemId","locationId","kind","quantity","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MovementKind"},"quantity":{"type":"number","exclusiveMinimum":0,"description":"Always positive. **The `kind` decides whether it adds or removes stock**, not the sign (decided 28 September, audit R171).\n"},"unit":{"type":"string"},"reason":{"type":"string","maxLength":500,"description":"**Required for `adjustmentIn`, `adjustmentOut` and `waste`** (decided 28 September, audit R171); adjustments are reported separately.\n"},"costCenterId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateStockTransferRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","fromLocationId","toLocationId","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"fromLocationId":{"type":"string","format":"uuid"},"toLocationId":{"type":"string","format":"uuid"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"}}}},"note":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"GoodsReceipt": {"x-ticvai-persistence":"inventory.goods_receipt + inventory.goods_receipt_line","type":"object","required":["id","receiptNumber","purchaseOrderId","locationId","lines","receivedByPrincipalId","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"receiptNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152), e.g. `MAR-GR-000431`. Not gapless; only tax invoices are gapless, per legal entity. A receipt recorded offline takes the next number from the range its device holds in reserve.\n"},"purchaseOrderId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"deliveryNoteReference":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string","format":"uuid","readOnly":true,"description":"One batch or expiry line of the receipt. What `rejectReceivedGoods` addresses (decided 28 September, audit R171).\n"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"orderedQuantity":{"type":"number"},"receivedQuantity":{"type":"number"},"rejectedQuantity":{"type":"number"},"batchNumber":{"type":"string","nullable":true},"expiryDate":{"type":"string","format":"date","nullable":true},"unitCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"totalValue":{"x-ticvai-column":"net_value_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"receivedByPrincipalId":{"type":"string","format":"uuid"},"journalEntryId":{"type":"string","nullable":true,"description":"The accrual the supplier invoice will later match against."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"LocationKind": {"type":"string","enum":["mainStore","subStore","kitchen","bar","retailFloor","cellar","transit"]},
"MerchandiseReservation": {"x-ticvai-persistence":"retail.reservation + retail.reservation_line","type":"object","required":["id","outletId","lines","status","expiresAt"],"properties":{"id":{"type":"string"},"reservationNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"lines":{"type":"array","items":{"type":"object","properties":{"merchandiseId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"}}}},"status":{"type":"string","enum":["reserved","collected","expired","cancelled"]},"collectionNote":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date-time"},"collectedAt":{"type":"string","format":"date-time","nullable":true}}},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall","grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings"],"x-ticvai-money-valued":["grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings","inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-extended-2-october":"**Eight finance measures added 2 October 2026** (Chinmay; CHG-FIN-007, CHG-FIN-010), each with the source and formula of the seeded KPI of the same code in `ReportingSystemKpi`: `grossSales`, `discounts`, `refunds`, `netRevenue`, `recognisedRevenue`, `deferredRevenue`, `taxCollected` and `takings`, so an alert rule can watch them (a refund spike, takings below a target). Formulas are the D-185 default; client finance sign-off is pending.","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"MovementKind": {"type":"string","description":"**The kind decides the direction** (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` (the finished item entering stock; the ingredients leave as `issue`). Out: `issue`, `saleDepletion`, `waste`, `adjustmentOut`, `transferOut`, `countLoss`, `supplierReturn`. `adjustment` and `countAdjustment` were split into an in and an out kind so that no kind has two directions.\n","enum":["receipt","issue","saleDepletion","waste","adjustmentIn","adjustmentOut","transferOut","transferIn","countGain","countLoss","supplierReturn","production"]},
"OutletStockLine": {"x-ticvai-persistence":"none — projection over inventory","type":"object","required":["merchandiseId","name","onHand","isBelowReorderPoint"],"properties":{"merchandiseId":{"type":"string","format":"uuid"},"sku":{"type":"string"},"name":{"type":"string"},"categoryName":{"type":"string","nullable":true},"onHand":{"type":"number"},"allocated":{"type":"number","description":"Held by an unexpired collection reservation."},"available":{"type":"number"},"isBelowReorderPoint":{"type":"boolean"},"lastSoldAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceCheck": {"x-ticvai-persistence":"none — computed","type":"object","required":["merchandiseId","name","listPrice","effectivePrice","onHand"],"properties":{"merchandiseId":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid","description":"The outlet whose price and stock this is: the asking workstation's outlet, or `outletId` for a caller with none (decided 28 September, audit R215).\n"},"sku":{"type":"string"},"name":{"type":"string"},"listPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"effectivePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"After any live promotion."},"appliedPromotionCode":{"type":"string","nullable":true},"onHand":{"type":"number"},"isAvailable":{"type":"boolean"},"siblingOutlets":{"type":"array","description":"Stock elsewhere in the venue, so a colleague can be sent.","items":{"type":"object","properties":{"outletId":{"type":"string","format":"uuid"},"outletName":{"type":"string"},"onHand":{"type":"number"}}}}}},
"PurchaseOrder": {"x-ticvai-persistence":"inventory.purchase_order + inventory.purchase_order_line","type":"object","required":["id","purchaseOrderNumber","supplierId","status","lines","total","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"purchaseOrderNumber":{"type":"string","readOnly":true,"description":"**Per venue, in sequence** (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for an order with no venue. Proposed format `PO-<venue code>-<sequence, six digits>`, client to correct.\n"},"requisitionId":{"type":"string","format":"uuid","nullable":true,"description":"Null on a blanket order or an RFQ award, which are raised without one."},"quotationId":{"type":"string","format":"uuid","nullable":true,"description":"The quotation selected when the order was raised (`createPurchaseOrder` requires it). **The link that shows the comparison was made**, which `rfqId` alone does not."},"supplierId":{"type":"string","format":"uuid"},"supplierName":{"type":"string"},"kind":{"type":"string","enum":["standard","blanket","release","rfqAward"],"default":"standard","description":"BL-159. **A blanket order is a price and a commitment, not a delivery.** Releases draw against it, and modelling each release as its own purchase order loses the contract that makes the price valid.\n"},"blanketParentId":{"type":"string","format":"uuid","nullable":true,"description":"The blanket order this release draws against — another purchase order, so the same id type."},"contractPriceValidUntil":{"type":"string","format":"date","nullable":true},"rfqId":{"type":"string","format":"uuid","nullable":true,"description":"Where this order came from a quotation round. **Keeping the link is what lets a venue show it took the best of three**, which is usually the procurement rule rather than a preference.\n"},"supplierInvoiceRef":{"type":"string","nullable":true,"description":"BL-123. **Purchase orders and goods receipts both existed — the third leg did not.** A three-way match with two legs is a two-way match, and it is the supplier invoice that carries the price nobody has checked yet.\n"},"matchStatus":{"type":"string","nullable":true,"enum":["unmatched","matched","priceVariance","quantityVariance","bothVariance"],"description":"**The variance kinds are separated because they have different owners** — a price variance is a buyer's problem and a quantity variance is a receiving one.\n"},"status":{"$ref":"#/components/schemas/PurchaseOrderStatus"},"deliverToLocationId":{"type":"string","format":"uuid","nullable":true,"description":"**Scoped 31 August.** A purchase order is raised by somebody, for somewhere, and carried neither. `requisitionId` reaches a venue through a join, but **a purchase order raised without a requisition — a blanket order, an RFQ award — had no scope at all**, so nothing could answer *whose budget is this* without guessing.\n\n**`deliverToLocationId` is separate from `venueId` on purpose.** A tenant buying centrally and delivering to three venues is one order and three destinations; collapsing them would force one order per venue and lose the volume the tenant negotiated for."},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"orderedQuantity":{"type":"number"},"receivedQuantity":{"type":"number"},"outstandingQuantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"The selected quotation line's price, kept beside `unitPrice` (audit R171)."},"priceOverrideReason":{"type":"string","nullable":true,"description":"Why `unitPrice` differs from `quotedUnitPrice` (audit R171)."},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expectedDelivery":{"type":"string","format":"date"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"supplierReference":{"type":"string","nullable":true,"description":"The supplier's own order reference, from `acknowledgePurchaseOrder`."},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Null is the supplier performance figure** — goods arriving against an order never acknowledged."},"closeShortReason":{"type":"string","nullable":true,"description":"Why the balance was written off, from `closePurchaseOrderShort`."},"cancelReason":{"type":"string","nullable":true,"description":"From `cancelPurchaseOrder`."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The pending approval request raised by `cancelPurchaseOrder` or `closePurchaseOrderShort` (kinds `purchaseOrderCancel`, `purchaseOrderShortClose`; audit R144). Null when none is open."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Which venue is buying. **Null on a tenant-level order** — see `deliverToLocationId`."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Present on every order regardless of whether a venue is named, because a tenant-level order still belongs to a tenant."}}},
"PurchaseOrderStatus": {"type":"string","enum":["raised","sent","acknowledged","partiallyReceived","received","closedShort","cancelled"]},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"Requisition": {"x-ticvai-persistence":"inventory.requisition + inventory.requisition_line","type":"object","required":["id","requisitionNumber","venueId","status","lines","raisedByPrincipalId","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"requisitionNumber":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"costCenterId":{"type":"string","format":"uuid","nullable":true},"justification":{"type":"string","nullable":true},"status":{"$ref":"#/components/schemas/RequisitionStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"requestedQuantity":{"type":"number"},"suggestedQuantity":{"type":"number","nullable":true,"description":"**Kept, never overwritten** (`updateRequisitionLines`). Null on a line nobody suggested.\n"},"approvedQuantity":{"type":"number","nullable":true},"orderedQuantity":{"type":"number","nullable":true},"unit":{"type":"string"},"reason":{"type":"string","nullable":true,"description":"Why the requested quantity differs from the suggestion."},"note":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"estimatedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvalNote":{"type":"string","nullable":true},"requiredBy":{"type":"string","format":"date"},"createdAt":{"type":"string","format":"date-time"},"approvedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true,"description":"From `rejectRequisition`. What the requester reads before copying it into a new draft."},"rejectedAt":{"type":"string","format":"date-time","nullable":true},"returnQuestion":{"type":"string","nullable":true,"description":"From `returnRequisition`. What the requester must answer before resubmitting."},"returnedAt":{"type":"string","format":"date-time","nullable":true},"cancelReason":{"type":"string","nullable":true,"description":"From `cancelRequisition`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true}}},
"RequisitionStatus": {"type":"string","enum":["draft","pendingApproval","approved","rejected","returnedForInfo","ordered","closed","cancelled"]},
"RequisitionSuggestion": {"x-ticvai-persistence":"none — computed","type":"object","required":["itemId","onHand","reorderPoint","suggestedQuantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"onHand":{"type":"number"},"reorderPoint":{"type":"number"},"parLevel":{"type":"number"},"suggestedQuantity":{"type":"number"},"averageDailyConsumption":{"type":"number"},"daysOfCoverRemaining":{"type":"number"},"preferredSupplierId":{"type":"string","format":"uuid","nullable":true},"leadTimeDays":{"type":"integer","nullable":true}}},
"SerialisedItem": {"type":"object","x-ticvai-persistence":"inventory.serialised_item","description":"Retail Board 4 of the client's design set, 20 August. **`StockBatch` was added on 18 August with a lot number, and serialisation to the individual item is a step beyond it.**\nA lot answers *which delivery did this come from*. A serial answers *where is this exact one* — which is what a jewellery counter, a phone, a ticketed collectible or anything with a warranty needs.\n**Most stock is not serialised and should not be.** Turning it on for a 2 AED keyring creates a row per keyring, so it is a per-item decision rather than a policy.\n","required":["id","itemId","serial","status"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"description":"The batch it arrived in, where the item is both lotted and serialised."},"serial":{"type":"string","description":"**Unique within the item, not globally.** Two manufacturers reuse serial numbers and a global constraint would refuse the second one.\n"},"locationId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["inStock","reserved","sold","returned","damaged","lost","inTransit","warranty"]},"soldOnOrderLineId":{"type":"string","format":"uuid","nullable":true,"description":"**The link that makes serialisation worth having.** A warranty claim, a recall and a proof of purchase all start with *which sale was this exact item*.\n"},"warrantyUntil":{"type":"string","format":"date","nullable":true},"receivedAt":{"type":"string","format":"date-time"}}},
"StartStockCountRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","locationId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["full","cycle","spot"]},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"For cycle counts — restrict to these categories."},"isBlind":{"type":"boolean","default":true,"description":"Expected quantities withheld from the counting device. Defaults true because a counter who can see the figure reconciles to it rather than to the shelf. **The expected quantity and the variance stay hidden until the count is submitted** (decided 28 September, audit R110).\n"}}},
"StockCount": {"x-ticvai-persistence":"inventory.count + inventory.count_line","type":"object","required":["id","locationId","kind","status","isBlind","lineCount","countedCount","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"locationName":{"type":"string"},"kind":{"type":"string"},"status":{"$ref":"#/components/schemas/CountStatus"},"isBlind":{"type":"boolean"},"lineCount":{"type":"integer"},"countedCount":{"type":"integer"},"varianceLineCount":{"type":"integer"},"varianceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"startedByPrincipalId":{"type":"string","format":"uuid"},"postedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"journalEntryId":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"postedAt":{"type":"string","format":"date-time","nullable":true},"recountReason":{"type":"string","nullable":true,"description":"Why the count was last sent back by `recountStockCount`."},"recountSignedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor whose step-up sent the count back last (audit R144)."},"cancelReason":{"type":"string","nullable":true,"description":"Why it was abandoned, from `cancelStockCount`."}}},
"StockLocation": {"x-ticvai-persistence":"inventory.location","type":"object","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/LocationKind"},"parentLocationId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"}}},
"StockMovement": {"x-ticvai-persistence":"inventory.movement","allOf":[{"$ref":"#/components/schemas/CreateStockMovementRequest"},{"type":"object","required":["balanceAfter","principalId","createdAt"],"properties":{"balanceAfter":{"type":"number"},"unitCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"x-ticvai-column":"net_cost_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"principalId":{"type":"string","format":"uuid"},"sourceType":{"type":"string","nullable":true,"description":"What generated it — an order, a count, a transfer."},"sourceId":{"type":"string","nullable":true},"journalEntryId":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]},
"StockPosition": {"x-ticvai-persistence":"none — derived from movements","type":"object","required":["itemId","locationId","onHand","unit"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"locationId":{"type":"string","format":"uuid"},"locationName":{"type":"string"},"onHand":{"type":"number"},"allocated":{"type":"number","description":"**Reserved for orders**: the quantity under an active stock reservation for an order (decided 28 September, audit R171). A transfer is not allocation: dispatched stock has already left on-hand and sits in transit.\n"},"available":{"type":"number","description":"**On-hand minus allocated** (decided 28 September, audit R171). What can still be sold or issued.\n"},"unit":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lastCountedAt":{"type":"string","format":"date-time","nullable":true},"lastMovementAt":{"type":"string","format":"date-time","nullable":true}}},
"StockTransfer": {"x-ticvai-persistence":"inventory.transfer + inventory.transfer_line","type":"object","required":["id","fromLocationId","toLocationId","status","lines","dispatchedAt"],"properties":{"id":{"type":"string","format":"uuid"},"transferNumber":{"type":"string"},"fromLocationId":{"type":"string","format":"uuid"},"toLocationId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/TransferStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"dispatchedQuantity":{"type":"number"},"receivedQuantity":{"type":"number","nullable":true},"discrepancy":{"type":"number","nullable":true},"discrepancyReason":{"type":"string","nullable":true}}}},"dispatchedByPrincipalId":{"type":"string","format":"uuid"},"receivedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"dispatchedAt":{"type":"string","format":"date-time"},"receivedAt":{"type":"string","format":"date-time","nullable":true},"closeShortReason":{"type":"string","nullable":true,"description":"Why the balance was written off, from `closeTransferShort`."},"closeShortSignedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor whose step-up closed the transfer short (audit R144)."},"fromVenueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue of `fromLocationId`. Set by the server (audit R183)."},"toVenueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue of `toLocationId`. Set by the server (audit R183)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). `fromLocationId` and `toLocationId` give the endpoints; **this gives the owner**, the source venue's scope.\n\n**Both venues see a transfer between them** (decided 28 September, audit R183). It used to sit at the tenant above both, where neither venue could see it. The row is owned at the source venue and `toScopePath` admits the destination venue too."},"toScopePath":{"type":"string","readOnly":true,"description":"The destination venue's scope. Row-level security admits a caller whose scope matches `scopePath` or `toScopePath`, so both venues read the transfer (decided 28 September, audit R183).\n"}}},
"TemperatureLog": {"type":"object","x-ticvai-persistence":"fnb.temperature_log","description":"Board 5J of the client F&B pack, 20 August. **HACCP records are a UAE regulatory obligation, they are inspected, and nothing in 947 operations touched them** — a venue that cannot produce a temperature log has a compliance failure rather than a missing screen.\n**A reading out of range is not an error, it is a finding.** The log records it, opens a corrective action, and keeps the reading — **deleting a bad reading is the one thing an inspector looks for.**\n**Offline-capable and it must be.** A walk-in freezer is where the signal is worst and the readings matter most.\n","required":["id","checkPointId","recordedAt","valueCelsius","outcome"],"properties":{"id":{"type":"string","format":"uuid"},"checkPointId":{"type":"string","format":"uuid","description":"The unit, station or delivery being read."},"checkPointKind":{"type":"string","enum":["fridge","freezer","holdingCabinet","blastChiller","coreProbe","delivery","displayCounter","ambient"]},"recordedAt":{"type":"string","format":"date-time"},"recordedByPrincipalId":{"type":"string","format":"uuid"},"valueCelsius":{"type":"number"},"minCelsius":{"type":"number","nullable":true},"maxCelsius":{"type":"number","nullable":true},"outcome":{"type":"string","enum":["inRange","outOfRange","notTaken"],"description":"**`notTaken` is a record, not an absence.** A check that did not happen is itself a finding, and a log with a gap cannot be told apart from a log nobody kept.\n"},"deviceReported":{"type":"boolean","default":false,"description":"**A probe reading and a person's reading are different evidence.** An inspector treats them differently and so should the record.\n"},"correctiveActionId":{"type":"string","format":"uuid","nullable":true}}},
"TransferStatus": {"type":"string","enum":["dispatched","inTransit","received","partiallyReceived","cancelled"]}
}
```
