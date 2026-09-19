# P09-tenants-licensing-01 — P09 · Tenants & Licensing

**9 screens · 34 operations · 39 schemas · 14 permissions**

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

- **Every control that can be refused must be gated.** 14 permissions apply here:
  `DEVELOPER_ADMIN, DEVELOPER_VIEW, PARTNER_MANAGE, PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_TERMINATE, PLATFORM_TENANT_VIEW, SCOPE_MANAGE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: getTenantLicences
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-005` | Tenant Directory | listDetail | 15 | 3 | — |
| `ADM-006` | Tenant Hierarchy Explorer | listDetail | 9 | 0 | — |
| `ADM-007` | Module & Feature Entitlement | listDetail | 9 | 1 | — |
| `ADM-008` | Subscription & Plan Management | listDetail | 19 | 0 | — |
| `ADM-009` | Tenant Billing & Invoicing | listDetail | 9 | 0 | — |
| `ADM-010` | Usage Metering | listDetail | 7 | 0 | — |
| `ADM-011` | Licence & Seat Management | listDetail | 11 | 1 | — |
| `ADM-012` | Tenant Isolation & Resource Pool | listDetail | 8 | 0 | — |
| `ADM-015` | API Rate Limit & Quota Management | listDetail | 9 | 0 | — |

## Thin screens in this batch

