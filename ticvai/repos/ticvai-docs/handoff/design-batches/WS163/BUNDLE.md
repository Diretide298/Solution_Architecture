# WS163 — Resource Management Configuration board 9

**10 screens · 16 operations · 34 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `APPROVAL_DECIDE, APPROVAL_VIEW, ATTENDANCE_RECORD, INCIDENT_REPORT, PRODUCT_VIEW, RESOURCE_BOOK, RESOURCE_VIEW, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-933` | My Resource Operations Home | listDetail | 1 | 0 | — |
| `BO-934` | My Schedule & Assignment Calendar | listDetail | 1 | 0 | — |
| `BO-935` | Assignment Detail & Operational Brief | listDetail | 6 | 0 | — |
| `BO-936` | Mobile Staff Check-In & Check-Out | listDetail | 1 | 0 | — |
| `BO-937` | Resource Collection, Handover & Return | configEditor | 2 | 0 | — |
| `BO-938` | Employee Requests & Resource Support | listDetail | 2 | 0 | — |
| `BO-939` | Shift Change, Swap, Pickup & Release | listDetail | 2 | 0 | — |
| `BO-940` | Manager Mobile Approval Center | listDetail | 2 | 0 | — |
| `BO-941` | Operational Notifications & Live Alerts | listDetail | 1 | 0 | — |
| `BO-942` | Mobile Operations Control & Offline Sync | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-933, BO-936, BO-939, BO-940, BO-942 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-933",
  "name": "My Resource Operations Home",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "01",
   "page": 136
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/my-resource-operations-home-bo-933",
   "component": "apps/venue-management-web/src/routes/rentals/MyResourceOperationsHome.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-934",
    "BO-935",
    "BO-936",
    "BO-937",
    "BO-938",
    "BO-939",
    "BO-940",
    "BO-941",
    "BO-942"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-934",
     "trigger": "My Schedule & Assignment Calendar",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-935",
     "trigger": "Assignment Detail & Operational Brief",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-936",
     "trigger": "Mobile Staff Check-In & Check-Out",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-937",
     "trigger": "Resource Collection, Handover & Return",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-938",
     "trigger": "Employee Requests & Resource Support",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-939",
     "trigger": "Shift Change, Swap, Pickup & Release",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-940",
     "trigger": "Manager Mobile Approval Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-941",
     "trigger": "Operational Notifications & Live Alerts",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-942",
     "trigger": "Mobile Operations Control & Offline Sync",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§The screen shall display) and no metric row",
  "purpose": "Provide each employee with a personalized operational landing screen showing what requires their attention now and next.",
  "purposeNote": "Employees can immediately understand their current operational status and next required action without navigating through multiple screens.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 136 §The screen shall display"
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
       "label": "Every resource operations home",
       "columns": [
        "Current shift",
        "Current assignment",
        "Next assignment",
        "Today's schedule",
        "Assigned venue",
        "Check-in status",
        "Break status",
        "Pending tasks",
        "Resource handovers",
        "Employee requests",
        "Notifications",
        "Manager messages",
        "Smart Operational Card",
        "“What am I supposed to do now?”"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 136 §The screen shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource operations home",
       "bindsTo": null,
       "columns": [
        "Current shift",
        "Current assignment",
        "Next assignment",
        "Today's schedule",
        "Assigned venue",
        "Check-in status",
        "Break status",
        "Pending tasks",
        "Resource handovers",
        "Employee requests",
        "Notifications",
        "Manager messages",
        "Smart Operational Card",
        "“What am I supposed to do now?”"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Private Ski Lesson”, “Group Ski Lesson”, “Zone B”, “The employee may ask”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 136 §The screen shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource operations home list.",
   "error": "Could not load. Names which read failed and leaves the resource operations home untouched.",
   "emptyFirstRun": "No resource operations home yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource operations home are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResourceBookings",
    "contract": "resources",
    "purpose": "Today's assignments",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Current shift",
    "Current assignment",
    "Next assignment",
    "Today's schedule",
    "Assigned venue",
    "Check-in status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-933",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-933"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 136. 0 of 14 labels bound to a contract property; 14 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-934",
  "name": "My Schedule & Assignment Calendar",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "02",
   "page": 137
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/my-schedule-assignment-calendar-bo-934",
   "component": "apps/venue-management-web/src/routes/rentals/MyScheduleAssignmentCalendar.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide employees with a mobile view of their working schedule and operational assignments.",
  "purposeNote": "Employees can view their complete operational schedule and receive synchronized updates whenever assignments change.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 137 §Display"
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
       "kind": "calendarView",
       "label": "Calendar",
       "operation": "getResourceCalendar",
       "notes": "The signed-in person's schedule and assignments. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.",
       "provenance": "decided 29 September 2026, 17 September minutes M17-03 (applied 30 September)"
      },
      {
       "kind": "dataTable",
       "label": "Every schedule calendar",
       "columns": [
        "Upcoming",
        "Confirmed",
        "In Progress",
        "Completed",
        "Changed",
        "Cancelled",
        "Requires Attention",
        "Live Updates"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 137 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected schedule calendar",
       "bindsTo": null,
       "columns": [
        "Upcoming",
        "Confirmed",
        "In Progress",
        "Completed",
        "Changed",
        "Cancelled",
        "Requires Attention",
        "Live Updates"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Zone A”, “Zone C”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 137 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Schedule Timeline",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 137 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The schedule calendar list.",
   "error": "Could not load. Names which read failed and leaves the schedule calendar untouched.",
   "emptyFirstRun": "No schedule calendar yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the schedule calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceCalendar",
    "contract": "resources",
    "purpose": "My schedule",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Upcoming",
    "Confirmed",
    "In Progress",
    "Completed",
    "Changed",
    "Cancelled"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-934",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-934"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 137. 0 of 8 labels bound to a contract property; 9 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Schedule Timeline dropped (view heading; the timeline renders getResourceCalendar).",
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
  "id": "BO-935",
  "name": "Assignment Detail & Operational Brief",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "03",
   "page": 138
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/assignment-detail-operational-brief-bo-935",
   "component": "apps/venue-management-web/src/routes/rentals/AssignmentDetailOperationalBrief.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Give the employee all information required to execute a specific assignment.",
  "purposeNote": "Employees can access all permitted operational information needed to execute an assignment from one mobile screen.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Display"
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
       "label": "Every detail operational brief",
       "columns": [
        "Assignment",
        "Date",
        "Start/end",
        "Venue",
        "Zone/location",
        "Role",
        "Status",
        "Priority",
        "Operational Information"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected detail operational brief",
       "bindsTo": null,
       "columns": [
        "Assignment",
        "Date",
        "Start/end",
        "Venue",
        "Zone/location",
        "Role",
        "Status",
        "Priority",
        "Operational Information"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Depending on assignment type”, “Where appropriate, provide”, “Equipment Required”, “Customer Information”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Start assignment",
       "operation": "setResourceBookingProgress",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Check in",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Contact supervisor",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Report issue",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Request replacement",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View checklist",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete assignment",
       "operation": "setResourceBookingProgress",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 138 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The detail operational brief list.",
   "error": "Could not load. Names which read failed and leaves the detail operational brief untouched.",
   "emptyFirstRun": "No detail operational brief yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the detail operational brief are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResource",
    "contract": "resources",
    "purpose": "The resource for this assignment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listResourceBookings",
    "contract": "resources",
    "purpose": "The assignment itself",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "recordAttendance",
    "contract": "workforce",
    "purpose": "Check in to the assignment",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Check in; Report issue"
   },
   {
    "operationId": "reportIncident",
    "contract": "maintenance",
    "purpose": "Report an issue on the assignment",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Check in; Report issue"
   },
   {
    "operationId": "setResourceBookingProgress",
    "contract": "resources",
    "purpose": "Start or complete",
    "trigger": "onAction"
   },
   {
    "operationId": "raiseResourceRequest",
    "contract": "resources",
    "purpose": "Raise request",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "Assignment",
    "Date",
    "Start/end",
    "Venue",
    "Zone/location",
    "Role"
   ],
   "params": [
    {
     "name": "resourceId",
     "from": "navigation"
    },
    {
     "name": "bookingId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-935",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-935"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 138. 0 of 9 labels bound to a contract property; 16 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Check in: `recordAttendance`; Report issue: `reportIncident`; Contact supervisor dropped (phone/chat link to the supervisor, no API action); View checklist dropped (navigation); still owed by a contract change: `setResourceBookingProgress`, `raiseResourceRequest`.",
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
  "id": "BO-936",
  "name": "Mobile Staff Check-In & Check-Out",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "04",
   "page": 139
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/mobile-staff-check-in-check-out-bo-936",
   "component": "apps/venue-management-web/src/routes/rentals/MobileStaffCheckInCheckOut.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow employees to record attendance and assignment presence from the Employee App.",
  "purposeNote": "Employees can record shift and assignment attendance from the mobile application with configurable validation and full audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 139 §Display"
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
       "label": "Every mobile staff check-in",
       "columns": [
        "Shift",
        "08:00–16:00",
        "Venue",
        "Ski School",
        "Current Time",
        "07:56",
        "Status",
        "Ready to Check In",
        "[CHECK IN]"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 139 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected mobile staff check-in",
       "bindsTo": null,
       "columns": [
        "Shift",
        "08:00–16:00",
        "Venue",
        "Ski School",
        "Current Time",
        "07:56",
        "Status",
        "Ready to Check In",
        "[CHECK IN]"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Check-In”, “Assignment Check-In”, “On checkout, display”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 139 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The mobile staff check-in list.",
   "error": "Could not load. Names which read failed and leaves the mobile staff check-in untouched.",
   "emptyFirstRun": "No mobile staff check-in yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mobile staff check-in are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordAttendance",
    "contract": "workforce",
    "purpose": "Check in or out",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Shift",
    "08:00–16:00",
    "Venue",
    "Ski School",
    "Current Time",
    "07:56"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-936",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-936"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 139. 0 of 9 labels bound to a contract property; 15 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-937",
  "name": "Resource Collection, Handover & Return",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "05",
   "page": 141
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-collection-handover-return-bo-937",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceCollectionHandoverReturn.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Digitally manage physical resources transferred between employees, departments, or operational locations.",
  "purposeNote": "Physical-resource custody can be digitally tracked through scan-driven collection, handover, and return workflows.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Good",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 141 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Minor damage",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 141 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Damaged",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 141 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Missing component",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 141 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Return",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 141 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource collection handover configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource collection handover untouched.",
   "emptyFirstRun": "No resource collection handover configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "checkOutResource",
    "contract": "resources",
    "purpose": "Hand it over",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "checkInResource",
    "contract": "resources",
    "purpose": "Take it back",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-937",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-937"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 141. 0 of 0 labels bound to a contract property; 5 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-938",
  "name": "Employee Requests & Resource Support",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "06",
   "page": 142
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/employee-requests-resource-support-bo-938",
   "component": "apps/venue-management-web/src/routes/rentals/EmployeeRequestsResourceSupport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow frontline employees to submit operational resource-related requests directly from the Employee App.",
  "purposeNote": "Employees can report operational resource issues and requests digitally, and those requests can trigger the appropriate backend workflow.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 142"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 142"
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
       "label": "Replacement resource",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 142 §Support configurable requests such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Additional equipment",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 142 §Support configurable requests such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Resource issue",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 142 §Support configurable requests such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Maintenance request",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 142 §Support configurable requests such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Assignment change",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 142 §Support configurable requests such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue change request",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 142 §Support configurable requests such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule clarification",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 142 §Support configurable requests such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Custom operational request",
       "operation": "raiseResourceRequest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 142 §Support configurable requests such as"
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
   "loading": "The employee requests resource list.",
   "error": "Could not load. Names which read failed and leaves the employee requests resource untouched.",
   "emptyFirstRun": "No employee requests resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the employee requests resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "raiseMyCase",
    "contract": "marketing-crm",
    "purpose": "Raise a request",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "raiseResourceRequest",
    "contract": "resources",
    "purpose": "Raise request",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-938",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-938"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 142. 0 of 0 labels bound to a contract property; 8 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `raiseResourceRequest`.",
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
  "id": "BO-939",
  "name": "Shift Change, Swap, Pickup & Release",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "07",
   "page": 143
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/shift-change-swap-pickup-release-bo-939",
   "component": "apps/venue-management-web/src/routes/rentals/ShiftChangeSwapPickupRelease.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Expose the Board 4 Shift Marketplace capabilities through the Employee App. This screen does not recreate shift rules; it consumes the workforce rules already configured in Board 4.",
  "purposeNote": "Employees can manage permitted shift changes through mobile self-service while all qualification, compliance, and approval rules remain enforced centrally.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 143"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 143"
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
       "impliedBy": "requestShiftSwap",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listShiftSwapRequests",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "requestShiftSwap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The shift change swap list.",
   "error": "Could not load. Names which read failed and leaves the shift change swap untouched.",
   "emptyFirstRun": "No shift change swap yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the shift change swap are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "requestShiftSwap",
    "contract": "workforce",
    "purpose": "Swap, pick up or release",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listShiftSwapRequests",
    "contract": "workforce",
    "purpose": "Requests outstanding",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-939",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-939"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 143. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assignmentId",
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
  "id": "BO-940",
  "name": "Manager Mobile Approval Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "08",
   "page": 144
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/manager-mobile-approval-center-bo-940",
   "component": "apps/venue-management-web/src/routes/rentals/ManagerMobileApprovalCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized supervisors and managers to approve operational requests without requiring access to the desktop backend.",
  "purposeNote": "Authorized managers can review and action operational approvals from mobile with sufficient validation context to make an informed decision.",
  "gaps": [
   {
    "operation": null,
    "why": "**Manager Mobile Approval Center declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 144"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 144"
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
       "impliedBy": "listApprovalRequests",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "decideApprovalRequest",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The mobile approval list.",
   "error": "Could not load. Names which read failed and leaves the mobile approval untouched.",
   "emptyFirstRun": "No mobile approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mobile approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Approvals on mobile",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Decide",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-940",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-940"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 144. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "requestId",
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
  "id": "BO-941",
  "name": "Operational Notifications & Live Alerts",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "09",
   "page": 145
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/operational-notifications-live-alerts-bo-941",
   "component": "apps/venue-management-web/src/routes/rentals/OperationalNotificationsLiveAlerts.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide employees and managers with timely, prioritized operational notifications.",
  "purposeNote": "Operational changes and critical resource events are communicated to the correct users with configurable priority, acknowledgement, and escalation behavior.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 145"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 145"
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
       "label": "Assignment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 145 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 145 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 145 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 145 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Attendance",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 145 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Approval",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 145 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Emergency/critical operations",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 145 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "AI recommendation",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 145 §Support"
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
   "loading": "The operational notifications live list.",
   "error": "Could not load. Names which read failed and leaves the operational notifications live untouched.",
   "emptyFirstRun": "No operational notifications live yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational notifications live are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAnnouncements",
    "contract": "workforce",
    "purpose": "Live alerts and notices",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-941",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-941"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 145. 0 of 0 labels bound to a contract property; 8 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Assignment, Schedule, Resource, Event, Attendance, Approval, Emergency/critical operations are choices sent by `listAnnouncements` (field gap: add kind filter and extend AnnouncementKind with assignment|schedule|resource|event|attendance|approval (emergency exists)); AI recommendation dropped (AI design pending review).",
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
  "id": "BO-942",
  "name": "Mobile Operations Control & Offline Sync",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "9",
   "number": "10",
   "page": 146
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/mobile-operations-control-offline-sync-bo-942",
   "component": "apps/venue-management-web/src/routes/rentals/MobileOperationsControlOfflineSync.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-933"
   ],
   "exitTo": [
    "BO-933"
   ],
   "transitions": [
    {
     "to": "BO-933",
     "trigger": "Back to My Resource Operations Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure and monitor how Resource Management operates on mobile devices, particularly where connectivity is unreliable. Provide TICVAI with the executive and administrative control layer for the entire Resource Management ecosystem. Board 10 shall consolidate information from all previous boards to answer four fundamental questions: 1. Are our resources being used efficiently? 2. Are they generating the expected operational and financial value? 3. Are resource decisions compliant, controlled, and auditable? 4. What should management change to improve future performance?",
  "purposeNote": "The Employee App can support configured resource operations during temporary connectivity loss and safely synchronize transactions when connectivity returns without compromising the authoritative resource state. Board 9 — Role-Based Mobile Experience Board 9 should not show every employee the same application. The mobile interface shall adapt based on role.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 146"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 146"
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
       "label": "Board 9 — Smart Mobile Home Principle",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 146 §Operations Manager"
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
   "loading": "The mobile operations offline list.",
   "error": "Could not load. Names which read failed and leaves the mobile operations offline untouched.",
   "emptyFirstRun": "No mobile operations offline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mobile operations offline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameplaySyncStatus",
    "contract": "games",
    "purpose": "Offline sync state",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-942",
   "workshopBoard": "wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-942"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 146. 0 of 0 labels bound to a contract property; 1 of 156 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Board 9 — Smart Mobile Home Principle dropped (board heading).",
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
 "checkInResource": {
  "method": "POST",
  "path": "/resource-bookings/{bookingId}/check-in",
  "contract": "resources",
  "summary": "Take it back, and settle the deposit",
  "permission": "RESOURCE_BOOK",
  "offlineCapable": true,
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
  "responds": "ResourceBooking"
 },
 "checkOutResource": {
  "method": "POST",
  "path": "/resource-bookings/{bookingId}/check-out",
  "contract": "resources",
  "summary": "Hand it over, with a deposit against it",
  "permission": "RESOURCE_BOOK",
  "offlineCapable": true,
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
  "responds": "ResourceBooking"
 },
 "decideApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/decide",
  "contract": "approvals",
  "summary": "Approve, reject, return or ask for information",
  "permission": "APPROVAL_DECIDE",
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
  "responds": "ApprovalRequest"
 },
 "getGameplaySyncStatus": {
  "method": "GET",
  "path": "/gameplay-sync-status",
  "contract": "games",
  "summary": "What readers took offline and have not sent",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReaderSyncStatus"
 },
 "getResource": {
  "method": "GET",
  "path": "/resources/{resourceId}",
  "contract": "resources",
  "summary": "One resource, with every configured section",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Resource"
 },
 "getResourceCalendar": {
  "method": "GET",
  "path": "/resource-calendar",
  "contract": "resources",
  "summary": "Every resource against time, with conflicts already marked",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
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
    "name": "resourceTypeId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "granularity",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ResourceCalendarRow"
 },
 "listAnnouncements": {
  "method": "GET",
  "path": "/announcements",
  "contract": "workforce",
  "summary": "What staff have been told",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "unacknowledgedOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Announcement"
 },
 "listApprovalRequests": {
  "method": "GET",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Requests awaiting a decision, or already decided",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "raisedByMe",
    "in": "query",
    "required": null
   },
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
    "name": "breachingWithinMinutes",
    "in": "query",
    "required": null
   },
   {
    "name": "sort",
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
 "listResourceBookings": {
  "method": "GET",
  "path": "/resource-bookings",
  "contract": "resources",
  "summary": "Bookings, filtered",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "resourceId",
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
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ResourceBooking"
 },
 "listShiftSwapRequests": {
  "method": "GET",
  "path": "/shift-swaps",
  "contract": "workforce",
  "summary": "Swap requests and their state",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ShiftSwap"
 },
 "raiseMyCase": {
  "method": "POST",
  "path": "/my/cases",
  "contract": "marketing-crm",
  "summary": "Report something — lost property, a complaint, a question",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Case"
 },
 "raiseResourceRequest": {
  "method": "POST",
  "path": "/resource-requests",
  "contract": "resources",
  "summary": "Ask for a replacement, extra equipment or a change to an assignment",
  "permission": "RESOURCE_VIEW",
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
  "requestBody": "ResourceRequestInput",
  "responds": "ResourceRequest"
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
 "reportIncident": {
  "method": "POST",
  "path": "/incidents",
  "contract": "maintenance",
  "summary": "Report an incident",
  "permission": "INCIDENT_REPORT",
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
  "requestBody": "ReportIncidentRequest",
  "responds": "Incident"
 },
 "requestShiftSwap": {
  "method": "POST",
  "path": "/rota-assignments/{assignmentId}/swap",
  "contract": "workforce",
  "summary": "Ask someone to take your shift",
  "permission": "WORKFORCE_VIEW",
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
 "setResourceBookingProgress": {
  "method": "POST",
  "path": "/resource-bookings/{bookingId}/progress",
  "contract": "resources",
  "summary": "Start or complete a staff or instructor assignment",
  "permission": "RESOURCE_BOOK",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ResourceBookingProgressInput",
  "responds": "ResourceBooking"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Announcement": {
  "type": "object",
  "x-ticvai-persistence": "workforce.announcement",
  "required": [
   "title",
   "body",
   "kind",
   "publishedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "title": {
    "type": "string",
    "maxLength": 140
   },
   "body": {
    "type": "string",
    "maxLength": 4000
   },
   "kind": {
    "$ref": "#/components/schemas/AnnouncementKind"
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "departmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresAcknowledgement": {
    "type": "boolean"
   },
   "deliveryChannels": {
    "type": "array",
    "description": "How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n",
    "items": {
     "type": "string",
     "enum": [
      "inApp",
      "push"
     ]
    },
    "default": [
     "inApp",
     "push"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "locale": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "AnnouncementKind": {
  "type": "string",
  "description": "`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n",
  "enum": [
   "operational",
   "safety",
   "emergency",
   "hr",
   "celebration"
  ]
 },
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration",
   "productChange",
   "pricingChange"
  ]
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.",
    "properties": {
     "riskScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "riskBand": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "priorityScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "escalationSuggestion": {
      "type": "object",
      "description": "A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.",
      "properties": {
       "action": {
        "type": "string",
        "enum": [
         "escalate",
         "addBackupApprover",
         "none"
        ]
       },
       "reason": {
        "type": "string",
        "nullable": true
       }
      }
     },
     "signals": {
      "type": "array",
      "maxItems": 10,
      "description": "The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.",
      "items": {
       "type": "object",
       "properties": {
        "code": {
         "type": "string"
        },
        "contribution": {
         "type": "number"
        },
        "detail": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "scoreId": {
      "type": "string",
      "format": "uuid",
      "description": "The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."
     },
     "decisionRecordId": {
      "type": "string",
      "description": "The ai decision record, for the audit of what the AI said and why."
     },
     "assessedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "returned",
   "informationRequested",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
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
 "Case": {
  "x-ticvai-persistence": "marketing.case",
  "x-ticvai-retired-columns": [
   "guest_name",
   "subject",
   "is_sla_breached"
  ],
  "type": "object",
  "required": [
   "id",
   "caseNumber",
   "subject",
   "status",
   "priority",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."
   },
   "caseNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"
   },
   "subject": {
    "type": "string",
    "x-ticvai-column": "title",
    "description": "**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CaseKind"
     }
    ],
    "nullable": true,
    "description": "What the guest said it was about, where the guest raised it."
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "description": "How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time the case was raised — the start of the SLA clock."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the case arrived. Equal to `recordedAt` for a case raised online."
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"
   },
   "status": {
    "$ref": "#/components/schemas/CaseStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "relatedOrderId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isSlaBreached": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"
   },
   "slaPausedSeconds": {
    "type": "integer",
    "description": "Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"
   },
   "escalationCount": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CaseKind": {
  "type": "string",
  "description": "**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n",
  "enum": [
   "lostProperty",
   "complaint",
   "question",
   "accessibility",
   "refundRequest",
   "other"
  ]
 },
 "CasePriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent"
  ]
 },
 "CaseStatus": {
  "type": "string",
  "enum": [
   "open",
   "inProgress",
   "awaitingGuest",
   "escalated",
   "resolved",
   "closed"
  ]
 },
 "Incident": {
  "x-ticvai-persistence": "maintenance.incident",
  "type": "object",
  "required": [
   "id",
   "incidentNumber",
   "kind",
   "severity",
   "status",
   "venueId",
   "occurredAt",
   "reportedByPrincipalId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
   },
   "kind": {
    "$ref": "#/components/schemas/IncidentKind"
   },
   "severity": {
    "$ref": "#/components/schemas/IncidentSeverity"
   },
   "status": {
    "$ref": "#/components/schemas/IncidentStatus"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationDescription": {
    "type": "string",
    "nullable": true
   },
   "isReportable": {
    "type": "boolean",
    "description": "Requires notification to an external authority within a statutory window."
   },
   "notificationDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reportedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "correctiveWorkOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "IncidentKind": {
  "type": "string",
  "enum": [
   "guestInjury",
   "staffInjury",
   "nearMiss",
   "propertyDamage",
   "equipmentFailure",
   "securityIncident",
   "fireOrEvacuation",
   "foodSafety",
   "environmental",
   "other"
  ]
 },
 "IncidentSeverity": {
  "type": "string",
  "enum": [
   "nearMiss",
   "minor",
   "moderate",
   "major",
   "critical"
  ]
 },
 "IncidentStatus": {
  "type": "string",
  "enum": [
   "reported",
   "underInvestigation",
   "actionRequired",
   "closed"
  ]
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
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
 "ReaderSyncStatus": {
  "type": "object",
  "description": "Board 8.8. **Revenue the platform has not seen.**",
  "properties": {
   "readerId": {
    "type": "string",
    "format": "uuid"
   },
   "readerName": {
    "type": "string"
   },
   "pendingTransactions": {
    "type": "integer"
   },
   "pendingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "oldestPendingAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastSyncAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "edgePackageVersion": {
    "type": "integer",
    "nullable": true
   },
   "edgePackageStale": {
    "type": "boolean"
   },
   "status": {
    "type": "string",
    "enum": [
     "online",
     "offline",
     "degraded",
     "unreachable"
    ]
   }
  }
 },
 "ReportIncidentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "kind",
   "severity",
   "venueId",
   "description",
   "occurredAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/IncidentKind"
   },
   "severity": {
    "$ref": "#/components/schemas/IncidentSeverity"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "description": {
    "type": "string",
    "minLength": 3,
    "maxLength": 10000
   },
   "involvedSubjectIds": {
    "type": "array",
    "description": "Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "involvedStaffPrincipalIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "witnessCount": {
    "type": "integer"
   },
   "firstAidGiven": {
    "type": "boolean",
    "default": false
   },
   "emergencyServicesCalled": {
    "type": "boolean",
    "default": false
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Resource": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource",
  "description": "**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId"
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
   "kind": {
    "$ref": "#/components/schemas/ResourceKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "parentResourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true,
    "description": "Configurable per kind — capacity, size, shade, power, poolside."
   },
   "setupMinutes": {
    "type": "integer",
    "default": 0,
    "description": "**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"
   },
   "teardownMinutes": {
    "type": "integer",
    "default": 0,
    "description": "After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"
   },
   "cleaningPolicy": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ResourceCleaningPolicy"
     }
    ],
    "nullable": true,
    "description": "How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."
   },
   "requiresQualification": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Qualification codes a person must hold to be assigned to this."
   },
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "booked",
     "checkedOut",
     "maintenance",
     "retired"
    ]
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ResourceBooking": {
  "type": "object",
  "x-ticvai-persistence": "resources.booking",
  "required": [
   "id",
   "resourceId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "$ref": "#/components/schemas/ResourceBookingStatus"
   },
   "holdId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"
   },
   "recurrenceGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "conditionOut": {
    "type": "string",
    "nullable": true
   },
   "conditionIn": {
    "type": "string",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"
   }
  }
 },
 "ResourceBookingProgressInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the step is recorded on resources.booking",
  "description": "What `setResourceBookingProgress` takes (decided 29 September, readiness close-out).",
  "required": [
   "state",
   "recordedAt"
  ],
  "properties": {
   "state": {
    "type": "string",
    "enum": [
     "started",
     "completed"
    ],
    "description": "`started` is recorded as `checkedOut`, `completed` as `returned`."
   },
   "note": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the employee pressed the button on the device, not when the write reached the server."
   }
  }
 },
 "ResourceBookingStatus": {
  "type": "string",
  "enum": [
   "reserved",
   "checkedOut",
   "returned",
   "overdue",
   "cancelled",
   "noShow"
  ]
 },
 "ResourceCalendarRow": {
  "type": "object",
  "description": "Board 2.01. **One resource across the window, with its states already computed** — including conflict, which a client cannot derive from a booking list.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "resourceName": {
    "type": "string"
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "utilisationPercent": {
    "type": "number"
   },
   "segments": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "state": {
       "type": "string",
       "enum": [
        "available",
        "reserved",
        "assigned",
        "partiallyUtilised",
        "fullyUtilised",
        "unavailable",
        "onBreak",
        "onLeave",
        "underMaintenance",
        "operationallyBlocked",
        "pendingApproval",
        "conflict"
       ]
      },
      "bookingId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "conflictsWith": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   }
  }
 },
 "ResourceCleaningPolicy": {
  "x-ticvai-persistence": "none — columns on resources.resource",
  "type": "object",
  "description": "**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n",
  "required": [
   "mode",
   "bufferMinutes"
  ],
  "properties": {
   "mode": {
    "type": "string",
    "enum": [
     "afterEveryBooking",
     "timesPerDay"
    ]
   },
   "bufferMinutes": {
    "type": "integer",
    "minimum": 5,
    "maximum": 240,
    "description": "Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."
   },
   "cleaningsPerDay": {
    "type": "integer",
    "minimum": 1,
    "maximum": 24,
    "nullable": true,
    "description": "Required for `timesPerDay`; ignored for `afterEveryBooking`."
   },
   "windowStart": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Venue-local time the cleaning window opens. Null means the resource's opening time."
   },
   "windowEnd": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Venue-local time the cleaning window closes. Null means the resource's closing time."
   }
  }
 },
 "ResourceKind": {
  "type": "string",
  "description": "BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n",
  "enum": [
   "cabana",
   "lounger",
   "locker",
   "wheelchair",
   "stroller",
   "equipment",
   "room",
   "auditorium",
   "vehicle",
   "instructor",
   "staff",
   "table",
   "pitch",
   "studio",
   "other"
  ],
  "x-ticvai-refuses": {
   "mealPlan": "**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."
  }
 },
 "ResourceRequest": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_request",
  "description": "**An employee's request about the resources on an assignment** (decided 29 September, readiness close-out; BO-935, BO-938). New table. Raised `open`, then `acknowledged`, `resolved` or `declined` by the resource manager.\n",
  "required": [
   "id",
   "kind",
   "detail",
   "status",
   "raisedByPrincipalId",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/ResourceRequestKind"
   },
   "bookingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "detail": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "acknowledged",
     "resolved",
     "declined"
    ],
    "readOnly": true,
    "description": "`open` on raise."
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "resolutionNote": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "ResourceRequestInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `raiseResourceRequest` takes.",
  "required": [
   "id",
   "kind",
   "detail",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7, so a request raised offline is not duplicated on sync."
   },
   "kind": {
    "$ref": "#/components/schemas/ResourceRequestKind"
   },
   "bookingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "detail": {
    "type": "string",
    "minLength": 3,
    "maxLength": 2000
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ResourceRequestKind": {
  "type": "string",
  "enum": [
   "replacementResource",
   "additionalEquipment",
   "resourceIssue",
   "maintenanceRequest",
   "assignmentChange",
   "venueChange",
   "scheduleClarification",
   "other"
  ],
  "description": "The request kinds on BO-935 / BO-938 (decided 29 September, readiness close-out). `other` is the pack's custom operational request."
 },
 "ShiftSwap": {
  "type": "object",
  "x-ticvai-persistence": "workforce.shift_swap",
  "required": [
   "id",
   "assignmentId",
   "fromPrincipalId",
   "toPrincipalId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assignmentId": {
    "type": "string",
    "format": "uuid"
   },
   "fromPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "toPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "awaitingPeer",
     "awaitingApproval",
     "approved",
     "rejected",
     "withdrawn"
    ],
    "description": "**Both parties before the supervisor.** A swap approved against someone who never agreed is a gap in the rota nobody notices until the shift starts.\n"
   },
   "approvalRequestId": {
    "type": "string",
    "nullable": true,
    "description": "Routed through `approvals` rather than a second mechanism here."
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "StoredValueKind": {
  "type": "string",
  "description": "**Six things in this package hold a balance and behave the same way** — a wallet, a gift card, a game card, a voucher, a loyalty position and a prepaid entitlement. They were built separately across three sessions and each grew its own balance, bonus balance, status, blocked reason and expiry (CF-126).\n**The concern is not tidiness. Only one of the six could hold an authorisation.** `authoriseWalletSpend` / `captureWalletAuthorisation` / `relinquishWalletAuthorisation` gave two-phase spend to the retail wallet alone, so **a guest with 200 game credits starting a play the machine then failed had no held balance** — the credits were either taken or not, with no third state.\nThe entities stay distinct because their lifecycles genuinely differ — a gift card activates at a till, a loyalty position never expires the same way. **What is shared is the spend mechanism**, and this enum is what lets it be shared.\n",
  "enum": [
   "wallet",
   "giftCard",
   "gameCard",
   "voucher",
   "loyalty",
   "prepaidEntitlement"
  ]
 }
}
```
