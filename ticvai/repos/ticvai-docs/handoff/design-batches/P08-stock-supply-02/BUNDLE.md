# P08-stock-supply-02 — P08 · Stock & Supply (2 of 2)

**6 screens · 20 operations · 29 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `AI_USE, INCIDENT_VIEW, ORDER_MODIFY, PROCUREMENT_REQUEST, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-105` | Stock & Supply | A | 17 | 6 | 6 | 18 | 1 | 4 | — | notStarted (generated) |
| `BO-137` | Recipe Consumption & Theoretical Inventory | C | 3 | 27 | 6 | 10 | 1 | 6 | — | notStarted (generated) |
| `BO-138` | Production Execution & Batch Management | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-139` | Wastage, Spoilage, Returns & Write-Off | C | 21 | 6 | 5 | 15 | 1 | 0 | — | notStarted (generated) |
| `BO-140` | Product Availability, 86 & Operational Food Safety | C | 8 | 51 | 6 | 4 | 0 | 0 | — | notStarted (generated) |
| `BO-141` | Operational Alerts, AI Replenishment & Action Center | D | 18 | 18 | 6 | 6 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-138 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-105` Stock & Supply

**Everything in stock & supply.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 1 · needs the `core` module |
| Block | Block A · ticket #29005 (VM-BO-105) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listInventoryItems` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/stock-supply` |

**What the spec says about it.** Section landing. **9 screens reach the entry point through here** — before 20 August they reached it through nothing.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): The hub bound an inventory-item table, a purchase-order table and a venue-settings panel, duplicating BO-081 and BO-051; a hub's operations are the KPI read plus … Removed 2 October 2026 (CHG-WIR-008): The hub bound an inventory-item table, a purchase-order table and a venue-settings panel, duplicating BO-081 and BO-051; a hub's operations are the KPI read plus … Removed 2 October 2026 (CHG-WIR-008): The hub bound an inventory-item table, a purchase-order table and a venue-settings panel, duplicating BO-081 and BO-051; a hub's operations are the KPI read plus …

**From the Food, Beverage & Retail process.** The Stock & Supply landing page in Venue Management. It is a hub: one card per stock and procurement screen, the two seeded KPI tiles, and nothing else. The one thing to get right is that it stays a launcher. It must not become a second item list and a second purchase-order list, which is what the generated definition shows.

