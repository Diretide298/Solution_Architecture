# P14-developer-api-01 — P14 · Developer & API

**8 screens · 28 operations · 18 schemas · 3 permissions**

Platform P14 Developer · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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
  `DEVELOPER_ADMIN, DEVELOPER_MANAGE, DEVELOPER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `DEV-001` | API Reference | listDetail | 2 | 0 | — |
| `DEV-002` | Register & Organisation | configEditor | 2 | 1 | — |
| `DEV-003` | Clients & Credentials | listDetail | 6 | 4 | — |
| `DEV-004` | Sandbox | listDetail | 5 | 3 | — |
| `DEV-005` | Webhooks | listDetail | 5 | 2 | — |
| `DEV-006` | Usage & Limits | statusTracker | 2 | 0 | — |
| `DEV-007` | Marketplace Listing | listDetail | 2 | 1 | — |
| `DEV-008` | Programme Administration | configEditor | 7 | 5 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "DEV-001",
  "name": "API Reference",
  "module": "Developer & API",
  "requiresModule": "developerApi",
  "wave": 2,
  "implementation": {
   "app": "developer-portal-web",
   "route": "/developer/reference",
   "component": "apps/developer-portal-web/src/routes/developer/ApiReference.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "DEV-002",
    "DEV-004",
    "DEV-008"
   ],
   "isEntryPoint": true,
   "transitions": [
    {
     "to": "DEV-002",
     "trigger": "They register their organisation",
     "provenance": "flow F27 step 1→2",
     "operation": "listApiVersions"
    },
    {
     "to": "DEV-004",
     "trigger": "Sandbox",
     "provenance": "structural — DEV-001 is P14's home screen and its exits are its launcher"
    },
    {
     "to": "DEV-008",
     "trigger": "Programme Administration",
     "carries": [
      "version"
     ],
     "provenance": "derived — DEV-008 declares entryState.params listingId, requestId, version and DEV-001 holds version, so an edge into it carries them"
    }
   ]
  },
  "notes": "CF-135. **A portal over artefacts that already exist**, which is why this is frontend scope rather than a contract gap — the twelve domain-13 rows left open after the contract landed are all this screen and its siblings. **The API reference.** A developer arrives at the documentation, not at a sign-up form — registration is what they do after reading. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listApiVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Read the contract, and call it without leaving the page.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every API version",
       "bindsTo": "ApiVersion",
       "columns": [
        "ApiVersion.status",
        "ApiVersion.releasedAt",
        "ApiVersion.deprecatedAt",
        "ApiVersion.sunsetAt",
        "ApiVersion.minimumNoticeMonths",
        "ApiVersion.migrationGuideUrl",
        "ApiVersion.activeClientCount"
       ],
       "operation": "listApiVersions",
       "provenance": "contract public-api.yaml GET /api-versions"
      },
      {
       "kind": "detailPanel",
       "bindsTo": "operation",
       "notes": "Request, response, scopes and error codes. **The error codes are what a developer comes back for**, and they are the section most documentation buries.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "codeBlock",
       "notes": "A working example per language. **Copy-paste that runs** — an example with a placeholder token teaches nothing about auth, which is where integrations fail.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Try it",
       "notes": "Runs against the sandbox, never production. **The environment is stated on the button**, because a try-it that quietly hits production is how somebody refunds a real order while reading the docs.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "label": "Changelog for the selected version",
       "bindsTo": "ApiVersion.changes",
       "operation": "listApiVersions",
       "notes": "**Every operation added, changed, deprecated or removed, with breaking changes marked** (17 September minutes, M17-14; ADR-0026).",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected API version",
       "bindsTo": "ApiVersion",
       "columns": [
        "ApiVersion.status",
        "ApiVersion.releasedAt",
        "ApiVersion.deprecatedAt",
        "ApiVersion.sunsetAt",
        "ApiVersion.minimumNoticeMonths",
        "ApiVersion.migrationGuideUrl",
        "ApiVersion.activeClientCount"
       ],
       "operation": "listApiVersions",
       "provenance": "contract public-api.yaml GET /api-versions"
      }
     ]
    },
    {
     "name": "sideNav",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search operations",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "treeNav",
       "bindsTo": "ApiScope",
       "notes": "**Grouped by licensable module, then contract** (17 September minutes, M17-05 and M17-12): a developer sees which operations each module brings and which scope opens them, so a CRM partner reads the CRM operations and knows it will be granted nothing else.",
       "provenance": "carried from the previous definition",
       "operation": "listApiScopes"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operation list; the current version renders first.",
   "error": "Could not load the reference. **Names which contract failed** — 28 files load independently and one missing does not mean the API is down.\n",
   "emptyFirstRun": "**Never empty in practice** — the contracts are the documentation and they ship with the platform. An empty reference means the artefacts did not load, which is an error rather than a first run.\n",
   "emptyNoResults": "No operation matches this search. **Search covers the summary and the description**, not just the operationId, because a developer looking for *\"how do I refund\"* does not know it is called `createRefund`.\n",
   "emptyNoAccess": "Shown when the caller lacks `DEVELOPER_VIEW`, which `listApiVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApiVersions",
    "contract": "public-api",
    "purpose": "Which versions exist and which is current",
    "trigger": "onLoad"
   },
   {
    "operationId": "listApiScopes",
    "contract": "public-api",
    "purpose": "The module scope catalogue the reference is grouped by",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "entryState": {
   "preloaded": [
    "ApiVersion.status",
    "ApiVersion.releasedAt",
    "ApiVersion.deprecatedAt",
    "ApiVersion.sunsetAt",
    "ApiVersion.minimumNoticeMonths"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P14 Developer.dc.html#dev-001"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P14",
   "formFactor": "web",
   "app": "developer-portal-web",
   "operator": "partner",
   "name": "Developer Portal",
   "shortName": "Developer",
   "audience": "partner",
   "offlineCapable": false,
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "DEV-002",
  "name": "Register & Organisation",
  "module": "Developer & API",
  "requiresModule": "developerApi",
  "wave": 2,
  "implementation": {
   "app": "developer-portal-web",
   "route": "/developer/organisation",
   "component": "apps/developer-portal-web/src/routes/developer/OrganisationForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "DEV-001"
   ],
   "exitTo": [
    "DEV-003"
   ],
   "transitions": [
    {
     "to": "DEV-003",
     "trigger": "They create a sandbox client and take the secret",
     "provenance": "flow F27 step 2→3",
     "operation": "registerDeveloper"
    }
   ]
  },
  "notes": "13.1.6 to 13.1.10. **The organisation administers its own people** — Softlabs maintaining every integrator's staff list is Softlabs doing their HR.\n",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`registerDeveloper`, `setDeveloperMembers`) and no read of a population — it is settings, not a list",
  "purpose": "Sign up as an organisation, and manage who at it may do what.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "DeveloperAccount.id",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "textField",
       "label": "organisationName",
       "bindsTo": "DeveloperAccount.organisationName",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "textField",
       "label": "contactEmail",
       "bindsTo": "DeveloperAccount.contactEmail",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "textField",
       "label": "websiteUrl",
       "bindsTo": "DeveloperAccount.websiteUrl",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "textField",
       "label": "countryCode",
       "bindsTo": "DeveloperAccount.countryCode",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "textField",
       "label": "partnerId",
       "bindsTo": "DeveloperAccount.partnerId",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "textField",
       "label": "status",
       "bindsTo": "DeveloperAccount.status",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "textField",
       "label": "verifiedAt",
       "bindsTo": "DeveloperAccount.verifiedAt",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "textField",
       "label": "Organisation name",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Contact email",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "bindsTo": "members",
       "notes": "Role per member — owner, admin, developer, read-only.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Invite",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Register developer",
       "operation": "registerDeveloper",
       "provenance": "contract public-api.yaml POST /developers"
      },
      {
       "kind": "secondaryButton",
       "label": "Save developer members",
       "operation": "setDeveloperMembers",
       "provenance": "contract public-api.yaml PUT /developers/{developerId}/members"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The organisation and its members.",
   "error": "Could not load. Your credentials are unaffected.",
   "emptyFirstRun": "**You are the first member and you are the owner.** An integration outlives the engineer who built it, so this is an organisation rather than a personal account — and the invite action is the point of the state.\n",
   "emptyNoAccess": "**You are a member and not an owner.** Stated plainly rather than shown as an empty list, because a developer who sees no colleagues assumes the page is broken.\n"
  },
  "apis": [
   {
    "operationId": "registerDeveloper",
    "contract": "public-api",
    "purpose": "Register",
    "trigger": "onAction"
   },
   {
    "operationId": "setDeveloperMembers",
    "contract": "public-api",
    "purpose": "Manage members",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "developerId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `developerId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P14 Developer.dc.html#dev-002"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetDeveloperMembers",
    "component": "modal",
    "trigger": "Save developer members",
    "body": "**Collects what `setDeveloperMembers` sends before it is called.** Required: `members`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save developer members",
     "operation": "setDeveloperMembers"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "members"
     ]
    },
    "provenance": "contract public-api.yaml PUT /developers/{developerId}/members"
   }
  ],
  "_platform": {
   "code": "P14",
   "formFactor": "web",
   "app": "developer-portal-web",
   "operator": "partner",
   "name": "Developer Portal",
   "shortName": "Developer",
   "audience": "partner",
   "offlineCapable": false,
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "DEV-003",
  "name": "Clients & Credentials",
  "module": "Developer & API",
  "requiresModule": "developerApi",
  "wave": 2,
  "implementation": {
   "app": "developer-portal-web",
   "route": "/developer/clients",
   "component": "apps/developer-portal-web/src/routes/developer/ClientList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "DEV-002"
   ],
   "exitTo": [
    "DEV-004",
    "DEV-005",
    "DEV-008"
   ],
   "transitions": [
    {
     "to": "DEV-005",
     "trigger": "Webhooks",
     "provenance": "derived — DEV-005 declares entryState.params subscriptionId and DEV-003 holds none of them, so the edge carries nothing and DEV-005 opens cold"
    },
    {
     "to": "DEV-004",
     "trigger": "They provision a sandbox and build against it",
     "provenance": "flow F27 step 3→4",
     "operation": "createApiClient",
     "carries": [
      "clientId"
     ]
    },
    {
     "to": "DEV-008",
     "trigger": "TICVAI decides the request",
     "provenance": "flow F36 step 4→5",
     "operation": "requestProductionAccess",
     "carries": [
      "listingId"
     ]
    }
   ]
  },
  "notes": "CF-135a. **The one credential model** — 2.7.52, 7.1.25 and 7.1.30 each asserted their own. **Rotation carries an overlap window and revocation does not**: one is hygiene, the other is what you reach for when a secret has leaked, and a grace period defeats it.\n",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listApiClients` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Create a client, choose its scopes, and rotate its secret without an outage.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every API client",
       "bindsTo": "ApiClient",
       "columns": [
        "ApiClient.id",
        "ApiClient.developerId",
        "ApiClient.name",
        "ApiClient.clientId",
        "ApiClient.environment",
        "ApiClient.scopes",
        "ApiClient.allowedTenantIds",
        "ApiClient.ipAllowList",
        "ApiClient.status",
        "ApiClient.lastUsedAt"
       ],
       "operation": "listApiClients",
       "provenance": "contract public-api.yaml GET /api-clients"
      },
      {
       "kind": "dataTable",
       "bindsTo": "ApiClient[]",
       "notes": "Environment is a column and not a badge. **A sandbox key and a production key that look alike is how somebody uses the wrong one**, and the difference must survive a glance.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Create client",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "**The secret is shown once.** The banner says so before it is generated, not after — a system that can show you a secret later is a system that stores one.\n **A production client is never created here** (M17-06): it is issued by TICVAI on an approved production access request, and its first secret is taken once with Rotate.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "multiSelect",
       "label": "Scopes, by module",
       "bindsTo": "ApiScope",
       "operation": "listApiScopes",
       "notes": "**A scope picker grouped by module** (M17-05): `{module}.read` and `{module}.write`, with unlicensed modules shown and disabled rather than hidden.",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected API client",
       "bindsTo": "ApiClient",
       "columns": [
        "ApiClient.id",
        "ApiClient.developerId",
        "ApiClient.name",
        "ApiClient.clientId",
        "ApiClient.environment",
        "ApiClient.scopes",
        "ApiClient.allowedTenantIds",
        "ApiClient.ipAllowList",
        "ApiClient.status",
        "ApiClient.lastUsedAt"
       ],
       "operation": "listApiClients",
       "provenance": "contract public-api.yaml GET /api-clients"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create API client",
       "operation": "createApiClient",
       "provenance": "contract public-api.yaml POST /api-clients"
      },
      {
       "kind": "secondaryButton",
       "label": "Rotate API credential",
       "operation": "rotateApiCredential",
       "provenance": "contract public-api.yaml POST /api-clients/{clientId}/credentials"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke API credential",
       "operation": "revokeApiCredential",
       "provenance": "contract public-api.yaml DELETE /api-clients/{clientId}/credentials"
      },
      {
       "kind": "secondaryButton",
       "label": "Request production access",
       "operation": "requestProductionAccess",
       "notes": "**Production keys only after certification** (M17-06). Enabled on a sandbox client whose integration is certified; asks for the tenants, the scopes and the IP allow-list. TICVAI issues the production client.",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRevokeApiCredential",
    "component": "confirmDialog",
    "trigger": "Revoke API credential",
    "body": "**Names what `revokeApiCredential` changes and what it leaves alone**, in the consequence rather than the verb. A clients credentials this affects should be identified in the dialog, not just counted.",
    "provenance": "contract public-api.yaml DELETE /api-clients/{clientId}/credentials"
   },
   {
    "id": "formCreateApiClient",
    "component": "modal",
    "trigger": "Create API client",
    "body": "**Collects what `createApiClient` sends before it is called.** Required: `id`, `developerId`, `name`, `environment`, `scopes`, `status`. Optional: `clientId`, `allowedTenantIds`, `ipAllowList`, `lastUsedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ApiClient",
    "confirm": {
     "label": "Create API client",
     "operation": "createApiClient"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "developerId",
      "name",
      "environment",
      "scopes",
      "status",
      "clientId",
      "allowedTenantIds",
      "ipAllowList",
      "lastUsedAt"
     ]
    },
    "provenance": "contract public-api.yaml POST /api-clients"
   },
   {
    "id": "formRotateApiCredential",
    "component": "modal",
    "trigger": "Rotate API credential",
    "body": "**Collects what `rotateApiCredential` sends before it is called.** Nothing in the body is required. Optional: `overlapHours`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Rotate API credential",
     "operation": "rotateApiCredential"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "overlapHours"
     ]
    },
    "provenance": "contract public-api.yaml POST /api-clients/{clientId}/credentials"
   },
   {
    "id": "formRequestProductionAccess",
    "component": "modal",
    "trigger": "Request production access",
    "body": "**Collects what `requestProductionAccess` sends before it is called.** Required: `listingId` (a certified integration), `scopes`, `allowedTenantIds`, `ipAllowList` (at least one address, M17-07). Optional: `note`. The form says that a new production key is issued and the sandbox key stays a sandbox key.",
    "confirm": {
     "label": "Request production access",
     "operation": "requestProductionAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "listingId",
      "scopes",
      "allowedTenantIds",
      "ipAllowList",
      "note"
     ]
    },
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "states": {
   "loading": "Clients, sandbox first.",
   "error": "Could not load clients. Existing credentials keep working.",
   "emptyFirstRun": "**No clients yet. Create a sandbox one** — the action says sandbox because a first client should never be a production client, and defaulting the other way is how a first API call hits a live venue.\n",
   "emptyNoResults": "No client matches this environment or scope.",
   "emptyNoAccess": "You are a read-only member. Credentials are hidden, not absent."
  },
  "apis": [
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "Clients with their environment and scopes",
    "trigger": "onLoad"
   },
   {
    "operationId": "createApiClient",
    "contract": "public-api",
    "purpose": "Create one",
    "trigger": "onAction",
    "invalidates": [
     "listApiClients"
    ]
   },
   {
    "operationId": "rotateApiCredential",
    "contract": "public-api",
    "purpose": "New secret with an overlap",
    "trigger": "onAction",
    "invalidates": [
     "listApiClients"
    ]
   },
   {
    "operationId": "revokeApiCredential",
    "contract": "public-api",
    "purpose": "Revoke now",
    "trigger": "onAction",
    "invalidates": [
     "listApiClients"
    ]
   },
   {
    "operationId": "listApiScopes",
    "contract": "public-api",
    "purpose": "Scopes to choose from, by module",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "operationId": "requestProductionAccess",
    "contract": "public-api",
    "purpose": "Ask for production keys for a certified integration",
    "trigger": "onAction",
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "clientId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `clientId`.",
   "preloaded": [
    "ApiClient.id",
    "ApiClient.developerId",
    "ApiClient.name",
    "ApiClient.clientId",
    "ApiClient.environment"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P14 Developer.dc.html#dev-003"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P14",
   "formFactor": "web",
   "app": "developer-portal-web",
   "operator": "partner",
   "name": "Developer Portal",
   "shortName": "Developer",
   "audience": "partner",
   "offlineCapable": false,
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "DEV-004",
  "name": "Sandbox",
  "module": "Developer & API",
  "requiresModule": "developerApi",
  "wave": 2,
  "implementation": {
   "app": "developer-portal-web",
   "route": "/developer/sandbox",
   "component": "apps/developer-portal-web/src/routes/developer/SandboxList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "DEV-001",
    "DEV-003"
   ],
   "exitTo": [
    "DEV-005",
    "DEV-007"
   ],
   "transitions": [
    {
     "to": "DEV-005",
     "trigger": "They subscribe to the events they need and watch the deliveries",
     "provenance": "flow F27 step 4→5"
    },
    {
     "to": "DEV-007",
     "trigger": "They submit the integration for certification",
     "provenance": "flow F36 step 1→2",
     "operation": "createSandbox"
    }
   ]
  },
  "notes": "Decisions D2 and D3. **One shared sandbox, synthetic data only** — which removes the PDPL and DESC exposure entirely. Tenant-specific validation runs on per-customer staging.\n",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSandboxes` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Test against synthetic data, and reset to a known state.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every sandbox",
       "bindsTo": "Sandbox",
       "columns": [
        "Sandbox.id",
        "Sandbox.name",
        "Sandbox.developerId",
        "Sandbox.status",
        "Sandbox.dataProfile",
        "Sandbox.containsProductionData",
        "Sandbox.expiresAt",
        "Sandbox.lastResetAt"
       ],
       "operation": "listSandboxes",
       "provenance": "contract public-api.yaml GET /sandboxes"
      },
      {
       "kind": "cardList",
       "bindsTo": "Sandbox[]",
       "notes": "Venue kind, record counts, expiry.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Provision sandbox",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Reset",
       "notes": "Confirms by naming what goes. **\"Reset — 5,000 guests and 12 months of orders will be regenerated\"** rather than \"are you sure\", because a developer mid-test needs to know what they are about to lose.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "**Expiry, counted in days.** A sandbox that vanishes with no warning is a developer who thinks the platform broke.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected sandbox",
       "bindsTo": "Sandbox",
       "columns": [
        "Sandbox.id",
        "Sandbox.name",
        "Sandbox.developerId",
        "Sandbox.status",
        "Sandbox.dataProfile",
        "Sandbox.containsProductionData",
        "Sandbox.expiresAt",
        "Sandbox.lastResetAt"
       ],
       "operation": "listSandboxes",
       "provenance": "contract public-api.yaml GET /sandboxes"
      },
      {
       "kind": "detailPanel",
       "label": "Path to production",
       "bindsTo": "ProductionAccessRequest",
       "operation": "listProductionAccessRequests",
       "notes": "**Sandbox, certification, production** (17 September minutes, M17-06): where this developer stands, the certification and the production access request with its decision.",
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
       "label": "Create sandbox",
       "operation": "createSandbox",
       "provenance": "contract public-api.yaml POST /sandboxes"
      },
      {
       "kind": "destructiveButton",
       "label": "Reset sandbox",
       "operation": "resetSandbox",
       "provenance": "contract public-api.yaml POST /sandboxes/{sandboxId}/reset"
      },
      {
       "kind": "secondaryButton",
       "label": "Promote to production",
       "operation": "requestProductionAccess",
       "notes": "Opens the production access request for the client tested here; disabled until the integration is certified.",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmResetSandbox",
    "component": "confirmDialog",
    "trigger": "Reset sandbox",
    "body": "**Names what `resetSandbox` changes and what it leaves alone**, in the consequence rather than the verb. A sandbox this affects should be identified in the dialog, not just counted.",
    "provenance": "contract public-api.yaml POST /sandboxes/{sandboxId}/reset"
   },
   {
    "id": "formCreateSandbox",
    "component": "modal",
    "trigger": "Create sandbox",
    "body": "**Collects what `createSandbox` sends before it is called.** Required: `name`, `dataProfile`. Optional: `expiresAfterDays`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create sandbox",
     "operation": "createSandbox"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "dataProfile",
      "expiresAfterDays"
     ]
    },
    "provenance": "contract public-api.yaml POST /sandboxes"
   },
   {
    "id": "formRequestProductionAccess",
    "component": "modal",
    "trigger": "Promote to production",
    "body": "**Collects what `requestProductionAccess` sends before it is called.** Required: `listingId`, `scopes`, `allowedTenantIds`, `ipAllowList`. Optional: `note`.",
    "confirm": {
     "label": "Promote to production",
     "operation": "requestProductionAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "listingId",
      "scopes",
      "allowedTenantIds",
      "ipAllowList",
      "note"
     ]
    },
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "states": {
   "loading": "Sandboxes with their data profile.",
   "error": "Could not load. A running sandbox is unaffected.",
   "emptyFirstRun": "**No sandbox yet. Provisioning takes a few minutes and the data is generated, not copied** — no production data is ever cloned or masked into it, which is the decision the whole environment rests on.\n",
   "emptyNoResults": "No sandbox matches.",
   "emptyNoAccess": "You do not have DEVELOPER_MANAGE."
  },
  "apis": [
   {
    "operationId": "listSandboxes",
    "contract": "public-api",
    "purpose": "Sandboxes and their expiry",
    "trigger": "onLoad"
   },
   {
    "operationId": "createSandbox",
    "contract": "public-api",
    "purpose": "Provision one",
    "trigger": "onAction",
    "invalidates": [
     "listSandboxes"
    ]
   },
   {
    "operationId": "resetSandbox",
    "contract": "public-api",
    "purpose": "Back to clean",
    "trigger": "onAction",
    "invalidates": [
     "listSandboxes"
    ]
   },
   {
    "operationId": "listProductionAccessRequests",
    "contract": "public-api",
    "purpose": "The path to production and its state",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "operationId": "requestProductionAccess",
    "contract": "public-api",
    "purpose": "Promote a tested integration to production",
    "trigger": "onAction",
    "invalidates": [
     "listProductionAccessRequests"
    ],
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "sandboxId",
     "from": "deepLink"
    },
    {
     "name": "clientId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `sandboxId`.",
   "preloaded": [
    "Sandbox.id",
    "Sandbox.name",
    "Sandbox.developerId",
    "Sandbox.status",
    "Sandbox.dataProfile"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P14 Developer.dc.html#dev-004"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P14",
   "formFactor": "web",
   "app": "developer-portal-web",
   "operator": "partner",
   "name": "Developer Portal",
   "shortName": "Developer",
   "audience": "partner",
   "offlineCapable": false,
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "DEV-005",
  "name": "Webhooks",
  "module": "Developer & API",
  "requiresModule": "developerApi",
  "wave": 2,
  "implementation": {
   "app": "developer-portal-web",
   "route": "/developer/webhooks",
   "component": "apps/developer-portal-web/src/routes/developer/WebhookList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "DEV-003",
    "DEV-004"
   ],
   "exitTo": [
    "DEV-006"
   ],
   "transitions": [
    {
     "to": "DEV-006",
     "trigger": "They go live (production keys only after certification, flow F36), and watch whether it is healthy",
     "provenance": "flow F27 step 5→6"
    }
   ]
  },
  "notes": "13.1.26 to 13.1.30, 13.3.17 to 13.3.23. **The 29 events already existed and nothing outside could receive one.**\n",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listWebhookSubscriptions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Subscribe to events, see every delivery, and replay what was missed.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "API client",
       "operation": "listWebhookSubscriptions",
       "notes": "Sends `?clientId=` to `listWebhookSubscriptions`. Empty lists every subscription in the tenant; a client narrows it to that client's subscriptions. A partner sees only its own client's whatever it sends (decided 28 September, audit R214 (4)).",
       "provenance": "contract public-api.yaml GET /webhook-subscriptions"
      },
      {
       "kind": "dataTable",
       "label": "Every webhook subscription",
       "bindsTo": "WebhookSubscription",
       "columns": [
        "WebhookSubscription.id",
        "WebhookSubscription.clientId",
        "WebhookSubscription.endpointUrl",
        "WebhookSubscription.eventTypes",
        "WebhookSubscription.filters",
        "WebhookSubscription.signingSecret",
        "WebhookSubscription.status",
        "WebhookSubscription.consecutiveFailures",
        "WebhookSubscription.disabledReason"
       ],
       "operation": "listWebhookSubscriptions",
       "provenance": "contract public-api.yaml GET /webhook-subscriptions"
      },
      {
       "kind": "dataTable",
       "label": "Every webhook delivery",
       "bindsTo": "WebhookDelivery",
       "columns": [
        "WebhookDelivery.id",
        "WebhookDelivery.subscriptionId",
        "WebhookDelivery.eventId",
        "WebhookDelivery.eventType",
        "WebhookDelivery.status",
        "WebhookDelivery.attemptCount",
        "WebhookDelivery.responseCode",
        "WebhookDelivery.responseBodyExcerpt",
        "WebhookDelivery.isReplay",
        "WebhookDelivery.deliveredAt"
       ],
       "operation": "listWebhookDeliveries",
       "provenance": "contract public-api.yaml GET /webhook-subscriptions/{subscriptionId}/deliveries"
      },
      {
       "kind": "dataTable",
       "bindsTo": "WebhookDelivery[]",
       "notes": "Status, attempts, response code and an excerpt of the receiver's own error. **The excerpt is what makes the log useful** — a 500 with their own message in it answers the question without a support conversation.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Replay from…",
       "notes": "Bounded by retention, and the replay is marked in the payload. **A consumer that cannot tell a replay from a live event will double-count.**\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected webhook subscription",
       "bindsTo": "WebhookSubscription",
       "columns": [
        "WebhookSubscription.id",
        "WebhookSubscription.clientId",
        "WebhookSubscription.endpointUrl",
        "WebhookSubscription.eventTypes",
        "WebhookSubscription.filters",
        "WebhookSubscription.signingSecret",
        "WebhookSubscription.status",
        "WebhookSubscription.consecutiveFailures",
        "WebhookSubscription.disabledReason"
       ],
       "operation": "listWebhookSubscriptions",
       "provenance": "contract public-api.yaml GET /webhook-subscriptions"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create webhook subscription",
       "operation": "createWebhookSubscription",
       "provenance": "contract public-api.yaml POST /webhook-subscriptions"
      },
      {
       "kind": "secondaryButton",
       "label": "Replay events",
       "operation": "replayEvents",
       "provenance": "contract public-api.yaml POST /webhook-subscriptions/{subscriptionId}/replay"
      }
     ]
    },
    {
     "name": "sideNav",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "WebhookSubscription[]",
       "notes": "Failing subscriptions sort first and carry the consecutive-failure count. **A developer is told before it is disabled, not after.**\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Subscriptions; failing ones first.",
   "error": "Could not load. Deliveries continue regardless of this screen.",
   "emptyFirstRun": "**No subscriptions. Twenty-nine business events are available** — and the state names a few, because a developer who does not know what exists cannot subscribe to it.\n",
   "emptyNoResults": "No delivery matches this window or status.",
   "emptyNoAccess": "You do not have DEVELOPER_VIEW."
  },
  "apis": [
   {
    "operationId": "listWebhookSubscriptions",
    "contract": "public-api",
    "purpose": "The tenant's webhook subscriptions, filterable by API client (`clientId`, audit R214 (4))",
    "trigger": "onLoad"
   },
   {
    "operationId": "createWebhookSubscription",
    "contract": "public-api",
    "purpose": "Subscribe",
    "trigger": "onAction",
    "invalidates": [
     "listWebhookSubscriptions"
    ]
   },
   {
    "operationId": "listWebhookDeliveries",
    "contract": "public-api",
    "purpose": "The delivery log",
    "trigger": "onAction",
    "invalidates": [
     "listWebhookSubscriptions"
    ]
   },
   {
    "operationId": "replayEvents",
    "contract": "public-api",
    "purpose": "Re-deliver from a point in time",
    "trigger": "onAction",
    "invalidates": [
     "listWebhookSubscriptions"
    ]
   },
   {
    "operationId": "listWebhookEventTypes",
    "contract": "public-api",
    "purpose": "Events a subscription can take",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subscriptionId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `subscriptionId`.",
   "preloaded": [
    "WebhookSubscription.id",
    "WebhookSubscription.clientId",
    "WebhookSubscription.endpointUrl",
    "WebhookSubscription.eventTypes",
    "WebhookSubscription.filters"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P14 Developer.dc.html#dev-005"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateWebhookSubscription",
    "component": "modal",
    "trigger": "Create webhook subscription",
    "body": "**Collects what `createWebhookSubscription` sends before it is called.** Required: `id`, `clientId`, `endpointUrl`, `eventTypes`, `status`. Optional: `filters`, `signingSecret`, `consecutiveFailures`, `disabledReason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "WebhookSubscription",
    "confirm": {
     "label": "Create webhook subscription",
     "operation": "createWebhookSubscription"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "clientId",
      "endpointUrl",
      "eventTypes",
      "status",
      "filters",
      "signingSecret",
      "consecutiveFailures",
      "disabledReason"
     ]
    },
    "provenance": "contract public-api.yaml POST /webhook-subscriptions"
   },
   {
    "id": "formReplayEvents",
    "component": "modal",
    "trigger": "Replay events",
    "body": "**Collects what `replayEvents` sends before it is called.** Required: `from`. Optional: `to`, `eventTypes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Replay events",
     "operation": "replayEvents"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "from",
      "to",
      "eventTypes"
     ]
    },
    "provenance": "contract public-api.yaml POST /webhook-subscriptions/{subscriptionId}/replay"
   }
  ],
  "_platform": {
   "code": "P14",
   "formFactor": "web",
   "app": "developer-portal-web",
   "operator": "partner",
   "name": "Developer Portal",
   "shortName": "Developer",
   "audience": "partner",
   "offlineCapable": false,
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "DEV-006",
  "name": "Usage & Limits",
  "module": "Developer & API",
  "requiresModule": "developerApi",
  "wave": 2,
  "implementation": {
   "app": "developer-portal-web",
   "route": "/developer/usage",
   "component": "apps/developer-portal-web/src/routes/developer/UsageDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "DEV-005"
   ],
   "exitTo": [
    "DEV-001",
    "DEV-007"
   ],
   "transitions": [
    {
     "to": "DEV-007",
     "trigger": "They submit the integration for certification and listing",
     "provenance": "flow F27 step 6→7",
     "operation": "getApiUsage"
    }
   ]
  },
  "notes": "13.1.16 to 13.1.20 and 13.1.41 to 13.1.45. **One screen for five requirements, because they are one question asked five ways.**\n",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getApiUsage` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See whether the integration is healthy, and whose fault it is when it is not.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The API usage",
       "bindsTo": "ApiUsageSummary",
       "columns": [
        "ApiUsageSummary.totalCalls",
        "ApiUsageSummary.successRate",
        "ApiUsageSummary.clientErrorRate",
        "ApiUsageSummary.serverErrorRate",
        "ApiUsageSummary.p50LatencyMs",
        "ApiUsageSummary.p95LatencyMs",
        "ApiUsageSummary.p99LatencyMs",
        "ApiUsageSummary.quotaBreaches",
        "ApiUsageSummary.byOperation"
       ],
       "operation": "getApiUsage",
       "provenance": "contract public-api.yaml GET /api-usage"
      },
      {
       "kind": "metricTile",
       "notes": "Calls, success rate, p95 latency, quota headroom.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "bindsTo": "ApiUsageSummary",
       "notes": "**Client errors and server errors on separate series.** A 4xx is the integrator's problem and a 5xx is ours, and one combined error rate lets both sides blame the other.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "bindsTo": "byOperation",
       "notes": "Per operation, sorted by error rate rather than by volume.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "label": "Flagged traffic",
       "bindsTo": "ApiAnomaly",
       "columns": [
        "ApiAnomaly.clientId",
        "ApiAnomaly.measure",
        "ApiAnomaly.observed",
        "ApiAnomaly.baseline",
        "ApiAnomaly.actionTaken",
        "ApiAnomaly.detectedAt"
       ],
       "operation": "listApiAnomalies",
       "notes": "**Abnormal volume on your own clients** (17 September minutes, M17-07), so a runaway integration is seen here before a venue calls.",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Call volume; the current window renders first.",
   "error": "Could not load usage. Your quota is unaffected.",
   "emptyFirstRun": "**No calls yet.** The state links to the reference rather than sitting blank — a developer who has registered and not called anything is a developer who needs a first request.\n",
   "emptyNoResults": "No calls in this window.",
   "emptyNoAccess": "You do not have DEVELOPER_VIEW."
  },
  "apis": [
   {
    "operationId": "getApiUsage",
    "contract": "public-api",
    "purpose": "Calls, errors, latency",
    "trigger": "onLoad"
   },
   {
    "operationId": "listApiAnomalies",
    "contract": "public-api",
    "purpose": "Abnormal traffic flagged on the developer's clients",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P14 Developer.dc.html#dev-006"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P14",
   "formFactor": "web",
   "app": "developer-portal-web",
   "operator": "partner",
   "name": "Developer Portal",
   "shortName": "Developer",
   "audience": "partner",
   "offlineCapable": false,
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "DEV-007",
  "name": "Marketplace Listing",
  "module": "Developer & API",
  "requiresModule": "developerApi",
  "wave": 3,
  "implementation": {
   "app": "developer-portal-web",
   "route": "/developer/marketplace",
   "component": "apps/developer-portal-web/src/routes/developer/ListingList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "DEV-006"
   ],
   "exitTo": [
    "DEV-006",
    "DEV-008"
   ],
   "inferred": false,
   "notes": "**Returns to DEV-006.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "DEV-008",
     "trigger": "TICVAI reviews the integration and certifies it",
     "provenance": "flow F36 step 2→3",
     "operation": "submitIntegrationListing"
    }
   ]
  },
  "notes": "13.1.49 and 13.1.50, decision D1. **A listing, not an installation** — the integration runs on the developer's own infrastructure, and third-party code does not execute inside TICVAI.\n",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listIntegrationListings` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Submit an integration for certification, and see where it is in review.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every integration listing",
       "bindsTo": "IntegrationListing",
       "columns": [
        "IntegrationListing.id",
        "IntegrationListing.developerId",
        "IntegrationListing.name",
        "IntegrationListing.category",
        "IntegrationListing.description",
        "IntegrationListing.integrationUrl",
        "IntegrationListing.requiredScopes",
        "IntegrationListing.status",
        "IntegrationListing.certifiedUntil",
        "IntegrationListing.certifiedAgainstVersion",
        "IntegrationListing.listingFeeModel"
       ],
       "operation": "listIntegrationListings",
       "provenance": "contract public-api.yaml GET /listings"
      },
      {
       "kind": "primaryButton",
       "label": "Submit for certification",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "**Certification expires, and the date is shown.** An integration certified against v1 and still listed after v3 is Softlabs vouching for something nobody has looked at in two years.\n When it lapses, the production clients issued against it are suspended.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected integration listing",
       "bindsTo": "IntegrationListing",
       "columns": [
        "IntegrationListing.id",
        "IntegrationListing.developerId",
        "IntegrationListing.name",
        "IntegrationListing.category",
        "IntegrationListing.description",
        "IntegrationListing.integrationUrl",
        "IntegrationListing.requiredScopes",
        "IntegrationListing.status",
        "IntegrationListing.certifiedUntil",
        "IntegrationListing.certifiedAgainstVersion",
        "IntegrationListing.listingFeeModel"
       ],
       "operation": "listIntegrationListings",
       "provenance": "contract public-api.yaml GET /listings"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Submit integration listing",
       "operation": "submitIntegrationListing",
       "provenance": "contract public-api.yaml POST /listings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Listings with their certification status.",
   "error": "Could not load listings.",
   "emptyFirstRun": "**Nothing submitted. Certification gates production keys and the listing** (17 September minutes, M17-06): build and test in the sandbox, submit here, and once certified request production access. A private integration is certified without appearing in the marketplace.",
   "emptyNoResults": "No listing matches this category or status.",
   "emptyNoAccess": "You do not have DEVELOPER_MANAGE."
  },
  "apis": [
   {
    "operationId": "listIntegrationListings",
    "contract": "public-api",
    "purpose": "Published integrations",
    "trigger": "onLoad"
   },
   {
    "operationId": "submitIntegrationListing",
    "contract": "public-api",
    "purpose": "Submit for review",
    "trigger": "onAction",
    "invalidates": [
     "listIntegrationListings"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "IntegrationListing.id",
    "IntegrationListing.developerId",
    "IntegrationListing.name",
    "IntegrationListing.category",
    "IntegrationListing.description"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P14 Developer.dc.html#dev-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSubmitIntegrationListing",
    "component": "modal",
    "trigger": "Submit integration listing",
    "body": "**Collects what `submitIntegrationListing` sends before it is called.** Required: `id`, `developerId`, `name`, `category`, `status`. Optional: `description`, `integrationUrl`, `requiredScopes`, `certifiedUntil`, `certifiedAgainstVersion`, `listingFeeModel`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "IntegrationListing",
    "confirm": {
     "label": "Submit integration listing",
     "operation": "submitIntegrationListing"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "developerId",
      "name",
      "category",
      "status",
      "description",
      "integrationUrl",
      "requiredScopes",
      "certifiedUntil",
      "certifiedAgainstVersion",
      "listingFeeModel"
     ]
    },
    "provenance": "contract public-api.yaml POST /listings"
   }
  ],
  "_platform": {
   "code": "P14",
   "formFactor": "web",
   "app": "developer-portal-web",
   "operator": "partner",
   "name": "Developer Portal",
   "shortName": "Developer",
   "audience": "partner",
   "offlineCapable": false,
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "DEV-008",
  "name": "Programme Administration",
  "module": "Developer & API",
  "requiresModule": "developerApi",
  "wave": 2,
  "implementation": {
   "app": "developer-portal-web",
   "route": "/developer/admin",
   "component": "apps/developer-portal-web/src/routes/developer/ProgrammeAdmin.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "DEV-001"
   ],
   "exitTo": [
    "DEV-001",
    "DEV-003"
   ],
   "inferred": false,
   "notes": "**Returns to DEV-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "DEV-003",
     "trigger": "They request production access for the certified integration",
     "provenance": "flow F36 step 3→4, F36 step 5→6",
     "carries": [
      "clientId"
     ]
    }
   ]
  },
  "notes": "**`DEVELOPER_ADMIN` throughout, and never shown to a developer.** Decision D5 makes the commercial model configuration rather than code — this is the surface, and the rates themselves remain CF-135c. **Staff audience on a partner platform, and deliberately.** Every operation here — `setApiQuota`, `certifyIntegration`, `setApiLicensing`, `deprecateApiVersion` — is **Softlabs administering the programme, not a developer self-serving.** A developer who could set their own quota has no quota.\n\n**Declared on the screen rather than the platform** because P14 is a partner surface with one staff screen on it, and moving the screen to P09 would separate the console from the catalogue it governs. `check-screens` reads `screen.audience` before the platform’s.",
  "density": "compact",
  "audience": "staff",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setApiQuota`, `certifyIntegration`, `setApiLicensing`) and no read of a population — it is settings, not a list",
  "purpose": "Set quotas, certify integrations and configure licensing.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "ApiQuota.id",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "textField",
       "label": "clientId",
       "bindsTo": "ApiQuota.clientId",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "textField",
       "label": "sustainedPerMinute",
       "bindsTo": "ApiQuota.sustainedPerMinute",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "textField",
       "label": "burstPerSecond",
       "bindsTo": "ApiQuota.burstPerSecond",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "textField",
       "label": "dailyCap",
       "bindsTo": "ApiQuota.dailyCap",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "textField",
       "label": "perOperationOverrides",
       "bindsTo": "ApiQuota.perOperationOverrides",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "textField",
       "label": "onBreach",
       "bindsTo": "ApiQuota.onBreach",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "primaryButton",
       "label": "Approve",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Reject",
       "notes": "Requires a reason the developer can act on, never a bare rejection.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "**Deprecating a version names how many clients call it and which operations they use.** A generic \"v1 is retiring\" to somebody using three of two hundred endpoints is a message they will ignore.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "label": "Production access requests",
       "bindsTo": "ProductionAccessRequest",
       "operation": "listProductionAccessRequests",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save API quota",
       "operation": "setApiQuota",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "secondaryButton",
       "label": "Certify integration",
       "operation": "certifyIntegration",
       "provenance": "contract public-api.yaml POST /listings/{listingId}/certify"
      },
      {
       "kind": "secondaryButton",
       "label": "Save API licensing",
       "operation": "setApiLicensing",
       "provenance": "contract public-api.yaml PUT /api-licensing"
      },
      {
       "kind": "secondaryButton",
       "label": "Deprecate API version",
       "operation": "deprecateApiVersion",
       "provenance": "contract public-api.yaml POST /api-versions/{version}/deprecate"
      },
      {
       "kind": "secondaryButton",
       "label": "Decide production access",
       "operation": "decideProductionAccess",
       "provenance": "29 September pass (P29 group A)"
      },
      {
       "kind": "secondaryButton",
       "label": "Save anomaly rule",
       "operation": "setApiAnomalyRule",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    },
    {
     "name": "sideNav",
     "slot": "carried",
     "components": [
      {
       "kind": "treeNav",
       "notes": "Quotas · Certification queue · Production access · Anomaly rules · Licensing · Versions.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Pending certifications first.",
   "error": "Could not load.",
   "emptyFirstRun": "Nothing awaiting review.",
   "emptyNoAccess": "**This is a Softlabs screen and you are a developer.** Said plainly — a blank administration page shown to a partner is worse than a refusal, because they will file a support ticket about it.\n",
   "emptyNoResults": "No production access request with this status. Names the filter and offers to clear it."
  },
  "apis": [
   {
    "operationId": "setApiQuota",
    "contract": "public-api",
    "purpose": "Rate limits per client",
    "trigger": "onAction"
   },
   {
    "operationId": "certifyIntegration",
    "contract": "public-api",
    "purpose": "Certify, reject or revoke",
    "trigger": "onAction"
   },
   {
    "operationId": "setApiLicensing",
    "contract": "public-api",
    "purpose": "Which modules a tenant licenses",
    "trigger": "onAction"
   },
   {
    "operationId": "deprecateApiVersion",
    "contract": "public-api",
    "purpose": "Announce a sunset",
    "trigger": "onAction"
   },
   {
    "operationId": "listProductionAccessRequests",
    "contract": "public-api",
    "purpose": "The production key queue",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "operationId": "decideProductionAccess",
    "contract": "public-api",
    "purpose": "Issue or refuse production keys",
    "trigger": "onAction",
    "invalidates": [
     "listProductionAccessRequests"
    ],
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "operationId": "setApiAnomalyRule",
    "contract": "public-api",
    "purpose": "When API traffic is flagged",
    "trigger": "onAction",
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "listingId",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    },
    {
     "name": "requestId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `listingId`, `version`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P14 Developer.dc.html#dev-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCertifyIntegration",
    "component": "modal",
    "trigger": "Certify integration",
    "body": "**Collects what `certifyIntegration` sends before it is called.** Required: `decision`. Optional: `certifiedUntil`, `notes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Certify integration",
     "operation": "certifyIntegration"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "certifiedUntil",
      "notes"
     ]
    },
    "provenance": "contract public-api.yaml POST /listings/{listingId}/certify"
   },
   {
    "id": "formSetApiLicensing",
    "component": "modal",
    "trigger": "Save API licensing",
    "body": "**Collects what `setApiLicensing` sends before it is called.** Required: `licensedModules`. Optional: `id`, `callAllowancePerMonth`, `overageRatePerThousand`, `revenueSharePercent`, `effectiveFrom`, `effectiveTo`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ApiLicence",
    "confirm": {
     "label": "Save API licensing",
     "operation": "setApiLicensing"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "licensedModules",
      "id",
      "callAllowancePerMonth",
      "overageRatePerThousand",
      "revenueSharePercent",
      "effectiveFrom",
      "effectiveTo"
     ]
    },
    "provenance": "contract public-api.yaml PUT /api-licensing"
   },
   {
    "id": "formDeprecateApiVersion",
    "component": "modal",
    "trigger": "Deprecate API version",
    "body": "**Collects what `deprecateApiVersion` sends before it is called.** Required: `sunsetAt`, `reason`. Optional: `migrationGuideUrl`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Deprecate API version",
     "operation": "deprecateApiVersion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "sunsetAt",
      "reason",
      "migrationGuideUrl"
     ]
    },
    "provenance": "contract public-api.yaml POST /api-versions/{version}/deprecate"
   },
   {
    "id": "formDecideProductionAccess",
    "component": "modal",
    "trigger": "Decide production access",
    "body": "**Collects what `decideProductionAccess` sends before it is called.** Required: `decision`. Optional: `reason` (required to reject), `scopes` (narrow only), `credentialTtlDays`.",
    "confirm": {
     "label": "Decide production access",
     "operation": "decideProductionAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "reason",
      "scopes",
      "credentialTtlDays"
     ]
    },
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "id": "formSetApiAnomalyRule",
    "component": "modal",
    "trigger": "Save anomaly rule",
    "body": "**Collects what `setApiAnomalyRule` sends before it is called.** Required: `ruleKey`, `measure`, `comparison`, `threshold`, `action`.",
    "bindsTo": "ApiAnomalyRule",
    "confirm": {
     "label": "Save anomaly rule",
     "operation": "setApiAnomalyRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ruleKey",
      "clientId",
      "measure",
      "comparison",
      "threshold",
      "windowMinutes",
      "action",
      "isActive"
     ]
    },
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "_platform": {
   "code": "P14",
   "formFactor": "web",
   "app": "developer-portal-web",
   "operator": "partner",
   "name": "Developer Portal",
   "shortName": "Developer",
   "audience": "partner",
   "offlineCapable": false,
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
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
 "certifyIntegration": {
  "method": "POST",
  "path": "/listings/{listingId}/certify",
  "contract": "public-api",
  "summary": "Approve, reject or revoke a certification",
  "permission": "DEVELOPER_ADMIN",
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
  "responds": "IntegrationListing"
 },
 "createApiClient": {
  "method": "POST",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Create a client with scopes and an environment",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "ApiClient",
  "responds": null
 },
 "createSandbox": {
  "method": "POST",
  "path": "/sandboxes",
  "contract": "public-api",
  "summary": "Provision a sandbox with synthetic data",
  "permission": "DEVELOPER_MANAGE",
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
 },
 "createWebhookSubscription": {
  "method": "POST",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "Subscribe to business events",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "WebhookSubscription",
  "responds": "WebhookSubscription"
 },
 "decideProductionAccess": {
  "method": "POST",
  "path": "/production-access-requests/{requestId}/decide",
  "contract": "public-api",
  "summary": "Approve or reject production access",
  "permission": "DEVELOPER_ADMIN",
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
  "responds": "ProductionAccessRequest"
 },
 "deprecateApiVersion": {
  "method": "POST",
  "path": "/api-versions/{version}/deprecate",
  "contract": "public-api",
  "summary": "Announce a sunset date and notify subscribers",
  "permission": "DEVELOPER_ADMIN",
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
  "responds": "ApiVersion"
 },
 "getApiUsage": {
  "method": "GET",
  "path": "/api-usage",
  "contract": "public-api",
  "summary": "Calls, errors, latency and success rate",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApiUsageSummary"
 },
 "listApiAnomalies": {
  "method": "GET",
  "path": "/api-anomalies",
  "contract": "public-api",
  "summary": "Flagged API traffic",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "clientId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
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
 "listApiClients": {
  "method": "GET",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Registered clients for this developer",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApiClient"
 },
 "listApiScopes": {
  "method": "GET",
  "path": "/api-scopes",
  "contract": "public-api",
  "summary": "The scope catalogue, one read and one write scope per module",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "module",
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
 "listApiVersions": {
  "method": "GET",
  "path": "/api-versions",
  "contract": "public-api",
  "summary": "Versions, their status and their sunset dates",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApiVersion"
 },
 "listIntegrationListings": {
  "method": "GET",
  "path": "/listings",
  "contract": "public-api",
  "summary": "Published third-party integrations",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "IntegrationListing"
 },
 "listProductionAccessRequests": {
  "method": "GET",
  "path": "/production-access-requests",
  "contract": "public-api",
  "summary": "Production access requests, pending first",
  "permission": "DEVELOPER_VIEW",
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
 "listSandboxes": {
  "method": "GET",
  "path": "/sandboxes",
  "contract": "public-api",
  "summary": "Sandbox environments",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Sandbox"
 },
 "listWebhookDeliveries": {
  "method": "GET",
  "path": "/webhook-subscriptions/{subscriptionId}/deliveries",
  "contract": "public-api",
  "summary": "What was sent, what failed, and why",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "WebhookDelivery"
 },
 "listWebhookEventTypes": {
  "method": "GET",
  "path": "/webhook-event-types",
  "contract": "public-api",
  "summary": "The events a webhook may subscribe to",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "publisher",
    "in": "query",
    "required": false
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
 "listWebhookSubscriptions": {
  "method": "GET",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "The tenant's webhook subscriptions, filterable by API client",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "clientId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WebhookSubscription"
 },
 "registerDeveloper": {
  "method": "POST",
  "path": "/developers",
  "contract": "public-api",
  "summary": "Register a developer or organisation",
  "permission": "DEVELOPER_VIEW",
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
  "requestBody": "DeveloperAccount",
  "responds": "DeveloperAccount"
 },
 "replayEvents": {
  "method": "POST",
  "path": "/webhook-subscriptions/{subscriptionId}/replay",
  "contract": "public-api",
  "summary": "Re-deliver events from a point in time",
  "permission": "DEVELOPER_MANAGE",
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
 },
 "requestProductionAccess": {
  "method": "POST",
  "path": "/api-clients/{clientId}/production-access",
  "contract": "public-api",
  "summary": "Ask for production keys for a sandbox client that passed certification",
  "permission": "DEVELOPER_MANAGE",
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
  "responds": "ProductionAccessRequest"
 },
 "resetSandbox": {
  "method": "POST",
  "path": "/sandboxes/{sandboxId}/reset",
  "contract": "public-api",
  "summary": "Back to a clean synthetic dataset",
  "permission": "DEVELOPER_MANAGE",
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
 },
 "revokeApiCredential": {
  "method": "DELETE",
  "path": "/api-clients/{clientId}/credentials",
  "contract": "public-api",
  "summary": "Revoke immediately",
  "permission": "DEVELOPER_MANAGE",
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
 },
 "rotateApiCredential": {
  "method": "POST",
  "path": "/api-clients/{clientId}/credentials",
  "contract": "public-api",
  "summary": "Issue a new secret, with an overlap window",
  "permission": "DEVELOPER_MANAGE",
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
 },
 "setApiAnomalyRule": {
  "method": "PUT",
  "path": "/api-anomaly-rules",
  "contract": "public-api",
  "summary": "When API traffic is flagged as abnormal",
  "permission": "DEVELOPER_ADMIN",
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
  "requestBody": "ApiAnomalyRule",
  "responds": "ApiAnomalyRule"
 },
 "setApiLicensing": {
  "method": "PUT",
  "path": "/api-licensing",
  "contract": "public-api",
  "summary": "Which API modules a tenant has licensed, and on what terms",
  "permission": "DEVELOPER_ADMIN",
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
  "requestBody": "ApiLicence",
  "responds": "ApiLicence"
 },
 "setApiQuota": {
  "method": "PUT",
  "path": "/api-quotas",
  "contract": "public-api",
  "summary": "Rate limits and throttling per client",
  "permission": "DEVELOPER_ADMIN",
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
  "requestBody": "ApiQuota",
  "responds": "ApiQuota"
 },
 "setDeveloperMembers": {
  "method": "PUT",
  "path": "/developers/{developerId}/members",
  "contract": "public-api",
  "summary": "Who at this organisation may do what",
  "permission": "DEVELOPER_MANAGE",
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
 },
 "submitIntegrationListing": {
  "method": "POST",
  "path": "/listings",
  "contract": "public-api",
  "summary": "Submit an integration for certification (and, if public, listing)",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "IntegrationListing",
  "responds": "IntegrationListing"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApiAnomaly": {
  "type": "object",
  "x-ticvai-persistence": "control.api_anomaly",
  "description": "One flagged breach of an anomaly rule (M17-07).",
  "required": [
   "id",
   "ruleKey",
   "clientId",
   "detectedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "ruleKey": {
    "type": "string"
   },
   "clientId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "control.api_client"
   },
   "measure": {
    "type": "string"
   },
   "observed": {
    "type": "number"
   },
   "baseline": {
    "type": "number",
    "nullable": true
   },
   "actionTaken": {
    "type": "string",
    "enum": [
     "flag",
     "throttle",
     "suspend"
    ]
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ApiAnomalyRule": {
  "type": "object",
  "x-ticvai-persistence": "control.api_anomaly_rule",
  "description": "**When API traffic is abnormal** (17 September minutes, M17-07). Platform defaults ship for every tenant; TICVAI tightens them per tenant or per client.\n",
  "required": [
   "ruleKey",
   "measure",
   "comparison",
   "threshold",
   "action"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "ruleKey": {
    "type": "string"
   },
   "clientId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "control.api_client",
    "description": "Null applies to every client of the tenant."
   },
   "measure": {
    "type": "string",
    "enum": [
     "callsPerMinute",
     "clientErrorShare",
     "allowListRefusals",
     "unusualOperations",
     "authFailures"
    ]
   },
   "comparison": {
    "type": "string",
    "enum": [
     "aboveBaselineMultiple",
     "aboveFixed"
    ],
    "description": "`aboveBaselineMultiple`: above `threshold` x the same hour over the last four weeks."
   },
   "threshold": {
    "type": "number"
   },
   "windowMinutes": {
    "type": "integer",
    "minimum": 1,
    "default": 5
   },
   "action": {
    "type": "string",
    "enum": [
     "flag",
     "throttle",
     "suspend"
    ],
    "default": "flag"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ApiClient": {
  "type": "object",
  "x-ticvai-persistence": "control.api_client",
  "description": "CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n",
  "required": [
   "id",
   "developerId",
   "name",
   "environment",
   "scopes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "clientId": {
    "type": "string",
    "readOnly": true
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "production"
    ],
    "description": "**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"
   },
   "scopes": {
    "type": "array",
    "description": "**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n",
    "items": {
     "type": "string",
     "pattern": "^[a-zA-Z]+\\.(read|write)$"
    }
   },
   "issuedBy": {
    "type": "string",
    "enum": [
     "partner",
     "ticvai"
    ],
    "readOnly": true,
    "description": "Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"
   },
   "certificationListingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "control.integration_listing",
    "description": "For a production client, the certified integration it was issued against."
   },
   "credentialTtlDays": {
    "type": "integer",
    "minimum": 1,
    "maximum": 730,
    "nullable": true,
    "description": "Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the key stops working unless rotated. No token is issued after it."
   },
   "allowedTenantIds": {
    "type": "array",
    "description": "13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "description": "13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked"
    ],
    "readOnly": true
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
   }
  }
 },
 "ApiLicence": {
  "type": "object",
  "x-ticvai-persistence": "control.api_licence",
  "description": "13.3.24, decision D5. **Configuration, not code** — rates and terms change without a release.\n**The rates themselves are CF-135c and remain open.** This is the surface they will be set through.\n",
  "required": [
   "tenantId",
   "licensedModules"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "licensedModules": {
    "type": "array",
    "description": "**The example in the requirement is the shape**: a venue licensing the ticketing API and not the F&B one. **The platform module list** (17 September minutes, M17-05), so the licence, the scope catalogue and the modules a tenant buys are one vocabulary.\n",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
    }
   },
   "callAllowancePerMonth": {
    "type": "integer",
    "nullable": true
   },
   "catalogueWriteException": {
    "type": "object",
    "nullable": true,
    "description": "**M17-04: the one way a client reaches a catalogue write**, set by TICVAI platform staff only (`setApiLicensing` refuses anyone else 403 `platform-staff-only`). Null, the default, means no partner or developer client of this tenant can create or change products, price lists, prices, channel capacity, lifecycle or alternative codes.\n",
    "required": [
     "clientId",
     "operationIds",
     "reason",
     "grantedUntil"
    ],
    "properties": {
     "clientId": {
      "type": "string",
      "format": "uuid",
      "x-ticvai-references": "control.api_client"
     },
     "operationIds": {
      "type": "array",
      "minItems": 1,
      "items": {
       "type": "string",
       "enum": [
        "createProduct",
        "updateProduct",
        "setProductAttributes",
        "createPriceList",
        "updatePriceList",
        "copyPriceList",
        "setPrices",
        "createChannelCapacity",
        "updateChannelCapacity",
        "setChannelAllocations",
        "transitionProductLifecycle",
        "setAlternativeCodes"
       ]
      }
     },
     "reason": {
      "type": "string",
      "maxLength": 500
     },
     "grantedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true
     },
     "grantedUntil": {
      "type": "string",
      "format": "date"
     }
    }
   },
   "overageRatePerThousand": {
    "type": "number",
    "nullable": true
   },
   "revenueSharePercent": {
    "type": "number",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   }
  }
 },
 "ApiQuota": {
  "type": "object",
  "x-ticvai-persistence": "control.api_limit",
  "description": "13.1.36 and 13.1.37. **A quota protects the venue, not the developer.**\n",
  "required": [
   "clientId",
   "sustainedPerMinute"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "clientId": {
    "type": "string",
    "format": "uuid"
   },
   "sustainedPerMinute": {
    "type": "integer"
   },
   "burstPerSecond": {
    "type": "integer",
    "description": "**Separate from the sustained rate**, because a nightly sync is a legitimate spike and a flat per-second limit either blocks it or permits the flood it was meant to stop.\n"
   },
   "dailyCap": {
    "type": "integer",
    "nullable": true
   },
   "perOperationOverrides": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    },
    "description": "**Availability checks and order creation deserve different limits** — one is cheap and polled, the other is expensive and rare.\n"
   },
   "onBreach": {
    "type": "string",
    "enum": [
     "throttle",
     "reject",
     "queue"
    ],
    "default": "throttle"
   }
  }
 },
 "ApiScope": {
  "type": "object",
  "x-ticvai-persistence": "none — generated at release from x-ticvai-api-scope on each partner-callable operation",
  "description": "**One module scope** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, and the operations it opens.\n**A write scope never opens a catalogue write** (M17-04): `ticketing.write` opens carts, orders and holds for a partner or developer client, and no product, price list, price, channel capacity, lifecycle or alternative-code write, since those operations are not partner-callable and carry no `x-ticvai-api-scope`. Only a platform-staff `ApiLicence.catalogueWriteException` opens one, for one named client.\n",
  "required": [
   "scope",
   "module",
   "access"
  ],
  "properties": {
   "scope": {
    "type": "string",
    "description": "e.g. `ticketing.read`."
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
   },
   "access": {
    "type": "string",
    "enum": [
     "read",
     "write"
    ]
   },
   "description": {
    "type": "string"
   },
   "operations": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "contract": {
       "type": "string"
      },
      "operationId": {
       "type": "string"
      }
     }
    }
   },
   "licensed": {
    "type": "boolean",
    "description": "Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`)."
   }
  }
 },
 "ApiUsageSummary": {
  "type": "object",
  "description": "13.1.16 to 13.1.20, 13.1.41 to 13.1.45. **One endpoint because they are one question asked five ways.**\n",
  "properties": {
   "totalCalls": {
    "type": "integer"
   },
   "successRate": {
    "type": "number"
   },
   "clientErrorRate": {
    "type": "number",
    "description": "**4xx — the integrator's problem.** Separated because a single error rate lets both sides blame the other.\n"
   },
   "serverErrorRate": {
    "type": "number",
    "description": "5xx — TICVAI's problem."
   },
   "p50LatencyMs": {
    "type": "number"
   },
   "p95LatencyMs": {
    "type": "number"
   },
   "p99LatencyMs": {
    "type": "number"
   },
   "quotaBreaches": {
    "type": "integer"
   },
   "byOperation": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "operationId": {
       "type": "string"
      },
      "calls": {
       "type": "integer"
      },
      "errorRate": {
       "type": "number"
      }
     }
    }
   }
  }
 },
 "ApiVersion": {
  "type": "object",
  "x-ticvai-persistence": "control.api_version",
  "description": "13.1.31 to 13.1.35, ADR-0026. **CF-141 is sharper under D1**: a single supported production version was tenable when only Softlabs called the API, and **with third parties a breaking change with no window breaks somebody else's business.**\n",
  "required": [
   "version",
   "status"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "preview",
     "current",
     "deprecated",
     "sunset"
    ]
   },
   "releasedAt": {
    "type": "string",
    "format": "date-time"
   },
   "deprecatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "sunsetAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "minimumNoticeMonths": {
    "type": "integer",
    "default": 12,
    "description": "**The commitment, not the intention.** A deprecation policy without a stated minimum is a policy that shortens under pressure.\n"
   },
   "migrationGuideUrl": {
    "type": "string",
    "nullable": true
   },
   "activeClientCount": {
    "type": "integer",
    "readOnly": true
   },
   "changes": {
    "type": "array",
    "description": "**The developer changelog for this version** (17 September minutes, M17-14): every operation added, changed, deprecated or removed, and whether the change is breaking under ADR-0026. Generated at release from the contract diff; shown on DEV-001.\n",
    "items": {
     "type": "object",
     "required": [
      "operationId",
      "kind"
     ],
     "properties": {
      "operationId": {
       "type": "string"
      },
      "contract": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "added",
        "changed",
        "deprecated",
        "removed"
       ]
      },
      "breaking": {
       "type": "boolean",
       "default": false
      },
      "summary": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "DeveloperAccount": {
  "type": "object",
  "x-ticvai-persistence": "control.developer_account",
  "description": "13.1.6 to 13.1.9. **An organisation, because an integration outlives the engineer who built it.** A credential tied to somebody's personal account dies when they leave.\n**Not a tenant and not a partner.** A partner resells tickets; a developer writes software, and one organisation may be both.\n",
  "required": [
   "id",
   "organisationName",
   "contactEmail",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "organisationName": {
    "type": "string"
   },
   "contactEmail": {
    "type": "string",
    "format": "email"
   },
   "websiteUrl": {
    "type": "string",
    "nullable": true
   },
   "countryCode": {
    "type": "string"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where this developer is also a commercial partner. **The link exists and the two are not the same record**, which is what CF-135a was about.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "verified",
     "suspended",
     "closed"
    ],
    "readOnly": true
   },
   "verifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "IntegrationListing": {
  "type": "object",
  "x-ticvai-persistence": "control.integration_listing",
  "description": "13.1.50, decision D1. **A listing, not an installation.** The integration runs on the developer's own infrastructure.\n**Third-party code does not execute inside TICVAI** — stated rather than assumed, because that is a different product with a different threat model.\n",
  "required": [
   "id",
   "developerId",
   "name",
   "category",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "category": {
    "type": "string",
    "enum": [
     "crm",
     "marketing",
     "accounting",
     "hotel",
     "transport",
     "analytics",
     "accessibility",
     "other"
    ]
   },
   "description": {
    "type": "string"
   },
   "integrationUrl": {
    "type": "string"
   },
   "requiredScopes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "submitted",
     "inReview",
     "certified",
     "rejected",
     "revoked",
     "delisted"
    ],
    "readOnly": true
   },
   "certifiedUntil": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "readOnly": true,
    "description": "**Certification expires.** An integration certified against v1 and still listed after v3 is TICVAI vouching for something it has not looked at in two years.\n"
   },
   "certifiedAgainstVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "listingFeeModel": {
    "type": "string",
    "enum": [
     "none",
     "flat",
     "revenueShare"
    ],
    "nullable": true
   },
   "visibility": {
    "type": "string",
    "enum": [
     "public",
     "private"
    ],
    "default": "public",
    "description": "`private`: certified for production access and never shown in the marketplace (17 September minutes, M17-06). `public`: also listed once certified.\n"
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
 },
 "ProductionAccessRequest": {
  "type": "object",
  "x-ticvai-persistence": "control.production_access_request",
  "description": "**A developer's request for production keys** (17 September minutes, M17-06): sandbox, then certification, then production.\n",
  "required": [
   "id",
   "developerId",
   "sandboxClientId",
   "listingId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "sandboxClientId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "control.api_client"
   },
   "listingId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "control.integration_listing"
   },
   "scopes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "allowedTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "approved",
     "rejected",
     "withdrawn"
    ],
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "productionClientId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "control.api_client"
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "Sandbox": {
  "type": "object",
  "x-ticvai-persistence": "control.sandbox",
  "description": "D2 and D3. **One shared TICVAI sandbox, synthetic data only.**\n",
  "required": [
   "id",
   "name",
   "status",
   "dataProfile"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string"
   },
   "developerId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "provisioning",
     "active",
     "resetting",
     "expired",
     "deleted"
    ],
    "readOnly": true
   },
   "dataProfile": {
    "$ref": "#/components/schemas/SyntheticDataProfile"
   },
   "containsProductionData": {
    "type": "boolean",
    "default": false,
    "readOnly": true,
    "description": "**Always false, and stated rather than assumed** (D2). No cloning, no masking. It is a field so that a future reversal is a visible change rather than a silent one — and because **the whole PDPL and DESC argument for this contract rests on it.**\n"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "lastResetAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "SyntheticDataProfile": {
  "type": "object",
  "description": "13.2.5 and 13.2.13. **What the synthetic dataset contains**, so a developer can test against a shape that resembles a real venue without any of it being real.\n**Generated, not sampled.** Sampling production and calling it synthetic is masking with extra steps.\n",
  "properties": {
   "venueKind": {
    "type": "string",
    "enum": [
     "themePark",
     "waterPark",
     "museum",
     "theatre",
     "stadium",
     "arena",
     "mixed"
    ]
   },
   "productCount": {
    "type": "integer",
    "default": 200
   },
   "guestCount": {
    "type": "integer",
    "default": 5000
   },
   "seatMapIncluded": {
    "type": "boolean",
    "default": true
   },
   "historicalMonths": {
    "type": "integer",
    "default": 12,
    "description": "**Backdated synthetic orders**, because an integration reading a reporting API against an empty venue tests nothing.\n"
   },
   "locale": {
    "type": "string",
    "default": "en-AE"
   }
  }
 },
 "WebhookDelivery": {
  "type": "object",
  "x-ticvai-persistence": "control.webhook_delivery",
  "description": "13.1.30. **The log a developer needs most**, and without it every question becomes a support ticket.\n",
  "required": [
   "id",
   "subscriptionId",
   "eventType",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subscriptionId": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "eventType": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "delivered",
     "failed",
     "retrying",
     "abandoned"
    ]
   },
   "attemptCount": {
    "type": "integer"
   },
   "responseCode": {
    "type": "integer",
    "nullable": true
   },
   "responseBodyExcerpt": {
    "type": "string",
    "nullable": true,
    "description": "**Truncated, and it is what makes the log useful** — a 500 with the receiver's own error message in it answers the question without a conversation.\n"
   },
   "isReplay": {
    "type": "boolean",
    "default": false
   },
   "isTest": {
    "type": "boolean",
    "default": false,
    "description": "Sent by `testWebhookSubscription` (VM close-out, 29 September). Marked in the payload so a receiver never books it, and never counted towards `consecutiveFailures`.\n"
   },
   "deliveredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WebhookEventCatalogueEntry": {
  "type": "object",
  "x-ticvai-persistence": "none — read from the event catalogue (events/*.yaml) shipped with the release",
  "description": "One event a webhook may subscribe to, as the event catalogue declares it. What a receiver needs to write a handler: the name, the version in the payload, who publishes it, what it is about and when, and the payload fields.\n",
  "required": [
   "name",
   "version",
   "publisher"
  ],
  "properties": {
   "name": {
    "$ref": "#/components/schemas/WebhookEventType"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "publisher": {
    "type": "string",
    "description": "The one context that publishes it."
   },
   "aggregate": {
    "type": "string",
    "description": "What the event is about. Delivery is ordered within one instance of it."
   },
   "description": {
    "type": "string"
   },
   "emittedWhen": {
    "type": "string",
    "nullable": true
   },
   "payload": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "type"
     ],
     "properties": {
      "field": {
       "type": "string"
      },
      "type": {
       "type": "string"
      },
      "required": {
       "type": "boolean",
       "default": true
      },
      "notes": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "WebhookEventType": {
  "type": "string",
  "description": "**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n",
  "enum": [
   "access.validated",
   "accreditation.applicationDecided",
   "accreditation.credentialIssued",
   "accreditation.holderStatusChanged",
   "accreditation.renewalDue",
   "ai.ceilingApproaching",
   "apiClient.anomalyDetected",
   "approval.escalated",
   "approval.expired",
   "approval.granted",
   "approval.rejected",
   "approval.requested",
   "approval.stepCompleted",
   "assets.documentIndexed",
   "cart.abandoned",
   "catalogue.productPublished",
   "consent.deviceConsentClaimed",
   "consent.deviceConsentRecorded",
   "conversation.handedOver",
   "device.enrolmentChanged",
   "device.firmwareReleased",
   "device.firmwareRolloutCompleted",
   "device.statusChanged",
   "device.tamperDetected",
   "entitlement.expiringSoon",
   "entitlement.issued",
   "entitlement.statusChanged",
   "fnb.menuPublished",
   "fnb.orderReady",
   "inventory.purchaseOrderReceived",
   "ledger.journalPosted",
   "ledger.periodClosed",
   "maintenance.assetReturnedToService",
   "maintenance.templatePublished",
   "maintenance.workOrderCompleted",
   "marketing.caseClosed",
   "order.chargebackRecorded",
   "order.completed",
   "order.paid",
   "order.refunded",
   "performance.cancelled",
   "reporting.definitionPublished",
   "retail.merchandisePublished",
   "seat.blocked",
   "seat.held",
   "seat.released",
   "seat.sold",
   "seatMap.published",
   "shift.closed",
   "stock.depleted",
   "tenant.suspended",
   "whitelabel.contentPublished"
  ]
 },
 "WebhookSubscription": {
  "type": "object",
  "x-ticvai-persistence": "control.webhook_subscription",
  "description": "13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n",
  "required": [
   "id",
   "clientId",
   "endpointUrl",
   "eventTypes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "clientId": {
    "type": "string",
    "format": "uuid"
   },
   "endpointUrl": {
    "type": "string"
   },
   "eventTypes": {
    "type": "array",
    "description": "**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. Each entry is a name from the webhook event catalogue (`WebhookEventType`).\n",
    "items": {
     "$ref": "#/components/schemas/WebhookEventType"
    }
   },
   "filters": {
    "type": "object",
    "nullable": true,
    "description": "13.3.22. Tenant, venue, or a business condition on the payload.",
    "additionalProperties": true
   },
   "signingSecret": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingVerification",
     "active",
     "paused",
     "failing",
     "disabled"
    ],
    "readOnly": true
   },
   "consecutiveFailures": {
    "type": "integer",
    "readOnly": true
   },
   "disabledReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"
   }
  }
 }
}
```
