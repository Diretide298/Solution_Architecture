# P10-access-account-01 — P10 · Access & Account

**5 screens · 29 operations · 27 schemas · 12 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 12 permissions apply here:
  `CREDIT_MANAGE, CREDIT_OVERRIDE, DEVELOPER_MANAGE, DEVELOPER_VIEW, GUEST_VIEW, MARKETING_SEND, ORDER_VIEW, PARTNER_MANAGE, PERMISSION_GRANT, PERMISSION_VIEW, SESSION_FORCE_LOGOUT, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-001` | Partner Login / MFA | listDetail | 13 | 5 | — |
| `PTR-003` | Profile & Company Details | listDetail | 4 | 2 | — |
| `PTR-004` | Notifications | statusTracker | 2 | 1 | — |
| `PTR-019` | API Credentials & Integration | listDetail | 7 | 4 | — |
| `PTR-020` | Sub-Agent Management | listDetail | 3 | 2 | — |

## Thin screens in this batch

**PTR-004 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "PTR-001",
  "name": "Partner Login / MFA",
  "module": "Access & Account",
  "requiresModule": "partner",
  "wave": 2,
  "capability": "C35",
  "implementation": {
   "app": "partner-web",
   "route": "/general/partner-login-mfa",
   "component": "apps/partner-web/src/routes/general/PartnerLoginMfaList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "inferred": true,
   "exitTo": [
    "PTR-002",
    "PTR-003",
    "PTR-004",
    "PTR-005",
    "PTR-006",
    "PTR-007",
    "PTR-008",
    "PTR-009",
    "PTR-010",
    "PTR-011",
    "PTR-012",
    "PTR-013",
    "PTR-014",
    "PTR-015",
    "PTR-016",
    "PTR-017",
    "PTR-018",
    "PTR-019",
    "PTR-020",
    "PTR-021",
    "PTR-022",
    "PTR-032",
    "PTR-042"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "provenance": "structural — PTR-001 is P10's home screen and its exits are its launcher",
     "carries": [
      "accountId",
      "orderId"
     ]
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "structural — PTR-001 is P10's home screen and its exits are its launcher"
    },
    {
     "to": "PTR-004",
     "trigger": "Notifications",
     "provenance": "structural — PTR-001 is P10's home screen and its exits are its launcher"
    },
    {
     "to": "PTR-022",
     "trigger": "Opens the partner command centre",
     "provenance": "flow F110 step 1→2"
    },
    {
     "to": "PTR-006",
     "trigger": "Product Catalog (B2B Pricing)",
     "provenance": "derived — PTR-006 declares entryState.params priceListId, productId and PTR-001 holds none of them. The edge carries nothing: priceListId, productId only pre-select (deep link or optional), and PTR-006 opens on its own"
    },
    {
     "to": "PTR-008",
     "trigger": "Booking Creation",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — PTR-008 declares entryState.params orderId and PTR-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "PTR-009",
     "trigger": "Group / Bulk Booking",
     "provenance": "derived — PTR-009 declares entryState.params blockId and PTR-001 holds none of them. The edge carries nothing: blockId only pre-selects (deep link or optional), and PTR-009 opens on its own"
    },
    {
     "to": "PTR-010",
     "trigger": "Cart & Quote",
     "provenance": "derived — PTR-010 declares entryState.params lineId, promotionId and PTR-001 holds none of them. The edge carries nothing: lineId, promotionId only pre-select (deep link or optional), and PTR-010 opens on its own"
    },
    {
     "to": "PTR-011",
     "trigger": "Quote Management",
     "provenance": "derived — PTR-011 declares entryState.params agreementId and PTR-001 holds none of them. The edge carries nothing: agreementId only pre-selects (deep link or optional), and PTR-011 opens on its own"
    },
    {
     "to": "PTR-012",
     "trigger": "Checkout / Credit Purchase",
     "provenance": "derived — PTR-012 declares entryState.params paymentId and PTR-001 holds none of them. The edge carries nothing: paymentId only pre-selects (deep link or optional), and PTR-012 opens on its own"
    },
    {
     "to": "PTR-013",
     "trigger": "Credit Limit & Balance",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — PTR-013 declares entryState.params accountId and PTR-001 holds accountId, so an edge into it carries them"
    },
    {
     "to": "PTR-014",
     "trigger": "Settlement & Payment History",
     "provenance": "derived — PTR-014 declares entryState.params settlementId and PTR-001 holds none of them. The edge carries nothing: settlementId only pre-selects (deep link or optional), and PTR-014 opens on its own"
    },
    {
     "to": "PTR-015",
     "trigger": "Order History",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — PTR-015 declares entryState.params orderId and PTR-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "PTR-016",
     "trigger": "Voucher / Ticket Download",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — PTR-016 declares entryState.params orderId and PTR-001 holds orderId, so an edge into it carries them"
    },
    {
     "to": "PTR-017",
     "trigger": "Commission Statement",
     "provenance": "derived — PTR-017 declares entryState.params agreementId and PTR-001 holds none of them. The edge carries nothing: agreementId only pre-selects (deep link or optional), and PTR-017 opens on its own"
    },
    {
     "to": "PTR-018",
     "trigger": "Reports & Sales Performance",
     "provenance": "derived — PTR-018 declares entryState.params conversationId, reportId and PTR-001 holds none of them. The edge carries nothing: conversationId, reportId only pre-select (deep link or optional), and PTR-018 opens on its own"
    },
    {
     "to": "PTR-019",
     "trigger": "API Credentials & Integration",
     "provenance": "derived — PTR-019 declares entryState.params clientId and PTR-001 holds none of them. The edge carries nothing: PTR-019 finds clientId (listApiClients) itself, and PTR-019 opens on its own"
    },
    {
     "to": "PTR-020",
     "trigger": "Sub-Agent Management",
     "provenance": "derived — PTR-020 declares entryState.params delegatedAccessId and PTR-001 holds none of them. The edge carries nothing: delegatedAccessId only pre-selects (deep link or optional), and PTR-020 opens on its own"
    },
    {
     "to": "PTR-021",
     "trigger": "Support & Contact",
     "provenance": "derived — PTR-021 declares entryState.params caseId and PTR-001 holds none of them. The edge carries nothing: caseId only pre-selects (deep link or optional), and PTR-021 opens on its own"
    },
    {
     "to": "PTR-007",
     "trigger": "Availability Search",
     "provenance": "structural — PTR-001 is P10's home screen and its exits are its launcher"
    },
    {
     "to": "PTR-032",
     "trigger": "Commercial Agreement Command Center",
     "provenance": "structural — PTR-001 is P10's home screen and its exits are its launcher"
    },
    {
     "to": "PTR-042",
     "trigger": "Partner Operations Command Center",
     "provenance": "structural — PTR-001 is P10's home screen and its exits are its launcher"
    },
    {
     "to": "PTR-005",
     "trigger": "Books against the allocation",
     "provenance": "flow F10 step 1→2",
     "operation": "getB2bCredit",
     "carries": [
      "orderId"
     ]
    },
    {
     "to": "SUP-001",
     "trigger": "A back-office user signs in through the same door",
     "provenance": "flow F104 step 4→5",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "challengeId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listActiveSessions` reads the population and `getB2bCredit` reads one of them — list, select, act",
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
      },
      {
       "kind": "dataTable",
       "label": "Every partner agreement",
       "bindsTo": "PartnerAgreement",
       "columns": [
        "PartnerAgreement.id",
        "PartnerAgreement.partnerId",
        "PartnerAgreement.partnerName",
        "PartnerAgreement.status",
        "PartnerAgreement.rateMode",
        "PartnerAgreement.commissionPercent",
        "PartnerAgreement.volumeTiers",
        "PartnerAgreement.volumeWindow",
        "PartnerAgreement.seasonalRates",
        "PartnerAgreement.segmentTier",
        "PartnerAgreement.brandingAssetId",
        "PartnerAgreement.storefrontSubdomain"
       ],
       "operation": "listPartnerAgreements",
       "provenance": "contract subscription.yaml GET /partner-agreements"
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
      },
      {
       "kind": "detailPanel",
       "label": "The credit position",
       "bindsTo": "CreditPosition",
       "columns": [
        "CreditPosition.id",
        "CreditPosition.accountId",
        "CreditPosition.accountName",
        "CreditPosition.creditLimit",
        "CreditPosition.used",
        "CreditPosition.available",
        "CreditPosition.isOverLimit",
        "CreditPosition.isSuspended",
        "CreditPosition.paymentTermsDays",
        "CreditPosition.oldestUnpaidInvoiceAt",
        "CreditPosition.daysOverdue",
        "CreditPosition.activeOverrides",
        "CreditPosition.scopePath"
       ],
       "operation": "getB2bCredit",
       "provenance": "contract orders.yaml GET /b2b-accounts/{accountId}/credit"
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
       "kind": "destructiveButton",
       "label": "Force logout",
       "operation": "forceLogout",
       "provenance": "contract identity.yaml POST /auth/sessions/{sessionId}/force-logout"
      },
      {
       "kind": "destructiveButton",
       "label": "Override credit limit",
       "operation": "overrideCreditLimit",
       "provenance": "contract orders.yaml POST /b2b-accounts/{accountId}/credit/override"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke all sessions",
       "operation": "revokeAllSessions",
       "provenance": "contract identity.yaml POST /auth/sessions/revoke-all"
      },
      {
       "kind": "secondaryButton",
       "label": "Save b2b credit limit",
       "operation": "setB2bCreditLimit",
       "provenance": "contract orders.yaml PUT /b2b-accounts/{accountId}/credit"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmForceLogout",
    "component": "confirmDialog",
    "trigger": "Force logout",
    "body": "**Names what `forceLogout` changes and what it leaves alone**, in the consequence rather than the verb. A partner login mfa this affects should be identified in the dialog, not just counted. **Collects what `forceLogout` sends before it is called.** Required: `reason`.",
    "provenance": "contract identity.yaml POST /auth/sessions/{sessionId}/force-logout"
   },
   {
    "id": "confirmOverrideCreditLimit",
    "component": "confirmDialog",
    "trigger": "Override credit limit",
    "body": "**Names what `overrideCreditLimit` changes and what it leaves alone**, in the consequence rather than the verb. A partner login mfa this affects should be identified in the dialog, not just counted. **Collects what `overrideCreditLimit` sends before it is called.** Required: `orderId`, `amount`, `reason`. Optional: `expiresAt`.",
    "provenance": "contract orders.yaml POST /b2b-accounts/{accountId}/credit/override"
   },
   {
    "id": "confirmRevokeAllSessions",
    "component": "confirmDialog",
    "trigger": "Revoke all sessions",
    "body": "**Names what `revokeAllSessions` changes and what it leaves alone**, in the consequence rather than the verb. A partner login mfa this affects should be identified in the dialog, not just counted. **Collects what `revokeAllSessions` sends before it is called.** Required: `reason`, `stepUpToken`. Optional: `venueId`, `excludeSelf`.",
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
   },
   {
    "id": "formSetB2bCreditLimit",
    "component": "modal",
    "trigger": "Save b2b credit limit",
    "body": "**Collects what `setB2bCreditLimit` sends before it is called.** Required: `creditLimit`, `reason`. Optional: `paymentTermsDays`, `isSuspended`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save b2b credit limit",
     "operation": "setB2bCreditLimit"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "creditLimit",
      "reason",
      "paymentTermsDays",
      "isSuspended"
     ]
    },
    "provenance": "contract orders.yaml PUT /b2b-accounts/{accountId}/credit"
   }
  ],
  "states": {
   "loading": "The partner login mfa list.",
   "error": "Could not load. Names which read failed and leaves the partner login mfa untouched.",
   "emptyFirstRun": "No partner login mfa yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, workstationId and the partner login mfa are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getB2bCredit` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "mfaRequired": "**Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any platform-staff permission, or one the tenant added), so after `login` the screen calls `createMfaChallenge` and asks for the authenticator code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says so. A principal with no enrolled method is sent to enrol first (decided 28 September, audit R135, R126)."
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
    "operationId": "login",
    "contract": "identity",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "getB2bCredit",
    "contract": "orders",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
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
    "operationId": "overrideCreditLimit",
    "contract": "orders",
    "purpose": "Authorise an order beyond the credit limit",
    "trigger": "onAction",
    "invalidates": [
     "listActiveSessions"
    ]
   },
   {
    "operationId": "revokeAllSessions",
    "contract": "identity",
    "purpose": "Revoke every session in scope",
    "trigger": "onAction",
    "invalidates": [
     "listActiveSessions"
    ]
   },
   {
    "operationId": "setB2bCreditLimit",
    "contract": "orders",
    "purpose": "Set a partner credit limit",
    "trigger": "onAction",
    "invalidates": [
     "listActiveSessions"
    ]
   },
   {
    "operationId": "listPartnerAgreements",
    "contract": "subscription",
    "purpose": "Commercial agreements with B2B partners",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "accountId",
     "from": "deepLink"
    },
    {
     "name": "challengeId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `accountId`.",
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-001"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-003",
  "name": "Profile & Company Details",
  "module": "Access & Account",
  "requiresModule": "partner",
  "wave": 2,
  "capability": "C56",
  "implementation": {
   "app": "partner-web",
   "route": "/general/profile-and-company-details",
   "component": "apps/partner-web/src/routes/general/ProfileAndCompanyDetailsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-001",
    "PTR-004"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "provenance": "derived — PTR-001 declares entryState.params accountId, challengeId and PTR-003 holds none of them. The edge carries nothing: PTR-003 is opened from PTR-001, so this edge is the way back and PTR-001 keeps its own state"
    },
    {
     "to": "PTR-004",
     "trigger": "Notifications",
     "provenance": "derived — PTR-004 declares entryState.params messageId and PTR-003 holds none of them. The edge carries nothing: messageId only pre-selects (deep link or optional), and PTR-004 opens on its own"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPrincipals` reads the population and `getPrincipal` reads one of them — list, select, act",
  "purpose": "What we hold about staff, and what they can change.",
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
   "loading": "The profile company list.",
   "error": "Could not load. Names which read failed and leaves the profile company untouched.",
   "emptyFirstRun": "No profile company yet. Offers Create principal (`createPrincipal`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on scopePath, isActive and the profile company are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `USER_MANAGE`, which `getPrincipal` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getPrincipal",
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
    "operationId": "listPrincipals",
    "contract": "identity",
    "purpose": "List principals",
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-003"
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
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-004",
  "name": "Notifications",
  "module": "Access & Account",
  "requiresModule": "partner",
  "wave": 3,
  "capability": "C59",
  "implementation": {
   "app": "partner-web",
   "route": "/general/notifications",
   "component": "apps/partner-web/src/routes/general/NotificationsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-001",
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "provenance": "derived — PTR-001 declares entryState.params accountId, challengeId and PTR-004 holds none of them. The edge carries nothing: PTR-004 is opened from PTR-001, so this edge is the way back and PTR-001 keeps its own state"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-004 holds none of them. The edge carries nothing: PTR-003 needs nothing to open"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getMessageStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Work with notifications for this venue.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The message dispatch",
       "bindsTo": "MessageDispatch",
       "columns": [
        "MessageDispatch.id",
        "MessageDispatch.subjectId",
        "MessageDispatch.campaignId",
        "MessageDispatch.channel",
        "MessageDispatch.templateId",
        "MessageDispatch.status",
        "MessageDispatch.failureReason",
        "MessageDispatch.providerReference",
        "MessageDispatch.queuedAt",
        "MessageDispatch.deliveredAt"
       ],
       "operation": "getMessageStatus",
       "provenance": "contract marketing-crm.yaml GET /messages/{messageId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Send transactional message",
       "operation": "sendTransactionalMessage",
       "provenance": "contract marketing-crm.yaml POST /messages"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The notifications, read by `getMessageStatus`.",
   "error": "Could not load. Names which read failed and leaves the notifications untouched.",
   "emptyFirstRun": "No notifications yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW`, which `getMessageStatus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "sendTransactionalMessage",
    "contract": "marketing-crm",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "getMessageStatus",
    "contract": "marketing-crm",
    "purpose": "Delivery status of one message",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "messageId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `messageId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-004"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSendTransactionalMessage",
    "component": "modal",
    "trigger": "Send transactional message",
    "body": "**Collects what `sendTransactionalMessage` sends before it is called.** Required: `subjectId`, `templateId`, `channel`. Optional: `mergeValues`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Send transactional message",
     "operation": "sendTransactionalMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "subjectId",
      "templateId",
      "channel",
      "mergeValues"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /messages"
   }
  ],
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-019",
  "name": "API Credentials & Integration",
  "module": "Access & Account",
  "requiresModule": "developerApi",
  "wave": 3,
  "implementation": {
   "app": "partner-web",
   "route": "/general/api-credentials-and-integration",
   "component": "apps/partner-web/src/routes/general/ApiCredentialsAndIntegrationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-001",
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "provenance": "derived — PTR-001 declares entryState.params accountId, challengeId and PTR-019 holds none of them. The edge carries nothing: PTR-019 is opened from PTR-001, so this edge is the way back and PTR-001 keeps its own state"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-019 holds none of them. The edge carries nothing: PTR-003 needs nothing to open"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Licensed on `developerApi`, not on `partner`.** The partner licence is what puts a partner on this portal at all; this screen's whole function is the developer API, and without that licence there is nothing on it to show. Declared `partner` it warned as a two-licence page, which is exactly the drift the rule exists to catch.",
  "openQuestions": [
   "Blocked — Developer & API workshop"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listApiClients` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "API Credentials & Integration — the screen a person opens when they need to deal with api credentials & integration.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Scopes, by module",
       "bindsTo": "ApiScope",
       "operation": "listApiScopes",
       "notes": "**A scope picker grouped by module** (M17-05): `{module}.read` and `{module}.write`, with unlicensed modules shown and disabled rather than hidden. No scope opens a catalogue write (M17-04).",
       "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
      },
      {
       "kind": "banner",
       "label": "Production access",
       "bindsTo": "ProductionAccessRequest",
       "operation": "listProductionAccessRequests",
       "notes": "**Where production access stands** (M17-06): sandbox only, requested (pending), approved (a production client issued by TICVAI) or rejected with the reason. Production keys only after certification; a sandbox key is never promoted.",
       "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
      },
      {
       "kind": "dataTable",
       "label": "Every API client",
       "bindsTo": "ApiClient",
       "columns": [
        "ApiClient.id",
        "ApiClient.developerId",
        "ApiClient.name",
        "ApiClient.clientId",
        "ApiClient.environment",
        "ApiClient.scopes",
        "ApiClient.allowedTenantIds",
        "ApiClient.ipAllowList",
        "ApiClient.status",
        "ApiClient.lastUsedAt"
       ],
       "operation": "listApiClients",
       "provenance": "contract public-api.yaml GET /api-clients"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected API client",
       "bindsTo": "ApiClient",
       "columns": [
        "ApiClient.id",
        "ApiClient.developerId",
        "ApiClient.name",
        "ApiClient.clientId",
        "ApiClient.environment",
        "ApiClient.scopes",
        "ApiClient.allowedTenantIds",
        "ApiClient.ipAllowList",
        "ApiClient.status",
        "ApiClient.lastUsedAt"
       ],
       "operation": "listApiClients",
       "provenance": "contract public-api.yaml GET /api-clients"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Request production access",
       "operation": "requestProductionAccess",
       "notes": "**Production keys only after certification** (M17-06). Enabled on a sandbox client whose integration is certified; asks for the tenants, the scopes and the IP allow-list. TICVAI issues the production client.",
       "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
      },
      {
       "kind": "primaryButton",
       "label": "Create API client",
       "operation": "createApiClient",
       "provenance": "contract public-api.yaml POST /api-clients"
      },
      {
       "kind": "secondaryButton",
       "label": "Rotate API credential",
       "operation": "rotateApiCredential",
       "provenance": "contract public-api.yaml POST /api-clients/{clientId}/credentials"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke API credential",
       "operation": "revokeApiCredential",
       "provenance": "contract public-api.yaml DELETE /api-clients/{clientId}/credentials"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formRequestProductionAccess",
    "component": "modal",
    "trigger": "Request production access",
    "body": "**Collects what `requestProductionAccess` sends before it is called.** Required: `listingId` (a certified integration), `scopes`, `allowedTenantIds`, `ipAllowList` (at least one address, M17-07). Optional: `note`. The form says that a new production key is issued and the sandbox key stays a sandbox key.",
    "confirm": {
     "label": "Request production access",
     "operation": "requestProductionAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "listingId",
      "scopes",
      "allowedTenantIds",
      "ipAllowList",
      "note"
     ]
    },
    "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
   },
   {
    "id": "confirmRevokeApiCredential",
    "component": "confirmDialog",
    "trigger": "Revoke API credential",
    "body": "**Names what `revokeApiCredential` changes and what it leaves alone**, in the consequence rather than the verb. A api credentials integration this affects should be identified in the dialog, not just counted.",
    "provenance": "contract public-api.yaml DELETE /api-clients/{clientId}/credentials"
   },
   {
    "id": "formCreateApiClient",
    "component": "modal",
    "trigger": "Create API client",
    "body": "**Collects what `createApiClient` sends before it is called.** Required: `id`, `developerId`, `name`, `environment`, `scopes`, `status`. Optional: `clientId`, `allowedTenantIds`, `ipAllowList`, `lastUsedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ApiClient",
    "confirm": {
     "label": "Create API client",
     "operation": "createApiClient"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "developerId",
      "name",
      "environment",
      "scopes",
      "status",
      "clientId",
      "allowedTenantIds",
      "ipAllowList",
      "lastUsedAt"
     ]
    },
    "provenance": "contract public-api.yaml POST /api-clients"
   },
   {
    "id": "formRotateApiCredential",
    "component": "modal",
    "trigger": "Rotate API credential",
    "body": "**Collects what `rotateApiCredential` sends before it is called.** Nothing in the body is required. Optional: `overlapHours`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Rotate API credential",
     "operation": "rotateApiCredential"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "overlapHours"
     ]
    },
    "provenance": "contract public-api.yaml POST /api-clients/{clientId}/credentials"
   }
  ],
  "states": {
   "loading": "Detail loads",
   "error": "Could not load",
   "emptyFirstRun": "Not found — it may have been deleted or moved out of scope",
   "emptyNoResults": "Never shown: `listApiClients` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `DEVELOPER_VIEW`, which `listApiClients` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApiScopes",
    "contract": "public-api",
    "purpose": "Scopes to choose from, by module",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
   },
   {
    "operationId": "listProductionAccessRequests",
    "contract": "public-api",
    "purpose": "Where production access stands for these clients",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
   },
   {
    "operationId": "requestProductionAccess",
    "contract": "public-api",
    "purpose": "Ask for production keys for a certified integration",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
   },
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "Clients issued to this partner",
    "trigger": "onLoad"
   },
   {
    "operationId": "createApiClient",
    "contract": "public-api",
    "purpose": "Issue a client",
    "trigger": "onAction",
    "invalidates": [
     "listApiClients"
    ]
   },
   {
    "operationId": "rotateApiCredential",
    "contract": "public-api",
    "purpose": "Rotate a key without downtime",
    "trigger": "onAction",
    "invalidates": [
     "listApiClients"
    ]
   },
   {
    "operationId": "revokeApiCredential",
    "contract": "public-api",
    "purpose": "Revoke a key immediately",
    "trigger": "onAction",
    "invalidates": [
     "listApiClients"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "clientId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Rotation and revocation act on one client**, which arrives from the row the partner chose. Opened cold the screen lists clients rather than offering an action with no subject — revoking the wrong key is not recoverable by the person who did it.",
   "preloaded": [
    "ApiClient.id",
    "ApiClient.developerId",
    "ApiClient.name",
    "ApiClient.clientId",
    "ApiClient.environment"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-019"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-020",
  "name": "Sub-Agent Management",
  "module": "Access & Account",
  "requiresModule": "partner",
  "wave": 3,
  "capability": "C56",
  "implementation": {
   "app": "partner-web",
   "route": "/general/sub-agent-management",
   "component": "apps/partner-web/src/routes/general/SubAgentManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-001",
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "provenance": "derived — PTR-001 declares entryState.params accountId, challengeId and PTR-020 holds none of them. The edge carries nothing: PTR-020 is opened from PTR-001, so this edge is the way back and PTR-001 keeps its own state"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-020 holds none of them. The edge carries nothing: PTR-003 needs nothing to open"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDelegatedAccess` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Add sub-agent management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listDelegatedAccess",
       "notes": "Sends `?principalId=` to `listDelegatedAccess`.",
       "provenance": "contract identity.yaml GET /delegated-access"
      },
      {
       "kind": "textField",
       "label": "Role id",
       "operation": "listDelegatedAccess",
       "notes": "Sends `?roleId=` to `listDelegatedAccess`.",
       "provenance": "contract identity.yaml GET /delegated-access"
      },
      {
       "kind": "dataTable",
       "label": "Every delegated access",
       "bindsTo": "DelegatedAccess",
       "columns": [
        "DelegatedAccess.id",
        "DelegatedAccess.principalId",
        "DelegatedAccess.roleId",
        "DelegatedAccess.permission",
        "DelegatedAccess.subjectId",
        "DelegatedAccess.overSubjectId",
        "DelegatedAccess.overObjectRef",
        "DelegatedAccess.delegationKind",
        "DelegatedAccess.quota",
        "DelegatedAccess.isRevocableBySubject",
        "DelegatedAccess.scopePath",
        "DelegatedAccess.effect"
       ],
       "operation": "listDelegatedAccess",
       "provenance": "contract identity.yaml GET /delegated-access"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected delegated access",
       "bindsTo": "DelegatedAccess",
       "columns": [
        "DelegatedAccess.id",
        "DelegatedAccess.principalId",
        "DelegatedAccess.roleId",
        "DelegatedAccess.permission",
        "DelegatedAccess.subjectId",
        "DelegatedAccess.overSubjectId",
        "DelegatedAccess.overObjectRef",
        "DelegatedAccess.delegationKind",
        "DelegatedAccess.quota",
        "DelegatedAccess.isRevocableBySubject",
        "DelegatedAccess.scopePath",
        "DelegatedAccess.effect",
        "DelegatedAccess.validFrom",
        "DelegatedAccess.validTo",
        "DelegatedAccess.createdByPrincipalId"
       ],
       "operation": "listDelegatedAccess",
       "provenance": "contract identity.yaml GET /delegated-access"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create delegated access",
       "operation": "createDelegatedAccess",
       "provenance": "contract identity.yaml POST /delegated-access"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete delegated access",
       "operation": "deleteDelegatedAccess",
       "provenance": "contract identity.yaml DELETE /delegated-access/{delegatedAccessId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteDelegatedAccess",
    "component": "confirmDialog",
    "trigger": "Delete delegated access",
    "body": "**Names what `deleteDelegatedAccess` changes and what it leaves alone**, in the consequence rather than the verb. A sub-agent this affects should be identified in the dialog, not just counted.",
    "provenance": "contract identity.yaml DELETE /delegated-access/{delegatedAccessId}"
   },
   {
    "id": "formCreateDelegatedAccess",
    "component": "modal",
    "trigger": "Create delegated access",
    "body": "**Collects what `createDelegatedAccess` sends before it is called.** Required: `permission`, `scopePath`, `effect`. Optional: `principalId`, `roleId`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateGrantRequest",
    "confirm": {
     "label": "Create delegated access",
     "operation": "createDelegatedAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permission",
      "scopePath",
      "effect",
      "principalId",
      "roleId",
      "validFrom",
      "validTo"
     ]
    },
    "provenance": "contract identity.yaml POST /delegated-access"
   }
  ],
  "states": {
   "loading": "The sub-agent list.",
   "error": "Could not load. Names which read failed and leaves the sub-agent untouched.",
   "emptyFirstRun": "No sub-agent yet. Offers Create delegated access (`createDelegatedAccess`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on principalId, roleId and the sub-agent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PERMISSION_VIEW`, which `listDelegatedAccess` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createDelegatedAccess",
    "contract": "identity",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "deleteDelegatedAccess",
    "contract": "identity",
    "purpose": "Remove a grant",
    "trigger": "onAction",
    "invalidates": [
     "listDelegatedAccess"
    ]
   },
   {
    "operationId": "listDelegatedAccess",
    "contract": "identity",
    "purpose": "List grants for a principal or role",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "delegatedAccessId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `delegatedAccessId`.",
   "preloaded": [
    "DelegatedAccess.id",
    "DelegatedAccess.principalId",
    "DelegatedAccess.roleId",
    "DelegatedAccess.permission",
    "DelegatedAccess.subjectId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-020"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
 "createApiClient": {
  "method": "POST",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Create a client with scopes and an environment",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "ApiClient",
  "responds": null
 },
 "createDelegatedAccess": {
  "method": "POST",
  "path": "/delegated-access",
  "contract": "identity",
  "summary": "Assign a grant",
  "permission": "PERMISSION_GRANT",
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
  "requestBody": "CreateGrantRequest",
  "responds": "DelegatedAccess"
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
 "deleteDelegatedAccess": {
  "method": "DELETE",
  "path": "/delegated-access/{delegatedAccessId}",
  "contract": "identity",
  "summary": "Remove a grant",
  "permission": "PERMISSION_GRANT",
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
 "getB2bCredit": {
  "method": "GET",
  "path": "/b2b-accounts/{accountId}/credit",
  "contract": "orders",
  "summary": "Partner credit position",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CreditPosition"
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
 "getMessageStatus": {
  "method": "GET",
  "path": "/messages/{messageId}",
  "contract": "marketing-crm",
  "summary": "Delivery status of one message",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MessageDispatch"
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
 "listApiClients": {
  "method": "GET",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Registered clients for this developer",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApiClient"
 },
 "listApiScopes": {
  "method": "GET",
  "path": "/api-scopes",
  "contract": "public-api",
  "summary": "The scope catalogue, one read and one write scope per module",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "module",
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
 "listDelegatedAccess": {
  "method": "GET",
  "path": "/delegated-access",
  "contract": "identity",
  "summary": "List grants for a principal or role",
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
    "name": "roleId",
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
 "listPartnerAgreements": {
  "method": "GET",
  "path": "/partner-agreements",
  "contract": "subscription",
  "summary": "Commercial agreements with B2B partners",
  "permission": "PARTNER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "expiringWithinDays",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PartnerAgreement"
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
 "listProductionAccessRequests": {
  "method": "GET",
  "path": "/production-access-requests",
  "contract": "public-api",
  "summary": "Production access requests, pending first",
  "permission": "DEVELOPER_VIEW",
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
 "overrideCreditLimit": {
  "method": "POST",
  "path": "/b2b-accounts/{accountId}/credit/override",
  "contract": "orders",
  "summary": "Authorise an order beyond the credit limit",
  "permission": "CREDIT_OVERRIDE",
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
  "responds": "CreditPosition"
 },
 "requestProductionAccess": {
  "method": "POST",
  "path": "/api-clients/{clientId}/production-access",
  "contract": "public-api",
  "summary": "Ask for production keys for a sandbox client that passed certification",
  "permission": "DEVELOPER_MANAGE",
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
  "responds": "ProductionAccessRequest"
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
 "revokeApiCredential": {
  "method": "DELETE",
  "path": "/api-clients/{clientId}/credentials",
  "contract": "public-api",
  "summary": "Revoke immediately",
  "permission": "DEVELOPER_MANAGE",
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
 "rotateApiCredential": {
  "method": "POST",
  "path": "/api-clients/{clientId}/credentials",
  "contract": "public-api",
  "summary": "Issue a new secret, with an overlap window",
  "permission": "DEVELOPER_MANAGE",
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
 "sendTransactionalMessage": {
  "method": "POST",
  "path": "/messages",
  "contract": "marketing-crm",
  "summary": "Send a transactional message",
  "permission": "MARKETING_SEND",
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
 "setB2bCreditLimit": {
  "method": "PUT",
  "path": "/b2b-accounts/{accountId}/credit",
  "contract": "orders",
  "summary": "Set a partner credit limit",
  "permission": "CREDIT_MANAGE",
  "offlineCapable": false,
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
  "responds": "CreditPosition"
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
 "ApiClient": {
  "type": "object",
  "x-ticvai-persistence": "control.api_client",
  "description": "CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n",
  "required": [
   "id",
   "developerId",
   "name",
   "environment",
   "scopes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "clientId": {
    "type": "string",
    "readOnly": true
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "production"
    ],
    "description": "**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"
   },
   "scopes": {
    "type": "array",
    "description": "**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n",
    "items": {
     "type": "string",
     "pattern": "^[a-zA-Z]+\\.(read|write)$"
    }
   },
   "issuedBy": {
    "type": "string",
    "enum": [
     "partner",
     "ticvai"
    ],
    "readOnly": true,
    "description": "Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"
   },
   "certificationListingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "control.integration_listing",
    "description": "For a production client, the certified integration it was issued against."
   },
   "credentialTtlDays": {
    "type": "integer",
    "minimum": 1,
    "maximum": 730,
    "nullable": true,
    "description": "Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the key stops working unless rotated. No token is issued after it."
   },
   "allowedTenantIds": {
    "type": "array",
    "description": "13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "description": "13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked"
    ],
    "readOnly": true
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
   }
  }
 },
 "ApiScope": {
  "type": "object",
  "x-ticvai-persistence": "none — generated at release from x-ticvai-api-scope on each partner-callable operation",
  "description": "**One module scope** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, and the operations it opens.\n**A write scope never opens a catalogue write** (M17-04): `ticketing.write` opens carts, orders and holds for a partner or developer client, and no product, price list, price, channel capacity, lifecycle or alternative-code write, since those operations are not partner-callable and carry no `x-ticvai-api-scope`. Only a platform-staff `ApiLicence.catalogueWriteException` opens one, for one named client.\n",
  "required": [
   "scope",
   "module",
   "access"
  ],
  "properties": {
   "scope": {
    "type": "string",
    "description": "e.g. `ticketing.read`."
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
   },
   "access": {
    "type": "string",
    "enum": [
     "read",
     "write"
    ]
   },
   "description": {
    "type": "string"
   },
   "operations": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "contract": {
       "type": "string"
      },
      "operationId": {
       "type": "string"
      }
     }
    }
   },
   "licensed": {
    "type": "boolean",
    "description": "Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`)."
   }
  }
 },
 "CreateGrantRequest": {
  "type": "object",
  "required": [
   "permission",
   "scopePath",
   "effect"
  ],
  "properties": {
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "roleId": {
    "type": "string",
    "format": "uuid"
   },
   "permission": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "effect": {
    "type": "string",
    "enum": [
     "ALLOW",
     "DENY"
    ]
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
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
 "CreditPosition": {
  "x-ticvai-persistence": "orders.b2b_credit + orders.credit_override",
  "type": "object",
  "required": [
   "accountId",
   "creditLimit",
   "used",
   "available",
   "isSuspended"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "accountId": {
    "type": "string",
    "format": "uuid"
   },
   "accountName": {
    "type": "string"
   },
   "creditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "used": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "available": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "isOverLimit": {
    "type": "boolean"
   },
   "isSuspended": {
    "type": "boolean"
   },
   "paymentTermsDays": {
    "type": "integer"
   },
   "oldestUnpaidInvoiceAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "daysOverdue": {
    "type": "integer"
   },
   "activeOverrides": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "orderId": {
       "type": "string",
       "format": "uuid"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "authorisedByPrincipalId": {
       "type": "string",
       "format": "uuid"
      },
      "reason": {
       "type": "string"
      },
      "expiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "DelegatedAccess": {
  "x-ticvai-persistence": "identity.delegated_access",
  "type": "object",
  "required": [
   "id",
   "permission",
   "scopePath",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "roleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "permission": {
    "type": "string",
    "description": "From the permission enum. `*` permitted on DENY only."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "CF-132, CL-05. **A grant held by a guest rather than a staff principal.**\nSection 5.5 asks for portfolios — a primary holder assigning entitlements, transfer between linked accounts, shared wallets with individual tracking — and it appears ten times across ten sections. **Every one of those reduces to the same question: who may act on whose behalf, over what, and until when.**\n**That is a grant, not a household table.** A primary holder assigning an entitlement is a grant. A group leader holding tickets for twelve is a grant. A corporate account enrolling members is a grant with a quota. **A shared wallet with individual tracking is a grant over a balance, and the transaction log already records who spent.**\n**A household table would answer one of those four.**\n"
   },
   "overSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Whose behalf. **Null for a staff grant, which is the existing behaviour** — every grant written before 18 August means exactly what it meant before.\n"
   },
   "overObjectRef": {
    "type": "string",
    "nullable": true,
    "description": "**Where the authority is over a thing rather than a scope** — a wallet, an entitlement, a booking. `scopePath` answers *where*; this answers *what*, and a guest's authority is almost always over a specific object rather than a branch of the tree.\n"
   },
   "delegationKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "primaryHolder",
     "familyMember",
     "groupLeader",
     "attendee",
     "corporateAdmin",
     "corporateMember",
     "carer"
    ],
    "description": "**What kind of relationship this expresses**, for display and for reporting. The mechanism does not branch on it — a family member and a group attendee are the same grant with different words around them, which is the point.\n"
   },
   "quota": {
    "type": "integer",
    "nullable": true,
    "description": "2.14.15 and 4.3.11. **How many the holder may assign.** A corporate account with fifty allocations and a family with four are the same structure with different numbers.\n"
   },
   "isRevocableBySubject": {
    "type": "boolean",
    "default": true,
    "description": "**Whether the person it is over can end it.** A guest who linked a family member should be able to unlink them; a corporate member should not be able to revoke their employer's oversight — and **a delegation nobody can end is a delegation somebody will regret.**\n"
   },
   "scopePath": {
    "type": "string"
   },
   "effect": {
    "type": "string",
    "enum": [
     "ALLOW",
     "DENY"
    ]
   },
   "permissionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from `identity.user_access`, 20 September, when that table was collapsed into this one.** `permission` above is free text; this names a row in `identity.permission`, the catalogue wired the same day. A grant that names a catalogue row can be checked against the keys the contracts actually enforce — which is the whole point of a catalogue that reported *154 on operations, 35 in roles.yaml, 0 shared*.\nNullable because a role grant carries no permission at all.\n"
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "Taken from `identity.user_access`. This table recorded `revokedBy` and not when, so it could say who revoked a grant and not whether it was before or after the thing somebody is asking about.\n"
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
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
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
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
 },
 "MessageDispatch": {
  "x-ticvai-append-only": "queuedAt",
  "x-ticvai-persistence": "marketing.message_dispatch",
  "type": "object",
  "required": [
   "id",
   "subjectId",
   "channel",
   "status",
   "queuedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "messageTriggerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `MessageTrigger` that fired it, and through its `event` the `BusinessEvent` and source module; null for a campaign or a direct send. Attempts are in `MessageDispatchAttempt`. (decided 29 September, data model for the agreed operations)"
   },
   "campaignVariantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "marketing.campaign_variant",
    "description": "The A/B variant sent (22.1.17; 29 September, build pass, group G2). Null for a single-content campaign or a triggered message."
   },
   "plannedSendAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The per-recipient hour chosen by `sendTimeMode` `optimised` (22.3.19, 22.9.16); null when sent at the scheduled time."
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "sent",
     "delivered",
     "opened",
     "clicked",
     "bounced",
     "failed",
     "suppressed"
    ]
   },
   "failureReason": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "queuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "deliveredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isTest": {
    "type": "boolean",
    "default": false,
    "description": "A `testSendCampaign` message. Excluded from `CampaignPerformance` and `Campaign.sentCount`."
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "From the provider's engagement events. `CampaignPerformance.opened` counts these."
   },
   "clickedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "complainedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "unsubscribedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "PartnerAgreement": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_agreement",
  "x-ticvai-retired-columns": [
   "partner_name"
  ],
  "required": [
   "partnerId",
   "rateMode",
   "validFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "x-ticvai-references": "control.partner",
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner) this agreement is with. The agreement carries the terms; control.partner carries who the partner is and whether it may trade. **Resolves to control.partner**, not to platform.tenant as the naming convention guessed before the partner master existed (decided 29 September, writers pass; DM4)"
   },
   "partnerName": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The partner's trading name, **read from control.partner.trading_name** (Partner.tradingName) when the agreement is returned and never stored on the agreement, so a renamed partner cannot show two names (decided 29 September, writers pass; DM4)"
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "**Amending creates a version.** An order placed last week was placed under last week's rate, and settlement must be able to say which.\n"
   },
   "status": {
    "$ref": "#/components/schemas/PartnerAgreementStatus"
   },
   "rateMode": {
    "$ref": "#/components/schemas/PartnerRateMode"
   },
   "commissionPercent": {
    "type": "number",
    "nullable": true
   },
   "volumeTiers": {
    "type": "array",
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: the tiers are rows of control.partner_rate_volume_band** (`PartnerRate.volumeBands`, written by setPartnerRateNet), one set per rate row, so a tier can differ by product, venue or channel. Accepted and ignored on write; not returned once the bands exist. `volumeWindow` below still says over which window the bands count (decided 29 September, writers pass; DM4).\n\n2.7.57. **A tier that changes at a threshold needs the sale to look back at cumulative volume, and nothing did.** Flat net rates and per-channel price lists cover the simple case and stop there.\n**The window is the argument, not the tier.** A partner who sells 400 in January and 400 in February is either a 400-tier partner twice or an 800-tier partner once, and the two are different money. `volumeWindow` says which.\n",
    "items": {
     "type": "object",
     "required": [
      "fromUnits",
      "commissionPercent"
     ],
     "properties": {
      "fromUnits": {
       "type": "integer"
      },
      "commissionPercent": {
       "type": "number"
      },
      "appliesRetrospectively": {
       "type": "boolean",
       "default": false,
       "description": "**Whether crossing a tier reprices what came before it.** Retrospective is what a partner assumes and prospective is what a venue budgets for — it has to be stated.\n"
      }
     }
    }
   },
   "volumeWindow": {
    "type": "string",
    "nullable": true,
    "enum": [
     "calendarMonth",
     "calendarQuarter",
     "calendarYear",
     "agreementYear",
     "rolling12Months"
    ]
   },
   "seasonalRates": {
    "type": "array",
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: a seasonal rate is a control.partner_rate row** with `seasonalRate: true` and its own `effectiveFrom`/`effectiveTo` (`PartnerRate`, written by setPartnerRateNet); the most specific row in force wins. Accepted and ignored on write (decided 29 September, writers pass; DM4).\n\nRates that change by date range. **Separate from the volume tier because they compound** — a peak-season rate at a high volume tier is both, and a single rate table cannot say so.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date"
      },
      "to": {
       "type": "string",
       "format": "date"
      },
      "commissionPercent": {
       "type": "number"
      }
     }
    }
   },
   "segmentTier": {
    "type": "string",
    "nullable": true
   },
   "brandingAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "2.7.x, BL-078. **A reseller selling a venue's tickets under their own brand is a second scope level white-label does not have** — `BrandIdentity` and `setTheme` are tenant-scoped throughout.\n**Co-branding rather than replacement.** The venue's identity stays on the ticket because the ticket admits to the venue; the partner's sits beside it.\n"
   },
   "storefrontSubdomain": {
    "type": "string",
    "nullable": true
   },
   "sponsorship": {
    "type": "object",
    "nullable": true,
    "description": "BL-050. **Sponsorship inventory is sellable capacity of a different kind** — logo placements, hospitality allocations, naming rights. It is closer to a partner agreement than to a product: **a sponsor buys a relationship for a season, not a ticket for a date.**\nModelled here rather than as a `ProductKind` because the commercial terms — the term, the exclusivity, the settlement — are the agreement's, and duplicating them onto a product would mean two places to disagree.\n",
    "properties": {
     "placements": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "surface": {
         "type": "string",
         "enum": [
          "signage",
          "ticketFace",
          "appBanner",
          "emailFooter",
          "venueNaming",
          "zoneNaming",
          "uniform",
          "printedMap"
         ]
        },
        "quantity": {
         "type": "integer"
        },
        "exclusive": {
         "type": "boolean",
         "default": false,
         "description": "**Exclusivity is the expensive word.** A sponsor paying for category exclusivity has bought the absence of a competitor, and a second agreement breaching it is a legal problem rather than a scheduling one.\n"
        }
       }
      }
     },
     "hospitalityAllocation": {
      "type": "integer",
      "nullable": true,
      "description": "Tickets or cabanas included. **Issued as invitations, not sales** — no revenue attaches."
     },
     "categoryExclusivity": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "netRates": {
    "type": "array",
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: net rates are rows of control.partner_rate** (`PartnerRate` with `pricingModel: netRate`, `netRate` and the `maxDiscountPercent` guardrail), written by setPartnerRateNet. Per product or category; absent means the commission applies across the catalogue. Accepted and ignored on write (decided 29 September, writers pass; DM4)",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "categoryId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "netPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "maxDiscountPercent": {
       "type": "number",
       "nullable": true,
       "description": "1.6.10. **What the partner may not undercut.** A reseller selling below the venue's own price damages the direct channel, and the venue usually cares more about that than the margin.\n"
      }
     }
    }
   },
   "creditTermDays": {
    "type": "integer",
    "description": "2.7.36. Net 30, net 60. Drives when an invoice becomes overdue."
   },
   "acceptedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-079. **Electronic acceptance against a version**, following the `signatureRef` precedent. An agreement accepted with no version recorded is an agreement nobody can produce in a dispute.\n"
   },
   "acceptedVersion": {
    "type": "integer",
    "nullable": true
   },
   "acceptedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "corporateAllocations": {
    "type": "array",
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: allocations are rows of control.partner_allocation** (`PartnerAllocation`, written by setPartnerAllocations and read by listCommercialAllocationQuota); used quantity is counted from orders against the row, not stored. Accepted and ignored on write (decided 29 September, writers pass; DM4).\n\nBL-035. **`PartnerAgreement` covered commercial terms and not allocations.** A corporate account with fifty places for its staff is the same structure as a reseller with fifty to sell, and **the difference is that a corporate member does not pay.**\n",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer"
      },
      "usedQuantity": {
       "type": "integer",
       "readOnly": true
      },
      "perMemberLimit": {
       "type": "integer",
       "nullable": true
      },
      "validTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "settlementCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "**The currency this partner is billed and settles in**, which is often not the venue's. A UK tour operator selling a Dubai attraction is invoiced in GBP against sales booked in AED, and the difference is somebody's exposure.\n**`creditLimit` and `netRates` are expressed in this currency**, not the venue's — a limit in the wrong currency is a limit that moves with the exchange rate.\n"
   },
   "fxPolicy": {
    "type": "string",
    "enum": [
     "rateAtSale",
     "rateAtInvoice",
     "fixedRate"
    ],
    "default": "rateAtSale",
    "description": "**Which rate converts a sale into the settlement currency, and it is a commercial term.** `rateAtSale` puts the movement on the partner; `rateAtInvoice` puts it on the venue; `fixedRate` puts it on whoever guessed wrong when the agreement was signed.\n**Not a default to leave alone** — on a monthly statement across a moving rate the three produce materially different numbers, and the partner will have assumed one of them.\n"
   },
   "fixedRate": {
    "type": "number",
    "nullable": true,
    "description": "Where `fxPolicy` is `fixedRate`. **An amendment creates a version** so an old statement stays readable."
   },
   "creditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "allowedChannels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresApprovalAboveValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "2.7.39. Routes through `approvals` rather than a second mechanism here."
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "2.7.37. **An agreement that lapses silently keeps selling at rates nobody agreed to**, discovered at settlement rather than at sale. Null means open-ended, which should be rare and deliberate.\n"
   },
   "expiryAlertDays": {
    "type": "integer",
    "default": 30
   },
   "approvalRequestId": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "notes": {
    "type": "string"
   },
   "agreementName": {
    "type": "string",
    "nullable": true,
    "description": "Agreement name (decided 29 September, data model DM4)"
   },
   "agreementType": {
    "type": "string",
    "nullable": true,
    "description": "Agreement type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26) (decided 29 September, data model DM4)"
   },
   "contractReference": {
    "type": "string",
    "nullable": true,
    "description": "Contract reference (decided 29 September, data model DM4)"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The contracting legal entity (ledger.legal_entity) (decided 29 September, data model DM4)"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Brand the agreement covers; empty for every brand of the tenant (decided 29 September, data model DM4)"
   },
   "territory": {
    "type": "string",
    "nullable": true,
    "description": "Territory (decided 29 September, data model DM4)"
   },
   "commercialOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Commercial owner, a staff principal (decided 29 September, data model DM4)"
   },
   "financeOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Finance owner, a staff principal (decided 29 September, data model DM4)"
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "nullable": true,
    "description": "Pricing basis (pack p.27 pricing models); the rows are `control.partner_rate` (decided 29 September, data model DM4)"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "nullable": true,
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale). Held here once; the billing screen reads and sets this column (decided 29 September, data model DM4)"
   },
   "renewalType": {
    "type": "string",
    "enum": [
     "manual",
     "auto"
    ],
    "nullable": true,
    "description": "Renewal type (decided 29 September, data model DM4)"
   },
   "renewalNoticeDays": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Renewal notice period in days (decided 29 September, data model DM4)"
   },
   "renegotiationRequired": {
    "type": "boolean",
    "default": false,
    "description": "Renegotiation required before renewal (decided 29 September, data model DM4)"
   },
   "renewalRequiresApproval": {
    "type": "boolean",
    "description": "Renewal needs approval (decided 29 September, data model DM4)"
   },
   "minimumCommitment": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Minimum commitment: tickets over the agreement term (decided 29 September, data model DM4)"
   },
   "salesTarget": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Sales target over the agreement term (decided 29 September, data model DM4)"
   },
   "agreementValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Agreement value (MoM 31 Aug 4.4: each agreement captures term/value) (decided 29 September, data model DM4)"
   },
   "commissionTerms": {
    "type": "string",
    "nullable": true,
    "description": "Commission terms as written in the contract; the rules that compute it are `control.partner_commission_rule` (decided 29 September, data model DM4)"
   },
   "creditTerms": {
    "type": "string",
    "nullable": true,
    "description": "Credit terms as written in the contract (decided 29 September, data model DM4)"
   },
   "allocationTerms": {
    "type": "string",
    "nullable": true,
    "description": "Allocation terms as written in the contract; the allocations are `control.partner_allocation` (decided 29 September, data model DM4)"
   },
   "cancellationConditions": {
    "type": "string",
    "nullable": true,
    "description": "Cancellation conditions (decided 29 September, data model DM4)"
   },
   "refundConditions": {
    "type": "string",
    "nullable": true,
    "description": "Refund conditions (pack p.26) (decided 29 September, data model DM4)"
   },
   "bookingRestrictions": {
    "type": "string",
    "nullable": true,
    "description": "Booking restrictions as written in the contract; the enforced limits are `control.partner_booking_limit` (decided 29 September, data model DM4)"
   },
   "settlementTerms": {
    "type": "string",
    "nullable": true,
    "description": "Settlement terms (decided 29 September, data model DM4)"
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope, as every control.partner_* row carries it, so row-level security scopes the agreement the same way (decided 29 September, writers pass; DM4)"
   }
  }
 },
 "PartnerAgreementStatus": {
  "type": "string",
  "enum": [
   "pendingApproval",
   "active",
   "expiringSoon",
   "expired",
   "suspended",
   "terminated"
  ]
 },
 "PartnerRateMode": {
  "type": "string",
  "description": "**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n",
  "enum": [
   "netRate",
   "commission"
  ]
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
 "ProductionAccessRequest": {
  "type": "object",
  "x-ticvai-persistence": "control.production_access_request",
  "description": "**A developer's request for production keys** (17 September minutes, M17-06): sandbox, then certification, then production.\n",
  "required": [
   "id",
   "developerId",
   "sandboxClientId",
   "listingId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "sandboxClientId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "control.api_client"
   },
   "listingId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "control.integration_listing"
   },
   "scopes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "allowedTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "approved",
     "rejected",
     "withdrawn"
    ],
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "productionClientId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "control.api_client"
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
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
