# P01-account-self-service-01 — P01 · Account & Self-Service

**5 screens · 46 operations · 37 schemas · 5 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## What to build

**A working surface, not a drawing of one.** The reference is `sources/designs/TICVAI_POS_Terminal_client_approved.html` — a Claude Design
build from these same sources, and the one the client responded to. Open it and match its depth:
real state, seeded data, controls that do something. Do not describe it, read it.

## What is in this folder

| file | what it is |
|---|---|
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, MARKETING_VIEW, ORDER_MODIFY, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **6 of these operations work offline**: getEntitlement, getGuestSession, getOrder, listConsentPurposes, listMyEntitlements, listOrders
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-016` | Login / Register | listDetail | 20 | 1 | — |
| `WEB-017` | My Account Dashboard | listDetail | 9 | 2 | — |
| `WEB-018` | My Tickets | listDetail | 8 | 0 | — |
| `WEB-019` | Order History | listDetail | 5 | 0 | — |
| `WEB-020` | Profile & Preferences | listDetail | 6 | 0 | — |

## Thin screens in this batch

**WEB-019 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-016",
  "name": "Login / Register",
  "module": "Account & Self-Service",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C36",
  "implementation": {
   "app": "guest-web",
   "route": "/account-and-self-service/login-register",
   "component": "apps/guest-web/src/routes/account-and-self-service/LoginRegisterList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-017",
    "WEB-018",
    "WEB-019"
   ],
   "transitions": [
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "carries": [
      "deviceId",
      "itemId",
      "subjectId"
     ],
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, subjectId, so an edge into it must carry them"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "carries": [
      "entitlementId",
      "orderId"
     ],
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId, so an edge into it must carry them"
    },
    {
     "to": "WEB-019",
     "trigger": "Order History",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-019 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "GST-039",
     "trigger": "They set a profile",
     "provenance": "flow F56 step 3→4",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Corrected 24 August**: removed getCurrentSession, logout, selectRole. **A guest surface has no roles to select and its own logout** — `selectRole` is ADR-0002 staff authorisation and `getCurrentSession` is the staff session. `guestLogout` and `getGuestSession` are the equivalents and both already existed. **The screen was calling the staff identity surface because nothing checked that a guest platform only calls guest operations.**",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMfaMethods` reads the population and `getGuestSession` reads one of them — list, select, act",
  "purpose": "Get a guest into the app, fast, on a device that may be shared.",
  "gaps": [
   {
    "operation": "listSsoProviders",
    "why": "**1 declared operation reach no component on this screen**: listSsoProviders. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every login register",
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
       "label": "The selected login register",
       "bindsTo": "GuestSession",
       "columns": [
        "GuestSession.subjectId",
        "GuestSession.displayName",
        "GuestSession.tokens",
        "GuestSession.isVerified",
        "GuestSession.identityProviders",
        "GuestSession.guestLinkId",
        "GuestSession.homeCellName",
        "GuestSession.preferredLanguage",
        "GuestSession.expiresAt"
       ],
       "operation": "getGuestSession",
       "provenance": "contract identity.yaml GET /auth/guest/session"
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
       "operation": "registerGuest",
       "provenance": "contract identity.yaml POST /auth/guest/register"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeSsoAuthorization",
       "provenance": "contract identity.yaml POST /auth/sso/{providerId}/callback"
      },
      {
       "kind": "secondaryButton",
       "label": "Enrol",
       "operation": "enrolMfaMethod",
       "provenance": "contract identity.yaml POST /auth/mfa/methods"
      },
      {
       "kind": "secondaryButton",
       "label": "Guest",
       "operation": "guestLogout",
       "provenance": "contract identity.yaml DELETE /auth/guest/session"
      },
      {
       "kind": "secondaryButton",
       "label": "Guest",
       "operation": "guestSocialLogin",
       "provenance": "contract identity.yaml POST /auth/guest/social"
      },
      {
       "kind": "secondaryButton",
       "label": "Guest",
       "operation": "guestUaePassLogin",
       "provenance": "contract identity.yaml POST /auth/guest/uae-pass"
      },
      {
       "kind": "secondaryButton",
       "label": "Link",
       "operation": "linkGuestCheckout",
       "provenance": "contract identity.yaml POST /auth/guest/link-checkout"
      },
      {
       "kind": "secondaryButton",
       "label": "Login",
       "operation": "login",
       "provenance": "contract identity.yaml POST /auth/login"
      },
      {
       "kind": "secondaryButton",
       "label": "Refresh",
       "operation": "refreshToken",
       "provenance": "contract identity.yaml POST /auth/refresh"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove",
       "operation": "removeMfaMethod",
       "provenance": "contract identity.yaml DELETE /auth/mfa/methods/{methodId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Request",
       "operation": "requestGuestOtp",
       "provenance": "contract identity.yaml POST /auth/guest/otp"
      },
      {
       "kind": "secondaryButton",
       "label": "Start",
       "operation": "startSsoAuthorization",
       "provenance": "contract identity.yaml GET /auth/sso/{providerId}/authorize"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyGuestOtp",
       "provenance": "contract identity.yaml POST /auth/guest/otp/verify"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyMfaChallenge",
       "provenance": "contract identity.yaml POST /auth/mfa/challenge/{challengeId}/verify"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyMfaEnrolment",
       "provenance": "contract identity.yaml POST /auth/mfa/methods/{methodId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Claim",
       "operation": "claimCart",
       "provenance": "contract orders.yaml POST /carts/{cartId}/claim"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveMfaMethod",
    "component": "confirmDialog",
    "trigger": "Remove",
    "body": "**Names what `removeMfaMethod` changes and what it leaves alone**, in the consequence rather than the verb. A login register this affects should be identified in the dialog, not just counted.",
    "provenance": "contract identity.yaml DELETE /auth/mfa/methods/{methodId}"
   }
  ],
  "states": {
   "loading": "The login register list.",
   "error": "Could not load. Names which read failed and leaves the login register untouched.",
   "emptyFirstRun": "No login register yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the login register are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "registerGuest",
    "contract": "identity",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "completeSsoAuthorization",
    "contract": "identity",
    "purpose": "Exchange an SSO code for a session",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "enrolMfaMethod",
    "contract": "identity",
    "purpose": "Enrol an MFA method",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "getGuestSession",
    "contract": "identity",
    "purpose": "Read the current guest session",
    "trigger": "onLoad"
   },
   {
    "operationId": "guestLogout",
    "contract": "identity",
    "purpose": "End a guest session",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "guestSocialLogin",
    "contract": "identity",
    "purpose": "Sign in with Apple or Google",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "guestUaePassLogin",
    "contract": "identity",
    "purpose": "Sign in with a national identity provider",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "linkGuestCheckout",
    "contract": "identity",
    "purpose": "Attach a guest checkout to an account",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
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
    "operationId": "login",
    "contract": "identity",
    "purpose": "Authenticate and open a session",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "refreshToken",
    "contract": "identity",
    "purpose": "Rotate the access token",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "removeMfaMethod",
    "contract": "identity",
    "purpose": "Remove an MFA method",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "requestGuestOtp",
    "contract": "identity",
    "purpose": "Request a one-time code",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "startSsoAuthorization",
    "contract": "identity",
    "purpose": "Begin an SSO flow",
    "trigger": "onLoad"
   },
   {
    "operationId": "verifyGuestOtp",
    "contract": "identity",
    "purpose": "Verify a one-time code and issue a session",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "verifyMfaChallenge",
    "contract": "identity",
    "purpose": "Complete a step-up challenge",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "verifyMfaEnrolment",
    "contract": "identity",
    "purpose": "Complete enrolment",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "claimCart",
    "contract": "orders",
    "purpose": "Attach an anonymous cart to a guest",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "createMfaChallenge",
    "contract": "identity",
    "purpose": "Second factor at sign-in",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    },
    {
     "name": "challengeId",
     "from": "deepLink"
    },
    {
     "name": "methodId",
     "from": "deepLink"
    },
    {
     "name": "providerId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `challengeId`, `methodId`, `providerId`.",
   "preloaded": [
    "GuestSession.subjectId",
    "GuestSession.displayName",
    "GuestSession.tokens",
    "GuestSession.isVerified",
    "GuestSession.identityProviders"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-016"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 19 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-017",
  "name": "My Account Dashboard",
  "module": "Account & Self-Service",
  "requiresModule": "marketing",
  "wave": 1,
  "capability": "C36",
  "implementation": {
   "app": "guest-web",
   "route": "/account-and-self-service/my-account-dashboard",
   "component": "apps/guest-web/src/routes/account-and-self-service/MyAccountDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-016",
    "WEB-018",
    "WEB-019"
   ],
   "transitions": [
    {
     "to": "WEB-016",
     "trigger": "Login / Register",
     "carries": [
      "cartId",
      "challengeId",
      "methodId",
      "providerId"
     ],
     "provenance": "derived — WEB-016 declares entryState.params cartId, challengeId, methodId, providerId, so an edge into it must carry them"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "carries": [
      "entitlementId",
      "orderId"
     ],
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId, so an edge into it must carry them"
    },
    {
     "to": "WEB-019",
     "trigger": "Order History",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-019 declares entryState.params orderId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 26 August** — `Dashboards Board` frame `web-017`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.",
  "density": "compact",
  "boardFrames": [
   "Dashboards Board.dc.html#web-017"
  ],
  "pattern": "listDetail",
  "patternReason": "`listGuestDevices` reads the population and `getWishlist` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every account",
       "bindsTo": "GuestDevice",
       "columns": [
        "GuestDevice.id",
        "GuestDevice.subjectId",
        "GuestDevice.platform",
        "GuestDevice.tokenFingerprint",
        "GuestDevice.appVersion",
        "GuestDevice.osVersion",
        "GuestDevice.deviceModel",
        "GuestDevice.locale",
        "GuestDevice.status",
        "GuestDevice.failureCount",
        "GuestDevice.registeredAt",
        "GuestDevice.lastSeenAt"
       ],
       "operation": "listGuestDevices",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/devices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected account",
       "bindsTo": "Wishlist",
       "columns": [
        "Wishlist.subjectId",
        "Wishlist.items"
       ],
       "operation": "getWishlist",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/wishlist"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add",
       "operation": "addToWishlist",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/wishlist"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordConsent",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "secondaryButton",
       "label": "Register",
       "operation": "registerGuestDevice",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/devices"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove",
       "operation": "removeFromWishlist",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/wishlist/{itemId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke",
       "operation": "revokeGuestDevice",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/devices/{deviceId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveFromWishlist",
    "component": "confirmDialog",
    "trigger": "Remove",
    "body": "**Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A account this affects should be identified in the dialog, not just counted.",
    "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/wishlist/{itemId}"
   },
   {
    "id": "confirmRevokeGuestDevice",
    "component": "confirmDialog",
    "trigger": "Revoke",
    "body": "**Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A account this affects should be identified in the dialog, not just counted.",
    "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/devices/{deviceId}"
   }
  ],
  "states": {
   "loading": "Tiles skeleton",
   "error": "Partial. Each tile fails independently",
   "emptyFirstRun": "A new account with no orders — offers what to do next",
   "emptyNoResults": "The filter narrowed it and the account are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "addToWishlist",
    "contract": "marketing-crm",
    "purpose": "Save an item",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "getWishlist",
    "contract": "marketing-crm",
    "purpose": "Read a guest's saved items",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGuestDevices",
    "contract": "marketing-crm",
    "purpose": "A guest's registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordConsent",
    "contract": "marketing-crm",
    "purpose": "Record a consent decision",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "registerGuestDevice",
    "contract": "marketing-crm",
    "purpose": "Register a device for push",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "removeFromWishlist",
    "contract": "marketing-crm",
    "purpose": "Remove a saved item",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "revokeGuestDevice",
    "contract": "marketing-crm",
    "purpose": "Revoke a device registration",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "getMyChallenges",
    "contract": "marketing-crm",
    "purpose": "Outstanding security challenges",
    "trigger": "onLoad"
   },
   {
    "operationId": "respondToInvitation",
    "contract": "marketing-crm",
    "purpose": "Accept or decline an invitation",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "deviceId",
     "from": "deepLink"
    },
    {
     "name": "itemId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "token",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `deviceId`, `itemId`.",
   "preloaded": [
    "Wishlist.subjectId",
    "Wishlist.items"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-017",
   "note": "**Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-018",
  "name": "My Tickets",
  "module": "Account & Self-Service",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C09",
  "implementation": {
   "app": "guest-web",
   "route": "/account-and-self-service/my-tickets",
   "component": "apps/guest-web/src/routes/account-and-self-service/MyTicketsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-016",
    "WEB-017",
    "WEB-019"
   ],
   "transitions": [
    {
     "to": "WEB-016",
     "trigger": "Login / Register",
     "carries": [
      "cartId",
      "challengeId",
      "methodId",
      "providerId"
     ],
     "provenance": "derived — WEB-016 declares entryState.params cartId, challengeId, methodId, providerId, so an edge into it must carry them"
    },
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "carries": [
      "deviceId",
      "itemId",
      "subjectId"
     ],
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, subjectId, so an edge into it must carry them"
    },
    {
     "to": "WEB-019",
     "trigger": "Order History",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-019 declares entryState.params orderId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Dynamic QR with a visible countdown. Anti-screenshot, per the guest boards. Purpose derived from the screen name and its operations on 17 August, not from a requirement. The read surface Deep asked for. **All four were missing and the table itself did not exist until 18 August.** **Rewired on the 20 August review.** **`listEntitlements` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Cross-surface parity, 31 August**: added transferOrderTickets. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMyEntitlements` reads the population and `getEntitlement` reads one of them — list, select, act",
  "purpose": "Find my tickets for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementCredential",
    "why": "**3 declared operations reach no component on this screen**: getEntitlementCredential, getEntitlementHistory, listEntitlements. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every tickets",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom"
       ],
       "operation": "listMyEntitlements",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected tickets",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom",
        "Entitlement.validTo",
        "Entitlement.entriesUsed",
        "Entitlement.entriesAllowed",
        "Entitlement.lastEntryAt"
       ],
       "operation": "getEntitlement",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
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
       "impliedBy": "listMyEntitlements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tickets load",
   "error": "Could not load",
   "emptyFirstRun": "No tickets — distinguishes never bought from all past",
   "emptyNoResults": "Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMyEntitlements",
    "contract": "access",
    "purpose": "Every ticket, pass and membership this guest holds",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlement",
    "contract": "access",
    "purpose": "One entitlement, with what remains on it",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementCredential",
    "contract": "access",
    "purpose": "The thing that gets scanned",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementHistory",
    "contract": "access",
    "purpose": "Every scan, freeze, share and reissue against it",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEntitlements",
    "contract": "access",
    "purpose": "Every entitlement this guest holds, including expired",
    "trigger": "onLoad"
   },
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction",
    "invalidates": [
     "listMyEntitlements"
    ]
   },
   {
    "operationId": "issueWalletPass",
    "contract": "orders",
    "purpose": "Add the ticket to a phone wallet from the desktop",
    "trigger": "onAction"
   },
   {
    "operationId": "shareEntitlement",
    "contract": "orders",
    "purpose": "Send a ticket to somebody",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entitlementId",
     "from": "deepLink"
    },
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A ticket link opened after the event.** Shows the entitlement with its status — expired, used, transferred — because *not found* to somebody holding a ticket is the wrong answer.",
   "preloaded": [
    "Entitlement.id",
    "Entitlement.templateId",
    "Entitlement.productId",
    "Entitlement.orderId",
    "Entitlement.orderLineId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-018"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-019",
  "name": "Order History",
  "module": "Account & Self-Service",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C34",
  "implementation": {
   "app": "guest-web",
   "route": "/account-and-self-service/order-history",
   "component": "apps/guest-web/src/routes/account-and-self-service/OrderHistoryList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-016",
    "WEB-017",
    "WEB-018"
   ],
   "transitions": [
    {
     "to": "WEB-016",
     "trigger": "Login / Register",
     "carries": [
      "cartId",
      "challengeId",
      "methodId",
      "providerId"
     ],
     "provenance": "derived — WEB-016 declares entryState.params cartId, challengeId, methodId, providerId, so an edge into it must carry them"
    },
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "carries": [
      "deviceId",
      "itemId",
      "subjectId"
     ],
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, subjectId, so an edge into it must carry them"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "carries": [
      "entitlementId",
      "orderId"
     ],
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`listMyOrders` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Cross-surface parity, 31 August**: added getOrder, listOrders. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMyOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Find order history for this venue.",
  "gaps": [
   {
    "operation": "listOrders",
    "why": "**1 declared operation reach no component on this screen**: listOrders. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every order history",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount"
       ],
       "operation": "listMyOrders",
       "provenance": "contract orders.yaml GET /my/orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order history",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order history list.",
   "error": "Could not load. Names which read failed and leaves the order history untouched.",
   "emptyFirstRun": "No order history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction",
    "invalidates": [
     "listMyOrders"
    ]
   },
   {
    "operationId": "listMyOrders",
    "contract": "orders",
    "purpose": "The orders this guest placed",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRefundRequest",
    "contract": "orders",
    "purpose": "Ask for a refund",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "Order.id",
    "Order.orderNumber",
    "Order.channel",
    "Order.venueId",
    "Order.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-019"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-020",
  "name": "Profile & Preferences",
  "module": "Account & Self-Service",
  "requiresModule": "marketing",
  "wave": 1,
  "capability": "C36",
  "implementation": {
   "app": "guest-web",
   "route": "/account-and-self-service/profile-and-preferences",
   "component": "apps/guest-web/src/routes/account-and-self-service/ProfileAndPreferencesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-016",
    "WEB-017",
    "WEB-018"
   ],
   "transitions": [
    {
     "to": "WEB-016",
     "trigger": "Login / Register",
     "carries": [
      "cartId",
      "challengeId",
      "methodId",
      "providerId"
     ],
     "provenance": "derived — WEB-016 declares entryState.params cartId, challengeId, methodId, providerId, so an edge into it must carry them"
    },
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "carries": [
      "deviceId",
      "itemId",
      "subjectId"
     ],
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, subjectId, so an edge into it must carry them"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "carries": [
      "entitlementId",
      "orderId"
     ],
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Consent withdrawal must be as easy as granting it. Same screen, same number of clicks. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Profile and Preferences. **Wishlist and device operations removed; profile, consent and email verification added.** Deep listed exactly these. **Rewired on the 20 August review.**",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listConsentPurposes` reads the population and `getGuestProfile` reads one of them — list, select, act",
  "purpose": "Change how profile behaves here, and see which level the current value came from.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every profile preferences",
       "bindsTo": "ConsentPurposeConfig",
       "columns": [
        "ConsentPurposeConfig.purpose",
        "ConsentPurposeConfig.displayName",
        "ConsentPurposeConfig.description",
        "ConsentPurposeConfig.channels",
        "ConsentPurposeConfig.noticeVersion",
        "ConsentPurposeConfig.isRequiredForService",
        "ConsentPurposeConfig.expiresAfterMonths"
       ],
       "operation": "listConsentPurposes",
       "provenance": "contract marketing-crm.yaml GET /consent-purposes"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected profile preferences",
       "bindsTo": "GuestProfileDetail",
       "columns": [
        "GuestProfileDetail.id",
        "GuestProfileDetail.subjectId",
        "GuestProfileDetail.displayName",
        "GuestProfileDetail.email",
        "GuestProfileDetail.phone",
        "GuestProfileDetail.preferredLanguage",
        "GuestProfileDetail.preferredChannel",
        "GuestProfileDetail.guestLinkId",
        "GuestProfileDetail.tags",
        "GuestProfileDetail.engagementScore",
        "GuestProfileDetail.engagementTier",
        "GuestProfileDetail.lifetimeValue",
        "GuestProfileDetail.visitCount",
        "GuestProfileDetail.lastVisitAt",
        "GuestProfileDetail.isActive",
        "GuestProfileDetail.consents"
       ],
       "operation": "getGuestProfile",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}"
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
       "operation": "updateMyProfile",
       "provenance": "contract marketing-crm.yaml PATCH /guests/me/profile"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordConsent",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyGuestEmail",
       "provenance": "contract identity.yaml POST /auth/guest/verify-email"
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
       "impliedBy": "updateMyProfile",
       "label": "Save my profile",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listConsentPurposes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateMyProfile",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Profile and consents",
   "error": "**Save failed and the form keeps what was typed.** A consent change that silently did not save is a compliance failure, so the screen states it rather than showing success",
   "emptyFirstRun": "—",
   "emptyNoResults": "Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Read a guest profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateMyProfile",
    "contract": "marketing-crm",
    "purpose": "A guest correcting their own details",
    "trigger": "onAction",
    "invalidates": [
     "listConsentPurposes"
    ]
   },
   {
    "operationId": "recordConsent",
    "contract": "marketing-crm",
    "purpose": "Record a consent decision",
    "trigger": "onAction",
    "invalidates": [
     "listConsentPurposes"
    ]
   },
   {
    "operationId": "listConsentPurposes",
    "contract": "marketing-crm",
    "purpose": "Configured consent purposes",
    "trigger": "onLoad"
   },
   {
    "operationId": "verifyGuestEmail",
    "contract": "identity",
    "purpose": "Send a verification link, or consume one",
    "trigger": "onAction",
    "invalidates": [
     "listConsentPurposes"
    ]
   },
   {
    "operationId": "updateGuestPreferences",
    "contract": "marketing-crm",
    "purpose": "Change contact and consent preferences",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "GuestProfileDetail.id",
    "GuestProfileDetail.subjectId",
    "GuestProfileDetail.displayName",
    "GuestProfileDetail.email",
    "GuestProfileDetail.phone"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-020"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
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
 "addToWishlist": {
  "method": "POST",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Save an item",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Wishlist"
 },
 "claimCart": {
  "method": "POST",
  "path": "/carts/{cartId}/claim",
  "contract": "orders",
  "summary": "Attach an anonymous cart to a guest",
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
  "responds": "CartMergeResult"
 },
 "completeSsoAuthorization": {
  "method": "POST",
  "path": "/auth/sso/{providerId}/callback",
  "contract": "identity",
  "summary": "Exchange an SSO code for a session",
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
  "responds": "LoginResponse"
 },
 "createMfaChallenge": {
  "method": "POST",
  "path": "/auth/mfa/challenge",
  "contract": "identity",
  "summary": "Step-up authentication for a sensitive action",
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
 "createRefundRequest": {
  "method": "POST",
  "path": "/refund-requests",
  "contract": "orders",
  "summary": "Guest-initiated refund request",
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
 "getEntitlement": {
  "method": "GET",
  "path": "/entitlements/{entitlementId}",
  "contract": "access",
  "summary": "One entitlement, with what remains on it",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Entitlement"
 },
 "getEntitlementCredential": {
  "method": "GET",
  "path": "/entitlements/{entitlementId}/credential",
  "contract": "access",
  "summary": "The thing that gets scanned",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "rotate",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getEntitlementHistory": {
  "method": "GET",
  "path": "/entitlements/{entitlementId}/history",
  "contract": "access",
  "summary": "Every scan, freeze, share and reissue against it",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "getGuestProfile": {
  "method": "GET",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Read a guest profile",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestProfileDetail"
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
 "getMyChallenges": {
  "method": "GET",
  "path": "/guests/me/challenges",
  "contract": "marketing-crm",
  "summary": "Active challenges and how far along I am",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ChallengeProgress"
 },
 "getOrder": {
  "method": "GET",
  "path": "/orders/{orderId}",
  "contract": "orders",
  "summary": "Read an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Order"
 },
 "getWishlist": {
  "method": "GET",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Read a guest's saved items",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [],
  "requestBody": null,
  "responds": "Wishlist"
 },
 "guestLogout": {
  "method": "DELETE",
  "path": "/auth/guest/session",
  "contract": "identity",
  "summary": "End a guest session",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "allDevices",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "guestSocialLogin": {
  "method": "POST",
  "path": "/auth/guest/social",
  "contract": "identity",
  "summary": "Sign in with Apple or Google",
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
  "responds": "GuestSession"
 },
 "guestUaePassLogin": {
  "method": "POST",
  "path": "/auth/guest/uae-pass",
  "contract": "identity",
  "summary": "Sign in with a national identity provider",
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
  "responds": "GuestSession"
 },
 "issueWalletPass": {
  "method": "POST",
  "path": "/wallet-passes",
  "contract": "orders",
  "summary": "Generate an Apple or Google wallet pass",
  "permission": "ORDER_VIEW",
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
  "responds": "WalletPass"
 },
 "linkGuestCheckout": {
  "method": "POST",
  "path": "/auth/guest/link-checkout",
  "contract": "identity",
  "summary": "Attach a guest checkout to an account",
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
 "listConsentPurposes": {
  "method": "GET",
  "path": "/consent-purposes",
  "contract": "marketing-crm",
  "summary": "Configured consent purposes",
  "permission": "GUEST_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
  "responds": "ConsentPurposeConfig"
 },
 "listEntitlements": {
  "method": "GET",
  "path": "/my/entitlements/all",
  "contract": "access",
  "summary": "Every entitlement this guest holds, including expired",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "includeExpired",
    "in": "query",
    "required": false
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
  "responds": "Entitlement"
 },
 "listGuestDevices": {
  "method": "GET",
  "path": "/guests/{subjectId}/devices",
  "contract": "marketing-crm",
  "summary": "A guest's registered devices",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
  "responds": "GuestDevice"
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
 "listMyEntitlements": {
  "method": "GET",
  "path": "/guests/me/entitlements",
  "contract": "access",
  "summary": "Every ticket, pass and membership this guest holds",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "state",
    "in": "query",
    "required": null
   },
   {
    "name": "includeShared",
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
  "responds": "Entitlement"
 },
 "listMyOrders": {
  "method": "GET",
  "path": "/my/orders",
  "contract": "orders",
  "summary": "The orders this guest placed",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "since",
    "in": "query",
    "required": false
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
  "responds": "Order"
 },
 "listOrders": {
  "method": "GET",
  "path": "/orders",
  "contract": "orders",
  "summary": "List orders",
  "permission": "ORDER_VIEW",
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
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "createdTo",
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
 "recordConsent": {
  "method": "POST",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Record a consent decision",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecordConsentRequest",
  "responds": "ConsentState"
 },
 "refreshToken": {
  "method": "POST",
  "path": "/auth/refresh",
  "contract": "identity",
  "summary": "Rotate the access token",
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
  "responds": "TokenPair"
 },
 "registerGuest": {
  "method": "POST",
  "path": "/auth/guest/register",
  "contract": "identity",
  "summary": "Create a guest account",
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
  "requestBody": "RegisterGuestRequest",
  "responds": "GuestSession"
 },
 "registerGuestDevice": {
  "method": "POST",
  "path": "/guests/{subjectId}/devices",
  "contract": "marketing-crm",
  "summary": "Register a device for push",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestDevice"
 },
 "removeFromWishlist": {
  "method": "DELETE",
  "path": "/guests/{subjectId}/wishlist/{itemId}",
  "contract": "marketing-crm",
  "summary": "Remove a saved item",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
 "requestGuestOtp": {
  "method": "POST",
  "path": "/auth/guest/otp",
  "contract": "identity",
  "summary": "Request a one-time code",
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
 "respondToInvitation": {
  "method": "POST",
  "path": "/invitations/{token}/respond",
  "contract": "marketing-crm",
  "summary": "Accept or decline",
  "permission": "GUEST_VIEW",
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
  "responds": "Invitation"
 },
 "revokeGuestDevice": {
  "method": "DELETE",
  "path": "/guests/{subjectId}/devices/{deviceId}",
  "contract": "marketing-crm",
  "summary": "Revoke a device registration",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
 "shareEntitlement": {
  "method": "POST",
  "path": "/entitlements/{entitlementId}/share",
  "contract": "orders",
  "summary": "Let somebody else use this, without giving it away",
  "permission": "ORDER_MODIFY",
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
  "responds": "Problem"
 },
 "startSsoAuthorization": {
  "method": "GET",
  "path": "/auth/sso/{providerId}/authorize",
  "contract": "identity",
  "summary": "Begin an SSO flow",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "redirectUri",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "transferOrderTickets": {
  "method": "POST",
  "path": "/orders/{orderId}/transfer",
  "contract": "orders",
  "summary": "Transfer tickets to another guest",
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
 "updateGuestPreferences": {
  "method": "PUT",
  "path": "/guests/{subjectId}/preferences",
  "contract": "marketing-crm",
  "summary": "The things a regular should not have to say twice",
  "permission": "GUEST_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "subject",
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
 "updateMyProfile": {
  "method": "PATCH",
  "path": "/guests/me/profile",
  "contract": "marketing-crm",
  "summary": "A guest correcting their own details",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestProfile"
 },
 "verifyGuestEmail": {
  "method": "POST",
  "path": "/auth/guest/verify-email",
  "contract": "identity",
  "summary": "Send a verification link, or consume one",
  "permission": "GUEST_VIEW",
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
 "verifyGuestOtp": {
  "method": "POST",
  "path": "/auth/guest/otp/verify",
  "contract": "identity",
  "summary": "Verify a one-time code and issue a session",
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
  "responds": "GuestSession"
 },
 "verifyMfaChallenge": {
  "method": "POST",
  "path": "/auth/mfa/challenge/{challengeId}/verify",
  "contract": "identity",
  "summary": "Complete a step-up challenge",
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
 "Cart": {
  "type": "object",
  "x-ticvai-persistence": "orders.cart",
  "required": [
   "id",
   "venueId",
   "channel",
   "status",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "token": {
    "type": "string",
    "readOnly": true,
    "description": "**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null while anonymous. Set by `claimCart`."
   },
   "status": {
    "$ref": "#/components/schemas/CartStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CartLine"
    }
   },
   "conflicts": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CartConflict"
    }
   },
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "appliedPromotionIds": {
    "type": "array",
    "description": "**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "The earliest lease expiry in the cart, or the cart's own window where it holds none."
   },
   "extensionsUsed": {
    "type": "integer",
    "readOnly": true
   },
   "maxExtensions": {
    "type": "integer",
    "readOnly": true
   },
   "locale": {
    "type": "string"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CartMergeResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "cart"
  ],
  "properties": {
   "cart": {
    "$ref": "#/components/schemas/Cart"
   },
   "mergedLineCount": {
    "type": "integer"
   },
   "droppedLines": {
    "type": "array",
    "description": "**Reported, never silent.** Lines that could not be re-leased on merge are named, so a guest signing in is told what they lost rather than discovering it at checkout.\n",
    "items": {
     "type": "object",
     "properties": {
      "productName": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "noCapacity",
        "expired",
        "notSellableOnChannel",
        "duplicate"
       ]
      }
     }
    }
   }
  }
 },
 "ChallengeProgress": {
  "type": "object",
  "x-ticvai-persistence": "marketing.challenge_progress",
  "description": "22.6.15. **Progress is shown, not just the outcome.** A guest two visits from a reward behaves differently from one who does not know how close they are, which is the entire mechanism.\n",
  "required": [
   "id",
   "challengeId",
   "subjectId",
   "current",
   "target"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "challengeId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "portfolioId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a family or group challenge — where the shared progress accrues."
   },
   "current": {
    "type": "number"
   },
   "target": {
    "type": "number"
   },
   "streakCount": {
    "type": "integer",
    "nullable": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "rewardIssuedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ConsentDecision": {
  "type": "string",
  "enum": [
   "granted",
   "withdrawn",
   "notAsked"
  ]
 },
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "ConsentPurposeConfig": {
  "x-ticvai-persistence": "marketing.consent_purpose",
  "type": "object",
  "required": [
   "purpose",
   "channels",
   "noticeVersion",
   "isRequiredForService"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "displayName": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string",
    "description": "Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"
   },
   "isRequiredForService": {
    "type": "boolean",
    "description": "True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"
   },
   "expiresAfterMonths": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded"
  ]
 },
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "Entitlement": {
  "type": "object",
  "x-ticvai-persistence": "access.entitlement",
  "description": "**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n",
  "required": [
   "id",
   "templateId",
   "productId",
   "orderId",
   "subjectId",
   "status",
   "validFrom",
   "validTo"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "A ULID, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "description": "The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "mediaCode": {
    "type": "string",
    "description": "What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"
   },
   "status": {
    "$ref": "../spine/orders.yaml#/components/schemas/EntitlementStatus"
   },
   "statusNote": {
    "type": "string",
    "nullable": true,
    "description": "**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n"
   },
   "entriesUsed": {
    "type": "integer",
    "default": 0,
    "description": "**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true
   },
   "lastEntryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "frozenDays": {
    "type": "integer",
    "default": 0,
    "description": "Days added by a freeze. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"
   },
   "suspendedReason": {
    "type": "string",
    "nullable": true
   },
   "isNameBound": {
    "type": "boolean",
    "default": false
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "sharedWithSubjectIds": {
    "type": "array",
    "description": "`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedVia": {
    "type": "string",
    "enum": [
     "sale",
     "invitation",
     "reissue",
     "transfer",
     "resale",
     "membership",
     "groupBooking"
    ],
    "description": "**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"
   },
   "supersedesEntitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"
   },
   "walletValueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"
   }
  }
 },
 "GuestDevice": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_device",
  "required": [
   "id",
   "subjectId",
   "platform",
   "status",
   "registeredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android",
     "web"
    ]
   },
   "tokenFingerprint": {
    "type": "string",
    "description": "Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"
   },
   "appVersion": {
    "type": "string",
    "nullable": true
   },
   "osVersion": {
    "type": "string",
    "nullable": true
   },
   "deviceModel": {
    "type": "string",
    "nullable": true
   },
   "locale": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "revoked",
     "failed"
    ]
   },
   "failureCount": {
    "type": "integer",
    "description": "Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"
   },
   "registeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastSeenAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GuestProfile": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "type": "object",
  "required": [
   "subjectId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "nullable": true
   },
   "phone": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "preferredChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells. Marketing acts locally."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "engagementScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"
   },
   "engagementTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "new",
     "active",
     "occasional",
     "lapsing",
     "lapsed",
     "dormant"
    ],
    "description": "5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"
   },
   "lifetimeValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "visitCount": {
    "type": "integer"
   },
   "lastVisitAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "GuestProfileDetail": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "allOf": [
   {
    "$ref": "#/components/schemas/GuestProfile"
   },
   {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
     },
     "consents": {
      "$ref": "#/components/schemas/ConsentState"
     },
     "loyalty": {
      "$ref": "#/components/schemas/LoyaltyPosition"
     },
     "openCaseCount": {
      "type": "integer"
     },
     "recentOrderIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "membershipIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "notes": {
      "type": "string",
      "nullable": true
     }
    }
   }
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
 "Invitation": {
  "type": "object",
  "x-ticvai-persistence": "marketing.invitation",
  "description": "**Addressed and tokenised.** A guest accepting an invitation is claiming a specific place, not buying one.\n",
  "required": [
   "id",
   "campaignId",
   "token",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recipientEmail": {
    "type": "string",
    "format": "email",
    "nullable": true
   },
   "token": {
    "type": "string",
    "description": "**Single-use and unguessable.** An invitation link forwarded to a group chat is the failure mode, and a token that survives its first use is one that ends up there.\n"
   },
   "plusOnes": {
    "type": "integer",
    "default": 0
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "viewed",
     "accepted",
     "declined",
     "expired",
     "revoked"
    ]
   },
   "entitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "respondedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
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
    "description": "Returned once on successful verification. Not retrievable afterwards.",
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
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
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
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "nullable": true
   },
   "subjectId": {
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
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderLine"
   },
   {
    "type": "object",
    "required": [
     "serverUnitPrice",
     "taxAmount",
     "netAmount",
     "grossAmount"
    ],
    "properties": {
     "serverUnitPrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "What the server computed on ingest."
     },
     "priceVariance": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"
     },
     "taxAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "netAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "grossAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "entitlementIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     }
    }
   }
  ]
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
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
 "Payment": {
  "x-ticvai-persistence": "orders.payment",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "status",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "The amount in `tenderCurrency`, at that currency's own scale."
   },
   "fxRate": {
    "type": "number",
    "nullable": true,
    "description": "The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"
   },
   "fxRateSource": {
    "type": "string",
    "nullable": true,
    "enum": [
     "manual",
     "feed",
     "cardScheme"
    ],
    "description": "4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"
   },
   "changeCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "changeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "authorised",
     "captured",
     "pendingConfirmation",
     "declined",
     "failed",
     "voided",
     "refunded"
    ]
   },
   "providerName": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "lastInquiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "Problem": {
  "type": "object",
  "description": "RFC 9457 problem details. Every error response uses this shape.",
  "required": [
   "type",
   "title",
   "status"
  ],
  "properties": {
   "type": {
    "type": "string",
    "format": "uri"
   },
   "title": {
    "type": "string"
   },
   "status": {
    "type": "integer"
   },
   "detail": {
    "type": "string"
   },
   "instance": {
    "type": "string"
   },
   "traceId": {
    "type": "string"
   },
   "errors": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "code"
     ],
     "properties": {
      "field": {
       "type": "string"
      },
      "code": {
       "type": "string"
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "RecordConsentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "purpose",
   "decision",
   "noticeVersion",
   "source",
   "recordedAt"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "decision": {
    "$ref": "#/components/schemas/ConsentDecision"
   },
   "channels": {
    "type": "array",
    "description": "Omit to apply to every channel the purpose covers.",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string"
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "RegisterGuestRequest": {
  "type": "object",
  "required": [
   "identifier",
   "channel"
  ],
  "properties": {
   "identifier": {
    "type": "string",
    "maxLength": 256,
    "description": "Email address or mobile number in E.164."
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "sms",
     "whatsapp"
    ]
   },
   "displayName": {
    "type": "string",
    "maxLength": 200
   },
   "password": {
    "type": "string",
    "minLength": 8,
    "maxLength": 256,
    "description": "Optional. OTP-only accounts are supported and are the default."
   },
   "preferredLanguage": {
    "type": "string",
    "pattern": "^[a-z]{2}$"
   },
   "consents": {
    "type": "array",
    "description": "Consent captured at registration, recorded with the notice version.",
    "items": {
     "type": "object",
     "properties": {
      "purpose": {
       "type": "string"
      },
      "granted": {
       "type": "boolean"
      },
      "noticeVersion": {
       "type": "string"
      }
     }
    }
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
 "WalletPass": {
  "type": "object",
  "x-ticvai-persistence": "orders.wallet_pass",
  "description": "BL-029. **`appleWallet` and `googlePay` are feature toggles on the native apps** — there is no pass generation, no update push, no serial and no authentication token.\n**A wallet pass is a live object, not a download.** The value over a PDF is that it updates: a changed gate, a cancelled performance, a time that moved. **A pass that cannot be pushed to is a screenshot with better rounding.**\n",
  "required": [
   "id",
   "entitlementId",
   "platform",
   "serialNumber",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "platform": {
    "type": "string",
    "enum": [
     "apple",
     "google"
    ]
   },
   "serialNumber": {
    "type": "string"
   },
   "authenticationToken": {
    "type": "string",
    "format": "password",
    "description": "**Write-only.** How the device proves it may fetch an update, and the reason a leaked serial alone is not enough to read somebody's ticket.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "updated",
     "voided",
     "expired"
    ]
   },
   "lastPushedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "deviceRegistrations": {
    "type": "integer",
    "description": "How many devices hold it. **A guest with the pass on a phone and a watch is one entitlement and two registrations**, and both need the update.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "Wishlist": {
  "type": "object",
  "required": [
   "subjectId",
   "items"
  ],
  "x-ticvai-persistence": "none — wrapper. The items are the table, keyed by subject",
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "items": {
    "type": "array",
    "x-ticvai-persistence": "marketing.wishlist_item",
    "items": {
     "type": "object",
     "required": [
      "id",
      "variantId",
      "addedAt",
      "isAvailable"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "productName": {
       "type": "string"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceStartsAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "imageAssetRef": {
       "type": "string",
       "nullable": true
      },
      "isAvailable": {
       "type": "boolean",
       "description": "False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"
      },
      "unavailableReason": {
       "type": "string",
       "nullable": true
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 }
}
```
