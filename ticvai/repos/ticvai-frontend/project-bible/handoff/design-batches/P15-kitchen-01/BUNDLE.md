# P15-kitchen-01 — P15 · Kitchen

**10 screens · 27 operations · 28 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `INCIDENT_REPORT, INCIDENT_VIEW, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **18 of these operations work offline**: chaseStation, fireCourse, getCourseRules, getFnbOrder, getHaccpStatus, getKitchenSla, holdCourse, list86Events
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
| `KIT-001` | Kitchen Operations Command Center | A | 0 | 59 | 6 | 6 | 1 | 3 | — | notStarted (generated) |
| `KIT-002` | Kitchen Display System (KDS) | A | 11 | 14 | 6 | 6 | 2 | 3 | — | notStarted (generated) |
| `KIT-003` | Order Firing & Course Management | A | 18 | 0 | 6 | 4 | 3 | 0 | — | notStarted (generated) |
| `KIT-004` | Active Order Management & Fulfilment Journey | A | 0 | 22 | 6 | 8 | 1 | 6 | — | notStarted (generated) |
| `KIT-005` | Kitchen Station Workload & Dynamic Routing | A | 11 | 16 | 6 | 3 | 1 | 6 | — | notStarted (generated) |
| `KIT-006` | Expeditor & Order Assembly | A | 14 | 14 | 6 | 7 | 0 | 0 | — | notStarted (generated) |
| `KIT-007` | Guest Collection, Buzzer & Digital Notification | A | 0 | 20 | 6 | 6 | 2 | 0 | — | notStarted (generated) |
| `KIT-008` | Exceptions, Re-Fire & Unavailable Items | A | 14 | 14 | 6 | 4 | 0 | 0 | — | notStarted (generated) |
| `KIT-009` | SLA, Priority & Service Rules | A | 0 | 15 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `KIT-010` | Kitchen Performance, AI & Operational Optimization | A | 4 | 1 | 6 | 1 | 0 | 3 | — | notStarted (generated) |

## Thin screens in this batch

**KIT-007, KIT-010 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `KIT-001` Kitchen Operations Command Center

**Kitchen Operations Command Center — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28567 (APP-POS-KIT-001) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | commandCentre (touchLarge density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/kitchen-operations-command-center` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3a` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **`wireframe.status` corrected 25 August.** When these screens were repointed from the client pack to their own board on 24 August, the status stayed `designed` — **which claimed a client had drawn a board this package generated.** `derivedFrom` keeps the pack frame, which is where the design came from; `status` describes the file being pointed at, and those are different facts. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3a`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen Operations Command Center* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly. **DI-077 is superseded** (19 September: the kitchen display is TICVAI's own, not an integration point; design-notes correction fnb-retail KIT-001; CHG-SPO-017). The design-input index entry is the design-inputs owner's …

**From the Food, Beverage & Retail process.** The kitchen supervisor's or head chef's overview of the whole kitchen during service: how deep each station's rail is, the oldest ticket and how late it is against its target, held courses, refires and 86'd items, and a way into each working screen. It is not another rail. The one thing to get right: two glanceable numbers per station (tickets waiting, oldest age) and the exceptions that need a decision now, readable from two metres.

**Fixed on main** (the package already carries these; draw what it says): The screen repeats the station rail (ticket cards, Bump, a course number field and a free-text "Status" filter) with states copied from the … (CHG-SPO-017); The loading state says "oldest ticket first" while the cards say "ordered by promise time"; the contract says the rail order is the … (CHG-SPO-017); The meeting input "Softlabs need not build a full KDS, only an integration point" (31 July) is still in force in the design-input index. (CHG-CLN-012).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |
| Course | number field | — | min 1 | `listKitchenTickets` ?course |
| Outlet | picker: choose an outlet | — | — | `listKitchenStations` ?outletId |
| Outlet | picker: choose an outlet | — | — | `listFnbOrders` ?outletId |
| Table visit | picker: choose a table visit | — | — | `listFnbOrders` ?tableVisitId |
| Status | select | — | Ordered · Accepted · In preparation · Ready · Served · Collected · Delivered · Cancelled · Refunded | `listFnbOrders` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

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
| Printer devices | list or chips (count when long) | The kitchen printers assigned to this station (Chinmay, 2 October, workbook Q187: kitchen printers are in release 1; CHG-CSA-014), as … |
| Serves outlets | list or chips (count when long) | A producing outlet's station serving other outlets (Chinmay, 2 October, workbook Q186 and Q188; DI-330; CHG-CSA-015). |
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

**Every station, at a glance** (data table, from `listKitchenTickets`): The command centre spans every station (DI-332): load per station, late tickets and the oldest wait. No bump here: the rail is KIT-002. **The server's order, never re-sorted on the device** (`listKitchenTickets` orders by priority weights; design-notes correction fnb-retail): no "oldest first" and no "promise time" sort of its own.

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Per-station strip**: Each station (Grill, Fryer, Cold, Bar, Pastry) with tickets waiting and the age of the oldest, coloured against the outlet's target for that order type (amber at the warning percentage, red past target). No load percentage or capacity gauge in the first release. *(source: DI-332 / R277 / contracts/satellite/fnb.yaml#/components/schemas/KitchenSla)*
- **Orders by stage**: Counts of orders Received, Preparing, Ready (waiting for pickup or a runner) for the outlet; Ready orders waiting longest listed first. *(source: DI-332 / contracts/satellite/fnb.yaml#listFnbOrders)*
- **Needs attention**: Late tickets, held courses older than a few minutes, chased stations, items 86'd today with when they come back. *(source: contracts/satellite/fnb.yaml#holdCourse / contracts/satellite/fnb.yaml#chaseStation / contracts/satellite/fnb.yaml#list86Events)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Open a station's rail, the pass, collection, exceptions or rules**: Each tile opens its screen (KIT-002 for a station, KIT-006 the pass, KIT-007 collection, KIT-008 exceptions, KIT-009 rules). *(source: screens/P15-kitchen-display.yaml#KIT-001)*

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue); `listKitchenStations` (onLoad, List preparation stations and their routing); `listFnbOrders` (onLoad, List F&B orders)

**Where the user goes next**

- → `KIT-003` Order Firing & Course Management: *Order Firing & Course Management*; carries `ticketId`
- → `KIT-004` Active Order Management & Fulfilment Journey: *Active Order Management & Fulfilment Journey*; carries `orderId`
- → `KIT-005` Kitchen Station Workload & Dynamic Routing: *Kitchen Station Workload & Dynamic Routing*
- → `KIT-006` Expeditor & Order Assembly: *Expeditor & Order Assembly*; carries `ticketId`
- → `KIT-007` Guest Collection, Buzzer & Digital Notification: *Guest Collection, Buzzer & Digital Notification*; carries `orderId`
- → `KIT-008` Exceptions, Re-Fire & Unavailable Items: *Exceptions, Re-Fire & Unavailable Items*; carries `ticketId`
- → `KIT-009` SLA, Priority & Service Rules: *SLA, Priority & Service Rules*
- → `KIT-010` Kitchen Performance, AI & Operational Optimization: *Kitchen Performance, AI & Operational Optimization*
- → `KIT-002` Kitchen Display System (KDS): *Kitchen Display System (KDS)*; carries `ticketId`, `visitId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Every station's load, then the tickets, in the server's order. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the station chips; the kitchen is not empty. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, the screen's permission, and names it. The command centre is not tied to one station, so it never says "not assigned to a station". |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |

#### Edge cases to draw

- **Offline**: Amber banner, numbers from cache with their age; every bump made on station screens is journaled and syncs. *(source: screens/P15-kitchen-display.yaml#KIT-001)*
- **No tickets**: "The kitchen is clear" stated plainly, not a blank screen. *(source: screens/P15-kitchen-display.yaml#KIT-001)*

#### Consistency with other screens

- Match `KIT-002`: Same ticket card and colours; this screen shows counts, the station screen the cards.
- Match `BO-046`: The back office's kitchen view reads the same numbers after the fact.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro kitchen · dinner service
stations:
- Grill · 7 waiting · oldest 14 min (target 12) — red
- Fryer · 3 · 6 min
- Cold · 2 · 4 min
- Bar · 5 · 3 min
- Pastry · 1 · 2 min
stages: Received 2 · Preparing 14 · Ready 3 (oldest ready 5 min)
attention:
- T4 mains held 7 min — table not ready
- Grill chased twice
- Kunafa unavailable until 18:00
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `listKitchenStations` → `PRODUCT_VIEW` (read) · staff
- `listFnbOrders` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, the screen's permission, and names it. The command centre is not tied to one station, so it never says "not assigned to a station".

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

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (59 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `KIT-003`, `KIT-004`, `KIT-005`, `KIT-006`, `KIT-007`, `KIT-008`, `KIT-009`, `KIT-010`, `KIT-002`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-002` Kitchen Display System (KDS)

**Kitchen Display System (KDS) — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28568 (APP-POS-KIT-002) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as cashier, supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `ticketId` (KIT-002), `visitId` (deepLink) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/kitchen-display-system-kds` |

**What the spec says about it.** **Fire and hold leave the station display** (2 October 2026, CHG-CLN-006): the pass fires and holds courses (DI-407; KIT-003), and flow F88 step 2 no longer calls them here (CHG-SPO-020). **Built 20 August from board 3 of the client F&B design set.** **The screen the platform exists for.** Bumped, not tapped — a bump bar and a touch target sized for somebody wearing gloves. Nothing on it is more than one action deep. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Cross-platform navigation removed 24 August**: EMP-058. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3b` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen Display …

**From the Food, Beverage & Retail process.** The station display on the kitchen wall: the tickets this station must make, in the order the kitchen should make them, bumped with one touch or a bump bar by someone wearing gloves. The one thing to get right: each ticket card reads in a glance from two metres — order number or table, order type, items with options and allergy notes in red, and a fired timer counting up — and nothing is more than one action deep.

**Fixed on main** (the package already carries these; draw what it says): The layout has a number field "Course", a free-text "Status" filter, a table "Every kitchen ticket", and a "Save kitchen ticket status" … (CHG-SPO-017); Fire course and Hold course are on the station display. (CHG-CLN-006); The cards say "ordered by promise time not arrival", the loading state "oldest ticket first". (CHG-SPO-017).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Course | number field | optional | — | min 1 | — | Course chips, not a typed number (design-notes correction fnb-retail KIT-002). Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's … | `listKitchenTickets` ?course |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |

**Form: Save kitchen ticket status** (modal, opened by *Save kitchen ticket status*; *Save kitchen ticket status* calls `setKitchenTicketStatus`, *Cancel* sends nothing)

**A gesture on the card** (bump, start, ready); no form, no line ids typed and no time entered: the time is the device's (design-notes correction fnb-retail KIT-002).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | — | `setKitchenTicketStatus` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Advance specific lines. Omit for the whole ticket. | `setKitchenTicketStatus` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setKitchenTicketStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setKitchenTicketStatus` body |

Errors to draw in the form: 409 The move is not one of the four above. Names the ticket's current status.

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

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Course filter**: Chips with the outlet's course names (Starters · Mains · Desserts), not a number field; only that course's lines show. *(source: R277 / contracts/satellite/fnb.yaml#listKitchenTickets / contracts/satellite/fnb.yaml#setCourseRules)*
- **Station**: Never picked on the display; the display shows the station it is assigned to in station setup. *(source: R277 / contracts/satellite/fnb.yaml#/components/schemas/KitchenStation)*

#### Outputs: what the screen shows and produces

**Shown**

**Every kitchen ticket** (data table, from `listKitchenTickets`): **The server's order, never re-sorted on the device** (`listKitchenTickets` orders by priority weights; design-notes correction fnb-retail): no "oldest first" and no "promise time" sort of its own.

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

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
| Bump (primary button) | navigation or local | — | — | — | — |
| Save kitchen ticket status (primary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | works offline; gated `ORDER_MODIFY`; opens modal first; produces a document or message: Advance a kitchen ticket |
| Refire item (secondary button) | `refireItem` POST `/kitchen-tickets/{ticketId}/refire` | inline | KitchenTicket | — | works offline; gated `ORDER_MODIFY`; opens modal first |
| Recall kitchen ticket (secondary button) | `recallKitchenTicket` POST `/kitchen-tickets/{ticketId}/recall` | inline | KitchenTicket | 409 Past the recall window (`VenueSettings.fnb.recallWindowMinutes`, proposed default 10, audit R094). | works offline; gated `ORDER_MODIFY`; opens modal first; produces a document or message: Bring back a ticket that was bumped by mistake |
| Notify server (secondary button) | `notifyServer` POST `/table-visits/{visitId}/notify-server` | inline | no body | — | gated `ORDER_MODIFY`; opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Ticket card**: Header: "order number (counter) or table and covers (dine-in), order type badge, server. Lines: quantity," item, options indented, the note to the kitchen, allergen flags highlighted. A refire line is marked "REFIRE · overcooked". Priority tickets marked. Lines of a held course greyed with "Held". *(source: contracts/satellite/fnb.yaml#/components/schemas/KitchenTicket / contracts/satellite/fnb.yaml#refireItem)*
- **Fired timer**: Counts up from when the ticket (or course) was sent — never a countdown; resets when a course is completed; not shown for quick-service outlets. Turns amber at the warning percentage and red past the target for that order type. *(source: DI-334 / contracts/satellite/fnb.yaml#/components/schemas/KitchenSla)*
- **Rail order**: Exactly as the server returns it (priority, then the outlet's weights for age, promise time, table stage, VIP); the display does not re-sort. *(source: contracts/satellite/fnb.yaml#listKitchenTickets)*
- **Header**: Station name, tickets waiting and oldest age — two numbers. *(source: screens/P15-kitchen-display.yaml#KIT-002)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Start (tap a received ticket)**: Received → Preparing. *(source: contracts/satellite/fnb.yaml#setKitchenTicketStatus)*
- **Bump (ready)**: Preparing → Ready for the whole ticket or the tapped lines; the ticket leaves the rail and the counter or server sees it ready. *(source: contracts/satellite/fnb.yaml#setKitchenTicketStatus / F108 step 5)*
- **Recall**: Brings back a ticket bumped by mistake within the recall window (proposed 10 minutes); after it, the display offers a refire instead. *(source: contracts/satellite/fnb.yaml#recallKitchenTicket / R094)*
- **Refire line**: Remakes a line with a reason (overcooked, undercooked, wrong item, dropped, cold, allergy risk, guest changed mind, late add); not chargeable by default. *(source: contracts/satellite/fnb.yaml#refireItem / F29 step 6)*
- **Call server**: Notifies the table's assigned server (or the outlet supervisor if none) that food is ready, the guest is waiting, or there is an allergy query. *(source: contracts/satellite/fnb.yaml#notifyServer / R125 / F29 step 4)*

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
| Loading (`?state=loading`) | The rail. **The count renders before the tickets.** **The server's order, never re-sorted on the device** (`listKitchenTickets` orders by priority weights; design-notes correction fnb-retail): no "oldest first" and no "promise time" sort of its own. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission … |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Past the recall window (`VenueSettings.fnb.recallWindowMinutes`, proposed default 10, audit R094).; 409 The move is not one of the four above. Names the ticket's current status. |

#### Edge cases to draw

- **Offline**: The rail stays live from cache with an amber banner; every bump is journaled and syncs; new orders from tills on the venue network still arrive. *(source: screens/P15-kitchen-display.yaml#KIT-002 / contracts/satellite/fnb.yaml#createFnbOrder)*
- **The primary display of a station is down**: Tickets route to the station's fallback display; the fallback shows which station it is covering. *(source: DI-323 / contracts/satellite/fnb.yaml#/components/schemas/KitchenStation)*
- **A move the ticket's state does not allow (e.g. bump a received ticket straight to served)**: Refused with the ticket's current state; only Received→Preparing, Preparing→Ready, Ready→Recalled, Recalled→Preparing happen here. *(source: contracts/satellite/fnb.yaml#setKitchenTicketStatus)*
- **Recall after the window**: "Too late to recall — refire instead?" with the refire reasons. *(source: contracts/satellite/fnb.yaml#recallKitchenTicket)*

#### Consistency with other screens

- Match `POS-021`: The notes and allergen flags typed at the till appear here word for word.
- Match `KIT-003`: Held and fired courses look the same here and on the pass.
- Match `POS-022`: Ready on this display is Ready on the counter rail.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
station: Grill · 7 waiting · oldest 14 min
tickets:
- header: T4 · 6 covers · Dine-in · Priya
  course: Mains
  fired: '11:42'
  lines:
  - 2 × Ribeye 300 g — medium rare, peppercorn
  - '1 × Ribeye 300 g — well done · ALLERGY: no butter (milk)'
- header: BNG-004127 · Quick service
  lines:
  - 1 × Marina Smash Burger — medium, cheese · NO SESAME — allergy
- header: T9 · 2 covers
  lines:
  - 1 × Lamb chops — REFIRE · undercooked
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `refireItem` → `ORDER_MODIFY` (operate) · staff
- `recallKitchenTicket` → `ORDER_MODIFY` (operate) · staff
- `notifyServer` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission …

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

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

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

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump, Save kitchen ticket status, Refire item, Recall kitchen ticket, Notify server.
- [ ] Every transition is wired: `KIT-001`, `KIT-003`, `EMP-058`, `EMP-059`, `POS-022`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-003` Order Firing & Course Management

**Order Firing & Course Management — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28569 (APP-POS-KIT-003) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | configEditor (touchLarge density): the screen declares only writes (`setKitchenTicketStatus`, `prioritiseKitchenTicket`, `fireCourse`) and no read of a population — it is settings, not a list |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `ticketId` (KIT-002), `outletId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/order-firing-course-management` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Starters before mains is the entire job of a kitchen pass.** `KitchenTicket.coursing` carries `holdAndFire`, `phased` and `timed`; without it a table gets dessert while eating its starter. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3c` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3c`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Order Firing &amp; Course Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): "Save course rules" (setCourseRules, outlet configuration) sat on the live pass; course rules are set up before service (now on BO-136) (R254; design-notes …

**From the Food, Beverage & Retail process.** The pass (head chef or expeditor) for table service: courses of each table — starters before mains — and when the next course goes. The pass fires a held course when the table is ready, holds one when the table has gone quiet, and moves an urgent ticket up. The one thing to get right: per table, which course is out, which is held and for how long, and a single Fire button for the next course.

**Fixed on main** (the package already carries these; draw what it says): "Save course rules" (setCourseRules, outlet configuration) sits on the live pass, and the layout exposes the status request fields … (CHG-WIR-008); Course rules and kitchen targets have setters (setCourseRules, setKitchenSla) but no read operation. (CHG-WIR-008).

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

**Sent by *Save kitchen ticket status*** (`setKitchenTicketStatus`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | Received · Preparing · Ready · Served · Recalled · Cancelled | — | — | `setKitchenTicketStatus` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Advance specific lines. Omit for the whole ticket. | `setKitchenTicketStatus` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setKitchenTicketStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setKitchenTicketStatus` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Hold reason**: Table not ready · Guest request · Kitchen backed up · Waiting for previous course · Other (needs a note). *(source: contracts/satellite/fnb.yaml#holdCourse / R222)*
- **Fire at (timed coursing)**: Only for outlets using timed coursing; empty means now. *(source: contracts/satellite/fnb.yaml#fireCourse)*
- **Prioritise**: A reason is required (3+ characters); no position given means top of the rail; recorded against the person. *(source: contracts/satellite/fnb.yaml#prioritiseKitchenTicket / R125)*

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
| Bump (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Tables by course**: One row per table: covers, server, each course as a chip — Sent · Preparing · Ready · Served · Held (with how long). A held course keeps its place and shows its waiting time. *(source: contracts/satellite/fnb.yaml#holdCourse / DI-333)*
- **Coursing policy**: The outlet's default (Hold & fire, Timed, Phased, Fire all at once) shown as a label, per order type. *(source: contracts/satellite/fnb.yaml#setCourseRules)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Fire next course**: Sends the held course to the stations; works offline and replays in order. *(source: contracts/satellite/fnb.yaml#fireCourse)*
- **Hold course**: Stops a course going out, with a reason; it keeps its place on the rail. *(source: contracts/satellite/fnb.yaml#holdCourse)*
- **Move up**: Puts the ticket at the top of the rail (or a chosen place) with a reason; online only. *(source: contracts/satellite/fnb.yaml#prioritiseKitchenTicket)*

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
| Permission denied (`?state=emptyNoAccess`) | Without `ORDER_VIEW`, which `listKitchenTickets` requires, the screen does not load and this state names that permission. This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_MODIFY` gets this state naming `ORDER_MODIFY`**, the screen's `permission` and the one its fire, hold, status and prioritise actions need (the screen has no read); a button whose own `permission` the principal lacks is … |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The move is not one of the four above. Names the ticket's current status. |

#### Edge cases to draw

- **Offline**: Fire and hold work and replay in order; Move up needs the connection and is disabled with the reason. *(source: contracts/satellite/fnb.yaml#fireCourse / contracts/satellite/fnb.yaml#prioritiseKitchenTicket)*
- **Quick-service outlet**: No courses and no fired timer; the screen is not offered. *(source: DI-334)*

#### Consistency with other screens

- Match `EMP-058`: A server's "ready for mains" on the staff app reaches this screen; the server does not fire courses (DI-407).
- Match `KIT-002`: Held lines appear greyed with "Held" on the station rails.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tables:
- table: T2
  covers: 4
  server: Priya Nair
  courses: Starters served 19:52 · Mains held 6 min (table not ready) · Desserts —
- table: T4
  covers: 6
  courses: Starters served · Mains preparing (fired 20:03)
policy: Hold & fire for dine-in · Fire all at once for room service
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `prioritiseKitchenTicket` → `ORDER_MODIFY` (operate) · staff
- `fireCourse` → `ORDER_MODIFY` (operate) · staff
- `holdCourse` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Without `ORDER_VIEW`, which `listKitchenTickets` requires, the screen does not load and this state names that permission. This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_MODIFY` gets this state naming `ORDER_MODIFY`**, the screen's `permission` and the one its fire, hold, status and prioritise actions need (the screen has no read); a button whose own `permission` the principal lacks is …

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

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

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

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save kitchen ticket status, Prioritise kitchen ticket, Fire course, Hold course, Bump.
- [ ] Every transition is wired: `KIT-001`, `KIT-004`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-004` Active Order Management & Fulfilment Journey

**Follow one order from the till to the pass and out to the guest.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28570 (APP-POS-KIT-004) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenTickets` reads the population and `getFnbOrder` reads one of them — list, select, act |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `orderId` (KIT-002) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/active-order-management-fulfilment-journey` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3d` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

**From the Food, Beverage & Retail process.** One order's journey across stations for the pass or a supervisor: which of its kitchen tickets are ready, which are still on which station, and how it will be handed over. The one thing to get right: an order split across three stations reads as one order with its parts, so the pass knows what it is waiting for.

**Fixed on main** (the package already carries these; draw what it says): The layout repeats the station rail (cards, Bump, course number, status text field) instead of one order's detail. (CHG-SPO-017); The purpose is "Active Order Management & Fulfilment Journey — board 3 of the client F&B design set". (CHG-WIR-010).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |
| Course | number field | — | min 1 | `listKitchenTickets` ?course |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**This order's tickets, station by station** (data table, from `listKitchenTickets`): One order's journey from the till to the pass and out; it has no actions of its own (design-notes correction fnb-retail KIT-004).

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

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

**The F&B order** (detail panel, from `getFnbOrder`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Order header**: Order number or table, order type, guest name only for takeaway/delivery, promised time, nine-state status in the shared words (Ordered, Accepted, Preparing, Ready, Served, Collected, Delivered, Cancelled, Refunded). *(source: contracts/satellite/fnb.yaml#getFnbOrder / MATRIX 4.6.35 / MATRIX 5.1.11)*
- **Parts by station**: One row per kitchen ticket (station), with its status and age; the slowest part highlighted. *(source: contracts/satellite/fnb.yaml#/components/schemas/FnbOrder)*

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue); `getFnbOrder` (onLoad, Read an F&B order)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*
- → `KIT-008` Exceptions, Re-Fire & Unavailable Items: *Exceptions, Re-Fire & Unavailable Items*; carries `ticketId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order, then its tickets at each station. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks ORDER_VIEW for this outlet, and names it. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |

#### Edge cases to draw

- **Offline**: The order is read from cache with its age. *(source: contracts/satellite/fnb.yaml#getFnbOrder)*

#### Consistency with other screens

- Match `KIT-006`: Assembly on the pass uses the same per-station parts.
- Match `GST-025`: The guest's order tracker reads the same status words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order: BNG-004131 · Takeaway · Aisha Rahman · promised 13:10
parts:
- Grill — Ready 12:58
- Fryer — Preparing 6 min
- Bar — Ready 12:55
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `getFnbOrder` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks ORDER_VIEW for this outlet, and names it.

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

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `KIT-001`, `KIT-008`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-005` Kitchen Station Workload & Dynamic Routing

**Kitchen Station Workload & Dynamic Routing — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28571 (APP-POS-KIT-005) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure) |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenStations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/kitchen-station-workload-dynamic-routing` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Station Workload &amp; Dynamic Routing* matched at 0.89. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly. **Move work bound 4 October 2026 to rebalanceStationLoad (StationRebalance: moves[] fromStationId, toStationId, categoryIds; revertAt), as the contract types it (ledger); Bump is the rail's (KIT-002)** (CHG-FXS-002)

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): setKitchenStations is permanent station set-up and display assignment; the contract says a temporary move is the rebalance, and permanent set-up belongs in …

**From the Food, Beverage & Retail process.** A head chef moves work between stations mid-service when one is buried and another idle (a temporary rebalance that reverts at close), and sees each station's queue depth to decide. The one thing to get right: a rebalance is visibly temporary — it shows when it reverts — and is never mistaken for changing the permanent routing.

**Fixed on main** (the package already carries these; draw what it says): setKitchenStations (permanent station set-up and display assignment) is on the kitchen display, beside an "Outlet id" text field and a raw … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **R277 dropped the station-load tile from the first release. Is queue depth and oldest age per station acceptable as the "workload" on this screen?** → Drawn default stands (answer: "Default / recommended accepted"): Show depth and oldest age only; no load gauge or percentage. *(decided by Chinmay, 2026-10-02; DEC-055 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listKitchenStations`. | `listKitchenStations` ?outletId |
| Course | number field | optional | — | min 1 | — | Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in … | `listKitchenTickets` ?course |
| Move from station | picker: choose an id | optional | — | — | shows names, sends the id | moves[].fromStationId. | `KitchenStation.id` |
| Move to station | picker: choose an id | optional | — | — | shows names, sends the id | moves[].toStationId. | `KitchenStation.id` |
| Menu categories to move | repeatable rows | optional | — | — | — | moves[].categoryIds; one move per from/to pair. | `StationRebalance.moves` |
| Revert at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | The move undoes itself then; end of service by default. | `StationRebalance.revertAt` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |

**Sent by *Move work*** (`rebalanceStationLoad`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Moves `moves` | repeatable rows | required | — | — | — | — | `rebalanceStationLoad` body |
| From station `moves[].fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | — | `rebalanceStationLoad` body |
| To station `moves[].toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | — | `rebalanceStationLoad` body |
| Categorys `moves[].categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `rebalanceStationLoad` body |
| Revert at `revertAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rebalanceStationLoad` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Move**: From station, to station, which items (or all of a category), until when (defaults to the end of service). *(source: contracts/satellite/fnb.yaml#rebalanceStationLoad)*

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
| Move work (primary button) | `rebalanceStationLoad` POST `/kitchen-stations/rebalance` | StationRebalance | StationRebalance | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Stations**: Name, assigned displays (primary and fallback), tickets waiting and oldest age; a station with no working display flagged. No load percentage in the first release. *(source: contracts/satellite/fnb.yaml#listKitchenStations / R277)*
- **Active rebalances**: What moved, from where to where, and "reverts at 23:30". *(source: contracts/satellite/fnb.yaml#rebalanceStationLoad)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Move work**: Applies the temporary move; online only. *(source: contracts/satellite/fnb.yaml#rebalanceStationLoad)*

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
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission … |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |

#### Edge cases to draw

- **Offline**: Moving work is disabled with the reason; the station list shows from cache. *(source: contracts/satellite/fnb.yaml#rebalanceStationLoad)*

#### Consistency with other screens

- Match `BO-134`: Permanent stations and display assignment are set up in Venue Management; this screen only moves work for tonight.
- Match `BO-135`: Routing rules there decide where items go when no rebalance is active.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
stations:
- Grill · Display K2 (fallback K5) · 11 waiting · oldest 16 min
- Cold · Display K3 · 1 waiting
move: Burgers Grill → Fryer line until 23:30
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `listKitchenStations` → `PRODUCT_VIEW` (read) · staff
- `rebalanceStationLoad` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission …

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Kitchens are divided into stations (grill, fryer, beverage, dessert, etc.), each mapped to specific printers or KDS devices. Routing rules decide where an item prints/displays by category or item, with a fallback station/device if the primary one is offline or faulty. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-323)*

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

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

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Move work.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-006` Expeditor & Order Assembly

**Expeditor & Order Assembly — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28572 (APP-POS-KIT-006) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `ticketId` (KIT-002), `orderId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/expeditor-order-assembly` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **No expeditor role is modelled** — this reads and sets ticket status like the KDS. Whether an expeditor needs their own state is a kitchen question rather than a contract one. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Expeditor &amp; Order Assembly* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Food, Beverage & Retail process.** The expeditor at the pass assembles orders whose parts come from several stations, chases a station that is holding the rest up, prints the bag label for takeaway and delivery, and hands over. The one thing to get right: for each order, which parts are ready and which are missing, and a label that always carries the allergen flags.

**Fixed on main** (the package already carries these; draw what it says): The layout repeats the station rail (course number, status text field, "Every kitchen ticket", Bump). (CHG-SPO-017); Collection is recorded with markOrderCollected only; a runner's delivery has no action here. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |
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

**Form: Delivered** (modal, opened by *Delivered*; *Delivered* calls `recordOrderHandover`, *Cancel* sends nothing)

**Collects what `recordOrderHandover` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

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

**Whole orders, ready to assemble** (data table, from `listKitchenTickets`): The pass works whole orders across stations, not one station's tickets (design-notes correction fnb-retail KIT-006). **The server's order, never re-sorted on the device** (`listKitchenTickets` orders by priority weights; design-notes correction fnb-retail): no "oldest first" and no "promise time" sort of its own.

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Table label | text | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Buzzer code | text | BL-128. The pager number handed to a guest at a counter. |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |
| Priority | 1,234 | Higher fires sooner. Raised by Fast Pass or supervisor override. |

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

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
| Save kitchen ticket status (primary button) | `setKitchenTicketStatus` PUT `/kitchen/tickets/{ticketId}/status` | inline | KitchenTicket | 409 The move is not one of the four above. Names the ticket's current status. | works offline; gated `ORDER_MODIFY`; opens modal first; produces a document or message: Advance a kitchen ticket |
| Chase station (secondary button) | `chaseStation` POST `/kitchen-stations/{stationId}/chase` | inline | no body | — | works offline; gated `ORDER_MODIFY`; opens modal first |
| Mark order collected (secondary button) | `markOrderCollected` POST `/orders/{orderId}/collected` | inline | FnbOrder | — | works offline; gated `ORDER_MODIFY`; opens modal first |
| Print order label (secondary button) | `printOrderLabel` POST `/kitchen-tickets/{ticketId}/label` | — | OrderLabel | — | works offline; gated `ORDER_VIEW`; produces a document or message: A label for the bag |
| Delivered (secondary button) | `recordOrderHandover` POST `/guest-orders/{orderId}/delivery` | inline | GuestOrderStatus | 409 Order is not ready, or already closed; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)). | works offline; opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Assembly cards**: One card per order: parts ready (ticked) and missing (with station and age); complete orders rise to the top. *(source: contracts/satellite/fnb.yaml#listKitchenTickets)*
- **Bag label**: Order number, guest name, items with options, allergen flags — printed from the order, not composed on the device. *(source: contracts/satellite/fnb.yaml#printOrderLabel)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Chase station**: Asks the station where a line is; recorded as a chased exception (a station chased six times a service is a signal). *(source: contracts/satellite/fnb.yaml#chaseStation)*
- **Print label**: Prints the bag label for takeaway and delivery orders. *(source: contracts/satellite/fnb.yaml#printOrderLabel)*
- **Hand over**: Collected at the counter, or handed to a runner who records Delivered with the location. *(source: contracts/satellite/fnb.yaml#markOrderCollected / contracts/satellite/fnb.yaml#recordOrderHandover)*

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*
- → `KIT-002` Kitchen Display System (KDS): *Kitchen Display System (KDS)*; carries `ticketId`, `visitId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Whole orders, in the server's order. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission … |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Order is not ready, or already closed; 409 The move is not one of the four above. Names the ticket's current status.; 422 The outcome does not close this order's service mode, or a delivery names no location (audit R125 (1)). |

#### Edge cases to draw

- **Offline**: Chase, label and hand-over work offline and sync. *(source: contracts/satellite/fnb.yaml#chaseStation / contracts/satellite/fnb.yaml#printOrderLabel)*

#### Consistency with other screens

- Match `KIT-007`: An order assembled here moves to Ready for pickup on the guest board.
- Match `POS-029`: The till's queue shows the same ready orders.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
card: BNG-004131 · Takeaway · Aisha Rahman — Grill ✓, Bar ✓, Fryer missing (6 min) → Chase
label: 'BNG-004131 · Aisha Rahman · 1 × Loaded Fries · 1 × Smash Burger (no onions) · CONTAINS: gluten, milk, sesame'
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setKitchenTicketStatus` → `ORDER_MODIFY` (operate) · staff
- `chaseStation` → `ORDER_MODIFY` (operate) · staff
- `markOrderCollected` → `ORDER_MODIFY` (operate) · staff
- `printOrderLabel` → `ORDER_VIEW` (read) · staff
- `recordOrderHandover` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission …

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

None names this screen.

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

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

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save kitchen ticket status, Chase station, Mark order collected, Print order label, Delivered.
- [ ] Every transition is wired: `KIT-001`, `KIT-002`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-007` Guest Collection, Buzzer & Digital Notification

**Guest Collection, Buzzer & Digital Notification — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28573 (APP-POS-KIT-007) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read) |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/guest-collection-buzzer-digital-notification` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **`buzzerCode` exists and nothing dispatches to a physical pager.** The digital half works; the buzzer half assumes a device driver the package does not model. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3g` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **The customer-facing order status board is this screen's** (decided 1 October 2026, POS v2 decision POSV2-7, docs/registers/pos-v2-decisions.md): the board the guests read, order numbers only under Preparing and Ready for pickup, never a name. The till's Order Queue (POS-029) shows a mirror of it, not a board of its own. **The guest board is an unattended customer display** (POSV2-7; design-notes correction fnb-retail KIT-007; CHG-SPO-017): order numbers only, under Preparing and Ready for pickup, never a name and no staff control. Handover is recorded at the pass (KIT-006). The buzzer number is on the ticket, but nothing writes it from the till or dispatches to a pager yet (open entry CHG-SPO-019). **An unattended guest display, read-only** (decided by Chinmay, 3 October 2026 (CHG-SPF-008)): `recordOrderHandover`, its button and form left this screen; a handover is recorded on KIT-006 Expo …

**From the Food, Beverage & Retail process.** Two faces of collection. (1) The **guest status board**: a customer-facing screen in the dining area showing order numbers only, under Preparing and Ready for pickup, readable across the room; this screen owns it and the till's queue mirrors it (POSV2-7). (2) The collection point's staff view: call the number, hand over, record it. The one thing to get right: the guest board shows numbers only — never a name — and is an unattended display with no buttons.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The buzzer number exists on the ticket, but nothing writes it from the till and nothing dispatches to a pager. (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): The guest board is drawn inside a staff screen that also has the course number field, a status text field, "Every kitchen ticket" and Bump … (CHG-SPO-017).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does the guest board carry the venue's branding (it is guest-facing) or TICVAI branding (it runs on a staff device)?** → Drawn default stands (answer: "Default / recommended accepted"): Venue branding on the guest board; TICVAI branding on the staff collection view. *(decided by Chinmay, 2026-10-02; DEC-056 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |
| Course | number field | — | min 1 | `listKitchenTickets` ?course |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Guest status board — Preparing and Ready for pickup** (card list, from `listKitchenTickets`): **Order numbers only, never a name**, in two columns, Preparing and Ready for pickup, readable from across the room. **Owned here** (decided 1 October 2026, POSV2-7); the till's Order Queue (POS-029) mirrors it. The look is the v2 build's queue status board. **Read-only, in the order the server returns** (decided by Chinmay, 3 October 2026 (CHG-SPF-008)): order numbers, Preparing and Ready for …

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

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Guest status board**: Two columns, Preparing and Ready for pickup, large order numbers; a number moving to Ready animates once and may chime; numbers leave the board when collected. Only counter, takeaway and app-collection orders — never dine-in, delivery or partner orders. Venue branding allowed on this guest-facing display. *(source: POSV2-7 / DI-790 / DI-794 / screens/P15-kitchen-display.yaml#KIT-007)*
- **Staff collection list**: Ready orders with how long they have waited; buzzer number where pagers are used. *(source: contracts/satellite/fnb.yaml#/components/schemas/KitchenTicket / F108 step 6)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Handed over**: Records Collected (or Guest not found / Refused with a note, which leaves the order Ready). *(source: contracts/satellite/fnb.yaml#recordOrderHandover)*

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen ticket queue)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Order numbers under Preparing and Ready for pickup. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing preparing or ready: the board shows the venue's idle message. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic. |
| Permission denied (`?state=emptyNoAccess`) | Never shown on the board: it is an unattended guest display and carries no staff state. |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |

#### Edge cases to draw

- **Nobody collects a ready order**: It stays on the board, then is recorded as uncollected rather than silently closed. *(source: F108 step 6)*
- **Offline**: The board keeps showing from the venue network; a stale board shows a small "updating" marker, never a frozen list without notice. *(source: screens/P15-kitchen-display.yaml#KIT-007)*

#### Consistency with other screens

- Match `POS-029`: The till's queue shows a mirror of this board with the same numbers and columns (POSV2-7).
- Match `GST-025`: The guest's app tracker says "Ready for pickup" at the same moment the number moves here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
board:
  preparing:
  - '841'
  - '847'
  - '850'
  readyForPickup:
  - '846'
  - '848'
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Never shown on the board: it is an unattended guest display and carries no staff state.

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
- Quick-service (QSR) orders capture no pickup details: guest orders, pays, gets a receipt/order number and is notified via a KDS-driven order-status board. Takeaway/delivery do need contact and timing details. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-790)*

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-007` · status **notStarted** · provenance generated · **Drawn as FNB-3G in the client pack.** The pack's frame is the specification for this screen — it carries operations, states, entry params and exits, and it is better specified than anything derived …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3g`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3g`

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-008` Exceptions, Re-Fire & Unavailable Items

**Exceptions, Re-Fire & Unavailable Items — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28574 (APP-POS-KIT-008) |
| Who uses it | venue staff holding `INCIDENT_REPORT`, `INCIDENT_VIEW`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 operate, 3 read, 1 configure); in the flows as supervisor |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | listDetail (touchLarge density): `list86Events` reads the population and `getHaccpStatus` reads one of them — list, select, act |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `itemId` (KIT-002), `ticketId` (KIT-002), `outletId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/exceptions-re-fire-unavailable-items` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **86 is a kitchen word and a real state.** An item marked unavailable here stops selling at every till in the venue within seconds, which is the only reason to put it on a kitchen screen. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.** **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3h` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3h`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Exceptions, Re-Fire &amp; Unavailable Items* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly. **Bump and the unbound rail cards left 4 October 2026: the exceptions screen saves …

**Known gaps.** **`getHaccpStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. Removed 2 October 2026 (CHG-WIR-008): "Save kitchen ticket status" on an exceptions screen is plumbing; the screen shows today's events and has no ticket status to save (R254; design-notes correction …

**From the Food, Beverage & Retail process.** What went wrong in the kitchen tonight and the controls for it: take an item off sale (86) at once on every till and guest menu, see what was 86'd today and for how long, log an equipment failure or a late delivery, and the food-safety position before and during service. The one thing to get right: 86 is one tap with a reason and an optional return time, and it says it is live everywhere.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The food-safety status read declares its response inline, so the panel cannot bind to a named shape. (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): A "From" date picker and a raw "Every eighty six event" table, plus "Save kitchen ticket status" on an exceptions screen. (CHG-WIR-008).

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

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Take off sale (86)**: Item, reason (Sold out · Ingredient unavailable · Equipment down · Seasonal · Other with a note), back at (optional). Immediate; works offline and replays. *(source: contracts/satellite/fnb.yaml#setItemAvailability / R110 / R222)*
- **Kitchen exception**: Equipment down · Item ran out · Late delivery · Staff short · Power loss · Spillage · Other (note required); station and ticket optional; duration in minutes. *(source: contracts/satellite/fnb.yaml#logKitchenException / R222)*

#### Outputs: what the screen shows and produces

**Shown**

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
| Log kitchen exception (secondary button) | `logKitchenException` POST `/kitchen-exceptions` | inline | KitchenException | 400 Validation failed | works offline; gated `INCIDENT_REPORT`; opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Off sale today**: Item, when it went off, who called it, reason, back at / came back, orders refused meanwhile. *(source: contracts/satellite/fnb.yaml#list86Events)*
- **Food safety**: Checks due, checks missed, open corrective actions, unsigned findings, oldest open action; a missed check counts like a failed one. *(source: contracts/satellite/fnb.yaml#getHaccpStatus / R125)*

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
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one `list86Events`, the population it reads, enforces (`getHaccpStatus` needs `INCIDENT_VIEW` and reaches no component yet, see `gaps`); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's … |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **An item 86'd here while a till is offline**: The offline till keeps selling it; the kitchen refuses it at send, before payment. *(source: F108 step 3)*

#### Consistency with other screens

- Match `BO-140`: The back office's availability and food-safety screen shows the same 86 events; both apply immediately (R110(c)).
- Match `POS-021`: The till shows the item as Unavailable with the return time.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offSale:
- Kunafa — Sold out · 17:10 by Chef Rami · back at 18:00
- Grilled hammour — Supplier failure · 12:30 · back tomorrow
exception: Fryer 2 down · 40 min · Fryer station · 'oil temperature fault'
foodSafety: Checks due 3 · missed 1 · open actions 2 · oldest 5 h
```

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff
- `setItemAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `getHaccpStatus` → `INCIDENT_VIEW` (read) · staff
- `list86Events` → `PRODUCT_VIEW` (read) · staff
- `logKitchenException` → `INCIDENT_REPORT` (operate) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one `list86Events`, the population it reads, enforces (`getHaccpStatus` needs `INCIDENT_VIEW` and reaches no component yet, see `gaps`); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's …

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

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-008` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3h`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3h`
- Flow F83 *A kitchen works a service from the rail to the exception*, step 5: Exceptions, Re-Fire & Unavailable Items. → **Drawn by the client as FNB-3H.** 3 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 412).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save item availability, Log kitchen exception.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `INCIDENT_REPORT`, `INCIDENT_VIEW`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-009` SLA, Priority & Service Rules

**SLA, Priority & Service Rules — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28575 (APP-POS-KIT-009) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | configEditor (touchLarge density): the screen declares only writes (`prioritiseKitchenTicket`, `setVenueSettings`) and no read of a population — it is settings, not a list |
| Offline | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |
| Opens with | `venueId` (session), `stationId` (session), `outletId` (session) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/sla-priority-service-rules` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3j` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *SLA, Priority &amp; Service Rules* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): setVenueSettings (the whole venue record, TENANT_CONFIGURE) on a kitchen device is a permission leak, and prioritising one ticket is a live act on the pass … Removed 2 October 2026 (CHG-WIR-008): setVenueSettings (the whole venue record, TENANT_CONFIGURE) on a kitchen device is a permission leak, and prioritising one ticket is a live act on the pass … Contract gap recorded 2 October 2026 (CHG-WIR-011): No read of an outlet's course rules or kitchen SLA.

**From the Food, Beverage & Retail process.** The kitchen's targets and priority rules for an outlet: how long a ticket may wait per order type before it is late, when it turns amber, and what pushes a ticket up the rail (age, promise time, table stage, VIP). Used by a head chef or F&B manager before service. The one thing to get right: the targets read as plain minutes per order type, with a preview of how tonight's rail would look.

**Fixed on main** (the package already carries these; draw what it says): setVenueSettings (the whole venue settings record, TENANT_CONFIGURE — support hours, biometrics, segregated access) is on the kitchen … (CHG-WIR-008); Prioritising a single ticket ("Reason", "Priority" fields) is on a rules screen; there is no read of the current targets. (CHG-SPO-017).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Target per order type**: Minutes (at least 1) for Dine-in, Quick service, Takeaway, Delivery, Room service; warn at a percentage (default 80%). *(source: contracts/satellite/fnb.yaml#setKitchenSla / contracts/satellite/fnb.yaml#/components/schemas/KitchenSla)*
- **Priority weights**: Relative weights for ticket age, promise time, table stage and VIP, shown as sliders with a plain explanation. *(source: contracts/satellite/fnb.yaml#setKitchenSla)*
- **Recall window**: Minutes a bumped ticket can be recalled (proposed 10); a venue setting with a tenant default. *(source: R094 / contracts/satellite/fnb.yaml#recallKitchenTicket)*

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.

**Metric tile** (metric tile): Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).

**Targets set now** (detail panel, from `getKitchenSla`): How long a ticket may sit before it is late, per station; edited with Save. Prioritising a single ticket is a live act on the pass (KIT-003), not a rule here (design-notes correction fnb-retail KIT-009).

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | The outlet, from the path. The row's key. |
| Targets | list or chips (count when long) | — |
| Service mode | chip: Quick service, Table service, Room service, Collection, Delivery | — |
| Target minutes | 1,234 | — |
| Warn at percent | 1,234 | — |
| Priority weights | grouped details | The weight of each signal the board names — age, promise time, table stage, a VIP marker. |
| Age | 1,234 | — |
| Target ready at | 1,234 | Promise time. |
| Table stage | 1,234 | — |
| Vip | 1,234 | — |

**Course rules** (detail panel, from `getCourseRules`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | The outlet in the path. |
| Default coursing | chip: Fire and forget, Hold and fire, Phased, Timed, Delayed | How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to … |
| Course names | list or chips (count when long) | — |
| Auto fire minutes | 1,234 | — |
| Service mode overrides | grouped details | A different default per service mode. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bump (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getKitchenSla` (onLoad, The targets set now, so the rules editor loads what it …); `getCourseRules` (onLoad, How this outlet courses by default, shown beside the …)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything. |
| Error (`?state=error`) | Could not reach the platform. **The rail is still live from cache** and every bump is queued. |
| Empty, first run (`?state=emptyFirstRun`) | **No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise. |
| Permission denied (`?state=emptyNoAccess`) | This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. Shown when the caller lacks `PRODUCT_VIEW`, which `getKitchenSla` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` … |
| Offline (`?state=offline`) | **Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns. |

#### Edge cases to draw

- **Someone else saved the rules meanwhile**: "These rules changed since you opened them — reload." *(source: contracts/satellite/fnb.yaml#setKitchenSla)*

#### Consistency with other screens

- Match `BO-136`: The F&B global settings hold the venue-level defaults; this screen sets one outlet's targets.
- Match `KIT-002`: The amber/red colours on the rail come from these targets.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
targets:
- Dine-in mains 18 min (amber at 80%)
- Quick service 8 min
- Takeaway 12 min
- Delivery 15 min
weights: Age 3 · Promise time 5 · Table stage 2 · VIP 4
```

#### Permissions

- `setKitchenSla` → `PRODUCT_CONFIGURE` (configure) · staff
- `getKitchenSla` → `PRODUCT_VIEW` (read) · staff
- `getCourseRules` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. Shown when the caller lacks `PRODUCT_VIEW`, which `getKitchenSla` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` …

Screen guard: `ORDER_MODIFY`

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P15 Kitchen Display.dc.html#kit-009` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/FnB Board 3.dc.html#fnb-3j`
- Drawn by: Claude Design F&B pack, 20 August
- Client design-board frames: `FnB Board 3.dc.html#fnb-3j`

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 412).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-009?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bump.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `KIT-010` Kitchen Performance, AI & Operational Optimization

**Kitchen Performance, AI & Operational Optimization — board 3 of the client F&B design set.**

| | |
|---|---|
| App · platform | TICVAI POS · P15 Kitchen Display (display) |
| Module | Kitchen · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #29000 (APP-POS-KIT-010) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate) |
| Device and orientation | kiosk · LTR · dark theme |
| Pattern | statusTracker (touchLarge density): `getDashboard` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available offline.** `getDashboard` is an analytical read (ADR-0016) and there is nothing local to serve. The rail on KIT-001 is what survives a network loss. **Corrected 24 August**: the earlier wording described the kitchen rather than this screen, and a checker cannot tell those apart from … |
| Opens with | `venueId` (session), `stationId` (session), `dashboardId` (navigation) · cold entry: **Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment … |
| Route | `/kitchen/kitchen-performance-ai-operational-optimization` |

**What the spec says about it.** **Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3k` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **This is the performance and AI analysis (pack frame FNB-3K), not the rail** (design-notes correction finance-insights KIT-010; CHG-SPO-017): kitchen performance, station performance, demand forecast and the recommendations. The rail and Bump are KIT-002. The named reads behind those tiles do not exist yet (open entry CHG-SPO-019). **The dashboard is found with listDashboards (module fnb) 4 October 2026, so the screen no longer needs a dashboardId from KIT-002 (SPF-2's station-dashboard read); its tiles are the dashboard's reports (tileData). The rail cards and the unbound tile left: the rail is KIT-002** (CHG-FXS-003)

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Kitchen performance over a period: where time is lost, by station and by hour, with forecast demand beside it and a few recommendations, each with its expected effect. This is a manager's analytical view, not the live ticket rail. The one thing to get right: a recommendation is something to judge, so each shows its expected effect, its cost and its confidence, and nothing is applied from here.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The screen reads a generic dashboard, while the pack names kitchen performance, station performance, demand forecast and recommendation reads, and an "insufficient data" state. (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): The layout and states describe the live rail (ticket cards, Bump, "No tickets, the kitchen is clear"). (CHG-SPO-017).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is this shown on the kitchen display device (no one signed in) or only to a signed-in kitchen manager?** → Drawn default accepted: A signed-in manager; the assistant and recommendations need a person whose role scopes the answer. *(decided by Chinmay, 2026-10-02; DEC-087 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Dashboard | picker: choose an id | optional | — | — | shows names, sends the id | Query module fnb; the kitchen's shared dashboard by default. | `Dashboard.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |
| Module | select | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | `listDashboards` ?module |
| Include archived | toggle | off | — | `listDashboards` ?includeArchived |

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Period**: Last 7 / 30 / 90 days; default 30. *(source: screens/P15-kitchen-display.yaml#KIT-010)*
- **Kitchen**: The kitchens the person may see; default the device's kitchen. *(source: screens/P15-kitchen-display.yaml#KIT-010)*

#### Outputs: what the screen shows and produces

**Shown**

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Ask reporting question (primary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | gated `REPORT_VIEW_VENUE`; opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Headline tiles**: Tickets (with change against the prior period), average preparation time in minutes, on-time percentage against its target, re-fire rate, peak throughput in tickets per hour. *(source: screens/P15-kitchen-display.yaml#KIT-010)*
- **Preparation time against demand by hour**: Bars for ticket volume and a line for average preparation time, with the target as a reference line; a caption names when preparation time crosses the target ("19:30–21:00"). Two axes need their units stated. *(source: screens/P15-kitchen-display.yaml#KIT-010 / MATRIX 8.7.1)*
- **Station table**: Station, tickets, average preparation, on-time, re-fires; the constraint station is called out in words. *(source: screens/P15-kitchen-display.yaml#KIT-010)*
- **Demand forecast, next 7 days**: Labelled Forecast, against last week's actual; shows the peak hour against current capacity. *(source: DI-973 / screens/P15-kitchen-display.yaml#KIT-010)*
- **Recommendations**: At most three, each with expected effect ("+6.2 pts on-time"), cost or risk ("labour AED 180 per service", "4% waste risk") and confidence. *(source: screens/P15-kitchen-display.yaml#KIT-010 / MATRIX 8.6.21 / MATRIX 3.6.37)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Review all recommendations**: Opens the recommendation list; accepting one is done by a person on the routing or rota screen it names. *(source: screens/P15-kitchen-display.yaml#KIT-010 / F20 step 2)*

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …); `listDashboards` (onLoad, The venue's kitchen dashboard (module fnb, shared): its id …)

**Where the user goes next**

- → `KIT-001` Kitchen Operations Command Center: *Kitchen Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Kitchen and station performance for the period, then the AI analysis. |
| Error (`?state=error`) | Could not load the performance figures. Names which read failed. |
| Empty, first run (`?state=emptyFirstRun`) | **Insufficient data**: fewer service days than the analysis needs; says how many more. |
| Empty, no results (`?state=emptyNoResults`) | No service in the chosen period. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getDashboard` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Not available offline.** `getDashboard` is an analytical read (ADR-0016) and there is nothing local to serve. The rail on KIT-001 is what survives a network loss. **Corrected 24 August**: the earlier wording described the kitchen rather than this screen, and a checker cannot tell those apart from prose. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem) |

#### Edge cases to draw

- **Not enough history (first weeks after go-live)**: "Not enough history yet: forecasts start after 4 weeks of service." Tiles show what exists; the forecast panel is empty with that sentence. *(source: DI-280 / screens/P15-kitchen-display.yaml#KIT-010)*
- **Offline**: Not available; the live rail on KIT-001 is what keeps working. *(source: screens/P15-kitchen-display.yaml#KIT-010)*

#### Consistency with other screens

- Match `KIT-001`: The live rail owns bumping tickets and ticket cards; this screen owns analysis only.
- Match `ANL-003`: The same preparation-time and on-time definitions as the operational performance board.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
header: Main Kitchen · last 30 days · 12,486 tickets
tiles:
- Tickets 12,486 +8.2%
- Avg prep 12.8 min +0.6
- On-time 92.6% · target 95%
- Re-fire rate 1.4% −0.3 pts
- Peak 96 tickets/hour
stations:
- Grill · 4,286 · 15.4 min · 86.2% · 72 re-fires
- Fryer · 3,142 · 8.6 min · 95.4% · 24
- Cold Kitchen · 1,884 · 9.8 min · 96.8% · 11
recommendations:
- Add a second grill cook 19:00–21:30 · +6.2 pts on-time · labour AED 180 per service · confidence 91%
- Pre-sear patties at 18:45 · −2.1 min · 4% waste risk · confidence 78%
```

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff
- `listDashboards` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getDashboard` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `REPORT_VIEW_VENUE`

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for all of P15, 29 for every app (section *Design inputs from the client meetings* below).

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

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (1 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#KIT-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ask reporting question.
- [ ] Every transition is wired: `KIT-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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
"getCourseRules": {"method":"GET","path":"/outlets/{outletId}/course-rules","contract":"fnb","summary":"How this outlet courses by default (read)","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CourseRules"},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getFnbOrder": {"method":"GET","path":"/fnb-orders/{orderId}","contract":"fnb","summary":"Read an F&B order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"FnbOrder"},
"getHaccpStatus": {"method":"GET","path":"/food-safety/status","contract":"fnb","summary":"Where this venue stands, right now","permission":"INCIDENT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getKitchenSla": {"method":"GET","path":"/outlets/{outletId}/kitchen-sla","contract":"fnb","summary":"How long a ticket may sit before it is late (read)","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"KitchenSla"},
"holdCourse": {"method":"POST","path":"/kitchen-tickets/{ticketId}/hold","contract":"fnb","summary":"Stop a course going out","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"list86Events": {"method":"GET","path":"/outlets/{outletId}/86-events","contract":"fnb","summary":"What came off the menu today, when, and for how long","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDashboards": {"method":"GET","path":"/dashboards","contract":"reporting","summary":"List dashboards","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"includeArchived","in":"query","required":false}],"requestBody":null,"responds":"Dashboard"},
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
"setItemAvailability": {"method":"PUT","path":"/menu-items/{itemId}/availability","contract":"fnb","summary":"Mark an item available or eighty-sixed","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"setKitchenSla": {"method":"PUT","path":"/outlets/{outletId}/kitchen-sla","contract":"fnb","summary":"How long a ticket may sit before it is late","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"KitchenSla","responds":"KitchenSla"},
"setKitchenTicketStatus": {"method":"PUT","path":"/kitchen/tickets/{ticketId}/status","contract":"fnb","summary":"Advance a kitchen ticket","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"CourseRules": {"type":"object","x-ticvai-persistence":"fnb.course_rule","description":"**An outlet's coursing default.** It was written to the resolution cache only, which the service model calls losable without consequence — an outlet's default vanished on a cache flush. One row per outlet.\n","properties":{"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet in the path."},"defaultCoursing":{"$ref":"#/components/schemas/CoursingPolicy"},"courseNames":{"type":"array","items":{"type":"string"}},"autoFireMinutes":{"type":"integer","nullable":true},"serviceModeOverrides":{"type":"object","description":"A different default per service mode.","propertyNames":{"$ref":"#/components/schemas/ServiceMode"},"additionalProperties":{"$ref":"#/components/schemas/CoursingPolicy"}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `outlet` scope."}}},
"CoursingPolicy": {"type":"string","description":"How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n","enum":["fireAndForget","holdAndFire","phased","timed","delayed"]},
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"#/components/schemas/common::ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"CreateFnbOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently."},"seatNumber":{"type":"integer","nullable":true,"description":"Which cover ordered it. Drives split-by-covers accurately."},"course":{"type":"integer","nullable":true,"description":"Course grouping, so the kitchen fires in sequence."},"redeemEntitlementId":{"type":"string","nullable":true,"x-ticvai-references":"access.entitlement","description":"**A meal combo redeemed at the till or by a scan** (29 September, MOB-4; applied 30 September). The entitlement a bundle's `fnbMenuItem` component issued (promotions `BundleComponent.componentKind: fnbMenuItem`, `menuItemId`, `redeemAtOutletIds`). The line is priced at zero against it, `menuItemId` must be the component's menu item and the outlet one of `redeemAtOutletIds` (or any outlet with the item on a live menu when that list is empty), and the entitlement is marked used in the same step through access `validateAccess` at the outlet. An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is refused the same way if it was used meanwhile."}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"EightySixEvent": {"type":"object","x-ticvai-persistence":"fnb.sold_out_item","description":"Board 5J. **`setItemAvailability` recorded the current state and not the history.** An item 86'd at 7pm on a Saturday is a lost-sales figure and a prep-planning signal, and the package kept only the flag.\n**`refusedOrderCount` is what makes it worth keeping.** *Off for ninety minutes* is a note; *off for ninety minutes and eleven guests asked for it* is a purchasing decision.\n","required":["id","menuItemId","offAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"offAt":{"type":"string","format":"date-time"},"backAt":{"type":"string","format":"date-time","nullable":true},"reason":{"type":"string","enum":["ranOut","qualityIssue","equipmentDown","supplierFailure","seasonal","other"],"description":"`other` always carries a `note` (audit R222)."},"note":{"type":"string","maxLength":500,"nullable":true,"description":"The note given with the 86. Required where the reason is `other` (audit R222)."},"calledByPrincipalId":{"type":"string","format":"uuid"},"source":{"type":"string","readOnly":true,"enum":["manual","dailyCount"],"default":"manual","description":"**Who took the item off** (CHG-CSA-017). `manual`: a person, through `setItemAvailability`. `dailyCount`: the item's `remainingCount` reached zero and the system marked it unavailable (`setMenuItemDailyCount`; Chinmay, 2 October, workbook Q194). An automatic 86 carries no `calledByPrincipalId`.\n"},"refusedOrderCount":{"type":"integer","default":0,"readOnly":true}}},
"FnbOrder": {"x-ticvai-persistence":"fnb.service_order + fnb.service_order_line","type":"object","required":["id","orderNumber","outletId","serviceMode","status","lines","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"paymentTiming":{"allOf":[{"$ref":"#/components/schemas/common::OutletPaymentTiming"}],"readOnly":true,"description":"The outlet's payment timing when the order was placed (CHG-CSA-010), kept as a snapshot."},"sentToKitchenAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the order's kitchen tickets were created. Null on a `payFirst` order not yet paid (CHG-CSA-010)."},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"lines":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/CreateFnbOrderLine"},{"type":"object","properties":{"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"orders.sales_order","description":"**Retyped 29 September (SD-046)**, and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"},"updatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both offline-sync fields, and no plain updated timestamp.\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"kitchenTicketId":{"type":"string","format":"uuid","nullable":true},"kitchenTickets":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"The kitchen tickets this order created, one per station (SD-046). Returned, not stored here; they are `fnb.kitchen_ticket` rows.","items":{"$ref":"#/components/schemas/KitchenTicket"}},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"GuestOrderStatus": {"type":"object","x-ticvai-persistence":"none — projection over kitchen_ticket","required":["orderId","status","lines"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"isReadyForCollection":{"type":"boolean"},"lines":{"type":"array","description":"Per-line status. A guest waiting on one dish should see which.","items":{"type":"object","properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}}}},
"KitchenException": {"type":"object","x-ticvai-persistence":"fnb.kitchen_exception","description":"Board 3, 24 August. **Something that cost the kitchen a service and left no other trace** — equipment down, an item run out mid-ticket, a late delivery, a station short.\n`refireItem` covers a dish. **This covers the reasons a venue looking at a bad Saturday needs**, and which currently live in somebody's memory.\n","required":["id","kind","raisedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"stationId":{"type":"string","format":"uuid","nullable":true},"ticketId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["equipmentDown","itemRanOut","lateDelivery","staffShort","powerLoss","spillage","chased","other"],"description":"`other` always carries a `note` (audit R222)."},"durationMinutes":{"type":"integer","nullable":true},"raisedAt":{"type":"string","format":"date-time"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}},
"KitchenSla": {"type":"object","x-ticvai-persistence":"fnb.kitchen_sla","x-ticvai-primary-key":["outletId"],"description":"**How long a ticket may sit, per service mode, and what pushes it up the rail** (`setKitchenSla`). The priority weights are the ones `listKitchenTickets` orders the rail by.\n\n**Stored per outlet in `fnb.kitchen_sla`** (3 October 2026, CHG-R1S-005: the HLD/LLD cross-check found `setKitchenSla` wrote no table). One row per outlet; the targets and weights are held whole.\n","properties":{"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet, from the path. The row's key."},"targets":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","items":{"type":"object","required":["serviceMode","targetMinutes"],"properties":{"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"targetMinutes":{"type":"integer","minimum":1},"warnAtPercent":{"type":"integer","default":80}}}},"priorityWeights":{"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The weight of each signal the board names — age, promise time, table stage, a VIP marker.","properties":{"age":{"type":"integer","minimum":0},"targetReadyAt":{"type":"integer","minimum":0,"description":"Promise time."},"tableStage":{"type":"integer","minimum":0},"vip":{"type":"integer","minimum":0}}}}},
"KitchenStation": {"x-ticvai-persistence":"fnb.kitchen_station","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"menuItemIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Items routed to this station."},"displayWorkstationIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**The kitchen displays assigned to this station** (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks after it. Set with `setKitchenStations`. A display reads the rail for the station it is assigned to (`listKitchenTickets`). A workstation is assigned to at most one station; a second assignment is refused `400`.\n"},"displayEndpoint":{"type":"string","nullable":true,"description":"The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station, with a fallback device where the primary is down — 18 Aug minute). Absent where the station has no display assigned.\n"},"printerDeviceIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**The kitchen printers assigned to this station** (Chinmay, 2 October, workbook Q187: kitchen printers are in release 1; CHG-CSA-014), as tenancy `RegisteredDevice` ids of kind `receiptPrinter` or `labelPrinter`. A station may have printers, displays or both; a ticket for a station with printers is printed there as well as shown, and `printPrepSheet` sends the station's part of a prep sheet to them.\n"},"servesOutletIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**A producing outlet's station serving other outlets** (Chinmay, 2 October, workbook Q186 and Q188; DI-330; CHG-CSA-015). `outletId` is the producing outlet (the commissary or main kitchen); the outlets listed here route their orders to this station as if it were their own. Empty, the default, means the station serves only its own outlet.\n"},"isActive":{"type":"boolean"}}},
"KitchenTicket": {"x-ticvai-persistence":"fnb.kitchen_ticket + fnb.kitchen_ticket_line","type":"object","required":["id","orderId","outletId","status","lines","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"coursing":{"allOf":[{"$ref":"#/components/schemas/CoursingPolicy"}],"nullable":true,"description":"BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"},"buzzerCode":{"type":"string","nullable":true,"description":"BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"},"priority":{"type":"integer","description":"Higher fires sooner. Raised by Fast Pass or supervisor override."},"prioritisedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"prioritiseReason":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","status"],"properties":{"lineId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"refireOfLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."},"refireReason":{"allOf":[{"$ref":"#/components/schemas/RefireReason"}],"nullable":true,"readOnly":true},"isChargeable":{"type":"boolean","nullable":true,"readOnly":true,"description":"A refire's `chargeable` flag. Null on a line that is not a refire."},"course":{"type":"integer","nullable":true},"stationId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}},"createdAt":{"type":"string","format":"date-time"},"targetReadyAt":{"type":"string","format":"date-time","nullable":true},"elapsedSeconds":{"type":"integer"},"visitId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The table visit the ticket is for** (4 October 2026, CHG-FXC-011; KIT-002): the `{visitId}` `notifyServer` takes. Null for a counter or delivery order with no visit."}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"**The catalogue variant this item links to, for reporting, stock and tax class only. It is not where the price comes from** (Chinmay, 2 October, workbook Q34; CHG-CSA-009). F&B owns its own catalogue: F&B prices were migrated into the F&B service so ticketing scales as an isolated service (ADR-0028), and the price an outlet sells at is `price` on this item. The central catalogue prices tickets and single-price booths; it never reprices a dish. A menu belongs to one outlet, so `price` is that outlet's price, and an outlet may set its own; it changes through `updateMenu`, `setMenuSections` or `applyMenuActions` (`reprice`). Tax is computed on the order line by the tax engine. (Replaces the earlier text \"pricing and tax come from there — a menu is a presentation of the catalogue\", which was stale.)\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"dailyCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**How many portions the kitchen set for today** (`setMenuItemDailyCount`; Chinmay, 2 October, workbook Q194; CHG-CSA-017). Null means the item is not counted. Reset at the venue day start.\n"},"remainingCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**What is left of `dailyCount`** (\"6 left\" on the till and the guest menu). Each sale takes from it; **at zero the item is marked unavailable automatically**, with an `EightySixEvent` whose `source` is `dailyCount`. Null where the item is not counted.\n"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"OrderLabel": {"type":"object","x-ticvai-persistence":"none — rendered from the kitchen ticket and its order","description":"**What goes on the bag** (`printOrderLabel`). Order number, guest name, items and **the allergen flags, which are the reason the label is rendered by the server** from the same source as the order rather than printed from whatever the client has.\n","required":["ticketId","orderNumber","lines","allergens"],"properties":{"ticketId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"guestName":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"deliveryLabel":{"type":"string","nullable":true,"description":"Where it is going, as a runner would read it."},"buzzerCode":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["name","quantity"],"properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"allergens":{"type":"array","description":"Every allergen on the order, together. Present and possibly empty — never omitted.","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RefireReason": {"type":"string","description":"Why a line was made again (`refireItem`). The reasons are the data.","enum":["overcooked","undercooked","wrongItem","dropped","cold","allergyRisk","guestChangedMind","lateAdd"]},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"ServiceMode": {"type":"string","enum":["quickService","tableService","roomService","collection","delivery"]},
"StationRebalance": {"type":"object","description":"**A temporary move of work between stations** (`rebalanceStationLoad`). Reverts at `revertAt`, or at close where that is null — a permanent change is `setKitchenStations`.\n","required":["moves"],"properties":{"moves":{"type":"array","items":{"type":"object","required":["fromStationId","toStationId"],"properties":{"fromStationId":{"type":"string","format":"uuid"},"toStationId":{"type":"string","format":"uuid"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"revertAt":{"type":"string","format":"date-time","nullable":true}}}
}
```
