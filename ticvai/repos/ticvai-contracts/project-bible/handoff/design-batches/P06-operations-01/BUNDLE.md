# P06-operations-01 — P06 · Operations (1 of 5)

**10 screens · 57 operations · 62 schemas · 26 permissions**

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

- **Every control that can be refused must be gated.** 26 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, ANNOUNCEMENT_PUBLISH, CASH_LIFT, CASH_NO_SALE, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, MAINTENANCE_APPROVE, MAINTENANCE_EXECUTE, OVERSHORT_ACCEPT, PROCUREMENT_REQUEST`…. A control nobody can use must say so,
  not sit enabled and fail.
- **28 of these operations work offline**: acceptWorkOrder, acknowledgeAnnouncement, attachWorkOrderEvidence, completeWorkOrder, createCashMovement, createWorkOrder, getCurrentSession, getCurrentShift
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-001` | Sign in | listDetail | 6 | 1 | — |
| `EMP-002` | Select venue & role | listDetail | 5 | 1 | — |
| `EMP-003` | Home — on duty | approvalInbox | 17 | 11 | — |
| `EMP-009` | End shift | approvalInbox | 13 | 9 | — |
| `EMP-010` | Scan — ready | listDetail | 8 | 4 | — |
| `EMP-004` | Task list | listDetail | 15 | 11 | — |
| `EMP-005` | Task detail | listDetail | 18 | 11 | — |
| `EMP-006` | Raise a task | listDetail | 16 | 12 | — |
| `EMP-007` | Handover notes | listDetail | 4 | 1 | — |
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
    "operation": "listSsoProviders",
    "why": "**1 declared operation reaches no component on this screen**: listSsoProviders. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every MFA method",
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
      },
      {
       "kind": "dataTable",
       "label": "Every SSO provider",
       "bindsTo": "SsoProvider",
       "columns": [
        "SsoProvider.id",
        "SsoProvider.displayName",
        "SsoProvider.protocol",
        "SsoProvider.iconAssetRef",
        "SsoProvider.isEnforced",
        "SsoProvider.scopePath"
       ],
       "operation": "listSsoProviders",
       "provenance": "contract identity.yaml GET /auth/sso/providers"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected MFA method",
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
      },
      {
       "kind": "detailPanel",
       "label": "The session",
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
      },
      {
       "kind": "textField",
       "label": "Authentication code",
       "operation": "verifyMfaChallenge",
       "provenance": "contract identity.yaml POST /auth/mfa/challenge/{challengeId}/verify",
       "notes": "Shown only in the mfaRequired state (audit R135)."
      },
      {
       "kind": "primaryButton",
       "label": "Verify",
       "operation": "verifyMfaChallenge",
       "provenance": "contract identity.yaml POST /auth/mfa/challenge/{challengeId}/verify"
      },
      {
       "kind": "secondaryButton",
       "label": "Email me a code instead",
       "operation": "createMfaChallenge",
       "provenance": "contract identity.yaml POST /auth/mfa/challenge",
       "notes": "The fallback -- issues the challenge against the principal's email (`emailOtp`) method (audit R126 (5))."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sign list.",
   "error": "Could not load. Names which read failed and leaves the sign untouched.",
   "emptyFirstRun": "No sign yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listMfaMethods` takes no filter, so an empty list is always the first-run state above.",
   "mfaRequired": "**Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any platform-staff permission, or one the tenant added), so after `login` the screen calls `createMfaChallenge` and asks for the authenticator code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says so. A principal with no enrolled method is sent to enrol first (decided 28 September, audit R135, R126).",
   "offline": "Signs in against the cached principal list. A technician in a basement still needs their tasks"
  },
  "apis": [
   {
    "operationId": "login",
    "contract": "identity",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "getCurrentSession",
    "contract": "identity",
    "purpose": "Current session and effective permissions",
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
    "operationId": "createMfaChallenge",
    "contract": "identity",
    "purpose": "Second factor after login when the principal holds a permission in mfaRequiredForPermissions; action `signIn`, the primary method (authenticator app), or the email method as the fallback (decided 28 September, audit R135, R126 (5))",
    "trigger": "onAction"
   },
   {
    "operationId": "verifyMfaChallenge",
    "contract": "identity",
    "purpose": "Completes sign-in with the code; the session is usable only after it. Five wrong codes lock step-up (audit R126 (6))",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "challengeId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "MfaMethod.id",
    "MfaMethod.kind",
    "MfaMethod.label",
    "MfaMethod.maskedTarget",
    "MfaMethod.isActive"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-001"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formLogin",
    "component": "modal",
    "trigger": "Login",
    "body": "**Collects what `login` sends before it is called.** Required: `username`, `credential`, `workstationId`. Optional: `method`, `deviceFingerprint`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "LoginRequest",
    "confirm": {
     "label": "Login",
     "operation": "login"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "username",
      "credential",
      "workstationId",
      "method",
      "deviceFingerprint"
     ]
    },
    "provenance": "contract identity.yaml POST /auth/login"
   }
  ],
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
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-002 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-002 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRole, forceLogout, listActiveSessions, revokeAllSessions. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.** ** restored** — a role-select screen must read the roles. Over-stripped and caught by F08.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listMfaMethods` reads the population and `getCurrentSession` reads one of them — list, select, act",
  "purpose": "Confirm which hat this person is wearing today.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every MFA method",
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
      },
      {
       "kind": "dataTable",
       "label": "Every SSO provider",
       "bindsTo": "SsoProvider",
       "columns": [
        "SsoProvider.id",
        "SsoProvider.displayName",
        "SsoProvider.protocol",
        "SsoProvider.iconAssetRef",
        "SsoProvider.isEnforced",
        "SsoProvider.scopePath"
       ],
       "operation": "listSsoProviders",
       "provenance": "contract identity.yaml GET /auth/sso/providers"
      },
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
       "label": "The selected MFA method",
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
      },
      {
       "kind": "detailPanel",
       "label": "The session",
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
       "label": "Select role",
       "operation": "selectRole",
       "provenance": "contract identity.yaml POST /auth/select-role"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The select venue role list.",
   "error": "Could not load. Names which read failed and leaves the select venue role untouched.",
   "emptyFirstRun": "No select venue role yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listMfaMethods` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached from the last session"
  },
  "apis": [
   {
    "operationId": "selectRole",
    "contract": "identity",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "getCurrentSession",
    "contract": "identity",
    "purpose": "Current session and effective permissions",
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
    "MfaMethod.id",
    "MfaMethod.kind",
    "MfaMethod.label",
    "MfaMethod.maskedTarget",
    "MfaMethod.isActive"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-002"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSelectRole",
    "component": "modal",
    "trigger": "Select role",
    "body": "**Collects what `selectRole` sends before it is called.** Required: `roleId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Select role",
     "operation": "selectRole"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "roleId"
     ]
    },
    "provenance": "contract identity.yaml POST /auth/select-role"
   }
  ],
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
    "EMP-006",
    "EMP-008",
    "EMP-010",
    "EMP-014",
    "EMP-017",
    "EMP-019",
    "EMP-021",
    "EMP-022",
    "EMP-024",
    "EMP-025",
    "EMP-026",
    "EMP-028",
    "EMP-029",
    "EMP-030",
    "EMP-031",
    "EMP-033",
    "EMP-034",
    "EMP-037",
    "EMP-038",
    "EMP-039",
    "EMP-040",
    "EMP-042",
    "EMP-043",
    "EMP-046",
    "EMP-047",
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
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-003 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-003 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-051",
     "trigger": "Restaurant Service Command Center",
     "provenance": "derived — EMP-051 declares entryState.params outletId and EMP-003 holds none of them, so the edge carries nothing and EMP-051 opens cold"
    },
    {
     "to": "EMP-052",
     "trigger": "Floor Plan & Table Map",
     "provenance": "derived — EMP-052 declares entryState.params outletId and EMP-003 holds none of them, so the edge carries nothing and EMP-052 opens cold"
    },
    {
     "to": "EMP-053",
     "trigger": "Table & Seating Configuration",
     "provenance": "derived — EMP-053 declares entryState.params outletId, tableId and EMP-003 holds none of them, so the edge carries nothing and EMP-053 opens cold"
    },
    {
     "to": "EMP-054",
     "trigger": "Reservation Calendar & Timeline",
     "provenance": "derived — EMP-054 declares entryState.params  and EMP-003 holds none of them, so the edge carries nothing and EMP-054 opens cold"
    },
    {
     "to": "EMP-055",
     "trigger": "Create / Edit Reservation",
     "provenance": "derived — EMP-055 declares entryState.params  and EMP-003 holds none of them, so the edge carries nothing and EMP-055 opens cold"
    },
    {
     "to": "EMP-056",
     "trigger": "Walk-In & Waitlist Management",
     "provenance": "derived — EMP-056 declares entryState.params entryId and EMP-003 holds none of them, so the edge carries nothing and EMP-056 opens cold"
    },
    {
     "to": "EMP-057",
     "trigger": "Guest Profile & Dining History",
     "provenance": "derived — EMP-057 declares entryState.params subjectId and EMP-003 holds none of them, so the edge carries nothing and EMP-057 opens cold"
    },
    {
     "to": "EMP-058",
     "trigger": "Live Table & Service Management",
     "provenance": "derived — EMP-058 declares entryState.params entryId, reservationId, ticketId, visitId and EMP-003 holds none of them, so the edge carries nothing and EMP-058 opens cold"
    },
    {
     "to": "EMP-059",
     "trigger": "Table Order, Bill & Payment Management",
     "provenance": "derived — EMP-059 declares entryState.params visitId and EMP-003 holds none of them, so the edge carries nothing and EMP-059 opens cold"
    },
    {
     "to": "EMP-060",
     "trigger": "Reservation & Table Performance",
     "provenance": "derived — EMP-060 declares entryState.params outletId and EMP-003 holds none of them, so the edge carries nothing and EMP-060 opens cold"
    },
    {
     "to": "EMP-061",
     "trigger": "Retail Inventory Command Center",
     "provenance": "derived — EMP-061 declares entryState.params alertId, dashboardId and EMP-003 holds none of them, so the edge carries nothing and EMP-061 opens cold"
    },
    {
     "to": "EMP-062",
     "trigger": "Store Stock & SKU Availability",
     "provenance": "derived — EMP-062 declares entryState.params itemId and EMP-003 holds none of them, so the edge carries nothing and EMP-062 opens cold"
    },
    {
     "to": "EMP-063",
     "trigger": "Requisition & Smart Store Replenishment",
     "provenance": "derived — EMP-063 declares entryState.params  and EMP-003 holds none of them, so the edge carries nothing and EMP-063 opens cold"
    },
    {
     "to": "EMP-064",
     "trigger": "Store-to-Store & Warehouse Transfers",
     "provenance": "derived — EMP-064 declares entryState.params  and EMP-003 holds none of them, so the edge carries nothing and EMP-064 opens cold"
    },
    {
     "to": "EMP-065",
     "trigger": "Receiving & Store Put-Away",
     "provenance": "derived — EMP-065 declares entryState.params receiptId, transferId and EMP-003 holds none of them, so the edge carries nothing and EMP-065 opens cold"
    },
    {
     "to": "EMP-066",
     "trigger": "Stock Count & Cycle Count Management",
     "provenance": "derived — EMP-066 declares entryState.params countId and EMP-003 holds none of them, so the edge carries nothing and EMP-066 opens cold"
    },
    {
     "to": "EMP-067",
     "trigger": "Damage, Loss, Shrinkage & Stock Adjustment",
     "provenance": "derived — EMP-067 declares entryState.params actionId, outletId and EMP-003 holds none of them, so the edge carries nothing and EMP-067 opens cold"
    },
    {
     "to": "EMP-068",
     "trigger": "Reservation, Allocation & Omnichannel Inventory",
     "provenance": "derived — EMP-068 declares entryState.params outletId and EMP-003 holds none of them, so the edge carries nothing and EMP-068 opens cold"
    },
    {
     "to": "EMP-069",
     "trigger": "Barcode, RFID, Serialized Stock & Traceability",
     "provenance": "derived — EMP-069 declares entryState.params  and EMP-003 holds none of them, so the edge carries nothing and EMP-069 opens cold"
    },
    {
     "to": "EMP-070",
     "trigger": "Inventory Exceptions, AI Replenishment & Action Center",
     "provenance": "derived — EMP-070 declares entryState.params alertId and EMP-003 holds none of them, so the edge carries nothing and EMP-070 opens cold"
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
    },
    {
     "to": "EMP-006",
     "trigger": "Raise a task",
     "provenance": "derived — EMP-006 declares entryState.params workOrderId and EMP-003 holds none of them, so the edge carries nothing and EMP-006 opens cold"
    },
    {
     "to": "EMP-014",
     "trigger": "Ticket lookup",
     "provenance": "derived — EMP-014 declares entryState.params orderId and EMP-003 holds none of them, so the edge carries nothing and EMP-014 opens cold"
    },
    {
     "to": "EMP-019",
     "trigger": "AI assistant — home",
     "provenance": "derived — EMP-019 declares entryState.params conversationId and EMP-003 holds none of them, so the edge carries nothing and EMP-019 opens cold"
    },
    {
     "to": "EMP-021",
     "trigger": "Roster",
     "provenance": "derived — EMP-021 declares entryState.params assignmentId and EMP-003 holds none of them, so the edge carries nothing and EMP-021 opens cold"
    },
    {
     "to": "EMP-022",
     "trigger": "My rota",
     "provenance": "derived — EMP-022 declares entryState.params assignmentId and EMP-003 holds none of them, so the edge carries nothing and EMP-022 opens cold"
    },
    {
     "to": "EMP-024",
     "trigger": "Clock in / out",
     "provenance": "derived — EMP-024 declares entryState.params recordId and EMP-003 holds none of them, so the edge carries nothing and EMP-024 opens cold"
    },
    {
     "to": "EMP-025",
     "trigger": "Break management",
     "provenance": "derived — EMP-025 declares entryState.params recordId and EMP-003 holds none of them, so the edge carries nothing and EMP-025 opens cold"
    },
    {
     "to": "EMP-026",
     "trigger": "Incident report",
     "carries": [
      "incidentId"
     ],
     "provenance": "derived — EMP-026 declares entryState.params incidentId and EMP-003 holds incidentId, so an edge into it carries them"
    },
    {
     "to": "EMP-028",
     "trigger": "Lost & found",
     "provenance": "derived — EMP-028 declares entryState.params caseId and EMP-003 holds none of them, so the edge carries nothing and EMP-028 opens cold"
    },
    {
     "to": "EMP-029",
     "trigger": "Guest assistance",
     "carries": [
      "incidentId"
     ],
     "provenance": "derived — EMP-029 declares entryState.params caseId, incidentId and EMP-003 holds incidentId, so an edge into it carries them"
    },
    {
     "to": "EMP-030",
     "trigger": "Venue map",
     "provenance": "derived — EMP-030 declares entryState.params mapId and EMP-003 holds none of them, so the edge carries nothing and EMP-030 opens cold"
    },
    {
     "to": "EMP-031",
     "trigger": "Queue monitor",
     "provenance": "derived — EMP-031 declares entryState.params queueId and EMP-003 holds none of them, so the edge carries nothing and EMP-031 opens cold"
    },
    {
     "to": "EMP-033",
     "trigger": "Capacity view",
     "provenance": "derived — EMP-033 declares entryState.params channelCapacityId and EMP-003 holds none of them, so the edge carries nothing and EMP-033 opens cold"
    },
    {
     "to": "EMP-034",
     "trigger": "Walk-up sale",
     "provenance": "derived — EMP-034 declares entryState.params orderId, productId and EMP-003 holds none of them, so the edge carries nothing and EMP-034 opens cold"
    },
    {
     "to": "EMP-037",
     "trigger": "Notifications",
     "provenance": "derived — EMP-037 declares entryState.params announcementId, conversationId and EMP-003 holds none of them, so the edge carries nothing and EMP-037 opens cold"
    },
    {
     "to": "EMP-038",
     "trigger": "Broadcast to team",
     "provenance": "derived — EMP-038 declares entryState.params announcementId and EMP-003 holds none of them, so the edge carries nothing and EMP-038 opens cold"
    },
    {
     "to": "EMP-039",
     "trigger": "Announcements",
     "provenance": "derived — EMP-039 declares entryState.params announcementId and EMP-003 holds none of them, so the edge carries nothing and EMP-039 opens cold"
    },
    {
     "to": "EMP-047",
     "trigger": "Emergency mode",
     "provenance": "derived — EMP-047 declares entryState.params announcementId and EMP-003 holds none of them, so the edge carries nothing and EMP-047 opens cold"
    },
    {
     "to": "EMP-042",
     "trigger": "Profile",
     "provenance": "derived — EMP-042 declares entryState.params methodId and EMP-003 holds none of them, so the edge carries nothing and EMP-042 opens cold"
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "textField",
       "label": "Severity",
       "operation": "listIncidents",
       "notes": "Sends `?severity=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listIncidents",
       "notes": "Sends `?status=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "toggle",
       "label": "Is reportable",
       "operation": "listIncidents",
       "notes": "Sends `?isReportable=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every cash movement",
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
        "CashMovement.depositBoxId",
        "CashMovement.witnessPrincipalId",
        "CashMovement.withdrawalReason",
        "CashMovement.authorisedByPrincipalId"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "dataTable",
       "label": "Every shift",
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
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected incident",
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
        "Incident.assignedToPrincipalId",
        "Incident.reportedByPrincipalId",
        "Incident.correctiveWorkOrderId",
        "Incident.occurredAt",
        "Incident.recordedAt"
       ],
       "operation": "listIncidents",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "detailPanel",
       "label": "The incident",
       "bindsTo": "IncidentDetail",
       "columns": [
        "IncidentDetail.id",
        "IncidentDetail.incidentNumber",
        "IncidentDetail.kind",
        "IncidentDetail.severity",
        "IncidentDetail.status",
        "IncidentDetail.venueId",
        "IncidentDetail.assetId",
        "IncidentDetail.locationDescription",
        "IncidentDetail.isReportable",
        "IncidentDetail.notificationDueAt",
        "IncidentDetail.notifiedAt",
        "IncidentDetail.assignedToPrincipalId",
        "IncidentDetail.reportedByPrincipalId",
        "IncidentDetail.correctiveWorkOrderId",
        "IncidentDetail.occurredAt",
        "IncidentDetail.recordedAt"
       ],
       "operation": "getIncident",
       "provenance": "contract maintenance.yaml GET /incidents/{incidentId}"
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
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
       "operation": "getShift",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}"
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
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
       "label": "Accept shift variance",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve shift open",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "destructiveButton",
       "label": "Close shift",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Open shift",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record authority notification",
       "operation": "recordAuthorityNotification",
       "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
      },
      {
       "kind": "secondaryButton",
       "label": "Record no sale",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen shift",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Report incident",
       "operation": "reportIncident",
       "provenance": "contract maintenance.yaml POST /incidents"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume shift",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend shift",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      },
      {
       "kind": "secondaryButton",
       "label": "Save incident",
       "operation": "updateIncident",
       "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close shift",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A home duty this affects should be identified in the dialog, not just counted. **Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional: `nonCashDeclared`, `notes`, `releaseHeldLeases`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close",
    "bindsTo": "CloseShiftRequest"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend shift",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A home duty this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   },
   {
    "id": "formAcceptShiftVariance",
    "component": "modal",
    "trigger": "Accept shift variance",
    "body": "**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Accept shift variance",
     "operation": "acceptShiftVariance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
   },
   {
    "id": "formApproveShiftOpen",
    "component": "modal",
    "trigger": "Approve shift open",
    "body": "**Collects what `approveShiftOpen` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Approve shift open",
     "operation": "approveShiftOpen"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
   },
   {
    "id": "formOpenShift",
    "component": "modal",
    "trigger": "Open shift",
    "body": "**Collects what `openShift` sends before it is called.** Required: `workstationId`, `openingFloat`. Optional: `depositBoxCode`, `bagNumber`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "OpenShiftRequest",
    "confirm": {
     "label": "Open shift",
     "operation": "openShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "workstationId",
      "openingFloat",
      "depositBoxCode",
      "bagNumber",
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts"
   },
   {
    "id": "formRecordAuthorityNotification",
    "component": "modal",
    "trigger": "Record authority notification",
    "body": "**Collects what `recordAuthorityNotification` sends before it is called.** Required: `authority`, `notifiedAt`. Optional: `reference`, `notifiedByPrincipalId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record authority notification",
     "operation": "recordAuthorityNotification"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "authority",
      "notifiedAt",
      "reference",
      "notifiedByPrincipalId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
   },
   {
    "id": "formRecordNoSale",
    "component": "modal",
    "trigger": "Record no sale",
    "body": "**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record no sale",
     "operation": "recordNoSale"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
   },
   {
    "id": "formReopenShift",
    "component": "modal",
    "trigger": "Reopen shift",
    "body": "**Collects what `reopenShift` sends before it is called.** Required: `reason`, `supervisorStepUp` {`principalId`, `credential`}: the supervisor enters their staff PIN on this device, and may not be the principal who closed the shift. Refused 403 `approver-is-closer` or `supervisor-step-up-refused` (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen shift",
     "operation": "reopenShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "supervisorStepUp"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
   },
   {
    "id": "formReportIncident",
    "component": "modal",
    "trigger": "Report incident",
    "body": "**Collects what `reportIncident` sends before it is called.** Required: `id`, `kind`, `severity`, `venueId`, `description`, `occurredAt`, `recordedAt`. Optional: `assetId`, `locationDescription`, `involvedSubjectIds`, `involvedStaffPrincipalIds`, `witnessCount`, `firstAidGiven`, `emergencyServicesCalled`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ReportIncidentRequest",
    "confirm": {
     "label": "Report incident",
     "operation": "reportIncident"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "severity",
      "venueId",
      "description",
      "occurredAt",
      "recordedAt",
      "assetId",
      "locationDescription",
      "involvedSubjectIds",
      "involvedStaffPrincipalIds",
      "witnessCount",
      "firstAidGiven",
      "emergencyServicesCalled",
      "attachmentRefs"
     ]
    },
    "provenance": "contract maintenance.yaml POST /incidents"
   },
   {
    "id": "formResumeShift",
    "component": "modal",
    "trigger": "Resume shift",
    "body": "**Collects what `resumeShift` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resume shift",
     "operation": "resumeShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
   },
   {
    "id": "formUpdateIncident",
    "component": "modal",
    "trigger": "Save incident",
    "body": "**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save incident",
     "operation": "updateIncident"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "severity",
      "assignedToPrincipalId",
      "investigationNote",
      "rootCause",
      "correctiveActions",
      "correctiveWorkOrderId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
   }
  ],
  "states": {
   "loading": "The home duty list.",
   "error": "Could not load. Names which read failed and leaves the home duty untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Nothing matches the filter on severity, status, isReportable and the home duty are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onAction"
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
    "Incident.id",
    "Incident.incidentNumber",
    "Incident.kind",
    "Incident.severity",
    "Incident.status"
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
    "EMP-003",
    "EMP-049"
   ],
   "inferred": true,
   "entryFrom": [
    "EMP-017"
   ],
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-009 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-009 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-009 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "approvalInbox",
  "patternReason": "`approveShiftOpen` decides items that `listCashMovements` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Close out cleanly, including anything unsynced.",
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
      },
      {
       "kind": "dataTable",
       "label": "Every shift",
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
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cash movement",
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
        "CashMovement.depositBoxId",
        "CashMovement.witnessPrincipalId",
        "CashMovement.withdrawalReason",
        "CashMovement.authorisedByPrincipalId",
        "CashMovement.sequence",
        "CashMovement.syncedAt"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
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
       "operation": "getShift",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}"
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
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
       "label": "Close shift",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept shift variance",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve shift open",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "secondaryButton",
       "label": "Create cash movement",
       "operation": "createCashMovement",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Open shift",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record no sale",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen shift",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume shift",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend shift",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close shift",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A end shift this affects should be identified in the dialog, not just counted. **Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional: `nonCashDeclared`, `notes`, `releaseHeldLeases`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close",
    "bindsTo": "CloseShiftRequest"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend shift",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A end shift this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   },
   {
    "id": "formAcceptShiftVariance",
    "component": "modal",
    "trigger": "Accept shift variance",
    "body": "**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Accept shift variance",
     "operation": "acceptShiftVariance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
   },
   {
    "id": "formApproveShiftOpen",
    "component": "modal",
    "trigger": "Approve shift open",
    "body": "**Collects what `approveShiftOpen` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Approve shift open",
     "operation": "approveShiftOpen"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
   },
   {
    "id": "formCreateCashMovement",
    "component": "modal",
    "trigger": "Create cash movement",
    "body": "**Collects what `createCashMovement` sends before it is called.** Required: `id`, `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCashMovementRequest",
    "confirm": {
     "label": "Create cash movement",
     "operation": "createCashMovement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "amount",
      "recordedAt",
      "denominations",
      "reference",
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
   },
   {
    "id": "formOpenShift",
    "component": "modal",
    "trigger": "Open shift",
    "body": "**Collects what `openShift` sends before it is called.** Required: `workstationId`, `openingFloat`. Optional: `depositBoxCode`, `bagNumber`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "OpenShiftRequest",
    "confirm": {
     "label": "Open shift",
     "operation": "openShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "workstationId",
      "openingFloat",
      "depositBoxCode",
      "bagNumber",
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts"
   },
   {
    "id": "formRecordNoSale",
    "component": "modal",
    "trigger": "Record no sale",
    "body": "**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record no sale",
     "operation": "recordNoSale"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
   },
   {
    "id": "formReopenShift",
    "component": "modal",
    "trigger": "Reopen shift",
    "body": "**Collects what `reopenShift` sends before it is called.** Required: `reason`, `supervisorStepUp` {`principalId`, `credential`}: the supervisor enters their staff PIN on this device, and may not be the principal who closed the shift. Refused 403 `approver-is-closer` or `supervisor-step-up-refused` (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen shift",
     "operation": "reopenShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "supervisorStepUp"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
   },
   {
    "id": "formResumeShift",
    "component": "modal",
    "trigger": "Resume shift",
    "body": "**Collects what `resumeShift` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resume shift",
     "operation": "resumeShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
   }
  ],
  "states": {
   "loading": "The end shift list.",
   "error": "Could not load. Names which read failed and leaves the end shift untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Never shown: `listCashMovements` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Cannot close.** Closing needs the server total, and a locally computed variance is not a variance"
  },
  "apis": [
   {
    "operationId": "closeShift",
    "contract": "shift",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
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
    "CashMovement.id",
    "CashMovement.kind",
    "CashMovement.amount",
    "CashMovement.denominations",
    "CashMovement.reference"
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
    "EMP-003",
    "EMP-015"
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
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-010 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-010 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-010 holds none of them, so the edge carries nothing and EMP-003 opens cold"
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
       "kind": "textField",
       "label": "Access point id",
       "operation": "listScans",
       "notes": "Sends `?accessPointId=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "textField",
       "label": "Ticket id",
       "operation": "listScans",
       "notes": "Sends `?ticketId=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "textField",
       "label": "Outcome",
       "operation": "listScans",
       "notes": "Sends `?outcome=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "datePicker",
       "label": "Recorded from",
       "operation": "listScans",
       "notes": "Sends `?recordedFrom=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "datePicker",
       "label": "Recorded to",
       "operation": "listScans",
       "notes": "Sends `?recordedTo=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "dataTable",
       "label": "Every scan event",
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
        "ScanEvent.overridesScanId"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected scan event",
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
        "ScanEvent.overridesScanId",
        "ScanEvent.overrideReason",
        "ScanEvent.recordedAt",
        "ScanEvent.syncedAt"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "detailPanel",
       "label": "The offline package",
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
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup ticket",
       "operation": "lookupTicket",
       "provenance": "contract access.yaml GET /access/lookup"
      },
      {
       "kind": "destructiveButton",
       "label": "Override access",
       "operation": "overrideAccess",
       "provenance": "contract access.yaml POST /access/override"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate access",
       "operation": "validateAccess",
       "provenance": "contract access.yaml POST /access/validate"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate group access",
       "operation": "validateGroupAccess",
       "provenance": "contract access.yaml POST /access/group-validate"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmOverrideAccess",
    "component": "confirmDialog",
    "trigger": "Override access",
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A scan ready this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
    "provenance": "contract access.yaml POST /access/override"
   },
   {
    "id": "formSyncScans",
    "component": "modal",
    "trigger": "Sync scans",
    "body": "**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sync scans",
     "operation": "syncScans"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "deviceId",
      "scans"
     ]
    },
    "provenance": "contract access.yaml POST /access/scans"
   },
   {
    "id": "formValidateAccess",
    "component": "modal",
    "trigger": "Validate access",
    "body": "**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ValidateRequest",
    "confirm": {
     "label": "Validate access",
     "operation": "validateAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "mediaCode",
      "mediaKind",
      "direction",
      "recordedAt",
      "groupSize",
      "proximityToken"
     ]
    },
    "provenance": "contract access.yaml POST /access/validate"
   },
   {
    "id": "formValidateGroupAccess",
    "component": "modal",
    "trigger": "Validate group access",
    "body": "**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Validate group access",
     "operation": "validateGroupAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "mediaCode",
      "admitCount",
      "recordedAt",
      "direction"
     ]
    },
    "provenance": "contract access.yaml POST /access/group-validate"
   }
  ],
  "states": {
   "loading": "The scan ready list.",
   "error": "Could not load. Names which read failed and leaves the scan ready untouched.",
   "emptyFirstRun": "No scan ready yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the scan ready are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onAction"
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
   },
   {
    "operationId": "verifyAccreditationCredential",
    "contract": "accreditation",
    "purpose": "Verify a presented accreditation: photo, name, category, zones allowed now, validity",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "ScanEvent.id",
    "ScanEvent.accessPointId",
    "ScanEvent.venueId",
    "ScanEvent.scopePath",
    "ScanEvent.ticketId"
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
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-004 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-004 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-004 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    },
    {
     "to": "EMP-005",
     "trigger": "Completes a task",
     "provenance": "flow F08 step 5→6, F12 step 2→3, F65 step 2→3",
     "carries": [
      "workOrderId"
     ]
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
       "kind": "textField",
       "label": "Assigned to principal id",
       "operation": "listWorkOrders",
       "notes": "Sends `?assignedToPrincipalId=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listWorkOrders",
       "notes": "Sends `?status=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Priority",
       "operation": "listWorkOrders",
       "notes": "Sends `?priority=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Asset id",
       "operation": "listWorkOrders",
       "notes": "Sends `?assetId=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "toggle",
       "label": "Overdue only",
       "operation": "listWorkOrders",
       "notes": "Sends `?overdueOnly=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "dataTable",
       "label": "Every work order",
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
       "label": "The selected work order",
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
        "WorkOrder.status",
        "WorkOrder.priority",
        "WorkOrder.kind",
        "WorkOrder.assignedToPrincipalId",
        "WorkOrder.raisedByPrincipalId"
       ],
       "operation": "listWorkOrders",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "detailPanel",
       "label": "The work order",
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
       "label": "Accept work order",
       "operation": "acceptWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/accept"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject work order",
       "operation": "rejectWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject",
       "notes": "Asks for a reason; when the reason is Other a note is required, and the operation refuses 400 without it (decided 28 September, audit R222)."
      },
      {
       "kind": "secondaryButton",
       "label": "Attach work order evidence",
       "operation": "attachWorkOrderEvidence",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel work order",
       "operation": "cancelWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close work order",
       "operation": "closeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete work order",
       "operation": "completeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause work order",
       "operation": "pauseWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Record work order parts",
       "operation": "recordWorkOrderParts",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record work order time",
       "operation": "recordWorkOrderTime",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume work order",
       "operation": "resumeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/resume"
      },
      {
       "kind": "secondaryButton",
       "label": "Start work order",
       "operation": "startWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
      },
      {
       "kind": "secondaryButton",
       "label": "Save work order",
       "operation": "updateWorkOrder",
       "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify work order",
       "operation": "verifyWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectWorkOrder",
    "component": "confirmDialog",
    "trigger": "Reject work order",
    "body": "**Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
   },
   {
    "id": "confirmCancelWorkOrder",
    "component": "confirmDialog",
    "trigger": "Cancel work order",
    "body": "**Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted. **Collects what `cancelWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `supersededByWorkOrderId`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
   },
   {
    "id": "confirmCloseWorkOrder",
    "component": "confirmDialog",
    "trigger": "Close work order",
    "body": "**Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted. **Collects what `closeWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`, `duplicateOfWorkOrderId`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
   },
   {
    "id": "formAttachWorkOrderEvidence",
    "component": "modal",
    "trigger": "Attach work order evidence",
    "body": "**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Attach work order evidence",
     "operation": "attachWorkOrderEvidence"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "assetRef",
      "text",
      "capturedAt",
      "stage"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
   },
   {
    "id": "formCompleteWorkOrder",
    "component": "modal",
    "trigger": "Complete work order",
    "body": "**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Complete work order",
     "operation": "completeWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "resolution",
      "recordedAt",
      "resolutionCode",
      "attachmentRefs",
      "followUpRequired",
      "followUpNote"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
   },
   {
    "id": "formPauseWorkOrder",
    "component": "modal",
    "trigger": "Pause work order",
    "body": "**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `requisitionId`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Pause work order",
     "operation": "pauseWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "note",
      "requisitionId"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
   },
   {
    "id": "formRecordWorkOrderParts",
    "component": "modal",
    "trigger": "Record work order parts",
    "body": "**Collects what `recordWorkOrderParts` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record work order parts",
     "operation": "recordWorkOrderParts"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "lines"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
   },
   {
    "id": "formRecordWorkOrderTime",
    "component": "modal",
    "trigger": "Record work order time",
    "body": "**Collects what `recordWorkOrderTime` sends before it is called.** Required: `id`, `action`, `recordedAt`. Optional: `pauseReason`, `note`. **When the pause reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record work order time",
     "operation": "recordWorkOrderTime"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "action",
      "recordedAt",
      "pauseReason",
      "note"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
   },
   {
    "id": "formStartWorkOrder",
    "component": "modal",
    "trigger": "Start work order",
    "body": "**Collects what `startWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `startedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Start work order",
     "operation": "startWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startedAt"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
   },
   {
    "id": "formUpdateWorkOrder",
    "component": "modal",
    "trigger": "Save work order",
    "body": "**Collects what `updateWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `assignedToPrincipalId`, `priority`, `dueAt`, `description`, `categoryId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save work order",
     "operation": "updateWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "assignedToPrincipalId",
      "priority",
      "dueAt",
      "description",
      "categoryId"
     ]
    },
    "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
   },
   {
    "id": "formVerifyWorkOrder",
    "component": "modal",
    "trigger": "Verify work order",
    "body": "**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Verify work order",
     "operation": "verifyWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outcome",
      "note"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
   }
  ],
  "states": {
   "loading": "The task list list.",
   "error": "Could not load. Names which read failed and leaves the task list untouched.",
   "emptyFirstRun": "No task list yet. Offers Record work order parts (`recordWorkOrderParts`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the task list are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onAction"
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
    "WorkOrder.downtimeMinutes",
    "WorkOrder.rootCause",
    "WorkOrder.rootCauseNote",
    "WorkOrder.escalatedAt",
    "WorkOrder.escalationLevel"
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
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-005 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-005 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-005 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    },
    {
     "to": "BO-078",
     "trigger": "Raises a requisition against the work order",
     "provenance": "flow F15 step 1→2",
     "operation": "pauseWorkOrder",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "BO-030",
     "trigger": "Supervisor verifies",
     "provenance": "flow F12 step 3→4",
     "operation": "completeWorkOrder",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "workOrderId"
     ]
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
       "kind": "textField",
       "label": "Assigned to principal id",
       "operation": "listWorkOrders",
       "notes": "Sends `?assignedToPrincipalId=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listWorkOrders",
       "notes": "Sends `?status=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Priority",
       "operation": "listWorkOrders",
       "notes": "Sends `?priority=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Asset id",
       "operation": "listWorkOrders",
       "notes": "Sends `?assetId=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "toggle",
       "label": "Overdue only",
       "operation": "listWorkOrders",
       "notes": "Sends `?overdueOnly=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "dataTable",
       "label": "Every work order",
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
       "label": "The selected work order",
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
        "WorkOrder.status",
        "WorkOrder.priority",
        "WorkOrder.kind",
        "WorkOrder.assignedToPrincipalId",
        "WorkOrder.raisedByPrincipalId"
       ],
       "operation": "listWorkOrders",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "detailPanel",
       "label": "The work order",
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
       "label": "Start work order",
       "operation": "startWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause work order",
       "operation": "pauseWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete work order",
       "operation": "completeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept work order",
       "operation": "acceptWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/accept"
      },
      {
       "kind": "secondaryButton",
       "label": "Attach work order evidence",
       "operation": "attachWorkOrderEvidence",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel work order",
       "operation": "cancelWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close work order",
       "operation": "closeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Record work order parts",
       "operation": "recordWorkOrderParts",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record work order time",
       "operation": "recordWorkOrderTime",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject work order",
       "operation": "rejectWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject",
       "notes": "Asks for a reason; when the reason is Other a note is required, and the operation refuses 400 without it (decided 28 September, audit R222)."
      },
      {
       "kind": "secondaryButton",
       "label": "Resume work order",
       "operation": "resumeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/resume"
      },
      {
       "kind": "secondaryButton",
       "label": "Save work order",
       "operation": "updateWorkOrder",
       "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify work order",
       "operation": "verifyWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Parts reserved for this task",
       "bindsTo": "InventoryStockReservation",
       "columns": [
        "InventoryStockReservation.itemId",
        "InventoryStockReservation.quantity",
        "InventoryStockReservation.status"
       ],
       "operation": "listStockReservations",
       "notes": "**Reserved in the general inventory** (decided 17 September, M17-02), `sourceType` workOrder. *Record work order parts* issues from the reservation first. Needs signal: stock depletes in real time, so the reserve action is hidden offline.",
       "provenance": "contract inventory.yaml GET /stock-reservations"
      },
      {
       "kind": "secondaryButton",
       "label": "Reserve parts",
       "operation": "createStockReservation",
       "provenance": "contract inventory.yaml POST /stock-reservations"
      },
      {
       "kind": "secondaryButton",
       "label": "Release reserved parts",
       "operation": "releaseStockReservation",
       "provenance": "contract inventory.yaml POST /stock-reservations/{stockReservationId}/release"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelWorkOrder",
    "component": "confirmDialog",
    "trigger": "Cancel work order",
    "body": "**Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted. **Collects what `cancelWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `supersededByWorkOrderId`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
   },
   {
    "id": "confirmCloseWorkOrder",
    "component": "confirmDialog",
    "trigger": "Close work order",
    "body": "**Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted. **Collects what `closeWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`, `duplicateOfWorkOrderId`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
   },
   {
    "id": "confirmRejectWorkOrder",
    "component": "confirmDialog",
    "trigger": "Reject work order",
    "body": "**Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
   },
   {
    "id": "formStartWorkOrder",
    "component": "modal",
    "trigger": "Start work order",
    "body": "**Collects what `startWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `startedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Start work order",
     "operation": "startWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startedAt"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
   },
   {
    "id": "formPauseWorkOrder",
    "component": "modal",
    "trigger": "Pause work order",
    "body": "**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `requisitionId`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Pause work order",
     "operation": "pauseWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "note",
      "requisitionId"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
   },
   {
    "id": "formCompleteWorkOrder",
    "component": "modal",
    "trigger": "Complete work order",
    "body": "**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Complete work order",
     "operation": "completeWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "resolution",
      "recordedAt",
      "resolutionCode",
      "attachmentRefs",
      "followUpRequired",
      "followUpNote"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
   },
   {
    "id": "formAttachWorkOrderEvidence",
    "component": "modal",
    "trigger": "Attach work order evidence",
    "body": "**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Attach work order evidence",
     "operation": "attachWorkOrderEvidence"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "assetRef",
      "text",
      "capturedAt",
      "stage"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
   },
   {
    "id": "formRecordWorkOrderParts",
    "component": "modal",
    "trigger": "Record work order parts",
    "body": "**Collects what `recordWorkOrderParts` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record work order parts",
     "operation": "recordWorkOrderParts"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "lines"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
   },
   {
    "id": "formRecordWorkOrderTime",
    "component": "modal",
    "trigger": "Record work order time",
    "body": "**Collects what `recordWorkOrderTime` sends before it is called.** Required: `id`, `action`, `recordedAt`. Optional: `pauseReason`, `note`. **When the pause reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record work order time",
     "operation": "recordWorkOrderTime"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "action",
      "recordedAt",
      "pauseReason",
      "note"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
   },
   {
    "id": "formUpdateWorkOrder",
    "component": "modal",
    "trigger": "Save work order",
    "body": "**Collects what `updateWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `assignedToPrincipalId`, `priority`, `dueAt`, `description`, `categoryId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save work order",
     "operation": "updateWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "assignedToPrincipalId",
      "priority",
      "dueAt",
      "description",
      "categoryId"
     ]
    },
    "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
   },
   {
    "id": "formVerifyWorkOrder",
    "component": "modal",
    "trigger": "Verify work order",
    "body": "**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Verify work order",
     "operation": "verifyWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outcome",
      "note"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
   }
  ],
  "states": {
   "loading": "The task list.",
   "error": "Could not load. Names which read failed and leaves the task untouched.",
   "emptyFirstRun": "No task yet. Offers Record work order parts (`recordWorkOrderParts`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the task are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Editable offline. Findings and photos queue"
  },
  "apis": [
   {
    "operationId": "listStockReservations",
    "contract": "inventory",
    "purpose": "Parts reserved for the task (M17-02)",
    "trigger": "onAction",
    "provenance": "decided 17 September, M17-02 (the 29 September pass)"
   },
   {
    "operationId": "createStockReservation",
    "contract": "inventory",
    "purpose": "Reserve parts for the task (M17-02)",
    "trigger": "onAction",
    "provenance": "decided 17 September, M17-02 (the 29 September pass)",
    "invalidates": [
     "listStockReservations"
    ]
   },
   {
    "operationId": "releaseStockReservation",
    "contract": "inventory",
    "purpose": "Give reserved parts back (M17-02)",
    "trigger": "onAction",
    "provenance": "decided 17 September, M17-02 (the 29 September pass)",
    "invalidates": [
     "listStockReservations"
    ]
   },
   {
    "operationId": "getWorkOrder",
    "contract": "maintenance",
    "purpose": "Read a work order",
    "trigger": "onAction"
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
    },
    {
     "name": "stockReservationId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `workOrderId`.",
   "preloaded": [
    "WorkOrder.downtimeMinutes",
    "WorkOrder.rootCause",
    "WorkOrder.rootCauseNote",
    "WorkOrder.escalatedAt",
    "WorkOrder.escalationLevel"
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
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-006 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-006 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-006 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    },
    {
     "to": "EMP-004",
     "trigger": "It appears on the list for whoever is free",
     "provenance": "flow F65 step 1→2",
     "operation": "createWorkOrder",
     "carries": [
      "workOrderId"
     ]
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
       "kind": "textField",
       "label": "Assigned to principal id",
       "operation": "listWorkOrders",
       "notes": "Sends `?assignedToPrincipalId=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listWorkOrders",
       "notes": "Sends `?status=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Priority",
       "operation": "listWorkOrders",
       "notes": "Sends `?priority=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "textField",
       "label": "Asset id",
       "operation": "listWorkOrders",
       "notes": "Sends `?assetId=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "toggle",
       "label": "Overdue only",
       "operation": "listWorkOrders",
       "notes": "Sends `?overdueOnly=` to `listWorkOrders`.",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "dataTable",
       "label": "Every work order",
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
       "label": "The selected work order",
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
        "WorkOrder.status",
        "WorkOrder.priority",
        "WorkOrder.kind",
        "WorkOrder.assignedToPrincipalId",
        "WorkOrder.raisedByPrincipalId"
       ],
       "operation": "listWorkOrders",
       "provenance": "contract maintenance.yaml GET /work-orders"
      },
      {
       "kind": "detailPanel",
       "label": "The work order",
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
       "label": "Create work order",
       "operation": "createWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept work order",
       "operation": "acceptWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/accept"
      },
      {
       "kind": "secondaryButton",
       "label": "Attach work order evidence",
       "operation": "attachWorkOrderEvidence",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel work order",
       "operation": "cancelWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close work order",
       "operation": "closeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete work order",
       "operation": "completeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause work order",
       "operation": "pauseWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Record work order parts",
       "operation": "recordWorkOrderParts",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record work order time",
       "operation": "recordWorkOrderTime",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject work order",
       "operation": "rejectWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject",
       "notes": "Asks for a reason; when the reason is Other a note is required, and the operation refuses 400 without it (decided 28 September, audit R222)."
      },
      {
       "kind": "secondaryButton",
       "label": "Resume work order",
       "operation": "resumeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/resume"
      },
      {
       "kind": "secondaryButton",
       "label": "Start work order",
       "operation": "startWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
      },
      {
       "kind": "secondaryButton",
       "label": "Save work order",
       "operation": "updateWorkOrder",
       "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify work order",
       "operation": "verifyWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelWorkOrder",
    "component": "confirmDialog",
    "trigger": "Cancel work order",
    "body": "**Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `cancelWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `supersededByWorkOrderId`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
   },
   {
    "id": "confirmCloseWorkOrder",
    "component": "confirmDialog",
    "trigger": "Close work order",
    "body": "**Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `closeWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`, `duplicateOfWorkOrderId`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
   },
   {
    "id": "confirmRejectWorkOrder",
    "component": "confirmDialog",
    "trigger": "Reject work order",
    "body": "**Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/reject"
   },
   {
    "id": "formCreateWorkOrder",
    "component": "modal",
    "trigger": "Create work order",
    "body": "**Collects what `createWorkOrder` sends before it is called.** Required: `id`, `title`, `venueId`, `priority`, `recordedAt`. Optional: `description`, `assetId`, `locationDescription`, `kind`, `categoryId`, `assignedToPrincipalId`, `dueAt`, `attachmentRefs`, `takeAssetOutOfService`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateWorkOrderRequest",
    "confirm": {
     "label": "Create work order",
     "operation": "createWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "title",
      "venueId",
      "priority",
      "recordedAt",
      "description",
      "assetId",
      "locationDescription",
      "kind",
      "categoryId",
      "assignedToPrincipalId",
      "dueAt",
      "attachmentRefs",
      "takeAssetOutOfService"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders"
   },
   {
    "id": "formAttachWorkOrderEvidence",
    "component": "modal",
    "trigger": "Attach work order evidence",
    "body": "**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Attach work order evidence",
     "operation": "attachWorkOrderEvidence"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "assetRef",
      "text",
      "capturedAt",
      "stage"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
   },
   {
    "id": "formCompleteWorkOrder",
    "component": "modal",
    "trigger": "Complete work order",
    "body": "**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Complete work order",
     "operation": "completeWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "resolution",
      "recordedAt",
      "resolutionCode",
      "attachmentRefs",
      "followUpRequired",
      "followUpNote"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
   },
   {
    "id": "formPauseWorkOrder",
    "component": "modal",
    "trigger": "Pause work order",
    "body": "**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `requisitionId`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Pause work order",
     "operation": "pauseWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "note",
      "requisitionId"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/pause"
   },
   {
    "id": "formRecordWorkOrderParts",
    "component": "modal",
    "trigger": "Record work order parts",
    "body": "**Collects what `recordWorkOrderParts` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record work order parts",
     "operation": "recordWorkOrderParts"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "lines"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/parts"
   },
   {
    "id": "formRecordWorkOrderTime",
    "component": "modal",
    "trigger": "Record work order time",
    "body": "**Collects what `recordWorkOrderTime` sends before it is called.** Required: `id`, `action`, `recordedAt`. Optional: `pauseReason`, `note`. **When the pause reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record work order time",
     "operation": "recordWorkOrderTime"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "action",
      "recordedAt",
      "pauseReason",
      "note"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/time"
   },
   {
    "id": "formStartWorkOrder",
    "component": "modal",
    "trigger": "Start work order",
    "body": "**Collects what `startWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `startedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Start work order",
     "operation": "startWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startedAt"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/start"
   },
   {
    "id": "formUpdateWorkOrder",
    "component": "modal",
    "trigger": "Save work order",
    "body": "**Collects what `updateWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `assignedToPrincipalId`, `priority`, `dueAt`, `description`, `categoryId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save work order",
     "operation": "updateWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "assignedToPrincipalId",
      "priority",
      "dueAt",
      "description",
      "categoryId"
     ]
    },
    "provenance": "contract maintenance.yaml PATCH /work-orders/{workOrderId}"
   },
   {
    "id": "formVerifyWorkOrder",
    "component": "modal",
    "trigger": "Verify work order",
    "body": "**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Verify work order",
     "operation": "verifyWorkOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outcome",
      "note"
     ]
    },
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
   }
  ],
  "states": {
   "loading": "The raise task list.",
   "error": "Could not load. Names which read failed and leaves the raise task untouched.",
   "emptyFirstRun": "No raise task yet. Offers Create work order (`createWorkOrder`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the raise task are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onAction"
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
    "WorkOrder.downtimeMinutes",
    "WorkOrder.rootCause",
    "WorkOrder.rootCauseNote",
    "WorkOrder.escalatedAt",
    "WorkOrder.escalationLevel"
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
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-007 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-007 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-007 holds none of them, so the edge carries nothing and EMP-003 opens cold"
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
   "loading": "The handover notes list.",
   "error": "Could not load. Names which read failed and leaves the handover notes untouched.",
   "emptyFirstRun": "No handover notes yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on unacknowledgedOnly and the handover notes are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-007"
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
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-008 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-008 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-008 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: acceptShiftVariance, approveShiftOpen, closeShift, createCashMovement. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Removed 24 August**: openShift, recordNoSale, reopenShift, resumeShift. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listShifts` reads the population and `getCurrentShift` reads one of them — list, select, act",
  "purpose": "See what this person actually did today.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listShifts",
       "notes": "Sends `?workstationId=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listShifts",
       "notes": "Sends `?status=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "datePicker",
       "label": "Opened from",
       "operation": "listShifts",
       "notes": "Sends `?openedFrom=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "datePicker",
       "label": "Opened to",
       "operation": "listShifts",
       "notes": "Sends `?openedTo=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "dataTable",
       "label": "Every shift",
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
      },
      {
       "kind": "dataTable",
       "label": "Every cash movement",
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
        "CashMovement.depositBoxId",
        "CashMovement.witnessPrincipalId",
        "CashMovement.withdrawalReason",
        "CashMovement.authorisedByPrincipalId"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected shift",
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
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
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
       "operation": "getShift",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Suspend shift",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend shift",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A shift summary this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   }
  ],
  "states": {
   "loading": "The shift summary list.",
   "error": "Could not load. Names which read failed and leaves the shift summary untouched.",
   "emptyFirstRun": "No shift summary yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on workstationId, status, openedFrom, openedTo and the shift summary are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
  "offlineCapable": false,
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
 "createMfaChallenge": {
  "method": "POST",
  "path": "/auth/mfa/challenge",
  "contract": "identity",
  "summary": "Second factor at staff sign-in, and step-up for a sensitive action",
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
  "responds": null
 },
 "createStockReservation": {
  "method": "POST",
  "path": "/stock-reservations",
  "contract": "inventory",
  "summary": "Reserve stock for a work order or another need",
  "permission": "PROCUREMENT_REQUEST",
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
  "requestBody": "InventoryStockReservation",
  "responds": "InventoryStockReservation"
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
    "name": "sinceVersion",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
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
  "responds": "Page"
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
 "listStockReservations": {
  "method": "GET",
  "path": "/stock-reservations",
  "contract": "inventory",
  "summary": "Soft holds on stock",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "sourceType",
    "in": "query",
    "required": null
   },
   {
    "name": "sourceId",
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
    "name": "categoryId",
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
  "offlineCapable": false,
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
  "summary": "Open the Deposit Box without a sale",
  "permission": "CASH_NO_SALE",
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
 "releaseStockReservation": {
  "method": "POST",
  "path": "/stock-reservations/{stockReservationId}/release",
  "contract": "inventory",
  "summary": "Give reserved stock back",
  "permission": "PROCUREMENT_REQUEST",
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
  "responds": "InventoryStockReservation"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
 "verifyAccreditationCredential": {
  "method": "GET",
  "path": "/accreditation-credentials/verify",
  "contract": "accreditation",
  "summary": "Who holds this credential, and where may they go",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "identifier",
    "in": "query",
    "required": true
   },
   {
    "name": "zoneId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationCredentialVerification"
 },
 "verifyMfaChallenge": {
  "method": "POST",
  "path": "/auth/mfa/challenge/{challengeId}/verify",
  "contract": "identity",
  "summary": "Complete a sign-in or step-up challenge",
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
  "responds": null
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
 "AccessAccreditationCredential": {
  "type": "object",
  "x-ticvai-persistence": "access.accreditation_credential",
  "x-ticvai-agreed": "29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer",
  "description": "**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.",
  "required": [
   "id",
   "holderId",
   "encodedIdentifier",
   "admits",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The accreditation credential's id (`credentialId` on the events)."
   },
   "holderId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "description": "printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."
   },
   "encodedIdentifier": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "What the gate reads from the credential. Never sent to webhook subscribers."
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "zoneIds": {
    "type": "array",
    "description": "The holder's effective zones, from the event (`effectiveZones`).",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "holderStatus": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked",
     "expired",
     "archived"
    ],
    "description": "The holder's status as last published; only `active` admits."
   },
   "admits": {
    "type": "boolean",
    "description": "False once the credential is replaced or the holder is not active."
   },
   "sourceChangedAt": {
    "type": "string",
    "format": "date-time",
    "description": "The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005), the accreditation programme's scope."
   }
  }
 },
 "AccessDynamicPolicy": {
  "type": "object",
  "x-ticvai-persistence": "access.dynamic_policy",
  "description": "One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.access_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AccessPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAccessPolicyEffectiveness` in identity.",
  "required": [
   "id",
   "scopePath",
   "name",
   "policyType",
   "conditionExpression",
   "result",
   "status",
   "currentVersion"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The policyId"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node; where it applies further is access.policy_scope_assignment"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "policyType": {
    "type": "string",
    "enum": [
     "guestAttribute",
     "accreditation",
     "occupancy",
     "employee",
     "risk",
     "membership",
     "timeEvent"
    ]
   },
   "contextType": {
    "type": "string",
    "enum": [
     "date",
     "day",
     "time",
     "season",
     "event",
     "performance",
     "specialEvent",
     "holiday",
     "operatingCalendar",
     "occupancy",
     "attractionStatus"
    ],
    "nullable": true,
    "description": "Context/time/event policies (setContextTimeEvent)"
   },
   "identityType": {
    "type": "string",
    "enum": [
     "guest",
     "member",
     "annualPassHolder",
     "employee",
     "contractor",
     "vendor",
     "performer",
     "media",
     "vip",
     "security",
     "emergencyServices",
     "eventStaff"
    ],
    "nullable": true,
    "description": "Identity-based policies (listIdentityMembershipAccreditation)"
   },
   "conditionExpression": {
    "type": "string",
    "description": "Condition tree over access.access_attribute keys using AND, OR, NOT, IN and BETWEEN"
   },
   "result": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ]
   },
   "priority": {
    "type": "integer",
    "nullable": true
   },
   "allowedZoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "deniedZoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "monitorThresholdPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Occupancy policies. Percent at which the band becomes Monitor"
   },
   "restrictThresholdPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Occupancy policies. Percent at which the band becomes Restrict"
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
    "description": "The grant expires automatically at validTo"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "inactive",
     "expired"
    ],
    "default": "draft"
   },
   "currentVersion": {
    "type": "integer",
    "minimum": 1,
    "description": "The version in force (access.dynamic_policy_version)"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AccreditationCredentialVerification": {
  "type": "object",
  "description": "18.8.3. **What a steward needs to believe the person in front of them**: the face, the name, the category and the zones, and whether any of it is valid now. Returned by `verifyAccreditationCredential`; not stored.\n",
  "required": [
   "outcome"
  ],
  "properties": {
   "outcome": {
    "type": "string",
    "enum": [
     "valid",
     "notYetValid",
     "expired",
     "suspended",
     "revoked",
     "credentialReplaced",
     "credentialLost",
     "credentialInactive"
    ],
    "description": "`valid` only when the holder is `active`, today is inside the holder's validity, and the credential is `issued` or `active`"
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "credentialId": {
    "type": "string",
    "format": "uuid"
   },
   "credentialKind": {
    "type": "string"
   },
   "credentialStatus": {
    "type": "string"
   },
   "holderId": {
    "type": "string",
    "format": "uuid"
   },
   "accreditationNumber": {
    "type": "string"
   },
   "fullName": {
    "type": "string"
   },
   "photoAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "photoUrl": {
    "type": "string",
    "nullable": true,
    "description": "Signed and short-lived, so the scan screen can show the face without a second call"
   },
   "organisationName": {
    "type": "string",
    "nullable": true
   },
   "affiliationRole": {
    "type": "string",
    "nullable": true
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "categoryName": {
    "type": "string",
    "nullable": true
   },
   "holderStatus": {
    "type": "string"
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "effectiveZones": {
    "type": "array",
    "description": "The zones the holder may enter under their profiles and exceptions, today",
    "items": {
     "type": "object",
     "properties": {
      "zoneId": {
       "type": "string",
       "format": "uuid"
      },
      "zoneName": {
       "type": "string"
      },
      "allowedNow": {
       "type": "boolean",
       "description": "Inside the profile schedule (date, day, time, event phase) at this moment"
      }
     }
    }
   },
   "escortRequired": {
    "type": "boolean"
   },
   "zoneCheck": {
    "type": "object",
    "nullable": true,
    "description": "Present when `zoneId` was given",
    "properties": {
     "zoneId": {
      "type": "string",
      "format": "uuid"
     },
     "allowed": {
      "type": "boolean"
     },
     "reason": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "checkedAt": {
    "type": "string",
    "format": "date-time"
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
      "type": "string",
      "format": "uuid"
     },
     "depositBoxId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"
     },
     "witnessPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The cashier who countersigned a withdrawal. Null on other movements."
     },
     "withdrawalReason": {
      "allOf": [
       {
        "$ref": "#/components/schemas/WithdrawalReason"
       }
      ],
      "nullable": true
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
  ],
  "description": "`openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`.\n"
 },
 "CloseShiftRequest": {
  "type": "object",
  "required": [
   "countedCash",
   "recordedAt"
  ],
  "properties": {
   "countedCash": {
    "type": "array",
    "minItems": 1,
    "description": "**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n",
    "items": {
     "$ref": "#/components/schemas/CountedDenominationLine"
    }
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
 "CountedDenominationLine": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; lands as `CashCountLine` rows",
  "description": "**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n",
  "required": [
   "denominationId",
   "count"
  ],
  "properties": {
   "denominationId": {
    "type": "string",
    "format": "uuid",
    "description": "References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."
   },
   "count": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100000,
    "description": "**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."
   },
   "total": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"
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
    "format": "uuid",
    "description": "Client-generated UUIDv7."
   },
   "kind": {
    "$ref": "#/components/schemas/CashMovementKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "denominations": {
    "$ref": "#/components/schemas/DenominationCount",
    "x-ticvai-persisted": false,
    "description": "**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"
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
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
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
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderPriority"
     }
    ],
    "description": "**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"
   },
   "faultAssessment": {
    "$ref": "#/components/schemas/WorkOrderFaultAssessment"
   },
   "requiredQualificationCodes": {
    "type": "array",
    "maxItems": 10,
    "items": {
     "type": "string"
    },
    "description": "Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."
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
   "delegatedRightRevoked",
   "journeyNotCovered"
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
    "type": "string",
    "format": "uuid"
   },
   "incidentNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
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
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"
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
    "format": "uuid",
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
 "IncidentAuthorityNotification": {
  "x-ticvai-persistence": "maintenance.incident_authority_notification",
  "type": "object",
  "description": "**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n",
  "required": [
   "id",
   "incidentId",
   "authority",
   "notifiedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "format": "uuid"
   },
   "authority": {
    "type": "string",
    "maxLength": 200
   },
   "reference": {
    "type": "string",
    "maxLength": 128,
    "nullable": true
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time"
   },
   "notifiedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
      "nullable": true,
      "readOnly": true,
      "description": "The latest entry of `investigationNotes`, kept for readers that show one line."
     },
     "investigationNotes": {
      "type": "array",
      "readOnly": true,
      "description": "**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n",
      "items": {
       "$ref": "#/components/schemas/IncidentInvestigationNote"
      }
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
     "involvedParties": {
      "type": "array",
      "description": "Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n",
      "items": {
       "$ref": "#/components/schemas/IncidentInvolvedParty"
      }
     },
     "authorityNotifications": {
      "type": "array",
      "description": "Read from `maintenance.incident_authority_notification`, oldest first.",
      "items": {
       "$ref": "#/components/schemas/IncidentAuthorityNotification"
      }
     }
    }
   }
  ]
 },
 "IncidentInvestigationNote": {
  "x-ticvai-persistence": "maintenance.incident_investigation_note",
  "type": "object",
  "description": "**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n",
  "required": [
   "id",
   "incidentId",
   "note",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "format": "uuid"
   },
   "note": {
    "type": "string",
    "maxLength": 10000
   },
   "writtenByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "IncidentInvolvedParty": {
  "x-ticvai-persistence": "maintenance.incident_involved_party",
  "type": "object",
  "description": "**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n",
  "required": [
   "id",
   "incidentId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "subject",
     "staff"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `pii.subject` id where `kind` is `subject`."
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The staff principal where `kind` is `staff`."
   }
  }
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
 "InventoryStockReservation": {
  "type": "object",
  "x-ticvai-persistence": "inventory.stock_reservation",
  "description": "**Taken from the backend workbook, 20 September.** Temporarily reserves stock for an order or operational requirement so it cannot be allocated elsewhere.",
  "required": [
   "itemId",
   "locationId",
   "quantity",
   "sourceType",
   "sourceId",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "itemId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "number",
    "exclusiveMinimum": 0
   },
   "sourceType": {
    "$ref": "#/components/schemas/StockReservationSourceType"
   },
   "sourceId": {
    "type": "string",
    "format": "uuid",
    "description": "The id of what the stock is reserved for: a work order, a rental agreement or an order. A uuid, as every id is (ADR-0056); it was text from 29 September to 30 September because a work order id was then 26-character text (M17-02)."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "consumed",
     "released",
     "expired"
    ],
    "readOnly": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "releasedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
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
    "maxLength": 512,
    "writeOnly": true
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
     "requiresRoleSelection",
     "requiresMfa"
    ],
    "properties": {
     "requiresRoleSelection": {
      "type": "boolean"
     },
     "requiresMfa": {
      "type": "boolean",
      "description": "True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). The session is not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge."
     },
     "hasMfaMethod": {
      "type": "boolean",
      "description": "Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 (5))."
     },
     "mfaMethods": {
      "type": "array",
      "description": "The principal's active methods, so the client can offer the right one for the `signIn` challenge. Empty when `requiresMfa` is false.",
      "items": {
       "$ref": "#/components/schemas/MfaMethod"
      }
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
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "format": "uuid"
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
   "entitlementsVersion": {
    "type": "integer",
    "description": "The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."
   },
   "dynamicPolicies": {
    "type": "array",
    "description": "The active guest-admission dynamic policies for this access point's zones (SD-052), so an offline gate applies the same rules as an online one.",
    "items": {
     "$ref": "#/components/schemas/AccessDynamicPolicy"
    }
   },
   "entitlements": {
    "type": "array",
    "description": "Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.",
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
       "type": "string",
       "format": "uuid",
       "description": "The `Entitlement.id`."
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
       "type": "string",
       "format": "uuid",
       "description": "The `Entitlement.id` in the issuing cell."
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
   },
   "accreditationCredentials": {
    "type": "array",
    "description": "Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.",
    "items": {
     "$ref": "#/components/schemas/AccessAccreditationCredential"
    }
   }
  }
 },
 "OfflineScan": {
  "x-ticvai-persistence": "none — client-side journal",
  "allOf": [
   {
    "$ref": "#/components/schemas/ValidateRequest"
   },
   {
    "type": "object",
    "required": [
     "sequence",
     "localOutcome"
    ],
    "properties": {
     "sequence": {
      "type": "integer",
      "minimum": 1,
      "description": "Monotonic per device. The server processes in this order."
     },
     "localOutcome": {
      "allOf": [
       {
        "$ref": "#/components/schemas/ScanOutcome"
       }
      ],
      "description": "What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"
     },
     "localDenyReason": {
      "$ref": "#/components/schemas/DenyReason"
     },
     "overriddenByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "overrideReason": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
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
    "description": "When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are ordered against it.\n"
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
    "format": "uuid"
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
 "ScanEvent": {
  "x-ticvai-append-only": "recordedAt",
  "x-ticvai-persistence": "access.scan_event",
  "type": "object",
  "required": [
   "id",
   "accessPointId",
   "venueId",
   "outcome",
   "direction",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The scan's client-generated UUIDv7, the key offline replay deduplicates on."
   },
   "accessPointId": {
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
   "ticketId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `Entitlement.id` scanned; null where the media resolved to nothing."
   },
   "mediaCode": {
    "type": "string",
    "nullable": true
   },
   "outcome": {
    "$ref": "#/components/schemas/ScanOutcome"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "overridesScanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "description": "The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."
   },
   "dynamicPolicyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."
   },
   "dynamicPolicyVersion": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "The version of that policy in force at the scan, so a report spanning a change counts each version apart."
   },
   "dynamicPolicyResult": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ],
    "nullable": true,
    "description": "What the policy decided, which for a step-up is not the same as the scan's outcome."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."
   },
   "localSequence": {
    "type": "integer",
    "nullable": true,
    "description": "The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."
   },
   "packageVersion": {
    "type": "string",
    "nullable": true,
    "description": "The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null while pending. Differs from recordedAt for offline scans."
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
  "x-ticvai-persistence": "orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident",
  "description": "**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n",
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
    "format": "uuid",
    "description": "Client-generated UUIDv7. Also the idempotency key."
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
    "x-ticvai-column": "gross_sales_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the till took in sales, as the guest paid it — tax included."
   },
   "refundsTotal": {
    "x-ticvai-column": "gross_refunded_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the till paid back, as the guest was refunded it — tax included."
   },
   "liftsTotal": {
    "x-ticvai-column": "lifted_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."
   },
   "expectedCash": {
    "x-ticvai-column": "expected_cash_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept.\n"
   },
   "countedCash": {
    "x-ticvai-column": "counted_cash_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "What the close count found. Null until the shift is counted."
   },
   "variance": {
    "x-ticvai-column": "variance_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "Counted minus expected, as `ShiftCloseResult.variance`. Negative is short."
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
    "description": "When the device recorded the open. `openedAt` is the server's time."
   },
   "suspendedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "suspendReason": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "The `reason` given to `suspendShift`. Cleared on resume."
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"
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
       ],
       "description": "`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"
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
    "description": "True when the variance exceeds the venue's `shiftVarianceThreshold` (audit R094). The shift is then `pendingVariance` and only `acceptShiftVariance` finalises it (audit R080 (e)).\n"
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
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."
   }
  }
 },
 "StockReservationSourceType": {
  "type": "string",
  "enum": [
   "workOrder",
   "rentalAgreement",
   "order",
   "transfer",
   "other"
  ],
  "description": "What a stock reservation is for (decided 17 September, M17-02; `rentalAgreement` is the existing use from `rental.agreement_item`)."
 },
 "SupervisorStepUp": {
  "type": "object",
  "description": "**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n",
  "required": [
   "principalId",
   "credential"
  ],
  "properties": {
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "The supervisor signing. Recorded against the act."
   },
   "credential": {
    "type": "string",
    "maxLength": 512,
    "writeOnly": true,
    "description": "The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."
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
    "format": "uuid",
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
    "format": "uuid",
    "description": "Client-generated UUIDv7. Also the idempotency key and dedupe key."
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
    "format": "uuid"
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
   },
   "advisory": {
    "type": "object",
    "nullable": true,
    "description": "BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n",
    "properties": {
     "genderClassification": {
      "type": "string",
      "enum": [
       "women",
       "men",
       "undetermined"
      ],
      "description": "**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"
     },
     "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"
     },
     "reportedByDeviceId": {
      "type": "string",
      "format": "uuid",
      "description": "**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"
     }
    }
   }
  }
 },
 "WithdrawalReason": {
  "type": "string",
  "description": "Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.",
  "enum": [
   "banking",
   "safeDrop",
   "changeOrder",
   "other"
  ]
 },
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
  "x-ticvai-retired-columns": [
   "is_overdue"
  ],
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
    "x-ticvai-derived": "onWrite",
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"
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
    "type": "string",
    "format": "uuid"
   },
   "workOrderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
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
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "readOnly": true,
    "description": "The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."
   },
   "prioritySource": {
    "type": "string",
    "enum": [
     "scored",
     "assetOverride",
     "manual"
    ],
    "readOnly": true,
    "description": "Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."
   },
   "faultAssessment": {
    "$ref": "#/components/schemas/WorkOrderFaultAssessment"
   },
   "requiredQualificationCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Skills the job needs (M17-13)."
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
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"
   },
   "elapsedMinutes": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"
   },
   "isTimerRunning": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"
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
    "format": "uuid",
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
    "format": "uuid",
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
        "reservedQuantity": {
         "type": "number",
         "description": "Still reserved for this work order and not yet issued (M17-02)."
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
      "$ref": "../shared/common.yaml#/components/schemas/Money",
      "x-ticvai-column": "net_cost_amount"
     },
     "completedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"
     },
     "followUpRequired": {
      "type": "boolean",
      "default": false
     },
     "followUpNote": {
      "type": "string",
      "maxLength": 1000,
      "nullable": true
     },
     "verificationOutcome": {
      "type": "string",
      "enum": [
       "verified",
       "rejected"
      ],
      "nullable": true,
      "description": "The latest `verifyWorkOrder` outcome."
     },
     "verificationNote": {
      "type": "string",
      "maxLength": 1000,
      "nullable": true
     },
     "verifiedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "verifiedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "cancelReason": {
      "type": "string",
      "enum": [
       "raisedInError",
       "duplicate",
       "superseded",
       "noLongerRequired"
      ],
      "nullable": true
     },
     "cancelNote": {
      "type": "string",
      "maxLength": 300,
      "nullable": true
     },
     "supersededByWorkOrderId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "Set by `cancelWorkOrder` where the reason is `superseded`."
     },
     "cancelledAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "closeOutcome": {
      "type": "string",
      "enum": [
       "completedAndVerified",
       "notReproducible",
       "supersededByReplacement",
       "noLongerApplicable",
       "duplicate"
      ],
      "nullable": true
     },
     "closeNote": {
      "type": "string",
      "maxLength": 500,
      "nullable": true
     },
     "duplicateOfWorkOrderId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "Set by `closeWorkOrder` where the outcome is `duplicate`."
     },
     "closedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "closedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   }
  ]
 },
 "WorkOrderFaultAssessment": {
  "x-ticvai-persistence": "none — columns on maintenance.work_order",
  "type": "object",
  "description": "What the person raising a fault says about it, which the priority score reads (M17-01).",
  "properties": {
   "safetyRisk": {
    "type": "boolean",
    "default": false
   },
   "guestImpact": {
    "type": "string",
    "enum": [
     "none",
     "degraded",
     "closed"
    ],
    "default": "none"
   }
  }
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
