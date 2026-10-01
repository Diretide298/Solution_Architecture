# P08-stock-supply-02 — P08 · Stock & Supply (2 of 2)

**6 screens · 19 operations · 28 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `AI_USE, ORDER_MODIFY, PROCUREMENT_REQUEST, PROCUREMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, TENANT_VIEW`. A control nobody can use must say so,
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
| `BO-105` | Stock & Supply | B–D | 21 | 55 | 6 | 43 | 1 | 4 | — | notStarted (generated) |
| `BO-137` | Recipe Consumption & Theoretical Inventory | B–D | 3 | 32 | 6 | 10 | 1 | 6 | — | notStarted (generated) |
| `BO-138` | Production Execution & Batch Management | B–D | 15 | 20 | 6 | 26 | 1 | 0 | — | notStarted (generated) |
| `BO-139` | Wastage, Spoilage, Returns & Write-Off | B–D | 14 | 0 | 5 | 15 | 1 | 0 | — | notStarted (generated) |
| `BO-140` | Product Availability, 86 & Operational Food Safety | B–D | 8 | 20 | 6 | 7 | 0 | 0 | — | notStarted (generated) |
| `BO-141` | Operational Alerts, AI Replenishment & Action Center | B–D | 18 | 24 | 6 | 6 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-105` Stock & Supply

**Everything in stock & supply.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PROCUREMENT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `REPORT_VIEW_VENUE`, `TENANT_VIEW` (3 read, 1 configure, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listInventoryItems` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/stock-supply` |

**What the spec says about it.** Section landing. **9 screens reach the entry point through here** — before 20 August they reached it through nothing.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listInventoryItems`. | `listInventoryItems` ?venueId |
| Category id | picker: choose a category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?categoryId=` to `listInventoryItems`. | `listInventoryItems` ?categoryId |
| Below reorder point | toggle | optional | — | — | — | Sends `?belowReorderPoint=` to `listInventoryItems`. | `listInventoryItems` ?belowReorderPoint |
| Search | text field | optional | — | min length 1; max length 200 | — | Sends `?search=` to `listInventoryItems`. | `listInventoryItems` ?search |
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
| Status | select | — | Raised · Sent · Acknowledged · Partially received · Received · Closed short · Cancelled | `listPurchaseOrders` ?status |
| Supplier | picker: choose a supplier | — | — | `listPurchaseOrders` ?supplierId |

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

**Every inventory** (data table, from `listInventoryItems`)

| Shows | Format | Notes |
|---|---|---|
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Base unit | text | The unit stock is held in. Immutable once movements exist. |
| Purchase unit | text | How the supplier sells it — a case of 24 against a base unit of one. |
| Purchase unit factor | 1,234.5 | — |
| Costing method | chip: Weighted average, Fifo, Standard cost, Last purchase price | Fixed at item creation. Immutable once movements exist. |
| Reorder point | 1,234.5 | — |
| Reorder quantity | 1,234.5 | — |
| Par level | 1,234.5 | — |

**Every purchase order** (data table, from `listPurchaseOrders`)

| Shows | Format | Notes |
|---|---|---|
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

**The selected inventory** (detail panel, from `listInventoryItems`)

| Shows | Format | Notes |
|---|---|---|
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Base unit | text | The unit stock is held in. Immutable once movements exist. |
| Purchase unit | text | How the supplier sells it — a case of 24 against a base unit of one. |
| Purchase unit factor | 1,234.5 | — |
| Costing method | chip: Weighted average, Fifo, Standard cost, Last purchase price | Fixed at item creation. Immutable once movements exist. |
| Reorder point | 1,234.5 | — |
| Reorder quantity | 1,234.5 | — |
| Par level | 1,234.5 | — |
| Preferred supplier | the name it points at, never the id | — |
| Allow negative stock | yes / no (icon or chip) | True permits issue beyond on-hand. Occasionally needed at a bar mid-service; dangerous everywhere else. |
| Is perishable | yes / no (icon or chip) | — |
| Shelf life days | 1,234 | — |

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
| Create inventory item (primary button) | `createInventoryItem` POST `/inventory-items` | CreateInventoryItemRequest | InventoryItem | 400 Validation failed; 409 SKU already in use in this venue | opens modal first |

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `getVenueSettings` (onLoad, What is enabled here); `listInventoryItems` (onLoad, Stock on hand); `listPurchaseOrders` (onLoad, Orders placed with suppliers)

**Where the user goes next**

- → `BO-049` Stock Levels: *Stock Levels*; carries `itemId`
- → `BO-052` Goods Receipt: *Goods Receipt*; carries `purchaseOrderId`
- → `BO-078` Requisitions: *Requisitions*; carries `requisitionId`
- → `BO-079` Stock Count: *Stock Count*
- → `BO-080` Stock Transfers: *Stock Transfers*
- → `BO-081` Inventory Items: *Inventory Items*; carries `itemId`
- → `BO-083` Suppliers: *Suppliers*; carries `supplierId`
- → `BO-137` Recipe Consumption & Theoretical Inventory: *Recipe Consumption & Theoretical Inventory*
- → `BO-138` Production Execution & Batch Management: *Production Execution & Batch Management*
- → `BO-139` Wastage, Spoilage, Returns & Write-Off: *Wastage, Spoilage, Returns & Write-Off*
- → `BO-140` Product Availability, 86 & Operational Food Safety: *Product Availability, 86 & Operational Food Safety*; carries `itemId`
- → `BO-141` Operational Alerts, AI Replenishment & Action Center: *Operational Alerts, AI Replenishment & Action Center*
- → `BO-051` Purchase Orders: *Purchase Orders*; carries `purchaseOrderId`

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

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `listInventoryItems` → `PRODUCT_VIEW` (read) · staff
- `listPurchaseOrders` → `PROCUREMENT_VIEW` (read) · staff
- `createInventoryItem` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** You do not have permission for stock & supply. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

43 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 31 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (55 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-105?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create inventory item.
- [ ] Every transition is wired: `BO-049`, `BO-052`, `BO-078`, `BO-079`, `BO-080`, `BO-081`, `BO-083`, `BO-137`, `BO-138`, `BO-139`, `BO-140`, `BO-141`, `BO-051`.
- [ ] Every gated control is gated: `PROCUREMENT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `REPORT_VIEW_VENUE`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-137` Recipe Consumption & Theoretical Inventory

**Recipe Consumption & Theoretical Inventory — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as storekeeper, supervisor |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRecipes` reads the population and `getCountVariance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `countId` (deepLink), `runId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. A run opened from the list. |
| Route | `/stock-supply/recipe-consumption-theoretical-inventory` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

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
- Client design-board frames: `FnB Board 2.dc.html#fnb-2f`, `FnB Board 5.dc.html#fnb-5c`
- Flow F30 *A count is entered, varied and posted*, step 8: The variance feeds theoretical-against-actual. → **Recipes say 400 portions; the count says 380.** The gap is waste, theft or a wrong recipe, and this is the only place a venue finds out which.
- Flow F85 *Production is planned, costed and released*, step 2: Recipe Consumption & Theoretical Inventory. → **Drawn by the client as FNB-2F.** 2 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-137?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-008`, `BO-105`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-138` Production Execution & Batch Management

