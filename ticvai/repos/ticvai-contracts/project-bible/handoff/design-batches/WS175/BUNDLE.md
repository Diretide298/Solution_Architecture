# WS175 — Seat Management Venue Mapping Reference v1.0 board 11

**10 screens · 9 operations · 25 schemas · 5 permissions**

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
  `CAPACITY_CONFIGURE, PRODUCT_VIEW, REPORT_EXPORT, REPORT_MANAGE, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1051` | Seat Analytics Command Center | listDetail | 1 | 0 | — |
| `BO-1052` | Occupancy Reporting | listDetail | 1 | 0 | — |
| `BO-1053` | Zone Performance Reporting | listDetail | 1 | 0 | — |
| `BO-1054` | Revenue by Section | listDetail | 1 | 0 | — |
| `BO-1055` | Revenue by Seat Category | listDetail | 1 | 0 | — |
| `BO-1056` | Seat Utilization Analytics | listDetail | 1 | 0 | — |
| `BO-1057` | Hold Inventory Reporting | listDetail | 1 | 0 | — |
| `BO-1058` | Sales Pace & Pick Curves | listDetail | 1 | 0 | — |
| `BO-1059` | Heat Maps & Drill-Down | listDetail | 2 | 0 | — |
| `BO-1060` | Report Builder, Export & Audit | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-1051, BO-1055, BO-1057, BO-1058, BO-1059, BO-1060 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1051",
  "name": "Seat Analytics Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "01",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-analytics-command-center-bo-1051",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatAnalyticsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1052",
    "BO-1053",
    "BO-1054",
    "BO-1055",
    "BO-1056",
    "BO-1057",
    "BO-1058",
    "BO-1059",
    "BO-1060"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1052",
     "trigger": "Occupancy Reporting",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-1053",
     "trigger": "Zone Performance Reporting",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-1054",
     "trigger": "Revenue by Section",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-1055",
     "trigger": "Revenue by Seat Category",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-1056",
     "trigger": "Seat Utilization Analytics",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-1057",
     "trigger": "Hold Inventory Reporting",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-1058",
     "trigger": "Sales Pace & Pick Curves",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-1059",
     "trigger": "Heat Maps & Drill-Down",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-1060",
     "trigger": "Report Builder, Export & Audit",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a consolidated view of seat commercial and operational performance. Show occupancy, revenue, utilization, average ticket price, held inventory, release yield and forecast variance. Present trend, benchmark, target and prior-period comparison by tenant, venue and event. Surface low occupancy, excessive holds, inventory conflict, price variance and data-quality alerts. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 46"
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
       "impliedBy": "listSeats",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat analytics list.",
   "error": "Could not load. Names which read failed and leaves the seat analytics untouched.",
   "emptyFirstRun": "No seat analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeats",
    "contract": "seating",
    "purpose": "List seats in a map",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1051",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1051"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable."
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
  "id": "BO-1052",
  "name": "Occupancy Reporting",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "02",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/occupancy-reporting-bo-1052",
   "component": "apps/venue-management-web/src/routes/access-venue/OccupancyReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Report sold and attended occupancy against configured capacity. Calculate sold, issued, scanned, no-show, blocked, available and effective capacity with clear metric definitions. Analyze by event, performance, venue, section, category, channel and time. Compare events and periods and drill to approved seat-level evidence. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 46"
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
       "label": "Scope",
       "operation": "getKpiValues",
       "notes": "Sends `?scopePath=` (venue, event).",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Period",
       "operation": "getKpiValues",
       "notes": "Sends `?period=`.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Compare to",
       "operation": "getKpiValues",
       "notes": "Sends `?compareTo=`.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Sold occupancy",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.target",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "Needs a sold-occupancy KPI code; not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "metricTile",
       "label": "Scanned occupancy",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.target",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "Needs a scanned-occupancy KPI code; not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "metricTile",
       "label": "No-shows",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "Needs a no-show KPI code; not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Occupancy measures",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.name",
        "KpiValue.scopePath",
        "KpiValue.period",
        "KpiValue.value",
        "KpiValue.target",
        "KpiValue.comparison",
        "KpiValue.variancePercent",
        "KpiValue.status",
        "KpiValue.asOf"
       ],
       "operation": "getKpiValues",
       "notes": "Sold, issued, scanned, no-show, blocked, available and effective capacity, one KPI per row.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The occupancy reporting list.",
   "error": "Could not load. Names which read failed and leaves the occupancy reporting untouched.",
   "emptyFirstRun": "No occupancy reporting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the occupancy reporting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Occupancy KPIs",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1052",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1052"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from contract reporting.yaml GET /kpi-values. Pack labels with no schema field yet (shown as plain labels): KPI codes not seeded: sold, issued, scanned, no-show, blocked, available, effective capacity, Breakdown by section, category, channel, Seat-level evidence drill-down.",
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
  "id": "BO-1053",
  "name": "Zone Performance Reporting",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "03",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/zone-performance-reporting-bo-1053",
   "component": "apps/venue-management-web/src/routes/access-venue/ZonePerformanceReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Compare capacity, demand and yield across venue zones. Show zone capacity, sold, occupancy, average price, revenue, utilization, holds and release conversion. Rank zones and compare target, forecast, prior period and venue benchmark. Drill from zone to section, row and seat while preserving the selected metric and filters. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 46",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 46"
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
       "label": "Scope",
       "operation": "getKpiValues",
       "notes": "Sends `?scopePath=`; a zone is reachable only if zones are scope paths.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Period",
       "operation": "getKpiValues",
       "notes": "Sends `?period=`.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Compare to",
       "operation": "getKpiValues",
       "notes": "Sends `?compareTo=`; target, benchmark or prior period.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Zone occupancy",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "Needs a zone-occupancy KPI code; not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "metricTile",
       "label": "Zone revenue",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "Needs a zone-revenue KPI code; `takings` is venue-wide.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Zone ranking",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.scopePath",
        "KpiValue.name",
        "KpiValue.value",
        "KpiValue.target",
        "KpiValue.comparison",
        "KpiValue.variancePercent",
        "KpiValue.direction",
        "KpiValue.status"
       ],
       "operation": "getKpiValues",
       "notes": "Ranked by value; one KPI at a time.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The zone performance reporting list.",
   "error": "Could not load. Names which read failed and leaves the zone performance reporting untouched.",
   "emptyFirstRun": "No zone performance reporting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the zone performance reporting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "By zone",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1053",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1053"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from contract reporting.yaml GET /kpi-values. Pack labels with no schema field yet (shown as plain labels): KPI codes not seeded: zone capacity, sold, occupancy, average price, revenue, utilization, holds, release conversion, Zone as a scope level, Rank, Forecast comparison, Drill from zone to section, row, seat.",
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
  "id": "BO-1054",
  "name": "Revenue by Section",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "04",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/revenue-by-section-bo-1054",
   "component": "apps/venue-management-web/src/routes/access-venue/RevenueBySection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Analyze financial contribution from each seating section. Report gross/net revenue, tax, fees, discounts, refunds, average ticket price and percentage of performance total. Compare section revenue, yield, occupancy, price band and prior-year/forecast variance. Link summarized values to governed finance/order detail and reconciliation status. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
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
       "label": "Performance scope",
       "operation": "getKpiValues",
       "notes": "Sends `?scopePath=`.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Period",
       "operation": "getKpiValues",
       "notes": "Sends `?period=`.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Compare to",
       "operation": "getKpiValues",
       "notes": "Sends `?compareTo=`; samePeriodLastYear gives the pack's prior-year variance.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Net revenue",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "`takings` is the only seeded money KPI.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "metricTile",
       "label": "Average ticket price",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "Needs an average-ticket-price KPI code; not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Revenue by section",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.scopePath",
        "KpiValue.name",
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.variancePercent",
        "KpiValue.status",
        "Section",
        "Gross revenue",
        "Tax",
        "Fees",
        "Discounts",
        "Refunds",
        "% of performance total",
        "Reconciliation status"
       ],
       "operation": "getKpiValues",
       "notes": "KpiValue has no section dimension; the section columns are pack labels.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue section list.",
   "error": "Could not load. Names which read failed and leaves the revenue section untouched.",
   "emptyFirstRun": "No revenue section yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue section are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Revenue by section",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1054",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1054"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.47; contract reporting.yaml GET /kpi-values. Pack labels with no schema field yet (shown as plain labels): Section dimension, Gross revenue, Tax, Fees, Discounts, Refunds, % of performance total, Yield, Price band, Reconciliation status.",
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
  "id": "BO-1055",
  "name": "Revenue by Seat Category",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "05",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/revenue-by-seat-category-bo-1055",
   "component": "apps/venue-management-web/src/routes/access-venue/RevenueBySeatCategory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure performance of Premium, Standard, Value, Accessible and configured categories. Show revenue mix, seats sold, average price, discount, refund, yield and sell-through by category. Compare venue, event, performance, channel, customer segment and days to event. Preserve accessible-category privacy and prevent misleading comparison caused by protected inventory rules. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
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
       "impliedBy": "listSeatCategories",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue seat category list.",
   "error": "Could not load. Names which read failed and leaves the revenue seat category untouched.",
   "emptyFirstRun": "No revenue seat category yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue seat category are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatCategories",
    "contract": "seating",
    "purpose": "List seat categories",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1055",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1055"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1056",
  "name": "Seat Utilization Analytics",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "06",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-utilization-analytics-bo-1056",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatUtilizationAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure how effectively physical and sellable seating capacity is used. Calculate booked, sold, scanned, occupied estimate, idle and unavailable hours or performances as applicable. Analyze utilization by venue, map, section, seat type, day, time and event category. Identify permanently underused areas, recurring blocks, maintenance patterns and lost-sale opportunities. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
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
       "label": "Scope",
       "operation": "getKpiValues",
       "notes": "Sends `?scopePath=`.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Period",
       "operation": "getKpiValues",
       "notes": "Sends `?period=`.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Seat utilization",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.target",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "Needs a seat-utilization KPI code; not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "metricTile",
       "label": "Idle seat-performances",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.comparison"
       ],
       "operation": "getKpiValues",
       "notes": "Needs an idle KPI code; not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Utilization measures",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.name",
        "KpiValue.scopePath",
        "KpiValue.period",
        "KpiValue.value",
        "KpiValue.target",
        "KpiValue.variancePercent",
        "KpiValue.status",
        "KpiValue.stale"
       ],
       "operation": "getKpiValues",
       "notes": "Booked, sold, scanned, occupied estimate, idle and unavailable.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "chart",
       "label": "Underused areas",
       "columns": [
        "Section",
        "Seat type",
        "Day",
        "Time",
        "Utilization"
       ],
       "notes": "Permanently underused areas, recurring blocks and maintenance patterns; KpiValue has no section, seat-type or time-of-day dimension.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat utilization analytics list.",
   "error": "Could not load. Names which read failed and leaves the seat utilization analytics untouched.",
   "emptyFirstRun": "No seat utilization analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat utilization analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Seat utilisation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1056",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1056"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.47; contract reporting.yaml GET /kpi-values. Pack labels with no schema field yet (shown as plain labels): KPI codes not seeded: booked, sold, scanned, occupied estimate, idle, unavailable, Breakdown by map, section, seat type, day, time, event category, Lost-sale opportunities.",
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
  "id": "BO-1057",
  "name": "Hold Inventory Reporting",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "07",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hold-inventory-reporting-bo-1057",
   "component": "apps/venue-management-web/src/routes/access-venue/HoldInventoryReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Report the size, age and outcome of seat holds. Show held quantity/value, capacity percentage, active age, upcoming release, conversion and expired unused. Compare VIP, Sponsor, Artist, Media, Corporate, Internal and custom types by owner/stakeholder. Measure released-to-sold outcomes and potential revenue suppressed by late or unused holds. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
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
       "impliedBy": "listInventoryHolds",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hold inventory reporting list.",
   "error": "Could not load. Names which read failed and leaves the hold inventory reporting untouched.",
   "emptyFirstRun": "No hold inventory reporting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hold inventory reporting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listInventoryHolds",
    "contract": "catalogue",
    "purpose": "List leases",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1057",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1057"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1058",
  "name": "Sales Pace & Pick Curves",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "08",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/sales-pace-pick-curves-bo-1058",
   "component": "apps/venue-management-web/src/routes/access-venue/SalesPacePickCurves.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Analyze when seats sell and which inventory customers select first. Plot cumulative sales by days/hours to event against target, forecast and comparable events. Configuration Scope of Work | Version 1.0 47 Show seat-pick sequence by section, row, price, view and channel and identify preferred inventory patterns. Support cohort comparison and expose sufficient sample and confidence information for decisions. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 47"
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
       "impliedBy": "listDemandBookingCurve",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sales pace pick list.",
   "error": "Could not load. Names which read failed and leaves the sales pace pick untouched.",
   "emptyFirstRun": "No sales pace pick yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sales pace pick are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDemandBookingCurve",
    "contract": "catalogue",
    "purpose": "Sales pace and pick curve",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1058",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1058"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1059",
  "name": "Heat Maps & Drill-Down",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "09",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/heat-maps-drill-down-bo-1059",
   "component": "apps/venue-management-web/src/routes/access-venue/HeatMapsDrillDown.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Visualize spatial performance directly on the approved seat map. Display occupancy, revenue, average price, demand, availability, holds, scan and utilization heat maps. Switch level, section, row and seat granularity and synchronize filters with tables and charts. Open the supporting transactions where authorized and show metric definition, source and refresh time. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 48"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 48"
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
       "impliedBy": "runReport",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "runReport"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The heat maps drill-down list.",
   "error": "Could not load. Names which read failed and leaves the heat maps drill-down untouched.",
   "emptyFirstRun": "No heat maps drill-down yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the heat maps drill-down are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatInventory",
    "contract": "seating",
    "purpose": "The map behind the heat",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Drill down",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1059",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1059"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 48. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "reportId",
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
  "id": "BO-1060",
  "name": "Report Builder, Export & Audit",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "11",
   "number": "10",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/report-builder-export-audit-bo-1060",
   "component": "apps/venue-management-web/src/routes/access-venue/ReportBuilderExportAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1051"
   ],
   "exitTo": [
    "BO-1051"
   ],
   "transitions": [
    {
     "to": "BO-1051",
     "trigger": "Back to Seat Analytics Command Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized users to assemble and distribute controlled seat reports. Select approved dimensions, measures, filters, grouping, sorting, chart/map and date context. Save personal/team views and schedule email or in-app delivery with recipient and permission validation. Export CSV, XLSX or PDF subject to policy and log report definition, recipients, downloads and sensitive access. Metrics shall use versioned definitions and authoritative sources; row/seat and guest-level drill-down, exports and subscriptions follow RBAC/PBAC and data-retention rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 48 Board 12 - Multi-Tenant & Venue Configuration Figure 12. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 49",
  "gaps": [
   {
    "operation": null,
    "why": "**Report Builder, Export & Audit declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 48"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 48"
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
       "impliedBy": "createReport",
       "label": "Create report",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createReport"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report export audit list.",
   "error": "Could not load. Names which read failed and leaves the report export audit untouched.",
   "emptyFirstRun": "No report export audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the report export audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Build a seat report",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "exportReportResult",
    "contract": "reporting",
    "purpose": "Export it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1060",
   "workshopBoard": "wireframes/WS150 Seat Management Venue Mapping Reference v1.0 Board 11.dc.html#bo-1060"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 48. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "executionId",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "createReport": {
  "method": "POST",
  "path": "/reports",
  "contract": "reporting",
  "summary": "Create a custom report definition",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
 },
 "exportReportResult": {
  "method": "POST",
  "path": "/report-executions/{executionId}/export",
  "contract": "reporting",
  "summary": "Export a completed result",
  "permission": "REPORT_EXPORT",
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
 "getSeatInventory": {
  "method": "GET",
  "path": "/seat-inventory",
  "contract": "seating",
  "summary": "Every seat's state for a performance, in one read",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": true
   },
   {
    "name": "sectionId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatInventory"
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
    "name": "priceCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "sectionCode",
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
 "listInventoryHolds": {
  "method": "GET",
  "path": "/inventory-holds",
  "contract": "catalogue",
  "summary": "List inventory holds",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channelCapacityId",
    "in": "query",
    "required": null
   },
   {
    "name": "holderWorkstationId",
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
 "listSeatCategories": {
  "method": "GET",
  "path": "/seat-categories",
  "contract": "seating",
  "summary": "List seat categories",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatCategory"
 },
 "listSeats": {
  "method": "GET",
  "path": "/seat-maps/{seatMapId}/seats",
  "contract": "seating",
  "summary": "List seats in a map",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "sectionCode",
    "in": "query",
    "required": null
   },
   {
    "name": "rowLabel",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "attribute",
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
 "runReport": {
  "method": "POST",
  "path": "/reports/{reportId}/run",
  "contract": "reporting",
  "summary": "Run a report",
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
  "requestBody": "RunReportRequest",
  "responds": "ReportResult"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiDemandForecastingBookingCurveStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Venue id"
   },
   "product": {
    "type": "string",
    "description": "Product id",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "performance": {
    "type": "string",
    "description": "Performance id",
    "nullable": true
   },
   "date": {
    "type": "string",
    "description": "Date",
    "format": "date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot",
    "nullable": true
   },
   "priceCategory": {
    "type": "string",
    "description": "Price category",
    "nullable": true
   },
   "sectionCode": {
    "type": "string",
    "nullable": true,
    "description": "Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "confidence": {
    "type": "number",
    "description": "Forecast Confidence, percent"
   },
   "forecastFinalOccupancy": {
    "type": "number",
    "description": "Forecast Final Occupancy, percent"
   },
   "demand": {
    "type": "integer",
    "description": "Forecast demand"
   },
   "attendance": {
    "type": "integer",
    "description": "Forecast attendance"
   },
   "occupancy": {
    "type": "number",
    "description": "Forecast occupancy, percent"
   },
   "sellThrough": {
    "type": "number",
    "description": "Forecast sell-through, percent"
   },
   "expectedSellOutTime": {
    "type": "string",
    "description": "Expected Sell-Out Time; empty if no sell-out forecast",
    "format": "date-time",
    "nullable": true
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Forecast revenue"
   },
   "conversion": {
    "type": "number",
    "description": "Forecast conversion, percent"
   },
   "remainingInventory": {
    "type": "integer",
    "description": "Forecast remaining inventory at event"
   },
   "mape": {
    "type": "number",
    "description": "MAPE over closed forecasts at this level, percent"
   },
   "forecastBias": {
    "type": "number",
    "description": "Forecast Bias (positive = over-forecast), percent"
   },
   "overForecast": {
    "type": "number",
    "description": "Share of closed forecasts that over-forecast, percent"
   },
   "underForecast": {
    "type": "number",
    "description": "Share of closed forecasts that under-forecast, percent"
   },
   "forecastId": {
    "type": "string",
    "description": "Forecast id"
   },
   "horizon": {
    "type": "string",
    "description": "Forecast Horizon",
    "enum": [
     "intraday",
     "tomorrow",
     "days7",
     "days30",
     "eventHorizon",
     "seasonalHorizon"
    ]
   },
   "bookingCurve": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysBeforeEvent": {
       "type": "integer",
       "description": "T minus days"
      },
      "historicalExpectedPercentSold": {
       "type": "number",
       "description": "Historical expected curve, percent sold"
      },
      "actualPercentSold": {
       "type": "number",
       "nullable": true,
       "description": "Current actual curve, percent sold (empty for future points)"
      },
      "forecastPercentSold": {
       "type": "number",
       "description": "AI forecast curve, percent sold"
      }
     }
    },
    "description": "Booking Curve"
   },
   "signalContributions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "signal": {
       "type": "string",
       "enum": [
        "internalSales",
        "bookingVelocity",
        "occupancy",
        "historicalEvents",
        "nearbyEvent",
        "weather",
        "marketTourism",
        "competitor",
        "priceElasticity",
        "other"
       ],
       "description": "Signal category"
      },
      "contributionPercent": {
       "type": "number",
       "description": "Explanatory share of the forecast"
      }
     }
    },
    "description": "Model Inputs: which signals contributed"
   },
   "confidenceReasons": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "strongHistoricalData",
      "stableBookingPattern",
      "reliableExternalSignals",
      "limitedHistoricalData",
      "volatileBookingPattern",
      "degradedExternalSignals"
     ]
    },
    "description": "Reasons behind the forecast confidence"
   },
   "modelVersion": {
    "type": "string",
    "description": "Model version that produced the forecast"
   },
   "generatedAt": {
    "type": "string",
    "description": "When the forecast was produced",
    "format": "date-time"
   }
  }
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "CreateReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "category",
   "dataSource",
   "columns",
   "requiredPermission"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "category": {
    "$ref": "#/components/schemas/ReportCategory"
   },
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "minItems": 1,
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
   "parameters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportParameter"
    }
   },
   "requiredPermission": {
    "$ref": "../shared/permissions.yaml#/components/schemas/Permission",
    "description": "Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"
   },
   "maxDateRangeDays": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "default": 366,
    "description": "Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."
   }
  }
 },
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n",
  "enum": [
   "orders",
   "orderLines",
   "payments",
   "refunds",
   "shifts",
   "scanEvents",
   "entitlements",
   "products",
   "inventory",
   "stockMovements",
   "stockCounts",
   "waste",
   "workstations",
   "devices",
   "principals",
   "loyalty",
   "reviews",
   "queueEntries",
   "guests",
   "campaigns",
   "cases",
   "ledgerEntries",
   "workOrders",
   "approvals",
   "purchaseOrders",
   "receipts",
   "requisitions",
   "stockBatches",
   "resourceBookings",
   "delegations",
   "forms",
   "challenges",
   "wallets",
   "resaleListings",
   "accreditationApplications",
   "accreditationHolders",
   "accreditationCredentials",
   "forecastPoints"
  ],
  "x-ticvai-forecast-points": "**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"
 },
 "ExportFormat": {
  "type": "string",
  "enum": [
   "csv",
   "xlsx",
   "pdf",
   "json"
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
 "InventoryHold": {
  "x-ticvai-persistence": "catalogue.inventory_hold",
  "type": "object",
  "required": [
   "id",
   "channelCapacityId",
   "holderKind",
   "grantedUnits",
   "consumedUnits",
   "status",
   "acquiredAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "channelCapacityId": {
    "type": "string",
    "format": "uuid"
   },
   "holderKind": {
    "$ref": "#/components/schemas/InventoryHoldHolderKind"
   },
   "holderWorkstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The holding workstation when `holderKind` is `workstation`; null on a cart hold, because a browser has none (SD-023, 29 September)."
   },
   "holderCartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The holding cart (`orders.cart`) when `holderKind` is `cart` (SD-023, 29 September)."
   },
   "convertedOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The paid order the hold was converted for, set by `convertInventoryHold`."
   },
   "convertedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "parentLeaseId": {
    "type": "string",
    "nullable": true,
    "description": "Present when sub-leased from a venue edge node."
   },
   "requestedUnits": {
    "type": "integer"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Channel"
     }
    ],
    "description": "Allocation this lease draws from."
   },
   "grantedUnits": {
    "type": "integer",
    "description": "May be less than requested — a partial grant is not an error. Constrained by the channel's remaining allocation plus the general pool, never by raw capacity.\n"
   },
   "consumedUnits": {
    "type": "integer"
   },
   "status": {
    "$ref": "#/components/schemas/LeaseStatus"
   },
   "acquiredAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "releasedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "forceReleasedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "forceReleaseReason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "InventoryHoldHolderKind": {
  "type": "string",
  "enum": [
   "workstation",
   "cart"
  ],
  "default": "workstation",
  "description": "**Who holds the units** (decided 29 September, SD-023). A till, kiosk or edge node holds as a `workstation`; a guest's web or app cart holds as a `cart`, acquired by the order service. A browser has no workstation, so a cart hold carries `cartId` and no `holderWorkstationId`.\n"
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
 "LeaseStatus": {
  "type": "string",
  "description": "`states/lease.yaml`. **`expired` is set by that model's timer transition when `expiresAt` passes without a renewal**, not by any operation in this contract. The job that runs the timer is the sweeper ADR-0037 deferred: it returns an expired hold's unconsumed units to `remaining` in the same guarded statement as a release (SD-023, 29 September), and **writes `inventoryHold.expired` to the outbox in the same transaction** (SD-023/SD-033, applied 30 September; `events/inventoryHold-expired.yaml`), so the cart that held the units hears of it before checkout. A `converted` hold is never swept.\n**`converted` is set by `convertInventoryHold`** when the order that holds the units is paid (decided 29 September, SD-023); its units are `sold` and the sweeper never touches it.\n",
  "enum": [
   "active",
   "expired",
   "released",
   "forceReleased",
   "converted"
  ]
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
 "Point": {
  "type": "object",
  "required": [
   "x",
   "y"
  ],
  "properties": {
   "x": {
    "type": "number"
   },
   "y": {
    "type": "number"
   }
  }
 },
 "ReportCategory": {
  "type": "string",
  "enum": [
   "sales",
   "admission",
   "financial",
   "inventory",
   "guest",
   "operations",
   "marketing",
   "workforce",
   "compliance",
   "custom"
  ]
 },
 "ReportColumn": {
  "x-ticvai-persistence": "reporting.report_column",
  "type": "object",
  "required": [
   "field"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "aggregation": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Aggregation"
     }
    ],
    "default": "none"
   },
   "sortOrder": {
    "type": "integer"
   },
   "sortDirection": {
    "type": "string",
    "enum": [
     "asc",
     "desc"
    ]
   },
   "format": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "ReportDefinition": {
  "x-ticvai-persistence": "reporting.report_definition + reporting.report_column + reporting.report_filter",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "isSystem",
     "isRetired",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "version": {
      "type": "string",
      "description": "The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."
     },
     "isSystem": {
      "type": "boolean",
      "description": "Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"
     },
     "isRetired": {
      "type": "boolean"
     },
     "estimatedCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Informs whether it may run inline or must be queued."
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "scopePath": {
      "type": "string",
      "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
     }
    }
   }
  ]
 },
 "ReportFilter": {
  "x-ticvai-persistence": "reporting.report_filter",
  "type": "object",
  "required": [
   "field",
   "operator"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
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
     "contains",
     "isNull",
     "isNotNull"
    ]
   },
   "value": {
    "description": "**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"
   },
   "values": {
    "type": "array",
    "description": "The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.",
    "items": {}
   },
   "isParameter": {
    "type": "boolean",
    "default": false,
    "description": "Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"
   }
  }
 },
 "ReportParameter": {
  "x-ticvai-persistence": "reporting.report_parameter",
  "type": "object",
  "required": [
   "key",
   "label",
   "type",
   "isRequired"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "type": {
    "$ref": "#/components/schemas/FieldType"
   },
   "isRequired": {
    "type": "boolean"
   },
   "defaultValue": {
    "description": "Open on purpose. A value of this parameter's `type`, used when a run supplies none."
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
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."
   },
   "dateTo": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (audit R158)."
   },
   "forceAsync": {
    "type": "boolean",
    "default": false,
    "description": "Queue regardless of size, for a result to be collected later."
   }
  }
 },
 "Seat": {
  "x-ticvai-persistence": "seating.seat",
  "type": "object",
  "required": [
   "id",
   "sectionCode",
   "rowLabel",
   "seatNumber",
   "attribute"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "**Stable for the life of the seat.** Section, row and number are display labels that change on a refit; this does not. A ticket sold today must still resolve after a renumbering.\n"
   },
   "sectionCode": {
    "type": "string"
   },
   "rowLabel": {
    "type": "string"
   },
   "seatNumber": {
    "type": "string"
   },
   "displayLabel": {
    "type": "string",
    "description": "What the guest sees, e.g. `A2-7-11`."
   },
   "position": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Point"
     }
    ],
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "attribute": {
    "$ref": "#/components/schemas/SeatAttribute"
   },
   "companionSeatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Present on accessible seats. Sold together, released together."
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "SeatAttribute": {
  "type": "string",
  "description": "BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n",
  "enum": [
   "standard",
   "accessible",
   "companion",
   "obstructedView",
   "restrictedLegroom",
   "premium",
   "houseSeat",
   "buffer",
   "aisle",
   "endOfRow",
   "extraLegroom",
   "powerOutlet",
   "tableService",
   "shaded",
   "covered",
   "nearExit",
   "nearAccessibleWc",
   "wheelchairTransfer",
   "limitedRecline",
   "sofa",
   "beanbag"
  ]
 },
 "SeatCategory": {
  "x-ticvai-persistence": "seating.seat_category",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "rank"
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
   "displayColour": {
    "type": "string",
    "nullable": true
   },
   "rank": {
    "type": "integer",
    "description": "Ordering for best-seat assignment. Lower is better."
   },
   "seatCount": {
    "type": "integer"
   },
   "priceBands": {
    "type": "array",
    "description": "What a seat in this category costs, by band (decided 28 September, audit R275 (d), from the BO-1045 pack). Written by `createSeatCategory` and `updateSeatCategory`. A band may be narrowed to a sales channel or a customer segment and to a window; where several match a sale, the narrowest wins.\n",
    "items": {
     "$ref": "#/components/schemas/SeatPriceBand"
    }
   }
  }
 },
 "SeatInventory": {
  "type": "object",
  "description": "Board 4. **One read, because a real-time map assembling four endpoints renders one state late.**\n",
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "totals": {
    "type": "object",
    "properties": {
     "capacity": {
      "type": "integer"
     },
     "available": {
      "type": "integer"
     },
     "held": {
      "type": "integer"
     },
     "reserved": {
      "type": "integer"
     },
     "sold": {
      "type": "integer"
     },
     "blocked": {
      "type": "integer"
     },
     "outOfService": {
      "type": "integer"
     }
    }
   },
   "seats": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "seatId": {
       "type": "string",
       "format": "uuid"
      },
      "label": {
       "type": "string"
      },
      "state": {
       "type": "string",
       "enum": [
        "available",
        "held",
        "reserved",
        "sold",
        "blocked",
        "outOfService",
        "killed"
       ]
      },
      "holdPoolId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "orderId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "expiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "SeatPriceBand": {
  "x-ticvai-persistence": "seating.seat_price_band",
  "type": "object",
  "description": "One price band on a seat category (decided 28 September, audit R275 (d)). The currency is `amount.currency`, resolved from the region like every `Money` (ADR-0018), so the band carries no currency of its own.\n",
  "required": [
   "code",
   "displayLabel",
   "amount",
   "effectiveFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "seatCategoryId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "description": "Unique within the category."
   },
   "displayLabel": {
    "type": "string",
    "maxLength": 200
   },
   "displayColour": {
    "type": "string",
    "nullable": true,
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channel": {
    "nullable": true,
    "description": "Null means every channel.",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ]
   },
   "customerSegmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `marketing-crm` customer segment; null means everyone."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null means open-ended."
   }
  }
 }
}
```
