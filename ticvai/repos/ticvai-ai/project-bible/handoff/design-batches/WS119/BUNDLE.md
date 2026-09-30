# WS119 — AI Forecasting and Predictive Intelligence board 1

**10 screens · 15 operations · 15 schemas · 3 permissions**

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
  `AI_APPROVE, AI_CONFIGURE, AI_USE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-499` | Forecasting Command Center | commandCentre | 3 | 0 | — |
| `ADM-500` | Forecast Configuration & Forecasting Strategy | configEditor | 3 | 0 | — |
| `ADM-501` | Forecast Data & Signal Configuration | listDetail | 3 | 0 | — |
| `ADM-502` | Attendance & Visitation Forecast | listDetail | 3 | 0 | — |
| `ADM-503` | Ticket, Product & Timeslot Demand Forecast | listDetail | 1 | 0 | — |
| `ADM-504` | Channel & Booking Pace Forecast | listDetail | 1 | 0 | — |
| `ADM-505` | Revenue & Commercial Forecast | commandCentre | 1 | 0 | — |
| `ADM-506` | Forecast Drivers, Confidence & Explainability | listDetail | 4 | 0 | — |
| `ADM-507` | Forecast Scenario & What-If Simulator | listDetail | 3 | 0 | — |
| `ADM-508` | Forecast Accuracy, Review & Publication Center | listDetail | 5 | 0 | — |

## Thin screens in this batch

