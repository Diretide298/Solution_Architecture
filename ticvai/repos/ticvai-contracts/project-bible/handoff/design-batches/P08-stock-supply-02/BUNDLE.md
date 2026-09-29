# P08-stock-supply-02 — P08 · Stock & Supply (2 of 2)

**6 screens · 18 operations · 19 schemas · 7 permissions**

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
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ORDER_MODIFY, PROCUREMENT_REQUEST, PROCUREMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-105` | Stock & Supply | listDetail | 5 | 1 | — |
| `BO-137` | Recipe Consumption & Theoretical Inventory | listDetail | 4 | 0 | — |
| `BO-138` | Production Execution & Batch Management | listDetail | 3 | 2 | — |
| `BO-139` | Wastage, Spoilage, Returns & Write-Off | configEditor | 1 | 0 | — |
| `BO-140` | Product Availability, 86 & Operational Food Safety | listDetail | 3 | 1 | — |
| `BO-141` | Operational Alerts, AI Replenishment & Action Center | listDetail | 3 | 2 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-105",
  "name": "Stock & Supply",
  "module": "Stock & Supply",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/stock-supply",
   "component": "apps/venue-management-web/src/routes/home/StockSupplyList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-049",
    "BO-050",
    "BO-051",
    "BO-052",
    "BO-078",
    "BO-079",
    "BO-080",
    "BO-081",
    "BO-082",
    "BO-083",
    "BO-137",
    "BO-138",
    "BO-139",
    "BO-140",
    "BO-141"
   ],
   "transitions": [
    {
     "to": "BO-049",
     "trigger": "Stock Levels",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-049 declares entryState.params itemId and BO-105 holds itemId, so an edge into it carries them"
    },
    {
     "to": "BO-052",
     "trigger": "Goods Receipt",
     "carries": [
      "purchaseOrderId"
     ],
     "provenance": "derived — BO-052 declares entryState.params purchaseOrderId, receiptId, transferId and BO-105 holds purchaseOrderId, so an edge into it carries them"
    },
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "carries": [
      "requisitionId"
     ],
     "provenance": "derived — BO-078 declares entryState.params requisitionId and BO-105 holds requisitionId, so an edge into it carries them"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "provenance": "derived — BO-079 declares entryState.params countId and BO-105 holds none of them, so the edge carries nothing and BO-079 opens cold"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "provenance": "derived — BO-080 declares entryState.params transferId and BO-105 holds none of them, so the edge carries nothing and BO-080 opens cold"
    },
    {
     "to": "BO-081",
     "trigger": "Inventory Items",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-081 declares entryState.params itemId and BO-105 holds itemId, so an edge into it carries them"
    },
    {
     "to": "BO-083",
     "trigger": "Suppliers",
     "carries": [
      "supplierId"
     ],
     "provenance": "derived — BO-083 declares entryState.params supplierId and BO-105 holds supplierId, so an edge into it carries them"
    },
    {
     "to": "BO-137",
     "trigger": "Recipe Consumption & Theoretical Inventory",
     "provenance": "derived — BO-137 declares entryState.params countId, runId and BO-105 holds none of them, so the edge carries nothing and BO-137 opens cold"
    },
    {
     "to": "BO-138",
     "trigger": "Production Execution & Batch Management",
     "provenance": "derived — BO-138 declares entryState.params runId and BO-105 holds none of them, so the edge carries nothing and BO-138 opens cold"
    },
    {
     "to": "BO-139",
     "trigger": "Wastage, Spoilage, Returns & Write-Off",
     "provenance": "derived — BO-139 declares entryState.params outletId and BO-105 holds none of them, so the edge carries nothing and BO-139 opens cold"
    },
    {
     "to": "BO-140",
     "trigger": "Product Availability, 86 & Operational Food Safety",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-140 declares entryState.params itemId and BO-105 holds itemId, so an edge into it carries them"
    },
    {
     "to": "BO-141",
     "trigger": "Operational Alerts, AI Replenishment & Action Center",
     "provenance": "derived — BO-141 declares entryState.params alertId and BO-105 holds none of them, so the edge carries nothing and BO-141 opens cold"
    },
    {
     "to": "BO-051",
     "trigger": "Purchase Orders",
     "provenance": "moved 29 September, VM close-out: purchase orders sit in Stock & Supply beside Goods Receipt; BO-051 opens its list without an id",
     "carries": [
      "purchaseOrderId"
     ]
    }
   ]
  },
  "notes": "Section landing. **9 screens reach the entry point through here** — before 20 August they reached it through nothing.",
  "density": "compact",
  "boardFrames": [
   "Inventory Board 7.dc.html#inv-7a"
  ],
  "pattern": "listDetail",
  "patternReason": "`listInventoryItems` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in stock & supply.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listInventoryItems",
       "notes": "Sends `?venueId=` to `listInventoryItems`.",
       "provenance": "contract inventory.yaml GET /inventory-items"
      },
      {
       "kind": "textField",
       "label": "Category id",
       "operation": "listInventoryItems",
       "notes": "Sends `?categoryId=` to `listInventoryItems`.",
       "provenance": "contract inventory.yaml GET /inventory-items"
      },
      {
       "kind": "toggle",
       "label": "Below reorder point",
       "operation": "listInventoryItems",
       "notes": "Sends `?belowReorderPoint=` to `listInventoryItems`.",
       "provenance": "contract inventory.yaml GET /inventory-items"
      },
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listInventoryItems",
       "notes": "Sends `?search=` to `listInventoryItems`.",
       "provenance": "contract inventory.yaml GET /inventory-items"
      },
      {
       "kind": "dataTable",
       "label": "Every inventory",
       "bindsTo": "InventoryItem",
       "columns": [
        "InventoryItem.sku",
        "InventoryItem.barcode",
        "InventoryItem.name",
        "InventoryItem.venueId",
        "InventoryItem.categoryId",
        "InventoryItem.baseUnit",
        "InventoryItem.purchaseUnit",
        "InventoryItem.purchaseUnitFactor",
        "InventoryItem.costingMethod",
        "InventoryItem.reorderPoint",
        "InventoryItem.reorderQuantity",
        "InventoryItem.parLevel"
       ],
       "operation": "listInventoryItems",
       "provenance": "contract inventory.yaml GET /inventory-items"
      },
      {
       "kind": "dataTable",
       "label": "Every purchase order",
       "bindsTo": "PurchaseOrder",
       "columns": [
        "PurchaseOrder.id",
        "PurchaseOrder.purchaseOrderNumber",
        "PurchaseOrder.requisitionId",
        "PurchaseOrder.quotationId",
        "PurchaseOrder.supplierId",
        "PurchaseOrder.supplierName",
        "PurchaseOrder.kind",
        "PurchaseOrder.blanketParentId",
        "PurchaseOrder.contractPriceValidUntil",
        "PurchaseOrder.rfqId",
        "PurchaseOrder.supplierInvoiceRef",
        "PurchaseOrder.matchStatus"
       ],
       "operation": "listPurchaseOrders",
       "provenance": "contract inventory.yaml GET /purchase-orders"
      },
      {
       "kind": "metricTile",
       "label": "Takings and admissions today",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.code",
        "KpiValue.name",
        "KpiValue.value",
        "KpiValue.period",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "**Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "9 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search stock & supply",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inventory",
       "bindsTo": "InventoryItem",
       "columns": [
        "InventoryItem.sku",
        "InventoryItem.barcode",
        "InventoryItem.name",
        "InventoryItem.venueId",
        "InventoryItem.categoryId",
        "InventoryItem.baseUnit",
        "InventoryItem.purchaseUnit",
        "InventoryItem.purchaseUnitFactor",
        "InventoryItem.costingMethod",
        "InventoryItem.reorderPoint",
        "InventoryItem.reorderQuantity",
        "InventoryItem.parLevel",
        "InventoryItem.preferredSupplierId",
        "InventoryItem.allowNegativeStock",
        "InventoryItem.isPerishable",
        "InventoryItem.shelfLifeDays"
       ],
       "operation": "listInventoryItems",
       "provenance": "contract inventory.yaml GET /inventory-items"
      },
      {
       "kind": "detailPanel",
       "label": "The venue settings",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.currencyCode",
        "VenueSettings.currencyScale",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.biometrics",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create inventory item",
       "operation": "createInventoryItem",
       "provenance": "contract inventory.yaml POST /inventory-items"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in stock & supply yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for stock & supply. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Today's takings and admissions tiles — `kpiCodes=takings,admissions`, period defaulting to today (decided 28 September, audit R283)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listInventoryItems",
    "contract": "inventory",
    "purpose": "Stock on hand",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPurchaseOrders",
    "contract": "inventory",
    "purpose": "Orders placed with suppliers",
    "trigger": "onLoad"
   },
   {
    "operationId": "createInventoryItem",
    "contract": "inventory",
    "purpose": "Add an item",
    "trigger": "onAction",
    "invalidates": [
     "listInventoryItems"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
   "preloaded": [
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-105"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateInventoryItem",
    "component": "modal",
    "trigger": "Create inventory item",
    "body": "**Collects what `createInventoryItem` sends before it is called.** Required: `sku`, `name`, `venueId`, `baseUnit`, `costingMethod`. Optional: `barcode`, `categoryId`, `purchaseUnit`, `purchaseUnitFactor`, `reorderPoint`, `reorderQuantity`, `parLevel`, `preferredSupplierId`, `allowNegativeStock`, `isPerishable`, `shelfLifeDays`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateInventoryItemRequest",
    "confirm": {
     "label": "Create inventory item",
     "operation": "createInventoryItem"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "sku",
      "name",
      "venueId",
      "baseUnit",
      "costingMethod",
      "barcode",
      "categoryId",
      "purchaseUnit",
      "purchaseUnitFactor",
      "reorderPoint",
      "reorderQuantity",
      "parLevel",
      "preferredSupplierId",
      "allowNegativeStock",
      "isPerishable",
      "shelfLifeDays"
     ]
    },
    "provenance": "contract inventory.yaml POST /inventory-items"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-137",
  "name": "Recipe Consumption & Theoretical Inventory",
  "module": "Stock & Supply",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/stock-supply/recipe-consumption-theoretical-inventory",
   "component": "apps/venue-management-web/src/routes/ops/RecipeConsumptionTheoreticalInventoryList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-079",
    "BO-105",
    "BO-136"
   ],
   "exitTo": [
    "BO-008",
    "BO-105"
   ],
   "inferred": false,
   "notes": "**Returns to BO-105.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "flow F85 step 2→3"
    },
    {
     "to": "BO-105",
     "trigger": "Stock & Supply",
     "provenance": "derived — BO-105 declares entryState.params  and BO-137 holds none of them, so the edge carries nothing and BO-105 opens cold"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2f",
   "FnB Board 5.dc.html#fnb-5c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listRecipes` reads the population and `getCountVariance` reads one of them — list, select, act",
  "purpose": "Recipe Consumption & Theoretical Inventory — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listRecipes",
       "notes": "Sends `?search=` to `listRecipes`.",
       "provenance": "contract fnb.yaml GET /recipes"
      },
      {
       "kind": "textField",
       "label": "Menu item id",
       "operation": "listRecipes",
       "notes": "Sends `?menuItemId=` to `listRecipes`.",
       "provenance": "contract fnb.yaml GET /recipes"
      },
      {
       "kind": "dataTable",
       "label": "Every recipe",
       "bindsTo": "Recipe",
       "columns": [
        "Recipe.menuItemId",
        "Recipe.yield",
        "Recipe.ingredients",
        "Recipe.costPerPortion"
       ],
       "operation": "listRecipes",
       "provenance": "contract fnb.yaml GET /recipes"
      },
      {
       "kind": "dataTable",
       "label": "Every production run",
       "bindsTo": "ProductionRun",
       "columns": [
        "ProductionRun.id",
        "ProductionRun.recipeId",
        "ProductionRun.productionPlanId",
        "ProductionRun.producingOutletId",
        "ProductionRun.forOutletIds",
        "ProductionRun.plannedQuantity",
        "ProductionRun.actualQuantity",
        "ProductionRun.scheduledFor",
        "ProductionRun.status",
        "ProductionRun.varianceReason"
       ],
       "operation": "listProductionRuns",
       "provenance": "contract fnb.yaml GET /production-runs"
      },
      {
       "kind": "searchField",
       "label": "Search recipe consumption",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recipe",
       "bindsTo": "Recipe",
       "columns": [
        "Recipe.menuItemId",
        "Recipe.yield",
        "Recipe.ingredients",
        "Recipe.costPerPortion"
       ],
       "operation": "listRecipes",
       "provenance": "contract fnb.yaml GET /recipes"
      },
      {
       "kind": "detailPanel",
       "label": "The production run",
       "bindsTo": "ProductionRun",
       "columns": [
        "ProductionRun.id",
        "ProductionRun.recipeId",
        "ProductionRun.productionPlanId",
        "ProductionRun.producingOutletId",
        "ProductionRun.forOutletIds",
        "ProductionRun.plannedQuantity",
        "ProductionRun.actualQuantity",
        "ProductionRun.scheduledFor",
        "ProductionRun.status",
        "ProductionRun.varianceReason"
       ],
       "operation": "getProductionRun",
       "provenance": "contract fnb.yaml GET /production-runs/{runId}"
      },
      {
       "kind": "detailPanel",
       "label": "The count variance",
       "bindsTo": "CountVariance",
       "columns": [
        "CountVariance.countId",
        "CountVariance.totalVarianceValue",
        "CountVariance.exceptionCount",
        "CountVariance.lines"
       ],
       "operation": "getCountVariance",
       "provenance": "contract inventory.yaml GET /stock-counts/{countId}/variance"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recipe consumption theoretical list.",
   "error": "Could not load. Names which read failed and leaves the recipe consumption theoretical untouched.",
   "emptyFirstRun": "No recipe consumption theoretical yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on search, menuItemId and the recipe consumption theoretical are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listRecipes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecipes",
    "contract": "fnb",
    "purpose": "List recipes",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCountVariance",
    "contract": "inventory",
    "purpose": "Variance between counted and expected",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductionRuns",
    "contract": "fnb",
    "purpose": "What is being made, and what was",
    "trigger": "onLoad"
   },
   {
    "operationId": "getProductionRun",
    "contract": "fnb",
    "purpose": "One run — its plan, its output, and the gap",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "countId",
     "from": "deepLink"
    },
    {
     "name": "runId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first. A run opened from the list.",
   "preloaded": [
    "Recipe.menuItemId",
    "Recipe.yield",
    "Recipe.ingredients",
    "Recipe.costPerPortion"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-137",
   "derivedFrom": "wireframes/reference/FnB Board 2.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-138",
  "name": "Production Execution & Batch Management",
  "module": "Stock & Supply",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/stock-supply/production-execution-batch-management",
   "component": "apps/venue-management-web/src/routes/ops/ProductionExecutionBatchManagementList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-105"
   ],
   "exitTo": [
    "BO-105"
   ],
   "inferred": false,
   "notes": "**Returns to BO-105.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-105",
     "trigger": "Stock & Supply",
     "provenance": "derived — BO-105 declares entryState.params  and BO-138 holds none of them, so the edge carries nothing and BO-105 opens cold"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listExpiringBatches` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Production Execution & Batch Management — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "numberField",
       "label": "Within days",
       "operation": "listExpiringBatches",
       "notes": "Sends `?withinDays=` to `listExpiringBatches`.",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      },
      {
       "kind": "dataTable",
       "label": "Every stock batch",
       "bindsTo": "StockBatch",
       "columns": [
        "StockBatch.id",
        "StockBatch.itemId",
        "StockBatch.locationId",
        "StockBatch.batchCode",
        "StockBatch.lotNumber",
        "StockBatch.quantity",
        "StockBatch.receivedAt",
        "StockBatch.expiresAt",
        "StockBatch.supplierId",
        "StockBatch.status"
       ],
       "operation": "listExpiringBatches",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      },
      {
       "kind": "searchField",
       "label": "Search production execution",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected stock batch",
       "bindsTo": "StockBatch",
       "columns": [
        "StockBatch.id",
        "StockBatch.itemId",
        "StockBatch.locationId",
        "StockBatch.batchCode",
        "StockBatch.lotNumber",
        "StockBatch.quantity",
        "StockBatch.receivedAt",
        "StockBatch.expiresAt",
        "StockBatch.supplierId",
        "StockBatch.status"
       ],
       "operation": "listExpiringBatches",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Plan production run",
       "operation": "planProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete production run",
       "operation": "completeProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs/{runId}/complete"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The production execution batch list.",
   "error": "Could not load. Names which read failed and leaves the production execution batch untouched.",
   "emptyFirstRun": "No production execution batch yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on withinDays and the production execution batch are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listExpiringBatches` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "planProductionRun",
    "contract": "fnb",
    "purpose": "Plan a batch, for one outlet or several",
    "trigger": "onAction",
    "invalidates": [
     "listExpiringBatches"
    ]
   },
   {
    "operationId": "completeProductionRun",
    "contract": "fnb",
    "purpose": "Record what was actually made",
    "trigger": "onAction",
    "invalidates": [
     "listExpiringBatches"
    ]
   },
   {
    "operationId": "listExpiringBatches",
    "contract": "inventory",
    "purpose": "What is about to go out of date",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "runId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first.",
   "preloaded": [
    "StockBatch.id",
    "StockBatch.itemId",
    "StockBatch.locationId",
    "StockBatch.batchCode",
    "StockBatch.lotNumber"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-138"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPlanProductionRun",
    "component": "modal",
    "trigger": "Plan production run",
    "body": "**Collects what `planProductionRun` sends before it is called.** Required: `id`, `recipeId`, `plannedQuantity`, `status`. Optional: `productionPlanId`, `producingOutletId`, `forOutletIds`, `actualQuantity`, `scheduledFor`, `varianceReason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ProductionRun",
    "confirm": {
     "label": "Plan production run",
     "operation": "planProductionRun"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "recipeId",
      "plannedQuantity",
      "status",
      "productionPlanId",
      "producingOutletId",
      "forOutletIds",
      "actualQuantity",
      "scheduledFor",
      "varianceReason"
     ]
    },
    "provenance": "contract fnb.yaml POST /production-runs"
   },
   {
    "id": "formCompleteProductionRun",
    "component": "modal",
    "trigger": "Complete production run",
    "body": "**Collects what `completeProductionRun` sends before it is called.** Required: `actualQuantity`, `recordedAt`. Optional: `varianceReason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Complete production run",
     "operation": "completeProductionRun"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "actualQuantity",
      "recordedAt",
      "varianceReason"
     ]
    },
    "provenance": "contract fnb.yaml POST /production-runs/{runId}/complete"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-139",
  "name": "Wastage, Spoilage, Returns & Write-Off",
  "module": "Stock & Supply",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/stock-supply/wastage-spoilage-returns-write-off",
   "component": "apps/venue-management-web/src/routes/ops/WastageSpoilageReturnsWriteOffList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-105"
   ],
   "exitTo": [
    "BO-105"
   ],
   "inferred": false,
   "notes": "**Returns to BO-105.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-105",
     "trigger": "Stock & Supply",
     "provenance": "derived — BO-105 declares entryState.params  and BO-139 holds none of them, so the edge carries nothing and BO-105 opens cold"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "boardFrames": [
   "Inventory Board 3.dc.html#inv-3g",
   "Inventory Board 3.dc.html#inv-3j"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`recordWaste`) and no read of a population — it is settings, not a list",
  "purpose": "Wastage, Spoilage, Returns & Write-Off — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Record waste",
       "operation": "recordWaste",
       "provenance": "contract fnb.yaml POST /outlets/{outletId}/waste"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search wastage, spoilage, returns",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Id",
       "operation": "recordWaste",
       "notes": "Required.",
       "provenance": "contract fnb.yaml POST /outlets/{outletId}/waste"
      },
      {
       "kind": "multiSelect",
       "label": "Lines",
       "operation": "recordWaste",
       "notes": "Required.",
       "provenance": "contract fnb.yaml POST /outlets/{outletId}/waste"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "operation": "recordWaste",
       "notes": "Required.",
       "provenance": "contract fnb.yaml POST /outlets/{outletId}/waste"
      },
      {
       "kind": "datePicker",
       "label": "Recorded at",
       "operation": "recordWaste",
       "notes": "Required.",
       "provenance": "contract fnb.yaml POST /outlets/{outletId}/waste"
      },
      {
       "kind": "textField",
       "label": "Note",
       "operation": "recordWaste",
       "provenance": "contract fnb.yaml POST /outlets/{outletId}/waste"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved wastage spoilage returns.",
   "error": "Could not load. Names which read failed and leaves the wastage spoilage returns untouched.",
   "emptyFirstRun": "No wastage spoilage returns configured. The form opens empty and `recordWaste` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_MODIFY`, which `recordWaste` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordWaste",
    "contract": "fnb",
    "purpose": "Record waste",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "outletId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-139"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-140",
  "name": "Product Availability, 86 & Operational Food Safety",
  "module": "Stock & Supply",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/stock-supply/product-availability-86-operational-food-safet",
   "component": "apps/venue-management-web/src/routes/ops/ProductAvailability86OperationalFoodSaList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-105"
   ],
   "exitTo": [
    "BO-105"
   ],
   "inferred": false,
   "notes": "**Returns to BO-105.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-105",
     "trigger": "Stock & Supply",
     "provenance": "derived — BO-105 declares entryState.params  and BO-140 holds none of them, so the edge carries nothing and BO-105 opens cold"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Availability is immediate (decided 28 September, audit R110)** — the 86 toggle calls `setItemAvailability` at once; the Save changes step is gone. Reason Other needs a note (audit R222).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listExpiringBatches` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Product Availability, 86 & Operational Food Safety — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "numberField",
       "label": "Within days",
       "operation": "listExpiringBatches",
       "notes": "Sends `?withinDays=` to `listExpiringBatches`.",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      },
      {
       "kind": "dataTable",
       "label": "Every stock batch",
       "bindsTo": "StockBatch",
       "columns": [
        "StockBatch.id",
        "StockBatch.itemId",
        "StockBatch.locationId",
        "StockBatch.batchCode",
        "StockBatch.lotNumber",
        "StockBatch.quantity",
        "StockBatch.receivedAt",
        "StockBatch.expiresAt",
        "StockBatch.supplierId",
        "StockBatch.status"
       ],
       "operation": "listExpiringBatches",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      },
      {
       "kind": "searchField",
       "label": "Search product availability, 86",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected stock batch",
       "bindsTo": "StockBatch",
       "columns": [
        "StockBatch.id",
        "StockBatch.itemId",
        "StockBatch.locationId",
        "StockBatch.batchCode",
        "StockBatch.lotNumber",
        "StockBatch.quantity",
        "StockBatch.receivedAt",
        "StockBatch.expiresAt",
        "StockBatch.supplierId",
        "StockBatch.status"
       ],
       "operation": "listExpiringBatches",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "toggle",
       "label": "Available",
       "operation": "setItemAvailability",
       "notes": "**Takes effect immediately** (decided 28 September, audit R110) — switching an item off (86) or back on calls `setItemAvailability` at once and every terminal in the outlet follows; there is no Save changes step. Switching off asks only for the reason.",
       "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product availability operational list.",
   "error": "Could not load. Names which read failed and leaves the product availability operational untouched.",
   "emptyFirstRun": "No product availability operational yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on withinDays and the product availability operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listExpiringBatches` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setItemAvailability",
    "contract": "fnb",
    "purpose": "Mark an item available or eighty-sixed",
    "trigger": "onAction",
    "invalidates": [
     "listExpiringBatches"
    ]
   },
   {
    "operationId": "listExpiringBatches",
    "contract": "inventory",
    "purpose": "What is about to go out of date",
    "trigger": "onLoad"
   },
   {
    "operationId": "setTemperatureCheckpoint",
    "contract": "fnb",
    "purpose": "Define a temperature checkpoint and its safe range",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "itemId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first.",
   "preloaded": [
    "StockBatch.id",
    "StockBatch.itemId",
    "StockBatch.locationId",
    "StockBatch.batchCode",
    "StockBatch.lotNumber"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-140"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetItemAvailability",
    "component": "modal",
    "trigger": "Available",
    "body": "**The reason prompt when an item is switched off (86); confirming it is the call** — nothing waits for a later save (decided 28 September, audit R110). `isAvailable` and `recordedAt` come from the toggle. Optional: `reason` (soldOut, ingredientUnavailable, equipmentDown, seasonal, other), `note`, `restoreAt`. **Choosing Other makes the note required** — the prompt will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Switching an item back on sends at once with no prompt. Dismissing leaves the item as it was.",
    "confirm": {
     "label": "86 now",
     "operation": "setItemAvailability"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "note",
      "restoreAt"
     ]
    },
    "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-141",
  "name": "Operational Alerts, AI Replenishment & Action Center",
  "module": "Stock & Supply",
  "requiresModule": "analytics",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/stock-supply/operational-alerts-ai-replenishment-action-cen",
   "component": "apps/venue-management-web/src/routes/ops/OperationalAlertsAiReplenishmentActionList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-105",
    "BO-464"
   ],
   "exitTo": [
    "BO-105",
    "BO-464"
   ],
   "inferred": false,
   "notes": "**Returns to BO-105.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-105",
     "trigger": "Stock & Supply",
     "provenance": "derived — BO-105 declares entryState.params  and BO-141 holds none of them, so the edge carries nothing and BO-105 opens cold"
    },
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "inherited from BO-472 when it was merged here, 28 September (audit R276)",
     "back": true
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Absorbed BO-472 on 28 September (audit R276)**: Operational Alerts & Exception Center (Games & Rides board 8) called only `listAlerts`, already here; it is retired and BO-464 now opens this screen for the operational exception queue.",
  "density": "compact",
  "boardFrames": [
   "Inventory Board 4.dc.html#inv-4g",
   "Inventory Board 7.dc.html#inv-7c",
   "Inventory Board 1.dc.html#inv-10"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAlerts` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Operational Alerts, AI Replenishment & Action Center — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listAlerts",
       "notes": "Sends `?status=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Severity",
       "operation": "listAlerts",
       "notes": "Sends `?severity=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listAlerts",
       "notes": "Sends `?workstationId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listAlerts",
       "notes": "Sends `?shiftId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Item id",
       "operation": "listAlerts",
       "notes": "Sends `?itemId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "dataTable",
       "label": "Every alert",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "searchField",
       "label": "Search operational alerts, ai replenishment",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected alert",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Acknowledge alert",
       "operation": "acknowledgeAlert",
       "provenance": "contract reporting.yaml POST /alerts/{alertId}/acknowledge"
      },
      {
       "kind": "secondaryButton",
       "label": "Create requisition",
       "operation": "createRequisition",
       "permission": "PROCUREMENT_REQUEST",
       "provenance": "contract inventory.yaml POST /requisitions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational alerts replenishment list.",
   "error": "Could not load. Names which read failed and leaves the operational alerts replenishment untouched.",
   "emptyFirstRun": "No operational alerts replenishment yet. Offers Create requisition (`createRequisition`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, severity, workstationId, shiftId, itemId and the operational alerts replenishment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listAlerts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "acknowledgeAlert",
    "contract": "reporting",
    "purpose": "Take responsibility for it",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "createRequisition",
    "contract": "inventory",
    "purpose": "Raise a requisition",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "alertId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first.",
   "preloaded": [
    "Alert.id",
    "Alert.ruleId",
    "Alert.raisedAt",
    "Alert.severity",
    "Alert.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-141"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAcknowledgeAlert",
    "component": "modal",
    "trigger": "Acknowledge alert",
    "body": "**Collects what `acknowledgeAlert` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Acknowledge alert",
     "operation": "acknowledgeAlert"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "note"
     ]
    },
    "provenance": "contract reporting.yaml POST /alerts/{alertId}/acknowledge"
   },
   {
    "id": "formCreateRequisition",
    "component": "modal",
    "trigger": "Create requisition",
    "body": "**Collects what `createRequisition` sends before it is called.** Required: `id`, `venueId`, `lines`, `requiredBy`. Optional: `departmentId`, `costCenterId`, `justification`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateRequisitionRequest",
    "confirm": {
     "label": "Create requisition",
     "operation": "createRequisition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "lines",
      "requiredBy",
      "departmentId",
      "costCenterId",
      "justification"
     ]
    },
    "provenance": "contract inventory.yaml POST /requisitions"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "acknowledgeAlert": {
  "method": "POST",
  "path": "/alerts/{alertId}/acknowledge",
  "contract": "reporting",
  "summary": "Mark it seen",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Alert"
 },
 "completeProductionRun": {
  "method": "POST",
  "path": "/production-runs/{runId}/complete",
  "contract": "fnb",
  "summary": "Record what was actually made",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ProductionRun"
 },
 "createInventoryItem": {
  "method": "POST",
  "path": "/inventory-items",
  "contract": "inventory",
  "summary": "Create an inventory item",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateInventoryItemRequest",
  "responds": "InventoryItem"
 },
 "createRequisition": {
  "method": "POST",
  "path": "/requisitions",
  "contract": "inventory",
  "summary": "Raise a requisition",
  "permission": "PROCUREMENT_REQUEST",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateRequisitionRequest",
  "responds": "Requisition"
 },
 "getCountVariance": {
  "method": "GET",
  "path": "/stock-counts/{countId}/variance",
  "contract": "inventory",
  "summary": "Variance between counted and expected",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CountVariance"
 },
 "getKpiValues": {
  "method": "GET",
  "path": "/kpi-values",
  "contract": "reporting",
  "summary": "Current values, against target, with movement",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kpiIds",
    "in": "query",
    "required": null
   },
   {
    "name": "kpiCodes",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiValue"
 },
 "getProductionRun": {
  "method": "GET",
  "path": "/production-runs/{runId}",
  "contract": "fnb",
  "summary": "One run — its plan, its output, and the gap",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProductionRun"
 },
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "listAlerts": {
  "method": "GET",
  "path": "/alerts",
  "contract": "reporting",
  "summary": "What is currently wrong",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "severity",
    "in": "query",
    "required": null
   },
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "itemId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Alert"
 },
 "listExpiringBatches": {
  "method": "GET",
  "path": "/stock-batches/expiring",
  "contract": "inventory",
  "summary": "What is about to go out of date",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "withinDays",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listInventoryItems": {
  "method": "GET",
  "path": "/inventory-items",
  "contract": "inventory",
  "summary": "List inventory items",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "belowReorderPoint",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listProductionRuns": {
  "method": "GET",
  "path": "/production-runs",
  "contract": "fnb",
  "summary": "What is being made, and what was",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "locationKind",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listPurchaseOrders": {
  "method": "GET",
  "path": "/purchase-orders",
  "contract": "inventory",
  "summary": "List purchase orders",
  "permission": "PROCUREMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "supplierId",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listRecipes": {
  "method": "GET",
  "path": "/recipes",
  "contract": "fnb",
  "summary": "List recipes",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "menuItemId",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "planProductionRun": {
  "method": "POST",
  "path": "/production-runs",
  "contract": "fnb",
  "summary": "Plan a batch, for one outlet or several",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ProductionRun",
  "responds": "ProductionRun"
 },
 "recordWaste": {
  "method": "POST",
  "path": "/outlets/{outletId}/waste",
  "contract": "fnb",
  "summary": "Record waste",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "setItemAvailability": {
  "method": "PUT",
  "path": "/menu-items/{itemId}/availability",
  "contract": "fnb",
  "summary": "Mark an item available or eighty-sixed",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MenuItem"
 },
 "setTemperatureCheckpoint": {
  "method": "PUT",
  "path": "/food-safety/checkpoints",
  "contract": "fnb",
  "summary": "Define a checkpoint and its safe range",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "TemperatureCheckpoint",
  "responds": "TemperatureCheckpoint"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Alert": {
  "type": "object",
  "x-ticvai-persistence": "reporting.alert",
  "description": "A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n",
  "required": [
   "id",
   "ruleId",
   "raisedAt",
   "severity",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "ruleId": {
    "type": "string",
    "format": "uuid"
   },
   "ruleName": {
    "type": "string",
    "description": "`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"
   },
   "metric": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricSource"
     }
    ],
    "description": "The rule's metric, carried so the alert says what went out of range."
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "severity": {
    "$ref": "#/components/schemas/AlertSeverity"
   },
   "status": {
    "$ref": "#/components/schemas/AlertStatus"
   },
   "observedValue": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "threshold": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "scopePath": {
    "type": "string"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."
   },
   "shiftId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."
   },
   "itemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"
   },
   "acknowledgedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "acknowledgedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "acknowledgementNote": {
    "type": "string",
    "maxLength": 300,
    "nullable": true,
    "description": "The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"
   }
  }
 },
 "AlertSeverity": {
  "type": "string",
  "description": "How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.",
  "enum": [
   "info",
   "warning",
   "critical"
  ]
 },
 "AlertStatus": {
  "type": "string",
  "description": "Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.",
  "enum": [
   "raised",
   "acknowledged",
   "resolved",
   "expired"
  ]
 },
 "AllergenCode": {
  "type": "string",
  "description": "**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n",
  "enum": [
   "gluten",
   "crustaceans",
   "eggs",
   "fish",
   "peanuts",
   "soybeans",
   "milk",
   "nuts",
   "celery",
   "mustard",
   "sesame",
   "sulphites",
   "lupin",
   "molluscs"
  ]
 },
 "CostingMethod": {
  "type": "string",
  "description": "Fixed at item creation. Immutable once movements exist.",
  "enum": [
   "weightedAverage",
   "fifo",
   "standardCost",
   "lastPurchasePrice"
  ]
 },
 "CountVariance": {
  "x-ticvai-persistence": "none — computed at close",
  "type": "object",
  "required": [
   "countId",
   "totalVarianceValue",
   "lines"
  ],
  "properties": {
   "countId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "totalVarianceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exceptionCount": {
    "type": "integer",
    "description": "Lines beyond `VenueSettings.inventory.countVarianceTolerancePercent` (proposed default 2 per cent, audit R094), requiring review before posting."
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "itemId",
      "expectedQuantity",
      "countedQuantity",
      "variance",
      "isException"
     ],
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "itemName": {
       "type": "string"
      },
      "sku": {
       "type": "string"
      },
      "expectedQuantity": {
       "type": "number"
      },
      "countedQuantity": {
       "type": "number"
      },
      "variance": {
       "type": "number"
      },
      "variancePercentage": {
       "type": "number"
      },
      "varianceValue": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "isException": {
       "type": "boolean"
      },
      "recountCount": {
       "type": "integer",
       "description": "A line counted several times is itself a finding."
      },
      "note": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "CreateInventoryItemRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "sku",
   "name",
   "venueId",
   "baseUnit",
   "costingMethod"
  ],
  "properties": {
   "sku": {
    "type": "string",
    "maxLength": 64
   },
   "barcode": {
    "type": "string",
    "maxLength": 128
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "baseUnit": {
    "type": "string",
    "description": "The unit stock is held in. Immutable once movements exist."
   },
   "purchaseUnit": {
    "type": "string",
    "description": "How the supplier sells it — a case of 24 against a base unit of one."
   },
   "purchaseUnitFactor": {
    "type": "number",
    "minimum": 0,
    "default": 1
   },
   "costingMethod": {
    "$ref": "#/components/schemas/CostingMethod"
   },
   "reorderPoint": {
    "type": "number",
    "minimum": 0
   },
   "reorderQuantity": {
    "type": "number",
    "minimum": 0
   },
   "parLevel": {
    "type": "number",
    "minimum": 0
   },
   "preferredSupplierId": {
    "type": "string",
    "format": "uuid"
   },
   "allowNegativeStock": {
    "type": "boolean",
    "default": false,
    "description": "True permits issue beyond on-hand. Occasionally needed at a bar mid-service; dangerous everywhere else.\n"
   },
   "isPerishable": {
    "type": "boolean",
    "default": false
   },
   "shelfLifeDays": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "CreateRequisitionRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "lines",
   "requiredBy"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid"
   },
   "costCenterId": {
    "type": "string",
    "format": "uuid"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "itemId",
      "quantity"
     ],
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "number",
       "minimum": 0
      },
      "unit": {
       "type": "string"
      },
      "note": {
       "type": "string",
       "maxLength": 200
      }
     }
    }
   },
   "requiredBy": {
    "type": "string",
    "format": "date"
   },
   "justification": {
    "type": "string",
    "maxLength": 1000
   }
  }
 },
 "InventoryItem": {
  "x-ticvai-persistence": "inventory.item",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateInventoryItemRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "onHand",
     "isActive"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "onHand": {
      "type": "number",
      "description": "Derived from movements. Not directly editable."
     },
     "onOrder": {
      "type": "number"
     },
     "inTransit": {
      "type": "number"
     },
     "available": {
      "type": "number",
      "description": "On-hand minus allocated, where allocated is stock reserved for orders (decided 28 September, audit R171)."
     },
     "averageCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "lastPurchasePrice": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "isBelowReorderPoint": {
      "type": "boolean"
     },
     "hasMovements": {
      "type": "boolean",
      "description": "True locks costing method and base unit."
     },
     "isActive": {
      "type": "boolean"
     }
    }
   }
  ]
 },
 "KpiValue": {
  "type": "object",
  "description": "BI board 10.3. **Value, target, variance, direction and freshness in one read.**",
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "target": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "comparison": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "variancePercent": {
    "type": "number",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "up",
     "down",
     "flat"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "green",
     "amber",
     "red",
     "noTarget"
    ]
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "stale": {
    "type": "boolean",
    "description": "**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"
   }
  }
 },
 "MenuItem": {
  "x-ticvai-persistence": "fnb.menu_item",
  "type": "object",
  "required": [
   "id",
   "productVariantId",
   "name",
   "price",
   "isAvailable"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productVariantId": {
    "type": "string",
    "format": "uuid",
    "description": "The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "price": {
    "x-ticvai-column": "list_price",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "sortOrder": {
    "type": "integer"
   },
   "modifierGroupIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "stationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "menuSectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."
   },
   "isStockTracked": {
    "type": "boolean",
    "description": "True where a recipe exists. Stock-tracked items cannot be sold offline."
   },
   "isAvailable": {
    "type": "boolean"
   },
   "unavailableReason": {
    "type": "string",
    "nullable": true
   },
   "restoreAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."
   },
   "preparationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "allergens": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AllergenCode"
    }
   }
  }
 },
 "MetricSource": {
  "type": "string",
  "description": "**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n",
  "enum": [
   "occupancy",
   "capacityUtilisation",
   "admissionRate",
   "noShowRate",
   "conversion",
   "salesByOperator",
   "salesByWorkstation",
   "waitTime",
   "throughput",
   "abandonmentRate",
   "inventoryValuation",
   "stockTurnover",
   "stockAgeing",
   "wastageRate",
   "resaleVolume",
   "resaleCommission",
   "salesByInstructor",
   "resourceUtilisation",
   "allocationUtilisation",
   "channelAllocationBurn",
   "membershipChurn",
   "membershipRenewalRate",
   "supplierDeliveryPerformance",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "assetDowntime",
   "meanTimeToRepair",
   "challengeCompletionRate",
   "attributedRevenue"
  ],
  "x-ticvai-money-valued": [
   "inventoryValuation",
   "resaleCommission",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "attributedRevenue"
  ],
  "x-ticvai-money-valued-note": "**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n",
  "x-ticvai-extended": "18 August 2026",
  "x-ticvai-extension-note": "**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
 },
 "Page": {
  "type": "object",
  "required": [
   "items",
   "hasMore"
  ],
  "properties": {
   "items": {
    "type": "array",
    "items": {}
   },
   "nextCursor": {
    "type": "string"
   },
   "hasMore": {
    "type": "boolean"
   }
  }
 },
 "ProductionRun": {
  "type": "object",
  "x-ticvai-persistence": "fnb.production_run",
  "description": "BL-129. **A central kitchen makes 400 portions at 6am for four outlets**, and nothing modelled that — orders consume stock and no operation produced any.\n**Production converts ingredients into a sellable item**, which is a stock movement in both directions at once, and treating it as two unrelated adjustments loses the yield.\n",
  "required": [
   "id",
   "recipeId",
   "plannedQuantity",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "recipeId": {
    "type": "string",
    "format": "uuid"
   },
   "productionPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The plan whose release created this run. Null for a run planned directly."
   },
   "stationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The station whose prep list this run is on.** Copied from the plan line on release, where runs are grouped by station (audit R125 (7)).\n"
   },
   "producingOutletId": {
    "type": "string",
    "format": "uuid"
   },
   "forOutletIds": {
    "type": "array",
    "description": "**Where it goes.** A central kitchen produces for outlets that did not make it.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "plannedQuantity": {
    "type": "number"
   },
   "actualQuantity": {
    "type": "number",
    "nullable": true,
    "description": "BL-126. **Theoretical against actual is the whole point of recording this.** A recipe says 400 portions from the ingredients issued; the run says how many were made, and the gap is waste, theft or a recipe that is wrong.\n"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "planned",
     "inProgress",
     "completed",
     "cancelled"
    ]
   },
   "varianceReason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "Requisition": {
  "x-ticvai-persistence": "inventory.requisition + inventory.requisition_line",
  "type": "object",
  "required": [
   "id",
   "requisitionNumber",
   "venueId",
   "status",
   "lines",
   "raisedByPrincipalId",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "requisitionNumber": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "costCenterId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/RequisitionStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "lineId": {
       "type": "string"
      },
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "itemName": {
       "type": "string"
      },
      "requestedQuantity": {
       "type": "number"
      },
      "suggestedQuantity": {
       "type": "number",
       "nullable": true,
       "description": "**Kept, never overwritten** (`updateRequisitionLines`). Null on a line nobody suggested.\n"
      },
      "approvedQuantity": {
       "type": "number",
       "nullable": true
      },
      "orderedQuantity": {
       "type": "number",
       "nullable": true
      },
      "unit": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "nullable": true,
       "description": "Why the requested quantity differs from the suggestion."
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "estimatedCost": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "estimatedTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvalNote": {
    "type": "string",
    "nullable": true
   },
   "requiredBy": {
    "type": "string",
    "format": "date"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "approvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "rejectionReason": {
    "type": "string",
    "nullable": true,
    "description": "From `rejectRequisition`. What the requester reads before copying it into a new draft."
   },
   "rejectedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnQuestion": {
    "type": "string",
    "nullable": true,
    "description": "From `returnRequisition`. What the requester must answer before resubmitting."
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "cancelReason": {
    "type": "string",
    "nullable": true,
    "description": "From `cancelRequisition`."
   },
   "cancelledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "RequisitionStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pendingApproval",
   "approved",
   "rejected",
   "returnedForInfo",
   "ordered",
   "closed",
   "cancelled"
  ]
 },
 "TemperatureCheckpoint": {
  "type": "object",
  "x-ticvai-persistence": "fnb.temperature_checkpoint",
  "description": "**A unit that gets read, and the range it is required to hold.** The entity `TemperatureLog.checkPointId` has always been required to name and that nothing defined.\n**The safe range belongs here and is snapshotted onto each reading**, so that a range revised in March cannot silently re-judge a reading taken in January.",
  "required": [
   "id",
   "kind",
   "label",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "fridge",
     "freezer",
     "holdingCabinet",
     "blastChiller",
     "coreProbe",
     "delivery",
     "displayCounter",
     "ambient"
    ],
    "description": "The same closed set `TemperatureLog.checkPointKind` records."
   },
   "label": {
    "type": "string",
    "description": "**What the person reading it calls it** — *Walk-in 2*, *Dessert counter*. A checkpoint identified only by a uuid is one somebody will read the wrong unit for."
   },
   "minCelsius": {
    "type": "number",
    "nullable": true
   },
   "maxCelsius": {
    "type": "number",
    "nullable": true,
    "description": "**Null at either end is legitimate** — a core probe has a floor and no ceiling. Both null is not, and is what an unconfigured checkpoint looks like."
   },
   "checkFrequencyMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "**How often it must be read.** The gap this leaves open otherwise is the one an inspector finds: not a bad reading, but a missing one."
   },
   "requiresCorrectiveActionOnBreach": {
    "type": "boolean"
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `setVenueSettings`."
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "readOnly": true,
    "description": "**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "nullable": true,
    "readOnly": true,
    "description": "**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string",
      "description": "IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string",
         "description": "Wall-clock time the desk opens."
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time the desk closes."
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string",
      "description": "Wall-clock time sending stops",
      "in the region's time zone.": null
     },
     "to": {
      "type": "string",
      "description": "Wall-clock time sending resumes",
      "in the region's time zone.": null
     }
    }
   },
   "biometrics": {
    "type": "object",
    "nullable": true,
    "description": "CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false,
      "description": "**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"
     },
     "dpiaReference": {
      "type": "string",
      "nullable": true,
      "maxLength": 200,
      "description": "**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"
     },
     "consentNoticeAcknowledgedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"
     },
     "acknowledgedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "readOnly": true,
      "description": "**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"
     },
     "faceTagPurgeMinutesAfterClose": {
      "type": "integer",
      "nullable": true,
      "default": 0,
      "description": "BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       "off",
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": "off",
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "displayCurrencies": {
    "type": "array",
    "nullable": true,
    "description": "**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{3}$"
    }
   },
   "cartLeaseSeconds": {
    "type": "integer",
    "nullable": true,
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"
   },
   "cartHoldExtensionMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 30,
    "default": 5,
    "description": "How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."
   },
   "cartMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."
   },
   "resaleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."
   },
   "exchangeCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."
   },
   "rescheduleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."
   },
   "reservationMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."
   },
   "shiftVarianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"
   },
   "catalogue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxVariantsPerProduct": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 2000,
      "default": 200,
      "description": "Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."
     },
     "waitlistOfferHoldMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 1440,
      "default": 30,
      "description": "How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 10,
      "description": "A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationCount": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 50,
      "description": "A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     }
    }
   },
   "inventory": {
    "type": "object",
    "nullable": true,
    "properties": {
     "overReceiptTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 5,
      "description": "Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."
     },
     "countVarianceTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 2,
      "description": "Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."
     },
     "countVarianceApprovalAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"
     }
    }
   },
   "seating": {
    "type": "object",
    "nullable": true,
    "properties": {
     "seatHoldExtensionSeconds": {
      "type": "integer",
      "nullable": true,
      "minimum": 60,
      "maximum": 1800,
      "default": 300,
      "description": "What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."
     },
     "seatHoldMaxExtensions": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 5,
      "default": 2,
      "description": "How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."
     },
     "maxSeatsPerGuestOrder": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 50,
      "default": 10,
      "description": "**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"
     }
    }
   },
   "promotions": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 30,
      "description": "The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."
     },
     "nearZeroLinePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"
     }
    }
   },
   "fnb": {
    "type": "object",
    "nullable": true,
    "properties": {
     "recallWindowMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 60,
      "default": 10,
      "description": "Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."
     },
     "compEscalationAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"
     },
     "foodSafetyLeadPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"
     }
    }
   },
   "queue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "crossQueueLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 10,
      "default": 2,
      "description": "Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "reporting": {
    "type": "object",
    "nullable": true,
    "properties": {
     "inlineRunRowLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1000,
      "maximum": 100000,
      "default": 5000,
      "description": "Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."
     },
     "dashboardRefreshBudgetPerMinute": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 24,
      "description": "Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."
     }
    }
   },
   "marketing": {
    "type": "object",
    "nullable": true,
    "properties": {
     "attributionWindowDays": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 30,
      "default": 7,
      "description": "Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "identity": {
    "type": "object",
    "nullable": true,
    "properties": {
     "guestOtpMaxAttempts": {
      "type": "integer",
      "nullable": true,
      "minimum": 3,
      "maximum": 10,
      "default": 5,
      "description": "Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"
     },
     "guestTwoStep": {
      "type": "object",
      "nullable": true,
      "description": "**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n",
      "properties": {
       "enabled": {
        "type": "boolean",
        "default": false,
        "description": "Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."
       },
       "stepUpActions": {
        "type": "array",
        "uniqueItems": true,
        "description": "The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n",
        "items": {
         "type": "string",
         "enum": [
          "changeContactDetails",
          "changePassword",
          "managePaymentMethods",
          "transferTickets",
          "deleteAccount"
         ]
        },
        "default": [
         "changeContactDetails",
         "changePassword",
         "managePaymentMethods",
         "deleteAccount"
        ]
       }
      }
     }
    }
   }
  }
 }
}
```
