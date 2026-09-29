# WS126 — Event Management Configuration Backend Structure v1.0 board 2

**3 screens · 2 operations · 2 schemas · 1 permissions**

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
  `PERFORMANCE_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-697` | Event Schedule Command Center | listDetail | 1 | 0 | — |
| `BO-698` | Dynamic Performance Duration Configuration | listDetail | 1 | 0 | — |
| `BO-699` | Schedule Change & Rescheduling Configuration | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-697, BO-698, BO-699 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-697",
  "name": "Event Schedule Command Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "01",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-schedule-command-center-bo-697",
   "component": "apps/venue-management-web/src/routes/sell/EventScheduleCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-698",
    "BO-699"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-698",
     "trigger": "Dynamic Performance Duration Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-699",
     "trigger": "Schedule Change & Rescheduling Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide management with a consolidated backend view of the financial, commercial, sponsorship, attendance and operational performance of events.",
  "purposeNote": "Authorized users can obtain a consolidated view of event commercial and operational performance while data visibility remains controlled by tenant, entity and role permissions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 81"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 81"
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
       "impliedBy": "setEventSchedule",
       "label": "Save event schedule",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventSchedule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event schedule list.",
   "error": "Could not load. Names which read failed and leaves the event schedule untouched.",
   "emptyFirstRun": "No event schedule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event schedule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventSchedule",
    "contract": "catalogue",
    "purpose": "The schedule",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listEvents"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-697",
   "workshopBoard": "wireframes/WS49 Event Management Configuration Backend Structure v1.0 Board 2.dc.html#bo-697"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 81. 0 of 0 labels bound to a contract property; 0 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "eventId",
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
  "id": "BO-698",
  "name": "Dynamic Performance Duration Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "07",
   "page": 86
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/dynamic-performance-duration-configuration-bo-698",
   "component": "apps/venue-management-web/src/routes/sell/DynamicPerformanceDurationConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-697"
   ],
   "exitTo": [
    "BO-697"
   ],
   "transitions": [
    {
     "to": "BO-697",
     "trigger": "Back to Event Schedule Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Configure KPI by; Display) and no metric row",
  "purpose": "Configure measurable operational KPIs for staff, instructors and activity operators.",
  "purposeNote": "Administrators can define measurable operator/instructor KPIs and calculate performance using traceable operational records from completed sessions.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 86 §Display"
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
       "label": "Every dynamic performance duration",
       "columns": [
        "Target vs Actual"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 86 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dynamic performance duration",
       "bindsTo": null,
       "columns": [
        "Target vs Actual"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Set”.",
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 86 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic performance duration list.",
   "error": "Could not load. Names which read failed and leaves the dynamic performance duration untouched.",
   "emptyFirstRun": "No dynamic performance duration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic performance duration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventSchedule",
    "contract": "catalogue",
    "purpose": "Dynamic duration and turnaround",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listEvents"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Target vs Actual"
   ],
   "params": [
    {
     "name": "eventId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-698",
   "workshopBoard": "wireframes/WS49 Event Management Configuration Backend Structure v1.0 Board 2.dc.html#bo-698"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 86. 0 of 1 labels bound to a contract property; 1 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-699",
  "name": "Schedule Change & Rescheduling Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "08",
   "page": 87
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/schedule-change-rescheduling-configuration-bo-699",
   "component": "apps/venue-management-web/src/routes/sell/ScheduleChangeReschedulingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-697"
   ],
   "exitTo": [
    "BO-697"
   ],
   "transitions": [
    {
     "to": "BO-697",
     "trigger": "Back to Event Schedule Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure automatic invoice generation for eligible event-related customers and commercial accounts.",
  "purposeNote": "Eligible event transactions can trigger automated invoice requests with complete event and customer references while financial posting remains controlled by Finance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 87"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 87"
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
       "impliedBy": "rescheduleEvent",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "rescheduleEvent"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The schedule change rescheduling list.",
   "error": "Could not load. Names which read failed and leaves the schedule change rescheduling untouched.",
   "emptyFirstRun": "No schedule change rescheduling yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the schedule change rescheduling are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "rescheduleEvent",
    "contract": "catalogue",
    "purpose": "Move or cancel, and treat the tickets",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listEvents",
     "getSeatInventory"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-699",
   "workshopBoard": "wireframes/WS49 Event Management Configuration Backend Structure v1.0 Board 2.dc.html#bo-699"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 87. 0 of 0 labels bound to a contract property; 0 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "eventId",
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
 "rescheduleEvent": {
  "method": "POST",
  "path": "/events/{eventId}/reschedule",
  "contract": "catalogue",
  "summary": "Move or cancel, and decide what happens to the people who bought",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "requestBody": "EventReschedule",
  "responds": null
 },
 "setEventSchedule": {
  "method": "PUT",
  "path": "/events/{eventId}/schedule",
  "contract": "catalogue",
  "summary": "Performance times, durations and turnaround",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "requestBody": "EventSchedule",
  "responds": "EventSchedule"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "EventReschedule": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.event_reschedule",
  "description": "Event boards 7.4 and 7.5. **The decision that generates every phone call.**",
  "required": [
   "kind",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "moveTime",
     "moveDate",
     "moveVenue",
     "cancel",
     "abandon"
    ]
   },
   "performanceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "newStartsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "newSpaceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string"
   },
   "ticketTreatment": {
    "type": "string",
    "enum": [
     "moveAutomatically",
     "offerChoice",
     "refund",
     "creditToWallet",
     "honourAtAnyPerformance"
    ],
    "description": "**Made once and applied consistently**, rather than per guest at a desk."
   },
   "refundFees": {
    "type": "boolean",
    "default": true
   },
   "notifyGuests": {
    "type": "boolean",
    "default": true
   },
   "notificationTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "affectedOrders": {
    "type": "integer",
    "readOnly": true
   },
   "affectedGuests": {
    "type": "integer",
    "readOnly": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "EventSchedule": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.event_schedule",
  "description": "Event board 2.2. **A performance that overruns pushes the next one.**",
  "properties": {
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "performances": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "startsAt": {
       "type": "string",
       "format": "date-time"
      },
      "plannedMinutes": {
       "type": "integer"
      },
      "turnaroundMinutes": {
       "type": "integer",
       "default": 0
      },
      "spaceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "seatMapId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "durationIsDynamic": {
    "type": "boolean",
    "default": false
   },
   "maximumOverrunMinutes": {
    "type": "integer",
    "nullable": true
   },
   "cascadeOverrun": {
    "type": "boolean",
    "default": true,
    "description": "**Whether a late finish moves everything after it**, which is the honest behaviour and the one venues forget to ask for until the first time it happens.\n"
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
