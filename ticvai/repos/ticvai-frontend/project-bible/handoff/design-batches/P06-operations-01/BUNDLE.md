# P06-operations-01 — P06 · Operations (1 of 5)

**10 screens · 52 operations · 48 schemas · 23 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 23 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, ANNOUNCEMENT_PUBLISH, CASH_LIFT, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, MAINTENANCE_APPROVE, MAINTENANCE_EXECUTE, OVERSHORT_ACCEPT, REPORT_VIEW_VENUE, REPORT_VIEW_WORKSTATION`…. A control nobody can use must say so,
  not sit enabled and fail.
- **31 of these operations work offline**: acceptWorkOrder, acknowledgeAnnouncement, attachWorkOrderEvidence, closeShift, completeWorkOrder, createCashMovement, createWorkOrder, getCurrentSession
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-001` | Sign in | listDetail | 5 | 0 | — |
| `EMP-002` | Select venue & role | listDetail | 6 | 0 | — |
| `EMP-003` | Home — on duty | approvalInbox | 17 | 2 | — |
| `EMP-009` | End shift | approvalInbox | 13 | 2 | — |
| `EMP-010` | Scan — ready | listDetail | 7 | 1 | — |
| `EMP-004` | Task list | listDetail | 15 | 3 | — |
| `EMP-005` | Task detail | listDetail | 15 | 3 | — |
| `EMP-006` | Raise a task | listDetail | 16 | 3 | — |
| `EMP-007` | Handover notes | listDetail | 4 | 0 | — |
| `EMP-008` | Shift summary | listDetail | 5 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-001",
  "name": "Sign in",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/sign-in",
   "component": "apps/venue-staff-app/src/routes/operations/SignInDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-002",
    "EMP-003",
    "EMP-048"
   ],
   "inferred": true,
   "fromFlows": true,
   "isEntryPoint": true,
   "transitions": [
    {
     "to": "EMP-002",
     "trigger": "Selects venue and role",
     "provenance": "flow F08 step 1→2, F64 step 1→2"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "structural — EMP-001 is P06's home screen and its exits are its launcher"
    },
    {
     "to": "EMP-048",
     "trigger": "Opening checklist",
     "provenance": "structural — EMP-001 is P06's home screen and its exits are its launcher"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Sign in.** A shared device between shifts shows nothing until somebody identifies themselves. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable. **Removed 24 August**: forceLogout, listActiveSessions, revokeAllSessions. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listMfaMethods` reads the population and `getCurrentSession` reads one of them — list, select, act",
  "purpose": "Get an employee onto a shared device fast.",
  "gaps": [
   {
    "operation": "getGuestSession",
    "why": "**2 declared operations reach no component on this screen**: getGuestSession, listSsoProviders. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every sign",
       "bindsTo": "MfaMethod",
       "columns": [
        "MfaMethod.id",
        "MfaMethod.kind",
        "MfaMethod.label",
        "MfaMethod.maskedTarget",
        "MfaMethod.isActive",
        "MfaMethod.isPrimary",
        "MfaMethod.enrolledAt",
        "MfaMethod.lastUsedAt"
       ],
       "operation": "listMfaMethods",
       "provenance": "contract identity.yaml GET /auth/mfa/methods"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected sign",
       "bindsTo": "Session",
       "columns": [
        "Session.sessionId",
        "Session.principalId",
        "Session.roleId",
        "Session.displayName",
        "Session.scope",
        "Session.effectivePermissions",
        "Session.permissionsByScope",
        "Session.saleBoardId",
        "Session.workstation",
        "Session.openedAt",
        "Session.expiresAt"
       ],
       "operation": "getCurrentSession",
       "provenance": "contract identity.yaml GET /auth/session"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Login",
       "operation": "login",
       "provenance": "contract identity.yaml POST /auth/login"
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
       "impliedBy": "listMfaMethods",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "login",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sign list.",
   "error": "Could not load. Names which read failed and leaves the sign untouched.",
   "emptyFirstRun": "No sign yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sign are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Signs in against the cached principal list. A technician in a basement still needs their tasks"
  },
  "apis": [
   {
    "operationId": "login",
    "contract": "identity",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCurrentSession",
    "contract": "identity",
    "purpose": "Current session and effective permissions",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestSession",
    "contract": "identity",
    "purpose": "Read the current guest session",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMfaMethods",
    "contract": "identity",
    "purpose": "Enrolled MFA methods",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSsoProviders",
    "contract": "identity",
    "purpose": "Identity providers configured for this tenant",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Session.sessionId",
    "Session.principalId",
    "Session.roleId",
    "Session.displayName",
    "Session.scope"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-001"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-002",
  "name": "Select venue & role",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/select-venue-role",
   "component": "apps/venue-staff-app/src/routes/operations/SelectVenueRoleDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-003",
    "EMP-048"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "EMP-048",
     "trigger": "Works the opening checklist",
     "provenance": "flow F08 step 2→3, F64 step 2→3"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRole, forceLogout, listActiveSessions, revokeAllSessions. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.** ** restored** — a role-select screen must read the roles. Over-stripped and caught by F08.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listMfaMethods` reads the population and `getCurrentSession` reads one of them — list, select, act",
  "purpose": "Confirm which hat this person is wearing today.",
  "gaps": [
   {
    "operation": "getGuestSession",
    "why": "**3 declared operations reach no component on this screen**: getGuestSession, listSsoProviders, listRoles. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every select venue role",
       "bindsTo": "MfaMethod",
       "columns": [
        "MfaMethod.id",
        "MfaMethod.kind",
        "MfaMethod.label",
        "MfaMethod.maskedTarget",
        "MfaMethod.isActive",
        "MfaMethod.isPrimary",
        "MfaMethod.enrolledAt",
        "MfaMethod.lastUsedAt"
       ],
       "operation": "listMfaMethods",
       "provenance": "contract identity.yaml GET /auth/mfa/methods"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected select venue role",
       "bindsTo": "Session",
       "columns": [
        "Session.sessionId",
        "Session.principalId",
        "Session.roleId",
        "Session.displayName",
        "Session.scope",
        "Session.effectivePermissions",
        "Session.permissionsByScope",
        "Session.saleBoardId",
        "Session.workstation",
        "Session.openedAt",
        "Session.expiresAt"
       ],
       "operation": "getCurrentSession",
       "provenance": "contract identity.yaml GET /auth/session"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Select",
       "operation": "selectRole",
       "provenance": "contract identity.yaml POST /auth/select-role"
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
       "impliedBy": "listMfaMethods",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "selectRole",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The select venue role list.",
   "error": "Could not load. Names which read failed and leaves the select venue role untouched.",
   "emptyFirstRun": "No select venue role yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the select venue role are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached from the last session"
  },
  "apis": [
   {
    "operationId": "selectRole",
    "contract": "identity",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCurrentSession",
    "contract": "identity",
    "purpose": "Current session and effective permissions",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestSession",
    "contract": "identity",
    "purpose": "Read the current guest session",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMfaMethods",
    "contract": "identity",
    "purpose": "Enrolled MFA methods",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSsoProviders",
    "contract": "identity",
    "purpose": "Identity providers configured for this tenant",
    "trigger": "onLoad"
   },
   {
    "operationId": "listRoles",
    "contract": "identity",
    "purpose": "Roles this principal may take",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Session.sessionId",
    "Session.principalId",
    "Session.roleId",
    "Session.displayName",
    "Session.scope"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-002"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-003",
  "name": "Home — on duty",
  "module": "Operations",
  "requiresModule": "maintenance",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/home-on-duty",
   "component": "apps/venue-staff-app/src/routes/operations/HomeOnDutyDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-004",
    "EMP-048",
    "EMP-051",
    "EMP-052",
    "EMP-053",
    "EMP-054",
    "EMP-055",
    "EMP-056",
    "EMP-057",
    "EMP-058",
    "EMP-059",
    "EMP-060",
    "EMP-061",
    "EMP-062",
    "EMP-063",
    "EMP-064",
    "EMP-065",
    "EMP-066",
    "EMP-067",
    "EMP-068",
    "EMP-069",
    "EMP-070",
    "EMP-071",
    "EMP-081",
    "EMP-091"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "EMP-004",
     "trigger": "Works the task list",
     "provenance": "flow F08 step 4→5"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-051",
     "trigger": "Restaurant Service Command Center",
     "carries": [
      "outletId",
      "venueId"
     ],
     "provenance": "derived — EMP-051 declares entryState.params outletId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-052",
     "trigger": "Floor Plan & Table Map",
     "carries": [
      "outletId",
      "venueId"
     ],
     "provenance": "derived — EMP-052 declares entryState.params outletId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-053",
     "trigger": "Table & Seating Configuration",
     "carries": [
      "outletId",
      "venueId"
     ],
     "provenance": "derived — EMP-053 declares entryState.params outletId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-054",
     "trigger": "Reservation Calendar & Timeline",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — EMP-054 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-055",
     "trigger": "Create / Edit Reservation",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — EMP-055 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-056",
     "trigger": "Walk-In & Waitlist Management",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — EMP-056 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-057",
     "trigger": "Guest Profile & Dining History",
     "carries": [
      "subjectId",
      "venueId"
     ],
     "provenance": "derived — EMP-057 declares entryState.params subjectId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-058",
     "trigger": "Live Table & Service Management",
     "carries": [
      "entryId",
      "outletId",
      "reservationId",
      "ticketId",
      "venueId",
      "visitId"
     ],
     "provenance": "derived — EMP-058 declares entryState.params entryId, outletId, reservationId, ticketId, venueId, visitId, so an edge into it must carry them"
    },
    {
     "to": "EMP-059",
     "trigger": "Table Order, Bill & Payment Management",
     "carries": [
      "venueId",
      "visitId"
     ],
     "provenance": "derived — EMP-059 declares entryState.params venueId, visitId, so an edge into it must carry them"
    },
    {
     "to": "EMP-060",
     "trigger": "Reservation & Table Performance",
     "carries": [
      "outletId",
      "venueId"
     ],
     "provenance": "derived — EMP-060 declares entryState.params outletId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-061",
     "trigger": "Retail Inventory Command Center",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — EMP-061 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-062",
     "trigger": "Store Stock & SKU Availability",
     "carries": [
      "itemId",
      "venueId"
     ],
     "provenance": "derived — EMP-062 declares entryState.params itemId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-063",
     "trigger": "Requisition & Smart Store Replenishment",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — EMP-063 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-064",
     "trigger": "Store-to-Store & Warehouse Transfers",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — EMP-064 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-065",
     "trigger": "Receiving & Store Put-Away",
     "carries": [
      "receiptId",
      "transferId",
      "venueId"
     ],
     "provenance": "derived — EMP-065 declares entryState.params receiptId, transferId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-066",
     "trigger": "Stock Count & Cycle Count Management",
     "carries": [
      "countId",
      "venueId"
     ],
     "provenance": "derived — EMP-066 declares entryState.params countId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-067",
     "trigger": "Damage, Loss, Shrinkage & Stock Adjustment",
     "carries": [
      "actionId",
      "outletId",
      "venueId"
     ],
     "provenance": "derived — EMP-067 declares entryState.params actionId, outletId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-068",
     "trigger": "Reservation, Allocation & Omnichannel Inventory",
     "carries": [
      "outletId",
      "venueId"
     ],
     "provenance": "derived — EMP-068 declares entryState.params outletId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-069",
     "trigger": "Barcode, RFID, Serialized Stock & Traceability",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — EMP-069 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-070",
     "trigger": "Inventory Exceptions, AI Replenishment & Action Center",
     "carries": [
      "alertId",
      "venueId"
     ],
     "provenance": "derived — EMP-070 declares entryState.params alertId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-071",
     "trigger": "Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-081",
     "trigger": "Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-091",
     "trigger": "Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    }
   ],
   "entryFrom": [
    "EMP-071",
    "EMP-081",
    "EMP-091"
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **createCashMovement removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class).",
  "density": "comfortable",
  "pattern": "approvalInbox",
  "patternReason": "`approveShiftOpen` decides items that `listIncidents` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "The screen the device sits on between tasks.",
  "gaps": [
   {
    "operation": "getIncident",
    "why": "**4 declared operations reach no component on this screen**: getIncident, getShift, listCashMovements, listShifts. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
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
       "bindsTo": "Incident",
       "columns": [
        "Incident.id",
        "Incident.incidentNumber",
        "Incident.kind",
        "Incident.severity",
        "Incident.status",
        "Incident.venueId",
        "Incident.assetId",
        "Incident.locationDescription",
        "Incident.isReportable",
        "Incident.notificationDueAt",
        "Incident.notifiedAt",
        "Incident.assignedToPrincipalId"
       ],
       "operation": "listIncidents",
       "provenance": "contract maintenance.yaml GET /incidents"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected home duty",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber",
        "Shift.openingFloat",
        "Shift.salesTotal",
        "Shift.refundsTotal",
        "Shift.liftsTotal"
       ],
       "operation": "getCurrentShift",
       "provenance": "contract shift.yaml GET /shifts/current"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Accept",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Open",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordAuthorityNotification",
       "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Report",
       "operation": "reportIncident",
       "provenance": "contract maintenance.yaml POST /incidents"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateIncident",
       "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
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
       "impliedBy": "listIncidents",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "acceptShiftVariance",
       "label": "Accept shift variance",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "acceptShiftVariance",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A home duty this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A home duty this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   }
  ],
  "states": {
   "loading": "The home duty list.",
   "error": "Could not load. Names which read failed and leaves the home duty untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the home duty are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Last synced view, with its age. The pending count is always current because it is local"
  },
  "apis": [
   {
    "operationId": "getCurrentShift",
    "contract": "shift",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "listIncidents",
    "contract": "maintenance",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "acceptShiftVariance",
    "contract": "shift",
    "purpose": "Accept an over/short beyond the threshold",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "approveShiftOpen",
    "contract": "shift",
    "purpose": "Approve a shift opening outside tolerance",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "closeShift",
    "contract": "shift",
    "purpose": "Blind close-out",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "Read an incident",
    "trigger": "onLoad"
   },
   {
    "operationId": "getShift",
    "contract": "shift",
    "purpose": "Read a shift",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCashMovements",
    "contract": "shift",
    "purpose": "Lifts, adds and the opening float",
    "trigger": "onLoad"
   },
   {
    "operationId": "listShifts",
    "contract": "shift",
    "purpose": "List shifts",
    "trigger": "onLoad"
   },
   {
    "operationId": "openShift",
    "contract": "shift",
    "purpose": "Open a shift",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "recordAuthorityNotification",
    "contract": "maintenance",
    "purpose": "Record notification to an external authority",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "recordNoSale",
    "contract": "shift",
    "purpose": "Open the drawer without a sale",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "reopenShift",
    "contract": "shift",
    "purpose": "Reopen a shift closed in error",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "reportIncident",
    "contract": "maintenance",
    "purpose": "Report an incident",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "resumeShift",
    "contract": "shift",
    "purpose": "Resume a suspended shift",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "suspendShift",
    "contract": "shift",
    "purpose": "Suspend a shift so another user can log in",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "updateIncident",
    "contract": "maintenance",
    "purpose": "Investigate, escalate or close an incident",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "incidentId",
     "from": "deepLink"
    },
    {
     "name": "shiftId",
     "from": "session"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `incidentId`.",
   "preloaded": [
    "Shift.id",
    "Shift.workstationId",
    "Shift.venueId",
    "Shift.scopePath",
    "Shift.principalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-003"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 17 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-009",
  "name": "End shift",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/end-shift",
   "component": "apps/venue-staff-app/src/routes/operations/EndShiftDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": true,
   "entryFrom": [
    "EMP-017"
   ],
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "approvalInbox",
  "patternReason": "`approveShiftOpen` decides items that `listCashMovements` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Close out cleanly, including anything unsynced.",
  "gaps": [
   {
    "operation": "getShift",
    "why": "**2 declared operations reach no component on this screen**: getShift, listShifts. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
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
       "bindsTo": "CashMovement",
       "columns": [
        "CashMovement.id",
        "CashMovement.kind",
        "CashMovement.amount",
        "CashMovement.denominations",
        "CashMovement.reference",
        "CashMovement.reason",
        "CashMovement.recordedAt",
        "CashMovement.shiftId",
        "CashMovement.authorisedByPrincipalId",
        "CashMovement.sequence",
        "CashMovement.syncedAt"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected end shift",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber",
        "Shift.openingFloat",
        "Shift.salesTotal",
        "Shift.refundsTotal",
        "Shift.liftsTotal"
       ],
       "operation": "getCurrentShift",
       "provenance": "contract shift.yaml GET /shifts/current"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCashMovement",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Open",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
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
       "impliedBy": "listCashMovements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "closeShift",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A end shift this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A end shift this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   }
  ],
  "states": {
   "loading": "The end shift list.",
   "error": "Could not load. Names which read failed and leaves the end shift untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the end shift are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Cannot close.** Closing needs the server total, and a locally computed variance is not a variance"
  },
  "apis": [
   {
    "operationId": "closeShift",
    "contract": "shift",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "acceptShiftVariance",
    "contract": "shift",
    "purpose": "Accept an over/short beyond the threshold",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "approveShiftOpen",
    "contract": "shift",
    "purpose": "Approve a shift opening outside tolerance",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "createCashMovement",
    "contract": "shift",
    "purpose": "Record a cash lift or add",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "getCurrentShift",
    "contract": "shift",
    "purpose": "The open or suspended shift on the session's workstation",
    "trigger": "onLoad"
   },
   {
    "operationId": "getShift",
    "contract": "shift",
    "purpose": "Read a shift",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCashMovements",
    "contract": "shift",
    "purpose": "Lifts, adds and the opening float",
    "trigger": "onLoad"
   },
   {
    "operationId": "listShifts",
    "contract": "shift",
    "purpose": "List shifts",
    "trigger": "onLoad"
   },
   {
    "operationId": "openShift",
    "contract": "shift",
    "purpose": "Open a shift",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "recordNoSale",
    "contract": "shift",
    "purpose": "Open the drawer without a sale",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "reopenShift",
    "contract": "shift",
    "purpose": "Reopen a shift closed in error",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "resumeShift",
    "contract": "shift",
    "purpose": "Resume a suspended shift",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "suspendShift",
    "contract": "shift",
    "purpose": "Suspend a shift so another user can log in",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "shiftId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Shift.id",
    "Shift.workstationId",
    "Shift.venueId",
    "Shift.scopePath",
    "Shift.principalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-009"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-010",
  "name": "Scan — ready",
  "module": "Operations",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/scan-ready",
   "component": "apps/venue-staff-app/src/routes/operations/ScanReadyDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Absorbed EMP-011, EMP-012, EMP-013, EMP-016 on 18 August.** A scanner is one screen the device sits on all day, and an outcome is a state of it — **routing to `/access/admitted` for something gone in 1.5 seconds is a page load per guest**, and at a gate doing 40 a minute that is the whole problem. Every absorbed screen kept its copy as a named state.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "The raised centre action, and the thing this app is for.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every scan ready",
       "bindsTo": "ScanEvent",
       "columns": [
        "ScanEvent.id",
        "ScanEvent.accessPointId",
        "ScanEvent.venueId",
        "ScanEvent.scopePath",
        "ScanEvent.ticketId",
        "ScanEvent.mediaCode",
        "ScanEvent.outcome",
        "ScanEvent.denyReason",
        "ScanEvent.direction",
        "ScanEvent.operatorPrincipalId",
        "ScanEvent.deviceId",
        "ScanEvent.overriddenByPrincipalId"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected scan ready",
       "bindsTo": "OfflinePackage",
       "columns": [
        "OfflinePackage.generatedAt",
        "OfflinePackage.validFrom",
        "OfflinePackage.validTo",
        "OfflinePackage.accessPointId",
        "OfflinePackage.entitlements",
        "OfflinePackage.delegatedRights",
        "OfflinePackage.blacklist",
        "OfflinePackage.admissionRules"
       ],
       "operation": "getOfflinePackage",
       "provenance": "contract access.yaml GET /access/offline-package"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Sync",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup",
       "operation": "lookupTicket",
       "provenance": "contract access.yaml GET /access/lookup"
      },
      {
       "kind": "destructiveButton",
       "label": "Override",
       "operation": "overrideAccess",
       "provenance": "contract access.yaml POST /access/override"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateAccess",
       "provenance": "contract access.yaml POST /access/validate"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateGroupAccess",
       "provenance": "contract access.yaml POST /access/group-validate"
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
       "kind": "scanTarget",
       "derived": true,
       "impliedBy": "listScans",
       "notes": "**A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or explain something.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupTicket",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "syncScans",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmOverrideAccess",
    "component": "confirmDialog",
    "trigger": "Override",
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A scan ready this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml POST /access/override"
   }
  ],
  "states": {
   "loading": "The scan ready list.",
   "error": "Could not load. Names which read failed and leaves the scan ready untouched.",
   "emptyFirstRun": "No scan ready yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the scan ready are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Keep working when the network does not.** The screen already had an `offline` state."
  },
  "apis": [
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
    "trigger": "onLoad"
   },
   {
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupTicket",
    "contract": "access",
    "purpose": "Read-only validity check without admitting",
    "trigger": "onLoad"
   },
   {
    "operationId": "overrideAccess",
    "contract": "access",
    "purpose": "Admit against a failed validation",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "validateAccess",
    "contract": "access",
    "purpose": "Validate media at an access point and admit or deny",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "validateGroupAccess",
    "contract": "access",
    "purpose": "Admit a group on one read",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflinePackage.generatedAt",
    "OfflinePackage.validFrom",
    "OfflinePackage.validTo",
    "OfflinePackage.accessPointId",
    "OfflinePackage.entitlements"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-010"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-004",
  "name": "Task list",
  "module": "Operations",
  "requiresModule": "maintenance",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/task-list",
   "component": "apps/venue-staff-app/src/routes/operations/TaskListDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-005"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "EMP-005",
     "trigger": "Completes a task",
     "provenance": "flow F08 step 5→6, F12 step 2→3, F65 step 2→3"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ],
   "entryFrom": [
    "EMP-006"
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createWorkOrder. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act",
  "purpose": "See what is assigned, and what is overdue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every task list",
       "bindsTo": "WorkOrder",
       "columns": [
        "WorkOrder.downtimeMinutes",
        "WorkOrder.rootCause",
        "WorkOrder.rootCauseNote",
        "WorkOrder.escalatedAt",
        "WorkOrder.escalationLevel",
        "WorkOrder.id",
        "WorkOrder.workOrderNumber",
        "WorkOrder.title",
        "WorkOrder.venueId",
        "WorkOrder.assetId",
        "WorkOrder.assetName",
        "WorkOrder.status"
       ],
       "operation": "listWorkOrders",
       "provenance": "contract maintenance.yaml GET /work-orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected task list",
       "bindsTo": "WorkOrderDetail",
       "columns": [
        "WorkOrderDetail.downtimeMinutes",
        "WorkOrderDetail.rootCause",
        "WorkOrderDetail.rootCauseNote",
        "WorkOrderDetail.escalatedAt",
        "WorkOrderDetail.escalationLevel",
        "WorkOrderDetail.id",
        "WorkOrderDetail.workOrderNumber",
        "WorkOrderDetail.title",
        "WorkOrderDetail.venueId",
        "WorkOrderDetail.assetId",
        "WorkOrderDetail.assetName",
        "WorkOrderDetail.status",
        "WorkOrderDetail.priority",
        "WorkOrderDetail.kind",
        "WorkOrderDetail.assignedToPrincipalId",
        "WorkOrderDetail.raisedByPrincipalId"
       ],
       "operation": "getWorkOrder",
       "provenance": "contract maintenance.yaml GET /work-orders/{workOrderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Accept",
       "operation": "acceptWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/accept"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
      },
      {
       "kind": "secondaryButton",
       "label": "Attach",
       "operation": "attachWorkOrderEvidence",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause",
       "operation": "pauseWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordWorkOrderParts",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordWorkOrderTime",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/resume"
      },
      {
       "kind": "secondaryButton",
       "label": "Start",
       "operation": "startWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateWorkOrder",
       "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
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
       "impliedBy": "listWorkOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "acceptWorkOrder",
       "label": "Accept work order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelWorkOrder",
       "label": "Cancel work order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "acceptWorkOrder",
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
    "id": "confirmRejectWorkOrder",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
   },
   {
    "id": "confirmCancelWorkOrder",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
   },
   {
    "id": "confirmCloseWorkOrder",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
   }
  ],
  "states": {
   "loading": "The task list list.",
   "error": "Could not load. Names which read failed and leaves the task list untouched.",
   "emptyFirstRun": "No task list yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the task list are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Local queue. Tasks completed offline sync on return"
  },
  "apis": [
   {
    "operationId": "listWorkOrders",
    "contract": "maintenance",
    "purpose": "List work orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "acceptWorkOrder",
    "contract": "maintenance",
    "purpose": "The assignee takes the job",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "rejectWorkOrder",
    "contract": "maintenance",
    "purpose": "The assignee declines, with a reason",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "attachWorkOrderEvidence",
    "contract": "maintenance",
    "purpose": "Photo, video, document, note or signature",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "cancelWorkOrder",
    "contract": "maintenance",
    "purpose": "Cancel a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "closeWorkOrder",
    "contract": "maintenance",
    "purpose": "Administratively closed",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "completeWorkOrder",
    "contract": "maintenance",
    "purpose": "Complete a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "getWorkOrder",
    "contract": "maintenance",
    "purpose": "Read a work order",
    "trigger": "onLoad"
   },
   {
    "operationId": "pauseWorkOrder",
    "contract": "maintenance",
    "purpose": "Stopped, and why",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "recordWorkOrderParts",
    "contract": "maintenance",
    "purpose": "Record parts consumed",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "recordWorkOrderTime",
    "contract": "maintenance",
    "purpose": "Start, pause or stop work",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "resumeWorkOrder",
    "contract": "maintenance",
    "purpose": "Back to work",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "startWorkOrder",
    "contract": "maintenance",
    "purpose": "Work has begun",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "updateWorkOrder",
    "contract": "maintenance",
    "purpose": "Assign, reprioritise or amend",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "verifyWorkOrder",
    "contract": "maintenance",
    "purpose": "Supervisor verification",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "workOrderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `workOrderId`.",
   "preloaded": [
    "WorkOrderDetail.downtimeMinutes",
    "WorkOrderDetail.rootCause",
    "WorkOrderDetail.rootCauseNote",
    "WorkOrderDetail.escalatedAt",
    "WorkOrderDetail.escalationLevel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-004"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 15 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-005",
  "name": "Task detail",
  "module": "Operations",
  "requiresModule": "maintenance",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/task-detail",
   "component": "apps/venue-staff-app/src/routes/operations/TaskDetailDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-007"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "EMP-007",
     "trigger": "Writes handover notes",
     "provenance": "flow F08 step 6→7, F65 step 4→5"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-030",
     "trigger": "Supervisor verifies",
     "provenance": "flow F12 step 3→4",
     "operation": "completeWorkOrder",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "BO-078",
     "trigger": "Raises a requisition against the work order",
     "provenance": "flow F15 step 1→2",
     "operation": "pauseWorkOrder",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: BO-030, BO-078. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: createWorkOrder. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act",
  "purpose": "Do the task and record that it was done.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every task",
       "bindsTo": "WorkOrder",
       "columns": [
        "WorkOrder.downtimeMinutes",
        "WorkOrder.rootCause",
        "WorkOrder.rootCauseNote",
        "WorkOrder.escalatedAt",
        "WorkOrder.escalationLevel",
        "WorkOrder.id",
        "WorkOrder.workOrderNumber",
        "WorkOrder.title",
        "WorkOrder.venueId",
        "WorkOrder.assetId",
        "WorkOrder.assetName",
        "WorkOrder.status"
       ],
       "operation": "listWorkOrders",
       "provenance": "contract maintenance.yaml GET /work-orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected task",
       "bindsTo": "WorkOrderDetail",
       "columns": [
        "WorkOrderDetail.downtimeMinutes",
        "WorkOrderDetail.rootCause",
        "WorkOrderDetail.rootCauseNote",
        "WorkOrderDetail.escalatedAt",
        "WorkOrderDetail.escalationLevel",
        "WorkOrderDetail.id",
        "WorkOrderDetail.workOrderNumber",
        "WorkOrderDetail.title",
        "WorkOrderDetail.venueId",
        "WorkOrderDetail.assetId",
        "WorkOrderDetail.assetName",
        "WorkOrderDetail.status",
        "WorkOrderDetail.priority",
        "WorkOrderDetail.kind",
        "WorkOrderDetail.assignedToPrincipalId",
        "WorkOrderDetail.raisedByPrincipalId"
       ],
       "operation": "getWorkOrder",
       "provenance": "contract maintenance.yaml GET /work-orders/{workOrderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Start",
       "operation": "startWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause",
       "operation": "pauseWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept",
       "operation": "acceptWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/accept"
      },
      {
       "kind": "secondaryButton",
       "label": "Attach",
       "operation": "attachWorkOrderEvidence",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordWorkOrderParts",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordWorkOrderTime",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/resume"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateWorkOrder",
       "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
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
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelWorkOrder",
       "label": "Cancel work order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listWorkOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "startWorkOrder",
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
    "id": "confirmCancelWorkOrder",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
   },
   {
    "id": "confirmCloseWorkOrder",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
   },
   {
    "id": "confirmRejectWorkOrder",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
   }
  ],
  "states": {
   "loading": "The task list.",
   "error": "Could not load. Names which read failed and leaves the task untouched.",
   "emptyFirstRun": "No task yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the task are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Editable offline. Findings and photos queue"
  },
  "apis": [
   {
    "operationId": "getWorkOrder",
    "contract": "maintenance",
    "purpose": "Read a work order",
    "trigger": "onLoad"
   },
   {
    "operationId": "startWorkOrder",
    "contract": "maintenance",
    "purpose": "Work has begun",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "pauseWorkOrder",
    "contract": "maintenance",
    "purpose": "Stopped, and why",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "completeWorkOrder",
    "contract": "maintenance",
    "purpose": "Complete a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "acceptWorkOrder",
    "contract": "maintenance",
    "purpose": "The assignee takes the job",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "attachWorkOrderEvidence",
    "contract": "maintenance",
    "purpose": "Photo, video, document, note or signature",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "cancelWorkOrder",
    "contract": "maintenance",
    "purpose": "Cancel a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "closeWorkOrder",
    "contract": "maintenance",
    "purpose": "Administratively closed",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "listWorkOrders",
    "contract": "maintenance",
    "purpose": "List work orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordWorkOrderParts",
    "contract": "maintenance",
    "purpose": "Record parts consumed",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "recordWorkOrderTime",
    "contract": "maintenance",
    "purpose": "Start, pause or stop work",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "rejectWorkOrder",
    "contract": "maintenance",
    "purpose": "The assignee declines, with a reason",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "resumeWorkOrder",
    "contract": "maintenance",
    "purpose": "Back to work",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "updateWorkOrder",
    "contract": "maintenance",
    "purpose": "Assign, reprioritise or amend",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "verifyWorkOrder",
    "contract": "maintenance",
    "purpose": "Supervisor verification",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "workOrderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `workOrderId`.",
   "preloaded": [
    "WorkOrderDetail.downtimeMinutes",
    "WorkOrderDetail.rootCause",
    "WorkOrderDetail.rootCauseNote",
    "WorkOrderDetail.escalatedAt",
    "WorkOrderDetail.escalationLevel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-005"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 15 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-006",
  "name": "Raise a task",
  "module": "Operations",
  "requiresModule": "maintenance",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/raise-a-task",
   "component": "apps/venue-staff-app/src/routes/operations/RaiseATaskDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-004"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-004",
     "trigger": "It appears on the list for whoever is free",
     "provenance": "flow F65 step 1→2",
     "operation": "createWorkOrder"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act",
  "purpose": "Report something without finding a manager.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every raise task",
       "bindsTo": "WorkOrder",
       "columns": [
        "WorkOrder.downtimeMinutes",
        "WorkOrder.rootCause",
        "WorkOrder.rootCauseNote",
        "WorkOrder.escalatedAt",
        "WorkOrder.escalationLevel",
        "WorkOrder.id",
        "WorkOrder.workOrderNumber",
        "WorkOrder.title",
        "WorkOrder.venueId",
        "WorkOrder.assetId",
        "WorkOrder.assetName",
        "WorkOrder.status"
       ],
       "operation": "listWorkOrders",
       "provenance": "contract maintenance.yaml GET /work-orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected raise task",
       "bindsTo": "WorkOrderDetail",
       "columns": [
        "WorkOrderDetail.downtimeMinutes",
        "WorkOrderDetail.rootCause",
        "WorkOrderDetail.rootCauseNote",
        "WorkOrderDetail.escalatedAt",
        "WorkOrderDetail.escalationLevel",
        "WorkOrderDetail.id",
        "WorkOrderDetail.workOrderNumber",
        "WorkOrderDetail.title",
        "WorkOrderDetail.venueId",
        "WorkOrderDetail.assetId",
        "WorkOrderDetail.assetName",
        "WorkOrderDetail.status",
        "WorkOrderDetail.priority",
        "WorkOrderDetail.kind",
        "WorkOrderDetail.assignedToPrincipalId",
        "WorkOrderDetail.raisedByPrincipalId"
       ],
       "operation": "getWorkOrder",
       "provenance": "contract maintenance.yaml GET /work-orders/{workOrderId}"
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
       "operation": "createWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept",
       "operation": "acceptWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/accept"
      },
      {
       "kind": "secondaryButton",
       "label": "Attach",
       "operation": "attachWorkOrderEvidence",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause",
       "operation": "pauseWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordWorkOrderParts",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordWorkOrderTime",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/resume"
      },
      {
       "kind": "secondaryButton",
       "label": "Start",
       "operation": "startWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateWorkOrder",
       "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
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
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createWorkOrder",
       "label": "Create work order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelWorkOrder",
       "label": "Cancel work order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listWorkOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createWorkOrder",
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
    "id": "confirmCancelWorkOrder",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
   },
   {
    "id": "confirmCloseWorkOrder",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
   },
   {
    "id": "confirmRejectWorkOrder",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
   }
  ],
  "states": {
   "loading": "The raise task list.",
   "error": "Could not load. Names which read failed and leaves the raise task untouched.",
   "emptyFirstRun": "No raise task yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the raise task are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Queues locally. A task raised in a plant room must not need signal"
  },
  "apis": [
   {
    "operationId": "createWorkOrder",
    "contract": "maintenance",
    "purpose": "Raise a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "acceptWorkOrder",
    "contract": "maintenance",
    "purpose": "The assignee takes the job",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "attachWorkOrderEvidence",
    "contract": "maintenance",
    "purpose": "Photo, video, document, note or signature",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "cancelWorkOrder",
    "contract": "maintenance",
    "purpose": "Cancel a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "closeWorkOrder",
    "contract": "maintenance",
    "purpose": "Administratively closed",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "completeWorkOrder",
    "contract": "maintenance",
    "purpose": "Complete a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "getWorkOrder",
    "contract": "maintenance",
    "purpose": "Read a work order",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWorkOrders",
    "contract": "maintenance",
    "purpose": "List work orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "pauseWorkOrder",
    "contract": "maintenance",
    "purpose": "Stopped, and why",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "recordWorkOrderParts",
    "contract": "maintenance",
    "purpose": "Record parts consumed",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "recordWorkOrderTime",
    "contract": "maintenance",
    "purpose": "Start, pause or stop work",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "rejectWorkOrder",
    "contract": "maintenance",
    "purpose": "The assignee declines, with a reason",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "resumeWorkOrder",
    "contract": "maintenance",
    "purpose": "Back to work",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "startWorkOrder",
    "contract": "maintenance",
    "purpose": "Work has begun",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "updateWorkOrder",
    "contract": "maintenance",
    "purpose": "Assign, reprioritise or amend",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "verifyWorkOrder",
    "contract": "maintenance",
    "purpose": "Supervisor verification",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "workOrderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `workOrderId`.",
   "preloaded": [
    "WorkOrderDetail.downtimeMinutes",
    "WorkOrderDetail.rootCause",
    "WorkOrderDetail.rootCauseNote",
    "WorkOrderDetail.escalatedAt",
    "WorkOrderDetail.escalationLevel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-006"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 16 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-007",
  "name": "Handover notes",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/handover-notes",
   "component": "apps/venue-staff-app/src/routes/operations/HandoverNotesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-009"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "EMP-009",
     "trigger": "Ends the shift",
     "provenance": "flow F08 step 7→8"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act",
  "purpose": "Tell the next shift what they are walking into.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every handover notes",
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
       "label": "The selected handover notes",
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
   "loading": "The handover notes list.",
   "error": "Could not load. Names which read failed and leaves the handover notes untouched.",
   "emptyFirstRun": "No handover notes yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the handover notes are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Editable offline and synced at end of shift"
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-008",
  "name": "Shift summary",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/shift-summary",
   "component": "apps/venue-staff-app/src/routes/operations/ShiftSummaryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-017"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-017",
     "trigger": "Anything unsynced is pushed first",
     "provenance": "flow F72 step 1→2"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: acceptShiftVariance, approveShiftOpen, closeShift, createCashMovement. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Removed 24 August**: openShift, recordNoSale, reopenShift, resumeShift. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listShifts` reads the population and `getCurrentShift` reads one of them — list, select, act",
  "purpose": "See what this person actually did today.",
  "gaps": [
   {
    "operation": "getShift",
    "why": "**2 declared operations reach no component on this screen**: getShift, listCashMovements. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every shift summary",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber"
       ],
       "operation": "listShifts",
       "provenance": "contract shift.yaml GET /shifts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected shift summary",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber",
        "Shift.openingFloat",
        "Shift.salesTotal",
        "Shift.refundsTotal",
        "Shift.liftsTotal"
       ],
       "operation": "getCurrentShift",
       "provenance": "contract shift.yaml GET /shifts/current"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
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
       "impliedBy": "listShifts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "suspendShift",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A shift summary this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   }
  ],
  "states": {
   "loading": "The shift summary list.",
   "error": "Could not load. Names which read failed and leaves the shift summary untouched.",
   "emptyFirstRun": "No shift summary yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the shift summary are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Local totals, marked as unreconciled"
  },
  "apis": [
   {
    "operationId": "listShifts",
    "contract": "shift",
    "purpose": "List shifts",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCurrentShift",
    "contract": "shift",
    "purpose": "The open or suspended shift on the session's workstation",
    "trigger": "onLoad"
   },
   {
    "operationId": "getShift",
    "contract": "shift",
    "purpose": "Read a shift",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCashMovements",
    "contract": "shift",
    "purpose": "Lifts, adds and the opening float",
    "trigger": "onLoad"
   },
   {
    "operationId": "suspendShift",
    "contract": "shift",
    "purpose": "Suspend a shift so another user can log in",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "shiftId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Shift.id",
    "Shift.workstationId",
    "Shift.venueId",
    "Shift.scopePath",
    "Shift.principalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
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
 "acceptShiftVariance": {
  "method": "POST",
  "path": "/shifts/{shiftId}/accept-variance",
  "contract": "shift",
  "summary": "Accept an over/short beyond the threshold",
  "permission": "OVERSHORT_ACCEPT",
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
  "responds": "Shift"
 },
 "acceptWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/accept",
  "contract": "maintenance",
  "summary": "The assignee takes the job",
  "permission": "MAINTENANCE_EXECUTE",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkOrder"
 },
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
 "approveShiftOpen": {
  "method": "POST",
  "path": "/shifts/{shiftId}/approve-open",
  "contract": "shift",
  "summary": "Approve a shift opening outside tolerance",
  "permission": "SHIFT_APPROVE_OPEN",
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
  "responds": "Shift"
 },
 "attachWorkOrderEvidence": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/attachments",
  "contract": "maintenance",
  "summary": "Photo, video, document, note or signature",
  "permission": "MAINTENANCE_EXECUTE",
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
  "responds": "WorkOrderAttachment"
 },
 "cancelWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/cancel",
  "contract": "maintenance",
  "summary": "Cancel a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
 },
 "closeShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/close",
  "contract": "shift",
  "summary": "Blind close-out",
  "permission": "SHIFT_CLOSE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CloseShiftRequest",
  "responds": "ShiftCloseResult"
 },
 "closeWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/close",
  "contract": "maintenance",
  "summary": "Administratively closed",
  "permission": "MAINTENANCE_APPROVE",
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
  "responds": "WorkOrder"
 },
 "completeWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/complete",
  "contract": "maintenance",
  "summary": "Complete a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
 },
 "createCashMovement": {
  "method": "POST",
  "path": "/shifts/{shiftId}/cash-movements",
  "contract": "shift",
  "summary": "Record a cash lift or add",
  "permission": "CASH_LIFT",
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
  "requestBody": "CreateCashMovementRequest",
  "responds": "CashMovement"
 },
 "createWorkOrder": {
  "method": "POST",
  "path": "/work-orders",
  "contract": "maintenance",
  "summary": "Raise a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "requestBody": "CreateWorkOrderRequest",
  "responds": "WorkOrder"
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
 "getCurrentSession": {
  "method": "GET",
  "path": "/auth/session",
  "contract": "identity",
  "summary": "Current session and effective permissions",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "Session"
 },
 "getCurrentShift": {
  "method": "GET",
  "path": "/shifts/current",
  "contract": "shift",
  "summary": "The open or suspended shift on the session's workstation",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "Shift"
 },
 "getGuestSession": {
  "method": "GET",
  "path": "/auth/guest/session",
  "contract": "identity",
  "summary": "Read the current guest session",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestSession"
 },
 "getIncident": {
  "method": "GET",
  "path": "/incidents/{incidentId}",
  "contract": "maintenance",
  "summary": "Read an incident",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "IncidentDetail"
 },
 "getOfflinePackage": {
  "method": "GET",
  "path": "/access/offline-package",
  "contract": "access",
  "summary": "Entitlement and rule set for offline validation",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": "validFrom",
    "in": "query",
    "required": true
   },
   {
    "name": "validTo",
    "in": "query",
    "required": true
   },
   {
    "name": "If-None-Match",
    "in": "header",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OfflinePackage"
 },
 "getShift": {
  "method": "GET",
  "path": "/shifts/{shiftId}",
  "contract": "shift",
  "summary": "Read a shift",
  "permission": "REPORT_VIEW_WORKSTATION",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Shift"
 },
 "getWorkOrder": {
  "method": "GET",
  "path": "/work-orders/{workOrderId}",
  "contract": "maintenance",
  "summary": "Read a work order",
  "permission": "WORK_ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WorkOrderDetail"
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
 "listCashMovements": {
  "method": "GET",
  "path": "/shifts/{shiftId}/cash-movements",
  "contract": "shift",
  "summary": "Lifts, adds and the opening float",
  "permission": "REPORT_VIEW_WORKSTATION",
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
  "responds": "CashMovement"
 },
 "listIncidents": {
  "method": "GET",
  "path": "/incidents",
  "contract": "maintenance",
  "summary": "List incidents",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "severity",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "isReportable",
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
 "listMfaMethods": {
  "method": "GET",
  "path": "/auth/mfa/methods",
  "contract": "identity",
  "summary": "Enrolled MFA methods",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MfaMethod"
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
 "listScans": {
  "method": "GET",
  "path": "/access/scans",
  "contract": "access",
  "summary": "List scan events",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "accessPointId",
    "in": "query",
    "required": null
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedTo",
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
 "listShifts": {
  "method": "GET",
  "path": "/shifts",
  "contract": "shift",
  "summary": "List shifts",
  "permission": "REPORT_VIEW_WORKSTATION",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "openedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "openedTo",
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
 "listSsoProviders": {
  "method": "GET",
  "path": "/auth/sso/providers",
  "contract": "identity",
  "summary": "Identity providers configured for this tenant",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SsoProvider"
 },
 "listWorkOrders": {
  "method": "GET",
  "path": "/work-orders",
  "contract": "maintenance",
  "summary": "List work orders",
  "permission": "WORK_ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToPrincipalId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "priority",
    "in": "query",
    "required": null
   },
   {
    "name": "assetId",
    "in": "query",
    "required": null
   },
   {
    "name": "overdueOnly",
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
 "login": {
  "method": "POST",
  "path": "/auth/login",
  "contract": "identity",
  "summary": "Authenticate and open a session",
  "permission": null,
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
  "requestBody": "LoginRequest",
  "responds": "LoginResponse"
 },
 "lookupTicket": {
  "method": "GET",
  "path": "/access/lookup",
  "contract": "access",
  "summary": "Read-only validity check without admitting",
  "permission": "TICKET_LOOKUP",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "mediaCode",
    "in": "query",
    "required": null
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TicketStatus"
 },
 "openShift": {
  "method": "POST",
  "path": "/shifts",
  "contract": "shift",
  "summary": "Open a shift",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "OpenShiftRequest",
  "responds": "Shift"
 },
 "overrideAccess": {
  "method": "POST",
  "path": "/access/override",
  "contract": "access",
  "summary": "Admit against a failed validation",
  "permission": "ACCESS_OVERRIDE",
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
  "responds": "ValidationResult"
 },
 "pauseWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/pause",
  "contract": "maintenance",
  "summary": "Stopped, and why",
  "permission": "MAINTENANCE_EXECUTE",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkOrder"
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
 "recordAuthorityNotification": {
  "method": "POST",
  "path": "/incidents/{incidentId}/notify-authority",
  "contract": "maintenance",
  "summary": "Record notification to an external authority",
  "permission": "INCIDENT_MANAGE",
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
  "responds": "Incident"
 },
 "recordNoSale": {
  "method": "POST",
  "path": "/shifts/{shiftId}/no-sale",
  "contract": "shift",
  "summary": "Open the drawer without a sale",
  "permission": "SHIFT_SUSPEND",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "NoSaleEvent"
 },
 "recordWorkOrderParts": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/parts",
  "contract": "maintenance",
  "summary": "Record parts consumed",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrderDetail"
 },
 "recordWorkOrderTime": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/time",
  "contract": "maintenance",
  "summary": "Start, pause or stop work",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
 },
 "rejectWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/reject",
  "contract": "maintenance",
  "summary": "The assignee declines, with a reason",
  "permission": "MAINTENANCE_EXECUTE",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkOrder"
 },
 "reopenShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/reopen",
  "contract": "shift",
  "summary": "Reopen a shift closed in error",
  "permission": "SHIFT_REOPEN",
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
  "responds": "Shift"
 },
 "reportIncident": {
  "method": "POST",
  "path": "/incidents",
  "contract": "maintenance",
  "summary": "Report an incident",
  "permission": "INCIDENT_REPORT",
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
  "requestBody": "ReportIncidentRequest",
  "responds": "Incident"
 },
 "resumeShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/resume",
  "contract": "shift",
  "summary": "Resume a suspended shift",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Shift"
 },
 "resumeWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/resume",
  "contract": "maintenance",
  "summary": "Back to work",
  "permission": "MAINTENANCE_EXECUTE",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkOrder"
 },
 "selectRole": {
  "method": "POST",
  "path": "/auth/select-role",
  "contract": "identity",
  "summary": "Choose a role for a multi-role session",
  "permission": null,
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
  "responds": "Session"
 },
 "startWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/start",
  "contract": "maintenance",
  "summary": "Work has begun",
  "permission": "MAINTENANCE_EXECUTE",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkOrder"
 },
 "suspendShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/suspend",
  "contract": "shift",
  "summary": "Suspend a shift so another user can log in",
  "permission": "SHIFT_SUSPEND",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Shift"
 },
 "syncScans": {
  "method": "POST",
  "path": "/access/scans",
  "contract": "access",
  "summary": "Replay scans recorded offline",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "ScanSyncResult"
 },
 "updateIncident": {
  "method": "PATCH",
  "path": "/incidents/{incidentId}",
  "contract": "maintenance",
  "summary": "Investigate, escalate or close an incident",
  "permission": "INCIDENT_MANAGE",
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
  "responds": "Incident"
 },
 "updateWorkOrder": {
  "method": "PATCH",
  "path": "/work-orders/{workOrderId}",
  "contract": "maintenance",
  "summary": "Assign, reprioritise or amend",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
 },
 "validateAccess": {
  "method": "POST",
  "path": "/access/validate",
  "contract": "access",
  "summary": "Validate media at an access point and admit or deny",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ValidateRequest",
  "responds": "ValidationResult"
 },
 "validateGroupAccess": {
  "method": "POST",
  "path": "/access/group-validate",
  "contract": "access",
  "summary": "Admit a group on one read",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ValidationResult"
 },
 "verifyWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/verify",
  "contract": "maintenance",
  "summary": "Supervisor verification",
  "permission": "WORK_ORDER_VERIFY",
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
  "responds": "WorkOrder"
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
 "CashMovement": {
  "x-ticvai-persistence": "orders.cash_movement",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateCashMovementRequest"
   },
   {
    "type": "object",
    "required": [
     "shiftId",
     "authorisedByPrincipalId",
     "sequence"
    ],
    "properties": {
     "shiftId": {
      "type": "string"
     },
     "authorisedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "description": "The principal who authorised the movement, recorded for audit."
     },
     "sequence": {
      "type": "integer",
      "description": "Monotonic within the shift. Preserves order across an offline batch."
     },
     "syncedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "CashMovementKind": {
  "type": "string",
  "enum": [
   "openingFloat",
   "lift",
   "add"
  ]
 },
 "CloseShiftRequest": {
  "type": "object",
  "required": [
   "countedCash",
   "recordedAt"
  ],
  "properties": {
   "countedCash": {
    "$ref": "#/components/schemas/DenominationCount"
   },
   "nonCashDeclared": {
    "type": "array",
    "description": "Declared totals per non-cash tender, for reconciliation against captured payments.\n",
    "items": {
     "type": "object",
     "required": [
      "tender",
      "amount"
     ],
     "properties": {
      "tender": {
       "type": "string"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "notes": {
    "type": "string",
    "maxLength": 1000
   },
   "releaseHeldLeases": {
    "type": "boolean",
    "default": true,
    "description": "Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateCashMovementRequest": {
  "type": "object",
  "required": [
   "id",
   "kind",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID."
   },
   "kind": {
    "$ref": "#/components/schemas/CashMovementKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "denominations": {
    "$ref": "#/components/schemas/DenominationCount"
   },
   "reference": {
    "type": "string",
    "maxLength": 64,
    "description": "Safe drop reference or bag number."
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateWorkOrderRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "title",
   "venueId",
   "priority",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "title": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 5000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderKind"
     }
    ],
    "default": "corrective"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "attachmentRefs": {
    "type": "array",
    "description": "Photo-first. Expected at creation, not added later from memory.",
    "items": {
     "type": "string"
    }
   },
   "takeAssetOutOfService": {
    "type": "boolean",
    "default": false,
    "description": "Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DenominationCount": {
  "type": "array",
  "description": "**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n",
  "items": {
   "$ref": "#/components/schemas/CashCountLine"
  },
  "minItems": 1
 },
 "DenyReason": {
  "type": "string",
  "description": "Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n",
  "enum": [
   "notFound",
   "notYetValid",
   "expired",
   "alreadyUsed",
   "reentryLimitReached",
   "exitRequiredBeforeReentry",
   "wrongAccessPoint",
   "wrongPerformance",
   "outsideAdmissionWindow",
   "entitlementSuspended",
   "blacklisted",
   "capacityReached",
   "waiverRequired",
   "accompanimentRequired",
   "mediaDeactivated",
   "unpaid",
   "delegatedRightExhausted",
   "delegatedRightRevoked"
  ]
 },
 "Direction": {
  "type": "string",
  "enum": [
   "entry",
   "exit",
   "reentry",
   "crossover"
  ]
 },
 "GuestSession": {
  "x-ticvai-persistence": "none — Redis session registry",
  "type": "object",
  "required": [
   "subjectId",
   "tokens",
   "isVerified",
   "expiresAt"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "tokens": {
    "$ref": "#/components/schemas/TokenPair"
   },
   "isVerified": {
    "type": "boolean",
    "description": "False until an OTP or a verified provider identity confirms ownership. An unverified account may browse but not transact.\n"
   },
   "identityProviders": {
    "type": "array",
    "description": "Linked providers. Several may resolve to one account.",
    "items": {
     "type": "string",
     "enum": [
      "password",
      "otp",
      "apple",
      "google",
      "uaePass"
     ]
    }
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells (ADR-0010)."
   },
   "homeCellName": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Longer lived than a staff session. No single-session rule — a guest may be signed in on a phone and a laptop at once.\n"
   }
  }
 },
 "Incident": {
  "x-ticvai-persistence": "maintenance.incident",
  "type": "object",
  "required": [
   "id",
   "incidentNumber",
   "kind",
   "severity",
   "status",
   "venueId",
   "occurredAt",
   "reportedByPrincipalId"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "incidentNumber": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/IncidentKind"
   },
   "severity": {
    "$ref": "#/components/schemas/IncidentSeverity"
   },
   "status": {
    "$ref": "#/components/schemas/IncidentStatus"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationDescription": {
    "type": "string",
    "nullable": true
   },
   "isReportable": {
    "type": "boolean",
    "description": "Requires notification to an external authority within a statutory window."
   },
   "notificationDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reportedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "correctiveWorkOrderId": {
    "type": "string",
    "nullable": true
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "IncidentDetail": {
  "x-ticvai-persistence": "maintenance.incident",
  "allOf": [
   {
    "$ref": "#/components/schemas/Incident"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string",
      "description": "The original report. Never edited — investigation adds to the record."
     },
     "investigationNote": {
      "type": "string",
      "nullable": true
     },
     "rootCause": {
      "type": "string",
      "nullable": true
     },
     "correctiveActions": {
      "type": "string",
      "nullable": true
     },
     "firstAidGiven": {
      "type": "boolean"
     },
     "emergencyServicesCalled": {
      "type": "boolean"
     },
     "witnessCount": {
      "type": "integer"
     },
     "attachmentRefs": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "authorityNotifications": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "authority": {
         "type": "string"
        },
        "reference": {
         "type": "string",
         "nullable": true
        },
        "notifiedAt": {
         "type": "string",
         "format": "date-time"
        },
        "notifiedByPrincipalId": {
         "type": "string",
         "format": "uuid"
        }
       }
      }
     }
    }
   }
  ]
 },
 "IncidentKind": {
  "type": "string",
  "enum": [
   "guestInjury",
   "staffInjury",
   "nearMiss",
   "propertyDamage",
   "equipmentFailure",
   "securityIncident",
   "fireOrEvacuation",
   "foodSafety",
   "environmental",
   "other"
  ]
 },
 "IncidentSeverity": {
  "type": "string",
  "enum": [
   "nearMiss",
   "minor",
   "moderate",
   "major",
   "critical"
  ]
 },
 "IncidentStatus": {
  "type": "string",
  "enum": [
   "reported",
   "underInvestigation",
   "actionRequired",
   "closed"
  ]
 },
 "LoginRequest": {
  "type": "object",
  "required": [
   "username",
   "credential",
   "workstationId"
  ],
  "properties": {
   "username": {
    "type": "string",
    "maxLength": 256
   },
   "credential": {
    "type": "string",
    "description": "Password, PIN, card token or RFID token depending on `method`.\n",
    "maxLength": 512
   },
   "method": {
    "type": "string",
    "description": "**`pin` is how a till is actually used.** A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets shortened, shared or written on the drawer. The employee number goes in `username` and the PIN in `credential`, so the shape of the request does not change — only what the operator types.\n\n**A PIN is weaker than a password and the difference is bounded by the device, not by the secret.** `workstationId` is required on every login and is *NOT a permission source*: it says which till, and the till is on a venue network in a staff area. A PIN is a reasonable credential there and nowhere else, which is why this is an enum value and not a policy flag — a surface that wants it has to ask for it by name.\n\nAdded 10 September 2026 for `POS-000 Sign In`.\n",
    "enum": [
     "password",
     "pin",
     "card",
     "rfid",
     "sso"
    ],
    "default": "password"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "description": "Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. NOT a permission source.\n"
   },
   "deviceFingerprint": {
    "type": "string",
    "maxLength": 256
   }
  }
 },
 "LoginResponse": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/TokenPair"
   },
   {
    "type": "object",
    "required": [
     "requiresRoleSelection"
    ],
    "properties": {
     "requiresRoleSelection": {
      "type": "boolean"
     },
     "availableRoles": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/RoleSummary"
      }
     },
     "session": {
      "$ref": "#/components/schemas/Session"
     }
    }
   }
  ]
 },
 "MediaKind": {
  "type": "string",
  "enum": [
   "image",
   "video",
   "audio",
   "document",
   "vector",
   "font",
   "archive"
  ]
 },
 "MfaKind": {
  "type": "string",
  "enum": [
   "totp",
   "smsOtp",
   "emailOtp",
   "biometric",
   "hardwareToken"
  ]
 },
 "MfaMethod": {
  "x-ticvai-persistence": "identity.mfa_method",
  "type": "object",
  "required": [
   "id",
   "kind",
   "isActive",
   "enrolledAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MfaKind"
   },
   "label": {
    "type": "string",
    "nullable": true
   },
   "maskedTarget": {
    "type": "string",
    "nullable": true,
    "description": "Partially masked destination, so a person can tell two methods apart."
   },
   "isActive": {
    "type": "boolean"
   },
   "isPrimary": {
    "type": "boolean"
   },
   "enrolledAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "NoSaleEvent": {
  "type": "object",
  "x-ticvai-persistence": "orders.no_sale_event",
  "required": [
   "id",
   "shiftId",
   "reason",
   "principalId",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "shiftId": {
    "type": "string"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "reason": {
    "type": "string"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "countThisShift": {
    "type": "integer",
    "description": "Running count. Returned so the terminal can show it — a cashier who can see they are on their ninth no-sale behaves differently from one who cannot.\n"
   }
  }
 },
 "OfflinePackage": {
  "x-ticvai-persistence": "none — generated artefact in object storage",
  "type": "object",
  "required": [
   "etag",
   "generatedAt",
   "validFrom",
   "validTo",
   "accessPointId",
   "entitlements"
  ],
  "properties": {
   "etag": {
    "type": "string"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "entitlements": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "ticketId",
      "mediaCodes",
      "validFrom",
      "validTo",
      "entriesAllowed",
      "reentryAllowed"
     ],
     "properties": {
      "ticketId": {
       "type": "string"
      },
      "mediaCodes": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "A ticket may carry several media over its life."
      },
      "validFrom": {
       "type": "string",
       "format": "date-time"
      },
      "validTo": {
       "type": "string",
       "format": "date-time"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "entriesUsed": {
       "type": "integer"
      },
      "reentryAllowed": {
       "type": "boolean"
      },
      "admissionRulesId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "delegatedRights": {
    "type": "array",
    "description": "Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n",
    "items": {
     "type": "object",
     "required": [
      "rightId",
      "ticketId",
      "issuingCellId",
      "validFrom",
      "validTo",
      "entriesAllowed",
      "entriesConsumed"
     ],
     "properties": {
      "rightId": {
       "type": "string"
      },
      "ticketId": {
       "type": "string"
      },
      "issuingCellId": {
       "type": "string"
      },
      "guestLinkId": {
       "type": "string",
       "nullable": true
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
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "entriesConsumed": {
       "type": "integer"
      },
      "admissionRulesId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "blacklist": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media codes to deny outright regardless of entitlement state."
   },
   "admissionRules": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "openMinutesBefore",
      "closeMinutesAfter"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "openMinutesBefore": {
       "type": "integer"
      },
      "closeMinutesAfter": {
       "type": "integer"
      },
      "maxDurationMinutes": {
       "type": "integer",
       "nullable": true
      },
      "requiresExitBeforeReentry": {
       "type": "boolean"
      }
     }
    }
   }
  }
 },
 "OpenShiftRequest": {
  "type": "object",
  "required": [
   "workstationId",
   "openingFloat"
  ],
  "properties": {
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "openingFloat": {
    "$ref": "#/components/schemas/DenominationCount"
   },
   "depositBoxCode": {
    "type": "string",
    "maxLength": 64,
    "description": "Physical container assigned to this shift. Required where the venue configures deposit box allocation.\n"
   },
   "bagNumber": {
    "type": "string",
    "maxLength": 64,
    "description": "Required where the venue configures bag numbers as mandatory."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the device recorded it. Differs from server receipt time for shifts opened offline.\n"
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
 "ReportIncidentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "kind",
   "severity",
   "venueId",
   "description",
   "occurredAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "kind": {
    "$ref": "#/components/schemas/IncidentKind"
   },
   "severity": {
    "$ref": "#/components/schemas/IncidentSeverity"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "description": {
    "type": "string",
    "minLength": 3,
    "maxLength": 10000
   },
   "involvedSubjectIds": {
    "type": "array",
    "description": "Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "involvedStaffPrincipalIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "witnessCount": {
    "type": "integer"
   },
   "firstAidGiven": {
    "type": "boolean",
    "default": false
   },
   "emergencyServicesCalled": {
    "type": "boolean",
    "default": false
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ResolutionCode": {
  "type": "string",
  "enum": [
   "repaired",
   "partReplaced",
   "adjusted",
   "cleaned",
   "noFaultFound",
   "referredExternal",
   "replaced",
   "deferred"
  ]
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
 "ScanOutcome": {
  "type": "string",
  "enum": [
   "admitted",
   "denied",
   "overridden"
  ]
 },
 "ScanSyncResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "accepted",
   "results"
  ],
  "properties": {
   "accepted": {
    "type": "integer",
    "description": "Entries processed before any stop."
   },
   "stoppedAtSequence": {
    "type": "integer",
    "nullable": true,
    "description": "Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"
   },
   "results": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "sequence",
      "status"
     ],
     "properties": {
      "id": {
       "type": "string"
      },
      "sequence": {
       "type": "integer"
      },
      "status": {
       "type": "string",
       "enum": [
        "accepted",
        "duplicate",
        "reconciled",
        "rejected"
       ]
      },
      "serverOutcome": {
       "$ref": "#/components/schemas/ScanOutcome"
      },
      "divergence": {
       "type": "string",
       "nullable": true,
       "description": "Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"
      },
      "error": {
       "$ref": "../shared/common.yaml#/components/schemas/Problem"
      }
     }
    }
   }
  }
 },
 "Session": {
  "type": "object",
  "required": [
   "sessionId",
   "principalId",
   "roleId",
   "scope",
   "effectivePermissions",
   "saleBoardId"
  ],
  "properties": {
   "sessionId": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "roleId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "scope": {
    "type": "array",
    "description": "Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/ScopeRef"
    }
   },
   "effectivePermissions": {
    "allOf": [
     {
      "$ref": "../shared/permissions.yaml#/components/schemas/PermissionSet"
     }
    ],
    "description": "Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"
   },
   "permissionsByScope": {
    "type": "array",
    "description": "Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/ScopedPermissions"
    }
   },
   "saleBoardId": {
    "type": "string",
    "format": "uuid",
    "description": "Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n"
   },
   "workstation": {
    "$ref": "#/components/schemas/WorkstationContext"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Shift": {
  "x-ticvai-persistence": "orders.shift",
  "type": "object",
  "required": [
   "id",
   "workstationId",
   "venueId",
   "scopePath",
   "principalId",
   "status",
   "currency",
   "currencyScale",
   "openedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "Who opened it. Cash reconciles to a person and a drawer."
   },
   "principalDisplayName": {
    "type": "string"
   },
   "incidents": {
    "type": "array",
    "description": "BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "noSale",
        "drawerOpen",
        "override",
        "voidAfterPayment",
        "guestDispute",
        "tillJam",
        "priceQuery",
        "other"
       ]
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "note": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "status": {
    "$ref": "#/components/schemas/ShiftStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "depositBoxCode": {
    "type": "string",
    "nullable": true
   },
   "bagNumber": {
    "type": "string",
    "nullable": true
   },
   "openingFloat": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "salesTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundsTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "liftsTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "heldLeaseCount": {
    "type": "integer",
    "description": "Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the device recorded the open. Differs from `openedAt` when offline."
   },
   "suspendedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null while the shift has unsynced operations."
   },
   "approvals": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "principalId",
      "at"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "open",
        "close",
        "variance"
       ]
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "ShiftCloseResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "shift",
   "expectedCash",
   "countedCash",
   "variance",
   "requiresAcceptance"
  ],
  "properties": {
   "shift": {
    "$ref": "#/components/schemas/Shift"
   },
   "expectedCash": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "countedCash": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Counted minus expected. Negative is short."
   },
   "requiresAcceptance": {
    "type": "boolean",
    "description": "True when the variance exceeds the configured threshold."
   },
   "nonCashVariances": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "tender",
      "declared",
      "captured",
      "variance"
     ],
     "properties": {
      "tender": {
       "type": "string"
      },
      "declared": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "captured": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "variance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "ShiftStatus": {
  "type": "string",
  "enum": [
   "pendingApproval",
   "open",
   "suspended",
   "pendingVariance",
   "pendingClosure",
   "closed",
   "autoClosed"
  ]
 },
 "SsoProtocol": {
  "type": "string",
  "enum": [
   "oidc",
   "saml2"
  ]
 },
 "SsoProvider": {
  "x-ticvai-persistence": "identity.sso_provider",
  "type": "object",
  "required": [
   "id",
   "displayName",
   "protocol"
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
   "iconAssetRef": {
    "type": "string",
    "nullable": true
   },
   "isEnforced": {
    "type": "boolean",
    "description": "True disables password login for principals covered by this provider."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "TicketStatus": {
  "x-ticvai-persistence": "none — computed from entitlement and scans",
  "description": "**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n",
  "type": "object",
  "required": [
   "ticketId",
   "isValid"
  ],
  "properties": {
   "ticketId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Stable for the life of the ticket, independent of the media carrying it."
   },
   "mediaCode": {
    "type": "string",
    "nullable": true
   },
   "productName": {
    "type": "string"
   },
   "holderName": {
    "type": "string",
    "nullable": true,
    "description": "Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"
   },
   "isValid": {
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
    "nullable": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "entriesUsed": {
    "type": "integer"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true,
    "description": "Null means unlimited."
   },
   "reentryAllowed": {
    "type": "boolean"
   },
   "isInsideVenue": {
    "type": "boolean",
    "description": "Derived from the last scan. Drives anti-passback evaluation."
   },
   "issuingCellId": {
    "type": "string",
    "nullable": true,
    "description": "Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   }
  }
 },
 "TokenPair": {
  "x-ticvai-persistence": "none — transient",
  "type": "object",
  "required": [
   "accessToken",
   "refreshToken",
   "expiresIn"
  ],
  "properties": {
   "accessToken": {
    "type": "string",
    "description": "JWT carrying `sid`, validated per request against the session registry."
   },
   "refreshToken": {
    "type": "string"
   },
   "expiresIn": {
    "type": "integer",
    "description": "Seconds"
   }
  }
 },
 "ValidateRequest": {
  "type": "object",
  "required": [
   "id",
   "mediaCode",
   "mediaKind",
   "direction",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key and dedupe key."
   },
   "mediaCode": {
    "type": "string",
    "maxLength": 256,
    "description": "What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"
   },
   "mediaKind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "groupSize": {
    "type": "integer",
    "minimum": 1,
    "description": "For group media admitting several holders on one read."
   },
   "proximityToken": {
    "type": "string",
    "description": "BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time of the read. Authoritative for ordering, not for validity."
   }
  }
 },
 "ValidationResult": {
  "x-ticvai-persistence": "none — computed, persisted as scan_event",
  "type": "object",
  "required": [
   "scanId",
   "outcome",
   "accessPointId",
   "recordedAt"
  ],
  "properties": {
   "scanId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "outcome": {
    "$ref": "#/components/schemas/ScanOutcome"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   },
   "denyDetail": {
    "type": "string",
    "description": "Human-readable, localised. For operator display, never for logic."
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "ticket": {
    "$ref": "#/components/schemas/TicketStatus"
   },
   "admittedCount": {
    "type": "integer",
    "description": "Holders admitted on this read. Differs from groupSize on partial admission."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "serverEvaluatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
  "type": "object",
  "required": [
   "id",
   "workOrderNumber",
   "title",
   "venueId",
   "status",
   "priority",
   "kind",
   "createdAt"
  ],
  "properties": {
   "downtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n"
   },
   "rootCause": {
    "type": "string",
    "nullable": true,
    "enum": [
     "wearAndTear",
     "operatorError",
     "guestDamage",
     "manufacturingDefect",
     "environmental",
     "softwareFault",
     "powerFailure",
     "deferredMaintenance",
     "unknown"
    ],
    "description": "**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"
   },
   "rootCauseNote": {
    "type": "string",
    "nullable": true
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "escalationLevel": {
    "type": "integer",
    "default": 0,
    "description": "**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"
   },
   "id": {
    "type": "string"
   },
   "workOrderNumber": {
    "type": "string"
   },
   "title": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetName": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "kind": {
    "$ref": "#/components/schemas/WorkOrderKind"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "elapsedMinutes": {
    "type": "integer"
   },
   "isTimerRunning": {
    "type": "boolean"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean"
   },
   "requiresVerification": {
    "type": "boolean"
   },
   "sourcePlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceInspectionId": {
    "type": "string",
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkOrderAttachment": {
  "type": "object",
  "x-ticvai-persistence": "maintenance.work_order_attachment",
  "required": [
   "id",
   "workOrderId",
   "kind",
   "capturedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "workOrderId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "photo",
     "video",
     "document",
     "note",
     "signature"
    ]
   },
   "assetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "text": {
    "type": "string",
    "nullable": true
   },
   "stage": {
    "type": "string",
    "enum": [
     "before",
     "during",
     "after",
     "signOff"
    ],
    "nullable": true
   },
   "capturedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "capturedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time. **Distinct from when it synced** — a photo taken at 09:14 in a basement and uploaded at 11:40 is evidence of the first, not the second.\n"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkOrderDetail": {
  "x-ticvai-persistence": "maintenance.work_order",
  "allOf": [
   {
    "$ref": "#/components/schemas/WorkOrder"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string",
      "nullable": true
     },
     "resolution": {
      "type": "string",
      "nullable": true
     },
     "resolutionCode": {
      "$ref": "#/components/schemas/ResolutionCode"
     },
     "attachmentRefs": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "timeEntries": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "action": {
         "type": "string"
        },
        "principalId": {
         "type": "string",
         "format": "uuid"
        },
        "pauseReason": {
         "type": "string",
         "nullable": true
        },
        "recordedAt": {
         "type": "string",
         "format": "date-time"
        }
       }
      }
     },
     "parts": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "inventoryItemId": {
         "type": "string",
         "format": "uuid"
        },
        "itemName": {
         "type": "string"
        },
        "quantity": {
         "type": "number"
        },
        "cost": {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       }
      }
     },
     "labourCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "partsCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "totalCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "verifiedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   }
  ]
 },
 "WorkOrderKind": {
  "type": "string",
  "enum": [
   "corrective",
   "planned",
   "inspectionFollowUp",
   "incidentCorrective",
   "improvement"
  ]
 },
 "WorkOrderPriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent",
   "emergency"
  ]
 },
 "WorkOrderStatus": {
  "type": "string",
  "enum": [
   "open",
   "assigned",
   "inProgress",
   "paused",
   "awaitingParts",
   "completed",
   "verified",
   "closed",
   "cancelled"
  ]
 },
 "WorkstationContext": {
  "type": "object",
  "required": [
   "id",
   "code",
   "venueId",
   "regionId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "description": "Inherited from the workstation, never selected by the operator."
   },
   "devices": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "driver"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "receiptPrinter",
        "ticketPrinter",
        "cashDrawer",
        "barcodeScanner",
        "rfidReader",
        "paymentTerminal",
        "customerDisplay"
       ]
      },
      "driver": {
       "type": "string"
      },
      "identifier": {
       "type": "string"
      }
     }
    }
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4
   },
   "timezone": {
    "type": "string"
   },
   "cellName": {
    "type": "string",
    "description": "The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"
   },
   "deploymentProfile": {
    "type": "string",
    "enum": [
     "terminalLocal",
     "venueEdge",
     "thin"
    ],
    "description": "Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"
   }
  }
 }
}
```
