# P08-people-access-rights-01 — P08 · People & Access Rights (1 of 2)

**10 screens · 28 operations · 20 schemas · 10 permissions**

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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `ANNOUNCEMENT_PUBLISH, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW, ATTENDANCE_RECORD, ROLE_MANAGE, USER_MANAGE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **5 of these operations work offline**: acknowledgeAnnouncement, listAnnouncements, listRoles, listRotaAssignments, recordAttendance
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-053` | Staff Directory | listDetail | 4 | 0 | — |
| `BO-054` | Role Assignment | listDetail | 2 | 0 | — |
| `BO-055` | Rota & Scheduling | listDetail | 4 | 0 | — |
| `BO-056` | Time & Attendance | listDetail | 3 | 0 | — |
| `BO-057` | Training & Certification | listDetail | 1 | 0 | — |
| `BO-066` | Notification Settings | listDetail | 4 | 0 | — |
| `BO-084` | Approval Inbox | approvalInbox | 3 | 0 | — |
| `BO-085` | Approval Request | approvalInbox | 5 | 1 | — |
| `BO-086` | Approval Matrix | listDetail | 2 | 0 | — |
| `BO-087` | Approval Delegations | listDetail | 3 | 1 | — |

## Thin screens in this batch

**BO-086 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every staff",
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
       "label": "The selected staff",
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
       "label": "Create",
       "operation": "createPrincipal",
       "provenance": "contract identity.yaml POST /principals"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePrincipal",
       "provenance": "contract identity.yaml PATCH /principals/{principalId}"
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
       "impliedBy": "listPrincipals",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createPrincipal",
       "label": "Create principal",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createPrincipal",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staff list.",
   "error": "Could not load. Names which read failed and leaves the staff untouched.",
   "emptyFirstRun": "No staff yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the staff are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
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
   "note": "**Drawn by Claude Design on `Marketing Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
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
       "label": "Every role assignment",
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
       "label": "The selected role assignment",
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
       "label": "Create",
       "operation": "createRole",
       "provenance": "contract identity.yaml POST /roles"
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
       "impliedBy": "listRoles",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createRole",
       "label": "Create role",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createRole",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The role assignment list.",
   "error": "Could not load. Names which read failed and leaves the role assignment untouched.",
   "emptyFirstRun": "No role assignment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the role assignment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   }
  ],
  "entryState": {
   "preloaded": [
    "Role.id",
    "Role.code",
    "Role.name",
    "Role.description",
    "Role.permissions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-054"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every rota scheduling",
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
       "label": "The selected rota scheduling",
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
       "label": "Create",
       "operation": "createRotaAssignment",
       "provenance": "contract workforce.yaml POST /rota-assignments"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateRotaAssignment",
       "provenance": "contract workforce.yaml PATCH /rota-assignments/{assignmentId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Request",
       "operation": "requestShiftSwap",
       "provenance": "contract workforce.yaml POST /rota-assignments/{assignmentId}/swap"
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
       "impliedBy": "listRotaAssignments",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createRotaAssignment",
       "label": "Create rota assignment",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createRotaAssignment",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rota scheduling list.",
   "error": "Could not load. Names which read failed and leaves the rota scheduling untouched.",
   "emptyFirstRun": "No rota scheduling yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rota scheduling are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every time attendance",
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
       "label": "The selected time attendance",
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
        "AttendanceRecord.exception"
       ],
       "operation": "listAttendance",
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
       "label": "Amend",
       "operation": "amendAttendance",
       "provenance": "contract workforce.yaml POST /attendance/{recordId}/amend"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordAttendance",
       "provenance": "contract workforce.yaml POST /attendance/clock"
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
       "impliedBy": "listAttendance",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "amendAttendance",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The time attendance list.",
   "error": "Could not load. Names which read failed and leaves the time attendance untouched.",
   "emptyFirstRun": "No time attendance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the time attendance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every training certification",
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
       "label": "The selected training certification",
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
       "impliedBy": "listPrincipals",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The training certification list.",
   "error": "Could not load. Names which read failed and leaves the training certification untouched.",
   "emptyFirstRun": "No training certification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the training certification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
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
       "kind": "dataTable",
       "label": "Every notification settings",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected notification settings",
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
       "label": "Publish",
       "operation": "publishAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements"
      },
      {
       "kind": "secondaryButton",
       "label": "Acknowledge",
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
       "impliedBy": "listAnnouncements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "publishAnnouncement",
       "label": "Publish announcement",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "publishAnnouncement",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishAnnouncement",
       "notes": "Declares `publishAnnouncement`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The notification settings list.",
   "error": "Could not load. Names which read failed and leaves the notification settings untouched.",
   "emptyFirstRun": "No notification settings yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the notification settings are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
    "AnnouncementReach.announcementId",
    "AnnouncementReach.targeted",
    "AnnouncementReach.delivered",
    "AnnouncementReach.acknowledged",
    "AnnouncementReach.outstanding"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-066"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "BO-001",
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
     "to": "BO-085",
     "trigger": "Approves it",
     "provenance": "flow F14 step 3→4",
     "operation": "listApprovalRequests"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-087",
     "trigger": "Approval Delegations",
     "carries": [
      "delegationId"
     ],
     "provenance": "derived — BO-087 declares entryState.params delegationId, so an edge into it must carry them"
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
       "label": "The selected approval",
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
       "label": "Decide",
       "operation": "decideApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/decide"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
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
   "emptyNoResults": "The filter narrowed it and the approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-084"
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
    "BO-001",
    "BO-084",
    "BO-086",
    "BO-087"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-084",
     "trigger": "Approval Inbox",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-084 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "BO-087",
     "trigger": "Approval Delegations",
     "carries": [
      "delegationId"
     ],
     "provenance": "derived — BO-087 declares entryState.params delegationId, so an edge into it must carry them"
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
       "label": "Decide",
       "operation": "decideApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/decide"
      },
      {
       "kind": "secondaryButton",
       "label": "Resubmit",
       "operation": "resubmitApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/resubmit"
      },
      {
       "kind": "destructiveButton",
       "label": "Withdraw",
       "operation": "withdrawApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/withdraw"
      },
      {
       "kind": "secondaryButton",
       "label": "Evaluate",
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
    "trigger": "Withdraw",
    "body": "**Names what `withdrawApprovalRequest` changes and what it leaves alone**, in the consequence rather than the verb. A approval request this affects should be identified in the dialog, not just counted.",
    "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/withdraw"
   }
  ],
  "states": {
   "loading": "The approval request list.",
   "error": "Could not load. Names which read failed and leaves the approval request untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the approval request are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "BO-001",
    "BO-084",
    "BO-085",
    "BO-087"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-084",
     "trigger": "Approval Inbox",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-084 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "BO-085",
     "trigger": "Approval Request",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-085 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "BO-087",
     "trigger": "Approval Delegations",
     "carries": [
      "delegationId"
     ],
     "provenance": "derived — BO-087 declares entryState.params delegationId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every approval",
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
       "label": "The selected approval",
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
       "label": "Save changes",
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
   "emptyFirstRun": "No approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "BO-001",
    "BO-084",
    "BO-085",
    "BO-086"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-084",
     "trigger": "Approval Inbox",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-084 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "BO-085",
     "trigger": "Approval Request",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-085 declares entryState.params requestId, so an edge into it must carry them"
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
       "label": "Every approval delegations",
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
       "label": "The selected approval delegations",
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
       "label": "Create",
       "operation": "createApprovalDelegation",
       "provenance": "contract approvals.yaml POST /delegations"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke",
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
    "trigger": "Revoke",
    "body": "**Names what `revokeApprovalDelegation` changes and what it leaves alone**, in the consequence rather than the verb. A approval delegations this affects should be identified in the dialog, not just counted.",
    "provenance": "contract approvals.yaml DELETE /delegations/{delegationId}"
   }
  ],
  "states": {
   "loading": "The approval delegations list.",
   "error": "Could not load. Names which read failed and leaves the approval delegations untouched.",
   "emptyFirstRun": "No approval delegations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval delegations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
  "summary": "Approve or reject",
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
  "responds": "RotaAssignment"
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
    "format": "uuid"
   },
   "delegatePrincipalId": {
    "type": "string",
    "format": "uuid"
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
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "shiftVariance",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodReopen",
   "tenantMigration"
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
    "description": "11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n"
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
    "description": "11.1.12. **Nothing supplies this yet** — risk scoring is parked with the model-dependent AI. The field exists so adding the engine later is configuration rather than a schema change.\n"
   },
   "condition": {
    "type": "string",
    "nullable": true,
    "description": "11.1.13. Evaluated against the attributes the caller supplied."
   },
   "approverRoleIds": {
    "type": "array",
    "minItems": 1,
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
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAfterMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.53. An unanswered request eventually stops waiting."
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
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
    "nullable": true
   },
   "amendmentReason": {
    "type": "string",
    "nullable": true
   },
   "originalOccurredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"
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
    "maxLength": 512
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
    "type": "string"
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
    "description": "**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n"
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
    "description": "What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n"
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
 }
}
```
