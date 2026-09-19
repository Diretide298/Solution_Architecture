# WS66 — Unified BI Reporting and AI Analytics Platform board 1

**9 screens · 0 operations · 0 schemas · 0 permissions**

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
| `ANL-012` | Live Operations Dashboard | commandCentre | 0 | 0 | — |
| `ANL-013` | Revenue Pulse | commandCentre | 0 | 0 | — |
| `ANL-014` | Attendance & Footfall Intelligence | commandCentre | 0 | 0 | — |
| `ANL-015` | Capacity & Utilization Monitor | commandCentre | 0 | 0 | — |
| `ANL-016` | Sales & Channel Performance | commandCentre | 0 | 0 | — |
| `ANL-017` | Customer, Membership & Loyalty Pulse | listDetail | 0 | 0 | — |
| `ANL-018` | Alerts & Exception Center | listDetail | 0 | 0 | — |
| `ANL-019` | AI Management Insights | listDetail | 0 | 0 | — |
| `ANL-020` | Multi-Site & Performance Comparison | commandCentre | 0 | 0 | — |

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
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a real-time view of what is happening across all operating locations.",
  "purposeNote": "Authorized operations users can identify the live status of each site and immediately drill into abnormal conditions.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-012"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 4. 0 of 0 labels bound to a contract property; 14 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
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
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide real-time visibility into revenue generation across TICVAI.",
  "purposeNote": "Management can identify revenue performance and drill down from consolidated revenue to site → business unit → channel → product → transaction level, subject to permissions.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-013"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 12 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
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
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Monitor visitor movement and attendance across venues.",
  "purposeNote": "Users can understand historical, current and forecast visitor volumes and drill into the underlying attendance data.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-014"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 15 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
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
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized monitoring of available and consumed capacity.",
  "purposeNote": "Users can identify underutilized, approaching-capacity and fully utilized locations/resources in real time.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-015"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 8 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
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
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide management with consolidated commercial performance across every sales channel.",
  "purposeNote": "Management can compare channel profitability and sales performance from one dashboard.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-016"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 12 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a consolidated view of customer health and engagement.",
  "purposeNote": "Authorized users can understand customer acquisition, engagement, retention, membership and loyalty performance without accessing separate CRM dashboards.",
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
  "apis": [],
  "entryState": {
   "preloaded": [
    "Unique Customers",
    "New Customers",
    "Returning Customers",
    "Repeat Visit %",
    "Average Customer Spend",
    "Customer Lifetime Value"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-017"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 8. 0 of 22 labels bound to a contract property; 22 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each Alert Shall Display) and no metric row",
  "purpose": "Create one centralized location for management-level KPI and operational exceptions.",
  "purposeNote": "Management can identify and manage important business exceptions from a centralized queue.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-018"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 9. 0 of 11 labels bound to a contract property; 11 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide management with proactive AI-generated business intelligence rather than requiring users to manually analyze every dashboard.",
  "purposeNote": "Users receive explainable, traceable AI insights linked to the underlying supporting data.",
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
   "regions": []
  },
  "states": {
   "loading": "The insights list.",
   "error": "Could not load. Names which read failed and leaves the insights untouched.",
   "emptyFirstRun": "No insights yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the insights are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-019"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
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
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Comparison KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow enterprise management to compare sites, venues, attractions and business units.",
  "purposeNote": "Management can benchmark operating entities using normalized KPIs and drill into the causes of performance differences.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-020"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 14 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
