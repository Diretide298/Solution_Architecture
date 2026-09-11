# WS89 — Rental Management board 2

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-504` | Rental Inventory Command Center | commandCentre | 0 | 0 | — |
| `BO-505` | Serialized Equipment Registry | configEditor | 0 | 0 | — |
| `BO-506` | Equipment / Asset Profile | listDetail | 0 | 0 | — |
| `BO-507` | Pooled Inventory Management | listDetail | 0 | 0 | — |
| `BO-508` | Equipment Status & Condition Management | listDetail | 0 | 0 | — |
| `BO-509` | QR / Barcode Equipment Identification | listDetail | 0 | 0 | — |
| `BO-510` | Inventory Location Allocation | listDetail | 0 | 0 | — |
| `BO-511` | Inventory Transfer Management | listDetail | 0 | 0 | — |
| `BO-512` | Inventory Adjustment & Exception Management | listDetail | 0 | 0 | — |
| `BO-513` | Inventory Intelligence & Rebalancing | listDetail | 0 | 0 | — |

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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-504"
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-505"
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
   "regions": []
  },
  "states": {
   "loading": "The equipment asset profile list.",
   "error": "Could not load. Names which read failed and leaves the equipment asset profile untouched.",
   "emptyFirstRun": "No equipment asset profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment asset profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-506"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Increase Quantity, Decrease Quantity, Adjust Inventory, Transfer Quantity, Mark Out of Service. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 20 §Actions"
   },
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-507"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 20. 0 of 0 labels bound to a contract property; 5 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The equipment status condition list.",
   "error": "Could not load. Names which read failed and leaves the equipment status condition untouched.",
   "emptyFirstRun": "No equipment status condition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment status condition are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-508"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The barcode equipment identification list.",
   "error": "Could not load. Names which read failed and leaves the barcode equipment identification untouched.",
   "emptyFirstRun": "No barcode equipment identification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the barcode equipment identification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-509"
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
   "regions": []
  },
  "states": {
   "loading": "The inventory location allocation list.",
   "error": "Could not load. Names which read failed and leaves the inventory location allocation untouched.",
   "emptyFirstRun": "No inventory location allocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory location allocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-510"
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
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Serialized asset transfer, Pooled quantity transfer, Bulk transfer, Scheduled transfer, Emergency transfer. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 23 §Support"
   },
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-511"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 23. 0 of 0 labels bound to a contract property; 5 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The inventory adjustment exception list.",
   "error": "Could not load. Names which read failed and leaves the inventory adjustment exception untouched.",
   "emptyFirstRun": "No inventory adjustment exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory adjustment exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-512"
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
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Review Recommendation | Create Transfer | Dismiss. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 24 §Actions"
   },
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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-513"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 24. 0 of 8 labels bound to a contract property; 9 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
