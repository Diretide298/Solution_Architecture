# WS103 — Subscription Licensing AI Self Service board 6

**9 screens · 13 operations · 24 schemas · 8 permissions**

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
  `PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW, REGION_CONFIGURE, SCOPE_MANAGE, TENANT_CONFIGURE, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-419` | Provisioning Command Center | listDetail | 1 | 0 | — |
| `ADM-420` | Tenant & Organization Provisioning | listDetail | 1 | 0 | — |
| `ADM-421` | Venue & Operational Structure Creation | configEditor | 4 | 1 | — |
| `ADM-422` | Administrator & Security Initialization | configEditor | 2 | 0 | — |
| `ADM-423` | License & Entitlement Activation | listDetail | 1 | 0 | — |
| `ADM-424` | Module Activation & Dependency Validation | listDetail | 1 | 0 | — |
| `ADM-425` | Venue Template Application | listDetail | 1 | 0 | — |
| `ADM-426` | Initial Configuration & Regional Defaults | configEditor | 1 | 0 | — |
| `ADM-427` | Provisioning Validation & Exception Management | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-419, ADM-420, ADM-423, ADM-424, ADM-425, ADM-427 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-419",
  "name": "Provisioning Command Center",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "1",
   "page": 72
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/provisioning-command-center-adm-419",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ProvisioningCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-420",
    "ADM-421",
    "ADM-422",
    "ADM-423",
    "ADM-424",
    "ADM-425",
    "ADM-426",
    "ADM-427"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "ADM-420",
     "trigger": "Tenant & Organization Provisioning",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-421",
     "trigger": "Venue & Operational Structure Creation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-422",
     "trigger": "Administrator & Security Initialization",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-423",
     "trigger": "License & Entitlement Activation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-424",
     "trigger": "Module Activation & Dependency Validation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-425",
     "trigger": "Venue Template Application",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-426",
     "trigger": "Initial Configuration & Regional Defaults",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-427",
     "trigger": "Provisioning Validation & Exception Management",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show the overall status of the customer's environment creation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 72"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 72"
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
       "impliedBy": "createTenant",
       "label": "Create tenant",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createTenant"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The provisioning list.",
   "error": "Could not load. Names which read failed and leaves the provisioning untouched.",
   "emptyFirstRun": "No provisioning yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the provisioning are still there. The pack's own statuses are Pending — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createTenant",
    "contract": "subscription",
    "purpose": "Provision the tenant",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-419",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-419"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 72. 0 of 0 labels bound to a contract property; 6 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 },
 {
  "id": "ADM-420",
  "name": "Tenant & Organization Provisioning",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "2",
   "page": 73
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/tenant-organization-provisioning-adm-420",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/TenantOrganizationProvisioning.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the customer's isolated TICVAI environment and primary organization structure.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 73"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 73"
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
       "impliedBy": "createOrgUnit",
       "label": "Create org unit",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createOrgUnit"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant organization provisioning list.",
   "error": "Could not load. Names which read failed and leaves the tenant organization provisioning untouched.",
   "emptyFirstRun": "No tenant organization provisioning yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant organization provisioning are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createOrgUnit",
    "contract": "tenancy",
    "purpose": "Venue and operational structure",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-420",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-420"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 73. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 },
 {
  "id": "ADM-421",
  "name": "Venue & Operational Structure Creation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "3",
   "page": 74
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/venue-operational-structure-creation-adm-421",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/VenueOperationalStructureCreation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Venue Settings) and no display directory — it is settings, not a population",
  "purpose": "Automatically create the initial venue structure using information collected during onboarding.",
  "gaps": [
   {
    "operation": null,
    "why": "**Venue & Operational Structure Creation declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status"
       ],
       "operation": "listTenants",
       "notes": "**Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant into it is open.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "Open grant into this tenant",
       "bindsTo": "PlatformStaffGrant",
       "columns": [
        "PlatformStaffGrant.id",
        "PlatformStaffGrant.operatorDisplayName",
        "PlatformStaffGrant.permissions",
        "PlatformStaffGrant.reason",
        "PlatformStaffGrant.ticketRef",
        "PlatformStaffGrant.openedAt",
        "PlatformStaffGrant.expiresAt"
       ],
       "operation": "openPlatformStaffGrant",
       "notes": "**Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "primaryButton",
       "label": "Open access grant",
       "operation": "openPlatformStaffGrant",
       "notes": "Shown until a grant into the picked tenant is open; asks for the second factor first (step-up, audit R135).",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "selectField",
       "label": "Venue Name",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Venue Type",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Address",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Operating Region",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Default Language",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Operating Model",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formOpenPlatformStaffGrant",
    "component": "modal",
    "trigger": "Open access grant",
    "body": "**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.",
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
   }
  ],
  "states": {
   "loading": "The venue operational structure configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the venue operational structure untouched.",
   "emptyFirstRun": "No venue operational structure configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist",
   "grantRequired": "**No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098)."
  },
  "apis": [
   {
    "operationId": "openPlatformStaffGrant",
    "contract": "identity",
    "purpose": "Open a time-boxed, audited platform-staff grant into the picked tenant before any tenant-scoped operation here; the tenant sees it (decided 28 September, audit R098)",
    "trigger": "onAction"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "The tenant picker — the operator picks a tenant before acting in its cell (audit R098)",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPrincipal",
    "contract": "identity",
    "purpose": "The first administrator",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setPasswordPolicy",
    "contract": "identity",
    "purpose": "Security initialisation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-421",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-421"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 74. 0 of 0 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 },
 {
  "id": "ADM-422",
  "name": "Administrator & Security Initialization",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "4",
   "page": 75
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/administrator-security-initialization-adm-422",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/AdministratorSecurityInitialization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Security Setup) and no display directory — it is settings, not a population",
  "purpose": "Create the initial authorized customer administrator and establish the tenant security baseline.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "✓ Administrator Account Created",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Email Verified",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "textField",
       "label": "✓ Tenant Access Assigned",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "textField",
       "label": "✓ Default Role Applied",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "textField",
       "label": "✓ Security Policy Applied",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "textField",
       "label": "✓ Audit Logging Enabled",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The administrator security initialization configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the administrator security initialization untouched.",
   "emptyFirstRun": "No administrator security initialization configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getTenantLicences",
    "contract": "subscription",
    "purpose": "Licence and entitlement activation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "addLicenceAddOn",
    "contract": "subscription",
    "purpose": "Activate an add-on",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-422",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-422"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 75. 0 of 0 labels bound to a contract property; 6 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "session"
    }
   ]
  },
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
 },
 {
  "id": "ADM-423",
  "name": "License & Entitlement Activation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "5",
   "page": 76
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/license-entitlement-activation-adm-423",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/LicenseEntitlementActivation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Translate the commercial subscription purchased in Board 5 into enforceable technical entitlements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 76"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 76"
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
       "impliedBy": "listModuleCatalogue",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The license entitlement activation list.",
   "error": "Could not load. Names which read failed and leaves the license entitlement activation untouched.",
   "emptyFirstRun": "No license entitlement activation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the license entitlement activation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listModuleCatalogue",
    "contract": "subscription",
    "purpose": "Module activation and dependencies",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-423",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-423"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 76. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 },
 {
  "id": "ADM-424",
  "name": "Module Activation & Dependency Validation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "6",
   "page": 77
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/module-activation-dependency-validation-adm-424",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ModuleActivationDependencyValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Activate the modules purchased in Board 4/5 and verify all required dependencies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 77"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 77"
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
       "impliedBy": "listVenueTypeTemplates",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The module activation dependency list.",
   "error": "Could not load. Names which read failed and leaves the module activation dependency untouched.",
   "emptyFirstRun": "No module activation dependency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the module activation dependency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVenueTypeTemplates",
    "contract": "subscription",
    "purpose": "Apply a venue template",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-424",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-424"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 },
 {
  "id": "ADM-425",
  "name": "Venue Template Application",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "7",
   "page": 77
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/venue-template-application-adm-425",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/VenueTemplateApplication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Apply an appropriate initial configuration template based on the venue assessment from Board 2.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 77"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 77"
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
       "impliedBy": "updateRegionSettings",
       "label": "Save region settings",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateRegionSettings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue template application list.",
   "error": "Could not load. Names which read failed and leaves the venue template application untouched.",
   "emptyFirstRun": "No venue template application yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue template application are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRegionSettings",
    "contract": "tenancy",
    "purpose": "Regional defaults",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-425",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-425"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "regionId",
     "from": "navigation"
    }
   ]
  },
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
 },
 {
  "id": "ADM-426",
  "name": "Initial Configuration & Regional Defaults",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "8",
   "page": 78
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/initial-configuration-regional-defaults-adm-426",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/InitialConfigurationRegionalDefaults.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Low-risk settings such as; Business-critical settings such as) and no display directory — it is settings, not a population",
  "purpose": "Apply safe initial defaults using information already provided during onboarding.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Low-risk settings such as"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Low-risk settings such as"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Low-risk settings such as"
      },
      {
       "kind": "selectField",
       "label": "Venue Type",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Low-risk settings such as"
      },
      {
       "kind": "selectField",
       "label": "Ticket prices",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Tax",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Refund policy",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Payment rules",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Access rules",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Settlement",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Capacity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The initial regional defaults configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the initial regional defaults untouched.",
   "emptyFirstRun": "No initial regional defaults configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "runGoLiveValidation",
    "contract": "subscription",
    "purpose": "Validate the provisioning",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGoLiveReadiness"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-426",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-426"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 78. 0 of 0 labels bound to a contract property; 11 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 },
 {
  "id": "ADM-427",
  "name": "Provisioning Validation & Exception Management",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "9",
   "page": 79
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/provisioning-validation-exception-management-adm-427",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ProvisioningValidationExceptionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Validate that the environment has been created correctly before handing it to customer configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 79"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 79"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The provisioning validation exception list.",
   "error": "Could not load. Names which read failed and leaves the provisioning validation exception untouched.",
   "emptyFirstRun": "No provisioning validation exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the provisioning validation exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGoLiveReadiness",
    "contract": "subscription",
    "purpose": "Provisioning outcome",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-427",
   "workshopBoard": "wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-427"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 79. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "addLicenceAddOn": {
  "method": "POST",
  "path": "/tenants/{tenantId}/licences/add-ons",
  "contract": "subscription",
  "summary": "License a module outside the plan",
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
  "requestBody": "LicenceAddOn",
  "responds": "LicencePosition"
 },
 "createOrgUnit": {
  "method": "POST",
  "path": "/org-units",
  "contract": "tenancy",
  "summary": "Create a scope node",
  "permission": "SCOPE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "brand",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateScopeNodeRequest",
  "responds": "OrgUnit"
 },
 "createPrincipal": {
  "method": "POST",
  "path": "/principals",
  "contract": "identity",
  "summary": "Create a principal",
  "permission": "USER_MANAGE",
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
  "requestBody": "CreatePrincipalRequest",
  "responds": "Principal"
 },
 "createTenant": {
  "method": "POST",
  "path": "/tenants",
  "contract": "subscription",
  "summary": "Create a tenant",
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
  "requestBody": "CreateTenantRequest",
  "responds": "Tenant"
 },
 "getGoLiveReadiness": {
  "method": "GET",
  "path": "/go-live-readiness",
  "contract": "subscription",
  "summary": "Everything that must pass before a tenant can sell",
  "permission": "PLATFORM_TENANT_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "tenantId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "GoLiveReadiness"
 },
 "getTenantLicences": {
  "method": "GET",
  "path": "/tenants/{tenantId}/licences",
  "contract": "subscription",
  "summary": "What a tenant is licensed to use",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "LicencePosition"
 },
 "listModuleCatalogue": {
  "method": "GET",
  "path": "/module-catalogue",
  "contract": "subscription",
  "summary": "Modules, their dependencies and their commercial treatment",
  "permission": "PLATFORM_PLAN_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [],
  "requestBody": null,
  "responds": "ModuleListing"
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
 "listVenueTypeTemplates": {
  "method": "GET",
  "path": "/venue-type-templates",
  "contract": "subscription",
  "summary": "Starting configurations by venue kind",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueTypeTemplate"
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
 "runGoLiveValidation": {
  "method": "POST",
  "path": "/go-live-readiness/run",
  "contract": "subscription",
  "summary": "Run the validation plan against a tenant",
  "permission": "PLATFORM_TENANT_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
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
 "setPasswordPolicy": {
  "method": "PUT",
  "path": "/password-policy",
  "contract": "identity",
  "summary": "Length, breach check, lockout and step-up",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "PasswordPolicy",
  "responds": "PasswordPolicy"
 },
 "updateRegionSettings": {
  "method": "PUT",
  "path": "/regions/{regionId}/settings",
  "contract": "tenancy",
  "summary": "Update region settings",
  "permission": "REGION_CONFIGURE",
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
  "requestBody": "RegionSettings",
  "responds": "RegionSettings"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreatePrincipalRequest": {
  "type": "object",
  "required": [
   "username",
   "displayName"
  ],
  "properties": {
   "username": {
    "type": "string",
    "maxLength": 256
   },
   "displayName": {
    "type": "string",
    "maxLength": 200
   },
   "initialCredential": {
    "type": "string",
    "maxLength": 512,
    "writeOnly": true
   },
   "mustChangeCredential": {
    "type": "boolean",
    "default": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "CreateScopeNodeRequest": {
  "type": "object",
  "required": [
   "level",
   "parentId",
   "code",
   "name"
  ],
  "properties": {
   "level": {
    "$ref": "#/components/schemas/ScopeLevel"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "description": "Required for every level except tenant, which the cell creates at provisioning."
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[a-z0-9_]+$",
    "description": "Becomes the final ltree segment. Immutable once created."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   }
  }
 },
 "CreateTenantRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "billingEmail"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[a-z0-9-]+$"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "billingEmail": {
    "type": "string"
   },
   "billingAddress": {
    "type": "string",
    "maxLength": 500
   },
   "accountManagerPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "EntitlementLimit": {
  "type": "object",
  "required": [
   "metric",
   "limit"
  ],
  "properties": {
   "metric": {
    "$ref": "#/components/schemas/UsageMetric"
   },
   "limit": {
    "type": "integer",
    "nullable": true,
    "x-ticvai-column": "limit_value",
    "description": "Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."
   },
   "overageAllowed": {
    "type": "boolean",
    "default": false
   },
   "overageUnitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "GoLiveReadiness": {
  "type": "object",
  "x-ticvai-persistence": "subscription.go_live_readiness",
  "description": "Board 8. **The screen that stops a launch going wrong in public.**",
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "runAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "notStarted",
     "running",
     "blocked",
     "readyWithWarnings",
     "ready"
    ]
   },
   "groups": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "ticketingAndProducts",
        "salesChannels",
        "payment",
        "ticketQrAccess",
        "usersAndSecurity",
        "integrations",
        "communications",
        "financialSetup"
       ]
      },
      "label": {
       "type": "string"
      },
      "checks": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "code": {
          "type": "string"
         },
         "label": {
          "type": "string"
         },
         "outcome": {
          "type": "string",
          "enum": [
           "pass",
           "warn",
           "fail",
           "skipped"
          ]
         },
         "detail": {
          "type": "string",
          "nullable": true
         },
         "remediation": {
          "type": "string",
          "nullable": true
         }
        }
       }
      }
     }
    }
   },
   "blockers": {
    "type": "integer"
   },
   "warnings": {
    "type": "integer"
   },
   "signedOffBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "signedOffAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "LicenceAddOn": {
  "x-ticvai-persistence": "control.licence_add_on + control.licence_add_on_limit",
  "x-ticvai-retired-columns": [
   "plan_id"
  ],
  "description": "**Belongs to the tenant, not the plan.** Add-ons survive a plan change unless explicitly removed (`addLicenceAddOn`), so a row keyed on `plan_id` would be lost, or silently re-applied to every tenant on that plan, at the first plan change. The tenant comes from the path. `limitOverrides` are child rows in `control.licence_add_on_limit`.",
  "type": "object",
  "required": [
   "moduleKey"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The tenant the add-on was sold to — the `tenantId` in the path, never the body."
   },
   "moduleKey": {
    "type": "string"
   },
   "limitOverrides": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/EntitlementLimit"
    }
   },
   "price": {
    "x-ticvai-column": "list_price",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "note": {
    "type": "string",
    "maxLength": 500
   }
  }
 },
 "LicencePosition": {
  "x-ticvai-persistence": "none — union of the tenant's plan (control.tenant.plan_id -> subscription.plan_module, subscription.plan_limit) and its add-ons (control.licence_add_on, control.licence_add_on_limit by tenant_id)",
  "type": "object",
  "required": [
   "tenantId",
   "licensedModules",
   "limits"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "licensedModules": {
    "type": "array",
    "description": "Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it.\n",
    "items": {
     "type": "object",
     "required": [
      "moduleKey",
      "source"
     ],
     "properties": {
      "moduleKey": {
       "type": "string"
      },
      "displayName": {
       "type": "string"
      },
      "source": {
       "type": "string",
       "enum": [
        "plan",
        "addOn"
       ]
      },
      "validTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "limits": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/EntitlementLimit"
    }
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
 "ModuleListing": {
  "type": "object",
  "x-ticvai-persistence": "subscription.module_listing",
  "description": "Board 4.6. **A marketplace without a dependency graph sells combinations that cannot be provisioned.**\n**TICVAI configures each module's price here, and tenants are billed per module (decided 29 September, Chinmay).** A usage-priced module (the AI module's tokens) has `pricingBasis` `metered`: `price` is then per `meteredUnitSize` units of `meteredMetric`, and the invoice carries it as a `metered` line.\n",
  "required": [
   "moduleCode"
  ],
  "properties": {
   "moduleCode": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "category": {
    "type": "string",
    "nullable": true
   },
   "requiresModules": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "incompatibleWithModules": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "includedInTiers": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "price": {
    "x-ticvai-column": "list_price",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "included",
     "flatFee",
     "perVenue",
     "perUnit",
     "revenueShare",
     "metered"
    ]
   },
   "meteredMetric": {
    "allOf": [
     {
      "$ref": "#/components/schemas/UsageMetric"
     }
    ],
    "nullable": true,
    "description": "For `metered`, what is counted (`aiTokens` for the AI module). Null otherwise."
   },
   "meteredUnitSize": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "For `metered`, how many units `price` buys (e.g. 1000 tokens). Null otherwise."
   },
   "provisioningMinutes": {
    "type": "integer",
    "nullable": true
   },
   "requiresProfessionalServices": {
    "type": "boolean",
    "default": false
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "beta",
     "deprecated",
     "withdrawn"
    ]
   }
  }
 },
 "OrgUnit": {
  "x-ticvai-persistence": "platform.scope",
  "type": "object",
  "required": [
   "id",
   "level",
   "path",
   "code",
   "name",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "level": {
    "$ref": "#/components/schemas/ScopeLevel"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "path": {
    "type": "string",
    "description": "Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "isActive": {
    "type": "boolean",
    "description": "False causes every permission query at or beneath this node to resolve to DENY.\n"
   },
   "childCount": {
    "type": "integer",
    "minimum": 0
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
 "PasswordPolicy": {
  "type": "object",
  "x-ticvai-persistence": "identity.password_policy",
  "description": "BL-144. **Written by `setPasswordPolicy`, which returns it**, at tenant scope. Before BL-144 the package had no password policy, no lockout and no forced change at first logon anywhere.\n**Modelled on NIST SP 800-63B rather than on habit.** Length beats composition, and forced rotation on a schedule makes passwords worse — people increment a digit. Rotation is here because some tenants are contractually required to have it, **not because it helps.**\n",
  "required": [
   "id",
   "scopePath",
   "minLength"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server. Required in the response only; ignored if a request sends it."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005), written by the server from the caller's tenant (`x-ticvai-config-scope: tenant`). Required in the response only; ignored if a request sends it."
   },
   "minLength": {
    "type": "integer",
    "default": 12,
    "minimum": 8,
    "description": "A tenant may raise the length and never set it below 8 (decided 28 September, audit R126 (7))."
   },
   "requireBreachCheck": {
    "type": "boolean",
    "default": true,
    "description": "**The single most effective rule.** Refusing a password known to be breached stops more account takeovers than every composition rule combined.\n"
   },
   "maxAgeDays": {
    "type": "integer",
    "nullable": true,
    "description": "**Null is the recommended value.** Forced rotation produces `Summer2026!` becoming `Summer2027!`, and it is offered because some tenants are contractually obliged to have it rather than because it works.\n"
   },
   "recoveryMethods": {
    "type": "array",
    "description": "BL-132. **A guest locked out had no path back** — lockout existed and recovery did not, which turns a forgotten password into a support call.\n**Ordered by strength, and the venue chooses which it offers.** Email is weakest and universal; a verified phone is stronger; an in-person check at a desk is strongest and only available to a guest who is already at the venue.\n",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "sms",
      "securityQuestions",
      "inPersonVerification",
      "supportAssisted"
     ]
    }
   },
   "maxConcurrentSessions": {
    "type": "integer",
    "nullable": true,
    "description": "BL-145. **Null, and that is the decision.** A staff principal has one live session, full stop: ADR-0004 keeps a server-side session registry (the `sid` claim, `ActiveSession`), and §3.1.3 refuses a second sign-in rather than counting towards a limit (confirmed 28 September, audit R184). A number here would only ever mean 1.\nThe requirement asked for it configurable. **Configurable to null is still an answer.**\n"
   },
   "deviceRestriction": {
    "type": "object",
    "nullable": true,
    "description": "BL-146. **Device, browser, IP and location restriction on access.** Applies to staff principals, not guests — a guest restricted to one device is a guest who cannot use their new phone.\n**Warn before block by default.** An IP restriction that blocks silently is a venue manager locked out on the day their ISP rotates an address.\n",
    "properties": {
     "allowedIpRanges": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "allowedCountries": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "requireRegisteredDevice": {
      "type": "boolean",
      "default": false
     },
     "onViolation": {
      "type": "string",
      "enum": [
       "warn",
       "requireStepUp",
       "block"
      ],
      "default": "requireStepUp"
     }
    }
   },
   "lockoutAfterAttempts": {
    "type": "integer",
    "default": 10
   },
   "lockoutMinutes": {
    "type": "integer",
    "default": 15,
    "description": "**A temporary lockout, not a permanent one.** Permanent lockout on failed attempts is a denial-of-service anybody can run against a known username.\n"
   },
   "forceChangeOnFirstLogon": {
    "type": "boolean",
    "default": true
   },
   "reusePreventionCount": {
    "type": "integer",
    "default": 5,
    "minimum": 0,
    "maximum": 24,
    "description": "**How many previous credentials a staff member may not reuse** — the last 5 unless the tenant sets another (decided 28 September, audit R132). `changeOwnCredential` refuses a match with `422`.\n"
   },
   "mfaRequiredForPermissions": {
    "type": "array",
    "description": "**Step-up rather than blanket MFA.** Requiring it for a refund approval and not for reading a rota is what stops people sharing devices to avoid it.\n**MFA is required by permission, not by role** (decided 28 September, audit R135). A principal holding any permission listed here must keep an active method (`removeMfaMethod` refuses to remove the last one). **The default is the platform floor**: `ROLE_MANAGE`, `LEDGER_APPROVE` and every `PLATFORM_*` permission. A tenant may add to the list and never remove a floor entry; a body that drops one is refused `400`.\n",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
    },
    "default": [
     "ROLE_MANAGE",
     "LEDGER_APPROVE",
     "PLATFORM_TENANT_VIEW",
     "PLATFORM_TENANT_MANAGE",
     "PLATFORM_TENANT_TERMINATE",
     "PLATFORM_TENANT_ACCESS",
     "PLATFORM_PLAN_MANAGE",
     "PLATFORM_CELL_VIEW",
     "PLATFORM_CELL_MANAGE",
     "PLATFORM_BILLING_VIEW",
     "PLATFORM_BILLING_MANAGE",
     "PLATFORM_RELEASE_VIEW",
     "PLATFORM_RELEASE_MANAGE",
     "PLATFORM_RELEASE_PROMOTE",
     "PLATFORM_MIGRATION_VIEW",
     "PLATFORM_MIGRATION_APPLY"
    ]
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
    "format": "uuid"
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
 "Principal": {
  "x-ticvai-persistence": "identity.principal",
  "type": "object",
  "required": [
   "id",
   "username",
   "displayName",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "username": {
    "type": "string"
   },
   "displayName": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Past this, resolution returns DENY regardless of grants."
   },
   "primaryRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Determines the landing screen when the principal holds several roles and picks one at login.\n"
   },
   "roles": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RoleSummary"
    }
   },
   "lastLoginAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "RoleSummary": {
  "x-ticvai-persistence": "none — projection over role",
  "type": "object",
  "required": [
   "id",
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
   "isPrimary": {
    "type": "boolean"
   }
  }
 },
 "ScopeLevel": {
  "type": "string",
  "description": "**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n",
  "enum": [
   "tenant",
   "brand",
   "region",
   "venue",
   "department",
   "subDepartment",
   "workstation",
   "outlet",
   "subject"
  ]
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
 },
 "UsageMetric": {
  "type": "string",
  "enum": [
   "venues",
   "workstations",
   "activeUsers",
   "devices",
   "brandedApps",
   "aiTokens",
   "apiCalls",
   "storageGb",
   "transactions",
   "guestProfiles"
  ]
 },
 "VenueTypeTemplate": {
  "type": "object",
  "x-ticvai-persistence": "control.venue_type_template",
  "description": "BL-165. **What a venue of this kind starts with.** Product kinds, price list structure, access profiles, roles, report set.\n**A template is a starting point and not a constraint** — everything it creates is editable the moment it lands, which is the difference between a template and a plan tier.\n",
  "required": [
   "id",
   "name",
   "venueKind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "venueKind": {
    "type": "string",
    "enum": [
     "themePark",
     "waterPark",
     "museum",
     "theatre",
     "stadium",
     "arena",
     "zoo",
     "aquarium",
     "cinema",
     "attraction",
     "mixed"
    ]
   },
   "seedsProductKinds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "seedsRoles": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "seedsAdmissionProfiles": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "seedsReports": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 }
}
```
