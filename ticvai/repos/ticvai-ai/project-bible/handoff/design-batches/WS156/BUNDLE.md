# WS156 — Resource Management Configuration board 2

**9 screens · 12 operations · 7 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `RESOURCE_BOOK, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-864` | Resource Calendar Command Center | listDetail | 3 | 0 | — |
| `BO-865` | Calendar Filters, Search & Smart Discovery | listDetail | 2 | 0 | — |
| `BO-866` | Resource Availability Schedule Configuration | configEditor | 2 | 0 | — |
| `BO-867` | Resource Time-Slot Configuration | configEditor | 2 | 0 | — |
| `BO-868` | Advance Reservation Management | configEditor | 3 | 0 | — |
| `BO-869` | Recurring Reservation Configuration | configEditor | 2 | 0 | — |
| `BO-870` | Operational Time & Resource Blocking | configEditor | 3 | 0 | — |
| `BO-871` | Multi-Event Resource Planning | listDetail | 2 | 0 | — |
| `BO-872` | Smart Assignment & Drag-and-Drop Reallocation | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-864, BO-865, BO-871, BO-872 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-864",
  "name": "Resource Calendar Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "01",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-calendar-command-center-bo-864",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceCalendarCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-865",
    "BO-866",
    "BO-867",
    "BO-868",
    "BO-869",
    "BO-870",
    "BO-871",
    "BO-872"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-865",
     "trigger": "Calendar Filters, Search & Smart Discovery",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-866",
     "trigger": "Resource Availability Schedule Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-867",
     "trigger": "Resource Time-Slot Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-868",
     "trigger": "Advance Reservation Management",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "bookingId"
     ]
    },
    {
     "to": "BO-869",
     "trigger": "Recurring Reservation Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "bookingId"
     ]
    },
    {
     "to": "BO-870",
     "trigger": "Operational Time & Resource Blocking",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-871",
     "trigger": "Multi-Event Resource Planning",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-872",
     "trigger": "Smart Assignment & Drag-and-Drop Reallocation",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "bookingId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the main operational calendar from which users can see and manage resource availability, reservations, assignments and operational blocks.",
  "purposeNote": "Authorized users can view the real-time operational status of permitted resources and initiate resource-management actions directly from the calendar.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 20"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 20"
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
       "impliedBy": "bookResource",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "bookResource"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource calendar list.",
   "error": "Could not load. Names which read failed and leaves the resource calendar untouched.",
   "emptyFirstRun": "No resource calendar yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceCalendar",
    "contract": "resources",
    "purpose": "Every resource against time",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "bookResource",
    "contract": "resources",
    "purpose": "Create a reservation from a free slot",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings",
     "getResourceAvailability"
    ]
   },
   {
    "operationId": "createResourceBlock",
    "contract": "resources",
    "purpose": "Block a period",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceBlocks",
     "getResourceCalendar"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-864",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-864"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 54 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-865",
  "name": "Calendar Filters, Search & Smart Discovery",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "02",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/calendar-filters-search-smart-discovery-bo-865",
   "component": "apps/venue-management-web/src/routes/rentals/CalendarFiltersSearchSmartDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-864"
   ],
   "exitTo": [
    "BO-864"
   ],
   "transitions": [
    {
     "to": "BO-864",
     "trigger": "Back to Resource Calendar Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to quickly locate the correct resource instead of manually searching through hundreds or thousands of resources.",
  "purposeNote": "Users can identify suitable resources through structured filters or conversational AI without manually reviewing the entire resource inventory.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 21"
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
       "label": "Search calendar filters search",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 21 §Users shall filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Date range",
        "Time range",
        "Resource type",
        "Resource category",
        "Resource name",
        "Venue",
        "Department",
        "Availability",
        "Capacity",
        "Skill",
        "Certification",
        "Status",
        "Assignment status"
       ],
       "notes": "The pack filters this screen by date range, time range, resource type, resource category, resource name, venue and 7 more — which are present is a decision the pack already made.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 21 §Users shall filter by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The calendar filters search list.",
   "error": "Could not load. Names which read failed and leaves the calendar filters search untouched.",
   "emptyFirstRun": "No calendar filters search yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the calendar filters search are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceCalendar",
    "contract": "resources",
    "purpose": "The filtered grid",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "suggestResources",
    "contract": "resources",
    "purpose": "Find one that matches",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-865",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-865"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 21. 0 of 13 labels bound to a contract property; 13 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-866",
  "name": "Resource Availability Schedule Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "03",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-availability-schedule-configuration-bo-866",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceAvailabilityScheduleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-864"
   ],
   "exitTo": [
    "BO-864"
   ],
   "transitions": [
    {
     "to": "BO-864",
     "trigger": "Back to Resource Calendar Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure; Availability may be configured using) and no display directory — it is settings, not a population",
  "purpose": "Define the baseline schedule controlling when each resource can be used.",
  "purposeNote": "Every resource has an effective availability calendar derived from configured schedules, inherited operating rules and approved exceptions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Available days",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Opening time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Closing time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Effective date",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry date",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Time zone",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Seasonal availability",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venue operating hours",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Resource-specific operating hours",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Public holidays",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venue closures",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maintenance periods",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Staff leave",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Training",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Private blocks",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Operational shutdowns",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Special events",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Inheritance",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Standard weekly schedules",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Availability may be configured using"
      },
      {
       "kind": "selectField",
       "label": "Specific dates",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Availability may be configured using"
      },
      {
       "kind": "selectField",
       "label": "Seasonal schedules",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Availability may be configured using"
      },
      {
       "kind": "selectField",
       "label": "Exception dates",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Availability may be configured using"
      },
      {
       "kind": "selectField",
       "label": "Imported schedules",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Availability may be configured using"
      },
      {
       "kind": "selectField",
       "label": "External workforce schedules",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Availability may be configured using"
      },
      {
       "kind": "selectField",
       "label": "Availability Exceptions",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 22 §Availability may be configured using"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource availability schedule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource availability schedule untouched.",
   "emptyFirstRun": "No resource availability schedule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getResourceSchedule",
    "contract": "resources",
    "purpose": "The pattern as configured",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setResourceSchedule",
    "contract": "resources",
    "purpose": "Operating hours and working pattern",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceSchedule",
     "getResourceAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-866",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-866"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 25 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
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
  "id": "BO-867",
  "name": "Resource Time-Slot Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "04",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-time-slot-configuration-bo-867",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceTimeSlotConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-864"
   ],
   "exitTo": [
    "BO-864"
   ],
   "transitions": [
    {
     "to": "BO-864",
     "trigger": "Back to Resource Calendar Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Control how available resource time is converted into reservable or assignable time slots.",
  "purposeNote": "Administrators can determine precisely how resource availability is converted into customer-facing or operational booking slots.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Slot duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Slot interval",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Start time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "End time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Booking increments",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Buffer before",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Buffer after",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Capacity per slot",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Concurrent reservations",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum notice",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      },
      {
       "kind": "textField",
       "label": "Maximum advance booking period",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 23 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource time-slot configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource time-slot untouched.",
   "emptyFirstRun": "No resource time-slot configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setResourceSchedule",
    "contract": "resources",
    "purpose": "Slot length and booking limits",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceSchedule",
     "getResourceAvailability"
    ]
   },
   {
    "operationId": "getResourceSchedule",
    "contract": "resources",
    "purpose": "The current slots",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-867",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-867"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 23. 0 of 0 labels bound to a contract property; 13 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
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
  "id": "BO-868",
  "name": "Advance Reservation Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "05",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/advance-reservation-management-bo-868",
   "component": "apps/venue-management-web/src/routes/rentals/AdvanceReservationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-864"
   ],
   "exitTo": [
    "BO-864"
   ],
   "transitions": [
    {
     "to": "BO-864",
     "trigger": "Back to Resource Calendar Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Users shall configure; Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Allow resources to be reserved before final operational assignment or ticket transaction.",
  "purposeNote": "Authorized users can reserve resources in advance while TICVAI prevents invalid or conflicting reservations.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Reservation reference",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Resource type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Date",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Start time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "End time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Customer/event/experience",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Capacity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Reservation status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Notes",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Reservation States",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Hold duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic expiry",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Extension permissions",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Release rules",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Smart Availability",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Availability",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Existing bookings",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Dependencies",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venue restrictions",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Resource status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Operational blocks",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 24 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The advance reservation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the advance reservation untouched.",
   "emptyFirstRun": "No advance reservation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResourceBookings",
    "contract": "resources",
    "purpose": "Reservations ahead",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "bookResource",
    "contract": "resources",
    "purpose": "Reserve in advance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings",
     "getResourceAvailability"
    ]
   },
   {
    "operationId": "updateResourceBooking",
    "contract": "resources",
    "purpose": "Move or resize it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-868",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-868"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 26 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-869",
  "name": "Recurring Reservation Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "06",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/recurring-reservation-configuration-bo-869",
   "component": "apps/venue-management-web/src/routes/rentals/RecurringReservationConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-864"
   ],
   "exitTo": [
    "BO-864"
   ],
   "transitions": [
    {
     "to": "BO-864",
     "trigger": "Back to Resource Calendar Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Users shall configure) and no display directory — it is settings, not a population",
  "purpose": "Allow resources to be reserved repeatedly without creating each reservation individually.",
  "purposeNote": "Users can create and manage recurring resource reservations while TICVAI validates every occurrence and clearly identifies exceptions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Start date",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "End date",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Frequency",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Days",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Times",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Number of occurrences",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Exceptions",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Conflict Handling",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Users shall configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Selected weekdays",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected dates",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 26 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recurring reservation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the recurring reservation untouched.",
   "emptyFirstRun": "No recurring reservation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "bookResource",
    "contract": "resources",
    "purpose": "Create the series",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings",
     "getResourceAvailability"
    ]
   },
   {
    "operationId": "cancelResourceBooking",
    "contract": "resources",
    "purpose": "Cancel an occurrence or the series",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-869",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-869"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 12 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Selected weekdays are choices sent by `bookResource` (recurrence.daysOfWeek); Selected dates are choices sent by `bookResource` (one booking per selected date; field gap: recurrence has no explicit dates[]).",
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
  "id": "BO-870",
  "name": "Operational Time & Resource Blocking",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "08",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/operational-time-resource-blocking-bo-870",
   "component": "apps/venue-management-web/src/routes/rentals/OperationalTimeResourceBlocking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-864"
   ],
   "exitTo": [
    "BO-864"
   ],
   "transitions": [
    {
     "to": "BO-864",
     "trigger": "Back to Resource Calendar Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Users shall configure) and no display directory — it is settings, not a population",
  "purpose": "Protect non-customer-facing time required for preparation, movement, maintenance and operational activities.",
  "purposeNote": "Operational time blocks automatically affect resource availability and prevent reservations that would interfere with required operational activities.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Setup",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Teardown",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Cleaning",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maintenance",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Inspection",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Travel",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Break",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Training",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Private use",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venue closure",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Operational hold",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Custom block",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 28 §Users shall configure"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational time resource configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the operational time resource untouched.",
   "emptyFirstRun": "No operational time resource configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResourceBlocks",
    "contract": "resources",
    "purpose": "Blocks in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createResourceBlock",
    "contract": "resources",
    "purpose": "Block a window",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceBlocks",
     "getResourceCalendar"
    ]
   },
   {
    "operationId": "releaseResourceBlock",
    "contract": "resources",
    "purpose": "Put it back into service",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceBlocks",
     "getResourceCalendar"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-870",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-870"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 28. 0 of 0 labels bound to a contract property; 12 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "blockId",
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
  "id": "BO-871",
  "name": "Multi-Event Resource Planning",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "09",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/multi-event-resource-planning-bo-871",
   "component": "apps/venue-management-web/src/routes/rentals/MultiEventResourcePlanning.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-864"
   ],
   "exitTo": [
    "BO-864"
   ],
   "transitions": [
    {
     "to": "BO-864",
     "trigger": "Back to Resource Calendar Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§The screen shall display) and no metric row",
  "purpose": "Allow operations teams to manage shared resources across multiple simultaneous events, experiences and operational activities.",
  "purposeNote": "Operations teams can understand resource demand across parallel events and identify shortages or allocation conflicts before operations begin.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 29 §The screen shall display"
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
       "label": "Every multi-event resource planning",
       "columns": [
        "Events",
        "Experiences",
        "Resources",
        "Venues",
        "Time periods",
        "Assignments",
        "Conflicts",
        "Capacity",
        "Resource gaps"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 29 §The screen shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected multi-event resource planning",
       "bindsTo": null,
       "columns": [
        "Events",
        "Experiences",
        "Resources",
        "Venues",
        "Time periods",
        "Assignments",
        "Conflicts",
        "Capacity",
        "Resource gaps"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Event A”, “Event B”, “Events may be assigned”, “Resource allocation can consider”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 29 §The screen shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-event resource planning list.",
   "error": "Could not load. Names which read failed and leaves the multi-event resource planning untouched.",
   "emptyFirstRun": "No multi-event resource planning yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-event resource planning are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceCalendar",
    "contract": "resources",
    "purpose": "Several events at once",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "allocateResources",
    "contract": "resources",
    "purpose": "Fill each requirement",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Events",
    "Experiences",
    "Resources",
    "Venues",
    "Time periods",
    "Assignments"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-871",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-871"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 29. 0 of 9 labels bound to a contract property; 9 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-872",
  "name": "Smart Assignment & Drag-and-Drop Reallocation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "2",
   "number": "10",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/smart-assignment-drag-and-drop-reallocation-bo-872",
   "component": "apps/venue-management-web/src/routes/rentals/SmartAssignmentDragAndDropReallocation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-864"
   ],
   "exitTo": [
    "BO-864"
   ],
   "transitions": [
    {
     "to": "BO-864",
     "trigger": "Back to Resource Calendar Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the fast, visual assignment experience that operational users and cashiers can use when assigning or changing resources. This should become one of the signature TICVAI Resource Management experiences. Provide TICVAI with a centralized backend configuration environment for treating employees, instructors, contractors, technicians, security personnel, event staff, and other personnel as intelligent operational resources.",
  "purposeNote": "Authorized users can assign or reassign resources visually through drag-and-drop or AI Smart Assign, with real-time validation preventing invalid allocations and all changes recorded in audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 30"
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
       "impliedBy": "updateResourceBooking",
       "label": "Save resource booking",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateResourceBooking"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The smart drag-and-drop reallocation list.",
   "error": "Could not load. Names which read failed and leaves the smart drag-and-drop reallocation untouched.",
   "emptyFirstRun": "No smart drag-and-drop reallocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the smart drag-and-drop reallocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateResourceBooking",
    "contract": "resources",
    "purpose": "Drag to reassign, extend or shorten",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings"
    ]
   },
   {
    "operationId": "getResourceCalendar",
    "contract": "resources",
    "purpose": "The grid being dragged on",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-872",
   "workshopBoard": "wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-872"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 101 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "allocateResources": {
  "method": "POST",
  "path": "/resource-allocations",
  "contract": "resources",
  "summary": "Fill a requirement from the pool, rotating rather than repeating",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "bookResource": {
  "method": "POST",
  "path": "/resource-bookings",
  "contract": "resources",
  "summary": "Reserve a specific resource for a window — staff only",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "cancelResourceBooking": {
  "method": "DELETE",
  "path": "/resource-bookings/{bookingId}",
  "contract": "resources",
  "summary": "Cancel one occurrence, or the whole series",
  "permission": "RESOURCE_BOOK",
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
    "name": "scope",
    "in": "query",
    "required": true
   },
   {
    "name": "reason",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ResourceBooking"
 },
 "createResourceBlock": {
  "method": "POST",
  "path": "/resource-blocks",
  "contract": "resources",
  "summary": "Take a resource out of service for a window, with a reason",
  "permission": "RESOURCE_MANAGE",
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
  "requestBody": "ResourceBlock",
  "responds": "ResourceBlock"
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
 "getResourceSchedule": {
  "method": "GET",
  "path": "/resources/{resourceId}/schedule",
  "contract": "resources",
  "summary": "The pattern of when it is normally available",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceSchedule"
 },
 "listResourceBlocks": {
  "method": "GET",
  "path": "/resource-blocks",
  "contract": "resources",
  "summary": "Operational, setup and maintenance blocks",
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
   }
  ],
  "requestBody": null,
  "responds": "ResourceBlock"
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
 "releaseResourceBlock": {
  "method": "DELETE",
  "path": "/resource-blocks/{blockId}",
  "contract": "resources",
  "summary": "Put it back into service",
  "permission": "RESOURCE_MANAGE",
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
 "setResourceSchedule": {
  "method": "PUT",
  "path": "/resources/{resourceId}/schedule",
  "contract": "resources",
  "summary": "Operating hours, working pattern and bookable slots",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourceSchedule",
  "responds": "ResourceSchedule"
 },
 "suggestResources": {
  "method": "GET",
  "path": "/resource-suggestions",
  "contract": "resources",
  "summary": "Resources matching a requirement, by attribute",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "resourceTypeId",
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
    "name": "attributes",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 },
 "updateResourceBooking": {
  "method": "PATCH",
  "path": "/resource-bookings/{bookingId}",
  "contract": "resources",
  "summary": "Extend, shorten or reassign a booking",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
    "default": 0
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
 "ResourceBlock": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_block",
  "description": "Board 2.07. **A block is not a booking**, and the reason travels with it so an operator knows whether to wait or to look elsewhere.\n",
  "required": [
   "resourceId",
   "from",
   "to",
   "reason"
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
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "reason": {
    "type": "string",
    "enum": [
     "setup",
     "teardown",
     "maintenance",
     "blackout",
     "closed",
     "operational",
     "training"
    ]
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "createdBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
 "ResourceSchedule": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_schedule",
  "description": "Boards 2.03 and 2.04. **A recurring pattern with exceptions, not a list of dates.** A schedule written as concrete dates silently expires.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "availabilityMode": {
    "type": "string",
    "enum": [
     "alwaysAvailable",
     "scheduled",
     "onRequest"
    ]
   },
   "windows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "from": {
       "type": "string",
       "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
       "description": "Local time of day, HH:MM."
      },
      "to": {
       "type": "string",
       "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
       "description": "Local time of day, HH:MM."
      },
      "effectiveFrom": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "effectiveTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "slotMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "**How finely this resource's time can be cut**, which is a property of the resource and not of the product sold against it.\n"
   },
   "minimumBookingMinutes": {
    "type": "integer",
    "nullable": true
   },
   "maximumBookingMinutes": {
    "type": "integer",
    "nullable": true
   },
   "advanceBookingDays": {
    "type": "integer",
    "nullable": true
   },
   "exceptions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "closed": {
       "type": "boolean"
      },
      "from": {
       "type": "string",
       "nullable": true,
       "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
       "description": "Local time of day, HH:MM."
      },
      "to": {
       "type": "string",
       "nullable": true,
       "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
       "description": "Local time of day, HH:MM."
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
