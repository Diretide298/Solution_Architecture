# P08-stock-supply-01 — P08 · Stock & Supply (1 of 2)

**10 screens · 56 operations · 42 schemas · 12 permissions**

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

- **Every control that can be refused must be gated.** 12 permissions apply here:
  `APPROVAL_ACT, LEDGER_APPROVE, LEDGER_POST, LEDGER_VIEW, ORDER_VIEW, PROCUREMENT_MANAGE, PROCUREMENT_RECEIVE, PROCUREMENT_REQUEST, PROCUREMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-049` | Stock Levels | listDetail | 6 | 3 | — |
| `BO-050` | Stock Position & Valuation | statusTracker | 2 | 0 | — |
| `BO-051` | Purchase Orders | listDetail | 7 | 4 | — |
| `BO-052` | Goods Receipt | listDetail | 12 | 7 | — |
| `BO-078` | Requisitions | approvalInbox | 10 | 6 | — |
| `BO-079` | Stock Count | listDetail | 9 | 7 | — |
| `BO-080` | Stock Transfers | listDetail | 6 | 4 | — |
| `BO-081` | Inventory Items | listDetail | 9 | 3 | — |
| `BO-082` | Stock Movements | listDetail | 4 | 2 | — |
| `BO-083` | Suppliers | listDetail | 8 | 3 | — |

## Thin screens in this batch

