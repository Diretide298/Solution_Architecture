# P08-stock-supply-02 — P08 · Stock & Supply (2 of 2)

**5 screens · 12 operations · 9 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **8 of these operations work offline**: completeProductionRun, createRequisition, getCountVariance, getProductionRun, listExpiringBatches, listProductionRuns, recordWaste, setItemAvailability
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-137` | Recipe Consumption & Theoretical Inventory | listDetail | 4 | 0 | — |
| `BO-138` | Production Execution & Batch Management | listDetail | 3 | 0 | — |
| `BO-139` | Wastage, Spoilage, Returns & Write-Off | configEditor | 1 | 0 | — |
| `BO-140` | Product Availability, 86 & Operational Food Safety | listDetail | 2 | 0 | — |
| `BO-141` | Operational Alerts, AI Replenishment & Action Center | listDetail | 3 | 0 | — |

## Thin screens in this batch

**BO-137, BO-139 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-105 declares entryState.params venueId, so an edge into it must carry them"
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
  "gaps": [
   {
    "operation": "listProductionRuns",
    "why": "**2 declared operations reach no component on this screen**: listProductionRuns, getProductionRun. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every recipe consumption theoretical",
       "bindsTo": "Recipe",
       "columns": [
        "Recipe.menuItemId",
        "Recipe.yield",
        "Recipe.ingredients",
        "Recipe.costPerPortion"
       ],
       "operation": "listRecipes",
       "provenance": "contract fnb.yaml GET /recipes"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recipe consumption theoretical",
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
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search recipe consumption",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recipe consumption theoretical list.",
   "error": "Could not load. Names which read failed and leaves the recipe consumption theoretical untouched.",
   "emptyFirstRun": "No recipe consumption theoretical yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recipe consumption theoretical are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "CountVariance.countId",
    "CountVariance.totalVarianceValue",
    "CountVariance.exceptionCount",
    "CountVariance.lines"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-137",
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-105 declares entryState.params venueId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every production execution batch",
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
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected production execution batch",
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
       "label": "Plan",
       "operation": "planProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs/{runId}/complete"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search production execution",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The production execution batch list.",
   "error": "Could not load. Names which read failed and leaves the production execution batch untouched.",
   "emptyFirstRun": "No production execution batch yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the production execution batch are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-105 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`recordWaste`) and no read of a population — it is settings, not a list",
  "purpose": "Wastage, Spoilage, Returns & Write-Off — from the client design board, 20 August.",
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved wastage spoilage returns.",
   "error": "Could not load. Names which read failed and leaves the wastage spoilage returns untouched.",
   "emptyFirstRun": "No wastage spoilage returns configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-105 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.",
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
       "kind": "dataTable",
       "label": "Every product availability operational",
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
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product availability operational",
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
       "label": "Save changes",
       "operation": "setItemAvailability",
       "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search product availability, 86",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product availability operational list.",
   "error": "Could not load. Names which read failed and leaves the product availability operational untouched.",
   "emptyFirstRun": "No product availability operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product availability operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-105 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.",
  "density": "compact",
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
       "kind": "dataTable",
       "label": "Every operational alerts replenishment",
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
       "label": "The selected operational alerts replenishment",
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
       "label": "Search operational alerts, ai replenishment",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational alerts replenishment list.",
   "error": "Could not load. Names which read failed and leaves the operational alerts replenishment untouched.",
   "emptyFirstRun": "No operational alerts replenishment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational alerts replenishment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
  "responds": "StockBatch"
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
  "responds": "ProductionRun"
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
 "StockBatch": {
  "type": "object",
  "x-ticvai-persistence": "inventory.stock_batch",
  "description": "BL-122. **`isPerishable` and `shelfLifeDays` are on the item, so a shelf life is declared and never instantiated.** Two deliveries of the same milk arriving a week apart are one stock level with one implied expiry, and the older one is invisible.\n**A batch is the instance that actually expires.** Without it, first-expiry-first-out is not computable and a venue discovers the problem by smell.\n",
  "required": [
   "id",
   "itemId",
   "locationId",
   "quantity",
   "receivedAt"
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
   "batchCode": {
    "type": "string",
    "nullable": true
   },
   "lotNumber": {
    "type": "string",
    "nullable": true,
    "description": "The supplier's own reference. **A recall names a lot number**, and an inventory that cannot resolve one has to discard everything.\n"
   },
   "quantity": {
    "type": "number"
   },
   "receivedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "supplierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "quarantined",
     "expired",
     "recalled",
     "consumed",
     "written-off"
    ]
   }
  }
 }
}
```
