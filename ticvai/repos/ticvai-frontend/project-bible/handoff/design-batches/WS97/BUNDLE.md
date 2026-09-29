# WS97 — Rental Management board 10

**10 screens · 8 operations · 12 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `ASSET_VIEW, PRODUCT_VIEW, RENTAL_VIEW, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE, RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-584` | Rental Executive Command Center | listDetail | 1 | 0 | — |
| `BO-585` | Rental Revenue & Commercial Analytics | commandCentre | 1 | 0 | — |
| `BO-586` | Utilization & Capacity Analytics | commandCentre | 1 | 0 | — |
| `BO-587` | Inventory & Equipment Performance Analytics | commandCentre | 1 | 0 | — |
| `BO-588` | Rental Duration, Extension & Return Analytics | commandCentre | 1 | 0 | — |
| `BO-589` | Damage, Loss, Deposit & Exception Analytics | commandCentre | 1 | 0 | — |
| `BO-590` | Location & Channel Performance | listDetail | 1 | 0 | — |
| `BO-591` | Rental Forecasting & Demand Intelligence | commandCentre | 1 | 0 | — |
| `BO-592` | Audit, Governance & Operational Control | listDetail | 1 | 0 | — |
| `BO-593` | AI Rental Management Copilot & Action Center | commandCentre | 1 | 0 | — |

## Thin screens in this batch

