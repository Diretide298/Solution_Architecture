# WS128 — Event Management Configuration Backend Structure v1.0 board 4

**3 screens · 1 operations · 1 schemas · 1 permissions**

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
  `CAPACITY_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-703` | Seating & Capacity Command Center | listDetail | 1 | 0 | — |
| `BO-704` | Event Capacity Profile Configuration | listDetail | 1 | 0 | — |
| `BO-705` | Seating Mode & Reservation Configuration | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-703, BO-704, BO-705 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-703",
  "name": "Seating & Capacity Command Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "01",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/seating-capacity-command-center-bo-703",
   "component": "apps/venue-management-web/src/routes/sell/SeatingCapacityCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-704",
    "BO-705"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-704",
     "trigger": "Event Capacity Profile Configuration",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-705",
     "trigger": "Seating Mode & Reservation Configuration",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
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
       "impliedBy": "setEventCapacityProfile",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventCapacityProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seating capacity list.",
   "error": "Could not load. Names which read failed and leaves the seating capacity untouched.",
   "emptyFirstRun": "No seating capacity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seating capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventCapacityProfile",
    "contract": "catalogue",
    "purpose": "Capacity at a glance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatInventory"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-703",
   "workshopBoard": "wireframes/WS51 Event Management Configuration Backend Structure v1.0 Board 4.dc.html#bo-703"
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
  "id": "BO-704",
  "name": "Event Capacity Profile Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "02",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-capacity-profile-configuration-bo-704",
   "component": "apps/venue-management-web/src/routes/sell/EventCapacityProfileConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-703"
   ],
   "exitTo": [
    "BO-703"
   ],
   "transitions": [
    {
     "to": "BO-703",
     "trigger": "Back to Seating & Capacity Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
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
       "impliedBy": "setEventCapacityProfile",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventCapacityProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event capacity profile list.",
   "error": "Could not load. Names which read failed and leaves the event capacity profile untouched.",
   "emptyFirstRun": "No event capacity profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event capacity profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventCapacityProfile",
    "contract": "catalogue",
    "purpose": "The capacity profile",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatInventory"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-704",
   "workshopBoard": "wireframes/WS51 Event Management Configuration Backend Structure v1.0 Board 4.dc.html#bo-704"
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
  "id": "BO-705",
  "name": "Seating Mode & Reservation Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "03",
   "page": 83
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/seating-mode-reservation-configuration-bo-705",
   "component": "apps/venue-management-web/src/routes/sell/SeatingModeReservationConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-703"
   ],
   "exitTo": [
    "BO-703"
   ],
   "transitions": [
    {
     "to": "BO-703",
     "trigger": "Back to Seating & Capacity Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
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
       "impliedBy": "setEventCapacityProfile",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventCapacityProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seating mode reservation list.",
   "error": "Could not load. Names which read failed and leaves the seating mode reservation untouched.",
   "emptyFirstRun": "No seating mode reservation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seating mode reservation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventCapacityProfile",
    "contract": "catalogue",
    "purpose": "Seating mode",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatInventory"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-705",
   "workshopBoard": "wireframes/WS51 Event Management Configuration Backend Structure v1.0 Board 4.dc.html#bo-705"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 83. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "setEventCapacityProfile": {
  "method": "PUT",
  "path": "/events/{eventId}/capacity-profile",
  "contract": "catalogue",
  "summary": "How many, in what mode, and held back for whom",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "EventCapacityProfile",
  "responds": "EventCapacityProfile"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "EventCapacityProfile": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.event_capacity_profile",
  "description": "Event board 4.2. **Capacity is four numbers, not one.**",
  "properties": {
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "mode": {
    "type": "string",
    "enum": [
     "reservedSeating",
     "unreservedSeating",
     "standing",
     "mixed",
     "capacityOnly"
    ],
    "description": "**The same hall is seated on Friday and standing on Saturday**, so the mode is per performance.\n"
   },
   "safeMaximum": {
    "type": "integer"
   },
   "sellable": {
    "type": "integer"
   },
   "held": {
    "type": "integer",
    "default": 0
   },
   "accessibleProvision": {
    "type": "integer",
    "default": 0
   },
   "companionSeats": {
    "type": "integer",
    "default": 0
   },
   "overbookPercent": {
    "type": "number",
    "default": 0
   },
   "seatMapId": {
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
