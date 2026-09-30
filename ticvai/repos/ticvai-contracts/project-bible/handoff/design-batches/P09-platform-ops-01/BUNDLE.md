# P09-platform-ops-01 — P09 · Platform Ops

**1 screens · 2 operations · 1 schemas · 2 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
  `PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-318` | Dead Letters | listDetail | 2 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-318",
  "name": "Dead Letters",
  "module": "Platform Ops",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/dead-letters",
   "component": "apps/ticvai-web/src/routes/DeadLetters.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "ADM-001"
   ],
   "inferred": false,
   "entryFrom": [
    "ADM-002"
   ],
   "notes": "**Reached from ADM-002** — a top-level console section. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-318 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    }
   ]
  },
  "notes": "Added 4 September. **47 consumers declare `retryThenDeadLetter` and all 47 are marked `isCritical`, and until this screen existed nothing in the package read the table they land in.** Deliberately not DEV-005 Webhooks: `replayEvents` is partner-facing redelivery of a customer's own integration, and handling a platform failure as a customer integration question is how it stays unfixed.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDeadLetters` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Every event the platform gave up on, and the act that puts it back. A dead letter is work the platform accepted and did not do.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Consumer",
       "operation": "listDeadLetters",
       "notes": "Sends `?consumer=` to `listDeadLetters`.",
       "provenance": "contract platform-ops.yaml GET /dead-letters"
      },
      {
       "kind": "datePicker",
       "label": "Since",
       "operation": "listDeadLetters",
       "notes": "Sends `?since=` to `listDeadLetters`.",
       "provenance": "contract platform-ops.yaml GET /dead-letters"
      },
      {
       "kind": "dataTable",
       "label": "Every dead letter",
       "bindsTo": "DeadLetter",
       "columns": [
        "DeadLetter.id",
        "DeadLetter.outboxId",
        "DeadLetter.eventName",
        "DeadLetter.consumer",
        "DeadLetter.payload",
        "DeadLetter.attempts",
        "DeadLetter.lastError",
        "DeadLetter.lastAttemptAt",
        "DeadLetter.replayCount",
        "DeadLetter.scopePath"
       ],
       "operation": "listDeadLetters",
       "provenance": "contract platform-ops.yaml GET /dead-letters"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dead letter",
       "bindsTo": "DeadLetter",
       "columns": [
        "DeadLetter.id",
        "DeadLetter.outboxId",
        "DeadLetter.eventName",
        "DeadLetter.consumer",
        "DeadLetter.payload",
        "DeadLetter.attempts",
        "DeadLetter.lastError",
        "DeadLetter.lastAttemptAt",
        "DeadLetter.replayCount",
        "DeadLetter.scopePath"
       ],
       "operation": "listDeadLetters",
       "provenance": "contract platform-ops.yaml GET /dead-letters"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Replay dead letter",
       "operation": "replayDeadLetter",
       "provenance": "contract platform-ops.yaml POST /dead-letters/{deadLetterId}/replay"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dead letters list.",
   "error": "Could not load. Names which read failed and leaves the dead letters untouched.",
   "emptyFirstRun": "No dead letters yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on consumer, since and the dead letters are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listDeadLetters` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDeadLetters",
    "contract": "platform-ops",
    "purpose": "Events the retry path gave up on",
    "trigger": "onLoad"
   },
   {
    "operationId": "replayDeadLetter",
    "contract": "platform-ops",
    "purpose": "Put one back on the queue",
    "trigger": "onAction",
    "invalidates": [
     "listDeadLetters"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "deadLetterId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**The ordinary path is a row on this screen**, and `replayDeadLetter` takes the id from the row the operator chose. A deep link is how an alert reaches one directly; if that id is already replayed or gone the screen says so and shows the list, because a replay issued against a row nobody can see is a replay nobody can account for.",
   "preloaded": [
    "DeadLetter.id",
    "DeadLetter.outboxId",
    "DeadLetter.eventName",
    "DeadLetter.consumer",
    "DeadLetter.payload"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-318"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
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
 "listDeadLetters": {
  "method": "GET",
  "path": "/dead-letters",
  "contract": "platform-ops",
  "summary": "Undeliverable events",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "consumer",
    "in": "query",
    "required": null
   },
   {
    "name": "since",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DeadLetter"
 },
 "replayDeadLetter": {
  "method": "POST",
  "path": "/dead-letters/{deadLetterId}/replay",
  "contract": "platform-ops",
  "summary": "Re-enter the delivery path",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "deadLetterId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DeadLetter"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "DeadLetter": {
  "x-ticvai-append-only": "createdAt",
  "type": "object",
  "x-ticvai-persistence": "platform.dead_letter",
  "description": "ADR-0033. **An outbox row whose delivery failed after its retry budget.**\n\n**A financial posting is never dead-lettered** — `ledger.journal_entry` is append-only and a failed posting is an incident. **Nor is a DSAR**: `platform.dsar_request` carries a legal clock, and a dead-lettered erasure nobody works is a regulatory failure with a timestamp on it. Both halt and alert.",
  "required": [
   "id"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "outboxId": {
    "type": "string",
    "format": "uuid",
    "description": "The row that would not deliver."
   },
   "eventName": {
    "type": "string"
   },
   "consumer": {
    "type": "string",
    "description": "Which consumer failed. **A dead letter you cannot attribute is a log entry with a table’s overhead.**"
   },
   "payload": {
    "type": "object",
    "description": "The event as it was written. **Replay needs the payload, not a reference to a row that may have moved on.**"
   },
   "attempts": {
    "type": "integer",
    "description": "**Five, exponential from one second, jittered** (ADR-0033). Jitter because a thousand failures at the same instant retry at the same instant."
   },
   "lastError": {
    "type": "string"
   },
   "lastAttemptAt": {
    "type": "string",
    "format": "date-time"
   },
   "replayCount": {
    "type": "integer",
    "default": 0,
    "description": "**A replay is a new attempt, not a reset.** An operator retrying the same poison message forty times should be able to see that they did."
   },
   "scopePath": {
    "type": "string"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 }
}
```
