# P09-platform-ops-01 — P09 · Platform Ops

**1 screens · 6 operations · 4 schemas · 2 permissions**

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
| `ADM-318` | Dead Letters | listDetail | 6 | 2 | — |

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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-318 holds none of them. The edge carries nothing: ADM-001 finds challengeId (createMfaChallenge), methodId (enrolMfaMethod) itself, and ADM-001 opens on its own"
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
    },
    {
     "name": "republishes",
     "slot": "collection",
     "notes": "**Republish from the outbox** (ADR-0058, amended 1 October). Here until it has a screen of its own: after a broker loss or a DR failover the messages the broker held are gone, and the dead letters are where an operator is already looking when that happens.",
     "components": [
      {
       "kind": "selectField",
       "label": "Republish status",
       "operation": "listOutboxRepublishes",
       "notes": "Sends `?status=` to `listOutboxRepublishes`.",
       "provenance": "contract platform-ops.yaml GET /outbox-republishes"
      },
      {
       "kind": "textField",
       "label": "Tenant",
       "operation": "listOutboxRepublishes",
       "notes": "Sends `?tenantId=` to `listOutboxRepublishes`.",
       "provenance": "contract platform-ops.yaml GET /outbox-republishes"
      },
      {
       "kind": "dataTable",
       "label": "Outbox republishes, newest first",
       "bindsTo": "OutboxRepublish",
       "columns": [
        "OutboxRepublish.tenantId",
        "OutboxRepublish.from",
        "OutboxRepublish.to",
        "OutboxRepublish.eventNames",
        "OutboxRepublish.status",
        "OutboxRepublish.cursorAt",
        "OutboxRepublish.rowsPublished",
        "OutboxRepublish.requestedBy",
        "OutboxRepublish.requestedAt"
       ],
       "operation": "listOutboxRepublishes",
       "provenance": "contract platform-ops.yaml GET /outbox-republishes"
      }
     ]
    },
    {
     "name": "republishDetail",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected republish and its progress",
       "bindsTo": "OutboxRepublish",
       "columns": [
        "OutboxRepublish.id",
        "OutboxRepublish.tenantId",
        "OutboxRepublish.from",
        "OutboxRepublish.to",
        "OutboxRepublish.eventNames",
        "OutboxRepublish.reason",
        "OutboxRepublish.status",
        "OutboxRepublish.cursorAt",
        "OutboxRepublish.rowsPublished",
        "OutboxRepublish.lastError",
        "OutboxRepublish.requestedBy",
        "OutboxRepublish.requestedAt",
        "OutboxRepublish.startedAt",
        "OutboxRepublish.finishedAt"
       ],
       "operation": "getOutboxRepublish",
       "notes": "Refetched while the republish is `queued` or `running`, so `cursorAt` and `rowsPublished` move.",
       "provenance": "contract platform-ops.yaml GET /outbox-republishes/{republishId}"
      }
     ]
    },
    {
     "name": "republishActions",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Republish from the outbox",
       "operation": "republishOutbox",
       "permission": "PLATFORM_CELL_MANAGE",
       "notes": "Opens `formRepublishOutbox`.",
       "provenance": "contract platform-ops.yaml POST /outbox-republishes"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel republish",
       "operation": "cancelOutboxRepublish",
       "permission": "PLATFORM_CELL_MANAGE",
       "notes": "Only on a `queued` or `running` republish. Opens `confirmCancelOutboxRepublish`.",
       "provenance": "contract platform-ops.yaml POST /outbox-republishes/{republishId}/cancel"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formRepublishOutbox",
    "component": "modal",
    "trigger": "Republish from the outbox",
    "body": "**Collects what `republishOutbox` sends before it is called.** Required: `tenantId`, `from`, `to` (`from` before `to`, `to` no later than now) and `reason` (up to 500 characters). Optional: `eventNames`, catalogue names; empty means every event. **Says how to choose `from`**: when the oldest message the lost broker still held was published; if unknown, the time of the loss minus one hour, or the start of any consumer halt then in progress, whichever is earlier. Too early costs duplicates the inboxes skip; too late loses events. A `409` names the republish the tenant already has; a `422` names the oldest `from` the hot outbox still holds. Dismissing sends nothing.",
    "confirm": {
     "label": "Republish",
     "operation": "republishOutbox"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tenantId",
      "from",
      "to",
      "eventNames",
      "reason"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /outbox-republishes"
   },
   {
    "id": "confirmCancelOutboxRepublish",
    "component": "confirmDialog",
    "trigger": "Cancel republish",
    "body": "**Names the tenant, the range and how far it has got** (`cursorAt`, `rowsPublished`). The relay stops after the batch in flight and keeps the cursor, so a new request can start where this one stopped. A republish that has already finished is refused `409` `republish-finished`.",
    "confirm": {
     "label": "Cancel republish",
     "operation": "cancelOutboxRepublish"
    },
    "provenance": "contract platform-ops.yaml POST /outbox-republishes/{republishId}/cancel"
   }
  ],
  "states": {
   "loading": "The dead letters list.",
   "error": "Could not load. Names which read failed and leaves the dead letters untouched.",
   "emptyFirstRun": "No dead letters yet. **Offers no create action for them** — this screen declares no operation that makes one — and says so rather than showing an empty table. The republish list below it keeps its own action, `republishOutbox`.",
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
   },
   {
    "operationId": "listOutboxRepublishes",
    "contract": "platform-ops",
    "purpose": "Every outbox republish asked for, newest first, with how far each has got",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOutboxRepublish",
    "contract": "platform-ops",
    "purpose": "Follow one republish while it runs",
    "trigger": "onAction"
   },
   {
    "operationId": "republishOutbox",
    "contract": "platform-ops",
    "purpose": "Send one tenant database's outbox rows for a time range to the broker again",
    "trigger": "onAction",
    "invalidates": [
     "listOutboxRepublishes"
    ]
   },
   {
    "operationId": "cancelOutboxRepublish",
    "contract": "platform-ops",
    "purpose": "Stop a republish after its current batch, keeping the cursor",
    "trigger": "onAction",
    "invalidates": [
     "listOutboxRepublishes",
     "getOutboxRepublish"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "deadLetterId",
     "from": "deepLink"
    },
    {
     "name": "republishId",
     "from": "navigation"
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
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen. The four outbox republish operations (ADR-0058, amended 1 October) were added on 1 October 2026 and sit here until republish has a screen of its own.",
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
 "cancelOutboxRepublish": {
  "method": "POST",
  "path": "/outbox-republishes/{republishId}/cancel",
  "contract": "platform-ops",
  "summary": "Stop a republish after its current batch",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OutboxRepublish"
 },
 "getOutboxRepublish": {
  "method": "GET",
  "path": "/outbox-republishes/{republishId}",
  "contract": "platform-ops",
  "summary": "One republish and its progress",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "platform",
  "parameters": [],
  "requestBody": null,
  "responds": "OutboxRepublish"
 },
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
 "listOutboxRepublishes": {
  "method": "GET",
  "path": "/outbox-republishes",
  "contract": "platform-ops",
  "summary": "Outbox republishes, newest first",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "tenantId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
 },
 "republishOutbox": {
  "method": "POST",
  "path": "/outbox-republishes",
  "contract": "platform-ops",
  "summary": "Republish one tenant database's outbox rows for a time range",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "OutboxRepublishRequest",
  "responds": null
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
 },
 "OutboxRepublish": {
  "type": "object",
  "x-ticvai-persistence": "control.outbox_republish",
  "description": "**One republish of a tenant database's outbox** (ADR-0058, amended 1 October). A job row in the regional control database beside the relay lease table `control.outbox_relay`. The relay loop holding the tenant's lease carries it out, alternating one republish batch with each live batch, and moves `cursorAt` as it goes. **At most one `queued` or `running` per tenant.** A cancelled or failed job keeps its cursor, so a new request can start where it stopped. The rows republished keep their `published_at`.",
  "required": [
   "id",
   "tenantId",
   "from",
   "to",
   "reason",
   "status",
   "rowsPublished",
   "requestedBy",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "tenantId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "control.tenant",
    "description": "The tenant whose database's outbox is republished."
   },
   "from": {
    "type": "string",
    "format": "date-time",
    "x-ticvai-column": "range_starts_at",
    "description": "Inclusive start of the outbox `created_at` range."
   },
   "to": {
    "type": "string",
    "format": "date-time",
    "x-ticvai-column": "range_ends_at",
    "description": "Exclusive end of the outbox `created_at` range."
   },
   "eventNames": {
    "type": "array",
    "nullable": true,
    "description": "The event names asked for; null means every event.",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "queued",
     "running",
     "completed",
     "failed",
     "cancelled"
    ],
    "description": "`queued` until the lease holder picks it up; `completed` when the cursor reaches `to`; `failed` with `lastError` after the relay's retry budget; `cancelled` by `cancelOutboxRepublish`."
   },
   "cursorAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "How far it has got, the `created_at` of the last row published (with the row id as the keyset tiebreak, held by the relay). Null until the first batch."
   },
   "rowsPublished": {
    "type": "integer",
    "minimum": 0,
    "default": 0,
    "readOnly": true
   },
   "lastError": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "requestedBy": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-column": "requested_by_principal_id",
    "description": "The staff principal who asked."
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "finishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "Set on `completed`, `failed` or `cancelled`."
   }
  }
 },
 "OutboxRepublishRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request body",
  "description": "**What a person asks to republish** (ADR-0058, amended 1 October). One tenant database, a half-open range of `created_at`, optionally some event names, and why.",
  "required": [
   "tenantId",
   "from",
   "to",
   "reason"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid",
    "description": "The tenant whose database's outbox is read (`control.tenant`)."
   },
   "from": {
    "type": "string",
    "format": "date-time",
    "description": "Inclusive. **Early enough**: when the oldest message still held by the lost broker was published; when unknown, the time of the loss minus one hour, or the start of any consumer halt then in progress, whichever is earlier. Must be before `to`."
   },
   "to": {
    "type": "string",
    "format": "date-time",
    "description": "Exclusive. No later than now; after a DR failover, the time of the request."
   },
   "eventNames": {
    "type": "array",
    "description": "Catalogue event names (`events/`) to republish; absent means every event. An unknown name is the shared `400` `validation`.",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "description": "Why, for the audit trail (e.g. \"broker rebuilt after DR failover to the secondary region\")."
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
 }
}
```
