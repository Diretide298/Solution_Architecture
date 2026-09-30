# P07-access-01 — P07 · Access (1 of 2)

**10 screens · 27 operations · 44 schemas · 10 permissions**

Platform P07 Venue Scanner · ships as **venue-staff-mobile** ·
staff audience · handheld ·
offline-capable

## Who this is for

**staff on handheld.** Everything below is how you know what is
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
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, ORDER_CREATE, ORDER_VIEW, PERMISSION_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, SHIFT_OPEN, TICKET_LOOKUP, TURNSTILE_MODE_SET`. A control nobody can use must say so,
  not sit enabled and fail.
- **14 of these operations work offline**: consumeCrossRegionEntitlement, endPodiumShift, getAccessPoint, getCrossRegionEntitlement, getCurrentSession, getCurrentShift, listAccessPoints, listBlacklist
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SCN-001` | Sign in | listDetail | 9 | 3 | — |
| `SCN-002` | Access point & direction | listDetail | 5 | 3 | — |
| `SCN-003` | Ready to scan | listDetail | 10 | 5 | — |
| `SCN-007` | Group admission | listDetail | 7 | 4 | — |
| `SCN-008` | Manual entry | listDetail | 7 | 4 | — |
| `SCN-009` | Ticket lookup | listDetail | 7 | 4 | — |
| `SCN-011` | Delegated right | statusTracker | 2 | 1 | — |
| `SCN-013` | Offline journal | listDetail | 7 | 4 | — |
| `SCN-014` | Sync & reconciliation | listDetail | 9 | 5 | — |
| `SCN-015` | Offline package | listDetail | 7 | 4 | — |

## Thin screens in this batch

