# P09-ai-01 — P09 · AI

**1 screens · 14 operations · 15 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, AI_USE, PLATFORM_AI_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-037` | AI Provider & Credentials | listDetail | 14 | 3 | — |

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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-037 holds none of them, so the edge carries nothing and ADM-001 opens cold"
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
  "notes": "Added 17 August. **The key is entered once and never returned** — the screen shows a reference, a rotation date and a last-verified date, never a secret. Test before activate. **Not on the wireframe board.**\n\n**Per tenant, not per region (decided 28 September, audit R203).** Platform staff pick a tenant, open a platform-staff grant into it (audit R098), and set that tenant's provider with `setAiProvider` (`PLATFORM_TENANT_MANAGE`, read from the operator's own token; the open grant ties the change to the tenant's audit); the region only restricts the choice. The screen shows the tenant's region's residency restriction before the form, and a provider whose `residency` is outside it is refused `409 residency-refused`, which the form shows against the residency field.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAiProviders` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Configure which model a tenant uses, within what its region allows, hold the key, and prove it works before anyone relies on it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "publishGate",
       "impliedBy": "publishPromptTemplate",
       "notes": "Declares `publishPromptTemplate`. **The gate names what the publish will affect before it happens**: which tenants, venues or capabilities take the new version, and that the previous one stays available to roll back to.",
       "provenance": "check-screens publish rule, 29 September 2026"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status",
        "Tenant.regionId"
       ],
       "operation": "listTenants",
       "notes": "The provider is set per tenant (decided 28 September, audit R203); the list below is the picked tenant's providers.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "Open grant into this tenant",
       "bindsTo": "PlatformStaffGrant",
       "columns": [
        "PlatformStaffGrant.id",
        "PlatformStaffGrant.permissions",
        "PlatformStaffGrant.reason",
        "PlatformStaffGrant.expiresAt"
       ],
       "operation": "listOwnPlatformStaffGrants",
       "notes": "**Always visible while the screen acts on a tenant** (decided 28 September, audit R098, R203). `setAiProvider` is checked against the operator's own `PLATFORM_TENANT_MANAGE`, and in addition needs a grant into the tenant open, so the change is audited against it; reading the providers and the region needs the grant to carry `AI_CONFIGURE` and `SCOPE_VIEW`. Found after a reload with `listOwnPlatformStaffGrants`.",
       "provenance": "contract identity.yaml GET /platform-staff-grants/mine"
      },
      {
       "kind": "primaryButton",
       "label": "Open access grant",
       "operation": "openPlatformStaffGrant",
       "notes": "Shown until a grant into the picked tenant is open; asks for the second factor first (step-up, audit R135).",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "banner",
       "label": "Region residency restriction",
       "bindsTo": "RegionSettings.allowedAiResidencies",
       "operation": "getRegionSettings",
       "notes": "Names the residencies the picked tenant's home region allows for AI processing (`RegionSettings.allowedAiResidencies`; empty means no restriction), and says that `setAiProvider` refuses any other residency with 409 `residency-refused` (decided 28 September, audit R203). The region is `Tenant.regionId`, read with `getRegionSettings`; a tenant with no region yet shows the 409 rule only.",
       "provenance": "contract tenancy.yaml GET /regions/{regionId}/settings"
      },
      {
       "kind": "dataTable",
       "label": "Every AI provider",
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
       "label": "The selected AI provider",
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
      },
      {
       "kind": "detailPanel",
       "label": "Tasks and model fit",
       "bindsTo": "AiProvider",
       "columns": [
        "AiProvider.taskKeys",
        "AiProvider.fitnessWarnings",
        "AiProvider.managedBy",
        "AiProvider.modelId"
       ],
       "operation": "listAiProviders",
       "notes": "**One managed provider by default (AI-D02)**, with a small and a stronger model per agent task; a second provider or a tenant key only where TICVAI enabled it (AI-D14). `taskKeys` binds a provider to named agent tasks (M21-03). **Fitness warnings are shown, never blocking** (M21-09): a model below a task's floor is underpowered, one far above its ceiling is overpowered.",
       "provenance": "29 September pass (P29 group A)"
      },
      {
       "kind": "banner",
       "label": "Model fit warning",
       "operation": "setAiProvider",
       "notes": "Shown after `setAiProvider` returns `fitnessWarnings`: names the task, the score and the band.",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save AI provider",
       "operation": "setAiProvider",
       "provenance": "contract ai.yaml PUT /providers"
      },
      {
       "kind": "secondaryButton",
       "label": "Save AI credential",
       "operation": "setAiCredential",
       "provenance": "contract ai.yaml PUT /ai-providers/{providerId}/credential"
      },
      {
       "kind": "secondaryButton",
       "label": "Test AI provider",
       "operation": "testAiProvider",
       "provenance": "contract ai.yaml POST /ai-providers/{providerId}/test"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The provider credentials list.",
   "error": "Could not load. Names which read failed and leaves the provider credentials untouched.",
   "emptyFirstRun": "No provider credentials yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listAiProviders` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `AI_CONFIGURE`, which `listAiProviders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "grantRequired": "**No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so the provider list and every action are disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098, R203)."
  },
  "apis": [
   {
    "operationId": "listAiProviders",
    "contract": "ai",
    "purpose": "Configured providers and their order",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "The tenant picker — the provider is a per-tenant setting (audit R203)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getRegionSettings",
    "contract": "tenancy",
    "purpose": "The picked tenant's region's allowed AI residencies, for the restriction banner (audit R203)",
    "trigger": "onAction"
   },
   {
    "operationId": "listOwnPlatformStaffGrants",
    "contract": "identity",
    "purpose": "Find a grant into the picked tenant already open, after a reload (audit R098)",
    "trigger": "onAction"
   },
   {
    "operationId": "openPlatformStaffGrant",
    "contract": "identity",
    "purpose": "Open a time-boxed, audited platform-staff grant into the picked tenant before setting its provider; the tenant sees it (decided 28 September, audit R098, R203)",
    "trigger": "onAction",
    "invalidates": [
     "listOwnPlatformStaffGrants"
    ]
   },
   {
    "operationId": "setAiProvider",
    "contract": "ai",
    "purpose": "Configure the picked tenant's provider, per tenant with the region's compliance gate — 409 residency-refused (decided 28 September, audit R203)",
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
   },
   {
    "operationId": "listAiModels",
    "contract": "ai",
    "purpose": "The model catalogue",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setAiModel",
    "contract": "ai",
    "purpose": "Add or change a platform model (platform)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listPromptTemplates",
    "contract": "ai",
    "purpose": "The prompt registry",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "publishPromptTemplate",
    "contract": "ai",
    "purpose": "Publish a prompt template version",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setAiByokEnablement",
    "contract": "ai",
    "purpose": "Enable or disable bring-your-own-key for a tenant (platform)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAiByokEnablement",
    "contract": "ai",
    "purpose": "Whether a tenant may bring its own key",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "providerId",
     "from": "deepLink"
    },
    {
     "name": "regionId",
     "from": "navigation",
     "optional": true
    },
    {
     "name": "modelId",
     "from": "navigation"
    },
    {
     "name": "templateKey",
     "from": "navigation"
    },
    {
     "name": "tenantId",
     "from": "session"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `providerId`. `regionId` is not carried in: it is the picked tenant's `Tenant.regionId`, read from `listTenants` once a tenant is chosen, and feeds `getRegionSettings` for the residency banner (audit R203).",
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
  "overlays": [
   {
    "id": "formOpenPlatformStaffGrant",
    "component": "modal",
    "trigger": "Open access grant",
    "body": "**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client ULID), `permissions` (tenant permissions only; `AI_CONFIGURE` and `SCOPE_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Open access grant",
     "operation": "openPlatformStaffGrant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permissions",
      "reason",
      "ticketRef",
      "expiresAt"
     ]
    },
    "provenance": "contract identity.yaml POST /platform-staff-grants"
   },
   {
    "id": "formSetAiProvider",
    "component": "modal",
    "trigger": "Save AI provider",
    "body": "**Collects what `setAiProvider` sends before it is called.** Required: `kind`, `capability`, `priority`, `isActive`. Optional: `id`, `model`, `failoverProviderId`, `degradeGracefully`, `scopeLevel`, `scopePath`, `credentialRef`, `credentialRotatedAt`, `credentialExpiresAt`, `lastVerifiedAt`, `endpoint`, `residency` and 1 more. **Set for the picked tenant**; a `residency` outside what the tenant's region allows is refused `409 residency-refused` and shown against that field (decided 28 September, audit R203). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AiProvider",
    "confirm": {
     "label": "Save AI provider",
     "operation": "setAiProvider"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "capability",
      "priority",
      "isActive",
      "id",
      "model",
      "failoverProviderId",
      "degradeGracefully",
      "scopeLevel",
      "scopePath",
      "credentialRef",
      "credentialRotatedAt",
      "credentialExpiresAt",
      "lastVerifiedAt",
      "endpoint",
      "residency",
      "maxTokens"
     ]
    },
    "provenance": "contract ai.yaml PUT /providers"
   },
   {
    "id": "formSetAiCredential",
    "component": "modal",
    "trigger": "Save AI credential",
    "body": "**Collects what `setAiCredential` sends before it is called.** Required: `secret`. Optional: `expiresAt`, `graceMinutes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save AI credential",
     "operation": "setAiCredential"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "secret",
      "expiresAt",
      "graceMinutes"
     ]
    },
    "provenance": "contract ai.yaml PUT /ai-providers/{providerId}/credential"
   }
  ],
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
 "getAiByokEnablement": {
  "method": "GET",
  "path": "/tenants/{tenantId}/byok",
  "contract": "ai",
  "summary": "Whether a tenant may bring its own key",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AiByokEnablement"
 },
 "getRegionSettings": {
  "method": "GET",
  "path": "/regions/{regionId}/settings",
  "contract": "tenancy",
  "summary": "Read region settings",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "RegionSettings"
 },
 "listAiModels": {
  "method": "GET",
  "path": "/models",
  "contract": "ai",
  "summary": "The model catalogue",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "layer",
    "in": "query",
    "required": null
   },
   {
    "name": "producerType",
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
 "listAiProviders": {
  "method": "GET",
  "path": "/providers",
  "contract": "ai",
  "summary": "Configured providers and their order",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AiProvider"
 },
 "listOwnPlatformStaffGrants": {
  "method": "GET",
  "path": "/platform-staff-grants/mine",
  "contract": "identity",
  "summary": "The calling platform operator's own grants into this tenant",
  "permission": "PLATFORM_TENANT_ACCESS",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "activeOnly",
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
 "listPromptTemplates": {
  "method": "GET",
  "path": "/prompt-templates",
  "contract": "ai",
  "summary": "The prompt registry",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "task",
    "in": "query",
    "required": null
   },
   {
    "name": "layer",
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
 "listTenants": {
  "method": "GET",
  "path": "/tenants",
  "contract": "subscription",
  "summary": "List tenants",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "planId",
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
 "openPlatformStaffGrant": {
  "method": "POST",
  "path": "/platform-staff-grants",
  "contract": "identity",
  "summary": "A platform operator opens a time-boxed grant into this tenant",
  "permission": "PLATFORM_TENANT_ACCESS",
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
  "responds": "PlatformStaffGrant"
 },
 "publishPromptTemplate": {
  "method": "POST",
  "path": "/prompt-templates/{templateKey}/versions",
  "contract": "ai",
  "summary": "Publish a prompt template version",
  "permission": "AI_APPROVE",
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
  "responds": "AiPromptTemplate"
 },
 "setAiByokEnablement": {
  "method": "PUT",
  "path": "/tenants/{tenantId}/byok",
  "contract": "ai",
  "summary": "Enable or disable bring-your-own-key for a tenant (platform)",
  "permission": "PLATFORM_AI_MANAGE",
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
  "requestBody": "AiByokEnablement",
  "responds": "AiByokEnablement"
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
 "setAiModel": {
  "method": "PUT",
  "path": "/models/{modelId}",
  "contract": "ai",
  "summary": "Add or change a platform model (platform)",
  "permission": "PLATFORM_AI_MANAGE",
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
  "requestBody": "AiModel",
  "responds": "AiModel"
 },
 "setAiProvider": {
  "method": "PUT",
  "path": "/providers",
  "contract": "ai",
  "summary": "Configure a provider",
  "permission": "PLATFORM_TENANT_MANAGE",
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
 "AiByokEnablement": {
  "type": "object",
  "x-ticvai-persistence": "ai.byok_enablement",
  "description": "**Whether a tenant may bring its own model key** (decided 29 September, design 8 on 5.9). TICVAI decides it per tenant with `PLATFORM_AI_MANAGE`; it is not tenant self-service. Until it is enabled, `setAiProvider` refuses `managedBy: tenant`. One row per tenant.",
  "required": [
   "tenantId",
   "enabled"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "enabled": {
    "type": "boolean"
   },
   "coverage": {
    "type": "string",
    "enum": [
     "perTask",
     "allTasks"
    ],
    "default": "perTask",
    "description": "Whether the tenant may supply a key per task or one key for everything."
   },
   "allowedTasks": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Where `coverage` is `perTask`: the gateway tasks a tenant key may serve. Empty means any."
   },
   "reason": {
    "type": "string",
    "maxLength": 1000
   },
   "platformStaffGrantId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The open platform-staff grant the change was made under (audit R098)."
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
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
 "AiModel": {
  "type": "object",
  "x-ticvai-persistence": "ai.model",
  "description": "**The model catalogue** (design 3.1 Registry, 3.3; AIC-013, AIC-026). One row per model a task can be routed to: large language models, embedding and reranking models, and classical models (LightGBM, statistical forecasters) registered the same way so lifecycle, release and audit are uniform. **Platform rows** are mastered in the control plane and replicated read-only into each tenant database with the tenant root as `scopePath`; a tenant row exists only where bring-your-own-key is enabled for the tenant.",
  "required": [
   "layer",
   "modelName",
   "producerType"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "layer": {
    "type": "string",
    "enum": [
     "platform",
     "tenant"
    ]
   },
   "providerKind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiProviderKind"
     }
    ],
    "nullable": true
   },
   "producerType": {
    "type": "string",
    "enum": [
     "llm",
     "embedding",
     "reranker",
     "classical",
     "rule"
    ]
   },
   "modelName": {
    "type": "string",
    "description": "The deployment or model name as the provider knows it, or the package and version for a classical model."
   },
   "capabilities": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiCapability"
    }
   },
   "contextTokens": {
    "type": "integer",
    "nullable": true
   },
   "toolCalling": {
    "type": "boolean",
    "default": false
   },
   "structuredOutput": {
    "type": "boolean",
    "default": false
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "residency": {
    "type": "string",
    "nullable": true,
    "description": "Where inference happens. Checked against `tenancy.RegionSettings.allowedAiResidencies`."
   },
   "inputCostPerMillionTokens": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "outputCostPerMillionTokens": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "lifecycle": {
    "type": "object",
    "description": "Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.",
    "properties": {
     "development": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     },
     "staging": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     },
     "production": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     }
    }
   },
   "isDefaultForTasks": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Tasks this model is the default for (AIC-010), e.g. `assistant.guest.answer`, `config.extract`."
   },
   "taskFitness": {
    "type": "array",
    "readOnly": true,
    "description": "**Evaluated fitness per task** (21 September minutes, M21-09, our proposal): a score from the task's golden set (`runAiEvaluation`) and the band the task needs. Below `floor` the model is underpowered for the task; far above `ceiling` it is overpowered (it costs more than the task needs). `setAiProvider` returns a warning (`AiProvider.fitnessWarnings`) when a choice falls outside the band, and ADM-037 shows the band beside `setAiModel`; neither refuses on it.",
    "items": {
     "type": "object",
     "required": [
      "taskKey",
      "score"
     ],
     "properties": {
      "taskKey": {
       "type": "string"
      },
      "score": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "floor": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "ceiling": {
       "type": "number",
       "minimum": 0,
       "maximum": 1,
       "nullable": true
      },
      "evaluationRunId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "evaluatedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiPromptTemplate": {
  "type": "object",
  "x-ticvai-persistence": "ai.prompt_template",
  "description": "**The prompt registry** (design 3.1 Registry, AIC-022). Versioned and **immutable once published**: a change is a new version, so every decision record can name the exact template it used. Platform templates are replicated read-only like platform models; a tenant may publish its own variant of a task's template.",
  "required": [
   "templateKey",
   "version",
   "layer",
   "task",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "templateKey": {
    "type": "string"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "layer": {
    "type": "string",
    "enum": [
     "platform",
     "tenant"
    ]
   },
   "task": {
    "type": "string",
    "description": "The gateway task it serves (design 3.3), e.g. `assistant.guest.answer`, `case.summarise`, `guidedChoice.wording`."
   },
   "body": {
    "type": "string",
    "description": "The template text. Stable content first, so the provider's prefix cache applies (ADR-0034)."
   },
   "variables": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "outputSchema": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "JSON Schema the structured output must satisfy, where the task has one."
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "retired"
    ]
   },
   "contentHash": {
    "type": "string",
    "readOnly": true
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
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
    "description": "Assigned on create. Sent to `setAiProvider` to replace that provider; left out to create one."
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
    "description": "**Where this provider configuration applies, and therefore whose token pays for it.** A tenant-scoped provider means that tenant's usage bills against their own key at the provider — **an independent reconciliation source against our own meter**, which is the point of per-tenant tokens rather than one platform key.\n`venue` exists for the case where one venue's volume justifies its own key, or where a venue is billed separately from the rest of its tenant.\n**`tenant` is the decided level** (audit R203, ADR-0009): a tenant's provider is set per tenant, by platform staff on ADM-037. `venue` narrows inside a tenant; `platform` is only the platform's fallback. **No provider is configured per region**: a region restricts the choice through `tenancy.RegionSettings.allowedAiResidencies` and nothing else, and the table's `region_id` is the tenant's home region, recorded so that gate can be re-checked.\n"
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
   },
   "managedBy": {
    "type": "string",
    "enum": [
     "ticvai",
     "tenant"
    ],
    "default": "ticvai",
    "description": "**Who holds the provider account, and so who pays** (AI design 5.9, decided 29 September). `ticvai`: TICVAI-managed, metered per tenant and re-billed per token. `tenant`: bring-your-own-key, accepted only where TICVAI enabled it for the tenant (`setAiByokEnablement`); the tenant pays the provider and TICVAI meters for visibility.\n"
   },
   "modelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.model",
    "description": "The model in the catalogue (`listAiModels`) this provider serves. Null for an older row that names its model only in `model`."
   },
   "taskKeys": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "**Which agent tasks this provider serves** (21 September minutes, M21-03: different agents may use different models chosen for the task). Empty means every task of its `capability`. A task listed on two providers goes to the lower `priority`. **AI-D02 stands:** one managed provider (Azure OpenAI in UAE North) serves every task by default, with a small and a stronger model per task; a second provider or a tenant's own key is added only where TICVAI enables it for the tenant (AI-D14, `setAiByokEnablement`)."
   },
   "fitnessWarnings": {
    "type": "array",
    "readOnly": true,
    "description": "**The model-fitness check at the last write** (21 September minutes, M21-09). For each task in `taskKeys` whose model scores outside the task's band in `AiModel.taskFitness`, or has no score, one warning. A warning never blocks the write; it is shown on ADM-037 and kept so the choice is auditable.",
    "items": {
     "type": "object",
     "properties": {
      "taskKey": {
       "type": "string"
      },
      "score": {
       "type": "number",
       "nullable": true
      },
      "floor": {
       "type": "number"
      },
      "direction": {
       "type": "string",
       "enum": [
        "underpowered",
        "overpowered",
        "unscored"
       ]
      }
     }
    }
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
   "localLlm",
   "openaiCompatible"
  ],
  "description": "`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
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
 },
 "Permission": {
  "type": "string",
  "enum": [
   "SESSION_FORCE_LOGOUT",
   "USER_MANAGE",
   "ROLE_MANAGE",
   "PERMISSION_GRANT",
   "PERMISSION_VIEW",
   "PERMISSION_MANAGE",
   "PLATFORM_TENANT_VIEW",
   "PLATFORM_TENANT_MANAGE",
   "PLATFORM_TENANT_TERMINATE",
   "PLATFORM_PLAN_MANAGE",
   "PLATFORM_CELL_VIEW",
   "PLATFORM_CELL_MANAGE",
   "PLATFORM_BILLING_VIEW",
   "PLATFORM_AI_MANAGE",
   "PLATFORM_BILLING_MANAGE",
   "PLATFORM_RELEASE_VIEW",
   "PLATFORM_RELEASE_MANAGE",
   "PLATFORM_RELEASE_PROMOTE",
   "PLATFORM_MIGRATION_VIEW",
   "PLATFORM_MIGRATION_APPLY",
   "PLATFORM_TENANT_ACCESS",
   "TENANT_CONFIGURE",
   "TENANT_VIEW",
   "TENANT_PUBLISH",
   "SCOPE_VIEW",
   "SCOPE_MANAGE",
   "REGION_CONFIGURE",
   "WORKSTATION_CONFIGURE",
   "PRODUCT_VIEW",
   "PRODUCT_CONFIGURE",
   "PRODUCT_APPROVE",
   "PRODUCT_PUBLISH",
   "PRICE_VIEW",
   "PRICE_CONFIGURE",
   "EVENT_CONFIGURE",
   "PERFORMANCE_CONFIGURE",
   "CAPACITY_CONFIGURE",
   "ORDER_VIEW",
   "ORDER_VIEW_OTHER",
   "ORDER_CREATE",
   "ORDER_MODIFY",
   "ORDER_DISCOUNT",
   "ORDER_CANCEL",
   "ORDER_VOID",
   "ORDER_REFUND",
   "ORDER_REFUND_APPROVE",
   "ORDER_REFUND_BULK",
   "ORDER_EXCHANGE",
   "ORDER_RESCHEDULE",
   "ORDER_REPRINT",
   "PRICE_OVERRIDE",
   "DISCOUNT_APPLY",
   "CREDIT_MANAGE",
   "CREDIT_OVERRIDE",
   "WALLET_VIEW",
   "WALLET_OPERATE",
   "WALLET_CONFIGURE",
   "PAYMENT_VIEW",
   "PAYMENT_CONFIGURE",
   "PAYMENT_PROVIDER_MANAGE",
   "PAYMENT_DISPUTE",
   "SHIFT_OPEN",
   "SHIFT_CLOSE",
   "SHIFT_SUSPEND",
   "SHIFT_CLOSE_OTHER",
   "SHIFT_APPROVE_OPEN",
   "SHIFT_APPROVE_CLOSE",
   "SHIFT_REOPEN",
   "CASH_LIFT",
   "CASH_ADD",
   "CASH_NO_SALE",
   "DEPOSIT_BOX_MODIFY_OWN",
   "DEPOSIT_BOX_MODIFY_OTHER",
   "OVERSHORT_ACCEPT",
   "ACCESS_VALIDATE",
   "ACCESS_OVERRIDE",
   "ACCESS_POINT_CONFIGURE",
   "TURNSTILE_MODE_SET",
   "TICKET_LOOKUP",
   "ACCREDITATION_VIEW",
   "ACCREDITATION_APPLY",
   "ACCREDITATION_APPROVE",
   "ACCREDITATION_ISSUE",
   "ACCREDITATION_MANAGE",
   "ACCREDITATION_CONFIGURE",
   "REPORT_VIEW_OWN",
   "REPORT_VIEW_WORKSTATION",
   "REPORT_VIEW_VENUE",
   "REPORT_VIEW_REGION",
   "REPORT_VIEW_TENANT",
   "REPORT_EXPORT",
   "REPORT_EXPORT_PII",
   "REPORT_MANAGE",
   "REPORT_SCHEDULE",
   "LEDGER_VIEW",
   "LEDGER_POST",
   "LEDGER_APPROVE",
   "TAX_CONFIGURE",
   "ACCOUNT_CONFIGURE",
   "SETTLEMENT_VIEW",
   "SETTLEMENT_RECONCILE",
   "GUEST_VIEW",
   "GUEST_VIEW_PII",
   "GUEST_MANAGE",
   "VENUE_MAP_VIEW",
   "VENUE_MAP_MANAGE",
   "VENUE_MAP_PUBLISH",
   "RESOURCE_VIEW",
   "RESOURCE_BOOK",
   "RESOURCE_MANAGE",
   "RESOURCE_CONFIGURE",
   "RENTAL_VIEW",
   "RENTAL_BOOK",
   "RENTAL_OPERATE",
   "RENTAL_MANAGE",
   "RENTAL_CONFIGURE",
   "RENTAL_PRICE",
   "RENTAL_APPROVE",
   "RENTAL_OVERRIDE",
   "DEVELOPER_VIEW",
   "DEVELOPER_MANAGE",
   "DEVELOPER_ADMIN",
   "LOYALTY_ACCRUE",
   "LOYALTY_REDEEM",
   "LOYALTY_ADJUST",
   "MARKETING_VIEW",
   "MARKETING_MANAGE",
   "MARKETING_SEND",
   "CASE_VIEW",
   "CASE_MANAGE",
   "ASSET_LIBRARY_VIEW",
   "ASSET_LIBRARY_MANAGE",
   "ASSET_LIBRARY_APPROVE",
   "ASSET_LIBRARY_SHARE",
   "QUEUE_VIEW",
   "QUEUE_MANAGE",
   "QUEUE_REDEEM",
   "QUEUE_OVERRIDE",
   "TRANSPORT_VIEW",
   "TRANSPORT_MANAGE",
   "TRANSPORT_PRICE",
   "ASSET_VIEW",
   "ASSET_MANAGE",
   "WORK_ORDER_VIEW",
   "WORK_ORDER_MANAGE",
   "WORK_ORDER_VERIFY",
   "INSPECTION_VIEW",
   "INSPECTION_SUBMIT",
   "INSPECTION_MANAGE",
   "INCIDENT_REPORT",
   "INCIDENT_VIEW",
   "INCIDENT_MANAGE",
   "KIOSK_ATTEND",
   "DEVICE_VIEW",
   "DEVICE_CONFIGURE",
   "DEVICE_MANAGE",
   "APPROVAL_ACT",
   "APPROVAL_DELEGATE",
   "AI_USE",
   "AI_CONFIGURE",
   "AI_APPROVE",
   "AI_AUDIT_VIEW",
   "RISK_REVIEW",
   "RISK_INVESTIGATE",
   "AUDIT_VIEW",
   "APPROVAL_VIEW",
   "APPROVAL_REQUEST",
   "APPROVAL_DECIDE",
   "APPROVAL_CONFIGURE",
   "MAINTENANCE_EXECUTE",
   "MAINTENANCE_APPROVE",
   "WORKFORCE_VIEW",
   "WORKFORCE_MANAGE",
   "ATTENDANCE_RECORD",
   "ANNOUNCEMENT_PUBLISH",
   "ANNOUNCEMENT_EMERGENCY",
   "PARTNER_VIEW",
   "PARTNER_MANAGE",
   "PARKING_CONFIGURE",
   "PAYMENT_VOID",
   "PROCUREMENT_VIEW",
   "PROCUREMENT_REQUEST",
   "PROCUREMENT_MANAGE",
   "PROCUREMENT_RECEIVE"
  ]
 },
 "Placement": {
  "x-ticvai-persistence": "none — embedded in region_settings",
  "type": "object",
  "description": "Read-only here. Set by the Control Plane at provisioning.\nEvery region is its own logical cell. Placement determines the infrastructure backing it, which is how cost is controlled without varying the split rule: `shared` puts several regions' databases on one cluster; `dedicated` and `isolated` give a region its own. Regions in different countries MUST have placements in their respective jurisdictions.\n",
  "readOnly": true,
  "required": [
   "mode"
  ],
  "properties": {
   "mode": {
    "type": "string",
    "enum": [
     "shared",
     "dedicated",
     "isolated",
     "clientHosted"
    ]
   },
   "cellName": {
    "type": "string"
   },
   "cloudRegion": {
    "type": "string"
   }
  }
 },
 "PlatformStaffGrant": {
  "type": "object",
  "x-ticvai-persistence": "identity.platform_staff_grant",
  "description": "**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n",
  "required": [
   "id",
   "operatorPrincipalId",
   "permissions",
   "reason",
   "openedAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The platform operator, from the Control Plane token. Set by the server."
   },
   "operatorDisplayName": {
    "type": "string",
    "readOnly": true
   },
   "permissions": {
    "type": "array",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
    }
   },
   "reason": {
    "type": "string"
   },
   "ticketRef": {
    "type": "string",
    "nullable": true
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant root. **Operations write it at `tenant` scope**; the server sets it."
   }
  }
 },
 "RegionSettings": {
  "x-ticvai-persistence": "platform.region_settings",
  "type": "object",
  "required": [
   "countryCode",
   "currencyCode",
   "currencyScale",
   "timeZone",
   "fiscalYearStartMonth"
  ],
  "properties": {
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "description": "ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell."
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "description": "Decimal places for this region's currency. Varies by currency — some use 2, some use 3. Money columns are numeric(18,4) and carry the scale explicitly, because a fixed 2-place type silently truncates 3-place currencies.\n"
   },
   "timeZone": {
    "type": "string",
    "description": "IANA zone, e.g. `Asia/Dubai`."
   },
   "dateFormat": {
    "type": "string",
    "default": "dd/MM/yyyy"
   },
   "numberFormat": {
    "type": "string",
    "default": "#,##0.00"
   },
   "fiscalYearStartMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 12,
    "description": "Varies by country."
   },
   "allowedAiResidencies": {
    "type": "array",
    "description": "**The region's compliance gate on AI providers** (decided 28 September, audit R203; ADR-0009). The `AiProvider.residency` values a tenant in this region may use; empty means no restriction. `ai.setAiProvider` refuses any other residency with `409 residency-refused`. A prompt carrying guest data that reaches a provider hosted elsewhere is a cross-border transfer, and this is where a region says which it allows.\n",
    "default": [],
    "items": {
     "type": "string"
    }
   },
   "placement": {
    "$ref": "#/components/schemas/Placement"
   },
   "cellName": {
    "type": "string",
    "readOnly": true,
    "description": "The cell serving this region. One cell per tenant per region (ADR-0014).\n"
   }
  }
 },
 "SuspensionMode": {
  "type": "string",
  "description": "Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n",
  "enum": [
   "readOnly",
   "noNewSales",
   "fullLockout"
  ]
 },
 "Tenant": {
  "x-ticvai-persistence": "control.tenant",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "status",
   "createdAt"
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
   "status": {
    "$ref": "#/components/schemas/TenantStatus"
   },
   "suspensionMode": {
    "$ref": "#/components/schemas/SuspensionMode"
   },
   "suspensionReason": {
    "type": "string",
    "nullable": true
   },
   "suspensionEffectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."
   },
   "suspensionNoticeMessage": {
    "$ref": "#/components/schemas/LocalisedText",
    "description": "The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."
   },
   "terminationScheduledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When `terminateTenant` started the retention window. Null when no termination is under way."
   },
   "terminationRetentionUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."
   },
   "terminationReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "terminationRequestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planName": {
    "type": "string",
    "nullable": true
   },
   "cellCount": {
    "type": "integer"
   },
   "venueCount": {
    "type": "integer"
   },
   "regionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"
   },
   "billingEmail": {
    "type": "string"
   },
   "billingAddress": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."
   },
   "accountManagerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "TenantStatus": {
  "type": "string",
  "enum": [
   "onboarding",
   "active",
   "suspended",
   "terminating",
   "terminated"
  ]
 }
}
```
