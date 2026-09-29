# WS127 — Event Management Configuration Backend Structure v1.0 board 3

**3 screens · 2 operations · 1 schemas · 1 permissions**

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
  `EVENT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-700` | Venue & Space Command Center | listDetail | 1 | 0 | — |
| `BO-701` | Venue Master Configuration | listDetail | 1 | 0 | — |
| `BO-702` | Space Access Rules Configuration | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-700, BO-701, BO-702 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-700",
  "name": "Venue & Space Command Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "01",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/venue-space-command-center-bo-700",
   "component": "apps/venue-management-web/src/routes/sell/VenueSpaceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-701",
    "BO-702"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-701",
     "trigger": "Venue Master Configuration",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-702",
     "trigger": "Space Access Rules Configuration",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
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
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSpaces",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue space list.",
   "error": "Could not load. Names which read failed and leaves the venue space untouched.",
   "emptyFirstRun": "No venue space yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue space are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSpaces",
    "contract": "catalogue",
    "purpose": "Spaces at this venue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-700",
   "workshopBoard": "wireframes/WS50 Event Management Configuration Backend Structure v1.0 Board 3.dc.html#bo-700"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 81. 0 of 0 labels bound to a contract property; 0 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-701",
  "name": "Venue Master Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "02",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/venue-master-configuration-bo-701",
   "component": "apps/venue-management-web/src/routes/sell/VenueMasterConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-700"
   ],
   "exitTo": [
    "BO-700"
   ],
   "transitions": [
    {
     "to": "BO-700",
     "trigger": "Back to Venue & Space Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
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
       "impliedBy": "setSpace",
       "label": "Save space",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSpace"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue master list.",
   "error": "Could not load. Names which read failed and leaves the venue master untouched.",
   "emptyFirstRun": "No venue master yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue master are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSpace",
    "contract": "catalogue",
    "purpose": "Define a space",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSpaces"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-701",
   "workshopBoard": "wireframes/WS50 Event Management Configuration Backend Structure v1.0 Board 3.dc.html#bo-701"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 82. 0 of 0 labels bound to a contract property; 0 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-702",
  "name": "Space Access Rules Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "06",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/space-access-rules-configuration-bo-702",
   "component": "apps/venue-management-web/src/routes/sell/SpaceAccessRulesConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-700"
   ],
   "exitTo": [
    "BO-700"
   ],
   "transitions": [
    {
     "to": "BO-700",
     "trigger": "Back to Venue & Space Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
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
       "label": "Every space access rules",
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
       "label": "The selected space access rules",
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
   "loading": "The space access rules list.",
   "error": "Could not load. Names which read failed and leaves the space access rules untouched.",
   "emptyFirstRun": "No space access rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the space access rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSpace",
    "contract": "catalogue",
    "purpose": "Space access rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSpaces"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "AI Proposal",
    "Existing / Approved Configuration"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-702",
   "workshopBoard": "wireframes/WS50 Event Management Configuration Backend Structure v1.0 Board 3.dc.html#bo-702"
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
 "listSpaces": {
  "method": "GET",
  "path": "/spaces",
  "contract": "catalogue",
  "summary": "Halls, rooms and areas an event can occupy",
  "permission": "EVENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Space"
 },
 "setSpace": {
  "method": "PUT",
  "path": "/spaces",
  "contract": "catalogue",
  "summary": "Define a space, its capacity and its access rules",
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
  "requestBody": "Space",
  "responds": "Space"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Space": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.space",
  "description": "Event board 3.2. **Bookable, as distinct from navigable** — `venue-map` owns the geometry.\n",
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "venueMapZoneId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Where the space is also a bookable `resources` resource**, so its calendar and conflict detection come from there rather than a second scheduler.\n"
   },
   "parentSpaceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "maximumCapacity": {
    "type": "integer",
    "nullable": true
   },
   "safeCapacity": {
    "type": "integer",
    "nullable": true
   },
   "setupMinutes": {
    "type": "integer",
    "default": 0
   },
   "teardownMinutes": {
    "type": "integer",
    "default": 0
   },
   "accessRules": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true
   },
   "bookable": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