**SCN-011 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SCN-001",
  "name": "Sign in",
  "module": "Access",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/sign-in",
   "component": "apps/venue-scanner/src/routes/access/SignInDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-002",
    "SCN-003"
   ],
   "inferred": true,
   "fromFlows": true,
   "isEntryPoint": true,
   "transitions": [
    {
     "to": "SCN-002",
     "trigger": "Confirms access point and direction",
     "provenance": "flow F06 step 1→2, F61 step 1→2"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "provenance": "structural — SCN-001 is P07's home screen and its exits are its launcher"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **createCashMovement removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Sign in.** The session carries the workstation, so the device cannot scan before it knows who is holding it. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable. **`selectRole` and `resolvePermissions` wired 24 August.** ADR-0002 makes authorisation user-driven and **a sign-in screen that does not resolve a role is a sign-in that grants nothing** — found by walking F61. **Removed 24 August**: acceptShiftVariance, approveShiftOpen, closeShift, forceLogout, getShift, listActiveSessions, listCashMovements, listShifts, openShift, recordNoSale, reopenShift, resumeShift, revokeAllSessions, suspendShift. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listMfaMethods` reads the population and `getCurrentShift` reads one of them — list, select, act",
  "purpose": "PIN or badge. Session carries the workstation.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Select role",
       "operation": "selectRole",
       "provenance": "contract identity.yaml POST /auth/select-role"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve permissions",
       "operation": "resolvePermissions",
       "provenance": "contract identity.yaml POST /permissions/resolve"
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
   "emptyNoAccess": "Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "mfaRequired": "**Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any platform-staff permission, or one the tenant added), so after `login` the screen calls `createMfaChallenge` and asks for the authenticator code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says so. A principal with no enrolled method is sent to enrol first (decided 28 September, audit R135, R126).",
   "offline": "**Signs in against the cached principal list from the last bundle.** A steward locked out at 08:00 because the venue wifi is down is a gate that does not open"
  },
  "apis": [
   {
    "operationId": "login",
    "contract": "identity",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "getCurrentShift",
    "contract": "shift",
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
    "operationId": "selectRole",
    "contract": "identity",
    "purpose": "Choose a role for a multi-role session",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "resolvePermissions",
    "contract": "identity",
    "purpose": "Simulate a principal's effective permissions",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
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
     "name": "shiftId",
     "from": "session"
    },
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
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-001"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
   },
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
   },
   {
    "id": "formResolvePermissions",
    "component": "modal",
    "trigger": "Resolve permissions",
    "body": "**Collects what `resolvePermissions` sends before it is called.** Required: `principalId`, `roleId`. Optional: `atScopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resolve permissions",
     "operation": "resolvePermissions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "principalId",
      "roleId",
      "atScopePath"
     ]
    },
    "provenance": "contract identity.yaml POST /permissions/resolve"
   }
  ],
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-002",
  "name": "Access point & direction",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/access-point-direction",
   "component": "apps/venue-scanner/src/routes/access/AccessPointDirectionDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-003",
    "SCN-013",
    "SCN-015",
    "SCN-016"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "SCN-015",
     "trigger": "Loads the offline package",
     "provenance": "flow F06 step 2→3, F61 step 2→3"
    },
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-002 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "provenance": "derived — SCN-003 declares entryState.params mediaCode, rightId and SCN-002 holds none of them, so the edge carries nothing and SCN-003 opens cold"
    },
    {
     "to": "SCN-016",
     "trigger": "Gate mode",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-016 declares entryState.params accessPointId, changeId and SCN-002 holds accessPointId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Authoring operations removed 24 August**: createAccessPoint, setAccessPointGeofence, updateAccessPoint. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere. **`setTurnstileMode` belongs here and flow F06 is why.** It was taken off on 4 September on the reasoning that this screen only reads — but F06 *guest enters the venue* step 2 is 'confirms access point and direction'. **Since 28 September (audit R221) confirming the direction is not setting the mode**: the direction is fixed per access point and shown here read-only; what the operator sets is the operating mode (required), with the turnstile mode (freeRotation or closed) as an optional narrowing under normal or podium only.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listAccessPoints` reads the population and `getAccessPoint` reads one of them — list, select, act",
  "purpose": "Confirm what this device is doing before it does it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listAccessPoints",
       "notes": "Sends `?venueId=` to `listAccessPoints`.",
       "provenance": "contract access.yaml GET /access-points"
      },
      {
       "kind": "dataTable",
       "label": "Every access point",
       "bindsTo": "AccessPoint",
       "columns": [
        "AccessPoint.id",
        "AccessPoint.code",
        "AccessPoint.name",
        "AccessPoint.venueId",
        "AccessPoint.scopePath",
        "AccessPoint.externalCredentialSources",
        "AccessPoint.scanAnomalyRules",
        "AccessPoint.operatingMode",
        "AccessPoint.vehicleLocationCapture",
        "AccessPoint.mode",
        "AccessPoint.direction",
        "AccessPoint.antiPassbackEnabled"
       ],
       "operation": "listAccessPoints",
       "provenance": "contract access.yaml GET /access-points"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access point",
       "bindsTo": "AccessPoint",
       "columns": [
        "AccessPoint.id",
        "AccessPoint.code",
        "AccessPoint.name",
        "AccessPoint.venueId",
        "AccessPoint.scopePath",
        "AccessPoint.externalCredentialSources",
        "AccessPoint.scanAnomalyRules",
        "AccessPoint.operatingMode",
        "AccessPoint.vehicleLocationCapture",
        "AccessPoint.mode",
        "AccessPoint.direction",
        "AccessPoint.antiPassbackEnabled",
        "AccessPoint.isActive",
        "AccessPoint.lastHeartbeatAt"
       ],
       "operation": "getAccessPoint",
       "provenance": "contract access.yaml GET /access-points/{accessPointId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save gate mode",
       "operation": "setTurnstileMode",
       "provenance": "contract access.yaml PUT /access-points/{accessPointId}/mode"
      },
      {
       "kind": "secondaryButton",
       "label": "Start podium shift",
       "operation": "startPodiumShift",
       "permission": "TURNSTILE_MODE_SET",
       "notes": "**The operator signs in to a podium** (BO-225; P07 SCN-002 where the scanner picks its access point).",
       "provenance": "contract access.yaml POST /podiums/{podiumId}/shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "End podium shift",
       "operation": "endPodiumShift",
       "permission": "TURNSTILE_MODE_SET",
       "notes": "**The operator signs out of the podium**: sets `logoutAt`.",
       "provenance": "contract access.yaml POST /podium-shifts/{shiftId}/end"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access point direction list.",
   "error": "Could not load. Names which read failed and leaves the access point direction untouched.",
   "emptyFirstRun": "No access point direction yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId and the access point direction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `SCOPE_VIEW`, which `listAccessPoints` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Fully offline. The access point list is in the bundle"
  },
  "apis": [
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAccessPoint",
    "contract": "access",
    "purpose": "Read an access point",
    "trigger": "onAction"
   },
   {
    "operationId": "setTurnstileMode",
    "contract": "access",
    "purpose": "Set the gate's operating mode (required), optionally narrowed by the turnstile mode; the direction is display-only (audit R221)",
    "trigger": "onAction",
    "invalidates": [
     "listAccessPoints"
    ]
   },
   {
    "operationId": "startPodiumShift",
    "contract": "access",
    "purpose": "Start an operator shift on a podium",
    "trigger": "onAction",
    "invalidates": [
     "listAccessPoints"
    ]
   },
   {
    "operationId": "endPodiumShift",
    "contract": "access",
    "purpose": "End an operator shift on a podium",
    "trigger": "onAction",
    "invalidates": [
     "listAccessPoints"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "accessPointId",
     "from": "deepLink"
    },
    {
     "name": "podiumId",
     "from": "session"
    },
    {
     "name": "shiftId",
     "from": "session"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `accessPointId`.",
   "preloaded": [
    "AccessPoint.id",
    "AccessPoint.code",
    "AccessPoint.name",
    "AccessPoint.venueId",
    "AccessPoint.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-002"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetTurnstileMode",
    "component": "modal",
    "trigger": "Save gate mode",
    "body": "**Collects what `setTurnstileMode` sends before it is called.** Required: `operatingMode` (normal, freeFlow, dropArm, closed, podium, maintenance). Optional: `mode` (freeRotation or closed), offered only with normal or podium, since the other four already decide the arm and the server refuses it 400; and `reason`. **Direction is not on this form**: it is fixed per access point and set in the back office (BO-064) with createAccessPoint/updateAccessPoint (decided 28 September, audit R221). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save gate mode",
     "operation": "setTurnstileMode"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "operatingMode",
      "mode",
      "reason"
     ]
    },
    "provenance": "contract access.yaml PUT /access-points/{accessPointId}/mode"
   },
   {
    "id": "formStartPodiumShift",
    "component": "modal",
    "trigger": "Start podium shift",
    "body": "**Collects what `startPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `role`, `accessDeviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Start podium shift",
     "operation": "startPodiumShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "role",
      "accessDeviceId"
     ]
    },
    "provenance": "contract access.yaml POST /podiums/{podiumId}/shifts"
   },
   {
    "id": "formEndPodiumShift",
    "component": "modal",
    "trigger": "End podium shift",
    "body": "**Collects what `endPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `handoverNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "End podium shift",
     "operation": "endPodiumShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "handoverNote"
     ]
    },
    "provenance": "contract access.yaml POST /podium-shifts/{shiftId}/end"
   }
  ],
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-003",
  "name": "Ready to scan",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/ready-to-scan",
   "component": "apps/venue-scanner/src/routes/access/ReadyToScanDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003",
    "SCN-007",
    "SCN-008",
    "SCN-009",
    "SCN-011",
    "SCN-014"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "SCN-007",
     "trigger": "A school party of forty arrives on one booking",
     "provenance": "flow F61 step 4→5"
    },
    {
     "to": "SCN-014",
     "trigger": "Syncs the journal when signal returns",
     "provenance": "flow F06 step 5→6, F19 step 3→4"
    },
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-003 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-003 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "carries": [
      "mediaCode",
      "rightId"
     ],
     "provenance": "derived — SCN-003 declares entryState.params mediaCode, rightId and SCN-003 holds mediaCode, rightId, so an edge into it carries them"
    },
    {
     "to": "PTR-015",
     "trigger": "Reviews usage",
     "provenance": "flow F10 step 4→5",
     "operation": "validateAccess",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "SCN-011",
     "trigger": "Delegated right",
     "carries": [
      "rightId"
     ],
     "provenance": "derived — SCN-011 declares entryState.params rightId and SCN-003 holds rightId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Absorbed SCN-004, SCN-005, SCN-006, SCN-010, SCN-012 on 18 August.** A scanner is one screen the device sits on all day, and an outcome is a state of it — **routing to `/access/admitted` for something gone in 1.5 seconds is a page load per guest**, and at a gate doing 40 a minute that is the whole problem. Every absorbed screen kept its copy as a named state. **Authoring operations removed 24 August**: addBlacklistEntry, removeBlacklistEntry. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "The screen the device sits on all day.",
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
       "kind": "dataTable",
       "label": "Every blacklist entry",
       "bindsTo": "BlacklistEntry",
       "columns": [
        "BlacklistEntry.mediaCode",
        "BlacklistEntry.reason",
        "BlacklistEntry.addedAt",
        "BlacklistEntry.addedByPrincipalId",
        "BlacklistEntry.expiresAt",
        "BlacklistEntry.scopePath"
       ],
       "operation": "listBlacklist",
       "provenance": "contract access.yaml GET /blacklist"
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
      },
      {
       "kind": "secondaryButton",
       "label": "Consume cross region entitlement",
       "operation": "consumeCrossRegionEntitlement",
       "provenance": "contract cross-region.yaml POST /cross-region-entitlements/{rightId}/consume"
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
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A ready scan this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
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
   },
   {
    "id": "formConsumeCrossRegionEntitlement",
    "component": "modal",
    "trigger": "Consume cross region entitlement",
    "body": "**Collects what `consumeCrossRegionEntitlement` sends before it is called.** Required: `id`, `entries`, `scanId`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Consume cross region entitlement",
     "operation": "consumeCrossRegionEntitlement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "entries",
      "scanId",
      "recordedAt"
     ]
    },
    "provenance": "contract cross-region.yaml POST /cross-region-entitlements/{rightId}/consume"
   }
  ],
  "states": {
   "loading": "The ready scan list.",
   "error": "Could not load. Names which read failed and leaves the ready scan untouched.",
   "emptyFirstRun": "No ready scan yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the ready scan are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Same loop, different truth. Amber says so.** Was a separate screen until 18 August, and the screen already had an `offline` state — two places describing one condition is two places to disagree.",
   "admitted": "**Green, and gone in 1.5 seconds.** The absorbed SCN-004. Shows what was admitted and against which right; at a gate doing 40 a minute this is the state the device is in most of the time.",
   "denied": "Denied with the reason and the time of the previous scan. **The reason matters more than the refusal** — a steward has to explain it to somebody standing in front of them. The absorbed SCN-005.",
   "overrideRequired": "A supervisor override, which requires a permission a steward may not hold, and records who, why and when. The absorbed SCN-006.",
   "blocked": "Blacklisted or otherwise barred. **No override is offered on the device** — this is not a judgement a steward makes at a lane. The absorbed SCN-010."
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
    "operationId": "consumeCrossRegionEntitlement",
    "contract": "cross-region",
    "purpose": "Consume entries against a right, locally authoritative",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "listBlacklist",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "verifyAccreditationCredential",
    "contract": "accreditation",
    "purpose": "Verify an accreditation credential presented at a service gate",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mediaCode",
     "from": "deepLink"
    },
    {
     "name": "rightId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mediaCode`, `rightId`.",
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
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-003"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-007",
  "name": "Group admission",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/group-admission",
   "component": "apps/venue-scanner/src/routes/access/GroupAdmissionDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003"
   ],
   "inferred": false,
   "entryFrom": [
    "SCN-003"
   ],
   "notes": "**Reached from SCN-003** — a group is admitted from the scan that found it. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-007 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-007 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "SCN-003",
     "trigger": "The session ends and the device syncs",
     "provenance": "flow F61 step 6→7",
     "operation": "listScans",
     "carries": [
      "mediaCode",
      "rightId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "Partial admission is the normal case, not the error.",
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
       "label": "Validate group access",
       "operation": "validateGroupAccess",
       "provenance": "contract access.yaml POST /access/group-validate"
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
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate access",
       "operation": "validateAccess",
       "provenance": "contract access.yaml POST /access/validate"
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
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A group admission this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
    "provenance": "contract access.yaml POST /access/override"
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
   }
  ],
  "states": {
   "loading": "The group admission list.",
   "error": "Could not load. Names which read failed and leaves the group admission untouched.",
   "emptyFirstRun": "No group admission yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the group admission are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Fully offline. Admits what is valid and states the shortfall"
  },
  "apis": [
   {
    "operationId": "validateGroupAccess",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
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
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
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
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-008",
  "name": "Manual entry",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/manual-entry",
   "component": "apps/venue-scanner/src/routes/access/ManualEntryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003",
    "SCN-009"
   ],
   "inferred": false,
   "entryFrom": [
    "SCN-003"
   ],
   "notes": "**Reached from SCN-003** — manual entry is what a failed scan falls back to. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "SCN-009",
     "trigger": "The ticket is found and its history read",
     "provenance": "flow F62 step 1→2",
     "operation": "lookupTicket"
    },
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-008 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-008 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "carries": [
      "mediaCode",
      "rightId"
     ],
     "provenance": "derived — SCN-003 declares entryState.params mediaCode, rightId and SCN-008 holds mediaCode, rightId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "Damaged media, dead phone battery, printed slip.",
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
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupTicket",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "scanTarget",
       "derived": true,
       "impliedBy": "listScans",
       "notes": "**A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or explain something.",
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
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
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
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A manual entry this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
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
   "loading": "The manual entry list.",
   "error": "Could not load. Names which read failed and leaves the manual entry untouched.",
   "emptyFirstRun": "No manual entry yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the manual entry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Searches the bundle only. A reference issued after the last sync will not be found, and the screen says so rather than denying"
  },
  "apis": [
   {
    "operationId": "lookupTicket",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
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
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
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
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-009",
  "name": "Ticket lookup",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/ticket-lookup",
   "component": "apps/venue-scanner/src/routes/access/TicketLookupDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003"
   ],
   "inferred": false,
   "entryFrom": [
    "SCN-003",
    "SCN-008"
   ],
   "notes": "**Reached from SCN-003** — a lookup answers a scan that did not resolve. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely. **Also reached from SCN-008 Manual entry** — flow F62 *a ticket will not scan* goes scan, manual entry, lookup, and declaring the navigation non-inferred is what turned that missing edge from a warning into a failure.",
   "transitions": [
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-009 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-009 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "SCN-003",
     "trigger": "It is valid",
     "provenance": "flow F62 step 2→3",
     "carries": [
      "mediaCode",
      "rightId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "Reads. Does not admit, does not decrement.",
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
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupTicket",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "scanTarget",
       "derived": true,
       "impliedBy": "listScans",
       "notes": "**A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or explain something.",
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
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
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
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A ticket lookup this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
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
   "loading": "The ticket lookup list.",
   "error": "Could not load. Names which read failed and leaves the ticket lookup untouched.",
   "emptyFirstRun": "No ticket lookup yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the ticket lookup are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Bundle only, and the bundle age is shown beside the results"
  },
  "apis": [
   {
    "operationId": "lookupTicket",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
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
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
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
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-009"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-011",
  "name": "Delegated right",
  "module": "Access",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/delegated-right",
   "component": "apps/venue-scanner/src/routes/access/DelegatedRightDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003"
   ],
   "inferred": false,
   "entryFrom": [
    "SCN-003"
   ],
   "notes": "**Reached from SCN-003** — a delegated right is checked against the scan presenting it. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-011 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-011 holds none of them, so the edge carries nothing and SCN-002 opens cold"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "carries": [
      "rightId"
     ],
     "provenance": "derived — SCN-003 declares entryState.params mediaCode, rightId and SCN-011 holds rightId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getCrossRegionEntitlement` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "A ticket issued in another cell, redeemed here.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The cross region entitlement",
       "bindsTo": "CrossRegionEntitlement",
       "columns": [
        "CrossRegionEntitlement.id",
        "CrossRegionEntitlement.rightId",
        "CrossRegionEntitlement.ticketId",
        "CrossRegionEntitlement.guestLinkId",
        "CrossRegionEntitlement.issuingCellName",
        "CrossRegionEntitlement.consumingCellName",
        "CrossRegionEntitlement.mediaCodes",
        "CrossRegionEntitlement.validFrom",
        "CrossRegionEntitlement.validTo",
        "CrossRegionEntitlement.admissionRulesId",
        "CrossRegionEntitlement.venueId",
        "CrossRegionEntitlement.entriesAllowed",
        "CrossRegionEntitlement.entriesConsumed",
        "CrossRegionEntitlement.status",
        "CrossRegionEntitlement.lastConsumedAt",
        "CrossRegionEntitlement.lastReconciledAt"
       ],
       "operation": "getCrossRegionEntitlement",
       "provenance": "contract cross-region.yaml GET /cross-region-entitlements/{rightId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Consume cross region entitlement",
       "operation": "consumeCrossRegionEntitlement",
       "provenance": "contract cross-region.yaml POST /cross-region-entitlements/{rightId}/consume"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The delegated right, read by `getCrossRegionEntitlement`.",
   "error": "Could not load. Names which read failed and leaves the delegated right untouched.",
   "emptyFirstRun": "No delegated right yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TICKET_LOOKUP`, which `getCrossRegionEntitlement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available offline.** A delegated right issued in another region cannot be verified from a local bundle, and admitting on trust is how a pass gets used twice in two countries"
  },
  "apis": [
   {
    "operationId": "getCrossRegionEntitlement",
    "contract": "cross-region",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "consumeCrossRegionEntitlement",
    "contract": "cross-region",
    "purpose": "Consume entries against a right, locally authoritative",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "rightId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `rightId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-011"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formConsumeCrossRegionEntitlement",
    "component": "modal",
    "trigger": "Consume cross region entitlement",
    "body": "**Collects what `consumeCrossRegionEntitlement` sends before it is called.** Required: `id`, `entries`, `scanId`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Consume cross region entitlement",
     "operation": "consumeCrossRegionEntitlement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "entries",
      "scanId",
      "recordedAt"
     ]
    },
    "provenance": "contract cross-region.yaml POST /cross-region-entitlements/{rightId}/consume"
   }
  ],
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-013",
  "name": "Offline journal",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/offline-journal",
   "component": "apps/venue-scanner/src/routes/access/OfflineJournalDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003",
    "SCN-014"
   ],
   "inferred": false,
   "entryFrom": [
    "SCN-002",
    "SCN-015"
   ],
   "notes": "**Reached from SCN-002** — the journal is reached from the access point it belongs to. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "SCN-014",
     "trigger": "The network returns and the journal posts",
     "provenance": "flow F63 step 2→3",
     "operation": "listScans"
    },
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-013 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-013 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "carries": [
      "mediaCode",
      "rightId"
     ],
     "provenance": "derived — SCN-003 declares entryState.params mediaCode, rightId and SCN-013 holds mediaCode, rightId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "What the device decided, before anyone confirmed it.",
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
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
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
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A offline journal this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
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
   "loading": "The offline journal list.",
   "error": "Could not load. Names which read failed and leaves the offline journal untouched.",
   "emptyFirstRun": "No offline journal yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the offline journal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "The journal is the offline record. It is why an offline admit is recoverable"
  },
  "apis": [
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
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
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
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
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-013"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-014",
  "name": "Sync & reconciliation",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/sync-reconciliation",
   "component": "apps/venue-scanner/src/routes/access/SyncReconciliationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003"
   ],
   "inferred": false,
   "fromFlows": true,
   "entryFrom": [
    "SCN-003",
    "SCN-013"
   ],
   "notes": "**Reached from SCN-013** — reconciliation follows the journal it reconciles. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-014 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-014 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "carries": [
      "mediaCode",
      "rightId"
     ],
     "provenance": "derived — SCN-003 declares entryState.params mediaCode, rightId and SCN-014 holds mediaCode, rightId, so an edge into it carries them"
    },
    {
     "to": "ADM-003",
     "trigger": "Reconciliation confirms it",
     "provenance": "flow F19 step 4→5",
     "operation": "syncScans",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: ADM-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listSyncRejections` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "The screen nobody designs and everybody needs.",
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
       "operation": "listSyncRejections",
       "notes": "Sends `?workstationId=` to `listSyncRejections`.",
       "provenance": "contract orders.yaml GET /sync/rejections"
      },
      {
       "kind": "selectField",
       "label": "Kind",
       "operation": "listSyncRejections",
       "notes": "Sends `?kind=` to `listSyncRejections`.",
       "provenance": "contract orders.yaml GET /sync/rejections"
      },
      {
       "kind": "toggle",
       "label": "Resolved",
       "operation": "listSyncRejections",
       "notes": "Sends `?resolved=` to `listSyncRejections`.",
       "provenance": "contract orders.yaml GET /sync/rejections"
      },
      {
       "kind": "dataTable",
       "label": "Every sync rejection",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
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
       "impliedBy": "syncScans",
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
       "label": "The selected sync rejection",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId",
        "SyncRejection.resolution",
        "SyncRejection.resolvedRecordId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
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
       "label": "Sync orders",
       "operation": "syncOrders",
       "provenance": "contract orders.yaml POST /sync/orders"
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
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A sync reconciliation this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
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
    "id": "formSyncOrders",
    "component": "modal",
    "trigger": "Sync orders",
    "body": "**Collects what `syncOrders` sends before it is called.** Required: `deviceId`, `orders`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sync orders",
     "operation": "syncOrders"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "deviceId",
      "orders"
     ]
    },
    "provenance": "contract orders.yaml POST /sync/orders"
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
   "loading": "The sync reconciliation list.",
   "error": "Could not load. Names which read failed and leaves the sync reconciliation untouched.",
   "emptyFirstRun": "No sync reconciliation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on workstationId, kind, resolved and the sync reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Not applicable. This screen exists to end the offline period"
  },
  "apis": [
   {
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "listSyncRejections",
    "contract": "orders",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
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
     "listSyncRejections"
    ]
   },
   {
    "operationId": "syncOrders",
    "contract": "orders",
    "purpose": "Replay orders recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   },
   {
    "operationId": "validateAccess",
    "contract": "access",
    "purpose": "Validate media at an access point and admit or deny",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   },
   {
    "operationId": "validateGroupAccess",
    "contract": "access",
    "purpose": "Admit a group on one read",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "SyncRejection.id",
    "SyncRejection.workstationId",
    "SyncRejection.kind",
    "SyncRejection.recordedAt",
    "SyncRejection.rejectedAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-014"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SCN-015",
  "name": "Offline package",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/offline-package",
   "component": "apps/venue-scanner/src/routes/access/OfflinePackageDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003",
    "SCN-013"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "SCN-013",
     "trigger": "Scans journal locally while the network is gone",
     "provenance": "flow F63 step 1→2",
     "operation": "getOfflinePackage"
    },
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-015 holds none of them, so the edge carries nothing and SCN-001 opens cold"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-015 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "SCN-003",
     "trigger": "Waits at the ready screen",
     "provenance": "flow F06 step 3→4, F61 step 3→4",
     "operation": "getOfflinePackage",
     "carries": [
      "mediaCode",
      "rightId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "Rule changes land here, not instantly.",
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
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
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
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A offline package this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
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
   "loading": "The offline package list.",
   "error": "Could not load. Names which read failed and leaves the offline package untouched.",
   "emptyFirstRun": "No offline package yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the offline package are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cannot refresh. The existing bundle continues to be used and its age is shown"
  },
  "apis": [
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
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
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
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
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-015"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
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
 "consumeCrossRegionEntitlement": {
  "method": "POST",
  "path": "/cross-region-entitlements/{rightId}/consume",
  "contract": "cross-region",
  "summary": "Consume entries against a right, locally authoritative",
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
  "responds": "CrossRegionEntitlement"
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
 "endPodiumShift": {
  "method": "POST",
  "path": "/podium-shifts/{shiftId}/end",
  "contract": "access",
  "summary": "End an operator shift on a podium",
  "permission": "TURNSTILE_MODE_SET",
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
  "responds": "AccessPodiumShift"
 },
 "getAccessPoint": {
  "method": "GET",
  "path": "/access-points/{accessPointId}",
  "contract": "access",
  "summary": "Read an access point",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessPoint"
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
 "listAccessPoints": {
  "method": "GET",
  "path": "/access-points",
  "contract": "access",
  "summary": "List access points",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
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
 "listBlacklist": {
  "method": "GET",
  "path": "/blacklist",
  "contract": "access",
  "summary": "List blacklisted media",
  "permission": "SCOPE_VIEW",
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
 "listSyncRejections": {
  "method": "GET",
  "path": "/sync/rejections",
  "contract": "orders",
  "summary": "Entries the server refused",
  "permission": "ORDER_VIEW",
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
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "resolved",
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
 "resolvePermissions": {
  "method": "POST",
  "path": "/permissions/resolve",
  "contract": "identity",
  "summary": "Simulate a principal's effective permissions",
  "permission": "PERMISSION_VIEW",
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
 "setTurnstileMode": {
  "method": "PUT",
  "path": "/access-points/{accessPointId}/mode",
  "contract": "access",
  "summary": "Set the operating mode of an access point",
  "permission": "TURNSTILE_MODE_SET",
  "offlineCapable": true,
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
  "responds": "AccessPoint"
 },
 "startPodiumShift": {
  "method": "POST",
  "path": "/podiums/{podiumId}/shifts",
  "contract": "access",
  "summary": "Start an operator shift on a podium",
  "permission": "TURNSTILE_MODE_SET",
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
  "responds": "AccessPodiumShift"
 },
 "syncOrders": {
  "method": "POST",
  "path": "/sync/orders",
  "contract": "orders",
  "summary": "Replay orders recorded offline",
  "permission": "ORDER_CREATE",
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
  "responds": "OrderSyncResult"
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
 "AccessPodiumShift": {
  "type": "object",
  "x-ticvai-persistence": "access.podium_shift",
  "description": "One operator session on a podium or device: who, in what role, where, and login and logout times. Logout is null while the shift is open (declared 29 September, data-model close-out DM1) Written by startPodiumShift and endPodiumShift; an identity sign-out ends the open shift (decided 29 September, writers pass).",
  "required": [
   "id",
   "venueId",
   "operatorPrincipalId",
   "loginAt",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "role": {
    "type": "string",
    "nullable": true
   },
   "podiumId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accessDeviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Device used (access.access_device)"
   },
   "loginAt": {
    "type": "string",
    "format": "date-time"
   },
   "logoutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   }
  }
 },
 "AccessPoint": {
  "x-ticvai-persistence": "access.access_point",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "operatingMode",
   "isActive"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "externalCredentialSources": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExternalCredentialSourceList"
     }
    ],
    "description": "BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"
   },
   "scanAnomalyRules": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ScanAnomalyRuleList"
     }
    ],
    "description": "BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"
   },
   "operatingMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "default": "normal",
    "description": "**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"
   },
   "vehicleLocationCapture": {
    "type": "boolean",
    "default": false,
    "description": "BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"
   },
   "mode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TurnstileMode"
     }
    ],
    "nullable": true,
    "description": "Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"
   },
   "direction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Direction"
     }
    ],
    "description": "**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"
   },
   "antiPassbackEnabled": {
    "type": "boolean"
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false,
    "description": "Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."
   },
   "driver": {
    "type": "string",
    "nullable": true,
    "description": "Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"
   },
   "geofence": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointGeofence"
     }
    ],
    "nullable": true,
    "description": "Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "AccessPointGeofence": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n",
  "required": [
   "enforcement"
  ],
  "properties": {
   "latitude": {
    "type": "number"
   },
   "longitude": {
    "type": "number"
   },
   "radiusMetres": {
    "type": "integer",
    "minimum": 5,
    "maximum": 5000
   },
   "enforcement": {
    "type": "string",
    "enum": [
     "off",
     "warn",
     "deny"
    ],
    "description": "`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"
   },
   "allowProximityBeacon": {
    "type": "boolean",
    "description": "Accept a BLE proximity assertion in place of GPS. Better indoors."
   }
  }
 },
 "AccessPointOperatingMode": {
  "type": "string",
  "description": "BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n",
  "enum": [
   "normal",
   "freeFlow",
   "dropArm",
   "closed",
   "podium",
   "maintenance"
  ]
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
 "BlacklistEntry": {
  "x-ticvai-persistence": "access.blacklist",
  "type": "object",
  "required": [
   "mediaCode",
   "reason",
   "addedAt",
   "addedByPrincipalId"
  ],
  "properties": {
   "mediaCode": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "**Unique within the tenant** (decided 28 September, audit R108): one entry per code. `addBlacklistEntry` refuses a second entry with `409 duplicate-code`. **One code space for both lists** (decided 29 September, writers pass): a code on the blacklist cannot also be whitelisted; adding it to the other list is the same `409 duplicate-code`. Move a code between lists by removing and re-adding it."
   },
   "reason": {
    "type": "string"
   },
   "addedAt": {
    "type": "string",
    "format": "date-time"
   },
   "addedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "listType": {
    "type": "string",
    "enum": [
     "blacklist",
     "whitelist"
    ],
    "default": "blacklist",
    "description": "A blacklist entry refuses the media; a whitelist entry is an approved exception to a restriction (added 29 September, data-model close-out DM1)."
   },
   "disableScope": {
    "type": "string",
    "enum": [
     "entireCredential",
     "venueAccess",
     "attractionAccess",
     "reEntry",
     "fastPass",
     "specificEntitlement"
    ],
    "default": "entireCredential",
    "description": "What the entry disables (added 29 September, data-model close-out DM1)."
   },
   "distributedTo": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "centralPlatform",
      "venueEdge",
      "onlineGates",
      "offlineRevocationPackage"
     ]
    },
    "description": "Where the restriction has been distributed so far, as `listCredentialDisableBlacklist` returns it (added 29 September, data-model close-out DM1)."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "CreateOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "venueId",
   "channel",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for an anonymous sale. Identity and entitlement are separate."
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells."
   },
   "catalogueBundleVersion": {
    "type": "string",
    "description": "The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreatePaymentRequest": {
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."
   },
   "returnUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true,
    "description": "Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
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
    "format": "uuid"
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
 "ExternalCredentialSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n",
  "items": {
   "type": "object",
   "properties": {
    "kind": {
     "type": "string",
     "enum": [
      "hotelRoomCard",
      "corporateBadge",
      "cityPass",
      "transitCard",
      "partnerToken"
     ]
    },
    "providerName": {
     "type": "string"
    },
    "endpoint": {
     "type": "string"
    },
    "credentialRef": {
     "type": "string"
    },
    "grantsProductId": {
     "type": "string",
     "format": "uuid"
    }
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
 "OfflineOrder": {
  "x-ticvai-persistence": "none — client-side journal, not server storage",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderRequest"
   },
   {
    "type": "object",
    "required": [
     "sequence",
     "payments"
    ],
    "properties": {
     "sequence": {
      "type": "integer",
      "minimum": 1,
      "description": "Monotonic per device. Processed in this order."
     },
     "payments": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CreatePaymentRequest"
      }
     }
    }
   }
  ]
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
 "OrderSyncResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "accepted",
   "results"
  ],
  "properties": {
   "accepted": {
    "type": "integer"
   },
   "stoppedAtSequence": {
    "type": "integer",
    "nullable": true,
    "description": "First entry that hit a **transient** failure (SD-028, 29 September): a refusal on the merits no longer stops the batch. Null when every entry was accepted, duplicate or quarantined. The client retries from here and never past it.\n"
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
       "type": "string",
       "format": "uuid",
       "description": "The `OfflineOrder.id` this result is about."
      },
      "sequence": {
       "type": "integer"
      },
      "status": {
       "type": "string",
       "enum": [
        "accepted",
        "duplicate",
        "rejected",
        "blockedByRejection"
       ],
       "description": "`rejected`: refused on its merits and quarantined in `sync.rejection`; the batch continues. `blockedByRejection`: depends on a rejected entry for the same order (a void, a refund, a later payment) and is quarantined with it (SD-028, 29 September)."
      },
      "orderNumber": {
       "type": "string",
       "nullable": true
      },
      "priceVariance": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Posted to the variance account. Not surfaced to the cashier."
      },
      "varianceExceedsThreshold": {
       "type": "boolean",
       "description": "True when review is required per the venue's variance threshold."
      },
      "rejectionId": {
       "type": "string",
       "nullable": true,
       "description": "For a `rejected` or `blockedByRejection` entry, the `sync.rejection` row it was quarantined into (SD-028). The batch carried on past it."
      },
      "error": {
       "$ref": "../shared/common.yaml#/components/schemas/Problem"
      }
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
 "PermissionSet": {
  "type": "array",
  "items": {
   "$ref": "#/components/schemas/Permission"
  },
  "uniqueItems": true
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
 "ScanAnomalyRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n",
  "items": {
   "type": "object",
   "properties": {
    "rule": {
     "type": "string",
     "enum": [
      "simultaneousEntry",
      "impossibleTravelTime",
      "rapidReentry",
      "sharedDevice",
      "velocityBreach"
     ]
    },
    "action": {
     "type": "string",
     "enum": [
      "log",
      "flag",
      "requireSupervisor",
      "deny"
     ]
    },
    "thresholdSeconds": {
     "type": "integer",
     "nullable": true
    }
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
 "ScopedPermissions": {
  "type": "object",
  "description": "Permissions effective at a given scope path, after deny resolution. Clients filter navigation on this and never compute permissions themselves.\n",
  "required": [
   "scopePath",
   "permissions"
  ],
  "properties": {
   "scopePath": {
    "type": "string",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$"
   },
   "permissions": {
    "$ref": "#/components/schemas/PermissionSet"
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
 "SyncRejection": {
  "x-ticvai-persistence": "sync.rejection",
  "type": "object",
  "required": [
   "id",
   "workstationId",
   "kind",
   "rejectedAt",
   "problem"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "order",
     "payment",
     "refund",
     "void",
     "scan"
    ]
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "rejectedAt": {
    "type": "string",
    "format": "date-time"
   },
   "problem": {
    "$ref": "../shared/common.yaml#/components/schemas/Problem"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "resolution": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "enum": [
     "posted",
     "voided",
     "refunded"
    ],
    "description": "What `resolveSyncRejection` recorded. Null while the rejection waits."
   },
   "resolvedRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The order, void or refund the resolution produced — what stops the entry being posted twice."
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
 "TurnstileMode": {
  "type": "string",
  "description": "**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n",
  "enum": [
   "freeRotation",
   "closed"
  ]
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
