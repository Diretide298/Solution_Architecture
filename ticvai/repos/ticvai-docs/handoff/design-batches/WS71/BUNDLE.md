# WS71 — Unified BI Reporting and AI Analytics Platform board 10

**10 screens · 13 operations · 16 schemas · 3 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `REPORT_MANAGE, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ANL-061` | BI & Analytics Administration Command Center | commandCentre | 2 | 0 | — |
| `ANL-062` | Enterprise KPI Library | listDetail | 2 | 0 | — |
| `ANL-063` | KPI Targets, Thresholds & Scorecards | configEditor | 2 | 0 | — |
| `ANL-064` | Benchmark & Comparative Analytics Configuration | commandCentre | 3 | 1 | — |
| `ANL-065` | Data Source & Integration Registry | listDetail | 1 | 0 | — |
| `ANL-066` | Semantic Model & Business Data Catalogue | listDetail | 2 | 0 | — |
| `ANL-067` | Data Refresh, Pipeline & Data Health Monitor | commandCentre | 1 | 0 | — |
| `ANL-068` | Embedded BI, Workspace & Tenant Administration | configEditor | 1 | 0 | — |
| `ANL-069` | Analytics Performance, Usage & Cost Monitor | commandCentre | 1 | 0 | — |
| `ANL-070` | Analytics Governance, Security & Audit Center | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ANL-062, ANL-065, ANL-066, ANL-070 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-061",
  "name": "BI & Analytics Administration Command Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.1",
   "page": 123
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/bi-analytics-administration-command-center-anl-061",
   "component": "apps/venue-management-web/src/routes/analytics/BiAnalyticsAdministrationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-062",
    "ANL-063",
    "ANL-064",
    "ANL-065",
    "ANL-066",
    "ANL-067",
    "ANL-068",
    "ANL-069",
    "ANL-070"
   ],
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Back to Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-070",
     "trigger": "Analytics Governance, Security & Audit Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-062",
     "trigger": "Enterprise KPI Library",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-063",
     "trigger": "KPI Targets, Thresholds & Scorecards",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-064",
     "trigger": "Benchmark & Comparative Analytics Configuration",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-065",
     "trigger": "Data Source & Integration Registry",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-066",
     "trigger": "Semantic Model & Business Data Catalogue",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-067",
     "trigger": "Data Refresh, Pipeline & Data Health Monitor",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-068",
     "trigger": "Embedded BI, Workspace & Tenant Administration",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-069",
     "trigger": "Analytics Performance, Usage & Cost Monitor",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can determine overall analytics-platform health without reviewing multiple technical systems.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each component shall show) — counts over a population, then the population",
  "purpose": "Provide administrators with one consolidated view of the health and governance of the TICVAI analytics platform.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Each component shall show"
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
       "label": "Active Dashboards",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Active Reports",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Published KPIs",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Connected Data Sources",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Active Datasets",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Data Refresh Success %",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Data Quality Score",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Failed Refreshes",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "BI Service Health",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "AI Analytics Health",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Active Alerts",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Analytics Users",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Display"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every analytics administration",
       "columns": [
        "Healthy / Warning / Critical / Offline"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Each component shall show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected analytics administration",
       "bindsTo": null,
       "columns": [
        "Healthy / Warning / Critical / Offline"
       ],
       "notes": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 123 §Each component shall show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The analytics administration list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the analytics administration untouched.",
   "emptyFirstRun": "No analytics administration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the analytics administration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAnalyticsUsage",
    "contract": "reporting",
    "purpose": "Estate at a glance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAnalyticsPipelines",
    "contract": "reporting",
    "purpose": "Data health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-061",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-061"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 123. 0 of 1 labels bound to a contract property; 13 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-062",
  "name": "Enterprise KPI Library",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.2",
   "page": 124
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/enterprise-kpi-library-anl-062",
   "component": "apps/venue-management-web/src/routes/analytics/EnterpriseKpiLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§KPI Categories; KPI Status) and no metric row",
  "purpose": "Maintain the authoritative catalogue of approved TICVAI business KPIs. This is essential because every dashboard must use the same definition of a metric.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 124 §KPI Categories"
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
       "label": "Every enterprise kpi",
       "columns": [
        "Executive",
        "Sales",
        "Revenue",
        "Finance",
        "Operations",
        "Access",
        "Customer",
        "Membership",
        "Loyalty",
        "Marketing",
        "F&B",
        "Retail",
        "Inventory",
        "Resources"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 124 §KPI Categories"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected enterprise kpi",
       "bindsTo": null,
       "columns": [
        "Executive",
        "Sales",
        "Revenue",
        "Finance",
        "Operations",
        "Access",
        "Customer",
        "Membership",
        "Loyalty",
        "Marketing",
        "F&B",
        "Retail",
        "Inventory",
        "Resources"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Formula”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 124 §KPI Categories"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The enterprise kpi list.",
   "error": "Could not load. Names which read failed and leaves the enterprise kpi untouched.",
   "emptyFirstRun": "No enterprise kpi yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the enterprise kpi are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listKpis",
    "contract": "reporting",
    "purpose": "The enterprise library",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createKpi",
    "contract": "reporting",
    "purpose": "Add a KPI",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listKpis",
     "getKpiValues"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Executive",
    "Sales",
    "Revenue",
    "Finance",
    "Operations",
    "Access"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-062",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-062"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 124. 0 of 14 labels bound to a contract property; 30 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-063",
  "name": "KPI Targets, Thresholds & Scorecards",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.3",
   "page": 125
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/kpi-targets-thresholds-scorecards-anl-063",
   "component": "apps/venue-management-web/src/routes/analytics/KpiTargetsThresholdsScorecards.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Targets may be configured by) and no display directory — it is settings, not a population",
  "purpose": "Centrally configure performance targets and thresholds used throughout TICVAI analytics.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Organization",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 125 §Targets may be configured by"
      },
      {
       "kind": "selectField",
       "label": "Site",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 125 §Targets may be configured by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 125 §Targets may be configured by"
      },
      {
       "kind": "selectField",
       "label": "Attraction",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 125 §Targets may be configured by"
      },
      {
       "kind": "selectField",
       "label": "Business Unit",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 125 §Targets may be configured by"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 125 §Targets may be configured by"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 125 §Targets may be configured by"
      },
      {
       "kind": "selectField",
       "label": "Period",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 125 §Targets may be configured by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The kpi targets thresholds configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the kpi targets thresholds untouched.",
   "emptyFirstRun": "No kpi targets thresholds configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setKpiTargets",
    "contract": "reporting",
    "purpose": "Targets and scorecards",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getKpiValues"
    ]
   },
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Where they stand",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-063",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-063"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 125. 0 of 0 labels bound to a contract property; 8 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "kpiId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-064",
  "name": "Benchmark & Comparative Analytics Configuration",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.4",
   "page": 127
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/benchmark-comparative-analytics-configuration-anl-064",
   "component": "apps/venue-management-web/src/routes/analytics/BenchmarkComparativeAnalyticsConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Support metrics such as) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Define how TICVAI compares performance between sites, periods and peer groups.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Revenue per Visitor",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 127 §Support metrics such as"
      },
      {
       "kind": "metricTile",
       "label": "Transactions per 1,000 Visitors",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 127 §Support metrics such as"
      },
      {
       "kind": "metricTile",
       "label": "Entries per Gate per Hour",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 127 §Support metrics such as"
      },
      {
       "kind": "metricTile",
       "label": "Incidents per 10,000 Visitors",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 127 §Support metrics such as"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per m² where applicable",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 127 §Support metrics such as"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per Operating Hour",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 127 §Support metrics such as"
      },
      {
       "kind": "metricTile",
       "label": "Utilization %",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 127 §Support metrics such as"
      },
      {
       "kind": "textField",
       "label": "Scope path",
       "operation": "listSiteNormalisationBases",
       "notes": "Sends `?scopePath=` to `listSiteNormalisationBases`.",
       "provenance": "contract reporting.yaml GET /site-normalisation-bases"
      },
      {
       "kind": "datePicker",
       "label": "Period from",
       "operation": "listSiteNormalisationBases",
       "notes": "Sends `?periodFrom=` to `listSiteNormalisationBases`.",
       "provenance": "contract reporting.yaml GET /site-normalisation-bases"
      },
      {
       "kind": "datePicker",
       "label": "Period to",
       "operation": "listSiteNormalisationBases",
       "notes": "Sends `?periodTo=` to `listSiteNormalisationBases`.",
       "provenance": "contract reporting.yaml GET /site-normalisation-bases"
      },
      {
       "kind": "dataTable",
       "label": "Every site normalisation basis",
       "bindsTo": "SiteNormalisationBasis",
       "columns": [
        "SiteNormalisationBasis.id",
        "SiteNormalisationBasis.scopePath",
        "SiteNormalisationBasis.periodStart",
        "SiteNormalisationBasis.periodEnd",
        "SiteNormalisationBasis.visitors",
        "SiteNormalisationBasis.operatingHours",
        "SiteNormalisationBasis.staffedPositions",
        "SiteNormalisationBasis.areaSquareMetres"
       ],
       "operation": "listSiteNormalisationBases",
       "provenance": "contract reporting.yaml GET /site-normalisation-bases"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save site normalisation basis",
       "operation": "setSiteNormalisationBasis",
       "permission": "REPORT_MANAGE",
       "notes": "**The writer of `reporting.site_normalisation_basis`** (decided 29 September, writers pass).",
       "provenance": "contract reporting.yaml PUT /site-normalisation-bases"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The benchmark comparative analytics list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the benchmark comparative analytics untouched.",
   "emptyFirstRun": "No benchmark comparative analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the benchmark comparative analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAnalyticsBenchmark",
    "contract": "reporting",
    "purpose": "Configure the comparison basis",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSiteNormalisationBases",
    "contract": "reporting",
    "purpose": "The denominators each site is benchmarked by",
    "trigger": "onLoad"
   },
   {
    "operationId": "setSiteNormalisationBasis",
    "contract": "reporting",
    "purpose": "Set the denominators a site is benchmarked by",
    "trigger": "onAction",
    "invalidates": [
     "getAnalyticsBenchmark",
     "listSiteNormalisationBases"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Revenue per Visitor",
    "Transactions per 1,000 Visitors",
    "Entries per Gate per Hour",
    "Incidents per 10,000 Visitors",
    "Revenue per m² where applicable",
    "Revenue per Operating Hour"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-064",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-064"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 127. 0 of 0 labels bound to a contract property; 7 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetSiteNormalisationBasis",
    "component": "modal",
    "trigger": "Save site normalisation basis",
    "body": "**Collects what `setSiteNormalisationBasis` sends before it is called.** Required: `bases`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save site normalisation basis",
     "operation": "setSiteNormalisationBasis"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "bases"
     ]
    },
    "provenance": "contract reporting.yaml PUT /site-normalisation-bases"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-065",
  "name": "Data Source & Integration Registry",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.5",
   "page": 128
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/data-source-integration-registry-anl-065",
   "component": "apps/venue-management-web/src/routes/analytics/DataSourceIntegrationRegistry.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can identify every source feeding BI and understand its current status and ownership.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Maintain a centralized catalogue of data sources feeding the analytics platform.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 128 §Display"
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
       "label": "Every data source integration",
       "columns": [
        "Source Name",
        "Source Type",
        "Owner",
        "Connection",
        "Authentication Method",
        "Refresh Type",
        "Last Sync",
        "Records Processed",
        "Status",
        "Data Classification"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 128 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected data source integration",
       "bindsTo": null,
       "columns": [
        "Source Name",
        "Source Type",
        "Owner",
        "Connection",
        "Authentication Method",
        "Refresh Type",
        "Last Sync",
        "Records Processed",
        "Status",
        "Data Classification"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Important Security Principle”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 128 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data source integration list.",
   "error": "Could not load. Names which read failed and leaves the data source integration untouched.",
   "emptyFirstRun": "No data source integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data source integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAnalyticsPipelines",
    "contract": "reporting",
    "purpose": "Sources and integrations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Source Name",
    "Source Type",
    "Owner",
    "Connection",
    "Authentication Method",
    "Refresh Type"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-065",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-065"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 128. 0 of 10 labels bound to a contract property; 10 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-066",
  "name": "Semantic Model & Business Data Catalogue",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.6",
   "page": 129
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/semantic-model-business-data-catalogue-anl-066",
   "component": "apps/venue-management-web/src/routes/analytics/SemanticModelBusinessDataCatalogue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Dashboards, reports and AI operate against a consistent governed business-data model rather than independently querying raw tables.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Create the governed business layer between raw data and dashboards/AI. This is one of the most important technical screens in Board 10.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 129 §Detect"
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
       "label": "Every semantic model business",
       "columns": [
        "Missing relationships",
        "Circular relationships",
        "Duplicate aggregation risk",
        "Invalid cardinality",
        "Broken references"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 129 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected semantic model business",
       "bindsTo": null,
       "columns": [
        "Missing relationships",
        "Circular relationships",
        "Duplicate aggregation risk",
        "Invalid cardinality",
        "Broken references"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Customer”, “Order”, “Ticket”, “Admission”, “F&B Sale”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 129 §Detect"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The semantic model business list.",
   "error": "Could not load. Names which read failed and leaves the semantic model business untouched.",
   "emptyFirstRun": "No semantic model business yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the semantic model business are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSemanticModel",
    "contract": "reporting",
    "purpose": "The catalogue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setSemanticModel",
    "contract": "reporting",
    "purpose": "Publish it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSemanticModel",
     "listReportFields"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Missing relationships",
    "Circular relationships",
    "Duplicate aggregation risk",
    "Invalid cardinality",
    "Broken references"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-066",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-066"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 129. 0 of 5 labels bound to a contract property; 13 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-067",
  "name": "Data Refresh, Pipeline & Data Health Monitor",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.7",
   "page": 130
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/data-refresh-pipeline-data-health-monitor-anl-067",
   "component": "apps/venue-management-web/src/routes/analytics/DataRefreshPipelineDataHealthMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can identify stale or failed analytics data before users unknowingly make decisions from outdated information.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Monitor) — counts over a population, then the population",
  "purpose": "Monitor movement of information from operational systems into the analytics platform.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §Monitor"
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
       "label": "Pipelines Running",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Successful Refreshes",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failed Refreshes",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Refresh Duration",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Data Latency",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Stale Datasets",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Records Processed",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every data refresh pipeline",
       "columns": [
        "Completeness",
        "Timeliness",
        "Accuracy checks",
        "Duplicate records",
        "Missing values",
        "Schema changes",
        "Reconciliation status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected data refresh pipeline",
       "bindsTo": null,
       "columns": [
        "Completeness",
        "Timeliness",
        "Accuracy checks",
        "Duplicate records",
        "Missing values",
        "Schema changes",
        "Reconciliation status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Source”, “Ticketing Dataset Delayed”, “Affected”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 130 §Monitor"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data refresh pipeline list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the data refresh pipeline untouched.",
   "emptyFirstRun": "No data refresh pipeline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data refresh pipeline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAnalyticsPipelines",
    "contract": "reporting",
    "purpose": "Refresh and freshness",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Pipelines Running",
    "Successful Refreshes",
    "Failed Refreshes",
    "Average Refresh Duration",
    "Data Latency",
    "Stale Datasets"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-067",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-067"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 130. 0 of 7 labels bound to a contract property; 14 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-068",
  "name": "Embedded BI, Workspace & Tenant Administration",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.8",
   "page": 131
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/embedded-bi-workspace-tenant-administration-anl-068",
   "component": "apps/venue-management-web/src/routes/analytics/EmbeddedBiWorkspaceTenantAdministration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "BI content can be securely embedded and governed across TICVAI tenants and environments.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how BI technology is embedded inside TICVAI and separated across clients/tenants.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Navigation",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 131 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Theme",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 131 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Branding",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 131 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 131 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default Dashboard",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 131 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mobile behavior",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 131 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full-screen mode",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 131 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The embedded tenant administration configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the embedded tenant administration untouched.",
   "emptyFirstRun": "No embedded tenant administration configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDashboards",
    "contract": "reporting",
    "purpose": "Workspaces and embedding",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-068",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-068"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 131. 0 of 0 labels bound to a contract property; 7 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-069",
  "name": "Analytics Performance, Usage & Cost Monitor",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.9",
   "page": 132
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/analytics-performance-usage-cost-monitor-anl-069",
   "component": "apps/venue-management-web/src/routes/analytics/AnalyticsPerformanceUsageCostMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Usage KPIs; Performance KPIs) and a per-row directory (§Identify) — counts over a population, then the population",
  "purpose": "Monitor BI adoption, system performance, capacity consumption and analytical operating costs.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Identify"
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
       "label": "Active Analytics Users",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Dashboard Views",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Report Runs",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "AI Queries",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Exports",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "API Requests",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Peak Concurrent Users",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Dashboard Load Time",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Performance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Query Duration",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Performance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Slowest Reports",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Performance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Failed Queries",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Performance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Dataset Size",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Performance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Refresh Duration",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Performance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Embedded BI Availability",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Performance KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every analytics performance usage",
       "columns": [
        "Most Used Dashboards",
        "Least Used Dashboards",
        "Most Used Reports",
        "Unused Reports",
        "Most Queried KPIs",
        "Most Active Users/Roles"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected analytics performance usage",
       "bindsTo": null,
       "columns": [
        "Most Used Dashboards",
        "Least Used Dashboards",
        "Most Used Reports",
        "Unused Reports",
        "Most Queried KPIs",
        "Most Active Users/Roles"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Where supported, monitor”, “Tenant Usage”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 132 §Identify"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The analytics performance usage list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the analytics performance usage untouched.",
   "emptyFirstRun": "No analytics performance usage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the analytics performance usage are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAnalyticsUsage",
    "contract": "reporting",
    "purpose": "Usage, runtime and cost",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Active Analytics Users",
    "Dashboard Views",
    "Report Runs",
    "AI Queries",
    "Exports",
    "API Requests"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-069",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-069"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 132. 0 of 6 labels bound to a contract property; 20 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-070",
  "name": "Analytics Governance, Security & Audit Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "10",
   "number": "10.10",
   "page": 133
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/analytics-governance-security-audit-center-anl-070",
   "component": "apps/venue-management-web/src/routes/analytics/AnalyticsGovernanceSecurityAuditCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-061"
   ],
   "exitTo": [
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-061",
     "trigger": "Back to BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Critical Data Architecture for the Complete Module Board 10 should make the underlying architecture clear to Soft Labs.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor; Show) and no metric row",
  "purpose": "Provide final governance over the entire BI and analytics environment.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 133 §Monitor"
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
       "label": "Every analytics governance security",
       "columns": [
        "Dashboard Permissions",
        "Report Permissions",
        "Dataset Permissions",
        "KPI Changes",
        "Data Exports",
        "API Access",
        "AI Access",
        "Sensitive Data Usage",
        "Configuration Changes",
        "Administrative Actions",
        "AI Queries",
        "Blocked Queries",
        "Sensitive-Data Requests",
        "AI Cost",
        "Model Errors",
        "Low-Confidence Answers",
        "User Feedback"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 133 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected analytics governance security",
       "bindsTo": null,
       "columns": [
        "Dashboard Permissions",
        "Report Permissions",
        "Dataset Permissions",
        "KPI Changes",
        "Data Exports",
        "API Access",
        "AI Access",
        "Sensitive Data Usage",
        "Configuration Changes",
        "Administrative Actions",
        "AI Queries",
        "Blocked Queries",
        "Sensitive-Data Requests",
        "AI Cost",
        "Model Errors",
        "Low-Confidence Answers",
        "User Feedback"
       ],
       "notes": "The pack groups this record's detail under its own headings: “The desired structure is”, “Unified Data Integration Layer”, “Analytics Data Platform”, “Instead”, “Board 10 Benchmarking”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 133 §Monitor"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The analytics governance security list.",
   "error": "Could not load. Names which read failed and leaves the analytics governance security untouched.",
   "emptyFirstRun": "No analytics governance security yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the analytics governance security are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSecurityDetectionGovernance",
    "contract": "access",
    "purpose": "Security Analytics, AI Detection & Governance",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Dashboard Permissions",
    "Report Permissions",
    "Dataset Permissions",
    "KPI Changes",
    "Data Exports",
    "API Access"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-070",
   "workshopBoard": "wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-070"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 133. 0 of 17 labels bound to a contract property; 24 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
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
 "createKpi": {
  "method": "POST",
  "path": "/kpis",
  "contract": "reporting",
  "summary": "Define a KPI once, for everywhere",
  "permission": "REPORT_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "KpiDefinition",
  "responds": "KpiDefinition"
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
 "getAnalyticsUsage": {
  "method": "GET",
  "path": "/analytics-usage",
  "contract": "reporting",
  "summary": "Which dashboards and reports are actually used, and what they cost",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
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
  "responds": "AnalyticsUsageRow"
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
 "getSemanticModel": {
  "method": "GET",
  "path": "/semantic-model",
  "contract": "reporting",
  "summary": "The business data catalogue reports are built from",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SemanticModel"
 },
 "listAnalyticsPipelines": {
  "method": "GET",
  "path": "/analytics-pipelines",
  "contract": "reporting",
  "summary": "Data sources, refresh state and freshness",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AnalyticsPipeline"
 },
 "listDashboards": {
  "method": "GET",
  "path": "/dashboards",
  "contract": "reporting",
  "summary": "List dashboards",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "module",
    "in": "query",
    "required": false
   },
   {
    "name": "includeArchived",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "Dashboard"
 },
 "listKpis": {
  "method": "GET",
  "path": "/kpis",
  "contract": "reporting",
  "summary": "The enterprise KPI library",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "KpiDefinition"
 },
 "listSecurityDetectionGovernance": {
  "method": "GET",
  "path": "/security-detection-governance",
  "contract": "access",
  "summary": "Security Analytics, AI Detection & Governance",
  "permission": "REPORT_VIEW_VENUE",
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
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "park",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "reseller",
    "in": "query",
    "required": false
   },
   {
    "name": "credentialType",
    "in": "query",
    "required": false
   },
   {
    "name": "media",
    "in": "query",
    "required": false
   },
   {
    "name": "device",
    "in": "query",
    "required": false
   },
   {
    "name": "gate",
    "in": "query",
    "required": false
   },
   {
    "name": "timeDay",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "SecurityAnalyticsAiDetectionGovernanceView"
 },
 "listSiteNormalisationBases": {
  "method": "GET",
  "path": "/site-normalisation-bases",
  "contract": "reporting",
  "summary": "The denominators each site is benchmarked by",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "periodFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "periodTo",
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
 "setKpiTargets": {
  "method": "PUT",
  "path": "/kpis/{kpiId}/targets",
  "contract": "reporting",
  "summary": "Targets, thresholds and what red means",
  "permission": "REPORT_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiTarget"
 },
 "setSemanticModel": {
  "method": "PUT",
  "path": "/semantic-model",
  "contract": "reporting",
  "summary": "Publish the catalogue",
  "permission": "REPORT_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SemanticModel",
  "responds": "SemanticModel"
 },
 "setSiteNormalisationBasis": {
  "method": "PUT",
  "path": "/site-normalisation-bases",
  "contract": "reporting",
  "summary": "Set the denominators a site is benchmarked by",
  "permission": "REPORT_MANAGE",
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
  "responds": "SiteNormalisationBasis"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Aggregation": {
  "type": "string",
  "enum": [
   "none",
   "count",
   "countDistinct",
   "sum",
   "average",
   "min",
   "max"
  ]
 },
 "AnalyticsPipeline": {
  "type": "object",
  "x-ticvai-persistence": "reporting.pipeline",
  "description": "BI board 10.7. **Freshness decides whether a dashboard can be trusted.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "sourceKind": {
    "type": "string"
   },
   "datasets": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "schedule": {
    "type": "string",
    "nullable": true
   },
   "lastRunAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastSuccessAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "freshnessMinutes": {
    "type": "integer",
    "nullable": true
   },
   "expectedFreshnessMinutes": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "healthy",
     "degraded",
     "stale",
     "failed",
     "paused"
    ]
   },
   "lastError": {
    "type": "string",
    "nullable": true
   },
   "rowsLastRun": {
    "type": "integer",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AnalyticsUsageRow": {
  "type": "object",
  "description": "BI board 10.9. **The number that lets a BI estate be pruned.**",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "opens": {
    "type": "integer"
   },
   "distinctUsers": {
    "type": "integer"
   },
   "lastOpenedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "averageRuntimeMs": {
    "type": "integer",
    "nullable": true
   },
   "rowsScanned": {
    "type": "integer",
    "nullable": true
   },
   "neverOpened": {
    "type": "boolean"
   }
  }
 },
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
 "CreateDashboardRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "module",
   "tiles"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey",
    "description": "**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"
   },
   "isShared": {
    "type": "boolean",
    "default": false
   },
   "tiles": {
    "type": "array",
    "minItems": 1,
    "maxItems": 24,
    "items": {
     "$ref": "#/components/schemas/DashboardTile"
    }
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
 "FieldType": {
  "type": "string",
  "enum": [
   "string",
   "integer",
   "decimal",
   "money",
   "boolean",
   "date",
   "dateTime",
   "uuid",
   "enum"
  ]
 },
 "KpiDefinition": {
  "type": "object",
  "x-ticvai-persistence": "reporting.kpi_definition",
  "description": "BI boards 2.5 and 10.2. **One definition, referenced everywhere** — otherwise *revenue* means two things in the same meeting.\n",
  "required": [
   "code",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "description": "`takings` and `admissions` are seeded for every tenant as system KPIs (decided 28 September, audit R283), and the five accreditation KPIs for every tenant with the accreditation module (29 September, build pass). The seeded codes are `ReportingSystemKpi`.\n"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "domain": {
    "type": "string",
    "nullable": true
   },
   "formula": {
    "type": "string",
    "description": "**Expressed against the semantic model, not against tables.** A KPI written in SQL is a KPI that breaks when the warehouse is reshaped.\n"
   },
   "unit": {
    "type": "string",
    "enum": [
     "currency",
     "count",
     "percentage",
     "duration",
     "ratio",
     "score"
    ]
   },
   "higherIsBetter": {
    "type": "boolean",
    "default": true,
    "description": "**Refund rate and revenue both go up.** Without this the status colour is a coin toss.\n"
   },
   "defaultPeriod": {
    "type": "string",
    "nullable": true
   },
   "owner": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "KpiTarget": {
  "type": "object",
  "x-ticvai-persistence": "reporting.kpi_target",
  "description": "BI board 2.6. **The threshold is what turns a number into a status.**",
  "required": [
   "scopePath",
   "period",
   "target"
  ],
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "description": "The scope this target applies to. With `period`, the key `setKpiTargets` matches on."
   },
   "period": {
    "type": "string"
   },
   "target": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "amberAt": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "redAt": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "stretch": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
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
 "SecurityAnalyticsAiDetectionGovernanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Security Analytics, AI Detection & Governance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fraudAttempts": {
    "type": "integer",
    "description": "Fraud Attempts"
   },
   "preventedFraud": {
    "type": "integer",
    "description": "Prevented Fraud"
   },
   "credentialSharing": {
    "type": "integer",
    "description": "Credential Sharing"
   },
   "biometricAlerts": {
    "type": "integer",
    "description": "Biometric Alerts"
   },
   "deviceBindingViolations": {
    "type": "integer",
    "description": "Device-Binding Violations"
   },
   "companionViolations": {
    "type": "integer",
    "description": "Companion Violations"
   },
   "blacklistHits": {
    "type": "integer",
    "description": "Blacklist Hits"
   },
   "identityLocks": {
    "type": "integer",
    "description": "Identity Locks"
   },
   "securityOverrides": {
    "type": "integer",
    "description": "Security Overrides"
   },
   "detectionRate": {
    "type": "number",
    "description": "Detection Rate"
   },
   "falsePositiveIndicator": {
    "type": "number",
    "description": "False Positive Indicator"
   },
   "operatorOverrideRate": {
    "type": "number",
    "description": "Operator Override Rate"
   },
   "averageInvestigationTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "averageResponseTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "recurringFraudRate": {
    "type": "number",
    "description": "Recurring Fraud Rate"
   },
   "financialExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Financial Exposure"
   },
   "estimatedFraudPrevented": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated Fraud Prevented"
   },
   "duplicateUsage": {
    "type": "integer"
   }
  }
 },
 "SemanticModel": {
  "type": "object",
  "x-ticvai-persistence": "reporting.semantic_model",
  "description": "BI boards 3.3 and 10.6. **A vocabulary, not a schema.** Exposing joins to report authors produces reports that are wrong invisibly.\n",
  "properties": {
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "Assigned by the server on each publish."
   },
   "domains": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "description": {
       "type": "string",
       "nullable": true
      },
      "datasets": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "code": {
          "type": "string"
         },
         "name": {
          "type": "string"
         },
         "grain": {
          "type": "string",
          "description": "**What one row means.** The single most common cause of a wrong report is a join that silently multiplied the grain.\n"
         },
         "fields": {
          "type": "array",
          "items": {
           "type": "object",
           "properties": {
            "code": {
             "type": "string"
            },
            "label": {
             "type": "string"
            },
            "dataType": {
             "$ref": "#/components/schemas/FieldType"
            },
            "aggregation": {
             "allOf": [
              {
               "$ref": "#/components/schemas/Aggregation"
              }
             ],
             "nullable": true,
             "description": "The default aggregation for the field, where it has one."
            },
            "sensitive": {
             "type": "boolean",
             "default": false
            },
            "description": {
             "type": "string",
             "nullable": true
            }
           }
          }
         }
        }
       }
      }
     }
    }
   },
   "relationships": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "fromDataset": {
       "type": "string"
      },
      "toDataset": {
       "type": "string"
      },
      "cardinality": {
       "type": "string",
       "enum": [
        "oneToOne",
        "oneToMany",
        "manyToOne",
        "manyToMany"
       ]
      }
     }
    }
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "SiteNormalisationBasis": {
  "type": "object",
  "x-ticvai-persistence": "reporting.site_normalisation_basis",
  "description": "BI boards 7.9 and 10.4. **The denominators a benchmark divides by**, per site and period: visitors, operating hours, staffed positions and area, one for each `BenchmarkNormalisation` other than `none`. Read by `getAnalyticsBenchmark` for the period that covers the benchmark (data model, 29 September).\n",
  "required": [
   "scopePath",
   "periodStart",
   "periodEnd"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "description": "The site (venue scope) the basis applies to."
   },
   "periodStart": {
    "type": "string",
    "format": "date"
   },
   "periodEnd": {
    "type": "string",
    "format": "date"
   },
   "visitors": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "description": "`perVisitor`."
   },
   "operatingHours": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "description": "`perOperatingHour`."
   },
   "staffedPositions": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "description": "`perStaffedPosition`. Average positions staffed over the period."
   },
   "areaSquareMetres": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "description": "`perSquareMetre`. Operated area."
   }
  }
 }
}
```
