# P09-overview-health-01 — P09 · Overview & Health

**5 screens · 22 operations · 27 schemas · 8 permissions**

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
  `AI_AUDIT_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_RELEASE_PROMOTE, PLATFORM_RELEASE_VIEW, PLATFORM_TENANT_VIEW, TICKET_LOOKUP, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **2 of these operations work offline**: getCrossRegionEntitlement, getTenantLicences
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-002` | Platform Dashboard | listDetail | 6 | 0 | — |
| `ADM-003` | Cross-Tenant Health Dashboard | listDetail | 10 | 1 | — |
| `ADM-004` | Platform Audit Log | listDetail | 1 | 0 | — |
| `ADM-013` | Tenant Performance Monitor | listDetail | 7 | 1 | — |
| `ADM-029` | Deployment Monitor | listDetail | 12 | 1 | — |

## Thin screens in this batch

**ADM-002, ADM-004 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-002",
  "name": "Platform Dashboard",
  "module": "Overview & Health",
  "requiresModule": "membership",
  "wave": 1,
  "capability": "C95",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/platform-dashboard",
   "component": "apps/ticvai-web/src/routes/general/PlatformDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "ADM-001",
    "ADM-003",
    "ADM-004",
    "ADM-005",
    "ADM-006",
    "ADM-007",
    "ADM-008",
    "ADM-012",
    "ADM-020",
    "ADM-021",
    "ADM-319",
    "ADM-329",
    "ADM-339",
    "ADM-349",
    "ADM-359",
    "ADM-369",
    "ADM-379",
    "ADM-389",
    "ADM-399",
    "ADM-409",
    "ADM-419",
    "ADM-449",
    "ADM-459"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-329",
     "trigger": "Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-339",
     "trigger": "Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-349",
     "trigger": "Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-359",
     "trigger": "Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-004",
     "trigger": "Platform Audit Log",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-005",
     "trigger": "Tenant Directory",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-006",
     "trigger": "Tenant Hierarchy Explorer",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-007",
     "trigger": "Module & Feature Entitlement",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-008",
     "trigger": "Subscription & Plan Management",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-012",
     "trigger": "Tenant Isolation & Resource Pool",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-020",
     "trigger": "Creates the first principal and grants it the role",
     "provenance": "flow F109 step 4→5",
     "operation": "listTenants"
    },
    {
     "to": "ADM-021",
     "trigger": "Defines the role the first administrator will hold",
     "provenance": "flow F109 step 2→3"
    },
    {
     "to": "ADM-369",
     "trigger": "Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-459",
     "trigger": "Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-379",
     "trigger": "Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-389",
     "trigger": "Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-399",
     "trigger": "Recommended Package Overview",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "ADM-409",
     "trigger": "Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-419",
     "trigger": "Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-449",
     "trigger": "Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **Drawn 26 August** — `Dashboards Board` frame `adm-002`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.",
  "density": "compact",
  "boardFrames": [
   "Dashboards Board.dc.html#adm-002"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTenants` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
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
       "label": "Every platform",
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
       "label": "The selected platform",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The platform list.",
   "error": "Could not load. Names which read failed and leaves the platform untouched.",
   "emptyFirstRun": "No platform yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the platform are still there. Names the active filter and offers to clear it.",
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
    "EntitlementUsage.metrics",
    "EntitlementUsage.asAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-002",
   "note": "**Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-003",
  "name": "Cross-Tenant Health Dashboard",
  "module": "Overview & Health",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C95",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/cross-tenant-health-dashboard",
   "component": "apps/ticvai-web/src/routes/general/CrossTenantHealthDashboard.tsx",
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
   "fromFlows": true,
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
     "to": "SCN-003",
     "trigger": "Guest scans at the other venue",
     "provenance": "flow F19 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: SCN-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Drawn 26 August** — `Dashboards Board` frame `adm-003`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.",
  "density": "compact",
  "boardFrames": [
   "Dashboards Board.dc.html#adm-003"
  ],
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
  "gaps": [
   {
    "operation": "getCell",
    "why": "**3 declared operations reach no component on this screen**: getCell, getCellCapacity, getCrossRegionEntitlement. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every cross-tenant health",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cross-tenant health",
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
       "label": "Cancel",
       "operation": "cancelDecommission",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Decommission",
       "operation": "decommissionCell",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateCellTier",
       "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Propagate",
       "operation": "propagateCrossRegionEntitlement",
       "provenance": "contract cross-region.yaml POST /cross-region-entitlements"
      },
      {
       "kind": "secondaryButton",
       "label": "Reconcile",
       "operation": "reconcileRedemptions",
       "provenance": "contract cross-region.yaml POST /cross-region-entitlements/reconcile"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelDecommission",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A cross-tenant health this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   }
  ],
  "states": {
   "loading": "The cross-tenant health list.",
   "error": "Could not load. Names which read failed and leaves the cross-tenant health untouched.",
   "emptyFirstRun": "No cross-tenant health yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-tenant health are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "from page inventory",
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
    "operationId": "propagateCrossRegionEntitlement",
    "contract": "cross-region",
    "purpose": "Propagate a right from the issuing cell to a consuming cell",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "getCrossRegionEntitlement",
    "contract": "cross-region",
    "purpose": "Read a redemption right",
    "trigger": "onLoad"
   },
   {
    "operationId": "reconcileRedemptions",
    "contract": "cross-region",
    "purpose": "Report consumption back to the issuing cell",
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
    },
    {
     "name": "rightId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `cellId`, `rightId`.",
   "preloaded": [
    "CellHealth.isHealthy",
    "CellHealth.isSchemaBehind",
    "CellHealth.databaseStatus",
    "CellHealth.replicationLagSeconds",
    "CellHealth.lastBackupAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-003",
   "note": "**Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-004",
  "name": "Platform Audit Log",
  "module": "Overview & Health",
  "requiresModule": "ai",
  "wave": 2,
  "capability": "C97",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/platform-audit-log",
   "component": "apps/ticvai-web/src/routes/general/PlatformAuditLogList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-031"
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
    },
    {
     "to": "BO-068",
     "trigger": "Audit Log",
     "provenance": "flow F106 step 2→3",
     "operation": "listAiInteractions",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — Control Plane audit not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAiInteractions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find platform audit log for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every platform audit log",
       "bindsTo": "AiInteraction",
       "columns": [
        "AiInteraction.id",
        "AiInteraction.conversationId",
        "AiInteraction.principalId",
        "AiInteraction.audience",
        "AiInteraction.subjectId",
        "AiInteraction.billableToTenantId",
        "AiInteraction.scopePath",
        "AiInteraction.capability",
        "AiInteraction.prompt",
        "AiInteraction.response",
        "AiInteraction.sources",
        "AiInteraction.outcome"
       ],
       "operation": "listAiInteractions",
       "provenance": "contract ai.yaml GET /interactions"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected platform audit log",
       "bindsTo": "AiInteraction",
       "columns": [
        "AiInteraction.id",
        "AiInteraction.conversationId",
        "AiInteraction.principalId",
        "AiInteraction.audience",
        "AiInteraction.subjectId",
        "AiInteraction.billableToTenantId",
        "AiInteraction.scopePath",
        "AiInteraction.capability",
        "AiInteraction.prompt",
        "AiInteraction.response",
        "AiInteraction.sources",
        "AiInteraction.outcome",
        "AiInteraction.refusalReason",
        "AiInteraction.provider",
        "AiInteraction.model",
        "AiInteraction.promptTokens"
       ],
       "operation": "listAiInteractions",
       "provenance": "contract ai.yaml GET /interactions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The platform audit log list.",
   "error": "Could not load. Names which read failed and leaves the platform audit log untouched.",
   "emptyFirstRun": "No platform audit log yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the platform audit log are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiInteractions",
    "contract": "ai",
    "purpose": "Every prompt, response and action",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiInteraction.id",
    "AiInteraction.conversationId",
    "AiInteraction.principalId",
    "AiInteraction.audience",
    "AiInteraction.subjectId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-004"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-013",
  "name": "Tenant Performance Monitor",
  "module": "Overview & Health",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/tenant-performance-monitor",
   "component": "apps/ticvai-web/src/routes/general/TenantPerformanceMonitorDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-012"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-014"
   ],
   "transitions": [
    {
     "to": "ADM-014",
     "trigger": "Auto-Scaling Configuration",
     "provenance": "flow F97 step 2→3"
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
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act",
  "purpose": "See tenant performance monitor for this venue.",
  "gaps": [
   {
    "operation": "getCell",
    "why": "**2 declared operations reach no component on this screen**: getCell, getCellCapacity. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every tenant performance",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected tenant performance",
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
       "label": "Cancel",
       "operation": "cancelDecommission",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Decommission",
       "operation": "decommissionCell",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateCellTier",
       "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelDecommission",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A tenant performance this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   }
  ],
  "states": {
   "loading": "The tenant performance list.",
   "error": "Could not load. Names which read failed and leaves the tenant performance untouched.",
   "emptyFirstRun": "No tenant performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "from page inventory",
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
    "CellHealth.isHealthy",
    "CellHealth.isSchemaBehind",
    "CellHealth.databaseStatus",
    "CellHealth.replicationLagSeconds",
    "CellHealth.lastBackupAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-013"
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
  "id": "ADM-029",
  "name": "Deployment Monitor",
  "module": "Overview & Health",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/deployment-monitor",
   "component": "apps/ticvai-web/src/routes/general/DeploymentMonitorDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-023"
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
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getRollout` reads one of them — list, select, act",
  "purpose": "Find deployment monitor for this venue.",
  "gaps": [
   {
    "operation": "listRollouts",
    "why": "**4 declared operations reach no component on this screen**: listRollouts, getCell, getCellCapacity, getCellHealth. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every deployment",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected deployment",
       "bindsTo": "RolloutDetail",
       "columns": [
        "RolloutDetail.id",
        "RolloutDetail.reinventoryHoldId",
        "RolloutDetail.environment",
        "RolloutDetail.status",
        "RolloutDetail.cellsTotal",
        "RolloutDetail.cellsComplete",
        "RolloutDetail.cellsFailed",
        "RolloutDetail.startedByPrincipalId",
        "RolloutDetail.approvedByPrincipalId",
        "RolloutDetail.pausedReason",
        "RolloutDetail.startedAt",
        "RolloutDetail.completedAt",
        "RolloutDetail.cells"
       ],
       "operation": "getRollout",
       "provenance": "contract platform-ops.yaml GET /rollouts/{rolloutId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Pause",
       "operation": "pauseRollout",
       "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Rollback",
       "operation": "rollbackRollout",
       "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/rollback"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelDecommission",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Decommission",
       "operation": "decommissionCell",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Start",
       "operation": "startRollout",
       "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/start"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateCellTier",
       "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelDecommission",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A deployment this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   }
  ],
  "states": {
   "loading": "The deployment list.",
   "error": "Could not load. Names which read failed and leaves the deployment untouched.",
   "emptyFirstRun": "No deployment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deployment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCellJobs",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "listRollouts",
    "contract": "platform-ops",
    "purpose": "Rollouts in flight",
    "trigger": "onLoad"
   },
   {
    "operationId": "getRollout",
    "contract": "platform-ops",
    "purpose": "Per-cell progress",
    "trigger": "onLoad"
   },
   {
    "operationId": "pauseRollout",
    "contract": "platform-ops",
    "purpose": "Halt before the next cell",
    "trigger": "onLoad"
   },
   {
    "operationId": "rollbackRollout",
    "contract": "platform-ops",
    "purpose": "Revert, where every migration is reversible",
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
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "Cell health and schema version",
    "trigger": "onLoad"
   },
   {
    "operationId": "startRollout",
    "contract": "platform-ops",
    "purpose": "Start or continue a rollout",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "updateCellTier",
    "contract": "subscription",
    "purpose": "Change a cell's tier",
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
    },
    {
     "name": "rolloutId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `cellId`, `rolloutId`.",
   "preloaded": [
    "RolloutDetail.id",
    "RolloutDetail.reinventoryHoldId",
    "RolloutDetail.environment",
    "RolloutDetail.status",
    "RolloutDetail.cellsTotal"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-029"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "getCrossRegionEntitlement": {
  "method": "GET",
  "path": "/cross-region-entitlements/{rightId}",
  "contract": "cross-region",
  "summary": "Read a redemption right",
  "permission": "TICKET_LOOKUP",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CrossRegionEntitlement"
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
 "getRollout": {
  "method": "GET",
  "path": "/rollouts/{rolloutId}",
  "contract": "platform-ops",
  "summary": "Rollout progress per cell",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "RolloutDetail"
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
 "listAiInteractions": {
  "method": "GET",
  "path": "/interactions",
  "contract": "ai",
  "summary": "Every prompt, response and action",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
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
  "responds": "AiInteraction"
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
 "listRollouts": {
  "method": "GET",
  "path": "/rollouts",
  "contract": "platform-ops",
  "summary": "List rollouts",
  "permission": "PLATFORM_RELEASE_VIEW",
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
 "pauseRollout": {
  "method": "POST",
  "path": "/rollouts/{rolloutId}/pause",
  "contract": "platform-ops",
  "summary": "Halt a rollout in progress",
  "permission": "PLATFORM_RELEASE_PROMOTE",
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
  "responds": "RolloutDetail"
 },
 "propagateCrossRegionEntitlement": {
  "method": "POST",
  "path": "/cross-region-entitlements",
  "contract": "cross-region",
  "summary": "Propagate a right from the issuing cell to a consuming cell",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PropagateRightRequest",
  "responds": "CrossRegionEntitlement"
 },
 "reconcileRedemptions": {
  "method": "POST",
  "path": "/cross-region-entitlements/reconcile",
  "contract": "cross-region",
  "summary": "Report consumption back to the issuing cell",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
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
 "rollbackRollout": {
  "method": "POST",
  "path": "/rollouts/{rolloutId}/rollback",
  "contract": "platform-ops",
  "summary": "Roll a rollout back",
  "permission": "PLATFORM_RELEASE_PROMOTE",
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
 "startRollout": {
  "method": "POST",
  "path": "/rollouts/{rolloutId}/start",
  "contract": "platform-ops",
  "summary": "Start or continue a rollout",
  "permission": "PLATFORM_RELEASE_PROMOTE",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiInteraction": {
  "type": "object",
  "x-ticvai-persistence": "ai.interaction",
  "required": [
   "id",
   "principalId",
   "capability",
   "outcome",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "audience": {
    "type": "string",
    "enum": [
     "staff",
     "guest"
    ],
    "description": "**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"
   },
   "billableToTenantId": {
    "type": "string",
    "format": "uuid",
    "description": "Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"
   },
   "scopePath": {
    "type": "string"
   },
   "capability": {
    "type": "string"
   },
   "prompt": {
    "type": "string"
   },
   "response": {
    "type": "string"
   },
   "sources": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiSource"
    }
   },
   "outcome": {
    "type": "string",
    "enum": [
     "answered",
     "refused",
     "applied",
     "rejected",
     "failed"
    ]
   },
   "refusalReason": {
    "type": "string",
    "nullable": true
   },
   "provider": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "model": {
    "type": "string"
   },
   "promptTokens": {
    "type": "integer"
   },
   "completionTokens": {
    "type": "integer"
   },
   "costMinor": {
    "type": "integer",
    "description": "In the region's base currency",
    "minor units": null
   },
   "latencyMs": {
    "type": "integer"
   },
   "maskedFieldCount": {
    "type": "integer",
    "description": "How many fields were redacted. Zero on a prompt touching guest data is a defect."
   },
   "traceId": {
    "type": "string"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
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
 },
 "AiSource": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded in the interaction",
  "description": "What the answer was grounded in (8.3.70). **An answer with no sources is a guess**, and the interface should show it as one.\n",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "document",
     "product",
     "entitlement",
     "report",
     "record"
    ]
   },
   "id": {
    "type": "string"
   },
   "title": {
    "type": "string"
   },
   "collectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "excerpt": {
    "type": "string"
   },
   "relevance": {
    "type": "number"
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
 "CrossRegionEntitlement": {
  "x-ticvai-persistence": "platform.cross_region_entitlement",
  "type": "object",
  "required": [
   "rightId",
   "ticketId",
   "issuingCellName",
   "consumingCellName",
   "validFrom",
   "validTo",
   "entriesAllowed",
   "entriesConsumed",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "rightId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "ticketId": {
    "type": "string"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true
   },
   "issuingCellName": {
    "type": "string"
   },
   "consumingCellName": {
    "type": "string"
   },
   "mediaCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null where the right is valid at any venue in the consuming cell."
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true,
    "description": "Null means unlimited."
   },
   "entriesConsumed": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "exhausted",
     "revoked",
     "expired"
    ]
   },
   "lastConsumedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastReconciledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "PropagateRightRequest": {
  "type": "object",
  "required": [
   "rightId",
   "ticketId",
   "issuingCellName",
   "validFrom",
   "validTo",
   "admissionRulesId",
   "entriesAllowed"
  ],
  "properties": {
   "rightId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "ticketId": {
    "type": "string"
   },
   "guestLinkId": {
    "type": "string"
   },
   "issuingCellName": {
    "type": "string"
   },
   "mediaCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "Rollout": {
  "type": "object",
  "x-ticvai-persistence": "control.rollout",
  "required": [
   "id",
   "reinventoryHoldId",
   "environment",
   "status",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "reinventoryHoldId": {
    "type": "string",
    "format": "uuid"
   },
   "environment": {
    "$ref": "#/components/schemas/EnvironmentKind"
   },
   "status": {
    "$ref": "#/components/schemas/RolloutStatus"
   },
   "cellsTotal": {
    "type": "integer"
   },
   "cellsComplete": {
    "type": "integer"
   },
   "cellsFailed": {
    "type": "integer"
   },
   "startedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "pausedReason": {
    "type": "string",
    "nullable": true
   },
   "startedAt": {
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
 "RolloutCell": {
  "type": "object",
  "x-ticvai-persistence": "control.rollout_cell",
  "required": [
   "cellId",
   "status"
  ],
  "properties": {
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "cellName": {
    "type": "string"
   },
   "regionName": {
    "type": "string"
   },
   "countryCode": {
    "type": "string"
   },
   "isCanary": {
    "type": "boolean"
   },
   "wave": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "running",
     "complete",
     "failed",
     "skipped",
     "rolledBack"
    ]
   },
   "fromVersion": {
    "type": "string",
    "nullable": true
   },
   "toVersion": {
    "type": "string",
    "nullable": true
   },
   "error": {
    "type": "string",
    "nullable": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "RolloutDetail": {
  "allOf": [
   {
    "$ref": "#/components/schemas/Rollout"
   },
   {
    "type": "object",
    "x-ticvai-persistence": "none — projection over rollout and cell state",
    "properties": {
     "cells": {
      "type": "array",
      "description": "Per-cell state. \"60% complete\" says nothing about whether the failing 40% is one region or forty venues.\n",
      "items": {
       "$ref": "#/components/schemas/RolloutCell"
      }
     }
    }
   }
  ]
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
 }
}
```
