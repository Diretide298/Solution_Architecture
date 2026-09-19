# P09-ai-01 — P09 · AI

**1 screens · 4 operations · 3 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `AI_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-037` | AI Provider & Credentials | listDetail | 4 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-037",
  "name": "AI Provider & Credentials",
  "module": "AI",
  "requiresModule": "ai",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "ticvai-web",
   "route": "/ai/providers",
   "component": "apps/ticvai-web/src/routes/AiProviderCredentials.tsx",
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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "BO-091",
     "trigger": "AI Policy & Spend",
     "provenance": "flow F100 step 1→2",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Added 17 August. **The key is entered once and never returned** — the screen shows a reference, a rotation date and a last-verified date, never a secret. Test before activate. **Not on the wireframe board.**",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAiProviders` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Configure which model a tenant uses, hold the key, and prove it works before anyone relies on it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every provider credentials",
       "bindsTo": "AiProvider",
       "columns": [
        "AiProvider.id",
        "AiProvider.kind",
        "AiProvider.capability",
        "AiProvider.model",
        "AiProvider.failoverProviderId",
        "AiProvider.degradeGracefully",
        "AiProvider.priority",
        "AiProvider.scopeLevel",
        "AiProvider.scopePath",
        "AiProvider.credentialRef",
        "AiProvider.credentialRotatedAt",
        "AiProvider.credentialExpiresAt"
       ],
       "operation": "listAiProviders",
       "provenance": "contract ai.yaml GET /providers"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected provider credentials",
       "bindsTo": "AiProvider",
       "columns": [
        "AiProvider.id",
        "AiProvider.kind",
        "AiProvider.capability",
        "AiProvider.model",
        "AiProvider.failoverProviderId",
        "AiProvider.degradeGracefully",
        "AiProvider.priority",
        "AiProvider.scopeLevel",
        "AiProvider.scopePath",
        "AiProvider.credentialRef",
        "AiProvider.credentialRotatedAt",
        "AiProvider.credentialExpiresAt",
        "AiProvider.lastVerifiedAt",
        "AiProvider.endpoint",
        "AiProvider.residency",
        "AiProvider.maxTokens"
       ],
       "operation": "listAiProviders",
       "provenance": "contract ai.yaml GET /providers"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setAiProvider",
       "provenance": "contract ai.yaml PUT /providers"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAiCredential",
       "provenance": "contract ai.yaml PUT /ai-providers/{providerId}/credential"
      },
      {
       "kind": "secondaryButton",
       "label": "Test",
       "operation": "testAiProvider",
       "provenance": "contract ai.yaml POST /ai-providers/{providerId}/test"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAiProviders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setAiProvider",
       "label": "Save ai provider",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAiProvider",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The provider credentials list.",
   "error": "Could not load. Names which read failed and leaves the provider credentials untouched.",
   "emptyFirstRun": "No provider credentials yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the provider credentials are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiProviders",
    "contract": "ai",
    "purpose": "Configured providers and their order",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAiProvider",
    "contract": "ai",
    "purpose": "Configure a provider",
    "trigger": "onAction",
    "invalidates": [
     "listAiProviders"
    ]
   },
   {
    "operationId": "setAiCredential",
    "contract": "ai",
    "purpose": "Store or rotate a provider key",
    "trigger": "onAction",
    "invalidates": [
     "listAiProviders"
    ]
   },
   {
    "operationId": "testAiProvider",
    "contract": "ai",
    "purpose": "Check the key works before anyone relies on it",
    "trigger": "onAction",
    "invalidates": [
     "listAiProviders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "providerId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `providerId`.",
   "preloaded": [
    "AiProvider.id",
    "AiProvider.kind",
    "AiProvider.capability",
    "AiProvider.model",
    "AiProvider.failoverProviderId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-037"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "listAiProviders": {
  "method": "GET",
  "path": "/providers",
  "contract": "ai",
  "summary": "Configured providers and their order",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "AiProvider"
 },
 "setAiCredential": {
  "method": "PUT",
  "path": "/ai-providers/{providerId}/credential",
  "contract": "ai",
  "summary": "Store or rotate a provider key",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiProvider"
 },
 "setAiProvider": {
  "method": "PUT",
  "path": "/providers",
  "contract": "ai",
  "summary": "Configure a provider",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AiProvider",
  "responds": "AiProvider"
 },
 "testAiProvider": {
  "method": "POST",
  "path": "/ai-providers/{providerId}/test",
  "contract": "ai",
  "summary": "Check the key works before anyone relies on it",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "AiCapability": {
  "type": "string",
  "description": "What a capability needs, not which provider serves it. This indirection is what makes \"no provider SDK in capability code\" enforceable.\n**`speechToText` and `textToSpeech` added 18 August (BL-164)** — voice added rather than declined. **Speech is the capability where UAE residency is hardest to satisfy**: the major providers run it in fewer regions than text, and a guest speaking into a kiosk is producing personal data in the moment. `AiProvider.residency` already carries the constraint and **speech is the capability most likely to fail it**, which is why it is separate rather than folded into `chat`.\n",
  "enum": [
   "chat",
   "embedding",
   "vision",
   "rerank",
   "speechToText",
   "textToSpeech"
  ]
 },
 "AiProvider": {
  "type": "object",
  "x-ticvai-persistence": "ai.provider",
  "required": [
   "kind",
   "capability",
   "priority",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "capability": {
    "$ref": "#/components/schemas/AiCapability"
   },
   "model": {
    "type": "string"
   },
   "failoverProviderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-151. **A provider outage with no fallback is every AI surface going dark at once**, and the surfaces most likely to be noticed are the guest-facing ones.\n**Failover is declared per capability because a provider is** — a fallback covering chat and not embedding leaves search broken while the concierge works, which reads as a stranger failure than a clean outage.\n"
   },
   "degradeGracefully": {
    "type": "boolean",
    "default": true,
    "description": "**Where no fallback answers, the surface degrades rather than errors.** Semantic search falls back to keyword, the concierge offers a human, a recommendation returns the rule-based set — **an AI feature that returns a 500 is worse than one that quietly becomes ordinary software.**\n"
   },
   "priority": {
    "type": "integer",
    "description": "Failover order (8.4.26). Lower is tried first."
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "platform",
     "tenant",
     "venue"
    ],
    "description": "**Where this provider configuration applies, and therefore whose token pays for it.** A tenant-scoped provider means that tenant's usage bills against their own key at the provider — **an independent reconciliation source against our own meter**, which is the point of per-tenant tokens rather than one platform key.\n`venue` exists for the case where one venue's volume justifies its own key, or where a venue is billed separately from the rest of its tenant.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "Resolved scope node. Nearest ancestor wins (ADR-0018)."
   },
   "tenantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null only where `scopeLevel` is `platform`."
   },
   "credentialRef": {
    "type": "string",
    "description": "A key-vault reference, never the key. A key typed into a form ends up in a screenshot.\n"
   },
   "credentialRotatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "credentialExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Where the provider issues expiring keys. **A key that lapses silently takes the assistant down without an error anyone reads** — the expiry is surfaced so it can be chased before it bites.\n"
   },
   "lastVerifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When `testAiProvider` last confirmed the key works."
   },
   "endpoint": {
    "type": "string",
    "nullable": true
   },
   "residency": {
    "type": "string",
    "description": "Where inference physically happens. **A prompt reaching a provider hosted elsewhere is a cross-border transfer** (ADR-0009), and this field is what makes that auditable rather than assumed.\n"
   },
   "maxTokens": {
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "AiProviderKind": {
  "type": "string",
  "enum": [
   "openai",
   "gemini",
   "anthropic",
   "azureOpenai",
   "localLlm"
  ]
 }
}
```
