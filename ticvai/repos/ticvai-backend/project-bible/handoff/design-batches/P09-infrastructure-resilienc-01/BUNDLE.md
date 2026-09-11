# P09-infrastructure-resilienc-01 — P09 · Infrastructure & Resilience

**4 screens · 11 operations · 10 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-014` | Auto-Scaling Configuration | listDetail | 8 | 1 | — |
| `ADM-030` | Infrastructure Sizing & Scaling Policy | listDetail | 9 | 1 | — |
| `ADM-033` | Backup & DR Status | listDetail | 8 | 1 | — |
| `ADM-034` | Archival Job Monitor | listDetail | 8 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-014",
  "name": "Auto-Scaling Configuration",
  "module": "Infrastructure & Resilience",
  "requiresModule": "membership",
  "wave": 3,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/auto-scaling-configuration",
   "component": "apps/ticvai-web/src/routes/general/AutoScalingConfigurationForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-013"
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
   "No contract — infrastructure, Terraform not API"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellCapacity` reads one of them — list, select, act",
  "purpose": "Change how auto-scaling behaves here, and see which level the current value came from.",
  "gaps": [
   {
    "operation": "getCell",
    "why": "**3 declared operations reach no component on this screen**: getCell, getCellHealth, getScalingPolicy. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every auto-scaling",
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
       "label": "The selected auto-scaling",
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
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A auto-scaling this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   }
  ],
  "states": {
   "loading": "The auto-scaling list.",
   "error": "Could not load. Names which read failed and leaves the auto-scaling untouched.",
   "emptyFirstRun": "No auto-scaling yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the auto-scaling are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCellCapacity",
    "contract": "subscription",
    "purpose": "Load against headroom",
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
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "Cell health and schema version",
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
    "operationId": "getScalingPolicy",
    "contract": "platform-ops",
    "purpose": "Floors, ceilings and target utilisation",
    "trigger": "onLoad"
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
    "CellCapacity.kind",
    "CellCapacity.tenantCount",
    "CellCapacity.isConstrained",
    "CellCapacity.constrainedDimension",
    "CellCapacity.dimensions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-014"
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
  "id": "ADM-030",
  "name": "Infrastructure Sizing & Scaling Policy",
  "module": "Infrastructure & Resilience",
  "requiresModule": "membership",
  "wave": 3,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/infrastructure-sizing-and-scaling-policy",
   "component": "apps/ticvai-web/src/routes/general/InfrastructureSizingAndScalingPolicyForm.tsx",
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
   "No contract — Terraform"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellCapacity` reads one of them — list, select, act",
  "purpose": "See infrastructure sizing & scaling policy for this venue.",
  "gaps": [
   {
    "operation": "getCell",
    "why": "**3 declared operations reach no component on this screen**: getCell, getCellHealth, getScalingPolicy. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every infrastructure sizing scaling",
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
       "label": "The selected infrastructure sizing scaling",
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
       "operation": "setScalingPolicy",
       "provenance": "contract platform-ops.yaml PUT /scaling-policies"
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
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A infrastructure sizing scaling this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   }
  ],
  "states": {
   "loading": "The infrastructure sizing scaling list.",
   "error": "Could not load. Names which read failed and leaves the infrastructure sizing scaling untouched.",
   "emptyFirstRun": "No infrastructure sizing scaling yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the infrastructure sizing scaling are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCellCapacity",
    "contract": "subscription",
    "purpose": "Load against headroom",
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
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "Cell health and schema version",
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
    "operationId": "getScalingPolicy",
    "contract": "platform-ops",
    "purpose": "The policy as it stands",
    "trigger": "onLoad"
   },
   {
    "operationId": "setScalingPolicy",
    "contract": "platform-ops",
    "purpose": "Change it",
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
    "CellCapacity.kind",
    "CellCapacity.tenantCount",
    "CellCapacity.isConstrained",
    "CellCapacity.constrainedDimension",
    "CellCapacity.dimensions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-030"
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
  "id": "ADM-033",
  "name": "Backup & DR Status",
  "module": "Infrastructure & Resilience",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/backup-and-dr-status",
   "component": "apps/ticvai-web/src/routes/general/BackupAndDrStatusDashboard.tsx",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act",
  "purpose": "See backup & dr status for this venue.",
  "gaps": [
   {
    "operation": "getCell",
    "why": "**3 declared operations reach no component on this screen**: getCell, getCellCapacity, listBackupRuns. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every backup status",
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
       "label": "The selected backup status",
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
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A backup status this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   }
  ],
  "states": {
   "loading": "The backup status list.",
   "error": "Could not load. Names which read failed and leaves the backup status untouched.",
   "emptyFirstRun": "No backup status yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the backup status are still there. Names the active filter and offers to clear it.",
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
    "operationId": "listBackupRuns",
    "contract": "platform-ops",
    "purpose": "Backups taken and how old the newest is",
    "trigger": "onLoad"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-033"
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
  "id": "ADM-034",
  "name": "Archival Job Monitor",
  "module": "Infrastructure & Resilience",
  "requiresModule": "membership",
  "wave": 3,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/archival-job-monitor",
   "component": "apps/ticvai-web/src/routes/general/ArchivalJobMonitorDashboard.tsx",
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
   "No contract — retention not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCell` reads one of them — list, select, act",
  "purpose": "Find archival job monitor for this venue.",
  "gaps": [
   {
    "operation": "getCellCapacity",
    "why": "**3 declared operations reach no component on this screen**: getCellCapacity, getCellHealth, listArchivalJobs. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every archival job",
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
       "label": "The selected archival job",
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
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A archival job this affects should be identified in the dialog, not just counted.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   }
  ],
  "states": {
   "loading": "The archival job list.",
   "error": "Could not load. Names which read failed and leaves the archival job untouched.",
   "emptyFirstRun": "No archival job yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the archival job are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCellJobs",
    "contract": "subscription",
    "purpose": "Provisioning, migration and maintenance jobs",
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
    "operationId": "updateCellTier",
    "contract": "subscription",
    "purpose": "Change a cell's tier",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "listArchivalJobs",
    "contract": "platform-ops",
    "purpose": "Archival and retention jobs",
    "trigger": "onLoad"
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
    "CellDetail.id",
    "CellDetail.name",
    "CellDetail.kind",
    "CellDetail.clusterId",
    "CellDetail.isReachable"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-034"
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
 "getScalingPolicy": {
  "method": "GET",
  "path": "/scaling-policies",
  "contract": "platform-ops",
  "summary": "The floors, ceilings and target utilisation a cell scales on",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "ScalingPolicy"
 },
 "listArchivalJobs": {
  "method": "GET",
  "path": "/archival-jobs",
  "contract": "platform-ops",
  "summary": "Archival and retention jobs",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "ArchivalJob"
 },
 "listBackupRuns": {
  "method": "GET",
  "path": "/backup-runs",
  "contract": "platform-ops",
  "summary": "Backups taken and what they cover",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "BackupRun"
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
 "setScalingPolicy": {
  "method": "PUT",
  "path": "/scaling-policies",
  "contract": "platform-ops",
  "summary": "Change the scaling policy",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": "ScalingPolicy",
  "responds": "ScalingPolicy"
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
 "ArchivalJob": {
  "type": "object",
  "x-ticvai-persistence": "control.archival_job",
  "description": "**Drafted 4 September.** One archival or retention run. Retention is a legal obligation, so a stalled job is a compliance failure rather than a housekeeping one.",
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
   "policyName": {
    "type": "string"
   },
   "targetTable": {
    "type": "string"
   },
   "rowsArchived": {
    "type": "integer"
   },
   "rowsPurged": {
    "type": "integer"
   },
   "state": {
    "type": "string",
    "enum": [
     "scheduled",
     "running",
     "succeeded",
     "failed"
    ]
   },
   "runAt": {
    "type": "string",
    "format": "date-time"
   },
   "error": {
    "type": "string"
   }
  }
 },
 "BackupRun": {
  "type": "object",
  "x-ticvai-persistence": "control.backup_run",
  "description": "**Drafted 4 September.** One backup run. The question this answers is not *did it run* but *how old is the newest restorable copy* - a job that succeeds nightly against an empty database succeeds forever.",
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
   "scope": {
    "type": "string",
    "enum": [
     "cell",
     "tenant"
    ]
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time"
   },
   "state": {
    "type": "string",
    "enum": [
     "running",
     "succeeded",
     "failed"
    ]
   },
   "sizeBytes": {
    "type": "integer"
   },
   "restoreTestedAt": {
    "type": "string",
    "format": "date-time",
    "description": "**A backup nobody has restored is a hypothesis.**"
   },
   "error": {
    "type": "string"
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
 "ScalingPolicy": {
  "type": "object",
  "x-ticvai-persistence": "control.scaling_policy",
  "description": "**Drafted 4 September.** What a cell scales on. **A floor and a ceiling are not symmetric** - the floor is the size the environment is stood up at before traffic arrives, and the ceiling is a cap on absorbing a peak nobody predicted (ADR-0035).",
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
   "service": {
    "type": "string"
   },
   "replicaFloor": {
    "type": "integer"
   },
   "replicaCeiling": {
    "type": "integer",
    "description": "Null means no maximum, which is the correct setting for a burst cell."
   },
   "targetUtilisationPct": {
    "type": "integer"
   },
   "scaleStepPct": {
    "type": "integer"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 }
}
```
