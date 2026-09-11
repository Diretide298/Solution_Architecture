# P06-stock-on-the-floor-01 — P06 · Stock on the Floor

**10 screens · 27 operations · 26 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, LEDGER_POST, ORDER_CREATE, ORDER_MODIFY, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `EMP-061` | Retail Inventory Command Center | listDetail | 2 | 0 | — |
| `EMP-062` | Store Stock & SKU Availability | statusTracker | 4 | 0 | — |
| `EMP-063` | Requisition & Smart Store Replenishment | listDetail | 2 | 0 | — |
| `EMP-064` | Store-to-Store & Warehouse Transfers | listDetail | 2 | 0 | — |
| `EMP-065` | Receiving & Store Put-Away | statusTracker | 4 | 1 | — |
| `EMP-066` | Stock Count & Cycle Count Management | statusTracker | 6 | 0 | — |
| `EMP-067` | Damage, Loss, Shrinkage & Stock Adjustment | configEditor | 4 | 0 | — |
| `EMP-068` | Reservation, Allocation & Omnichannel Inventory | statusTracker | 2 | 0 | — |
| `EMP-069` | Barcode, RFID, Serialized Stock & Traceability | listDetail | 2 | 0 | — |
| `EMP-070` | Inventory Exceptions, AI Replenishment & Action Center | listDetail | 3 | 0 | — |

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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every retail inventory",
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
       "label": "The selected retail inventory",
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
    }
   ]
  },
  "states": {
   "loading": "The retail inventory list.",
   "error": "Could not load. Names which read failed and leaves the retail inventory untouched.",
   "emptyFirstRun": "No retail inventory yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the retail inventory are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-061",
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
    "why": "**1 declared operation reach no component on this screen**: getHaccpStatus. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "The selected store stock sku",
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
       "label": "Log",
       "operation": "logTemperature",
       "provenance": "contract fnb.yaml POST /food-safety/temperature-logs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
    }
   ]
  },
  "states": {
   "loading": "The store stock sku list.",
   "error": "Could not load. Names which read failed and leaves the store stock sku untouched.",
   "emptyFirstRun": "No store stock sku yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the store stock sku are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every requisition smart store",
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
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected requisition smart store",
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
       "label": "Create",
       "operation": "createRequisition",
       "provenance": "contract inventory.yaml POST /requisitions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
    }
   ]
  },
  "states": {
   "loading": "The requisition smart store list.",
   "error": "Could not load. Names which read failed and leaves the requisition smart store untouched.",
   "emptyFirstRun": "No requisition smart store yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the requisition smart store are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
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
       "label": "Every store-to-store warehouse transfers",
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
       "label": "The selected store-to-store warehouse transfers",
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
       "label": "Create",
       "operation": "createStockTransfer",
       "provenance": "contract inventory.yaml POST /stock-transfers"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
    }
   ]
  },
  "states": {
   "loading": "The store-to-store warehouse transfers list.",
   "error": "Could not load. Names which read failed and leaves the store-to-store warehouse transfers untouched.",
   "emptyFirstRun": "No store-to-store warehouse transfers yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the store-to-store warehouse transfers are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-052",
     "trigger": "The rest is received and the transfer closes short",
     "provenance": "flow F35 step 3→4",
     "crossesDevice": true,
     "back": false
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
  "gaps": [
   {
    "operation": "getStockTransfer",
    "why": "**1 declared operation reach no component on this screen**: getStockTransfer. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
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
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectReceivedGoods",
       "provenance": "contract inventory.yaml POST /goods-receipts/{receiptId}/reject"
      },
      {
       "kind": "secondaryButton",
       "label": "Log",
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
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectReceivedGoods",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Names what `rejectReceivedGoods` changes and what it leaves alone**, in the consequence rather than the verb. A receiving store put-away this affects should be identified in the dialog, not just counted.",
    "provenance": "contract inventory.yaml POST /goods-receipts/{receiptId}/reject"
   }
  ],
  "states": {
   "loading": "The receiving store put-away list.",
   "error": "Could not load. Names which read failed and leaves the receiving store put-away untouched.",
   "emptyFirstRun": "No receiving store put-away yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the receiving store put-away are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-079",
     "trigger": "The supervisor reviews the variance",
     "provenance": "flow F30 step 3→4, F30 step 6→7",
     "operation": "enterCountLine",
     "crossesDevice": true,
     "back": false
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
       "label": "The selected stock count cycle",
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
       "label": "Enter",
       "operation": "enterCountLine",
       "provenance": "contract fnb.yaml POST /stock-counts/{countId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Request",
       "operation": "requestRecount",
       "provenance": "contract fnb.yaml POST /stock-counts/{countId}/recount"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setDailyCount",
       "provenance": "contract inventory.yaml PUT /stock-counts/daily"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search stock count",
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
    }
   ]
  },
  "states": {
   "loading": "The stock count cycle list.",
   "error": "Could not load. Names which read failed and leaves the stock count cycle untouched.",
   "emptyFirstRun": "No stock count cycle yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stock count cycle are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "purpose": "Variance between counted and expected",
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
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-044",
     "trigger": "The venue manager reviews open and unsigned findings before service",
     "provenance": "flow F28 step 5→6",
     "operation": "signCorrectiveAction",
     "crossesDevice": true,
     "back": false
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
  "gaps": [
   {
    "operation": "recordWaste",
    "why": "**`recordWaste` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract fnb.yaml POST /outlets/{outletId}/waste"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Record",
       "operation": "recordWaste",
       "provenance": "contract fnb.yaml POST /outlets/{outletId}/waste"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createStockMovement",
       "provenance": "contract inventory.yaml POST /stock-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Log",
       "operation": "logTemperature",
       "provenance": "contract fnb.yaml POST /food-safety/temperature-logs"
      },
      {
       "kind": "secondaryButton",
       "label": "Sign",
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved damage loss shrinkage.",
   "error": "Could not load. Names which read failed and leaves the damage loss shrinkage untouched.",
   "emptyFirstRun": "No damage loss shrinkage configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "purpose": "Record an issue, return or adjustment",
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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
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
       "label": "The selected reservation allocation omnichannel",
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
       "label": "Reserve",
       "operation": "reserveMerchandise",
       "provenance": "contract retail.yaml POST /outlets/{outletId}/reserve"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
    }
   ]
  },
  "states": {
   "loading": "The reservation allocation omnichannel list.",
   "error": "Could not load. Names which read failed and leaves the reservation allocation omnichannel untouched.",
   "emptyFirstRun": "No reservation allocation omnichannel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservation allocation omnichannel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every barcode rfid serialized",
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
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected barcode rfid serialized",
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
       "label": "Lookup",
       "operation": "lookupMerchandise",
       "provenance": "contract retail.yaml GET /merchandise/lookup"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
    }
   ]
  },
  "states": {
   "loading": "The barcode rfid serialized list.",
   "error": "Could not load. Names which read failed and leaves the barcode rfid serialized untouched.",
   "emptyFirstRun": "No barcode rfid serialized yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the barcode rfid serialized are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every inventory exceptions replenishment",
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
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inventory exceptions replenishment",
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
       "label": "Acknowledge",
       "operation": "acknowledgeAlert",
       "provenance": "contract reporting.yaml POST /alerts/{alertId}/acknowledge"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createRequisition",
       "provenance": "contract inventory.yaml POST /requisitions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
    }
   ]
  },
  "states": {
   "loading": "The inventory exceptions replenishment list.",
   "error": "Could not load. Names which read failed and leaves the inventory exceptions replenishment untouched.",
   "emptyFirstRun": "No inventory exceptions replenishment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory exceptions replenishment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "note": "**Drawn by Claude Design on `Inventory Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "responds": "SerialisedItem"
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
 "logColdChain": {
  "method": "POST",
  "path": "/food-safety/cold-chain",
  "contract": "fnb",
  "summary": "The temperature a delivery arrived at, and what was decided",
  "permission": "INCIDENT_REPORT",
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
  "conflictPolicy": "lastWriterWins",
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
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "severity": {
    "type": "string",
    "enum": [
     "info",
     "warning",
     "critical"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "raised",
     "acknowledged",
     "resolved",
     "expired"
    ]
   },
   "observedValue": {
    "type": "number"
   },
   "threshold": {
    "type": "number"
   },
   "scopePath": {
    "type": "string"
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
   "source": {
    "type": "string",
    "enum": [
     "temperatureExcursion",
     "coldChainBreach",
     "expiredStock",
     "contamination",
     "pestSighting",
     "equipmentFailure",
     "manual"
    ]
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
    ]
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
    "description": "**A critical finding a shift cannot close.** Escalation exists so a supervisor signs what a cook should not.\n"
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
