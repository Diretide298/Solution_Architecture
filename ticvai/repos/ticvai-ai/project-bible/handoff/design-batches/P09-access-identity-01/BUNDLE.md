# P09-access-identity-01 — P09 · Access & Identity

**3 screens · 18 operations · 17 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ROLE_MANAGE, SESSION_FORCE_LOGOUT, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-001` | Platform Login / MFA | listDetail | 12 | 6 | — |
| `ADM-020` | Platform User Directory | listDetail | 4 | 2 | — |
| `ADM-021` | Platform Role Management | listDetail | 2 | 1 | — |

## Thin screens in this batch

**ADM-021 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-001",
  "name": "Platform Login / MFA",
  "module": "Access & Identity",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C35",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/platform-login-mfa",
   "component": "apps/ticvai-web/src/routes/general/PlatformLoginMfaList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-002",
    "ADM-004"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-001 holds none of them. The edge carries nothing: ADM-001 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-004",
     "trigger": "Platform Audit Log",
     "provenance": "derived — ADM-004 declares entryState.params decisionRecordId and ADM-001 holds none of them. The edge carries nothing: ADM-004 finds decisionRecordId (listAiInteractions) itself, and ADM-004 opens on its own"
    },
    {
     "to": "PTR-001",
     "trigger": "A partner user signs in through the same door",
     "provenance": "flow F104 step 3→4",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "challengeId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listActiveSessions` reads the population and `getCurrentSession` reads one of them — list, select, act",
  "purpose": "Get someone into the app, fast, on a device that may be shared.",
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
       "operation": "listActiveSessions",
       "notes": "Sends `?venueId=` to `listActiveSessions`.",
       "provenance": "contract identity.yaml GET /auth/sessions"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listActiveSessions",
       "notes": "Sends `?principalId=` to `listActiveSessions`.",
       "provenance": "contract identity.yaml GET /auth/sessions"
      },
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listActiveSessions",
       "notes": "Sends `?workstationId=` to `listActiveSessions`.",
       "provenance": "contract identity.yaml GET /auth/sessions"
      },
      {
       "kind": "dataTable",
       "label": "Every active session",
       "bindsTo": "ActiveSession",
       "columns": [
        "ActiveSession.sessionId",
        "ActiveSession.principalId",
        "ActiveSession.principalName",
        "ActiveSession.roleId",
        "ActiveSession.roleName",
        "ActiveSession.workstationId",
        "ActiveSession.workstationName",
        "ActiveSession.venueId",
        "ActiveSession.ipAddress",
        "ActiveSession.deviceInfo",
        "ActiveSession.hasOpenShift",
        "ActiveSession.mfaSatisfied"
       ],
       "operation": "listActiveSessions",
       "provenance": "contract identity.yaml GET /auth/sessions"
      },
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
       "label": "The selected active session",
       "bindsTo": "ActiveSession",
       "columns": [
        "ActiveSession.status",
        "ActiveSession.sessionId",
        "ActiveSession.principalId",
        "ActiveSession.principalName",
        "ActiveSession.roleId",
        "ActiveSession.roleName",
        "ActiveSession.workstationId",
        "ActiveSession.workstationName",
        "ActiveSession.venueId",
        "ActiveSession.ipAddress",
        "ActiveSession.deviceInfo",
        "ActiveSession.hasOpenShift",
        "ActiveSession.mfaSatisfied",
        "ActiveSession.startedAt",
        "ActiveSession.lastSeenAt"
       ],
       "operation": "listActiveSessions",
       "provenance": "contract identity.yaml GET /auth/sessions"
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
       "notes": "Shown only in the mfaRequired state, after `login`, for the authenticator-app code or the emailed code (decided 28 September, audit R135, R126 (5)).",
       "provenance": "contract identity.yaml POST /auth/mfa/challenge/{challengeId}/verify"
      },
      {
       "kind": "primaryButton",
       "label": "Verify",
       "operation": "verifyMfaChallenge",
       "notes": "Completes sign-in; the session is usable only after it. Five wrong codes lock step-up (429 step-up-locked, audit R126 (6)).",
       "provenance": "contract identity.yaml POST /auth/mfa/challenge/{challengeId}/verify"
      },
      {
       "kind": "secondaryButton",
       "label": "Email me a code instead",
       "operation": "createMfaChallenge",
       "notes": "The fallback: a new challenge with the email method (`emailOtp`) instead of the authenticator app (decided 28 September, audit R126 (5)).",
       "provenance": "contract identity.yaml POST /auth/mfa/challenge"
      },
      {
       "kind": "secondaryButton",
       "label": "Enrol MFA method",
       "operation": "enrolMfaMethod",
       "notes": "**A platform operator must hold a method to sign in** — every platform-staff permission is in the MFA floor (decided 28 September, audit R135). On a first sign-in with no method enrolled, the screen goes to enrolment before anything else. The kind picker offers only the authenticator app (`totp`) and email (`emailOtp`); any other kind is refused 422 mfa-kind-not-allowed (audit R126 (5)).",
       "provenance": "contract identity.yaml POST /auth/mfa/methods"
      },
      {
       "kind": "secondaryButton",
       "label": "Confirm enrolment",
       "operation": "verifyMfaEnrolment",
       "notes": "The method is not active until the first code is verified. Recovery codes are shown once, from the enrolment response, and never again.",
       "provenance": "contract identity.yaml POST /auth/mfa/methods/{methodId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove MFA method",
       "operation": "removeMfaMethod",
       "notes": "Removing the last active method is refused 409 while the principal holds a permission that requires MFA — for platform staff, always (decided 28 September, audit R135).",
       "provenance": "contract identity.yaml DELETE /auth/mfa/methods/{methodId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Force logout",
       "operation": "forceLogout",
       "provenance": "contract identity.yaml POST /auth/sessions/{sessionId}/force-logout"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke all sessions",
       "operation": "revokeAllSessions",
       "provenance": "contract identity.yaml POST /auth/sessions/revoke-all"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formEnrolMfaMethod",
    "component": "modal",
    "trigger": "Enrol MFA method",
    "body": "**Collects what `enrolMfaMethod` sends before it is called.** Required: `kind` — the authenticator app (`totp`) or email (`emailOtp`) only (decided 28 September, audit R126 (5)). Optional: `target` (the email address for `emailOtp`). The response carries the secret or QR for the app and the recovery codes, shown once. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Enrol",
     "operation": "enrolMfaMethod"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "target"
     ]
    },
    "provenance": "contract identity.yaml POST /auth/mfa/methods"
   },
   {
    "id": "formVerifyMfaEnrolment",
    "component": "modal",
    "trigger": "Confirm enrolment",
    "body": "**Collects what `verifyMfaEnrolment` sends before it is called.** Required: `code`, the first code from the new method. The method is active only after this. Dismissing sends nothing; the method stays pending.",
    "confirm": {
     "label": "Confirm enrolment",
     "operation": "verifyMfaEnrolment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code"
     ]
    },
    "provenance": "contract identity.yaml POST /auth/mfa/methods/{methodId}"
   },
   {
    "id": "confirmRemoveMfaMethod",
    "component": "confirmDialog",
    "trigger": "Remove MFA method",
    "body": "**Names the method being removed and what remains.** Removing the last active method is refused 409 while the principal holds a permission that requires MFA (decided 28 September, audit R135); the dialog says so before it is sent rather than after.",
    "confirm": {
     "label": "Remove",
     "operation": "removeMfaMethod"
    },
    "provenance": "contract identity.yaml DELETE /auth/mfa/methods/{methodId}"
   },
   {
    "id": "confirmForceLogout",
    "component": "confirmDialog",
    "trigger": "Force logout",
    "body": "**Names what `forceLogout` changes and what it leaves alone**, in the consequence rather than the verb. A platform login mfa this affects should be identified in the dialog, not just counted. **Collects what `forceLogout` sends before it is called.** Required: `reason`.",
    "provenance": "contract identity.yaml POST /auth/sessions/{sessionId}/force-logout"
   },
   {
    "id": "confirmRevokeAllSessions",
    "component": "confirmDialog",
    "trigger": "Revoke all sessions",
    "body": "**Names what `revokeAllSessions` changes and what it leaves alone**, in the consequence rather than the verb. A platform login mfa this affects should be identified in the dialog, not just counted. **Collects what `revokeAllSessions` sends before it is called.** Required: `reason`, `stepUpToken`. Optional: `venueId`, `excludeSelf`.",
    "provenance": "contract identity.yaml POST /auth/sessions/revoke-all"
   },
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
  "states": {
   "loading": "The platform login mfa list.",
   "error": "Could not load. Names which read failed and leaves the platform login mfa untouched.",
   "emptyFirstRun": "No platform login mfa yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, workstationId and the platform login mfa are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `SESSION_FORCE_LOGOUT`, which `listActiveSessions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "mfaRequired": "**Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any platform-staff permission, or one the tenant added), so after `login` the screen calls `createMfaChallenge` and asks for the authenticator code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says so. A principal with no enrolled method is sent to enrol first (decided 28 September, audit R135, R126).",
   "mfaEnrolmentRequired": "**First sign-in, no method yet.** A platform operator always requires MFA (every `PLATFORM_*` permission is in the floor), so one with no enrolled method cannot finish signing in: the screen enrols the authenticator app (`enrolMfaMethod`, email as the fallback), confirms it with the first code (`verifyMfaEnrolment`), then continues to the mfaRequired step (decided 28 September, audit R135, R126 (5))."
  },
  "apis": [
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
   },
   {
    "operationId": "enrolMfaMethod",
    "contract": "identity",
    "purpose": "A platform operator's first method, at first sign-in — authenticator app, or email as the fallback (decided 28 September, audit R135, R126 (5))",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "verifyMfaEnrolment",
    "contract": "identity",
    "purpose": "Activates the enrolled method with its first code",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "removeMfaMethod",
    "contract": "identity",
    "purpose": "Remove a method; the last one is refused 409 while a listed permission is held (audit R135)",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "login",
    "contract": "identity",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "forceLogout",
    "contract": "identity",
    "purpose": "Supervisor termination of an abandoned session",
    "trigger": "onAction",
    "invalidates": [
     "listActiveSessions"
    ]
   },
   {
    "operationId": "getCurrentSession",
    "contract": "identity",
    "purpose": "Current session and effective permissions",
    "trigger": "onLoad"
   },
   {
    "operationId": "listActiveSessions",
    "contract": "identity",
    "purpose": "List active sessions",
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
    "operationId": "revokeAllSessions",
    "contract": "identity",
    "purpose": "Revoke every session in scope",
    "trigger": "onAction",
    "invalidates": [
     "listActiveSessions"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "challengeId",
     "from": "navigation"
    },
    {
     "name": "methodId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "ActiveSession.status",
    "ActiveSession.sessionId",
    "ActiveSession.principalId",
    "ActiveSession.principalName",
    "ActiveSession.roleId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-001"
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
  "id": "ADM-020",
  "name": "Platform User Directory",
  "module": "Access & Identity",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C56",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/platform-user-directory",
   "component": "apps/ticvai-web/src/routes/general/PlatformUserDirectoryList.tsx",
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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-020 holds none of them. The edge carries nothing: ADM-001 finds challengeId (createMfaChallenge), methodId (enrolMfaMethod) itself, and ADM-001 opens on its own"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-020 holds none of them. The edge carries nothing: ADM-020 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPrincipals` reads the population and `getPrincipal` reads one of them — list, select, act",
  "purpose": "Find the right one quickly, and act on it without opening it.",
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The platform user list.",
   "error": "Could not load. Names which read failed and leaves the platform user untouched.",
   "emptyFirstRun": "No platform user yet. Offers Create principal (`createPrincipal`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on scopePath, isActive and the platform user are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrincipals",
    "contract": "identity",
    "purpose": "from page inventory",
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
    "operationId": "getPrincipal",
    "contract": "identity",
    "purpose": "Read a principal",
    "trigger": "onLoad"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-020"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
  "id": "ADM-021",
  "name": "Platform Role Management",
  "module": "Access & Identity",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C56",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/platform-role-management",
   "component": "apps/ticvai-web/src/routes/general/PlatformRoleManagementForm.tsx",
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
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-021 holds none of them. The edge carries nothing: ADM-001 finds challengeId (createMfaChallenge), methodId (enrolMfaMethod) itself, and ADM-001 opens on its own"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-021 holds none of them. The edge carries nothing: ADM-021 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listRoles` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find platform role management for this venue.",
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
   "loading": "The platform role list.",
   "error": "Could not load. Names which read failed and leaves the platform role untouched.",
   "emptyFirstRun": "No platform role yet. Offers Create role (`createRole`).",
   "emptyNoResults": "Never shown: `listRoles` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRoles",
    "contract": "identity",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRole",
    "contract": "identity",
    "purpose": "from page inventory",
    "trigger": "onAction"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-021"
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
 "enrolMfaMethod": {
  "method": "POST",
  "path": "/auth/mfa/methods",
  "contract": "identity",
  "summary": "Enrol an MFA method",
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
  "responds": "MfaEnrolment"
 },
 "forceLogout": {
  "method": "POST",
  "path": "/auth/sessions/{sessionId}/force-logout",
  "contract": "identity",
  "summary": "Supervisor termination of an abandoned session",
  "permission": "SESSION_FORCE_LOGOUT",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "sessionId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": null
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
 "listActiveSessions": {
  "method": "GET",
  "path": "/auth/sessions",
  "contract": "identity",
  "summary": "List active sessions",
  "permission": "SESSION_FORCE_LOGOUT",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "workstationId",
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
 "removeMfaMethod": {
  "method": "DELETE",
  "path": "/auth/mfa/methods/{methodId}",
  "contract": "identity",
  "summary": "Remove an MFA method",
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
 "revokeAllSessions": {
  "method": "POST",
  "path": "/auth/sessions/revoke-all",
  "contract": "identity",
  "summary": "Revoke every session in scope",
  "permission": "SESSION_FORCE_LOGOUT",
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
 "verifyMfaEnrolment": {
  "method": "POST",
  "path": "/auth/mfa/methods/{methodId}",
  "contract": "identity",
  "summary": "Complete enrolment",
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
  "responds": "MfaMethod"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ActiveSession": {
  "x-ticvai-persistence": "none — Redis session registry",
  "type": "object",
  "required": [
   "sessionId",
   "principalId",
   "status",
   "startedAt",
   "lastSeenAt"
  ],
  "properties": {
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SessionStatus"
     }
    ],
    "description": "**A registry that only holds live sessions cannot answer why one ended.** Kept on the record so a supervisor asking *what happened to till 4* gets `terminated` or `expired` rather than an absence.\n"
   },
   "sessionId": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "principalName": {
    "type": "string"
   },
   "roleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "roleName": {
    "type": "string",
    "nullable": true
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "workstationName": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ipAddress": {
    "type": "string",
    "nullable": true
   },
   "deviceInfo": {
    "type": "string",
    "nullable": true
   },
   "hasOpenShift": {
    "type": "boolean",
    "description": "Revoking this session leaves cash unreconciled."
   },
   "mfaSatisfied": {
    "type": "boolean"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastSeenAt": {
    "type": "string",
    "format": "date-time"
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
 "MfaEnrolment": {
  "x-ticvai-persistence": "none — transient",
  "type": "object",
  "required": [
   "methodId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
   },
   "methodId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MfaKind"
   },
   "secret": {
    "type": "string",
    "nullable": true,
    "description": "TOTP shared secret. Returned once, at enrolment, and never again."
   },
   "qrCodeUri": {
    "type": "string",
    "nullable": true
   },
   "recoveryCodes": {
    "type": "array",
    "description": "Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n",
    "items": {
     "type": "string"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
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
 "SessionStatus": {
  "type": "string",
  "description": "**The life of one signed-in session, which is not the life of a shift.** A shift holds the float and survives a break; a session holds the person and does not. `ShiftStatus.suspended` is where a break lives — *break cover; float intact, workstation released* — and the release of the workstation is exactly why the session ends rather than pausing: the next person opens their own.\n**One principal, one active session per workstation.** Enforced by the `ActiveSession` registry rather than by a state, because it is a fact about the set of sessions and not about any one of them.\n",
  "enum": [
   "active",
   "signedOut",
   "terminated",
   "expired"
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
