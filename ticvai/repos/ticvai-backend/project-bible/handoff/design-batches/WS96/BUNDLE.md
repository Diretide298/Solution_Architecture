# WS96 — Rental Management board 9

**10 screens · 17 operations · 20 schemas · 7 permissions**

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
  `ASSET_MANAGE, ASSET_VIEW, INSPECTION_SUBMIT, MAINTENANCE_EXECUTE, WORK_ORDER_MANAGE, WORK_ORDER_VERIFY, WORK_ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-574` | Maintenance Command Center | commandCentre | 2 | 0 | — |
| `BO-575` | Maintenance Rule & Service Plan Configuration | configEditor | 3 | 0 | — |
| `BO-576` | Maintenance Calendar & Scheduling | configEditor | 2 | 0 | — |
| `BO-577` | Maintenance Work Order | listDetail | 5 | 0 | — |
| `BO-578` | Technician Repair Workspace | listDetail | 3 | 0 | — |
| `BO-579` | Parts, Cost & Maintenance Expense Tracking | listDetail | 1 | 0 | — |
| `BO-580` | Asset Maintenance History & Lifecycle | listDetail | 1 | 0 | — |
| `BO-581` | Return-to-Service Inspection & Approval | listDetail | 2 | 0 | — |
| `BO-582` | Asset Retirement, Write-Off & Replacement Recommendation | listDetail | 2 | 0 | — |
| `BO-583` | Maintenance Intelligence & Predictive AI | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-578, BO-579, BO-580, BO-581, BO-582, BO-583 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-574",
  "name": "Maintenance Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "1",
   "page": 109
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/maintenance-command-center-bo-574",
   "component": "apps/venue-management-web/src/routes/rentals/MaintenanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-575",
    "BO-576",
    "BO-577",
    "BO-578",
    "BO-579",
    "BO-580",
    "BO-581",
    "BO-582",
    "BO-583"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-575",
     "trigger": "Maintenance Rule & Service Plan Configuration",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "BO-576",
     "trigger": "Maintenance Calendar & Scheduling",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-577",
     "trigger": "Maintenance Work Order",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "carries": [
      "workOrderId"
     ]
    },
    {
     "to": "BO-578",
     "trigger": "Technician Repair Workspace",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "carries": [
      "workOrderId"
     ]
    },
    {
     "to": "BO-579",
     "trigger": "Parts, Cost & Maintenance Expense Tracking",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "carries": [
      "workOrderId"
     ]
    },
    {
     "to": "BO-580",
     "trigger": "Asset Maintenance History & Lifecycle",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "carries": [
      "assetId"
     ]
    },
    {
     "to": "BO-581",
     "trigger": "Return-to-Service Inspection & Approval",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "carries": [
      "workOrderId"
     ]
    },
    {
     "to": "BO-582",
     "trigger": "Asset Retirement, Write-Off & Replacement Recommendation",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "carries": [
      "assetId"
     ]
    },
    {
     "to": "BO-583",
     "trigger": "Maintenance Intelligence & Predictive AI",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide maintenance teams and rental management with a real-time view of rental asset health and maintenance workload.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search maintenance",
       "provenance": "pack Rental_Management.pdf, page 109 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Location",
        "Product",
        "Asset",
        "Maintenance Type",
        "Priority",
        "Technician",
        "Status",
        "Due Date"
       ],
       "notes": "The pack filters this screen by venue, location, product, asset, maintenance type, priority and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 109 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Assets Under Maintenance",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Inspection Required",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Preventive Maintenance Due",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Overdue Maintenance",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Corrective Repairs",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Damage Repairs",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Awaiting Parts",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Ready for Return to Service",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Downtime",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Maintenance Alerts",
       "provenance": "pack Rental_Management.pdf, page 109 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The maintenance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the maintenance untouched.",
   "emptyFirstRun": "No maintenance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the maintenance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkOrders",
    "contract": "maintenance",
    "purpose": "Open work orders",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getDueMaintenance",
    "contract": "maintenance",
    "purpose": "What is due",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Assets Under Maintenance",
    "Inspection Required",
    "Preventive Maintenance Due",
    "Overdue Maintenance",
    "Corrective Repairs",
    "Damage Repairs"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-574",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-574"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 109. 0 of 9 labels bound to a contract property; 19 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-575",
  "name": "Maintenance Rule & Service Plan Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "2",
   "page": 110
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/maintenance-rule-service-plan-configuration-bo-575",
   "component": "apps/venue-management-web/src/routes/rentals/MaintenanceRuleServicePlanConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define when different rental products/assets require preventive maintenance. This is important because maintenance should not depend only on staff manually noticing a problem.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Product / Category",
       "provenance": "pack Rental_Management.pdf, page 110 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maintenance Type",
       "provenance": "pack Rental_Management.pdf, page 110 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Trigger",
       "provenance": "pack Rental_Management.pdf, page 110 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Service Checklist",
       "provenance": "pack Rental_Management.pdf, page 110 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Estimated Duration",
       "provenance": "pack Rental_Management.pdf, page 110 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Required Technician Skill",
       "provenance": "pack Rental_Management.pdf, page 110 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Required Approval",
       "provenance": "pack Rental_Management.pdf, page 110 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Post-Maintenance Inspection",
       "provenance": "pack Rental_Management.pdf, page 110 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The maintenance rule service configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the maintenance rule service untouched.",
   "emptyFirstRun": "No maintenance rule service configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listMaintenancePlans",
    "contract": "maintenance",
    "purpose": "Service plans",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createMaintenancePlan",
    "contract": "maintenance",
    "purpose": "Define a plan",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateMaintenancePlan",
    "contract": "maintenance",
    "purpose": "Change it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-575",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-575"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 110. 0 of 0 labels bound to a contract property; 8 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "planId",
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
  "id": "BO-576",
  "name": "Maintenance Calendar & Scheduling",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "3",
   "page": 111
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/maintenance-calendar-scheduling-bo-576",
   "component": "apps/venue-management-web/src/routes/rentals/MaintenanceCalendarScheduling.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Plan preventive and corrective maintenance while understanding its effect on rental capacity. The original requirement specifically calls for scheduled maintenance periods.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Asset",
       "provenance": "pack Rental_Management.pdf, page 111 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maintenance Type",
       "provenance": "pack Rental_Management.pdf, page 111 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Start Date/Time",
       "provenance": "pack Rental_Management.pdf, page 111 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expected Completion",
       "provenance": "pack Rental_Management.pdf, page 111 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Technician",
       "provenance": "pack Rental_Management.pdf, page 111 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Workshop/Location",
       "provenance": "pack Rental_Management.pdf, page 111 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Rental_Management.pdf, page 111 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The maintenance calendar scheduling configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the maintenance calendar scheduling untouched.",
   "emptyFirstRun": "No maintenance calendar scheduling configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getDueMaintenance",
    "contract": "maintenance",
    "purpose": "The maintenance calendar",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createWorkOrder",
    "contract": "maintenance",
    "purpose": "Schedule a job",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWorkOrders",
     "getDueMaintenance"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-576",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-576"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 111. 0 of 0 labels bound to a contract property; 7 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-577",
  "name": "Maintenance Work Order",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "4",
   "page": 112
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/maintenance-work-order-bo-577",
   "component": "apps/venue-management-web/src/routes/rentals/MaintenanceWorkOrder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create and manage the actual repair/service job.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 112"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 112"
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
       "impliedBy": "listWorkOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getWorkOrder",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createWorkOrder",
       "label": "Create work order",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createWorkOrder"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The maintenance work order list.",
   "error": "Could not load. Names which read failed and leaves the maintenance work order untouched.",
   "emptyFirstRun": "No maintenance work order yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the maintenance work order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkOrders",
    "contract": "maintenance",
    "purpose": "List work orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWorkOrder",
    "contract": "maintenance",
    "purpose": "The job",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createWorkOrder",
    "contract": "maintenance",
    "purpose": "Raise one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWorkOrders",
     "getDueMaintenance"
    ]
   },
   {
    "operationId": "updateWorkOrder",
    "contract": "maintenance",
    "purpose": "Change it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWorkOrder",
     "listWorkOrders"
    ]
   },
   {
    "operationId": "attachWorkOrderEvidence",
    "contract": "maintenance",
    "purpose": "Photos and documents",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-577",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-577"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 112. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "workOrderId",
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
  "id": "BO-578",
  "name": "Technician Repair Workspace",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "5",
   "page": 113
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/technician-repair-workspace-bo-578",
   "component": "apps/venue-management-web/src/routes/rentals/TechnicianRepairWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the technician with a focused operational screen for executing maintenance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 113"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 113"
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
       "impliedBy": "startWorkOrder",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "startWorkOrder"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The technician repair list.",
   "error": "Could not load. Names which read failed and leaves the technician repair untouched.",
   "emptyFirstRun": "No technician repair yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the technician repair are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "startWorkOrder",
    "contract": "maintenance",
    "purpose": "Begin the repair",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWorkOrder",
     "listWorkOrders"
    ]
   },
   {
    "operationId": "recordWorkOrderTime",
    "contract": "maintenance",
    "purpose": "Time on the job. Pausing the timer with pause reason Other requires a note — the form will not send without it and the server refuses 400 (decided 28 September, audit R222)",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "completeWorkOrder",
    "contract": "maintenance",
    "purpose": "Finish it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWorkOrder",
     "listWorkOrders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-578",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-578"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 113. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "workOrderId",
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
  "id": "BO-579",
  "name": "Parts, Cost & Maintenance Expense Tracking",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "6",
   "page": 114
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/parts-cost-maintenance-expense-tracking-bo-579",
   "component": "apps/venue-management-web/src/routes/rentals/PartsCostMaintenanceExpenseTracking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Capture the operational cost associated with maintaining rental equipment. This should integrate with the broader Inventory/Procurement and Finance modules rather than recreate them.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 114"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 114"
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
       "impliedBy": "recordWorkOrderParts",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordWorkOrderParts"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The parts cost maintenance list.",
   "error": "Could not load. Names which read failed and leaves the parts cost maintenance untouched.",
   "emptyFirstRun": "No parts cost maintenance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the parts cost maintenance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordWorkOrderParts",
    "contract": "maintenance",
    "purpose": "Parts and cost",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-579",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-579"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 114. 0 of 0 labels bound to a contract property; 0 of 7 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "workOrderId",
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
  "id": "BO-580",
  "name": "Asset Maintenance History & Lifecycle",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "7",
   "page": 115
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/asset-maintenance-history-lifecycle-bo-580",
   "component": "apps/venue-management-web/src/routes/rentals/AssetMaintenanceHistoryLifecycle.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the complete maintenance history of an individual serialized rental asset. The original requirement specifically requires maintenance history tracking.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 115"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 115"
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
       "impliedBy": "getAssetHistory",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset maintenance history list.",
   "error": "Could not load. Names which read failed and leaves the asset maintenance history untouched.",
   "emptyFirstRun": "No asset maintenance history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset maintenance history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAssetHistory",
    "contract": "maintenance",
    "purpose": "Its life so far",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-580",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-580"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 115. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-581",
  "name": "Return-to-Service Inspection & Approval",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "8",
   "page": 116
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/return-to-service-inspection-approval-bo-581",
   "component": "apps/venue-management-web/src/routes/rentals/ReturnToServiceInspectionApproval.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Ensure repaired equipment does not automatically become rentable when a technician clicks “Repair Complete.” This is one of the most important controls in Board 9.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 116"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 116"
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
       "impliedBy": "submitInspection",
       "label": "Submit inspection",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "submitInspection"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The return-to-service inspection approval list.",
   "error": "Could not load. Names which read failed and leaves the return-to-service inspection approval untouched.",
   "emptyFirstRun": "No return-to-service inspection approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the return-to-service inspection approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "submitInspection",
    "contract": "maintenance",
    "purpose": "Return-to-service inspection",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "verifyWorkOrder",
    "contract": "maintenance",
    "purpose": "Approve the return to service",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWorkOrder",
     "listWorkOrders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-581",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-581"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 116. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "workOrderId",
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
  "id": "BO-582",
  "name": "Asset Retirement, Write-Off & Replacement Recommendation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "9",
   "page": 117
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/asset-retirement-write-off-replacement-recommendation-bo-582",
   "component": "apps/venue-management-web/src/routes/rentals/AssetRetirementWriteOffReplacementRecommendation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage assets that should no longer remain in the active rental fleet.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 117"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 117"
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
       "impliedBy": "getAssetHistory",
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
   "loading": "The asset retirement write-off list.",
   "error": "Could not load. Names which read failed and leaves the asset retirement write-off untouched.",
   "emptyFirstRun": "No asset retirement write-off yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset retirement write-off are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAssetStatus",
    "contract": "maintenance",
    "purpose": "Retire or write off",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAsset",
     "listAssets"
    ]
   },
   {
    "operationId": "getAssetHistory",
    "contract": "maintenance",
    "purpose": "The case for retiring it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-582",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-582"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 117. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-583",
  "name": "Maintenance Intelligence & Predictive AI",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "9",
   "number": "10",
   "page": 118
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/maintenance-intelligence-predictive-ai-bo-583",
   "component": "apps/venue-management-web/src/routes/rentals/MaintenanceIntelligencePredictiveAi.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-574"
   ],
   "exitTo": [
    "BO-574"
   ],
   "transitions": [
    {
     "to": "BO-574",
     "trigger": "Back to Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Use AI to move TICVAI from reactive maintenance toward predictive maintenance. This is where I recommend making the module significantly stronger than the original matrix.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 118 §Display"
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
       "label": "Every maintenance intelligence predictive",
       "columns": [
        "Assets at Risk",
        "Predicted Failures",
        "Upcoming Preventive Maintenance",
        "Repeat Failures",
        "High Maintenance Cost Assets",
        "Downtime by Product",
        "Maintenance Impact on Availability",
        "Mean Time Between Failures",
        "Mean Time to Repair"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 118 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected maintenance intelligence predictive",
       "bindsTo": null,
       "columns": [
        "Assets at Risk",
        "Predicted Failures",
        "Upcoming Preventive Maintenance",
        "Repeat Failures",
        "High Maintenance Cost Assets",
        "Downtime by Product",
        "Maintenance Impact on Availability",
        "Mean Time Between Failures",
        "Mean Time to Repair"
       ],
       "notes": "The pack groups this record's detail under its own headings: “BIKE-018”, “Instead of simply saying”, “Every 30 Days”, “Every 50 Rentals”, “Every 100 Rental Hours”, “Whichever Happens First”.",
       "provenance": "pack Rental_Management.pdf, page 118 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The maintenance intelligence predictive list.",
   "error": "Could not load. Names which read failed and leaves the maintenance intelligence predictive untouched.",
   "emptyFirstRun": "No maintenance intelligence predictive yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the maintenance intelligence predictive are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getDueMaintenance",
    "contract": "maintenance",
    "purpose": "Predictive maintenance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Assets at Risk",
    "Predicted Failures",
    "Upcoming Preventive Maintenance",
    "Repeat Failures",
    "High Maintenance Cost Assets",
    "Downtime by Product"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-583",
   "workshopBoard": "wireframes/WS124 Rental Management Board 9.dc.html#bo-583"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 118. 0 of 9 labels bound to a contract property; 9 of 99 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "attachWorkOrderEvidence": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/attachments",
  "contract": "maintenance",
  "summary": "Photo, video, document, note or signature",
  "permission": "MAINTENANCE_EXECUTE",
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
  "responds": "WorkOrderAttachment"
 },
 "completeWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/complete",
  "contract": "maintenance",
  "summary": "Complete a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
 },
 "createMaintenancePlan": {
  "method": "POST",
  "path": "/maintenance-plans",
  "contract": "maintenance",
  "summary": "Create a planned maintenance schedule",
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
  "requestBody": "MaintenancePlan",
  "responds": "MaintenancePlan"
 },
 "createWorkOrder": {
  "method": "POST",
  "path": "/work-orders",
  "contract": "maintenance",
  "summary": "Raise a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "requestBody": "CreateWorkOrderRequest",
  "responds": "WorkOrder"
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
 "getDueMaintenance": {
  "method": "GET",
  "path": "/maintenance-plans/due",
  "contract": "maintenance",
  "summary": "Planned tasks due or overdue",
  "permission": "ASSET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "withinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DueMaintenanceTask"
 },
 "getWorkOrder": {
  "method": "GET",
  "path": "/work-orders/{workOrderId}",
  "contract": "maintenance",
  "summary": "Read a work order",
  "permission": "WORK_ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WorkOrderDetail"
 },
 "listMaintenancePlans": {
  "method": "GET",
  "path": "/maintenance-plans",
  "contract": "maintenance",
  "summary": "List planned maintenance schedules",
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
 "listWorkOrders": {
  "method": "GET",
  "path": "/work-orders",
  "contract": "maintenance",
  "summary": "List work orders",
  "permission": "WORK_ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToPrincipalId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "priority",
    "in": "query",
    "required": null
   },
   {
    "name": "assetId",
    "in": "query",
    "required": null
   },
   {
    "name": "overdueOnly",
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
 "recordWorkOrderParts": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/parts",
  "contract": "maintenance",
  "summary": "Record parts consumed",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrderDetail"
 },
 "recordWorkOrderTime": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/time",
  "contract": "maintenance",
  "summary": "Start, pause or stop work",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
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
 "startWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/start",
  "contract": "maintenance",
  "summary": "Work has begun",
  "permission": "MAINTENANCE_EXECUTE",
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
  "responds": "WorkOrder"
 },
 "submitInspection": {
  "method": "POST",
  "path": "/inspections",
  "contract": "maintenance",
  "summary": "Submit a completed inspection",
  "permission": "INSPECTION_SUBMIT",
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
  "requestBody": "SubmitInspectionRequest",
  "responds": "InspectionResult"
 },
 "updateMaintenancePlan": {
  "method": "PATCH",
  "path": "/maintenance-plans/{planId}",
  "contract": "maintenance",
  "summary": "Amend or suspend a plan",
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
  "responds": "MaintenancePlan"
 },
 "updateWorkOrder": {
  "method": "PATCH",
  "path": "/work-orders/{workOrderId}",
  "contract": "maintenance",
  "summary": "Assign, reprioritise or amend",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
 },
 "verifyWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/verify",
  "contract": "maintenance",
  "summary": "Supervisor verification",
  "permission": "WORK_ORDER_VERIFY",
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
  "responds": "WorkOrder"
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
 "AssetCriticality": {
  "type": "string",
  "enum": [
   "safetyCritical",
   "revenueCritical",
   "standard",
   "low"
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
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
      "nullable": true
     }
    }
   }
  }
 },
 "CreateWorkOrderRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "title",
   "venueId",
   "priority",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "title": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 5000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderKind"
     }
    ],
    "default": "corrective"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "attachmentRefs": {
    "type": "array",
    "description": "Photo-first. Expected at creation, not added later from memory.",
    "items": {
     "type": "string"
    }
   },
   "takeAssetOutOfService": {
    "type": "boolean",
    "default": false,
    "description": "Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DueMaintenanceTask": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "planId",
   "assetId",
   "assetName",
   "dueAt",
   "isOverdue",
   "criticality"
  ],
  "properties": {
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planName": {
    "type": "string"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "assetName": {
    "type": "string"
   },
   "criticality": {
    "$ref": "#/components/schemas/AssetCriticality"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "isOverdue": {
    "type": "boolean"
   },
   "daysOverdue": {
    "type": "integer"
   },
   "triggeredBy": {
    "type": "string",
    "enum": [
     "interval",
     "usage"
    ]
   },
   "workOrderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   }
  }
 },
 "Inspection": {
  "x-ticvai-persistence": "maintenance.inspection",
  "type": "object",
  "required": [
   "id",
   "templateId",
   "venueId",
   "outcome",
   "performedByPrincipalId",
   "performedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "templateName": {
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
   "outcome": {
    "$ref": "#/components/schemas/InspectionOutcome"
   },
   "failedItemCount": {
    "type": "integer"
   },
   "failedSafetyCriticalCount": {
    "type": "integer"
   },
   "performedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "An inspection nobody signed is not an inspection."
   },
   "performedAt": {
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
   },
   "retainUntil": {
    "type": "string",
    "format": "date",
    "nullable": true
   }
  }
 },
 "InspectionItem": {
  "x-ticvai-persistence": "maintenance.inspection_item",
  "type": "object",
  "description": "**One answer to one question, which the API has always accepted and never stored.** `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and attachments; the only persistence ever claimed for them was `maintenance.inspection_response`, a table that does not exist.\nSo `maintenance.inspection_template_item` held the questions, `maintenance.inspection` held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was accepted over the wire and dropped** — on a record that takes an asset out of service.\nReturned on `InspectionResult`, not on `Inspection`: `listInspections` returns the latter in a list, and twenty item rows per inspection on a list screen is the wrong trade. The counts stay for exactly that reason.\n",
  "required": [
   "id",
   "inspectionId",
   "itemKey"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "inspectionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "templateItemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Nullable because a template changes and an inspection does not.** An answer recorded against an item that was later removed still has to be readable, so the key below is the durable record and this is the live link.\n"
   },
   "itemKey": {
    "type": "string",
    "maxLength": 120,
    "description": "The template item's `key`, copied at submission and never updated."
   },
   "label": {
    "type": "string",
    "nullable": true,
    "description": "The question as it was asked, copied at submission. **A template reworded next season must not silently reword last season's inspection.**\n"
   },
   "value": {
    "nullable": true,
    "description": "Whatever the item's `kind` calls for — a boolean, a number, a string."
   },
   "passed": {
    "type": "boolean",
    "nullable": true,
    "description": "Null where the item is informational rather than pass or fail."
   },
   "isSafetyCritical": {
    "type": "boolean",
    "default": false,
    "description": "Copied from the template item at submission, for the same reason as `label`: it is what makes `failedSafetyCriticalCount` reproducible, and the template can change.\n"
   },
   "note": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "attachmentAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**A deliberate array, and the same exception as `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer at the moment it was recorded. It is never queried from the other end — nobody asks which inspection items reference a photograph — and it must not change when an asset library is reorganised.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "InspectionResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "inspection",
   "consequences"
  ],
  "properties": {
   "inspection": {
    "$ref": "#/components/schemas/Inspection"
   },
   "items": {
    "type": "array",
    "description": "**The answers, which had nowhere to live until 20 September.** A failed safety-critical item takes an asset out of service and `consequences` below says it happened; this says which check caused it.\n",
    "items": {
     "$ref": "#/components/schemas/InspectionItem"
    }
   },
   "consequences": {
    "type": "object",
    "description": "What the submission triggered. A failed safety-critical item takes the asset out of service without waiting for anyone to decide.\n",
    "properties": {
     "assetTakenOutOfService": {
      "type": "boolean"
     },
     "workOrdersRaised": {
      "type": "array",
      "items": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      }
     },
     "productsSuspended": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "escalatedToPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   }
  }
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
 "ResolutionCode": {
  "type": "string",
  "enum": [
   "repaired",
   "partReplaced",
   "adjusted",
   "cleaned",
   "noFaultFound",
   "referredExternal",
   "replaced",
   "deferred"
  ]
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
 "SubmitInspectionRequest": {
  "x-ticvai-persistence": "maintenance.inspection + maintenance.inspection_item",
  "type": "object",
  "required": [
   "id",
   "templateId",
   "venueId",
   "responses",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "responses": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "key",
      "value"
     ],
     "properties": {
      "key": {
       "type": "string"
      },
      "value": {},
      "passed": {
       "type": "boolean",
       "nullable": true
      },
      "note": {
       "type": "string",
       "maxLength": 1000
      },
      "attachmentRefs": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
 "WorkOrderAttachment": {
  "type": "object",
  "x-ticvai-persistence": "maintenance.work_order_attachment",
  "required": [
   "id",
   "workOrderId",
   "kind",
   "capturedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "workOrderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "kind": {
    "type": "string",
    "enum": [
     "photo",
     "video",
     "document",
     "note",
     "signature"
    ]
   },
   "assetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "text": {
    "type": "string",
    "nullable": true
   },
   "stage": {
    "type": "string",
    "enum": [
     "before",
     "during",
     "after",
     "signOff"
    ],
    "nullable": true
   },
   "capturedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "capturedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time. **Distinct from when it synced** — a photo taken at 09:14 in a basement and uploaded at 11:40 is evidence of the first, not the second.\n"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkOrderDetail": {
  "x-ticvai-persistence": "maintenance.work_order",
  "allOf": [
   {
    "$ref": "#/components/schemas/WorkOrder"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string",
      "nullable": true
     },
     "resolution": {
      "type": "string",
      "nullable": true
     },
     "resolutionCode": {
      "$ref": "#/components/schemas/ResolutionCode"
     },
     "attachmentRefs": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "timeEntries": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "action": {
         "type": "string"
        },
        "principalId": {
         "type": "string",
         "format": "uuid"
        },
        "pauseReason": {
         "type": "string",
         "nullable": true
        },
        "recordedAt": {
         "type": "string",
         "format": "date-time"
        }
       }
      }
     },
     "parts": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "inventoryItemId": {
         "type": "string",
         "format": "uuid"
        },
        "itemName": {
         "type": "string"
        },
        "quantity": {
         "type": "number"
        },
        "cost": {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       }
      }
     },
     "labourCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "partsCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "totalCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money",
      "x-ticvai-column": "net_cost_amount"
     },
     "completedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"
     },
     "followUpRequired": {
      "type": "boolean",
      "default": false
     },
     "followUpNote": {
      "type": "string",
      "maxLength": 1000,
      "nullable": true
     },
     "verificationOutcome": {
      "type": "string",
      "enum": [
       "verified",
       "rejected"
      ],
      "nullable": true,
      "description": "The latest `verifyWorkOrder` outcome."
     },
     "verificationNote": {
      "type": "string",
      "maxLength": 1000,
      "nullable": true
     },
     "verifiedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "verifiedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "cancelReason": {
      "type": "string",
      "enum": [
       "raisedInError",
       "duplicate",
       "superseded",
       "noLongerRequired"
      ],
      "nullable": true
     },
     "cancelNote": {
      "type": "string",
      "maxLength": 300,
      "nullable": true
     },
     "supersededByWorkOrderId": {
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
      "nullable": true,
      "description": "Set by `cancelWorkOrder` where the reason is `superseded`."
     },
     "cancelledAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "closeOutcome": {
      "type": "string",
      "enum": [
       "completedAndVerified",
       "notReproducible",
       "supersededByReplacement",
       "noLongerApplicable",
       "duplicate"
      ],
      "nullable": true
     },
     "closeNote": {
      "type": "string",
      "maxLength": 500,
      "nullable": true
     },
     "duplicateOfWorkOrderId": {
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
      "nullable": true,
      "description": "Set by `closeWorkOrder` where the outcome is `duplicate`."
     },
     "closedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "closedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   }
  ]
 },
 "WorkOrderKind": {
  "type": "string",
  "enum": [
   "corrective",
   "planned",
   "inspectionFollowUp",
   "incidentCorrective",
   "improvement"
  ]
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
 },
 "WorkOrderStatus": {
  "type": "string",
  "enum": [
   "open",
   "assigned",
   "inProgress",
   "paused",
   "awaitingParts",
   "completed",
   "verified",
   "closed",
   "cancelled"
  ]
 }
}
```