**Production Execution & Batch Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 operate, 1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listExpiringBatches` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `runId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/stock-supply/production-execution-batch-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Within days | number field (days) | optional | 7 | — | — | Sends `?withinDays=` to `listExpiringBatches`. | `listExpiringBatches` ?withinDays |
| Search production execution | search field | — | — | — | — | — | — |

**Form: Plan production run** (modal, opened by *Plan production run*; *Plan production run* calls `planProductionRun`, *Cancel* sends nothing)

**Collects what `planProductionRun` sends before it is called.** Required: `id`, `recipeId`, `plannedQuantity`, `status`. Optional: `productionPlanId`, `producingOutletId`, `forOutletIds`, `actualQuantity`, `scheduledFor`, `varianceReason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `planProductionRun` body |
| Recipe `recipeId` | picker: choose a recipe | required | — | — | shows names, sends the id | — | `planProductionRun` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | The station whose prep list this run is on. Copied from the plan line on release, where runs are grouped by station (audit R125 (7)). | `planProductionRun` body |
| Producing outlet `producingOutletId` | picker: choose a producing outlet | optional | — | — | shows names, sends the id | — | `planProductionRun` body |
| For outlets `forOutletIds` | multi-picker: choose for outlets | optional | — | — | — | Where it goes. A central kitchen produces for outlets that did not make it. | `planProductionRun` body |
| Planned quantity `plannedQuantity` | number field | required | — | — | — | — | `planProductionRun` body |
| Actual quantity `actualQuantity` | number field | optional | — | — | — | BL-126. Theoretical against actual is the whole point of recording this. | `planProductionRun` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `planProductionRun` body |
| Status `status` | radio group | required | — | Planned · In progress · Completed · Cancelled | — | — | `planProductionRun` body |
| Variance reason `varianceReason` | text field | optional | — | — | — | — | `planProductionRun` body |

**Form: Complete production run** (modal, opened by *Complete production run*; *Complete production run* calls `completeProductionRun`, *Cancel* sends nothing)

**Collects what `completeProductionRun` sends before it is called.** Required: `actualQuantity`, `recordedAt`. Optional: `varianceReason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Actual quantity `actualQuantity` | number field | required | — | — | — | — | `completeProductionRun` body |
| Variance reason `varianceReason` | text field | optional | — | — | — | — | `completeProductionRun` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `completeProductionRun` body |

