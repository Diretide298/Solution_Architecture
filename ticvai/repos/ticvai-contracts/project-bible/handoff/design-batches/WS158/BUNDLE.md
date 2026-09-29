# WS158 — Resource Management Configuration board 4

**10 screens · 11 operations · 10 schemas · 3 permissions**

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
  `ATTENDANCE_RECORD, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-883` | Workforce Roster Command Center | listDetail | 2 | 0 | — |
| `BO-884` | Attraction & Operational Staffing Roster | listDetail | 1 | 0 | — |
| `BO-885` | Minimum Staffing & Coverage Rule Configuration | configEditor | 1 | 0 | — |
| `BO-886` | Staffing Gap & Coverage Control Center | listDetail | 1 | 0 | — |
| `BO-887` | Shift Marketplace & Workforce Requests | listDetail | 2 | 0 | — |
| `BO-888` | Attendance & Live Workforce Command Center | listDetail | 1 | 0 | — |
| `BO-889` | Staff Check-In, Check-Out & Attendance Exceptions | configEditor | 2 | 0 | — |
| `BO-890` | Workforce Compliance Validation Center | listDetail | 1 | 0 | — |
| `BO-891` | Labor Cost & Staffing Budget Control | listDetail | 1 | 0 | — |
| `BO-892` | AI Workforce Planner & Roster Optimization | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-883, BO-884, BO-887, BO-888, BO-890, BO-891 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-883",
  "name": "Workforce Roster Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "01",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/workforce-roster-command-center-bo-883",
   "component": "apps/venue-management-web/src/routes/rentals/WorkforceRosterCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-884",
    "BO-885",
    "BO-886",
    "BO-887",
    "BO-888",
    "BO-889",
    "BO-890",
    "BO-891",
    "BO-892"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-884",
     "trigger": "Attraction & Operational Staffing Roster",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-885",
     "trigger": "Minimum Staffing & Coverage Rule Configuration",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-886",
     "trigger": "Staffing Gap & Coverage Control Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-887",
     "trigger": "Shift Marketplace & Workforce Requests",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-888",
     "trigger": "Attendance & Live Workforce Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-889",
     "trigger": "Staff Check-In, Check-Out & Attendance Exceptions",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-890",
     "trigger": "Workforce Compliance Validation Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-891",
     "trigger": "Labor Cost & Staffing Budget Control",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-892",
     "trigger": "AI Workforce Planner & Roster Optimization",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide managers with the primary operational workspace for viewing and managing workforce deployment across venues, attractions, events, departments, and shifts.",
  "purposeNote": "Managers can understand the complete workforce position for their permitted operations and manage staffing directly from one operational roster workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 49"
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
       "impliedBy": "listRotaAssignments",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workforce roster list.",
   "error": "Could not load. Names which read failed and leaves the workforce roster untouched.",
   "emptyFirstRun": "No workforce roster yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workforce roster are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRotaAssignments",
    "contract": "workforce",
    "purpose": "The roster",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getStaffingCoverage",
    "contract": "workforce",
    "purpose": "Where it is short",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-883",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-883"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-884",
  "name": "Attraction & Operational Staffing Roster",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "02",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/attraction-operational-staffing-roster-bo-884",
   "component": "apps/venue-management-web/src/routes/rentals/AttractionOperationalStaffingRoster.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each candidate shall show) and no metric row",
  "purpose": "Create detailed staffing plans for individual attractions, experiences, venues, departments, and events.",
  "purposeNote": "Managers can construct operational staffing rosters against actual attraction, event, experience, and ticketing demand.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 50 §Each candidate shall show"
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
       "label": "Every attraction operational staffing",
       "columns": [
        "Name",
        "Photograph",
        "Role",
        "Skill level",
        "Certifications",
        "Availability",
        "Current hours",
        "Venue",
        "Overtime impact",
        "AI suitability score"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 50 §Each candidate shall show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected attraction operational staffing",
       "bindsTo": null,
       "columns": [
        "Name",
        "Photograph",
        "Role",
        "Skill level",
        "Certifications",
        "Availability",
        "Current hours",
        "Venue",
        "Overtime impact",
        "AI suitability score"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Managers shall select”, “Required”, “Scheduled”, “Managers may assign employees through”, “Ticket/Experience Visibility”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 50 §Each candidate shall show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attraction operational staffing list.",
   "error": "Could not load. Names which read failed and leaves the attraction operational staffing untouched.",
   "emptyFirstRun": "No attraction operational staffing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attraction operational staffing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createRotaAssignment",
    "contract": "workforce",
    "purpose": "Roster a position",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRotaAssignments",
     "getStaffingCoverage"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Name",
    "Photograph",
    "Role",
    "Skill level",
    "Certifications",
    "Availability"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-884",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-884"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 50. 0 of 10 labels bound to a contract property; 10 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-885",
  "name": "Minimum Staffing & Coverage Rule Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "03",
   "page": 52
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/minimum-staffing-coverage-rule-configuration-bo-885",
   "component": "apps/venue-management-web/src/routes/rentals/MinimumStaffingCoverageRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the minimum personnel required to operate safely and effectively.",
  "purposeNote": "Administrators can define fixed and demand-driven staffing requirements that TICVAI automatically evaluates against planned rosters.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Minimum",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Target",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Recommended",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Enforcement",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 52 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The minimum staffing coverage configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the minimum staffing coverage untouched.",
   "emptyFirstRun": "No minimum staffing coverage configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setStaffingRules",
    "contract": "workforce",
    "purpose": "Minimum staffing and cover",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getStaffingCoverage",
     "validateWorkforceCompliance"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-885",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-885"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 52. 0 of 0 labels bound to a contract property; 5 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-886",
  "name": "Staffing Gap & Coverage Control Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "04",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/staffing-gap-coverage-control-center-bo-886",
   "component": "apps/venue-management-web/src/routes/rentals/StaffingGapCoverageControlCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Identify workforce shortages before they create operational problems.",
  "purposeNote": "Managers can identify planned and live staffing gaps and receive actionable recommendations for resolving them.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 53"
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
       "kind": "datePicker",
       "label": "From",
       "operation": "getStaffingCoverage",
       "notes": "Sends `?from=` (required).",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "getStaffingCoverage",
       "notes": "Sends `?to=` (required).",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "operation": "getStaffingCoverage",
       "notes": "Sends `?venueId=`.",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "selectField",
       "label": "Severity",
       "operation": "getStaffingCoverage",
       "notes": "Client-side on `severity` (covered, tight, short, blocking); the pack's Informational / Warning / High / Critical scale does not map one to one.",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Planned gap",
       "bindsTo": "StaffingCoverage",
       "columns": [
        "StaffingCoverage.gap"
       ],
       "operation": "getStaffingCoverage",
       "notes": "Summed across positions.",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "metricTile",
       "label": "Blocking gaps",
       "bindsTo": "StaffingCoverage",
       "columns": [
        "StaffingCoverage.severity"
       ],
       "operation": "getStaffingCoverage",
       "notes": "Count where `severity` is blocking.",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "metricTile",
       "label": "Live operational gap",
       "columns": [
        "Live operational gap"
       ],
       "notes": "Required against checked-in staff (the pack's 12 required / 9 checked in = 3); no attendance field is returned.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 53"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Coverage by position",
       "bindsTo": "StaffingCoverage",
       "columns": [
        "StaffingCoverage.date",
        "StaffingCoverage.label",
        "StaffingCoverage.positionCode",
        "StaffingCoverage.from",
        "StaffingCoverage.to",
        "StaffingCoverage.required",
        "StaffingCoverage.rostered",
        "StaffingCoverage.qualified",
        "Checked in",
        "StaffingCoverage.gap",
        "StaffingCoverage.severity"
       ],
       "operation": "getStaffingCoverage",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected gap",
       "bindsTo": "StaffingCoverage",
       "columns": [
        "StaffingCoverage.venueId",
        "StaffingCoverage.label",
        "StaffingCoverage.from",
        "StaffingCoverage.to",
        "StaffingCoverage.required",
        "StaffingCoverage.rostered",
        "StaffingCoverage.qualified",
        "StaffingCoverage.gap",
        "StaffingCoverage.severity",
        "StaffingCoverage.openShiftIds",
        "Gap type",
        "Recommended employee",
        "Match score"
       ],
       "operation": "getStaffingCoverage",
       "notes": "Gap type (missing staff / role / skill / certification, absence- or demand-created) and the AI recommendation are pack labels.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 54"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staffing gap coverage list.",
   "error": "Could not load. Names which read failed and leaves the staffing gap coverage untouched.",
   "emptyFirstRun": "No staffing gap coverage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the staffing gap coverage are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getStaffingCoverage",
    "contract": "workforce",
    "purpose": "Gaps, by severity",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-886",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-886"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Resource_Management_Configuration_Reference.pdf p.53; pack Resource_Management_Configuration_Reference.pdf p.54; contract workforce.yaml GET /staffing-coverage. Pack labels with no schema field yet (shown as plain labels): Live operational gap, Checked-in (actual attendance), Gap type, Recommended employee, Match score.",
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
  "id": "BO-887",
  "name": "Shift Marketplace & Workforce Requests",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "05",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/shift-marketplace-workforce-requests-bo-887",
   "component": "apps/venue-management-web/src/routes/rentals/ShiftMarketplaceWorkforceRequests.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow employees and managers to manage shift changes through controlled workflows rather than informal manual communication.",
  "purposeNote": "Employees can request governed shift changes while TICVAI automatically validates qualifications, workforce rules, and operational coverage before approval.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 54"
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
       "impliedBy": "listOpenShifts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "claimOpenShift",
       "label": "Claim open shift",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "claimOpenShift"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The shift marketplace workforce list.",
   "error": "Could not load. Names which read failed and leaves the shift marketplace workforce untouched.",
   "emptyFirstRun": "No shift marketplace workforce yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the shift marketplace workforce are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOpenShifts",
    "contract": "workforce",
    "purpose": "The shift marketplace",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "claimOpenShift",
    "contract": "workforce",
    "purpose": "Pick one up",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listOpenShifts",
     "getStaffingCoverage"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-887",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-887"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-888",
  "name": "Attendance & Live Workforce Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "06",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/attendance-live-workforce-command-center-bo-888",
   "component": "apps/venue-management-web/src/routes/rentals/AttendanceLiveWorkforceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide real-time visibility into whether scheduled employees actually reported and are available for operation.",
  "purposeNote": "Managers can monitor planned versus actual workforce attendance in real time and immediately understand operational impact.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 55 §Display"
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
       "label": "Every attendance live workforce",
       "columns": [
        "Scheduled today",
        "Checked in",
        "Not yet arrived",
        "Late",
        "Absent",
        "No-show",
        "On break",
        "Checked out",
        "Overtime",
        "Attendance exceptions",
        "Planned vs Actual"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 55 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected attendance live workforce",
       "bindsTo": null,
       "columns": [
        "Scheduled today",
        "Checked in",
        "Not yet arrived",
        "Late",
        "Absent",
        "No-show",
        "On break",
        "Checked out",
        "Overtime",
        "Attendance exceptions",
        "Planned vs Actual"
       ],
       "notes": "The pack groups this record's detail under its own headings: “For each employee”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 55 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attendance live workforce list.",
   "error": "Could not load. Names which read failed and leaves the attendance live workforce untouched.",
   "emptyFirstRun": "No attendance live workforce yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attendance live workforce are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAttendance",
    "contract": "workforce",
    "purpose": "Live attendance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Scheduled today",
    "Checked in",
    "Not yet arrived",
    "Late",
    "Absent",
    "No-show"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-888",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-888"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 55. 0 of 11 labels bound to a contract property; 11 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-889",
  "name": "Staff Check-In, Check-Out & Attendance Exceptions",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "07",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/staff-check-in-check-out-attendance-exceptions-bo-889",
   "component": "apps/venue-management-web/src/routes/rentals/StaffCheckInCheckOutAttendanceExceptions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§The system shall capture; Every correction shall capture) and no display directory — it is settings, not a population",
  "purpose": "Record actual employee working activity and manage exceptions to scheduled attendance.",
  "purposeNote": "handling and complete auditability.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Planned check-in",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Actual check-in",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Planned check-out",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Actual check-out",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Attendance status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Lateness",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Early departure",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Overtime",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "No-show",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Exception",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Source/device",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "selectField",
       "label": "Exception Types",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §The system shall capture"
      },
      {
       "kind": "dataTable",
       "label": "Amendment history",
       "bindsTo": "AttendanceAmendment",
       "columns": [
        "AttendanceAmendment.amendedAt",
        "AttendanceAmendment.amendedByPrincipalId",
        "AttendanceAmendment.occurredAtBefore",
        "AttendanceAmendment.occurredAtAfter",
        "AttendanceAmendment.reason"
       ],
       "operation": "amendAttendance",
       "notes": "**Every correction, not only the last** (decided 28 September, audit R129 (7)) — read from `AttendanceRecord.amendments`: who, when, before, after and why.",
       "provenance": "contract workforce.yaml POST /attendance/{recordId}/amend"
      },
      {
       "kind": "selectField",
       "label": "Original value",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §Every correction shall capture"
      },
      {
       "kind": "selectField",
       "label": "New value",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §Every correction shall capture"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §Every correction shall capture"
      },
      {
       "kind": "selectField",
       "label": "Timestamp",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §Every correction shall capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §Every correction shall capture"
      },
      {
       "kind": "selectField",
       "label": "Approval where required",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §Every correction shall capture"
      },
      {
       "kind": "selectField",
       "label": "Mobile Assignment Check-In",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 56 §Every correction shall capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staff check-in check-out configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the staff check-in check-out untouched.",
   "emptyFirstRun": "No staff check-in check-out configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "recordAttendance",
    "contract": "workforce",
    "purpose": "Check in or out",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAttendance",
     "getLabourCost"
    ]
   },
   {
    "operationId": "amendAttendance",
    "contract": "workforce",
    "purpose": "Correct an exception",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAttendance",
     "getLabourCost"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-889",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-889"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 56. 0 of 0 labels bound to a contract property; 19 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "recordId",
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
  "id": "BO-890",
  "name": "Workforce Compliance Validation Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "08",
   "page": 58
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/workforce-compliance-validation-center-bo-890",
   "component": "apps/venue-management-web/src/routes/rentals/WorkforceComplianceValidationCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each issue shall display) and no metric row",
  "purpose": "Validate planned workforce schedules against legal, safety, certification, and organizational rules before roster publication or assignment.",
  "purposeNote": "No workforce roster is published without passing configured compliance validation or following an explicitly authorized exception workflow.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 58 §Each issue shall display"
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
       "label": "Every workforce compliance validation",
       "columns": [
        "Employee",
        "Rule violated",
        "Severity",
        "Affected shift",
        "Operational impact",
        "Recommended action"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 58 §Each issue shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected workforce compliance validation",
       "bindsTo": null,
       "columns": [
        "Employee",
        "Rule violated",
        "Severity",
        "Affected shift",
        "Operational impact",
        "Recommended action"
       ],
       "notes": "The pack groups this record's detail under its own headings: “The engine shall support”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 58 §Each issue shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workforce compliance validation list.",
   "error": "Could not load. Names which read failed and leaves the workforce compliance validation untouched.",
   "emptyFirstRun": "No workforce compliance validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workforce compliance validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "validateWorkforceCompliance",
    "contract": "workforce",
    "purpose": "Where the rota breaks a rule",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Employee",
    "Rule violated",
    "Severity",
    "Affected shift",
    "Operational impact",
    "Recommended action"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-890",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-890"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 58. 0 of 6 labels bound to a contract property; 6 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-891",
  "name": "Labor Cost & Staffing Budget Control",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "09",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/labor-cost-staffing-budget-control-bo-891",
   "component": "apps/venue-management-web/src/routes/rentals/LaborCostStaffingBudgetControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Give managers visibility into the financial impact of staffing decisions before and after roster publication.",
  "purposeNote": "Managers can understand staffing cost and budget impact before approving workforce plans and can analyze actual labor expenditure after operations.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 59 §Display"
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
       "label": "Every labor cost staffing",
       "columns": [
        "Budget",
        "Scheduled",
        "Forecast",
        "Actual",
        "Variance"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 59 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected labor cost staffing",
       "bindsTo": null,
       "columns": [
        "Budget",
        "Scheduled",
        "Forecast",
        "Actual",
        "Variance"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Cost Calculation”, “Managers shall understand”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 59 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The labor cost staffing list.",
   "error": "Could not load. Names which read failed and leaves the labor cost staffing untouched.",
   "emptyFirstRun": "No labor cost staffing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the labor cost staffing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getLabourCost",
    "contract": "workforce",
    "purpose": "Cost against budget",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Budget",
    "Scheduled",
    "Forecast",
    "Actual",
    "Variance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-891",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-891"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 59. 0 of 5 labels bound to a contract property; 5 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-892",
  "name": "AI Workforce Planner & Roster Optimization",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "4",
   "number": "10",
   "page": 60
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/ai-workforce-planner-roster-optimization-bo-892",
   "component": "apps/venue-management-web/src/routes/rentals/AiWorkforcePlannerRosterOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-883"
   ],
   "exitTo": [
    "BO-883"
   ],
   "transitions": [
    {
     "to": "BO-883",
     "trigger": "Back to Workforce Roster Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide TICVAI's intelligent workforce-planning experience by automatically generating or optimizing operational rosters. Administrators may configure optimization priorities such as: Best operational coverage Minimize overtime Minimize labor cost Balance employee hours Minimize cross-venue movement Maximize skill match Prioritize employee continuity Safety, compliance, and mandatory qualification rules shall remain hard constraints. AI Explanation Provide TICVAI with a centralized Resource Requirement & Assignment Engine that connects ticket products, attraction experiences, sessions, and time slots with the operational resources required to deliver them. Board 5 shall allow administrators to configure: Which resources an experience requires How many resources are required Which resource combinations are valid Which skills and qualifications are mandatory How resource requirements change with ticket quantity or capacity Whether customers may select a specific resource Whether customers may select a resource skill/type rather than a specific person Whether TICVAI should automatically allocate resources How resource priority is calculated What happens when the assigned resource becomes unavailable How assignments are exposed through POS, B2C, B2B, mobile, and APIs",
  "purposeNote": "compliance rules, availability, and cost while retaining human governance over final publication.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 60"
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
       "kind": "datePicker",
       "label": "From",
       "operation": "getStaffingCoverage",
       "notes": "Sends `?from=` (required).",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "getStaffingCoverage",
       "notes": "Sends `?to=` (required).",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "operation": "getStaffingCoverage",
       "notes": "Sends `?venueId=`.",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "selectField",
       "label": "Optimization objective",
       "notes": "Best coverage, minimise overtime, minimise labour cost, balance hours, minimise cross-venue movement, maximise skill match, continuity.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 61"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Staffing gaps (current roster)",
       "bindsTo": "StaffingCoverage",
       "columns": [
        "StaffingCoverage.gap"
       ],
       "operation": "getStaffingCoverage",
       "notes": "Summed; the AI-optimised side of the comparison has no read.",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      },
      {
       "kind": "metricTile",
       "label": "Coverage",
       "columns": [
        "Coverage"
       ],
       "notes": "The pack asks for coverage; the contract has no field for it.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 61"
      },
      {
       "kind": "metricTile",
       "label": "Overtime hours",
       "columns": [
        "Overtime hours"
       ],
       "notes": "The pack asks for overtime hours; the contract has no field for it.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 61"
      },
      {
       "kind": "metricTile",
       "label": "Projected labour cost",
       "columns": [
        "Projected labour cost"
       ],
       "notes": "The pack asks for projected labour cost; the contract has no field for it.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 61"
      },
      {
       "kind": "metricTile",
       "label": "Projected saving",
       "columns": [
        "Projected saving"
       ],
       "notes": "The pack asks for projected saving; the contract has no field for it.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 61"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Current roster coverage",
       "bindsTo": "StaffingCoverage",
       "columns": [
        "StaffingCoverage.date",
        "StaffingCoverage.label",
        "StaffingCoverage.from",
        "StaffingCoverage.to",
        "StaffingCoverage.required",
        "StaffingCoverage.rostered",
        "StaffingCoverage.qualified",
        "StaffingCoverage.gap",
        "StaffingCoverage.severity"
       ],
       "operation": "getStaffingCoverage",
       "provenance": "contract workforce.yaml GET /staffing-coverage"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Why this assignment",
       "columns": [
        "Employee",
        "Assignment",
        "Reasons",
        "Hard constraints satisfied"
       ],
       "notes": "The pack's explanation (\"Available, Level 3 Instructor, certification valid, language match, already at venue, no overtime\").",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 61"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Generate roster with AI",
       "notes": "No roster-generation operation is bound; the pack requires human approval before publishing.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 61"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workforce planner roster list.",
   "error": "Could not load. Names which read failed and leaves the workforce planner roster untouched.",
   "emptyFirstRun": "No workforce planner roster yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workforce planner roster are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getStaffingCoverage",
    "contract": "workforce",
    "purpose": "What the planner is optimising",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-892",
   "workshopBoard": "wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-892"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 60. 0 of 0 labels bound to a contract property; 0 of 118 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Resource_Management_Configuration_Reference.pdf p.61; contract workforce.yaml GET /staffing-coverage. Pack labels with no schema field yet (shown as plain labels): Coverage, Overtime hours, Projected labour cost, Projected saving, Cross-venue transfers, AI-optimised roster (scenario side), Assignment explanation, Optimization objective.",
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
 "amendAttendance": {
  "method": "POST",
  "path": "/attendance/{recordId}/amend",
  "contract": "workforce",
  "summary": "A supervisor corrects a record",
  "permission": "WORKFORCE_MANAGE",
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
  "responds": "AttendanceRecord"
 },
 "claimOpenShift": {
  "method": "POST",
  "path": "/shift-marketplace",
  "contract": "workforce",
  "summary": "Pick up a released shift",
  "permission": "WORKFORCE_VIEW",
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
  "responds": "OpenShift"
 },
 "createRotaAssignment": {
  "method": "POST",
  "path": "/rota-assignments",
  "contract": "workforce",
  "summary": "Put someone on the rota",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "RotaAssignment",
  "responds": "RotaAssignment"
 },
 "getLabourCost": {
  "method": "GET",
  "path": "/labour-cost",
  "contract": "workforce",
  "summary": "Rostered and actual labour cost against budget",
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
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "LabourCostRow"
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
   }
  ],
  "requestBody": null,
  "responds": "StaffingCoverage"
 },
 "listAttendance": {
  "method": "GET",
  "path": "/attendance",
  "contract": "workforce",
  "summary": "Who was here",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "date",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "exceptionsOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AttendanceRecord"
 },
 "listOpenShifts": {
  "method": "GET",
  "path": "/shift-marketplace",
  "contract": "workforce",
  "summary": "Shifts offered back, and who may take them",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OpenShift"
 },
 "listRotaAssignments": {
  "method": "GET",
  "path": "/rota-assignments",
  "contract": "workforce",
  "summary": "The rota",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "departmentId",
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
 "recordAttendance": {
  "method": "POST",
  "path": "/attendance/clock",
  "contract": "workforce",
  "summary": "Clock in, clock out, or take a break",
  "permission": "ATTENDANCE_RECORD",
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
  "responds": "AttendanceRecord"
 },
 "setStaffingRules": {
  "method": "PUT",
  "path": "/staffing-rules",
  "contract": "workforce",
  "summary": "Minimum cover, working-hour limits and overtime",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "StaffingRules",
  "responds": "StaffingRules"
 },
 "validateWorkforceCompliance": {
  "method": "GET",
  "path": "/workforce-compliance",
  "contract": "workforce",
  "summary": "Where the rota breaks a rule",
  "permission": "WORKFORCE_VIEW",
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
    "name": "to",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkforceComplianceFinding"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AttendanceAmendment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.attendance_amendment",
  "description": "One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n",
  "required": [
   "id",
   "attendanceRecordId",
   "amendedByPrincipalId",
   "amendedAt",
   "occurredAtBefore",
   "occurredAtAfter",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "attendanceRecordId": {
    "type": "string",
    "format": "uuid"
   },
   "amendedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "amendedAt": {
    "type": "string",
    "format": "date-time"
   },
   "occurredAtBefore": {
    "type": "string",
    "format": "date-time",
    "description": "The record's time before this correction."
   },
   "occurredAtAfter": {
    "type": "string",
    "format": "date-time",
    "description": "The time this correction set (`correctedAt` on the request)."
   },
   "reason": {
    "type": "string",
    "maxLength": 300
   }
  }
 },
 "AttendanceRecord": {
  "type": "object",
  "x-ticvai-persistence": "workforce.attendance",
  "required": [
   "id",
   "principalId",
   "kind",
   "occurredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "assignmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "clockIn",
     "clockOut",
     "breakStart",
     "breakEnd"
    ]
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time — when it happened."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "latitude": {
    "type": "number",
    "nullable": true
   },
   "longitude": {
    "type": "number",
    "nullable": true
   },
   "isAmended": {
    "type": "boolean",
    "readOnly": true
   },
   "amendedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Who made the latest amendment. The full history is `amendments` (audit R129 (7))."
   },
   "amendmentReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The latest amendment's reason. The full history is `amendments` (audit R129 (7))."
   },
   "originalOccurredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"
   },
   "amendments": {
    "type": "array",
    "readOnly": true,
    "description": "**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n",
    "items": {
     "$ref": "#/components/schemas/AttendanceAmendment"
    }
   },
   "exception": {
    "type": "string",
    "nullable": true,
    "enum": [
     "late",
     "earlyLeave",
     "missingClockOut",
     "noShow",
     "outOfGeofence",
     "unscheduled"
    ],
    "description": "Computed against the rota. Null where the record matches what was expected."
   }
  }
 },
 "LabourCostRow": {
  "type": "object",
  "description": "Resource board 4.9. **Rostered and actual diverge every day.**",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "rosteredHours": {
    "type": "number"
   },
   "actualHours": {
    "type": "number"
   },
   "overtimeHours": {
    "type": "number"
   },
   "rosteredCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "actualCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "budget": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variancePercent": {
    "type": "number"
   },
   "headcount": {
    "type": "integer"
   }
  }
 },
 "OpenShift": {
  "type": "object",
  "x-ticvai-persistence": "workforce.open_shift",
  "description": "Resource board 4.6. **How a gap gets filled at nine on a Friday without a manager ringing round.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "rotaAssignmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "shiftTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "positionCode": {
    "type": "string"
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "releasedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "requiredQualifications": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "eligiblePrincipalCount": {
    "type": "integer",
    "readOnly": true
   },
   "incentiveRateMultiplier": {
    "type": "number",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "claimed",
     "pendingApproval",
     "filled",
     "expired",
     "withdrawn"
    ]
   },
   "claimedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "claimedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
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
 "RotaAssignment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.rota_assignment",
  "required": [
   "principalId",
   "venueId",
   "startsAt",
   "endsAt",
   "position"
  ],
  "properties": {
   "overtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"
   },
   "restPeriodBefore": {
    "type": "integer",
    "nullable": true,
    "description": "Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"
   },
   "breachesWorkingHourLimit": {
    "type": "boolean",
    "default": false,
    "readOnly": true,
    "description": "**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"
   },
   "labourCost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "position": {
    "type": "string",
    "description": "What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"
   },
   "requiredRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "$ref": "#/components/schemas/RotaStatus"
   },
   "breakMinutes": {
    "type": "integer",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "RotaStatus": {
  "type": "string",
  "enum": [
   "planned",
   "published",
   "confirmed",
   "swapPending",
   "cancelled",
   "completed",
   "noShow"
  ]
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
   }
  }
 },
 "StaffingRules": {
  "type": "object",
  "x-ticvai-persistence": "workforce.staffing_rules + workforce.position_requirement",
  "description": "Resource board 4.3. **A safety rule before it is a cost rule.**",
  "properties": {
   "minimumCover": {
    "type": "array",
    "description": "**Minimum staffing per position, venue and time window, with the qualifications it requires**: the rows of `workforce.position_requirement` (data model for the agreed operations, 29 September). `getStaffingCoverage` measures the rota against them; before this they were an array with no table, so no minimum was stored.",
    "items": {
     "type": "object",
     "required": [
      "id",
      "positionCode",
      "minimumHeadcount"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "positionCode": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "venueId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "attractionId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "minimumHeadcount": {
       "type": "integer",
       "minimum": 0
      },
      "daysOfWeek": {
       "type": "array",
       "nullable": true,
       "description": "Days the minimum applies; absent means every day the venue is open",
       "items": {
        "type": "string",
        "enum": [
         "monday",
         "tuesday",
         "wednesday",
         "thursday",
         "friday",
         "saturday",
         "sunday"
        ]
       }
      },
      "startsAt": {
       "type": "string",
       "nullable": true,
       "description": "Start of the time window, local time (HH:MM) as `ShiftTemplate.startsAt`; absent means opening"
      },
      "endsAt": {
       "type": "string",
       "nullable": true,
       "description": "End of the time window, local time (HH:MM); absent means closing"
      },
      "requiredQualifications": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "appliesWhenOpen": {
       "type": "boolean",
       "default": true
      },
      "blocksOperation": {
       "type": "boolean",
       "default": true,
       "description": "**A ride requiring two operators cannot run with one.** Where this is true the attraction closes rather than running short.\n"
      }
     }
    }
   },
   "maximumHoursPerDay": {
    "type": "integer",
    "nullable": true
   },
   "maximumHoursPerWeek": {
    "type": "integer",
    "nullable": true
   },
   "minimumRestHours": {
    "type": "integer",
    "nullable": true
   },
   "maximumConsecutiveDays": {
    "type": "integer",
    "nullable": true
   },
   "overtime": {
    "type": "object",
    "properties": {
     "allowed": {
      "type": "boolean",
      "default": true
     },
     "afterHoursPerWeek": {
      "type": "integer",
      "nullable": true
     },
     "rateMultiplier": {
      "type": "number",
      "nullable": true
     },
     "requiresApproval": {
      "type": "boolean",
      "default": true
     }
    }
   },
   "minimumAgeForNightShift": {
    "type": "integer",
    "nullable": true
   },
   "defaultIncentiveRateMultiplier": {
    "type": "number",
    "nullable": true,
    "minimum": 1,
    "description": "**What an open shift pays above base when it is released.** Added 22 September: `workforce.open_shift.incentive_rate_multiplier` was set per shift with nothing behind it, so two identical shifts could price differently and record no reason. The shift still carries its own value — **as the snapshot**, the rule-and-record split `payments.fee_rule` and `orders.order_fee` use — and this is where it comes from.\n**Top-level rather than beside `overtime`** so the value is its own column. Nested in an object it would be a key inside a JSON blob, which nothing can index, constrain or pair to the shift that uses it.\n"
   },
   "maximumIncentiveRateMultiplier": {
    "type": "number",
    "nullable": true,
    "minimum": 1,
    "description": "**The ceiling on an incentive.** A shift nobody claims is the moment somebody raises the multiplier in a hurry — the same reason `maximumDailyCharge` bounds a late fee."
   },
   "incentiveApprovalAbove": {
    "type": "number",
    "nullable": true,
    "minimum": 1,
    "description": "**Above this multiplier a second person approves the release.** Routed as an approval, not a boolean — `overtime.requiresApproval` beside it is one of 26 approval flags across the contracts that no approval kind, matrix row or SLA reaches."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WorkforceComplianceFinding": {
  "type": "object",
  "description": "Resource board 4.8. **Checked before the rota is published, not in an inspection.**",
  "properties": {
   "code": {
    "type": "string",
    "enum": [
     "expiredQualification",
     "missingQualification",
     "exceededDailyHours",
     "exceededWeeklyHours",
     "insufficientRest",
     "missedBreak",
     "consecutiveDaysExceeded",
     "underAgeNightShift",
     "belowMinimumCover"
    ]
   },
   "severity": {
    "type": "string",
    "enum": [
     "breach",
     "warning"
    ]
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "principalName": {
    "type": "string",
    "nullable": true
   },
   "date": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "detail": {
    "type": "string"
   },
   "rotaAssignmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 }
}
```
