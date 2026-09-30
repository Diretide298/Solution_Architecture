# WS89 — Rental Management board 2

**10 screens · 16 operations · 26 schemas · 5 permissions**

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
  `ASSET_MANAGE, ASSET_VIEW, PROCUREMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-504` | Rental Inventory Command Center | commandCentre | 2 | 0 | — |
| `BO-505` | Serialized Equipment Registry | configEditor | 2 | 0 | — |
| `BO-506` | Equipment / Asset Profile | listDetail | 2 | 0 | — |
| `BO-507` | Pooled Inventory Management | listDetail | 3 | 0 | — |
| `BO-508` | Equipment Status & Condition Management | listDetail | 2 | 0 | — |
| `BO-509` | QR / Barcode Equipment Identification | listDetail | 1 | 0 | — |
| `BO-510` | Inventory Location Allocation | listDetail | 2 | 0 | — |
| `BO-511` | Inventory Transfer Management | listDetail | 3 | 0 | — |
| `BO-512` | Inventory Adjustment & Exception Management | listDetail | 2 | 0 | — |
| `BO-513` | Inventory Intelligence & Rebalancing | listDetail | 3 | 0 | — |

## Thin screens in this batch

**BO-506, BO-508, BO-509, BO-510, BO-512, BO-513 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-504",
  "name": "Rental Inventory Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "1",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-inventory-command-center-bo-504",
   "component": "apps/venue-management-web/src/routes/rentals/RentalInventoryCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-505",
    "BO-506",
    "BO-507",
    "BO-508",
    "BO-509",
    "BO-510",
    "BO-511",
    "BO-512",
    "BO-513"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-505",
     "trigger": "Serialized Equipment Registry",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-506",
     "trigger": "Equipment / Asset Profile",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-507",
     "trigger": "Pooled Inventory Management",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-508",
     "trigger": "Equipment Status & Condition Management",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-509",
     "trigger": "QR / Barcode Equipment Identification",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-510",
     "trigger": "Inventory Location Allocation",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-511",
     "trigger": "Inventory Transfer Management",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-512",
     "trigger": "Inventory Adjustment & Exception Management",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-513",
     "trigger": "Inventory Intelligence & Rebalancing",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a real-time operational overview of all rental inventory across venues and locations.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental inventory",
       "provenance": "pack Rental_Management.pdf, page 17 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Location",
        "Product",
        "Category",
        "Tracking Model",
        "Inventory Status",
        "Condition",
        "Availability"
       ],
       "notes": "The pack filters this screen by tenant, venue, location, product, category, tracking model and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 17 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Inventory",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Available Now",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Reserved",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Rented",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Under Maintenance",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Damaged",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Lost",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Out of Service",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Inventory Utilization %",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Inventory Alerts",
       "provenance": "pack Rental_Management.pdf, page 17 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental inventory list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental inventory untouched.",
   "emptyFirstRun": "No rental inventory yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental inventory are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listInventoryItems",
    "contract": "inventory",
    "purpose": "Stock across locations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "What is where",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total Inventory",
    "Available Now",
    "Reserved",
    "Rented",
    "Under Maintenance",
    "Damaged"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-504",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-504"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 17. 0 of 9 labels bound to a contract property; 19 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-505",
  "name": "Serialized Equipment Registry",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "2",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/serialized-equipment-registry-bo-505",
   "component": "apps/venue-management-web/src/routes/rentals/SerializedEquipmentRegistry.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Fields) and no display directory — it is settings, not a population",
  "purpose": "Manage individually identifiable rental assets.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Serial Number",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Asset Code",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Manufacturer Serial Number",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Location",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Acquisition Date",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Purchase Cost",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Warranty Expiry",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Condition",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Rental_Management.pdf, page 18 §Fields"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The serialized equipment registry configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the serialized equipment registry untouched.",
   "emptyFirstRun": "No serialized equipment registry configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listSerialisedItems",
    "contract": "inventory",
    "purpose": "Individually identified assets",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAssets",
    "contract": "maintenance",
    "purpose": "The asset register behind them",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-505",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-505"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 18. 0 of 0 labels bound to a contract property; 10 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-506",
  "name": "Equipment / Asset Profile",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "3",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/equipment-asset-profile-bo-506",
   "component": "apps/venue-management-web/src/routes/rentals/EquipmentAssetProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a complete digital record for every serialized rental asset.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 19"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getAsset",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateAsset",
       "label": "Save asset",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateAsset"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The equipment asset profile list.",
   "error": "Could not load. Names which read failed and leaves the equipment asset profile untouched.",
   "emptyFirstRun": "No equipment asset profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment asset profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAsset",
    "contract": "maintenance",
    "purpose": "The asset profile",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateAsset",
    "contract": "maintenance",
    "purpose": "Change it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAsset",
     "listAssets"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-506",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-506"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-507",
  "name": "Pooled Inventory Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "4",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/pooled-inventory-management-bo-507",
   "component": "apps/venue-management-web/src/routes/rentals/PooledInventoryManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage products where individual physical items do not require serial-level tracking.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 20"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 20"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Increase Quantity",
       "provenance": "pack Rental_Management.pdf, page 20 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Decrease Quantity",
       "provenance": "pack Rental_Management.pdf, page 20 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Adjust Inventory",
       "provenance": "pack Rental_Management.pdf, page 20 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer Quantity",
       "provenance": "pack Rental_Management.pdf, page 20 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Mark Out of Service",
       "provenance": "pack Rental_Management.pdf, page 20 §Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The pooled inventory list.",
   "error": "Could not load. Names which read failed and leaves the pooled inventory untouched.",
   "emptyFirstRun": "No pooled inventory yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pooled inventory are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "Pooled quantities",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createStockMovement",
    "contract": "inventory",
    "purpose": "Adjust the pool",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getStockPositions",
     "listStockMovements"
    ]
   },
   {
    "operationId": "createStockTransfer",
    "contract": "inventory",
    "purpose": "Move pooled quantity to another location",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Transfer Quantity",
    "invalidates": [
     "getStockPositions"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-507",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-507"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 20. 0 of 0 labels bound to a contract property; 5 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Increase Quantity, Decrease Quantity, Adjust Inventory are choices sent by `createStockMovement` (kind adjustmentIn|adjustmentOut with reason); Mark Out of Service are choices sent by `createStockMovement` (kind adjustmentOut with reason outOfService; return with adjustmentIn); Transfer Quantity: `createStockTransfer`.",
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
  "id": "BO-508",
  "name": "Equipment Status & Condition Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "5",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/equipment-status-condition-management-bo-508",
   "component": "apps/venue-management-web/src/routes/rentals/EquipmentStatusConditionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Separate operational status from physical condition. This distinction is important.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 20"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 20"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setAssetStatus",
       "label": "Save asset status",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getAsset",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAssetStatus"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The equipment status condition list.",
   "error": "Could not load. Names which read failed and leaves the equipment status condition untouched.",
   "emptyFirstRun": "No equipment status condition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment status condition are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAssetStatus",
    "contract": "maintenance",
    "purpose": "Available, rented or faulty",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAsset",
     "listAssets"
    ]
   },
   {
    "operationId": "getAsset",
    "contract": "maintenance",
    "purpose": "Current condition",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-508",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-508"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-509",
  "name": "QR / Barcode Equipment Identification",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "6",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/qr-barcode-equipment-identification-bo-509",
   "component": "apps/venue-management-web/src/routes/rentals/QrBarcodeEquipmentIdentification.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give every physical serialized rental item a scannable digital identity. This incorporates the equipment-assignment scanning recommendation from the source.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 21"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 21"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupAsset",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The barcode equipment identification list.",
   "error": "Could not load. Names which read failed and leaves the barcode equipment identification untouched.",
   "emptyFirstRun": "No barcode equipment identification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the barcode equipment identification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "lookupAsset",
    "contract": "maintenance",
    "purpose": "Scan a QR or barcode",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-509",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-509"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 21. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-510",
  "name": "Inventory Location Allocation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "7",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/inventory-location-allocation-bo-510",
   "component": "apps/venue-management-web/src/routes/rentals/InventoryLocationAllocation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage how inventory is distributed among rental locations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 22"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listStockLocations",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createStockLocation",
       "label": "Create stock location",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createStockLocation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory location allocation list.",
   "error": "Could not load. Names which read failed and leaves the inventory location allocation untouched.",
   "emptyFirstRun": "No inventory location allocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory location allocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStockLocations",
    "contract": "inventory",
    "purpose": "Where stock may sit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createStockLocation",
    "contract": "inventory",
    "purpose": "Add a location",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listStockLocations"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-510",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-510"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-511",
  "name": "Inventory Transfer Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "8",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/inventory-transfer-management-bo-511",
   "component": "apps/venue-management-web/src/routes/rentals/InventoryTransferManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control physical inventory movement between locations. The original requirements explicitly include inventory transfers between locations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 23"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Serialized asset transfer",
       "provenance": "pack Rental_Management.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Pooled quantity transfer",
       "provenance": "pack Rental_Management.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Bulk transfer",
       "provenance": "pack Rental_Management.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Scheduled transfer",
       "provenance": "pack Rental_Management.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Emergency transfer",
       "provenance": "pack Rental_Management.pdf, page 23 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "label": "Inbound and outbound transfers",
       "bindsTo": "StockTransfer",
       "columns": [
        "StockTransfer.transferNumber",
        "StockTransfer.fromLocationId",
        "StockTransfer.toLocationId",
        "StockTransfer.fromVenueId",
        "StockTransfer.toVenueId",
        "StockTransfer.status",
        "StockTransfer.dispatchedAt",
        "StockTransfer.receivedAt"
       ],
       "operation": "listStockTransfers",
       "notes": "**Every transfer whose source or destination is this venue**, marked inbound or outbound (decided 28 September, audit R183).",
       "provenance": "contract inventory.yaml GET /stock-transfers"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory transfer list.",
   "error": "Could not load. Names which read failed and leaves the inventory transfer untouched.",
   "emptyFirstRun": "No inventory transfer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory transfer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStockTransfers",
    "contract": "inventory",
    "purpose": "Transfers in flight, inbound and outbound for this venue (decided 28 September, audit R183)",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createStockTransfer",
    "contract": "inventory",
    "purpose": "Move stock between stations",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listStockTransfers",
     "getStockPositions"
    ]
   },
   {
    "operationId": "receiveStockTransfer",
    "contract": "inventory",
    "purpose": "Receive it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listStockTransfers",
     "getStockPositions"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-511",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-511"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 23. 0 of 0 labels bound to a contract property; 5 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Pooled quantity transfer, Bulk transfer are choices sent by `createStockTransfer` (lines[] carry one or many items); Serialized asset transfer are choices sent by `createStockTransfer` (serialised item moved as a quantity-1 line; field gap: lines have no serial/assetId); Scheduled transfer, Emergency transfer are choices sent by `createStockTransfer` (field gap: add scheduledFor and priority (normal|emergency) to CreateStockTransferRequest).",
  "entryState": {
   "params": [
    {
     "name": "transferId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-512",
  "name": "Inventory Adjustment & Exception Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "9",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/inventory-adjustment-exception-management-bo-512",
   "component": "apps/venue-management-web/src/routes/rentals/InventoryAdjustmentExceptionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle physical inventory discrepancies and exceptional conditions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 23"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createStockMovement",
       "label": "Create stock movement",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listStockMovements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createStockMovement"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory adjustment exception list.",
   "error": "Could not load. Names which read failed and leaves the inventory adjustment exception untouched.",
   "emptyFirstRun": "No inventory adjustment exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory adjustment exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createStockMovement",
    "contract": "inventory",
    "purpose": "Adjust with a reason",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getStockPositions",
     "listStockMovements"
    ]
   },
   {
    "operationId": "listStockMovements",
    "contract": "inventory",
    "purpose": "Adjustments so far",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-512",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-512"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-513",
  "name": "Inventory Intelligence & Rebalancing",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "2",
   "number": "10",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/inventory-intelligence-rebalancing-bo-513",
   "component": "apps/venue-management-web/src/routes/rentals/InventoryIntelligenceRebalancing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-504"
   ],
   "exitTo": [
    "BO-504"
   ],
   "transitions": [
    {
     "to": "BO-504",
     "trigger": "Back to Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Use operational data and AI to improve rental inventory distribution and utilization. This is one of the areas where TICVAI should go beyond the original matrix.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 24 §Display"
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
       "label": "Every inventory intelligence rebalancing",
       "columns": [
        "Utilization by product",
        "Utilization by location",
        "Idle equipment",
        "Shortage risk",
        "Excess inventory",
        "Maintenance impact",
        "Unavailable inventory",
        "Inventory turnover"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 24 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inventory intelligence rebalancing",
       "bindsTo": null,
       "columns": [
        "Utilization by product",
        "Utilization by location",
        "Idle equipment",
        "Shortage risk",
        "Excess inventory",
        "Maintenance impact",
        "Unavailable inventory",
        "Inventory turnover"
       ],
       "notes": "The pack groups this record's detail under its own headings: “North Station”, “Marina Station”, “The board should visually demonstrate”, “Serialized Asset”, “Pooled Inventory”, “Integration Boundaries”.",
       "provenance": "pack Rental_Management.pdf, page 24 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Review Recommendation | Create Transfer | Dismiss",
       "provenance": "pack Rental_Management.pdf, page 24 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory intelligence rebalancing list.",
   "error": "Could not load. Names which read failed and leaves the inventory intelligence rebalancing untouched.",
   "emptyFirstRun": "No inventory intelligence rebalancing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory intelligence rebalancing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "Imbalance across locations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getSuggestedRequisitions",
    "contract": "inventory",
    "purpose": "What to move, and where",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createStockTransfer",
    "contract": "inventory",
    "purpose": "Act on a rebalancing recommendation by raising the transfer (review/dismiss are client-side)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Review Recommendation | Create Transfer | Dismiss",
    "invalidates": [
     "getStockPositions",
     "getSuggestedRequisitions"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Utilization by product",
    "Utilization by location",
    "Idle equipment",
    "Shortage risk",
    "Excess inventory",
    "Maintenance impact"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-513",
   "workshopBoard": "wireframes/WS117 Rental Management Board 2.dc.html#bo-513"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 24. 0 of 8 labels bound to a contract property; 9 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Review Recommendation | Create Transfer | Dismiss: `createStockTransfer`.",
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
 "getAsset": {
  "method": "GET",
  "path": "/assets/{assetId}",
  "contract": "maintenance",
  "summary": "Read an asset with history and documents",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AssetDetail"
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
 "listAssets": {
  "method": "GET",
  "path": "/assets",
  "contract": "maintenance",
  "summary": "List assets",
  "permission": "ASSET_VIEW",
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
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "maintenanceDue",
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
 "lookupAsset": {
  "method": "GET",
  "path": "/assets/lookup",
  "contract": "maintenance",
  "summary": "Find an asset by tag or QR",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assetTag",
    "in": "query",
    "required": null
   },
   {
    "name": "serialNumber",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AssetDetail"
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
 "setAssetStatus": {
  "method": "PUT",
  "path": "/assets/{assetId}/status",
  "contract": "maintenance",
  "summary": "Take an asset out of service or return it",
  "permission": "ASSET_MANAGE",
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
  "requestBody": "SetAssetStatusRequest",
  "responds": "AssetStatusResult"
 },
 "updateAsset": {
  "method": "PATCH",
  "path": "/assets/{assetId}",
  "contract": "maintenance",
  "summary": "Amend an asset",
  "permission": "ASSET_MANAGE",
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
  "responds": "Asset"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Asset": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateAssetRequest"
   },
   {
    "type": "object",
    "x-ticvai-retired-columns": [
     "is_maintenance_overdue",
     "document_refs"
    ],
    "required": [
     "id",
     "status"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "resourceId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"
     },
     "deviceId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"
     },
     "acquisitionCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "acquiredOn": {
      "type": "string",
      "format": "date",
      "nullable": true
     },
     "depreciation": {
      "type": "object",
      "nullable": true,
      "description": "**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n",
      "properties": {
       "method": {
        "type": "string",
        "enum": [
         "straightLine",
         "reducingBalance",
         "unitsOfProduction",
         "none"
        ]
       },
       "usefulLifeMonths": {
        "type": "integer"
       },
       "residualValue": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "accumulatedDepreciation": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     },
     "retiredOn": {
      "type": "string",
      "format": "date",
      "nullable": true,
      "description": "**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"
     },
     "disposalProceeds": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "status": {
      "$ref": "#/components/schemas/AssetStatus"
     },
     "statusReason": {
      "type": "string",
      "nullable": true
     },
     "openWorkOrderCount": {
      "type": "integer",
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"
     },
     "nextMaintenanceDueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"
     },
     "isMaintenanceOverdue": {
      "type": "boolean",
      "readOnly": true,
      "x-ticvai-persisted": false,
      "x-ticvai-derived": "onRead",
      "description": "`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"
     },
     "lastInspectionAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"
     },
     "usageCounter": {
      "type": "number",
      "nullable": true,
      "description": "Cycles, hours or kilometres. Drives usage-based maintenance."
     }
    }
   }
  ]
 },
 "AssetDetail": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/Asset"
   },
   {
    "type": "object",
    "properties": {
     "openWorkOrders": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/WorkOrder"
      }
     },
     "maintenancePlans": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/MaintenancePlan"
      }
     },
     "documents": {
      "type": "array",
      "description": "Manuals, procedures, certificates. What a technician needs on site. Read from `maintenance.asset_document`.\n",
      "items": {
       "$ref": "#/components/schemas/AssetDocument"
      }
     }
    }
   }
  ]
 },
 "AssetDocument": {
  "x-ticvai-persistence": "maintenance.asset_document",
  "type": "object",
  "description": "A document attached to an asset — manual, procedure, certificate — with the name and kind a technician needs on site. **One row per document**, because `AssetDetail.documents` returns a name and a kind for each and a `text[]` of refs has nowhere to hold either.\n",
  "required": [
   "id",
   "assetId",
   "ref"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "ref": {
    "type": "string",
    "description": "The document in the media store."
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AssetDocumentKind"
     }
    ],
    "nullable": true,
    "description": "Null where the document arrived as a bare ref in `documentRefs`."
   }
  }
 },
 "AssetDocumentInput": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "ref",
   "kind"
  ],
  "properties": {
   "ref": {
    "type": "string",
    "description": "The document in the media store."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "kind": {
    "$ref": "#/components/schemas/AssetDocumentKind"
   }
  }
 },
 "AssetDocumentKind": {
  "type": "string",
  "enum": [
   "manual",
   "sop",
   "certificate",
   "warranty",
   "drawing",
   "riskAssessment"
  ]
 },
 "AssetStatus": {
  "type": "string",
  "enum": [
   "inService",
   "outOfService",
   "underMaintenance",
   "awaitingParts",
   "retired",
   "disposed"
  ]
 },
 "AssetStatusResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asset",
   "downstreamEffects"
  ],
  "properties": {
   "asset": {
    "$ref": "#/components/schemas/Asset"
   },
   "downstreamEffects": {
    "type": "object",
    "description": "What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n",
    "properties": {
     "productsSuspended": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "accessPointBlocked": {
      "type": "boolean"
     },
     "performancesAffected": {
      "type": "integer"
     },
     "workOrderId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   }
  }
 },
 "CreateAssetRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "assetTag",
   "name",
   "venueId",
   "criticality"
  ],
  "properties": {
   "assetTag": {
    "type": "string",
    "maxLength": 64,
    "x-ticvai-unique": "venue",
    "description": "**Unique per venue** (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. Two venues may each have an `A-001`.\n"
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
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "criticality": {
    "$ref": "#/components/schemas/AssetCriticality"
   },
   "priorityOverride": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderPriority"
     }
    ],
    "nullable": true,
    "description": "**\"If this device goes down, raise this priority\"** (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. Null means the score decides.\n"
   },
   "manufacturer": {
    "type": "string",
    "maxLength": 200
   },
   "model": {
    "type": "string",
    "maxLength": 200
   },
   "serialNumber": {
    "type": "string",
    "maxLength": 128
   },
   "commissionedAt": {
    "type": "string",
    "format": "date"
   },
   "warrantyExpiresAt": {
    "type": "string",
    "format": "date"
   },
   "supplierId": {
    "type": "string",
    "format": "uuid"
   },
   "linkedProductIds": {
    "type": "array",
    "description": "Products this asset delivers. A fault here can stop them selling.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "linkedAccessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Access point this asset controls. Out of service blocks it."
   },
   "requiresInspectionToReturn": {
    "type": "boolean",
    "default": false,
    "description": "True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"
   },
   "documents": {
    "type": "array",
    "description": "Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from.\n",
    "items": {
     "$ref": "#/components/schemas/AssetDocumentInput"
    }
   },
   "documentRefs": {
    "type": "array",
    "x-ticvai-persisted": false,
    "description": "**The refs alone, kept for callers that predate `documents`.** Each ref sent here is stored as an `asset_document` row with no name and no kind. Returned as the refs of `documents`, computed on read — there is no second copy to fall out of step.\n",
    "items": {
     "type": "string"
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
 "MaintenancePlan": {
  "x-ticvai-persistence": "maintenance.preventive_plan",
  "type": "object",
  "required": [
   "id",
   "name",
   "assetId",
   "taskTemplate"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "assetCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Applies to every asset in the category rather than one."
   },
   "intervalDays": {
    "type": "integer",
    "nullable": true,
    "description": "Elapsed-time trigger."
   },
   "usageInterval": {
    "type": "number",
    "nullable": true,
    "description": "Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"
   },
   "leadTimeDays": {
    "type": "integer",
    "default": 7,
    "description": "How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"
   },
   "taskTemplate": {
    "type": "object",
    "required": [
     "title",
     "priority"
    ],
    "properties": {
     "title": {
      "type": "string"
     },
     "description": {
      "type": "string"
     },
     "priority": {
      "$ref": "#/components/schemas/WorkOrderPriority"
     },
     "estimatedMinutes": {
      "type": "integer"
     },
     "inspectionTemplateId": {
      "type": "string",
      "format": "uuid"
     },
     "requiredPartIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "lastCompletedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "nextDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
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
 "SetAssetStatusRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "status",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "status": {
    "$ref": "#/components/schemas/AssetStatus"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 1000
   },
   "inspectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for return to service where the asset demands it."
   },
   "raiseWorkOrder": {
    "type": "boolean",
    "default": false
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
  "x-ticvai-retired-columns": [
   "is_overdue"
  ],
  "type": "object",
  "required": [
   "id",
   "workOrderNumber",
   "title",
   "venueId",
   "status",
   "priority",
   "kind",
   "createdAt"
  ],
  "properties": {
   "downtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"
   },
   "rootCause": {
    "type": "string",
    "nullable": true,
    "enum": [
     "wearAndTear",
     "operatorError",
     "guestDamage",
     "manufacturingDefect",
     "environmental",
     "softwareFault",
     "powerFailure",
     "deferredMaintenance",
     "unknown"
    ],
    "description": "**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"
   },
   "rootCauseNote": {
    "type": "string",
    "nullable": true
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "escalationLevel": {
    "type": "integer",
    "default": 0,
    "description": "**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "workOrderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
   },
   "title": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "readOnly": true,
    "description": "The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."
   },
   "prioritySource": {
    "type": "string",
    "enum": [
     "scored",
     "assetOverride",
     "manual"
    ],
    "readOnly": true,
    "description": "Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."
   },
   "faultAssessment": {
    "$ref": "#/components/schemas/WorkOrderFaultAssessment"
   },
   "requiredQualificationCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Skills the job needs (M17-13)."
   },
   "kind": {
    "$ref": "#/components/schemas/WorkOrderKind"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"
   },
   "elapsedMinutes": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"
   },
   "isTimerRunning": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"
   },
   "requiresVerification": {
    "type": "boolean"
   },
   "sourcePlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceInspectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkOrderPriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent",
   "emergency"
  ]
 }
}
```
