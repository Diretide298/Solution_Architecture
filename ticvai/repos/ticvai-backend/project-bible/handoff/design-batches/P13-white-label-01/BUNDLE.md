# P13-white-label-01 — P13 · White Label (1 of 2)

**10 screens · 60 operations · 76 schemas · 18 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 18 permissions apply here:
  `ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, ASSET_MANAGE, ASSET_VIEW, ORDER_CREATE, ORDER_VIEW, PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_TERMINATE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **7 of these operations work offline**: getAsset, getMediaAsset, getMediaEntitlements, getTenantLicences, listAssets, lookupAsset, setAssetStatus
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-001` | Tenant Workspace | listDetail | 21 | 3 | — |
| `CMS-002` | Brand Kit | statusTracker | 4 | 0 | — |
| `CMS-003` | Typography | statusTracker | 4 | 0 | — |
| `CMS-004` | Logo & Assets | listDetail | 7 | 0 | — |
| `CMS-005` | Theme Editor | statusTracker | 2 | 0 | — |
| `CMS-006` | Component Preview | listDetail | 5 | 0 | — |
| `CMS-007` | Page Builder | statusTracker | 2 | 0 | — |
| `CMS-008` | Content Blocks | listDetail | 2 | 0 | — |
| `CMS-009` | Navigation & Menus | listDetail | 5 | 0 | — |
| `CMS-010` | Media Library | listDetail | 12 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-001",
  "name": "Tenant Workspace",
  "module": "White Label",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/tenant-workspace",
   "component": "apps/venue-management-web/src/routes/white-label/TenantWorkspaceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-002",
    "CMS-003",
    "CMS-004",
    "CMS-061",
    "CMS-071",
    "CMS-081",
    "CMS-091"
   ],
   "inferred": true,
   "isEntryPoint": true,
   "transitions": [
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "flow F102 step 1→2"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-004",
     "trigger": "Logo & Assets",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-061",
     "trigger": "Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-071",
     "trigger": "AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-081",
     "trigger": "DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "CMS-091",
     "trigger": "Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **The tenant workspace.** Lands a tenant on what is live rather than on a form. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable. **Drawn 31 August** — `Marketing Board 7.dc.html` frame `crm-7f` (*Agent Workspace*), matched on title at 0.84 within this board’s platforms.",
  "density": "compact",
  "boardFrames": [
   "Marketing Board 7.dc.html#crm-7f"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTenants` reads the population and `getSsoConfig` reads one of them — list, select, act",
  "purpose": "Land a tenant somewhere that shows what is live and what is not.",
  "gaps": [
   {
    "operation": "getEntitlementUsage",
    "why": "**7 declared operations reach no component on this screen**: getEntitlementUsage, getSubscription, getTenant, getTenantLicences, getUsageMetering, listSubscriptionInvoices, listTenantCells. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status",
        "Tenant.suspensionMode",
        "Tenant.suspensionReason",
        "Tenant.planId",
        "Tenant.planName",
        "Tenant.cellCount",
        "Tenant.venueCount",
        "Tenant.billingEmail",
        "Tenant.accountManagerPrincipalId"
       ],
       "operation": "listTenants",
       "provenance": "contract subscription.yaml GET /tenants"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected tenant",
       "bindsTo": "SsoProviderConfig",
       "columns": [
        "SsoProviderConfig.id",
        "SsoProviderConfig.displayName",
        "SsoProviderConfig.protocol",
        "SsoProviderConfig.metadataUrl",
        "SsoProviderConfig.issuer",
        "SsoProviderConfig.clientId",
        "SsoProviderConfig.clientSecretRef",
        "SsoProviderConfig.groupMappings",
        "SsoProviderConfig.autoProvisionPrincipals",
        "SsoProviderConfig.isEnforced",
        "SsoProviderConfig.isActive"
       ],
       "operation": "getSsoConfig",
       "provenance": "contract identity.yaml GET /tenants/sso-config"
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
       "operation": "setSsoConfig",
       "provenance": "contract identity.yaml PUT /tenants/sso-config"
      },
      {
       "kind": "secondaryButton",
       "label": "Add",
       "operation": "addLicenceAddOn",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createTenant",
       "provenance": "contract subscription.yaml POST /tenants"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate",
       "operation": "generateInvoice",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/invoices"
      },
      {
       "kind": "secondaryButton",
       "label": "Preview",
       "operation": "previewSubscriptionChange",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/subscription/preview"
      },
      {
       "kind": "secondaryButton",
       "label": "Provision",
       "operation": "provisionCell",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/cells"
      },
      {
       "kind": "secondaryButton",
       "label": "Reactivate",
       "operation": "reactivateTenant",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/reactivate"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove",
       "operation": "removeLicenceAddOn",
       "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setSubscription",
       "provenance": "contract subscription.yaml PUT /tenants/{tenantId}/subscription"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "operation": "suspendTenant",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/suspend"
      },
      {
       "kind": "destructiveButton",
       "label": "Terminate",
       "operation": "terminateTenant",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/terminate"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateTenant",
       "provenance": "contract subscription.yaml PATCH /tenants/{tenantId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listTenants",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setSsoConfig",
       "label": "Save sso config",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "removeLicenceAddOn",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "label": "Remove licence add on",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSsoConfig",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveLicenceAddOn",
    "component": "confirmDialog",
    "trigger": "Remove",
    "body": "**Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
   },
   {
    "id": "confirmSuspendTenant",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Names what `suspendTenant` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/suspend"
   },
   {
    "id": "confirmTerminateTenant",
    "component": "confirmDialog",
    "trigger": "Terminate",
    "body": "**Names what `terminateTenant` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/terminate"
   }
  ],
  "states": {
   "loading": "The tenant list.",
   "error": "Could not load. Names which read failed and leaves the tenant untouched.",
   "emptyFirstRun": "No tenant yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "List tenants",
    "trigger": "onLoad"
   },
   {
    "operationId": "setSsoConfig",
    "contract": "identity",
    "purpose": "Configure an identity provider",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "addLicenceAddOn",
    "contract": "subscription",
    "purpose": "License a module outside the plan",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "createTenant",
    "contract": "subscription",
    "purpose": "Create a tenant",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "generateInvoice",
    "contract": "subscription",
    "purpose": "Generate an invoice for a period",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSubscription",
    "contract": "subscription",
    "purpose": "Read the current subscription",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTenant",
    "contract": "subscription",
    "purpose": "Read a tenant with cells and subscription",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTenantLicences",
    "contract": "subscription",
    "purpose": "What a tenant is licensed to use",
    "trigger": "onLoad"
   },
   {
    "operationId": "getUsageMetering",
    "contract": "subscription",
    "purpose": "Metered usage for a period",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSubscriptionInvoices",
    "contract": "subscription",
    "purpose": "List subscription invoices",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   },
   {
    "operationId": "previewSubscriptionChange",
    "contract": "subscription",
    "purpose": "Preview the effect of a plan change",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "provisionCell",
    "contract": "subscription",
    "purpose": "Provision a cell for a region",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "reactivateTenant",
    "contract": "subscription",
    "purpose": "Lift a suspension",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "removeLicenceAddOn",
    "contract": "subscription",
    "purpose": "Remove an add-on",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "setSubscription",
    "contract": "subscription",
    "purpose": "Assign or change a subscription",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "suspendTenant",
    "contract": "subscription",
    "purpose": "Suspend a tenant",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "terminateTenant",
    "contract": "subscription",
    "purpose": "Begin termination",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "updateTenant",
    "contract": "subscription",
    "purpose": "Amend tenant details",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "SsoProviderConfig.id",
    "SsoProviderConfig.displayName",
    "SsoProviderConfig.protocol",
    "SsoProviderConfig.metadataUrl",
    "SsoProviderConfig.issuer"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-001",
   "note": "**Drawn by Claude Design on `Marketing Board 7.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 21 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-002",
  "name": "Brand Kit",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/brand-kit",
   "component": "apps/venue-management-web/src/routes/white-label/BrandKitDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-003",
    "CMS-004",
    "CMS-005"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-005",
     "trigger": "Sets the colour theme",
     "provenance": "flow F22 step 1→2"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    },
    {
     "to": "CMS-004",
     "trigger": "Logo & Assets",
     "carries": [
      "assetId"
     ],
     "provenance": "derived — CMS-004 declares entryState.params assetId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getBrandIdentity` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Set the things every surface reads.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected brand kit",
       "bindsTo": "BrandIdentity",
       "columns": [
        "BrandIdentity.logoAssetRef",
        "BrandIdentity.logoDarkAssetRef",
        "BrandIdentity.faviconAssetRef",
        "BrandIdentity.splashImageAssetRefs",
        "BrandIdentity.splashDurationSeconds",
        "BrandIdentity.splashBackgroundColour",
        "BrandIdentity.showLoadingIndicator",
        "BrandIdentity.splashChangeScope"
       ],
       "operation": "getBrandIdentity",
       "provenance": "contract white-label.yaml GET /tenant-config/brand"
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
       "operation": "setBrandIdentity",
       "provenance": "contract white-label.yaml PUT /tenant-config/brand"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createUpload",
       "provenance": "contract assets.yaml POST /media/uploads"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeUpload",
       "provenance": "contract assets.yaml POST /media/uploads/{uploadId}/complete"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setBrandIdentity",
       "label": "Save brand identity",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setBrandIdentity",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The brand kit list.",
   "error": "Could not load. Names which read failed and leaves the brand kit untouched.",
   "emptyFirstRun": "No brand kit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the brand kit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getBrandIdentity",
    "contract": "white-label",
    "purpose": "Read brand identity",
    "trigger": "onLoad"
   },
   {
    "operationId": "setBrandIdentity",
    "contract": "white-label",
    "purpose": "Set logo, favicon and splash",
    "trigger": "onAction"
   },
   {
    "operationId": "createUpload",
    "contract": "assets",
    "purpose": "Request a signed upload URL",
    "trigger": "onAction"
   },
   {
    "operationId": "completeUpload",
    "contract": "assets",
    "purpose": "Confirm an upload and create the asset",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "uploadId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `uploadId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-002"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-003",
  "name": "Typography",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/typography",
   "component": "apps/venue-management-web/src/routes/white-label/TypographyDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-004",
    "CMS-006"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "CMS-006",
     "trigger": "Component Preview",
     "provenance": "flow F102 step 2→3"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
    },
    {
     "to": "CMS-004",
     "trigger": "Logo & Assets",
     "carries": [
      "assetId"
     ],
     "provenance": "derived — CMS-004 declares entryState.params assetId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **37 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getFonts` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Choose the two typefaces and the scale under them.",
  "gaps": [
   {
    "operation": "getTheme",
    "why": "**1 declared operation reach no component on this screen**: getTheme. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "The selected typography",
       "bindsTo": "FontConfig",
       "columns": [
        "FontConfig.primaryLatin",
        "FontConfig.primaryArabic",
        "FontConfig.secondaryLatin",
        "FontConfig.secondaryArabic",
        "FontConfig.customFontAssetRefs",
        "FontConfig.changeScope"
       ],
       "operation": "getFonts",
       "provenance": "contract white-label.yaml GET /tenant-config/fonts"
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
       "operation": "setFonts",
       "provenance": "contract white-label.yaml PUT /tenant-config/fonts"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setTheme",
       "provenance": "contract white-label.yaml PUT /tenant-config/theme"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setFonts",
       "label": "Save fonts",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setFonts",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The typography list.",
   "error": "Could not load. Names which read failed and leaves the typography untouched.",
   "emptyFirstRun": "No typography yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the typography are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getFonts",
    "contract": "white-label",
    "purpose": "Read font configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTheme",
    "contract": "white-label",
    "purpose": "Read colour theme",
    "trigger": "onLoad"
   },
   {
    "operationId": "setFonts",
    "contract": "white-label",
    "purpose": "Set fonts",
    "trigger": "onAction"
   },
   {
    "operationId": "setTheme",
    "contract": "white-label",
    "purpose": "Set colour theme",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-003"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-004",
  "name": "Logo & Assets",
  "module": "White Label",
  "requiresModule": "maintenance",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/logo-assets",
   "component": "apps/venue-management-web/src/routes/white-label/LogoAssetsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAssets` reads the population and `getAsset` reads one of them — list, select, act",
  "purpose": "Hold the marks every surface needs, at the sizes it needs them.",
  "gaps": [
   {
    "operation": "getAssetHistory",
    "why": "**1 declared operation reach no component on this screen**: getAssetHistory. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every logo assets",
       "bindsTo": "Asset",
       "columns": [
        "Asset.assetTag",
        "Asset.name",
        "Asset.venueId",
        "Asset.categoryId",
        "Asset.locationDescription",
        "Asset.criticality",
        "Asset.manufacturer",
        "Asset.model",
        "Asset.serialNumber",
        "Asset.commissionedAt",
        "Asset.warrantyExpiresAt",
        "Asset.supplierId"
       ],
       "operation": "listAssets",
       "provenance": "contract maintenance.yaml GET /assets"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected logo assets",
       "bindsTo": "AssetDetail",
       "columns": [
        "AssetDetail.openWorkOrders",
        "AssetDetail.maintenancePlans",
        "AssetDetail.documents"
       ],
       "operation": "getAsset",
       "provenance": "contract maintenance.yaml GET /assets/{assetId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createAsset",
       "provenance": "contract maintenance.yaml POST /assets"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup",
       "operation": "lookupAsset",
       "provenance": "contract maintenance.yaml GET /assets/lookup"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAssetStatus",
       "provenance": "contract maintenance.yaml PUT /assets/{assetId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateAsset",
       "provenance": "contract maintenance.yaml PATCH /assets/{assetId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAssets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createAsset",
       "label": "Create asset",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupAsset",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAsset",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The logo assets list.",
   "error": "Could not load. Names which read failed and leaves the logo assets untouched.",
   "emptyFirstRun": "No logo assets yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the logo assets are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAssets",
    "contract": "maintenance",
    "purpose": "List assets",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAsset",
    "contract": "maintenance",
    "purpose": "Read an asset with history and documents",
    "trigger": "onLoad"
   },
   {
    "operationId": "createAsset",
    "contract": "maintenance",
    "purpose": "Register an asset",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   },
   {
    "operationId": "getAssetHistory",
    "contract": "maintenance",
    "purpose": "Service history",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupAsset",
    "contract": "maintenance",
    "purpose": "Find an asset by tag or QR",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAssetStatus",
    "contract": "maintenance",
    "purpose": "Take an asset out of service or return it",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   },
   {
    "operationId": "updateAsset",
    "contract": "maintenance",
    "purpose": "Amend an asset",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `assetId`.",
   "preloaded": [
    "AssetDetail.openWorkOrders",
    "AssetDetail.maintenancePlans",
    "AssetDetail.documents"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-004"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-005",
  "name": "Theme Editor",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/theme-editor",
   "component": "apps/venue-management-web/src/routes/white-label/ThemeEditorDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003",
    "CMS-007"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-007",
     "trigger": "Rearranges the homepage",
     "provenance": "flow F22 step 2→3"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getTheme` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Tune the theme and watch it apply everywhere at once.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected theme editor",
       "bindsTo": "Theme",
       "columns": [
        "Theme.primaryColour",
        "Theme.secondaryColour",
        "Theme.accentColour",
        "Theme.backgroundColour",
        "Theme.textColour",
        "Theme.darkMode",
        "Theme.cornerRadius"
       ],
       "operation": "getTheme",
       "provenance": "contract white-label.yaml GET /tenant-config/theme"
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
       "operation": "setTheme",
       "provenance": "contract white-label.yaml PUT /tenant-config/theme"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setTheme",
       "label": "Save theme",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setTheme",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The theme editor list.",
   "error": "Could not load. Names which read failed and leaves the theme editor untouched.",
   "emptyFirstRun": "No theme editor yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the theme editor are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTheme",
    "contract": "white-label",
    "purpose": "Read colour theme",
    "trigger": "onLoad"
   },
   {
    "operationId": "setTheme",
    "contract": "white-label",
    "purpose": "Set colour theme",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-005"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-006",
  "name": "Component Preview",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/component-preview",
   "component": "apps/venue-management-web/src/routes/white-label/ComponentPreviewDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": false,
   "entryFrom": [
    "CMS-003",
    "CMS-005"
   ],
   "notes": "**Reached from CMS-005** — a preview shows the component being edited. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    },
    {
     "to": "ADM-016",
     "trigger": "White-Label Branding Management",
     "provenance": "flow F102 step 3→4",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **36 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Check the theme against the components that carry it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every component preview",
       "bindsTo": "ConfigVersion",
       "columns": [
        "ConfigVersion.publishedAt",
        "ConfigVersion.publishedByPrincipalId",
        "ConfigVersion.publishedByName",
        "ConfigVersion.note",
        "ConfigVersion.isCurrent",
        "ConfigVersion.scheduledFor",
        "ConfigVersion.contentHash",
        "ConfigVersion.pendingBuildTimeChanges",
        "ConfigVersion.scopePath"
       ],
       "operation": "listConfigVersions",
       "provenance": "contract white-label.yaml GET /tenant-config/versions"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected component preview",
       "bindsTo": "ConfigVersion",
       "columns": [
        "ConfigVersion.publishedAt",
        "ConfigVersion.publishedByPrincipalId",
        "ConfigVersion.publishedByName",
        "ConfigVersion.note",
        "ConfigVersion.isCurrent",
        "ConfigVersion.scheduledFor",
        "ConfigVersion.contentHash",
        "ConfigVersion.pendingBuildTimeChanges",
        "ConfigVersion.scopePath"
       ],
       "operation": "listConfigVersions",
       "provenance": "contract white-label.yaml GET /tenant-config/versions"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createPreview",
       "provenance": "contract white-label.yaml POST /tenant-config/preview"
      },
      {
       "kind": "secondaryButton",
       "label": "Diff",
       "operation": "diffConfigVersion",
       "provenance": "contract white-label.yaml GET /tenant-config/versions/{version}/diff"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Restore",
       "operation": "restoreConfigVersion",
       "provenance": "contract white-label.yaml POST /tenant-config/versions/{version}/restore"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createPreview",
       "label": "Create preview",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listConfigVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createPreview",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishTenantConfig",
       "notes": "Declares `publishTenantConfig`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The component preview list.",
   "error": "Could not load. Names which read failed and leaves the component preview untouched.",
   "emptyFirstRun": "No component preview yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the component preview are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createPreview",
    "contract": "white-label",
    "purpose": "Generate a preview link",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "diffConfigVersion",
    "contract": "white-label",
    "purpose": "Compare a version against the working draft",
    "trigger": "onLoad"
   },
   {
    "operationId": "listConfigVersions",
    "contract": "white-label",
    "purpose": "Version history",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishTenantConfig",
    "contract": "white-label",
    "purpose": "Publish the working draft",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "restoreConfigVersion",
    "contract": "white-label",
    "purpose": "Restore a previous version",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`.",
   "preloaded": [
    "ConfigVersion.publishedAt",
    "ConfigVersion.publishedByPrincipalId",
    "ConfigVersion.publishedByName",
    "ConfigVersion.note",
    "ConfigVersion.isCurrent"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-006"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-007",
  "name": "Page Builder",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/page-builder",
   "component": "apps/venue-management-web/src/routes/white-label/PageBuilderDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003",
    "CMS-012"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-012",
     "trigger": "Previews in both directions",
     "provenance": "flow F22 step 3→4"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getHomepageLayout` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Assemble a storefront page from blocks the tenant cannot break.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected record",
       "bindsTo": "HomepageLayout",
       "columns": [
        "HomepageLayout.id",
        "HomepageLayout.sections"
       ],
       "operation": "getHomepageLayout",
       "provenance": "contract white-label.yaml GET /tenant-config/homepage"
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
       "operation": "setHomepageLayout",
       "provenance": "contract white-label.yaml PUT /tenant-config/homepage"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setHomepageLayout",
       "label": "Save homepage layout",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setHomepageLayout",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The record list.",
   "error": "Could not load. Names which read failed and leaves the record untouched.",
   "emptyFirstRun": "No record yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the record are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getHomepageLayout",
    "contract": "white-label",
    "purpose": "Read homepage layout",
    "trigger": "onLoad"
   },
   {
    "operationId": "setHomepageLayout",
    "contract": "white-label",
    "purpose": "Set homepage section order",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-008",
  "name": "Content Blocks",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/content-blocks",
   "component": "apps/venue-management-web/src/routes/white-label/ContentBlocksDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": false,
   "entryFrom": [
    "CMS-001"
   ],
   "notes": "**Reached from CMS-001** — a top-level workspace section. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPromoBlocks` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Define what a block can and cannot contain.",
  "gaps": [
   {
    "operation": "listBanners",
    "why": "**1 declared operation reach no component on this screen**: listBanners. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every content blocks",
       "bindsTo": "PromoBlock",
       "columns": [
        "PromoBlock.id",
        "PromoBlock.title",
        "PromoBlock.description",
        "PromoBlock.iconAssetRef",
        "PromoBlock.promotionId",
        "PromoBlock.linkTarget",
        "PromoBlock.startsAt",
        "PromoBlock.endsAt",
        "PromoBlock.state",
        "PromoBlock.sortOrder",
        "PromoBlock.scopePath"
       ],
       "operation": "listPromoBlocks",
       "provenance": "contract white-label.yaml GET /tenant-config/promo-blocks"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected content blocks",
       "bindsTo": "PromoBlock",
       "columns": [
        "PromoBlock.id",
        "PromoBlock.title",
        "PromoBlock.description",
        "PromoBlock.iconAssetRef",
        "PromoBlock.promotionId",
        "PromoBlock.linkTarget",
        "PromoBlock.startsAt",
        "PromoBlock.endsAt",
        "PromoBlock.state",
        "PromoBlock.sortOrder",
        "PromoBlock.scopePath"
       ],
       "operation": "listPromoBlocks",
       "provenance": "contract white-label.yaml GET /tenant-config/promo-blocks"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPromoBlocks",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The content blocks list.",
   "error": "Could not load. Names which read failed and leaves the content blocks untouched.",
   "emptyFirstRun": "No content blocks yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the content blocks are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromoBlocks",
    "contract": "white-label",
    "purpose": "List promotional blocks",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBanners",
    "contract": "white-label",
    "purpose": "List banners",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromoBlock.id",
    "PromoBlock.title",
    "PromoBlock.description",
    "PromoBlock.iconAssetRef",
    "PromoBlock.promotionId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-009",
  "name": "Navigation & Menus",
  "module": "White Label",
  "requiresModule": "fnb",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/navigation-menus",
   "component": "apps/venue-management-web/src/routes/white-label/NavigationMenusDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": false,
   "entryFrom": [
    "CMS-001"
   ],
   "notes": "**Reached from CMS-001** — a top-level workspace section. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMenus` reads the population and `getMenu` reads one of them — list, select, act",
  "purpose": "Decide what appears in the header and the footer.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every navigation menus",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive"
       ],
       "operation": "listMenus",
       "provenance": "contract fnb.yaml GET /menus"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected navigation menus",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive"
       ],
       "operation": "getMenu",
       "provenance": "contract fnb.yaml GET /menus/{menuId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createMenu",
       "provenance": "contract fnb.yaml POST /menus"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setMenuSections",
       "provenance": "contract fnb.yaml PUT /menus/{menuId}/sections"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateMenu",
       "provenance": "contract fnb.yaml PATCH /menus/{menuId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMenus",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createMenu",
       "label": "Create menu",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createMenu",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The navigation menus list.",
   "error": "Could not load. Names which read failed and leaves the navigation menus untouched.",
   "emptyFirstRun": "No navigation menus yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the navigation menus are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMenus",
    "contract": "fnb",
    "purpose": "List menus",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMenu",
    "contract": "fnb",
    "purpose": "Read a menu with sections and items",
    "trigger": "onLoad"
   },
   {
    "operationId": "createMenu",
    "contract": "fnb",
    "purpose": "Create a menu",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "setMenuSections",
    "contract": "fnb",
    "purpose": "Set menu sections and their item ordering",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "updateMenu",
    "contract": "fnb",
    "purpose": "Amend a menu",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "menuId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `menuId`.",
   "preloaded": [
    "Menu.id",
    "Menu.code",
    "Menu.name",
    "Menu.outletId",
    "Menu.availability"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-009"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-010",
  "name": "Media Library",
  "module": "White Label",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/media-library",
   "component": "apps/venue-management-web/src/routes/white-label/MediaLibraryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": false,
   "entryFrom": [
    "CMS-001"
   ],
   "notes": "**Reached from CMS-001** — a top-level workspace section. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`searchMedia` reads the population and `getMediaEntitlements` reads one of them — list, select, act",
  "purpose": "Hold the imagery, and know where it is used.",
  "gaps": [
   {
    "operation": "getExpiringRights",
    "why": "**3 declared operations reach no component on this screen**: getExpiringRights, getMediaAsset, listCollections. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every media",
       "bindsTo": "MediaAsset",
       "columns": [
        "MediaAsset.id",
        "MediaAsset.kind",
        "MediaAsset.status",
        "MediaAsset.filename",
        "MediaAsset.contentType",
        "MediaAsset.sizeBytes",
        "MediaAsset.title",
        "MediaAsset.altText",
        "MediaAsset.width",
        "MediaAsset.height",
        "MediaAsset.durationSeconds",
        "MediaAsset.customMetadata"
       ],
       "operation": "searchMedia",
       "provenance": "contract assets.yaml GET /media"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected media",
       "bindsTo": "MediaEntitlements",
       "columns": [
        "MediaEntitlements.mediaCode",
        "MediaEntitlements.mediaKind",
        "MediaEntitlements.subjectId",
        "MediaEntitlements.isValid",
        "MediaEntitlements.invalidReason",
        "MediaEntitlements.canAcceptMore",
        "MediaEntitlements.entitlements"
       ],
       "operation": "getMediaEntitlements",
       "provenance": "contract orders.yaml GET /media/{mediaCode}/entitlements"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Append",
       "operation": "appendEntitlementToMedia",
       "provenance": "contract orders.yaml POST /media/{mediaCode}/entitlements"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeUpload",
       "provenance": "contract assets.yaml POST /media/uploads/{uploadId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCollection",
       "provenance": "contract assets.yaml POST /media/collections"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createUpload",
       "provenance": "contract assets.yaml POST /media/uploads"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
       "operation": "deleteMediaAsset",
       "provenance": "contract assets.yaml DELETE /media/{mediaId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace",
       "operation": "replaceMediaAsset",
       "provenance": "contract assets.yaml POST /media/{mediaId}/replace"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateMediaAsset",
       "provenance": "contract assets.yaml PATCH /media/{mediaId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "searchMedia",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "deleteMediaAsset",
       "label": "Delete media asset",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCollections",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "appendEntitlementToMedia",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteMediaAsset",
    "component": "confirmDialog",
    "trigger": "Delete",
    "body": "**Names what `deleteMediaAsset` changes and what it leaves alone**, in the consequence rather than the verb. A media this affects should be identified in the dialog, not just counted.",
    "provenance": "contract assets.yaml DELETE /media/{mediaId}"
   }
  ],
  "states": {
   "loading": "The media list.",
   "error": "Could not load. Names which read failed and leaves the media untouched.",
   "emptyFirstRun": "No media yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the media are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMediaEntitlements",
    "contract": "orders",
    "purpose": "What is already on this media",
    "trigger": "onLoad"
   },
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "Search the asset library",
    "trigger": "onLoad"
   },
   {
    "operationId": "appendEntitlementToMedia",
    "contract": "orders",
    "purpose": "Add something to a ticket the guest already holds",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "completeUpload",
    "contract": "assets",
    "purpose": "Confirm an upload and create the asset",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "createCollection",
    "contract": "assets",
    "purpose": "Create a collection",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "createUpload",
    "contract": "assets",
    "purpose": "Request a signed upload URL",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "deleteMediaAsset",
    "contract": "assets",
    "purpose": "Delete an asset",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "getExpiringRights",
    "contract": "assets",
    "purpose": "Assets whose licence is expiring or expired",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMediaAsset",
    "contract": "assets",
    "purpose": "Read an asset with derivatives and usage",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCollections",
    "contract": "assets",
    "purpose": "List collections",
    "trigger": "onLoad"
   },
   {
    "operationId": "replaceMediaAsset",
    "contract": "assets",
    "purpose": "Replace the file behind an asset",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "updateMediaAsset",
    "contract": "assets",
    "purpose": "Amend metadata, tags or rights",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mediaCode",
     "from": "deepLink"
    },
    {
     "name": "mediaId",
     "from": "deepLink"
    },
    {
     "name": "uploadId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mediaCode`, `mediaId`, `uploadId`.",
   "preloaded": [
    "MediaEntitlements.mediaCode",
    "MediaEntitlements.mediaKind",
    "MediaEntitlements.subjectId",
    "MediaEntitlements.isValid",
    "MediaEntitlements.invalidReason"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-010"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
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
 "appendEntitlementToMedia": {
  "method": "POST",
  "path": "/media/{mediaCode}/entitlements",
  "contract": "orders",
  "summary": "Add something to a ticket the guest already holds",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AppendEntitlementRequest",
  "responds": "AppendEntitlementResult"
 },
 "completeUpload": {
  "method": "POST",
  "path": "/media/uploads/{uploadId}/complete",
  "contract": "assets",
  "summary": "Confirm an upload and create the asset",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "MediaAsset"
 },
 "createAsset": {
  "method": "POST",
  "path": "/assets",
  "contract": "maintenance",
  "summary": "Register an asset",
  "permission": "ASSET_MANAGE",
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
  "requestBody": "CreateAssetRequest",
  "responds": "Asset"
 },
 "createCollection": {
  "method": "POST",
  "path": "/media/collections",
  "contract": "assets",
  "summary": "Create a collection",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "Collection"
 },
 "createMenu": {
  "method": "POST",
  "path": "/menus",
  "contract": "fnb",
  "summary": "Create a menu",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "CreateMenuRequest",
  "responds": "Menu"
 },
 "createPreview": {
  "method": "POST",
  "path": "/tenant-config/preview",
  "contract": "white-label",
  "summary": "Generate a preview link",
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
  "requestBody": null,
  "responds": "Preview"
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
 "createUpload": {
  "method": "POST",
  "path": "/media/uploads",
  "contract": "assets",
  "summary": "Request a signed upload URL",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "UploadTicket"
 },
 "deleteMediaAsset": {
  "method": "DELETE",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Delete an asset",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": null
 },
 "diffConfigVersion": {
  "method": "GET",
  "path": "/tenant-config/versions/{version}/diff",
  "contract": "white-label",
  "summary": "Compare a version against the working draft",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "against",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ConfigDiff"
 },
 "generateInvoice": {
  "method": "POST",
  "path": "/tenants/{tenantId}/invoices",
  "contract": "subscription",
  "summary": "Generate an invoice for a period",
  "permission": "PLATFORM_BILLING_MANAGE",
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
  "responds": "SubscriptionInvoice"
 },
 "getAsset": {
  "method": "GET",
  "path": "/assets/{assetId}",
  "contract": "maintenance",
  "summary": "Read an asset with history and documents",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AssetDetail"
 },
 "getAssetHistory": {
  "method": "GET",
  "path": "/assets/{assetId}/history",
  "contract": "maintenance",
  "summary": "Service history",
  "permission": "ASSET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "getBrandIdentity": {
  "method": "GET",
  "path": "/tenant-config/brand",
  "contract": "white-label",
  "summary": "Read brand identity",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "BrandIdentity"
 },
 "getEntitlementUsage": {
  "method": "GET",
  "path": "/tenants/{tenantId}/entitlement-usage",
  "contract": "subscription",
  "summary": "Usage against licensed limits",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementUsage"
 },
 "getExpiringRights": {
  "method": "GET",
  "path": "/media/rights-expiring",
  "contract": "assets",
  "summary": "Assets whose licence is expiring or expired",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "withinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ExpiringMedia"
 },
 "getFonts": {
  "method": "GET",
  "path": "/tenant-config/fonts",
  "contract": "white-label",
  "summary": "Read font configuration",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "FontConfig"
 },
 "getHomepageLayout": {
  "method": "GET",
  "path": "/tenant-config/homepage",
  "contract": "white-label",
  "summary": "Read homepage layout",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "HomepageLayout"
 },
 "getMediaAsset": {
  "method": "GET",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Read an asset with derivatives and usage",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaAssetDetail"
 },
 "getMediaEntitlements": {
  "method": "GET",
  "path": "/media/{mediaCode}/entitlements",
  "contract": "orders",
  "summary": "What is already on this media",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaEntitlements"
 },
 "getMenu": {
  "method": "GET",
  "path": "/menus/{menuId}",
  "contract": "fnb",
  "summary": "Read a menu with sections and items",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Menu"
 },
 "getSsoConfig": {
  "method": "GET",
  "path": "/tenants/sso-config",
  "contract": "identity",
  "summary": "Read SSO configuration",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SsoProviderConfig"
 },
 "getSubscription": {
  "method": "GET",
  "path": "/tenants/{tenantId}/subscription",
  "contract": "subscription",
  "summary": "Read the current subscription",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Subscription"
 },
 "getTenant": {
  "method": "GET",
  "path": "/tenants/{tenantId}",
  "contract": "subscription",
  "summary": "Read a tenant with cells and subscription",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "TenantDetail"
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
 "getTheme": {
  "method": "GET",
  "path": "/tenant-config/theme",
  "contract": "white-label",
  "summary": "Read colour theme",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Theme"
 },
 "getUsageMetering": {
  "method": "GET",
  "path": "/tenants/{tenantId}/usage",
  "contract": "subscription",
  "summary": "Metered usage for a period",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "periodStart",
    "in": "query",
    "required": true
   },
   {
    "name": "periodEnd",
    "in": "query",
    "required": true
   },
   {
    "name": "metric",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "UsageReport"
 },
 "listAssets": {
  "method": "GET",
  "path": "/assets",
  "contract": "maintenance",
  "summary": "List assets",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "maintenanceDue",
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
 "listBanners": {
  "method": "GET",
  "path": "/tenant-config/banners",
  "contract": "white-label",
  "summary": "List banners",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "state",
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
 "listCollections": {
  "method": "GET",
  "path": "/media/collections",
  "contract": "assets",
  "summary": "List collections",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Collection"
 },
 "listConfigVersions": {
  "method": "GET",
  "path": "/tenant-config/versions",
  "contract": "white-label",
  "summary": "Version history",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
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
 "listMenus": {
  "method": "GET",
  "path": "/menus",
  "contract": "fnb",
  "summary": "List menus",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 "listPromoBlocks": {
  "method": "GET",
  "path": "/tenant-config/promo-blocks",
  "contract": "white-label",
  "summary": "List promotional blocks",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PromoBlock"
 },
 "listSubscriptionInvoices": {
  "method": "GET",
  "path": "/tenants/{tenantId}/invoices",
  "contract": "subscription",
  "summary": "List subscription invoices",
  "permission": "PLATFORM_BILLING_VIEW",
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
 "listTenantCells": {
  "method": "GET",
  "path": "/tenants/{tenantId}/cells",
  "contract": "subscription",
  "summary": "List a tenant's cells",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Cell"
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
 "lookupAsset": {
  "method": "GET",
  "path": "/assets/lookup",
  "contract": "maintenance",
  "summary": "Find an asset by tag or QR",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assetTag",
    "in": "query",
    "required": null
   },
   {
    "name": "serialNumber",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AssetDetail"
 },
 "previewSubscriptionChange": {
  "method": "POST",
  "path": "/tenants/{tenantId}/subscription/preview",
  "contract": "subscription",
  "summary": "Preview the effect of a plan change",
  "permission": "PLATFORM_TENANT_VIEW",
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
  "requestBody": "SetSubscriptionRequest",
  "responds": "SubscriptionPreview"
 },
 "provisionCell": {
  "method": "POST",
  "path": "/tenants/{tenantId}/cells",
  "contract": "subscription",
  "summary": "Provision a cell for a region",
  "permission": "PLATFORM_CELL_MANAGE",
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
  "requestBody": "ProvisionCellRequest",
  "responds": null
 },
 "publishTenantConfig": {
  "method": "POST",
  "path": "/tenant-config/publish",
  "contract": "white-label",
  "summary": "Publish the working draft",
  "permission": "TENANT_PUBLISH",
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
  "responds": "ConfigVersion"
 },
 "reactivateTenant": {
  "method": "POST",
  "path": "/tenants/{tenantId}/reactivate",
  "contract": "subscription",
  "summary": "Lift a suspension",
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
  "requestBody": null,
  "responds": "Tenant"
 },
 "removeLicenceAddOn": {
  "method": "DELETE",
  "path": "/tenants/{tenantId}/licences/add-ons",
  "contract": "subscription",
  "summary": "Remove an add-on",
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
  "requestBody": null,
  "responds": "LicencePosition"
 },
 "replaceMediaAsset": {
  "method": "POST",
  "path": "/media/{mediaId}/replace",
  "contract": "assets",
  "summary": "Replace the file behind an asset",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "MediaReplaceResult"
 },
 "restoreConfigVersion": {
  "method": "POST",
  "path": "/tenant-config/versions/{version}/restore",
  "contract": "white-label",
  "summary": "Restore a previous version",
  "permission": "TENANT_PUBLISH",
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
  "responds": "TenantConfig"
 },
 "searchMedia": {
  "method": "GET",
  "path": "/media",
  "contract": "assets",
  "summary": "Search the asset library",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "tag",
    "in": "query",
    "required": null
   },
   {
    "name": "collectionId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "unusedOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "rightsExpiringWithinDays",
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
 "setAssetStatus": {
  "method": "PUT",
  "path": "/assets/{assetId}/status",
  "contract": "maintenance",
  "summary": "Take an asset out of service or return it",
  "permission": "ASSET_MANAGE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SetAssetStatusRequest",
  "responds": "AssetStatusResult"
 },
 "setBrandIdentity": {
  "method": "PUT",
  "path": "/tenant-config/brand",
  "contract": "white-label",
  "summary": "Set logo, favicon and splash",
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
  "requestBody": "BrandIdentity",
  "responds": "BrandIdentity"
 },
 "setFonts": {
  "method": "PUT",
  "path": "/tenant-config/fonts",
  "contract": "white-label",
  "summary": "Set fonts",
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
  "requestBody": "FontConfig",
  "responds": "FontConfig"
 },
 "setHomepageLayout": {
  "method": "PUT",
  "path": "/tenant-config/homepage",
  "contract": "white-label",
  "summary": "Set homepage section order",
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
  "requestBody": "HomepageLayout",
  "responds": "HomepageLayout"
 },
 "setMenuSections": {
  "method": "PUT",
  "path": "/menus/{menuId}/sections",
  "contract": "fnb",
  "summary": "Set menu sections and their item ordering",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": "Menu"
 },
 "setSsoConfig": {
  "method": "PUT",
  "path": "/tenants/sso-config",
  "contract": "identity",
  "summary": "Configure an identity provider",
  "permission": "USER_MANAGE",
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
  "requestBody": "SsoProviderConfig",
  "responds": "SsoProviderConfig"
 },
 "setSubscription": {
  "method": "PUT",
  "path": "/tenants/{tenantId}/subscription",
  "contract": "subscription",
  "summary": "Assign or change a subscription",
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
  "requestBody": "SetSubscriptionRequest",
  "responds": "Subscription"
 },
 "setTheme": {
  "method": "PUT",
  "path": "/tenant-config/theme",
  "contract": "white-label",
  "summary": "Set colour theme",
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
  "requestBody": "Theme",
  "responds": "Theme"
 },
 "suspendTenant": {
  "method": "POST",
  "path": "/tenants/{tenantId}/suspend",
  "contract": "subscription",
  "summary": "Suspend a tenant",
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
  "requestBody": null,
  "responds": "Tenant"
 },
 "terminateTenant": {
  "method": "POST",
  "path": "/tenants/{tenantId}/terminate",
  "contract": "subscription",
  "summary": "Begin termination",
  "permission": "PLATFORM_TENANT_TERMINATE",
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
 "updateAsset": {
  "method": "PATCH",
  "path": "/assets/{assetId}",
  "contract": "maintenance",
  "summary": "Amend an asset",
  "permission": "ASSET_MANAGE",
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
  "responds": "Asset"
 },
 "updateMediaAsset": {
  "method": "PATCH",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Amend metadata, tags or rights",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "MediaAsset"
 },
 "updateMenu": {
  "method": "PATCH",
  "path": "/menus/{menuId}",
  "contract": "fnb",
  "summary": "Amend a menu",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": "Menu"
 },
 "updateTenant": {
  "method": "PATCH",
  "path": "/tenants/{tenantId}",
  "contract": "subscription",
  "summary": "Amend tenant details",
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
  "requestBody": null,
  "responds": "Tenant"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessibilitySettings": {
  "type": "object",
  "description": "BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n",
  "properties": {
   "largeTextAvailable": {
    "type": "boolean",
    "default": true
   },
   "highContrastAvailable": {
    "type": "boolean",
    "default": true
   },
   "simplifiedNavigationAvailable": {
    "type": "boolean",
    "default": true
   },
   "screenReaderSupported": {
    "type": "boolean",
    "default": true
   },
   "reachableHeightModeAvailable": {
    "type": "boolean",
    "default": false,
    "description": "**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"
   },
   "sessionTimeoutMultiplier": {
    "type": "number",
    "default": 1,
    "description": "**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"
   }
  }
 },
 "AppIcons": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "sourceAssetRef",
   "changeScope"
  ],
  "properties": {
   "sourceAssetRef": {
    "type": "string"
   },
   "derived": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string"
      },
      "size": {
       "type": "string"
      },
      "assetRef": {
       "type": "string"
      }
     }
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true
   },
   "liveVersion": {
    "type": "string",
    "nullable": true,
    "description": "Icon currently shipped. Differs from the draft until the next release."
   },
   "requiresRebuild": {
    "type": "boolean",
    "readOnly": true
   }
  }
 },
 "AppendEntitlementRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "variantId",
      "quantity"
     ],
     "properties": {
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "paymentMethod": {
    "type": "string",
    "enum": [
     "card",
     "cash",
     "wallet",
     "giftCard",
     "chargeToAccount"
    ]
   },
   "note": {
    "type": "string",
    "maxLength": 300
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AppendEntitlementResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "order",
   "media"
  ],
  "properties": {
   "order": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Order"
     }
    ],
    "description": "A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"
   },
   "media": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MediaEntitlements"
     }
    ],
    "description": "The full set now on the media, so the cashier can say what the QR does."
   },
   "addedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "Asset": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateAssetRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "resourceId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"
     },
     "acquisitionCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "acquiredOn": {
      "type": "string",
      "format": "date",
      "nullable": true
     },
     "depreciation": {
      "type": "object",
      "nullable": true,
      "description": "**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n",
      "properties": {
       "method": {
        "type": "string",
        "enum": [
         "straightLine",
         "reducingBalance",
         "unitsOfProduction",
         "none"
        ]
       },
       "usefulLifeMonths": {
        "type": "integer"
       },
       "residualValue": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "accumulatedDepreciation": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     },
     "retiredOn": {
      "type": "string",
      "format": "date",
      "nullable": true,
      "description": "**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"
     },
     "disposalProceeds": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "status": {
      "$ref": "#/components/schemas/AssetStatus"
     },
     "statusReason": {
      "type": "string",
      "nullable": true
     },
     "openWorkOrderCount": {
      "type": "integer"
     },
     "nextMaintenanceDueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "isMaintenanceOverdue": {
      "type": "boolean"
     },
     "lastInspectionAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "usageCounter": {
      "type": "number",
      "nullable": true,
      "description": "Cycles, hours or kilometres. Drives usage-based maintenance."
     }
    }
   }
  ]
 },
 "AssetCriticality": {
  "type": "string",
  "enum": [
   "safetyCritical",
   "revenueCritical",
   "standard",
   "low"
  ]
 },
 "AssetDetail": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/Asset"
   },
   {
    "type": "object",
    "properties": {
     "openWorkOrders": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/WorkOrder"
      }
     },
     "maintenancePlans": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/MaintenancePlan"
      }
     },
     "documents": {
      "type": "array",
      "description": "Manuals, procedures, certificates. What a technician needs on site.",
      "items": {
       "type": "object",
       "properties": {
        "ref": {
         "type": "string"
        },
        "name": {
         "type": "string"
        },
        "kind": {
         "type": "string",
         "enum": [
          "manual",
          "sop",
          "certificate",
          "warranty",
          "drawing",
          "riskAssessment"
         ]
        }
       }
      }
     }
    }
   }
  ]
 },
 "AssetStatus": {
  "type": "string",
  "enum": [
   "inService",
   "outOfService",
   "underMaintenance",
   "awaitingParts",
   "retired",
   "disposed"
  ]
 },
 "AssetStatusResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asset",
   "downstreamEffects"
  ],
  "properties": {
   "asset": {
    "$ref": "#/components/schemas/Asset"
   },
   "downstreamEffects": {
    "type": "object",
    "description": "What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n",
    "properties": {
     "productsSuspended": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "accessPointBlocked": {
      "type": "boolean"
     },
     "performancesAffected": {
      "type": "integer"
     },
     "workOrderId": {
      "type": "string",
      "nullable": true
     }
    }
   }
  }
 },
 "BrandIdentity": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "logoAssetRef"
  ],
  "properties": {
   "logoAssetRef": {
    "type": "string"
   },
   "logoDarkAssetRef": {
    "type": "string",
    "nullable": true,
    "description": "Used on dark backgrounds. Falls back to the primary logo."
   },
   "faviconAssetRef": {
    "type": "string",
    "nullable": true
   },
   "splashImageAssetRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "splashDurationSeconds": {
    "type": "integer",
    "minimum": 0,
    "maximum": 10,
    "default": 3
   },
   "splashBackgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "showLoadingIndicator": {
    "type": "boolean",
    "default": true
   },
   "splashChangeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Always `buildTime` for native apps."
   }
  }
 },
 "Cell": {
  "x-ticvai-persistence": "control.cell",
  "x-ticvai-retired-columns": [
   "tenant_id"
  ],
  "type": "object",
  "required": [
   "id",
   "name",
   "regionId",
   "countryCode",
   "tier",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/CellKind"
   },
   "clusterId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isReachable": {
    "type": "boolean",
    "default": true,
    "description": "False for `onPremise`. The Control Plane holds the record for licensing and support and **cannot reach the installation** — it may sit behind a firewall with no inbound route. Every operation assuming reachability must handle absence rather than timing out, and a cell that has not called home for a month is not necessarily broken.\n"
   },
   "lastContactAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first.\n"
   },
   "licenceExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. **An expired licence degrades rather than stops** — a venue whose gates refuse entry because a licence lapsed over a weekend is worse than one running unlicensed until Monday.\n"
   },
   "participatesInCrossCell": {
    "type": "boolean",
    "default": true,
    "description": "False by default for `onPremise`. Redeeming a pass issued elsewhere requires reaching the issuing cell at that moment, and an on-premise site may not be able to. Exclusion is the honest default; local-then-reconcile carries a double-redemption risk that needs a decision rather than an assumption.\n"
   },
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "regionName": {
    "type": "string"
   },
   "countryCode": {
    "type": "string"
   },
   "tier": {
    "$ref": "#/components/schemas/CellTier"
   },
   "status": {
    "$ref": "#/components/schemas/CellStatus"
   },
   "cloudProvider": {
    "type": "string",
    "nullable": true
   },
   "cloudRegion": {
    "type": "string",
    "nullable": true
   },
   "apiEndpoint": {
    "type": "string",
    "nullable": true
   },
   "venueCount": {
    "type": "integer"
   },
   "provisionedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "deploymentRef": {
    "type": "string",
    "nullable": true,
    "description": "**A pointer to where this cell runs, not a description of it.** A Kubernetes namespace, an ECS cluster ARN, a stack name — whatever the orchestrator calls the thing.\n\n**The platform does not model instances, nodes or shards** (31 August). Kubernetes already holds instance counts and they change by the second; a table copying them drifts within minutes and the copy would win.\n\n**The line is: routing decisions belong to the platform, provisioning facts belong to the orchestrator.** Qdrant is the proof — ADR-0021 makes the tenant *the* shard key, so nine operations route without a lookup and **a stored shard assignment would be a second copy of something derivable.**\n\n**CF-161 needed a table after all, and this said it did not.** The claim here was that one database per cell or one per service is a build-time decision and the DDL is identical either way. **ADR-0038 answered it per tenant**, which drops `Cell.tenantId`, adds `CellTenant`, `RolloutTenant` and a per-tenant migration row, and takes `control` out of the tenant template. `tools/derive-ddl.py` carried the same claim in its docstring.\n\n**A claim that a question cannot affect your artefact is the one most likely to be left standing after it does**, which is why the correction is recorded here rather than the sentence simply deleted."
   }
  }
 },
 "CellKind": {
  "type": "string",
  "description": "Four deployment models (ADR-0017). `shared` is the default; the others exist because a client asked or a law requires it.\n\n\n**`burst` added 31 August.** An environment stood up for one on-sale and torn down after (CF-162 scenario c). **It is not a jurisdiction and it is not permanent** — it holds a catalogue snapshot, three services of sixteen, and 17 tables of 380.\n\n**The other four are places data lives. This one is a place data passes through**, which is why it has its own lifecycle and a reconciliation obligation the others do not.",
  "enum": [
   "shared",
   "dedicated",
   "onPremise",
   "controlPlane",
   "burst"
  ]
 },
 "CellStatus": {
  "type": "string",
  "enum": [
   "provisioning",
   "active",
   "migrating",
   "suspended",
   "decommissioning",
   "failed"
  ]
 },
 "CellTier": {
  "type": "string",
  "enum": [
   "shared",
   "dedicated",
   "isolated",
   "clientHosted"
  ]
 },
 "ChangeScope": {
  "type": "string",
  "description": "Whether a change reaches guests on publish or needs a store release.\n",
  "enum": [
   "runtime",
   "buildTime"
  ]
 },
 "Collection": {
  "x-ticvai-persistence": "assets.media_collection",
  "type": "object",
  "required": [
   "id",
   "name",
   "assetCount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "parentCollectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetCount": {
    "type": "integer"
   },
   "coverAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "ConfigDiff": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fromVersion",
   "toVersion",
   "changes"
  ],
  "properties": {
   "fromVersion": {
    "type": "string"
   },
   "toVersion": {
    "type": "string"
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "area",
      "path",
      "changeKind"
     ],
     "properties": {
      "area": {
       "type": "string"
      },
      "path": {
       "type": "string"
      },
      "changeKind": {
       "type": "string",
       "enum": [
        "added",
        "removed",
        "modified"
       ]
      },
      "before": {
       "type": "string",
       "nullable": true
      },
      "after": {
       "type": "string",
       "nullable": true
      },
      "changeScope": {
       "$ref": "#/components/schemas/ChangeScope"
      }
     }
    }
   }
  }
 },
 "ConfigVersion": {
  "x-ticvai-persistence": "whitelabel.config_version",
  "type": "object",
  "required": [
   "version",
   "publishedAt",
   "publishedByPrincipalId",
   "note",
   "isCurrent"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedByName": {
    "type": "string"
   },
   "note": {
    "type": "string"
   },
   "isCurrent": {
    "type": "boolean"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "contentHash": {
    "type": "string"
   },
   "pendingBuildTimeChanges": {
    "type": "array",
    "description": "Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "platforms": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "CreateAssetRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "assetTag",
   "name",
   "venueId",
   "criticality"
  ],
  "properties": {
   "assetTag": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "criticality": {
    "$ref": "#/components/schemas/AssetCriticality"
   },
   "manufacturer": {
    "type": "string",
    "maxLength": 200
   },
   "model": {
    "type": "string",
    "maxLength": 200
   },
   "serialNumber": {
    "type": "string",
    "maxLength": 128
   },
   "commissionedAt": {
    "type": "string",
    "format": "date"
   },
   "warrantyExpiresAt": {
    "type": "string",
    "format": "date"
   },
   "supplierId": {
    "type": "string",
    "format": "uuid"
   },
   "linkedProductIds": {
    "type": "array",
    "description": "Products this asset delivers. A fault here can stop them selling.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "linkedAccessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Access point this asset controls. Out of service blocks it."
   },
   "requiresInspectionToReturn": {
    "type": "boolean",
    "default": false,
    "description": "True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"
   },
   "documentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "CreateMenuRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "outletId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "availability": {
    "$ref": "#/components/schemas/MenuAvailability"
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
 "DowngradeConflictProblem": {
  "x-ticvai-persistence": "none — error shape",
  "allOf": [
   {
    "$ref": "../shared/common.yaml#/components/schemas/Problem"
   },
   {
    "type": "object",
    "properties": {
     "modulesInUse": {
      "type": "array",
      "description": "Enabled by the tenant but not licensed by the target plan.",
      "items": {
       "type": "object",
       "properties": {
        "moduleKey": {
         "type": "string"
        },
        "displayName": {
         "type": "string"
        },
        "isEnabled": {
         "type": "boolean"
        }
       }
      }
     },
     "limitsExceeded": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "metric": {
         "$ref": "#/components/schemas/UsageMetric"
        },
        "currentUsage": {
         "type": "integer"
        },
        "targetLimit": {
         "type": "integer"
        }
       }
      }
     }
    }
   }
  ]
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
    "description": "Null means unlimited."
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
 "EntitlementStatus": {
  "type": "string",
  "description": "**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n",
  "enum": [
   "issued",
   "partiallyConsumed",
   "fullyConsumed",
   "expired",
   "cancelled",
   "surrendered"
  ]
 },
 "EntitlementUsage": {
  "x-ticvai-persistence": "none — aggregated from usage_record",
  "type": "object",
  "required": [
   "tenantId",
   "metrics"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "metrics": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "metric",
      "current",
      "isNearLimit"
     ],
     "properties": {
      "metric": {
       "$ref": "#/components/schemas/UsageMetric"
      },
      "current": {
       "type": "integer"
      },
      "limit": {
       "type": "integer",
       "nullable": true
      },
      "percentUsed": {
       "type": "number",
       "nullable": true
      },
      "isNearLimit": {
       "type": "boolean",
       "description": "Approaching a limit is an account conversation. Hitting one silently at a gate is an incident.\n"
      },
      "isExceeded": {
       "type": "boolean"
      }
     }
    }
   },
   "asAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ExpiringMedia": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "assetId",
   "filename",
   "validTo",
   "isExpired",
   "isInUse"
  ],
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "filename": {
    "type": "string"
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date"
   },
   "daysRemaining": {
    "type": "integer"
   },
   "isExpired": {
    "type": "boolean"
   },
   "isInUse": {
    "type": "boolean"
   },
   "liveUsageCount": {
    "type": "integer",
    "description": "Expired and live is the combination that matters."
   }
  }
 },
 "FeatureToggle": {
  "x-ticvai-persistence": "whitelabel.feature_toggle",
  "type": "object",
  "required": [
   "featureKey",
   "isEnabled",
   "changeScope"
  ],
  "properties": {
   "featureKey": {
    "type": "string",
    "enum": [
     "digitalCompanionMode",
     "aiConciergeChat",
     "lostAndFound",
     "pushNotifications",
     "socialSharing",
     "multiLanguage",
     "appleWallet",
     "googlePay",
     "applePay",
     "cashOnDelivery",
     "guestCheckout",
     "uaePassLogin"
    ]
   },
   "displayName": {
    "type": "string"
   },
   "isEnabled": {
    "type": "boolean"
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"
   },
   "requiresConfiguration": {
    "type": "boolean",
    "description": "True where the feature needs credentials or setup elsewhere first."
   }
  }
 },
 "FontConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryLatin"
  ],
  "properties": {
   "primaryLatin": {
    "type": "string"
   },
   "primaryArabic": {
    "type": "string",
    "nullable": true,
    "description": "Required when Arabic is enabled. A Latin face alone leaves Arabic in a system fallback that will not match.\n"
   },
   "secondaryLatin": {
    "type": "string",
    "nullable": true
   },
   "secondaryArabic": {
    "type": "string",
    "nullable": true
   },
   "customFontAssetRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Custom font files are `buildTime`; selecting a bundled face is `runtime`."
   }
  }
 },
 "FooterConfig": {
  "type": "object",
  "x-ticvai-persistence": "control.footer_config",
  "description": "BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n",
  "required": [
   "id",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "heading": {
       "type": "string"
      },
      "links": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "url": {
          "type": "string"
         },
         "opensCookiePreferences": {
          "type": "boolean",
          "default": false
         }
        }
       }
      }
     }
    }
   },
   "legalLinks": {
    "type": "object",
    "description": "**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n",
    "properties": {
     "termsUrl": {
      "type": "string"
     },
     "privacyUrl": {
      "type": "string"
     },
     "accessibilityUrl": {
      "type": "string",
      "nullable": true
     },
     "cookiePolicyUrl": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "copyrightText": {
    "type": "string"
   },
   "socialLinks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string"
      },
      "url": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "HeaderConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "layout"
  ],
  "properties": {
   "layout": {
    "type": "string",
    "enum": [
     "logoLeft",
     "logoCentre",
     "logoWithMenu"
    ]
   },
   "showLogo": {
    "type": "boolean",
    "default": true
   },
   "showMenu": {
    "type": "boolean",
    "default": true
   },
   "showNotifications": {
    "type": "boolean",
    "default": true
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   }
  }
 },
 "HomepageLayout": {
  "x-ticvai-persistence": "whitelabel.homepage_section",
  "type": "object",
  "required": [
   "sections"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "sortOrder",
      "isVisible"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "kind": {
       "$ref": "#/components/schemas/HomepageSectionKind"
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isVisible": {
       "type": "boolean"
      },
      "contentPageId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "maxItems": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "HomepageSectionKind": {
  "type": "string",
  "enum": [
   "heroBanner",
   "quickActions",
   "tickets",
   "whatsOn",
   "attractions",
   "membership",
   "dining",
   "shop",
   "promotions",
   "map",
   "customContent",
   "spacer"
  ]
 },
 "InvoiceStatus": {
  "type": "string",
  "enum": [
   "draft",
   "issued",
   "paid",
   "overdue",
   "disputed",
   "cancelled"
  ]
 },
 "LanguageConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "languages",
   "defaultLanguage"
  ],
  "properties": {
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "defaultLanguage": {
    "type": "string"
   },
   "rtlLanguages": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "string"
    }
   },
   "translationGaps": {
    "type": "array",
    "readOnly": true,
    "description": "Content lacking a version in an enabled language.",
    "items": {
     "type": "object",
     "properties": {
      "language": {
       "type": "string"
      },
      "missingCount": {
       "type": "integer"
      },
      "areas": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   }
  }
 },
 "LicenceAddOn": {
  "x-ticvai-persistence": "control.licence_add_on",
  "type": "object",
  "required": [
   "moduleKey"
  ],
  "properties": {
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
  "x-ticvai-persistence": "none — union of plan and add-ons",
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
 "LinkTarget": {
  "x-ticvai-persistence": "none — embedded",
  "type": "object",
  "required": [
   "kind"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "module",
     "contentPage",
     "product",
     "event",
     "externalUrl",
     "none"
    ]
   },
   "moduleKey": {
    "$ref": "#/components/schemas/ModuleKey"
   },
   "contentPageId": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "url": {
    "type": "string"
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
 "MaintenancePlan": {
  "x-ticvai-persistence": "maintenance.maintenance_plan",
  "type": "object",
  "required": [
   "id",
   "name",
   "assetId",
   "taskTemplate"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "assetCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Applies to every asset in the category rather than one."
   },
   "intervalDays": {
    "type": "integer",
    "nullable": true,
    "description": "Elapsed-time trigger."
   },
   "usageInterval": {
    "type": "number",
    "nullable": true,
    "description": "Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"
   },
   "leadTimeDays": {
    "type": "integer",
    "default": 7,
    "description": "How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"
   },
   "taskTemplate": {
    "type": "object",
    "required": [
     "title",
     "priority"
    ],
    "properties": {
     "title": {
      "type": "string"
     },
     "description": {
      "type": "string"
     },
     "priority": {
      "$ref": "#/components/schemas/WorkOrderPriority"
     },
     "estimatedMinutes": {
      "type": "integer"
     },
     "inspectionTemplateId": {
      "type": "string",
      "format": "uuid"
     },
     "requiredPartIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "lastCompletedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "nextDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "MediaAsset": {
  "x-ticvai-persistence": "assets.media_asset",
  "type": "object",
  "required": [
   "id",
   "kind",
   "status",
   "filename",
   "contentType",
   "sizeBytes",
   "referenceCount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "status": {
    "$ref": "#/components/schemas/MediaStatus"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Required before use in a guest-facing surface. WCAG 2.2 AA."
   },
   "width": {
    "type": "integer",
    "nullable": true
   },
   "height": {
    "type": "integer",
    "nullable": true
   },
   "durationSeconds": {
    "type": "number",
    "nullable": true
   },
   "customMetadata": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"
   },
   "sharedWithTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "url": {
    "type": "string",
    "description": "Signed and expiring for private assets; stable CDN URL for public ones."
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "referenceCount": {
    "type": "integer",
    "description": "How many surfaces reference this asset. Non-zero refuses deletion.\n"
   },
   "rights": {
    "$ref": "#/components/schemas/MediaRights"
   },
   "isRightsExpired": {
    "type": "boolean"
   },
   "version": {
    "type": "integer"
   },
   "uploadedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MediaAssetDetail": {
  "x-ticvai-persistence": "assets.media_asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/MediaAsset"
   },
   {
    "type": "object",
    "properties": {
     "derivatives": {
      "type": "array",
      "description": "Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n",
      "items": {
       "type": "object",
       "properties": {
        "label": {
         "type": "string"
        },
        "width": {
         "type": "integer"
        },
        "height": {
         "type": "integer"
        },
        "sizeBytes": {
         "type": "integer"
        },
        "url": {
         "type": "string"
        }
       }
      }
     },
     "usage": {
      "type": "array",
      "description": "Every place this asset is referenced.",
      "items": {
       "$ref": "#/components/schemas/MediaUsage"
      }
     },
     "collections": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "id": {
         "type": "string",
         "format": "uuid"
        },
        "name": {
         "type": "string"
        }
       }
      }
     },
     "previousVersions": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "version": {
         "type": "integer"
        },
        "replacedAt": {
         "type": "string",
         "format": "date-time"
        },
        "replacedByPrincipalId": {
         "type": "string",
         "format": "uuid"
        }
       }
      }
     }
    }
   }
  ]
 },
 "MediaEntitlements": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over entitlement and scan history",
  "required": [
   "mediaCode",
   "isValid",
   "entitlements"
  ],
  "properties": {
   "mediaCode": {
    "type": "string"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "qr",
     "wristband",
     "card",
     "nfc",
     "mobilePass"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isValid": {
    "type": "boolean"
   },
   "invalidReason": {
    "type": "string",
    "nullable": true
   },
   "canAcceptMore": {
    "type": "boolean",
    "description": "False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"
   },
   "entitlements": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementId": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "admission",
        "locker",
        "fnb",
        "retail",
        "parking",
        "rental",
        "experience",
        "membership"
       ]
      },
      "orderId": {
       "type": "string"
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      },
      "status": {
       "allOf": [
        {
         "$ref": "#/components/schemas/EntitlementStatus"
        }
       ],
       "description": "**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"
      },
      "entriesUsed": {
       "type": "integer"
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "redeemedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "transferredToSubjectId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "validTo": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "MediaKind": {
  "type": "string",
  "enum": [
   "image",
   "video",
   "audio",
   "document",
   "vector",
   "font",
   "archive"
  ]
 },
 "MediaReplaceResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asset",
   "affectedSurfaces"
  ],
  "properties": {
   "asset": {
    "$ref": "#/components/schemas/MediaAsset"
   },
   "affectedSurfaces": {
    "type": "integer",
    "description": "How many surfaces now show the new file."
   },
   "liveSurfaces": {
    "type": "integer",
    "description": "Of those, how many are published to guests right now."
   },
   "derivativesRegenerating": {
    "type": "boolean"
   }
  }
 },
 "MediaRights": {
  "x-ticvai-persistence": "none — embedded in asset",
  "type": "object",
  "description": "Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n",
  "properties": {
   "licenceKind": {
    "type": "string",
    "enum": [
     "owned",
     "royaltyFree",
     "rightsManaged",
     "creativeCommons",
     "editorialOnly",
     "unknown"
    ]
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "licenceReference": {
    "type": "string",
    "nullable": true
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "permittedUses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "web",
      "print",
      "socialMedia",
      "inVenue",
      "advertising",
      "internal"
     ]
    }
   },
   "attributionRequired": {
    "type": "boolean",
    "default": false
   },
   "attributionText": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "MediaStatus": {
  "type": "string",
  "enum": [
   "processing",
   "ready",
   "quarantined",
   "failed",
   "archived"
  ]
 },
 "MediaUsage": {
  "x-ticvai-persistence": "assets.media_usage",
  "type": "object",
  "required": [
   "surface",
   "referenceId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "surface": {
    "type": "string",
    "enum": [
     "tenantBranding",
     "homepageBanner",
     "promoBlock",
     "contentPage",
     "product",
     "event",
     "menuItem",
     "merchandise",
     "workOrder",
     "incident",
     "inspection",
     "campaign"
    ]
   },
   "referenceId": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "isLive": {
    "type": "boolean",
    "description": "True where the referencing surface is published to guests."
   }
  }
 },
 "Menu": {
  "x-ticvai-persistence": "fnb.menu",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "outletId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "availability": {
    "$ref": "#/components/schemas/MenuAvailability"
   },
   "sections": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MenuSection"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "MenuAvailability": {
  "x-ticvai-persistence": "none — embedded in menu",
  "type": "object",
  "description": "When this menu is in force. Absent means always.",
  "properties": {
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 0,
     "maximum": 6
    }
   },
   "startTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "endTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   }
  }
 },
 "MenuSection": {
  "x-ticvai-persistence": "fnb.menu_section",
  "type": "object",
  "required": [
   "code",
   "name",
   "sortOrder"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "sortOrder": {
    "type": "integer"
   },
   "items": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MenuItem"
    }
   }
  }
 },
 "ModuleEnablement": {
  "x-ticvai-persistence": "whitelabel.module_enablement",
  "type": "object",
  "required": [
   "moduleKey",
   "isLicensed",
   "isEnabled"
  ],
  "properties": {
   "moduleKey": {
    "$ref": "#/components/schemas/ModuleKey"
   },
   "displayName": {
    "type": "string"
   },
   "isLicensed": {
    "type": "boolean",
    "description": "From the tenant's subscription. False makes enablement impossible."
   },
   "isEnabled": {
    "type": "boolean"
   },
   "referencedBy": {
    "type": "array",
    "readOnly": true,
    "description": "Navigation items and homepage sections pointing at this module.",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "NavigationConfig": {
  "x-ticvai-persistence": "whitelabel.navigation_item",
  "type": "object",
  "required": [
   "kind",
   "items"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "bottomNavigation",
     "drawer",
     "tabs"
    ]
   },
   "items": {
    "type": "array",
    "maxItems": 12,
    "items": {
     "type": "object",
     "required": [
      "label",
      "target",
      "isVisible",
      "sortOrder"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "icon": {
       "type": "string"
      },
      "target": {
       "$ref": "#/components/schemas/LinkTarget"
      },
      "isVisible": {
       "type": "boolean",
       "description": "At most five may be visible in bottom navigation; the rest overflow."
      },
      "sortOrder": {
       "type": "integer"
      }
     }
    }
   }
  }
 },
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "Preview": {
  "x-ticvai-persistence": "none — short-lived, cache only",
  "type": "object",
  "required": [
   "previewId",
   "url",
   "expiresAt"
  ],
  "properties": {
   "previewId": {
    "type": "string",
    "format": "uuid"
   },
   "url": {
    "type": "string"
   },
   "platform": {
    "type": "string"
   },
   "theme": {
    "type": "string"
   },
   "language": {
    "type": "string"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "PromoBlock": {
  "x-ticvai-persistence": "whitelabel.promo_block",
  "type": "object",
  "required": [
   "id",
   "title"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "iconAssetRef": {
    "type": "string",
    "nullable": true
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Presentation only. A block may point at a promotion; it does not create or price one.\n"
   },
   "linkTarget": {
    "$ref": "#/components/schemas/LinkTarget"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "state": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ScheduleState"
     }
    ],
    "readOnly": true
   },
   "sortOrder": {
    "type": "integer"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ProvisionCellRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "regionId",
   "countryCode",
   "tier"
  ],
  "properties": {
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "description": "Determines the jurisdiction. Placement must be within it — this is enforced, not trusted.\n"
   },
   "tier": {
    "$ref": "#/components/schemas/CellTier"
   },
   "cloudProvider": {
    "type": "string"
   },
   "cloudRegion": {
    "type": "string"
   },
   "clientHostedEndpoint": {
    "type": "string",
    "nullable": true,
    "description": "Required for `clientHosted`, where no in-region cloud exists."
   }
  }
 },
 "ScheduleState": {
  "type": "string",
  "enum": [
   "draft",
   "scheduled",
   "active",
   "expired"
  ]
 },
 "SetAssetStatusRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "status",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "status": {
    "$ref": "#/components/schemas/AssetStatus"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 1000
   },
   "inspectionId": {
    "type": "string",
    "nullable": true,
    "description": "Required for return to service where the asset demands it."
   },
   "raiseWorkOrder": {
    "type": "boolean",
    "default": false
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "SetSubscriptionRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "planId"
  ],
  "properties": {
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planVersion": {
    "type": "string",
    "description": "Defaults to the current version."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   },
   "prorate": {
    "type": "boolean",
    "default": true
   },
   "note": {
    "type": "string",
    "maxLength": 500
   }
  }
 },
 "SsoGroupMapping": {
  "x-ticvai-persistence": "identity.sso_group_mapping",
  "type": "object",
  "required": [
   "externalGroup",
   "roleId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The table had no key at all — the response returned the external group, the role and the scope, which is everything a caller needs and not the row own identity.\n**(provider, external_group) is unique and would serve**, but a mapping is edited and revoked by an administrator, and **a row addressed by the values it holds cannot be corrected** — changing the group means deleting a mapping and creating another, which loses who granted it and when.\n"
   },
   "externalGroup": {
    "type": "string"
   },
   "roleId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "description": "Scope the mapped role is granted at."
   }
  }
 },
 "SsoProtocol": {
  "type": "string",
  "enum": [
   "oidc",
   "saml2"
  ]
 },
 "SsoProviderConfig": {
  "x-ticvai-persistence": "identity.sso_provider",
  "type": "object",
  "required": [
   "id",
   "displayName",
   "protocol",
   "groupMappings"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "protocol": {
    "$ref": "#/components/schemas/SsoProtocol"
   },
   "metadataUrl": {
    "type": "string",
    "nullable": true
   },
   "issuer": {
    "type": "string",
    "nullable": true
   },
   "clientId": {
    "type": "string",
    "nullable": true
   },
   "clientSecretRef": {
    "type": "string",
    "nullable": true,
    "description": "Key vault reference. The secret itself is never returned."
   },
   "groupMappings": {
    "type": "array",
    "minItems": 1,
    "description": "**A group with no mapping grants nothing.** No default role, ever — otherwise the identity provider becomes a way to mint access nobody configured.\n",
    "items": {
     "$ref": "#/components/schemas/SsoGroupMapping"
    }
   },
   "autoProvisionPrincipals": {
    "type": "boolean",
    "default": false,
    "description": "Create a principal on first successful sign-in."
   },
   "isEnforced": {
    "type": "boolean",
    "default": false
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "Subscription": {
  "x-ticvai-persistence": "control.subscription",
  "type": "object",
  "required": [
   "tenantId",
   "planId",
   "planVersion",
   "status",
   "startsAt"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planName": {
    "type": "string"
   },
   "planVersion": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "trial",
     "active",
     "pastDue",
     "cancelled",
     "expired"
    ]
   },
   "startsAt": {
    "type": "string",
    "format": "date"
   },
   "renewsAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "cancelledAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingPeriod": {
    "type": "string"
   }
  }
 },
 "SubscriptionInvoice": {
  "x-ticvai-persistence": "control.invoice + control.invoice_line",
  "type": "object",
  "required": [
   "id",
   "invoiceNumber",
   "tenantId",
   "periodStart",
   "periodEnd",
   "status",
   "total"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "invoiceNumber": {
    "type": "string"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "periodStart": {
    "type": "string",
    "format": "date"
   },
   "periodEnd": {
    "type": "string",
    "format": "date"
   },
   "status": {
    "$ref": "#/components/schemas/InvoiceStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "description": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "basePlan",
        "addOn",
        "overage",
        "oneOff",
        "credit"
       ]
      },
      "metric": {
       "$ref": "#/components/schemas/UsageMetric"
      },
      "quantity": {
       "type": "number"
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "planVersionUsed": {
    "type": "string",
    "description": "Priced against the version the tenant is subscribed to, not the latest."
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "paidAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "SubscriptionPreview": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "canApply",
   "priceChange"
  ],
  "properties": {
   "canApply": {
    "type": "boolean"
   },
   "priceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "proratedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "modulesGained": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modulesLost": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "conflicts": {
    "$ref": "#/components/schemas/DowngradeConflictProblem"
   },
   "cellTierChange": {
    "type": "object",
    "nullable": true,
    "properties": {
     "from": {
      "$ref": "#/components/schemas/CellTier"
     },
     "to": {
      "$ref": "#/components/schemas/CellTier"
     },
     "requiresMigration": {
      "type": "boolean"
     }
    }
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
   "billingEmail": {
    "type": "string"
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
 "TenantConfig": {
  "x-ticvai-persistence": "whitelabel.tenant_config",
  "type": "object",
  "required": [
   "tenantId",
   "version",
   "brand",
   "theme",
   "fonts",
   "navigation",
   "homepage",
   "languages"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "string"
   },
   "isDraft": {
    "type": "boolean"
   },
   "brand": {
    "$ref": "#/components/schemas/BrandIdentity"
   },
   "appIcons": {
    "$ref": "#/components/schemas/AppIcons"
   },
   "theme": {
    "$ref": "#/components/schemas/Theme"
   },
   "fonts": {
    "$ref": "#/components/schemas/FontConfig"
   },
   "footer": {
    "$ref": "#/components/schemas/FooterConfig"
   },
   "notificationBranding": {
    "type": "object",
    "nullable": true,
    "description": "BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n",
    "properties": {
     "senderName": {
      "type": "string"
     },
     "replyToEmail": {
      "type": "string",
      "format": "email"
     },
     "smsSenderId": {
      "type": "string",
      "nullable": true
     },
     "whatsappBusinessId": {
      "type": "string",
      "nullable": true
     },
     "logoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   },
   "enabledPaymentMethods": {
    "type": "array",
    "nullable": true,
    "description": "BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n",
    "items": {
     "type": "string"
    }
   },
   "accessibility": {
    "$ref": "#/components/schemas/AccessibilitySettings"
   },
   "header": {
    "$ref": "#/components/schemas/HeaderConfig"
   },
   "navigation": {
    "$ref": "#/components/schemas/NavigationConfig"
   },
   "homepage": {
    "$ref": "#/components/schemas/HomepageLayout"
   },
   "modules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ModuleEnablement"
    }
   },
   "features": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FeatureToggle"
    }
   },
   "languages": {
    "$ref": "#/components/schemas/LanguageConfig"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "TenantDetail": {
  "x-ticvai-persistence": "control.tenant",
  "allOf": [
   {
    "$ref": "#/components/schemas/Tenant"
   },
   {
    "type": "object",
    "properties": {
     "subscription": {
      "$ref": "#/components/schemas/Subscription"
     },
     "cells": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/Cell"
      }
     },
     "licences": {
      "$ref": "#/components/schemas/LicencePosition"
     }
    }
   }
  ]
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
 "Theme": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryColour",
   "secondaryColour",
   "backgroundColour",
   "textColour"
  ],
  "properties": {
   "primaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "secondaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "accentColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "textColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "darkMode": {
    "type": "object",
    "description": "Optional dark variant. Derived from the light theme when absent.",
    "properties": {
     "primaryColour": {
      "type": "string"
     },
     "backgroundColour": {
      "type": "string"
     },
     "textColour": {
      "type": "string"
     }
    }
   },
   "cornerRadius": {
    "type": "integer",
    "minimum": 0,
    "maximum": 32
   }
  }
 },
 "UploadTicket": {
  "x-ticvai-persistence": "assets.media_upload",
  "type": "object",
  "required": [
   "uploadId",
   "uploadUrl",
   "method",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "uploadId": {
    "type": "string",
    "format": "uuid"
   },
   "uploadUrl": {
    "type": "string",
    "description": "Signed. PUT the file here, then confirm with `/complete`."
   },
   "method": {
    "type": "string",
    "enum": [
     "PUT",
     "POST"
    ]
   },
   "headers": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "maxSizeBytes": {
    "type": "integer"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
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
 "UsageReport": {
  "x-ticvai-persistence": "none — aggregated",
  "type": "object",
  "required": [
   "tenantId",
   "periodStart",
   "periodEnd",
   "metrics"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "periodStart": {
    "type": "string",
    "format": "date"
   },
   "periodEnd": {
    "type": "string",
    "format": "date"
   },
   "metrics": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "metric": {
       "$ref": "#/components/schemas/UsageMetric"
      },
      "total": {
       "type": "number"
      },
      "included": {
       "type": "number",
       "nullable": true
      },
      "overage": {
       "type": "number"
      },
      "byVenue": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "venueId": {
          "type": "string",
          "format": "uuid"
         },
         "quantity": {
          "type": "number"
         }
        }
       }
      },
      "byCapability": {
       "type": "array",
       "description": "AI tokens only.",
       "items": {
        "type": "object",
        "properties": {
         "capability": {
          "type": "string"
         },
         "quantity": {
          "type": "number"
         }
        }
       }
      }
     }
    }
   }
  }
 },
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
  "type": "object",
  "required": [
   "id",
   "workOrderNumber",
   "title",
   "venueId",
   "status",
   "priority",
   "kind",
   "createdAt"
  ],
  "properties": {
   "downtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n"
   },
   "rootCause": {
    "type": "string",
    "nullable": true,
    "enum": [
     "wearAndTear",
     "operatorError",
     "guestDamage",
     "manufacturingDefect",
     "environmental",
     "softwareFault",
     "powerFailure",
     "deferredMaintenance",
     "unknown"
    ],
    "description": "**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"
   },
   "rootCauseNote": {
    "type": "string",
    "nullable": true
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "escalationLevel": {
    "type": "integer",
    "default": 0,
    "description": "**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"
   },
   "id": {
    "type": "string"
   },
   "workOrderNumber": {
    "type": "string"
   },
   "title": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetName": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "kind": {
    "$ref": "#/components/schemas/WorkOrderKind"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "elapsedMinutes": {
    "type": "integer"
   },
   "isTimerRunning": {
    "type": "boolean"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean"
   },
   "requiresVerification": {
    "type": "boolean"
   },
   "sourcePlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceInspectionId": {
    "type": "string",
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
