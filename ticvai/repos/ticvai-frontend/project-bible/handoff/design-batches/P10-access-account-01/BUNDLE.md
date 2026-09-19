# P10-access-account-01 — P10 · Access & Account

**5 screens · 25 operations · 23 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `CREDIT_MANAGE, CREDIT_OVERRIDE, DEVELOPER_MANAGE, DEVELOPER_VIEW, GUEST_VIEW, ORDER_VIEW, PARTNER_MANAGE, PERMISSION_GRANT, PERMISSION_VIEW, SESSION_FORCE_LOGOUT, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **2 of these operations work offline**: getCurrentSession, getGuestSession
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-001` | Partner Login / MFA | listDetail | 12 | 3 | — |
| `PTR-003` | Profile & Company Details | listDetail | 4 | 0 | — |
| `PTR-004` | Notifications | statusTracker | 2 | 0 | — |
| `PTR-019` | API Credentials & Integration | listDetail | 4 | 1 | — |
| `PTR-020` | Sub-Agent Management | listDetail | 3 | 1 | — |

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
    "PTR-022"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "PTR-005",
     "trigger": "Books against the allocation",
     "provenance": "flow F10 step 1→2",
     "operation": "getB2bCredit"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "provenance": "structural — PTR-001 is P10's home screen and its exits are its launcher"
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
     "to": "SUP-001",
     "trigger": "Agent Login",
     "provenance": "flow F104 step 2→3",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "PTR-022",
     "trigger": "Opens the partner command centre",
     "provenance": "flow F110 step 1→2"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listActiveSessions` reads the population and `getB2bCredit` reads one of them — list, select, act",
  "purpose": "Get someone into the app, fast, on a device that may be shared.",
  "gaps": [
   {
    "operation": "getCurrentSession",
    "why": "**5 declared operations reach no component on this screen**: getCurrentSession, getGuestSession, listMfaMethods, listSsoProviders, listPartnerAgreements. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every partner login mfa",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner login mfa",
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
       "kind": "destructiveButton",
       "label": "Force",
       "operation": "forceLogout",
       "provenance": "contract identity.yaml POST /auth/sessions/{sessionId}/force-logout"
      },
      {
       "kind": "destructiveButton",
       "label": "Override",
       "operation": "overrideCreditLimit",
       "provenance": "contract orders.yaml POST /b2b-accounts/{accountId}/credit/override"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke",
       "operation": "revokeAllSessions",
       "provenance": "contract identity.yaml POST /auth/sessions/revoke-all"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
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
    "trigger": "Force",
    "body": "**Names what `forceLogout` changes and what it leaves alone**, in the consequence rather than the verb. A partner login mfa this affects should be identified in the dialog, not just counted.",
    "provenance": "contract identity.yaml POST /auth/sessions/{sessionId}/force-logout"
   },
   {
    "id": "confirmOverrideCreditLimit",
    "component": "confirmDialog",
    "trigger": "Override",
    "body": "**Names what `overrideCreditLimit` changes and what it leaves alone**, in the consequence rather than the verb. A partner login mfa this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml POST /b2b-accounts/{accountId}/credit/override"
   },
   {
    "id": "confirmRevokeAllSessions",
    "component": "confirmDialog",
    "trigger": "Revoke",
    "body": "**Names what `revokeAllSessions` changes and what it leaves alone**, in the consequence rather than the verb. A partner login mfa this affects should be identified in the dialog, not just counted.",
    "provenance": "contract identity.yaml POST /auth/sessions/revoke-all"
   }
  ],
  "states": {
   "loading": "The partner login mfa list.",
   "error": "Could not load. Names which read failed and leaves the partner login mfa untouched.",
   "emptyFirstRun": "No partner login mfa yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner login mfa are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "login",
    "contract": "identity",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
    "operationId": "getGuestSession",
    "contract": "identity",
    "purpose": "Read the current guest session",
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
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `accountId`.",
   "preloaded": [
    "CreditPosition.id",
    "CreditPosition.accountId",
    "CreditPosition.accountName",
    "CreditPosition.creditLimit",
    "CreditPosition.used"
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
    "PTR-002",
    "PTR-004"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "accountId",
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId, so an edge into it must carry them"
    },
    {
     "to": "PTR-004",
     "trigger": "Notifications",
     "carries": [
      "messageId"
     ],
     "provenance": "derived — PTR-004 declares entryState.params messageId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every profile company",
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
       "label": "The selected profile company",
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
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createPrincipal",
       "label": "Create principal",
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
   "loading": "The profile company list.",
   "error": "Could not load. Names which read failed and leaves the profile company untouched.",
   "emptyFirstRun": "No profile company yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the profile company are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "PTR-002",
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "accountId",
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId, so an edge into it must carry them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "carries": [
      "principalId"
     ],
     "provenance": "derived — PTR-003 declares entryState.params principalId, so an edge into it must carry them"
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
       "label": "The selected notifications",
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
       "label": "Send",
       "operation": "sendTransactionalMessage",
       "provenance": "contract marketing-crm.yaml POST /messages"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "sendTransactionalMessage",
       "label": "Send transactional message",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "sendTransactionalMessage",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The notifications list.",
   "error": "Could not load. Names which read failed and leaves the notifications untouched.",
   "emptyFirstRun": "No notifications yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the notifications are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "sendTransactionalMessage",
    "contract": "marketing-crm",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
    "PTR-002",
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "accountId",
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId, so an edge into it must carry them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "carries": [
      "principalId"
     ],
     "provenance": "derived — PTR-003 declares entryState.params principalId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every api credentials integration",
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
       "label": "The selected api credentials integration",
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
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createApiClient",
       "provenance": "contract public-api.yaml POST /api-clients"
      },
      {
       "kind": "secondaryButton",
       "label": "Rotate",
       "operation": "rotateApiCredential",
       "provenance": "contract public-api.yaml POST /api-clients/{clientId}/credentials"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke",
       "operation": "revokeApiCredential",
       "provenance": "contract public-api.yaml DELETE /api-clients/{clientId}/credentials"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRevokeApiCredential",
    "component": "confirmDialog",
    "trigger": "Revoke",
    "body": "**Names what `revokeApiCredential` changes and what it leaves alone**, in the consequence rather than the verb. A api credentials integration this affects should be identified in the dialog, not just counted.",
    "provenance": "contract public-api.yaml DELETE /api-clients/{clientId}/credentials"
   }
  ],
  "states": {
   "loading": "Detail loads",
   "error": "Could not load",
   "emptyFirstRun": "Not found — it may have been deleted or moved out of scope",
   "emptyNoResults": "The filter narrowed it and the api credentials integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
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
    "PTR-002",
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "accountId",
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId, so an edge into it must carry them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "carries": [
      "principalId"
     ],
     "provenance": "derived — PTR-003 declares entryState.params principalId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every sub-agent",
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
       "label": "The selected sub-agent",
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
       "label": "Create",
       "operation": "createDelegatedAccess",
       "provenance": "contract identity.yaml POST /delegated-access"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
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
    "trigger": "Delete",
    "body": "**Names what `deleteDelegatedAccess` changes and what it leaves alone**, in the consequence rather than the verb. A sub-agent this affects should be identified in the dialog, not just counted.",
    "provenance": "contract identity.yaml DELETE /delegated-access/{delegatedAccessId}"
   }
  ],
  "states": {
   "loading": "The sub-agent list.",
   "error": "Could not load. Names which read failed and leaves the sub-agent untouched.",
   "emptyFirstRun": "No sub-agent yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sub-agent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createDelegatedAccess",
    "contract": "identity",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
  "parameters": [],
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
  "permission": null,
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
    "format": "uuid"
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
    "description": "**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing.\n",
    "items": {
     "type": "string"
    }
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
    "description": "13.1.38. Optional, and the strongest control available where an integrator has fixed egress.",
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
    ]
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
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
       "type": "string"
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
 "PartnerAgreement": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_agreement",
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
    "type": "string",
    "format": "uuid"
   },
   "partnerName": {
    "type": "string",
    "readOnly": true
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
    "description": "2.7.57. **A tier that changes at a threshold needs the sale to look back at cumulative volume, and nothing did.** Flat net rates and per-channel price lists cover the simple case and stop there.\n**The window is the argument, not the tier.** A partner who sells 400 in January and 400 in February is either a 400-tier partner twice or an 800-tier partner once, and the two are different money. `volumeWindow` says which.\n",
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
    "description": "Rates that change by date range. **Separate from the volume tier because they compound** — a peak-season rate at a high volume tier is both, and a single rate table cannot say so.\n",
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
    "description": "Per product or category. Absent means the commission applies across the catalogue.",
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
    "description": "BL-035. **`PartnerAgreement` covered commercial terms and not allocations.** A corporate account with fifty places for its staff is the same structure as a reseller with fifty to sell, and **the difference is that a corporate member does not pay.**\n",
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
