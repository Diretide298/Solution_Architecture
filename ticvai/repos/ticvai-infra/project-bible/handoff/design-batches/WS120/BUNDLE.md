# WS120 — AI Forecasting and Predictive Intelligence board 2

**10 screens · 9 operations · 14 schemas · 3 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `AI_CONFIGURE, AI_USE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-509` | Operational Forecasting Command Center | commandCentre | 2 | 0 | — |
| `ADM-510` | Capacity & Occupancy Forecast | listDetail | 4 | 0 | — |
| `ADM-511` | Attraction Utilization & Queue Forecast | listDetail | 3 | 0 | — |
| `ADM-512` | Entry, Access & Guest Flow Forecast | listDetail | 2 | 0 | — |
| `ADM-513` | Workforce Demand & Staffing Forecast | listDetail | 3 | 0 | — |
| `ADM-514` | POS, Kiosk & Frontline Service Forecast | listDetail | 2 | 0 | — |
| `ADM-515` | F&B, Retail & Inventory Demand Forecast | listDetail | 2 | 0 | — |
| `ADM-516` | Resource, Equipment & Facility Requirement Forecast | listDetail | 2 | 0 | — |
| `ADM-517` | Operational Scenario & Readiness Simulator | commandCentre | 3 | 0 | — |
| `ADM-518` | Operational Forecast Review, Recommendations & Handover | listDetail | 2 | 0 | — |

## Thin screens in this batch

