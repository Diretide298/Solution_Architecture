# WS12 — Access Control board 12

**10 screens · 16 operations · 19 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `REPORT_SCHEDULE, REPORT_VIEW_VENUE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-254` | Access Monitoring & Analytics Command Center | listDetail | 1 | 0 | — |
| `BO-255` | Live Venue Occupancy & People Counting | listDetail | 1 | 0 | — |
| `BO-256` | Graphical Access Map & Live Gate Performance | listDetail | 1 | 0 | — |
| `BO-257` | Attendance & Admission Analytics | listDetail | 1 | 0 | — |
| `BO-258` | Entry, Exit, Re-entry & Crossover Analytics | listDetail | 1 | 0 | — |
| `BO-259` | Throughput, Queue & Validation Performance Analytics | commandCentre | 1 | 0 | — |
| `BO-260` | Validation Outcome & Rejection Analytics | listDetail | 1 | 0 | — |
| `BO-261` | Guest Dwell Time, Length of Stay & Attraction Flow | commandCentre | 1 | 0 | — |
| `BO-262` | Access Reports, Scheduled Reporting & Data Export | listDetail | 7 | 0 | — |
| `BO-263` | AI Access Intelligence, Forecasting & Executive Insights | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-255, BO-256, BO-258, BO-260, BO-262, BO-263 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-254",
  "name": "Access Monitoring & Analytics Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.1",
   "page": 168
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-monitoring-analytics-command-center-bo-254",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessMonitoringAnalyticsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-255",
    "BO-256",
    "BO-257",
    "BO-258",
    "BO-259",
    "BO-260",
    "BO-261",
    "BO-262",
    "BO-263"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "provenance": "derived — BO-100 declares entryState.params  and BO-254 holds none of them, so the edge carries nothing and BO-100 opens cold"
    },
    {
     "to": "BO-255",
     "trigger": "Works in Live Venue Occupancy & People Counting",
     "provenance": "flow F122 step 1→2",
     "operation": "listAccessMonitoring"
    },
    {
     "to": "BO-256",
     "trigger": "Works in Graphical Access Map & Live Gate Performance",
     "provenance": "flow F122 step 3→4",
     "operation": "listAccessMonitoring"
    },
    {
     "to": "BO-257",
     "trigger": "Works in Attendance & Admission Analytics",
     "provenance": "flow F122 step 5→6",
     "operation": "listAccessMonitoring"
    },
    {
     "to": "BO-258",
     "trigger": "Works in Entry, Exit, Re-entry & Crossover Analytics",
     "provenance": "flow F122 step 7→8",
     "operation": "listAccessMonitoring"
    },
    {
     "to": "BO-259",
     "trigger": "Works in Throughput, Queue & Validation Performance Analytics",
     "provenance": "flow F122 step 9→10",
     "operation": "listAccessMonitoring"
    },
    {
     "to": "BO-260",
     "trigger": "Works in Validation Outcome & Rejection Analytics",
     "provenance": "flow F122 step 11→12",
     "operation": "listAccessMonitoring"
    },
    {
     "to": "BO-261",
     "trigger": "Works in Guest Dwell Time, Length of Stay & Attraction Flow",
     "provenance": "flow F122 step 13→14",
     "operation": "listAccessMonitoring"
    },
    {
     "to": "BO-262",
     "trigger": "Works in Access Reports, Scheduled Reporting & Data Export",
     "provenance": "flow F122 step 15→16",
     "operation": "listAccessMonitoring"
    },
    {
     "to": "BO-263",
     "trigger": "Works in AI Access Intelligence, Forecasting & Executive Insights",
     "provenance": "flow F122 step 17→18",
     "operation": "listAccessMonitoring"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can understand the overall access operation from one screen.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide a single executive and operational overview of access performance across all TICVAI-controlled venues.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Admissions Today",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.totalAdmissionsToday",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Entries",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.entries",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Exits",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.exits",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Currently In Venue",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.currentlyInVenue",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Re-entries",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.reEntries",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Crossovers",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.crossovers",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Group Admissions",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.groupAdmissions",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Fast Pass Uses",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.fastPassUses",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Valid Scans",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.validScans",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Rejected Scans",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.rejectedScans",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Intervention Rate",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.interventionRate",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Seconds",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.averageValidationTime",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Active Gates",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.activeGates",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Offline Devices",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterViewSummary.offlineDevices",
       "operation": "listAccessMonitoring",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every access monitoring analytics",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterView",
       "operation": "listAccessMonitoring",
       "provenance": "pack Access Control Module_Reference.pdf, page 168 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access monitoring analytics",
       "bindsTo": "AccessMonitoringAnalyticsCommandCenterView",
       "notes": "The pack groups this record's detail under its own headings: “TOTAL ADMISSIONS”, “CURRENTLY IN VENUE”, “Venue Comparison”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 168 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access monitoring analytics list.",
   "error": "Could not load. Names which read failed and leaves the access monitoring analytics untouched.",
   "emptyFirstRun": "No access monitoring analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access monitoring analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessMonitoring",
    "contract": "access",
    "purpose": "Access Monitoring & Analytics Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AccessMonitoringAnalyticsCommandCenterViewSummary.totalAdmissionsToday",
    "AccessMonitoringAnalyticsCommandCenterViewSummary.entries",
    "AccessMonitoringAnalyticsCommandCenterViewSummary.exits",
    "AccessMonitoringAnalyticsCommandCenterViewSummary.currentlyInVenue",
    "AccessMonitoringAnalyticsCommandCenterViewSummary.reEntries",
    "AccessMonitoringAnalyticsCommandCenterViewSummary.crossovers"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-254",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-254"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 168. 14 of 14 labels bound to a contract property; 14 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-255",
  "name": "Live Venue Occupancy & People Counting",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.2",
   "page": 170
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/live-venue-occupancy-people-counting-bo-255",
   "component": "apps/venue-management-web/src/routes/access-venue/LiveVenueOccupancyPeopleCounting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-254",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F122 step 2→3",
     "operation": "listLiveVenueOccupancy"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide real-time people counting and occupancy using entry and exit events.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 170"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 170"
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
       "impliedBy": "listLiveVenueOccupancy",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live venue occupancy list.",
   "error": "Could not load. Names which read failed and leaves the live venue occupancy untouched.",
   "emptyFirstRun": "No live venue occupancy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live venue occupancy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listLiveVenueOccupancy",
    "contract": "access",
    "purpose": "Live Venue Occupancy & People Counting",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "LiveVenueOccupancyPeopleCountingView.exits",
    "LiveVenueOccupancyPeopleCountingView.operationalAdjustments",
    "LiveVenueOccupancyPeopleCountingView.current",
    "LiveVenueOccupancyPeopleCountingView.capacity",
    "LiveVenueOccupancyPeopleCountingView.occupancy"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-255",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-255"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 170. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-256",
  "name": "Graphical Access Map & Live Gate Performance",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.3",
   "page": 171
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/graphical-access-map-live-gate-performance-bo-256",
   "component": "apps/venue-management-web/src/routes/access-venue/GraphicalAccessMapLiveGatePerformance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-254",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F122 step 4→5",
     "operation": "listGraphicalAccessMap"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can visually identify where access bottlenecks or abnormal conditions are occurring.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Turn the graphical access topology created in Board 1 into a live operational analytics map.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every graphical access map",
       "columns": [
        "GraphicalAccessMapLiveGatePerformanceView.pointType"
       ],
       "bindsTo": "GraphicalAccessMapLiveGatePerformanceView",
       "operation": "listGraphicalAccessMap",
       "provenance": "pack Access Control Module_Reference.pdf, page 171 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected graphical access map",
       "bindsTo": "GraphicalAccessMapLiveGatePerformanceView",
       "columns": [
        "GraphicalAccessMapLiveGatePerformanceView.pointType"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Guests”, “Throughput”, “Success”, “Reject”, “Yellow”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 171 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The graphical access map list.",
   "error": "Could not load. Names which read failed and leaves the graphical access map untouched.",
   "emptyFirstRun": "No graphical access map yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the graphical access map are still there. The pack's own statuses are 🟢 Healthy — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGraphicalAccessMap",
    "contract": "access",
    "purpose": "Graphical Access Map & Live Gate Performance",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GraphicalAccessMapLiveGatePerformanceView.pointType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-256",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-256"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 171. 8 of 8 labels bound to a contract property; 12 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-257",
  "name": "Attendance & Admission Analytics",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.4",
   "page": 172
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/attendance-admission-analytics-bo-257",
   "component": "apps/venue-management-web/src/routes/access-venue/AttendanceAdmissionAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-254",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F122 step 6→7",
     "operation": "listAttendanceAdmission"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide detailed reporting of who actually attended compared with tickets sold/reserved. This is particularly important because group admission may differ from purchased quantity.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search attendance admission analytics",
       "provenance": "pack Access Control Module_Reference.pdf, page 172 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Product",
        "Timeslot",
        "Membership",
        "B2B Partner",
        "Reseller",
        "Guest Category"
       ],
       "notes": "The pack filters this screen by ticket type, product, event, timeslot, membership, channel and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Access Control Module_Reference.pdf, page 172 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every attendance admission analytics",
       "columns": [
        "AttendanceAdmissionAnalyticsView.ticketsSold",
        "AttendanceAdmissionAnalyticsView.ticketsEligibleToday",
        "AttendanceAdmissionAnalyticsView.ticketsScanned",
        "AttendanceAdmissionAnalyticsView.uniqueGuests",
        "AttendanceAdmissionAnalyticsView.noShows",
        "AttendanceAdmissionAnalyticsView.groupAttendance",
        "AttendanceAdmissionAnalyticsView.membershipAttendance",
        "AttendanceAdmissionAnalyticsView.repeatEntry",
        "AttendanceAdmissionAnalyticsView.noShowRate"
       ],
       "bindsTo": "AttendanceAdmissionAnalyticsView",
       "operation": "listAttendanceAdmission",
       "provenance": "pack Access Control Module_Reference.pdf, page 172 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected attendance admission analytics",
       "bindsTo": "AttendanceAdmissionAnalyticsView",
       "columns": [
        "AttendanceAdmissionAnalyticsView.ticketsSold",
        "AttendanceAdmissionAnalyticsView.ticketsEligibleToday",
        "AttendanceAdmissionAnalyticsView.ticketsScanned",
        "AttendanceAdmissionAnalyticsView.uniqueGuests",
        "AttendanceAdmissionAnalyticsView.noShows",
        "AttendanceAdmissionAnalyticsView.groupAttendance",
        "AttendanceAdmissionAnalyticsView.membershipAttendance",
        "AttendanceAdmissionAnalyticsView.repeatEntry",
        "AttendanceAdmissionAnalyticsView.noShowRate"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Sold”, “Eligible”, “Attended”, “ATTENDANCE RATE”, “Purchased”, “Actual Attendance”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 172 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attendance admission analytics list.",
   "error": "Could not load. Names which read failed and leaves the attendance admission analytics untouched.",
   "emptyFirstRun": "No attendance admission analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attendance admission analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAttendanceAdmission",
    "contract": "access",
    "purpose": "Attendance & Admission Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AttendanceAdmissionAnalyticsView.ticketsSold",
    "AttendanceAdmissionAnalyticsView.ticketsEligibleToday",
    "AttendanceAdmissionAnalyticsView.ticketsScanned",
    "AttendanceAdmissionAnalyticsView.uniqueGuests",
    "AttendanceAdmissionAnalyticsView.noShows",
    "AttendanceAdmissionAnalyticsView.groupAttendance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-257",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-257"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 172. 17 of 23 labels bound to a contract property; 23 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-258",
  "name": "Entry, Exit, Re-entry & Crossover Analytics",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.5",
   "page": 174
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/entry-exit-re-entry-crossover-analytics-bo-258",
   "component": "apps/venue-management-web/src/routes/access-venue/EntryExitReEntryCrossoverAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-254",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F122 step 8→9",
     "operation": "listEntryExitCrossover"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can understand actual movement patterns rather than only total admission counts.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Measure) and no metric row",
  "purpose": "Analyze complete guest movement across the access journey.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every entry exit re-entry",
       "columns": [
        "EntryExitReEntryCrossoverAnalyticsView.reEntryRate",
        "EntryExitReEntryCrossoverAnalyticsView.averageTimeOutside",
        "EntryExitReEntryCrossoverAnalyticsView.mostUsedReEntryGates",
        "EntryExitReEntryCrossoverAnalyticsView.rejectedReEntry",
        "EntryExitReEntryCrossoverAnalyticsView.crossoverTime",
        "EntryExitReEntryCrossoverAnalyticsView.crossoverProduct"
       ],
       "bindsTo": "EntryExitReEntryCrossoverAnalyticsView",
       "operation": "listEntryExitCrossover",
       "provenance": "pack Access Control Module_Reference.pdf, page 174 §Measure"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected entry exit re-entry",
       "bindsTo": "EntryExitReEntryCrossoverAnalyticsView",
       "columns": [
        "EntryExitReEntryCrossoverAnalyticsView.reEntryRate",
        "EntryExitReEntryCrossoverAnalyticsView.averageTimeOutside",
        "EntryExitReEntryCrossoverAnalyticsView.mostUsedReEntryGates",
        "EntryExitReEntryCrossoverAnalyticsView.rejectedReEntry",
        "EntryExitReEntryCrossoverAnalyticsView.crossoverTime",
        "EntryExitReEntryCrossoverAnalyticsView.crossoverProduct"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Adventure Park”, “Water Park”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 174 §Measure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entry exit re-entry list.",
   "error": "Could not load. Names which read failed and leaves the entry exit re-entry untouched.",
   "emptyFirstRun": "No entry exit re-entry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entry exit re-entry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEntryExitCrossover",
    "contract": "access",
    "purpose": "Entry, Exit, Re-entry & Crossover Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "EntryExitReEntryCrossoverAnalyticsView.reEntryRate",
    "EntryExitReEntryCrossoverAnalyticsView.averageTimeOutside",
    "EntryExitReEntryCrossoverAnalyticsView.mostUsedReEntryGates",
    "EntryExitReEntryCrossoverAnalyticsView.rejectedReEntry"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-258",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-258"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 174. 8 of 8 labels bound to a contract property; 8 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-259",
  "name": "Throughput, Queue & Validation Performance Analytics",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.6",
   "page": 175
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/throughput-queue-validation-performance-analytics-bo-259",
   "component": "apps/venue-management-web/src/routes/access-venue/ThroughputQueueValidationPerformanceAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-254",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F122 step 10→11",
     "operation": "listThroughputQueueValidation"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can identify why specific gates or lanes are underperforming.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure the operational efficiency of gates and validation devices.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Guests per Minute",
       "provenance": "pack Access Control Module_Reference.pdf, page 175 §Show",
       "bindsTo": "ThroughputQueueValidationPerformanceAnalyticsView.guestsPerMinute"
      },
      {
       "kind": "metricTile",
       "label": "Guests per Hour",
       "provenance": "pack Access Control Module_Reference.pdf, page 175 §Show",
       "bindsTo": "ThroughputQueueValidationPerformanceAnalyticsView.guestsPerHour"
      },
      {
       "kind": "metricTile",
       "label": "Average Scan Time",
       "provenance": "pack Access Control Module_Reference.pdf, page 175 §Show",
       "bindsTo": "ThroughputQueueValidationPerformanceAnalyticsView.averageScanTime"
      },
      {
       "kind": "metricTile",
       "label": "Average Gate Cycle",
       "provenance": "pack Access Control Module_Reference.pdf, page 175 §Show",
       "bindsTo": "ThroughputQueueValidationPerformanceAnalyticsView.averageGateCycle"
      },
      {
       "kind": "metricTile",
       "label": "Success Rate",
       "provenance": "pack Access Control Module_Reference.pdf, page 175 §Show",
       "bindsTo": "ThroughputQueueValidationPerformanceAnalyticsView.successRate"
      },
      {
       "kind": "metricTile",
       "label": "Yellow Rate",
       "provenance": "pack Access Control Module_Reference.pdf, page 175 §Show",
       "bindsTo": "ThroughputQueueValidationPerformanceAnalyticsView.yellowRate"
      },
      {
       "kind": "metricTile",
       "label": "Reject Rate",
       "provenance": "pack Access Control Module_Reference.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Manual Intervention Rate",
       "provenance": "pack Access Control Module_Reference.pdf, page 175 §Show",
       "bindsTo": "ThroughputQueueValidationPerformanceAnalyticsView.manualInterventionRate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The throughput queue validation list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the throughput queue validation untouched.",
   "emptyFirstRun": "No throughput queue validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the throughput queue validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listThroughputQueueValidation",
    "contract": "access",
    "purpose": "Throughput, Queue & Validation Performance Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ThroughputQueueValidationPerformanceAnalyticsView.guestsPerMinute",
    "ThroughputQueueValidationPerformanceAnalyticsView.guestsPerHour",
    "ThroughputQueueValidationPerformanceAnalyticsView.averageScanTime",
    "ThroughputQueueValidationPerformanceAnalyticsView.averageGateCycle",
    "ThroughputQueueValidationPerformanceAnalyticsView.successRate",
    "ThroughputQueueValidationPerformanceAnalyticsView.yellowRate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-259",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-259"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 175. 7 of 7 labels bound to a contract property; 8 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-260",
  "name": "Validation Outcome & Rejection Analytics",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.7",
   "page": 176
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/validation-outcome-rejection-analytics-bo-260",
   "component": "apps/venue-management-web/src/routes/access-venue/ValidationOutcomeRejectionAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-254",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F122 step 12→13",
     "operation": "listValidationOutcomeRejection"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can identify the operational root cause behind access failures.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Analyze why guests are denied or require manual intervention.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 176"
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
       "label": "Search validation outcome rejection",
       "provenance": "pack Access Control Module_Reference.pdf, page 176 §Analyze By"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Gate",
        "Product",
        "Ticket Type",
        "Channel",
        "Reseller",
        "Operator",
        "Device",
        "Credential Type"
       ],
       "notes": "The pack filters this screen by venue, gate, product, ticket type, channel, reseller and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Access Control Module_Reference.pdf, page 176 §Analyze By"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validation outcome rejection list.",
   "error": "Could not load. Names which read failed and leaves the validation outcome rejection untouched.",
   "emptyFirstRun": "No validation outcome rejection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the validation outcome rejection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listValidationOutcomeRejection",
    "contract": "access",
    "purpose": "Validation Outcome & Rejection Analytics",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-260",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-260"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 176. 0 of 9 labels bound to a contract property; 9 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-261",
  "name": "Guest Dwell Time, Length of Stay & Attraction Flow",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.8",
   "page": 177
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/guest-dwell-time-length-of-stay-attraction-flow-bo-261",
   "component": "apps/venue-management-web/src/routes/access-venue/GuestDwellTimeLengthOfStayAttractionFlow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-254",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F122 step 14→15",
     "operation": "listGuestDwellTime"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "systems.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Use access events to understand how guests move through and use the venue.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Average Length of Stay",
       "provenance": "pack Access Control Module_Reference.pdf, page 177 §Show",
       "bindsTo": "GuestDwellTimeLengthOfStayAttractionFlowView.averageLengthOfStay"
      },
      {
       "kind": "metricTile",
       "label": "Median Stay",
       "provenance": "pack Access Control Module_Reference.pdf, page 177 §Show",
       "bindsTo": "GuestDwellTimeLengthOfStayAttractionFlowView.medianStay"
      },
      {
       "kind": "metricTile",
       "label": "Peak Arrival",
       "provenance": "pack Access Control Module_Reference.pdf, page 177 §Show",
       "bindsTo": "GuestDwellTimeLengthOfStayAttractionFlowView.peakArrival"
      },
      {
       "kind": "metricTile",
       "label": "Peak Departure",
       "provenance": "pack Access Control Module_Reference.pdf, page 177 §Show",
       "bindsTo": "GuestDwellTimeLengthOfStayAttractionFlowView.peakDeparture"
      },
      {
       "kind": "metricTile",
       "label": "Zone Dwell Time",
       "provenance": "pack Access Control Module_Reference.pdf, page 177 §Show",
       "bindsTo": "GuestDwellTimeLengthOfStayAttractionFlowView.zoneDwellTime"
      },
      {
       "kind": "metricTile",
       "label": "Attraction Visits",
       "provenance": "pack Access Control Module_Reference.pdf, page 177 §Show",
       "bindsTo": "GuestDwellTimeLengthOfStayAttractionFlowView.attractionVisits"
      },
      {
       "kind": "metricTile",
       "label": "Fast Pass Usage",
       "provenance": "pack Access Control Module_Reference.pdf, page 177 §Show",
       "bindsTo": "GuestDwellTimeLengthOfStayAttractionFlowView.fastPassUsage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest dwell time list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the guest dwell time untouched.",
   "emptyFirstRun": "No guest dwell time yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest dwell time are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGuestDwellTime",
    "contract": "access",
    "purpose": "Guest Dwell Time, Length of Stay & Attraction Flow",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GuestDwellTimeLengthOfStayAttractionFlowView.averageLengthOfStay",
    "GuestDwellTimeLengthOfStayAttractionFlowView.medianStay",
    "GuestDwellTimeLengthOfStayAttractionFlowView.peakArrival",
    "GuestDwellTimeLengthOfStayAttractionFlowView.peakDeparture",
    "GuestDwellTimeLengthOfStayAttractionFlowView.zoneDwellTime",
    "GuestDwellTimeLengthOfStayAttractionFlowView.attractionVisits"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-261",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-261"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 177. 7 of 7 labels bound to a contract property; 7 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-262",
  "name": "Access Reports, Scheduled Reporting & Data Export",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.9",
   "page": 179
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-reports-scheduled-reporting-data-export-bo-262",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessReportsScheduledReportingDataExport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-254",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F122 step 16→17",
     "operation": "listAccessReportScheduled"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can create, schedule and export access-control reports without development support.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide configurable operational and management reports.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 179"
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
       "label": "Search access reports scheduled",
       "provenance": "pack Access Control Module_Reference.pdf, page 179 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "notes": "The pack filters this screen by tenant, venue, park, zone, event, date and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Access Control Module_Reference.pdf, page 179 §Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access reports scheduled list.",
   "error": "Could not load. Names which read failed and leaves the access reports scheduled untouched.",
   "emptyFirstRun": "No access reports scheduled yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access reports scheduled are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessReportScheduled",
    "contract": "access",
    "purpose": "Access Reports, Scheduled Reporting & Data Export",
    "trigger": "onLoad"
   },
   {
    "operationId": "listReportSchedules",
    "contract": "reporting",
    "purpose": "The scheduled access reports",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run an access report now",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listReportSchedules"
    ]
   },
   {
    "operationId": "createReportSchedule",
    "contract": "reporting",
    "purpose": "Schedule an access report or export",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listReportSchedules"
    ]
   },
   {
    "operationId": "updateReportSchedule",
    "contract": "reporting",
    "purpose": "Amend, pause or resume a schedule",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listReportSchedules"
    ]
   },
   {
    "operationId": "deleteReportSchedule",
    "contract": "reporting",
    "purpose": "Delete a schedule",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listReportSchedules"
    ]
   },
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "The access reports to run or schedule",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-262",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-262"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 179. 11 of 11 labels bound to a contract property; 11 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "reportId",
     "from": "navigation"
    },
    {
     "name": "scheduleId",
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
  "id": "BO-263",
  "name": "AI Access Intelligence, Forecasting & Executive Insights",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "12",
   "number": "12.10",
   "page": 180
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ai-access-intelligence-forecasting-executive-insights-bo-263",
   "component": "apps/venue-management-web/src/routes/access-venue/AiAccessIntelligenceForecastingExecutiveInsights.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-254"
   ],
   "exitTo": [
    "BO-254"
   ],
   "inferred": false,
   "notes": "**Reached from BO-254, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "dashboards alone. Board 12 — Final 10-Screen Structure # Backend Screen Main Responsibility 12.1 Access Monitoring & Analytics Command Center Executive access overview 12.2 Live Venue Occupancy & People Counting Real-time occupancy 12.3 Graphical Access Map & Live Gate Performance Visual venue/gate monitoring 12.4 Attendance & Admission Analytics Actual attendance and no-shows 12.5 Entry, Exit, Re-entry & Crossover Analytics Complete guest movement 12.6 Throughput, Queue & Validation Performance Analytics Gate operational efficiency 12.7 Validation Outcome & Rejection Analytics Failure and int",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast) and no metric row",
  "purpose": "Turn access-control data into proactive operational intelligence. This should be the final intelligence screen of the entire Access Control module.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every access intelligence forecasting",
       "columns": [
        "AiAccessIntelligenceForecastingExecutiveInsightsView.tomorrowSAttendance",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.peakArrivalTime",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.peakExitTime",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.venueOccupancy",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.zoneOccupancy",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.gateDemand",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.groupArrivalPressure",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.reEntryDemand"
       ],
       "bindsTo": "AiAccessIntelligenceForecastingExecutiveInsightsView",
       "operation": "listAccessExecutiveInsight",
       "provenance": "pack Access Control Module_Reference.pdf, page 180 §Forecast"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access intelligence forecasting",
       "bindsTo": "AiAccessIntelligenceForecastingExecutiveInsightsView",
       "columns": [
        "AiAccessIntelligenceForecastingExecutiveInsightsView.tomorrowSAttendance",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.peakArrivalTime",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.peakExitTime",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.venueOccupancy",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.zoneOccupancy",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.gateDemand",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.groupArrivalPressure",
        "AiAccessIntelligenceForecastingExecutiveInsightsView.reEntryDemand"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Expected Attendance”, “Peak Arrival”, “Current Planned”, “Board 12 Key Workflow”, “Final Access Control Architecture”, “Board Area”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 180 §Forecast"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access intelligence forecasting list.",
   "error": "Could not load. Names which read failed and leaves the access intelligence forecasting untouched.",
   "emptyFirstRun": "No access intelligence forecasting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access intelligence forecasting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessExecutiveInsight",
    "contract": "access",
    "purpose": "AI Access Intelligence, Forecasting & Executive Insights",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiAccessIntelligenceForecastingExecutiveInsightsView.tomorrowSAttendance",
    "AiAccessIntelligenceForecastingExecutiveInsightsView.peakArrivalTime",
    "AiAccessIntelligenceForecastingExecutiveInsightsView.peakExitTime",
    "AiAccessIntelligenceForecastingExecutiveInsightsView.venueOccupancy",
    "AiAccessIntelligenceForecastingExecutiveInsightsView.zoneOccupancy",
    "AiAccessIntelligenceForecastingExecutiveInsightsView.gateDemand"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-263",
   "workshopBoard": "wireframes/WS29 Access Control Board 12.dc.html#bo-263"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 180. 8 of 8 labels bound to a contract property; 8 of 62 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createReportSchedule": {
  "method": "POST",
  "path": "/report-schedules",
  "contract": "reporting",
  "summary": "Schedule a report",
  "permission": "REPORT_SCHEDULE",
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
  "requestBody": "CreateReportScheduleRequest",
  "responds": "ReportSchedule"
 },
 "deleteReportSchedule": {
  "method": "DELETE",
  "path": "/report-schedules/{scheduleId}",
  "contract": "reporting",
  "summary": "Delete a schedule",
  "permission": "REPORT_SCHEDULE",
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
 "listAccessExecutiveInsight": {
  "method": "GET",
  "path": "/access-executive-insight",
  "contract": "access",
  "summary": "AI Access Intelligence, Forecasting & Executive Insights",
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
  "responds": "AiAccessIntelligenceForecastingExecutiveInsightsView"
 },
 "listAccessMonitoring": {
  "method": "GET",
  "path": "/access-monitoring",
  "contract": "access",
  "summary": "Access Monitoring & Analytics Command Center",
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
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listAccessReportScheduled": {
  "method": "GET",
  "path": "/access-report-scheduled",
  "contract": "access",
  "summary": "Access Reports, Scheduled Reporting & Data Export",
  "permission": "REPORT_VIEW_VENUE",
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
    "name": "park",
    "in": "query",
    "required": false
   },
   {
    "name": "zone",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketType",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "gate",
    "in": "query",
    "required": false
   },
   {
    "name": "device",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "AccessReportsScheduledReportingDataExportView"
 },
 "listAttendanceAdmission": {
  "method": "GET",
  "path": "/attendance-admission",
  "contract": "access",
  "summary": "Attendance & Admission Analytics",
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
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "timeslot",
    "in": "query",
    "required": false
   },
   {
    "name": "membership",
    "in": "query",
    "required": false
   },
   {
    "name": "b2bPartner",
    "in": "query",
    "required": false
   },
   {
    "name": "reseller",
    "in": "query",
    "required": false
   },
   {
    "name": "guestCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketType",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "AttendanceAdmissionAnalyticsView"
 },
 "listEntryExitCrossover": {
  "method": "GET",
  "path": "/entry-exit-crossover",
  "contract": "access",
  "summary": "Entry, Exit, Re-entry & Crossover Analytics",
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
  "responds": "EntryExitReEntryCrossoverAnalyticsView"
 },
 "listGraphicalAccessMap": {
  "method": "GET",
  "path": "/graphical-access-map",
  "contract": "access",
  "summary": "Graphical Access Map & Live Gate Performance",
  "permission": "SCOPE_VIEW",
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
    "name": "zone",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "GraphicalAccessMapLiveGatePerformanceView"
 },
 "listGuestDwellTime": {
  "method": "GET",
  "path": "/guest-dwell-time",
  "contract": "access",
  "summary": "Guest Dwell Time, Length of Stay & Attraction Flow",
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
  "responds": "GuestDwellTimeLengthOfStayAttractionFlowView"
 },
 "listLiveVenueOccupancy": {
  "method": "GET",
  "path": "/live-venue-occupancy",
  "contract": "access",
  "summary": "Live Venue Occupancy & People Counting",
  "permission": "SCOPE_VIEW",
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
  "responds": "LiveVenueOccupancyPeopleCountingView"
 },
 "listReportSchedules": {
  "method": "GET",
  "path": "/report-schedules",
  "contract": "reporting",
  "summary": "List scheduled reports",
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
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listReports": {
  "method": "GET",
  "path": "/reports",
  "contract": "reporting",
  "summary": "List available report definitions",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "category",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
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
 "listThroughputQueueValidation": {
  "method": "GET",
  "path": "/throughput-queue-validation",
  "contract": "access",
  "summary": "Throughput, Queue & Validation Performance Analytics",
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
  "responds": "ThroughputQueueValidationPerformanceAnalyticsView"
 },
 "listValidationOutcomeRejection": {
  "method": "GET",
  "path": "/validation-outcome-rejection",
  "contract": "access",
  "summary": "Validation Outcome & Rejection Analytics",
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
    "name": "gate",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketType",
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
    "name": "operator",
    "in": "query",
    "required": false
   },
   {
    "name": "device",
    "in": "query",
    "required": false
   },
   {
    "name": "credentialType",
    "in": "query",
    "required": false
   },
   {
    "name": "time",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ValidationOutcomeRejectionAnalyticsView"
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
 },
 "updateReportSchedule": {
  "method": "PATCH",
  "path": "/report-schedules/{scheduleId}",
  "contract": "reporting",
  "summary": "Amend, pause or resume a schedule",
  "permission": "REPORT_SCHEDULE",
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
  "responds": "ReportSchedule"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessReportsScheduledReportingDataExportView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Reports, Scheduled Reporting & Data Export displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "name": {
    "type": "string"
   },
   "reportId": {
    "type": "string"
   },
   "formats": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dashboard",
      "csv",
      "xlsx",
      "pdf",
      "apiDataFeed",
      "biIntegration"
     ]
    }
   },
   "filterCriteria": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Saved filters, e.g. venue=..., gate=..."
   },
   "scheduleTime": {
    "type": "string",
    "description": "Local time of day, e.g. 07:00"
   },
   "recipients": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Authorized recipients or reporting destinations"
   }
  },
  "required": [
   "reportId",
   "name"
  ]
 },
 "AiAccessIntelligenceForecastingExecutiveInsightsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What AI Access Intelligence, Forecasting & Executive Insights displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tomorrowSAttendance": {
    "type": "integer",
    "description": "Tomorrow's Attendance"
   },
   "peakArrivalTime": {
    "type": "string",
    "description": "Forecast time window, e.g. 09:40-10:30"
   },
   "peakExitTime": {
    "type": "string",
    "description": "Forecast time window"
   },
   "venueOccupancy": {
    "type": "integer",
    "description": "Venue Occupancy"
   },
   "zoneOccupancy": {
    "type": "integer",
    "description": "Zone Occupancy"
   },
   "gateDemand": {
    "type": "integer",
    "description": "Forecast guests per hour at peak across gates"
   },
   "groupArrivalPressure": {
    "type": "string",
    "description": "Group Arrival Pressure"
   },
   "reEntryDemand": {
    "type": "string",
    "description": "Re-entry Demand"
   },
   "deviceCapacity": {
    "type": "integer",
    "description": "Device Capacity"
   },
   "currentPlanned": {
    "type": "integer",
    "description": "Entry lanes currently planned"
   },
   "recommendedEntryLanes": {
    "type": "integer"
   },
   "aiRecommendation": {
    "type": "string",
    "description": "Advisory text only; any operational change goes through the normal permission and approval controls"
   }
  }
 },
 "AttendanceAdmissionAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Attendance & Admission Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketsSold": {
    "type": "integer",
    "description": "Tickets Sold"
   },
   "ticketsEligibleToday": {
    "type": "integer",
    "description": "Tickets Eligible Today"
   },
   "ticketsScanned": {
    "type": "integer",
    "description": "Tickets Scanned"
   },
   "uniqueGuests": {
    "type": "integer",
    "description": "Unique Guests"
   },
   "noShows": {
    "type": "integer",
    "description": "No-Shows"
   },
   "groupAttendance": {
    "type": "integer",
    "description": "Group Attendance"
   },
   "membershipAttendance": {
    "type": "integer",
    "description": "Membership Attendance"
   },
   "repeatEntry": {
    "type": "integer",
    "description": "Repeat Entry"
   },
   "attendanceRate": {
    "type": "number",
    "description": "Percent"
   },
   "noShowRate": {
    "type": "number",
    "description": "no-show rate"
   }
  }
 },
 "Cadence": {
  "x-ticvai-persistence": "none — embedded in schedule",
  "type": "object",
  "description": "**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n",
  "required": [
   "frequency"
  ],
  "properties": {
   "frequency": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     "quarterly",
     "onShiftClose",
     "onPeriodClose"
    ]
   },
   "dayOfWeek": {
    "type": "integer",
    "minimum": 0,
    "maximum": 6
   },
   "dayOfMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 31
   },
   "timeOfDay": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "timeZone": {
    "type": "string",
    "readOnly": true,
    "description": "Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."
   }
  }
 },
 "CreateReportScheduleRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "reportId",
   "cadence",
   "recipients",
   "format"
  ],
  "properties": {
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "cadence": {
    "$ref": "#/components/schemas/Cadence"
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."
   },
   "recipients": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/Recipient"
    }
   },
   "format": {
    "$ref": "#/components/schemas/ExportFormat"
   },
   "includePersonalData": {
    "type": "boolean",
    "default": false
   },
   "skipIfEmpty": {
    "type": "boolean",
    "default": true,
    "description": "An empty report every morning trains people to ignore the report."
   }
  }
 },
 "EntryExitReEntryCrossoverAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Entry, Exit, Re-entry & Crossover Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "reEntryRate": {
    "type": "number",
    "description": "Re-entry rate"
   },
   "averageTimeOutside": {
    "type": "integer",
    "description": "Minutes"
   },
   "mostUsedReEntryGates": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "most-used re-entry gates"
   },
   "rejectedReEntry": {
    "type": "integer",
    "description": "rejected re-entry"
   },
   "reEntryByProduct": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Product and re-entry count pairs"
   },
   "crossoverTime": {
    "type": "integer",
    "description": "Average minutes between leaving one park and entering the next"
   },
   "crossoverProduct": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Products used for crossover, with counts"
   },
   "crossoverUtilization": {
    "type": "number",
    "description": "crossover utilization"
   },
   "firstEntries": {
    "type": "integer"
   },
   "temporaryExits": {
    "type": "integer"
   },
   "reEntries": {
    "type": "integer"
   },
   "crossovers": {
    "type": "integer"
   },
   "finalExits": {
    "type": "integer"
   },
   "crossoverFlows": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "From park, to park and count, e.g. Park A to Park B"
   }
  }
 },
 "ExecutionStatus": {
  "type": "string",
  "enum": [
   "queued",
   "running",
   "completed",
   "failed",
   "cancelled",
   "expired"
  ]
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
 "GraphicalAccessMapLiveGatePerformanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Graphical Access Map & Live Gate Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "accessPointId": {
    "type": "string"
   },
   "pointType": {
    "type": "string",
    "enum": [
     "gate",
     "turnstile",
     "entryPoint",
     "exitPoint",
     "reEntryGate",
     "groupGate",
     "vipGate",
     "attractionAccess",
     "crossoverPoint"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "healthy",
     "warning",
     "critical",
     "offline"
    ]
   },
   "guests": {
    "type": "integer",
    "description": "Guests (the pack shows 4,821)"
   },
   "success": {
    "type": "number",
    "description": "Success rate, percent"
   },
   "reject": {
    "type": "number",
    "description": "Reject rate, percent"
   },
   "yellow": {
    "type": "number",
    "description": "Operator-review rate, percent"
   },
   "name": {
    "type": "string"
   },
   "parentId": {
    "type": "string",
    "description": "Zone or park the point sits in"
   },
   "throughputPerMinute": {
    "type": "number"
   },
   "averageValidationSeconds": {
    "type": "number"
   }
  },
  "required": [
   "accessPointId",
   "pointType",
   "status"
  ]
 },
 "GuestDwellTimeLengthOfStayAttractionFlowView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Guest Dwell Time, Length of Stay & Attraction Flow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "averageLengthOfStay": {
    "type": "integer",
    "description": "Minutes, where entry and exit data exist"
   },
   "medianStay": {
    "type": "integer",
    "description": "Minutes"
   },
   "peakArrival": {
    "type": "string",
    "description": "Time window, e.g. 09:40-10:30"
   },
   "peakDeparture": {
    "type": "string",
    "description": "Time window"
   },
   "zoneDwellTime": {
    "type": "integer",
    "description": "Average minutes in the selected zone"
   },
   "attractionVisits": {
    "type": "integer",
    "description": "Attraction Visits"
   },
   "fastPassUsage": {
    "type": "integer",
    "description": "Fast Pass Usage"
   },
   "reEntryBehavior": {
    "type": "string",
    "description": "Re-entry behavior"
   },
   "uniqueGuests": {
    "type": "integer",
    "description": "Unique Guests (the pack shows 5,842)"
   },
   "totalValidations": {
    "type": "integer",
    "description": "Total Validations (the pack shows 6,211)"
   },
   "repeatVisits": {
    "type": "integer",
    "description": "Repeat Visits (the pack shows 369)"
   }
  }
 },
 "LiveVenueOccupancyPeopleCountingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Live Venue Occupancy & People Counting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "areaLevel": {
    "type": "string",
    "enum": [
     "venue",
     "park",
     "zone",
     "attraction",
     "controlledArea"
    ]
   },
   "areaId": {
    "type": "string"
   },
   "exits": {
    "type": "integer",
    "description": "Exits (the pack shows ±)"
   },
   "operationalAdjustments": {
    "type": "integer",
    "description": "Operational Adjustments (the pack shows =)"
   },
   "current": {
    "type": "integer",
    "description": "Current (the pack shows 8,214)"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity (the pack shows 12,000)"
   },
   "occupancy": {
    "type": "number",
    "description": "Percent of capacity"
   },
   "areaName": {
    "type": "string"
   },
   "parentAreaId": {
    "type": "string"
   },
   "entries": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "normal",
     "warning",
     "high",
     "critical"
    ],
    "description": "Band from the configured occupancy thresholds"
   }
  },
  "required": [
   "areaId",
   "areaLevel"
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
 "Recipient": {
  "x-ticvai-persistence": "reporting.schedule_recipient",
  "type": "object",
  "description": "One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n",
  "required": [
   "kind",
   "address"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "principal",
     "email",
     "sftp",
     "webhook"
    ]
   },
   "address": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
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
 "ReportSchedule": {
  "x-ticvai-persistence": "reporting.schedule + reporting.schedule_recipient",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportScheduleRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "isPaused",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid",
      "description": "The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"
     },
     "isPaused": {
      "type": "boolean"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "lastRunStatus": {
      "$ref": "#/components/schemas/ExecutionStatus"
     },
     "nextRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "consecutiveFailures": {
      "type": "integer"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
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
 "ThroughputQueueValidationPerformanceAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Throughput, Queue & Validation Performance Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "gateId": {
    "type": "string"
   },
   "guestsPerMinute": {
    "type": "number",
    "description": "Guests per Minute"
   },
   "guestsPerHour": {
    "type": "integer",
    "description": "Guests per Hour"
   },
   "averageScanTime": {
    "type": "number",
    "description": "Seconds"
   },
   "averageGateCycle": {
    "type": "number",
    "description": "Seconds"
   },
   "successRate": {
    "type": "number",
    "description": "Success Rate"
   },
   "yellowRate": {
    "type": "number",
    "description": "Yellow Rate"
   },
   "manualInterventionRate": {
    "type": "number",
    "description": "Manual Intervention Rate"
   },
   "downtime": {
    "type": "integer",
    "description": "Minutes"
   },
   "bottleneckReason": {
    "type": "string",
    "enum": [
     "qrReadFailures",
     "excessiveManualVerification",
     "hardwareLatency",
     "policyComplexity",
     "wrongGuestRouting"
    ],
    "description": "Vocabulary listed under Potential reasons."
   },
   "gateName": {
    "type": "string"
   },
   "rejectRate": {
    "type": "number",
    "description": "Percent"
   },
   "underperforming": {
    "type": "boolean"
   }
  },
  "required": [
   "gateId"
  ]
 },
 "ValidationOutcomeRejectionAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Validation Outcome & Rejection Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "rejected": {
    "type": "integer",
    "description": "Rejected (the pack shows 482)"
   },
   "overrides": {
    "type": "integer",
    "description": "Overrides (the pack shows 281)"
   },
   "allowedRate": {
    "type": "number",
    "description": "Percent"
   },
   "operatorReviewRate": {
    "type": "number",
    "description": "Percent"
   },
   "deniedRate": {
    "type": "number",
    "description": "Percent"
   },
   "overrideRate": {
    "type": "number",
    "description": "Overrides as a percent of rejections"
   },
   "rejectionReasons": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Reason, count and share, e.g. Wrong Visit Date"
   }
  }
 }
}
```
