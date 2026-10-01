# P02-high-demand-access-01 — P02 · High-Demand Access

**1 screens · 2 operations · 2 schemas · 0 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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
- **0 of these operations work offline**
  
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-046` | Branded Queue / Waiting Room | statusTracker | 2 | 0 | — |

## Thin screens in this batch

**GST-046 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-046",
  "name": "Branded Queue / Waiting Room",
  "module": "High-Demand Access",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C98",
  "implementation": {
   "app": "guest-app",
   "route": "/general/branded-queue-waiting-room",
   "component": "apps/guest-app/src/routes/general/BrandedQueueWaitingRoomDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-007"
   ],
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-007"
   ],
   "transitions": [
    {
     "to": "GST-007",
     "trigger": "Continue to your tickets",
     "precondition": "`getWaitingRoomPosition` answers `admitted`. The app keeps `admission.token` and sends it as `X-Admission-Token` on `addCartLine` until `admission.expiresAt`",
     "carries": [
      "performanceId"
     ],
     "provenance": "ADR-0066 (accepted 1 October 2026) and its 1 October amendment"
    }
   ]
  },
  "notes": "**The on-sale waiting room (Q2), not the ride queue (Q1). Re-pointed 1 October under ADR-0066** from `getWaitTimes`, `getWaitingGuest` and `joinQueue`, which are the ride queue and wrote a `queue.entry` row per arriving guest, the load the room exists to keep away. The ride queue stays on GST-023. Arrival is `enterWaitingRoom` (a Redis counter, no database write, no personal data); the screen polls `getWaitingRoomPosition` every `pollAfterSeconds`. Admitted, it holds a short-lived signed admission token that `addCartLine` needs for this performance while its room is on (online cart holds only: the 1 October amendment exempts tills, kiosks and venue workstations). **Reached from the sale, not the home screen:** GST-007 lands here when `addCartLine` refuses `403 admission-required`, and admission returns there. `notRequired` (the room is off) goes straight back. **A guest surface is one product with two renderings** (WEB-015): the same named screen on web and app calls the same guest-callable operations.",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getWaitingRoomPosition` reads one guest's place in one performance's room, polled — the screen is about that one thing",
  "purpose": "The on-sale waiting room for one performance — the guest's place, the wait, and the way on to the sale once admitted.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Your place in the waiting room",
       "bindsTo": "WaitingRoomEntry",
       "columns": [
        "WaitingRoomEntry.state",
        "WaitingRoomEntry.position",
        "WaitingRoomEntry.aheadOfYou",
        "WaitingRoomEntry.estimatedWaitSeconds"
       ],
       "operation": "getWaitingRoomPosition",
       "provenance": "contract catalogue.yaml GET /performances/{performanceId}/waiting-room/entries/{waitingEntryId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Take my place",
       "operation": "enterWaitingRoom",
       "notes": "The one write on this screen, pressed rather than fired on load so a prefetch or a bot does not take a place. Hidden once the guest has one.",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/waiting-room/entries"
      },
      {
       "kind": "primaryButton",
       "label": "Continue to your tickets",
       "provenance": "ADR-0066; live when `getWaitingRoomPosition` answers `admitted`"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Taking a place in the room. *Take my place* (`enterWaitingRoom`) answers with a position, or `notRequired` and the guest goes straight on to the sale",
   "error": "**Lost the place.** A retry sends the same `Idempotency-Key` and gets the same entry back, so the guest is not sent to the back, and the screen says so. `expired` (the admission was not used in time) offers to enter again; `closed` (the room was switched off or the performance stopped selling) says so and goes back to the event",
   "emptyFirstRun": "—",
   "offline": "**The offline banner shows.** The last known position stays on screen with its age, and polling resumes with the same entry when the connection is back. Admission needs the connection."
  },
  "apis": [
   {
    "operationId": "enterWaitingRoom",
    "contract": "catalogue",
    "purpose": "Take a place in the performance's on-sale waiting room (ADR-0066); `notRequired` when the room is off",
    "trigger": "onAction"
   },
   {
    "operationId": "getWaitingRoomPosition",
    "contract": "catalogue",
    "purpose": "The guest's place, polled every `pollAfterSeconds`; admitted, it carries the admission token for `addCartLine`",
    "trigger": "onInterval"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "performanceId",
     "from": "GST-007"
    },
    {
     "name": "waitingEntryId",
     "from": "GST-046",
     "optional": true
    }
   ],
   "coldEntry": "**Named, closed or expired — never a 404** (ADR-0030). Opened with no performance, or one no longer selling, the room says so and offers the event."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-046",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 1 → Branded queue / waiting room"
   }
  },
  "apisNote": "Rebuilt 1 October 2026 on the two waiting-room operations (ADR-0066). Columns are the entry's guest-facing fields; `pollAfterSeconds` and `admission` are plumbing the screen acts on rather than shows.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
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
 "enterWaitingRoom": {
  "method": "POST",
  "path": "/performances/{performanceId}/waiting-room/entries",
  "contract": "catalogue",
  "summary": "Join the on-sale waiting room for a performance",
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
  "requestBody": null,
  "responds": "WaitingRoomEntry"
 },
 "getWaitingRoomPosition": {
  "method": "GET",
  "path": "/performances/{performanceId}/waiting-room/entries/{waitingEntryId}",
  "contract": "catalogue",
  "summary": "Where a waiting guest is, and the admission token once admitted",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WaitingRoomEntry"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "WaitingRoomAdmission": {
  "type": "object",
  "x-ticvai-persistence": "none — transient, a signed token that is checked and never stored",
  "description": "**The admission token** (ADR-0066). Signed with a Key Vault secret; carries the tenant, the performance, the expiry and a unique id, so it cannot be moved to another performance or replayed after it expires. Sent as `X-Admission-Token` (shared parameter `AdmissionToken`).",
  "required": [
   "token",
   "performanceId",
   "expiresAt"
  ],
  "properties": {
   "token": {
    "type": "string",
    "description": "The signed token, opaque to the client."
   },
   "tokenId": {
    "type": "string",
    "format": "uuid",
    "description": "The token's unique id."
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WaitingRoomEntry": {
  "type": "object",
  "x-ticvai-persistence": "none — transient, held in the room's Redis counters and never in a table",
  "description": "One guest's place in a performance's waiting room (ADR-0066). No personal data.",
  "required": [
   "waitingEntryId",
   "performanceId",
   "state"
  ],
  "properties": {
   "waitingEntryId": {
    "type": "string",
    "format": "uuid",
    "description": "A UUIDv7 minted on arrival; what the waiting page polls with."
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "state": {
    "type": "string",
    "enum": [
     "notRequired",
     "waiting",
     "admitted",
     "expired",
     "closed"
    ],
    "description": "`notRequired`: the room is off, go to the sale. `waiting`: keep polling. `admitted`: `admission` is set. `expired`: the admission was not used in time; enter again. `closed`: the room was switched off or the performance stopped selling."
   },
   "position": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Place in the room; null unless `waiting`."
   },
   "aheadOfYou": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "estimatedWaitSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "At the current release rate. An estimate, and the page says so."
   },
   "pollAfterSeconds": {
    "type": "integer",
    "minimum": 1,
    "default": 5
   },
   "admission": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WaitingRoomAdmission"
     }
    ],
    "nullable": true,
    "description": "Set when `state` is `admitted`."
   }
  }
 }
}
```