**ADM-510, ADM-511, ADM-512, ADM-513, ADM-514, ADM-515, ADM-516 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-509",
  "name": "Operational Forecasting Command Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "1",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/operational-forecasting-command-center-adm-509",
   "component": "apps/ticvai-web/src/routes/analytics/OperationalForecastingCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-510",
    "ADM-511",
    "ADM-512",
    "ADM-513",
    "ADM-514",
    "ADM-515",
    "ADM-516",
    "ADM-517",
    "ADM-518"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-510",
     "trigger": "Capacity & Occupancy Forecast",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-511",
     "trigger": "Attraction Utilization & Queue Forecast",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-512",
     "trigger": "Entry, Access & Guest Flow Forecast",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-513",
     "trigger": "Workforce Demand & Staffing Forecast",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-514",
     "trigger": "POS, Kiosk & Frontline Service Forecast",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-515",
     "trigger": "F&B, Retail & Inventory Demand Forecast",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-516",
     "trigger": "Resource, Equipment & Facility Requirement Forecast",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-517",
     "trigger": "Operational Scenario & Readiness Simulator",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-518",
     "trigger": "Operational Forecast Review, Recommendations & Handover",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide operations management with one central view of future operational pressure and predicted resource requirements.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search operational forecasting",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Date",
        "Time",
        "Zone",
        "Attraction",
        "Department",
        "Forecast Scenario"
       ],
       "notes": "The pack filters this screen by tenant, venue, date, time, zone, attraction and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Forecast Attendance",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Peak In-Venue Population",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Occupancy",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "High-Pressure Periods",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Attractions at Risk",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Queue Pressure Alerts",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Required Workforce",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Workforce Gap",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Required POS Capacity",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "F&B Demand Index",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Inventory Risk Items",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Operational Readiness Score",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 32 §Header KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational forecasting list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the operational forecasting untouched.",
   "emptyFirstRun": "No operational forecasting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational forecasting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-509",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-509"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 32. 0 of 8 labels bound to a contract property; 20 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-510",
  "name": "Capacity & Occupancy Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "2",
   "page": 34
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/capacity-occupancy-forecast-adm-510",
   "component": "apps/ticvai-web/src/routes/analytics/CapacityOccupancyForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Translate forecast attendance into predicted occupancy and capacity pressure across the venue.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 34"
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
       "impliedBy": "listOperationalRequirements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "configureAnomalyDetector",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "configureAnomalyDetector"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity occupancy forecast list.",
   "error": "Could not load. Names which read failed and leaves the capacity occupancy forecast untouched.",
   "emptyFirstRun": "No capacity occupancy forecast yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the capacity occupancy forecast are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "configureAnomalyDetector",
    "contract": "ai",
    "purpose": "Set an alert when the forecast crosses a threshold (e.g. attendance p50 above N, occupancy above % of capacity)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiInsights",
    "contract": "ai",
    "purpose": "Forecast threshold alerts (kind forecastThreshold)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-510",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-510"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "detectorKey",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-511",
  "name": "Attraction Utilization & Queue Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "3",
   "page": 36
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/attraction-utilization-queue-forecast-adm-511",
   "component": "apps/ticvai-web/src/routes/analytics/AttractionUtilizationQueueForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Predict demand, utilization and queue pressure for rides, attractions, experiences and service points.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 36"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 36"
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
       "impliedBy": "listOperationalRequirements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "requestSuggestion",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "requestSuggestion"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attraction utilization queue list.",
   "error": "Could not load. Names which read failed and leaves the attraction utilization queue untouched.",
   "emptyFirstRun": "No attraction utilization queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attraction utilization queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "Queue-balancing suggestion (kind queueBalancing): return-slot allocation and redirection",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-511",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-511"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-512",
  "name": "Entry, Access & Guest Flow Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "4",
   "page": 37
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/entry-access-guest-flow-forecast-adm-512",
   "component": "apps/ticvai-web/src/routes/analytics/EntryAccessGuestFlowForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Predict guest arrival, admission, exit and movement pressure across gates and venue zones.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 37"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 37"
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
       "impliedBy": "listOperationalRequirements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entry access guest list.",
   "error": "Could not load. Names which read failed and leaves the entry access guest untouched.",
   "emptyFirstRun": "No entry access guest yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entry access guest are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-512",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-512"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 0 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-513",
  "name": "Workforce Demand & Staffing Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "5",
   "page": 38
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/workforce-demand-staffing-forecast-adm-513",
   "component": "apps/ticvai-web/src/routes/analytics/WorkforceDemandStaffingForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Translate predicted operational demand into required staffing levels.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 38 §Show"
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
       "label": "Every workforce demand staffing",
       "columns": [
        "Required Staff",
        "Currently Scheduled",
        "Staffing Drivers",
        "Gate Staff Requirement",
        "Forecast arrival volume",
        "Gate throughput",
        "Group arrivals",
        "Credential mix",
        "Manual validation rate"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 38 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected workforce demand staffing",
       "bindsTo": null,
       "columns": [
        "Required Staff",
        "Currently Scheduled",
        "Staffing Drivers",
        "Gate Staff Requirement",
        "Forecast arrival volume",
        "Gate throughput",
        "Group arrivals",
        "Credential mix",
        "Manual validation rate"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Cashiers 16 21 -5 High”, “Role Productivity”, “Skills & Certification”.",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 38 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workforce demand staffing list.",
   "error": "Could not load. Names which read failed and leaves the workforce demand staffing untouched.",
   "emptyFirstRun": "No workforce demand staffing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workforce demand staffing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getStaffingCoverage",
    "contract": "workforce",
    "purpose": "Workforce demand and staffing forecast against rostered staff (basis=forecastRequirement)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Required Staff",
    "Currently Scheduled",
    "Staffing Drivers",
    "Gate Staff Requirement",
    "Forecast arrival volume",
    "Gate throughput"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-513",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-513"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 38. 0 of 9 labels bound to a contract property; 9 of 54 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-514",
  "name": "POS, Kiosk & Frontline Service Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "6",
   "page": 40
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/pos-kiosk-frontline-service-forecast-adm-514",
   "component": "apps/ticvai-web/src/routes/analytics/PosKioskFrontlineServiceForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast) and no metric row",
  "purpose": "Predict the number of active selling/service points required to handle expected transaction volume and maintain acceptable service levels.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 40 §Forecast"
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
       "label": "Every pos kiosk frontline",
       "columns": [
        "POS Counters",
        "Flying POS",
        "Ticket Windows",
        "Kiosks",
        "Guest Service Desks",
        "Membership Counters",
        "F&B POS",
        "Retail POS"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 40 §Forecast"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pos kiosk frontline",
       "bindsTo": null,
       "columns": [
        "POS Counters",
        "Flying POS",
        "Ticket Windows",
        "Kiosks",
        "Guest Service Desks",
        "Membership Counters",
        "F&B POS",
        "Retail POS"
       ],
       "notes": null,
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 40 §Forecast"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pos kiosk frontline list.",
   "error": "Could not load. Names which read failed and leaves the pos kiosk frontline untouched.",
   "emptyFirstRun": "No pos kiosk frontline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pos kiosk frontline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "POS Counters",
    "Flying POS",
    "Ticket Windows",
    "Kiosks",
    "Guest Service Desks",
    "Membership Counters"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-514",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-514"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 40. 0 of 8 labels bound to a contract property; 8 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-515",
  "name": "F&B, Retail & Inventory Demand Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "7",
   "page": 41
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/f-b-retail-inventory-demand-forecast-adm-515",
   "component": "apps/ticvai-web/src/routes/analytics/FBRetailInventoryDemandForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Translate visitor forecasts into expected F&B, retail and stock demand. This screen should forecast operational requirements without replacing the detailed F&B/Retail/Inventory modules already designed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 41"
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
       "impliedBy": "listOperationalRequirements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retail inventory demand list.",
   "error": "Could not load. Names which read failed and leaves the retail inventory demand untouched.",
   "emptyFirstRun": "No retail inventory demand yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the retail inventory demand are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-515",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-515"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-516",
  "name": "Resource, Equipment & Facility Requirement Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "8",
   "page": 42
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/resource-equipment-facility-requirement-forecast-adm-516",
   "component": "apps/ticvai-web/src/routes/analytics/ResourceEquipmentFacilityRequirementForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Predict non-workforce operational resources required to support expected visitor demand.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 42"
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
       "impliedBy": "listOperationalRequirements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource equipment facility list.",
   "error": "Could not load. Names which read failed and leaves the resource equipment facility untouched.",
   "emptyFirstRun": "No resource equipment facility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource equipment facility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-516",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-516"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-517",
  "name": "Operational Scenario & Readiness Simulator",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "9",
   "page": 44
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/operational-scenario-readiness-simulator-adm-517",
   "component": "apps/ticvai-web/src/routes/analytics/OperationalScenarioReadinessSimulator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Metric Baseline A B C) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow management to test operational alternatives before changing real configurations.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Readiness 87% 93% 90% 91%",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 44 §Metric Baseline A B C"
      },
      {
       "kind": "metricTile",
       "label": "Workforce Gap 18 0 18 18",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 44 §Metric Baseline A B C"
      },
      {
       "kind": "metricTile",
       "label": "Avg Queue 26m 24m 25m 19m",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 44 §Metric Baseline A B C"
      },
      {
       "kind": "metricTile",
       "label": "POS Wait 17m 16m 7m 16m",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 44 §Metric Baseline A B C"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational scenario readiness list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the operational scenario readiness untouched.",
   "emptyFirstRun": "No operational scenario readiness yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational scenario readiness are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createForecastScenario",
    "contract": "ai",
    "purpose": "Run a what-if",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "compareForecastScenarios",
    "contract": "ai",
    "purpose": "Compare scenarios",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-517",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-517"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 44. 0 of 0 labels bound to a contract property; 4 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-518",
  "name": "Operational Forecast Review, Recommendations & Handover",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "2",
   "number": "10",
   "page": 45
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/operational-forecast-review-recommendations-handover-adm-518",
   "component": "apps/ticvai-web/src/routes/analytics/OperationalForecastReviewRecommendationsHandover.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-509"
   ],
   "exitTo": [
    "ADM-509"
   ],
   "transitions": [
    {
     "to": "ADM-509",
     "trigger": "Back to Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Consolidate forecast findings into a controlled operational readiness plan and hand recommendations to the appropriate TICVAI modules. This is the final screen of the Forecasting module.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 20 actions on this screen and the screen declares 0 operations.** Unserved: Critical Board 1 → Board 2 Architecture, BOARD 1, ATTENDANCE, DEMAND & REVENUE FORECASTING, ├── Attendance, ├── Arrival Pattern, ├── Product Demand, ├── Timeslot Demand, ├── Channel Demand …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45"
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
       "label": "Critical Board 1 → Board 2 Architecture",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "BOARD 1",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "ATTENDANCE, DEMAND & REVENUE FORECASTING",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "├── Attendance",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "├── Arrival Pattern",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "├── Product Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "├── Timeslot Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "├── Channel Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 45 §Actions"
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
   "loading": "The operational forecast review list.",
   "error": "Could not load. Names which read failed and leaves the operational forecast review untouched.",
   "emptyFirstRun": "No operational forecast review yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational forecast review are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOperationalRequirements",
    "contract": "ai",
    "purpose": "Requirements derived from the forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideOperationalRequirement",
    "contract": "ai",
    "purpose": "Accept, modify or reject a requirement",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-518",
   "workshopBoard": "wireframes/WS13 AI Forecasting and Predictive Intelligence Board 2.dc.html#adm-518"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 45. 0 of 0 labels bound to a contract property; 20 of 172 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "requirementId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
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
 "compareForecastScenarios": {
  "method": "POST",
  "path": "/forecast-scenarios/compare",
  "contract": "ai",
  "summary": "Compare scenarios",
  "permission": "AI_USE",
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
  "responds": "AiScenarioComparison"
 },
 "configureAnomalyDetector": {
  "method": "PUT",
  "path": "/anomaly-detectors/{detectorKey}",
  "contract": "ai",
  "summary": "Set up anomaly detection on a KPI",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "AiAnomalyDetector",
  "responds": "AiAnomalyDetector"
 },
 "createForecastScenario": {
  "method": "POST",
  "path": "/forecast-scenarios",
  "contract": "ai",
  "summary": "Run a what-if",
  "permission": "AI_USE",
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
  "requestBody": "AiForecastScenario",
  "responds": null
 },
 "decideOperationalRequirement": {
  "method": "POST",
  "path": "/operational-requirements/{requirementId}/decide",
  "contract": "ai",
  "summary": "Accept, modify or reject a requirement",
  "permission": "AI_USE",
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
  "responds": "AiOperationalRequirement"
 },
 "getForecast": {
  "method": "GET",
  "path": "/forecasts",
  "contract": "ai",
  "summary": "Forecast values",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "definitionKey",
    "in": "query",
    "required": true
   },
   {
    "name": "versionId",
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
   },
   {
    "name": "dimensionKey",
    "in": "query",
    "required": null
   },
   {
    "name": "scenarioId",
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
 "getStaffingCoverage": {
  "method": "GET",
  "path": "/staffing-coverage",
  "contract": "workforce",
  "summary": "Where the rota is short, and by how much",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
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
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "basis",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "StaffingCoverage"
 },
 "listAiInsights": {
  "method": "GET",
  "path": "/insights",
  "contract": "ai",
  "summary": "Insights and anomalies",
  "permission": "AI_USE",
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
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "priority",
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
  "responds": "Page"
 },
 "listOperationalRequirements": {
  "method": "GET",
  "path": "/operational-requirements",
  "contract": "ai",
  "summary": "Requirements derived from the forecast",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
   },
   {
    "name": "versionId",
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
 "requestSuggestion": {
  "method": "POST",
  "path": "/ai/suggestions",
  "contract": "ai",
  "summary": "Ask for an answer, however it is currently produced",
  "permission": "AI_USE",
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
  "responds": "Suggestion"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiAnomalyDetector": {
  "type": "object",
  "x-ticvai-persistence": "ai.anomaly_detector",
  "description": "**An anomaly detector on one KPI** (C9, AIP-080..095). Configured thresholds on day one; a seasonal robust baseline (median/MAD) and peer comparison across venues as history builds. Detects **aggregate** deviations; actor-level patterns belong to risk, and both share one correlation key (AIP-090).",
  "required": [
   "detectorKey",
   "method"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "detectorKey": {
    "type": "string"
   },
   "source": {
    "type": "string",
    "enum": [
     "metric",
     "forecast",
     "deviceHealth"
    ],
    "default": "metric",
    "description": "What is watched (29 September, build): a semantic-layer KPI, a published forecast (8.2.20, 8.2.41), or device status events (8.9.9)."
   },
   "metricKey": {
    "type": "string",
    "nullable": true,
    "description": "A metric of the semantic layer (Reporting KPI). Required where `source` is `metric`."
   },
   "forecastSource": {
    "type": "object",
    "nullable": true,
    "description": "Required where `source` is `forecast`; `method` is then `threshold`.",
    "required": [
     "definitionKey",
     "comparator",
     "threshold"
    ],
    "properties": {
     "definitionKey": {
      "type": "string"
     },
     "dimensionKey": {
      "type": "string",
      "nullable": true
     },
     "percentile": {
      "type": "string",
      "enum": [
       "p10",
       "p50",
       "p90"
      ],
      "default": "p50"
     },
     "comparator": {
      "type": "string",
      "enum": [
       "above",
       "atOrAbove",
       "below",
       "atOrBelow"
      ]
     },
     "threshold": {
      "type": "number"
     },
     "thresholdKind": {
      "type": "string",
      "enum": [
       "absolute",
       "percentOfCapacity"
      ],
      "default": "absolute",
      "description": "`percentOfCapacity` compares with the period's capacity (occupancy, 8.2.41)."
     },
     "horizonDays": {
      "type": "integer",
      "minimum": 1,
      "maximum": 365,
      "nullable": true,
      "description": "Only points this many days ahead are compared. Null means the whole horizon."
     }
    }
   },
   "deviceHealthSource": {
    "type": "object",
    "nullable": true,
    "description": "Required where `source` is `deviceHealth`.",
    "properties": {
     "deviceKinds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "DeviceKind values; empty means every kind."
     },
     "failureRatePercent": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
     },
     "windowMinutes": {
      "type": "integer",
      "minimum": 5,
      "maximum": 1440,
      "default": 60
     }
    }
   },
   "method": {
    "type": "string",
    "enum": [
     "threshold",
     "seasonalRobustZ",
     "peerComparison",
     "model"
    ]
   },
   "thresholds": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "sensitivity": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high"
    ],
    "default": "medium"
   },
   "dimensions": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "cadence": {
    "type": "string",
    "enum": [
     "hourly",
     "daily"
    ]
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "falseAlarmRate": {
    "type": "number",
    "nullable": true,
    "readOnly": true,
    "description": "Share of its insights rejected over 90 days. The number that decides whether a model is worth it."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiEvidenceItemList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "The evidence of one decision record, stored with it.",
  "items": {
   "$ref": "#/components/schemas/AiEvidenceItem"
  }
 },
 "AiForecastPoint": {
  "type": "object",
  "x-ticvai-persistence": "ai.forecast_point",
  "description": "One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.",
  "required": [
   "versionId",
   "targetStart",
   "p50"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "versionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.forecast_version"
   },
   "scenarioId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.forecast_scenario",
    "description": "Set where the point belongs to a what-if scenario rather than the version itself."
   },
   "targetStart": {
    "type": "string",
    "format": "date-time"
   },
   "targetEnd": {
    "type": "string",
    "format": "date-time"
   },
   "dimensionKey": {
    "type": "string",
    "nullable": true,
    "description": "Canonical key of the breakdown, e.g. `product=…;channel=web`."
   },
   "p10": {
    "type": "number",
    "nullable": true
   },
   "p50": {
    "type": "number"
   },
   "p90": {
    "type": "number",
    "nullable": true
   },
   "unit": {
    "type": "string"
   },
   "drivers": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Component decomposition or SHAP contributions, largest first (ADM-506)."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiForecastScenario": {
  "type": "object",
  "x-ticvai-persistence": "ai.forecast_scenario",
  "description": "**A what-if against a published version** (ADM-507, ADM-517, BO-931). Changes nothing in production; its points are written with `scenarioId`.",
  "required": [
   "baseVersionId",
   "changes"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string"
   },
   "baseVersionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.forecast_version"
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lever"
     ],
     "properties": {
      "lever": {
       "type": "string",
       "enum": [
        "price",
        "capacity",
        "openingHours",
        "weather",
        "event",
        "marketing",
        "staffing",
        "closure"
       ]
      },
      "target": {
       "type": "string",
       "nullable": true
      },
      "value": {
       "type": "object",
       "additionalProperties": true,
       "nullable": true
      }
     }
    },
    "minItems": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "computing",
     "ready",
     "failed"
    ],
    "readOnly": true
   },
   "result": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true,
    "description": "Deltas against the base version by subject and period."
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiForecastVersion": {
  "type": "object",
  "x-ticvai-persistence": "ai.forecast_version",
  "description": "**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.",
  "required": [
   "definitionId",
   "versionNumber",
   "status",
   "basis"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "definitionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.forecast_definition"
   },
   "versionNumber": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "running",
     "draft",
     "awaitingApproval",
     "published",
     "superseded",
     "rejected",
     "failed"
    ],
    "readOnly": true
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producerRef": {
    "type": "string"
   },
   "modelVersion": {
    "type": "string",
    "nullable": true
   },
   "dataCutoffAt": {
    "type": "string",
    "format": "date-time",
    "description": "The analytical replica watermark the snapshot was taken at."
   },
   "horizonStart": {
    "type": "string",
    "format": "date-time"
   },
   "horizonEnd": {
    "type": "string",
    "format": "date-time"
   },
   "qualityChecks": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "Each gate and whether it passed."
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal",
    "description": "Null where the definition auto-published."
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiInsight": {
  "type": "object",
  "x-ticvai-persistence": "ai.insight",
  "description": "**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).",
  "required": [
   "kind",
   "title",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "anomaly",
     "forecastDeviation",
     "trend",
     "opportunity",
     "executiveSummary",
     "rootCause",
     "forecastThreshold",
     "marketingRecommendation"
    ]
   },
   "detectorId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.anomaly_detector"
   },
   "metricKey": {
    "type": "string",
    "nullable": true
   },
   "subjectKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "campaign",
     "journey",
     "forecastDefinition",
     "venue"
    ],
    "description": "What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."
   },
   "subjectRef": {
    "type": "string",
    "nullable": true
   },
   "recommendedAction": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."
   },
   "expectedImpact": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."
   },
   "title": {
    "type": "string"
   },
   "narrative": {
    "type": "string",
    "nullable": true
   },
   "evidence": {
    "$ref": "#/components/schemas/AiEvidenceItemList"
   },
   "magnitude": {
    "type": "number",
    "nullable": true
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "correlationKey": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "new",
     "reviewed",
     "accepted",
     "rejected",
     "actioned",
     "measured"
    ],
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "actionRef": {
    "type": "string",
    "nullable": true
   },
   "measuredImpact": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiMaturity": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded as jsonb on ai.suggestion and ai.forecast_version",
  "description": "**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.",
  "required": [
   "stage",
   "basedOn"
  ],
  "properties": {
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ],
    "description": "`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."
   },
   "basedOn": {
    "type": "string",
    "description": "The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "source"
     ],
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "venueSettings",
        "startingPattern",
        "calendar",
        "weather",
        "bookingsOnHand",
        "ownHistory",
        "importedHistory",
        "configuration",
        "trainedModel"
       ]
      },
      "detail": {
       "type": "string",
       "nullable": true,
       "description": "e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."
      },
      "observations": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ownDataShare": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."
   },
   "limitedHistory": {
    "type": "boolean"
   },
   "nextStage": {
    "type": "object",
    "nullable": true,
    "description": "What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.",
    "properties": {
     "stage": {
      "type": "string",
      "enum": [
       "learning",
       "established",
       "learned"
      ]
     },
     "needs": {
      "type": "string"
     },
     "expectedBy": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   }
  }
 },
 "AiOperationalRequirement": {
  "type": "object",
  "x-ticvai-persistence": "ai.operational_requirement",
  "description": "**A requirement derived from a forecast version** (design 2.2 C step 6, AIP-067): staff, POS, gates, F&B, stock or resources, computed with the tenant's productivity standards. **Autonomy L2 (prepare)**: it is sent to the owning module as a recommendation bound to that version, and a person applies it there.",
  "required": [
   "versionId",
   "kind",
   "periodStart",
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "versionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.forecast_version"
   },
   "kind": {
    "type": "string",
    "enum": [
     "staff",
     "pos",
     "kiosk",
     "gates",
     "fnb",
     "retail",
     "stock",
     "resource",
     "equipment",
     "facility"
    ]
   },
   "targetContract": {
    "type": "string",
    "description": "The owning module that applies it: `workforce`, `fnb`, `inventory`, `resources`, `access`."
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "A role, outlet, gate, item or resource type."
   },
   "periodStart": {
    "type": "string",
    "format": "date-time"
   },
   "periodEnd": {
    "type": "string",
    "format": "date-time"
   },
   "quantity": {
    "type": "number"
   },
   "quantityP90": {
    "type": "number",
    "nullable": true,
    "description": "The requirement at the forecast's 90th percentile, for planning to the busy case."
   },
   "unit": {
    "type": "string"
   },
   "productivityStandard": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "The standard used, e.g. covers per staff hour, scans per gate per hour."
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "accepted",
     "modified",
     "rejected",
     "handedOver",
     "expired"
    ],
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "decisionNote": {
    "type": "string",
    "nullable": true
   },
   "handoverRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The owning module's record once handed over."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiScenarioComparison": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from ai.forecast_point",
  "description": "Scenarios side by side against their base version.",
  "required": [
   "scenarios"
  ],
  "properties": {
   "scenarios": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiForecastScenario"
    }
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "subject": {
       "type": "string"
      },
      "periodStart": {
       "type": "string",
       "format": "date-time"
      },
      "base": {
       "type": "number"
      },
      "values": {
       "type": "object",
       "additionalProperties": true,
       "description": "Scenario id to value."
      }
     }
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
 "StaffingCoverage": {
  "type": "object",
  "description": "Resource board 4.4. **The gap is the product.**",
  "properties": {
   "date": {
    "type": "string",
    "format": "date"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "positionCode": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "from": {
    "type": "string"
   },
   "to": {
    "type": "string"
   },
   "required": {
    "type": "integer"
   },
   "rostered": {
    "type": "integer"
   },
   "qualified": {
    "type": "integer",
    "description": "**A position filled by somebody not qualified for it is still a gap.**"
   },
   "gap": {
    "type": "integer"
   },
   "severity": {
    "type": "string",
    "enum": [
     "covered",
     "tight",
     "short",
     "blocking"
    ]
   },
   "openShiftIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "basisApplied": {
    "type": "string",
    "enum": [
     "minimum",
     "forecastRequirement"
    ],
    "description": "Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."
   },
   "minimumRequired": {
    "type": "integer",
    "nullable": true,
    "description": "The configured minimum for the position and window."
   },
   "forecastRequired": {
    "type": "number",
    "nullable": true,
    "description": "The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."
   },
   "forecastRequiredP90": {
    "type": "number",
    "nullable": true,
    "description": "The busy-case requirement, for planning to the busy case."
   },
   "forecastVersionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."
   }
  }
 },
 "Suggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion",
  "description": "One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n",
  "required": [
   "id",
   "kind",
   "basis",
   "maturity",
   "producedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SuggestionKind"
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "scopePath": {
    "type": "string"
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "What it is about — a product, an outlet, an item, a party."
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "description": "The suggestion itself. Shape depends on `kind`."
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1,
    "description": "**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"
   },
   "explanation": {
    "type": "string",
    "description": "**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"
   },
   "inputs": {
    "type": "object",
    "additionalProperties": true,
    "description": "What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"
   },
   "producerRef": {
    "type": "string",
    "description": "The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"
   }
  }
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline.\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario",
   "sendTime",
   "wasteRisk",
   "queueBalancing",
   "itinerary"
  ]
 }
}
```
