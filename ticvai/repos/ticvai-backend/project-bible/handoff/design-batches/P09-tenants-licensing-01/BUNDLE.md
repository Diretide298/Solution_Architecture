# P09-tenants-licensing-01 — P09 · Tenants & Licensing

**9 screens · 40 operations · 46 schemas · 15 permissions**

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

- **Every control that can be refused must be gated.** 15 permissions apply here:
  `DEVELOPER_ADMIN, DEVELOPER_VIEW, PARTNER_MANAGE, PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_TERMINATE, PLATFORM_TENANT_VIEW`…. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-005` | Tenant Directory | listDetail | 16 | 9 | — |
| `ADM-006` | Tenant Hierarchy Explorer | listDetail | 9 | 2 | — |
| `ADM-007` | Module & Feature Entitlement | listDetail | 9 | 2 | — |
| `ADM-008` | Subscription & Plan Management | listDetail | 19 | 7 | — |
| `ADM-009` | Tenant Billing & Invoicing | listDetail | 10 | 1 | — |
| `ADM-010` | Usage Metering | listDetail | 7 | 0 | — |
| `ADM-011` | Licence & Seat Management | listDetail | 11 | 4 | — |
| `ADM-012` | Tenant Isolation & Resource Pool | listDetail | 8 | 1 | — |
| `ADM-015` | API Rate Limit & Quota Management | listDetail | 13 | 3 | — |

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
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-005 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-005 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-005 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-008",
     "trigger": "Subscription & Plan Management",
     "provenance": "flow F96 step 1→2",
     "carries": [
      "planId",
      "tenantId"
     ]
    },
    {
     "to": "ADM-012",
     "trigger": "Provisions or assigns a cell",
     "provenance": "flow F16 step 1→2",
     "carries": [
      "cellId",
      "tenantId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenants` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "Find the right one quickly, and act on it without opening it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
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
       "kind": "textField",
       "label": "Status",
       "operation": "listTenants",
       "notes": "Sends `?status=` to `listTenants`.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "textField",
       "label": "Plan id",
       "operation": "listTenants",
       "notes": "Sends `?planId=` to `listTenants`.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every cell",
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
       "label": "The selected tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status",
        "Tenant.suspensionMode",
        "Tenant.suspensionReason",
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId",
        "Tenant.planId",
        "Tenant.planName",
        "Tenant.cellCount",
        "Tenant.venueCount"
       ],
       "operation": "listTenants",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
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
       "label": "Add licence add on",
       "operation": "addLicenceAddOn",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "secondaryButton",
       "label": "Create tenant",
       "operation": "createTenant",
       "provenance": "contract subscription.yaml POST /tenants"
      },
      {
       "kind": "secondaryButton",
       "label": "Provision cell",
       "operation": "provisionCell",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/cells"
      },
      {
       "kind": "secondaryButton",
       "label": "Reactivate tenant",
       "operation": "reactivateTenant",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/reactivate"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove licence add on",
       "operation": "removeLicenceAddOn",
       "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "secondaryButton",
       "label": "Save SSO config",
       "operation": "setSsoConfig",
       "provenance": "contract identity.yaml PUT /tenants/sso-config"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend tenant",
       "operation": "suspendTenant",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/suspend"
      },
      {
       "kind": "destructiveButton",
       "label": "Terminate tenant",
       "operation": "terminateTenant",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/terminate"
      },
      {
       "kind": "secondaryButton",
       "label": "Save tenant",
       "operation": "updateTenant",
       "provenance": "contract subscription.yaml PATCH /tenants/{tenantId}"
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
    "body": "**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client ULID), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.",
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
    "id": "confirmRemoveLicenceAddOn",
    "component": "confirmDialog",
    "trigger": "Remove licence add on",
    "body": "**Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted. **Collects what `removeLicenceAddOn` sends before it is called.** Required: `moduleKey`, `reason`.",
    "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
   },
   {
    "id": "confirmSuspendTenant",
    "component": "confirmDialog",
    "trigger": "Suspend tenant",
    "body": "**Names what `suspendTenant` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted. **Collects what `suspendTenant` sends before it is called.** Required: `mode`, `reason`. Optional: `effectiveAt`, `noticeMessage`.",
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/suspend"
   },
   {
    "id": "confirmTerminateTenant",
    "component": "confirmDialog",
    "trigger": "Terminate tenant",
    "body": "**Names what `terminateTenant` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted. **Collects what `terminateTenant` sends before it is called.** Required: `reason`, `retentionDays`, `confirmTenantCode`.",
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/terminate"
   },
   {
    "id": "formAddLicenceAddOn",
    "component": "modal",
    "trigger": "Add licence add on",
    "body": "**Collects what `addLicenceAddOn` sends before it is called.** Required: `moduleKey`. Optional: `limitOverrides`, `price`, `validFrom`, `validTo`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "LicenceAddOn",
    "confirm": {
     "label": "Add licence add on",
     "operation": "addLicenceAddOn"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "moduleKey",
      "limitOverrides",
      "price",
      "validFrom",
      "validTo",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
   },
   {
    "id": "formCreateTenant",
    "component": "modal",
    "trigger": "Create tenant",
    "body": "**Collects what `createTenant` sends before it is called.** Required: `code`, `name`, `billingEmail`. Optional: `billingAddress`, `accountManagerPrincipalId`, `planId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateTenantRequest",
    "confirm": {
     "label": "Create tenant",
     "operation": "createTenant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "billingEmail",
      "billingAddress",
      "accountManagerPrincipalId",
      "planId"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants"
   },
   {
    "id": "formProvisionCell",
    "component": "modal",
    "trigger": "Provision cell",
    "body": "**Collects what `provisionCell` sends before it is called.** Required: `regionId`, `countryCode`, `tier`. Optional: `cloudProvider`, `cloudRegion`, `clientHostedEndpoint`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ProvisionCellRequest",
    "confirm": {
     "label": "Provision cell",
     "operation": "provisionCell"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "regionId",
      "countryCode",
      "tier",
      "cloudProvider",
      "cloudRegion",
      "clientHostedEndpoint"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/cells"
   },
   {
    "id": "formSetSsoConfig",
    "component": "modal",
    "trigger": "Save SSO config",
    "body": "**Collects what `setSsoConfig` sends before it is called.** Required: `id`, `displayName`, `protocol`, `groupMappings`. Optional: `metadataUrl`, `issuer`, `clientId`, `clientSecretRef`, `autoProvisionPrincipals`, `isEnforced`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SsoProviderConfig",
    "confirm": {
     "label": "Save SSO config",
     "operation": "setSsoConfig"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "displayName",
      "protocol",
      "groupMappings",
      "metadataUrl",
      "issuer",
      "clientId",
      "clientSecretRef",
      "autoProvisionPrincipals",
      "isEnforced",
      "isActive"
     ]
    },
    "provenance": "contract identity.yaml PUT /tenants/sso-config"
   },
   {
    "id": "formUpdateTenant",
    "component": "modal",
    "trigger": "Save tenant",
    "body": "**Collects what `updateTenant` sends before it is called.** Nothing in the body is required. Optional: `name`, `billingEmail`, `billingAddress`, `accountManagerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save tenant",
     "operation": "updateTenant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "billingEmail",
      "billingAddress",
      "accountManagerPrincipalId"
     ]
    },
    "provenance": "contract subscription.yaml PATCH /tenants/{tenantId}"
   }
  ],
  "states": {
   "loading": "The tenant list.",
   "error": "Could not load. Names which read failed and leaves the tenant untouched.",
   "emptyFirstRun": "No tenant yet. Offers Add licence add on (`addLicenceAddOn`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, planId and the tenant are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "Tenant.id",
    "Tenant.code",
    "Tenant.name",
    "Tenant.status",
    "Tenant.suspensionMode"
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
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-006 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-006 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-006 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-007",
     "trigger": "Enables the modules the tenant bought",
     "provenance": "flow F16 step 3→4",
     "carries": [
      "tenantId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenants` reads the population and `getSsoConfig` reads one of them — list, select, act",
  "purpose": "See tenant hierarchy explorer for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listTenants",
       "notes": "Sends `?status=` to `listTenants`.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "textField",
       "label": "Plan id",
       "operation": "listTenants",
       "notes": "Sends `?planId=` to `listTenants`.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every cell",
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
      },
      {
       "kind": "dataTable",
       "label": "Every org unit",
       "bindsTo": "OrgUnit",
       "columns": [
        "OrgUnit.id",
        "OrgUnit.level",
        "OrgUnit.parentId",
        "OrgUnit.path",
        "OrgUnit.code",
        "OrgUnit.name",
        "OrgUnit.isActive",
        "OrgUnit.childCount"
       ],
       "operation": "listOrgUnits",
       "provenance": "contract tenancy.yaml GET /org-units"
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
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status",
        "Tenant.suspensionMode",
        "Tenant.suspensionReason",
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId",
        "Tenant.planId",
        "Tenant.planName",
        "Tenant.cellCount",
        "Tenant.venueCount"
       ],
       "operation": "listTenants",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
       "label": "Save tenant",
       "operation": "updateTenant",
       "provenance": "contract subscription.yaml PATCH /tenants/{tenantId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create org unit",
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
   "emptyFirstRun": "No tenant hierarchy yet. Offers Create org unit (`createOrgUnit`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, planId and the tenant hierarchy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `USER_MANAGE`, which `getSsoConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "Tenant.id",
    "Tenant.code",
    "Tenant.name",
    "Tenant.status",
    "Tenant.suspensionMode"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-006"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formUpdateTenant",
    "component": "modal",
    "trigger": "Save tenant",
    "body": "**Collects what `updateTenant` sends before it is called.** Nothing in the body is required. Optional: `name`, `billingEmail`, `billingAddress`, `accountManagerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save tenant",
     "operation": "updateTenant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "billingEmail",
      "billingAddress",
      "accountManagerPrincipalId"
     ]
    },
    "provenance": "contract subscription.yaml PATCH /tenants/{tenantId}"
   },
   {
    "id": "formCreateOrgUnit",
    "component": "modal",
    "trigger": "Create org unit",
    "body": "**Collects what `createOrgUnit` sends before it is called.** Required: `level`, `parentId`, `code`, `name`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateScopeNodeRequest",
    "confirm": {
     "label": "Create org unit",
     "operation": "createOrgUnit"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "level",
      "parentId",
      "code",
      "name"
     ]
    },
    "provenance": "contract tenancy.yaml POST /org-units"
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
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-007 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-007 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-007 holds cellId, so an edge into it carries them"
    },
    {
     "to": "BO-074",
     "trigger": "Finance sets the chart of accounts",
     "provenance": "flow F16 step 4→5",
     "operation": "getTenantLicences",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "ADM-012",
     "trigger": "Tenant Isolation & Resource Pool",
     "provenance": "flow F96 step 4→5",
     "carries": [
      "cellId",
      "tenantId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: BO-074. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: generateInvoice, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: createTenant, provisionCell, reactivateTenant, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getTenantLicences` reads one of them — list, select, act",
  "purpose": "See module & feature entitlement for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell",
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
      },
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
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId"
       ],
       "operation": "listTenants",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
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
       "label": "The selected cell",
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
        "Cell.tier",
        "Cell.status",
        "Cell.cloudProvider",
        "Cell.cloudRegion",
        "Cell.apiEndpoint"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The subscription",
       "bindsTo": "Subscription",
       "columns": [
        "Subscription.planId",
        "Subscription.planName",
        "Subscription.planVersion",
        "Subscription.status",
        "Subscription.startsAt",
        "Subscription.renewsAt",
        "Subscription.cancelledAt",
        "Subscription.currentPrice",
        "Subscription.billingPeriod"
       ],
       "operation": "getSubscription",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/subscription"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
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
       "label": "Add licence add on",
       "operation": "addLicenceAddOn",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove licence add on",
       "operation": "removeLicenceAddOn",
       "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveLicenceAddOn",
    "component": "confirmDialog",
    "trigger": "Remove licence add on",
    "body": "**Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A module feature entitlement this affects should be identified in the dialog, not just counted. **Collects what `removeLicenceAddOn` sends before it is called.** Required: `moduleKey`, `reason`.",
    "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
   },
   {
    "id": "formAddLicenceAddOn",
    "component": "modal",
    "trigger": "Add licence add on",
    "body": "**Collects what `addLicenceAddOn` sends before it is called.** Required: `moduleKey`. Optional: `limitOverrides`, `price`, `validFrom`, `validTo`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "LicenceAddOn",
    "confirm": {
     "label": "Add licence add on",
     "operation": "addLicenceAddOn"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "moduleKey",
      "limitOverrides",
      "price",
      "validFrom",
      "validTo",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
   }
  ],
  "states": {
   "loading": "The module feature entitlement list.",
   "error": "Could not load. Names which read failed and leaves the module feature entitlement untouched.",
   "emptyFirstRun": "No module feature entitlement yet. Offers Add licence add on (`addLicenceAddOn`).",
   "emptyNoResults": "Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "Cell.id",
    "Cell.name",
    "Cell.kind",
    "Cell.clusterId",
    "Cell.isReachable"
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
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-008 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-008 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-008 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-011",
     "trigger": "Licence & Seat Management",
     "provenance": "flow F96 step 2→3",
     "carries": [
      "tenantId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPlans` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "Find subscription & plan management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every plan",
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
      },
      {
       "kind": "dataTable",
       "label": "Every subscription invoice",
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
      },
      {
       "kind": "dataTable",
       "label": "Every cell",
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
      },
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
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId"
       ],
       "operation": "listTenants",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "dataTable",
       "label": "Every partner agreement",
       "bindsTo": "PartnerAgreement",
       "columns": [
        "PartnerAgreement.id",
        "PartnerAgreement.partnerId",
        "PartnerAgreement.partnerName",
        "PartnerAgreement.status",
        "PartnerAgreement.rateMode",
        "PartnerAgreement.commissionPercent",
        "PartnerAgreement.volumeTiers",
        "PartnerAgreement.volumeWindow",
        "PartnerAgreement.seasonalRates",
        "PartnerAgreement.segmentTier",
        "PartnerAgreement.brandingAssetId",
        "PartnerAgreement.storefrontSubdomain"
       ],
       "operation": "listPartnerAgreements",
       "provenance": "contract subscription.yaml GET /partner-agreements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected plan",
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
        "Plan.isActive",
        "Plan.subscriberCount",
        "Plan.publishedAt"
       ],
       "operation": "getPlan",
       "provenance": "contract subscription.yaml GET /plans/{planId}"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The subscription",
       "bindsTo": "Subscription",
       "columns": [
        "Subscription.planId",
        "Subscription.planName",
        "Subscription.planVersion",
        "Subscription.status",
        "Subscription.startsAt",
        "Subscription.renewsAt",
        "Subscription.cancelledAt",
        "Subscription.currentPrice",
        "Subscription.billingPeriod"
       ],
       "operation": "getSubscription",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/subscription"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      },
      {
       "kind": "detailPanel",
       "label": "The usage report",
       "bindsTo": "UsageReport",
       "columns": [
        "UsageReport.periodStart",
        "UsageReport.periodEnd",
        "UsageReport.metrics"
       ],
       "operation": "getUsageMetering",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/usage"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
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
       "label": "Save subscription",
       "operation": "setSubscription",
       "provenance": "contract subscription.yaml PUT /tenants/{tenantId}/subscription"
      },
      {
       "kind": "secondaryButton",
       "label": "Create plan",
       "operation": "createPlan",
       "provenance": "contract subscription.yaml POST /plans"
      },
      {
       "kind": "secondaryButton",
       "label": "Create plan version",
       "operation": "createPlanVersion",
       "provenance": "contract subscription.yaml POST /plans/{planId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate invoice",
       "operation": "generateInvoice",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/invoices"
      },
      {
       "kind": "secondaryButton",
       "label": "Preview subscription change",
       "operation": "previewSubscriptionChange",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/subscription/preview"
      },
      {
       "kind": "secondaryButton",
       "label": "Create partner agreement",
       "operation": "createPartnerAgreement",
       "provenance": "contract subscription.yaml POST /partner-agreements"
      },
      {
       "kind": "secondaryButton",
       "label": "Save partner agreement",
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
   "emptyFirstRun": "No subscription plan yet. Offers Create plan (`createPlan`).",
   "emptyNoResults": "Never shown: `listPlans` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listPlans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
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
    "Plan.code",
    "Plan.name",
    "Plan.description",
    "Plan.cellTier",
    "Plan.licensedModules"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 19 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetSubscription",
    "component": "modal",
    "trigger": "Save subscription",
    "body": "**Collects what `setSubscription` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SetSubscriptionRequest",
    "confirm": {
     "label": "Save subscription",
     "operation": "setSubscription"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "planId",
      "planVersion",
      "effectiveFrom",
      "prorate",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml PUT /tenants/{tenantId}/subscription"
   },
   {
    "id": "formCreatePlan",
    "component": "modal",
    "trigger": "Create plan",
    "body": "**Collects what `createPlan` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePlanRequest",
    "confirm": {
     "label": "Create plan",
     "operation": "createPlan"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "cellTier",
      "licensedModules",
      "limits",
      "basePrice",
      "description",
      "billingPeriod",
      "includesBrandedApp",
      "includedAiTokens"
     ]
    },
    "provenance": "contract subscription.yaml POST /plans"
   },
   {
    "id": "formCreatePlanVersion",
    "component": "modal",
    "trigger": "Create plan version",
    "body": "**Collects what `createPlanVersion` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePlanRequest",
    "confirm": {
     "label": "Create plan version",
     "operation": "createPlanVersion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "cellTier",
      "licensedModules",
      "limits",
      "basePrice",
      "description",
      "billingPeriod",
      "includesBrandedApp",
      "includedAiTokens"
     ]
    },
    "provenance": "contract subscription.yaml POST /plans/{planId}"
   },
   {
    "id": "formGenerateInvoice",
    "component": "modal",
    "trigger": "Generate invoice",
    "body": "**Collects what `generateInvoice` sends before it is called.** Required: `periodStart`, `periodEnd`. Optional: `dryRun`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Generate invoice",
     "operation": "generateInvoice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "periodStart",
      "periodEnd",
      "dryRun"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/invoices"
   },
   {
    "id": "formPreviewSubscriptionChange",
    "component": "modal",
    "trigger": "Preview subscription change",
    "body": "**Collects what `previewSubscriptionChange` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SetSubscriptionRequest",
    "confirm": {
     "label": "Preview subscription change",
     "operation": "previewSubscriptionChange"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "planId",
      "planVersion",
      "effectiveFrom",
      "prorate",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/subscription/preview"
   },
   {
    "id": "formCreatePartnerAgreement",
    "component": "modal",
    "trigger": "Create partner agreement",
    "body": "**Collects what `createPartnerAgreement` sends before it is called.** Required: `partnerId`, `rateMode`, `validFrom`. Optional: `id`, `partnerName`, `status`, `commissionPercent`, `volumeTiers`, `volumeWindow`, `seasonalRates`, `segmentTier`, `brandingAssetId`, `storefrontSubdomain`, `sponsorship`, `netRates` and 17 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerAgreement",
    "confirm": {
     "label": "Create partner agreement",
     "operation": "createPartnerAgreement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "partnerId",
      "rateMode",
      "validFrom",
      "id",
      "partnerName",
      "status",
      "commissionPercent",
      "volumeTiers",
      "volumeWindow",
      "seasonalRates",
      "segmentTier",
      "brandingAssetId",
      "storefrontSubdomain",
      "sponsorship",
      "netRates",
      "creditTermDays",
      "acceptedByPrincipalId",
      "acceptedVersion"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-agreements"
   },
   {
    "id": "formUpdatePartnerAgreement",
    "component": "modal",
    "trigger": "Save partner agreement",
    "body": "**Collects what `updatePartnerAgreement` sends before it is called.** Required: `partnerId`, `rateMode`, `validFrom`. Optional: `id`, `partnerName`, `status`, `commissionPercent`, `volumeTiers`, `volumeWindow`, `seasonalRates`, `segmentTier`, `brandingAssetId`, `storefrontSubdomain`, `sponsorship`, `netRates` and 17 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerAgreement",
    "confirm": {
     "label": "Save partner agreement",
     "operation": "updatePartnerAgreement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "partnerId",
      "rateMode",
      "validFrom",
      "id",
      "partnerName",
      "status",
      "commissionPercent",
      "volumeTiers",
      "volumeWindow",
      "seasonalRates",
      "segmentTier",
      "brandingAssetId",
      "storefrontSubdomain",
      "sponsorship",
      "netRates",
      "creditTermDays",
      "acceptedByPrincipalId",
      "acceptedVersion"
     ]
    },
    "provenance": "contract subscription.yaml PATCH /partner-agreements/{agreementId}"
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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-009 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-009 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-009 holds cellId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: getUsageMetering, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSubscriptionInvoices` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "Find tenant billing & invoicing for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listSubscriptionInvoices",
       "notes": "Sends `?status=` to `listSubscriptionInvoices`.",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/invoices"
      },
      {
       "kind": "dataTable",
       "label": "Every subscription invoice",
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
      },
      {
       "kind": "dataTable",
       "label": "Every cell",
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
      },
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
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId"
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
       "label": "The selected subscription invoice",
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
        "SubscriptionInvoice.dueAt",
        "SubscriptionInvoice.paidAt"
       ],
       "operation": "listSubscriptionInvoices",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/invoices"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The subscription",
       "bindsTo": "Subscription",
       "columns": [
        "Subscription.planId",
        "Subscription.planName",
        "Subscription.planVersion",
        "Subscription.status",
        "Subscription.startsAt",
        "Subscription.renewsAt",
        "Subscription.cancelledAt",
        "Subscription.currentPrice",
        "Subscription.billingPeriod"
       ],
       "operation": "getSubscription",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/subscription"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
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
       "label": "Generate invoice",
       "operation": "generateInvoice",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/invoices"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant billing invoicing list.",
   "error": "Could not load. Names which read failed and leaves the tenant billing invoicing untouched.",
   "emptyFirstRun": "No tenant billing invoicing yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on status and the tenant billing invoicing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_BILLING_VIEW`, which `listSubscriptionInvoices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   },
   {
    "operationId": "listCreditNotes",
    "contract": "subscription",
    "purpose": "Credit notes beside the invoices",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
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
    "SubscriptionInvoice.id",
    "SubscriptionInvoice.invoiceNumber",
    "SubscriptionInvoice.periodStart",
    "SubscriptionInvoice.periodEnd",
    "SubscriptionInvoice.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-009"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formGenerateInvoice",
    "component": "modal",
    "trigger": "Generate invoice",
    "body": "**Collects what `generateInvoice` sends before it is called.** Required: `periodStart`, `periodEnd`. Optional: `dryRun`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Generate invoice",
     "operation": "generateInvoice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "periodStart",
      "periodEnd",
      "dryRun"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/invoices"
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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-010 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-010 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-010 holds cellId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getUsageMetering` reads one of them — list, select, act",
  "purpose": "See usage metering for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell",
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
      },
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
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId"
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
       "label": "The selected cell",
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
        "Cell.tier",
        "Cell.status",
        "Cell.cloudProvider",
        "Cell.cloudRegion",
        "Cell.apiEndpoint"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      },
      {
       "kind": "detailPanel",
       "label": "The usage report",
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
    }
   ]
  },
  "states": {
   "loading": "The usage metering list.",
   "error": "Could not load. Names which read failed and leaves the usage metering untouched.",
   "emptyFirstRun": "No usage metering yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getUsageMetering` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "Cell.id",
    "Cell.name",
    "Cell.kind",
    "Cell.clusterId",
    "Cell.isReachable"
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
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-011 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-011 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-011 holds cellId, so an edge into it carries them"
    },
    {
     "to": "PTR-020",
     "trigger": "Sub-Agent Management",
     "provenance": "flow F105 step 2→3",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "ADM-007",
     "trigger": "Module & Feature Entitlement",
     "provenance": "flow F96 step 3→4",
     "carries": [
      "tenantId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getUsageMetering, listSubscriptionInvoices. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: createTenant, provisionCell, reactivateTenant, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "See licence & seat management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell",
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
      },
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
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId"
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
       "label": "The selected cell",
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
        "Cell.tier",
        "Cell.status",
        "Cell.cloudProvider",
        "Cell.cloudRegion",
        "Cell.apiEndpoint"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The subscription",
       "bindsTo": "Subscription",
       "columns": [
        "Subscription.planId",
        "Subscription.planName",
        "Subscription.planVersion",
        "Subscription.status",
        "Subscription.startsAt",
        "Subscription.renewsAt",
        "Subscription.cancelledAt",
        "Subscription.currentPrice",
        "Subscription.billingPeriod"
       ],
       "operation": "getSubscription",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/subscription"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
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
       "label": "Add licence add on",
       "operation": "addLicenceAddOn",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "secondaryButton",
       "label": "Preview subscription change",
       "operation": "previewSubscriptionChange",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/subscription/preview"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove licence add on",
       "operation": "removeLicenceAddOn",
       "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
      },
      {
       "kind": "secondaryButton",
       "label": "Save subscription",
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
    "trigger": "Remove licence add on",
    "body": "**Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A licence seat this affects should be identified in the dialog, not just counted. **Collects what `removeLicenceAddOn` sends before it is called.** Required: `moduleKey`, `reason`.",
    "provenance": "contract subscription.yaml DELETE /tenants/{tenantId}/licences/add-ons"
   },
   {
    "id": "formAddLicenceAddOn",
    "component": "modal",
    "trigger": "Add licence add on",
    "body": "**Collects what `addLicenceAddOn` sends before it is called.** Required: `moduleKey`. Optional: `limitOverrides`, `price`, `validFrom`, `validTo`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "LicenceAddOn",
    "confirm": {
     "label": "Add licence add on",
     "operation": "addLicenceAddOn"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "moduleKey",
      "limitOverrides",
      "price",
      "validFrom",
      "validTo",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/licences/add-ons"
   },
   {
    "id": "formPreviewSubscriptionChange",
    "component": "modal",
    "trigger": "Preview subscription change",
    "body": "**Collects what `previewSubscriptionChange` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SetSubscriptionRequest",
    "confirm": {
     "label": "Preview subscription change",
     "operation": "previewSubscriptionChange"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "planId",
      "planVersion",
      "effectiveFrom",
      "prorate",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/subscription/preview"
   },
   {
    "id": "formSetSubscription",
    "component": "modal",
    "trigger": "Save subscription",
    "body": "**Collects what `setSubscription` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SetSubscriptionRequest",
    "confirm": {
     "label": "Save subscription",
     "operation": "setSubscription"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "planId",
      "planVersion",
      "effectiveFrom",
      "prorate",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml PUT /tenants/{tenantId}/subscription"
   }
  ],
  "states": {
   "loading": "The licence seat list.",
   "error": "Could not load. Names which read failed and leaves the licence seat untouched.",
   "emptyFirstRun": "No licence seat yet. Offers Add licence add on (`addLicenceAddOn`).",
   "emptyNoResults": "Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "Cell.id",
    "Cell.name",
    "Cell.kind",
    "Cell.clusterId",
    "Cell.isReachable"
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
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-012 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-012 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-012 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-006",
     "trigger": "Builds the scope tree",
     "provenance": "flow F16 step 2→3",
     "carries": [
      "tenantId"
     ]
    },
    {
     "to": "ADM-013",
     "trigger": "Tenant Performance Monitor",
     "provenance": "flow F97 step 1→2",
     "carries": [
      "cellId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTenantCells` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "Work with tenant isolation & resource pool for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell",
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
      },
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
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId"
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
       "label": "The selected cell",
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
        "Cell.tier",
        "Cell.status",
        "Cell.cloudProvider",
        "Cell.cloudRegion",
        "Cell.apiEndpoint"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      },
      {
       "kind": "detailPanel",
       "label": "The cell capacity",
       "bindsTo": "CellCapacity",
       "columns": [
        "CellCapacity.kind",
        "CellCapacity.tenantCount",
        "CellCapacity.isConstrained",
        "CellCapacity.constrainedDimension",
        "CellCapacity.dimensions",
        "CellCapacity.forecastBreachAt",
        "CellCapacity.measuredAt"
       ],
       "operation": "getCellCapacity",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/capacity"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
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
       "label": "Provision cell",
       "operation": "provisionCell",
       "provenance": "contract subscription.yaml POST /tenants/{tenantId}/cells"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant isolation resource list.",
   "error": "Could not load. Names which read failed and leaves the tenant isolation resource untouched.",
   "emptyFirstRun": "No tenant isolation resource yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "provisionCell",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onAction"
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
    "Cell.id",
    "Cell.name",
    "Cell.kind",
    "Cell.clusterId",
    "Cell.isReachable"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-012"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formProvisionCell",
    "component": "modal",
    "trigger": "Provision cell",
    "body": "**Collects what `provisionCell` sends before it is called.** Required: `regionId`, `countryCode`, `tier`. Optional: `cloudProvider`, `cloudRegion`, `clientHostedEndpoint`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ProvisionCellRequest",
    "confirm": {
     "label": "Provision cell",
     "operation": "provisionCell"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "regionId",
      "countryCode",
      "tier",
      "cloudProvider",
      "cloudRegion",
      "clientHostedEndpoint"
     ]
    },
    "provenance": "contract subscription.yaml POST /tenants/{tenantId}/cells"
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
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-015 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-015 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-015 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-011",
     "trigger": "Licence & Seat Management",
     "provenance": "flow F105 step 1→2",
     "carries": [
      "tenantId"
     ]
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell",
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
      },
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
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId"
       ],
       "operation": "listTenants",
       "provenance": "contract subscription.yaml GET /tenants"
      },
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
       "label": "Production access requests, pending first",
       "bindsTo": "ProductionAccessRequest",
       "columns": [
        "ProductionAccessRequest.developerId",
        "ProductionAccessRequest.listingId",
        "ProductionAccessRequest.scopes",
        "ProductionAccessRequest.allowedTenantIds",
        "ProductionAccessRequest.ipAllowList",
        "ProductionAccessRequest.status",
        "ProductionAccessRequest.requestedAt"
       ],
       "operation": "listProductionAccessRequests",
       "notes": "**Production keys only after certification** (17 September minutes, M17-06). The queue a TICVAI administrator works: each request names the certified integration, the tenants, the module scopes and the IP allow-list. Approving issues a new production client; the sandbox key is never promoted.",
       "provenance": "29 September pass (P29 group A)"
      },
      {
       "kind": "dataTable",
       "label": "Flagged API traffic",
       "bindsTo": "ApiAnomaly",
       "columns": [
        "ApiAnomaly.clientId",
        "ApiAnomaly.ruleKey",
        "ApiAnomaly.measure",
        "ApiAnomaly.observed",
        "ApiAnomaly.baseline",
        "ApiAnomaly.actionTaken",
        "ApiAnomaly.detectedAt"
       ],
       "operation": "listApiAnomalies",
       "notes": "**Abnormal volume is flagged, not only throttled** (M17-07): calls above the client's own baseline, refusals from outside the allow-list, calls to operations it never uses.",
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
       "label": "The selected cell",
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
        "Cell.tier",
        "Cell.status",
        "Cell.cloudProvider",
        "Cell.cloudRegion",
        "Cell.apiEndpoint"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
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
       "kind": "detailPanel",
       "label": "The licence position",
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
       "label": "Save API quota",
       "operation": "setApiQuota",
       "provenance": "contract public-api.yaml PUT /api-quotas"
      },
      {
       "kind": "primaryButton",
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
    }
   ]
  },
  "states": {
   "loading": "The api rate limit list.",
   "error": "Could not load. Names which read failed and leaves the api rate limit untouched.",
   "emptyFirstRun": "No api rate limit yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   },
   {
    "operationId": "listProductionAccessRequests",
    "contract": "public-api",
    "purpose": "The production key approval queue",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "operationId": "decideProductionAccess",
    "contract": "public-api",
    "purpose": "Approve or reject production keys for a certified integration",
    "trigger": "onAction",
    "invalidates": [
     "listProductionAccessRequests",
     "listApiClients"
    ],
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "operationId": "listApiAnomalies",
    "contract": "public-api",
    "purpose": "Flagged abnormal API traffic",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "operationId": "setApiAnomalyRule",
    "contract": "public-api",
    "purpose": "When traffic is flagged, throttled or suspended",
    "trigger": "onAction",
    "invalidates": [
     "listApiAnomalies"
    ],
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "ADM-002"
    },
    {
     "name": "requestId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Cell.id",
    "Cell.name",
    "Cell.kind",
    "Cell.clusterId",
    "Cell.isReachable"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-015"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetApiQuota",
    "component": "modal",
    "trigger": "Save API quota",
    "body": "**Collects what `setApiQuota` sends before it is called.** Required: `clientId`, `sustainedPerMinute`. Optional: `id`, `burstPerSecond`, `dailyCap`, `perOperationOverrides`, `onBreach`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ApiQuota",
    "confirm": {
     "label": "Save API quota",
     "operation": "setApiQuota"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "clientId",
      "sustainedPerMinute",
      "id",
      "burstPerSecond",
      "dailyCap",
      "perOperationOverrides",
      "onBreach"
     ]
    },
    "provenance": "contract public-api.yaml PUT /api-quotas"
   },
   {
    "id": "formDecideProductionAccess",
    "component": "modal",
    "trigger": "Decide production access",
    "body": "**Collects what `decideProductionAccess` sends before it is called.** Required: `decision`. Optional: `reason` (required to reject, in words the developer can act on), `scopes` (narrow only), `credentialTtlDays`. Dismissing sends nothing.",
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
    "body": "**Collects what `setApiAnomalyRule` sends before it is called.** Required: `ruleKey`, `measure`, `comparison`, `threshold`, `action`. Optional: `clientId`, `windowMinutes`, `isActive`. A `suspend` action is named in the form: it stops the client until someone reactivates it.",
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
 "listCreditNotes": {
  "method": "GET",
  "path": "/tenants/{tenantId}/credit-notes",
  "contract": "subscription",
  "summary": "List a tenant's credit notes",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "invoiceId",
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
  "parameters": [
   {
    "name": "offeredToTenantId",
    "in": "query",
    "required": false
   },
   {
    "name": "packageKind",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "Plan"
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
    "description": "False for `onPremiseIsolated`, true for `onPremiseConnected` (ADR-0046). When false, the Control Plane holds the record for licensing and support and **cannot reach the installation** — it may sit behind a firewall with no inbound route. Every operation assuming reachability must handle absence rather than timing out, and a cell that has not called home for a month is not necessarily broken.\n"
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
    "description": "False by default for `onPremiseIsolated`, available for `onPremiseConnected` (ADR-0046). Redeeming a pass issued elsewhere requires reaching the issuing cell at that moment, and an on-premise site may not be able to. Exclusion is the honest default; local-then-reconcile carries a double-redemption risk that needs a decision rather than an assumption.\n"
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
  "description": "Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law requires it.\n\n**On-premise is two configurations, not one (ADR-0046).** `onPremiseIsolated` keeps no channel to TICVAI — updates are pull-initiated or physically delivered, licensing is a signed file, support is blind. `onPremiseConnected` keeps an outbound control channel and is reachable, updatable and licensable in the ordinary way. The channel carries control traffic only and no natural person (ADR-0043); **AI inference is data, not control**, so connectivity alone does not grant the assistant.\n\nThere is no `hybrid`. The RFP's third model is answered by `onPremiseConnected`; a genuine split workload has never been asked for and would be a new decision.\n\n\n**`burst` added 31 August.** An environment stood up for one on-sale and torn down after (CF-162 scenario c). **It is not a jurisdiction and it is not permanent** — it holds a catalogue snapshot, three services of sixteen, and 17 tables of 380.\n\n**The other four are places data lives. This one is a place data passes through**, which is why it has its own lifecycle and a reconciliation obligation the others do not.",
  "enum": [
   "shared",
   "dedicated",
   "onPremiseIsolated",
   "onPremiseConnected",
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
    "nullable": true,
    "description": "AI tokens the package includes per billing period. Usage beyond it is a `metered` invoice line at the AI module's price (decided 29 September)."
   },
   "packageKind": {
    "type": "string",
    "enum": [
     "standard",
     "custom"
    ],
    "default": "standard",
    "description": "**Three standard packages, and custom ones allowed** (decided 29 September, Chinmay)."
   },
   "offeredToTenantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Private to one tenant** (decided 29 September, Chinmay): a custom package offered only to this tenant; `listPlans` shows it to no other tenant and `setSubscription` refuses it for any other (422 `plan-not-offered`). Null for a package any tenant may buy. Custom packages only."
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
 "ModuleKey": {
  "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
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
 "PartnerAgreement": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_agreement",
  "x-ticvai-retired-columns": [
   "partner_name"
  ],
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
    "x-ticvai-references": "control.partner",
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner) this agreement is with. The agreement carries the terms; control.partner carries who the partner is and whether it may trade. **Resolves to control.partner**, not to platform.tenant as the naming convention guessed before the partner master existed (decided 29 September, writers pass; DM4)"
   },
   "partnerName": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The partner's trading name, **read from control.partner.trading_name** (Partner.tradingName) when the agreement is returned and never stored on the agreement, so a renamed partner cannot show two names (decided 29 September, writers pass; DM4)"
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
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: the tiers are rows of control.partner_rate_volume_band** (`PartnerRate.volumeBands`, written by setPartnerRateNet), one set per rate row, so a tier can differ by product, venue or channel. Accepted and ignored on write; not returned once the bands exist. `volumeWindow` below still says over which window the bands count (decided 29 September, writers pass; DM4).\n\n2.7.57. **A tier that changes at a threshold needs the sale to look back at cumulative volume, and nothing did.** Flat net rates and per-channel price lists cover the simple case and stop there.\n**The window is the argument, not the tier.** A partner who sells 400 in January and 400 in February is either a 400-tier partner twice or an 800-tier partner once, and the two are different money. `volumeWindow` says which.\n",
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
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: a seasonal rate is a control.partner_rate row** with `seasonalRate: true` and its own `effectiveFrom`/`effectiveTo` (`PartnerRate`, written by setPartnerRateNet); the most specific row in force wins. Accepted and ignored on write (decided 29 September, writers pass; DM4).\n\nRates that change by date range. **Separate from the volume tier because they compound** — a peak-season rate at a high volume tier is both, and a single rate table cannot say so.\n",
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
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: net rates are rows of control.partner_rate** (`PartnerRate` with `pricingModel: netRate`, `netRate` and the `maxDiscountPercent` guardrail), written by setPartnerRateNet. Per product or category; absent means the commission applies across the catalogue. Accepted and ignored on write (decided 29 September, writers pass; DM4)",
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
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: allocations are rows of control.partner_allocation** (`PartnerAllocation`, written by setPartnerAllocations and read by listCommercialAllocationQuota); used quantity is counted from orders against the row, not stored. Accepted and ignored on write (decided 29 September, writers pass; DM4).\n\nBL-035. **`PartnerAgreement` covered commercial terms and not allocations.** A corporate account with fifty places for its staff is the same structure as a reseller with fifty to sell, and **the difference is that a corporate member does not pay.**\n",
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
   },
   "agreementName": {
    "type": "string",
    "nullable": true,
    "description": "Agreement name (decided 29 September, data model DM4)"
   },
   "agreementType": {
    "type": "string",
    "nullable": true,
    "description": "Agreement type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26) (decided 29 September, data model DM4)"
   },
   "contractReference": {
    "type": "string",
    "nullable": true,
    "description": "Contract reference (decided 29 September, data model DM4)"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The contracting legal entity (ledger.legal_entity) (decided 29 September, data model DM4)"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Brand the agreement covers; empty for every brand of the tenant (decided 29 September, data model DM4)"
   },
   "territory": {
    "type": "string",
    "nullable": true,
    "description": "Territory (decided 29 September, data model DM4)"
   },
   "commercialOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Commercial owner, a staff principal (decided 29 September, data model DM4)"
   },
   "financeOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Finance owner, a staff principal (decided 29 September, data model DM4)"
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "nullable": true,
    "description": "Pricing basis (pack p.27 pricing models); the rows are `control.partner_rate` (decided 29 September, data model DM4)"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "nullable": true,
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale). Held here once; the billing screen reads and sets this column (decided 29 September, data model DM4)"
   },
   "renewalType": {
    "type": "string",
    "enum": [
     "manual",
     "auto"
    ],
    "nullable": true,
    "description": "Renewal type (decided 29 September, data model DM4)"
   },
   "renewalNoticeDays": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Renewal notice period in days (decided 29 September, data model DM4)"
   },
   "renegotiationRequired": {
    "type": "boolean",
    "default": false,
    "description": "Renegotiation required before renewal (decided 29 September, data model DM4)"
   },
   "renewalRequiresApproval": {
    "type": "boolean",
    "description": "Renewal needs approval (decided 29 September, data model DM4)"
   },
   "minimumCommitment": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Minimum commitment: tickets over the agreement term (decided 29 September, data model DM4)"
   },
   "salesTarget": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Sales target over the agreement term (decided 29 September, data model DM4)"
   },
   "agreementValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Agreement value (MoM 31 Aug 4.4: each agreement captures term/value) (decided 29 September, data model DM4)"
   },
   "commissionTerms": {
    "type": "string",
    "nullable": true,
    "description": "Commission terms as written in the contract; the rules that compute it are `control.partner_commission_rule` (decided 29 September, data model DM4)"
   },
   "creditTerms": {
    "type": "string",
    "nullable": true,
    "description": "Credit terms as written in the contract (decided 29 September, data model DM4)"
   },
   "allocationTerms": {
    "type": "string",
    "nullable": true,
    "description": "Allocation terms as written in the contract; the allocations are `control.partner_allocation` (decided 29 September, data model DM4)"
   },
   "cancellationConditions": {
    "type": "string",
    "nullable": true,
    "description": "Cancellation conditions (decided 29 September, data model DM4)"
   },
   "refundConditions": {
    "type": "string",
    "nullable": true,
    "description": "Refund conditions (pack p.26) (decided 29 September, data model DM4)"
   },
   "bookingRestrictions": {
    "type": "string",
    "nullable": true,
    "description": "Booking restrictions as written in the contract; the enforced limits are `control.partner_booking_limit` (decided 29 September, data model DM4)"
   },
   "settlementTerms": {
    "type": "string",
    "nullable": true,
    "description": "Settlement terms (decided 29 September, data model DM4)"
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope, as every control.partner_* row carries it, so row-level security scopes the agreement the same way (decided 29 September, writers pass; DM4)"
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
 "Plan": {
  "x-ticvai-persistence": "subscription.plan + subscription.plan_module + subscription.plan_limit",
  "description": "**A plan's modules and limits are rows, keyed on `plan_id`.** `licensedModules` and `limits` are required on every plan, and `subscription.plan` alone had no column for either — so the licence position, the downgrade check and every module gate had nothing to read. `plan_module` holds one row per licensed `ModuleKey`; `plan_limit` one row per `EntitlementLimit`. Both belong to the plan version the row is, so a subscriber on an earlier version keeps the modules and limits they were sold.",
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
    "format": "date",
    "description": "Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1))."
   },
   "prorate": {
    "type": "boolean",
    "default": true,
    "description": "An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). Kept so a preview can show the unprorated figure; `setSubscription` applies the rule whatever is sent."
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
  "x-ticvai-persistence": "subscription.contract",
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
   "scheduledChange": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.",
    "properties": {
     "planId": {
      "type": "string",
      "format": "uuid"
     },
     "planVersion": {
      "type": "string"
     },
     "effectiveFrom": {
      "type": "string",
      "format": "date",
      "description": "Always the `renewsAt` it was scheduled against."
     }
    }
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingPeriod": {
    "type": "string"
   }
  }
 },
 "SubscriptionCreditNote": {
  "type": "object",
  "x-ticvai-persistence": "control.credit_note + control.credit_note_line",
  "description": "**A credit note against one tenant invoice** (20.7.7, 29 September build): its own number, lines, tax and total. The invoice it credits is never edited.",
  "required": [
   "id",
   "creditNoteNumber",
   "invoiceId",
   "tenantId",
   "reasonCode",
   "settlement",
   "total",
   "issuedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "creditNoteNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Gapless, per issuing legal entity, in its own sequence** (the R152 rule for invoices, decided 28 September, applied to credit notes): assigned at issue, never reused."
   },
   "invoiceId": {
    "type": "string",
    "description": "The invoice credited."
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "reasonCode": {
    "type": "string",
    "enum": [
     "billingError",
     "serviceCredit",
     "disputeResolution",
     "goodwill",
     "other"
    ]
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "settlement": {
    "type": "string",
    "enum": [
     "offsetNextInvoice",
     "refund"
    ]
   },
   "settlementStatus": {
    "type": "string",
    "enum": [
     "pending",
     "offset",
     "refunded"
    ],
    "readOnly": true,
    "description": "`offset` once a later invoice has taken it; `refunded` once the refund is recorded."
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "invoiceLineIndex": {
       "type": "integer"
      },
      "description": {
       "type": "string"
      },
      "quantity": {
       "type": "number",
       "nullable": true
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
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
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
    "type": "string",
    "readOnly": true,
    "description": "A tax invoice number, so **gapless, per legal entity** (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity that issues it, assigned when the invoice is issued, never reused. A cancelled invoice keeps its number.\n"
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
        "module",
        "addOn",
        "overage",
        "metered",
        "oneOff",
        "credit"
       ],
       "description": "`module`, one per licensed module at its platform price, and `metered`, usage such as AI tokens (decided 29 September)."
      },
      "moduleCode": {
       "type": "string",
       "nullable": true,
       "description": "The module a `module` or `metered` line charges for."
      },
      "audience": {
       "type": "string",
       "enum": [
        "staff",
        "guest"
       ],
       "nullable": true,
       "description": "For an AI `metered` line, whose usage it is."
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
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "planVersionUsed": {
    "type": "string",
    "description": "Priced against the version the tenant is subscribed to, not the latest."
   },
   "creditedTotal": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "The sum of the credit notes issued against this invoice (`issueCreditNote`); the invoice itself is never edited. Null with none."
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
