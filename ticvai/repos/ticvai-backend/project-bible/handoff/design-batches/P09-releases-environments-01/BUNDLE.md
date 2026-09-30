# P09-releases-environments-01 — P09 · Releases & Environments

**7 screens · 20 operations · 20 schemas · 6 permissions**

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
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-022` | Release & Version Management | listDetail | 7 | 4 | — |
| `ADM-023` | Staging Promotion & Approval | listDetail | 7 | 4 | — |
| `ADM-024` | Release Notification Composer | listDetail | 3 | 1 | — |
| `ADM-025` | Tenant Upgrade Scheduler | listDetail | 2 | 1 | — |
| `ADM-026` | End-of-Support Notice Management | listDetail | 3 | 2 | — |
| `ADM-027` | Database Migration Console | listDetail | 6 | 3 | — |
| `ADM-028` | Environment Registry | listDetail | 2 | 1 | — |

## Thin screens in this batch

**ADM-025, ADM-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-022 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-022 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
       "operation": "listReleases",
       "notes": "Sends `?status=` to `listReleases`.",
       "provenance": "contract platform-ops.yaml GET /releases"
      },
      {
       "kind": "textField",
       "label": "Environment",
       "operation": "listReleases",
       "notes": "Sends `?environment=` to `listReleases`.",
       "provenance": "contract platform-ops.yaml GET /releases"
      },
      {
       "kind": "dataTable",
       "label": "Every release",
       "bindsTo": "Release",
       "columns": [
        "Release.components",
        "Release.requiredMigrations",
        "Release.note",
        "Release.guestReleaseNotes",
        "Release.breakingChanges",
        "Release.id",
        "Release.status",
        "Release.createdByPrincipalId",
        "Release.promotedToStagingAt",
        "Release.promotedToProductionAt"
       ],
       "operation": "listReleases",
       "provenance": "contract platform-ops.yaml GET /releases"
      },
      {
       "kind": "publishGate",
       "impliedBy": "promoteRelease",
       "notes": "Declares `promoteRelease`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected release",
       "bindsTo": "Release",
       "columns": [
        "Release.components",
        "Release.requiredMigrations",
        "Release.note",
        "Release.guestReleaseNotes",
        "Release.breakingChanges",
        "Release.id",
        "Release.status",
        "Release.createdByPrincipalId",
        "Release.promotedToStagingAt",
        "Release.promotedToProductionAt"
       ],
       "operation": "listReleases",
       "provenance": "contract platform-ops.yaml GET /releases"
      },
      {
       "kind": "detailPanel",
       "label": "The release readiness",
       "bindsTo": "ReleaseReadiness",
       "columns": [
        "ReleaseReadiness.releaseId",
        "ReleaseReadiness.canPromote",
        "ReleaseReadiness.targetEnvironment",
        "ReleaseReadiness.gates"
       ],
       "operation": "getReleaseReadiness",
       "provenance": "contract platform-ops.yaml GET /releases/{releaseId}/readiness"
      },
      {
       "kind": "detailPanel",
       "label": "The release",
       "bindsTo": "ReleaseDetail",
       "columns": [
        "ReleaseDetail.rollouts",
        "ReleaseDetail.cellsOnThisVersion",
        "ReleaseDetail.cellsTotal"
       ],
       "operation": "getRelease",
       "provenance": "contract platform-ops.yaml GET /releases/{releaseId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create release",
       "operation": "createRelease",
       "provenance": "contract platform-ops.yaml POST /releases"
      },
      {
       "kind": "secondaryButton",
       "label": "Promote release",
       "operation": "promoteRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/promote"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject release",
       "operation": "rejectRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/reject"
      },
      {
       "kind": "destructiveButton",
       "label": "Withdraw release",
       "operation": "withdrawRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/withdraw"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectRelease",
    "component": "confirmDialog",
    "trigger": "Reject release",
    "body": "**Names what `rejectRelease` changes and what it leaves alone**, in the consequence rather than the verb. A release version this affects should be identified in the dialog, not just counted. **Collects what `rejectRelease` sends before it is called.** Required: `reason`.",
    "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/reject"
   },
   {
    "id": "confirmWithdrawRelease",
    "component": "confirmDialog",
    "trigger": "Withdraw release",
    "body": "**Names what `withdrawRelease` changes and what it leaves alone**, in the consequence rather than the verb. A release version this affects should be identified in the dialog, not just counted. **Collects what `withdrawRelease` sends before it is called.** Required: `reason`.",
    "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/withdraw"
   },
   {
    "id": "formCreateRelease",
    "component": "modal",
    "trigger": "Create release",
    "body": "**Collects what `createRelease` sends before it is called.** Required: `components`, `note`. Optional: `requiredMigrations`, `breakingChanges`, `guestReleaseNotes` (the public \"what's new\" for guests, one short text per locale, naming no person; decided 29 September, rev 3 GAP-B2). Guests read it on the Help screen once the release reaches their cell; `note` stays internal. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReleaseRequest",
    "confirm": {
     "label": "Create release",
     "operation": "createRelease"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "components",
      "note",
      "requiredMigrations",
      "breakingChanges",
      "guestReleaseNotes"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /releases"
   },
   {
    "id": "formPromoteRelease",
    "component": "modal",
    "trigger": "Promote release",
    "body": "**Collects what `promoteRelease` sends before it is called.** Required: `targetEnvironment`, `note`. Optional: `approverPrincipalId`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Promote release",
     "operation": "promoteRelease"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetEnvironment",
      "note",
      "approverPrincipalId",
      "stepUpToken"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/promote"
   }
  ],
  "states": {
   "loading": "The release version list.",
   "error": "Could not load. Names which read failed and leaves the release version untouched.",
   "emptyFirstRun": "No release version yet. Offers Create release (`createRelease`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, environment and the release version are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listReleases` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
   },
   {
    "operationId": "getReleaseReadiness",
    "contract": "platform-ops",
    "purpose": "Which gates pass and which block",
    "trigger": "onAction"
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
     "name": "releaseId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `releaseId`.",
   "preloaded": [
    "Release.components",
    "Release.requiredMigrations",
    "Release.note",
    "Release.breakingChanges",
    "Release.id"
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
    "ADM-029"
   ],
   "flowDerived": true,
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-023 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-023 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-029",
     "trigger": "Watches the rollout per cell",
     "provenance": "flow F04 step 3→4",
     "operation": "promoteRelease",
     "carries": [
      "rolloutId"
     ]
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
       "operation": "listReleases",
       "notes": "Sends `?status=` to `listReleases`.",
       "provenance": "contract platform-ops.yaml GET /releases"
      },
      {
       "kind": "textField",
       "label": "Environment",
       "operation": "listReleases",
       "notes": "Sends `?environment=` to `listReleases`.",
       "provenance": "contract platform-ops.yaml GET /releases"
      },
      {
       "kind": "dataTable",
       "label": "Every release",
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
      },
      {
       "kind": "publishGate",
       "impliedBy": "promoteRelease",
       "notes": "Declares `promoteRelease`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected release",
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
      },
      {
       "kind": "detailPanel",
       "label": "The release",
       "bindsTo": "ReleaseDetail",
       "columns": [
        "ReleaseDetail.rollouts",
        "ReleaseDetail.cellsOnThisVersion",
        "ReleaseDetail.cellsTotal"
       ],
       "operation": "getRelease",
       "provenance": "contract platform-ops.yaml GET /releases/{releaseId}"
      },
      {
       "kind": "detailPanel",
       "label": "The release readiness",
       "bindsTo": "ReleaseReadiness",
       "columns": [
        "ReleaseReadiness.releaseId",
        "ReleaseReadiness.canPromote",
        "ReleaseReadiness.targetEnvironment",
        "ReleaseReadiness.gates"
       ],
       "operation": "getReleaseReadiness",
       "provenance": "contract platform-ops.yaml GET /releases/{releaseId}/readiness"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Promote release",
       "operation": "promoteRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/promote"
      },
      {
       "kind": "secondaryButton",
       "label": "Create release",
       "operation": "createRelease",
       "provenance": "contract platform-ops.yaml POST /releases"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject release",
       "operation": "rejectRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/reject"
      },
      {
       "kind": "destructiveButton",
       "label": "Withdraw release",
       "operation": "withdrawRelease",
       "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/withdraw"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectRelease",
    "component": "confirmDialog",
    "trigger": "Reject release",
    "body": "**Names what `rejectRelease` changes and what it leaves alone**, in the consequence rather than the verb. A staging promotion approval this affects should be identified in the dialog, not just counted. **Collects what `rejectRelease` sends before it is called.** Required: `reason`.",
    "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/reject"
   },
   {
    "id": "confirmWithdrawRelease",
    "component": "confirmDialog",
    "trigger": "Withdraw release",
    "body": "**Names what `withdrawRelease` changes and what it leaves alone**, in the consequence rather than the verb. A staging promotion approval this affects should be identified in the dialog, not just counted. **Collects what `withdrawRelease` sends before it is called.** Required: `reason`.",
    "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/withdraw"
   },
   {
    "id": "formPromoteRelease",
    "component": "modal",
    "trigger": "Promote release",
    "body": "**Collects what `promoteRelease` sends before it is called.** Required: `targetEnvironment`, `note`. Optional: `approverPrincipalId`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Promote release",
     "operation": "promoteRelease"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetEnvironment",
      "note",
      "approverPrincipalId",
      "stepUpToken"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /releases/{releaseId}/promote"
   },
   {
    "id": "formCreateRelease",
    "component": "modal",
    "trigger": "Create release",
    "body": "**Collects what `createRelease` sends before it is called.** Required: `components`, `note`. Optional: `requiredMigrations`, `breakingChanges`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReleaseRequest",
    "confirm": {
     "label": "Create release",
     "operation": "createRelease"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "components",
      "note",
      "requiredMigrations",
      "breakingChanges"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /releases"
   }
  ],
  "states": {
   "loading": "The staging promotion approval list.",
   "error": "Could not load. Names which read failed and leaves the staging promotion approval untouched.",
   "emptyFirstRun": "No staging promotion approval yet. Offers Create release (`createRelease`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, environment and the staging promotion approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `getReleaseReadiness` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "promoteRelease",
    "contract": "platform-ops",
    "purpose": "Promote with an approver",
    "trigger": "onAction"
   },
   {
    "operationId": "getReleaseReadiness",
    "contract": "platform-ops",
    "purpose": "Checked before the request is offered",
    "trigger": "onAction"
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
    "trigger": "onAction"
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
     "name": "releaseId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `releaseId`.",
   "preloaded": [
    "Release.components",
    "Release.requiredMigrations",
    "Release.note",
    "Release.breakingChanges",
    "Release.id"
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
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-024 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-024 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every support notice",
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
      },
      {
       "kind": "dataTable",
       "label": "Every release",
       "bindsTo": "Release",
       "columns": [
        "Release.components",
        "Release.requiredMigrations",
        "Release.note",
        "Release.guestReleaseNotes",
        "Release.breakingChanges",
        "Release.id",
        "Release.status",
        "Release.createdByPrincipalId",
        "Release.promotedToStagingAt",
        "Release.promotedToProductionAt"
       ],
       "operation": "listReleases",
       "provenance": "contract platform-ops.yaml GET /releases"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishSupportNotice",
       "notes": "Declares `publishSupportNotice`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected support notice",
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
      },
      {
       "kind": "detailPanel",
       "label": "What's new for guests",
       "bindsTo": "Release",
       "columns": [
        "Release.version",
        "Release.guestReleaseNotes",
        "Release.promotedToProductionAt"
       ],
       "operation": "listReleases",
       "notes": "**The public, localised release notes a guest reads on the Help screen** (decided 29 September, rev 3 GAP-B2; WEB-025, WEB-045, GST-040 through `getTenantAppStatus.whatsNew`, the ten newest). Written with the release on ADM-022 (`createRelease.guestReleaseNotes`); shown here beside the staff notice so the two are composed together and say the same thing. Distinct from the staff-only recent changes, which name who made each change.",
       "provenance": "contract platform-ops.yaml GET /releases"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish support notice",
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
    }
   ]
  },
  "states": {
   "loading": "The release notification composer list.",
   "error": "Could not load. Names which read failed and leaves the release notification composer untouched.",
   "emptyFirstRun": "No release notification composer yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishSupportNotice",
    "contract": "platform-ops",
    "purpose": "Compose and publish a notice",
    "trigger": "onAction"
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
  "overlays": [
   {
    "id": "formPublishSupportNotice",
    "component": "modal",
    "trigger": "Publish support notice",
    "body": "**Collects what `publishSupportNotice` sends before it is called.** Required: `id`, `supportEndsAt`, `publishedAt`. Optional: `message`, `affectedTenantIds`, `publishedByPrincipalId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SupportNotice",
    "confirm": {
     "label": "Publish support notice",
     "operation": "publishSupportNotice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "supportEndsAt",
      "publishedAt",
      "message",
      "affectedTenantIds",
      "publishedByPrincipalId",
      "scopePath"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /support-notices"
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
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-025 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-025 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
       "label": "Every upgrade schedule",
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
       "label": "The selected upgrade schedule",
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
       "label": "Schedule tenant upgrade",
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
   "emptyFirstRun": "No tenant upgrade scheduler yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listUpgradeSchedules` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listUpgradeSchedules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
  "overlays": [
   {
    "id": "formScheduleTenantUpgrade",
    "component": "modal",
    "trigger": "Schedule tenant upgrade",
    "body": "**Collects what `scheduleTenantUpgrade` sends before it is called.** Required: `releaseVersion`, `scheduledFor`. Optional: `tenantName`, `deferredByTenant`, `deferralReason`, `maxDeferralUntil`, `notifiedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "UpgradeSchedule",
    "confirm": {
     "label": "Schedule tenant upgrade",
     "operation": "scheduleTenantUpgrade"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "releaseVersion",
      "scheduledFor",
      "tenantName",
      "deferredByTenant",
      "deferralReason",
      "maxDeferralUntil",
      "notifiedAt"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /upgrade-schedules"
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
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-026 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-026 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
       "label": "Every support notice",
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
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishSupportNotice",
       "notes": "Declares `publishSupportNotice`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected support notice",
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
       "label": "Publish support notice",
       "operation": "publishSupportNotice",
       "provenance": "contract platform-ops.yaml POST /support-notices"
      },
      {
       "kind": "secondaryButton",
       "label": "Deprecate API version",
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
    }
   ]
  },
  "states": {
   "loading": "The end-of-support notice list.",
   "error": "Could not load. Names which read failed and leaves the end-of-support notice untouched.",
   "emptyFirstRun": "No end-of-support notice yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
  "overlays": [
   {
    "id": "formPublishSupportNotice",
    "component": "modal",
    "trigger": "Publish support notice",
    "body": "**Collects what `publishSupportNotice` sends before it is called.** Required: `id`, `supportEndsAt`, `publishedAt`. Optional: `message`, `affectedTenantIds`, `publishedByPrincipalId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SupportNotice",
    "confirm": {
     "label": "Publish support notice",
     "operation": "publishSupportNotice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "supportEndsAt",
      "publishedAt",
      "message",
      "affectedTenantIds",
      "publishedByPrincipalId",
      "scopePath"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /support-notices"
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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-027 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-027 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Applied to",
       "operation": "listMigrations",
       "notes": "Sends `?appliedTo=` to `listMigrations`.",
       "provenance": "contract platform-ops.yaml GET /migrations"
      },
      {
       "kind": "toggle",
       "label": "Pending only",
       "operation": "listMigrations",
       "notes": "Sends `?pendingOnly=` to `listMigrations`.",
       "provenance": "contract platform-ops.yaml GET /migrations"
      },
      {
       "kind": "dataTable",
       "label": "Every migration",
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
       "label": "The selected migration",
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
      },
      {
       "kind": "detailPanel",
       "label": "The migration run",
       "bindsTo": "MigrationRun",
       "columns": [
        "MigrationRun.id",
        "MigrationRun.planId",
        "MigrationRun.status",
        "MigrationRun.canaryCellId",
        "MigrationRun.canaryTenantId",
        "MigrationRun.tenantsTotal",
        "MigrationRun.tenantsComplete",
        "MigrationRun.tenantsFailed",
        "MigrationRun.cellsTotal",
        "MigrationRun.cellsComplete",
        "MigrationRun.cellsFailed",
        "MigrationRun.startedByPrincipalId",
        "MigrationRun.startedAt",
        "MigrationRun.completedAt",
        "MigrationRun.cells",
        "MigrationRun.tenants"
       ],
       "operation": "getMigrationRun",
       "provenance": "contract platform-ops.yaml GET /migrations/runs/{runId}"
      },
      {
       "kind": "detailPanel",
       "label": "The version skew report",
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
       "label": "Plan migration",
       "operation": "planMigration",
       "provenance": "contract platform-ops.yaml POST /migrations/plan"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply migration",
       "operation": "applyMigration",
       "provenance": "contract platform-ops.yaml POST /migrations/apply"
      },
      {
       "kind": "secondaryButton",
       "label": "Rollback migration run",
       "operation": "rollbackMigrationRun",
       "provenance": "contract platform-ops.yaml POST /migrations/runs/{runId}/rollback"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The database migration console list.",
   "error": "Could not load. Names which read failed and leaves the database migration console untouched.",
   "emptyFirstRun": "No database migration console yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on appliedTo, pendingOnly and the database migration console are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_MIGRATION_VIEW`, which `listMigrations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
   },
   {
    "operationId": "applyMigration",
    "contract": "platform-ops",
    "purpose": "Apply a reviewed plan",
    "trigger": "onAction"
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
    "Migration.module",
    "Migration.description",
    "Migration.isReversible",
    "Migration.rollbackTestedAt",
    "Migration.checksum"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-027"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPlanMigration",
    "component": "modal",
    "trigger": "Plan migration",
    "body": "**Collects what `planMigration` sends before it is called.** Required: `targetVersion`. Optional: `cellIds`, `environment`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Plan migration",
     "operation": "planMigration"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetVersion",
      "cellIds",
      "environment"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /migrations/plan"
   },
   {
    "id": "formApplyMigration",
    "component": "modal",
    "trigger": "Apply migration",
    "body": "**Collects what `applyMigration` sends before it is called.** Required: `planId`, `stepUpToken`. Optional: `canaryCellId`, `haltOnFirstFailure`, `maintenanceWindow`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Apply migration",
     "operation": "applyMigration"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "planId",
      "stepUpToken",
      "canaryCellId",
      "haltOnFirstFailure",
      "maintenanceWindow"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /migrations/apply"
   },
   {
    "id": "formRollbackMigrationRun",
    "component": "modal",
    "trigger": "Rollback migration run",
    "body": "**Collects what `rollbackMigrationRun` sends before it is called.** Required: `reason`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Rollback migration run",
     "operation": "rollbackMigrationRun"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "stepUpToken"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /migrations/runs/{runId}/rollback"
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
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-028 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-028 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
       "label": "Every environment",
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
       "label": "The selected environment",
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
       "label": "Register environment",
       "operation": "registerEnvironment",
       "provenance": "contract platform-ops.yaml POST /environments"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The environment registry list.",
   "error": "Could not load. Names which read failed and leaves the environment registry untouched.",
   "emptyFirstRun": "No environment registry yet. Offers Register environment (`registerEnvironment`).",
   "emptyNoResults": "Never shown: `listEnvironments` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listEnvironments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
  "overlays": [
   {
    "id": "formRegisterEnvironment",
    "component": "modal",
    "trigger": "Register environment",
    "body": "**Collects what `registerEnvironment` sends before it is called.** Required: `id`, `kind`, `name`. Optional: `cellIds`, `requiresApprovalToPromote`, `soakHours`, `currentReleaseVersion`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Environment",
    "confirm": {
     "label": "Register environment",
     "operation": "registerEnvironment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "name",
      "cellIds",
      "requiresApprovalToPromote",
      "soakHours",
      "currentReleaseVersion",
      "isActive"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /environments"
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
  "path": "/releases/{releaseId}",
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
  "path": "/releases/{releaseId}/readiness",
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
  "path": "/releases/{releaseId}/promote",
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
  "path": "/releases/{releaseId}/reject",
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
  "path": "/releases/{releaseId}/withdraw",
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
    "maxLength": 2000,
    "description": "Internal. Never shown to guests; `guestReleaseNotes` is."
   },
   "guestReleaseNotes": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "**The public, localised \"what's new\" for guests** (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and naming no person. Public once the release reaches the tenant's cell; read by the guest Help screen (WEB-025, WEB-045, GST-040) through `white-label.getTenantAppStatus`. Distinct from the staff-only `TenantAppStatus.recentChanges`, which names the principal behind each change and stays staff only.\n"
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
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "Migration": {
  "type": "object",
  "x-ticvai-persistence": "control.migration",
  "required": [
   "version",
   "module",
   "isReversible",
   "checksum"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "module": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "isReversible": {
    "type": "boolean",
    "description": "A rollback section exists and CI has executed it against a restored snapshot. A rollback nobody has run is a comment, not a rollback.\n"
   },
   "rollbackTestedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "checksum": {
    "type": "string",
    "description": "Compared on apply. A migration edited after it was applied somewhere is a defect the register catches, not a mystery to debug later.\n"
   },
   "estimatedLockMs": {
    "type": "integer",
    "nullable": true
   },
   "touchesPartitionedTable": {
    "type": "boolean"
   },
   "appliedCellCount": {
    "type": "integer"
   },
   "pendingCellCount": {
    "type": "integer"
   }
  }
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
     "$ref": "#/components/schemas/MigrationRunCell"
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
 "MigrationRunCell": {
  "type": "object",
  "x-ticvai-persistence": "none — rows of control.migration_run_cell, stored through MigrationRun",
  "description": "One cell's rollup within one migration run. **The fields of `RolloutCell` without its `rolloutId`**: a migration run is not a rollout, and its parent key `migration_run_id` comes from `MigrationRun.cells`.\n",
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
   "releaseId",
   "canPromote",
   "gates"
  ],
  "properties": {
   "releaseId": {
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
   "releaseId",
   "environment",
   "status",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "releaseId": {
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
 "RolloutTenant": {
  "type": "object",
  "x-ticvai-persistence": "control.rollout_tenant",
  "description": "What happened to one tenant database during one run. **The same shape as `RolloutCell` one level down**, and it serves the per-tenant rows of both a rollout and a migration run — the arrangement `RolloutCell` had with `rollout_cell` and `migration_run_cell` until `rollout_cell` needed its `rolloutId` parent key and the migration run's cells moved to `MigrationRunCell`.\n\n**`databaseName` is denormalised on purpose.** After a drop the run record still has to say what it touched, and a join to a row that no longer exists says nothing.\n",
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