**ADM-010, ADM-015 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-005",
  "name": "Tenant Directory",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 1,
  "capability": "C95",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/tenant-directory",
   "component": "apps/ticvai-web/src/routes/general/TenantDirectoryList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-008",
    "ADM-012"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "ADM-012",
     "trigger": "Provisions or assigns a cell",
     "provenance": "flow F16 step 1→2"
    },
    {
     "to": "ADM-008",
     "trigger": "Subscription & Plan Management",
     "provenance": "flow F96 step 1→2"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenants` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "Find the right one quickly, and act on it without opening it.",
  "gaps": [
   {
    "operation": "getSsoConfig",
    "why": "**4 declared operations reach no component on this screen**: getSsoConfig, getTenant, getTenantLicences, listTenantCells. Either the screen is missing what calls them, or the declaration is residue.",
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
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
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
       "operation": "setSsoConfig",
       "provenance": "contract identity.yaml PUT /tenants/sso-config"
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
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
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
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
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
    "operationId": "setSsoConfig",
    "contract": "identity",
    "purpose": "Configure an identity provider",
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
     "from": "ADM-002"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "EntitlementUsage.metrics",
    "EntitlementUsage.asAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-005"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 15 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-006",
  "name": "Tenant Hierarchy Explorer",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 1,
  "capability": "C20",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/tenant-hierarchy-explorer",
   "component": "apps/ticvai-web/src/routes/general/TenantHierarchyExplorerList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-007"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "ADM-007",
     "trigger": "Enables the modules the tenant bought",
     "provenance": "flow F16 step 3→4"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenants` reads the population and `getSsoConfig` reads one of them — list, select, act",
  "purpose": "See tenant hierarchy explorer for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementUsage",
    "why": "**5 declared operations reach no component on this screen**: getEntitlementUsage, getTenant, getTenantLicences, listTenantCells, listOrgUnits. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every tenant hierarchy",
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
       "label": "The selected tenant hierarchy",
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
       "operation": "updateTenant",
       "provenance": "contract subscription.yaml PATCH /tenants/{tenantId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createOrgUnit",
       "provenance": "contract tenancy.yaml POST /org-units"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant hierarchy list.",
   "error": "Could not load. Names which read failed and leaves the tenant hierarchy untouched.",
   "emptyFirstRun": "No tenant hierarchy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant hierarchy are still there. Names the active filter and offers to clear it.",
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
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
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
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateTenant",
    "contract": "subscription",
    "purpose": "Amend tenant details",
    "trigger": "onAction",
    "invalidates": [
     "listTenants"
    ]
   },
   {
    "operationId": "listOrgUnits",
    "contract": "tenancy",
    "purpose": "List scope nodes visible to the session",
    "trigger": "onLoad"
   },
   {
    "operationId": "createOrgUnit",
    "contract": "tenancy",
    "purpose": "Create a scope node",
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
     "from": "ADM-002"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-006"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-007",
  "name": "Module & Feature Entitlement",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 1,
  "capability": "C75",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/module-and-feature-entitlement",
   "component": "apps/ticvai-web/src/routes/general/ModuleAndFeatureEntitlementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-011"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-012"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "ADM-012",
     "trigger": "Tenant Isolation & Resource Pool",
     "provenance": "flow F96 step 4→5"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    },
    {
     "to": "BO-074",
     "trigger": "Finance sets the chart of accounts",
     "provenance": "flow F16 step 4→5",
     "operation": "getTenantLicences",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: BO-074. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: generateInvoice, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: createTenant, provisionCell, reactivateTenant, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getTenantLicences` reads one of them — list, select, act",
  "purpose": "See module & feature entitlement for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementUsage",
    "why": "**5 declared operations reach no component on this screen**: getEntitlementUsage, getSsoConfig, getSubscription, getTenant, listTenants. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every module feature entitlement",
       "bindsTo": "Cell",
       "columns": [
        "Cell.id",
        "Cell.name",
        "Cell.kind",
        "Cell.clusterId",
        "Cell.isReachable",
        "Cell.lastContactAt",
        "Cell.licenceExpiresAt",
        "Cell.participatesInCrossCell",
        "Cell.regionId",
        "Cell.regionName",
        "Cell.countryCode",
        "Cell.tier"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected module feature entitlement",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add",
       "operation": "addLicenceAddOn",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove",
       "operation": "removeLicenceAddOn",
       "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "addLicenceAddOn",
       "label": "Add licence add on",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listTenantCells",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
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
       "impliedBy": "addLicenceAddOn",
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
    "body": "**Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A module feature entitlement this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
   }
  ],
  "states": {
   "loading": "The module feature entitlement list.",
   "error": "Could not load. Names which read failed and leaves the module feature entitlement untouched.",
   "emptyFirstRun": "No module feature entitlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the module feature entitlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTenantLicences",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "addLicenceAddOn",
    "contract": "subscription",
    "purpose": "License a module outside the plan",
    "trigger": "onAction",
    "invalidates": [
     "listTenantCells"
    ]
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
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
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "List tenants",
    "trigger": "onLoad"
   },
   {
    "operationId": "removeLicenceAddOn",
    "contract": "subscription",
    "purpose": "Remove an add-on",
    "trigger": "onAction",
    "invalidates": [
     "listTenantCells"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "ADM-002"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "LicencePosition.planId",
    "LicencePosition.licensedModules",
    "LicencePosition.limits"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-008",
  "name": "Subscription & Plan Management",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 1,
  "capability": "C74",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/subscription-and-plan-management",
   "component": "apps/ticvai-web/src/routes/general/SubscriptionAndPlanManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-005"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-011"
   ],
   "transitions": [
    {
     "to": "ADM-011",
     "trigger": "Licence & Seat Management",
     "provenance": "flow F96 step 2→3"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPlans` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "Find subscription & plan management for this venue.",
  "gaps": [
   {
    "operation": "getPlan",
    "why": "**10 declared operations reach no component on this screen**: getPlan, getSsoConfig, getSubscription, getTenant, getTenantLicences, getUsageMetering, listSubscriptionInvoices, listTenantCells. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every subscription plan",
       "bindsTo": "Plan",
       "columns": [
        "Plan.code",
        "Plan.name",
        "Plan.description",
        "Plan.cellTier",
        "Plan.licensedModules",
        "Plan.limits",
        "Plan.basePrice",
        "Plan.billingPeriod",
        "Plan.includesBrandedApp",
        "Plan.includedAiTokens",
        "Plan.id",
        "Plan.isActive"
       ],
       "operation": "listPlans",
       "provenance": "contract subscription.yaml GET /plans"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected subscription plan",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
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
       "operation": "setSubscription",
       "provenance": "contract subscription.yaml PUT /tenants/{tenantId}/subscription"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPlan",
       "provenance": "contract subscription.yaml POST /plans"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPlanVersion",
       "provenance": "contract subscription.yaml POST /plans/{planId}"
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
       "label": "Create",
       "operation": "createPartnerAgreement",
       "provenance": "contract subscription.yaml POST /partner-agreements"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePartnerAgreement",
       "provenance": "contract subscription.yaml PATCH /partner-agreements/{agreementId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The subscription plan list.",
   "error": "Could not load. Names which read failed and leaves the subscription plan untouched.",
   "emptyFirstRun": "No subscription plan yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription plan are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPlans",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "setSubscription",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPlan",
    "contract": "subscription",
    "purpose": "Create a subscription plan",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "createPlanVersion",
    "contract": "subscription",
    "purpose": "Publish a new version of a plan",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "generateInvoice",
    "contract": "subscription",
    "purpose": "Generate an invoice for a period",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPlan",
    "contract": "subscription",
    "purpose": "Read a plan",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
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
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "List tenants",
    "trigger": "onLoad"
   },
   {
    "operationId": "previewSubscriptionChange",
    "contract": "subscription",
    "purpose": "Preview the effect of a plan change",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "listPartnerAgreements",
    "contract": "subscription",
    "purpose": "Commercial agreements with B2B partners",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPartnerAgreement",
    "contract": "subscription",
    "purpose": "Agree commercial terms with a partner",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "updatePartnerAgreement",
    "contract": "subscription",
    "purpose": "Amend, suspend or terminate",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "agreementId",
     "from": "deepLink"
    },
    {
     "name": "planId",
     "from": "deepLink"
    },
    {
     "name": "tenantId",
     "from": "ADM-002"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `agreementId`, `planId`.",
   "preloaded": [
    "EntitlementUsage.metrics",
    "EntitlementUsage.asAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 19 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-009",
  "name": "Tenant Billing & Invoicing",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C74",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/tenant-billing-and-invoicing",
   "component": "apps/ticvai-web/src/routes/general/TenantBillingAndInvoicingDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003"
   ],
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
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: getUsageMetering, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSubscriptionInvoices` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "Find tenant billing & invoicing for this venue.",
  "gaps": [
   {
    "operation": "getSsoConfig",
    "why": "**6 declared operations reach no component on this screen**: getSsoConfig, getSubscription, getTenant, getTenantLicences, listTenantCells, listTenants. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every tenant billing invoicing",
       "bindsTo": "SubscriptionInvoice",
       "columns": [
        "SubscriptionInvoice.id",
        "SubscriptionInvoice.invoiceNumber",
        "SubscriptionInvoice.periodStart",
        "SubscriptionInvoice.periodEnd",
        "SubscriptionInvoice.status",
        "SubscriptionInvoice.lines",
        "SubscriptionInvoice.subtotal",
        "SubscriptionInvoice.taxAmount",
        "SubscriptionInvoice.total",
        "SubscriptionInvoice.planVersionUsed",
        "SubscriptionInvoice.issuedAt",
        "SubscriptionInvoice.dueAt"
       ],
       "operation": "listSubscriptionInvoices",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/invoices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected tenant billing invoicing",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Generate",
       "operation": "generateInvoice",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/invoices"
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
       "impliedBy": "listSubscriptionInvoices",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "generateInvoice",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant billing invoicing list.",
   "error": "Could not load. Names which read failed and leaves the tenant billing invoicing untouched.",
   "emptyFirstRun": "No tenant billing invoicing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant billing invoicing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSubscriptionInvoices",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "generateInvoice",
    "contract": "subscription",
    "purpose": "Generate an invoice for a period",
    "trigger": "onAction",
    "invalidates": [
     "listSubscriptionInvoices"
    ]
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
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
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "List tenants",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "ADM-002"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "EntitlementUsage.metrics",
    "EntitlementUsage.asAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-009"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-010",
  "name": "Usage Metering",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C74",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/usage-metering",
   "component": "apps/ticvai-web/src/routes/general/UsageMeteringDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003"
   ],
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
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getUsageMetering` reads one of them — list, select, act",
  "purpose": "See usage metering for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementUsage",
    "why": "**5 declared operations reach no component on this screen**: getEntitlementUsage, getSsoConfig, getTenant, getTenantLicences, listTenants. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every usage metering",
       "bindsTo": "Cell",
       "columns": [
        "Cell.id",
        "Cell.name",
        "Cell.kind",
        "Cell.clusterId",
        "Cell.isReachable",
        "Cell.lastContactAt",
        "Cell.licenceExpiresAt",
        "Cell.participatesInCrossCell",
        "Cell.regionId",
        "Cell.regionName",
        "Cell.countryCode",
        "Cell.tier"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected usage metering",
       "bindsTo": "UsageReport",
       "columns": [
        "UsageReport.periodStart",
        "UsageReport.periodEnd",
        "UsageReport.metrics"
       ],
       "operation": "getUsageMetering",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/usage"
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
       "impliedBy": "listTenantCells",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The usage metering list.",
   "error": "Could not load. Names which read failed and leaves the usage metering untouched.",
   "emptyFirstRun": "No usage metering yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the usage metering are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getUsageMetering",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
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
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "List tenants",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "ADM-002"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "UsageReport.periodStart",
    "UsageReport.periodEnd",
    "UsageReport.metrics"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-010"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-011",
  "name": "Licence & Seat Management",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C75",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/licence-and-seat-management",
   "component": "apps/ticvai-web/src/routes/general/LicenceAndSeatManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-008",
    "ADM-015"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-007"
   ],
   "transitions": [
    {
     "to": "ADM-007",
     "trigger": "Module & Feature Entitlement",
     "provenance": "flow F96 step 3→4"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    },
    {
     "to": "PTR-020",
     "trigger": "Sub-Agent Management",
     "provenance": "flow F105 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getUsageMetering, listSubscriptionInvoices. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: createTenant, provisionCell, reactivateTenant, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "See licence & seat management for this venue.",
  "gaps": [
   {
    "operation": "getSsoConfig",
    "why": "**5 declared operations reach no component on this screen**: getSsoConfig, getSubscription, getTenant, getTenantLicences, listTenants. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every licence seat",
       "bindsTo": "Cell",
       "columns": [
        "Cell.id",
        "Cell.name",
        "Cell.kind",
        "Cell.clusterId",
        "Cell.isReachable",
        "Cell.lastContactAt",
        "Cell.licenceExpiresAt",
        "Cell.participatesInCrossCell",
        "Cell.regionId",
        "Cell.regionName",
        "Cell.countryCode",
        "Cell.tier"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected licence seat",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add",
       "operation": "addLicenceAddOn",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "secondaryButton",
       "label": "Preview",
       "operation": "previewSubscriptionChange",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/subscription/preview"
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
    "body": "**Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A licence seat this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
   }
  ],
  "states": {
   "loading": "The licence seat list.",
   "error": "Could not load. Names which read failed and leaves the licence seat untouched.",
   "emptyFirstRun": "No licence seat yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the licence seat are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "addLicenceAddOn",
    "contract": "subscription",
    "purpose": "License a module outside the plan",
    "trigger": "onAction",
    "invalidates": [
     "listTenantCells"
    ]
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
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
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "List tenants",
    "trigger": "onLoad"
   },
   {
    "operationId": "previewSubscriptionChange",
    "contract": "subscription",
    "purpose": "Preview the effect of a plan change",
    "trigger": "onAction",
    "invalidates": [
     "listTenantCells"
    ]
   },
   {
    "operationId": "removeLicenceAddOn",
    "contract": "subscription",
    "purpose": "Remove an add-on",
    "trigger": "onAction",
    "invalidates": [
     "listTenantCells"
    ]
   },
   {
    "operationId": "setSubscription",
    "contract": "subscription",
    "purpose": "Assign or change a subscription",
    "trigger": "onAction",
    "invalidates": [
     "listTenantCells"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "ADM-002"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "EntitlementUsage.metrics",
    "EntitlementUsage.asAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-011"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-012",
  "name": "Tenant Isolation & Resource Pool",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 1,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/tenant-isolation-and-resource-pool",
   "component": "apps/ticvai-web/src/routes/general/TenantIsolationAndResourcePoolDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-007"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-006",
    "ADM-013"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "ADM-006",
     "trigger": "Builds the scope tree",
     "provenance": "flow F16 step 2→3"
    },
    {
     "to": "ADM-013",
     "trigger": "Tenant Performance Monitor",
     "provenance": "flow F97 step 1→2"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "Work with tenant isolation & resource pool for this venue.",
  "gaps": [
   {
    "operation": "getSsoConfig",
    "why": "**5 declared operations reach no component on this screen**: getSsoConfig, getTenant, getTenantLicences, listTenants, getCellCapacity. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every tenant isolation resource",
       "bindsTo": "Cell",
       "columns": [
        "Cell.id",
        "Cell.name",
        "Cell.kind",
        "Cell.clusterId",
        "Cell.isReachable",
        "Cell.lastContactAt",
        "Cell.licenceExpiresAt",
        "Cell.participatesInCrossCell",
        "Cell.regionId",
        "Cell.regionName",
        "Cell.countryCode",
        "Cell.tier"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected tenant isolation resource",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Provision",
       "operation": "provisionCell",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/cells"
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
       "impliedBy": "listTenantCells",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "provisionCell",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant isolation resource list.",
   "error": "Could not load. Names which read failed and leaves the tenant isolation resource untouched.",
   "emptyFirstRun": "No tenant isolation resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant isolation resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "provisionCell",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
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
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "List tenants",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCellCapacity",
    "contract": "subscription",
    "purpose": "Load against headroom",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cellId",
     "from": "deepLink"
    },
    {
     "name": "tenantId",
     "from": "ADM-002"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `cellId`.",
   "preloaded": [
    "EntitlementUsage.metrics",
    "EntitlementUsage.asAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-012"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-015",
  "name": "API Rate Limit & Quota Management",
  "module": "Tenants & Licensing",
  "requiresModule": "membership",
  "wave": 3,
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/api-rate-limit-and-quota-management",
   "component": "apps/ticvai-web/src/routes/general/ApiRateLimitAndQuotaManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-011"
   ],
   "transitions": [
    {
     "to": "ADM-011",
     "trigger": "Licence & Seat Management",
     "provenance": "flow F105 step 1→2"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **`setApiQuota` wired 24 August.** This screen is named *API Rate Limit & Quota Management* and **declared no quota operation at all** — it carried nine subscription operations and six tenant-lifecycle ones instead. **The screen for the job could not do the job**, and only writing F105 against it surfaced that.",
  "openQuestions": [
   "Blocked — Developer & API workshop"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getTenantLicences` reads one of them — list, select, act",
  "purpose": "See api rate limit & quota management for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementUsage",
    "why": "**6 declared operations reach no component on this screen**: getEntitlementUsage, getSsoConfig, getTenant, listTenants, getApiUsage, listApiClients. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every api rate limit",
       "bindsTo": "Cell",
       "columns": [
        "Cell.id",
        "Cell.name",
        "Cell.kind",
        "Cell.clusterId",
        "Cell.isReachable",
        "Cell.lastContactAt",
        "Cell.licenceExpiresAt",
        "Cell.participatesInCrossCell",
        "Cell.regionId",
        "Cell.regionName",
        "Cell.countryCode",
        "Cell.tier"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected api rate limit",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
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
       "operation": "setApiQuota",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The api rate limit list.",
   "error": "Could not load. Names which read failed and leaves the api rate limit untouched.",
   "emptyFirstRun": "No api rate limit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the api rate limit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTenantLicences",
    "contract": "subscription",
    "purpose": "What a tenant is licensed to use",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTenant",
    "contract": "subscription",
    "purpose": "Read a tenant with cells and subscription",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "List tenants",
    "trigger": "onLoad"
   },
   {
    "operationId": "setApiQuota",
    "contract": "public-api",
    "purpose": "Rate limits and throttling per client",
    "trigger": "onAction",
    "invalidates": [
     "listTenantCells"
    ]
   },
   {
    "operationId": "getApiUsage",
    "contract": "public-api",
    "purpose": "Calls, errors, latency and success rate",
    "trigger": "onLoad"
   },
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "Registered clients for this developer",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "ADM-002"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "LicencePosition.planId",
    "LicencePosition.licensedModules",
    "LicencePosition.limits"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-015"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "createPartnerAgreement": {
  "method": "POST",
  "path": "/partner-agreements",
  "contract": "subscription",
  "summary": "Agree commercial terms with a partner",
  "permission": "PARTNER_MANAGE",
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
  "requestBody": "PartnerAgreement",
  "responds": "PartnerAgreement"
 },
 "createPlan": {
  "method": "POST",
  "path": "/plans",
  "contract": "subscription",
  "summary": "Create a subscription plan",
  "permission": "PLATFORM_PLAN_MANAGE",
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
  "requestBody": "CreatePlanRequest",
  "responds": "Plan"
 },
 "createPlanVersion": {
  "method": "POST",
  "path": "/plans/{planId}",
  "contract": "subscription",
  "summary": "Publish a new version of a plan",
  "permission": "PLATFORM_PLAN_MANAGE",
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
  "requestBody": "CreatePlanRequest",
  "responds": "Plan"
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
 "getCellCapacity": {
  "method": "GET",
  "path": "/cells/{cellId}/capacity",
  "contract": "subscription",
  "summary": "Load against headroom",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "window",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CellCapacity"
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
 "getPlan": {
  "method": "GET",
  "path": "/plans/{planId}",
  "contract": "subscription",
  "summary": "Read a plan",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Plan"
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
 "listOrgUnits": {
  "method": "GET",
  "path": "/org-units",
  "contract": "tenancy",
  "summary": "List scope nodes visible to the session",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "under",
    "in": "query",
    "required": null
   },
   {
    "name": "level",
    "in": "query",
    "required": null
   },
   {
    "name": "includeInactive",
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
 "listPartnerAgreements": {
  "method": "GET",
  "path": "/partner-agreements",
  "contract": "subscription",
  "summary": "Commercial agreements with B2B partners",
  "permission": "PARTNER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "expiringWithinDays",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PartnerAgreement"
 },
 "listPlans": {
  "method": "GET",
  "path": "/plans",
  "contract": "subscription",
  "summary": "List subscription plans",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Plan"
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
 "updatePartnerAgreement": {
  "method": "PATCH",
  "path": "/partner-agreements/{agreementId}",
  "contract": "subscription",
  "summary": "Amend, suspend or terminate",
  "permission": "PARTNER_MANAGE",
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
  "requestBody": "PartnerAgreement",
  "responds": "PartnerAgreement"
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
    "format": "uuid"
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
    "description": "**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing.\n",
    "items": {
     "type": "string"
    }
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
    "description": "13.1.38. Optional, and the strongest control available where an integrator has fixed egress.",
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
    ]
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
   }
  }
 },
 "ApiQuota": {
  "type": "object",
  "x-ticvai-persistence": "control.api_quota",
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
 "CellCapacity": {
  "type": "object",
  "x-ticvai-persistence": "none — measured, not stored",
  "required": [
   "cellId",
   "isConstrained",
   "dimensions",
   "measuredAt"
  ],
  "properties": {
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/CellKind"
   },
   "tenantCount": {
    "type": "integer",
    "description": "Reported, and **deliberately not the sizing signal.** Forty quiet tenants may load a cell less than three busy ones.\n"
   },
   "isConstrained": {
    "type": "boolean"
   },
   "constrainedDimension": {
    "type": "string",
    "nullable": true
   },
   "dimensions": {
    "type": "array",
    "description": "Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both.\n",
    "items": {
     "type": "object",
     "required": [
      "dimension",
      "used",
      "headroom"
     ],
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "concurrentUsers",
        "transactionsPerSecond",
        "scansPerSecond",
        "databaseConnections",
        "storageGb",
        "replicationLag",
        "cpu"
       ]
      },
      "used": {
       "type": "number"
      },
      "limit": {
       "type": "number"
      },
      "headroom": {
       "type": "number",
       "description": "Fraction remaining. Negative means already over."
      },
      "peakAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "forecastBreachAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats an invented date.\n"
   },
   "measuredAt": {
    "type": "string",
    "format": "date-time"
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
 "CreatePlanRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "cellTier",
   "licensedModules",
   "limits",
   "basePrice"
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
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "cellTier": {
    "$ref": "#/components/schemas/CellTier"
   },
   "licensedModules": {
    "type": "array",
    "minItems": 1,
    "description": "**A closed set as of 24 August.** `moduleKey` was a free string, so nothing could join a licence to a screen — **a tenant without an F&B licence was still served every F&B screen**, because no screen said which module it belonged to in a form the licence could match.\n**The key is the join.** `screen.requiresModule` names one of these, and navigation is built from the intersection of what a tenant licensed and what their role permits.\n",
    "items": {
     "$ref": "#/components/schemas/ModuleKey"
    }
   },
   "limits": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/EntitlementLimit"
    }
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingPeriod": {
    "type": "string",
    "enum": [
     "monthly",
     "quarterly",
     "annual"
    ]
   },
   "includesBrandedApp": {
    "type": "boolean",
    "description": "Branded native publishing carries per-tenant operational cost and is priced, not absorbed.\n"
   },
   "includedAiTokens": {
    "type": "integer",
    "nullable": true
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
 "ModuleKey": {
  "type": "string",
  "description": "What a tenant buys, and what a screen belongs to. **One vocabulary for both sides of the join**, because two lists that must agree are one list somebody forgets to update.\n**Grain chosen to match how a venue buys, not how the package is built.** `fnb` is one module even though it spans four contracts; `ticketing` and `access` are separate because a venue can run a museum with no gates and a stadium with no shop.\n",
  "enum": [
   "core",
   "ticketing",
   "access",
   "fnb",
   "retail",
   "inventory",
   "seating",
   "membership",
   "marketing",
   "resources",
   "queue",
   "games",
   "maintenance",
   "accreditation",
   "partner",
   "developerApi",
   "analytics",
   "ai"
  ],
  "x-ticvai-note": "**`core` is listed and cannot be unlicensed.** It exists so a screen can say it belongs to no optional module rather than leaving the field empty — **an empty field and *always on* look identical, and only one of them is a decision.**\n"
 },
 "OrgUnit": {
  "x-ticvai-persistence": "platform.org_unit",
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
 "PartnerAgreement": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_agreement",
  "required": [
   "partnerId",
   "rateMode",
   "validFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid"
   },
   "partnerName": {
    "type": "string",
    "readOnly": true
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "**Amending creates a version.** An order placed last week was placed under last week's rate, and settlement must be able to say which.\n"
   },
   "status": {
    "$ref": "#/components/schemas/PartnerAgreementStatus"
   },
   "rateMode": {
    "$ref": "#/components/schemas/PartnerRateMode"
   },
   "commissionPercent": {
    "type": "number",
    "nullable": true
   },
   "volumeTiers": {
    "type": "array",
    "description": "2.7.57. **A tier that changes at a threshold needs the sale to look back at cumulative volume, and nothing did.** Flat net rates and per-channel price lists cover the simple case and stop there.\n**The window is the argument, not the tier.** A partner who sells 400 in January and 400 in February is either a 400-tier partner twice or an 800-tier partner once, and the two are different money. `volumeWindow` says which.\n",
    "items": {
     "type": "object",
     "required": [
      "fromUnits",
      "commissionPercent"
     ],
     "properties": {
      "fromUnits": {
       "type": "integer"
      },
      "commissionPercent": {
       "type": "number"
      },
      "appliesRetrospectively": {
       "type": "boolean",
       "default": false,
       "description": "**Whether crossing a tier reprices what came before it.** Retrospective is what a partner assumes and prospective is what a venue budgets for — it has to be stated.\n"
      }
     }
    }
   },
   "volumeWindow": {
    "type": "string",
    "nullable": true,
    "enum": [
     "calendarMonth",
     "calendarQuarter",
     "calendarYear",
     "agreementYear",
     "rolling12Months"
    ]
   },
   "seasonalRates": {
    "type": "array",
    "description": "Rates that change by date range. **Separate from the volume tier because they compound** — a peak-season rate at a high volume tier is both, and a single rate table cannot say so.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date"
      },
      "to": {
       "type": "string",
       "format": "date"
      },
      "commissionPercent": {
       "type": "number"
      }
     }
    }
   },
   "segmentTier": {
    "type": "string",
    "nullable": true
   },
   "brandingAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "2.7.x, BL-078. **A reseller selling a venue's tickets under their own brand is a second scope level white-label does not have** — `BrandIdentity` and `setTheme` are tenant-scoped throughout.\n**Co-branding rather than replacement.** The venue's identity stays on the ticket because the ticket admits to the venue; the partner's sits beside it.\n"
   },
   "storefrontSubdomain": {
    "type": "string",
    "nullable": true
   },
   "sponsorship": {
    "type": "object",
    "nullable": true,
    "description": "BL-050. **Sponsorship inventory is sellable capacity of a different kind** — logo placements, hospitality allocations, naming rights. It is closer to a partner agreement than to a product: **a sponsor buys a relationship for a season, not a ticket for a date.**\nModelled here rather than as a `ProductKind` because the commercial terms — the term, the exclusivity, the settlement — are the agreement's, and duplicating them onto a product would mean two places to disagree.\n",
    "properties": {
     "placements": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "surface": {
         "type": "string",
         "enum": [
          "signage",
          "ticketFace",
          "appBanner",
          "emailFooter",
          "venueNaming",
          "zoneNaming",
          "uniform",
          "printedMap"
         ]
        },
        "quantity": {
         "type": "integer"
        },
        "exclusive": {
         "type": "boolean",
         "default": false,
         "description": "**Exclusivity is the expensive word.** A sponsor paying for category exclusivity has bought the absence of a competitor, and a second agreement breaching it is a legal problem rather than a scheduling one.\n"
        }
       }
      }
     },
     "hospitalityAllocation": {
      "type": "integer",
      "nullable": true,
      "description": "Tickets or cabanas included. **Issued as invitations, not sales** — no revenue attaches."
     },
     "categoryExclusivity": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "netRates": {
    "type": "array",
    "description": "Per product or category. Absent means the commission applies across the catalogue.",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "categoryId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "netPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "maxDiscountPercent": {
       "type": "number",
       "nullable": true,
       "description": "1.6.10. **What the partner may not undercut.** A reseller selling below the venue's own price damages the direct channel, and the venue usually cares more about that than the margin.\n"
      }
     }
    }
   },
   "creditTermDays": {
    "type": "integer",
    "description": "2.7.36. Net 30, net 60. Drives when an invoice becomes overdue."
   },
   "acceptedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-079. **Electronic acceptance against a version**, following the `signatureRef` precedent. An agreement accepted with no version recorded is an agreement nobody can produce in a dispute.\n"
   },
   "acceptedVersion": {
    "type": "integer",
    "nullable": true
   },
   "acceptedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "corporateAllocations": {
    "type": "array",
    "description": "BL-035. **`PartnerAgreement` covered commercial terms and not allocations.** A corporate account with fifty places for its staff is the same structure as a reseller with fifty to sell, and **the difference is that a corporate member does not pay.**\n",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer"
      },
      "usedQuantity": {
       "type": "integer",
       "readOnly": true
      },
      "perMemberLimit": {
       "type": "integer",
       "nullable": true
      },
      "validTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "settlementCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "**The currency this partner is billed and settles in**, which is often not the venue's. A UK tour operator selling a Dubai attraction is invoiced in GBP against sales booked in AED, and the difference is somebody's exposure.\n**`creditLimit` and `netRates` are expressed in this currency**, not the venue's — a limit in the wrong currency is a limit that moves with the exchange rate.\n"
   },
   "fxPolicy": {
    "type": "string",
    "enum": [
     "rateAtSale",
     "rateAtInvoice",
     "fixedRate"
    ],
    "default": "rateAtSale",
    "description": "**Which rate converts a sale into the settlement currency, and it is a commercial term.** `rateAtSale` puts the movement on the partner; `rateAtInvoice` puts it on the venue; `fixedRate` puts it on whoever guessed wrong when the agreement was signed.\n**Not a default to leave alone** — on a monthly statement across a moving rate the three produce materially different numbers, and the partner will have assumed one of them.\n"
   },
   "fixedRate": {
    "type": "number",
    "nullable": true,
    "description": "Where `fxPolicy` is `fixedRate`. **An amendment creates a version** so an old statement stays readable."
   },
   "creditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "allowedChannels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresApprovalAboveValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "2.7.39. Routes through `approvals` rather than a second mechanism here."
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "2.7.37. **An agreement that lapses silently keeps selling at rates nobody agreed to**, discovered at settlement rather than at sale. Null means open-ended, which should be rare and deliberate.\n"
   },
   "expiryAlertDays": {
    "type": "integer",
    "default": 30
   },
   "approvalRequestId": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "notes": {
    "type": "string"
   }
  }
 },
 "PartnerAgreementStatus": {
  "type": "string",
  "enum": [
   "pendingApproval",
   "active",
   "expiringSoon",
   "expired",
   "suspended",
   "terminated"
  ]
 },
 "PartnerRateMode": {
  "type": "string",
  "description": "**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n",
  "enum": [
   "netRate",
   "commission"
  ]
 },
 "Plan": {
  "x-ticvai-persistence": "control.subscription_plan",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreatePlanRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "isActive",
     "subscriberCount"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "version": {
      "type": "string",
      "description": "Existing subscribers stay on the version they were sold. A price change never applies retroactively.\n"
     },
     "isActive": {
      "type": "boolean"
     },
     "subscriberCount": {
      "type": "integer"
     },
     "publishedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
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
 "ScopeLevel": {
  "type": "string",
  "description": "**The eight organisational levels, and the shared copy of them.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition and this mirrors it so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n",
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
 }
}
```
