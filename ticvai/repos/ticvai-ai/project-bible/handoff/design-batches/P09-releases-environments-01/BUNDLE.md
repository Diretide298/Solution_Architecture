# P09-releases-environments-01 — P09 · Releases & Environments

**7 screens · 20 operations · 18 schemas · 6 permissions**

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
  `DEVELOPER_ADMIN, PLATFORM_MIGRATION_APPLY, PLATFORM_MIGRATION_VIEW, PLATFORM_RELEASE_MANAGE, PLATFORM_RELEASE_PROMOTE, PLATFORM_RELEASE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-022` | Release & Version Management | listDetail | 7 | 2 | — |
| `ADM-023` | Staging Promotion & Approval | listDetail | 7 | 2 | — |
| `ADM-024` | Release Notification Composer | listDetail | 3 | 0 | — |
| `ADM-025` | Tenant Upgrade Scheduler | listDetail | 2 | 0 | — |
| `ADM-026` | End-of-Support Notice Management | listDetail | 3 | 0 | — |
| `ADM-027` | Database Migration Console | listDetail | 6 | 0 | — |
| `ADM-028` | Environment Registry | listDetail | 2 | 0 | — |

## Thin screens in this batch

**ADM-025 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-022",
  "name": "Release & Version Management",
  "module": "Releases & Environments",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/release-and-version-management",
   "component": "apps/ticvai-web/src/routes/general/ReleaseAndVersionManagementForm.tsx",
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
    "ADM-027"
   ],
   "flowDerived": true,
   "transitions": [
    {
     "to": "ADM-027",
     "trigger": "Plans the migrations the release requires",
     "provenance": "flow F04 step 1→2"
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
   "No contract — new scope, 30 Jul"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReleases` reads the population and `getRelease` reads one of them — list, select, act",
  "purpose": "Find release & version management for this venue.",
  "gaps": [
   {
    "operation": "getReleaseReadiness",
    "why": "**1 declared operation reach no component on this screen**: getReleaseReadiness. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every release version",
       "bindsTo": "Release",
       "columns": [
        "Release.components",
        "Release.requiredMigrations",
        "Release.note",
        "Release.breakingChanges",
        "Release.id",
        "Release.status",
        "Release.createdByPrincipalId",
        "Release.promotedToStagingAt",
        "Release.promotedToProductionAt"
       ],
       "operation": "listReleases",
       "provenance": "contract platform-ops.yaml GET /releases"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected release version",
       "bindsTo": "ReleaseDetail",
       "columns": [
        "ReleaseDetail.rollouts",
        "ReleaseDetail.cellsOnThisVersion",
        "ReleaseDetail.cellsTotal"
       ],
       "operation": "getRelease",
       "provenance": "contract platform-ops.yaml GET /releases/{reinventoryHoldId}"
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
       "operation": "createRelease",
       "provenance": "contract platform-ops.yaml POST /releases"
      },
      {
       "kind": "secondaryButton",
       "label": "Promote",
       "operation": "promoteRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/promote"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/reject"
      },
      {
       "kind": "destructiveButton",
       "label": "Withdraw",
       "operation": "withdrawRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/withdraw"
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
       "kind": "publishGate",
       "impliedBy": "promoteRelease",
       "notes": "Declares `promoteRelease`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectRelease",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Names what `rejectRelease` changes and what it leaves alone**, in the consequence rather than the verb. A release version this affects should be identified in the dialog, not just counted.",
    "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/reject"
   },
   {
    "id": "confirmWithdrawRelease",
    "component": "confirmDialog",
    "trigger": "Withdraw",
    "body": "**Names what `withdrawRelease` changes and what it leaves alone**, in the consequence rather than the verb. A release version this affects should be identified in the dialog, not just counted.",
    "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/withdraw"
   }
  ],
  "states": {
   "loading": "The release version list.",
   "error": "Could not load. Names which read failed and leaves the release version untouched.",
   "emptyFirstRun": "No release version yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the release version are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReleases",
    "contract": "platform-ops",
    "purpose": "Release list",
    "trigger": "onLoad"
   },
   {
    "operationId": "getRelease",
    "contract": "platform-ops",
    "purpose": "Release detail with rollout state",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReleaseReadiness",
    "contract": "platform-ops",
    "purpose": "Which gates pass and which block",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRelease",
    "contract": "platform-ops",
    "purpose": "Cut a release",
    "trigger": "onAction",
    "invalidates": [
     "listReleases"
    ]
   },
   {
    "operationId": "promoteRelease",
    "contract": "platform-ops",
    "purpose": "Promote a release to the next environment",
    "trigger": "onAction",
    "invalidates": [
     "listReleases"
    ]
   },
   {
    "operationId": "rejectRelease",
    "contract": "platform-ops",
    "purpose": "Reject a release back a stage",
    "trigger": "onAction",
    "invalidates": [
     "listReleases"
    ]
   },
   {
    "operationId": "withdrawRelease",
    "contract": "platform-ops",
    "purpose": "Withdraw a release",
    "trigger": "onAction",
    "invalidates": [
     "listReleases"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "reinventoryHoldId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `reinventoryHoldId`.",
   "preloaded": [
    "ReleaseDetail.rollouts",
    "ReleaseDetail.cellsOnThisVersion",
    "ReleaseDetail.cellsTotal"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-022"
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
  "id": "ADM-023",
  "name": "Staging Promotion & Approval",
  "module": "Releases & Environments",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/staging-promotion-and-approval",
   "component": "apps/ticvai-web/src/routes/general/StagingPromotionAndApprovalWizard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-027"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-029"
   ],
   "flowDerived": true,
   "transitions": [
    {
     "to": "ADM-029",
     "trigger": "Watches the rollout per cell",
     "provenance": "flow F04 step 3→4",
     "operation": "promoteRelease"
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
   "No contract — new scope, 30 Jul"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReleases` reads the population and `getReleaseReadiness` reads one of them — list, select, act",
  "purpose": "Work with staging promotion & approval for this venue.",
  "gaps": [
   {
    "operation": "getRelease",
    "why": "**1 declared operation reach no component on this screen**: getRelease. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every staging promotion approval",
       "bindsTo": "Release",
       "columns": [
        "Release.components",
        "Release.requiredMigrations",
        "Release.note",
        "Release.breakingChanges",
        "Release.id",
        "Release.status",
        "Release.createdByPrincipalId",
        "Release.promotedToStagingAt",
        "Release.promotedToProductionAt"
       ],
       "operation": "listReleases",
       "provenance": "contract platform-ops.yaml GET /releases"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected staging promotion approval",
       "bindsTo": "ReleaseReadiness",
       "columns": [
        "ReleaseReadiness.reinventoryHoldId",
        "ReleaseReadiness.canPromote",
        "ReleaseReadiness.targetEnvironment",
        "ReleaseReadiness.gates"
       ],
       "operation": "getReleaseReadiness",
       "provenance": "contract platform-ops.yaml GET /releases/{reinventoryHoldId}/readiness"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Promote",
       "operation": "promoteRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/promote"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createRelease",
       "provenance": "contract platform-ops.yaml POST /releases"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/reject"
      },
      {
       "kind": "destructiveButton",
       "label": "Withdraw",
       "operation": "withdrawRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/withdraw"
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
       "kind": "publishGate",
       "impliedBy": "promoteRelease",
       "notes": "Declares `promoteRelease`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectRelease",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Names what `rejectRelease` changes and what it leaves alone**, in the consequence rather than the verb. A staging promotion approval this affects should be identified in the dialog, not just counted.",
    "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/reject"
   },
   {
    "id": "confirmWithdrawRelease",
    "component": "confirmDialog",
    "trigger": "Withdraw",
    "body": "**Names what `withdrawRelease` changes and what it leaves alone**, in the consequence rather than the verb. A staging promotion approval this affects should be identified in the dialog, not just counted.",
    "provenance": "contract platform-ops.yaml POST /releases/{reinventoryHoldId}/withdraw"
   }
  ],
  "states": {
   "loading": "The staging promotion approval list.",
   "error": "Could not load. Names which read failed and leaves the staging promotion approval untouched.",
   "emptyFirstRun": "No staging promotion approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the staging promotion approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "promoteRelease",
    "contract": "platform-ops",
    "purpose": "Promote with an approver",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReleaseReadiness",
    "contract": "platform-ops",
    "purpose": "Checked before the request is offered",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRelease",
    "contract": "platform-ops",
    "purpose": "Cut a release",
    "trigger": "onAction",
    "invalidates": [
     "listReleases"
    ]
   },
   {
    "operationId": "getRelease",
    "contract": "platform-ops",
    "purpose": "Read a release with its rollout state",
    "trigger": "onLoad"
   },
   {
    "operationId": "listReleases",
    "contract": "platform-ops",
    "purpose": "List releases",
    "trigger": "onLoad"
   },
   {
    "operationId": "rejectRelease",
    "contract": "platform-ops",
    "purpose": "Reject a release back a stage",
    "trigger": "onAction",
    "invalidates": [
     "listReleases"
    ]
   },
   {
    "operationId": "withdrawRelease",
    "contract": "platform-ops",
    "purpose": "Withdraw a release",
    "trigger": "onAction",
    "invalidates": [
     "listReleases"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "reinventoryHoldId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `reinventoryHoldId`.",
   "preloaded": [
    "ReleaseReadiness.reinventoryHoldId",
    "ReleaseReadiness.canPromote",
    "ReleaseReadiness.targetEnvironment",
    "ReleaseReadiness.gates"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-023"
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
  "id": "ADM-024",
  "name": "Release Notification Composer",
  "module": "Releases & Environments",
  "requiresModule": "core",
  "wave": 3,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/release-notification-composer",
   "component": "apps/ticvai-web/src/routes/general/ReleaseNotificationComposerForm.tsx",
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
   "No contract — new scope, 30 Jul"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Push live release notification composer for this venue.",
  "gaps": [
   {
    "operation": "listReleases",
    "why": "**1 declared operation reach no component on this screen**: listReleases. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every release notification composer",
       "bindsTo": "SupportNotice",
       "columns": [
        "SupportNotice.id",
        "SupportNotice.supportEndsAt",
        "SupportNotice.message",
        "SupportNotice.affectedTenantIds",
        "SupportNotice.publishedByPrincipalId",
        "SupportNotice.publishedAt",
        "SupportNotice.scopePath"
       ],
       "operation": "listSupportNotices",
       "provenance": "contract platform-ops.yaml GET /support-notices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected release notification composer",
       "bindsTo": "SupportNotice",
       "columns": [
        "SupportNotice.id",
        "SupportNotice.supportEndsAt",
        "SupportNotice.message",
        "SupportNotice.affectedTenantIds",
        "SupportNotice.publishedByPrincipalId",
        "SupportNotice.publishedAt",
        "SupportNotice.scopePath"
       ],
       "operation": "listSupportNotices",
       "provenance": "contract platform-ops.yaml GET /support-notices"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish",
       "operation": "publishSupportNotice",
       "provenance": "contract platform-ops.yaml POST /support-notices"
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
       "kind": "publishGate",
       "impliedBy": "publishSupportNotice",
       "notes": "Declares `publishSupportNotice`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The release notification composer list.",
   "error": "Could not load. Names which read failed and leaves the release notification composer untouched.",
   "emptyFirstRun": "No release notification composer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the release notification composer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishSupportNotice",
    "contract": "platform-ops",
    "purpose": "Compose and publish a notice",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSupportNotices",
    "contract": "platform-ops",
    "purpose": "End-of-support notices",
    "trigger": "onLoad"
   },
   {
    "operationId": "listReleases",
    "contract": "platform-ops",
    "purpose": "Releases and their readiness",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "SupportNotice.id",
    "SupportNotice.supportEndsAt",
    "SupportNotice.message",
    "SupportNotice.affectedTenantIds",
    "SupportNotice.publishedByPrincipalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-024"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-025",
  "name": "Tenant Upgrade Scheduler",
  "module": "Releases & Environments",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/tenant-upgrade-scheduler",
   "component": "apps/ticvai-web/src/routes/general/TenantUpgradeSchedulerForm.tsx",
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
   "No contract — new scope, 30 Jul"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listUpgradeSchedules` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find tenant upgrade scheduler for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every tenant upgrade scheduler",
       "bindsTo": "UpgradeSchedule",
       "columns": [
        "UpgradeSchedule.tenantName",
        "UpgradeSchedule.releaseVersion",
        "UpgradeSchedule.scheduledFor",
        "UpgradeSchedule.deferredByTenant",
        "UpgradeSchedule.deferralReason",
        "UpgradeSchedule.maxDeferralUntil",
        "UpgradeSchedule.notifiedAt"
       ],
       "operation": "listUpgradeSchedules",
       "provenance": "contract platform-ops.yaml GET /upgrade-schedules"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected tenant upgrade scheduler",
       "bindsTo": "UpgradeSchedule",
       "columns": [
        "UpgradeSchedule.tenantName",
        "UpgradeSchedule.releaseVersion",
        "UpgradeSchedule.scheduledFor",
        "UpgradeSchedule.deferredByTenant",
        "UpgradeSchedule.deferralReason",
        "UpgradeSchedule.maxDeferralUntil",
        "UpgradeSchedule.notifiedAt"
       ],
       "operation": "listUpgradeSchedules",
       "provenance": "contract platform-ops.yaml GET /upgrade-schedules"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Schedule",
       "operation": "scheduleTenantUpgrade",
       "provenance": "contract platform-ops.yaml POST /upgrade-schedules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant upgrade scheduler list.",
   "error": "Could not load. Names which read failed and leaves the tenant upgrade scheduler untouched.",
   "emptyFirstRun": "No tenant upgrade scheduler yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant upgrade scheduler are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUpgradeSchedules",
    "contract": "platform-ops",
    "purpose": "Scheduled tenant upgrades",
    "trigger": "onLoad"
   },
   {
    "operationId": "scheduleTenantUpgrade",
    "contract": "platform-ops",
    "purpose": "Schedule or defer",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "UpgradeSchedule.tenantName",
    "UpgradeSchedule.releaseVersion",
    "UpgradeSchedule.scheduledFor",
    "UpgradeSchedule.deferredByTenant",
    "UpgradeSchedule.deferralReason"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-025"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-026",
  "name": "End-of-Support Notice Management",
  "module": "Releases & Environments",
  "requiresModule": "core",
  "wave": 3,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/end-of-support-notice-management",
   "component": "apps/ticvai-web/src/routes/general/EndOfSupportNoticeManagementForm.tsx",
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
   "No contract — new scope, 30 Jul"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Answer a question without needing a person.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every end-of-support notice",
       "bindsTo": "SupportNotice",
       "columns": [
        "SupportNotice.id",
        "SupportNotice.supportEndsAt",
        "SupportNotice.message",
        "SupportNotice.affectedTenantIds",
        "SupportNotice.publishedByPrincipalId",
        "SupportNotice.publishedAt",
        "SupportNotice.scopePath"
       ],
       "operation": "listSupportNotices",
       "provenance": "contract platform-ops.yaml GET /support-notices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected end-of-support notice",
       "bindsTo": "SupportNotice",
       "columns": [
        "SupportNotice.id",
        "SupportNotice.supportEndsAt",
        "SupportNotice.message",
        "SupportNotice.affectedTenantIds",
        "SupportNotice.publishedByPrincipalId",
        "SupportNotice.publishedAt",
        "SupportNotice.scopePath"
       ],
       "operation": "listSupportNotices",
       "provenance": "contract platform-ops.yaml GET /support-notices"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish",
       "operation": "publishSupportNotice",
       "provenance": "contract platform-ops.yaml POST /support-notices"
      },
      {
       "kind": "secondaryButton",
       "label": "Deprecate",
       "operation": "deprecateApiVersion",
       "provenance": "contract public-api.yaml POST /api-versions/{version}/deprecate"
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
       "kind": "publishGate",
       "impliedBy": "publishSupportNotice",
       "notes": "Declares `publishSupportNotice`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The end-of-support notice list.",
   "error": "Could not load. Names which read failed and leaves the end-of-support notice untouched.",
   "emptyFirstRun": "No end-of-support notice yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the end-of-support notice are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSupportNotices",
    "contract": "platform-ops",
    "purpose": "End-of-support notices",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishSupportNotice",
    "contract": "platform-ops",
    "purpose": "Publish an end-of-support notice",
    "trigger": "onAction",
    "invalidates": [
     "listSupportNotices"
    ]
   },
   {
    "operationId": "deprecateApiVersion",
    "contract": "public-api",
    "purpose": "Mark a version end-of-support",
    "trigger": "onAction",
    "invalidates": [
     "listSupportNotices"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "version",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one the screen says what is missing and offers that list — never an empty form that looks configurable.",
   "preloaded": [
    "SupportNotice.id",
    "SupportNotice.supportEndsAt",
    "SupportNotice.message",
    "SupportNotice.affectedTenantIds",
    "SupportNotice.publishedByPrincipalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-026"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-027",
  "name": "Database Migration Console",
  "module": "Releases & Environments",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/database-migration-console",
   "component": "apps/ticvai-web/src/routes/general/DatabaseMigrationConsoleDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-022"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-023"
   ],
   "flowDerived": true,
   "transitions": [
    {
     "to": "ADM-023",
     "trigger": "Requests promotion with an approver",
     "provenance": "flow F04 step 2→3",
     "operation": "planMigration"
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
   "No contract — the unowned orchestrator"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMigrations` reads the population and `getVersionSkew` reads one of them — list, select, act",
  "purpose": "Find database migration console for this venue.",
  "gaps": [
   {
    "operation": "getMigrationRun",
    "why": "**1 declared operation reach no component on this screen**: getMigrationRun. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every database migration console",
       "bindsTo": "Migration",
       "columns": [
        "Migration.module",
        "Migration.description",
        "Migration.isReversible",
        "Migration.rollbackTestedAt",
        "Migration.checksum",
        "Migration.estimatedLockMs",
        "Migration.touchesPartitionedTable",
        "Migration.appliedCellCount",
        "Migration.pendingCellCount"
       ],
       "operation": "listMigrations",
       "provenance": "contract platform-ops.yaml GET /migrations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected database migration console",
       "bindsTo": "VersionSkewReport",
       "columns": [
        "VersionSkewReport.asAt",
        "VersionSkewReport.hasUnexplainedSkew",
        "VersionSkewReport.cells"
       ],
       "operation": "getVersionSkew",
       "provenance": "contract platform-ops.yaml GET /migrations/version-skew"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Plan",
       "operation": "planMigration",
       "provenance": "contract platform-ops.yaml POST /migrations/plan"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply",
       "operation": "applyMigration",
       "provenance": "contract platform-ops.yaml POST /migrations/apply"
      },
      {
       "kind": "secondaryButton",
       "label": "Rollback",
       "operation": "rollbackMigrationRun",
       "provenance": "contract platform-ops.yaml POST /migrations/runs/{runId}/rollback"
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
       "impliedBy": "listMigrations",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "planMigration",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The database migration console list.",
   "error": "Could not load. Names which read failed and leaves the database migration console untouched.",
   "emptyFirstRun": "No database migration console yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the database migration console are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMigrations",
    "contract": "platform-ops",
    "purpose": "The migration register",
    "trigger": "onLoad"
   },
   {
    "operationId": "planMigration",
    "contract": "platform-ops",
    "purpose": "Plan without applying — the safety step",
    "trigger": "onLoad"
   },
   {
    "operationId": "applyMigration",
    "contract": "platform-ops",
    "purpose": "Apply a reviewed plan",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVersionSkew",
    "contract": "platform-ops",
    "purpose": "Schema and application version per cell",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMigrationRun",
    "contract": "platform-ops",
    "purpose": "Migration run progress per cell",
    "trigger": "onLoad"
   },
   {
    "operationId": "rollbackMigrationRun",
    "contract": "platform-ops",
    "purpose": "Roll a migration run back",
    "trigger": "onAction",
    "invalidates": [
     "listMigrations"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "runId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `runId`.",
   "preloaded": [
    "VersionSkewReport.asAt",
    "VersionSkewReport.hasUnexplainedSkew",
    "VersionSkewReport.cells"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-027"
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
  "id": "ADM-028",
  "name": "Environment Registry",
  "module": "Releases & Environments",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/environment-registry",
   "component": "apps/ticvai-web/src/routes/general/EnvironmentRegistryDetail.tsx",
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
   "No contract — not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listEnvironments` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find environment registry for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every environment registry",
       "bindsTo": "Environment",
       "columns": [
        "Environment.id",
        "Environment.kind",
        "Environment.name",
        "Environment.cellIds",
        "Environment.requiresApprovalToPromote",
        "Environment.soakHours",
        "Environment.currentReleaseVersion",
        "Environment.isActive"
       ],
       "operation": "listEnvironments",
       "provenance": "contract platform-ops.yaml GET /environments"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected environment registry",
       "bindsTo": "Environment",
       "columns": [
        "Environment.id",
        "Environment.kind",
        "Environment.name",
        "Environment.cellIds",
        "Environment.requiresApprovalToPromote",
        "Environment.soakHours",
        "Environment.currentReleaseVersion",
        "Environment.isActive"
       ],
       "operation": "listEnvironments",
       "provenance": "contract platform-ops.yaml GET /environments"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Register",
       "operation": "registerEnvironment",
       "provenance": "contract platform-ops.yaml POST /environments"
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
       "impliedBy": "listEnvironments",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "registerEnvironment",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The environment registry list.",
   "error": "Could not load. Names which read failed and leaves the environment registry untouched.",
   "emptyFirstRun": "No environment registry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the environment registry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEnvironments",
    "contract": "platform-ops",
    "purpose": "Environment registry",
    "trigger": "onLoad"
   },
   {
    "operationId": "registerEnvironment",
    "contract": "platform-ops",
    "purpose": "Register an environment",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Environment.id",
    "Environment.kind",
    "Environment.name",
    "Environment.cellIds",
    "Environment.requiresApprovalToPromote"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-028"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "applyMigration": {
  "method": "POST",
  "path": "/migrations/apply",
  "contract": "platform-ops",
  "summary": "Apply a planned migration run",
  "permission": "PLATFORM_MIGRATION_APPLY",
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
 "createRelease": {
  "method": "POST",
  "path": "/releases",
  "contract": "platform-ops",
  "summary": "Cut a release",
  "permission": "PLATFORM_RELEASE_MANAGE",
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
  "requestBody": "CreateReleaseRequest",
  "responds": "Release"
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
 "getMigrationRun": {
  "method": "GET",
  "path": "/migrations/runs/{runId}",
  "contract": "platform-ops",
  "summary": "Migration run progress per cell",
  "permission": "PLATFORM_MIGRATION_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MigrationRun"
 },
 "getRelease": {
  "method": "GET",
  "path": "/releases/{reinventoryHoldId}",
  "contract": "platform-ops",
  "summary": "Read a release with its rollout state",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ReleaseDetail"
 },
 "getReleaseReadiness": {
  "method": "GET",
  "path": "/releases/{reinventoryHoldId}/readiness",
  "contract": "platform-ops",
  "summary": "Whether a release can be promoted, and what blocks it",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ReleaseReadiness"
 },
 "getVersionSkew": {
  "method": "GET",
  "path": "/migrations/version-skew",
  "contract": "platform-ops",
  "summary": "Schema and application version across every cell",
  "permission": "PLATFORM_MIGRATION_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "VersionSkewReport"
 },
 "listEnvironments": {
  "method": "GET",
  "path": "/environments",
  "contract": "platform-ops",
  "summary": "The environment registry",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Environment"
 },
 "listMigrations": {
  "method": "GET",
  "path": "/migrations",
  "contract": "platform-ops",
  "summary": "The migration register",
  "permission": "PLATFORM_MIGRATION_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "appliedTo",
    "in": "query",
    "required": null
   },
   {
    "name": "pendingOnly",
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
 "listReleases": {
  "method": "GET",
  "path": "/releases",
  "contract": "platform-ops",
  "summary": "List releases",
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
    "name": "environment",
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
 "listSupportNotices": {
  "method": "GET",
  "path": "/support-notices",
  "contract": "platform-ops",
  "summary": "End-of-support notices",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SupportNotice"
 },
 "listUpgradeSchedules": {
  "method": "GET",
  "path": "/upgrade-schedules",
  "contract": "platform-ops",
  "summary": "Scheduled tenant upgrades",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "UpgradeSchedule"
 },
 "planMigration": {
  "method": "POST",
  "path": "/migrations/plan",
  "contract": "platform-ops",
  "summary": "Plan a migration run without applying it",
  "permission": "PLATFORM_MIGRATION_VIEW",
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
  "responds": "MigrationPlan"
 },
 "promoteRelease": {
  "method": "POST",
  "path": "/releases/{reinventoryHoldId}/promote",
  "contract": "platform-ops",
  "summary": "Promote a release to the next environment",
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
 "publishSupportNotice": {
  "method": "POST",
  "path": "/support-notices",
  "contract": "platform-ops",
  "summary": "Publish an end-of-support notice",
  "permission": "PLATFORM_RELEASE_MANAGE",
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
  "requestBody": "SupportNotice",
  "responds": "SupportNotice"
 },
 "registerEnvironment": {
  "method": "POST",
  "path": "/environments",
  "contract": "platform-ops",
  "summary": "Register an environment",
  "permission": "PLATFORM_RELEASE_MANAGE",
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
  "requestBody": "Environment",
  "responds": "Environment"
 },
 "rejectRelease": {
  "method": "POST",
  "path": "/releases/{reinventoryHoldId}/reject",
  "contract": "platform-ops",
  "summary": "Reject a release back a stage",
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
 "rollbackMigrationRun": {
  "method": "POST",
  "path": "/migrations/runs/{runId}/rollback",
  "contract": "platform-ops",
  "summary": "Roll a migration run back",
  "permission": "PLATFORM_MIGRATION_APPLY",
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
 "scheduleTenantUpgrade": {
  "method": "POST",
  "path": "/upgrade-schedules",
  "contract": "platform-ops",
  "summary": "Schedule or defer a tenant upgrade",
  "permission": "PLATFORM_RELEASE_MANAGE",
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
  "requestBody": "UpgradeSchedule",
  "responds": "UpgradeSchedule"
 },
 "withdrawRelease": {
  "method": "POST",
  "path": "/releases/{reinventoryHoldId}/withdraw",
  "contract": "platform-ops",
  "summary": "Withdraw a release",
  "permission": "PLATFORM_RELEASE_MANAGE",
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
   }
  }
 },
 "ComponentVersion": {
  "type": "object",
  "required": [
   "component",
   "version"
  ],
  "properties": {
   "component": {
    "type": "string",
    "enum": [
     "backend",
     "frontend",
     "ai",
     "infra",
     "contracts"
    ]
   },
   "version": {
    "type": "string"
   },
   "imageDigest": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "CreateReleaseRequest": {
  "type": "object",
  "required": [
   "version",
   "components",
   "note"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "components": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/ComponentVersion"
    }
   },
   "requiredMigrations": {
    "type": "array",
    "description": "Migration versions this release depends on.",
    "items": {
     "type": "string"
    }
   },
   "note": {
    "type": "string",
    "minLength": 3,
    "maxLength": 2000
   },
   "breakingChanges": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "Environment": {
  "type": "object",
  "x-ticvai-persistence": "control.environment",
  "required": [
   "id",
   "kind",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/EnvironmentKind"
   },
   "name": {
    "type": "string"
   },
   "cellIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresApprovalToPromote": {
    "type": "boolean"
   },
   "soakHours": {
    "type": "integer",
    "description": "How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality.\n"
   },
   "currentReleaseVersion": {
    "type": "string",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "EnvironmentKind": {
  "type": "string",
  "enum": [
   "dev",
   "staging",
   "production"
  ]
 },
 "MigrationPlan": {
  "type": "object",
  "x-ticvai-persistence": "control.migration_plan",
  "required": [
   "id",
   "targetVersion",
   "computedAt",
   "cells",
   "allReversible"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "targetVersion": {
    "type": "string"
   },
   "computedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "A plan is computed against cell state at a moment. Beyond this it is stale and apply refuses it rather than applying to a different world than it was made for.\n"
   },
   "allReversible": {
    "type": "boolean"
   },
   "irreversible": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "totalEstimatedLockMs": {
    "type": "integer"
   },
   "cells": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "cellId": {
       "type": "string",
       "format": "uuid"
      },
      "cellName": {
       "type": "string"
      },
      "tenantSelection": {
       "type": "string",
       "description": "Which of the cell's tenant databases the plan targets. **A plan that can only say \"this region\" cannot express the rollout ADR-0038 makes normal** — a cell is a region holding many tenants, and a wave may be a subset of one.",
       "enum": [
        "all",
        "named"
       ]
      },
      "tenantIds": {
       "type": "array",
       "description": "Present only where `tenantSelection` is `named`. **Named rather than counted**, for the reason `migration_run_cell` gives about partial failure: a set recorded as a number cannot be checked against what actually ran.",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "currentVersion": {
       "type": "string"
      },
      "migrationsToApply": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "estimatedLockMs": {
       "type": "integer"
      },
      "warnings": {
       "type": "array",
       "description": "A long lock on a partitioned table during trading hours is the output this endpoint exists to produce.\n",
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
 "MigrationRun": {
  "type": "object",
  "x-ticvai-persistence": "control.migration_run + control.migration_run_cell + control.migration_run_tenant",
  "description": "One run, its per-region rollup, and its per-tenant outcomes. **The third table exists because ADR-0038 made a cell a region holding many tenants**, and `migration_run_cell`'s own note says it is there so *\"a partial failure is named rather than counted\"* — which is exactly what it stopped doing. A run that fails for twenty of two hundred tenants had one row saying `failed`.\n\nThe rollup stays. *\"How is the UAE doing\"* is a real question and computing it from two hundred rows on every read is not.\n",
  "required": [
   "id",
   "planId",
   "status",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "canary",
     "running",
     "paused",
     "complete",
     "failed",
     "rolledBack"
    ]
   },
   "canaryCellId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Which region the canary tenant is in. **The canary itself is a tenant** — a first cell holding two hundred databases is not a cheap failure, and cheap failure is the only thing a canary is for."
   },
   "canaryTenantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "tenantsTotal": {
    "type": "integer"
   },
   "tenantsComplete": {
    "type": "integer"
   },
   "tenantsFailed": {
    "type": "integer"
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
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "cells": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RolloutCell"
    }
   },
   "tenants": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RolloutTenant"
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
 "Release": {
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReleaseRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status",
     "createdAt"
    ],
    "x-ticvai-persistence": "control.release + control.release_component",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "status": {
      "$ref": "#/components/schemas/ReleaseStatus"
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "promotedToStagingAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "promotedToProductionAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "ReleaseDetail": {
  "allOf": [
   {
    "$ref": "#/components/schemas/Release"
   },
   {
    "type": "object",
    "x-ticvai-persistence": "none — projection",
    "properties": {
     "rollouts": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/Rollout"
      }
     },
     "cellsOnThisVersion": {
      "type": "integer"
     },
     "cellsTotal": {
      "type": "integer"
     }
    }
   }
  ]
 },
 "ReleaseReadiness": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "reinventoryHoldId",
   "canPromote",
   "gates"
  ],
  "properties": {
   "reinventoryHoldId": {
    "type": "string",
    "format": "uuid"
   },
   "canPromote": {
    "type": "boolean"
   },
   "targetEnvironment": {
    "$ref": "#/components/schemas/EnvironmentKind"
   },
   "gates": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "gate",
      "passed"
     ],
     "properties": {
      "gate": {
       "type": "string",
       "enum": [
        "priorEnvironmentHealthy",
        "soakPeriodElapsed",
        "migrationsReversible",
        "noOpenIncidents",
        "approvalRecorded",
        "contractsCompatible"
       ]
      },
      "passed": {
       "type": "boolean"
      },
      "detail": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "ReleaseStatus": {
  "type": "string",
  "enum": [
   "draft",
   "inDev",
   "inStaging",
   "inProduction",
   "superseded",
   "withdrawn"
  ]
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
 "RolloutTenant": {
  "type": "object",
  "x-ticvai-persistence": "control.rollout_tenant",
  "description": "What happened to one tenant database during one run. **The same shape as `RolloutCell` one level down**, and it serves the per-tenant rows of both a rollout and a migration run — which is the arrangement `RolloutCell` already has with `rollout_cell` and `migration_run_cell`.\n\n**`databaseName` is denormalised on purpose.** After a drop the run record still has to say what it touched, and a join to a row that no longer exists says nothing.\n",
  "required": [
   "tenantId",
   "cellId",
   "status"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "databaseName": {
    "type": "string"
   },
   "isCanary": {
    "type": "boolean"
   },
   "wave": {
    "type": "integer",
    "description": "A wave is now a set of tenants and may be a subset of one cell."
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
 "SupportNotice": {
  "type": "object",
  "x-ticvai-persistence": "control.support_notice",
  "required": [
   "id",
   "version",
   "supportEndsAt",
   "publishedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "string"
   },
   "supportEndsAt": {
    "type": "string",
    "format": "date"
   },
   "message": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "affectedTenantIds": {
    "type": "array",
    "readOnly": true,
    "description": "Computed from cell versions, never typed. A notice to the wrong list is worse than none.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "UpgradeSchedule": {
  "type": "object",
  "x-ticvai-persistence": "control.upgrade_schedule",
  "required": [
   "tenantId",
   "releaseVersion",
   "scheduledFor"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "tenantName": {
    "type": "string"
   },
   "releaseVersion": {
    "type": "string"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time"
   },
   "deferredByTenant": {
    "type": "boolean"
   },
   "deferralReason": {
    "type": "string",
    "nullable": true
   },
   "maxDeferralUntil": {
    "type": "string",
    "format": "date-time",
    "description": "Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports.\n"
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "VersionSkewReport": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from cell state",
  "required": [
   "asAt",
   "cells",
   "hasUnexplainedSkew"
  ],
  "properties": {
   "asAt": {
    "type": "string",
    "format": "date-time"
   },
   "hasUnexplainedSkew": {
    "type": "boolean",
    "description": "Skew during a rollout is expected. Skew outside one is a defect, and separating the two is the entire value of this report.\n**An on-premise cell is a third case: legitimately behind, indefinitely**, because the client has not scheduled the window and TICVAI cannot push. It is not counted here and must not appear as a defect (ADR-0017).\n"
   },
   "cells": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "cellId": {
       "type": "string",
       "format": "uuid"
      },
      "cellName": {
       "type": "string"
      },
      "schemaVersion": {
       "type": "string"
      },
      "applicationVersion": {
       "type": "string"
      },
      "isBehind": {
       "type": "boolean"
      },
      "versionsBehind": {
       "type": "integer"
      },
      "reason": {
       "type": "string",
       "nullable": true,
       "enum": [
        "midRollout",
        "rolloutPaused",
        "rolloutFailed",
        "tenantDeferred",
        "onPremiseNotScheduled",
        "unexplained"
       ]
      }
     }
    }
   }
  }
 }
}
```
