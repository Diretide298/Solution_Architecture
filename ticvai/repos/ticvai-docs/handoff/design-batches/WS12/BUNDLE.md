# WS12 — Access Control board 12

**10 screens · 10 operations · 10 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
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
| `BO-262` | Access Reports, Scheduled Reporting & Data Export | listDetail | 1 | 0 | — |
| `BO-263` | AI Access Intelligence, Forecasting & Executive Insights | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-254, BO-255, BO-256, BO-258, BO-260, BO-262, BO-263 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide a single executive and operational overview of access performance across all TICVAI-controlled venues.",
  "purposeNote": "Management can understand the overall access operation from one screen.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every access monitoring analytics",
       "columns": [
        "AccessMonitoringAnalyticsCommandCenterView.totalAdmissionsToday",
        "AccessMonitoringAnalyticsCommandCenterView.entries",
        "AccessMonitoringAnalyticsCommandCenterView.exits",
        "AccessMonitoringAnalyticsCommandCenterView.currentlyInVenue",
        "AccessMonitoringAnalyticsCommandCenterView.reEntries",
        "AccessMonitoringAnalyticsCommandCenterView.crossovers",
        "AccessMonitoringAnalyticsCommandCenterView.groupAdmissions",
        "AccessMonitoringAnalyticsCommandCenterView.fastPassUses",
        "AccessMonitoringAnalyticsCommandCenterView.validScans",
        "AccessMonitoringAnalyticsCommandCenterView.rejectedScans",
        "AccessMonitoringAnalyticsCommandCenterView.interventionRate",
        "AccessMonitoringAnalyticsCommandCenterView.averageValidationTime",
        "AccessMonitoringAnalyticsCommandCenterView.activeGates",
        "AccessMonitoringAnalyticsCommandCenterView.offlineDevices"
       ],
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
       "columns": [
        "AccessMonitoringAnalyticsCommandCenterView.totalAdmissionsToday",
        "AccessMonitoringAnalyticsCommandCenterView.entries",
        "AccessMonitoringAnalyticsCommandCenterView.exits",
        "AccessMonitoringAnalyticsCommandCenterView.currentlyInVenue",
        "AccessMonitoringAnalyticsCommandCenterView.reEntries",
        "AccessMonitoringAnalyticsCommandCenterView.crossovers",
        "AccessMonitoringAnalyticsCommandCenterView.groupAdmissions",
        "AccessMonitoringAnalyticsCommandCenterView.fastPassUses",
        "AccessMonitoringAnalyticsCommandCenterView.validScans",
        "AccessMonitoringAnalyticsCommandCenterView.rejectedScans",
        "AccessMonitoringAnalyticsCommandCenterView.interventionRate",
        "AccessMonitoringAnalyticsCommandCenterView.averageValidationTime",
        "AccessMonitoringAnalyticsCommandCenterView.activeGates",
        "AccessMonitoringAnalyticsCommandCenterView.offlineDevices"
       ],
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
    "AccessMonitoringAnalyticsCommandCenterView.totalAdmissionsToday",
    "AccessMonitoringAnalyticsCommandCenterView.entries",
    "AccessMonitoringAnalyticsCommandCenterView.exits",
    "AccessMonitoringAnalyticsCommandCenterView.currentlyInVenue",
    "AccessMonitoringAnalyticsCommandCenterView.reEntries",
    "AccessMonitoringAnalyticsCommandCenterView.crossovers"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-254"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-255"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Turn the graphical access topology created in Board 1 into a live operational analytics map.",
  "purposeNote": "Operations can visually identify where access bottlenecks or abnormal conditions are occurring.",
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
        "GraphicalAccessMapLiveGatePerformanceView.gates",
        "GraphicalAccessMapLiveGatePerformanceView.turnstiles",
        "GraphicalAccessMapLiveGatePerformanceView.entryPoints",
        "GraphicalAccessMapLiveGatePerformanceView.exitPoints",
        "GraphicalAccessMapLiveGatePerformanceView.reEntryGates",
        "GraphicalAccessMapLiveGatePerformanceView.groupGates",
        "GraphicalAccessMapLiveGatePerformanceView.vipGates",
        "GraphicalAccessMapLiveGatePerformanceView.attractionAccess"
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
        "GraphicalAccessMapLiveGatePerformanceView.gates",
        "GraphicalAccessMapLiveGatePerformanceView.turnstiles",
        "GraphicalAccessMapLiveGatePerformanceView.entryPoints",
        "GraphicalAccessMapLiveGatePerformanceView.exitPoints",
        "GraphicalAccessMapLiveGatePerformanceView.reEntryGates",
        "GraphicalAccessMapLiveGatePerformanceView.groupGates",
        "GraphicalAccessMapLiveGatePerformanceView.vipGates",
        "GraphicalAccessMapLiveGatePerformanceView.attractionAccess"
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
    "GraphicalAccessMapLiveGatePerformanceView.gates",
    "GraphicalAccessMapLiveGatePerformanceView.turnstiles",
    "GraphicalAccessMapLiveGatePerformanceView.entryPoints",
    "GraphicalAccessMapLiveGatePerformanceView.exitPoints",
    "GraphicalAccessMapLiveGatePerformanceView.reEntryGates",
    "GraphicalAccessMapLiveGatePerformanceView.groupGates"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-256"
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
        "AttendanceAdmissionAnalyticsView.ticketType",
        "Product",
        "AttendanceAdmissionAnalyticsView.event",
        "Timeslot",
        "Membership",
        "AttendanceAdmissionAnalyticsView.channel",
        "B2B Partner",
        "Reseller",
        "AttendanceAdmissionAnalyticsView.customerSegment",
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
        "AttendanceAdmissionAnalyticsView.noShowRate",
        "AttendanceAdmissionAnalyticsView.ticketType",
        "AttendanceAdmissionAnalyticsView.channel",
        "AttendanceAdmissionAnalyticsView.event",
        "AttendanceAdmissionAnalyticsView.dateTime"
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
        "AttendanceAdmissionAnalyticsView.noShowRate",
        "AttendanceAdmissionAnalyticsView.ticketType",
        "AttendanceAdmissionAnalyticsView.channel",
        "AttendanceAdmissionAnalyticsView.event",
        "AttendanceAdmissionAnalyticsView.dateTime"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-257"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Measure) and no metric row",
  "purpose": "Analyze complete guest movement across the access journey.",
  "purposeNote": "Management can understand actual movement patterns rather than only total admission counts.",
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
        "EntryExitReEntryCrossoverAnalyticsView.parkAParkB",
        "EntryExitReEntryCrossoverAnalyticsView.parkBParkA",
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
        "EntryExitReEntryCrossoverAnalyticsView.parkAParkB",
        "EntryExitReEntryCrossoverAnalyticsView.parkBParkA",
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
    "EntryExitReEntryCrossoverAnalyticsView.rejectedReEntry",
    "EntryExitReEntryCrossoverAnalyticsView.parkAParkB",
    "EntryExitReEntryCrossoverAnalyticsView.parkBParkA"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-258"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure the operational efficiency of gates and validation devices.",
  "purposeNote": "Management can identify why specific gates or lanes are underperforming.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-259"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Analyze why guests are denied or require manual intervention.",
  "purposeNote": "Management can identify the operational root cause behind access failures.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-260"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Use access events to understand how guests move through and use the venue.",
  "purposeNote": "systems.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-261"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide configurable operational and management reports.",
  "purposeNote": "Authorized users can create, schedule and export access-control reports without development support.",
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
       "columns": [
        "AccessReportsScheduledReportingDataExportView.tenant",
        "AccessReportsScheduledReportingDataExportView.venue",
        "AccessReportsScheduledReportingDataExportView.park",
        "AccessReportsScheduledReportingDataExportView.zone",
        "AccessReportsScheduledReportingDataExportView.event",
        "AccessReportsScheduledReportingDataExportView.date",
        "AccessReportsScheduledReportingDataExportView.ticketType",
        "AccessReportsScheduledReportingDataExportView.product",
        "AccessReportsScheduledReportingDataExportView.gate",
        "AccessReportsScheduledReportingDataExportView.device",
        "AccessReportsScheduledReportingDataExportView.channel"
       ],
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-262"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 179. 11 of 11 labels bound to a contract property; 11 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast) and no metric row",
  "purpose": "Turn access-control data into proactive operational intelligence. This should be the final intelligence screen of the entire Access Control module.",
  "purposeNote": "dashboards alone. Board 12 — Final 10-Screen Structure # Backend Screen Main Responsibility 12.1 Access Monitoring & Analytics Command Center Executive access overview 12.2 Live Venue Occupancy & People Counting Real-time occupancy 12.3 Graphical Access Map & Live Gate Performance Visual venue/gate monitoring 12.4 Attendance & Admission Analytics Actual attendance and no-shows 12.5 Entry, Exit, Re-entry & Crossover Analytics Complete guest movement 12.6 Throughput, Queue & Validation Performance Analytics Gate operational efficiency 12.7 Validation Outcome & Rejection Analytics Failure and int",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-263"
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
 "listAccessExecutiveInsight": {
  "method": "GET",
  "path": "/access-executive-insight",
  "contract": "access",
  "summary": "AI Access Intelligence, Forecasting & Executive Insights",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiAccessIntelligenceForecastingExecutiveInsightsView"
 },
 "listAccessMonitoring": {
  "method": "GET",
  "path": "/access-monitoring",
  "contract": "access",
  "summary": "Access Monitoring & Analytics Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessMonitoringAnalyticsCommandCenterView"
 },
 "listAccessReportScheduled": {
  "method": "GET",
  "path": "/access-report-scheduled",
  "contract": "access",
  "summary": "Access Reports, Scheduled Reporting & Data Export",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessReportsScheduledReportingDataExportView"
 },
 "listAttendanceAdmission": {
  "method": "GET",
  "path": "/attendance-admission",
  "contract": "access",
  "summary": "Attendance & Admission Analytics",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "GraphicalAccessMapLiveGatePerformanceView"
 },
 "listGuestDwellTime": {
  "method": "GET",
  "path": "/guest-dwell-time",
  "contract": "access",
  "summary": "Guest Dwell Time, Length of Stay & Attraction Flow",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "LiveVenueOccupancyPeopleCountingView"
 },
 "listThroughputQueueValidation": {
  "method": "GET",
  "path": "/throughput-queue-validation",
  "contract": "access",
  "summary": "Throughput, Queue & Validation Performance Analytics",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ThroughputQueueValidationPerformanceAnalyticsView"
 },
 "listValidationOutcomeRejection": {
  "method": "GET",
  "path": "/validation-outcome-rejection",
  "contract": "access",
  "summary": "Validation Outcome & Rejection Analytics",
  "permission": "SCOPE_VIEW",
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
   }
  ],
  "requestBody": null,
  "responds": "ValidationOutcomeRejectionAnalyticsView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessMonitoringAnalyticsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Monitoring & Analytics Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalAdmissionsToday": {
    "type": "integer",
    "description": "Total Admissions Today"
   },
   "entries": {
    "type": "integer",
    "description": "Entries"
   },
   "exits": {
    "type": "integer",
    "description": "Exits"
   },
   "currentlyInVenue": {
    "type": "string",
    "description": "Currently In Venue"
   },
   "reEntries": {
    "type": "integer",
    "description": "Re-entries"
   },
   "crossovers": {
    "type": "integer",
    "description": "Crossovers"
   },
   "groupAdmissions": {
    "type": "integer",
    "description": "Group Admissions"
   },
   "fastPassUses": {
    "type": "integer",
    "description": "Fast Pass Uses"
   },
   "validScans": {
    "type": "integer",
    "description": "Valid Scans"
   },
   "rejectedScans": {
    "type": "integer",
    "description": "Rejected Scans"
   },
   "interventionRate": {
    "type": "number",
    "description": "Intervention Rate"
   },
   "averageValidationTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Validation Time"
   },
   "activeGates": {
    "type": "integer",
    "description": "Active Gates"
   },
   "offlineDevices": {
    "type": "integer",
    "description": "Offline Devices"
   },
   "totalAdmissions": {
    "type": "integer",
    "description": "TOTAL ADMISSIONS (the pack shows 42,684)"
   },
   "avgValidation": {
    "type": "number",
    "description": "AVG. VALIDATION"
   }
  }
 },
 "AccessReportsScheduledReportingDataExportView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Reports, Scheduled Reporting & Data Export displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "device": {
    "type": "string",
    "description": "Device"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "dashboard": {
    "type": "string",
    "description": "Dashboard"
   },
   "csv": {
    "type": "string",
    "description": "CSV"
   },
   "xlsx": {
    "type": "string",
    "description": "XLSX"
   },
   "pdf": {
    "type": "string",
    "description": "PDF"
   },
   "apiDataFeed": {
    "type": "string",
    "description": "API/Data Feed"
   },
   "biIntegration": {
    "type": "string",
    "description": "BI integration"
   },
   "rbac": {
    "type": "string",
    "description": "RBAC"
   },
   "tenantIsolation": {
    "type": "string",
    "description": "tenant isolation"
   },
   "fieldLevelRestrictions": {
    "type": "string",
    "description": "field-level restrictions"
   },
   "retentionRules": {
    "type": "string",
    "description": "retention rules"
   }
  }
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
    "format": "date-time",
    "description": "Peak Arrival Time"
   },
   "peakExitTime": {
    "type": "string",
    "format": "date-time",
    "description": "Peak Exit Time"
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
    "type": "string",
    "description": "Gate Demand"
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
   "expectedAttendance": {
    "type": "integer",
    "description": "Expected Attendance (the pack shows 28,400)"
   },
   "currentPlanned": {
    "type": "string",
    "description": "Current Planned (the pack shows 10)"
   },
   "forecastAiRecommend": {
    "type": "string",
    "description": "Forecast → AI Recommend"
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
    "type": "string",
    "description": "Tickets Sold"
   },
   "ticketsEligibleToday": {
    "type": "string",
    "description": "Tickets Eligible Today"
   },
   "ticketsScanned": {
    "type": "string",
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
    "type": "string",
    "description": "Repeat Entry"
   },
   "attendanceRate": {
    "type": "integer",
    "description": "Attendance Rate"
   },
   "noShowRate": {
    "type": "number",
    "description": "no-show rate"
   },
   "ticketType": {
    "type": "string",
    "description": "ticket type"
   },
   "channel": {
    "type": "string",
    "description": "channel"
   },
   "event": {
    "type": "string",
    "description": "event"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "date/time"
   },
   "customerSegment": {
    "type": "string",
    "description": "customer segment"
   },
   "sold": {
    "type": "string",
    "description": "Sold (the pack shows 25,000)"
   },
   "eligible": {
    "type": "string",
    "description": "Eligible (the pack shows 23,842)"
   },
   "attended": {
    "type": "string",
    "description": "Attended (the pack shows 21,384)"
   },
   "purchased": {
    "type": "string",
    "description": "Purchased (the pack shows 120)"
   },
   "actualAttendance": {
    "type": "integer",
    "description": "Actual Attendance (the pack shows 112)"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance (the pack shows 93.3%)"
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
    "type": "string",
    "format": "date-time",
    "description": "average time outside"
   },
   "mostUsedReEntryGates": {
    "type": "integer",
    "description": "most-used re-entry gates"
   },
   "rejectedReEntry": {
    "type": "integer",
    "description": "rejected re-entry"
   },
   "reEntryByProduct": {
    "type": "string",
    "description": "re-entry by product"
   },
   "parkAParkB": {
    "type": "string",
    "description": "Park A → Park B"
   },
   "parkBParkA": {
    "type": "string",
    "description": "Park B → Park A"
   },
   "crossoverTime": {
    "type": "string",
    "format": "date-time",
    "description": "crossover time"
   },
   "crossoverProduct": {
    "type": "string",
    "description": "crossover product"
   },
   "crossoverUtilization": {
    "type": "number",
    "description": "crossover utilization"
   },
   "waterPark": {
    "type": "string",
    "description": "Water Park (the pack shows 1,327)"
   }
  }
 },
 "GraphicalAccessMapLiveGatePerformanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Graphical Access Map & Live Gate Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "gates": {
    "type": "integer",
    "description": "Gates"
   },
   "turnstiles": {
    "type": "integer",
    "description": "Turnstiles"
   },
   "entryPoints": {
    "type": "integer",
    "description": "Entry points"
   },
   "exitPoints": {
    "type": "integer",
    "description": "Exit points"
   },
   "reEntryGates": {
    "type": "integer",
    "description": "Re-entry gates"
   },
   "groupGates": {
    "type": "integer",
    "description": "Group gates"
   },
   "vipGates": {
    "type": "integer",
    "description": "VIP gates"
   },
   "attractionAccess": {
    "type": "string",
    "description": "attraction access"
   },
   "crossoverPoints": {
    "type": "integer",
    "description": "crossover points"
   },
   "healthy": {
    "type": "string",
    "description": "🟢 Healthy"
   },
   "warning": {
    "type": "string",
    "description": "🟡 Warning"
   },
   "critical": {
    "type": "string",
    "description": "🔴 Critical"
   },
   "offline": {
    "type": "integer",
    "description": "⚫ Offline"
   },
   "guests": {
    "type": "integer",
    "description": "Guests (the pack shows 171 | Pa ge, 4,821)"
   },
   "success": {
    "type": "string",
    "description": "Success (the pack shows 96.4%)"
   },
   "reject": {
    "type": "string",
    "description": "Reject (the pack shows 2.1%)"
   },
   "yellow": {
    "type": "string",
    "description": "Yellow (the pack shows 1.5%)"
   }
  }
 },
 "GuestDwellTimeLengthOfStayAttractionFlowView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Guest Dwell Time, Length of Stay & Attraction Flow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "averageLengthOfStay": {
    "type": "number",
    "description": "Average Length of Stay"
   },
   "medianStay": {
    "type": "string",
    "description": "Median Stay"
   },
   "peakArrival": {
    "type": "string",
    "description": "Peak Arrival"
   },
   "peakDeparture": {
    "type": "string",
    "description": "Peak Departure"
   },
   "zoneDwellTime": {
    "type": "string",
    "format": "date-time",
    "description": "Zone Dwell Time"
   },
   "attractionVisits": {
    "type": "integer",
    "description": "Attraction Visits"
   },
   "fastPassUsage": {
    "type": "string",
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
   "fastPass": {
    "type": "string",
    "description": "Fast Pass (the pack shows 1,827)"
   },
   "repeatVisits": {
    "type": "integer",
    "description": "Repeat Visits (the pack shows 369)"
   },
   "unnecessary": {
    "type": "string",
    "description": "unnecessary"
   }
  }
 },
 "LiveVenueOccupancyPeopleCountingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Live Venue Occupancy & People Counting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "exits": {
    "type": "integer",
    "description": "Exits (the pack shows ±)"
   },
   "operationalAdjustments": {
    "type": "integer",
    "description": "Operational Adjustments (the pack shows =)"
   },
   "current": {
    "type": "string",
    "description": "Current (the pack shows 8,214)"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity (the pack shows 12,000)"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy (the pack shows 68.5%)"
   },
   "kidsZone": {
    "type": "string",
    "description": "Kids Zone (the pack shows 1,842 / 2,500, 🟢 74%)"
   },
   "adventureZone": {
    "type": "string",
    "description": "Adventure Zone (the pack shows 3,107 / 3,500, 🟠 89%)"
   },
   "vipZone": {
    "type": "string",
    "description": "VIP Zone (the pack shows 421 / 600, 🟢 70%)"
   },
   "normal": {
    "type": "string",
    "description": "Normal (the pack shows 0–79%)"
   },
   "warning": {
    "type": "string",
    "description": "Warning (the pack shows 80–89%)"
   },
   "high": {
    "type": "string",
    "description": "High (the pack shows 90–94%)"
   },
   "critical": {
    "type": "string",
    "description": "Critical (the pack shows 95%+)"
   }
  }
 },
 "ThroughputQueueValidationPerformanceAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Throughput, Queue & Validation Performance Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestsPerMinute": {
    "type": "string",
    "description": "Guests per Minute"
   },
   "guestsPerHour": {
    "type": "string",
    "description": "Guests per Hour"
   },
   "averageScanTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Scan Time"
   },
   "averageGateCycle": {
    "type": "number",
    "description": "Average Gate Cycle"
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
    "type": "string",
    "description": "Downtime"
   },
   "gateGuestsHrValidationRejectIntervention": {
    "type": "string",
    "description": "Gate Guests/hr Validation Reject Intervention"
   },
   "g011482039s1208": {
    "type": "number",
    "description": "G01 1,482 0.39s 1.2% 0.8%"
   },
   "g021391042s1411": {
    "type": "number",
    "description": "G02 1,391 0.42s 1.4% 1.1%"
   },
   "g03821081s8264": {
    "type": "number",
    "description": "G03 821 0.81s 8.2% 6.4%"
   },
   "gate03Underperforming": {
    "type": "string",
    "description": "GATE 03 — UNDERPERFORMING"
   },
   "reasonsType": {
    "type": "string",
    "enum": [
     "qrReadFailures",
     "excessiveManualVerification",
     "hardwareLatency",
     "policyComplexity",
     "wrongGuestRouting"
    ],
    "description": "Vocabulary listed under Potential reasons."
   }
  }
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
   }
  }
 }
}
```
