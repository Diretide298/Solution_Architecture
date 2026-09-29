# WS66 — Unified BI Reporting and AI Analytics Platform board 1

**9 screens · 11 operations · 25 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_USE, PRICE_VIEW, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ANL-012` | Live Operations Dashboard | commandCentre | 2 | 0 | — |
| `ANL-013` | Revenue Pulse | commandCentre | 1 | 0 | — |
| `ANL-014` | Attendance & Footfall Intelligence | commandCentre | 1 | 0 | — |
| `ANL-015` | Capacity & Utilization Monitor | commandCentre | 1 | 0 | — |
| `ANL-016` | Sales & Channel Performance | commandCentre | 1 | 0 | — |
| `ANL-017` | Customer, Membership & Loyalty Pulse | listDetail | 2 | 0 | — |
| `ANL-018` | Alerts & Exception Center | listDetail | 1 | 0 | — |
| `ANL-019` | AI Management Insights | listDetail | 5 | 0 | — |
| `ANL-020` | Multi-Site & Performance Comparison | commandCentre | 2 | 0 | — |

## Thin screens in this batch

**ANL-018, ANL-019 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-012",
  "name": "Live Operations Dashboard",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "2",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/live-operations-dashboard-anl-012",
   "component": "apps/venue-management-web/src/routes/analytics/LiveOperationsDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-020"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-020"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Back to Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-012 holds none of them, so the edge carries nothing and ANL-001 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized operations users can identify the live status of each site and immediately drill into abnormal conditions.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a real-time view of what is happening across all operating locations.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Visitors currently on-site",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Entries today",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Exits today",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Current occupancy",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Capacity remaining",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Occupancy %",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Active gates",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Gate status",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Active POS terminals",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Active sessions/timeslots",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Current queues",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Resource utilization",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Operational incidents",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "System/device exceptions",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 4 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the live operations untouched.",
   "emptyFirstRun": "No live operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Live operational KPIs",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What needs attention",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Visitors currently on-site",
    "Entries today",
    "Exits today",
    "Current occupancy",
    "Capacity remaining",
    "Occupancy %"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-012",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-012"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 4. 0 of 0 labels bound to a contract property; 14 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-013",
  "name": "Revenue Pulse",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "3",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/revenue-pulse-anl-013",
   "component": "apps/venue-management-web/src/routes/analytics/RevenuePulse.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-020"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-020"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Back to Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-013 holds none of them, so the edge carries nothing and ANL-001 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can identify revenue performance and drill down from consolidated revenue to site → business unit → channel → product → transaction level, subject to permissions.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide real-time visibility into revenue generation across TICVAI.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Revenue Today",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue This Hour",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue vs Target",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue vs Yesterday",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue vs Same Day Last Week",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue vs Same Period Last Year",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue by Site",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue by Attraction",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue by Product",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue by Channel",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue by Business Unit",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Revenue by Payment Method",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 5 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue pulse list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the revenue pulse untouched.",
   "emptyFirstRun": "No revenue pulse yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue pulse are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Revenue against target",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Revenue Today",
    "Revenue This Hour",
    "Revenue vs Target",
    "Revenue vs Yesterday",
    "Revenue vs Same Day Last Week",
    "Revenue vs Same Period Last Year"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-013",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-013"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 12 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-014",
  "name": "Attendance & Footfall Intelligence",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "4",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/attendance-footfall-intelligence-anl-014",
   "component": "apps/venue-management-web/src/routes/analytics/AttendanceFootfallIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-020"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-020"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Back to Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-014 holds none of them, so the edge carries nothing and ANL-001 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can understand historical, current and forecast visitor volumes and drill into the underlying attendance data.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Monitor visitor movement and attendance across venues.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Visitors",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Current Visitors On-Site",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Entry Count",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Exit Count",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Hourly Footfall",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Peak Entry Time",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Average Visit Duration",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Attendance by Site",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Attendance by Attraction",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Attendance by Ticket Type",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Attendance by Product",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Attendance by Timeslot",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Repeat Visits",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "No-Show %",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Ticketed vs Actual Attendance",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 6 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attendance footfall intelligence list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the attendance footfall intelligence untouched.",
   "emptyFirstRun": "No attendance footfall intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attendance footfall intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Attendance and footfall",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total Visitors",
    "Current Visitors On-Site",
    "Entry Count",
    "Exit Count",
    "Hourly Footfall",
    "Peak Entry Time"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-014",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-014"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 15 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-015",
  "name": "Capacity & Utilization Monitor",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "5",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/capacity-utilization-monitor-anl-015",
   "component": "apps/venue-management-web/src/routes/analytics/CapacityUtilizationMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-020"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-020"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Back to Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-015 holds none of them, so the edge carries nothing and ANL-001 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can identify underutilized, approaching-capacity and fully utilized locations/resources in real time.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized monitoring of available and consumed capacity.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Available Capacity",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Booked Capacity",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Used Capacity",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Remaining Capacity",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Utilization %",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "No-Show %",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Peak Utilization",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Utilization",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity utilization list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the capacity utilization untouched.",
   "emptyFirstRun": "No capacity utilization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the capacity utilization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Capacity and utilisation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Available Capacity",
    "Booked Capacity",
    "Used Capacity",
    "Remaining Capacity",
    "Utilization %",
    "No-Show %"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-015",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-015"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 8 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-016",
  "name": "Sales & Channel Performance",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "6",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/sales-channel-performance-anl-016",
   "component": "apps/venue-management-web/src/routes/analytics/SalesChannelPerformance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-020"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-020"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Back to Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-016 holds none of them, so the edge carries nothing and ANL-001 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can compare channel profitability and sales performance from one dashboard.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide management with consolidated commercial performance across every sales channel.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Gross Sales",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Net Sales",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Transactions",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Tickets Sold",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Order Value",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Conversion Rate",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Discount Value",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Refunds",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Cancellations",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Commission",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Upsell Revenue",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Cross-Sell Revenue",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 7 §KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sales channel performance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the sales channel performance untouched.",
   "emptyFirstRun": "No sales channel performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sales channel performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Sales by channel",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Gross Sales",
    "Net Sales",
    "Transactions",
    "Tickets Sold",
    "Average Order Value",
    "Conversion Rate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-016",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-016"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 12 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-017",
  "name": "Customer, Membership & Loyalty Pulse",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "7",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/customer-membership-loyalty-pulse-anl-017",
   "component": "apps/venue-management-web/src/routes/analytics/CustomerMembershipLoyaltyPulse.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-020"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-020"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Back to Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-017 holds dashboardId, reportId, so an edge into it carries them"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can understand customer acquisition, engagement, retention, membership and loyalty performance without accessing separate CRM dashboards.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a consolidated view of customer health and engagement.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 8 §Display"
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
       "label": "Search customer membership loyalty",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 8 §Allow filtering by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Customer segment",
        "Membership type",
        "Geography",
        "Demographic group",
        "Acquisition source",
        "Visit frequency",
        "Spend tier"
       ],
       "notes": "The pack filters this screen by customer segment, membership type, geography, demographic group, acquisition source, visit frequency and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 8 §Allow filtering by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every customer membership loyalty",
       "columns": [
        "Unique Customers",
        "New Customers",
        "Returning Customers",
        "Repeat Visit %",
        "Average Customer Spend",
        "Customer Lifetime Value",
        "Active Members",
        "New Memberships",
        "Membership Renewals",
        "Membership Expiring",
        "Loyalty Members",
        "Loyalty Earn",
        "Loyalty Burn",
        "Outstanding Loyalty Liability",
        "Customer Satisfaction Score"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 8 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer membership loyalty",
       "bindsTo": null,
       "columns": [
        "Unique Customers",
        "New Customers",
        "Returning Customers",
        "Repeat Visit %",
        "Average Customer Spend",
        "Customer Lifetime Value",
        "Active Members",
        "New Memberships",
        "Membership Renewals",
        "Membership Expiring",
        "Loyalty Members",
        "Loyalty Earn",
        "Loyalty Burn",
        "Outstanding Loyalty Liability",
        "Customer Satisfaction Score"
       ],
       "notes": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 8 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer membership loyalty list.",
   "error": "Could not load. Names which read failed and leaves the customer membership loyalty untouched.",
   "emptyFirstRun": "No customer membership loyalty yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer membership loyalty are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Membership and loyalty",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Loyalty dashboard (active members, tiers, liability, breakage, retention)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Unique Customers",
    "New Customers",
    "Returning Customers",
    "Repeat Visit %",
    "Average Customer Spend",
    "Customer Lifetime Value"
   ],
   "params": [
    {
     "name": "dashboardId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-017",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-017"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 8. 0 of 22 labels bound to a contract property; 22 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-018",
  "name": "Alerts & Exception Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "8",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/alerts-exception-center-anl-018",
   "component": "apps/venue-management-web/src/routes/analytics/AlertsExceptionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-020"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-020"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Back to Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-018 holds none of them, so the edge carries nothing and ANL-001 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can identify and manage important business exceptions from a centralized queue.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each Alert Shall Display) and no metric row",
  "purpose": "Create one centralized location for management-level KPI and operational exceptions.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 9 §Each Alert Shall Display"
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
       "label": "Every alerts exception",
       "columns": [
        "Severity",
        "KPI",
        "Current value",
        "Expected/target value",
        "Variance",
        "Site",
        "Detection time",
        "Source system",
        "Owner",
        "Status",
        "Recommended action"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 9 §Each Alert Shall Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected alerts exception",
       "bindsTo": null,
       "columns": [
        "Severity",
        "KPI",
        "Current value",
        "Expected/target value",
        "Variance",
        "Site",
        "Detection time",
        "Source system",
        "Owner",
        "Status",
        "Recommended action"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Alert Categories”, “Alert Workflow”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 9 §Each Alert Shall Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The alerts exception list.",
   "error": "Could not load. Names which read failed and leaves the alerts exception untouched.",
   "emptyFirstRun": "No alerts exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the alerts exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionAlertException",
    "contract": "promotions",
    "purpose": "Promotion Alerts & Exception Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Severity",
    "KPI",
    "Current value",
    "Expected/target value",
    "Variance",
    "Site"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-018",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-018"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 9. 0 of 11 labels bound to a contract property; 11 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-019",
  "name": "AI Management Insights",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "9",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-management-insights-anl-019",
   "component": "apps/venue-management-web/src/routes/analytics/AiManagementInsights.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-020"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-020"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Back to Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-019 holds none of them, so the edge carries nothing and ANL-001 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users receive explainable, traceable AI insights linked to the underlying supporting data.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide management with proactive AI-generated business intelligence rather than requiring users to manually analyze every dashboard.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 10"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 10"
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
       "impliedBy": "askReportingQuestion",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAnalyticsAnomalies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
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
   "loading": "The insights list.",
   "error": "Could not load. Names which read failed and leaves the insights untouched.",
   "emptyFirstRun": "No insights yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the insights are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Ask about what moved",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAnalyticsAnomalies",
    "contract": "reporting",
    "purpose": "What moved unexpectedly",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAiInsights",
    "contract": "ai",
    "purpose": "Insights and anomalies",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideAiInsight",
    "contract": "ai",
    "purpose": "Review, accept, reject or mark an insight actioned",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "explainMetricChange",
    "contract": "ai",
    "purpose": "Why did this metric change",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-019",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-019"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "insightId",
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
  "id": "ANL-020",
  "name": "Multi-Site & Performance Comparison",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/multi-site-performance-comparison-anl-020",
   "component": "apps/venue-management-web/src/routes/analytics/MultiSitePerformanceComparison.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-012",
    "ANL-013",
    "ANL-014",
    "ANL-015",
    "ANL-016",
    "ANL-017",
    "ANL-018",
    "ANL-019"
   ],
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Back to Executive Command Center",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-012",
     "trigger": "Live Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-013",
     "trigger": "Revenue Pulse",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-014",
     "trigger": "Attendance & Footfall Intelligence",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-015",
     "trigger": "Capacity & Utilization Monitor",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-016",
     "trigger": "Sales & Channel Performance",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-017",
     "trigger": "Customer, Membership & Loyalty Pulse",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-018",
     "trigger": "Alerts & Exception Center",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-019",
     "trigger": "AI Management Insights",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can benchmark operating entities using normalized KPIs and drill into the causes of performance differences.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Comparison KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow enterprise management to compare sites, venues, attractions and business units.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Revenue",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Growth",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Attendance",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Capacity Utilization",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per Visitor",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Transaction Value",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Conversion",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Refund %",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Membership Conversion",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Repeat Visitor %",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Customer Satisfaction",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "F&B Spend",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Retail Spend",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Operational Exceptions",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 11 §Comparison KPIs"
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
    }
   ]
  },
  "states": {
   "loading": "The multi-site performance comparison list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the multi-site performance comparison untouched.",
   "emptyFirstRun": "No multi-site performance comparison yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-site performance comparison are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAnalyticsBenchmark",
    "contract": "reporting",
    "purpose": "Site against site, normalised",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSiteNormalisationBases",
    "contract": "reporting",
    "purpose": "The denominators each site is benchmarked by",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Revenue",
    "Revenue Growth",
    "Attendance",
    "Capacity Utilization",
    "Revenue per Visitor",
    "Average Transaction Value"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-020",
   "workshopBoard": "wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-020"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 14 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "decideAiInsight": {
  "method": "POST",
  "path": "/insights/{insightId}/decide",
  "contract": "ai",
  "summary": "Review, accept, reject or mark an insight actioned",
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
  "responds": "AiInsight"
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
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
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
   },
   {
    "name": "severity",
    "in": "query",
    "required": null
   },
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "itemId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Alert"
 },
 "listAnalyticsAnomalies": {
  "method": "GET",
  "path": "/analytics-anomalies",
  "contract": "reporting",
  "summary": "Numbers that moved more than they should have",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "severity",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AnalyticsAnomaly"
 },
 "listPromotionAlertException": {
  "method": "GET",
  "path": "/promotion-alert-exception",
  "contract": "promotions",
  "summary": "Promotion Alerts & Exception Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionAlertsExceptionCenterView"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
   "ruleName": {
    "type": "string",
    "description": "`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"
   },
   "metric": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricSource"
     }
    ],
    "description": "The rule's metric, carried so the alert says what went out of range."
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "severity": {
    "$ref": "#/components/schemas/AlertSeverity"
   },
   "status": {
    "$ref": "#/components/schemas/AlertStatus"
   },
   "observedValue": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "threshold": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "scopePath": {
    "type": "string"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."
   },
   "shiftId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."
   },
   "itemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"
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
   "acknowledgementNote": {
    "type": "string",
    "maxLength": 300,
    "nullable": true,
    "description": "The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."
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
 "AlertSeverity": {
  "type": "string",
  "description": "How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.",
  "enum": [
   "info",
   "warning",
   "critical"
  ]
 },
 "AlertStatus": {
  "type": "string",
  "description": "Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.",
  "enum": [
   "raised",
   "acknowledged",
   "resolved",
   "expired"
  ]
 },
 "AnalyticsAnomaly": {
  "type": "object",
  "x-ticvai-persistence": "reporting.anomaly",
  "description": "BI boards 9.5 and 9.6. **A departure from the series' own behaviour**, which catches what no threshold was set for.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kpiId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "metric": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time"
   },
   "observed": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "expected": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "deviationSigma": {
    "type": "number",
    "nullable": true
   },
   "severity": {
    "$ref": "#/components/schemas/AnomalySeverity"
   },
   "candidateCauses": {
    "type": "array",
    "description": "**The beginning of the question, not the end of it.**",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string"
      },
      "value": {
       "type": "string"
      },
      "contribution": {
       "type": "number"
      }
     }
    }
   },
   "acknowledgedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "acknowledgedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "AnomalySeverity": {
  "type": "string",
  "description": "Shared by `AnalyticsAnomaly` and the `listAnalyticsAnomalies` filter.",
  "enum": [
   "low",
   "medium",
   "high"
  ]
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
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
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
   },
   "compiledSql": {
    "type": "string",
    "nullable": true,
    "description": "The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"
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
 "MetricSource": {
  "type": "string",
  "description": "**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n",
  "enum": [
   "occupancy",
   "capacityUtilisation",
   "admissionRate",
   "noShowRate",
   "conversion",
   "salesByOperator",
   "salesByWorkstation",
   "waitTime",
   "throughput",
   "abandonmentRate",
   "inventoryValuation",
   "stockTurnover",
   "stockAgeing",
   "wastageRate",
   "resaleVolume",
   "resaleCommission",
   "salesByInstructor",
   "resourceUtilisation",
   "allocationUtilisation",
   "channelAllocationBurn",
   "membershipChurn",
   "membershipRenewalRate",
   "supplierDeliveryPerformance",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "assetDowntime",
   "meanTimeToRepair",
   "challengeCompletionRate",
   "attributedRevenue",
   "loyaltyActiveMembers",
   "loyaltyTierDistribution",
   "loyaltyPointsLiability",
   "loyaltyBreakageRate",
   "loyaltyMemberRetention",
   "challengeParticipationRate",
   "gamificationLoyaltyImpact",
   "gamificationMembershipImpact",
   "gamificationRetention",
   "accreditationApplications",
   "accreditationTimeToDecision",
   "accreditationCredentialsIssued",
   "accreditationActiveHolders",
   "accreditationRenewalsDue",
   "staffingShortfall"
  ],
  "x-ticvai-money-valued": [
   "inventoryValuation",
   "resaleCommission",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "attributedRevenue",
   "loyaltyPointsLiability"
  ],
  "x-ticvai-extended-29-september": "**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n",
  "x-ticvai-money-valued-note": "**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n",
  "x-ticvai-extended": "18 August 2026",
  "x-ticvai-extension-note": "**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"
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
   "reliability"
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
    "description": "What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."
   },
   "semanticSpec": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingSemanticQuerySpec"
     }
    ],
    "nullable": true,
    "description": "What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"
   },
   "generatedQuery": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GeneratedQuery"
     }
    ],
    "nullable": true,
    "description": "The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"
   },
   "result": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportResult"
     }
    ],
    "nullable": true,
    "description": "Null when the question is outside the semantic model."
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."
   },
   "reliability": {
    "$ref": "#/components/schemas/ReportingAnswerReliability"
   },
   "unavailableReason": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingUnavailableReason"
     }
    ],
    "nullable": true,
    "description": "Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "deprecated": true,
    "description": "Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."
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
 "PromotionAlertsExceptionCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Alerts & Exception Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "alertType": {
    "type": "string",
    "enum": [
     "missingProduct",
     "missingEligibility",
     "invalidDates",
     "invalidDiscount",
     "invalidCode",
     "missingApproval",
     "budgetNearLimit",
     "budgetExceeded",
     "marginBelowThreshold",
     "excessiveDiscountExposure",
     "promotionFailedToPublish",
     "productUnavailable",
     "bundleComponentUnavailable",
     "channelSynchronizationFailure",
     "lowConversion",
     "lowRedemption",
     "unexpectedHighRedemption",
     "campaignUnderperforming",
     "abnormalCouponUsage",
     "excessiveRepeatRedemption",
     "suspiciousCustomerBehavior",
     "promoCodeLeakage"
    ],
    "description": "What the alert is about."
   },
   "severity": {
    "type": "string",
    "enum": [
     "information",
     "warning",
     "critical"
    ],
    "description": "Alert severity."
   },
   "alertId": {
    "type": "string",
    "description": "Alert ID"
   },
   "promotionId": {
    "type": "string",
    "description": "Promotion ID"
   },
   "alertCategory": {
    "type": "string",
    "enum": [
     "configuration",
     "financial",
     "operational",
     "commercial",
     "fraudRisk"
    ],
    "description": "The pack's alert group."
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the alert was raised"
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
 "ReportingAnswerReliability": {
  "type": "string",
  "description": "**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n",
  "enum": [
   "grounded",
   "partial",
   "conflictingSources",
   "insufficientEvidence"
  ]
 },
 "ReportingSemanticQuerySpec": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n",
  "required": [
   "metric",
   "period"
  ],
  "properties": {
   "metric": {
    "type": "string",
    "description": "A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."
   },
   "dimensions": {
    "type": "array",
    "maxItems": 5,
    "description": "Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.",
    "items": {
     "type": "string"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "operator"
     ],
     "properties": {
      "field": {
       "type": "string",
       "description": "A `SemanticModel` field code."
      },
      "operator": {
       "type": "string",
       "enum": [
        "equals",
        "notEquals",
        "greaterThan",
        "lessThan",
        "between",
        "in",
        "notIn",
        "isNull",
        "isNotNull"
       ]
      },
      "values": {
       "type": "array",
       "description": "**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n",
       "items": {}
      }
     }
    }
   },
   "period": {
    "type": "string",
    "description": "ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."
   },
   "comparison": {
    "type": "string",
    "nullable": true,
    "description": "As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.",
    "enum": [
     "previousPeriod",
     "samePeriodLastYear",
     "target",
     "benchmark"
    ]
   },
   "semanticModelVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."
   }
  }
 },
 "ReportingUnavailableReason": {
  "type": "string",
  "description": "Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.",
  "enum": [
   "metricNotModelled",
   "dimensionNotModelled",
   "filterNotModelled",
   "comparisonNotAvailable",
   "periodOutsideHistory"
  ]
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