**Fixed on main** (the package already carries these; draw what it says): The hub binds an inventory-item table, a purchase-order table and a venue-settings detail panel (biometrics, quiet hours, segregated … (CHG-WIR-008); The hub declares getVenueSettings for "What is enabled here". The contract says it carries no module enablement and no retail setting. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search stock & supply | search field | — | — | — | — | — | — |

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

#### Outputs: what the screen shows and produces

**Shown**

**Takings and admissions today** (metric tile, from `getKpiValues`): **Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Card list** (card list): 9 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create inventory item (primary button) | `createInventoryItem` POST `/inventory-items` | CreateInventoryItemRequest | InventoryItem | 400 Validation failed; 409 SKU already in use in this venue | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **KPI tiles**: Two tiles only, "Takings today" and "Admissions today", read for today in the venue's time zone. Show no attention counts on the cards (for example "3 requisitions waiting") until a summary operation exists. *(source: R283 / contracts/satellite/reporting.yaml#getKpiValues)*
- **Screen cards**: Cards in the order a storekeeper works: Stock Levels, Inventory Items, Stock Count, Stock Movements, Requisitions, Purchase Orders, Goods Receipt, Stock Transfers, Suppliers, then the F&B stock screens (Recipe Consumption, Production, Wastage, Product Availability & 86, Alerts). Each card has a one-line plain purpose. A card whose module is not licensed for the tenant is not shown. The journey gets shorter; it does not look broken. *(source: F76 step 1 / F92 step 1 / DI-342)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Add inventory item**: A shortcut that opens the same create form as Inventory Items (BO-081). Not a separate form. *(source: contracts/satellite/inventory.yaml#createInventoryItem)*

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …)

**Where the user goes next**

- → `BO-049` Stock Levels: *Stock Levels*; carries `itemId`
- → `BO-052` Goods Receipt: *Goods Receipt*
- → `BO-078` Requisitions: *Requisitions*
- → `BO-079` Stock Count: *Stock Count*
- → `BO-080` Stock Transfers: *Stock Transfers*
- → `BO-081` Inventory Items: *Inventory Items*; carries `itemId`
- → `BO-083` Suppliers: *Suppliers*
- → `BO-137` Recipe Consumption & Theoretical Inventory: *Recipe Consumption & Theoretical Inventory*
- → `BO-138` Production Execution & Batch Management: *Production Execution & Batch Management*
- → `BO-139` Wastage, Spoilage, Returns & Write-Off: *Wastage, Spoilage, Returns & Write-Off*
- → `BO-140` Product Availability, 86 & Operational Food Safety: *Product Availability, 86 & Operational Food Safety*
- → `BO-141` Operational Alerts, AI Replenishment & Action Center: *Operational Alerts, AI Replenishment & Action Center*
- → `BO-051` Purchase Orders: *Purchase Orders*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in stock & supply yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for stock & supply. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 SKU already in use in this venue |

#### Edge cases to draw

- **Principal holds more than one venue**: Ask which venue before the page renders. Never show the first venue by default. *(source: screens/P08-venue-back-office.yaml#BO-105)*
- **No permission for any stock screen**: Say in plain words that this account has no access to Stock & Supply. Do not show an empty grid of cards. *(source: screens/P08-venue-back-office.yaml#BO-105)*

#### Consistency with other screens

- Match `BO-081`: The add-item form is the BO-081 form, field for field.
- Match `BO-102`: Same hub pattern as the Sell landing (two KPI tiles, cards, no attention counts).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aqua Park (AQP)
kpis:
- label: Takings today
  value: AED 184,320.50
  comparison: +6.2% vs yesterday
- label: Admissions today
  value: 7,412
  comparison: -1.8% vs yesterday
cards:
- Stock Levels
- Inventory Items
- Stock Count
- Stock Movements
- Requisitions
- Purchase Orders
- Goods Receipt
- Stock Transfers
- Suppliers
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `createInventoryItem` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** You do not have permission for stock & supply. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.5.35 | FIFO, LIFO, and Weighted Average costing methods. | Bundles and Promotions | CONTRACTED | `createInventoryItem` |
| 7.4.33 | It is expected that the software can sell PLUs considered as simple items which could possibly be inventory managed. | F&B POS | CONTRACTED | `createInventoryItem` |
| 7.4.34 | Food and Beverage PLUs can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `createInventoryItem` |
| 7.4.35 | Retail PLUs can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `createInventoryItem` |
| 7.4.39 | Wristbands can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `createInventoryItem` |
| 10.1.4 | The system should be able to sync all the SKU products and Standalone SKU products from the inventory management and make it available to sell as per availability and pricing strategy. | Games & F&B Integration | CONTRACTED | `createInventoryItem` |
| 15.1.1 | Inventory Item Master - System shall support centralized inventory item management. | Inventory Management | CONTRACTED | `createInventoryItem` |
| 15.1.2 | Item Categories - System shall support inventory item categorization. | Inventory Management | CONTRACTED | `createInventoryItem` |
| 15.1.3 | SKU Management - System shall support SKU management. | Inventory Management | CONTRACTED | `createInventoryItem` |
| 15.1.4 | Barcode Management - System shall support barcode management. | Inventory Management | CONTRACTED | `createInventoryItem` |
| 15.1.5 | Product Attributes - System shall support configurable product attributes. | Inventory Management | CONTRACTED | `createInventoryItem` |
| 15.1.6 | Product Variants - System shall support product variants. | Inventory Management | CONTRACTED | `createInventoryItem` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory & Procurement covers both F&B and Retail: total inventory value, item counts and out-of-stock items, broken down by department/sub-department. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-342)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-105` · status **notStarted** · provenance generated
- Client design-board frames: `Inventory Board 7.dc.html#inv-7a`

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-105?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create inventory item.
- [ ] Every transition is wired: `BO-049`, `BO-052`, `BO-078`, `BO-079`, `BO-080`, `BO-081`, `BO-083`, `BO-137`, `BO-138`, `BO-139`, `BO-140`, `BO-141`, `BO-051`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-137` Recipe Consumption & Theoretical Inventory

**Recipe Consumption & Theoretical Inventory — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `fnb` module |
| Block | Block C · task VM-BO-137 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as storekeeper, supervisor |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRecipes` reads the population and `getCountVariance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `countId` (deepLink), `runId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. A run opened from the list. |
| Route | `/stock-supply/recipe-consumption-theoretical-inventory` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

**From the Food, Beverage & Retail process.** What the recipes say should have been used against what the count found, per outlet and count period (FNB-5C, F30 step 8): theoretical, actual, variance %, its value, and the lines beyond the venue's tolerance. The client asked for recipe-based ingredient consumption in the F&B stock view. The one thing to get right is that the variance is only shown once the count is submitted, never while counting.

**Known correction pending (do not draw the wrong version)**

- **The board frame fnb-2f ("Recipe & BOM Costing") is attached here.** Why: It is BO-110's frame; this screen's frame is fnb-5c. *(source: screens/P08-venue-back-office.yaml#BO-137; Food, Beverage & Retail)*
- **The main population is "Every recipe" (listRecipes) with a "Menu item id" field and raw recipe columns, plus a raw production-run table with ids.** Why: The population is the count's variance lines; recipes are context, not the list. *(source: screens/P08-venue-back-office.yaml#BO-137 / R254; Food, Beverage & Retail)*
- **No read returns theoretical and actual use over a period, or a probable cause per line (FNB-5C); the variance read is per count (on-hand expected against counted).** Why: The frame's period totals and "probable cause" column have no source; draw per-count variance until one exists. *(source: contracts/satellite/inventory.yaml#getCountVariance / screens/P08-venue-back-office.yaml#BO-137; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "probable cause" (re-fires logged, trim yield, breakage) wanted in r1, and from which data?** → Drawn default stands (answer: "No cause column; link to waste and production for the period"): Omit the column; link to waste and production for the same period. *(decided by Chinmay, 2026-10-02; DEC-191 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | text field | optional | — | — | — | Sends `?search=` to `listRecipes`. | `listRecipes` ?search |
| Menu item id | picker: choose a menu item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?menuItemId=` to `listRecipes`. | `listRecipes` ?menuItemId |
| Search recipe consumption | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Planned · In progress · Completed · Cancelled | `listProductionRuns` ?status |
| Location kind | segmented control | — | Outlet · Commissary | `listProductionRuns` ?locationKind |
| From | date picker | — | — | `listProductionRuns` ?from |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet and count**: Outlet picker, then a submitted count (by date, "Count 24 Oct 2026, Oasis Bistro kitchen"); not an id. *(source: contracts/satellite/inventory.yaml#getCountVariance / F30 step 8)*
- **Filter**: All items / Over tolerance; sort by value (default) or by variance %. *(source: screens/P08-venue-back-office.yaml#BO-137)*

#### Outputs: what the screen shows and produces

**Shown**

**Every recipe** (data table, from `listRecipes`)

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Yield | 1,234.5 | Portions produced by one execution. |
| Ingredients | list or chips (count when long) | — |
| Cost per portion | AED 1,234.50 | Computed, never entered (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided … |

**Every production run** (data table, from `listProductionRuns`)

| Shows | Format | Notes |
|---|---|---|
| Planned quantity | 1,234.5 | — |
| Actual quantity | 1,234.5 | BL-126. Theoretical against actual is the whole point of recording this. |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, In progress, Completed, Cancelled | — |
| Variance reason | text | — |

**The selected recipe** (detail panel, from `listRecipes`)

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Yield | 1,234.5 | Portions produced by one execution. |
| Ingredients | list or chips (count when long) | — |
| Cost per portion | AED 1,234.50 | Computed, never entered (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided … |

**The production run** (detail panel, from `getProductionRun`)

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

**The count variance** (detail panel, from `getCountVariance`)

| Shows | Format | Notes |
|---|---|---|
| Count | the name it points at, never the id | — |
| Total variance value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Exception count | 1,234 | Lines beyond `VenueSettings.inventory.countVarianceTolerancePercent` (proposed default 2 per cent, audit R094), requiring review before … |
| Lines | list or chips (count when long) | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Variance table**: Per ingredient - expected, counted, variance % (signed, one decimal), value in AED; lines beyond the tolerance (proposed 2%, venue setting) highlighted and counted in the header. *(source: contracts/satellite/inventory.yaml#getCountVariance / R094)*
- **Production yield**: Runs in the period with planned, made and yield %, since a low batch yield explains part of the gap. *(source: contracts/satellite/fnb.yaml#listProductionRuns / F85 step 2)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Open the item**: Goes to the ingredient's product detail to fix a unit, a recipe line or a cost. *(source: screens/P08-venue-back-office.yaml#BO-137)*

**Data it reads**: `listRecipes` (onLoad, List recipes); `getCountVariance` (onLoad, Variance between counted and expected); `listProductionRuns` (onLoad, What is being made, and what was)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-105` Stock & Supply: *Stock & Supply*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recipe consumption theoretical list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recipe consumption theoretical untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recipe consumption theoretical yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on search, menuItemId and the recipe consumption theoretical are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listRecipes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Count is still open. |

#### Edge cases to draw

- **The count is still open or being counted**: "Variance appears when the count is submitted" - never partial figures (409 from the read). *(source: R110 / contracts/satellite/inventory.yaml#getCountVariance)*
- **A cancelled production run in the period**: Its ingredients count as used; the run shows as cancelled with its consumption. *(source: contracts/satellite/fnb.yaml#planProductionRun)*

#### Consistency with other screens

- Match `BO-079`: The count is entered on Stock Count; this screen only reads its variance.
- Match `BO-110`: Same units as the recipe lines.
- Match `BO-049`: DI-340 scopes both; the F&B stock command centre links here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro kitchen
count: Submitted 25 Oct 2026, 07:40 GST by Daniel Brooks
lines:
- item: Beef Patty 150g
  expected: 1,842 pc
  counted: 1,914 pc
  variance: +3.9%
  value: AED 461.00
- item: Fresh Sea Bass
  expected: 42.6 kg
  counted: 48.2 kg
  variance: +13.1%
  value: AED 728.00
- item: Tomato
  expected: 73.6 kg
  counted: 74.4 kg
  variance: +1.1%
  value: AED 7.00
```

#### Permissions

- `listRecipes` → `PRODUCT_VIEW` (read) · staff
- `getCountVariance` → `PRODUCT_VIEW` (read) · staff
- `listProductionRuns` → `PRODUCT_VIEW` (read) · staff
- `getProductionRun` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listRecipes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.21 | The system should be able to generate discrepancy report generated prior to making an inventory adjustment. | Retail POS | CONTRACTED | `getCountVariance` |
| 4.6.36 | Compare theoretical recipe cost versus actual inventory consumption and wastage, highlighting variances and operational inefficiencies. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.7 | Manage recipe yields, shrinkage, wastage and final portions. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.12 | Plan kitchen production quantities based on expected demand. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.13 | Manage batch preparation and production runs. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.16 | Generate production sheets for kitchen operations. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.17 | Support central kitchen and commissary operations supplying multiple outlets, including production batches, transfers, yields, and planning. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.18 | Generate replenishment requests automatically based on demand forecasts, stock levels, and attendance projections. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.19 | Generate production schedules using reservations, attendance forecasts, event schedules, and inventory availability. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 5.1.10 | Manage kitchen production capacity. | F&B & Guest Management | CONTRACTED | data `ProductionRun` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- F&B Stock Command Center shows stock value, low-stock/critical/out-of-stock items and recipe-based ingredient consumption. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-340)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-137` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 2.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 5.dc.html#fnb-5c`
- Flow F30 *A count is entered, varied and posted*, step 8: The variance feeds theoretical-against-actual. → **Recipes say 400 portions; the count says 380.** The gap is waste, theft or a wrong recipe, and this is the only place a venue finds out which.
- Flow F85 *Production is planned, costed and released*, step 2: Recipe Consumption & Theoretical Inventory. → **Drawn by the client as FNB-2F.** 2 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-137?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-008`, `BO-105`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-138` Production Execution & Batch Management

**Production Execution & Batch Management — from the client design board, 20 August (merged into BO-112 Production Planning & Production Sheets).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listExpiringBatches` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `runId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/stock-supply/production-execution-batch-management` |

**What the spec says about it.** **Merged into BO-112** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). Batch execution is a tab of the one Production screen (design-note correction fnb-retail BO-112). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-112, and nothing on it is built separately. **Added 20 August from the client design board.** The operations existed and no screen called them.

**From the Food, Beverage & Retail process.** Today's production batches being made: planned against made, yield, state, and the components issued (FNB-5D). The client asked for planned versus actual versus yield and batch losses. A batch that under-yields shows here before it shows up as stock variance. The one thing to get right is that yield is derived from made over planned, never typed or stored, and that ingredients left stock when the batch started.

**Known correction pending (do not draw the wrong version)**

- **No board frame; the client's frame FNB-5D ("Production Execution & Batch") is listed on BO-136.** Why: The designer would draw this screen from nothing. *(source: screens/P08-venue-back-office.yaml#BO-138; Food, Beverage & Retail)*
- **The "Plan production run" modal requires id and status and offers actualQuantity, varianceReason and productionPlanId.** Why: Id and status are plumbing, the plan link is read-only, actual and variance belong to completion. *(source: contracts/satellite/fnb.yaml#planProductionRun / R254; Food, Beverage & Retail)*
- **No start or cancel operation for a batch (see BO-113).** Why: "Start" is when ingredients leave stock (R125 (8)) and cannot be drawn honestly. *(source: R125; Food, Beverage & Retail)*
- **Overlap with BO-113 and BO-112 (same plan and complete operations).** Why: One Production screen with tabs (see BO-112). *(source: DI-987; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The population is listExpiringBatches - supplier stock batches with lot numbers and expiry - not production batches; the "Within days" … (CHG-WIR-008).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Kitchen and day**: Kitchen or commissary picker and the day (today by default). *(source: contracts/satellite/fnb.yaml#listProductionRuns)*
- **Complete batch**: Made quantity in the item's unit; a reason when made is below planned (optional in the contract); the time is the device's. *(source: contracts/satellite/fnb.yaml#completeProductionRun / designer default)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Batch list**: Item, planned, made, yield % (one decimal), state - Planned, Running, Complete, Cancelled - with a "Low yield" highlight on a complete batch well below plan; running batches show who started them and when. *(source: contracts/satellite/fnb.yaml#getProductionRun / screens/P08-venue-back-office.yaml#BO-138)*
- **Waste-risk suggestion**: Items at risk with quantity, value and a recommended action (reduce prep, promote, transfer, use in a recipe), with its maturity badge and plain explanation; a person applies it elsewhere. *(source: MATRIX 4.8.15 / MATRIX 4.1.19 / contracts/satellite/ai.yaml#requestSuggestion)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Complete batch**: Moves the made quantity into stock; refused if the batch is not running, with its state named; works offline. *(source: contracts/satellite/fnb.yaml#completeProductionRun)*
- **New batch**: Plans a batch outside the day's plan. *(source: contracts/satellite/fnb.yaml#planProductionRun)*

**Where the user goes next**

- → `BO-105` Stock & Supply: *Stock & Supply*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to BO-112 while it opens. |
| Error (`?state=error`) | Could not open BO-112; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to BO-112, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to BO-112. |
| Permission denied (`?state=emptyNoAccess`) | As BO-112: shown when the caller lacks the access BO-112 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Completed offline**: Shows "Saved on this device, will sync" and replays in order when back online. *(source: contracts/satellite/fnb.yaml#completeProductionRun)*
- **A correction to the made quantity later**: Yield recomputes from the corrected figure (it is never stored). *(source: contracts/satellite/fnb.yaml#getProductionRun)*

#### Consistency with other screens

- Match `BO-113`: Commissary batches are the same list filtered to the commissary.
- Match `BO-139`: Batch losses recorded as waste use the reason Over-production or Preparation error.
- Match `BO-137`: Low yields here explain variance there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kitchen: Central Commissary - Tue 3 Nov 2026
batches:
- batch: BAT-118
  item: Burger Sauce (SUB-0071)
  planned: 12.0 kg
  made: '-'
  state: Running - started 14:20 by Priya Nair
- batch: BAT-116
  item: Beef Patty 150g (ITM-1042)
  planned: 400 pc
  made: 386 pc
  yield: 96.5%
  state: Complete
- batch: BAT-115
  item: Sea Bass Fillets
  planned: 28.0 kg
  made: 16.8 kg
  yield: 60.0%
  state: Complete - low yield
```

#### Permissions

**A refused user sees:** As BO-112: shown when the caller lacks the access BO-112 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Production execution & batch management shows planned vs. actual vs. yield quantity and batch losses; wastage/spoilage must be recorded per item. Outlets raise requisitions to replenish from the central warehouse. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-341)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-138` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-138?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-105`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-139` Wastage, Spoilage, Returns & Write-Off

**Wastage, Spoilage, Returns & Write-Off — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `fnb` module |
| Block | Block C · task VM-BO-139 |
| Who uses it | venue staff holding `AI_USE`, `ORDER_MODIFY`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 operate, 1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`recordWaste`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `outletId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/stock-supply/wastage-spoilage-returns-write-off` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-011): No read lists recorded waste per item, with value and reason.

**From the Food, Beverage & Retail process.** Logging waste where it happens - item, quantity, reason - and seeing what was wasted, where, and what it cost (FNB-5E). Waste depletes stock without a sale and is the ground truth for waste prediction, so the reason code matters more than it looks. The client asked for wastage and spoilage recorded per item. The one thing to get right is a fast entry (item, quantity, reason) that works offline and shows its value at current cost.

**Known correction pending (do not draw the wrong version)**

- **The form shows an "Id" text field and a "Recorded at" date picker.** Why: The id is generated by the device (idempotency) and the time is the device's own; neither is typed. *(source: contracts/satellite/fnb.yaml#recordWaste / R254; Food, Beverage & Retail)*
- **"Lines" is a multi-select.** Why: A waste line is item plus quantity plus unit; a multi-select cannot carry quantities. *(source: contracts/satellite/fnb.yaml#recordWaste; Food, Beverage & Retail)*
- **No read of recorded waste exists, so the screen is a lone form (configEditor) with no list, history or totals.** Why: FNB-5E and DI-341 need the list of waste per item; MATRIX 6.1.38 promises count, value and a split by reason. *(source: screens/P08-venue-back-office.yaml#BO-139 / MATRIX 6.1.38 / DI-341; Food, Beverage & Retail)*
- **The attached frames are Inventory Board 3 inv-3g (Adjustment & Write-Off) and inv-3j (Shrinkage & Accuracy); the F&B frame FNB-5E (Wastage, Spoilage & Write-Off) is mapped to EMP-067.** Why: The inventory frames are adjustments across warehouses; the F&B waste frame is this screen's. *(source: screens/P08-venue-back-office.yaml#BO-139; Food, Beverage & Retail)*
- **The reasons the frames use (Trim, Re-fire, Equipment failure) are not in the reason list, and there is no "Other" with a note.** Why: Staff will pick the nearest wrong reason, which poisons the waste-prediction ground truth the contract warns about. *(source: contracts/satellite/fnb.yaml#recordWaste / screens/P08-venue-back-office.yaml#BO-139 / R222; Food, Beverage & Retail)*
- **The name says "Returns" but the screen records only food waste; retail returns are elsewhere.** Why: Rename to "Wastage, Spoilage & Write-Off" to avoid a cashier looking here for a refund. *(source: R139 / screens/P08-venue-back-office.yaml#BO-139; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does waste above a value need approval (FNB-5E draws AED 100 / 500 / 2,000 bands and photo evidence above AED 500)? R144 lists recounts and retail returns, not waste, and no setting or approval call exists.** → A waste-approval policy the venue can switch on or off; when on, value bands and a photo above a value. *(decided by Chinmay, 2026-10-02; DEC-192 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search wastage, spoilage, returns | search field | — | — | — | — | — | — |
| Id | text field | — | — | — | — | Required. | — |
| Lines | multi select | — | — | — | — | Required. | — |
| Reason | select field | — | — | — | — | Required. | — |
| Recorded at | date picker | — | — | — | — | Required. | — |
| Note | text field | — | — | — | — | — | — |

**Form: Save waste approval policy** (modal, opened by *Save waste approval policy*; *Save waste approval policy* calls `setWasteApprovalPolicy`, *Cancel* sends nothing)

**Collects what `setWasteApprovalPolicy` sends before it is called.** Required: `enabled`. Optional: `bands`, `photoRequiredAbove`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Enabled `enabled` | toggle | required | off | — | — | — | `setWasteApprovalPolicy` body |
| Bands `bands` | repeatable rows | optional | — | — | — | Value bands in ascending `fromValue`; a record's value falls in the last band it reaches. | `setWasteApprovalPolicy` body |
| From value `bands[].fromValue` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setWasteApprovalPolicy` body |
| Requires approval `bands[].requiresApproval` | toggle | required | — | — | — | — | `setWasteApprovalPolicy` body |
| Approver permission `bands[].approverPermission` | text field | optional | — | — | — | The permission an approver in this band holds (a value of the permission vocabulary, e.g. | `setWasteApprovalPolicy` body |
| Photo required above `photoRequiredAbove` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | At or above this value a photo is required (`recordWaste.photoAssetId`). Null means never. | `setWasteApprovalPolicy` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

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

- **Outlet**: Outlet picker (the user's outlet by default); never an id. *(source: contracts/satellite/fnb.yaml#recordWaste)*
- **Lines**: One or more lines, each an item (search by name), quantity and unit; not a multi-select. Value at current cost is shown per line as it is typed. *(source: contracts/satellite/fnb.yaml#recordWaste / DI-341)*
- **Reason**: Spoilage, Preparation error, Customer return, Breakage, Over-production, Expired. One reason per entry; mixed reasons are separate entries. *(source: contracts/satellite/fnb.yaml#recordWaste / MATRIX 4.6.31)*
- **Note**: Optional, up to 500 characters. *(source: contracts/satellite/fnb.yaml#recordWaste)*

#### Outputs: what the screen shows and produces

**Shown**

**Waste approval policy** (detail panel, from `getWasteApprovalPolicy`): **A policy the venue switches on or off (decided 2 October 2026 by Chinmay, DEC-192; CHG-CSA-016):** off by default; when on, value bands decide approval and a photo is required above a value.

| Shows | Format | Notes |
|---|---|---|
| Enabled | yes / no (icon or chip) | — |
| Bands | list or chips (count when long) | Value bands in ascending `fromValue`; a record's value falls in the last band it reaches. |
| From value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Requires approval | yes / no (icon or chip) | — |
| Approver permission | text | The permission an approver in this band holds (a value of the permission vocabulary, e.g. |
| Photo required above | AED 1,234.50 | At or above this value a photo is required (`recordWaste.photoAssetId`). Null means never. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record waste (primary button) | `recordWaste` POST `/outlets/{outletId}/waste` | inline | inline | 422 The waste-approval policy is on and the value needs photo evidence that was not sent (`photo-required`, CHG-CSA-016). | — |
| Save waste approval policy (secondary button) | `setWasteApprovalPolicy` PUT `/waste-approval-policy` | WasteApprovalPolicy | WasteApprovalPolicy | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Recorded**: "Recorded - value AED 1,456.00 at current cost" after save, with the entry added to the list. *(source: contracts/satellite/fnb.yaml#recordWaste)*
- **Waste list**: Date, outlet, item, reason, quantity, value, logged by; filter by reason and period; value by reason as a split. *(source: screens/P08-venue-back-office.yaml#BO-139 / MATRIX 6.1.38)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Record waste**: Depletes stock for each line and records the value; offline it is kept on the device and sent in order. *(source: contracts/satellite/fnb.yaml#recordWaste)*

**Data it reads**: `getWasteApprovalPolicy` (onLoad, The waste-approval policy in force (DEC-192))

**Where the user goes next**

- → `BO-105` Stock & Supply: *Stock & Supply*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved wastage spoilage returns. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wastage spoilage returns untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wastage spoilage returns configured. The form opens empty and `recordWaste` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getWasteApprovalPolicy` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `requestSuggestion`; `ORDER_MODIFY` for `recordWaste`; `PRODUCT_CONFIGURE` for `setWasteApprovalPolicy`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem); 422 The waste-approval policy is on and the value needs photo evidence that was not sent (`photo-required`, CHG-CSA-016). |

#### Edge cases to draw

- **Offline**: Recorded on the device with "Will sync"; the time recorded is when it was logged, not when it synced. *(source: contracts/satellite/fnb.yaml#recordWaste)*
- **A large write-off**: Where the venue has switched its waste-approval policy on, an entry above a value band waits for approval and needs a photo above the photo threshold (FNB-5E: AED 100 / 500 / 2,000); with the policy off, no approval step is drawn. *(source: screens/P08-venue-back-office.yaml#BO-139 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **A retail customer return**: Not here - retail returns go through the till by receipt or order number; "Customer return" here is food sent back. *(source: R139 / contracts/satellite/fnb.yaml#recordWaste)*

#### Consistency with other screens

- Match `EMP-067`: The same waste entry on the staff app (FNB-5E is mapped to EMP-067); same reasons, same fields.
- Match `BO-044`: F&B Outlets also records waste; one entry component.
- Match `BO-138`: Batch losses use Over-production or Preparation error.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entries:
- date: 24 Oct 2026 21:40
  outlet: Oasis Bistro
  item: Fresh Sea Bass
  qty: 11.2 kg
  reason: Preparation error
  value: AED 1,456.00
  by: Priya Nair
- date: 23 Oct 2026 09:15
  outlet: Bite & Go
  item: Brioche Bun
  qty: 104 pc
  reason: Breakage
  value: AED 218.40
  by: Omar Ziad
- date: 22 Oct 2026 16:05
  outlet: Beach Hut kiosk
  item: Milk full fat
  qty: 12 L
  reason: Expired
  value: AED 86.00
  by: Aisha Rahman
```

#### Permissions

- `recordWaste` → `ORDER_MODIFY` (operate) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest
- `getWasteApprovalPolicy` → `PRODUCT_VIEW` (read) · staff
- `setWasteApprovalPolicy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getWasteApprovalPolicy` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `requestSuggestion`; `ORDER_MODIFY` for `recordWaste`; `PRODUCT_CONFIGURE` for `setWasteApprovalPolicy`.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.31 | Allow mobile recording of food waste and spoilage. | Bundles and Promotions | CONTRACTED | `recordWaste` |
| 4.7.2 | The system should be able to allow negative sales for various operational scenarios. | Bundles and Promotions | CONTRACTED | `recordWaste` |
| 4.7.3 | The system should allow manual recording of wastage of F&B products. | Bundles and Promotions | CONTRACTED | `recordWaste` |
| 6.1.38 | The system should be able to report on F&B wastage: 1.Wastage count 2.Value of wastage 3.Normal wastage/abnormal wastage. | Retail POS | CONTRACTED | `recordWaste` |
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.8.15 | AI predicts potential food waste and recommends actions. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 5.4.24 | Segment customers automatically. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.27 | Recommend staffing adjustments, ride allocation, and queue balancing. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.36 | The system shall estimate queue wait times using historical and real-time operational data. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Production execution & batch management shows planned vs. actual vs. yield quantity and batch losses; wastage/spoilage must be recorded per item. Outlets raise requisitions to replenish from the central warehouse. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-341)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-139` · status **notStarted** · provenance generated
- Client design-board frames: `Inventory Board 3.dc.html#inv-3g`, `Inventory Board 3.dc.html#inv-3j`
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 412, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-139?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record waste, Save waste approval policy.
- [ ] Every transition is wired: `BO-105`.
- [ ] Every gated control is gated: `AI_USE`, `ORDER_MODIFY`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 6 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-140` Product Availability, 86 & Operational Food Safety

**Product Availability, 86 & Operational Food Safety — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `fnb` module |
| Block | Block C · task VM-BO-140 |
| Who uses it | venue staff holding `INCIDENT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listExpiringBatches` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `itemId` (deepLink), `menuId` (navigation), `outletId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/stock-supply/product-availability-86-operational-food-safet` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Availability is immediate (decided 28 September, audit R110)** — the 86 toggle calls `setItemAvailability` at once; the Save changes step is gone. Reason Other needs a note (audit R222).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): The population was listExpiringBatches (stock batches), so the Available toggle had no menu item to bind; the list is the outlet's menu items with availability …

**From the Food, Beverage & Retail process.** What is sellable right now at an outlet, and the kitchen's food-safety state beside it (FNB-5J, FNB-2H). Staff switch a dish off (86) with a reason and an optional automatic return time, and on again; the change is live on every till and guest menu of the outlet the moment it returns - there is no Save step. The HACCP side shows checks due and missed, open corrective actions and the temperature checkpoints. The one thing to get right is the immediacy of the toggle and the "Other needs a note" rule.

**Known correction pending (do not draw the wrong version)**

- **No board frame; FNB-5J ("Availability, 86 & Food Safety") is mapped to EMP-062 and FNB-2H ("Availability & 86 Management") to nothing.** Why: Attach both so the designer starts from the client's drawing. *(source: screens/P08-venue-back-office.yaml#BO-140; Food, Beverage & Retail)*
- **Marking an item unavailable is on seven screens (POS-021, POS-024, EMP-062, BO-014, BO-049, BO-140, KIT-008) and HACCP status on three (EMP-062, BO-044, KIT-008).** Why: Make BO-140 the back-office home for F&B availability and food safety; the others are shortcuts with the same behaviour (DI-671). *(source: DI-671 / contracts/satellite/fnb.yaml#setItemAvailability; Food, Beverage & Retail)*
- **FNB-5J says a safety 86 cannot be cleared until its corrective action is signed, and FNB-2H distinguishes stock-driven 86s that clear on receipt; the contract has no link between an 86 and a corrective action, and no stock-driven 86.** Why: The frame promises behaviour nothing implements; draw only manual 86 until decided. *(source: screens/P08-venue-back-office.yaml#BO-140 / contracts/satellite/fnb.yaml#setItemAvailability; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The population is listExpiringBatches (stock batches, lot numbers, supplier, "Within days") - the Available toggle has no menu item to bind … (CHG-WIR-008); list86Events, getHaccpStatus and listTemperatureCheckpoints are not declared; setTemperatureCheckpoint is, with no list to edit from. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should a temperature breach automatically 86 the dishes that depend on that unit (FNB-5J "auto-86 on safety breach")?** → Drawn default stands (answer: "Suggest, don't auto: the breach banner offers '86 affected items'"): No automatic 86; the breach banner suggests "86 affected items". *(decided by Chinmay, 2026-10-02; DEC-193 / CHG-NOTE-004)*
- **Are daily counts ("6 left") with automatic 86 at zero in scope (FNB-2H "Count set")? No operation sets a count.** → Daily counts ('6 left') on menu items; an item goes sold out automatically at zero. *(decided by Chinmay, 2026-10-02; DEC-194 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search product availability, 86 | search field | — | — | — | — | — | — |
| Available | toggle | — | — | — | — | **Takes effect immediately** (decided 28 September, audit R110) — switching an item off (86) or back on calls `setItemAvailability` at once and every terminal in the outlet follows; there is no Save … | — |

**Form: Available** (modal, opened by *Available*; *86 now* calls `setItemAvailability`, *Cancel* sends nothing)

**The reason prompt when an item is switched off (86); confirming it is the call** — nothing waits for a later save (decided 28 September, audit R110). `isAvailable` and `recordedAt` come from the toggle. Optional: `reason` (soldOut, ingredientUnavailable, equipmentDown, seasonal, other), `note`, `restoreAt`. **Choosing Other makes the note required** — the prompt will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Switching an item back on sends at once with no prompt. Dismissing leaves the item as it was.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is available `isAvailable` | toggle | required | — | — | — | — | `setItemAvailability` body |
| Reason `reason` | radio group | optional | — | Sold out · Ingredient unavailable · Equipment down · Seasonal · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `setItemAvailability` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `setItemAvailability` body |
| Restore at `restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Automatic restore, typically at next service. Kept as `MenuItem.restoreAt`. | `setItemAvailability` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `setItemAvailability` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Set daily count** (modal, opened by *Set daily count*; *Set daily count* calls `setMenuItemDailyCount`, *Cancel* sends nothing)

**Collects what `setMenuItemDailyCount` sends before it is called.** Required: `count`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Count `count` | number field | required | — | min 0 | — | Portions for today. Null stops counting the item. | `setMenuItemDailyCount` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet**: Outlet picker by name; the list is that outlet's menu items grouped by section, with search. *(source: contracts/satellite/fnb.yaml#getMenu / DI-330)*
- **Available toggle**: Off opens a short prompt - reason (Sold out, Ingredient unavailable, Equipment down, Seasonal, Other), note, and "Back on" (Next service, End of day, a chosen time, or By hand). Choosing Other makes the note required and the confirm button stays disabled until it is filled. On sends at once with no prompt. *(source: R110 / R222 / contracts/satellite/fnb.yaml#setItemAvailability)*
- **Temperature checkpoint**: Label as staff call it (Walk-in 2, Dessert counter), kind (Fridge, Freezer, Holding cabinet, Blast chiller, Core probe, Delivery, Display counter, Ambient), safe range in degrees C (either end may be empty, not both), how often it must be read (minutes), whether a breach needs a corrective action, active. *(source: contracts/satellite/fnb.yaml#setTemperatureCheckpoint)*

#### Outputs: what the screen shows and produces

**Shown**

**Menu items** (detail panel, from `getMenu`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Days of week | list or chips (count when long) | — |
| Start time | text | Wall-clock time, in the Region's time zone. |
| End time | text | Wall-clock time, in the Region's time zone. |
| Valid from | 1 Oct 2026 | Calendar day, in the Region's time zone, not UTC. |
| Valid to | 1 Oct 2026 | Calendar day, in the Region's time zone, not UTC. |
| Sections | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Sort order | 1,234 | — |
| Items | list or chips (count when long) | The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`. |
| ID | the name it points at, never the id | — |
| Product variant | the name it points at, never the id | The catalogue variant this item links to, for reporting, stock and tax class only. |
| Name | text | — |
| Description | text | — |

**86 history** (data table, from `list86Events`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Menu item | the name it points at, never the id | — |
| Off at | 1 Oct 2026, 14:30 | — |
| Back at | 1 Oct 2026, 14:30 | — |
| Reason | chip: Ran out, Quality issue, Equipment down, Supplier failure, Seasonal, Other | `other` always carries a `note` (audit R222). |
| Note | text | The note given with the 86. Required where the reason is `other` (audit R222). |
| Called by principal | the name it points at, never the id | — |
| Source | chip: Manual, Daily count | Who took the item off (CHG-CSA-017). `manual`: a person, through `setItemAvailability`. |
| Refused order count | 1,234 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Food safety** (detail panel, from `getHaccpStatus`)

| Shows | Format | Notes |
|---|---|---|
| Checks due | 1,234 | — |
| Checks missed | 1,234 | — |
| Open actions | 1,234 | — |
| Unsigned actions | 1,234 | — |
| Oldest open action age hours | 1,234 | — |
| Last inspection at | 1 Oct 2026, 14:30 | — |

**Checkpoints** (data table, from `listTemperatureCheckpoints`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Kind | chip: Fridge, Freezer, Holding cabinet, Blast chiller, Core probe, Delivery… | The same closed set `TemperatureLog.checkPointKind` records. |
| Label | text | What the person reading it calls it — *Walk-in 2*, *Dessert counter*. A checkpoint identified only by a uuid is one somebody will read the … |
| Min celsius | 1,234.5 | — |
| Max celsius | 1,234.5 | Null at either end is legitimate — a core probe has a floor and no ceiling. Both null is not, and is what an unconfigured checkpoint looks … |
| Check frequency minutes | 1,234 | How often it must be read. The gap this leaves open otherwise is the one an inspector finds: not a bad reading, but a missing one. |
| Requires corrective action on breach | yes / no (icon or chip) | — |
| Is active | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Set daily count (secondary button) | `setMenuItemDailyCount` PUT `/menu-items/{itemId}/daily-count` | inline | MenuItem | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Item status**: Available, or "86" with reason, since when, who, and "back at 18:00" when a return time is set; guests see the same item as "Sold out". *(source: contracts/satellite/fnb.yaml#/components/schemas/MenuItem / contracts/satellite/fnb.yaml#getGuestMenu)*
- **86 history**: Time off, time back, who called it and refused orders, per item and outlet, for the day and 30 days. *(source: contracts/satellite/fnb.yaml#list86Events / screens/P08-venue-back-office.yaml#BO-140)*
- **Food-safety status**: Checks due, checks missed, open corrective actions and unsigned findings; a missed check counts the same as a failed one. An open breach shows the unit, peak reading, limit and duration. *(source: contracts/satellite/fnb.yaml#getHaccpStatus / F28 step 1 / F28 step 6)*
- **Temperatures**: Degrees Celsius with one decimal; a reading outside the range in danger colour, near the limit in warning. *(source: contracts/satellite/fnb.yaml#/components/schemas/TemperatureLog)*
- **Daily counts**: An item can carry a daily count ("6 left"); at zero it goes Sold out automatically, until the next count. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **86 now**: Live on every till and guest menu of the outlet when it returns; the row flips at once and the history adds the event. Other without a note is refused (400) and the prompt says why. *(source: R110 / R222 / contracts/satellite/fnb.yaml#setItemAvailability)*
- **Back on**: Immediate, no prompt. *(source: R110 / contracts/satellite/fnb.yaml#setItemAvailability)*
- **Save checkpoint**: Saves the unit and its range; past readings keep the range they were judged against (a range revised now does not re-judge January). *(source: contracts/satellite/fnb.yaml#setTemperatureCheckpoint)*

**Data it reads**: `getMenu` (onLoad, The outlet's menu items with their availability); `getHaccpStatus` (onLoad, Food-safety status); `listTemperatureCheckpoints` (onLoad, The temperature checkpoints to edit)

**Where the user goes next**

- → `BO-105` Stock & Supply: *Stock & Supply*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product availability operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product availability operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product availability operational yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on withinDays and the product availability operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getMenu` requires to show this screen, and names that permission (the screen's other reads need `INCIDENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setItemAvailability`, `setTemperatureCheckpoint` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **The device is offline when an item is 86'd**: The toggle shows "Saved on this device - tills will update when it reconnects"; offline tills keep selling from the cached menu and the kitchen refuses an 86'd item before the guest pays. *(source: contracts/satellite/fnb.yaml#setItemAvailability / F108 step 3)*
- **Someone else changed the same item first**: The row refreshes to the current state with "Changed by Omar Ziad at 19:42" (412). *(source: contracts/satellite/fnb.yaml#setItemAvailability)*
- **A checkpoint is not read in time**: A minor corrective action opens on its own (missed check) and appears in the open list. *(source: R125 / contracts/satellite/fnb.yaml#logTemperature)*
- **Escalating a critical finding with no food-safety lead**: Refused; the message links to F&B settings to name the lead. *(source: R096 / contracts/satellite/fnb.yaml#escalateCorrectiveAction)*

#### Consistency with other screens

- Match `KIT-008`: The kitchen's unavailable-items view; same reasons, same "86" wording, same history.
- Match `POS-021`: The till greys the item with "86" the moment this returns.
- Match `EMP-062`: The staff app's availability and HACCP entry; same toggle behaviour and prompt.
- Match `BO-136`: The food-safety lead is named on F&B settings.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Bite & Go (Aqua Park)
unavailable:
- item: Chicken Machboos
  reason: Ingredient unavailable
  since: '11:05'
  by: Priya Nair
  backOn: Next service 18:00
- item: Mango Lassi
  reason: Other
  note: Blender down, engineer called
  since: '12:20'
  by: Omar Ziad
  backOn: By hand
breach:
  unit: Chiller 2 - Bite & Go
  peak: 8.4 C
  limit: 5.0 C
  duration: 40 min
  action: Open - assigned to Fatima Al Suwaidi
haccp:
  roundsDone: 3 of 4
  missed: 1
  openActions: 2
  unsigned: 1
checkpoints:
- label: Walk-in 2
  kind: Fridge
  range: 0.0 to 5.0 C
  every: 120 min
- label: Hot hold - pass
  kind: Holding cabinet
  range: 63.0 C and above
  every: 60 min
```

#### Permissions

- `setItemAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `setTemperatureCheckpoint` → `PRODUCT_CONFIGURE` (configure) · staff
- `getMenu` → `PRODUCT_VIEW` (read) · staff
- `list86Events` → `PRODUCT_VIEW` (read) · staff
- `getHaccpStatus` → `INCIDENT_VIEW` (read) · staff
- `listTemperatureCheckpoints` → `PRODUCT_VIEW` (read) · staff
- `setMenuItemDailyCount` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getMenu` requires to show this screen, and names that permission (the screen's other reads need `INCIDENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setItemAvailability`, `setTemperatureCheckpoint` …

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.9 | The system should be able to allow the back office to limit the sale of a particular item per day or per timeslot.(example: Happy hour time slot based sales). | Bundles and Promotions | CONTRACTED | `setItemAvailability` |
| 2.1.32 | System shall allow guests to purchase food and beverage items through self-service kiosks. The kiosk shall support menu browsing, product customization, combo meals, upsell recommendations … | Ticketing Sales | CONTRACTED | data `Menu` |
| 2.1.33 | System shall allow guests to purchase retail merchandise through self-service kiosks. The kiosk shall support product browsing, inventory validation, variant selection (size, color, style) … | Ticketing Sales | CONTRACTED | data `Menu` |
| 4.6.13 | The system should have a interface for kiosks where the guest should be able to place order via the self service option all the way till completing payments. | Bundles and Promotions | CONTRACTED | data `Menu` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-140` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 404, 412).
- [ ] Every output is drawn (51 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-140?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Set daily count.
- [ ] Every transition is wired: `BO-105`.
- [ ] Every gated control is gated: `INCIDENT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-141` Operational Alerts, AI Replenishment & Action Center

**Operational Alerts, AI Replenishment & Action Center — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `analytics` module |
| Block | Block D · task VM-BO-141 |
| Who uses it | venue staff holding `PROCUREMENT_REQUEST`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAlerts` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `alertId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/stock-supply/operational-alerts-ai-replenishment-action-cen` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Absorbed BO-472 on 28 September (audit R276)**: Operational Alerts & Exception Center (Games & Rides board 8) called only `listAlerts`, already here; it is retired and BO-464 now opens this screen for the operational exception queue.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** One queue for operational problems, including stock alerts that should become a requisition. From the reporting angle: each alert says what left its range, by how much, where, and since when, and is acknowledged by a named person rather than dismissed. The one thing to get right: an alert resolves itself when the figure is back in range; acknowledging means "I am on it", not "make it go away".

**Known correction pending (do not draw the wrong version)**

- **The screen is named "AI Replenishment" but declares no AI suggestion operation.** Why: The replenishment recommendation has no source; only alerts and requisitions are wired. *(source: screens/P08-venue-back-office.yaml#BO-141; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | radio group | optional | — | Raised · Acknowledged · Resolved · Expired | — | Sends `?status=` to `listAlerts`. | `listAlerts` ?status |
| Severity | segmented control | optional | — | Info · Warning · Critical | — | Sends `?severity=` to `listAlerts`. | `listAlerts` ?severity |
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listAlerts`. | `listAlerts` ?workstationId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listAlerts`. | `listAlerts` ?shiftId |
| Item id | picker: choose an item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?itemId=` to `listAlerts`. | `listAlerts` ?itemId |
| Search operational alerts, ai replenishment | search field | — | — | — | — | — | — |

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

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Acknowledge note**: Up to 300 characters saying what is being done. *(source: contracts/satellite/reporting.yaml#/components/schemas/Alert)*
- **Requisition from an alert**: Item prefilled from the alert, quantity, required-by date, cost centre, justification. *(source: contracts/satellite/reporting.yaml#/components/schemas/Alert / contracts/satellite/inventory.yaml#createRequisition)*
- **Filters**: Severity, status (raised, acknowledged, resolved, expired); outlet and item as pick lists, not ids. *(source: contracts/satellite/reporting.yaml#/components/schemas/AlertStatus)*

#### Outputs: what the screen shows and produces

**Shown**

**Every alert** (data table, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Acknowledged at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | Set when the metric returns to range, automatically. An alert that only a person can close is an alert list that only grows. |
| Escalated at | 1 Oct 2026, 14:30 | Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. |

**The selected alert** (detail panel, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Rule | the name it points at, never the id | — |
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Observed value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Threshold | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Scope path | text | — |
| Acknowledged by principal | the name it points at, never the id | — |
| Acknowledged at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | Set when the metric returns to range, automatically. An alert that only a person can close is an alert list that only grows. |
| Escalated at | 1 Oct 2026, 14:30 | Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Acknowledge alert (primary button) | `acknowledgeAlert` POST `/alerts/{alertId}/acknowledge` | inline | Alert | — | opens modal first |
| Create requisition (secondary button) | `createRequisition` POST `/requisitions` | CreateRequisitionRequest | Requisition | 400 Validation failed | gated `PROCUREMENT_REQUEST`; opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Alert row**: Rule name, observed value against threshold, item or workstation, raised time, escalated flag; critical first. *(source: contracts/satellite/reporting.yaml#/components/schemas/Alert)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Acknowledge**: Records who and the note; escalation stops. *(source: contracts/satellite/reporting.yaml#acknowledgeAlert)*
- **Raise requisition**: Creates the requisition and links it to the alert. *(source: contracts/satellite/inventory.yaml#createRequisition)*

**Data it reads**: `listAlerts` (onLoad, What is currently raised)

**Where the user goes next**

- → `BO-105` Stock & Supply: *Stock & Supply*
- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational alerts replenishment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational alerts replenishment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational alerts replenishment yet. Offers Create requisition (`createRequisition`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, severity, workstationId, shiftId, itemId and the operational alerts replenishment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listAlerts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PROCUREMENT_REQUEST` for `createRequisition`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Nobody acknowledges a critical alert**: It escalates after the venue's set minutes; the row shows "Escalated". *(source: contracts/satellite/reporting.yaml#/components/schemas/Alert)*

#### Consistency with other screens

- Match `POS-020`: Same alert vocabulary and severities.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
alerts:
- Critical · Bottled water 500 ml below reorder level · Surf Café · 38 left, reorder at 120 · since 09:14
- Warning · Wastage rate 6.2% above 4% · Main Kitchen · since yesterday
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

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-141` · status **notStarted** · provenance generated
- Client design-board frames: `Inventory Board 4.dc.html#inv-4g`, `Inventory Board 7.dc.html#inv-7c`, `Inventory Board 1.dc.html#inv-10`
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 16: Works in Operational Alerts, AI Replenishment & Action Center (Operational Alerts & Exception Center, merged into it on … → Provide one central queue for operational problems requiring attention.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-141?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Acknowledge alert, Create requisition.
- [ ] Every transition is wired: `BO-105`, `BO-464`.
- [ ] Every gated control is gated: `PROCUREMENT_REQUEST`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acknowledgeAlert": {"method":"POST","path":"/alerts/{alertId}/acknowledge","contract":"reporting","summary":"Mark it seen","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Alert"},
"createInventoryItem": {"method":"POST","path":"/inventory-items","contract":"inventory","summary":"Create an inventory item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateInventoryItemRequest","responds":"InventoryItem"},
"createRequisition": {"method":"POST","path":"/requisitions","contract":"inventory","summary":"Raise a requisition","permission":"PROCUREMENT_REQUEST","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRequisitionRequest","responds":"Requisition"},
"getCountVariance": {"method":"GET","path":"/stock-counts/{countId}/variance","contract":"inventory","summary":"Variance between counted and expected","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CountVariance"},
"getHaccpStatus": {"method":"GET","path":"/food-safety/status","contract":"fnb","summary":"Where this venue stands, right now","permission":"INCIDENT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getMenu": {"method":"GET","path":"/menus/{menuId}","contract":"fnb","summary":"Read a menu with sections and items","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Menu"},
"getProductionRun": {"method":"GET","path":"/production-runs/{runId}","contract":"fnb","summary":"One run — its plan, its output, and the gap","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductionRun"},
"getWasteApprovalPolicy": {"method":"GET","path":"/waste-approval-policy","contract":"fnb","summary":"The venue's waste-approval policy","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WasteApprovalPolicy"},
"list86Events": {"method":"GET","path":"/outlets/{outletId}/86-events","contract":"fnb","summary":"What came off the menu today, when, and for how long","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listProductionRuns": {"method":"GET","path":"/production-runs","contract":"fnb","summary":"What is being made, and what was","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationKind","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRecipes": {"method":"GET","path":"/recipes","contract":"fnb","summary":"List recipes","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":"menuItemId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTemperatureCheckpoints": {"method":"GET","path":"/food-safety/checkpoints","contract":"fnb","summary":"The units that get read, and the range each must hold","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordWaste": {"method":"POST","path":"/outlets/{outletId}/waste","contract":"fnb","summary":"Record waste","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"setItemAvailability": {"method":"PUT","path":"/menu-items/{itemId}/availability","contract":"fnb","summary":"Mark an item available or eighty-sixed","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"setMenuItemDailyCount": {"method":"PUT","path":"/menu-items/{itemId}/daily-count","contract":"fnb","summary":"Set today's count for a dish","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"setTemperatureCheckpoint": {"method":"PUT","path":"/food-safety/checkpoints","contract":"fnb","summary":"Define a checkpoint and its safe range","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"TemperatureCheckpoint","responds":"TemperatureCheckpoint"},
"setWasteApprovalPolicy": {"method":"PUT","path":"/waste-approval-policy","contract":"fnb","summary":"Switch waste approval on or off, and set its bands","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WasteApprovalPolicy","responds":"WasteApprovalPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"CostingMethod": {"type":"string","description":"Fixed at item creation. Immutable once movements exist.","enum":["weightedAverage","fifo","standardCost","lastPurchasePrice"]},
"CountVariance": {"x-ticvai-persistence":"none — computed at close","type":"object","required":["countId","totalVarianceValue","lines"],"properties":{"countId":{"type":"string","format":"uuid"},"totalVarianceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exceptionCount":{"type":"integer","description":"Lines beyond `VenueSettings.inventory.countVarianceTolerancePercent` (proposed default 2 per cent, audit R094), requiring review before posting."},"lines":{"type":"array","items":{"type":"object","required":["itemId","expectedQuantity","countedQuantity","variance","isException"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"expectedQuantity":{"type":"number"},"countedQuantity":{"type":"number"},"variance":{"type":"number"},"variancePercentage":{"type":"number"},"varianceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isException":{"type":"boolean"},"recountCount":{"type":"integer","description":"A line counted several times is itself a finding."},"note":{"type":"string","nullable":true}}}}}},
"CreateInventoryItemRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["sku","name","venueId","baseUnit","costingMethod"],"properties":{"sku":{"type":"string","maxLength":64},"barcode":{"type":"string","maxLength":128},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"baseUnit":{"type":"string","description":"The unit stock is held in. Immutable once movements exist."},"purchaseUnit":{"type":"string","description":"How the supplier sells it — a case of 24 against a base unit of one."},"purchaseUnitFactor":{"type":"number","minimum":0,"default":1},"costingMethod":{"$ref":"#/components/schemas/CostingMethod"},"reorderPoint":{"type":"number","minimum":0},"reorderQuantity":{"type":"number","minimum":0},"parLevel":{"type":"number","minimum":0},"preferredSupplierId":{"type":"string","format":"uuid"},"allowNegativeStock":{"type":"boolean","default":false,"description":"True permits issue beyond on-hand. Occasionally needed at a bar mid-service; dangerous everywhere else.\n"},"isPerishable":{"type":"boolean","default":false},"shelfLifeDays":{"type":"integer","nullable":true}}},
"CreateRequisitionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","venueId","lines","requiredBy"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid"},"costCenterId":{"type":"string","format":"uuid"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"},"note":{"type":"string","maxLength":200}}}},"requiredBy":{"type":"string","format":"date"},"justification":{"type":"string","maxLength":1000}}},
"EightySixEvent": {"type":"object","x-ticvai-persistence":"fnb.sold_out_item","description":"Board 5J. **`setItemAvailability` recorded the current state and not the history.** An item 86'd at 7pm on a Saturday is a lost-sales figure and a prep-planning signal, and the package kept only the flag.\n**`refusedOrderCount` is what makes it worth keeping.** *Off for ninety minutes* is a note; *off for ninety minutes and eleven guests asked for it* is a purchasing decision.\n","required":["id","menuItemId","offAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"offAt":{"type":"string","format":"date-time"},"backAt":{"type":"string","format":"date-time","nullable":true},"reason":{"type":"string","enum":["ranOut","qualityIssue","equipmentDown","supplierFailure","seasonal","other"],"description":"`other` always carries a `note` (audit R222)."},"note":{"type":"string","maxLength":500,"nullable":true,"description":"The note given with the 86. Required where the reason is `other` (audit R222)."},"calledByPrincipalId":{"type":"string","format":"uuid"},"source":{"type":"string","readOnly":true,"enum":["manual","dailyCount"],"default":"manual","description":"**Who took the item off** (CHG-CSA-017). `manual`: a person, through `setItemAvailability`. `dailyCount`: the item's `remainingCount` reached zero and the system marked it unavailable (`setMenuItemDailyCount`; Chinmay, 2 October, workbook Q194). An automatic 86 carries no `calledByPrincipalId`.\n"},"refusedOrderCount":{"type":"integer","default":0,"readOnly":true}}},
"InventoryItem": {"x-ticvai-persistence":"inventory.item","allOf":[{"$ref":"#/components/schemas/CreateInventoryItemRequest"},{"type":"object","required":["id","onHand","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"onHand":{"type":"number","description":"Derived from movements. Not directly editable."},"onOrder":{"type":"number"},"inTransit":{"type":"number"},"available":{"type":"number","description":"On-hand minus allocated, where allocated is stock reserved for orders (decided 28 September, audit R171)."},"averageCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lastPurchasePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isBelowReorderPoint":{"type":"boolean"},"hasMovements":{"type":"boolean","description":"True locks costing method and base unit."},"isActive":{"type":"boolean"}}}]},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"**The catalogue variant this item links to, for reporting, stock and tax class only. It is not where the price comes from** (Chinmay, 2 October, workbook Q34; CHG-CSA-009). F&B owns its own catalogue: F&B prices were migrated into the F&B service so ticketing scales as an isolated service (ADR-0028), and the price an outlet sells at is `price` on this item. The central catalogue prices tickets and single-price booths; it never reprices a dish. A menu belongs to one outlet, so `price` is that outlet's price, and an outlet may set its own; it changes through `updateMenu`, `setMenuSections` or `applyMenuActions` (`reprice`). Tax is computed on the order line by the tax engine. (Replaces the earlier text \"pricing and tax come from there — a menu is a presentation of the catalogue\", which was stale.)\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"dailyCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**How many portions the kitchen set for today** (`setMenuItemDailyCount`; Chinmay, 2 October, workbook Q194; CHG-CSA-017). Null means the item is not counted. Reset at the venue day start.\n"},"remainingCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**What is left of `dailyCount`** (\"6 left\" on the till and the guest menu). Each sale takes from it; **at zero the item is marked unavailable automatically**, with an `EightySixEvent` whose `source` is `dailyCount`. Null where the item is not counted.\n"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall","grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings"],"x-ticvai-money-valued":["grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings","inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-extended-2-october":"**Eight finance measures added 2 October 2026** (Chinmay; CHG-FIN-007, CHG-FIN-010), each with the source and formula of the seeded KPI of the same code in `ReportingSystemKpi`: `grossSales`, `discounts`, `refunds`, `netRevenue`, `recognisedRevenue`, `deferredRevenue`, `taxCollected` and `takings`, so an alert rule can watch them (a refund spike, takings below a target). Formulas are the D-185 default; client finance sign-off is pending.","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductionRun": {"type":"object","x-ticvai-persistence":"fnb.production_run","description":"BL-129. **A central kitchen makes 400 portions at 6am for four outlets**, and nothing modelled that — orders consume stock and no operation produced any.\n**Production converts ingredients into a sellable item**, which is a stock movement in both directions at once, and treating it as two unrelated adjustments loses the yield.\n","required":["id","recipeId","plannedQuantity","status"],"properties":{"id":{"type":"string","format":"uuid"},"recipeId":{"type":"string","format":"uuid"},"productionPlanId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The plan whose release created this run. Null for a run planned directly."},"stationId":{"type":"string","format":"uuid","nullable":true,"description":"**The station whose prep list this run is on.** Copied from the plan line on release, where runs are grouped by station (audit R125 (7)).\n"},"producingOutletId":{"type":"string","format":"uuid"},"forOutletIds":{"type":"array","description":"**Where it goes.** A central kitchen produces for outlets that did not make it.\n","items":{"type":"string","format":"uuid"}},"plannedQuantity":{"type":"number"},"actualQuantity":{"type":"number","nullable":true,"description":"BL-126. **Theoretical against actual is the whole point of recording this.** A recipe says 400 portions from the ingredients issued; the run says how many were made, and the gap is waste, theft or a recipe that is wrong.\n"},"scheduledFor":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["planned","inProgress","completed","cancelled"]},"varianceReason":{"type":"string","nullable":true}}},
"Recipe": {"x-ticvai-persistence":"fnb.recipe + fnb.recipe_ingredient","type":"object","required":["menuItemId","ingredients"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"yield":{"type":"number","minimum":0,"description":"Portions produced by one execution."},"ingredients":{"type":"array","minItems":1,"items":{"type":"object","required":["inventoryItemId","quantity","unit"],"properties":{"inventoryItemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"},"isOptional":{"type":"boolean","default":false}}}},"costPerPortion":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Computed, never entered** (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided by `yield`. Recomputed when the recipe or an ingredient cost changes.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**The recipe's own id** (4 October 2026, CHG-FXC-003; the Sprint 1-2 judging found no operation returned one, so `listIngredientSubstitutes`, `setIngredientSubstitutes` and `SubstitutionRule.recipeId` had nothing to send). One recipe per menu item: `setRecipe` upserts on `menuItemId` and returns the id it kept."}}},
"Requisition": {"x-ticvai-persistence":"inventory.requisition + inventory.requisition_line","type":"object","required":["id","requisitionNumber","venueId","status","lines","raisedByPrincipalId","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"requisitionNumber":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"costCenterId":{"type":"string","format":"uuid","nullable":true},"justification":{"type":"string","nullable":true},"status":{"$ref":"#/components/schemas/RequisitionStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"requestedQuantity":{"type":"number"},"suggestedQuantity":{"type":"number","nullable":true,"description":"**Kept, never overwritten** (`updateRequisitionLines`). Null on a line nobody suggested.\n"},"approvedQuantity":{"type":"number","nullable":true},"orderedQuantity":{"type":"number","nullable":true},"unit":{"type":"string"},"reason":{"type":"string","nullable":true,"description":"Why the requested quantity differs from the suggestion."},"note":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"estimatedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvalNote":{"type":"string","nullable":true},"requiredBy":{"type":"string","format":"date"},"createdAt":{"type":"string","format":"date-time"},"approvedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true,"description":"From `rejectRequisition`. What the requester reads before copying it into a new draft."},"rejectedAt":{"type":"string","format":"date-time","nullable":true},"returnQuestion":{"type":"string","nullable":true,"description":"From `returnRequisition`. What the requester must answer before resubmitting."},"returnedAt":{"type":"string","format":"date-time","nullable":true},"cancelReason":{"type":"string","nullable":true,"description":"From `cancelRequisition`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true}}},
"RequisitionStatus": {"type":"string","enum":["draft","pendingApproval","approved","rejected","returnedForInfo","ordered","closed","cancelled"]},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"TemperatureCheckpoint": {"type":"object","x-ticvai-persistence":"fnb.temperature_checkpoint","description":"**A unit that gets read, and the range it is required to hold.** The entity `TemperatureLog.checkPointId` has always been required to name and that nothing defined.\n**The safe range belongs here and is snapshotted onto each reading**, so that a range revised in March cannot silently re-judge a reading taken in January.","required":["id","kind","label","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["fridge","freezer","holdingCabinet","blastChiller","coreProbe","delivery","displayCounter","ambient"],"description":"The same closed set `TemperatureLog.checkPointKind` records."},"label":{"type":"string","description":"**What the person reading it calls it** — *Walk-in 2*, *Dessert counter*. A checkpoint identified only by a uuid is one somebody will read the wrong unit for."},"minCelsius":{"type":"number","nullable":true},"maxCelsius":{"type":"number","nullable":true,"description":"**Null at either end is legitimate** — a core probe has a floor and no ceiling. Both null is not, and is what an unconfigured checkpoint looks like."},"checkFrequencyMinutes":{"type":"integer","nullable":true,"description":"**How often it must be read.** The gap this leaves open otherwise is the one an inspector finds: not a bad reading, but a missing one."},"requiresCorrectiveActionOnBreach":{"type":"boolean"},"isActive":{"type":"boolean"},"scopePath":{"type":"string"}}},
"WasteApprovalPolicy": {"type":"object","x-ticvai-persistence":"fnb.waste_approval_policy","description":"**Whether waste needs approval, and above what value** (Chinmay, 2 October, workbook Q192; CHG-CSA-016). Off by default: a venue that never set one has `enabled` false. One row per venue.\n","required":["enabled"],"properties":{"enabled":{"type":"boolean","default":false},"bands":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Value bands in ascending `fromValue`; a record's value falls in the last band it reaches. A value below the first band needs nothing.","items":{"type":"object","required":["fromValue","requiresApproval"],"properties":{"fromValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"requiresApproval":{"type":"boolean"},"approverPermission":{"type":"string","nullable":true,"description":"The permission an approver in this band holds (a value of the permission vocabulary, e.g. `APPROVAL_ACT`)."}}}},"photoRequiredAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"At or above this value a photo is required (`recordWaste.photoAssetId`). Null means never."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}}
}
```
