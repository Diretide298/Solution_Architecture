# P01-high-demand-access-01 — P01 · High-Demand Access

**1 screens · 3 operations · 7 schemas · 0 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: getWaitTimes
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-015` | Branded Queue / Waiting Room | statusTracker | 3 | 0 | — |

## Thin screens in this batch

**WEB-015 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-015",
  "name": "Branded Queue / Waiting Room",
  "module": "High-Demand Access",
  "requiresModule": "queue",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/high-demand-access/virtual-waiting-room",
   "component": "apps/guest-web/src/routes/high-demand-access/VirtualWaitingRoomDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Renamed 31 August** from *Virtual Waiting Room*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest.",
  "openQuestions": [
   "CF-48 — Q2 Virtual Waiting Room. Edge infrastructure, not the Q1 queue contract. Build-or-buy decision outstanding with Dinesh and Qossai."
  ],
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getWaitingGuest` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Virtual Waiting Room — the screen a person opens when they need to deal with virtual waiting room.",
  "gaps": [
   {
    "operation": "getWaitTimes",
    "why": "**1 declared operation reach no component on this screen**: getWaitTimes. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected branded queue waiting",
       "bindsTo": "WaitingGuest",
       "columns": [
        "WaitingGuest.id",
        "WaitingGuest.queueId",
        "WaitingGuest.queueName",
        "WaitingGuest.subjectId",
        "WaitingGuest.partyNumber",
        "WaitingGuest.partySize",
        "WaitingGuest.status",
        "WaitingGuest.positionInQueue",
        "WaitingGuest.partiesAhead",
        "WaitingGuest.estimatedCallAt",
        "WaitingGuest.isFastPass",
        "WaitingGuest.entitlementId",
        "WaitingGuest.calledAt",
        "WaitingGuest.returnWindowEndsAt",
        "WaitingGuest.redeemedAt",
        "WaitingGuest.admittedCount"
       ],
       "operation": "getWaitingGuest",
       "provenance": "contract queue.yaml GET /waiting-guests/{entryId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Join",
       "operation": "joinQueue",
       "provenance": "contract queue.yaml POST /waiting-guests"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "joinQueue",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Position in the queue, updating",
   "error": "**Lost the queue position.** The worst failure on this screen: it re-queues rather than silently admitting, and says so, because a guest who thinks they lost their place will open a second tab and make it worse",
   "emptyFirstRun": "—",
   "emptyNoResults": "The filter narrowed it and the branded queue waiting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "joinQueue",
    "contract": "queue",
    "purpose": "Join a virtual queue",
    "trigger": "onAction"
   },
   {
    "operationId": "getWaitingGuest",
    "contract": "queue",
    "purpose": "Read a queue entry",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entryId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `entryId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-015"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
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
 "getWaitTimes": {
  "method": "GET",
  "path": "/queues/wait-times",
  "contract": "queue",
  "summary": "Wait times across a venue",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": true
   },
   {
    "name": "category",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WaitTime"
 },
 "getWaitingGuest": {
  "method": "GET",
  "path": "/waiting-guests/{entryId}",
  "contract": "queue",
  "summary": "Read a queue entry",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WaitingGuest"
 },
 "joinQueue": {
  "method": "POST",
  "path": "/waiting-guests",
  "contract": "queue",
  "summary": "Join a virtual queue",
  "permission": null,
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
  "requestBody": "JoinQueueRequest",
  "responds": "WaitingGuest"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "JoinQueueRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "queueId",
   "partySize",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "partySize": {
    "type": "integer",
    "minimum": 1
   },
   "entitlementId": {
    "type": "string",
    "nullable": true,
    "description": "Fast Pass or priority entitlement. Owned by Product & Entitlement — this contract references it and never defines it.\n"
   },
   "partyHeightsCm": {
    "type": "array",
    "description": "Where the queue has a height requirement. Refusing here is far better than refusing at the ride, in front of a child who has already waited.\n",
    "items": {
     "type": "integer"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "QueueEntryStatus": {
  "type": "string",
  "enum": [
   "waiting",
   "called",
   "redeemed",
   "expired",
   "noShow",
   "cancelled",
   "released"
  ]
 },
 "QueueStatus": {
  "type": "string",
  "enum": [
   "open",
   "paused",
   "closed",
   "atCapacity"
  ]
 },
 "WaitTime": {
  "x-ticvai-persistence": "none — computed from readings and throughput",
  "type": "object",
  "required": [
   "queueId",
   "waitMinutes",
   "source",
   "asOf",
   "isStale"
  ],
  "properties": {
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "queueName": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "attractionProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/QueueStatus"
   },
   "waitMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "Null where the queue is closed or no estimate is available."
   },
   "source": {
    "$ref": "#/components/schemas/WaitTimeSource"
   },
   "isStale": {
    "type": "boolean",
    "description": "The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current.\n"
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WaitTimeSource": {
  "type": "string",
  "description": "Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n",
  "enum": [
   "sensor",
   "throughput",
   "manual",
   "unavailable"
  ]
 },
 "WaitingGuest": {
  "x-ticvai-persistence": "queue.waiting_guest",
  "type": "object",
  "required": [
   "id",
   "queueId",
   "partyNumber",
   "partySize",
   "status",
   "joinedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "queueName": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "partyNumber": {
    "type": "integer",
    "description": "What the guest sees and what appears on signage."
   },
   "partySize": {
    "type": "integer"
   },
   "status": {
    "$ref": "#/components/schemas/QueueEntryStatus"
   },
   "positionInQueue": {
    "type": "integer",
    "nullable": true
   },
   "partiesAhead": {
    "type": "integer",
    "nullable": true
   },
   "estimatedCallAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isFastPass": {
    "type": "boolean"
   },
   "entitlementId": {
    "type": "string",
    "nullable": true
   },
   "calledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnWindowEndsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "redeemedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "admittedCount": {
    "type": "integer",
    "nullable": true
   },
   "joinedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 }
}
```