**BO-050 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-049",
  "name": "Stock Levels",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/stock-levels",
   "component": "apps/venue-management-web/src/routes/venue-operations/StockLevelsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-079",
    "BO-080",
    "BO-081",
    "BO-082"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-082",
     "trigger": "The four orders are sourced from another store instead",
     "provenance": "flow F35 step 6→7",
     "operation": "createStockMovement"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "provenance": "derived — BO-079 declares entryState.params countId and BO-049 holds none of them, so the edge carries nothing and BO-079 opens cold"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "provenance": "derived — BO-080 declares entryState.params transferId and BO-049 holds none of them, so the edge carries nothing and BO-080 opens cold"
    },
    {
     "to": "EMP-065",
     "trigger": "The delivery arrives",
     "provenance": "flow F35 step 1→2",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "BO-081",
     "trigger": "Inventory Items",
     "provenance": "flow F92 step 1→2",
     "carries": [
      "itemId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): F&B Stock & Operations Command Center; Outlet Stock & Ingredient Availability. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5a",
   "FnB Board 5.dc.html#fnb-5b",
   "Retail Board 4.dc.html#ret-4a",
   "Retail Board 4.dc.html#ret-4h",
   "Inventory Board 1.dc.html#inv-7",
   "Inventory Board 1.dc.html#inv-9"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockLocations` reads the population and `getStockPositions` reads one of them — list, select, act",
  "purpose": "Know what is on the shelf and what is on order.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every stock location",
       "bindsTo": "StockLocation",
       "columns": [
        "StockLocation.id",
        "StockLocation.code",
        "StockLocation.name",
        "StockLocation.venueId",
        "StockLocation.kind",
        "StockLocation.parentLocationId",
        "StockLocation.isActive"
       ],
       "operation": "listStockLocations",
       "provenance": "contract inventory.yaml GET /stock-locations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected stock location",
       "bindsTo": "StockLocation",
       "columns": [
        "StockLocation.id",
        "StockLocation.code",
        "StockLocation.name",
        "StockLocation.venueId",
        "StockLocation.kind",
        "StockLocation.parentLocationId",
        "StockLocation.isActive"
       ],
       "operation": "listStockLocations",
       "provenance": "contract inventory.yaml GET /stock-locations"
      },
      {
       "kind": "detailPanel",
       "label": "The stock valuation",
       "bindsTo": "StockValuation",
       "columns": [
        "StockValuation.asAt",
        "StockValuation.total",
        "StockValuation.byLocation",
        "StockValuation.byCategory"
       ],
       "operation": "getStockValuation",
       "provenance": "contract inventory.yaml GET /stock/valuation"
      },
      {
       "kind": "detailPanel",
       "label": "The stock position",
       "bindsTo": "StockPosition",
       "columns": [
        "StockPosition.itemId",
        "StockPosition.itemName",
        "StockPosition.sku",
        "StockPosition.locationId",
        "StockPosition.locationName",
        "StockPosition.onHand",
        "StockPosition.allocated",
        "StockPosition.available",
        "StockPosition.unit",
        "StockPosition.value",
        "StockPosition.lastCountedAt",
        "StockPosition.lastMovementAt"
       ],
       "operation": "getStockPositions",
       "provenance": "contract inventory.yaml GET /stock"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save item availability",
       "operation": "setItemAvailability",
       "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
      },
      {
       "kind": "secondaryButton",
       "label": "Create stock transfer",
       "operation": "createStockTransfer",
       "provenance": "contract inventory.yaml POST /stock-transfers"
      },
      {
       "kind": "secondaryButton",
       "label": "Create stock movement",
       "operation": "createStockMovement",
       "provenance": "contract inventory.yaml POST /stock-movements"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stock levels list.",
   "error": "Could not load. Names which read failed and leaves the stock levels untouched.",
   "emptyFirstRun": "No stock levels yet. Offers Create stock transfer (`createStockTransfer`).",
   "emptyNoResults": "Never shown: `listStockLocations` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "Stock on hand by item and location",
    "trigger": "onLoad"
   },
   {
    "operationId": "getStockValuation",
    "contract": "inventory",
    "purpose": "Stock value by location and category",
    "trigger": "onLoad"
   },
   {
    "operationId": "setItemAvailability",
    "contract": "fnb",
    "purpose": "Mark an item available or eighty-sixed",
    "trigger": "onAction",
    "invalidates": [
     "listStockLocations"
    ]
   },
   {
    "operationId": "createStockTransfer",
    "contract": "inventory",
    "purpose": "Send stock to another location",
    "trigger": "onAction",
    "invalidates": [
     "listStockLocations"
    ]
   },
   {
    "operationId": "createStockMovement",
    "contract": "inventory",
    "purpose": "Record an issue, return or adjustment",
    "trigger": "onAction",
    "invalidates": [
     "listStockLocations"
    ]
   },
   {
    "operationId": "listStockLocations",
    "contract": "inventory",
    "purpose": "List stock locations",
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
     "name": "itemId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "An item opened from the catalogue.",
   "preloaded": [
    "StockLocation.id",
    "StockLocation.code",
    "StockLocation.name",
    "StockLocation.venueId",
    "StockLocation.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-049",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetItemAvailability",
    "component": "modal",
    "trigger": "Save item availability",
    "body": "**Collects what `setItemAvailability` sends before it is called.** Required: `isAvailable`, `recordedAt`. Optional: `reason`, `restoreAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save item availability",
     "operation": "setItemAvailability"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "isAvailable",
      "recordedAt",
      "reason",
      "restoreAt"
     ]
    },
    "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
   },
   {
    "id": "formCreateStockTransfer",
    "component": "modal",
    "trigger": "Create stock transfer",
    "body": "**Collects what `createStockTransfer` sends before it is called.** Required: `id`, `fromLocationId`, `toLocationId`, `lines`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateStockTransferRequest",
    "confirm": {
     "label": "Create stock transfer",
     "operation": "createStockTransfer"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "fromLocationId",
      "toLocationId",
      "lines",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-transfers"
   },
   {
    "id": "formCreateStockMovement",
    "component": "modal",
    "trigger": "Create stock movement",
    "body": "**Collects what `createStockMovement` sends before it is called.** Required: `id`, `itemId`, `locationId`, `kind`, `quantity`, `recordedAt`. Optional: `unit`, `reason`, `costCenterId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateStockMovementRequest",
    "confirm": {
     "label": "Create stock movement",
     "operation": "createStockMovement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "itemId",
      "locationId",
      "kind",
      "quantity",
      "recordedAt",
      "unit",
      "reason",
      "costCenterId"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-movements"
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
  "id": "BO-050",
  "name": "Stock Position & Valuation",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/stock-count",
   "component": "apps/venue-management-web/src/routes/venue-operations/StockCountDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": true,
   "entryFrom": [
    "BO-105"
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Named `Stock Count` and carrying `getStockPositions` and `getStockValuation`** — two screens with one name, while `BO-079 Stock Count` holds the actual counting operations. Renamed 20 August; the operations were right.",
  "density": "compact",
  "boardFrames": [
   "Inventory Board 3.dc.html#inv-3h",
   "Inventory Board 7.dc.html#inv-7d"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getStockPositions` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Count the shelf and account for the difference.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The stock position",
       "bindsTo": "StockPosition",
       "columns": [
        "StockPosition.itemId",
        "StockPosition.itemName",
        "StockPosition.sku",
        "StockPosition.locationId",
        "StockPosition.locationName",
        "StockPosition.onHand",
        "StockPosition.allocated",
        "StockPosition.available",
        "StockPosition.unit",
        "StockPosition.value",
        "StockPosition.lastCountedAt",
        "StockPosition.lastMovementAt"
       ],
       "operation": "getStockPositions",
       "provenance": "contract inventory.yaml GET /stock"
      },
      {
       "kind": "detailPanel",
       "label": "The stock valuation",
       "bindsTo": "StockValuation",
       "columns": [
        "StockValuation.asAt",
        "StockValuation.total",
        "StockValuation.byLocation",
        "StockValuation.byCategory"
       ],
       "operation": "getStockValuation",
       "provenance": "contract inventory.yaml GET /stock/valuation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stock position valuation, read by `getStockPositions`.",
   "error": "Could not load. Names which read failed and leaves the stock position valuation untouched.",
   "emptyFirstRun": "No stock position valuation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "Stock on hand by item and location",
    "trigger": "onLoad"
   },
   {
    "operationId": "getStockValuation",
    "contract": "inventory",
    "purpose": "Stock value by location and category",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-050"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-051",
  "name": "Purchase Orders",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/purchase-orders",
   "component": "apps/venue-management-web/src/routes/venue-operations/PurchaseOrdersDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-052"
   ],
   "transitions": [
    {
     "to": "BO-052",
     "trigger": "Receive against this order",
     "provenance": "purpose — a purchase order that has been sent is received on Goods Receipt (decided 28 September, audit R254)",
     "carries": [
      "purchaseOrderId"
     ]
    }
   ],
   "entryFrom": [
    "BO-105"
   ],
   "inferred": false,
   "notes": "**Moved 29 September (VM close-out) from Orders & Money to Stock & Supply**, beside BO-052 Goods Receipt: a purchase order is stock supply, not guest money, and `requiresModule` is inventory like its receipt. Reached from BO-105; the old cold link from BO-101 Orders & Money is removed."
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. **Rebound 28 September to the inventory purchase-order operations** (decided 28 September, audit R254): it carried 13 sales-order operations (`listOrders`, `voidOrder`, `holdOrder` and the rest), attached by name resemblance as BO-070 was, and none of them orders stock. It now lists, raises, sends, acknowledges, cancels and short-closes purchase orders; receiving is BO-052. Guards are the procurement permissions (audit R091 (4)), and cancel and close-short may answer 202 pending a finance approver (audit R144).",
  "density": "compact",
  "boardFrames": [
   "Inventory Board 5.dc.html#inv-5a",
   "Inventory Board 5.dc.html#inv-5h",
   "Inventory Board 5.dc.html#inv-5j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPurchaseOrders` reads the population and `getPurchaseOrder` reads one of them — list, select, act",
  "purpose": "Order more of what is running out.",
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
       "operation": "listPurchaseOrders",
       "notes": "Sends `?status=` to `listPurchaseOrders`.",
       "provenance": "contract inventory.yaml GET /purchase-orders"
      },
      {
       "kind": "textField",
       "label": "Supplier id",
       "operation": "listPurchaseOrders",
       "notes": "Sends `?supplierId=` to `listPurchaseOrders`.",
       "provenance": "contract inventory.yaml GET /purchase-orders"
      },
      {
       "kind": "dataTable",
       "label": "Every purchase order",
       "bindsTo": "PurchaseOrder",
       "columns": [
        "PurchaseOrder.purchaseOrderNumber",
        "PurchaseOrder.supplierName",
        "PurchaseOrder.kind",
        "PurchaseOrder.status",
        "PurchaseOrder.matchStatus",
        "PurchaseOrder.approvalRequestId"
       ],
       "operation": "listPurchaseOrders",
       "notes": "A row with `approvalRequestId` set shows *pending approval* (audit R144).",
       "provenance": "contract inventory.yaml GET /purchase-orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected purchase order",
       "bindsTo": "PurchaseOrder",
       "columns": [
        "PurchaseOrder.purchaseOrderNumber",
        "PurchaseOrder.requisitionId",
        "PurchaseOrder.supplierName",
        "PurchaseOrder.kind",
        "PurchaseOrder.blanketParentId",
        "PurchaseOrder.contractPriceValidUntil",
        "PurchaseOrder.rfqId",
        "PurchaseOrder.supplierInvoiceRef",
        "PurchaseOrder.matchStatus",
        "PurchaseOrder.status",
        "PurchaseOrder.approvalRequestId",
        "PurchaseOrder.deliverToLocationId",
        "PurchaseOrder.lines",
        "PurchaseOrder.subtotal",
        "PurchaseOrder.taxAmount"
       ],
       "operation": "getPurchaseOrder",
       "provenance": "contract inventory.yaml GET /purchase-orders/{purchaseOrderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create purchase order",
       "operation": "createPurchaseOrder",
       "permission": "PROCUREMENT_MANAGE",
       "notes": "PO lines prefill the unit price from the selected quotation; changing it asks for an override reason (decided 28 September, audit R171).",
       "provenance": "contract inventory.yaml POST /purchase-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Send purchase order",
       "operation": "sendPurchaseOrder",
       "permission": "PROCUREMENT_MANAGE",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/send"
      },
      {
       "kind": "secondaryButton",
       "label": "Acknowledge purchase order",
       "operation": "acknowledgePurchaseOrder",
       "permission": "PROCUREMENT_MANAGE",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/acknowledge"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel purchase order",
       "operation": "cancelPurchaseOrder",
       "permission": "PROCUREMENT_MANAGE",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close purchase order short",
       "operation": "closePurchaseOrderShort",
       "permission": "PROCUREMENT_MANAGE",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/close-short"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formCreatePurchaseOrder",
    "component": "modal",
    "trigger": "Create purchase order",
    "body": "**Collects what `createPurchaseOrder` sends before it is called.** Required: `id`, `requisitionId`, `supplierId`, `quotationId`, `lines`, `expectedDelivery`. Optional: `deliverToLocationId`, `note`. **Each line's `unitPrice` is prefilled from the selected quotation**; if the user changes it, the line asks for `priceOverrideReason`, which the server requires (400) whenever the price differs from the quotation (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePurchaseOrderRequest",
    "confirm": {
     "label": "Create purchase order",
     "operation": "createPurchaseOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "requisitionId",
      "supplierId",
      "quotationId",
      "lines",
      "expectedDelivery",
      "deliverToLocationId",
      "note"
     ]
    },
    "provenance": "contract inventory.yaml POST /purchase-orders"
   },
   {
    "id": "formAcknowledgePurchaseOrder",
    "component": "modal",
    "trigger": "Acknowledge purchase order",
    "body": "**Collects what `acknowledgePurchaseOrder` sends before it is called.** Required: `supplierReference`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Acknowledge purchase order",
     "operation": "acknowledgePurchaseOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "supplierReference"
     ]
    },
    "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/acknowledge"
   },
   {
    "id": "confirmCancelPurchaseOrder",
    "component": "confirmDialog",
    "trigger": "Cancel purchase order",
    "body": "**Names what `cancelPurchaseOrder` changes and what it leaves alone**, in the consequence rather than the verb: the order number, the supplier and the value not yet received. **Collects what `cancelPurchaseOrder` sends before it is called.** Required: `reason`. **It may answer 202 pending a finance approver** (decided 28 September, audit R144): the order is unchanged, shows *cancellation pending approval* and carries `approvalRequestId` until the approver acts.",
    "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/cancel"
   },
   {
    "id": "confirmClosePurchaseOrderShort",
    "component": "confirmDialog",
    "trigger": "Close purchase order short",
    "body": "**Names what `closePurchaseOrderShort` changes and what it leaves alone**, in the consequence rather than the verb: the balance that will no longer be expected. **Collects what `closePurchaseOrderShort` sends before it is called.** Required: `reason`. **It may answer 202 pending a finance approver** (decided 28 September, audit R144): the order is unchanged, shows *close-short pending approval* and carries `approvalRequestId` until the approver acts.",
    "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/close-short"
   }
  ],
  "states": {
   "loading": "The purchase orders list.",
   "error": "Could not load. Names which read failed and leaves the purchase orders untouched.",
   "emptyFirstRun": "No purchase orders yet. Offers Create purchase order (`createPurchaseOrder`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status and supplierId, and the purchase orders are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PROCUREMENT_VIEW`, which `listPurchaseOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPurchaseOrders",
    "contract": "inventory",
    "purpose": "List purchase orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPurchaseOrder",
    "contract": "inventory",
    "purpose": "Read a purchase order with receipt progress",
    "trigger": "onAction"
   },
   {
    "operationId": "createPurchaseOrder",
    "contract": "inventory",
    "purpose": "Raise a purchase order",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "sendPurchaseOrder",
    "contract": "inventory",
    "purpose": "Issue the order to the supplier",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "acknowledgePurchaseOrder",
    "contract": "inventory",
    "purpose": "Record the supplier acknowledgement",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "cancelPurchaseOrder",
    "contract": "inventory",
    "purpose": "Cancel a purchase order",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "closePurchaseOrderShort",
    "contract": "inventory",
    "purpose": "Close an order accepting the balance will not arrive",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "purchaseOrderId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the purchase order or says plainly that it is gone.** Without `purchaseOrderId` the list opens. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold.",
   "preloaded": [
    "PurchaseOrder.id",
    "PurchaseOrder.purchaseOrderNumber",
    "PurchaseOrder.supplierName",
    "PurchaseOrder.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-051"
  },
  "apisNote": "Rebound 28 September 2026 to the seven inventory purchase-order operations (audit R254); the 13 sales-order operations it declared before were attached by name resemblance.",
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
  "id": "BO-052",
  "name": "Goods Receipt",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/goods-receipt",
   "component": "apps/venue-management-web/src/routes/venue-operations/GoodsReceiptDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-049"
   ],
   "inferred": true,
   "fromFlows": true,
   "entryFrom": [
    "BO-080",
    "BO-105",
    "BO-051"
   ],
   "transitions": [
    {
     "to": "EMP-005",
     "trigger": "The technician resumes",
     "provenance": "flow F15 step 4→5",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "BO-049",
     "trigger": "The website has already sold four of the damaged units",
     "provenance": "flow F35 step 4→5",
     "carries": [
      "itemId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Pulled to Wave 2 (CF-101). Requisitions are Wave 1 and receipt was Wave 3 — **the end of the chain arriving two waves after the start.** **Cross-platform navigation removed 24 August**: EMP-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4e",
   "Inventory Board 6.dc.html#inv-6a",
   "Inventory Board 6.dc.html#inv-6b",
   "Inventory Board 6.dc.html#inv-6c",
   "Inventory Board 6.dc.html#inv-6d",
   "Inventory Board 6.dc.html#inv-6e",
   "Inventory Board 2.dc.html#inv-2d",
   "Inventory Board 2.dc.html#inv-2e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPurchaseOrders` reads the population and `getPurchaseOrder` reads one of them — list, select, act",
  "purpose": "Book in what actually arrived.",
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
       "operation": "listPurchaseOrders",
       "notes": "Sends `?status=` to `listPurchaseOrders`.",
       "provenance": "contract inventory.yaml GET /purchase-orders"
      },
      {
       "kind": "textField",
       "label": "Supplier id",
       "operation": "listPurchaseOrders",
       "notes": "Sends `?supplierId=` to `listPurchaseOrders`.",
       "provenance": "contract inventory.yaml GET /purchase-orders"
      },
      {
       "kind": "dataTable",
       "label": "Every purchase order",
       "bindsTo": "PurchaseOrder",
       "columns": [
        "PurchaseOrder.id",
        "PurchaseOrder.purchaseOrderNumber",
        "PurchaseOrder.requisitionId",
        "PurchaseOrder.supplierId",
        "PurchaseOrder.supplierName",
        "PurchaseOrder.kind",
        "PurchaseOrder.blanketParentId",
        "PurchaseOrder.contractPriceValidUntil",
        "PurchaseOrder.rfqId",
        "PurchaseOrder.supplierInvoiceRef",
        "PurchaseOrder.matchStatus",
        "PurchaseOrder.status",
        "PurchaseOrder.approvalRequestId"
       ],
       "operation": "listPurchaseOrders",
       "provenance": "contract inventory.yaml GET /purchase-orders"
      },
      {
       "kind": "dataTable",
       "label": "Every goods receipt",
       "bindsTo": "GoodsReceipt",
       "columns": [
        "GoodsReceipt.id",
        "GoodsReceipt.receiptNumber",
        "GoodsReceipt.purchaseOrderId",
        "GoodsReceipt.locationId",
        "GoodsReceipt.deliveryNoteReference",
        "GoodsReceipt.lines",
        "GoodsReceipt.totalValue",
        "GoodsReceipt.receivedByPrincipalId",
        "GoodsReceipt.journalEntryId",
        "GoodsReceipt.recordedAt",
        "GoodsReceipt.syncedAt"
       ],
       "operation": "listGoodsReceipts",
       "provenance": "contract inventory.yaml GET /goods-receipts"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
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
       "label": "The selected purchase order",
       "bindsTo": "PurchaseOrder",
       "columns": [
        "PurchaseOrder.id",
        "PurchaseOrder.purchaseOrderNumber",
        "PurchaseOrder.requisitionId",
        "PurchaseOrder.supplierId",
        "PurchaseOrder.supplierName",
        "PurchaseOrder.kind",
        "PurchaseOrder.blanketParentId",
        "PurchaseOrder.contractPriceValidUntil",
        "PurchaseOrder.rfqId",
        "PurchaseOrder.supplierInvoiceRef",
        "PurchaseOrder.matchStatus",
        "PurchaseOrder.status",
        "PurchaseOrder.approvalRequestId",
        "PurchaseOrder.deliverToLocationId",
        "PurchaseOrder.lines",
        "PurchaseOrder.subtotal",
        "PurchaseOrder.taxAmount"
       ],
       "operation": "getPurchaseOrder",
       "provenance": "contract inventory.yaml GET /purchase-orders/{purchaseOrderId}"
      },
      {
       "kind": "detailPanel",
       "label": "The stock transfer",
       "bindsTo": "StockTransfer",
       "columns": [
        "StockTransfer.id",
        "StockTransfer.transferNumber",
        "StockTransfer.fromLocationId",
        "StockTransfer.toLocationId",
        "StockTransfer.status",
        "StockTransfer.lines",
        "StockTransfer.dispatchedByPrincipalId",
        "StockTransfer.receivedByPrincipalId",
        "StockTransfer.dispatchedAt",
        "StockTransfer.receivedAt",
        "StockTransfer.closeShortReason",
        "StockTransfer.scopePath"
       ],
       "operation": "getStockTransfer",
       "provenance": "contract inventory.yaml GET /stock-transfers/{transferId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create goods receipt",
       "operation": "createGoodsReceipt",
       "permission": "PROCUREMENT_RECEIVE",
       "provenance": "contract inventory.yaml POST /goods-receipts"
      },
      {
       "kind": "secondaryButton",
       "label": "Acknowledge purchase order",
       "operation": "acknowledgePurchaseOrder",
       "permission": "PROCUREMENT_MANAGE",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/acknowledge"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel purchase order",
       "operation": "cancelPurchaseOrder",
       "permission": "PROCUREMENT_MANAGE",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close purchase order short",
       "operation": "closePurchaseOrderShort",
       "permission": "PROCUREMENT_MANAGE",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/close-short"
      },
      {
       "kind": "secondaryButton",
       "label": "Create purchase order",
       "operation": "createPurchaseOrder",
       "permission": "PROCUREMENT_MANAGE",
       "notes": "PO lines prefill the unit price from the selected quotation; changing it asks for an override reason (decided 28 September, audit R171).",
       "provenance": "contract inventory.yaml POST /purchase-orders"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject received goods",
       "operation": "rejectReceivedGoods",
       "permission": "PROCUREMENT_RECEIVE",
       "notes": "**Rejects receipt lines, not items** — the picker lists the receipt's batch/expiry lines by `lineId` (decided 28 September, audit R171). Choosing reason Other makes the note required (audit R222).",
       "provenance": "contract inventory.yaml POST /goods-receipts/{receiptId}/reject"
      },
      {
       "kind": "secondaryButton",
       "label": "Send purchase order",
       "operation": "sendPurchaseOrder",
       "permission": "PROCUREMENT_MANAGE",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/send"
      },
      {
       "kind": "destructiveButton",
       "label": "Close transfer short",
       "operation": "closeTransferShort",
       "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/close-short"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelPurchaseOrder",
    "component": "confirmDialog",
    "trigger": "Cancel purchase order",
    "body": "**Names what `cancelPurchaseOrder` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted. **Collects what `cancelPurchaseOrder` sends before it is called.** Required: `reason`. **It may answer 202 pending a finance approver** (decided 28 September, audit R144): the order is unchanged, shows *cancellation pending approval* and carries `approvalRequestId` until the approver acts.",
    "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/cancel"
   },
   {
    "id": "confirmClosePurchaseOrderShort",
    "component": "confirmDialog",
    "trigger": "Close purchase order short",
    "body": "**Names what `closePurchaseOrderShort` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted. **Collects what `closePurchaseOrderShort` sends before it is called.** Required: `reason`. **It may answer 202 pending a finance approver** (decided 28 September, audit R144): the order is unchanged, shows *close-short pending approval* and carries `approvalRequestId` until the approver acts.",
    "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/close-short"
   },
   {
    "id": "confirmRejectReceivedGoods",
    "component": "confirmDialog",
    "trigger": "Reject received goods",
    "body": "**Names what `rejectReceivedGoods` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted. **Collects what `rejectReceivedGoods` sends before it is called.** Required: `lines` — each a receipt line picked by `lineId` (the batch or expiry line, so one item received on two batches can be rejected on one of them) with the `quantity` rejected (decided 28 September, audit R171) — and `reason` (damaged, wrongItem, qualityFailure, shortDated, overDelivery, other). `note` is optional, **and required (at least 3 characters) when the reason is Other**; the dialog will not confirm without it and the server refuses 400 (decided 28 September, audit R222).",
    "provenance": "contract inventory.yaml POST /goods-receipts/{receiptId}/reject"
   },
   {
    "id": "confirmCloseTransferShort",
    "component": "confirmDialog",
    "trigger": "Close transfer short",
    "body": "**Names what `closeTransferShort` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted. **Collects what `closeTransferShort` sends before it is called.** Required: `reason` and `supervisorStepUp` — a supervisor enters their staff PIN on this device (`principalId`, `credential`); a refused PIN is 403 supervisor-step-up-refused (decided 28 September, audit R144).",
    "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/close-short"
   },
   {
    "id": "formCreateGoodsReceipt",
    "component": "modal",
    "trigger": "Create goods receipt",
    "body": "**Collects what `createGoodsReceipt` sends before it is called.** Required: `id`, `purchaseOrderId`, `locationId`, `lines`, `recordedAt`. Optional: `deliveryNoteReference`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateGoodsReceiptRequest",
    "confirm": {
     "label": "Create goods receipt",
     "operation": "createGoodsReceipt"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "purchaseOrderId",
      "locationId",
      "lines",
      "recordedAt",
      "deliveryNoteReference"
     ]
    },
    "provenance": "contract inventory.yaml POST /goods-receipts"
   },
   {
    "id": "formAcknowledgePurchaseOrder",
    "component": "modal",
    "trigger": "Acknowledge purchase order",
    "body": "**Collects what `acknowledgePurchaseOrder` sends before it is called.** Required: `supplierReference`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Acknowledge purchase order",
     "operation": "acknowledgePurchaseOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "supplierReference"
     ]
    },
    "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/acknowledge"
   },
   {
    "id": "formCreatePurchaseOrder",
    "component": "modal",
    "trigger": "Create purchase order",
    "body": "**Collects what `createPurchaseOrder` sends before it is called.** Required: `id`, `requisitionId`, `supplierId`, `quotationId`, `lines`, `expectedDelivery`. Optional: `deliverToLocationId`, `note`. **Each line's `unitPrice` is prefilled from the selected quotation**; if the user changes it, the line asks for `priceOverrideReason`, which the server requires (400) whenever the price differs from the quotation (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePurchaseOrderRequest",
    "confirm": {
     "label": "Create purchase order",
     "operation": "createPurchaseOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "requisitionId",
      "supplierId",
      "quotationId",
      "lines",
      "expectedDelivery",
      "deliverToLocationId",
      "note"
     ]
    },
    "provenance": "contract inventory.yaml POST /purchase-orders"
   }
  ],
  "states": {
   "loading": "The goods receipt list.",
   "error": "Could not load. Names which read failed and leaves the goods receipt untouched.",
   "emptyFirstRun": "No goods receipt yet. Offers Create goods receipt (`createGoodsReceipt`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, supplierId and the goods receipt are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PROCUREMENT_VIEW`, which `listPurchaseOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createGoodsReceipt",
    "contract": "inventory",
    "purpose": "Receive goods against a purchase order",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "listPurchaseOrders",
    "contract": "inventory",
    "purpose": "List purchase orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "acknowledgePurchaseOrder",
    "contract": "inventory",
    "purpose": "Record the supplier acknowledgement",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "cancelPurchaseOrder",
    "contract": "inventory",
    "purpose": "Cancel a purchase order",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "closePurchaseOrderShort",
    "contract": "inventory",
    "purpose": "Close an order accepting the balance will not arrive",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "createPurchaseOrder",
    "contract": "inventory",
    "purpose": "Raise a purchase order",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "getPurchaseOrder",
    "contract": "inventory",
    "purpose": "Read a purchase order with receipt progress",
    "trigger": "onAction"
   },
   {
    "operationId": "listGoodsReceipts",
    "contract": "inventory",
    "purpose": "List goods receipts",
    "trigger": "onLoad"
   },
   {
    "operationId": "rejectReceivedGoods",
    "contract": "inventory",
    "purpose": "Reject received goods",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "sendPurchaseOrder",
    "contract": "inventory",
    "purpose": "Issue the order to the supplier",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "closeTransferShort",
    "contract": "inventory",
    "purpose": "Close a transfer accepting the balance will not arrive",
    "trigger": "onAction",
    "invalidates": [
     "listPurchaseOrders"
    ]
   },
   {
    "operationId": "getStockTransfer",
    "contract": "inventory",
    "purpose": "One transfer, its manifest and where it is",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "purchaseOrderId",
     "from": "deepLink"
    },
    {
     "name": "receiptId",
     "from": "deepLink"
    },
    {
     "name": "transferId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `purchaseOrderId`, `receiptId`, `transferId`.",
   "preloaded": [
    "PurchaseOrder.id",
    "PurchaseOrder.purchaseOrderNumber",
    "PurchaseOrder.requisitionId",
    "PurchaseOrder.supplierId",
    "PurchaseOrder.supplierName"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-052",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-078",
  "name": "Requisitions",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/inventory/requisitions",
   "component": "apps/venue-management-web/src/routes/inventory/Requisitions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-079",
    "BO-080",
    "BO-081",
    "BO-084"
   ],
   "inferred": true,
   "fromFlows": true,
   "entryFrom": [
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "provenance": "flow F76 step 3→4, F92 step 3→4"
    },
    {
     "to": "BO-084",
     "trigger": "A manager approves it",
     "provenance": "flow F15 step 2→3",
     "operation": "createRequisition"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "provenance": "derived — BO-079 declares entryState.params countId and BO-078 holds none of them, so the edge carries nothing and BO-079 opens cold"
    },
    {
     "to": "BO-081",
     "trigger": "Inventory Items",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-081 declares entryState.params itemId and BO-078 holds itemId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 2 board screen(s): Requisition & Smart Replenishment; Store Inventory & Replenishment Configuration. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5f",
   "Retail Board 4.dc.html#ret-4c",
   "Retail Board 4.dc.html#ret-4k",
   "Inventory Board 4.dc.html#inv-4a",
   "Inventory Board 4.dc.html#inv-4e",
   "Inventory Board 4.dc.html#inv-4f",
   "Inventory Board 4.dc.html#inv-4h",
   "Inventory Board 4.dc.html#inv-4j",
   "Inventory Board 5.dc.html#inv-5b",
   "Inventory Board 5.dc.html#inv-5c",
   "Inventory Board 5.dc.html#inv-5d",
   "Inventory Board 5.dc.html#inv-5e",
   "Inventory Board 5.dc.html#inv-5f",
   "Inventory Board 5.dc.html#inv-5g"
  ],
  "pattern": "approvalInbox",
  "patternReason": "`approveRequisition` decides items that `listRequisitions` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Raise, track and approve a request to buy something.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listRequisitions",
       "notes": "Sends `?status=` to `listRequisitions`.",
       "provenance": "contract inventory.yaml GET /requisitions"
      },
      {
       "kind": "textField",
       "label": "Raised by principal id",
       "operation": "listRequisitions",
       "notes": "Sends `?raisedByPrincipalId=` to `listRequisitions`.",
       "provenance": "contract inventory.yaml GET /requisitions"
      },
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "Requisition",
       "columns": [
        "Requisition.id",
        "Requisition.requisitionNumber",
        "Requisition.venueId",
        "Requisition.departmentId",
        "Requisition.status",
        "Requisition.lines",
        "Requisition.estimatedTotal",
        "Requisition.raisedByPrincipalId",
        "Requisition.approvedByPrincipalId",
        "Requisition.approvalNote",
        "Requisition.requiredBy",
        "Requisition.approvedAt"
       ],
       "operation": "listRequisitions",
       "provenance": "contract inventory.yaml GET /requisitions"
      },
      {
       "kind": "dataTable",
       "label": "Every stock location",
       "bindsTo": "StockLocation",
       "columns": [
        "StockLocation.id",
        "StockLocation.code",
        "StockLocation.name",
        "StockLocation.venueId",
        "StockLocation.kind",
        "StockLocation.parentLocationId",
        "StockLocation.isActive"
       ],
       "operation": "listStockLocations",
       "provenance": "contract inventory.yaml GET /stock-locations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected requisition",
       "bindsTo": "Requisition",
       "columns": [
        "Requisition.id",
        "Requisition.requisitionNumber",
        "Requisition.venueId",
        "Requisition.departmentId",
        "Requisition.costCenterId",
        "Requisition.justification",
        "Requisition.status",
        "Requisition.lines",
        "Requisition.estimatedTotal",
        "Requisition.raisedByPrincipalId",
        "Requisition.approvedByPrincipalId",
        "Requisition.approvalNote",
        "Requisition.requiredBy",
        "Requisition.approvedAt",
        "Requisition.rejectionReason",
        "Requisition.rejectedAt"
       ],
       "operation": "listRequisitions",
       "provenance": "contract inventory.yaml GET /requisitions"
      },
      {
       "kind": "detailPanel",
       "label": "The requisition suggestion",
       "bindsTo": "RequisitionSuggestion",
       "columns": [
        "RequisitionSuggestion.itemId",
        "RequisitionSuggestion.itemName",
        "RequisitionSuggestion.sku",
        "RequisitionSuggestion.onHand",
        "RequisitionSuggestion.reorderPoint",
        "RequisitionSuggestion.parLevel",
        "RequisitionSuggestion.suggestedQuantity",
        "RequisitionSuggestion.averageDailyConsumption",
        "RequisitionSuggestion.daysOfCoverRemaining",
        "RequisitionSuggestion.preferredSupplierId",
        "RequisitionSuggestion.leadTimeDays"
       ],
       "operation": "getSuggestedRequisitions",
       "provenance": "contract inventory.yaml GET /requisitions/suggested"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create requisition",
       "operation": "createRequisition",
       "permission": "PROCUREMENT_REQUEST",
       "provenance": "contract inventory.yaml POST /requisitions"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve requisition",
       "operation": "approveRequisition",
       "permission": "APPROVAL_ACT",
       "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/approve"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject requisition",
       "operation": "rejectRequisition",
       "permission": "APPROVAL_ACT",
       "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/reject"
      },
      {
       "kind": "secondaryButton",
       "label": "Return requisition",
       "operation": "returnRequisition",
       "permission": "APPROVAL_ACT",
       "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/return"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel requisition",
       "operation": "cancelRequisition",
       "permission": "PROCUREMENT_REQUEST",
       "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Compare quotations",
       "operation": "compareQuotations",
       "permission": "PROCUREMENT_VIEW",
       "provenance": "contract inventory.yaml GET /requisitions/{requisitionId}/quotations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save requisition lines",
       "operation": "updateRequisitionLines",
       "permission": "PROCUREMENT_REQUEST",
       "provenance": "contract inventory.yaml PUT /requisitions/{requisitionId}/lines"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectRequisition",
    "component": "confirmDialog",
    "trigger": "Reject requisition",
    "body": "**Names what `rejectRequisition` changes and what it leaves alone**, in the consequence rather than the verb. A requisitions this affects should be identified in the dialog, not just counted. **Collects what `rejectRequisition` sends before it is called.** Required: `reason`.",
    "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/reject"
   },
   {
    "id": "confirmCancelRequisition",
    "component": "confirmDialog",
    "trigger": "Cancel requisition",
    "body": "**Names what `cancelRequisition` changes and what it leaves alone**, in the consequence rather than the verb. A requisitions this affects should be identified in the dialog, not just counted. **Collects what `cancelRequisition` sends before it is called.** Required: `reason`.",
    "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/cancel"
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
   },
   {
    "id": "formApproveRequisition",
    "component": "modal",
    "trigger": "Approve requisition",
    "body": "**Collects what `approveRequisition` sends before it is called.** Required: `decision`. Optional: `note`, `amendedLines`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Approve requisition",
     "operation": "approveRequisition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "note",
      "amendedLines"
     ]
    },
    "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/approve"
   },
   {
    "id": "formReturnRequisition",
    "component": "modal",
    "trigger": "Return requisition",
    "body": "**Collects what `returnRequisition` sends before it is called.** Required: `question`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Return requisition",
     "operation": "returnRequisition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "question"
     ]
    },
    "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/return"
   },
   {
    "id": "formUpdateRequisitionLines",
    "component": "modal",
    "trigger": "Save requisition lines",
    "body": "**Collects what `updateRequisitionLines` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save requisition lines",
     "operation": "updateRequisitionLines"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "lines"
     ]
    },
    "provenance": "contract inventory.yaml PUT /requisitions/{requisitionId}/lines"
   }
  ],
  "states": {
   "loading": "The requisitions list.",
   "error": "Could not load. Names which read failed and leaves the requisitions untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Nothing matches the filter on status, raisedByPrincipalId and the requisitions are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PROCUREMENT_VIEW`, which `listRequisitions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRequisitions",
    "contract": "inventory",
    "purpose": "List requisitions",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRequisition",
    "contract": "inventory",
    "purpose": "Raise a requisition",
    "trigger": "onAction",
    "invalidates": [
     "listRequisitions"
    ]
   },
   {
    "operationId": "approveRequisition",
    "contract": "inventory",
    "purpose": "Approve or reject a requisition",
    "trigger": "onAction",
    "invalidates": [
     "listRequisitions"
    ]
   },
   {
    "operationId": "rejectRequisition",
    "contract": "inventory",
    "purpose": "Reject a requisition",
    "trigger": "onAction",
    "invalidates": [
     "listRequisitions"
    ]
   },
   {
    "operationId": "returnRequisition",
    "contract": "inventory",
    "purpose": "Return a requisition for more information",
    "trigger": "onAction",
    "invalidates": [
     "listRequisitions"
    ]
   },
   {
    "operationId": "cancelRequisition",
    "contract": "inventory",
    "purpose": "Cancel a requisition",
    "trigger": "onAction",
    "invalidates": [
     "listRequisitions"
    ]
   },
   {
    "operationId": "getSuggestedRequisitions",
    "contract": "inventory",
    "purpose": "Draft requisitions from reorder points",
    "trigger": "onLoad"
   },
   {
    "operationId": "compareQuotations",
    "contract": "inventory",
    "purpose": "Compare quotations for a requisition",
    "trigger": "onAction"
   },
   {
    "operationId": "listStockLocations",
    "contract": "inventory",
    "purpose": "List stock locations",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateRequisitionLines",
    "contract": "inventory",
    "purpose": "Change what an outlet is asking for, before it is approved",
    "trigger": "onAction",
    "invalidates": [
     "listRequisitions"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "requisitionId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `requisitionId`.",
   "preloaded": [
    "Requisition.id",
    "Requisition.requisitionNumber",
    "Requisition.venueId",
    "Requisition.departmentId",
    "Requisition.costCenterId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-078",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-079",
  "name": "Stock Count",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/inventory/stock-count",
   "component": "apps/venue-management-web/src/routes/inventory/StockCount.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-049",
    "BO-078",
    "BO-080",
    "BO-081",
    "BO-137"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-049",
     "trigger": "Stock Levels",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-049 declares entryState.params itemId and BO-079 holds itemId, so an edge into it carries them"
    },
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "provenance": "derived — BO-078 declares entryState.params requisitionId and BO-079 holds none of them, so the edge carries nothing and BO-078 opens cold"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "provenance": "derived — BO-080 declares entryState.params transferId and BO-079 holds none of them, so the edge carries nothing and BO-080 opens cold"
    },
    {
     "to": "BO-081",
     "trigger": "Inventory Items",
     "provenance": "flow F76 step 1→2",
     "carries": [
      "itemId"
     ]
    },
    {
     "to": "BO-137",
     "trigger": "The variance feeds theoretical-against-actual",
     "provenance": "flow F30 step 7→8",
     "operation": "postStockCount",
     "carries": [
      "countId"
     ]
    },
    {
     "to": "EMP-066",
     "trigger": "The lines are recounted and re-entered",
     "provenance": "flow F30 step 5→6",
     "operation": "requestRecount",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "countId"
     ]
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 1 board screen(s): Stock Count, Reconciliation & Variance. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Blind counting (decided 28 September, audit R110)**: while a count is open or counting the screen shows the pre-filled item list with a blank count and no expected quantity or variance; variance appears only after submission.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5h",
   "Retail Board 4.dc.html#ret-4f",
   "Inventory Board 3.dc.html#inv-3a",
   "Inventory Board 3.dc.html#inv-3d",
   "Inventory Board 3.dc.html#inv-3e",
   "Inventory Board 3.dc.html#inv-3f"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockCounts` reads the population and `getCountVariance` reads one of them — list, select, act",
  "purpose": "Count what is there, blind, and resolve the variance.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Location id",
       "operation": "listStockCounts",
       "notes": "Sends `?locationId=` to `listStockCounts`.",
       "provenance": "contract inventory.yaml GET /stock-counts"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listStockCounts",
       "notes": "Sends `?status=` to `listStockCounts`.",
       "provenance": "contract inventory.yaml GET /stock-counts"
      },
      {
       "kind": "dataTable",
       "label": "Every stock count",
       "bindsTo": "StockCount",
       "columns": [
        "StockCount.id",
        "StockCount.locationId",
        "StockCount.locationName",
        "StockCount.kind",
        "StockCount.status",
        "StockCount.isBlind",
        "StockCount.lineCount",
        "StockCount.countedCount",
        "StockCount.varianceLineCount",
        "StockCount.varianceValue",
        "StockCount.startedByPrincipalId",
        "StockCount.postedByPrincipalId"
       ],
       "operation": "listStockCounts",
       "notes": "**Variance columns stay blank while a count is `open` or `counting`** (decided 28 September, audit R110) — they fill only once the count is submitted.",
       "provenance": "contract inventory.yaml GET /stock-counts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected stock count",
       "bindsTo": "StockCount",
       "columns": [
        "StockCount.id",
        "StockCount.locationId",
        "StockCount.locationName",
        "StockCount.kind",
        "StockCount.status",
        "StockCount.isBlind",
        "StockCount.lineCount",
        "StockCount.countedCount",
        "StockCount.varianceLineCount",
        "StockCount.varianceValue",
        "StockCount.startedByPrincipalId",
        "StockCount.postedByPrincipalId",
        "StockCount.journalEntryId",
        "StockCount.startedAt",
        "StockCount.closedAt",
        "StockCount.postedAt"
       ],
       "operation": "listStockCounts",
       "provenance": "contract inventory.yaml GET /stock-counts"
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
       "notes": "**Called only after the count is submitted** (decided 28 September, audit R110). While the count is `open` or `counting` the server answers 409 and the panel reads *Variance appears once the count is submitted* — never a zero.",
       "provenance": "contract inventory.yaml GET /stock-counts/{countId}/variance"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Start stock count",
       "operation": "startStockCount",
       "provenance": "contract inventory.yaml POST /stock-counts"
      },
      {
       "kind": "secondaryButton",
       "label": "Post stock count",
       "operation": "postStockCount",
       "provenance": "contract inventory.yaml POST /stock-counts/{countId}/post"
      },
      {
       "kind": "secondaryButton",
       "label": "Recount stock count",
       "operation": "recountStockCount",
       "provenance": "contract inventory.yaml POST /stock-counts/{countId}/recount"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel stock count",
       "operation": "cancelStockCount",
       "provenance": "contract inventory.yaml POST /stock-counts/{countId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Submit counted quantities",
       "operation": "submitCountLines",
       "notes": "**Lines arrive pre-filled from on-hand stock** — one per item at the location (per category for a cycle count) with the count blank; the counter enters only what is on the shelf. No expected quantity and no variance is shown while the count is open or counting (decided 28 September, audit R110, R171).",
       "provenance": "contract inventory.yaml POST /stock-counts/{countId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Enter count line",
       "operation": "enterCountLine",
       "notes": "**Shows the counted quantity only.** The F&B response still carries `theoreticalQuantity` and `variance`; the screen does not display them until the count is submitted (decided 28 September, audit R110).",
       "provenance": "contract fnb.yaml POST /fnb-stock-counts/{countId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Request recount",
       "operation": "requestRecount",
       "provenance": "contract fnb.yaml POST /fnb-stock-counts/{countId}/recount"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelStockCount",
    "component": "confirmDialog",
    "trigger": "Cancel stock count",
    "body": "**Names what `cancelStockCount` changes and what it leaves alone**, in the consequence rather than the verb. A stock count this affects should be identified in the dialog, not just counted. **Collects what `cancelStockCount` sends before it is called.** Required: `reason`.",
    "provenance": "contract inventory.yaml POST /stock-counts/{countId}/cancel"
   },
   {
    "id": "formStartStockCount",
    "component": "modal",
    "trigger": "Start stock count",
    "body": "**Collects what `startStockCount` sends before it is called.** Required: `id`, `locationId`, `kind`. Optional: `categoryIds`, `isBlind`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "StartStockCountRequest",
    "confirm": {
     "label": "Start stock count",
     "operation": "startStockCount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "locationId",
      "kind",
      "categoryIds",
      "isBlind"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-counts"
   },
   {
    "id": "formPostStockCount",
    "component": "modal",
    "trigger": "Post stock count",
    "body": "**Collects what `postStockCount` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Post stock count",
     "operation": "postStockCount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "note"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-counts/{countId}/post"
   },
   {
    "id": "formRecountStockCount",
    "component": "modal",
    "trigger": "Recount stock count",
    "body": "**Collects what `recountStockCount` sends before it is called.** Required: `reason` and `supervisorStepUp` — a supervisor enters their staff PIN on this device (`principalId`, `credential`); a refused PIN is 403 supervisor-step-up-refused (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Recount stock count",
     "operation": "recountStockCount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "supervisorStepUp"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-counts/{countId}/recount"
   },
   {
    "id": "formSubmitCountLines",
    "component": "modal",
    "trigger": "Submit counted quantities",
    "body": "**Collects what `submitCountLines` sends before it is called.** Required: `lines` (each `itemId`, `countedQuantity`, `recordedAt`; optional `unit`, `note`). The item list is pre-filled from on-hand stock with the count blank, and **no expected quantity or variance is shown** (decided 28 September, audit R110). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Submit counted quantities",
     "operation": "submitCountLines"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "lines"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-counts/{countId}/lines"
   },
   {
    "id": "formEnterCountLine",
    "component": "modal",
    "trigger": "Enter count line",
    "body": "**Collects what `enterCountLine` sends before it is called.** Required: `recordedAt`, `itemId`, `countedQuantity`. Optional: `locationId`, `uom`, `batchId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Enter count line",
     "operation": "enterCountLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "itemId",
      "countedQuantity",
      "locationId",
      "uom",
      "batchId",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /fnb-stock-counts/{countId}/lines"
   },
   {
    "id": "formRequestRecount",
    "component": "modal",
    "trigger": "Request recount",
    "body": "**Collects what `requestRecount` sends before it is called.** Required: `lineIds`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request recount",
     "operation": "requestRecount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "lineIds",
      "reason"
     ]
    },
    "provenance": "contract fnb.yaml POST /fnb-stock-counts/{countId}/recount"
   }
  ],
  "states": {
   "loading": "The stock count list.",
   "error": "Could not load. Names which read failed and leaves the stock count untouched.",
   "emptyFirstRun": "No stock count yet. Offers Request recount (`requestRecount`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on locationId, status and the stock count are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listStockCounts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStockCounts",
    "contract": "inventory",
    "purpose": "List stock counts",
    "trigger": "onLoad"
   },
   {
    "operationId": "startStockCount",
    "contract": "inventory",
    "purpose": "Start a stock count",
    "trigger": "onAction",
    "invalidates": [
     "listStockCounts"
    ]
   },
   {
    "operationId": "postStockCount",
    "contract": "inventory",
    "purpose": "Post a count and adjust stock",
    "trigger": "onAction",
    "invalidates": [
     "listStockCounts"
    ]
   },
   {
    "operationId": "recountStockCount",
    "contract": "inventory",
    "purpose": "Send a count back to be recounted",
    "trigger": "onAction",
    "invalidates": [
     "listStockCounts"
    ]
   },
   {
    "operationId": "cancelStockCount",
    "contract": "inventory",
    "purpose": "Abandon a count",
    "trigger": "onAction",
    "invalidates": [
     "listStockCounts"
    ]
   },
   {
    "operationId": "submitCountLines",
    "contract": "inventory",
    "purpose": "Submit counted quantities against the pre-filled lines; returns no expected quantity and no variance (decided 28 September, audit R110)",
    "trigger": "onAction",
    "invalidates": [
     "listStockCounts"
    ]
   },
   {
    "operationId": "getCountVariance",
    "contract": "inventory",
    "purpose": "Variance between counted and expected, once the count is submitted (409 before, audit R110)",
    "trigger": "onAction"
   },
   {
    "operationId": "enterCountLine",
    "contract": "fnb",
    "purpose": "What was actually on the shelf",
    "trigger": "onAction",
    "invalidates": [
     "listStockCounts"
    ]
   },
   {
    "operationId": "requestRecount",
    "contract": "fnb",
    "purpose": "Send a line back to be counted again",
    "trigger": "onAction",
    "invalidates": [
     "listStockCounts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "countId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `countId`.",
   "preloaded": [
    "StockCount.id",
    "StockCount.locationId",
    "StockCount.locationName",
    "StockCount.kind",
    "StockCount.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-079",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-080",
  "name": "Stock Transfers",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/inventory/stock-transfers",
   "component": "apps/venue-management-web/src/routes/inventory/StockTransfers.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-052",
    "BO-078",
    "BO-079",
    "BO-081"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "provenance": "derived — BO-078 declares entryState.params requisitionId and BO-080 holds none of them, so the edge carries nothing and BO-078 opens cold"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "provenance": "derived — BO-079 declares entryState.params countId and BO-080 holds none of them, so the edge carries nothing and BO-079 opens cold"
    },
    {
     "to": "BO-081",
     "trigger": "Inventory Items",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-081 declares entryState.params itemId and BO-080 holds itemId, so an edge into it carries them"
    },
    {
     "to": "BO-052",
     "trigger": "Goods Receipt",
     "provenance": "flow F76 step 4→5, F92 step 4→5",
     "carries": [
      "purchaseOrderId",
      "transferId"
     ]
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 1 board screen(s): Transfers, Distribution & Outlet Receiving. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4d",
   "Inventory Board 3.dc.html#inv-3b",
   "Inventory Board 3.dc.html#inv-3c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockTransfers` reads the population and `getStockTransfer` reads one of them — list, select, act",
  "purpose": "Move stock between venues, and receive what arrives. Shows inbound and outbound transfers for the venue (decided 28 September, audit R183).",
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
       "operation": "listStockTransfers",
       "notes": "Sends `?status=` to `listStockTransfers`.",
       "provenance": "contract inventory.yaml GET /stock-transfers"
      },
      {
       "kind": "dataTable",
       "label": "Every stock transfer",
       "bindsTo": "StockTransfer",
       "columns": [
        "StockTransfer.id",
        "StockTransfer.transferNumber",
        "StockTransfer.fromLocationId",
        "StockTransfer.toLocationId",
        "StockTransfer.status",
        "StockTransfer.lines",
        "StockTransfer.dispatchedByPrincipalId",
        "StockTransfer.receivedByPrincipalId",
        "StockTransfer.dispatchedAt",
        "StockTransfer.receivedAt",
        "StockTransfer.fromVenueId",
        "StockTransfer.toVenueId",
        "StockTransfer.scopePath"
       ],
       "operation": "listStockTransfers",
       "notes": "**Inbound and outbound** (decided 28 September, audit R183) — the list holds every transfer whose source or destination is this venue; each row is marked outbound (`fromVenueId` is this venue) or inbound (`toVenueId` is this venue), and the direction is a filter.",
       "provenance": "contract inventory.yaml GET /stock-transfers"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create stock transfer",
       "operation": "createStockTransfer",
       "provenance": "contract inventory.yaml POST /stock-transfers"
      },
      {
       "kind": "secondaryButton",
       "label": "Receive stock transfer",
       "operation": "receiveStockTransfer",
       "notes": "Offered on inbound transfers only — the destination venue receives (audit R183).",
       "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/receive"
      },
      {
       "kind": "destructiveButton",
       "label": "Close transfer short",
       "operation": "closeTransferShort",
       "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/close-short"
      },
      {
       "kind": "secondaryButton",
       "label": "Create goods receipt",
       "operation": "createGoodsReceipt",
       "provenance": "contract inventory.yaml POST /goods-receipts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "reads",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The stock transfer",
       "bindsTo": "StockTransfer",
       "columns": [
        "StockTransfer.id",
        "StockTransfer.transferNumber",
        "StockTransfer.fromLocationId",
        "StockTransfer.toLocationId",
        "StockTransfer.status",
        "StockTransfer.lines",
        "StockTransfer.dispatchedByPrincipalId",
        "StockTransfer.receivedByPrincipalId",
        "StockTransfer.dispatchedAt",
        "StockTransfer.receivedAt",
        "StockTransfer.closeShortReason",
        "StockTransfer.fromVenueId",
        "StockTransfer.toVenueId",
        "StockTransfer.scopePath"
       ],
       "operation": "getStockTransfer",
       "provenance": "contract inventory.yaml GET /stock-transfers/{transferId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseTransferShort",
    "component": "confirmDialog",
    "trigger": "Close transfer short",
    "body": "**Names what `closeTransferShort` changes and what it leaves alone**, in the consequence rather than the verb. A stock transfers this affects should be identified in the dialog, not just counted. **Collects what `closeTransferShort` sends before it is called.** Required: `reason` and `supervisorStepUp` — a supervisor enters their staff PIN on this device (`principalId`, `credential`); a refused PIN is 403 supervisor-step-up-refused (decided 28 September, audit R144).",
    "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/close-short"
   },
   {
    "id": "formCreateStockTransfer",
    "component": "modal",
    "trigger": "Create stock transfer",
    "body": "**Collects what `createStockTransfer` sends before it is called.** Required: `id`, `fromLocationId`, `toLocationId`, `lines`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateStockTransferRequest",
    "confirm": {
     "label": "Create stock transfer",
     "operation": "createStockTransfer"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "fromLocationId",
      "toLocationId",
      "lines",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-transfers"
   },
   {
    "id": "formReceiveStockTransfer",
    "component": "modal",
    "trigger": "Receive stock transfer",
    "body": "**Collects what `receiveStockTransfer` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Receive stock transfer",
     "operation": "receiveStockTransfer"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "lines"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/receive"
   },
   {
    "id": "formCreateGoodsReceipt",
    "component": "modal",
    "trigger": "Create goods receipt",
    "body": "**Collects what `createGoodsReceipt` sends before it is called.** Required: `id`, `purchaseOrderId`, `locationId`, `lines`, `recordedAt`. Optional: `deliveryNoteReference`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateGoodsReceiptRequest",
    "confirm": {
     "label": "Create goods receipt",
     "operation": "createGoodsReceipt"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "purchaseOrderId",
      "locationId",
      "lines",
      "recordedAt",
      "deliveryNoteReference"
     ]
    },
    "provenance": "contract inventory.yaml POST /goods-receipts"
   }
  ],
  "states": {
   "loading": "The stock transfers list.",
   "error": "Could not load. Names which read failed and leaves the stock transfers untouched.",
   "emptyFirstRun": "No stock transfers yet. Offers Create stock transfer (`createStockTransfer`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status and the stock transfers are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listStockTransfers` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStockTransfers",
    "contract": "inventory",
    "purpose": "Inbound and outbound transfers for this venue (decided 28 September, audit R183)",
    "trigger": "onLoad"
   },
   {
    "operationId": "createStockTransfer",
    "contract": "inventory",
    "purpose": "Send stock to another location",
    "trigger": "onAction",
    "invalidates": [
     "listStockTransfers"
    ]
   },
   {
    "operationId": "receiveStockTransfer",
    "contract": "inventory",
    "purpose": "Receive a transfer",
    "trigger": "onAction",
    "invalidates": [
     "listStockTransfers"
    ]
   },
   {
    "operationId": "closeTransferShort",
    "contract": "inventory",
    "purpose": "Close a transfer accepting the balance will not arrive",
    "trigger": "onAction",
    "invalidates": [
     "listStockTransfers"
    ]
   },
   {
    "operationId": "createGoodsReceipt",
    "contract": "inventory",
    "purpose": "Receive goods against a purchase order",
    "trigger": "onAction",
    "invalidates": [
     "listStockTransfers"
    ]
   },
   {
    "operationId": "getStockTransfer",
    "contract": "inventory",
    "purpose": "One transfer, its manifest and where it is",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "transferId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `transferId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-080",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-081",
  "name": "Inventory Items",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/inventory/inventory-items",
   "component": "apps/venue-management-web/src/routes/inventory/InventoryItems.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-078",
    "BO-079",
    "BO-080"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-049",
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "provenance": "flow F76 step 2→3, F92 step 2→3"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "provenance": "derived — BO-079 declares entryState.params countId and BO-081 holds none of them, so the edge carries nothing and BO-079 opens cold"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "provenance": "derived — BO-080 declares entryState.params transferId and BO-081 holds none of them, so the edge carries nothing and BO-080 opens cold"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4b",
   "Inventory Board 1.dc.html#inv-2",
   "Inventory Board 1.dc.html#inv-3",
   "Inventory Board 1.dc.html#inv-4",
   "Inventory Board 1.dc.html#inv-5",
   "Inventory Board 2.dc.html#inv-2b",
   "Inventory Board 2.dc.html#inv-2c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listInventoryItems` reads the population and `getInventoryItem` reads one of them — list, select, act",
  "purpose": "What the venue stocks, and where.",
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
       "label": "Every stock location",
       "bindsTo": "StockLocation",
       "columns": [
        "StockLocation.id",
        "StockLocation.code",
        "StockLocation.name",
        "StockLocation.venueId",
        "StockLocation.kind",
        "StockLocation.parentLocationId",
        "StockLocation.isActive"
       ],
       "operation": "listStockLocations",
       "provenance": "contract inventory.yaml GET /stock-locations"
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
       "operation": "getInventoryItem",
       "provenance": "contract inventory.yaml GET /inventory-items/{itemId}"
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
      },
      {
       "kind": "secondaryButton",
       "label": "Save inventory item",
       "operation": "updateInventoryItem",
       "provenance": "contract inventory.yaml PATCH /inventory-items/{itemId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup inventory item",
       "operation": "lookupInventoryItem",
       "provenance": "contract inventory.yaml GET /inventory-items/lookup"
      },
      {
       "kind": "secondaryButton",
       "label": "Create stock location",
       "operation": "createStockLocation",
       "provenance": "contract inventory.yaml POST /stock-locations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory items list.",
   "error": "Could not load. Names which read failed and leaves the inventory items untouched.",
   "emptyFirstRun": "No inventory items yet. Offers Create inventory item (`createInventoryItem`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, categoryId, belowReorderPoint, search and the inventory items are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listInventoryItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listInventoryItems",
    "contract": "inventory",
    "purpose": "List inventory items",
    "trigger": "onLoad"
   },
   {
    "operationId": "getInventoryItem",
    "contract": "inventory",
    "purpose": "Read an item with stock position",
    "trigger": "onAction"
   },
   {
    "operationId": "createInventoryItem",
    "contract": "inventory",
    "purpose": "Create an inventory item",
    "trigger": "onAction",
    "invalidates": [
     "listInventoryItems"
    ]
   },
   {
    "operationId": "updateInventoryItem",
    "contract": "inventory",
    "purpose": "Amend an item",
    "trigger": "onAction",
    "invalidates": [
     "listInventoryItems"
    ]
   },
   {
    "operationId": "lookupInventoryItem",
    "contract": "inventory",
    "purpose": "Look up by barcode or SKU",
    "trigger": "onAction"
   },
   {
    "operationId": "listStockLocations",
    "contract": "inventory",
    "purpose": "List stock locations",
    "trigger": "onLoad"
   },
   {
    "operationId": "createStockLocation",
    "contract": "inventory",
    "purpose": "Create a stock location",
    "trigger": "onAction",
    "invalidates": [
     "listInventoryItems"
    ]
   },
   {
    "operationId": "getInventoryKitDefinition",
    "contract": "inventory",
    "purpose": "Show kit components",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setInventoryKitDefinition",
    "contract": "inventory",
    "purpose": "Edit kit components",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "itemId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `itemId`.",
   "preloaded": [
    "InventoryItem.sku",
    "InventoryItem.barcode",
    "InventoryItem.name",
    "InventoryItem.venueId",
    "InventoryItem.categoryId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-081",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
   },
   {
    "id": "formUpdateInventoryItem",
    "component": "modal",
    "trigger": "Save inventory item",
    "body": "**Collects what `updateInventoryItem` sends before it is called.** Nothing in the body is required. Optional: `name`, `categoryId`, `reorderPoint`, `reorderQuantity`, `parLevel`, `preferredSupplierId`, `isActive`, `costingMethod`, `baseUnit`. **Category and preferred supplier can be cleared** — each picker has a *None* choice that sends `null` (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save inventory item",
     "operation": "updateInventoryItem"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "categoryId",
      "reorderPoint",
      "reorderQuantity",
      "parLevel",
      "preferredSupplierId",
      "isActive",
      "costingMethod",
      "baseUnit"
     ]
    },
    "provenance": "contract inventory.yaml PATCH /inventory-items/{itemId}"
   },
   {
    "id": "formCreateStockLocation",
    "component": "modal",
    "trigger": "Create stock location",
    "body": "**Collects what `createStockLocation` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`. Optional: `parentLocationId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create stock location",
     "operation": "createStockLocation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "kind",
      "parentLocationId"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-locations"
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
  "id": "BO-082",
  "name": "Stock Movements",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/inventory/stock-movements",
   "component": "apps/venue-management-web/src/routes/inventory/StockMovements.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-078",
    "BO-079",
    "BO-080"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-079",
     "trigger": "A cycle count on that line is triggered to confirm the position",
     "provenance": "flow F35 step 7→8"
    },
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "provenance": "derived — BO-078 declares entryState.params requisitionId and BO-082 holds none of them, so the edge carries nothing and BO-078 opens cold"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "provenance": "derived — BO-080 declares entryState.params transferId and BO-082 holds none of them, so the edge carries nothing and BO-080 opens cold"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Moved to wave 1 on 24 August.** F34 walks a retail sale and its return, which is a wave-1 journey — **a venue that can take a return and cannot disposition the item puts damaged stock back on the shelf**, and the count finds it three weeks later.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4g",
   "Inventory Board 1.dc.html#inv-8",
   "Inventory Board 2.dc.html#inv-2j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockMovements` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Every movement, and why it happened.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Item id",
       "operation": "listStockMovements",
       "notes": "Sends `?itemId=` to `listStockMovements`.",
       "provenance": "contract inventory.yaml GET /stock-movements"
      },
      {
       "kind": "textField",
       "label": "Location id",
       "operation": "listStockMovements",
       "notes": "Sends `?locationId=` to `listStockMovements`.",
       "provenance": "contract inventory.yaml GET /stock-movements"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listStockMovements",
       "notes": "Sends `?kind=` to `listStockMovements`. Offers every `MovementKind`, including `adjustmentIn`/`adjustmentOut` and `countGain`/`countLoss`, which replaced `adjustment` and `countAdjustment` (audit R171).",
       "provenance": "contract inventory.yaml GET /stock-movements"
      },
      {
       "kind": "datePicker",
       "label": "Recorded from",
       "operation": "listStockMovements",
       "notes": "Sends `?recordedFrom=` to `listStockMovements`.",
       "provenance": "contract inventory.yaml GET /stock-movements"
      },
      {
       "kind": "datePicker",
       "label": "Recorded to",
       "operation": "listStockMovements",
       "notes": "Sends `?recordedTo=` to `listStockMovements`.",
       "provenance": "contract inventory.yaml GET /stock-movements"
      },
      {
       "kind": "dataTable",
       "label": "Every stock movement",
       "bindsTo": "StockMovement",
       "columns": [
        "StockMovement.id",
        "StockMovement.itemId",
        "StockMovement.locationId",
        "StockMovement.kind",
        "StockMovement.quantity",
        "StockMovement.unit",
        "StockMovement.reason",
        "StockMovement.costCenterId",
        "StockMovement.recordedAt",
        "StockMovement.balanceAfter",
        "StockMovement.unitCost",
        "StockMovement.totalCost"
       ],
       "operation": "listStockMovements",
       "notes": "`countGain` and `countLoss` rows are shown (posted by a stock count), never entered here; quantity is always positive and the kind shows the direction (decided 28 September, audit R171).",
       "provenance": "contract inventory.yaml GET /stock-movements"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected stock movement",
       "bindsTo": "StockMovement",
       "columns": [
        "StockMovement.id",
        "StockMovement.itemId",
        "StockMovement.locationId",
        "StockMovement.kind",
        "StockMovement.quantity",
        "StockMovement.unit",
        "StockMovement.reason",
        "StockMovement.costCenterId",
        "StockMovement.recordedAt",
        "StockMovement.balanceAfter",
        "StockMovement.unitCost",
        "StockMovement.totalCost",
        "StockMovement.principalId",
        "StockMovement.sourceType",
        "StockMovement.sourceId",
        "StockMovement.journalEntryId"
       ],
       "operation": "listStockMovements",
       "provenance": "contract inventory.yaml GET /stock-movements"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create stock movement",
       "operation": "createStockMovement",
       "provenance": "contract inventory.yaml POST /stock-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Create stock transfer",
       "operation": "createStockTransfer",
       "provenance": "contract inventory.yaml POST /stock-transfers"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stock movements list.",
   "error": "Could not load. Names which read failed and leaves the stock movements untouched.",
   "emptyFirstRun": "No stock movements yet. Offers Create stock movement (`createStockMovement`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on itemId, locationId, kind, recordedFrom, recordedTo and the stock movements are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listStockMovements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStockMovements",
    "contract": "inventory",
    "purpose": "The movement ledger",
    "trigger": "onLoad"
   },
   {
    "operationId": "createStockMovement",
    "contract": "inventory",
    "purpose": "Record an issue, return or adjustment",
    "trigger": "onAction",
    "invalidates": [
     "listStockMovements"
    ]
   },
   {
    "operationId": "createStockTransfer",
    "contract": "inventory",
    "purpose": "Send stock to another location",
    "trigger": "onAction",
    "invalidates": [
     "listStockMovements"
    ]
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "StockMovement.id",
    "StockMovement.itemId",
    "StockMovement.locationId",
    "StockMovement.kind",
    "StockMovement.quantity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-082",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateStockMovement",
    "component": "modal",
    "trigger": "Create stock movement",
    "body": "**Collects what `createStockMovement` sends before it is called.** Required: `id`, `itemId`, `locationId`, `kind`, `quantity`, `recordedAt`. Optional: `unit`, `reason`, `costCenterId`. **The kind picker offers `adjustmentIn` and `adjustmentOut`** (and issue, waste, supplierReturn); the kind decides the direction, so **quantity is entered positive** and the field refuses a sign. **Reason is required for adjustmentIn, adjustmentOut and waste** — the dialog will not confirm without it and the server refuses 400 (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateStockMovementRequest",
    "confirm": {
     "label": "Create stock movement",
     "operation": "createStockMovement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "itemId",
      "locationId",
      "kind",
      "quantity",
      "recordedAt",
      "unit",
      "reason",
      "costCenterId"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-movements"
   },
   {
    "id": "formCreateStockTransfer",
    "component": "modal",
    "trigger": "Create stock transfer",
    "body": "**Collects what `createStockTransfer` sends before it is called.** Required: `id`, `fromLocationId`, `toLocationId`, `lines`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateStockTransferRequest",
    "confirm": {
     "label": "Create stock transfer",
     "operation": "createStockTransfer"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "fromLocationId",
      "toLocationId",
      "lines",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract inventory.yaml POST /stock-transfers"
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
  "id": "BO-083",
  "name": "Suppliers",
  "module": "Stock & Supply",
  "requiresModule": "inventory",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/inventory/suppliers",
   "component": "apps/venue-management-web/src/routes/inventory/Suppliers.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-007",
    "BO-078",
    "BO-079",
    "BO-080"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "carries": [
      "requisitionId"
     ],
     "provenance": "derived — BO-078 declares entryState.params requisitionId and BO-083 holds requisitionId, so an edge into it carries them"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "provenance": "derived — BO-079 declares entryState.params countId and BO-083 holds none of them, so the edge carries nothing and BO-079 opens cold"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "provenance": "derived — BO-080 declares entryState.params transferId and BO-083 holds none of them, so the edge carries nothing and BO-080 opens cold"
    },
    {
     "to": "BO-007",
     "trigger": "The new range becomes products in the directory",
     "provenance": "flow F78 step 1→2"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "Retail Board 2.dc.html#ret-2g",
   "Inventory Board 4.dc.html#inv-4b",
   "Inventory Board 4.dc.html#inv-4c",
   "Inventory Board 4.dc.html#inv-4d",
   "Inventory Board 7.dc.html#inv-7f"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSuppliers` reads the population and `getSupplierPerformance` reads one of them — list, select, act",
  "purpose": "Who we buy from, and what they quoted. Suppliers are the tenant's; a venue sees them read-only and records quotations (decided 28 September, audit R183).",
  "gaps": [
   {
    "operation": "getSupplierPerformance",
    "why": "**`getSupplierPerformance` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract reporting.yaml GET /suppliers/{supplierId}/performance"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every supplier",
       "bindsTo": "Supplier",
       "columns": [
        "Supplier.id",
        "Supplier.code",
        "Supplier.name",
        "Supplier.contactName",
        "Supplier.contactEmail",
        "Supplier.contactPhone",
        "Supplier.taxRegistrationNumber",
        "Supplier.paymentTermsDays",
        "Supplier.leadTimeDays",
        "Supplier.currency",
        "Supplier.accountId",
        "Supplier.isActive"
       ],
       "operation": "listSuppliers",
       "provenance": "contract inventory.yaml GET /suppliers"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create supplier",
       "operation": "createSupplier",
       "permission": "PROCUREMENT_MANAGE",
       "notes": "**Tenant scope only** (decided 28 September, audit R183) — suppliers are created and edited at tenant level; a session scoped to a venue does not see this button.",
       "provenance": "contract inventory.yaml POST /suppliers"
      },
      {
       "kind": "secondaryButton",
       "label": "Record quotation",
       "operation": "recordQuotation",
       "permission": "PROCUREMENT_MANAGE",
       "notes": "A venue user records quotations against the tenant's suppliers; the quotation carries the venue's scope (decided 28 September, audit R183).",
       "provenance": "contract inventory.yaml POST /suppliers/{supplierId}/quotations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save supplier",
       "operation": "updateSupplier",
       "permission": "PROCUREMENT_MANAGE",
       "notes": "**Tenant scope only** (decided 28 September, audit R183); at venue scope the supplier is read-only.",
       "provenance": "contract inventory.yaml PUT /suppliers/{supplierId}"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "reads",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Supplier performance",
       "operation": "getSupplierPerformance",
       "notes": "Shows `ordersPlaced`, `onTimeInFullPercent`, `averageDaysLate`, `shortDeliveryPercent`, `rejectionPercent`, `rejectionReasons`, `priceVariancePercent` from `getSupplierPerformance`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract reporting.yaml GET /suppliers/{supplierId}/performance"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The suppliers list.",
   "error": "Could not load. Names which read failed and leaves the suppliers untouched.",
   "emptyFirstRun": "No suppliers yet. At tenant scope offers Create supplier (`createSupplier`); at venue scope says suppliers are set up by the tenant (audit R183).",
   "emptyNoResults": "Never shown: `listSuppliers` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PROCUREMENT_VIEW`, which `listSuppliers` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSuppliers",
    "contract": "inventory",
    "purpose": "List suppliers",
    "trigger": "onLoad"
   },
   {
    "operationId": "createSupplier",
    "contract": "inventory",
    "purpose": "Create a supplier — tenant scope only; venues read suppliers (decided 28 September, audit R183)",
    "trigger": "onAction",
    "invalidates": [
     "listSuppliers"
    ]
   },
   {
    "operationId": "recordQuotation",
    "contract": "inventory",
    "purpose": "Record a supplier quotation",
    "trigger": "onAction",
    "invalidates": [
     "listSuppliers"
    ]
   },
   {
    "operationId": "updateSupplier",
    "contract": "inventory",
    "purpose": "Change terms, or stop buying from them — tenant scope only (audit R183)",
    "trigger": "onAction",
    "invalidates": [
     "listSuppliers"
    ]
   },
   {
    "operationId": "getSupplierPerformance",
    "contract": "reporting",
    "purpose": "getSupplierPerformance",
    "trigger": "onAction"
   },
   {
    "operationId": "listSupplierContracts",
    "contract": "inventory",
    "purpose": "Supplier contracts list",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "createSupplierContract",
    "contract": "inventory",
    "purpose": "Add a supplier contract",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "updateSupplierContract",
    "contract": "inventory",
    "purpose": "Edit, activate or end a supplier contract",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "supplierId",
     "from": "deepLink"
    },
    {
     "name": "contractId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `supplierId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-083",
   "derivedFrom": "wireframes/reference/Retail Board 2.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateSupplier",
    "component": "modal",
    "trigger": "Create supplier",
    "body": "**Collects what `createSupplier` sends before it is called.** Required: `id`, `code`, `name`. Optional: `contactName`, `contactEmail`, `contactPhone`, `taxRegistrationNumber`, `paymentTermsDays`, `leadTimeDays`, `currency`, `accountId`, `isActive`, `status`, `statusReason`, `minimumOrderValue` and 1 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Supplier",
    "confirm": {
     "label": "Create supplier",
     "operation": "createSupplier"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "contactName",
      "contactEmail",
      "contactPhone",
      "taxRegistrationNumber",
      "paymentTermsDays",
      "leadTimeDays",
      "currency",
      "accountId",
      "isActive",
      "status",
      "statusReason",
      "minimumOrderValue",
      "scopePath"
     ]
    },
    "provenance": "contract inventory.yaml POST /suppliers"
   },
   {
    "id": "formRecordQuotation",
    "component": "modal",
    "trigger": "Record quotation",
    "body": "**Collects what `recordQuotation` sends before it is called.** Required: `requisitionId`, `lines`, `validUntil`. Optional: `reference`, `leadTimeDays`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateQuotationRequest",
    "confirm": {
     "label": "Record quotation",
     "operation": "recordQuotation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "requisitionId",
      "lines",
      "validUntil",
      "reference",
      "leadTimeDays",
      "note"
     ]
    },
    "provenance": "contract inventory.yaml POST /suppliers/{supplierId}/quotations"
   },
   {
    "id": "formUpdateSupplier",
    "component": "modal",
    "trigger": "Save supplier",
    "body": "**Collects what `updateSupplier` sends before it is called.** Nothing in the body is required. Optional: `name`, `status`, `statusReason`, `paymentTermDays`, `leadTimeDays`, `minimumOrderValue`, `contacts`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save supplier",
     "operation": "updateSupplier"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "status",
      "statusReason",
      "paymentTermDays",
      "leadTimeDays",
      "minimumOrderValue",
      "contacts"
     ]
    },
    "provenance": "contract inventory.yaml PUT /suppliers/{supplierId}"
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
 "acknowledgePurchaseOrder": {
  "method": "POST",
  "path": "/purchase-orders/{purchaseOrderId}/acknowledge",
  "contract": "inventory",
  "summary": "Record the supplier acknowledgement",
  "permission": "PROCUREMENT_MANAGE",
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
  "responds": "PurchaseOrder"
 },
 "approveRequisition": {
  "method": "POST",
  "path": "/requisitions/{requisitionId}/approve",
  "contract": "inventory",
  "summary": "Approve or reject a requisition",
  "permission": "APPROVAL_ACT",
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
  "responds": "Requisition"
 },
 "cancelPurchaseOrder": {
  "method": "POST",
  "path": "/purchase-orders/{purchaseOrderId}/cancel",
  "contract": "inventory",
  "summary": "Cancel a purchase order",
  "permission": "PROCUREMENT_MANAGE",
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
  "responds": "PurchaseOrder"
 },
 "cancelRequisition": {
  "method": "POST",
  "path": "/requisitions/{requisitionId}/cancel",
  "contract": "inventory",
  "summary": "Cancel a requisition",
  "permission": "PROCUREMENT_REQUEST",
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
  "responds": "Requisition"
 },
 "cancelStockCount": {
  "method": "POST",
  "path": "/stock-counts/{countId}/cancel",
  "contract": "inventory",
  "summary": "Abandon a count",
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
  "requestBody": null,
  "responds": "StockCount"
 },
 "closePurchaseOrderShort": {
  "method": "POST",
  "path": "/purchase-orders/{purchaseOrderId}/close-short",
  "contract": "inventory",
  "summary": "Close an order accepting the balance will not arrive",
  "permission": "PROCUREMENT_MANAGE",
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
  "responds": "PurchaseOrder"
 },
 "closeTransferShort": {
  "method": "POST",
  "path": "/stock-transfers/{transferId}/close-short",
  "contract": "inventory",
  "summary": "Close a transfer accepting the balance will not arrive",
  "permission": "LEDGER_APPROVE",
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
  "responds": "StockTransfer"
 },
 "compareQuotations": {
  "method": "GET",
  "path": "/requisitions/{requisitionId}/quotations",
  "contract": "inventory",
  "summary": "Compare quotations for a requisition",
  "permission": "PROCUREMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "QuotationComparison"
 },
 "createGoodsReceipt": {
  "method": "POST",
  "path": "/goods-receipts",
  "contract": "inventory",
  "summary": "Receive goods against a purchase order",
  "permission": "PROCUREMENT_RECEIVE",
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
  "requestBody": "CreateGoodsReceiptRequest",
  "responds": "GoodsReceipt"
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
 "createPurchaseOrder": {
  "method": "POST",
  "path": "/purchase-orders",
  "contract": "inventory",
  "summary": "Raise a purchase order",
  "permission": "PROCUREMENT_MANAGE",
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
  "requestBody": "CreatePurchaseOrderRequest",
  "responds": "PurchaseOrder"
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
 "createStockLocation": {
  "method": "POST",
  "path": "/stock-locations",
  "contract": "inventory",
  "summary": "Create a stock location",
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
  "requestBody": null,
  "responds": "StockLocation"
 },
 "createStockMovement": {
  "method": "POST",
  "path": "/stock-movements",
  "contract": "inventory",
  "summary": "Record an issue, return or adjustment",
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
  "requestBody": "CreateStockMovementRequest",
  "responds": "StockMovement"
 },
 "createStockTransfer": {
  "method": "POST",
  "path": "/stock-transfers",
  "contract": "inventory",
  "summary": "Send stock to another location",
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
  "requestBody": "CreateStockTransferRequest",
  "responds": "StockTransfer"
 },
 "createSupplier": {
  "method": "POST",
  "path": "/suppliers",
  "contract": "inventory",
  "summary": "Create a supplier",
  "permission": "PROCUREMENT_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "Supplier",
  "responds": "Supplier"
 },
 "createSupplierContract": {
  "method": "POST",
  "path": "/suppliers/{supplierId}/contracts",
  "contract": "inventory",
  "summary": "Record a purchasing contract with a supplier",
  "permission": "PROCUREMENT_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "InventorySupplierContract"
 },
 "enterCountLine": {
  "method": "POST",
  "path": "/fnb-stock-counts/{countId}/lines",
  "contract": "fnb",
  "summary": "What was actually on the shelf",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
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
 "getInventoryItem": {
  "method": "GET",
  "path": "/inventory-items/{itemId}",
  "contract": "inventory",
  "summary": "Read an item with stock position",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "InventoryItem"
 },
 "getInventoryKitDefinition": {
  "method": "GET",
  "path": "/inventory-items/{itemId}/kit-definition",
  "contract": "inventory",
  "summary": "The components a kit item is made of",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "InventoryKitDefinition"
 },
 "getPurchaseOrder": {
  "method": "GET",
  "path": "/purchase-orders/{purchaseOrderId}",
  "contract": "inventory",
  "summary": "Read a purchase order with receipt progress",
  "permission": "PROCUREMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PurchaseOrder"
 },
 "getStockPositions": {
  "method": "GET",
  "path": "/stock",
  "contract": "inventory",
  "summary": "Stock on hand by item and location",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "itemId",
    "in": "query",
    "required": null
   },
   {
    "name": "includeZero",
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
 "getStockTransfer": {
  "method": "GET",
  "path": "/stock-transfers/{transferId}",
  "contract": "inventory",
  "summary": "One transfer, its manifest and where it is",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "StockTransfer"
 },
 "getStockValuation": {
  "method": "GET",
  "path": "/stock/valuation",
  "contract": "inventory",
  "summary": "Stock value by location and category",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "StockValuation"
 },
 "getSuggestedRequisitions": {
  "method": "GET",
  "path": "/requisitions/suggested",
  "contract": "inventory",
  "summary": "Draft requisitions from reorder points",
  "permission": "PROCUREMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "locationId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getSupplierPerformance": {
  "method": "GET",
  "path": "/suppliers/{supplierId}/performance",
  "contract": "reporting",
  "summary": "On-time, in-full, and what was rejected",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "listGoodsReceipts": {
  "method": "GET",
  "path": "/goods-receipts",
  "contract": "inventory",
  "summary": "List goods receipts",
  "permission": "PROCUREMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "purchaseOrderId",
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
 "listOrders": {
  "method": "GET",
  "path": "/orders",
  "contract": "orders",
  "summary": "List orders",
  "permission": "ORDER_VIEW",
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
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "createdTo",
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
 "listRequisitions": {
  "method": "GET",
  "path": "/requisitions",
  "contract": "inventory",
  "summary": "List requisitions",
  "permission": "PROCUREMENT_VIEW",
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
    "name": "raisedByPrincipalId",
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
 "listStockCounts": {
  "method": "GET",
  "path": "/stock-counts",
  "contract": "inventory",
  "summary": "List stock counts",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
 "listStockLocations": {
  "method": "GET",
  "path": "/stock-locations",
  "contract": "inventory",
  "summary": "List stock locations",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "listStockMovements": {
  "method": "GET",
  "path": "/stock-movements",
  "contract": "inventory",
  "summary": "The movement ledger",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "itemId",
    "in": "query",
    "required": null
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedTo",
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
 "listStockTransfers": {
  "method": "GET",
  "path": "/stock-transfers",
  "contract": "inventory",
  "summary": "List transfers",
  "permission": "PRODUCT_VIEW",
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
 "listSupplierContracts": {
  "method": "GET",
  "path": "/supplier-contracts",
  "contract": "inventory",
  "summary": "Supplier contracts, by supplier, status or expiry",
  "permission": "PROCUREMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "supplierId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "expiringBefore",
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
 "listSuppliers": {
  "method": "GET",
  "path": "/suppliers",
  "contract": "inventory",
  "summary": "List suppliers",
  "permission": "PROCUREMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "lookupInventoryItem": {
  "method": "GET",
  "path": "/inventory-items/lookup",
  "contract": "inventory",
  "summary": "Look up by barcode or SKU",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "barcode",
    "in": "query",
    "required": null
   },
   {
    "name": "sku",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "InventoryItem"
 },
 "postStockCount": {
  "method": "POST",
  "path": "/stock-counts/{countId}/post",
  "contract": "inventory",
  "summary": "Post a count and adjust stock",
  "permission": "LEDGER_POST",
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
  "responds": "StockCount"
 },
 "receiveStockTransfer": {
  "method": "POST",
  "path": "/stock-transfers/{transferId}/receive",
  "contract": "inventory",
  "summary": "Receive a transfer",
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
  "requestBody": null,
  "responds": "StockTransfer"
 },
 "recordQuotation": {
  "method": "POST",
  "path": "/suppliers/{supplierId}/quotations",
  "contract": "inventory",
  "summary": "Record a supplier quotation",
  "permission": "PROCUREMENT_MANAGE",
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
  "requestBody": "CreateQuotationRequest",
  "responds": "Quotation"
 },
 "recountStockCount": {
  "method": "POST",
  "path": "/stock-counts/{countId}/recount",
  "contract": "inventory",
  "summary": "Send a count back to be recounted",
  "permission": "LEDGER_APPROVE",
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
  "responds": "StockCount"
 },
 "rejectReceivedGoods": {
  "method": "POST",
  "path": "/goods-receipts/{receiptId}/reject",
  "contract": "inventory",
  "summary": "Reject received goods",
  "permission": "PROCUREMENT_RECEIVE",
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
  "responds": "GoodsReceipt"
 },
 "rejectRequisition": {
  "method": "POST",
  "path": "/requisitions/{requisitionId}/reject",
  "contract": "inventory",
  "summary": "Reject a requisition",
  "permission": "APPROVAL_ACT",
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
  "responds": "Requisition"
 },
 "requestRecount": {
  "method": "POST",
  "path": "/fnb-stock-counts/{countId}/recount",
  "contract": "fnb",
  "summary": "Send a line back to be counted again",
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
  "requestBody": null,
  "responds": "RecountResult"
 },
 "returnRequisition": {
  "method": "POST",
  "path": "/requisitions/{requisitionId}/return",
  "contract": "inventory",
  "summary": "Return a requisition for more information",
  "permission": "APPROVAL_ACT",
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
  "responds": "Requisition"
 },
 "sendPurchaseOrder": {
  "method": "POST",
  "path": "/purchase-orders/{purchaseOrderId}/send",
  "contract": "inventory",
  "summary": "Issue the order to the supplier",
  "permission": "PROCUREMENT_MANAGE",
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
  "responds": "PurchaseOrder"
 },
 "setInventoryKitDefinition": {
  "method": "PUT",
  "path": "/inventory-items/{itemId}/kit-definition",
  "contract": "inventory",
  "summary": "Make an item a kit of other stocked items",
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
  "requestBody": "InventoryKitDefinition",
  "responds": "InventoryKitDefinition"
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MenuItem"
 },
 "startStockCount": {
  "method": "POST",
  "path": "/stock-counts",
  "contract": "inventory",
  "summary": "Start a stock count",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "StartStockCountRequest",
  "responds": "StockCount"
 },
 "submitCountLines": {
  "method": "POST",
  "path": "/stock-counts/{countId}/lines",
  "contract": "inventory",
  "summary": "Submit counted quantities",
  "permission": "PRODUCT_CONFIGURE",
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
 "updateInventoryItem": {
  "method": "PATCH",
  "path": "/inventory-items/{itemId}",
  "contract": "inventory",
  "summary": "Amend an item",
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
  "requestBody": null,
  "responds": "InventoryItem"
 },
 "updateRequisitionLines": {
  "method": "PUT",
  "path": "/requisitions/{requisitionId}/lines",
  "contract": "inventory",
  "summary": "Change what an outlet is asking for, before it is approved",
  "permission": "PROCUREMENT_REQUEST",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Requisition"
 },
 "updateSupplier": {
  "method": "PUT",
  "path": "/suppliers/{supplierId}",
  "contract": "inventory",
  "summary": "Change terms, or stop buying from them",
  "permission": "PROCUREMENT_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Supplier"
 },
 "updateSupplierContract": {
  "method": "PATCH",
  "path": "/supplier-contracts/{contractId}",
  "contract": "inventory",
  "summary": "Extend, activate or end a supplier contract",
  "permission": "PROCUREMENT_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "InventorySupplierContract"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "CountStatus": {
  "type": "string",
  "enum": [
   "open",
   "counting",
   "closed",
   "variancePending",
   "posted",
   "cancelled"
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
 "CreateGoodsReceiptRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "purchaseOrderId",
   "locationId",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "purchaseOrderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "deliveryNoteReference": {
    "type": "string",
    "maxLength": 128
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "itemId",
      "receivedQuantity"
     ],
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "receivedQuantity": {
       "type": "number",
       "minimum": 0
      },
      "unit": {
       "type": "string"
      },
      "batchNumber": {
       "type": "string",
       "maxLength": 64
      },
      "expiryDate": {
       "type": "string",
       "format": "date",
       "description": "Required for perishable items."
      },
      "note": {
       "type": "string",
       "maxLength": 200
      }
     }
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
 "CreatePurchaseOrderRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "requisitionId",
   "supplierId",
   "quotationId",
   "lines",
   "expectedDelivery"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "requisitionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "supplierId": {
    "type": "string",
    "format": "uuid"
   },
   "quotationId": {
    "type": "string",
    "format": "uuid"
   },
   "deliverToLocationId": {
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
      "unitPrice": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Omitted, the selected quotation line's price. **Editable with a reason** (decided 28 September, audit R171).\n"
      },
      "priceOverrideReason": {
       "type": "string",
       "maxLength": 500,
       "nullable": true,
       "description": "Required when `unitPrice` differs from the quotation line (audit R171)."
      }
     }
    }
   },
   "expectedDelivery": {
    "type": "string",
    "format": "date"
   },
   "note": {
    "type": "string",
    "maxLength": 1000
   }
  }
 },
 "CreateQuotationRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "requisitionId",
   "lines",
   "validUntil"
  ],
  "properties": {
   "requisitionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "reference": {
    "type": "string",
    "maxLength": 128
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "itemId",
      "unitPrice",
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
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "unit": {
       "type": "string"
      }
     }
    }
   },
   "leadTimeDays": {
    "type": "integer"
   },
   "validUntil": {
    "type": "string",
    "format": "date"
   },
   "note": {
    "type": "string",
    "maxLength": 1000
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
 "CreateStockMovementRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "itemId",
   "locationId",
   "kind",
   "quantity",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "itemId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MovementKind"
   },
   "quantity": {
    "type": "number",
    "exclusiveMinimum": 0,
    "description": "Always positive. **The `kind` decides whether it adds or removes stock**, not the sign (decided 28 September, audit R171).\n"
   },
   "unit": {
    "type": "string"
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "description": "**Required for `adjustmentIn`, `adjustmentOut` and `waste`** (decided 28 September, audit R171); adjustments are reported separately.\n"
   },
   "costCenterId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateStockTransferRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "fromLocationId",
   "toLocationId",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "fromLocationId": {
    "type": "string",
    "format": "uuid"
   },
   "toLocationId": {
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
      }
     }
    }
   },
   "note": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "GoodsReceipt": {
  "x-ticvai-persistence": "inventory.goods_receipt + inventory.goods_receipt_line",
  "type": "object",
  "required": [
   "id",
   "receiptNumber",
   "purchaseOrderId",
   "locationId",
   "lines",
   "receivedByPrincipalId",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "receiptNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152), e.g. `MAR-GR-000431`. Not gapless; only tax invoices are gapless, per legal entity. A receipt recorded offline takes the next number from the range its device holds in reserve.\n"
   },
   "purchaseOrderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "deliveryNoteReference": {
    "type": "string",
    "nullable": true
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "lineId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
       "readOnly": true,
       "description": "One batch or expiry line of the receipt. What `rejectReceivedGoods` addresses (decided 28 September, audit R171).\n"
      },
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "itemName": {
       "type": "string"
      },
      "orderedQuantity": {
       "type": "number"
      },
      "receivedQuantity": {
       "type": "number"
      },
      "rejectedQuantity": {
       "type": "number"
      },
      "batchNumber": {
       "type": "string",
       "nullable": true
      },
      "expiryDate": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "unitCost": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "totalValue": {
    "x-ticvai-column": "net_value_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "receivedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "journalEntryId": {
    "type": "string",
    "nullable": true,
    "description": "The accrual the supplier invoice will later match against."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "InventoryKitComponent": {
  "x-ticvai-persistence": "inventory.kit_component",
  "type": "object",
  "description": "4.4.20. One component of a kit and the quantity one kit consumes.",
  "required": [
   "componentItemId",
   "quantity"
  ],
  "properties": {
   "kitItemId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "componentItemId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "number",
    "exclusiveMinimum": 0
   },
   "unit": {
    "type": "string",
    "nullable": true,
    "description": "The component's base unit where omitted."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the kit item's venue scope."
   }
  }
 },
 "InventoryKitDefinition": {
  "x-ticvai-persistence": "none — composed of the item's inventory.kit_component rows",
  "type": "object",
  "description": "4.4.20. Also the `setInventoryKitDefinition` body.",
  "required": [
   "components"
  ],
  "properties": {
   "kitItemId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "components": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/InventoryKitComponent"
    }
   }
  }
 },
 "InventorySupplierContract": {
  "type": "object",
  "x-ticvai-persistence": "inventory.supplier_contract",
  "description": "**Taken from the backend workbook, 20 September.** Stores purchasing agreements, validity dates, and commercial terms agreed with a supplier.",
  "required": [
   "supplierId",
   "number",
   "name",
   "validFrom",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "supplierId": {
    "type": "string",
    "format": "uuid"
   },
   "number": {
    "type": "string",
    "maxLength": 100
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "currencyCode": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "paymentTermsDays": {
    "type": "integer",
    "nullable": true
   },
   "documentReference": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "status": {
    "type": "string",
    "maxLength": 30,
    "enum": [
     "draft",
     "active",
     "expired",
     "terminated"
    ],
    "description": "Written by `createSupplierContract` and `updateSupplierContract`; `expired` is set by the server once `validTo` has passed (29 September, writers pass)."
   },
   "statusReason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "LocationKind": {
  "type": "string",
  "enum": [
   "mainStore",
   "subStore",
   "kitchen",
   "bar",
   "retailFloor",
   "cellar",
   "transit"
  ]
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
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
   }
  }
 },
 "MovementKind": {
  "type": "string",
  "description": "**The kind decides the direction** (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` (the finished item entering stock; the ingredients leave as `issue`). Out: `issue`, `saleDepletion`, `waste`, `adjustmentOut`, `transferOut`, `countLoss`, `supplierReturn`. `adjustment` and `countAdjustment` were split into an in and an out kind so that no kind has two directions.\n",
  "enum": [
   "receipt",
   "issue",
   "saleDepletion",
   "waste",
   "adjustmentIn",
   "adjustmentOut",
   "transferOut",
   "transferIn",
   "countGain",
   "countLoss",
   "supplierReturn",
   "production"
  ]
 },
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
 },
 "OrderSummary": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "id",
   "orderNumber",
   "status",
   "grossAmount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderNumber": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "The same vocabulary as `Order.channel`, which this projects."
   },
   "lineCount": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "The cashier who raised it — what the held-orders list shows."
   },
   "holdLabel": {
    "type": "string",
    "nullable": true,
    "description": "As `Order.holdLabel`."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
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
 "PurchaseOrder": {
  "x-ticvai-persistence": "inventory.purchase_order + inventory.purchase_order_line",
  "type": "object",
  "required": [
   "id",
   "purchaseOrderNumber",
   "supplierId",
   "status",
   "lines",
   "total",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "purchaseOrderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Per venue, in sequence** (decided 28 September, audit R171). Assigned by the server from the venue's gap-free sequence, or the tenant's for an order with no venue. Proposed format `PO-<venue code>-<sequence, six digits>`, client to correct.\n"
   },
   "requisitionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "Null on a blanket order or an RFQ award, which are raised without one."
   },
   "quotationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The quotation selected when the order was raised (`createPurchaseOrder` requires it). **The link that shows the comparison was made**, which `rfqId` alone does not."
   },
   "supplierId": {
    "type": "string",
    "format": "uuid"
   },
   "supplierName": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "standard",
     "blanket",
     "release",
     "rfqAward"
    ],
    "default": "standard",
    "description": "BL-159. **A blanket order is a price and a commitment, not a delivery.** Releases draw against it, and modelling each release as its own purchase order loses the contract that makes the price valid.\n"
   },
   "blanketParentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The blanket order this release draws against — another purchase order, so the same id type."
   },
   "contractPriceValidUntil": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "rfqId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where this order came from a quotation round. **Keeping the link is what lets a venue show it took the best of three**, which is usually the procurement rule rather than a preference.\n"
   },
   "supplierInvoiceRef": {
    "type": "string",
    "nullable": true,
    "description": "BL-123. **Purchase orders and goods receipts both existed — the third leg did not.** A three-way match with two legs is a two-way match, and it is the supplier invoice that carries the price nobody has checked yet.\n"
   },
   "matchStatus": {
    "type": "string",
    "nullable": true,
    "enum": [
     "unmatched",
     "matched",
     "priceVariance",
     "quantityVariance",
     "bothVariance"
    ],
    "description": "**The variance kinds are separated because they have different owners** — a price variance is a buyer's problem and a quantity variance is a receiving one.\n"
   },
   "status": {
    "$ref": "#/components/schemas/PurchaseOrderStatus"
   },
   "deliverToLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Scoped 31 August.** A purchase order is raised by somebody, for somewhere, and carried neither. `requisitionId` reaches a venue through a join, but **a purchase order raised without a requisition — a blanket order, an RFQ award — had no scope at all**, so nothing could answer *whose budget is this* without guessing.\n\n**`deliverToLocationId` is separate from `venueId` on purpose.** A tenant buying centrally and delivering to three venues is one order and three destinations; collapsing them would force one order per venue and lose the volume the tenant negotiated for."
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
      "orderedQuantity": {
       "type": "number"
      },
      "receivedQuantity": {
       "type": "number"
      },
      "outstandingQuantity": {
       "type": "number"
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "quotedUnitPrice": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "nullable": true,
       "description": "The selected quotation line's price, kept beside `unitPrice` (audit R171)."
      },
      "priceOverrideReason": {
       "type": "string",
       "nullable": true,
       "description": "Why `unitPrice` differs from `quotedUnitPrice` (audit R171)."
      },
      "lineTotal": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "subtotal": {
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "expectedDelivery": {
    "type": "string",
    "format": "date"
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "supplierReference": {
    "type": "string",
    "nullable": true,
    "description": "The supplier's own order reference, from `acknowledgePurchaseOrder`."
   },
   "acknowledgedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Null is the supplier performance figure** — goods arriving against an order never acknowledged."
   },
   "closeShortReason": {
    "type": "string",
    "nullable": true,
    "description": "Why the balance was written off, from `closePurchaseOrderShort`."
   },
   "cancelReason": {
    "type": "string",
    "nullable": true,
    "description": "From `cancelPurchaseOrder`."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The pending approval request raised by `cancelPurchaseOrder` or `closePurchaseOrderShort` (kinds `purchaseOrderCancel`, `purchaseOrderShortClose`; audit R144). Null when none is open."
   },
   "cancelledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Which venue is buying. **Null on a tenant-level order** — see `deliverToLocationId`."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Present on every order regardless of whether a venue is named, because a tenant-level order still belongs to a tenant."
   }
  }
 },
 "PurchaseOrderStatus": {
  "type": "string",
  "enum": [
   "raised",
   "sent",
   "acknowledged",
   "partiallyReceived",
   "received",
   "closedShort",
   "cancelled"
  ]
 },
 "Quotation": {
  "x-ticvai-persistence": "inventory.quotation + inventory.quotation_line",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateQuotationRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "supplierId",
     "total",
     "receivedAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "supplierId": {
      "type": "string",
      "format": "uuid"
     },
     "supplierName": {
      "type": "string"
     },
     "total": {
      "x-ticvai-column": "gross_amount",
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "isSelected": {
      "type": "boolean"
     },
     "receivedAt": {
      "type": "string",
      "format": "date-time"
     },
     "scopePath": {
      "type": "string",
      "description": "The partition key. A quotation is sought by somebody and the scope says who, the venue that recorded it, against a tenant supplier (audit R183)."
     }
    }
   }
  ]
 },
 "QuotationComparison": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "requisitionId",
   "quotations",
   "lowestTotalSupplierId"
  ],
  "properties": {
   "requisitionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "quotations": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Quotation"
    }
   },
   "lowestTotalSupplierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "shortestLeadTimeSupplierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "byLine": {
    "type": "array",
    "description": "Per-line comparison. The cheapest total is not always the cheapest line.",
    "items": {
     "type": "object",
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "itemName": {
       "type": "string"
      },
      "prices": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "supplierId": {
          "type": "string",
          "format": "uuid"
         },
         "unitPrice": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         },
         "isLowest": {
          "type": "boolean"
         }
        }
       }
      }
     }
    }
   }
  }
 },
 "RecountResult": {
  "type": "object",
  "x-ticvai-persistence": "none — response shape",
  "description": "The lines `requestRecount` reopened.",
  "required": [
   "countId",
   "reopenedLineIds"
  ],
  "properties": {
   "countId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "reopenedLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "reason": {
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
 "RequisitionSuggestion": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "itemId",
   "onHand",
   "reorderPoint",
   "suggestedQuantity"
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
   "onHand": {
    "type": "number"
   },
   "reorderPoint": {
    "type": "number"
   },
   "parLevel": {
    "type": "number"
   },
   "suggestedQuantity": {
    "type": "number"
   },
   "averageDailyConsumption": {
    "type": "number"
   },
   "daysOfCoverRemaining": {
    "type": "number"
   },
   "preferredSupplierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "leadTimeDays": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "StartStockCountRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "locationId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "full",
     "cycle",
     "spot"
    ]
   },
   "categoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "For cycle counts — restrict to these categories."
   },
   "isBlind": {
    "type": "boolean",
    "default": true,
    "description": "Expected quantities withheld from the counting device. Defaults true because a counter who can see the figure reconciles to it rather than to the shelf. **The expected quantity and the variance stay hidden until the count is submitted** (decided 28 September, audit R110).\n"
   }
  }
 },
 "StockCount": {
  "x-ticvai-persistence": "inventory.count + inventory.count_line",
  "type": "object",
  "required": [
   "id",
   "locationId",
   "kind",
   "status",
   "isBlind",
   "lineCount",
   "countedCount",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "locationName": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/CountStatus"
   },
   "isBlind": {
    "type": "boolean"
   },
   "lineCount": {
    "type": "integer"
   },
   "countedCount": {
    "type": "integer"
   },
   "varianceLineCount": {
    "type": "integer"
   },
   "varianceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "startedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "postedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "journalEntryId": {
    "type": "string",
    "nullable": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "postedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recountReason": {
    "type": "string",
    "nullable": true,
    "description": "Why the count was last sent back by `recountStockCount`."
   },
   "recountSignedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The supervisor whose step-up sent the count back last (audit R144)."
   },
   "cancelReason": {
    "type": "string",
    "nullable": true,
    "description": "Why it was abandoned, from `cancelStockCount`."
   }
  }
 },
 "StockLocation": {
  "x-ticvai-persistence": "inventory.location",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/LocationKind"
   },
   "parentLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "StockMovement": {
  "x-ticvai-persistence": "inventory.movement",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateStockMovementRequest"
   },
   {
    "type": "object",
    "required": [
     "balanceAfter",
     "principalId",
     "createdAt"
    ],
    "properties": {
     "balanceAfter": {
      "type": "number"
     },
     "unitCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "totalCost": {
      "x-ticvai-column": "net_cost_amount",
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "principalId": {
      "type": "string",
      "format": "uuid"
     },
     "sourceType": {
      "type": "string",
      "nullable": true,
      "description": "What generated it — an order, a count, a transfer."
     },
     "sourceId": {
      "type": "string",
      "nullable": true
     },
     "journalEntryId": {
      "type": "string",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "StockPosition": {
  "x-ticvai-persistence": "none — derived from movements",
  "type": "object",
  "required": [
   "itemId",
   "locationId",
   "onHand",
   "unit"
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
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "locationName": {
    "type": "string"
   },
   "onHand": {
    "type": "number"
   },
   "allocated": {
    "type": "number",
    "description": "**Reserved for orders**: the quantity under an active stock reservation for an order (decided 28 September, audit R171). A transfer is not allocation: dispatched stock has already left on-hand and sits in transit.\n"
   },
   "available": {
    "type": "number",
    "description": "**On-hand minus allocated** (decided 28 September, audit R171). What can still be sold or issued.\n"
   },
   "unit": {
    "type": "string"
   },
   "value": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lastCountedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastMovementAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "StockTransfer": {
  "x-ticvai-persistence": "inventory.transfer + inventory.transfer_line",
  "type": "object",
  "required": [
   "id",
   "fromLocationId",
   "toLocationId",
   "status",
   "lines",
   "dispatchedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "transferNumber": {
    "type": "string"
   },
   "fromLocationId": {
    "type": "string",
    "format": "uuid"
   },
   "toLocationId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "$ref": "#/components/schemas/TransferStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "itemName": {
       "type": "string"
      },
      "dispatchedQuantity": {
       "type": "number"
      },
      "receivedQuantity": {
       "type": "number",
       "nullable": true
      },
      "discrepancy": {
       "type": "number",
       "nullable": true
      },
      "discrepancyReason": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "dispatchedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "receivedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "dispatchedAt": {
    "type": "string",
    "format": "date-time"
   },
   "receivedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closeShortReason": {
    "type": "string",
    "nullable": true,
    "description": "Why the balance was written off, from `closeTransferShort`."
   },
   "closeShortSignedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The supervisor whose step-up closed the transfer short (audit R144)."
   },
   "fromVenueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The venue of `fromLocationId`. Set by the server (audit R183)."
   },
   "toVenueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The venue of `toLocationId`. Set by the server (audit R183)."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). `fromLocationId` and `toLocationId` give the endpoints; **this gives the owner**, the source venue's scope.\n\n**Both venues see a transfer between them** (decided 28 September, audit R183). It used to sit at the tenant above both, where neither venue could see it. The row is owned at the source venue and `toScopePath` admits the destination venue too."
   },
   "toScopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The destination venue's scope. Row-level security admits a caller whose scope matches `scopePath` or `toScopePath`, so both venues read the transfer (decided 28 September, audit R183).\n"
   }
  }
 },
 "StockValuation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asAt",
   "total",
   "byLocation"
  ],
  "properties": {
   "asAt": {
    "type": "string",
    "format": "date"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "byLocation": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "locationId": {
       "type": "string",
       "format": "uuid"
      },
      "locationName": {
       "type": "string"
      },
      "value": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "itemCount": {
       "type": "integer"
      }
     }
    }
   },
   "byCategory": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "categoryId": {
       "type": "string",
       "format": "uuid"
      },
      "categoryName": {
       "type": "string"
      },
      "value": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "SupervisorStepUp": {
  "type": "object",
  "description": "**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n",
  "required": [
   "principalId",
   "credential"
  ],
  "properties": {
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "The supervisor signing. Recorded against the act."
   },
   "credential": {
    "type": "string",
    "maxLength": 512,
    "writeOnly": true,
    "description": "The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."
   }
  }
 },
 "Supplier": {
  "x-ticvai-persistence": "inventory.supplier",
  "type": "object",
  "required": [
   "id",
   "code",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "x-ticvai-unique": "tenant",
    "description": "**Unique per tenant** (decided 28 September, audit R108).\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "contactName": {
    "type": "string",
    "nullable": true
   },
   "contactEmail": {
    "type": "string",
    "nullable": true
   },
   "contactPhone": {
    "type": "string",
    "nullable": true
   },
   "taxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "paymentTermsDays": {
    "type": "integer",
    "nullable": true
   },
   "leadTimeDays": {
    "type": "integer",
    "nullable": true
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "accountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "onHold",
     "suspended",
     "terminated"
    ],
    "description": "Set by `updateSupplier`. **A supplier on hold stops appearing in requisitions and purchase orders while its history stays intact.**"
   },
   "statusReason": {
    "type": "string",
    "nullable": true
   },
   "minimumOrderValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.** Suppliers are owned at tenant and venues quote against them (decided 28 September, audit R183)."
   }
  }
 },
 "TransferStatus": {
  "type": "string",
  "enum": [
   "dispatched",
   "inTransit",
   "received",
   "partiallyReceived",
   "cancelled"
  ]
 }
}
```
