# P09-security-compliance-01 — P09 · Security & Compliance

**2 screens · 16 operations · 20 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-031` | Security & Compliance Dashboard | listDetail | 7 | 3 | — |
| `ADM-032` | WAF & Security Policy View | listDetail | 9 | 4 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-031",
  "name": "Security & Compliance Dashboard",
  "module": "Security & Compliance",
  "requiresModule": "analytics",
  "wave": 3,
  "capability": "C97",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/security-and-compliance-dashboard",
   "component": "apps/ticvai-web/src/routes/general/SecurityAndComplianceDashboard.tsx",
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
    "ADM-004"
   ],
   "transitions": [
    {
     "to": "ADM-004",
     "trigger": "Platform Audit Log",
     "provenance": "flow F106 step 1→2"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-031 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-031 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDashboards` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
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
       "kind": "textField",
       "label": "Module",
       "operation": "listDashboards",
       "notes": "Sends `?module=` to `listDashboards`.",
       "provenance": "contract reporting.yaml GET /dashboards"
      },
      {
       "kind": "toggle",
       "label": "Include archived",
       "operation": "listDashboards",
       "notes": "Sends `?includeArchived=` to `listDashboards`.",
       "provenance": "contract reporting.yaml GET /dashboards"
      },
      {
       "kind": "dataTable",
       "label": "Every dashboard",
       "bindsTo": "Dashboard",
       "columns": [
        "Dashboard.name",
        "Dashboard.description",
        "Dashboard.venueId",
        "Dashboard.isShared",
        "Dashboard.tiles",
        "Dashboard.id",
        "Dashboard.ownerPrincipalId",
        "Dashboard.aggregateCost"
       ],
       "operation": "listDashboards",
       "provenance": "contract reporting.yaml GET /dashboards"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dashboard",
       "bindsTo": "Dashboard",
       "columns": [
        "Dashboard.name",
        "Dashboard.module",
        "Dashboard.description",
        "Dashboard.venueId",
        "Dashboard.isShared",
        "Dashboard.tiles",
        "Dashboard.id",
        "Dashboard.ownerPrincipalId",
        "Dashboard.aggregateCost",
        "Dashboard.archivedAt"
       ],
       "operation": "listDashboards",
       "provenance": "contract reporting.yaml GET /dashboards"
      },
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create dashboard",
       "operation": "createDashboard",
       "provenance": "contract reporting.yaml POST /dashboards"
      },
      {
       "kind": "secondaryButton",
       "label": "Save dashboard",
       "operation": "updateDashboard",
       "provenance": "contract reporting.yaml PUT /dashboards/{dashboardId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The security compliance list.",
   "error": "Could not load. Names which read failed and leaves the security compliance untouched.",
   "emptyFirstRun": "No security compliance yet. Offers Create dashboard (`createDashboard`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on module, includeArchived and the security compliance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listDashboards` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "operationId": "listDashboards",
    "contract": "reporting",
    "purpose": "List dashboards",
    "trigger": "onLoad"
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onAction"
   },
   {
    "operationId": "createDashboard",
    "contract": "reporting",
    "purpose": "Create a dashboard",
    "trigger": "onAction",
    "invalidates": [
     "listDashboards"
    ]
   },
   {
    "operationId": "updateDashboard",
    "contract": "reporting",
    "purpose": "Update a dashboard",
    "trigger": "onAction",
    "invalidates": [
     "listDashboards"
    ]
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "dashboardId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `dashboardId`.",
   "preloaded": [
    "Dashboard.name",
    "Dashboard.module",
    "Dashboard.description",
    "Dashboard.venueId",
    "Dashboard.isShared"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-031"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
   },
   {
    "id": "formCreateDashboard",
    "component": "modal",
    "trigger": "Create dashboard",
    "body": "**Collects what `createDashboard` sends before it is called.** Required: `name`, `module`, `tiles`. Optional: `description`, `venueId`, `isShared`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateDashboardRequest",
    "confirm": {
     "label": "Create dashboard",
     "operation": "createDashboard"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "module",
      "tiles",
      "description",
      "venueId",
      "isShared"
     ]
    },
    "provenance": "contract reporting.yaml POST /dashboards"
   },
   {
    "id": "formUpdateDashboard",
    "component": "modal",
    "trigger": "Save dashboard",
    "body": "**Collects what `updateDashboard` sends before it is called.** Required: `name`, `module`, `tiles`. Optional: `description`, `venueId`, `isShared`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateDashboardRequest",
    "confirm": {
     "label": "Save dashboard",
     "operation": "updateDashboard"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "module",
      "tiles",
      "description",
      "venueId",
      "isShared"
     ]
    },
    "provenance": "contract reporting.yaml PUT /dashboards/{dashboardId}"
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
  "id": "ADM-032",
  "name": "WAF & Security Policy View",
  "module": "Security & Compliance",
  "requiresModule": "membership",
  "wave": 3,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/waf-and-security-policy-view",
   "component": "apps/ticvai-web/src/routes/general/WafAndSecurityPolicyViewForm.tsx",
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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-032 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-032 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-032 holds cellId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — infrastructure"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act",
  "purpose": "See waf & security policy view for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell job",
       "bindsTo": "CellJob",
       "columns": [
        "CellJob.id",
        "CellJob.kind",
        "CellJob.status",
        "CellJob.progressPercent",
        "CellJob.message",
        "CellJob.error",
        "CellJob.scheduledFor",
        "CellJob.completedAt"
       ],
       "operation": "listCellJobs",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/jobs"
      },
      {
       "kind": "dataTable",
       "label": "Every waf rule",
       "bindsTo": "WafRule",
       "columns": [
        "WafRule.id",
        "WafRule.name",
        "WafRule.action",
        "WafRule.matchOn",
        "WafRule.pattern",
        "WafRule.enabled",
        "WafRule.hitCount24h"
       ],
       "operation": "listWafRules",
       "provenance": "contract platform-ops.yaml GET /waf-policies"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cell job",
       "bindsTo": "CellJob",
       "columns": [
        "CellJob.id",
        "CellJob.kind",
        "CellJob.status",
        "CellJob.progressPercent",
        "CellJob.message",
        "CellJob.error",
        "CellJob.scheduledFor",
        "CellJob.completedAt"
       ],
       "operation": "listCellJobs",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/jobs"
      },
      {
       "kind": "detailPanel",
       "label": "The cell",
       "bindsTo": "CellDetail",
       "columns": [
        "CellDetail.id",
        "CellDetail.name",
        "CellDetail.kind",
        "CellDetail.clusterId",
        "CellDetail.isReachable",
        "CellDetail.lastContactAt",
        "CellDetail.licenceExpiresAt",
        "CellDetail.participatesInCrossCell",
        "CellDetail.regionId",
        "CellDetail.regionName",
        "CellDetail.countryCode",
        "CellDetail.tier",
        "CellDetail.status",
        "CellDetail.cloudProvider",
        "CellDetail.cloudRegion",
        "CellDetail.apiEndpoint"
       ],
       "operation": "getCell",
       "provenance": "contract subscription.yaml GET /cells/{cellId}"
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
       "label": "The cell health",
       "bindsTo": "CellHealth",
       "columns": [
        "CellHealth.isHealthy",
        "CellHealth.isSchemaBehind",
        "CellHealth.databaseStatus",
        "CellHealth.replicationLagSeconds",
        "CellHealth.lastBackupAt",
        "CellHealth.lastRestoreDrillAt",
        "CellHealth.checkedAt"
       ],
       "operation": "getCellHealth",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/health"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Cancel decommission",
       "operation": "cancelDecommission",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Decommission cell",
       "operation": "decommissionCell",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Save cell tier",
       "operation": "updateCellTier",
       "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save waf policy",
       "operation": "setWafPolicy",
       "provenance": "contract platform-ops.yaml PUT /waf-policies"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelDecommission",
    "component": "confirmDialog",
    "trigger": "Cancel decommission",
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A waf security policy this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   },
   {
    "id": "formDecommissionCell",
    "component": "modal",
    "trigger": "Decommission cell",
    "body": "**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decommission cell",
     "operation": "decommissionCell"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
   },
   {
    "id": "formUpdateCellTier",
    "component": "modal",
    "trigger": "Save cell tier",
    "body": "**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save cell tier",
     "operation": "updateCellTier"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tier",
      "scheduledFor"
     ]
    },
    "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
   },
   {
    "id": "formSetWafPolicy",
    "component": "modal",
    "trigger": "Save waf policy",
    "body": "**Collects what `setWafPolicy` sends before it is called.** Required: `id`. Optional: `name`, `action`, `matchOn`, `pattern`, `enabled`, `hitCount24h`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "WafRule",
    "confirm": {
     "label": "Save waf policy",
     "operation": "setWafPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "name",
      "action",
      "matchOn",
      "pattern",
      "enabled",
      "hitCount24h"
     ]
    },
    "provenance": "contract platform-ops.yaml PUT /waf-policies"
   }
  ],
  "states": {
   "loading": "The waf security policy list.",
   "error": "Could not load. Names which read failed and leaves the waf security policy untouched.",
   "emptyFirstRun": "No waf security policy yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "Cell health and schema version",
    "trigger": "onLoad"
   },
   {
    "operationId": "cancelDecommission",
    "contract": "subscription",
    "purpose": "Halt a decommission",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "decommissionCell",
    "contract": "subscription",
    "purpose": "Begin decommissioning a cell",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "getCell",
    "contract": "subscription",
    "purpose": "Read a cell",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCellCapacity",
    "contract": "subscription",
    "purpose": "Load against headroom",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCellJobs",
    "contract": "subscription",
    "purpose": "Provisioning, migration and maintenance jobs",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateCellTier",
    "contract": "subscription",
    "purpose": "Change a cell's tier",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "listWafRules",
    "contract": "platform-ops",
    "purpose": "Firewall rules in force",
    "trigger": "onLoad"
   },
   {
    "operationId": "setWafPolicy",
    "contract": "platform-ops",
    "purpose": "Change the firewall policy",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cellId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `cellId`.",
   "preloaded": [
    "CellJob.id",
    "CellJob.kind",
    "CellJob.status",
    "CellJob.progressPercent",
    "CellJob.message"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-032"
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
 "cancelDecommission": {
  "method": "POST",
  "path": "/cells/{cellId}/cancel-decommission",
  "contract": "subscription",
  "summary": "Halt a decommission",
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
  "requestBody": null,
  "responds": null
 },
 "createDashboard": {
  "method": "POST",
  "path": "/dashboards",
  "contract": "reporting",
  "summary": "Create a dashboard",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateDashboardRequest",
  "responds": "Dashboard"
 },
 "decommissionCell": {
  "method": "POST",
  "path": "/cells/{cellId}/decommission",
  "contract": "subscription",
  "summary": "Begin decommissioning a cell",
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
  "requestBody": null,
  "responds": null
 },
 "getCell": {
  "method": "GET",
  "path": "/cells/{cellId}",
  "contract": "subscription",
  "summary": "Read a cell",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CellDetail"
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
 "getCellHealth": {
  "method": "GET",
  "path": "/cells/{cellId}/health",
  "contract": "subscription",
  "summary": "Cell health and schema version",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CellHealth"
 },
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
 },
 "listCellJobs": {
  "method": "GET",
  "path": "/cells/{cellId}/jobs",
  "contract": "subscription",
  "summary": "Provisioning, migration and maintenance jobs",
  "permission": "PLATFORM_CELL_VIEW",
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
 "listDashboards": {
  "method": "GET",
  "path": "/dashboards",
  "contract": "reporting",
  "summary": "List dashboards",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "module",
    "in": "query",
    "required": false
   },
   {
    "name": "includeArchived",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "Dashboard"
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
 "listWafRules": {
  "method": "GET",
  "path": "/waf-policies",
  "contract": "platform-ops",
  "summary": "Web application firewall rules in force",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "WafRule"
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
 "recordDashboardView": {
  "method": "POST",
  "path": "/dashboards/{dashboardId}/views",
  "contract": "reporting",
  "summary": "Record that a dashboard was opened",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "append",
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
 "setWafPolicy": {
  "method": "PUT",
  "path": "/waf-policies",
  "contract": "platform-ops",
  "summary": "Change the firewall policy",
  "permission": "PLATFORM_CELL_MANAGE",
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
  "requestBody": "WafRule",
  "responds": "WafRule"
 },
 "updateCellTier": {
  "method": "PATCH",
  "path": "/cells/{cellId}",
  "contract": "subscription",
  "summary": "Change a cell's tier",
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
  "requestBody": null,
  "responds": null
 },
 "updateDashboard": {
  "method": "PUT",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Update a dashboard",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateDashboardRequest",
  "responds": "Dashboard"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "CellDetail": {
  "x-ticvai-persistence": "control.cell",
  "allOf": [
   {
    "$ref": "#/components/schemas/Cell"
   },
   {
    "type": "object",
    "properties": {
     "health": {
      "$ref": "#/components/schemas/CellHealth"
     },
     "activeJobs": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CellJob"
      }
     }
    }
   }
  ]
 },
 "CellHealth": {
  "x-ticvai-persistence": "none — polled, not stored",
  "type": "object",
  "required": [
   "cellId",
   "isHealthy",
   "schemaVersion",
   "checkedAt"
  ],
  "properties": {
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "isHealthy": {
    "type": "boolean"
   },
   "schemaVersion": {
    "type": "string",
    "description": "From the cell's version register. Skew across a tenant's cells is expected during rollout; unexplained skew is a defect.\n"
   },
   "isSchemaBehind": {
    "type": "boolean"
   },
   "databaseStatus": {
    "type": "string"
   },
   "replicationLagSeconds": {
    "type": "number",
    "nullable": true
   },
   "lastBackupAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastRestoreDrillAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "checkedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CellJob": {
  "x-ticvai-persistence": "control.cell_job",
  "type": "object",
  "required": [
   "id",
   "cellId",
   "kind",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "provision",
     "tierMigration",
     "schemaMigration",
     "backup",
     "restore",
     "decommission"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "running",
     "completed",
     "failed",
     "rolledBack"
    ]
   },
   "progressPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100
   },
   "message": {
    "type": "string",
    "nullable": true
   },
   "error": {
    "type": "string",
    "nullable": true
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "CellTier": {
  "type": "string",
  "enum": [
   "shared",
   "dedicated",
   "isolated",
   "clientHosted"
  ]
 },
 "CreateDashboardRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "module",
   "tiles"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey",
    "description": "**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"
   },
   "isShared": {
    "type": "boolean",
    "default": false
   },
   "tiles": {
    "type": "array",
    "minItems": 1,
    "maxItems": 24,
    "items": {
     "$ref": "#/components/schemas/DashboardTile"
    }
   }
  }
 },
 "Dashboard": {
  "x-ticvai-persistence": "reporting.dashboard + reporting.dashboard_tile",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateDashboardRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "aggregateCost",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "aggregateCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Combined refresh load of every tile."
     },
     "archivedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
 },
 "DashboardTile": {
  "x-ticvai-persistence": "reporting.dashboard_tile",
  "type": "object",
  "required": [
   "id",
   "reportId",
   "visualisation",
   "position"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "title": {
    "type": "string"
   },
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "visualisation": {
    "type": "string",
    "description": "**Extended 22 September from eight marks to twenty** against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one MVP. Nine were genuinely missing — `combo`, `matrix`, `funnel`, `waterfall`, `treemap`, `scatter`, `map`, `ribbon`, `decompositionTree` — and three are layout variants of marks already here: `area` beside `line`, `donut` beside `pie`, `stackedBar100` beside `stackedBar`.\n**`number` is the source's KPI / card.** Its comparison, variance, trend sparkline and status icon are tile parameters rather than separate marks.\n**Two of the eighteen are deliberately not here** — see `x-ticvai-refuses`. The source lists them as components; the platform already models each of them elsewhere, and a second model of either is the drift this enum exists to prevent.\n",
    "enum": [
     "number",
     "line",
     "area",
     "bar",
     "stackedBar",
     "stackedBar100",
     "combo",
     "pie",
     "donut",
     "table",
     "matrix",
     "gauge",
     "heatmap",
     "funnel",
     "waterfall",
     "treemap",
     "scatter",
     "map",
     "ribbon",
     "decompositionTree"
    ],
    "x-ticvai-refuses": {
     "slicer": "**A control, not a mark.** The source's slicer / filter is already `ReportFilter.isParameter` plus `ReportParameter` — a run-time prompt bound to the report. A slicer on the canvas places that parameter; it does not render a result, so it is not a visualisation and a second filter model beside `ReportFilter` would be one somebody keeps in step by hand.",
     "narrative": "**Generated prose belongs with `ai.Suggestion`.** The source's narrative / insight text (*\"Admissions are 12% above last Tuesday\"*) is model output with traceability requirements, not a way of drawing a query result.",
     "cohort": "**Not one of the eighteen.** It appears once in the source as a *usage* — *\"the Customer & Membership dashboard shall use cards, cohort and trend charts\"* — never as a specified component. A cohort view is a `matrix` or `heatmap` over a cohort dimension."
    },
    "x-ticvai-note": "**These marks cannot yet bind data.** `ReportColumn` carries `field`, `label`, `aggregation` and `format` and **no encoding role** — no axis, series, size or colour. A `number` needs none and an eight-mark enum survived without one; a `scatter` needs x, y, size and colour, and a `combo` needs a secondary axis with stated units. **Adding `ReportColumn.role` is the harder half of this decision and is deliberately not made here** — it is the field-wells model the source's builder specifies, and it belongs with the engine and semantic-layer split that needs an ADR first.\n"
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Open on purpose, and not yet specified.** Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — for `number`, the comparison, variance, sparkline and status icon. The per-visualisation display shape waits on the field-wells decision in `visualisation`'s `x-ticvai-note`.\n"
   },
   "refreshSeconds": {
    "type": "integer",
    "minimum": 30,
    "description": "Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume.\n"
   },
   "position": {
    "type": "object",
    "required": [
     "row",
     "column",
     "width",
     "height"
    ],
    "properties": {
     "row": {
      "type": "integer"
     },
     "column": {
      "type": "integer"
     },
     "width": {
      "type": "integer"
     },
     "height": {
      "type": "integer"
     }
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
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
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
 },
 "WafRule": {
  "type": "object",
  "x-ticvai-persistence": "control.waf_rule",
  "description": "**Drafted 4 September.** One firewall rule, and the reason it is a row rather than a config file is that somebody has to be able to say who changed it and when.",
  "required": [
   "id"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "action": {
    "type": "string",
    "enum": [
     "allow",
     "block",
     "rateLimit",
     "challenge"
    ]
   },
   "matchOn": {
    "type": "string",
    "description": "What the rule inspects - a path, a header, a source range."
   },
   "pattern": {
    "type": "string"
   },
   "enabled": {
    "type": "boolean"
   },
   "hitCount24h": {
    "type": "integer",
    "description": "**A rule with no hits is either protecting nothing or blocking everything silently**, and both want looking at."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 }
}
```