**ADM-501, ADM-502, ADM-503, ADM-504, ADM-506, ADM-507, ADM-508 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-499",
  "name": "Forecasting Command Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "1",
   "page": 4
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/forecasting-command-center-adm-499",
   "component": "apps/ticvai-web/src/routes/analytics/ForecastingCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-500",
    "ADM-501",
    "ADM-502",
    "ADM-503",
    "ADM-504",
    "ADM-505",
    "ADM-506",
    "ADM-507",
    "ADM-508"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-500",
     "trigger": "Forecast Configuration & Forecasting Strategy",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "definitionKey"
     ]
    },
    {
     "to": "ADM-501",
     "trigger": "Forecast Data & Signal Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "definitionKey"
     ]
    },
    {
     "to": "ADM-502",
     "trigger": "Attendance & Visitation Forecast",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-503",
     "trigger": "Ticket, Product & Timeslot Demand Forecast",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-504",
     "trigger": "Channel & Booking Pace Forecast",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-505",
     "trigger": "Revenue & Commercial Forecast",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-506",
     "trigger": "Forecast Drivers, Confidence & Explainability",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-507",
     "trigger": "Forecast Scenario & What-If Simulator",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-508",
     "trigger": "Forecast Accuracy, Review & Publication Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "definitionKey",
      "versionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide management with one central view of expected attendance, demand and revenue across venues and future periods.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Forecast Attendance Today",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Attendance Tomorrow",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Attendance Next 7 Days",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Revenue",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Current Bookings",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Expected Walk-In",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Occupancy",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Demand Index",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Confidence",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast vs Actual",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Forecast Accuracy",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Active Forecast Alerts",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 4 §Header KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The forecasting list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the forecasting untouched.",
   "emptyFirstRun": "No forecasting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the forecasting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listForecastDefinitions",
    "contract": "ai",
    "purpose": "What is forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "exportForecastVersion",
    "contract": "ai",
    "purpose": "Export the forecast version as CSV, Excel or JSON",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-499",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-499"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 4. 0 of 0 labels bound to a contract property; 12 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "versionId",
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
  "id": "ADM-500",
  "name": "Forecast Configuration & Forecasting Strategy",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "2",
   "page": 6
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/forecast-configuration-forecasting-strategy-adm-500",
   "component": "apps/ticvai-web/src/routes/analytics/ForecastConfigurationForecastingStrategy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Fields; Options conceptually) and no display directory — it is settings, not a population",
  "purpose": "Configure what TICVAI should forecast, at what level of detail, for what horizon and how frequently forecasts should be refreshed. This screen establishes the forecasting object.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Forecast Name",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Forecast Type",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Forecast Target",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Forecast Horizon",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Time Granularity",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Refresh Frequency",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Historical Window",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Model Strategy",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Confidence Policy",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Effective Dates",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Forecast Types",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Attendance",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Ticket Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Product Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Revenue",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Channel Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Timeslot Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Event Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Membership Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Add-On Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Experience Demand",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Intraday",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Next Day",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "7 Days",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "14 Days",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "30 Days",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "90 Days",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 6 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Producer",
       "bindsTo": "AiForecastDefinition.producer",
       "operation": "setForecastDefinition",
       "notes": "`rule`, `statistical` or `ensemble` (M18-16). A model only arrives by promotion.",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "numberField",
       "label": "History window (months)",
       "bindsTo": "AiForecastDefinition.historyWindowMonths",
       "operation": "setForecastDefinition",
       "notes": "Default 36 (M18-16).",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "selectField",
       "label": "Cold start",
       "bindsTo": "AiForecastDefinition.coldStart",
       "operation": "setForecastDefinition",
       "notes": "**What the forecast stands on before there is history** (AI functions review): the venue AI profile with the venue-type pattern, a sister venue, a category, or imported history; the starting range and how many observations the prior is worth.",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The forecast forecasting strategy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the forecast forecasting strategy untouched.",
   "emptyFirstRun": "No forecast forecasting strategy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listForecastDefinitions",
    "contract": "ai",
    "purpose": "What is forecast",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setForecastDefinition",
    "contract": "ai",
    "purpose": "Define a forecast",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "runForecast",
    "contract": "ai",
    "purpose": "Run a forecast now",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-500",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-500"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 57 of 80 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "definitionKey",
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
  "id": "ADM-501",
  "name": "Forecast Data & Signal Configuration",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "3",
   "page": 8
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/forecast-data-signal-configuration-adm-501",
   "component": "apps/ticvai-web/src/routes/analytics/ForecastDataSignalConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define which historical, current and contextual signals may contribute to each forecast.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 8"
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
       "impliedBy": "setForecastDefinition",
       "label": "Save forecast definition",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listForecastSignals",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setForecastDefinition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The forecast data signal list.",
   "error": "Could not load. Names which read failed and leaves the forecast data signal untouched.",
   "emptyFirstRun": "No forecast data signal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the forecast data signal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setForecastDefinition",
    "contract": "ai",
    "purpose": "Define a forecast",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listForecastSignals",
    "contract": "ai",
    "purpose": "Forecast signals and their freshness",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "configureForecastSignalSource",
    "contract": "ai",
    "purpose": "Set up a forecast signal",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-501",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-501"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 88 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "definitionKey",
     "from": "navigation"
    },
    {
     "name": "signalKey",
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
  "id": "ADM-502",
  "name": "Attendance & Visitation Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "4",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/attendance-visitation-forecast-adm-502",
   "component": "apps/ticvai-web/src/routes/analytics/AttendanceVisitationForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "versionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide detailed prediction of future venue attendance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 11"
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
       "impliedBy": "configureAnomalyDetector",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAiInsights",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
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
   "loading": "The attendance visitation forecast list.",
   "error": "Could not load. Names which read failed and leaves the attendance visitation forecast untouched.",
   "emptyFirstRun": "No attendance visitation forecast yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attendance visitation forecast are still there. Names the active filter and offers to clear it.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-502",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-502"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-503",
  "name": "Ticket, Product & Timeslot Demand Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "5",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/ticket-product-timeslot-demand-forecast-adm-503",
   "component": "apps/ticvai-web/src/routes/analytics/TicketProductTimeslotDemandForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "versionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Predict demand at the product and inventory level so TICVAI can understand what customers are likely to buy, not only total attendance.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 12 §Show"
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
       "label": "Every ticket product timeslot",
       "columns": [
        "Days Before Visit",
        "Cumulative Sales",
        "Current Booking Curve",
        "Historical Average",
        "Forecast Final Demand",
        "Product Relationships"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 12 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected ticket product timeslot",
       "bindsTo": null,
       "columns": [
        "Days Before Visit",
        "Cumulative Sales",
        "Current Booking Curve",
        "Historical Average",
        "Forecast Final Demand",
        "Product Relationships"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Family Meal demand typically increases”, “Where enough evidence exists, estimate”.",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 12 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket product timeslot list.",
   "error": "Could not load. Names which read failed and leaves the ticket product timeslot untouched.",
   "emptyFirstRun": "No ticket product timeslot yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket product timeslot are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Days Before Visit",
    "Cumulative Sales",
    "Current Booking Curve",
    "Historical Average",
    "Forecast Final Demand",
    "Product Relationships"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-503",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-503"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 12. 0 of 6 labels bound to a contract property; 6 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-504",
  "name": "Channel & Booking Pace Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "6",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/channel-booking-pace-forecast-adm-504",
   "component": "apps/ticvai-web/src/routes/analytics/ChannelBookingPaceForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "versionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast) and no metric row",
  "purpose": "Predict where and when future sales are expected to arrive. This is particularly useful because a venue with 10,000 current bookings may still receive significant B2C, POS, reseller and walk-in volume.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 13 §Forecast"
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
       "label": "Every channel booking pace",
       "columns": [
        "B2C Website",
        "Mobile App",
        "POS",
        "Flying POS",
        "Kiosk",
        "B2B",
        "Reseller",
        "OTA / API Partners where applicable",
        "Call Center / Agent",
        "Walk-In",
        "Channel Forecast",
        "Channel Current Expected Additional Final Forecast"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 13 §Forecast"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel booking pace",
       "bindsTo": null,
       "columns": [
        "B2C Website",
        "Mobile App",
        "POS",
        "Flying POS",
        "Kiosk",
        "B2B",
        "Reseller",
        "OTA / API Partners where applicable",
        "Call Center / Agent",
        "Walk-In",
        "Channel Forecast",
        "Channel Current Expected Additional Final Forecast"
       ],
       "notes": "The pack groups this record's detail under its own headings: “POS/Walk-In 0 2,950 2,950”.",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 13 §Forecast"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel booking pace list.",
   "error": "Could not load. Names which read failed and leaves the channel booking pace untouched.",
   "emptyFirstRun": "No channel booking pace yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel booking pace are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "B2C Website",
    "Mobile App",
    "POS",
    "Flying POS",
    "Kiosk",
    "B2B"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-504",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-504"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 13. 0 of 12 labels bound to a contract property; 12 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-505",
  "name": "Revenue & Commercial Forecast",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "7",
   "page": 15
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/revenue-commercial-forecast-adm-505",
   "component": "apps/ticvai-web/src/routes/analytics/RevenueCommercialForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "versionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Revenue KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Forecast future revenue based on predicted sales, attendance, product mix, current pricing and other approved commercial signals.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Forecast Ticket Revenue",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Membership Revenue",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Add-On Revenue",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast F&B Revenue where supported",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Retail Revenue where supported",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Total Forecast Revenue",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per Visitor",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Revenue vs Budget / Target where available",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Confidence Range",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 15 §Revenue KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue commercial forecast list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the revenue commercial forecast untouched.",
   "emptyFirstRun": "No revenue commercial forecast yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue commercial forecast are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-505",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-505"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 9 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-506",
  "name": "Forecast Drivers, Confidence & Explainability",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "8",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/forecast-drivers-confidence-explainability-adm-506",
   "component": "apps/ticvai-web/src/routes/analytics/ForecastDriversConfidenceExplainability.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "versionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Explain why the forecast changed and how much uncertainty exists. This is essential because management should not receive only: “Tomorrow attendance = 16,120.” They need to understand the basis and uncertainty. Forecast Attendance 16,120 Confidence Range 15,300 – 17,050 Confidence Status High Key Drivers Example: Current Booking Pace Positive +Strong Saturday Historical Demand Positive +Strong Special Event Positive +Medium Weather Forecast Positive +Medium Current Price Neutral Recent Cancellation Rate Negative Medium Forecast Change Explanation Previous: 15,640 Current: 16,120 Change: +480 Structured explanation: Current booking pace increased above the historical Saturday pattern, while expected weather conditions improved. These signals contributed to an upward revision.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 16 §Show"
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
       "label": "Every forecast drivers confidence",
       "columns": [
        "Limited Historical Data",
        "New Product",
        "New Event",
        "Missing Weather",
        "Abnormal Promotion",
        "High Cancellation Variability",
        "Unusual Booking Pattern",
        "Confidence by Horizon",
        "92% / High",
        "84% / High",
        "71% / Medium",
        "58% / Lower"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 16 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected forecast drivers confidence",
       "bindsTo": null,
       "columns": [
        "Limited Historical Data",
        "New Product",
        "New Event",
        "Missing Weather",
        "Abnormal Promotion",
        "High Cancellation Variability",
        "Unusual Booking Pattern",
        "Confidence by Horizon",
        "92% / High",
        "84% / High",
        "71% / Medium",
        "58% / Lower"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Where applicable”, “Ensemble”.",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 16 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The forecast drivers confidence list.",
   "error": "Could not load. Names which read failed and leaves the forecast drivers confidence untouched.",
   "emptyFirstRun": "No forecast drivers confidence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the forecast drivers confidence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "explainMetricChange",
    "contract": "ai",
    "purpose": "Why did this metric change",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listForecastVersions",
    "contract": "ai",
    "purpose": "Forecast versions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getForecastAccuracy",
    "contract": "ai",
    "purpose": "Measured forecast accuracy",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Limited Historical Data",
    "New Product",
    "New Event",
    "Missing Weather",
    "Abnormal Promotion",
    "High Cancellation Variability"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-506",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-506"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 16. 0 of 12 labels bound to a contract property; 12 of 64 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-507",
  "name": "Forecast Scenario & What-If Simulator",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "9",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/forecast-scenario-what-if-simulator-adm-507",
   "component": "apps/ticvai-web/src/routes/analytics/ForecastScenarioWhatIfSimulator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "versionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow management to test possible future conditions without changing production configuration. This is one of the most important screens.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 18 §Show"
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
       "label": "Every forecast scenario what-if",
       "columns": [
        "Attendance",
        "Revenue",
        "Product Demand",
        "Peak Time",
        "Capacity Pressure",
        "Confidence",
        "Operational Implications"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 18 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected forecast scenario what-if",
       "bindsTo": null,
       "columns": [
        "Attendance",
        "Revenue",
        "Product Demand",
        "Peak Time",
        "Capacity Pressure",
        "Confidence",
        "Operational Implications"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Attendance”, “Simulation”, “Important Boundary”, “If management chooses a scenario”.",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 18 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The forecast scenario what-if list.",
   "error": "Could not load. Names which read failed and leaves the forecast scenario what-if untouched.",
   "emptyFirstRun": "No forecast scenario what-if yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the forecast scenario what-if are still there. Names the active filter and offers to clear it.",
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
   }
  ],
  "entryState": {
   "preloaded": [
    "Attendance",
    "Revenue",
    "Product Demand",
    "Peak Time",
    "Capacity Pressure",
    "Confidence"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-507",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-507"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 18. 0 of 7 labels bound to a contract property; 7 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-508",
  "name": "Forecast Accuracy, Review & Publication Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "AI_Forecasting_and_Predictive_Intelligence_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 20
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/analytics/forecast-accuracy-review-publication-center-adm-508",
   "component": "apps/ticvai-web/src/routes/analytics/ForecastAccuracyReviewPublicationCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-499"
   ],
   "exitTo": [
    "ADM-499"
   ],
   "transitions": [
    {
     "to": "ADM-499",
     "trigger": "Back to Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "versionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Measure forecast quality over time and publish approved forecast outputs for use by other TICVAI modules. A forecasting system should continuously answer: How accurate have our forecasts actually been? Forecast vs Actual Example:",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 20 §Analyze"
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
       "kind": "publishGate",
       "impliedBy": "publishForecastVersion",
       "notes": "Declares `publishForecastVersion`. **The gate names what the publish will affect before it happens**: which tenants, venues or capabilities take the new version, and that the previous one stays available to roll back to.",
       "provenance": "check-screens publish rule, 29 September 2026"
      },
      {
       "kind": "dataTable",
       "label": "Every forecast accuracy review",
       "columns": [
        "Venue",
        "Product",
        "Channel",
        "Timeslot",
        "Day Type",
        "Forecast Horizon",
        "Model",
        "Event Type",
        "Forecast Bias",
        "Saturday Walk-In",
        "7.4%",
        "MODEL REVIEW RECOMMENDED",
        "Forecast Version",
        "Forecast ID",
        "Version",
        "Generated Time",
        "Model Version",
        "Data Cut-Off",
        "Confidence",
        "Status",
        "Publication Status",
        "Draft",
        "Generated",
        "Reviewed",
        "Published",
        "Superseded",
        "Archived"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 20 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected forecast accuracy review",
       "bindsTo": null,
       "columns": [
        "Venue",
        "Product",
        "Channel",
        "Timeslot",
        "Day Type",
        "Forecast Horizon",
        "Model",
        "Event Type",
        "Forecast Bias",
        "Saturday Walk-In",
        "7.4%",
        "MODEL REVIEW RECOMMENDED",
        "Forecast Version",
        "Forecast ID",
        "Version",
        "Generated Time",
        "Model Version",
        "Data Cut-Off",
        "Confidence",
        "Status",
        "Publication Status",
        "Draft",
        "Generated",
        "Reviewed",
        "Published",
        "Superseded",
        "Archived"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Next Day”, “Consumers”, “DATA PREPARATION / FEATURE LAYER”, “CONFIDENCE & EXPLAINABILITY”, “SCENARIO ENGINE”, “Conceptually”.",
       "provenance": "pack AI_Forecasting_and_Predictive_Intelligence_Reference.pdf, page 20 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The forecast accuracy review list.",
   "error": "Could not load. Names which read failed and leaves the forecast accuracy review untouched.",
   "emptyFirstRun": "No forecast accuracy review yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the forecast accuracy review are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "runForecast",
    "contract": "ai",
    "purpose": "Run a forecast now",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listForecastVersions",
    "contract": "ai",
    "purpose": "Forecast versions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "publishForecastVersion",
    "contract": "ai",
    "purpose": "Publish a forecast version",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getForecastAccuracy",
    "contract": "ai",
    "purpose": "Measured forecast accuracy",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "exportForecastVersion",
    "contract": "ai",
    "purpose": "Export the forecast version as CSV, Excel or JSON",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Venue",
    "Product",
    "Channel",
    "Timeslot",
    "Day Type",
    "Forecast Horizon"
   ],
   "params": [
    {
     "name": "definitionKey",
     "from": "navigation"
    },
    {
     "name": "versionId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-508",
   "workshopBoard": "wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-508"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Forecasting_and_Predictive_Intelligence_Reference.pdf page 20. 0 of 27 labels bound to a contract property; 27 of 311 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "configureForecastSignalSource": {
  "method": "PUT",
  "path": "/forecast-signals/{signalKey}",
  "contract": "ai",
  "summary": "Set up a forecast signal",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "AiSignalSource",
  "responds": "AiSignalSource"
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
 "explainMetricChange": {
  "method": "POST",
  "path": "/insights/explain-metric-change",
  "contract": "ai",
  "summary": "Why did this metric change",
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
  "responds": "AiMetricChangeExplanation"
 },
 "exportForecastVersion": {
  "method": "POST",
  "path": "/forecast-versions/{versionId}/exports",
  "contract": "ai",
  "summary": "Export a forecast version as a file",
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
  "responds": null
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
 "getForecastAccuracy": {
  "method": "GET",
  "path": "/forecast-accuracy",
  "contract": "ai",
  "summary": "Measured forecast accuracy",
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
    "name": "horizonDays",
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
 "listForecastDefinitions": {
  "method": "GET",
  "path": "/forecast-definitions",
  "contract": "ai",
  "summary": "What is forecast",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "subject",
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
 "listForecastSignals": {
  "method": "GET",
  "path": "/forecast-signals",
  "contract": "ai",
  "summary": "Forecast signals and their freshness",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "kind",
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
 "listForecastVersions": {
  "method": "GET",
  "path": "/forecast-versions",
  "contract": "ai",
  "summary": "Forecast versions",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "definitionKey",
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
 "publishForecastVersion": {
  "method": "POST",
  "path": "/forecast-versions/{versionId}/publish",
  "contract": "ai",
  "summary": "Publish a forecast version",
  "permission": "AI_APPROVE",
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
  "responds": "AiForecastVersion"
 },
 "runForecast": {
  "method": "POST",
  "path": "/forecast-definitions/{definitionKey}/runs",
  "contract": "ai",
  "summary": "Run a forecast now",
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
  "requestBody": null,
  "responds": null
 },
 "setForecastDefinition": {
  "method": "PUT",
  "path": "/forecast-definitions/{definitionKey}",
  "contract": "ai",
  "summary": "Define a forecast",
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
  "requestBody": "AiForecastDefinition",
  "responds": "AiForecastDefinition"
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
 "AiEvidenceItem": {
  "type": "object",
  "x-ticvai-persistence": "none — held in jsonb on ai.decision_record.evidence, through AiEvidenceItemList",
  "description": "One piece of evidence behind a decision, **labelled by origin** (AIC-197): read from a source system, derived by a rule or feature, or inferred by a model. An explanation is built from these, never from a model's chain of thought (AIC-192).",
  "required": [
   "label",
   "kind"
  ],
  "properties": {
   "label": {
    "type": "string",
    "enum": [
     "source",
     "derived",
     "modelInferred"
    ]
   },
   "kind": {
    "type": "string",
    "description": "What it is: `feature`, `rule`, `document`, `metric`, `transaction`, `candidateSet`."
   },
   "ref": {
    "type": "string",
    "nullable": true,
    "description": "Where it came from: a table and id, a document chunk, a metric key."
   },
   "name": {
    "type": "string"
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "observedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "AiForecastAccuracy": {
  "type": "object",
  "x-ticvai-persistence": "ai.forecast_accuracy",
  "description": "**Measured accuracy by horizon** (AIP-044, ADM-508), labelled measured: WAPE, bias and interval coverage against the baseline rule. These are the numbers the promotion gate reads (design 3.5).",
  "required": [
   "definitionId",
   "horizonDays",
   "periodStart"
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
   "versionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.forecast_version"
   },
   "producerRef": {
    "type": "string"
   },
   "horizonDays": {
    "type": "integer",
    "minimum": 0
   },
   "periodStart": {
    "type": "string",
    "format": "date-time"
   },
   "periodEnd": {
    "type": "string",
    "format": "date-time"
   },
   "wape": {
    "type": "number",
    "nullable": true
   },
   "bias": {
    "type": "number",
    "nullable": true
   },
   "intervalCoverage": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Share of actuals inside the 10th-90th percentile band."
   },
   "baselineWape": {
    "type": "number",
    "nullable": true
   },
   "measuredAt": {
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
 "AiForecastDefinition": {
  "type": "object",
  "x-ticvai-persistence": "ai.forecast_definition",
  "description": "**What is forecast, at what grain, for what horizon, how often and by which producer** (design 3.1 Forecast, 5.2; ADM-500). One forecasting service for the platform: BI's extra subjects are definitions here, not a second forecaster (AIP-036, AIP-037).",
  "required": [
   "definitionKey",
   "subject",
   "grain",
   "horizonDays",
   "producer"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "definitionKey": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "subject": {
    "type": "string",
    "enum": [
     "attendance",
     "arrivalPattern",
     "productDemand",
     "timeslotDemand",
     "channelPace",
     "revenue",
     "occupancy",
     "attractionUtilisation",
     "queue",
     "entryFlow",
     "staffing",
     "posDemand",
     "fnbDemand",
     "retailDemand",
     "stockDemand",
     "resourceDemand",
     "refunds",
     "cashCollection",
     "membershipRenewals",
     "churn"
    ]
   },
   "grain": {
    "type": "string",
    "enum": [
     "hour",
     "day",
     "week",
     "month"
    ]
   },
   "dimensions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Breakdowns forecast directly or reconciled to. **Documented keys (29 September, build; 8.2.12, 8.2.14, 8.2.27):** `product`, `channel`, `timeslot`, `gate`, `outlet`, `customerSegment` and `originCountry`. `customerSegment` is the marketing-crm segment (of those in `segmentIds`, else the membership tier) the guest belonged to on the day of the booking; `originCountry` is the guest profile's country, else the order's billing country, else the channel's market, recorded as `unknown` rather than guessed. **The nightly snapshot (design 2.2 C step 1) carries both for every booking and admission**, so a definition that names them is forecast and reconciled by them. Any other key is accepted and forecast only where the snapshot carries it."
   },
   "segmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "The marketing-crm segments `customerSegment` breaks down by, in priority order where a guest is in several. Empty means membership tiers."
   },
   "horizonDays": {
    "type": "integer",
    "minimum": 1,
    "maximum": 730
   },
   "refreshCadence": {
    "type": "string",
    "enum": [
     "hourly",
     "daily",
     "weekly"
    ]
   },
   "producer": {
    "type": "string",
    "enum": [
     "rule",
     "statistical",
     "model",
     "ensemble"
    ],
    "description": "Which producer is live (design 3.10). A model is promoted only through `promoteAiRelease`. **`ensemble`** (18 September minutes, M18-16): a weighted blend of the rule and statistical producers, and of a promoted model where one exists; the weights are recorded on each version. Setting `ensemble` never brings in an unpromoted model."
   },
   "historyWindowMonths": {
    "type": "integer",
    "minimum": 1,
    "maximum": 60,
    "default": 36,
    "description": "How much of the venue's own history the statistical producer reads (18 September minutes, M18-16: \"36 months of history\"). Imported history (`importVenueHistory`) counts. Less than the window is not an error: the cold-start setting fills the gap."
   },
   "coldStart": {
    "type": "object",
    "description": "**What the forecast stands on before the venue has history** (29 September, AI functions review; forecasting book p.27 \"New Venue / New Product Problem\"). Day one is never empty: the prior is the venue AI settings (typical weekday and weekend attendance, capacity, opening hours) x the starting pattern for the venue type x the UAE calendar x weather, with bookings on hand as a floor. The statistical producer blends own data in as `(k x prior + n x own) / (k + n)`, with `k` = `priorWeightObservations`. The version's `maturity` says which stage it reached.",
    "properties": {
     "strategy": {
      "type": "string",
      "enum": [
       "venueSettings",
       "startingPattern",
       "sisterVenue",
       "categoryBaseline",
       "importedHistory"
      ],
      "default": "venueSettings",
      "description": "`venueSettings` uses the onboarding figures with the venue-type pattern; `sisterVenue` a venue of the same tenant; `categoryBaseline` a product category's own history; `importedHistory` means an import covers the window and the prior only fills unseen holidays."
     },
     "sisterVenueId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "For `sisterVenue`. Same tenant only (no data is pooled across tenants, AIP-149)."
     },
     "priorWeightObservations": {
      "type": "integer",
      "minimum": 1,
      "maximum": 52,
      "default": 4,
      "description": "`k`: how many own observations the prior is worth (4 same weekdays by default)."
     },
     "startingBandPercent": {
      "type": "integer",
      "minimum": 5,
      "maximum": 80,
      "default": 40,
      "description": "The width of the range while the prior carries most of the weight (about +/-40%)."
     }
    }
   },
   "producerRef": {
    "type": "string",
    "readOnly": true
   },
   "shadowProducerRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Runs alongside and is recorded, never shown (design 3.5)."
   },
   "autoPublish": {
    "type": "boolean",
    "default": false,
    "description": "Publish without approval when the quality gates pass (autonomy L4, design 3.8). Otherwise an `AI_APPROVE` holder publishes."
   },
   "qualityGates": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Completeness, blocking signals and accuracy-regression thresholds a version must pass to publish."
   },
   "signalKeys": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Signal sources this definition may use (ADM-501)."
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
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
 "AiMetricChangeExplanation": {
  "type": "object",
  "x-ticvai-persistence": "none — computed; written as an ai.insight of kind rootCause when kept",
  "description": "**Why a metric changed** (AIP-176..180, ANL-056): drivers with their contribution, computed from the semantic layer. The narrative binds every figure to a result placeholder (design 8, 5.10).",
  "required": [
   "metricKey",
   "change",
   "drivers"
  ],
  "properties": {
   "metricKey": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "comparison": {
    "type": "string"
   },
   "change": {
    "type": "number"
   },
   "changePercent": {
    "type": "number",
    "nullable": true
   },
   "drivers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string"
      },
      "member": {
       "type": "string"
      },
      "contribution": {
       "type": "number"
      },
      "evidence": {
       "$ref": "#/components/schemas/AiEvidenceItem"
      }
     }
    }
   },
   "narrative": {
    "type": "string",
    "nullable": true
   },
   "reliability": {
    "type": "string",
    "enum": [
     "grounded",
     "partial",
     "conflictingSources",
     "insufficientEvidence"
    ]
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time"
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
 "AiSignalSource": {
  "type": "object",
  "x-ticvai-persistence": "ai.signal_source",
  "description": "**A forecast signal** (AIP-199..203, ADM-501): weather (a commercial API, decided 29 September), holidays, calendar, events. Freshness and coverage are recorded; **missing data is stored as unavailable, never defaulted** (AIP-203).",
  "required": [
   "signalKey",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "signalKey": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "weather",
     "publicHoliday",
     "schoolCalendar",
     "religiousCalendar",
     "event",
     "marketing",
     "internal"
    ]
   },
   "provider": {
    "type": "string",
    "nullable": true
   },
   "credentialRef": {
    "type": "string",
    "nullable": true,
    "description": "A key-vault reference for a paid API, never the key."
   },
   "refreshCadence": {
    "type": "string",
    "enum": [
     "hourly",
     "daily",
     "weekly",
     "manual"
    ]
   },
   "coverage": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "readOnly": true
   },
   "freshAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
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
 }
}
```
