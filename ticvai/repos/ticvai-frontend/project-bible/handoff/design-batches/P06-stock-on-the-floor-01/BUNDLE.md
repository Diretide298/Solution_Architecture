# P06-stock-on-the-floor-01 — P06 · Stock on the Floor

**10 screens · 29 operations · 38 schemas · 12 permissions**

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
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 12 permissions apply here:
  `INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, LEDGER_POST, ORDER_CREATE, ORDER_MODIFY, PROCUREMENT_RECEIVE, PROCUREMENT_REQUEST, PROCUREMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **15 of these operations work offline**: createGoodsReceipt, createRequisition, enterCountLine, getCountVariance, getHaccpStatus, getStockPositions, getStockTransfer, listRequisitions
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-061` | Retail Inventory Command Center | listDetail | 6 | 0 | — |
| `EMP-062` | Store Stock & SKU Availability | statusTracker | 4 | 2 | — |
| `EMP-063` | Requisition & Smart Store Replenishment | listDetail | 2 | 1 | — |
| `EMP-064` | Store-to-Store & Warehouse Transfers | listDetail | 2 | 1 | — |
| `EMP-065` | Receiving & Store Put-Away | statusTracker | 4 | 3 | — |
| `EMP-066` | Stock Count & Cycle Count Management | statusTracker | 6 | 5 | — |
| `EMP-067` | Damage, Loss, Shrinkage & Stock Adjustment | configEditor | 4 | 3 | — |
| `EMP-068` | Reservation, Allocation & Omnichannel Inventory | statusTracker | 2 | 1 | — |
| `EMP-069` | Barcode, RFID, Serialized Stock & Traceability | listDetail | 2 | 0 | — |
| `EMP-070` | Inventory Exceptions, AI Replenishment & Action Center | listDetail | 3 | 2 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-061",
  "name": "Retail Inventory Command Center",
  "module": "Stock on the Floor",
  "requiresModule": "inventory",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/retail-inventory-command-center",
   "component": "apps/venue-staff-app/src/routes/operations/RetailInventoryCommandCenterDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003",
    "EMP-060"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.**",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4d",
   "FnB Board 4.dc.html#fnb-4e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockMovements` reads the population and `getStockPositions` reads one of them — list, select, act",
  "purpose": "Retail Inventory Command Center — from the client design board, 20 August.",
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
       "notes": "Sends `?kind=` to `listStockMovements`.",
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
       "provenance": "contract inventory.yaml GET /stock-movements"
      },
      {
       "kind": "searchField",
       "label": "Search retail inventory command center",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
    }
   ]
  },
  "states": {
   "loading": "The retail inventory list.",
   "error": "Could not load. Names which read failed and leaves the retail inventory untouched.",
   "emptyFirstRun": "No retail inventory yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on itemId, locationId, kind, recordedFrom, recordedTo and the retail inventory are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "Stock on hand by item and location",
    "trigger": "onLoad"
   },
   {
    "operationId": "listStockMovements",
    "contract": "inventory",
    "purpose": "The movement ledger",
    "trigger": "onLoad"
   },
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Today's takings and revenue KPIs on the phone",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Store manager's mobile dashboard",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "Daily revenue alerts (also pushed, deliverTo push)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "acknowledgeAlert",
    "contract": "reporting",
    "purpose": "Acknowledge an alert",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
     "from": "navigation"
    },
    {
     "name": "dashboardId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-061",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-062",
  "name": "Store Stock & SKU Availability",
  "module": "Stock on the Floor",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/store-stock-sku-availability",
   "component": "apps/venue-staff-app/src/routes/operations/StoreStockSkuAvailabilityDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-067"
   ],
   "transitions": [
    {
     "to": "EMP-067",
     "trigger": "They read the unit and record the temperature",
     "provenance": "flow F28 step 1→2",
     "operation": "getHaccpStatus"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.** **Links to EMP-067 for the reading itself** — F28 step 1 to step 2, and a due-checks list that cannot reach the recording screen is a list nobody acts on.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5j"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getStockPositions` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Store Stock & SKU Availability — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "getHaccpStatus",
    "why": "**`getHaccpStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract fnb.yaml GET /food-safety/status"
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
       "label": "Haccp status",
       "operation": "getHaccpStatus",
       "notes": "Shows `checksDue`, `checksMissed`, `openActions`, `unsignedActions`, `oldestOpenActionAgeHours`, `lastInspectionAt` from `getHaccpStatus`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract fnb.yaml GET /food-safety/status"
      },
      {
       "kind": "searchField",
       "label": "Search store stock",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
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
       "label": "Log temperature",
       "operation": "logTemperature",
       "provenance": "contract fnb.yaml POST /food-safety/temperature-logs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The store stock sku, read by `getStockPositions`.",
   "error": "Could not load. Names which read failed and leaves the store stock sku untouched.",
   "emptyFirstRun": "No store stock sku yet. Offers Log temperature (`logTemperature`).",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "Stock on hand by item and location",
    "trigger": "onLoad"
   },
   {
    "operationId": "setItemAvailability",
    "contract": "fnb",
    "purpose": "Mark an item available or eighty-sixed",
    "trigger": "onAction"
   },
   {
    "operationId": "getHaccpStatus",
    "contract": "fnb",
    "purpose": "getHaccpStatus",
    "trigger": "onLoad"
   },
   {
    "operationId": "logTemperature",
    "contract": "fnb",
    "purpose": "logTemperature",
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
     "name": "itemId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-062",
   "derivedFrom": "wireframes/reference/FnB Board 5.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetItemAvailability",
    "component": "modal",
    "trigger": "Save item availability",
    "body": "**Collects what `setItemAvailability` sends before it is called.** Required: `isAvailable`, `recordedAt`. Optional: `reason`, `restoreAt`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
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
      "restoreAt",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
   },
   {
    "id": "formLogTemperature",
    "component": "modal",
    "trigger": "Log temperature",
    "body": "**Collects what `logTemperature` sends before it is called.** Required: `id`, `checkPointId`, `recordedAt`, `valueCelsius`, `outcome`. Optional: `checkPointKind`, `recordedByPrincipalId`, `minCelsius`, `maxCelsius`, `deviceReported`, `correctiveActionId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "TemperatureLog",
    "confirm": {
     "label": "Log temperature",
     "operation": "logTemperature"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "checkPointId",
      "recordedAt",
      "valueCelsius",
      "outcome",
      "checkPointKind",
      "recordedByPrincipalId",
      "minCelsius",
      "maxCelsius",
      "deviceReported",
      "correctiveActionId"
     ]
    },
    "provenance": "contract fnb.yaml POST /food-safety/temperature-logs"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-063",
  "name": "Requisition & Smart Store Replenishment",
  "module": "Stock on the Floor",
  "requiresModule": "inventory",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/requisition-smart-store-replenishment",
   "component": "apps/venue-staff-app/src/routes/operations/RequisitionSmartStoreReplenishmentDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4f"
  ],
  "pattern": "listDetail",
  "patternReason": "`listRequisitions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Requisition & Smart Store Replenishment — from the client design board, 20 August.",
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
       "label": "Every requisition",
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
       "kind": "searchField",
       "label": "Search requisition",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
       "label": "The selected requisition",
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
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create requisition",
       "operation": "createRequisition",
       "provenance": "contract inventory.yaml POST /requisitions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The requisition smart store list.",
   "error": "Could not load. Names which read failed and leaves the requisition smart store untouched.",
   "emptyFirstRun": "No requisition smart store yet. Offers Create requisition (`createRequisition`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, raisedByPrincipalId and the requisition smart store are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listRequisitions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
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
    "operationId": "listRequisitions",
    "contract": "inventory",
    "purpose": "List requisitions",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "Requisition.id",
    "Requisition.requisitionNumber",
    "Requisition.venueId",
    "Requisition.departmentId",
    "Requisition.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-063",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-064",
  "name": "Store-to-Store & Warehouse Transfers",
  "module": "Stock on the Floor",
  "requiresModule": "inventory",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/store-to-store-warehouse-transfers",
   "component": "apps/venue-staff-app/src/routes/operations/StoreToStoreWarehouseTransfersDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4g"
  ],
  "pattern": "listDetail",
  "patternReason": "`listStockLocations` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Store-to-Store & Warehouse Transfers — from the client design board, 20 August.",
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
      },
      {
       "kind": "searchField",
       "label": "Search store-to-store",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The store-to-store warehouse transfers list.",
   "error": "Could not load. Names which read failed and leaves the store-to-store warehouse transfers untouched.",
   "emptyFirstRun": "No store-to-store warehouse transfers yet. Offers Create stock transfer (`createStockTransfer`).",
   "emptyNoResults": "Never shown: `listStockLocations` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listStockLocations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
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
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-064",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-065",
  "name": "Receiving & Store Put-Away",
  "module": "Stock on the Floor",
  "requiresModule": "inventory",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/receiving-store-put-away",
   "component": "apps/venue-staff-app/src/routes/operations/ReceivingStorePutAwayDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-052",
     "trigger": "The rest is received and the transfer closes short",
     "provenance": "flow F35 step 3→4",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "purchaseOrderId",
      "receiptId",
      "transferId"
     ]
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.**",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5g"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getStockTransfer` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Receiving & Store Put-Away — from the client design board, 20 August.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create goods receipt",
       "operation": "createGoodsReceipt",
       "provenance": "contract inventory.yaml POST /goods-receipts"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject received goods",
       "operation": "rejectReceivedGoods",
       "provenance": "contract inventory.yaml POST /goods-receipts/{receiptId}/reject",
       "notes": "Rejects by receipt line (`lineId`, the batch and expiry received), not by item (audit R171); when the reason is Other a note is required, and the operation refuses 400 without it (decided 28 September, audit R222)."
      },
      {
       "kind": "secondaryButton",
       "label": "Log cold chain",
       "operation": "logColdChain",
       "provenance": "contract fnb.yaml POST /food-safety/cold-chain"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search receiving",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
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
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectReceivedGoods",
    "component": "confirmDialog",
    "trigger": "Reject received goods",
    "body": "**Names what `rejectReceivedGoods` changes and what it leaves alone**, in the consequence rather than the verb. A receiving store put-away this affects should be identified in the dialog, not just counted. **Collects what `rejectReceivedGoods` sends before it is called.** Required: `lines`, `reason`. Optional: `note`.",
    "provenance": "contract inventory.yaml POST /goods-receipts/{receiptId}/reject"
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
    "id": "formLogColdChain",
    "component": "modal",
    "trigger": "Log cold chain",
    "body": "**Collects what `logColdChain` sends before it is called.** Required: `id`, `recordedAt`, `valueCelsius`, `decision`. Optional: `goodsReceiptId`, `transferId`, `thresholdCelsius`, `correctiveActionId`, `supplierClaimRaised`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ColdChainEvent",
    "confirm": {
     "label": "Log cold chain",
     "operation": "logColdChain"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "recordedAt",
      "valueCelsius",
      "decision",
      "goodsReceiptId",
      "transferId",
      "thresholdCelsius",
      "correctiveActionId",
      "supplierClaimRaised"
     ]
    },
    "provenance": "contract fnb.yaml POST /food-safety/cold-chain"
   }
  ],
  "states": {
   "loading": "The receiving store put-away, read by `getStockTransfer`.",
   "error": "Could not load. Names which read failed and leaves the receiving store put-away untouched.",
   "emptyFirstRun": "No receiving store put-away yet. Offers Create goods receipt (`createGoodsReceipt`).",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getStockTransfer` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "createGoodsReceipt",
    "contract": "inventory",
    "purpose": "Receive goods against a purchase order",
    "trigger": "onAction"
   },
   {
    "operationId": "rejectReceivedGoods",
    "contract": "inventory",
    "purpose": "Reject received goods",
    "trigger": "onAction"
   },
   {
    "operationId": "logColdChain",
    "contract": "fnb",
    "purpose": "logColdChain",
    "trigger": "onAction"
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
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "receiptId",
     "from": "EMP-003"
    },
    {
     "name": "transferId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. A transfer opened from the list, or scanned from the delivery note. **The receiver opens the manifest before touching the delivery** — a store that accepts first and reads after has already accepted the shortfall."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-065",
   "derivedFrom": "wireframes/reference/FnB Board 5.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-066",
  "name": "Stock Count & Cycle Count Management",
  "module": "Stock on the Floor",
  "requiresModule": "inventory",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/stock-count-cycle-count-management",
   "component": "apps/venue-staff-app/src/routes/operations/StockCountCycleCountManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-079",
     "trigger": "The supervisor reviews the variance",
     "provenance": "flow F30 step 3→4, F30 step 6→7",
     "operation": "enterCountLine",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "countId"
     ]
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Drawn 31 August** — `Retail Board 4.dc.html` frame `ret-4f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Stock Count &amp; Cycle Count Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4f"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getCountVariance` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Stock Count & Cycle Count Management — from the client design board, 20 August.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
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
       "provenance": "contract inventory.yaml GET /stock-counts/{countId}/variance",
       "notes": "**Shown only after the count is submitted.** While the count is `open` or `counting` the screen shows no expected quantity and no variance, and `getCountVariance` answers 409 whatever the caller's permission (decided 28 September, audit R110 (a))."
      },
      {
       "kind": "searchField",
       "label": "Search stock count",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking. **The lines arrive pre-filled from on-hand stock** — one card per item at the location, with a blank count and no expected figure; the counter enters what is on the shelf (audit R110 (a), R171 (7)).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
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
       "label": "Enter count line",
       "operation": "enterCountLine",
       "provenance": "contract fnb.yaml POST /fnb-stock-counts/{countId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Request recount",
       "operation": "requestRecount",
       "provenance": "contract fnb.yaml POST /fnb-stock-counts/{countId}/recount"
      },
      {
       "kind": "secondaryButton",
       "label": "Save daily count",
       "operation": "setDailyCount",
       "provenance": "contract inventory.yaml PUT /stock-counts/daily"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stock count cycle, read by `getCountVariance`.",
   "error": "Could not load. Names which read failed and leaves the stock count cycle untouched.",
   "emptyFirstRun": "No stock count cycle yet. Offers Request recount (`requestRecount`).",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getCountVariance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "startStockCount",
    "contract": "inventory",
    "purpose": "Start a stock count",
    "trigger": "onAction"
   },
   {
    "operationId": "postStockCount",
    "contract": "inventory",
    "purpose": "Post a count and adjust stock",
    "trigger": "onAction"
   },
   {
    "operationId": "getCountVariance",
    "contract": "inventory",
    "purpose": "Variance between counted and expected, after submission only (409 while open or counting, audit R110 (a))",
    "trigger": "onLoad"
   },
   {
    "operationId": "enterCountLine",
    "contract": "fnb",
    "purpose": "What was actually on the shelf",
    "trigger": "onAction"
   },
   {
    "operationId": "requestRecount",
    "contract": "fnb",
    "purpose": "Send a line back to be counted again",
    "trigger": "onAction"
   },
   {
    "operationId": "setDailyCount",
    "contract": "inventory",
    "purpose": "Which items get counted every day",
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
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-066",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formStartStockCount",
    "component": "modal",
    "trigger": "Start stock count",
    "body": "**Collects what `startStockCount` sends before it is called.** Required: `id`, `locationId`, `kind`. Optional: `categoryIds`, `isBlind` (defaults true). Starting pre-fills one line per item with stock at the location, expected snapshotted and hidden until submission (audit R110 (a)). Dismissing sends nothing; the screen behind is unchanged.",
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
    "id": "formEnterCountLine",
    "component": "modal",
    "trigger": "Enter count line",
    "body": "**Collects what `enterCountLine` sends before it is called.** Required: `recordedAt`, `itemId`, `countedQuantity`. Optional: `locationId`, `uom`, `batchId`, `note`. `enterCountLine` returns no expected quantity or variance, and the screen shows neither until the count is submitted, then reads `getCountVariance` (decided 28 September, audit R110 (a)). Dismissing sends nothing; the screen behind is unchanged.",
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
   },
   {
    "id": "formSetDailyCount",
    "component": "modal",
    "trigger": "Save daily count",
    "body": "**Collects what `setDailyCount` sends before it is called.** Required: `itemIds`. Optional: `locationId`, `dueBy`, `postsAdjustment`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save daily count",
     "operation": "setDailyCount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "itemIds",
      "locationId",
      "dueBy",
      "postsAdjustment"
     ]
    },
    "provenance": "contract inventory.yaml PUT /stock-counts/daily"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-067",
  "name": "Damage, Loss, Shrinkage & Stock Adjustment",
  "module": "Stock on the Floor",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/damage-loss-shrinkage-stock-adjustment",
   "component": "apps/venue-staff-app/src/routes/operations/DamageLossShrinkageStockAdjustmentDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-044",
     "trigger": "The venue manager reviews open and unsigned findings before service",
     "provenance": "flow F28 step 5→6",
     "operation": "signCorrectiveAction",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "actionId",
      "outletId"
     ]
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.**",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5e"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`recordWaste`, `createStockMovement`, `logTemperature`) and no read of a population — it is settings, not a list",
  "purpose": "Damage, Loss, Shrinkage & Stock Adjustment — from the client design board, 20 August.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Create stock movement",
       "operation": "createStockMovement",
       "provenance": "contract inventory.yaml POST /stock-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Log temperature",
       "operation": "logTemperature",
       "provenance": "contract fnb.yaml POST /food-safety/temperature-logs"
      },
      {
       "kind": "secondaryButton",
       "label": "Sign corrective action",
       "operation": "signCorrectiveAction",
       "provenance": "contract fnb.yaml POST /food-safety/corrective-actions/{actionId}/sign"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search damage, loss, shrinkage",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
   "loading": "The saved damage loss shrinkage.",
   "error": "Could not load. Names which read failed and leaves the damage loss shrinkage untouched.",
   "emptyFirstRun": "No damage loss shrinkage configured. The form opens empty and `recordWaste` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_MODIFY`, which `recordWaste` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "recordWaste",
    "contract": "fnb",
    "purpose": "Record waste",
    "trigger": "onAction"
   },
   {
    "operationId": "createStockMovement",
    "contract": "inventory",
    "purpose": "Record an adjustment in or out, or waste; positive quantity, reason required (audit R171)",
    "trigger": "onAction"
   },
   {
    "operationId": "logTemperature",
    "contract": "fnb",
    "purpose": "logTemperature",
    "trigger": "onAction"
   },
   {
    "operationId": "signCorrectiveAction",
    "contract": "fnb",
    "purpose": "signCorrectiveAction",
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
     "from": "EMP-003"
    },
    {
     "name": "actionId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. A corrective action opened from the food-safety list or an alert. **An action opened from an alert is the common path** — the platform raises it, somebody signs it, and the link is how they get there."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-067",
   "derivedFrom": "wireframes/reference/FnB Board 5.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateStockMovement",
    "component": "modal",
    "trigger": "Create stock movement",
    "body": "**Collects what `createStockMovement` sends before it is called.** Required: `id`, `itemId`, `locationId`, `kind`, `quantity`, `recordedAt`. Optional: `unit`, `reason`, `costCenterId`. **The kind picker offers `adjustmentIn`, `adjustmentOut` and `waste`** — the kind decides the direction, so the quantity is always entered positive; `countGain` and `countLoss` are shown on movements a count posted but are not offered here. **A reason is mandatory for an adjustment or waste** (400 without one) (decided 28 September, audit R171). Dismissing sends nothing; the screen behind is unchanged.",
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
    "id": "formLogTemperature",
    "component": "modal",
    "trigger": "Log temperature",
    "body": "**Collects what `logTemperature` sends before it is called.** Required: `id`, `checkPointId`, `recordedAt`, `valueCelsius`, `outcome`. Optional: `checkPointKind`, `recordedByPrincipalId`, `minCelsius`, `maxCelsius`, `deviceReported`, `correctiveActionId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "TemperatureLog",
    "confirm": {
     "label": "Log temperature",
     "operation": "logTemperature"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "checkPointId",
      "recordedAt",
      "valueCelsius",
      "outcome",
      "checkPointKind",
      "recordedByPrincipalId",
      "minCelsius",
      "maxCelsius",
      "deviceReported",
      "correctiveActionId"
     ]
    },
    "provenance": "contract fnb.yaml POST /food-safety/temperature-logs"
   },
   {
    "id": "formSignCorrectiveAction",
    "component": "modal",
    "trigger": "Sign corrective action",
    "body": "**Collects what `signCorrectiveAction` sends before it is called.** Required: `actionTaken`. Optional: `disposal`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sign corrective action",
     "operation": "signCorrectiveAction"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "actionTaken",
      "disposal"
     ]
    },
    "provenance": "contract fnb.yaml POST /food-safety/corrective-actions/{actionId}/sign"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-068",
  "name": "Reservation, Allocation & Omnichannel Inventory",
  "module": "Stock on the Floor",
  "requiresModule": "inventory",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/reservation-allocation-omnichannel-inventory",
   "component": "apps/venue-staff-app/src/routes/operations/ReservationAllocationOmnichannelInDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `Retail Board 4.dc.html` frame `ret-4h`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Reservation, Allocation &amp; Omnichannel Inventory* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4h"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getStockPositions` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Reservation, Allocation & Omnichannel Inventory — from the client design board, 20 August.",
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
       "kind": "searchField",
       "label": "Search reservation, allocation",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Reserve merchandise",
       "operation": "reserveMerchandise",
       "provenance": "contract retail.yaml POST /outlets/{outletId}/reserve"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation allocation omnichannel, read by `getStockPositions`.",
   "error": "Could not load. Names which read failed and leaves the reservation allocation omnichannel untouched.",
   "emptyFirstRun": "No reservation allocation omnichannel yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getStockPositions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "Stock on hand by item and location",
    "trigger": "onLoad"
   },
   {
    "operationId": "reserveMerchandise",
    "contract": "retail",
    "purpose": "Reserve an item for collection",
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
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-068",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formReserveMerchandise",
    "component": "modal",
    "trigger": "Reserve merchandise",
    "body": "**Collects what `reserveMerchandise` sends before it is called.** Required: `id`, `lines`, `expiresAt`. Optional: `subjectId`, `collectionNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reserve merchandise",
     "operation": "reserveMerchandise"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "lines",
      "expiresAt",
      "subjectId",
      "collectionNote"
     ]
    },
    "provenance": "contract retail.yaml POST /outlets/{outletId}/reserve"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-069",
  "name": "Barcode, RFID, Serialized Stock & Traceability",
  "module": "Stock on the Floor",
  "requiresModule": "inventory",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/barcode-rfid-serialized-stock-traceability",
   "component": "apps/venue-staff-app/src/routes/operations/BarcodeRfidSerializedStockTraceabiDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `Retail Board 4.dc.html` frame `ret-4j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Barcode, RFID, Serialized Stock &amp; Traceability* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSerialisedItems` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Barcode, RFID, Serialized Stock & Traceability — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Serial",
       "operation": "listSerialisedItems",
       "notes": "Sends `?serial=` to `listSerialisedItems`.",
       "provenance": "contract inventory.yaml GET /serialised-items"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listSerialisedItems",
       "notes": "Sends `?status=` to `listSerialisedItems`.",
       "provenance": "contract inventory.yaml GET /serialised-items"
      },
      {
       "kind": "dataTable",
       "label": "Every serialised",
       "bindsTo": "SerialisedItem",
       "columns": [
        "SerialisedItem.id",
        "SerialisedItem.itemId",
        "SerialisedItem.batchId",
        "SerialisedItem.serial",
        "SerialisedItem.locationId",
        "SerialisedItem.status",
        "SerialisedItem.soldOnOrderLineId",
        "SerialisedItem.warrantyUntil",
        "SerialisedItem.receivedAt"
       ],
       "operation": "listSerialisedItems",
       "provenance": "contract inventory.yaml GET /serialised-items"
      },
      {
       "kind": "searchField",
       "label": "Search barcode, rfid, serialized stock",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
       "label": "The selected serialised",
       "bindsTo": "SerialisedItem",
       "columns": [
        "SerialisedItem.id",
        "SerialisedItem.itemId",
        "SerialisedItem.batchId",
        "SerialisedItem.serial",
        "SerialisedItem.locationId",
        "SerialisedItem.status",
        "SerialisedItem.soldOnOrderLineId",
        "SerialisedItem.warrantyUntil",
        "SerialisedItem.receivedAt"
       ],
       "operation": "listSerialisedItems",
       "provenance": "contract inventory.yaml GET /serialised-items"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Lookup merchandise",
       "operation": "lookupMerchandise",
       "provenance": "contract retail.yaml GET /merchandise/lookup"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The barcode rfid serialized list.",
   "error": "Could not load. Names which read failed and leaves the barcode rfid serialized untouched.",
   "emptyFirstRun": "No barcode rfid serialized yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on serial, status and the barcode rfid serialized are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listSerialisedItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "listSerialisedItems",
    "contract": "inventory",
    "purpose": "listSerialisedItems",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupMerchandise",
    "contract": "retail",
    "purpose": "Price and stock check by barcode",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "SerialisedItem.id",
    "SerialisedItem.itemId",
    "SerialisedItem.batchId",
    "SerialisedItem.serial",
    "SerialisedItem.locationId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-069",
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-070",
  "name": "Inventory Exceptions, AI Replenishment & Action Center",
  "module": "Stock on the Floor",
  "requiresModule": "analytics",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/inventory-exceptions-ai-replenishment-action-cen",
   "component": "apps/venue-staff-app/src/routes/operations/InventoryExceptionsAiReplenishmentDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `Inventory Board 1.dc.html` frame `inv-10` (*Inventory Exceptions, Data Quality & AI*). **Inventory Board 1 is the only one of the seven that maps onto screens this package has** — item master, categories, UoM, locations, statuses, movement history. Boards 2 to 7 draw a warehouse and procurement suite the contracts do not contain.",
  "density": "comfortable",
  "boardFrames": [
   "Inventory Board 1.dc.html#inv-10"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAlerts` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Inventory Exceptions, AI Replenishment & Action Center — from the client design board, 20 August.",
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
       "label": "Search inventory exceptions, ai replenishment",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
       "provenance": "contract inventory.yaml POST /requisitions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory exceptions replenishment list.",
   "error": "Could not load. Names which read failed and leaves the inventory exceptions replenishment untouched.",
   "emptyFirstRun": "No inventory exceptions replenishment yet. Offers Create requisition (`createRequisition`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, severity, workstationId, shiftId, itemId and the inventory exceptions replenishment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listAlerts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available offline.** `listAlerts` reads the analytical replica (ADR-0016). **Corrected 24 August** — the shared \"works from cache and queues what it records\" wording was applied to a screen whose only operation is an analytical read."
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
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-070",
   "derivedFrom": "wireframes/reference/Inventory Board 1.dc.html",
   "note": "**Drawn by Claude Design on `Inventory Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
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
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
 },
 "getHaccpStatus": {
  "method": "GET",
  "path": "/food-safety/status",
  "contract": "fnb",
  "summary": "Where this venue stands, right now",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
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
   },
   {
    "name": "interval",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiValue"
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
 "listSerialisedItems": {
  "method": "GET",
  "path": "/serialised-items",
  "contract": "inventory",
  "summary": "Where each individual item is",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "serial",
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
 "logColdChain": {
  "method": "POST",
  "path": "/food-safety/cold-chain",
  "contract": "fnb",
  "summary": "The temperature a delivery arrived at, and what was decided",
  "permission": "INCIDENT_REPORT",
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
  "requestBody": "ColdChainEvent",
  "responds": "ColdChainEvent"
 },
 "logTemperature": {
  "method": "POST",
  "path": "/food-safety/temperature-logs",
  "contract": "fnb",
  "summary": "Record a temperature check, in range or not",
  "permission": "INCIDENT_REPORT",
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
  "requestBody": "TemperatureLog",
  "responds": null
 },
 "lookupMerchandise": {
  "method": "GET",
  "path": "/merchandise/lookup",
  "contract": "retail",
  "summary": "Price and stock check by barcode",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
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
   },
   {
    "name": "includeSiblingOutlets",
    "in": "query",
    "required": null
   },
   {
    "name": "outletId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PriceCheck"
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
 "reserveMerchandise": {
  "method": "POST",
  "path": "/outlets/{outletId}/reserve",
  "contract": "retail",
  "summary": "Reserve an item for collection",
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
  "requestBody": null,
  "responds": "MerchandiseReservation"
 },
 "setDailyCount": {
  "method": "PUT",
  "path": "/stock-counts/daily",
  "contract": "inventory",
  "summary": "Which items get counted every day",
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
 "signCorrectiveAction": {
  "method": "POST",
  "path": "/food-safety/corrective-actions/{actionId}/sign",
  "contract": "fnb",
  "summary": "Say what was done, and put a name to it",
  "permission": "INCIDENT_MANAGE",
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
  "responds": "CorrectiveAction"
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
 "ColdChainEvent": {
  "type": "object",
  "x-ticvai-persistence": "fnb.cold_chain_event",
  "description": "Board 5G. **A delivery arriving warm is a rejection decision made at the door**, and the package had `createGoodsReceipt` with nowhere to record the temperature it arrived at.\n**The reading is taken before the receipt is posted**, not after — once stock is received it has entered the kitchen, and a claim against a supplier needs the reading that refused it.\n",
  "required": [
   "id",
   "recordedAt",
   "valueCelsius",
   "decision"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "goodsReceiptId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "transferId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "valueCelsius": {
    "type": "number"
   },
   "thresholdCelsius": {
    "type": "number"
   },
   "decision": {
    "type": "string",
    "enum": [
     "accepted",
     "acceptedWithNote",
     "partiallyRejected",
     "rejected"
    ]
   },
   "correctiveActionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "supplierClaimRaised": {
    "type": "boolean",
    "default": false
   }
  }
 },
 "CorrectiveAction": {
  "type": "object",
  "x-ticvai-persistence": "fnb.corrective_action",
  "description": "What was done about a finding, and who signed it. **Opened automatically by an out-of-range reading or a cold-chain breach**, because an action that depends on somebody remembering to raise it is an action that is not raised.\n**Signed by a named principal, and the signature is the record.** *Discarded and reset* with nobody against it is not a corrective action.\n",
  "required": [
   "id",
   "raisedAt",
   "source",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**Who raised it, which is who may not sign it when it is critical** (`signCorrectiveAction`). Null where the action was opened automatically by a reading or a cold-chain breach."
   },
   "source": {
    "type": "string",
    "enum": [
     "temperatureExcursion",
     "coldChainBreach",
     "expiredStock",
     "contamination",
     "pestSighting",
     "equipmentFailure",
     "missedCheck",
     "manual"
    ],
    "description": "`missedCheck` is raised by the server when a checkpoint goes past its `checkFrequencyMinutes` with no reading (audit R125 (5))."
   },
   "sourceRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "severity": {
    "type": "string",
    "enum": [
     "observation",
     "minor",
     "major",
     "critical"
    ],
    "description": "**Set by the source when the platform opens it** (decided 28 September, audit R125 (5)): an out-of-range reading or a cold-chain breach opens at `major`, a missed check at `minor`. `critical` is a person's escalation, not a default."
   },
   "actionTaken": {
    "type": "string",
    "nullable": true
   },
   "disposal": {
    "type": "string",
    "enum": [
     "none",
     "discarded",
     "reworked",
     "quarantined",
     "returned"
    ],
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "actioned",
     "signed",
     "escalated",
     "closed"
    ]
   },
   "signedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "signedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "escalatedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A critical finding a shift cannot close.** Escalation exists so a supervisor signs what a cook should not. Always the venue's food-safety lead at the time of escalation (`fnb.foodSafetyLeadPrincipalId`, audit R096 (9)).\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
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
    "format": "uuid"
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
    "format": "uuid"
   },
   "purchaseOrderId": {
    "type": "string",
    "format": "uuid"
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
    "format": "uuid"
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
    "format": "uuid"
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
    "format": "uuid"
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
 "Dashboard": {
  "x-ticvai-persistence": "reporting.dashboard + reporting.dashboard_tile",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateDashboardRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "aggregateCost",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "aggregateCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Combined refresh load of every tile."
     },
     "archivedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
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
    "format": "uuid"
   },
   "receiptNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152), e.g. `MAR-GR-000431`. Not gapless; only tax invoices are gapless, per legal entity. A receipt recorded offline takes the next number from the range its device holds in reserve.\n"
   },
   "purchaseOrderId": {
    "type": "string",
    "format": "uuid"
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
       "format": "uuid",
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
   "bucketStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."
   },
   "groupKey": {
    "type": "string",
    "nullable": true,
    "description": "The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."
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
 "MerchandiseReservation": {
  "x-ticvai-persistence": "retail.reservation + retail.reservation_line",
  "type": "object",
  "required": [
   "id",
   "outletId",
   "lines",
   "status",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "reservationNumber": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "merchandiseId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      }
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "reserved",
     "collected",
     "expired",
     "cancelled"
    ]
   },
   "collectionNote": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "collectedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
   "attributedRevenue",
   "loyaltyActiveMembers",
   "loyaltyTierDistribution",
   "loyaltyPointsLiability",
   "loyaltyBreakageRate",
   "loyaltyMemberRetention",
   "challengeParticipationRate",
   "gamificationLoyaltyImpact",
   "gamificationMembershipImpact",
   "gamificationRetention",
   "accreditationApplications",
   "accreditationTimeToDecision",
   "accreditationCredentialsIssued",
   "accreditationActiveHolders",
   "accreditationRenewalsDue",
   "staffingShortfall"
  ],
  "x-ticvai-money-valued": [
   "inventoryValuation",
   "resaleCommission",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "attributedRevenue",
   "loyaltyPointsLiability"
  ],
  "x-ticvai-extended-29-september": "**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n",
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
 "PriceCheck": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "merchandiseId",
   "name",
   "listPrice",
   "effectivePrice",
   "onHand"
  ],
  "properties": {
   "merchandiseId": {
    "type": "string",
    "format": "uuid"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "description": "The outlet whose price and stock this is: the asking workstation's outlet, or `outletId` for a caller with none (decided 28 September, audit R215).\n"
   },
   "sku": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "listPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "effectivePrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "After any live promotion."
   },
   "appliedPromotionCode": {
    "type": "string",
    "nullable": true
   },
   "onHand": {
    "type": "number"
   },
   "isAvailable": {
    "type": "boolean"
   },
   "siblingOutlets": {
    "type": "array",
    "description": "Stock elsewhere in the venue, so a colleague can be sent.",
    "items": {
     "type": "object",
     "properties": {
      "outletId": {
       "type": "string",
       "format": "uuid"
      },
      "outletName": {
       "type": "string"
      },
      "onHand": {
       "type": "number"
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
    "format": "uuid"
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
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
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
    "format": "uuid"
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
 "SerialisedItem": {
  "type": "object",
  "x-ticvai-persistence": "inventory.serialised_item",
  "description": "Retail Board 4 of the client's design set, 20 August. **`StockBatch` was added on 18 August with a lot number, and serialisation to the individual item is a step beyond it.**\nA lot answers *which delivery did this come from*. A serial answers *where is this exact one* — which is what a jewellery counter, a phone, a ticketed collectible or anything with a warranty needs.\n**Most stock is not serialised and should not be.** Turning it on for a 2 AED keyring creates a row per keyring, so it is a per-item decision rather than a policy.\n",
  "required": [
   "id",
   "itemId",
   "serial",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "itemId": {
    "type": "string",
    "format": "uuid"
   },
   "batchId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The batch it arrived in, where the item is both lotted and serialised."
   },
   "serial": {
    "type": "string",
    "description": "**Unique within the item, not globally.** Two manufacturers reuse serial numbers and a global constraint would refuse the second one.\n"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "inStock",
     "reserved",
     "sold",
     "returned",
     "damaged",
     "lost",
     "inTransit",
     "warranty"
    ]
   },
   "soldOnOrderLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The link that makes serialisation worth having.** A warranty claim, a recall and a proof of purchase all start with *which sale was this exact item*.\n"
   },
   "warrantyUntil": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "receivedAt": {
    "type": "string",
    "format": "date-time"
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
    "format": "uuid"
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
    "format": "uuid"
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
    "format": "uuid"
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
 "TemperatureLog": {
  "type": "object",
  "x-ticvai-persistence": "fnb.temperature_log",
  "description": "Board 5J of the client F&B pack, 20 August. **HACCP records are a UAE regulatory obligation, they are inspected, and nothing in 947 operations touched them** — a venue that cannot produce a temperature log has a compliance failure rather than a missing screen.\n**A reading out of range is not an error, it is a finding.** The log records it, opens a corrective action, and keeps the reading — **deleting a bad reading is the one thing an inspector looks for.**\n**Offline-capable and it must be.** A walk-in freezer is where the signal is worst and the readings matter most.\n",
  "required": [
   "id",
   "checkPointId",
   "recordedAt",
   "valueCelsius",
   "outcome"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "checkPointId": {
    "type": "string",
    "format": "uuid",
    "description": "The unit, station or delivery being read."
   },
   "checkPointKind": {
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
    ]
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "valueCelsius": {
    "type": "number"
   },
   "minCelsius": {
    "type": "number",
    "nullable": true
   },
   "maxCelsius": {
    "type": "number",
    "nullable": true
   },
   "outcome": {
    "type": "string",
    "enum": [
     "inRange",
     "outOfRange",
     "notTaken"
    ],
    "description": "**`notTaken` is a record, not an absence.** A check that did not happen is itself a finding, and a log with a gap cannot be told apart from a log nobody kept.\n"
   },
   "deviceReported": {
    "type": "boolean",
    "default": false,
    "description": "**A probe reading and a person's reading are different evidence.** An inspector treats them differently and so should the record.\n"
   },
   "correctiveActionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
