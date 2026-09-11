# WS96 — Rental Management board 9

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
| `BO-574` | Maintenance Command Center | commandCentre | 0 | 0 | — |
| `BO-575` | Maintenance Rule & Service Plan Configuration | configEditor | 0 | 0 | — |
| `BO-576` | Maintenance Calendar & Scheduling | configEditor | 0 | 0 | — |
| `BO-577` | Maintenance Work Order | listDetail | 0 | 0 | — |
| `BO-578` | Technician Repair Workspace | listDetail | 0 | 0 | — |
| `BO-579` | Parts, Cost & Maintenance Expense Tracking | listDetail | 0 | 0 | — |
| `BO-580` | Asset Maintenance History & Lifecycle | listDetail | 0 | 0 | — |
| `BO-581` | Return-to-Service Inspection & Approval | listDetail | 0 | 0 | — |
| `BO-582` | Asset Retirement, Write-Off & Replacement Recommendation | listDetail | 0 | 0 | — |
| `BO-583` | Maintenance Intelligence & Predictive AI | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-577, BO-578, BO-579, BO-580, BO-581, BO-582, BO-583 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-576",
     "trigger": "Maintenance Calendar & Scheduling",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-577",
     "trigger": "Maintenance Work Order",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-578",
     "trigger": "Technician Repair Workspace",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-579",
     "trigger": "Parts, Cost & Maintenance Expense Tracking",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-580",
     "trigger": "Asset Maintenance History & Lifecycle",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-581",
     "trigger": "Return-to-Service Inspection & Approval",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-582",
     "trigger": "Asset Retirement, Write-Off & Replacement Recommendation",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-574"
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-575"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 110. 0 of 0 labels bound to a contract property; 8 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-576"
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
   "regions": []
  },
  "states": {
   "loading": "The maintenance work order list.",
   "error": "Could not load. Names which read failed and leaves the maintenance work order untouched.",
   "emptyFirstRun": "No maintenance work order yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the maintenance work order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-577"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 112. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The technician repair list.",
   "error": "Could not load. Names which read failed and leaves the technician repair untouched.",
   "emptyFirstRun": "No technician repair yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the technician repair are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-578"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 113. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The parts cost maintenance list.",
   "error": "Could not load. Names which read failed and leaves the parts cost maintenance untouched.",
   "emptyFirstRun": "No parts cost maintenance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the parts cost maintenance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-579"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 114. 0 of 0 labels bound to a contract property; 0 of 7 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The asset maintenance history list.",
   "error": "Could not load. Names which read failed and leaves the asset maintenance history untouched.",
   "emptyFirstRun": "No asset maintenance history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset maintenance history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-580"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 115. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The return-to-service inspection approval list.",
   "error": "Could not load. Names which read failed and leaves the return-to-service inspection approval untouched.",
   "emptyFirstRun": "No return-to-service inspection approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the return-to-service inspection approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-581"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 116. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The asset retirement write-off list.",
   "error": "Could not load. Names which read failed and leaves the asset retirement write-off untouched.",
   "emptyFirstRun": "No asset retirement write-off yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset retirement write-off are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-582"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 117. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-583"
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
