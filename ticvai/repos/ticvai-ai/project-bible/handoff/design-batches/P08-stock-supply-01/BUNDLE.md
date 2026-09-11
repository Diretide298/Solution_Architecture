# P08-stock-supply-01 — P08 · Stock & Supply (1 of 2)

**10 screens · 51 operations · 31 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `APPROVAL_ACT, LEDGER_APPROVE, LEDGER_POST, LEDGER_VIEW, ORDER_CANCEL, ORDER_CREATE, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **16 of these operations work offline**: createGoodsReceipt, createRequisition, enterCountLine, getCountVariance, getInventoryItem, getStockPositions, getStockTransfer, getVenueSettings
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-049` | Stock Levels | listDetail | 6 | 0 | — |
| `BO-050` | Stock Position & Valuation | statusTracker | 2 | 0 | — |
| `BO-052` | Goods Receipt | listDetail | 12 | 4 | — |
| `BO-078` | Requisitions | approvalInbox | 10 | 2 | — |
| `BO-079` | Stock Count | listDetail | 8 | 1 | — |
| `BO-080` | Stock Transfers | listDetail | 6 | 1 | — |
| `BO-081` | Inventory Items | listDetail | 7 | 0 | — |
| `BO-082` | Stock Movements | listDetail | 4 | 0 | — |
| `BO-083` | Suppliers | listDetail | 5 | 0 | — |
| `BO-105` | Stock & Supply | listDetail | 4 | 0 | — |

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
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
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
     "to": "BO-081",
     "trigger": "Inventory Items",
     "provenance": "flow F92 step 1→2"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "carries": [
      "countId"
     ],
     "provenance": "derived — BO-079 declares entryState.params countId, so an edge into it must carry them"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "carries": [
      "transferId"
     ],
     "provenance": "derived — BO-080 declares entryState.params transferId, so an edge into it must carry them"
    },
    {
     "to": "EMP-065",
     "trigger": "The delivery arrives",
     "provenance": "flow F35 step 1→2",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): F&B Stock & Operations Command Center; Outlet Stock & Ingredient Availability. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5a",
   "FnB Board 5.dc.html#fnb-5b",
   "Retail Board 4.dc.html#ret-4a",
   "Retail Board 4.dc.html#ret-4h"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockLocations` reads the population and `getStockPositions` reads one of them — list, select, act",
  "purpose": "Know what is on the shelf and what is on order.",
  "gaps": [
   {
    "operation": "getStockValuation",
    "why": "**1 declared operation reach no component on this screen**: getStockValuation. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every stock levels",
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
       "label": "The selected stock levels",
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
       "label": "Save changes",
       "operation": "setItemAvailability",
       "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createStockTransfer",
       "provenance": "contract inventory.yaml POST /stock-transfers"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createStockMovement",
       "provenance": "contract inventory.yaml POST /stock-movements"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setItemAvailability",
       "label": "Save item availability",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listStockLocations",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setItemAvailability",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stock levels list.",
   "error": "Could not load. Names which read failed and leaves the stock levels untouched.",
   "emptyFirstRun": "No stock levels yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stock levels are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "StockPosition.itemId",
    "StockPosition.itemName",
    "StockPosition.sku",
    "StockPosition.locationId",
    "StockPosition.locationName"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-049",
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
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Named `Stock Count` and carrying `getStockPositions` and `getStockValuation`** — two screens with one name, while `BO-079 Stock Count` holds the actual counting operations. Renamed 20 August; the operations were right.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getStockPositions` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Count the shelf and account for the difference.",
  "gaps": [
   {
    "operation": "getStockValuation",
    "why": "**1 declared operation reach no component on this screen**: getStockValuation. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected stock position valuation",
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
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stock position valuation list.",
   "error": "Could not load. Names which read failed and leaves the stock position valuation untouched.",
   "emptyFirstRun": "No stock position valuation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stock position valuation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-049"
   ],
   "inferred": true,
   "fromFlows": true,
   "entryFrom": [
    "BO-080",
    "BO-105"
   ],
   "transitions": [
    {
     "to": "BO-049",
     "trigger": "The website has already sold four of the damaged units",
     "provenance": "flow F35 step 4→5"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    },
    {
     "to": "EMP-005",
     "trigger": "The technician resumes",
     "provenance": "flow F15 step 4→5",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Pulled to Wave 2 (CF-101). Requisitions are Wave 1 and receipt was Wave 3 — **the end of the chain arriving two waves after the start.** **Cross-platform navigation removed 24 August**: EMP-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPurchaseOrders` reads the population and `getPurchaseOrder` reads one of them — list, select, act",
  "purpose": "Book in what actually arrived.",
  "gaps": [
   {
    "operation": "listGoodsReceipts",
    "why": "**2 declared operations reach no component on this screen**: listGoodsReceipts, getStockTransfer. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every goods receipt",
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
        "PurchaseOrder.status"
       ],
       "operation": "listPurchaseOrders",
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
       "label": "The selected goods receipt",
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
       "label": "Create",
       "operation": "createGoodsReceipt",
       "provenance": "contract inventory.yaml POST /goods-receipts"
      },
      {
       "kind": "secondaryButton",
       "label": "Acknowledge",
       "operation": "acknowledgePurchaseOrder",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/acknowledge"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelPurchaseOrder",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closePurchaseOrderShort",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/close-short"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPurchaseOrder",
       "provenance": "contract inventory.yaml POST /purchase-orders"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectReceivedGoods",
       "provenance": "contract inventory.yaml POST /goods-receipts/{receiptId}/reject"
      },
      {
       "kind": "secondaryButton",
       "label": "Send",
       "operation": "sendPurchaseOrder",
       "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/send"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeTransferShort",
       "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/close-short"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createGoodsReceipt",
       "label": "Create goods receipt",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPurchaseOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelPurchaseOrder",
       "label": "Cancel purchase order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createGoodsReceipt",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelPurchaseOrder",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelPurchaseOrder` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/cancel"
   },
   {
    "id": "confirmClosePurchaseOrderShort",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closePurchaseOrderShort` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /purchase-orders/{purchaseOrderId}/close-short"
   },
   {
    "id": "confirmRejectReceivedGoods",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Names what `rejectReceivedGoods` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /goods-receipts/{receiptId}/reject"
   },
   {
    "id": "confirmCloseTransferShort",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeTransferShort` changes and what it leaves alone**, in the consequence rather than the verb. A goods receipt this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/close-short"
   }
  ],
  "states": {
   "loading": "The goods receipt list.",
   "error": "Could not load. Names which read failed and leaves the goods receipt untouched.",
   "emptyFirstRun": "No goods receipt yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the goods receipt are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
    "BO-001",
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
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "carries": [
      "countId"
     ],
     "provenance": "derived — BO-079 declares entryState.params countId, so an edge into it must carry them"
    },
    {
     "to": "BO-081",
     "trigger": "Inventory Items",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-081 declares entryState.params itemId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 2 board screen(s): Requisition & Smart Replenishment; Store Inventory & Replenishment Configuration. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5f",
   "Retail Board 4.dc.html#ret-4c",
   "Retail Board 4.dc.html#ret-4k"
  ],
  "pattern": "approvalInbox",
  "patternReason": "`approveRequisition` decides items that `listRequisitions` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Raise, track and approve a request to buy something.",
  "gaps": [
   {
    "operation": "listStockLocations",
    "why": "**1 declared operation reach no component on this screen**: listStockLocations. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected requisitions",
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
       "label": "Create",
       "operation": "createRequisition",
       "provenance": "contract inventory.yaml POST /requisitions"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "operation": "approveRequisition",
       "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/approve"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectRequisition",
       "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/reject"
      },
      {
       "kind": "secondaryButton",
       "label": "Return",
       "operation": "returnRequisition",
       "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/return"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelRequisition",
       "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Compare",
       "operation": "compareQuotations",
       "provenance": "contract inventory.yaml GET /requisitions/{requisitionId}/quotations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateRequisitionLines",
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
    "trigger": "Reject",
    "body": "**Names what `rejectRequisition` changes and what it leaves alone**, in the consequence rather than the verb. A requisitions this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/reject"
   },
   {
    "id": "confirmCancelRequisition",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelRequisition` changes and what it leaves alone**, in the consequence rather than the verb. A requisitions this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /requisitions/{requisitionId}/cancel"
   }
  ],
  "states": {
   "loading": "The requisitions list.",
   "error": "Could not load. Names which read failed and leaves the requisitions untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the requisitions are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
    "RequisitionSuggestion.itemId",
    "RequisitionSuggestion.itemName",
    "RequisitionSuggestion.sku",
    "RequisitionSuggestion.onHand",
    "RequisitionSuggestion.reorderPoint"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-078",
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
    "BO-001",
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
     "to": "BO-081",
     "trigger": "Inventory Items",
     "provenance": "flow F76 step 1→2"
    },
    {
     "to": "BO-137",
     "trigger": "The variance feeds theoretical-against-actual",
     "provenance": "flow F30 step 7→8",
     "operation": "postStockCount"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-049",
     "trigger": "Stock Levels",
     "carries": [
      "itemId",
      "venueId"
     ],
     "provenance": "derived — BO-049 declares entryState.params itemId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "carries": [
      "requisitionId"
     ],
     "provenance": "derived — BO-078 declares entryState.params requisitionId, so an edge into it must carry them"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "carries": [
      "transferId"
     ],
     "provenance": "derived — BO-080 declares entryState.params transferId, so an edge into it must carry them"
    },
    {
     "to": "EMP-066",
     "trigger": "The lines are recounted and re-entered",
     "provenance": "flow F30 step 5→6",
     "operation": "requestRecount",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 1 board screen(s): Stock Count, Reconciliation & Variance. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5h",
   "Retail Board 4.dc.html#ret-4f"
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Start",
       "operation": "startStockCount",
       "provenance": "contract inventory.yaml POST /stock-counts"
      },
      {
       "kind": "secondaryButton",
       "label": "Post",
       "operation": "postStockCount",
       "provenance": "contract inventory.yaml POST /stock-counts/{countId}/post"
      },
      {
       "kind": "secondaryButton",
       "label": "Recount",
       "operation": "recountStockCount",
       "provenance": "contract inventory.yaml POST /stock-counts/{countId}/recount"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelStockCount",
       "provenance": "contract inventory.yaml POST /stock-counts/{countId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Enter",
       "operation": "enterCountLine",
       "provenance": "contract fnb.yaml POST /stock-counts/{countId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Request",
       "operation": "requestRecount",
       "provenance": "contract fnb.yaml POST /stock-counts/{countId}/recount"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelStockCount",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelStockCount` changes and what it leaves alone**, in the consequence rather than the verb. A stock count this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /stock-counts/{countId}/cancel"
   }
  ],
  "states": {
   "loading": "The stock count list.",
   "error": "Could not load. Names which read failed and leaves the stock count untouched.",
   "emptyFirstRun": "No stock count yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stock count are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "operationId": "getCountVariance",
    "contract": "inventory",
    "purpose": "Variance between counted and expected",
    "trigger": "onLoad"
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
    "CountVariance.countId",
    "CountVariance.totalVarianceValue",
    "CountVariance.exceptionCount",
    "CountVariance.lines"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-079",
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
    "BO-001",
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
     "to": "BO-052",
     "trigger": "Goods Receipt",
     "provenance": "flow F76 step 4→5, F92 step 4→5"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "carries": [
      "requisitionId"
     ],
     "provenance": "derived — BO-078 declares entryState.params requisitionId, so an edge into it must carry them"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "carries": [
      "countId"
     ],
     "provenance": "derived — BO-079 declares entryState.params countId, so an edge into it must carry them"
    },
    {
     "to": "BO-081",
     "trigger": "Inventory Items",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-081 declares entryState.params itemId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Improved 20 August against the client design board**, answering 1 board screen(s): Transfers, Distribution & Outlet Receiving. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockTransfers` reads the population and `getStockTransfer` reads one of them — list, select, act",
  "purpose": "Move stock between venues, and receive what arrives.",
  "gaps": [
   {
    "operation": "getStockTransfer",
    "why": "**1 declared operation reach no component on this screen**: getStockTransfer. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every stock transfers",
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
        "StockTransfer.scopePath"
       ],
       "operation": "listStockTransfers",
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
       "label": "Create",
       "operation": "createStockTransfer",
       "provenance": "contract inventory.yaml POST /stock-transfers"
      },
      {
       "kind": "secondaryButton",
       "label": "Receive",
       "operation": "receiveStockTransfer",
       "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/receive"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeTransferShort",
       "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/close-short"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createGoodsReceipt",
       "provenance": "contract inventory.yaml POST /goods-receipts"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseTransferShort",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeTransferShort` changes and what it leaves alone**, in the consequence rather than the verb. A stock transfers this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /stock-transfers/{transferId}/close-short"
   }
  ],
  "states": {
   "loading": "The stock transfers list.",
   "error": "Could not load. Names which read failed and leaves the stock transfers untouched.",
   "emptyFirstRun": "No stock transfers yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stock transfers are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStockTransfers",
    "contract": "inventory",
    "purpose": "List transfers",
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
    "trigger": "onLoad"
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
    "BO-001",
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
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "carries": [
      "countId"
     ],
     "provenance": "derived — BO-079 declares entryState.params countId, so an edge into it must carry them"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "carries": [
      "transferId"
     ],
     "provenance": "derived — BO-080 declares entryState.params transferId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listInventoryItems` reads the population and `getInventoryItem` reads one of them — list, select, act",
  "purpose": "What the venue stocks, and where.",
  "gaps": [
   {
    "operation": "listStockLocations",
    "why": "**1 declared operation reach no component on this screen**: listStockLocations. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every inventory items",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inventory items",
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
       "label": "Create",
       "operation": "createInventoryItem",
       "provenance": "contract inventory.yaml POST /inventory-items"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateInventoryItem",
       "provenance": "contract inventory.yaml PATCH /inventory-items/{itemId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup",
       "operation": "lookupInventoryItem",
       "provenance": "contract inventory.yaml GET /inventory-items/lookup"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
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
   "emptyFirstRun": "No inventory items yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory items are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
    "trigger": "onLoad"
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
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "BO-001",
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
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "carries": [
      "requisitionId"
     ],
     "provenance": "derived — BO-078 declares entryState.params requisitionId, so an edge into it must carry them"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "carries": [
      "transferId"
     ],
     "provenance": "derived — BO-080 declares entryState.params transferId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Moved to wave 1 on 24 August.** F34 walks a retail sale and its return, which is a wave-1 journey — **a venue that can take a return and cannot disposition the item puts damaged stock back on the shelf**, and the count finds it three weeks later.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4g"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockMovements` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Every movement, and why it happened.",
  "gaps": [
   {
    "operation": "listOrders",
    "why": "**1 declared operation reach no component on this screen**: listOrders. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every stock movements",
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
       "provenance": "contract inventory.yaml GET /stock-movements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected stock movements",
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
       "label": "Create",
       "operation": "createStockMovement",
       "provenance": "contract inventory.yaml POST /stock-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
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
   "emptyFirstRun": "No stock movements yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stock movements are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
    "BO-001",
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
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "flow F78 step 1→2"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "carries": [
      "requisitionId"
     ],
     "provenance": "derived — BO-078 declares entryState.params requisitionId, so an edge into it must carry them"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "carries": [
      "countId"
     ],
     "provenance": "derived — BO-079 declares entryState.params countId, so an edge into it must carry them"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "carries": [
      "transferId"
     ],
     "provenance": "derived — BO-080 declares entryState.params transferId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "Retail Board 2.dc.html#ret-2g"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSuppliers` reads the population and `getSupplierPerformance` reads one of them — list, select, act",
  "purpose": "Who we buy from, and what they quoted.",
  "gaps": [
   {
    "operation": "getSupplierPerformance",
    "why": "**1 declared operation reach no component on this screen**: getSupplierPerformance. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every suppliers",
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
       "label": "Create",
       "operation": "createSupplier",
       "provenance": "contract inventory.yaml POST /suppliers"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordQuotation",
       "provenance": "contract inventory.yaml POST /suppliers/{supplierId}/quotations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateSupplier",
       "provenance": "contract inventory.yaml PUT /suppliers/{supplierId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The suppliers list.",
   "error": "Could not load. Names which read failed and leaves the suppliers untouched.",
   "emptyFirstRun": "No suppliers yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the suppliers are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "purpose": "Create a supplier",
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
    "purpose": "Change terms, or stop buying from them",
    "trigger": "onAction",
    "invalidates": [
     "listSuppliers"
    ]
   },
   {
    "operationId": "getSupplierPerformance",
    "contract": "reporting",
    "purpose": "getSupplierPerformance",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "supplierId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `supplierId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-083",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
      "itemId",
      "venueId"
     ],
     "provenance": "derived — BO-049 declares entryState.params itemId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-052",
     "trigger": "Goods Receipt",
     "carries": [
      "purchaseOrderId",
      "receiptId",
      "transferId"
     ],
     "provenance": "derived — BO-052 declares entryState.params purchaseOrderId, receiptId, transferId, so an edge into it must carry them"
    },
    {
     "to": "BO-078",
     "trigger": "Requisitions",
     "carries": [
      "requisitionId"
     ],
     "provenance": "derived — BO-078 declares entryState.params requisitionId, so an edge into it must carry them"
    },
    {
     "to": "BO-079",
     "trigger": "Stock Count",
     "carries": [
      "countId"
     ],
     "provenance": "derived — BO-079 declares entryState.params countId, so an edge into it must carry them"
    },
    {
     "to": "BO-080",
     "trigger": "Stock Transfers",
     "carries": [
      "transferId"
     ],
     "provenance": "derived — BO-080 declares entryState.params transferId, so an edge into it must carry them"
    },
    {
     "to": "BO-081",
     "trigger": "Inventory Items",
     "carries": [
      "itemId"
     ],
     "provenance": "derived — BO-081 declares entryState.params itemId, so an edge into it must carry them"
    },
    {
     "to": "BO-083",
     "trigger": "Suppliers",
     "carries": [
      "supplierId"
     ],
     "provenance": "derived — BO-083 declares entryState.params supplierId, so an edge into it must carry them"
    },
    {
     "to": "BO-137",
     "trigger": "Recipe Consumption & Theoretical Inventory",
     "carries": [
      "countId",
      "runId",
      "venueId"
     ],
     "provenance": "derived — BO-137 declares entryState.params countId, runId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-138",
     "trigger": "Production Execution & Batch Management",
     "carries": [
      "runId",
      "venueId"
     ],
     "provenance": "derived — BO-138 declares entryState.params runId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-139",
     "trigger": "Wastage, Spoilage, Returns & Write-Off",
     "carries": [
      "outletId",
      "venueId"
     ],
     "provenance": "derived — BO-139 declares entryState.params outletId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-140",
     "trigger": "Product Availability, 86 & Operational Food Safety",
     "carries": [
      "itemId",
      "venueId"
     ],
     "provenance": "derived — BO-140 declares entryState.params itemId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-141",
     "trigger": "Operational Alerts, AI Replenishment & Action Center",
     "carries": [
      "alertId",
      "venueId"
     ],
     "provenance": "derived — BO-141 declares entryState.params alertId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Section landing. **9 screens reach the entry point through here** — before 20 August they reached it through nothing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listInventoryItems` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in stock & supply, and what in it needs attention.",
  "gaps": [
   {
    "operation": "listPurchaseOrders",
    "why": "**1 declared operation reach no component on this screen**: listPurchaseOrders. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every stock supply",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected stock supply",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
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
       "label": "Create",
       "operation": "createInventoryItem",
       "provenance": "contract inventory.yaml POST /inventory-items"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "9 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search stock & supply",
       "provenance": "carried from the previous definition"
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
  "responds": null
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
  "permission": "ORDER_CANCEL",
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
  "responds": null
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
  "responds": null
 },
 "closePurchaseOrderShort": {
  "method": "POST",
  "path": "/purchase-orders/{purchaseOrderId}/close-short",
  "contract": "inventory",
  "summary": "Close an order accepting the balance will not arrive",
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
  "responds": null
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
  "responds": null
 },
 "compareQuotations": {
  "method": "GET",
  "path": "/requisitions/{requisitionId}/quotations",
  "contract": "inventory",
  "summary": "Compare quotations for a requisition",
  "permission": "PRODUCT_VIEW",
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
  "permission": "ORDER_CREATE",
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
  "permission": "ORDER_CREATE",
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
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "enterCountLine": {
  "method": "POST",
  "path": "/stock-counts/{countId}/lines",
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
 "getPurchaseOrder": {
  "method": "GET",
  "path": "/purchase-orders/{purchaseOrderId}",
  "contract": "inventory",
  "summary": "Read a purchase order with receipt progress",
  "permission": "PRODUCT_VIEW",
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
  "responds": null
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
  "permission": "PRODUCT_VIEW",
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
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "listGoodsReceipts": {
  "method": "GET",
  "path": "/goods-receipts",
  "contract": "inventory",
  "summary": "List goods receipts",
  "permission": "PRODUCT_VIEW",
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
  "responds": "StockLocation"
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
 "listSuppliers": {
  "method": "GET",
  "path": "/suppliers",
  "contract": "inventory",
  "summary": "List suppliers",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
  "responds": null
 },
 "rejectReceivedGoods": {
  "method": "POST",
  "path": "/goods-receipts/{receiptId}/reject",
  "contract": "inventory",
  "summary": "Reject received goods",
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
  "responds": "GoodsReceipt"
 },
 "rejectRequisition": {
  "method": "POST",
  "path": "/requisitions/{requisitionId}/reject",
  "contract": "inventory",
  "summary": "Reject a requisition",
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
  "responds": null
 },
 "requestRecount": {
  "method": "POST",
  "path": "/stock-counts/{countId}/recount",
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
  "responds": null
 },
 "returnRequisition": {
  "method": "POST",
  "path": "/requisitions/{requisitionId}/return",
  "contract": "inventory",
  "summary": "Return a requisition for more information",
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
  "responds": null
 },
 "sendPurchaseOrder": {
  "method": "POST",
  "path": "/purchase-orders/{purchaseOrderId}/send",
  "contract": "inventory",
  "summary": "Issue the order to the supplier",
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
 "updateSupplier": {
  "method": "PUT",
  "path": "/suppliers/{supplierId}",
  "contract": "inventory",
  "summary": "Change terms, or stop buying from them",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
    "type": "string"
   },
   "totalVarianceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exceptionCount": {
    "type": "integer",
    "description": "Lines beyond tolerance, requiring review before posting."
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
    "type": "string"
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
    "type": "string"
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
      "quantity",
      "unitPrice"
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
       "$ref": "../shared/common.yaml#/components/schemas/Money"
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
    "type": "string"
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
    "description": "Positive increases stock, negative decreases it."
   },
   "unit": {
    "type": "string"
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "description": "Required for adjustments, which are reported separately."
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
    "type": "string"
   },
   "receiptNumber": {
    "type": "string"
   },
   "purchaseOrderId": {
    "type": "string"
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
      "type": "number"
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
   "preparationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "allergens": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "MovementKind": {
  "type": "string",
  "enum": [
   "receipt",
   "issue",
   "saleDepletion",
   "waste",
   "adjustment",
   "transferOut",
   "transferIn",
   "countAdjustment",
   "supplierReturn",
   "production"
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
    "type": "string"
   },
   "purchaseOrderNumber": {
    "type": "string"
   },
   "requisitionId": {
    "type": "string"
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
    "format": "uuid",
    "nullable": true
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
      "lineTotal": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
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
      "description": "The partition key. A quotation is sought by somebody and the scope says who."
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
    "type": "string"
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
    "type": "string"
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
    "description": "Expected quantities withheld from the counting device. Defaults true because a counter who can see the figure reconciles to it rather than to the shelf.\n"
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
    "type": "string"
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
    "type": "string"
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
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). `fromLocationId` and `toLocationId` give the endpoints; **this gives the owner.** A transfer between two venues belongs to the tenant above both, and without it the row is addressable from neither end."
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
    "maxLength": 64
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
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region`, `tenant` scope.**"
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
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
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
      "type": "string"
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
         "type": "string"
        },
        "to": {
         "type": "string"
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
      "type": "string"
     },
     "to": {
      "type": "string"
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
         "type": "string"
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
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
       false,
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": false,
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
   }
  }
 }
}
```
