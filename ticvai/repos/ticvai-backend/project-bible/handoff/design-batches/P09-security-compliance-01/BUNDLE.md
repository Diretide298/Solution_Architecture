# P09-security-compliance-01 — P09 · Security & Compliance

**2 screens · 13 operations · 13 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-031` | Security & Compliance Dashboard | listDetail | 4 | 0 | — |
| `ADM-032` | WAF & Security Policy View | listDetail | 9 | 1 | — |

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
    "ADM-003",
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
       "kind": "dataTable",
       "label": "Every security compliance",
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
       "label": "The selected security compliance",
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
       "label": "Create",
       "operation": "createDashboard",
       "provenance": "contract reporting.yaml POST /dashboards"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
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
   "emptyFirstRun": "No security compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the security compliance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
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
    "trigger": "onLoad"
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
    "DashboardData.tileData"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-031"
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
  "openQuestions": [
   "No contract — infrastructure"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act",
  "purpose": "See waf & security policy view for this venue.",
  "gaps": [
   {
    "operation": "getCell",
    "why": "**3 declared operations reach no component on this screen**: getCell, getCellCapacity, listWafRules. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every waf security policy",
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
       "label": "The selected waf security policy",
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
       "label": "Save changes",
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
    "trigger": "Cancel",
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A waf security policy this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   }
  ],
  "states": {
   "loading": "The waf security policy list.",
   "error": "Could not load. Names which read failed and leaves the waf security policy untouched.",
   "emptyFirstRun": "No waf security policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the waf security policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
  "parameters": [],
  "requestBody": null,
  "responds": "Dashboard"
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
 "setWafPolicy": {
  "method": "PUT",
  "path": "/waf-policies",
  "contract": "platform-ops",
  "summary": "Change the firewall policy",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
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
 "CreateDashboardRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "tiles"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
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
    "enum": [
     "number",
     "line",
     "bar",
     "stackedBar",
     "pie",
     "table",
     "gauge",
     "heatmap"
    ]
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true
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
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true
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