**BO-584, BO-592, BO-593 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-584",
  "name": "Rental Executive Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "1",
   "page": 124
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-executive-command-center-bo-584",
   "component": "apps/venue-management-web/src/routes/rentals/RentalExecutiveCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-585",
    "BO-586",
    "BO-587",
    "BO-588",
    "BO-589",
    "BO-590",
    "BO-591",
    "BO-592",
    "BO-593"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-585",
     "trigger": "Rental Revenue & Commercial Analytics",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-586",
     "trigger": "Utilization & Capacity Analytics",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-587",
     "trigger": "Inventory & Equipment Performance Analytics",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-588",
     "trigger": "Rental Duration, Extension & Return Analytics",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-589",
     "trigger": "Damage, Loss, Deposit & Exception Analytics",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-590",
     "trigger": "Location & Channel Performance",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-591",
     "trigger": "Rental Forecasting & Demand Intelligence",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-592",
     "trigger": "Audit, Governance & Operational Control",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-593",
     "trigger": "AI Rental Management Copilot & Action Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide senior management with an immediate view of the overall rental business.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 124"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental executive",
       "provenance": "pack Rental_Management.pdf, page 124 §Global Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Rental Location",
        "Product",
        "Category",
        "Date Range",
        "Channel",
        "Customer Segment"
       ],
       "notes": "The pack filters this screen by tenant, venue, rental location, product, category, date range and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 124 §Global Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental executive list.",
   "error": "Could not load. Names which read failed and leaves the rental executive untouched.",
   "emptyFirstRun": "No rental executive yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental executive are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRentalBookings",
    "contract": "rental",
    "purpose": "The commercial picture",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-584",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-584"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 124. 0 of 8 labels bound to a contract property; 8 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-585",
  "name": "Rental Revenue & Commercial Analytics",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "2",
   "page": 126
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-revenue-commercial-analytics-bo-585",
   "component": "apps/venue-management-web/src/routes/rentals/RentalRevenueCommercialAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Analyze rental commercial performance. The original scope specifically requires reporting on rental revenue.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental revenue commercial",
       "provenance": "pack Rental_Management.pdf, page 126 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Product",
        "Category",
        "Venue",
        "Location",
        "Channel",
        "Day",
        "Time",
        "Customer segment"
       ],
       "notes": "The pack filters this screen by product, category, venue, location, channel, day and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 126 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Gross Rental Revenue",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Net Rental Revenue",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Transaction Value",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Revenue per Rental Hour",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Extension Revenue",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Late-Fee Revenue",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Damage Charges",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Deposit Captures",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Discount Value",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Refund Value",
       "provenance": "pack Rental_Management.pdf, page 126 §KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental revenue commercial list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental revenue commercial untouched.",
   "emptyFirstRun": "No rental revenue commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental revenue commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Rental revenue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Gross Rental Revenue",
    "Net Rental Revenue",
    "Average Transaction Value",
    "Average Revenue per Rental Hour",
    "Extension Revenue",
    "Late-Fee Revenue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-585",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-585"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 126. 0 of 8 labels bound to a contract property; 18 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-586",
  "name": "Utilization & Capacity Analytics",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "3",
   "page": 127
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/utilization-capacity-analytics-bo-586",
   "component": "apps/venue-management-web/src/routes/rentals/UtilizationCapacityAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Understand how efficiently rental inventory is being used. The original requirements specifically call for utilization-rate reporting.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Overall Utilization",
       "provenance": "pack Rental_Management.pdf, page 127 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Peak Utilization",
       "provenance": "pack Rental_Management.pdf, page 127 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Off-Peak Utilization",
       "provenance": "pack Rental_Management.pdf, page 127 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Idle Inventory",
       "provenance": "pack Rental_Management.pdf, page 127 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Sold-Out Hours",
       "provenance": "pack Rental_Management.pdf, page 127 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Lost Sales Due to Capacity",
       "provenance": "pack Rental_Management.pdf, page 127 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Protected Inventory Utilization",
       "provenance": "pack Rental_Management.pdf, page 127 §KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The utilization capacity analytics list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the utilization capacity analytics untouched.",
   "emptyFirstRun": "No utilization capacity analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the utilization capacity analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceUtilisation",
    "contract": "resources",
    "purpose": "Utilisation and capacity",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-586",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-586"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 127. 0 of 0 labels bound to a contract property; 7 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-587",
  "name": "Inventory & Equipment Performance Analytics",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "4",
   "page": 127
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/inventory-equipment-performance-analytics-bo-587",
   "component": "apps/venue-management-web/src/routes/rentals/InventoryEquipmentPerformanceAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Fleet KPIs) and a per-row directory (§Identify) — counts over a population, then the population",
  "purpose": "Measure the operational performance of the physical rental fleet. The original requirements call for reporting on inventory availability and equipment performance.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 127 §Identify"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Assets",
       "provenance": "pack Rental_Management.pdf, page 127 §Fleet KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Available",
       "provenance": "pack Rental_Management.pdf, page 127 §Fleet KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Rented",
       "provenance": "pack Rental_Management.pdf, page 127 §Fleet KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Maintenance",
       "provenance": "pack Rental_Management.pdf, page 127 §Fleet KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Out of Service",
       "provenance": "pack Rental_Management.pdf, page 127 §Fleet KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Lost",
       "provenance": "pack Rental_Management.pdf, page 127 §Fleet KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Rentals per Asset",
       "provenance": "pack Rental_Management.pdf, page 127 §Fleet KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Revenue per Asset",
       "provenance": "pack Rental_Management.pdf, page 127 §Fleet KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every inventory equipment performance",
       "columns": [
        "Most utilized assets",
        "Least utilized assets",
        "Highest revenue assets",
        "Highest maintenance assets",
        "Repeatedly damaged assets",
        "Excessively idle inventory"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 127 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inventory equipment performance",
       "bindsTo": null,
       "columns": [
        "Most utilized assets",
        "Least utilized assets",
        "Highest revenue assets",
        "Highest maintenance assets",
        "Repeatedly damaged assets",
        "Excessively idle inventory"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Equipment Performance”.",
       "provenance": "pack Rental_Management.pdf, page 127 §Identify"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory equipment performance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the inventory equipment performance untouched.",
   "emptyFirstRun": "No inventory equipment performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory equipment performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAssetHistory",
    "contract": "maintenance",
    "purpose": "Equipment performance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total Assets",
    "Available",
    "Rented",
    "Maintenance",
    "Out of Service",
    "Lost"
   ],
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-587",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-587"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 127. 0 of 6 labels bound to a contract property; 14 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-588",
  "name": "Rental Duration, Extension & Return Analytics",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "5",
   "page": 128
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-duration-extension-return-analytics-bo-588",
   "component": "apps/venue-management-web/src/routes/rentals/RentalDurationExtensionReturnAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Understand customer usage behavior after checkout. The source explicitly requires reporting on rental duration and late returns.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Average Planned Duration",
       "provenance": "pack Rental_Management.pdf, page 128 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Actual Duration",
       "provenance": "pack Rental_Management.pdf, page 128 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Extension Rate",
       "provenance": "pack Rental_Management.pdf, page 128 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Extension",
       "provenance": "pack Rental_Management.pdf, page 128 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "On-Time Return %",
       "provenance": "pack Rental_Management.pdf, page 128 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Late Return %",
       "provenance": "pack Rental_Management.pdf, page 128 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Late Duration",
       "provenance": "pack Rental_Management.pdf, page 128 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Critical Overdue Count",
       "provenance": "pack Rental_Management.pdf, page 128 §KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental duration extension list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental duration extension untouched.",
   "emptyFirstRun": "No rental duration extension yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental duration extension are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRentalBookings",
    "contract": "rental",
    "purpose": "Duration, extension and return",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-588",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-588"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 128. 0 of 0 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-589",
  "name": "Damage, Loss, Deposit & Exception Analytics",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "6",
   "page": 129
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/damage-loss-deposit-exception-analytics-bo-589",
   "component": "apps/venue-management-web/src/routes/rentals/DamageLossDepositExceptionAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Give management visibility into operational and financial risk. The original scope explicitly requires reporting on damaged items and deposit collection/refund.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Damage Cases",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Damage Rate",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Lost Equipment",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Total Damage Charges",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Deposit Collected/Authorized",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Deposit Released",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Deposit Captured",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Deposit Pending",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Waived Fees",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Manual Overrides",
       "provenance": "pack Rental_Management.pdf, page 129 §KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The damage loss deposit list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the damage loss deposit untouched.",
   "emptyFirstRun": "No damage loss deposit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the damage loss deposit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRentalBookings",
    "contract": "rental",
    "purpose": "Damage, loss and deposit exceptions",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Damage Cases",
    "Damage Rate",
    "Lost Equipment",
    "Total Damage Charges",
    "Deposit Collected/Authorized",
    "Deposit Released"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-589",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-589"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 129. 0 of 0 labels bound to a contract property; 10 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-590",
  "name": "Location & Channel Performance",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "7",
   "page": 130
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/location-channel-performance-bo-590",
   "component": "apps/venue-management-web/src/routes/rentals/LocationChannelPerformance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Compare rental performance across physical locations and sales channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 130"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "KPI",
       "operation": "getAnalyticsBenchmark",
       "notes": "Sends `?kpiId=` (required): rentals, revenue, utilisation, availability or damage, one per read.",
       "provenance": "contract reporting.yaml GET /analytics-benchmarks"
      },
      {
       "kind": "multiSelect",
       "label": "Locations",
       "operation": "getAnalyticsBenchmark",
       "notes": "Sends `?scopePaths=`.",
       "provenance": "contract reporting.yaml GET /analytics-benchmarks"
      },
      {
       "kind": "selectField",
       "label": "Normalise by",
       "operation": "getAnalyticsBenchmark",
       "notes": "Sends `?normaliseBy=`.",
       "provenance": "contract reporting.yaml GET /analytics-benchmarks"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Location comparison",
       "bindsTo": "BenchmarkRow",
       "columns": [
        "BenchmarkRow.label",
        "BenchmarkRow.value",
        "BenchmarkRow.normalisedValue",
        "BenchmarkRow.normaliseBy",
        "BenchmarkRow.rank",
        "BenchmarkRow.percentile"
       ],
       "operation": "getAnalyticsBenchmark",
       "notes": "One KPI per read; the pack's side-by-side Rentals / Revenue / Utilization / Availability / Damage table needs one read per KPI.",
       "provenance": "contract reporting.yaml GET /analytics-benchmarks"
      },
      {
       "kind": "chart",
       "label": "Channel comparison",
       "columns": [
        "Channel",
        "Bookings",
        "Revenue",
        "Average value",
        "Cancellation",
        "No-show",
        "Utilization contribution"
       ],
       "notes": "B2C, B2B, POS, Walk-In, Mobile App, API/Partner. Benchmarks compare scope paths, not sales channels.",
       "provenance": "pack Rental_Management.pdf, page 130"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "AI rebalancing insight",
       "columns": [
        "Insight",
        "Recommendation",
        "Linked inventory transfer"
       ],
       "notes": "The pack's Marina A to North Station example; no operation returns it.",
       "provenance": "pack Rental_Management.pdf, page 130"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The location channel performance list.",
   "error": "Could not load. Names which read failed and leaves the location channel performance untouched.",
   "emptyFirstRun": "No location channel performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the location channel performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAnalyticsBenchmark",
    "contract": "reporting",
    "purpose": "Location and channel performance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-590",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-590"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 130. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Rental_Management.pdf p.130; contract reporting.yaml GET /analytics-benchmarks. Pack labels with no schema field yet (shown as plain labels): Channel dimension (B2C, B2B, POS, Walk-In, Mobile App, API), Bookings, Average value, Cancellation, No-show, Utilization contribution, AI rebalancing insight.",
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
  "id": "BO-591",
  "name": "Rental Forecasting & Demand Intelligence",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "8",
   "page": 131
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-forecasting-demand-intelligence-bo-591",
   "component": "apps/venue-management-web/src/routes/rentals/RentalForecastingDemandIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Forecast KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Forecast future rental demand and identify capacity problems before they happen. This formally incorporates the AI utilization/demand forecasting recommendation from the source.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Expected Rentals",
       "provenance": "pack Rental_Management.pdf, page 131 §Forecast KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Expected Revenue",
       "provenance": "pack Rental_Management.pdf, page 131 §Forecast KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Utilization",
       "provenance": "pack Rental_Management.pdf, page 131 §Forecast KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Sell-Out Probability",
       "provenance": "pack Rental_Management.pdf, page 131 §Forecast KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Inventory Shortage Risk",
       "provenance": "pack Rental_Management.pdf, page 131 §Forecast KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Maintenance Capacity Impact",
       "provenance": "pack Rental_Management.pdf, page 131 §Forecast KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental forecasting demand list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental forecasting demand untouched.",
   "emptyFirstRun": "No rental forecasting demand yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental forecasting demand are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDemandBookingCurve",
    "contract": "catalogue",
    "purpose": "Demand forecast",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Expected Rentals",
    "Expected Revenue",
    "Forecast Utilization",
    "Sell-Out Probability",
    "Inventory Shortage Risk",
    "Maintenance Capacity Impact"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-591",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-591"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 131. 0 of 0 labels bound to a contract property; 6 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-592",
  "name": "Audit, Governance & Operational Control",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "9",
   "page": 131
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/audit-governance-operational-control-bo-592",
   "component": "apps/venue-management-web/src/routes/rentals/AuditGovernanceOperationalControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Provide management and administrators with traceability across Rental Management. The source requires role-based permissions and audit logging for rental operations.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 131 §Track"
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
       "label": "Every audit governance operational",
       "columns": [
        "Product configuration change",
        "Inventory adjustment",
        "Asset status override",
        "Price change",
        "Deposit override",
        "Booking modification",
        "Cancellation",
        "Equipment assignment",
        "Rental extension",
        "Equipment swap",
        "Late-fee waiver",
        "Damage assessment",
        "Damage-fee override",
        "Deposit capture",
        "Maintenance status change",
        "Asset retirement"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 131 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected audit governance operational",
       "bindsTo": null,
       "columns": [
        "Product configuration change",
        "Inventory adjustment",
        "Asset status override",
        "Price change",
        "Deposit override",
        "Booking modification",
        "Cancellation",
        "Equipment assignment",
        "Rental extension",
        "Equipment swap",
        "Late-fee waiver",
        "Damage assessment",
        "Damage-fee override",
        "Deposit capture",
        "Maintenance status change",
        "Asset retirement"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Audit Table”, “Export”, “Rental Operator”, “Maintenance”, “Finance”, “Manager”.",
       "provenance": "pack Rental_Management.pdf, page 131 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audit governance operational list.",
   "error": "Could not load. Names which read failed and leaves the audit governance operational untouched.",
   "emptyFirstRun": "No audit governance operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audit governance operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceAuditTrail",
    "contract": "resources",
    "purpose": "Governance and audit",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Product configuration change",
    "Inventory adjustment",
    "Asset status override",
    "Price change",
    "Deposit override",
    "Booking modification"
   ],
   "params": [
    {
     "name": "resourceId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-592",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-592"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 131. 0 of 16 labels bound to a contract property; 16 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-593",
  "name": "AI Rental Management Copilot & Action Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "10",
   "number": "10",
   "page": 133
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/ai-rental-management-copilot-action-center-bo-593",
   "component": "apps/venue-management-web/src/routes/rentals/AiRentalManagementCopilotActionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-584"
   ],
   "exitTo": [
    "BO-584"
   ],
   "transitions": [
    {
     "to": "BO-584",
     "trigger": "Back to Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs & Dashboards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a natural-language AI interface across the complete Rental Management module. I strongly recommend this as the final screen because it aligns the rental module with TICVAI's overall AI-first architecture. Instead of management having to manually navigate every report, they should be able to ask TICVAI questions.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "↓",
       "provenance": "pack Rental_Management.pdf, page 133 §KPIs & Dashboards"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "askReportingQuestion",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "askReportingQuestion"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental copilot action list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental copilot action untouched.",
   "emptyFirstRun": "No rental copilot action yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental copilot action are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Ask about rentals",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-593",
   "workshopBoard": "wireframes/WS125 Rental Management Board 10.dc.html#bo-593"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 133. 0 of 0 labels bound to a contract property; 1 of 112 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "askReportingQuestion": {
  "method": "POST",
  "path": "/reports/ask",
  "contract": "reporting",
  "summary": "Natural-language reporting query",
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
  "responds": "NaturalLanguageAnswer"
 },
 "getAnalyticsBenchmark": {
  "method": "GET",
  "path": "/analytics-benchmarks",
  "contract": "reporting",
  "summary": "One site against another, on a like-for-like basis",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "kpiId",
    "in": "query",
    "required": true
   },
   {
    "name": "scopePaths",
    "in": "query",
    "required": null
   },
   {
    "name": "normaliseBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "BenchmarkRow"
 },
 "getAssetHistory": {
  "method": "GET",
  "path": "/assets/{assetId}/history",
  "contract": "maintenance",
  "summary": "Service history",
  "permission": "ASSET_VIEW",
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
 "getResourceAuditTrail": {
  "method": "GET",
  "path": "/resources/{resourceId}/audit",
  "contract": "resources",
  "summary": "Every material change, with who and why",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceAuditEntry"
 },
 "getResourceUtilisation": {
  "method": "GET",
  "path": "/resource-utilisation",
  "contract": "resources",
  "summary": "How much of each resource's available time was used",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ResourceUtilisation"
 },
 "listDemandBookingCurve": {
  "method": "GET",
  "path": "/demand-booking-curve",
  "contract": "catalogue",
  "summary": "AI Demand Forecasting & Booking Curve Studio",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "performance",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "horizon",
    "in": "query",
    "required": false
   },
   {
    "name": "dateFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "dateTo",
    "in": "query",
    "required": false
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
 "listRentalBookings": {
  "method": "GET",
  "path": "/rental-bookings",
  "contract": "rental",
  "summary": "Reservations across venues and locations",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
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
  "responds": "RentalBooking"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BenchmarkNormalisation": {
  "type": "string",
  "description": "The basis a benchmark is compared on. Shared by `getAnalyticsBenchmark` and `BenchmarkRow`.",
  "enum": [
   "none",
   "perVisitor",
   "perOperatingHour",
   "perStaffedPosition",
   "perSquareMetre"
  ]
 },
 "BenchmarkRow": {
  "type": "object",
  "description": "BI board 10.4. **The normalisation travels with the comparison.**",
  "properties": {
   "scopePath": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "normalisedValue": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "normaliseBy": {
    "$ref": "#/components/schemas/BenchmarkNormalisation"
   },
   "rank": {
    "type": "integer"
   },
   "percentile": {
    "type": "number",
    "nullable": true
   }
  }
 },
 "GeneratedQuery": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n",
  "properties": {
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportColumn"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportFilter"
    }
   },
   "groupBy": {
    "type": "array",
    "items": {
     "type": "string"
    }
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
 "NaturalLanguageAnswer": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "conversationId",
   "question",
   "interpretation",
   "result",
   "confidence"
  ],
  "properties": {
   "conversationId": {
    "type": "string"
   },
   "question": {
    "type": "string"
   },
   "interpretation": {
    "type": "string",
    "description": "What the question was understood to mean, in plain language."
   },
   "generatedQuery": {
    "$ref": "#/components/schemas/GeneratedQuery",
    "description": "The structured query produced — data source, columns, filters, grouping. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`.\n"
   },
   "result": {
    "$ref": "#/components/schemas/ReportResult"
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "suggestedFollowUps": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modelVersion": {
    "type": "string"
   },
   "tokensUsed": {
    "type": "integer"
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
 "RentalBooking": {
  "type": "object",
  "x-ticvai-persistence": "rental.booking",
  "description": "Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n",
  "required": [
   "id",
   "productId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "reference": {
    "type": "string"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "returnLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "quantity": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "confirmed",
     "awaitingArrival",
     "checkedOut",
     "overdue",
     "partiallyReturned",
     "completed",
     "completedWithDamage",
     "notReturned",
     "cancelled",
     "noShow"
    ]
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accruedLateFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "readiness": {
    "type": "array",
    "readOnly": true,
    "description": "**Computed, not stored** — agreement, requirements, deposit, equipment.",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string"
      },
      "satisfied": {
       "type": "boolean"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "participants": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RentalParticipant"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalParticipant": {
  "type": "object",
  "x-ticvai-persistence": "rental.participant",
  "description": "Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "isPrimaryRenter": {
    "type": "boolean",
    "default": false
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "idNumber": {
    "type": "string",
    "nullable": true
   },
   "guardianName": {
    "type": "string",
    "nullable": true
   },
   "emergencyContact": {
    "type": "string",
    "nullable": true
   },
   "hasSignedWaiver": {
    "type": "boolean",
    "readOnly": true
   },
   "customFields": {
    "type": "object",
    "additionalProperties": true
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
 "ResourceAuditEntry": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_audit",
  "description": "Board 1.10. **Immutable, and it carries the previous value.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "actorId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "action": {
    "type": "string"
   },
   "field": {
    "type": "string",
    "nullable": true
   },
   "previousValue": {
    "nullable": true
   },
   "newValue": {
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "sourceChannel": {
    "type": "string",
    "nullable": true
   },
   "apiOrigin": {
    "type": "string",
    "nullable": true
   },
   "correlationId": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceUtilisation": {
  "type": "object",
  "description": "Board 10.02. **Booked time over available time**, where available knows about schedules, blocks, setup and travel.\n",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "availableMinutes": {
    "type": "integer"
   },
   "bookedMinutes": {
    "type": "integer"
   },
   "blockedMinutes": {
    "type": "integer"
   },
   "utilisationPercent": {
    "type": "number"
   },
   "bookingCount": {
    "type": "integer"
   }
  }
 }
}
```
