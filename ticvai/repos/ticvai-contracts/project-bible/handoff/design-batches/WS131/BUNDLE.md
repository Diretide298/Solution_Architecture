# WS131 — Event Management Configuration Backend Structure v1.0 board 7

**5 screens · 3 operations · 7 schemas · 3 permissions**

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
  `APPROVAL_REQUEST, EVENT_CONFIGURE, PERFORMANCE_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-716` | Event Lifecycle & Change Command Center | listDetail | 1 | 0 | — |
| `BO-717` | Lifecycle Transition Configuration | listDetail | 1 | 0 | — |
| `BO-718` | Event Change Request Configuration | listDetail | 1 | 0 | — |
| `BO-719` | Event Cancellation Workflow Configuration | listDetail | 1 | 0 | — |
| `BO-720` | Ticket, Reservation & Customer Treatment Configuration | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-716, BO-717, BO-718, BO-719, BO-720 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-716",
  "name": "Event Lifecycle & Change Command Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "01",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-lifecycle-change-command-center-bo-716",
   "component": "apps/venue-management-web/src/routes/sell/EventLifecycleChangeCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-717",
    "BO-718",
    "BO-719",
    "BO-720"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-717",
     "trigger": "Lifecycle Transition Configuration",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-718",
     "trigger": "Event Change Request Configuration",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-719",
     "trigger": "Event Cancellation Workflow Configuration",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-720",
     "trigger": "Ticket, Reservation & Customer Treatment Configuration",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
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
       "impliedBy": "setEventLifecycleState",
       "label": "Save event lifecycle state",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventLifecycleState"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event lifecycle change list.",
   "error": "Could not load. Names which read failed and leaves the event lifecycle change untouched.",
   "emptyFirstRun": "No event lifecycle change yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event lifecycle change are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventLifecycleState",
    "contract": "catalogue",
    "purpose": "Lifecycle at a glance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listEvents"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-716",
   "workshopBoard": "wireframes/WS54 Event Management Configuration Backend Structure v1.0 Board 7.dc.html#bo-716"
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
  "id": "BO-717",
  "name": "Lifecycle Transition Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "02",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/lifecycle-transition-configuration-bo-717",
   "component": "apps/venue-management-web/src/routes/sell/LifecycleTransitionConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-716"
   ],
   "exitTo": [
    "BO-716"
   ],
   "transitions": [
    {
     "to": "BO-716",
     "trigger": "Back to Event Lifecycle & Change Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
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
  "purpose": "Configure the financial plan and budget against which event performance will be measured.",
  "purposeNote": "Administrators can create an event-level financial plan and compare budget, commitments, actuals and forecasts using data referenced from the shared Finance services.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 82"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 82"
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
       "impliedBy": "setEventLifecycleState",
       "label": "Save event lifecycle state",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventLifecycleState"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lifecycle transition list.",
   "error": "Could not load. Names which read failed and leaves the lifecycle transition untouched.",
   "emptyFirstRun": "No lifecycle transition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the lifecycle transition are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventLifecycleState",
    "contract": "catalogue",
    "purpose": "Move through the lifecycle",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listEvents"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-717",
   "workshopBoard": "wireframes/WS54 Event Management Configuration Backend Structure v1.0 Board 7.dc.html#bo-717"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 82. 0 of 0 labels bound to a contract property; 0 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-718",
  "name": "Event Change Request Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "03",
   "page": 83
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-change-request-configuration-bo-718",
   "component": "apps/venue-management-web/src/routes/sell/EventChangeRequestConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-716"
   ],
   "exitTo": [
    "BO-716"
   ],
   "transitions": [
    {
     "to": "BO-716",
     "trigger": "Back to Event Lifecycle & Change Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define how financial performance should be measured and attributed to an event.",
  "purposeNote": "The system provides traceable event profitability using configured financial attribution rules without duplicating the underlying accounting ledger.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 83"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 83"
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
       "impliedBy": "createApprovalRequest",
       "label": "Create approval request",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event change request list.",
   "error": "Could not load. Names which read failed and leaves the event change request untouched.",
   "emptyFirstRun": "No event change request yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event change request are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createApprovalRequest",
    "contract": "approvals",
    "purpose": "Raise a change request",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-718",
   "workshopBoard": "wireframes/WS54 Event Management Configuration Backend Structure v1.0 Board 7.dc.html#bo-718"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 83. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-719",
  "name": "Event Cancellation Workflow Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "05",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-cancellation-workflow-configuration-bo-719",
   "component": "apps/venue-management-web/src/routes/sell/EventCancellationWorkflowConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-716"
   ],
   "exitTo": [
    "BO-716"
   ],
   "transitions": [
    {
     "to": "BO-716",
     "trigger": "Back to Event Lifecycle & Change Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
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
  "purpose": "Configure dashboards used to measure event sales, attendance and check-in performance.",
  "purposeNote": "Authorized users can monitor configured sales and attendance KPIs with current check-in information supplied by shared Ticketing and Access Control services.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85"
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
   "loading": "The event cancellation workflow list.",
   "error": "Could not load. Names which read failed and leaves the event cancellation workflow untouched.",
   "emptyFirstRun": "No event cancellation workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event cancellation workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "rescheduleEvent",
    "contract": "catalogue",
    "purpose": "Cancellation workflow",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-719",
   "workshopBoard": "wireframes/WS54 Event Management Configuration Backend Structure v1.0 Board 7.dc.html#bo-719"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 85. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-720",
  "name": "Ticket, Reservation & Customer Treatment Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "06",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/ticket-reservation-customer-treatment-configuration-bo-720",
   "component": "apps/venue-management-web/src/routes/sell/TicketReservationCustomerTreatmentConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-716"
   ],
   "exitTo": [
    "BO-716"
   ],
   "transitions": [
    {
     "to": "BO-716",
     "trigger": "Back to Event Lifecycle & Change Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow authorized administrators to use AI to accelerate creation of event configuration from natural-language instructions or existing templates.",
  "purposeNote": "AI can accelerate event setup while every proposed configuration remains reviewable, editable, permission-controlled and subject to normal approval workflows.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85 §Display"
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
       "label": "Every ticket reservation customer",
       "columns": [
        "AI Proposal",
        "Existing / Approved Configuration"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected ticket reservation customer",
       "bindsTo": null,
       "columns": [
        "AI Proposal",
        "Existing / Approved Configuration"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Administrators can”, “Critical Governance Principle”.",
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket reservation customer list.",
   "error": "Could not load. Names which read failed and leaves the ticket reservation customer untouched.",
   "emptyFirstRun": "No ticket reservation customer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket reservation customer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "rescheduleEvent",
    "contract": "catalogue",
    "purpose": "How tickets and customers are treated",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listEvents",
     "getSeatInventory"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "AI Proposal",
    "Existing / Approved Configuration"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-720",
   "workshopBoard": "wireframes/WS54 Event Management Configuration Backend Structure v1.0 Board 7.dc.html#bo-720"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 85. 0 of 2 labels bound to a contract property; 2 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Raise a request",
  "permission": "APPROVAL_REQUEST",
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
  "requestBody": "CreateApprovalRequest",
  "responds": "ApprovalRequest"
 },
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
 "setEventLifecycleState": {
  "method": "POST",
  "path": "/events/{eventId}/lifecycle",
  "contract": "catalogue",
  "summary": "Draft, planned, on sale, live, closed, cancelled",
  "permission": "EVENT_CONFIGURE",
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
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "CreateApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "kind",
   "subjectContract",
   "subjectType",
   "subjectId",
   "scopePath",
   "summary"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "subjectContract": {
    "type": "string",
    "description": "Which contract owns the thing being approved."
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "description": "**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string",
    "maxLength": 300,
    "description": "What the approver sees in their queue before opening it."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
   },
   "justification": {
    "type": "string",
    "maxLength": 1000
   },
   "isDraft": {
    "type": "boolean",
    "default": false,
    "description": "True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"
   }
  }
 },
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
 }
}
```
