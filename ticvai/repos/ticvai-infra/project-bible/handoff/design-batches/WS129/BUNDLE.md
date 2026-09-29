# WS129 — Event Management Configuration Backend Structure v1.0 board 5

**4 screens · 2 operations · 2 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ACCREDITATION_VIEW, EVENT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-706` | Registration & Attendance Command Center | listDetail | 1 | 0 | — |
| `BO-707` | Attendee Data & Registration Form Configuration | listDetail | 1 | 0 | — |
| `BO-708` | Accreditation & Participant Category Configuration | listDetail | 2 | 0 | — |
| `BO-709` | Event Admission & Entry Policy Configuration | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-706, BO-707, BO-708, BO-709 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-706",
  "name": "Registration & Attendance Command Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "5",
   "number": "01",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/registration-attendance-command-center-bo-706",
   "component": "apps/venue-management-web/src/routes/sell/RegistrationAttendanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-707",
    "BO-708",
    "BO-709"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-707",
     "trigger": "Attendee Data & Registration Form Configuration",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-708",
     "trigger": "Accreditation & Participant Category Configuration",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-709",
     "trigger": "Event Admission & Entry Policy Configuration",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
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
       "impliedBy": "setEventRegistration",
       "label": "Save event registration",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventRegistration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The registration attendance list.",
   "error": "Could not load. Names which read failed and leaves the registration attendance untouched.",
   "emptyFirstRun": "No registration attendance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the registration attendance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventRegistration",
    "contract": "catalogue",
    "purpose": "Registration at a glance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-706",
   "workshopBoard": "wireframes/WS52 Event Management Configuration Backend Structure v1.0 Board 5.dc.html#bo-706"
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
  "id": "BO-707",
  "name": "Attendee Data & Registration Form Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "5",
   "number": "05",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/attendee-data-registration-form-configuration-bo-707",
   "component": "apps/venue-management-web/src/routes/sell/AttendeeDataRegistrationFormConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-706"
   ],
   "exitTo": [
    "BO-706"
   ],
   "transitions": [
    {
     "to": "BO-706",
     "trigger": "Back to Registration & Attendance Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
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
       "impliedBy": "setEventRegistration",
       "label": "Save event registration",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventRegistration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attendee data registration list.",
   "error": "Could not load. Names which read failed and leaves the attendee data registration untouched.",
   "emptyFirstRun": "No attendee data registration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attendee data registration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventRegistration",
    "contract": "catalogue",
    "purpose": "Attendee data and form",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-707",
   "workshopBoard": "wireframes/WS52 Event Management Configuration Backend Structure v1.0 Board 5.dc.html#bo-707"
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
  "id": "BO-708",
  "name": "Accreditation & Participant Category Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "5",
   "number": "06",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/accreditation-participant-category-configuration-bo-708",
   "component": "apps/venue-management-web/src/routes/sell/AccreditationParticipantCategoryConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-706"
   ],
   "exitTo": [
    "BO-706"
   ],
   "transitions": [
    {
     "to": "BO-706",
     "trigger": "Back to Registration & Attendance Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
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
       "label": "Every accreditation participant category",
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
       "label": "The selected accreditation participant category",
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
   "loading": "The accreditation participant category list.",
   "error": "Could not load. Names which read failed and leaves the accreditation participant category untouched.",
   "emptyFirstRun": "No accreditation participant category yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation participant category are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventRegistration",
    "contract": "catalogue",
    "purpose": "Participant categories",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAccessProfiles",
    "contract": "accreditation",
    "purpose": "The passes they map to",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-708",
   "workshopBoard": "wireframes/WS52 Event Management Configuration Backend Structure v1.0 Board 5.dc.html#bo-708"
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
 },
 {
  "id": "BO-709",
  "name": "Event Admission & Entry Policy Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "5",
   "number": "08",
   "page": 87
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-admission-entry-policy-configuration-bo-709",
   "component": "apps/venue-management-web/src/routes/sell/EventAdmissionEntryPolicyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-706"
   ],
   "exitTo": [
    "BO-706"
   ],
   "transitions": [
    {
     "to": "BO-706",
     "trigger": "Back to Registration & Attendance Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
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
       "impliedBy": "setEventRegistration",
       "label": "Save event registration",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventRegistration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event admission entry list.",
   "error": "Could not load. Names which read failed and leaves the event admission entry untouched.",
   "emptyFirstRun": "No event admission entry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event admission entry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventRegistration",
    "contract": "catalogue",
    "purpose": "Admission and entry policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-709",
   "workshopBoard": "wireframes/WS52 Event Management Configuration Backend Structure v1.0 Board 5.dc.html#bo-709"
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
 "listAccessProfiles": {
  "method": "GET",
  "path": "/accreditation-access-profiles",
  "contract": "accreditation",
  "summary": "Named bundles of zones, dates and times",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessProfile"
 },
 "setEventRegistration": {
  "method": "PUT",
  "path": "/events/{eventId}/registration",
  "contract": "catalogue",
  "summary": "What is captured, from whom, and what it lets them in to",
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
  "requestBody": "EventRegistration",
  "responds": "EventRegistration"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessProfile": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.access_profile",
  "description": "Board 5.2. **How an estate stays governable.**",
  "required": [
   "code",
   "name"
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
   "zoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "operationalAreas": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "schedule": {
    "type": "array",
    "description": "**Zone, date and time are three dimensions and all three are needed.**",
    "items": {
     "type": "object",
     "properties": {
      "zoneId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "dateFrom": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "dateTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "from": {
       "type": "string",
       "nullable": true
      },
      "to": {
       "type": "string",
       "nullable": true
      },
      "eventPhase": {
       "type": "string",
       "nullable": true,
       "enum": [
        "build",
        "rehearsal",
        "doorsOpen",
        "liveShow",
        "breakdown"
       ]
      }
     }
    }
   },
   "escortRequired": {
    "type": "boolean",
    "default": false
   },
   "holderCount": {
    "type": "integer",
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "EventRegistration": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.event_registration",
  "description": "Event boards 5.2 and 5.3. **Registration is not ticketing.**",
  "properties": {
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "required": {
    "type": "boolean",
    "default": false
   },
   "formId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "capturePerAttendee": {
    "type": "boolean",
    "default": true
   },
   "participantCategories": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "accessProfileId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "**Where this meets `accreditation`** — a delegate, a speaker and a sponsor hold different passes to the same event.\n"
      },
      "quota": {
       "type": "integer",
       "nullable": true
      },
      "requiresApproval": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "admissionPolicy": {
    "type": "object",
    "properties": {
     "reEntryAllowed": {
      "type": "boolean",
      "default": true
     },
     "latecomerPolicy": {
      "type": "string",
      "nullable": true
     },
     "idCheckRequired": {
      "type": "boolean",
      "default": false
     },
     "minimumAge": {
      "type": "integer",
      "nullable": true
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
