# P08-people-access-rights-01 — P08 · People & Access Rights (1 of 2)

**10 screens · 39 operations · 32 schemas · 11 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `ANNOUNCEMENT_PUBLISH, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW, ATTENDANCE_RECORD, PERMISSION_VIEW, ROLE_MANAGE, USER_MANAGE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-053` | Staff Directory | listDetail | 10 | 3 | — |
| `BO-054` | Role Assignment | listDetail | 7 | 1 | — |
| `BO-055` | Rota & Scheduling | listDetail | 4 | 3 | — |
| `BO-056` | Time & Attendance | listDetail | 3 | 2 | — |
| `BO-057` | Training & Certification | listDetail | 1 | 0 | — |
| `BO-066` | Notification Settings | listDetail | 4 | 1 | — |
| `BO-084` | Approval Inbox | approvalInbox | 4 | 2 | — |
| `BO-085` | Approval Request | approvalInbox | 5 | 4 | — |
| `BO-086` | Approval Matrix | listDetail | 2 | 1 | — |
| `BO-087` | Approval Delegations | listDetail | 3 | 2 | — |

## Thin screens in this batch

**BO-054 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-053",
  "name": "Staff Directory",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/staff-directory",
   "component": "apps/venue-management-web/src/routes/venue-operations/StaffDirectoryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": true
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 31 August** — `Marketing Board 1.dc.html` frame `crm-1b` (*Guest Directory*), matched on title at 0.80 within this board’s platforms.",
  "density": "compact",
  "boardFrames": [
   "Marketing Board 1.dc.html#crm-1b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPrincipals` reads the population and `getPrincipal` reads one of them — list, select, act",
  "purpose": "Find anyone who works at this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Scope path",
       "operation": "listPrincipals",
       "notes": "Sends `?scopePath=` to `listPrincipals`.",
       "provenance": "contract identity.yaml GET /principals"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listPrincipals",
       "notes": "Sends `?isActive=` to `listPrincipals`.",
       "provenance": "contract identity.yaml GET /principals"
      },
      {
       "kind": "dataTable",
       "label": "Every principal",
       "bindsTo": "Principal",
       "columns": [
        "Principal.id",
        "Principal.username",
        "Principal.displayName",
        "Principal.isActive",
        "Principal.validFrom",
        "Principal.validTo",
        "Principal.primaryRoleId",
        "Principal.roles",
        "Principal.lastLoginAt"
       ],
       "operation": "listPrincipals",
       "provenance": "contract identity.yaml GET /principals"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected principal",
       "bindsTo": "Principal",
       "columns": [
        "Principal.id",
        "Principal.username",
        "Principal.displayName",
        "Principal.isActive",
        "Principal.validFrom",
        "Principal.validTo",
        "Principal.primaryRoleId",
        "Principal.roles",
        "Principal.lastLoginAt"
       ],
       "operation": "getPrincipal",
       "provenance": "contract identity.yaml GET /principals/{principalId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create principal",
       "operation": "createPrincipal",
       "provenance": "contract identity.yaml POST /principals"
      },
      {
       "kind": "secondaryButton",
       "label": "Save principal",
       "operation": "updatePrincipal",
       "provenance": "contract identity.yaml PATCH /principals/{principalId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Reset principal credential",
       "operation": "resetPrincipalCredential",
       "provenance": "contract identity.yaml POST /principals/{principalId}/credential-reset"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staff list.",
   "error": "Could not load. Names which read failed and leaves the staff untouched.",
   "emptyFirstRun": "No staff yet. Offers Create principal (`createPrincipal`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on scopePath, isActive and the staff are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "resetPrincipalCredential",
    "contract": "identity",
    "purpose": "Reset a forgotten password or PIN",
    "trigger": "onAction"
   },
   {
    "operationId": "listPrincipals",
    "contract": "identity",
    "purpose": "List principals",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPrincipal",
    "contract": "identity",
    "purpose": "Read a principal",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPrincipal",
    "contract": "identity",
    "purpose": "Create a principal",
    "trigger": "onAction",
    "invalidates": [
     "listPrincipals"
    ]
   },
   {
    "operationId": "updatePrincipal",
    "contract": "identity",
    "purpose": "Update or deactivate a principal",
    "trigger": "onAction",
    "invalidates": [
     "listPrincipals"
    ]
   },
   {
    "operationId": "listJobTitles",
    "contract": "workforce",
    "purpose": "Job titles",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setJobTitle",
    "contract": "workforce",
    "purpose": "Define a job title",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listJobTitles"
    ]
   },
   {
    "operationId": "listWorkAssignments",
    "contract": "workforce",
    "purpose": "Who is posted to which job title at which venue",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setWorkAssignment",
    "contract": "workforce",
    "purpose": "Post a person to a job title at a venue",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listJobTitles",
     "listWorkAssignments"
    ]
   },
   {
    "operationId": "suggestRoleAssignment",
    "contract": "identity",
    "purpose": "Roles to grant a new or moved member of staff (by principal, or by job title and posting before the principal exists)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "principalId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Principal.id",
    "Principal.username",
    "Principal.displayName",
    "Principal.isActive",
    "Principal.validFrom"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-053",
   "derivedFrom": "wireframes/reference/Marketing Board 1.dc.html",
   "note": "**Drawn by Claude Design on `Marketing Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "confirmResetPrincipalCredential",
    "component": "confirmDialog",
    "trigger": "Reset principal credential",
    "body": "**Names what `resetPrincipalCredential` changes and what it leaves alone**, in the consequence rather than the verb. A staff this affects should be identified in the dialog, not just counted. **Collects what `resetPrincipalCredential` sends before it is called.** Required: `method`, `temporaryCredential`, `reason`.",
    "bindsTo": "ResetCredentialRequest",
    "provenance": "contract identity.yaml POST /principals/{principalId}/credential-reset"
   },
   {
    "id": "formCreatePrincipal",
    "component": "modal",
    "trigger": "Create principal",
    "body": "**Collects what `createPrincipal` sends before it is called.** Required: `username`, `displayName`. Optional: `initialCredential`, `mustChangeCredential`, `validTo`, `roleIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePrincipalRequest",
    "confirm": {
     "label": "Create principal",
     "operation": "createPrincipal"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "username",
      "displayName",
      "initialCredential",
      "mustChangeCredential",
      "validTo",
      "roleIds"
     ]
    },
    "provenance": "contract identity.yaml POST /principals"
   },
   {
    "id": "formUpdatePrincipal",
    "component": "modal",
    "trigger": "Save principal",
    "body": "**Collects what `updatePrincipal` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `isActive`, `validTo`, `primaryRoleId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save principal",
     "operation": "updatePrincipal"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "displayName",
      "isActive",
      "validTo",
      "primaryRoleId"
     ]
    },
    "provenance": "contract identity.yaml PATCH /principals/{principalId}"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-054",
  "name": "Role Assignment",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/role-assignment",
   "component": "apps/venue-management-web/src/routes/venue-operations/RoleAssignmentDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": true
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listRoles` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Give somebody the permissions their job needs.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every role",
       "bindsTo": "Role",
       "columns": [
        "Role.id",
        "Role.code",
        "Role.name",
        "Role.description",
        "Role.permissions",
        "Role.inheritsFromRoleId",
        "Role.isSystem",
        "Role.principalCount",
        "Role.grantCount"
       ],
       "operation": "listRoles",
       "provenance": "contract identity.yaml GET /roles"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected role",
       "bindsTo": "Role",
       "columns": [
        "Role.id",
        "Role.code",
        "Role.name",
        "Role.description",
        "Role.permissions",
        "Role.inheritsFromRoleId",
        "Role.isSystem",
        "Role.principalCount",
        "Role.grantCount"
       ],
       "operation": "listRoles",
       "provenance": "contract identity.yaml GET /roles"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create role",
       "operation": "createRole",
       "provenance": "contract identity.yaml POST /roles"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The role assignment list.",
   "error": "Could not load. Names which read failed and leaves the role assignment untouched.",
   "emptyFirstRun": "No role assignment yet. Offers Create role (`createRole`).",
   "emptyNoResults": "Never shown: `listRoles` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRoles",
    "contract": "identity",
    "purpose": "List roles",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRole",
    "contract": "identity",
    "purpose": "Create a role",
    "trigger": "onAction",
    "invalidates": [
     "listRoles"
    ]
   },
   {
    "operationId": "setCapabilityTemplate",
    "contract": "identity",
    "purpose": "Save a tick-set of permissions under a name",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listRoles"
    ]
   },
   {
    "operationId": "listPermissionFindings",
    "contract": "identity",
    "purpose": "Unused and missing permissions for the role being assigned",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "suggestRoleAssignment",
    "contract": "identity",
    "purpose": "Suggested roles for the selected person from peers with the same job title and posting",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAccessReviewCampaigns",
    "contract": "identity",
    "purpose": "Open access reviews",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAccessReviewItems",
    "contract": "identity",
    "purpose": "My pending review items (assignedToMe)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Role.id",
    "Role.code",
    "Role.name",
    "Role.description",
    "Role.permissions"
   ],
   "params": [
    {
     "name": "campaignId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-054"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateRole",
    "component": "modal",
    "trigger": "Create role",
    "body": "**Collects what `createRole` sends before it is called.** Required: `code`, `name`. Optional: `description`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create role",
     "operation": "createRole"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "description"
     ]
    },
    "provenance": "contract identity.yaml POST /roles"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-055",
  "name": "Rota & Scheduling",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/rota-scheduling",
   "component": "apps/venue-management-web/src/routes/venue-operations/RotaSchedulingDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": true
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listRotaAssignments` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Decide who is on which gate, when.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listRotaAssignments",
       "notes": "Sends `?from=` to `listRotaAssignments`.",
       "provenance": "contract workforce.yaml GET /rota-assignments"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "listRotaAssignments",
       "notes": "Sends `?to=` to `listRotaAssignments`.",
       "provenance": "contract workforce.yaml GET /rota-assignments"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listRotaAssignments",
       "notes": "Sends `?principalId=` to `listRotaAssignments`.",
       "provenance": "contract workforce.yaml GET /rota-assignments"
      },
      {
       "kind": "textField",
       "label": "Department id",
       "operation": "listRotaAssignments",
       "notes": "Sends `?departmentId=` to `listRotaAssignments`.",
       "provenance": "contract workforce.yaml GET /rota-assignments"
      },
      {
       "kind": "dataTable",
       "label": "Every rota assignment",
       "bindsTo": "RotaAssignment",
       "columns": [
        "RotaAssignment.overtimeMinutes",
        "RotaAssignment.restPeriodBefore",
        "RotaAssignment.breachesWorkingHourLimit",
        "RotaAssignment.labourCost",
        "RotaAssignment.id",
        "RotaAssignment.principalId",
        "RotaAssignment.displayName",
        "RotaAssignment.venueId",
        "RotaAssignment.departmentId",
        "RotaAssignment.position",
        "RotaAssignment.requiredRoleId",
        "RotaAssignment.workstationId"
       ],
       "operation": "listRotaAssignments",
       "provenance": "contract workforce.yaml GET /rota-assignments"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rota assignment",
       "bindsTo": "RotaAssignment",
       "columns": [
        "RotaAssignment.overtimeMinutes",
        "RotaAssignment.restPeriodBefore",
        "RotaAssignment.breachesWorkingHourLimit",
        "RotaAssignment.labourCost",
        "RotaAssignment.id",
        "RotaAssignment.principalId",
        "RotaAssignment.displayName",
        "RotaAssignment.venueId",
        "RotaAssignment.departmentId",
        "RotaAssignment.position",
        "RotaAssignment.requiredRoleId",
        "RotaAssignment.workstationId",
        "RotaAssignment.startsAt",
        "RotaAssignment.endsAt",
        "RotaAssignment.status",
        "RotaAssignment.breakMinutes"
       ],
       "operation": "listRotaAssignments",
       "provenance": "contract workforce.yaml GET /rota-assignments"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create rota assignment",
       "operation": "createRotaAssignment",
       "provenance": "contract workforce.yaml POST /rota-assignments"
      },
      {
       "kind": "secondaryButton",
       "label": "Save rota assignment",
       "operation": "updateRotaAssignment",
       "provenance": "contract workforce.yaml PATCH /rota-assignments/{assignmentId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Request shift swap",
       "operation": "requestShiftSwap",
       "provenance": "contract workforce.yaml POST /rota-assignments/{assignmentId}/swap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rota scheduling list.",
   "error": "Could not load. Names which read failed and leaves the rota scheduling untouched.",
   "emptyFirstRun": "No rota scheduling yet. Offers Create rota assignment (`createRotaAssignment`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on from, to, principalId, departmentId and the rota scheduling are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRotaAssignments",
    "contract": "workforce",
    "purpose": "The rota",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRotaAssignment",
    "contract": "workforce",
    "purpose": "Put someone on the rota",
    "trigger": "onAction",
    "invalidates": [
     "listRotaAssignments"
    ]
   },
   {
    "operationId": "updateRotaAssignment",
    "contract": "workforce",
    "purpose": "Move or cancel an assignment",
    "trigger": "onAction",
    "invalidates": [
     "listRotaAssignments"
    ]
   },
   {
    "operationId": "requestShiftSwap",
    "contract": "workforce",
    "purpose": "Ask someone to take your shift",
    "trigger": "onAction",
    "invalidates": [
     "listRotaAssignments"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "assignmentId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `assignmentId`.",
   "preloaded": [
    "RotaAssignment.overtimeMinutes",
    "RotaAssignment.restPeriodBefore",
    "RotaAssignment.breachesWorkingHourLimit",
    "RotaAssignment.labourCost",
    "RotaAssignment.id"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-055"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateRotaAssignment",
    "component": "modal",
    "trigger": "Create rota assignment",
    "body": "**Collects what `createRotaAssignment` sends before it is called.** Required: `principalId`, `venueId`, `position`, `startsAt`, `endsAt`. Optional: `overtimeMinutes`, `restPeriodBefore`, `breachesWorkingHourLimit`, `labourCost`, `id`, `displayName`, `departmentId`, `requiredRoleId`, `workstationId`, `status`, `breakMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RotaAssignment",
    "confirm": {
     "label": "Create rota assignment",
     "operation": "createRotaAssignment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "principalId",
      "venueId",
      "position",
      "startsAt",
      "endsAt",
      "overtimeMinutes",
      "restPeriodBefore",
      "breachesWorkingHourLimit",
      "labourCost",
      "id",
      "displayName",
      "departmentId",
      "requiredRoleId",
      "workstationId",
      "status",
      "breakMinutes",
      "note"
     ]
    },
    "provenance": "contract workforce.yaml POST /rota-assignments"
   },
   {
    "id": "formUpdateRotaAssignment",
    "component": "modal",
    "trigger": "Save rota assignment",
    "body": "**Collects what `updateRotaAssignment` sends before it is called.** Required: `principalId`, `venueId`, `position`, `startsAt`, `endsAt`. Optional: `overtimeMinutes`, `restPeriodBefore`, `breachesWorkingHourLimit`, `labourCost`, `id`, `displayName`, `departmentId`, `requiredRoleId`, `workstationId`, `status`, `breakMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RotaAssignment",
    "confirm": {
     "label": "Save rota assignment",
     "operation": "updateRotaAssignment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "principalId",
      "venueId",
      "position",
      "startsAt",
      "endsAt",
      "overtimeMinutes",
      "restPeriodBefore",
      "breachesWorkingHourLimit",
      "labourCost",
      "id",
      "displayName",
      "departmentId",
      "requiredRoleId",
      "workstationId",
      "status",
      "breakMinutes",
      "note"
     ]
    },
    "provenance": "contract workforce.yaml PATCH /rota-assignments/{assignmentId}"
   },
   {
    "id": "formRequestShiftSwap",
    "component": "modal",
    "trigger": "Request shift swap",
    "body": "**Collects what `requestShiftSwap` sends before it is called.** Required: `toPrincipalId`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request shift swap",
     "operation": "requestShiftSwap"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "toPrincipalId",
      "reason"
     ]
    },
    "provenance": "contract workforce.yaml POST /rota-assignments/{assignmentId}/swap"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-056",
  "name": "Time & Attendance",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/time-attendance",
   "component": "apps/venue-management-web/src/routes/venue-operations/TimeAttendanceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": true
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAttendance` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Record who actually turned up.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "datePicker",
       "label": "Date",
       "operation": "listAttendance",
       "notes": "Sends `?date=` to `listAttendance`.",
       "provenance": "contract workforce.yaml GET /attendance"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listAttendance",
       "notes": "Sends `?principalId=` to `listAttendance`.",
       "provenance": "contract workforce.yaml GET /attendance"
      },
      {
       "kind": "toggle",
       "label": "Exceptions only",
       "operation": "listAttendance",
       "notes": "Sends `?exceptionsOnly=` to `listAttendance`.",
       "provenance": "contract workforce.yaml GET /attendance"
      },
      {
       "kind": "dataTable",
       "label": "Every attendance",
       "bindsTo": "AttendanceRecord",
       "columns": [
        "AttendanceRecord.id",
        "AttendanceRecord.principalId",
        "AttendanceRecord.assignmentId",
        "AttendanceRecord.venueId",
        "AttendanceRecord.kind",
        "AttendanceRecord.occurredAt",
        "AttendanceRecord.recordedAt",
        "AttendanceRecord.accessPointId",
        "AttendanceRecord.latitude",
        "AttendanceRecord.longitude",
        "AttendanceRecord.isAmended",
        "AttendanceRecord.amendedByPrincipalId"
       ],
       "operation": "listAttendance",
       "provenance": "contract workforce.yaml GET /attendance"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected attendance",
       "bindsTo": "AttendanceRecord",
       "columns": [
        "AttendanceRecord.id",
        "AttendanceRecord.principalId",
        "AttendanceRecord.assignmentId",
        "AttendanceRecord.venueId",
        "AttendanceRecord.kind",
        "AttendanceRecord.occurredAt",
        "AttendanceRecord.recordedAt",
        "AttendanceRecord.accessPointId",
        "AttendanceRecord.latitude",
        "AttendanceRecord.longitude",
        "AttendanceRecord.isAmended",
        "AttendanceRecord.amendedByPrincipalId",
        "AttendanceRecord.amendmentReason",
        "AttendanceRecord.originalOccurredAt",
        "AttendanceRecord.amendments",
        "AttendanceRecord.exception"
       ],
       "operation": "listAttendance",
       "provenance": "contract workforce.yaml GET /attendance"
      },
      {
       "kind": "dataTable",
       "label": "Amendment history",
       "bindsTo": "AttendanceAmendment",
       "columns": [
        "AttendanceAmendment.amendedAt",
        "AttendanceAmendment.amendedByPrincipalId",
        "AttendanceAmendment.occurredAtBefore",
        "AttendanceAmendment.occurredAtAfter",
        "AttendanceAmendment.reason"
       ],
       "operation": "listAttendance",
       "notes": "**Every correction, not only the last** (decided 28 September, audit R129 (7)) — read from `AttendanceRecord.amendments`: who, when, before, after and why.",
       "provenance": "contract workforce.yaml GET /attendance"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Amend attendance",
       "operation": "amendAttendance",
       "provenance": "contract workforce.yaml POST /attendance/{recordId}/amend"
      },
      {
       "kind": "secondaryButton",
       "label": "Record attendance",
       "operation": "recordAttendance",
       "provenance": "contract workforce.yaml POST /attendance/clock"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The time attendance list.",
   "error": "Could not load. Names which read failed and leaves the time attendance untouched.",
   "emptyFirstRun": "No time attendance yet. Offers Record attendance (`recordAttendance`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on date, principalId, exceptionsOnly and the time attendance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAttendance",
    "contract": "workforce",
    "purpose": "Who was here",
    "trigger": "onLoad"
   },
   {
    "operationId": "amendAttendance",
    "contract": "workforce",
    "purpose": "A supervisor corrects a record",
    "trigger": "onAction",
    "invalidates": [
     "listAttendance"
    ]
   },
   {
    "operationId": "recordAttendance",
    "contract": "workforce",
    "purpose": "Clock in, clock out, or take a break",
    "trigger": "onAction",
    "invalidates": [
     "listAttendance"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "recordId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `recordId`.",
   "preloaded": [
    "AttendanceRecord.id",
    "AttendanceRecord.principalId",
    "AttendanceRecord.assignmentId",
    "AttendanceRecord.venueId",
    "AttendanceRecord.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-056"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAmendAttendance",
    "component": "modal",
    "trigger": "Amend attendance",
    "body": "**Collects what `amendAttendance` sends before it is called.** Required: `correctedAt`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Amend attendance",
     "operation": "amendAttendance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "correctedAt",
      "reason"
     ]
    },
    "provenance": "contract workforce.yaml POST /attendance/{recordId}/amend"
   },
   {
    "id": "formRecordAttendance",
    "component": "modal",
    "trigger": "Record attendance",
    "body": "**Collects what `recordAttendance` sends before it is called.** Required: `kind`, `occurredAt`. Optional: `assignmentId`, `accessPointId`, `latitude`, `longitude`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record attendance",
     "operation": "recordAttendance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "occurredAt",
      "assignmentId",
      "accessPointId",
      "latitude",
      "longitude"
     ]
    },
    "provenance": "contract workforce.yaml POST /attendance/clock"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-057",
  "name": "Training & Certification",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 3,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/training-certification",
   "component": "apps/venue-management-web/src/routes/venue-operations/TrainingCertificationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": true
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPrincipals` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Know who is allowed to do what.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Scope path",
       "operation": "listPrincipals",
       "notes": "Sends `?scopePath=` to `listPrincipals`.",
       "provenance": "contract identity.yaml GET /principals"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listPrincipals",
       "notes": "Sends `?isActive=` to `listPrincipals`.",
       "provenance": "contract identity.yaml GET /principals"
      },
      {
       "kind": "dataTable",
       "label": "Every principal",
       "bindsTo": "Principal",
       "columns": [
        "Principal.id",
        "Principal.username",
        "Principal.displayName",
        "Principal.isActive",
        "Principal.validFrom",
        "Principal.validTo",
        "Principal.primaryRoleId",
        "Principal.roles",
        "Principal.lastLoginAt"
       ],
       "operation": "listPrincipals",
       "provenance": "contract identity.yaml GET /principals"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected principal",
       "bindsTo": "Principal",
       "columns": [
        "Principal.id",
        "Principal.username",
        "Principal.displayName",
        "Principal.isActive",
        "Principal.validFrom",
        "Principal.validTo",
        "Principal.primaryRoleId",
        "Principal.roles",
        "Principal.lastLoginAt"
       ],
       "operation": "listPrincipals",
       "provenance": "contract identity.yaml GET /principals"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The training certification list.",
   "error": "Could not load. Names which read failed and leaves the training certification untouched.",
   "emptyFirstRun": "No training certification yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on scopePath, isActive and the training certification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrincipals",
    "contract": "identity",
    "purpose": "List principals",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Principal.id",
    "Principal.username",
    "Principal.displayName",
    "Principal.isActive",
    "Principal.validFrom"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-057"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-066",
  "name": "Notification Settings",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/notification-settings",
   "component": "apps/venue-management-web/src/routes/venue-operations/NotificationSettingsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": true
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act",
  "purpose": "Decide what this venue tells people, and how.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "toggle",
       "label": "Unacknowledged only",
       "operation": "listAnnouncements",
       "notes": "Sends `?unacknowledgedOnly=` to `listAnnouncements`.",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "dataTable",
       "label": "Every announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishAnnouncement",
       "notes": "Declares `publishAnnouncement`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "detailPanel",
       "label": "The announcement reach",
       "bindsTo": "AnnouncementReach",
       "columns": [
        "AnnouncementReach.announcementId",
        "AnnouncementReach.targeted",
        "AnnouncementReach.delivered",
        "AnnouncementReach.acknowledged",
        "AnnouncementReach.outstanding"
       ],
       "operation": "getAnnouncementReach",
       "provenance": "contract workforce.yaml GET /announcements/{announcementId}/reach"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish announcement",
       "operation": "publishAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements"
      },
      {
       "kind": "secondaryButton",
       "label": "Acknowledge announcement",
       "operation": "acknowledgeAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements/{announcementId}/acknowledge"
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
   "loading": "The notification settings list.",
   "error": "Could not load. Names which read failed and leaves the notification settings untouched.",
   "emptyFirstRun": "No notification settings yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on unacknowledgedOnly and the notification settings are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAnnouncements",
    "contract": "workforce",
    "purpose": "What staff have been told",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishAnnouncement",
    "contract": "workforce",
    "purpose": "Tell staff something",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   },
   {
    "operationId": "acknowledgeAnnouncement",
    "contract": "workforce",
    "purpose": "Confirm you have read it",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   },
   {
    "operationId": "getAnnouncementReach",
    "contract": "workforce",
    "purpose": "Who has acknowledged, and who has not",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "announcementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `announcementId`.",
   "preloaded": [
    "Announcement.id",
    "Announcement.title",
    "Announcement.body",
    "Announcement.kind",
    "Announcement.venueIds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-066"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPublishAnnouncement",
    "component": "modal",
    "trigger": "Publish announcement",
    "body": "**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Announcement",
    "confirm": {
     "label": "Publish announcement",
     "operation": "publishAnnouncement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "body",
      "kind",
      "publishedAt",
      "id",
      "venueIds",
      "departmentIds",
      "roleIds",
      "requiresAcknowledgement",
      "expiresAt",
      "publishedByPrincipalId",
      "locale"
     ]
    },
    "provenance": "contract workforce.yaml POST /announcements"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-084",
  "name": "Approval Inbox",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/approvals/approval-inbox",
   "component": "apps/venue-management-web/src/routes/approvals/ApprovalInbox.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-052",
    "BO-085",
    "BO-086",
    "BO-087"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-052",
     "trigger": "The goods arrive and are received",
     "provenance": "flow F15 step 3→4"
    },
    {
     "to": "BO-087",
     "trigger": "Approval Delegations",
     "provenance": "derived — BO-087 declares entryState.params delegationId and BO-084 holds none of them. The edge carries nothing: delegationId only pre-selects (deep link or optional), and BO-087 opens on its own"
    },
    {
     "to": "BO-085",
     "trigger": "Approves it",
     "provenance": "flow F14 step 3→4",
     "operation": "listApprovalRequests",
     "carries": [
      "requestId"
     ]
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`decideApprovalRequest` decides items that `listApprovalRequests` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "What is waiting on this person, sorted by what breaches soonest.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "toggle",
       "label": "Assigned to me",
       "operation": "listApprovalRequests",
       "notes": "Sends `?assignedToMe=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "toggle",
       "label": "Raised by me",
       "operation": "listApprovalRequests",
       "notes": "Sends `?raisedByMe=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listApprovalRequests",
       "notes": "Sends `?status=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listApprovalRequests",
       "notes": "Sends `?kind=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "numberField",
       "label": "Breaching within minutes",
       "operation": "listApprovalRequests",
       "notes": "Sends `?breachingWithinMinutes=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "ApprovalRequest",
       "columns": [
        "ApprovalRequest.id",
        "ApprovalRequest.kind",
        "ApprovalRequest.rerouteOnNoApprover",
        "ApprovalRequest.outOfOfficeDelegateId",
        "ApprovalRequest.allowEmailApproval",
        "ApprovalRequest.reopenedFrom",
        "ApprovalRequest.status",
        "ApprovalRequest.subjectContract",
        "ApprovalRequest.subjectType",
        "ApprovalRequest.subjectId",
        "ApprovalRequest.scopePath",
        "ApprovalRequest.summary"
       ],
       "operation": "listApprovalRequests",
       "provenance": "contract approvals.yaml GET /approval-requests"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval request",
       "bindsTo": "ApprovalRequest",
       "columns": [
        "ApprovalRequest.id",
        "ApprovalRequest.kind",
        "ApprovalRequest.rerouteOnNoApprover",
        "ApprovalRequest.outOfOfficeDelegateId",
        "ApprovalRequest.allowEmailApproval",
        "ApprovalRequest.reopenedFrom",
        "ApprovalRequest.status",
        "ApprovalRequest.subjectContract",
        "ApprovalRequest.subjectType",
        "ApprovalRequest.subjectId",
        "ApprovalRequest.scopePath",
        "ApprovalRequest.summary",
        "ApprovalRequest.amount",
        "ApprovalRequest.justification",
        "ApprovalRequest.requestedByPrincipalId",
        "ApprovalRequest.matrixVersion"
       ],
       "operation": "listApprovalRequests",
       "provenance": "contract approvals.yaml GET /approval-requests"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Decide approval request",
       "operation": "decideApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/decide"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate approval request",
       "operation": "escalateApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/escalate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval list.",
   "error": "Could not load. Names which read failed and leaves the approval untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Nothing matches the filter on assignedToMe, raisedByMe, status, kind, breachingWithinMinutes and the approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalRequests` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Requests awaiting a decision, or already decided",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve or reject",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalRequests"
    ]
   },
   {
    "operationId": "escalateApprovalRequest",
    "contract": "approvals",
    "purpose": "Move it up a level",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalRequests"
    ]
   },
   {
    "operationId": "getApprovalRequestScore",
    "contract": "ai",
    "purpose": "Risk band, priority and suggested escalation for the request, as context only (no approve/reject suggestion)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "requestId",
     "from": "deepLink"
    },
    {
     "name": "approvalRequestId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `requestId`.",
   "preloaded": [
    "ApprovalRequest.id",
    "ApprovalRequest.kind",
    "ApprovalRequest.rerouteOnNoApprover",
    "ApprovalRequest.outOfOfficeDelegateId",
    "ApprovalRequest.allowEmailApproval"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-084"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formDecideApprovalRequest",
    "component": "modal",
    "trigger": "Decide approval request",
    "body": "**Collects what `decideApprovalRequest` sends before it is called.** Required: `decision`. Optional: `comment`, `reason`, `stepUpToken`, `signature`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decide approval request",
     "operation": "decideApprovalRequest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "comment",
      "reason",
      "stepUpToken",
      "signature"
     ]
    },
    "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/decide"
   },
   {
    "id": "formEscalateApprovalRequest",
    "component": "modal",
    "trigger": "Escalate approval request",
    "body": "**Collects what `escalateApprovalRequest` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Escalate approval request",
     "operation": "escalateApprovalRequest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/escalate"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-085",
  "name": "Approval Request",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/approvals/approval-request",
   "component": "apps/venue-management-web/src/routes/approvals/ApprovalRequest.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-084",
    "BO-086",
    "BO-087"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-084",
     "trigger": "Approval Inbox",
     "carries": [
      "approvalRequestId",
      "requestId"
     ],
     "provenance": "derived — BO-084 declares entryState.params approvalRequestId, requestId and BO-085 holds approvalRequestId, requestId, so an edge into it carries them"
    },
    {
     "to": "BO-087",
     "trigger": "Approval Delegations",
     "provenance": "derived — BO-087 declares entryState.params delegationId and BO-085 holds none of them. The edge carries nothing: delegationId only pre-selects (deep link or optional), and BO-087 opens on its own"
    },
    {
     "to": "POS-005",
     "trigger": "The till applies it and completes the sale",
     "provenance": "flow F14 step 4→5",
     "operation": "decideApprovalRequest",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Cross-platform navigation removed 24 August**: POS-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`decideApprovalRequest` decides items that `listApprovalRequests` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "One request, its subject, and the decision.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "toggle",
       "label": "Assigned to me",
       "operation": "listApprovalRequests",
       "notes": "Sends `?assignedToMe=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "toggle",
       "label": "Raised by me",
       "operation": "listApprovalRequests",
       "notes": "Sends `?raisedByMe=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listApprovalRequests",
       "notes": "Sends `?status=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listApprovalRequests",
       "notes": "Sends `?kind=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "numberField",
       "label": "Breaching within minutes",
       "operation": "listApprovalRequests",
       "notes": "Sends `?breachingWithinMinutes=` to `listApprovalRequests`.",
       "provenance": "contract approvals.yaml GET /approval-requests"
      },
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "ApprovalRequest",
       "columns": [
        "ApprovalRequest.id",
        "ApprovalRequest.kind",
        "ApprovalRequest.rerouteOnNoApprover",
        "ApprovalRequest.outOfOfficeDelegateId",
        "ApprovalRequest.allowEmailApproval",
        "ApprovalRequest.reopenedFrom",
        "ApprovalRequest.status",
        "ApprovalRequest.subjectContract",
        "ApprovalRequest.subjectType",
        "ApprovalRequest.subjectId",
        "ApprovalRequest.scopePath",
        "ApprovalRequest.summary"
       ],
       "operation": "listApprovalRequests",
       "provenance": "contract approvals.yaml GET /approval-requests"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval request",
       "bindsTo": "ApprovalRequest",
       "columns": [
        "ApprovalRequest.id",
        "ApprovalRequest.kind",
        "ApprovalRequest.rerouteOnNoApprover",
        "ApprovalRequest.outOfOfficeDelegateId",
        "ApprovalRequest.allowEmailApproval",
        "ApprovalRequest.reopenedFrom",
        "ApprovalRequest.status",
        "ApprovalRequest.subjectContract",
        "ApprovalRequest.subjectType",
        "ApprovalRequest.subjectId",
        "ApprovalRequest.scopePath",
        "ApprovalRequest.summary",
        "ApprovalRequest.amount",
        "ApprovalRequest.justification",
        "ApprovalRequest.requestedByPrincipalId",
        "ApprovalRequest.matrixVersion"
       ],
       "operation": "listApprovalRequests",
       "provenance": "contract approvals.yaml GET /approval-requests"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Decide approval request",
       "operation": "decideApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/decide"
      },
      {
       "kind": "secondaryButton",
       "label": "Resubmit approval request",
       "operation": "resubmitApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/resubmit"
      },
      {
       "kind": "destructiveButton",
       "label": "Withdraw approval request",
       "operation": "withdrawApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/withdraw"
      },
      {
       "kind": "secondaryButton",
       "label": "Evaluate approval requirement",
       "operation": "evaluateApprovalRequirement",
       "provenance": "contract approvals.yaml POST /approval-requests/evaluate"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmWithdrawApprovalRequest",
    "component": "confirmDialog",
    "trigger": "Withdraw approval request",
    "body": "**Names what `withdrawApprovalRequest` changes and what it leaves alone**, in the consequence rather than the verb. A approval request this affects should be identified in the dialog, not just counted. **Collects what `withdrawApprovalRequest` sends before it is called.** Nothing in the body is required. Optional: `reason`.",
    "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/withdraw"
   },
   {
    "id": "formDecideApprovalRequest",
    "component": "modal",
    "trigger": "Decide approval request",
    "body": "**Collects what `decideApprovalRequest` sends before it is called.** Required: `decision`. Optional: `comment`, `reason`, `stepUpToken`, `signature`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decide approval request",
     "operation": "decideApprovalRequest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "comment",
      "reason",
      "stepUpToken",
      "signature"
     ]
    },
    "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/decide"
   },
   {
    "id": "formResubmitApprovalRequest",
    "component": "modal",
    "trigger": "Resubmit approval request",
    "body": "**Collects what `resubmitApprovalRequest` sends before it is called.** Required: `changes`. Optional: `amount`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resubmit approval request",
     "operation": "resubmitApprovalRequest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "changes",
      "amount"
     ]
    },
    "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/resubmit"
   },
   {
    "id": "formEvaluateApprovalRequirement",
    "component": "modal",
    "trigger": "Evaluate approval requirement",
    "body": "**Collects what `evaluateApprovalRequirement` sends before it is called.** Required: `kind`, `scopePath`. Optional: `amount`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Evaluate approval requirement",
     "operation": "evaluateApprovalRequirement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "scopePath",
      "amount",
      "attributes"
     ]
    },
    "provenance": "contract approvals.yaml POST /approval-requests/evaluate"
   }
  ],
  "states": {
   "loading": "The approval request list.",
   "error": "Could not load. Names which read failed and leaves the approval request untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Nothing matches the filter on assignedToMe, raisedByMe, status, kind, breachingWithinMinutes and the approval request are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalRequests` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Requests awaiting a decision, or already decided",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve or reject",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalRequests"
    ]
   },
   {
    "operationId": "resubmitApprovalRequest",
    "contract": "approvals",
    "purpose": "Amend a rejected request and try again",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalRequests"
    ]
   },
   {
    "operationId": "withdrawApprovalRequest",
    "contract": "approvals",
    "purpose": "The requester takes it back",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalRequests"
    ]
   },
   {
    "operationId": "evaluateApprovalRequirement",
    "contract": "approvals",
    "purpose": "Does this need approval, and from whom",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalRequests"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "requestId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `requestId`.",
   "preloaded": [
    "ApprovalRequest.id",
    "ApprovalRequest.kind",
    "ApprovalRequest.rerouteOnNoApprover",
    "ApprovalRequest.outOfOfficeDelegateId",
    "ApprovalRequest.allowEmailApproval"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-085"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-086",
  "name": "Approval Matrix",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/approvals/approval-matrix",
   "component": "apps/venue-management-web/src/routes/approvals/ApprovalMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-084",
    "BO-085",
    "BO-087"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-084",
     "trigger": "Approval Inbox",
     "provenance": "derived — BO-084 declares entryState.params approvalRequestId, requestId and BO-086 holds none of them. The edge carries nothing: requestId only pre-selects (deep link or optional); BO-084 finds approvalRequestId (listApprovalRequests) itself, and BO-084 opens on its own"
    },
    {
     "to": "BO-085",
     "trigger": "Approval Request",
     "provenance": "derived — BO-085 declares entryState.params requestId and BO-086 holds none of them. The edge carries nothing: requestId only pre-selects (deep link or optional), and BO-085 opens on its own"
    },
    {
     "to": "BO-087",
     "trigger": "Approval Delegations",
     "provenance": "derived — BO-087 declares entryState.params delegationId and BO-086 holds none of them. The edge carries nothing: delegationId only pre-selects (deep link or optional), and BO-087 opens on its own"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listApprovalMatrices` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "What needs approval here, and who grants it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listApprovalMatrices",
       "notes": "Sends `?kind=` to `listApprovalMatrices`.",
       "provenance": "contract approvals.yaml GET /approval-matrices"
      },
      {
       "kind": "toggle",
       "label": "Effective",
       "operation": "listApprovalMatrices",
       "notes": "Sends `?effective=` to `listApprovalMatrices`.",
       "provenance": "contract approvals.yaml GET /approval-matrices"
      },
      {
       "kind": "dataTable",
       "label": "Every approval matrix",
       "bindsTo": "ApprovalMatrix",
       "columns": [
        "ApprovalMatrix.id",
        "ApprovalMatrix.kind",
        "ApprovalMatrix.scopeLevel",
        "ApprovalMatrix.scopePath",
        "ApprovalMatrix.rules",
        "ApprovalMatrix.isActive"
       ],
       "operation": "listApprovalMatrices",
       "provenance": "contract approvals.yaml GET /approval-matrices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval matrix",
       "bindsTo": "ApprovalMatrix",
       "columns": [
        "ApprovalMatrix.id",
        "ApprovalMatrix.kind",
        "ApprovalMatrix.scopeLevel",
        "ApprovalMatrix.scopePath",
        "ApprovalMatrix.rules",
        "ApprovalMatrix.isActive"
       ],
       "operation": "listApprovalMatrices",
       "provenance": "contract approvals.yaml GET /approval-matrices"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save approval matrix",
       "operation": "setApprovalMatrix",
       "provenance": "contract approvals.yaml PUT /approval-matrices"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval list.",
   "error": "Could not load. Names which read failed and leaves the approval untouched.",
   "emptyFirstRun": "No approval yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on kind, effective and the approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `APPROVAL_CONFIGURE`, which `listApprovalMatrices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalMatrices",
    "contract": "approvals",
    "purpose": "What requires approval here",
    "trigger": "onLoad"
   },
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Configure what requires approval",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalMatrices"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ApprovalMatrix.id",
    "ApprovalMatrix.kind",
    "ApprovalMatrix.scopeLevel",
    "ApprovalMatrix.scopePath",
    "ApprovalMatrix.rules"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-086"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetApprovalMatrix",
    "component": "modal",
    "trigger": "Save approval matrix",
    "body": "**Collects what `setApprovalMatrix` sends before it is called.** Required: `kind`, `scopeLevel`, `rules`. Optional: `id`, `scopePath`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ApprovalMatrix",
    "confirm": {
     "label": "Save approval matrix",
     "operation": "setApprovalMatrix"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "scopeLevel",
      "rules",
      "id",
      "scopePath",
      "isActive"
     ]
    },
    "provenance": "contract approvals.yaml PUT /approval-matrices"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-087",
  "name": "Approval Delegations",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/approvals/approval-delegations",
   "component": "apps/venue-management-web/src/routes/approvals/ApprovalDelegations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-084",
    "BO-085",
    "BO-086"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-084",
     "trigger": "Approval Inbox",
     "provenance": "derived — BO-084 declares entryState.params approvalRequestId, requestId and BO-087 holds none of them. The edge carries nothing: requestId only pre-selects (deep link or optional); BO-084 finds approvalRequestId (listApprovalRequests) itself, and BO-084 opens on its own"
    },
    {
     "to": "BO-085",
     "trigger": "Approval Request",
     "provenance": "derived — BO-085 declares entryState.params requestId and BO-087 holds none of them. The edge carries nothing: requestId only pre-selects (deep link or optional), and BO-085 opens on its own"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listApprovalDelegations` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Who is standing in for whom, and until when.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every approval delegation",
       "bindsTo": "ApprovalDelegation",
       "columns": [
        "ApprovalDelegation.id",
        "ApprovalDelegation.delegatorPrincipalId",
        "ApprovalDelegation.delegatePrincipalId",
        "ApprovalDelegation.kinds",
        "ApprovalDelegation.maxAmount",
        "ApprovalDelegation.from",
        "ApprovalDelegation.to",
        "ApprovalDelegation.reason",
        "ApprovalDelegation.isActive",
        "ApprovalDelegation.scopePath"
       ],
       "operation": "listApprovalDelegations",
       "provenance": "contract approvals.yaml GET /delegations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval delegation",
       "bindsTo": "ApprovalDelegation",
       "columns": [
        "ApprovalDelegation.id",
        "ApprovalDelegation.delegatorPrincipalId",
        "ApprovalDelegation.delegatePrincipalId",
        "ApprovalDelegation.kinds",
        "ApprovalDelegation.maxAmount",
        "ApprovalDelegation.from",
        "ApprovalDelegation.to",
        "ApprovalDelegation.reason",
        "ApprovalDelegation.isActive",
        "ApprovalDelegation.scopePath"
       ],
       "operation": "listApprovalDelegations",
       "provenance": "contract approvals.yaml GET /delegations"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create approval delegation",
       "operation": "createApprovalDelegation",
       "provenance": "contract approvals.yaml POST /delegations"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke approval delegation",
       "operation": "revokeApprovalDelegation",
       "provenance": "contract approvals.yaml DELETE /delegations/{delegationId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRevokeApprovalDelegation",
    "component": "confirmDialog",
    "trigger": "Revoke approval delegation",
    "body": "**Names what `revokeApprovalDelegation` changes and what it leaves alone**, in the consequence rather than the verb. A approval delegations this affects should be identified in the dialog, not just counted.",
    "provenance": "contract approvals.yaml DELETE /delegations/{delegationId}"
   },
   {
    "id": "formCreateApprovalDelegation",
    "component": "modal",
    "trigger": "Create approval delegation",
    "body": "**Collects what `createApprovalDelegation` sends before it is called.** Required: `delegatorPrincipalId`, `delegatePrincipalId`, `from`, `to`. Optional: `id`, `kinds`, `maxAmount`, `reason`, `isActive`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ApprovalDelegation",
    "confirm": {
     "label": "Create approval delegation",
     "operation": "createApprovalDelegation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "delegatorPrincipalId",
      "delegatePrincipalId",
      "from",
      "to",
      "id",
      "kinds",
      "maxAmount",
      "reason",
      "isActive",
      "scopePath"
     ]
    },
    "provenance": "contract approvals.yaml POST /delegations"
   }
  ],
  "states": {
   "loading": "The approval delegations list.",
   "error": "Could not load. Names which read failed and leaves the approval delegations untouched.",
   "emptyFirstRun": "No approval delegations yet. Offers Create approval delegation (`createApprovalDelegation`).",
   "emptyNoResults": "Never shown: `listApprovalDelegations` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `APPROVAL_VIEW`, which `listApprovalDelegations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalDelegations",
    "contract": "approvals",
    "purpose": "Who is standing in for whom",
    "trigger": "onLoad"
   },
   {
    "operationId": "createApprovalDelegation",
    "contract": "approvals",
    "purpose": "Delegate approval authority",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalDelegations"
    ]
   },
   {
    "operationId": "revokeApprovalDelegation",
    "contract": "approvals",
    "purpose": "End a delegation early",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalDelegations"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "delegationId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `delegationId`.",
   "preloaded": [
    "ApprovalDelegation.id",
    "ApprovalDelegation.delegatorPrincipalId",
    "ApprovalDelegation.delegatePrincipalId",
    "ApprovalDelegation.kinds",
    "ApprovalDelegation.maxAmount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-087"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
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
 "acknowledgeAnnouncement": {
  "method": "POST",
  "path": "/announcements/{announcementId}/acknowledge",
  "contract": "workforce",
  "summary": "Confirm you have read it",
  "permission": "WORKFORCE_VIEW",
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
  "requestBody": null,
  "responds": null
 },
 "amendAttendance": {
  "method": "POST",
  "path": "/attendance/{recordId}/amend",
  "contract": "workforce",
  "summary": "A supervisor corrects a record",
  "permission": "WORKFORCE_MANAGE",
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
  "responds": "AttendanceRecord"
 },
 "createApprovalDelegation": {
  "method": "POST",
  "path": "/delegations",
  "contract": "approvals",
  "summary": "Delegate approval authority",
  "permission": "APPROVAL_DECIDE",
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
  "requestBody": "ApprovalDelegation",
  "responds": "ApprovalDelegation"
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
 "createRole": {
  "method": "POST",
  "path": "/roles",
  "contract": "identity",
  "summary": "Create a role",
  "permission": "ROLE_MANAGE",
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
  "responds": "Role"
 },
 "createRotaAssignment": {
  "method": "POST",
  "path": "/rota-assignments",
  "contract": "workforce",
  "summary": "Put someone on the rota",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "RotaAssignment",
  "responds": "RotaAssignment"
 },
 "decideApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/decide",
  "contract": "approvals",
  "summary": "Approve, reject, return or ask for information",
  "permission": "APPROVAL_DECIDE",
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
  "responds": "ApprovalRequest"
 },
 "escalateApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/escalate",
  "contract": "approvals",
  "summary": "Move it up a level",
  "permission": "APPROVAL_REQUEST",
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
  "responds": "ApprovalRequest"
 },
 "evaluateApprovalRequirement": {
  "method": "POST",
  "path": "/approval-requests/evaluate",
  "contract": "approvals",
  "summary": "Does this need approval, and from whom",
  "permission": "APPROVAL_VIEW",
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
  "responds": "ApprovalRequirement"
 },
 "getAnnouncementReach": {
  "method": "GET",
  "path": "/announcements/{announcementId}/reach",
  "contract": "workforce",
  "summary": "Who has acknowledged, and who has not",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AnnouncementReach"
 },
 "getApprovalRequestScore": {
  "method": "GET",
  "path": "/approval-requests/{approvalRequestId}/score",
  "contract": "ai",
  "summary": "The latest context score of an approval request",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiApprovalRequestScore"
 },
 "getPrincipal": {
  "method": "GET",
  "path": "/principals/{principalId}",
  "contract": "identity",
  "summary": "Read a principal",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Principal"
 },
 "listAccessReviewCampaigns": {
  "method": "GET",
  "path": "/access-review-campaigns",
  "contract": "identity",
  "summary": "Access review campaigns, open first",
  "permission": "PERMISSION_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
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
 "listAccessReviewItems": {
  "method": "GET",
  "path": "/access-review-campaigns/{campaignId}/items",
  "contract": "identity",
  "summary": "The grants a campaign asks somebody to certify or revoke",
  "permission": "PERMISSION_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "findingKind",
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
 "listAnnouncements": {
  "method": "GET",
  "path": "/announcements",
  "contract": "workforce",
  "summary": "What staff have been told",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "unacknowledgedOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Announcement"
 },
 "listApprovalDelegations": {
  "method": "GET",
  "path": "/delegations",
  "contract": "approvals",
  "summary": "Who is standing in for whom",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ApprovalDelegation"
 },
 "listApprovalMatrices": {
  "method": "GET",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "What requires approval here",
  "permission": "APPROVAL_CONFIGURE",
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
    "name": "effective",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApprovalMatrix"
 },
 "listApprovalRequests": {
  "method": "GET",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Requests awaiting a decision, or already decided",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "raisedByMe",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "breachingWithinMinutes",
    "in": "query",
    "required": null
   },
   {
    "name": "sort",
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
 "listAttendance": {
  "method": "GET",
  "path": "/attendance",
  "contract": "workforce",
  "summary": "Who was here",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "date",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "exceptionsOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AttendanceRecord"
 },
 "listJobTitles": {
  "method": "GET",
  "path": "/job-titles",
  "contract": "workforce",
  "summary": "The job titles a posting can name",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WorkforceJobTitle"
 },
 "listPermissionFindings": {
  "method": "GET",
  "path": "/permission-findings",
  "contract": "identity",
  "summary": "Excessive, missing and conflicting permissions, per principal or role",
  "permission": "PERMISSION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "roleId",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "lookbackDays",
    "in": "query",
    "required": null
   },
   {
    "name": "deniedThreshold",
    "in": "query",
    "required": null
   },
   {
    "name": "draftPolicyId",
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
 "listPrincipals": {
  "method": "GET",
  "path": "/principals",
  "contract": "identity",
  "summary": "List principals",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "isActive",
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
 "listRoles": {
  "method": "GET",
  "path": "/roles",
  "contract": "identity",
  "summary": "List roles",
  "permission": "ROLE_MANAGE",
  "offlineCapable": true,
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
 "listRotaAssignments": {
  "method": "GET",
  "path": "/rota-assignments",
  "contract": "workforce",
  "summary": "The rota",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
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
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "departmentId",
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
 "listWorkAssignments": {
  "method": "GET",
  "path": "/work-assignments",
  "contract": "workforce",
  "summary": "Where each person is posted, and from when",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "employeeId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "activeOn",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkforceWorkAssignment"
 },
 "publishAnnouncement": {
  "method": "POST",
  "path": "/announcements",
  "contract": "workforce",
  "summary": "Tell staff something",
  "permission": "ANNOUNCEMENT_PUBLISH",
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
  "requestBody": "Announcement",
  "responds": "Announcement"
 },
 "recordAttendance": {
  "method": "POST",
  "path": "/attendance/clock",
  "contract": "workforce",
  "summary": "Clock in, clock out, or take a break",
  "permission": "ATTENDANCE_RECORD",
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
  "requestBody": null,
  "responds": "AttendanceRecord"
 },
 "requestShiftSwap": {
  "method": "POST",
  "path": "/rota-assignments/{assignmentId}/swap",
  "contract": "workforce",
  "summary": "Ask someone to take your shift",
  "permission": "WORKFORCE_VIEW",
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
 "resetPrincipalCredential": {
  "method": "POST",
  "path": "/principals/{principalId}/credential-reset",
  "contract": "identity",
  "summary": "Reset a member of staff's password or PIN",
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
  "requestBody": "ResetCredentialRequest",
  "responds": null
 },
 "resubmitApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/resubmit",
  "contract": "approvals",
  "summary": "Amend a rejected request and try again",
  "permission": "APPROVAL_REQUEST",
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
  "responds": "ApprovalRequest"
 },
 "revokeApprovalDelegation": {
  "method": "DELETE",
  "path": "/delegations/{delegationId}",
  "contract": "approvals",
  "summary": "End a delegation early",
  "permission": "APPROVAL_DECIDE",
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
 "setApprovalMatrix": {
  "method": "PUT",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "Configure what requires approval",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "ApprovalMatrix",
  "responds": "ApprovalMatrix"
 },
 "setCapabilityTemplate": {
  "method": "PUT",
  "path": "/capability-templates",
  "contract": "identity",
  "summary": "Save a tick-set under a name",
  "permission": "ROLE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CapabilityTemplate",
  "responds": "CapabilityTemplate"
 },
 "setJobTitle": {
  "method": "PUT",
  "path": "/job-titles",
  "contract": "workforce",
  "summary": "Define a job title",
  "permission": "WORKFORCE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "WorkforceJobTitle",
  "responds": "WorkforceJobTitle"
 },
 "setWorkAssignment": {
  "method": "PUT",
  "path": "/work-assignments",
  "contract": "workforce",
  "summary": "Post a person to a job title at a venue",
  "permission": "WORKFORCE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "WorkforceWorkAssignment",
  "responds": "WorkforceWorkAssignment"
 },
 "suggestRoleAssignment": {
  "method": "GET",
  "path": "/role-suggestions",
  "contract": "identity",
  "summary": "Which roles a person should probably hold, from peers with the same job and posting",
  "permission": "PERMISSION_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "jobTitleId",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "minPeerShare",
    "in": "query",
    "required": null
   },
   {
    "name": "minPeers",
    "in": "query",
    "required": null
   },
   {
    "name": "lookbackDays",
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
 "updatePrincipal": {
  "method": "PATCH",
  "path": "/principals/{principalId}",
  "contract": "identity",
  "summary": "Update or deactivate a principal",
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
  "requestBody": null,
  "responds": "Principal"
 },
 "updateRotaAssignment": {
  "method": "PATCH",
  "path": "/rota-assignments/{assignmentId}",
  "contract": "workforce",
  "summary": "Move or cancel an assignment",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "RotaAssignment",
  "responds": "RotaAssignment"
 },
 "withdrawApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/withdraw",
  "contract": "approvals",
  "summary": "The requester takes it back",
  "permission": "APPROVAL_REQUEST",
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
  "responds": "ApprovalRequest"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiApprovalRequestScore": {
  "type": "object",
  "x-ticvai-persistence": "ai.approval_request_score",
  "description": "**Context for an approval reviewer** (11.1.73..75): risk, priority and a suggested escalation for one pending request, the latest per request. **There is no approve or reject field, by design** (minutes of 8 September: AI in approvals never recommends or influences approve or reject).",
  "required": [
   "approvalRequestId",
   "riskScore",
   "riskBand",
   "priorityScore",
   "escalationSuggestion"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "approvals.request"
   },
   "trigger": {
    "type": "string",
    "enum": [
     "submitted",
     "resubmitted",
     "slaTick",
     "escalated"
    ]
   },
   "riskScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100
   },
   "riskBand": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Design 5.6: a risk score and band, never a probability."
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "description": "For ordering work in an inbox; higher first."
   },
   "escalationSuggestion": {
    "type": "object",
    "required": [
     "action"
    ],
    "properties": {
     "action": {
      "type": "string",
      "enum": [
       "escalate",
       "addBackupApprover",
       "none"
      ]
     },
     "reason": {
      "type": "string",
      "nullable": true
     }
    },
    "description": "A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy."
   },
   "signals": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "description": "e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate`, `approverUnavailable`."
      },
      "contribution": {
       "type": "number"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scoredAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "Announcement": {
  "type": "object",
  "x-ticvai-persistence": "workforce.announcement",
  "required": [
   "title",
   "body",
   "kind",
   "publishedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "title": {
    "type": "string",
    "maxLength": 140
   },
   "body": {
    "type": "string",
    "maxLength": 4000
   },
   "kind": {
    "$ref": "#/components/schemas/AnnouncementKind"
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "departmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresAcknowledgement": {
    "type": "boolean"
   },
   "deliveryChannels": {
    "type": "array",
    "description": "How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n",
    "items": {
     "type": "string",
     "enum": [
      "inApp",
      "push"
     ]
    },
    "default": [
     "inApp",
     "push"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "locale": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "AnnouncementKind": {
  "type": "string",
  "description": "`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n",
  "enum": [
   "operational",
   "safety",
   "emergency",
   "hr",
   "celebration"
  ]
 },
 "AnnouncementReach": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from workforce.announcement_receipt",
  "properties": {
   "announcementId": {
    "type": "string",
    "format": "uuid"
   },
   "targeted": {
    "type": "integer"
   },
   "delivered": {
    "type": "integer"
   },
   "acknowledged": {
    "type": "integer"
   },
   "outstanding": {
    "type": "array",
    "description": "**The list that matters.** For an operational notice it measures whether anyone read it; during an emergency it is the roll call.\n",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "onShift": {
       "type": "boolean"
      }
     }
    }
   }
  }
 },
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalDelegation": {
  "type": "object",
  "x-ticvai-persistence": "approvals.delegation",
  "required": [
   "delegatorPrincipalId",
   "delegatePrincipalId",
   "from",
   "to"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "delegatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"
   },
   "delegatePrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "A principal id, resolved to a name the same way as `delegatorPrincipalId`."
   },
   "kinds": {
    "type": "array",
    "description": "Absent means everything the delegator may approve.",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "maxAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "A delegate may be given less authority than the delegator, never more."
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time",
    "description": "**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"
   },
   "reason": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration",
   "productChange",
   "pricingChange"
  ]
 },
 "ApprovalMatrix": {
  "type": "object",
  "x-ticvai-persistence": "approvals.matrix",
  "required": [
   "kind",
   "scopeLevel",
   "rules"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"
   },
   "rules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalRule"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.",
    "properties": {
     "riskScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "riskBand": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "priorityScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "escalationSuggestion": {
      "type": "object",
      "description": "A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.",
      "properties": {
       "action": {
        "type": "string",
        "enum": [
         "escalate",
         "addBackupApprover",
         "none"
        ]
       },
       "reason": {
        "type": "string",
        "nullable": true
       }
      }
     },
     "signals": {
      "type": "array",
      "maxItems": 10,
      "description": "The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.",
      "items": {
       "type": "object",
       "properties": {
        "code": {
         "type": "string"
        },
        "contribution": {
         "type": "number"
        },
        "detail": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "scoreId": {
      "type": "string",
      "format": "uuid",
      "description": "The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."
     },
     "decisionRecordId": {
      "type": "string",
      "description": "The ai decision record, for the audit of what the AI said and why."
     },
     "assessedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "ApprovalRequirement": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "description": "The answer to \"does this need approval\", returned before the action.",
  "required": [
   "isRequired"
  ],
  "properties": {
   "isRequired": {
    "type": "boolean"
   },
   "matchedRule": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ApprovalRule"
     }
    ],
    "nullable": true
   },
   "matrixVersion": {
    "type": "integer",
    "nullable": true
   },
   "approvers": {
    "type": "array",
    "description": "Resolved, with delegations applied. **Named so the caller can say \"this needs Sara\"** rather than \"this needs approval\".\n",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "level": {
       "type": "integer"
      },
      "isDelegate": {
       "type": "boolean"
      },
      "delegatedFrom": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true
   },
   "noApproverAvailable": {
    "type": "boolean",
    "description": "**The case that must not fail silently.** A rule requiring a role nobody at this venue holds means the action is blocked forever, and the caller needs to know that now rather than after raising a request nobody can decide.\n"
   }
  }
 },
 "ApprovalRule": {
  "type": "object",
  "x-ticvai-persistence": "approvals.rule",
  "required": [
   "order",
   "approverRoleIds",
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "order": {
    "type": "integer",
    "description": "**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"
   },
   "minAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "riskScoreAbove": {
    "type": "number",
    "nullable": true,
    "description": "11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"
   },
   "condition": {
    "type": "string",
    "nullable": true,
    "description": "11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"
   },
   "approverRoleIds": {
    "type": "array",
    "minItems": 1,
    "description": "Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "approverScopeLevel": {
    "type": "string",
    "enum": [
     "venue",
     "department",
     "region",
     "tenant"
    ],
    "description": "11.1.39. Which organisational level the approver must sit at."
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "levels": {
    "type": "integer",
    "default": 1,
    "description": "11.1.3. Multi-level chains ask each level in turn."
   },
   "requiresMfa": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.14. Null means no SLA, which is different from a long one."
   },
   "escalateAfterMinutes": {
    "type": "integer",
    "nullable": true
   },
   "escalateToRoleIds": {
    "type": "array",
    "description": "Role ids from `identity.listRoles`, as `approverRoleIds`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAfterMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.53. An unanswered request eventually stops waiting."
   },
   "externalProviderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "returned",
   "informationRequested",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
 "AttendanceAmendment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.attendance_amendment",
  "description": "One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n",
  "required": [
   "id",
   "attendanceRecordId",
   "amendedByPrincipalId",
   "amendedAt",
   "occurredAtBefore",
   "occurredAtAfter",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "attendanceRecordId": {
    "type": "string",
    "format": "uuid"
   },
   "amendedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "amendedAt": {
    "type": "string",
    "format": "date-time"
   },
   "occurredAtBefore": {
    "type": "string",
    "format": "date-time",
    "description": "The record's time before this correction."
   },
   "occurredAtAfter": {
    "type": "string",
    "format": "date-time",
    "description": "The time this correction set (`correctedAt` on the request)."
   },
   "reason": {
    "type": "string",
    "maxLength": 300
   }
  }
 },
 "AttendanceRecord": {
  "type": "object",
  "x-ticvai-persistence": "workforce.attendance",
  "required": [
   "id",
   "principalId",
   "kind",
   "occurredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "assignmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "clockIn",
     "clockOut",
     "breakStart",
     "breakEnd"
    ]
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time — when it happened."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "latitude": {
    "type": "number",
    "nullable": true
   },
   "longitude": {
    "type": "number",
    "nullable": true
   },
   "isAmended": {
    "type": "boolean",
    "readOnly": true
   },
   "amendedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Who made the latest amendment. The full history is `amendments` (audit R129 (7))."
   },
   "amendmentReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The latest amendment's reason. The full history is `amendments` (audit R129 (7))."
   },
   "originalOccurredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"
   },
   "amendments": {
    "type": "array",
    "readOnly": true,
    "description": "**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n",
    "items": {
     "$ref": "#/components/schemas/AttendanceAmendment"
    }
   },
   "exception": {
    "type": "string",
    "nullable": true,
    "enum": [
     "late",
     "earlyLeave",
     "missingClockOut",
     "noShow",
     "outOfGeofence",
     "unscheduled"
    ],
    "description": "Computed against the rota. Null where the record matches what was expected."
   }
  }
 },
 "CapabilityTemplate": {
  "x-ticvai-persistence": "identity.capability_template",
  "type": "object",
  "description": "3.3.23, BL-110. **A named tick-set — a role, with nothing depending on the name.**\n",
  "required": [
   "code",
   "name",
   "capabilities"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
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
    "nullable": true
   },
   "capabilities": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written by the server at `tenant` scope; ignored if a request sends it."
   }
  }
 },
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
 "IdentityAccessReviewCampaign": {
  "type": "object",
  "x-ticvai-persistence": "identity.access_review_campaign",
  "description": "**A periodic access review** (7.1.35, 7.1.56; decided 29 September, build pass, group G2): which grants, reviewed by whom, by when. Its items are `identity.access_review_item`. Lifecycle in `states/access-review-campaign.yaml`.",
  "required": [
   "name",
   "scopePath",
   "reviewerMode",
   "dueAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005), and what is reviewed: every grant at or below it. Inside the caller's own scope. Operations write it at `venue` scope."
   },
   "roleIds": {
    "type": "array",
    "nullable": true,
    "description": "Only grants of these roles; null reviews every grant in scope.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "reviewerMode": {
    "type": "string",
    "enum": [
     "lineManager",
     "named"
    ],
    "description": "`lineManager`: each item goes to the holder's manager from their primary work assignment, falling back to the named reviewers where none is found. `named`: the named reviewers share the items."
   },
   "reviewerPrincipalIds": {
    "type": "array",
    "nullable": true,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "recurrence": {
    "type": "string",
    "enum": [
     "none",
     "quarterly",
     "semiAnnual",
     "annual"
    ],
    "default": "none"
   },
   "prefillFromFindings": {
    "type": "boolean",
    "default": true
   },
   "lookbackDays": {
    "type": "integer",
    "minimum": 7,
    "maximum": 365,
    "default": 90
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "completed",
     "expired"
    ],
    "readOnly": true
   },
   "itemCount": {
    "type": "integer",
    "readOnly": true
   },
   "decidedCount": {
    "type": "integer",
    "readOnly": true,
    "description": "Kept by `decideAccessReviewItem` in the same write, so the campaign list needs no count query."
   },
   "revokedCount": {
    "type": "integer",
    "readOnly": true
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "IdentityAccessReviewItem": {
  "type": "object",
  "x-ticvai-persistence": "identity.access_review_item",
  "description": "One grant under review in a campaign, with the finding that pre-filled it and the reviewer's decision (decided 29 September, build pass, group G2). Lifecycle in `states/access-review-item.yaml`.",
  "required": [
   "campaignId",
   "delegatedAccessId",
   "principalId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "identity.access_review_campaign"
   },
   "delegatedAccessId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "identity.delegated_access",
    "description": "The grant under review."
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "identity.principal"
   },
   "roleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.role"
   },
   "scopePath": {
    "type": "string",
    "description": "The grant's scope. **The partition key** (ADR-0005)."
   },
   "reviewerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal"
   },
   "findingKind": {
    "type": "string",
    "enum": [
     "none",
     "excessive",
     "conflicting"
    ],
    "default": "none"
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recommendation": {
    "type": "string",
    "enum": [
     "certify",
     "revoke",
     "review"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "certified",
     "revoked",
     "notReviewed"
    ],
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "reason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   }
  }
 },
 "IdentityPermissionFinding": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from grants (roles, delegations, policies) against identity.access_decision and identity.segregation_rule",
  "description": "One excessive, missing or conflicting permission (7.1.47; decided 29 September, build pass).",
  "required": [
   "kind",
   "principalId",
   "permission"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "excessive",
     "missing",
     "conflicting"
    ]
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "roleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The role that grants it, for excessive and conflicting; the role whose peers hold it, for missing."
   },
   "permission": {
    "type": "string"
   },
   "conflictingPermission": {
    "type": "string",
    "nullable": true,
    "description": "The other half of the pair, for conflicting."
   },
   "segregationRuleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "grantedBy": {
    "type": "string",
    "enum": [
     "role",
     "delegation",
     "policy"
    ],
    "nullable": true
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The last permit that used it; null when never used in the window."
   },
   "deniedCount": {
    "type": "integer",
    "nullable": true,
    "description": "For missing, the denials in the window."
   },
   "peersHoldingPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "For missing, the share of the role's holders at the same scope who hold the permission."
   },
   "recommendation": {
    "type": "string",
    "enum": [
     "revoke",
     "grant",
     "review"
    ]
   },
   "asDraft": {
    "type": "boolean",
    "default": false,
    "description": "True when the finding exists only because of the `draftPolicyId` evaluated."
   }
  }
 },
 "IdentityRoleSuggestion": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from workforce.work_assignment peers, identity.delegated_access and identity.access_decision",
  "description": "One role suggested for a person because peers with the same job title and posting hold it (7.1.35, 7.1.56; decided 29 September, build pass, group G2).",
  "required": [
   "roleId",
   "scopePath",
   "peersHoldingPercent",
   "recommendation"
  ],
  "properties": {
   "roleId": {
    "type": "string",
    "format": "uuid"
   },
   "roleCode": {
    "type": "string"
   },
   "roleName": {
    "type": "string"
   },
   "scopePath": {
    "type": "string",
    "description": "Where the peers hold it, and so where it would be granted."
   },
   "peerCount": {
    "type": "integer",
    "description": "Principals with the same job title at the same posting."
   },
   "peersHolding": {
    "type": "integer"
   },
   "peersHoldingPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "peersUsingPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Of the peers holding it, the share with a permit using one of its permissions in `lookbackDays`."
   },
   "alreadyHeld": {
    "type": "boolean"
   },
   "recommendation": {
    "type": "string",
    "enum": [
     "grant",
     "review",
     "held"
    ],
    "description": "`grant` where most peers hold and use it; `review` where they hold it and do not use it; `held` where the person has it already."
   },
   "evidence": {
    "type": "object",
    "description": "What the suggestion rests on, so the person granting can check it.",
    "properties": {
     "jobTitleId": {
      "type": "string",
      "format": "uuid"
     },
     "postingScopePath": {
      "type": "string"
     },
     "samplePeerPrincipalIds": {
      "type": "array",
      "maxItems": 5,
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "requiresApproval": {
      "type": "boolean",
      "description": "Whether granting this role raises an approval (a role carrying permission or price authority, ApprovalKind level 2)."
     }
    }
   }
  }
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
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
 "ResetCredentialRequest": {
  "type": "object",
  "description": "Request only; see `ChangeCredentialRequest`.",
  "required": [
   "method",
   "temporaryCredential",
   "reason"
  ],
  "properties": {
   "method": {
    "type": "string",
    "enum": [
     "password",
     "pin"
    ]
   },
   "temporaryCredential": {
    "type": "string",
    "maxLength": 512,
    "writeOnly": true,
    "description": "Issued to the principal out of band. Must be changed at next sign-in."
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   }
  }
 },
 "Role": {
  "x-ticvai-persistence": "identity.role",
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
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "permissions": {
    "type": "array",
    "description": "**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
    }
   },
   "inheritsFromRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"
   },
   "isSystem": {
    "type": "boolean",
    "default": false,
    "description": "**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n"
   },
   "principalCount": {
    "type": "integer"
   },
   "grantCount": {
    "type": "integer"
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
 "RotaAssignment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.rota_assignment",
  "required": [
   "principalId",
   "venueId",
   "startsAt",
   "endsAt",
   "position"
  ],
  "properties": {
   "overtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"
   },
   "restPeriodBefore": {
    "type": "integer",
    "nullable": true,
    "description": "Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"
   },
   "breachesWorkingHourLimit": {
    "type": "boolean",
    "default": false,
    "readOnly": true,
    "description": "**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"
   },
   "labourCost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "position": {
    "type": "string",
    "description": "What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"
   },
   "requiredRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "$ref": "#/components/schemas/RotaStatus"
   },
   "breakMinutes": {
    "type": "integer",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "RotaStatus": {
  "type": "string",
  "enum": [
   "planned",
   "published",
   "confirmed",
   "swapPending",
   "cancelled",
   "completed",
   "noShow"
  ]
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "WorkforceJobTitle": {
  "type": "object",
  "x-ticvai-persistence": "workforce.job_title",
  "description": "**Taken from the backend workbook, 20 September.** Stores job/designation definitions such as Cashier, Manager, Chef or Technician.",
  "required": [
   "tenantId",
   "code",
   "name",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 50
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "description": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkforceWorkAssignment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.work_assignment",
  "description": "**Taken from the backend workbook, 20 September.** Assigns an employee to a job and operational location/scope for an effective period.",
  "required": [
   "employeeId",
   "jobTitleId",
   "effectiveFrom",
   "isPrimary",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "employeeId": {
    "type": "string",
    "format": "uuid"
   },
   "jobTitleId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "isPrimary": {
    "type": "boolean"
   },
   "status": {
    "type": "string",
    "maxLength": 30
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 }
}
```