Errors to draw in the form: 409 The run is not `inProgress` (states/production-run.yaml). Names its current status.

#### Outputs: what the screen shows and produces

**Shown**

**Every stock batch** (data table, from `listExpiringBatches`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Item | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Batch code | text | — |
| Lot number | text | The supplier's own reference. A recall names a lot number, and an inventory that cannot resolve one has to discard everything. |
| Quantity | 1,234.5 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026 | — |
| Supplier | the name it points at, never the id | — |
| Status | chip: Available, Quarantined, Expired, Recalled, Consumed, Written off | — |

**The selected stock batch** (detail panel, from `listExpiringBatches`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Item | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Batch code | text | — |
| Lot number | text | The supplier's own reference. A recall names a lot number, and an inventory that cannot resolve one has to discard everything. |
| Quantity | 1,234.5 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026 | — |
| Supplier | the name it points at, never the id | — |
| Status | chip: Available, Quarantined, Expired, Recalled, Consumed, Written off | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Plan production run (primary button) | `planProductionRun` POST `/production-runs` | ProductionRun | ProductionRun | — | opens modal first |
| Complete production run (secondary button) | `completeProductionRun` POST `/production-runs/{runId}/complete` | inline | ProductionRun | 409 The run is not `inProgress` (states/production-run.yaml). Names its current status. | opens modal first |

**Data it reads**: `listExpiringBatches` (onLoad, What is about to go out of date)

**Where the user goes next**

- → `BO-105` Stock & Supply: *Stock & Supply*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The production execution batch list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the production execution batch untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No production execution batch yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on withinDays and the production execution batch are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listExpiringBatches` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The run is not `inProgress` (states/production-run.yaml). Names its current status.; 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Permissions

- `planProductionRun` → `PRODUCT_CONFIGURE` (configure) · staff
- `completeProductionRun` → `PRODUCT_CONFIGURE` (configure) · staff
- `listExpiringBatches` → `PRODUCT_VIEW` (read) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listExpiringBatches` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

26 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.8.15 | AI predicts potential food waste and recommends actions. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 5.4.24 | Segment customers automatically. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.27 | Recommend staffing adjustments, ride allocation, and queue balancing. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.36 | The system shall estimate queue wait times using historical and real-time operational data. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 8.9.9 | AI shall identify operational risks, anomalies, congestion, capacity issues, device failures, staffing shortages, and service disruptions and provide recommendations. | Unified Operations Dashboard | CONTRACTED | `requestSuggestion` |
| 15.4.7 | Inventory Optimization - System shall optimize inventory levels. | Inventory Management | CONTRACTED_PARTIAL | `requestSuggestion` |
| 22.2.25 | AI Audience Classification | Marketing & CRM | CONTRACTED | `requestSuggestion` |
| 4.6.36 | Compare theoretical recipe cost versus actual inventory consumption and wastage, highlighting variances and operational inefficiencies. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| … 14 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Production execution & batch management shows planned vs. actual vs. yield quantity and batch losses; wastage/spoilage must be recorded per item. Outlets raise requisitions to replenish from the central warehouse. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-341)*

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-138` · status **notStarted** · provenance generated
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-138?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Plan production run, Complete production run.
- [ ] Every transition is wired: `BO-105`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-139` Wastage, Spoilage, Returns & Write-Off

**Wastage, Spoilage, Returns & Write-Off — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `ORDER_MODIFY` (2 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`recordWaste`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `outletId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/stock-supply/wastage-spoilage-returns-write-off` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

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

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record waste (primary button) | `recordWaste` POST `/outlets/{outletId}/waste` | inline | inline | — | — |

**Where the user goes next**

- → `BO-105` Stock & Supply: *Stock & Supply*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved wastage spoilage returns. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wastage spoilage returns untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wastage spoilage returns configured. The form opens empty and `recordWaste` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_MODIFY`, which `recordWaste` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Permissions

- `recordWaste` → `ORDER_MODIFY` (operate) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `ORDER_MODIFY`, which `recordWaste` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-139?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record waste.
- [ ] Every transition is wired: `BO-105`.
- [ ] Every gated control is gated: `AI_USE`, `ORDER_MODIFY`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-140` Product Availability, 86 & Operational Food Safety

**Product Availability, 86 & Operational Food Safety — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listExpiringBatches` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `itemId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/stock-supply/product-availability-86-operational-food-safet` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Availability is immediate (decided 28 September, audit R110)** — the 86 toggle calls `setItemAvailability` at once; the Save changes step is gone. Reason Other needs a note (audit R222).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Within days | number field (days) | optional | 7 | — | — | Sends `?withinDays=` to `listExpiringBatches`. | `listExpiringBatches` ?withinDays |
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

#### Outputs: what the screen shows and produces

**Shown**

**Every stock batch** (data table, from `listExpiringBatches`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Item | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Batch code | text | — |
| Lot number | text | The supplier's own reference. A recall names a lot number, and an inventory that cannot resolve one has to discard everything. |
| Quantity | 1,234.5 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026 | — |
| Supplier | the name it points at, never the id | — |
| Status | chip: Available, Quarantined, Expired, Recalled, Consumed, Written off | — |

**The selected stock batch** (detail panel, from `listExpiringBatches`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Item | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Batch code | text | — |
| Lot number | text | The supplier's own reference. A recall names a lot number, and an inventory that cannot resolve one has to discard everything. |
| Quantity | 1,234.5 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026 | — |
| Supplier | the name it points at, never the id | — |
| Status | chip: Available, Quarantined, Expired, Recalled, Consumed, Written off | — |

**Data it reads**: `listExpiringBatches` (onLoad, What is about to go out of date)

**Where the user goes next**

- → `BO-105` Stock & Supply: *Stock & Supply*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product availability operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product availability operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product availability operational yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on withinDays and the product availability operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listExpiringBatches` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `setItemAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `listExpiringBatches` → `PRODUCT_VIEW` (read) · staff
- `setTemperatureCheckpoint` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listExpiringBatches` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.9 | The system should be able to allow the back office to limit the sale of a particular item per day or per timeslot.(example: Happy hour time slot based sales). | Bundles and Promotions | CONTRACTED | `setItemAvailability` |
| 4.5.17 | Track expiration dates and generate alerts. | Bundles and Promotions | CONTRACTED | data `StockBatch` |
| 4.5.18 | Track inventory by batch and lot numbers. | Bundles and Promotions | CONTRACTED | data `StockBatch` |
| 6.1.39 | The system should be able to report on aging stocks (comparison against defined/Expiry vs actual). | Retail POS | CONTRACTED | data `StockBatch` |
| 15.1.35 | Batch Number Tracking - System shall support batch tracking. | Inventory Management | CONTRACTED | data `StockBatch` |
| 15.1.36 | Lot Tracking - System shall support lot tracking. | Inventory Management | CONTRACTED | data `StockBatch` |
| 15.1.38 | Expiry Date Tracking - System shall support expiry date tracking. | Inventory Management | CONTRACTED | data `StockBatch` |

#### Client meeting inputs

None names this screen.

Also apply: 2 for P08 · Stock & Supply, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-140` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 412).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-140?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-105`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-141` Operational Alerts, AI Replenishment & Action Center

**Operational Alerts, AI Replenishment & Action Center — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Stock & Supply · wave 2 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PROCUREMENT_REQUEST`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAlerts` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `alertId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/stock-supply/operational-alerts-ai-replenishment-action-cen` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Absorbed BO-472 on 28 September (audit R276)**: Operational Alerts & Exception Center (Games & Rides board 8) called only `listAlerts`, already here; it is retired and BO-464 now opens this screen for the operational exception queue.

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

#### Outputs: what the screen shows and produces

**Shown**

**Every alert** (data table, from `listAlerts`)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listAlerts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `acknowledgeAlert` → `REPORT_VIEW_VENUE` (operate) · staff
- `createRequisition` → `PROCUREMENT_REQUEST` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listAlerts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-141?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Acknowledge alert, Create requisition.
- [ ] Every transition is wired: `BO-105`, `BO-464`.
- [ ] Every gated control is gated: `PROCUREMENT_REQUEST`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
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
"completeProductionRun": {"method":"POST","path":"/production-runs/{runId}/complete","contract":"fnb","summary":"Record what was actually made","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionRun"},
"createInventoryItem": {"method":"POST","path":"/inventory-items","contract":"inventory","summary":"Create an inventory item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateInventoryItemRequest","responds":"InventoryItem"},
"createRequisition": {"method":"POST","path":"/requisitions","contract":"inventory","summary":"Raise a requisition","permission":"PROCUREMENT_REQUEST","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRequisitionRequest","responds":"Requisition"},
"getCountVariance": {"method":"GET","path":"/stock-counts/{countId}/variance","contract":"inventory","summary":"Variance between counted and expected","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CountVariance"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getProductionRun": {"method":"GET","path":"/production-runs/{runId}","contract":"fnb","summary":"One run — its plan, its output, and the gap","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductionRun"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listExpiringBatches": {"method":"GET","path":"/stock-batches/expiring","contract":"inventory","summary":"What is about to go out of date","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"withinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInventoryItems": {"method":"GET","path":"/inventory-items","contract":"inventory","summary":"List inventory items","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"belowReorderPoint","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductionRuns": {"method":"GET","path":"/production-runs","contract":"fnb","summary":"What is being made, and what was","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationKind","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPurchaseOrders": {"method":"GET","path":"/purchase-orders","contract":"inventory","summary":"List purchase orders","permission":"PROCUREMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"supplierId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRecipes": {"method":"GET","path":"/recipes","contract":"fnb","summary":"List recipes","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":"menuItemId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"planProductionRun": {"method":"POST","path":"/production-runs","contract":"fnb","summary":"Plan a batch, for one outlet or several","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductionRun","responds":"ProductionRun"},
"recordWaste": {"method":"POST","path":"/outlets/{outletId}/waste","contract":"fnb","summary":"Record waste","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"setItemAvailability": {"method":"PUT","path":"/menu-items/{itemId}/availability","contract":"fnb","summary":"Mark an item available or eighty-sixed","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"setTemperatureCheckpoint": {"method":"PUT","path":"/food-safety/checkpoints","contract":"fnb","summary":"Define a checkpoint and its safe range","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"TemperatureCheckpoint","responds":"TemperatureCheckpoint"}
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
"InventoryItem": {"x-ticvai-persistence":"inventory.item","allOf":[{"$ref":"#/components/schemas/CreateInventoryItemRequest"},{"type":"object","required":["id","onHand","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"onHand":{"type":"number","description":"Derived from movements. Not directly editable."},"onOrder":{"type":"number"},"inTransit":{"type":"number"},"available":{"type":"number","description":"On-hand minus allocated, where allocated is stock reserved for orders (decided 28 September, audit R171)."},"averageCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lastPurchasePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isBelowReorderPoint":{"type":"boolean"},"hasMovements":{"type":"boolean","description":"True locks costing method and base unit."},"isActive":{"type":"boolean"}}}]},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall"],"x-ticvai-money-valued":["inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductionRun": {"type":"object","x-ticvai-persistence":"fnb.production_run","description":"BL-129. **A central kitchen makes 400 portions at 6am for four outlets**, and nothing modelled that — orders consume stock and no operation produced any.\n**Production converts ingredients into a sellable item**, which is a stock movement in both directions at once, and treating it as two unrelated adjustments loses the yield.\n","required":["id","recipeId","plannedQuantity","status"],"properties":{"id":{"type":"string","format":"uuid"},"recipeId":{"type":"string","format":"uuid"},"productionPlanId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The plan whose release created this run. Null for a run planned directly."},"stationId":{"type":"string","format":"uuid","nullable":true,"description":"**The station whose prep list this run is on.** Copied from the plan line on release, where runs are grouped by station (audit R125 (7)).\n"},"producingOutletId":{"type":"string","format":"uuid"},"forOutletIds":{"type":"array","description":"**Where it goes.** A central kitchen produces for outlets that did not make it.\n","items":{"type":"string","format":"uuid"}},"plannedQuantity":{"type":"number"},"actualQuantity":{"type":"number","nullable":true,"description":"BL-126. **Theoretical against actual is the whole point of recording this.** A recipe says 400 portions from the ingredients issued; the run says how many were made, and the gap is waste, theft or a recipe that is wrong.\n"},"scheduledFor":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["planned","inProgress","completed","cancelled"]},"varianceReason":{"type":"string","nullable":true}}},
"PurchaseOrder": {"x-ticvai-persistence":"inventory.purchase_order + inventory.purchase_order_line","type":"object","required":["id","purchaseOrderNumber","supplierId","status","lines","total","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"purchaseOrderNumber":{"type":"string","readOnly":true,"description":"**Per venue, in sequence** (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for an order with no venue. Proposed format `PO-<venue code>-<sequence, six digits>`, client to correct.\n"},"requisitionId":{"type":"string","format":"uuid","nullable":true,"description":"Null on a blanket order or an RFQ award, which are raised without one."},"quotationId":{"type":"string","format":"uuid","nullable":true,"description":"The quotation selected when the order was raised (`createPurchaseOrder` requires it). **The link that shows the comparison was made**, which `rfqId` alone does not."},"supplierId":{"type":"string","format":"uuid"},"supplierName":{"type":"string"},"kind":{"type":"string","enum":["standard","blanket","release","rfqAward"],"default":"standard","description":"BL-159. **A blanket order is a price and a commitment, not a delivery.** Releases draw against it, and modelling each release as its own purchase order loses the contract that makes the price valid.\n"},"blanketParentId":{"type":"string","format":"uuid","nullable":true,"description":"The blanket order this release draws against — another purchase order, so the same id type."},"contractPriceValidUntil":{"type":"string","format":"date","nullable":true},"rfqId":{"type":"string","format":"uuid","nullable":true,"description":"Where this order came from a quotation round. **Keeping the link is what lets a venue show it took the best of three**, which is usually the procurement rule rather than a preference.\n"},"supplierInvoiceRef":{"type":"string","nullable":true,"description":"BL-123. **Purchase orders and goods receipts both existed — the third leg did not.** A three-way match with two legs is a two-way match, and it is the supplier invoice that carries the price nobody has checked yet.\n"},"matchStatus":{"type":"string","nullable":true,"enum":["unmatched","matched","priceVariance","quantityVariance","bothVariance"],"description":"**The variance kinds are separated because they have different owners** — a price variance is a buyer's problem and a quantity variance is a receiving one.\n"},"status":{"$ref":"#/components/schemas/PurchaseOrderStatus"},"deliverToLocationId":{"type":"string","format":"uuid","nullable":true,"description":"**Scoped 31 August.** A purchase order is raised by somebody, for somewhere, and carried neither. `requisitionId` reaches a venue through a join, but **a purchase order raised without a requisition — a blanket order, an RFQ award — had no scope at all**, so nothing could answer *whose budget is this* without guessing.\n\n**`deliverToLocationId` is separate from `venueId` on purpose.** A tenant buying centrally and delivering to three venues is one order and three destinations; collapsing them would force one order per venue and lose the volume the tenant negotiated for."},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"orderedQuantity":{"type":"number"},"receivedQuantity":{"type":"number"},"outstandingQuantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"The selected quotation line's price, kept beside `unitPrice` (audit R171)."},"priceOverrideReason":{"type":"string","nullable":true,"description":"Why `unitPrice` differs from `quotedUnitPrice` (audit R171)."},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expectedDelivery":{"type":"string","format":"date"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"supplierReference":{"type":"string","nullable":true,"description":"The supplier's own order reference, from `acknowledgePurchaseOrder`."},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Null is the supplier performance figure** — goods arriving against an order never acknowledged."},"closeShortReason":{"type":"string","nullable":true,"description":"Why the balance was written off, from `closePurchaseOrderShort`."},"cancelReason":{"type":"string","nullable":true,"description":"From `cancelPurchaseOrder`."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The pending approval request raised by `cancelPurchaseOrder` or `closePurchaseOrderShort` (kinds `purchaseOrderCancel`, `purchaseOrderShortClose`; audit R144). Null when none is open."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Which venue is buying. **Null on a tenant-level order** — see `deliverToLocationId`."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Present on every order regardless of whether a venue is named, because a tenant-level order still belongs to a tenant."}}},
"PurchaseOrderStatus": {"type":"string","enum":["raised","sent","acknowledged","partiallyReceived","received","closedShort","cancelled"]},
"Recipe": {"x-ticvai-persistence":"fnb.recipe + fnb.recipe_ingredient","type":"object","required":["menuItemId","ingredients"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"yield":{"type":"number","minimum":0,"description":"Portions produced by one execution."},"ingredients":{"type":"array","minItems":1,"items":{"type":"object","required":["inventoryItemId","quantity","unit"],"properties":{"inventoryItemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"},"isOptional":{"type":"boolean","default":false}}}},"costPerPortion":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Computed, never entered** (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided by `yield`. Recomputed when the recipe or an ingredient cost changes.\n"}}},
"Requisition": {"x-ticvai-persistence":"inventory.requisition + inventory.requisition_line","type":"object","required":["id","requisitionNumber","venueId","status","lines","raisedByPrincipalId","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"requisitionNumber":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"costCenterId":{"type":"string","format":"uuid","nullable":true},"justification":{"type":"string","nullable":true},"status":{"$ref":"#/components/schemas/RequisitionStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"requestedQuantity":{"type":"number"},"suggestedQuantity":{"type":"number","nullable":true,"description":"**Kept, never overwritten** (`updateRequisitionLines`). Null on a line nobody suggested.\n"},"approvedQuantity":{"type":"number","nullable":true},"orderedQuantity":{"type":"number","nullable":true},"unit":{"type":"string"},"reason":{"type":"string","nullable":true,"description":"Why the requested quantity differs from the suggestion."},"note":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"estimatedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"raisedByPrincipalId":{"type":"string","format":"uuid"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvalNote":{"type":"string","nullable":true},"requiredBy":{"type":"string","format":"date"},"createdAt":{"type":"string","format":"date-time"},"approvedAt":{"type":"string","format":"date-time","nullable":true},"rejectionReason":{"type":"string","nullable":true,"description":"From `rejectRequisition`. What the requester reads before copying it into a new draft."},"rejectedAt":{"type":"string","format":"date-time","nullable":true},"returnQuestion":{"type":"string","nullable":true,"description":"From `returnRequisition`. What the requester must answer before resubmitting."},"returnedAt":{"type":"string","format":"date-time","nullable":true},"cancelReason":{"type":"string","nullable":true,"description":"From `cancelRequisition`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true}}},
"RequisitionStatus": {"type":"string","enum":["draft","pendingApproval","approved","rejected","returnedForInfo","ordered","closed","cancelled"]},
"StockBatch": {"type":"object","x-ticvai-persistence":"inventory.stock_batch","description":"BL-122. **`isPerishable` and `shelfLifeDays` are on the item, so a shelf life is declared and never instantiated.** Two deliveries of the same milk arriving a week apart are one stock level with one implied expiry, and the older one is invisible.\n**A batch is the instance that actually expires.** Without it, first-expiry-first-out is not computable and a venue discovers the problem by smell.\n","required":["id","itemId","locationId","quantity","receivedAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"batchCode":{"type":"string","nullable":true},"lotNumber":{"type":"string","nullable":true,"description":"The supplier's own reference. **A recall names a lot number**, and an inventory that cannot resolve one has to discard everything.\n"},"quantity":{"type":"number"},"receivedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date","nullable":true},"supplierId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["available","quarantined","expired","recalled","consumed","written-off"]}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"TemperatureCheckpoint": {"type":"object","x-ticvai-persistence":"fnb.temperature_checkpoint","description":"**A unit that gets read, and the range it is required to hold.** The entity `TemperatureLog.checkPointId` has always been required to name and that nothing defined.\n**The safe range belongs here and is snapshotted onto each reading**, so that a range revised in March cannot silently re-judge a reading taken in January.","required":["id","kind","label","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["fridge","freezer","holdingCabinet","blastChiller","coreProbe","delivery","displayCounter","ambient"],"description":"The same closed set `TemperatureLog.checkPointKind` records."},"label":{"type":"string","description":"**What the person reading it calls it** — *Walk-in 2*, *Dessert counter*. A checkpoint identified only by a uuid is one somebody will read the wrong unit for."},"minCelsius":{"type":"number","nullable":true},"maxCelsius":{"type":"number","nullable":true,"description":"**Null at either end is legitimate** — a core probe has a floor and no ceiling. Both null is not, and is what an unconfigured checkpoint looks like."},"checkFrequencyMinutes":{"type":"integer","nullable":true,"description":"**How often it must be read.** The gap this leaves open otherwise is the one an inspector finds: not a bad reading, but a missing one."},"requiresCorrectiveActionOnBreach":{"type":"boolean"},"isActive":{"type":"boolean"},"scopePath":{"type":"string"}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}}
}
```
