# P01-account-self-service-01 — P01 · Account & Self-Service

**5 screens · 47 operations · 48 schemas · 7 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, LEDGER_POST, LEDGER_VIEW, MARKETING_VIEW, ORDER_MODIFY, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-016` | Login / Register | form | 14 | 8 | — |
| `WEB-017` | My Account Dashboard | listDetail | 9 | 6 | — |
| `WEB-018` | My Tickets | listDetail | 8 | 3 | — |
| `WEB-019` | Order History | listDetail | 10 | 2 | — |
| `WEB-020` | Profile & Preferences | listDetail | 8 | 4 | — |

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
    "WEB-001",
    "WEB-010",
    "WEB-008",
    "WEB-012",
    "WEB-005",
    "WEB-049"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-010",
    "WEB-011",
    "WEB-012",
    "WEB-017",
    "WEB-018",
    "WEB-019"
   ],
   "transitions": [
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, token and WEB-016 holds none of them, so the edge carries nothing and WEB-017 opens cold"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId and WEB-016 holds none of them, so the edge carries nothing and WEB-018 opens cold"
    },
    {
     "to": "WEB-019",
     "trigger": "Order History",
     "provenance": "derived — WEB-019 declares entryState.params documentId, invoiceId, orderId and WEB-016 holds none of them, so the edge carries nothing and WEB-019 opens cold"
    },
    {
     "to": "WEB-010",
     "trigger": "Signed in and verified — back to the cart",
     "precondition": "arrived from the cart",
     "carries": [
      "cartId"
     ],
     "provenance": "decided 17 September 2026 — no order against an unproven contact; rule on identity verifyGuestEmail, per-site guestCheckout off by default (matrix 2.6.28)"
    },
    {
     "to": "WEB-011",
     "trigger": "Guest Details & Attendee Forms",
     "provenance": "derived — WEB-011 declares entryState.params deviceId, itemId and WEB-016 holds none of them, so the edge carries nothing and WEB-011 opens cold"
    },
    {
     "to": "WEB-012",
     "trigger": "Checkout — Payment",
     "provenance": "derived — WEB-012 declares entryState.params orderId, paymentId and WEB-016 holds none of them, so the edge carries nothing and WEB-012 opens cold"
    },
    {
     "to": "GST-039",
     "trigger": "They set a profile",
     "provenance": "flow F56 step 3→4",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "subjectId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Corrected 24 August**: removed getCurrentSession, logout, selectRole. **A guest surface has no roles to select and its own logout** — `selectRole` is ADR-0002 staff authorisation and `getCurrentSession` is the staff session. `guestLogout` and `getGuestSession` are the equivalents and both already existed. **The screen was calling the staff identity surface because nothing checked that a guest platform only calls guest operations.** **Rebuilt 28 September as a guest sign-in form** (decided 28 September, audit R167, R073 (a)): removed `login`, `startSsoAuthorization`, `completeSsoAuthorization`, `listSsoProviders` and the six MFA operations — guests have no enterprise SSO. **The second factor came back on 29 September, per venue** (see below). Password sign-in is `guestPasswordLogin`.\n\n**Rev 3 (decided 29 September).** **Guest two-step verification is a per-venue setting, off by default** (GAP-B1, per venue, `VenueSettings.identity.guestTwoStep`; supersedes the second part of audit R167, *no guest MFA*; the first part, no enterprise SSO for guests, stands). The prompt appears only when the guest signs in at, or acts at, a venue that has it on; enrolment is on the guest's account (WEB-024). **Sign-in gate (REV3-3):** this screen is where WEB-008 (after add-ons) or WEB-012 (at payment) sends a guest who is not signed in, and it returns them to the cart with the basket kept; a guest code is offered instead when guest checkout is on (`FeatureToggle guestCheckout`, off by default; match returning guests by `GuestMatchPolicy.matchBy`; DG-1, no change). UAE Pass and linking guest checkouts are declared (GAP-B3, already).\n\n**The venue in context is sent** (decided 29 September, rev 3 GAP-B1, per venue): `verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin` and `createMfaChallenge` take an optional `venueId`, the venue the app or booking is in, so the second factor is asked only where that venue has guest two-step verification on.\n\n**29 September (W1).** The guest pop-up asks only `guestContactFields` (Email only / + name / + mobile) and the code; after the code nothing is asked again and the guest returns to the cart and on to the T&Cs.",
  "density": "compact",
  "pattern": "form",
  "patternReason": "**A sign-in form, not a list.** Four ways in (a one-time code, a password, Apple or Google, UAE Pass) and a way to register; `getGuestSession` is the one piece of context. Rebuilt 28 September: the screen had been generated as a list of MFA methods and SSO providers, neither of which a guest has (decided 28 September, audit R167, R073 (a)). The second-factor prompt is back as a step of sign-in, only at a venue that has guest two-step verification on (decided 29 September, rev 3 GAP-B1).",
  "purpose": "Get a guest into the site, fast, on a device that may be shared: a one-time code to the email or mobile, a password, Apple or Google, or UAE Pass, or register a new account. **No enterprise SSO for guests** (decided 28 September, audit R167, first part). **A second factor only where the venue enabled guest two-step verification** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of R167).",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "signIn",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Email or mobile number",
       "operation": "requestGuestOtp",
       "notes": "**Guest checkout asks only the configured fields** (W1): `BookingFlowSettings.guestContactFields` (email, mobile, name).",
       "provenance": "contract identity.yaml POST /auth/guest/otp"
      },
      {
       "kind": "primaryButton",
       "label": "Send me a code",
       "operation": "requestGuestOtp",
       "provenance": "contract identity.yaml POST /auth/guest/otp"
      },
      {
       "kind": "textField",
       "label": "Code",
       "operation": "verifyGuestOtp",
       "notes": "Shown once a code has been sent; `verifyGuestOtp` returns the `GuestSession`.",
       "provenance": "contract identity.yaml POST /auth/guest/otp/verify"
      },
      {
       "kind": "primaryButton",
       "label": "Sign in with the code",
       "operation": "verifyGuestOtp",
       "provenance": "contract identity.yaml POST /auth/guest/otp/verify"
      },
      {
       "kind": "textField",
       "label": "Password",
       "operation": "guestPasswordLogin",
       "notes": "**Password sign-in** (decided 28 September, audit R073 (a)): sends `identifier`, `password` and the device's `deviceId` to `guestPasswordLogin`, which returns the same `GuestSession`. A wrong password, an unknown identifier and an account with no password are one answer (401) and the screen shows one message for all of them, never which it was. Signing in here ends this device's previous guest session.",
       "provenance": "contract identity.yaml POST /auth/guest/password"
      },
      {
       "kind": "secondaryButton",
       "label": "Sign in with password",
       "operation": "guestPasswordLogin",
       "provenance": "contract identity.yaml POST /auth/guest/password"
      },
      {
       "kind": "secondaryButton",
       "label": "Continue with Apple or Google",
       "operation": "guestSocialLogin",
       "provenance": "contract identity.yaml POST /auth/guest/social"
      },
      {
       "kind": "secondaryButton",
       "label": "Continue with UAE Pass",
       "operation": "guestUaePassLogin",
       "provenance": "contract identity.yaml POST /auth/guest/uae-pass"
      },
      {
       "kind": "secondaryButton",
       "label": "Create an account",
       "operation": "registerGuest",
       "provenance": "contract identity.yaml POST /auth/guest/register"
      },
      {
       "kind": "textField",
       "label": "Verification code",
       "notes": "**Only when the returned `GuestSession` has `requiresMfa`**, which happens only at a venue whose `VenueSettings.identity.guestTwoStep.enabled` is on and only for a guest who enrolled a method (the venue is the one the site or booking is in). `createMfaChallenge` (`action: signIn`) sends the code (authenticator, email code as fallback); the session is usable after `verifyMfaChallenge`. At a venue with it off, the default, nothing is asked.",
       "operation": "verifyMfaChallenge",
       "provenance": "decided 29 September, rev 3 GAP-B1 (per venue)"
      }
     ]
    },
    {
     "name": "session",
     "slot": "context",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Who is signed in on this device",
       "bindsTo": "GuestSession",
       "columns": [
        "GuestSession.subjectId",
        "GuestSession.displayName",
        "GuestSession.isVerified",
        "GuestSession.identityProviders",
        "GuestSession.preferredLanguage",
        "GuestSession.expiresAt"
       ],
       "operation": "getGuestSession",
       "notes": "Shown only when a guest session already exists on this device, with a way to sign out so a shared device is handed over clean.",
       "provenance": "contract identity.yaml GET /auth/guest/session"
      },
      {
       "kind": "secondaryButton",
       "label": "Sign out",
       "operation": "guestLogout",
       "provenance": "contract identity.yaml DELETE /auth/guest/session"
      },
      {
       "kind": "secondaryButton",
       "label": "Link an order I placed as a guest",
       "operation": "linkGuestCheckout",
       "provenance": "contract identity.yaml POST /auth/guest/link-checkout"
      },
      {
       "kind": "secondaryButton",
       "label": "Keep my cart",
       "operation": "claimCart",
       "notes": "Called after sign-in when the guest arrived from the cart, so the anonymous cart becomes theirs.",
       "provenance": "contract orders.yaml POST /carts/{cartId}/claim"
      },
      {
       "kind": "secondaryButton",
       "label": "Refresh token",
       "operation": "refreshToken",
       "notes": "Not a button the guest sees; the client rotates the access token before it expires.",
       "provenance": "contract identity.yaml POST /auth/refresh"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formRegisterGuest",
    "component": "modal",
    "trigger": "Create an account",
    "body": "**Collects what `registerGuest` sends before it is called.** Required: `identifier`, `channel`. Optional: `displayName`, `password`, `preferredLanguage`, `consents`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RegisterGuestRequest",
    "confirm": {
     "label": "Register guest",
     "operation": "registerGuest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "identifier",
      "channel",
      "displayName",
      "password",
      "preferredLanguage",
      "consents"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formGuestPasswordLogin",
    "component": "modal",
    "trigger": "Sign in with password",
    "body": "**Collects what `guestPasswordLogin` sends before it is called.** Required: `identifier`, `password`. Optional: `deviceId` (sent by the client, not typed). A 401 is one message whatever the cause; a 429 or a locked account says to try again later or use a one-time code instead (decided 28 September, audit R073 (a)). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sign in",
     "operation": "guestPasswordLogin"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "identifier",
      "password",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formGuestSocialLogin",
    "component": "modal",
    "trigger": "Continue with Apple or Google",
    "body": "**Collects what `guestSocialLogin` sends before it is called.** Required: `provider`, `idToken`. Optional: `deviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Guest social login",
     "operation": "guestSocialLogin"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "provider",
      "idToken",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formGuestUaePassLogin",
    "component": "modal",
    "trigger": "Continue with UAE Pass",
    "body": "**Collects what `guestUaePassLogin` sends before it is called.** Required: `code`, `redirectUri`. Optional: `state`, `deviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Guest uae pass login",
     "operation": "guestUaePassLogin"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "redirectUri",
      "state",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formLinkGuestCheckout",
    "component": "modal",
    "trigger": "Link an order I placed as a guest",
    "body": "**Collects what `linkGuestCheckout` sends before it is called.** Required: `orderReference`. Optional: `verificationCode`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Link guest checkout",
     "operation": "linkGuestCheckout"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "orderReference",
      "verificationCode"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRefreshToken",
    "component": "modal",
    "trigger": "Refresh token",
    "body": "**Collects what `refreshToken` sends before it is called.** Required: `refreshToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Refresh token",
     "operation": "refreshToken"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "refreshToken"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRequestGuestOtp",
    "component": "modal",
    "trigger": "Send me a code",
    "body": "**Collects what `requestGuestOtp` sends before it is called.** Required: `identifier`, `channel`. Optional: `purpose`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request guest OTP",
     "operation": "requestGuestOtp"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "identifier",
      "channel",
      "purpose"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formVerifyGuestOtp",
    "component": "modal",
    "trigger": "Sign in with the code",
    "body": "**Collects what `verifyGuestOtp` sends before it is called.** Required: `identifier`, `code`. Optional: `deviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Verify guest OTP",
     "operation": "verifyGuestOtp"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "identifier",
      "code",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "Checking whether this device already holds a guest session. The sign-in form stays visible.",
   "error": "Identity could not be reached. **Says so rather than saying the password or code is wrong**, and keeps what was typed.",
   "emptyFirstRun": "**Nobody signed in on this device** — the normal state. The form offers a code, a password, Apple or Google and UAE Pass, and Create an account (`registerGuest`).",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025), and this is the screen a guest who is not signed in is sent to, so it has no no-access case of its own. A session that has expired lands here with the screen it came from kept, and returns to it after sign-in.",
   "signInRefused": "**One message for every refusal of a password sign-in**: `guestPasswordLogin` answers 401 alike for a wrong password, an unknown identifier, an account with no password and a locked account, and the screen never says which. Too many attempts (429, or the lockout after `PasswordPolicy.lockoutAfterAttempts`) says to try again later and offers **Send me a code** instead (decided 28 September, audit R073 (a)).",
   "offline": "**Not available, and the offline banner says why.** Signing in, registering and verifying a code need the server."
  },
  "apis": [
   {
    "operationId": "registerGuest",
    "contract": "identity",
    "purpose": "Create a guest account",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
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
     "getGuestSession"
    ]
   },
   {
    "operationId": "guestPasswordLogin",
    "contract": "identity",
    "purpose": "Sign in with the email or mobile and the password set at registration (identifier, password, deviceId -> GuestSession); one indistinguishable 401, lockout, 429 (decided 28 September, audit R073 (a))",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "guestSocialLogin",
    "contract": "identity",
    "purpose": "Sign in with Apple or Google",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "guestUaePassLogin",
    "contract": "identity",
    "purpose": "Sign in with a national identity provider",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "linkGuestCheckout",
    "contract": "identity",
    "purpose": "Attach a guest checkout to an account",
    "trigger": "onAction"
   },
   {
    "operationId": "refreshToken",
    "contract": "identity",
    "purpose": "Rotate the access token",
    "trigger": "onAction"
   },
   {
    "operationId": "requestGuestOtp",
    "contract": "identity",
    "purpose": "Request a one-time code",
    "trigger": "onAction"
   },
   {
    "operationId": "verifyGuestOtp",
    "contract": "identity",
    "purpose": "Verify a one-time code and issue a session",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "claimCart",
    "contract": "orders",
    "purpose": "Attach an anonymous cart to a guest",
    "trigger": "onAction"
   },
   {
    "operationId": "createMfaChallenge",
    "contract": "identity",
    "purpose": "Ask for the second factor (`action: signIn`) when the session comes back `requiresMfa` at a venue with guest two-step verification on",
    "trigger": "onAction"
   },
   {
    "operationId": "verifyMfaChallenge",
    "contract": "identity",
    "purpose": "Check the second-factor code and release the session",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "claimDeviceConsent",
    "contract": "marketing-crm",
    "purpose": "Attach this browser's cookie decision to the guest after sign-in or registration",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
     "from": "navigation"
    },
    {
     "name": "subjectId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Needs nothing.** A guest arriving cold signs in and goes to My Account; one sent from the cart carries `cartId` and goes back to it. The SSO deep-link parameter (`providerId`) went with the operations that used it (audit R167); a second-factor challenge is created in place, never arrives by link."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-016",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Header profile icon (signed out), or automatically when leaving Add-ons / at payment",
    "differences": "No password sign-in and no mobile-number OTP (YAML has guestPasswordLogin and 'Email or mobile number'); it is a modal, not a page. Account → Security still shows 'Two-step verification' and passkeys, which the YAML ruled out for guests (R167). Guest checkout route belongs to WEB-012 in the prototype."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 19 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
      "challengeId",
      "subjectId"
     ],
     "provenance": "derived — WEB-016 declares entryState.params challengeId, subjectId and WEB-017 holds challengeId, subjectId, so an edge into it carries them"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId and WEB-017 holds none of them, so the edge carries nothing and WEB-018 opens cold"
    },
    {
     "to": "WEB-019",
     "trigger": "Order History",
     "provenance": "derived — WEB-019 declares entryState.params documentId, invoiceId, orderId and WEB-017 holds none of them, so the edge carries nothing and WEB-019 opens cold"
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
       "label": "Every guest device",
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
       "label": "The selected guest device",
       "bindsTo": "GuestDevice",
       "columns": [
        "GuestDevice.id",
        "GuestDevice.subjectId",
        "GuestDevice.platform",
        "GuestDevice.tokenFingerprint",
        "GuestDevice.tokenRef",
        "GuestDevice.appVersion",
        "GuestDevice.osVersion",
        "GuestDevice.deviceModel",
        "GuestDevice.locale",
        "GuestDevice.status",
        "GuestDevice.failureCount",
        "GuestDevice.registeredAt",
        "GuestDevice.lastSeenAt",
        "GuestDevice.revokedAt"
       ],
       "operation": "listGuestDevices",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/devices"
      },
      {
       "kind": "detailPanel",
       "label": "The challenge",
       "bindsTo": "Challenge",
       "columns": [
        "Challenge.id",
        "Challenge.name",
        "Challenge.kind",
        "Challenge.scope",
        "Challenge.goal",
        "Challenge.eventId",
        "Challenge.rewardKind",
        "Challenge.rewardValue",
        "Challenge.rewardAmount",
        "Challenge.badgeAssetId",
        "Challenge.startsAt",
        "Challenge.endsAt",
        "Challenge.status",
        "Challenge.scopePath"
       ],
       "operation": "getMyChallenges",
       "provenance": "contract marketing-crm.yaml GET /guests/me/challenges"
      },
      {
       "kind": "detailPanel",
       "label": "The wishlist",
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
       "label": "Add to wishlist",
       "operation": "addToWishlist",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/wishlist"
      },
      {
       "kind": "secondaryButton",
       "label": "Record consent",
       "operation": "recordConsent",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "secondaryButton",
       "label": "Register guest device",
       "operation": "registerGuestDevice",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/devices"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove from wishlist",
       "operation": "removeFromWishlist",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/wishlist/{itemId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke guest device",
       "operation": "revokeGuestDevice",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/devices/{deviceId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Respond to invitation",
       "operation": "respondToInvitation",
       "provenance": "contract marketing-crm.yaml POST /invitations/{token}/respond"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveFromWishlist",
    "component": "confirmDialog",
    "trigger": "Remove from wishlist",
    "body": "**Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A account this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "confirmRevokeGuestDevice",
    "component": "confirmDialog",
    "trigger": "Revoke guest device",
    "body": "**Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A account this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formRespondToInvitation",
    "component": "modal",
    "trigger": "Respond to invitation",
    "body": "**Collects what `respondToInvitation` sends before it is called.** Required: `response`. Optional: `plusOnes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Respond to invitation",
     "operation": "respondToInvitation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "response",
      "plusOnes"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formAddToWishlist",
    "component": "modal",
    "trigger": "Add to wishlist",
    "body": "**Collects what `addToWishlist` sends before it is called.** Required: `variantId`. Optional: `performanceId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add to wishlist",
     "operation": "addToWishlist"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "variantId",
      "performanceId",
      "note"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRecordConsent",
    "component": "modal",
    "trigger": "Record consent",
    "body": "**Collects what `recordConsent` sends before it is called.** Required: `purpose`, `decision`, `noticeVersion`, `source`, `recordedAt`. Optional: `channels`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RecordConsentRequest",
    "confirm": {
     "label": "Record consent",
     "operation": "recordConsent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "purpose",
      "decision",
      "noticeVersion",
      "source",
      "recordedAt",
      "channels"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRegisterGuestDevice",
    "component": "modal",
    "trigger": "Register guest device",
    "body": "**Collects what `registerGuestDevice` sends before it is called.** Required: `platform`, `token`. Optional: `appVersion`, `osVersion`, `deviceModel`, `locale`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Register guest device",
     "operation": "registerGuestDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "platform",
      "token",
      "appVersion",
      "osVersion",
      "deviceModel",
      "locale"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "Tiles skeleton",
   "error": "Partial. Each tile fails independently",
   "emptyFirstRun": "A new account with no orders — offers what to do next",
   "emptyNoResults": "Never shown: `listGuestDevices` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
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
    "GuestDevice.id",
    "GuestDevice.subjectId",
    "GuestDevice.platform",
    "GuestDevice.tokenFingerprint",
    "GuestDevice.tokenRef"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-017",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Sign in → avatar menu → 'Account overview'",
    "differences": "Prototype makes the account a single page with section panes; most YAML account screens (019–024, 026, 027, 030, 031, 034) are panes of it. Groups & invitations (respondToInvitation, getMyChallenges, referral code) sits here. Signed-out state 'Sign in to see your account' is drawn."
   },
   "derivedFrom": "wireframes/reference/Dashboards Board.dc.html",
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
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
     "provenance": "derived — WEB-016 declares entryState.params challengeId, subjectId and WEB-018 holds none of them, so the edge carries nothing and WEB-016 opens cold"
    },
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, token and WEB-018 holds none of them, so the edge carries nothing and WEB-017 opens cold"
    },
    {
     "to": "WEB-019",
     "trigger": "Order History",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-019 declares entryState.params documentId, invoiceId, orderId and WEB-018 holds orderId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Dynamic QR with a visible countdown: a rotating code derived in the page from the `rotation` seed that `getEntitlementCredential` returns, with the seconds to the next step shown (audit R230). **No screenshot blocking on the web** — a browser cannot enforce it, so the page promises none (decided 28 September, audit R077 (c)). Purpose derived from the screen name and its operations on 17 August, not from a requirement. The read surface Deep asked for. **All four were missing and the table itself did not exist until 18 August.** **Rewired on the 20 August review.** **`listEntitlements` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Cross-surface parity, 31 August**: added transferOrderTickets. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMyEntitlements` reads the population and `getEntitlement` reads one of them — list, select, act",
  "purpose": "Find my tickets for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementCredential",
    "why": "**`getEntitlementCredential` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract access.yaml GET /entitlements/{entitlementId}/credential"
   },
   {
    "operation": "getEntitlementHistory",
    "why": "**`getEntitlementHistory` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract access.yaml GET /entitlements/{entitlementId}/history"
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
       "kind": "selectField",
       "label": "State",
       "operation": "listMyEntitlements",
       "notes": "Sends `?state=` to `listMyEntitlements`.",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "toggle",
       "label": "Include shared",
       "operation": "listMyEntitlements",
       "notes": "Sends `?includeShared=` to `listMyEntitlements`.",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "dataTable",
       "label": "Every entitlement",
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
      },
      {
       "kind": "dataTable",
       "label": "Entitlement history",
       "operation": "getEntitlementHistory",
       "notes": "Shows `at`, `kind`, `accessPointName`, `denyReason`, `byPrincipalName` from `getEntitlementHistory`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}/history"
      },
      {
       "kind": "dataTable",
       "label": "Every entitlement",
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
       "operation": "listEntitlements",
       "provenance": "contract access.yaml GET /my/entitlements/all"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected entitlement",
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
      },
      {
       "kind": "detailPanel",
       "label": "Entitlement credential",
       "operation": "getEntitlementCredential",
       "notes": "Shows `mediaCode`, `payload`, `expiresAt` from `getEntitlementCredential`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one. **A rotating code derived on the device** (decided 28 September, audit R230): while online the screen fetches `rotation` (secret, `timeStepSeconds`, `digits`, `algorithm`, valid `validFrom` to `validTo`) and computes the current code from the seed and the clock, with a visible countdown to the next step; it keeps rotating with no signal. A null `rotation` (wristband, wallet pass) shows the static code. **No screenshot blocking on the web** — a browser cannot enforce it and the page promises none (audit R077 (c)).",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}/credential"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Issue wallet pass",
       "operation": "issueWalletPass",
       "provenance": "contract orders.yaml POST /wallet-passes"
      },
      {
       "kind": "secondaryButton",
       "label": "Share entitlement",
       "operation": "shareEntitlement",
       "provenance": "contract orders.yaml POST /entitlements/{entitlementId}/share"
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
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Tickets already loaded stay visible with their age, and a ticket's rotating code is derived on the device from its seed, so it changes with no signal (decided 28 September, audit R230). Sharing, transferring and adding to a phone wallet need the connection."
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
    "purpose": "The thing that gets scanned — with the `rotation` seed the device derives the rotating code from (audit R230)",
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
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-018",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Header 'My tickets' → a ticket → 'Manage' (ticket sheet)",
    "differences": "QR is static — no rotating code with a visible countdown (YAML R230). Prototype adds reschedule, add guests, refund, resale and cancel on the ticket sheet (YAML routes refunds to WEB-019 and transfers to WEB-030)."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formIssueWalletPass",
    "component": "modal",
    "trigger": "Issue wallet pass",
    "body": "**Collects what `issueWalletPass` sends before it is called.** Required: `entitlementId`, `platform`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Issue wallet pass",
     "operation": "issueWalletPass"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "entitlementId",
      "platform"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formShareEntitlement",
    "component": "modal",
    "trigger": "Share entitlement",
    "body": "**Collects what `shareEntitlement` sends before it is called.** Required: `toSubjectId`. Optional: `validUntil`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Share entitlement",
     "operation": "shareEntitlement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "toSubjectId",
      "validUntil"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formTransferOrderTickets",
    "component": "modal",
    "trigger": "Transfer order tickets",
    "body": "**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer order tickets",
     "operation": "transferOrderTickets"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ticketIds",
      "recipient",
      "message"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
      "subjectId"
     ],
     "provenance": "derived — WEB-016 declares entryState.params challengeId, subjectId and WEB-019 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, token and WEB-019 holds none of them, so the edge carries nothing and WEB-017 opens cold"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId and WEB-019 holds orderId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`listMyOrders` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Cross-surface parity, 31 August**: added getOrder, listOrders. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMyOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Find order history for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "datePicker",
       "label": "Since",
       "operation": "listMyOrders",
       "notes": "Sends `?since=` to `listMyOrders`.",
       "provenance": "contract orders.yaml GET /my/orders"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
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
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order",
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
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Create refund request",
       "operation": "createRefundRequest",
       "provenance": "contract orders.yaml POST /refund-requests"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order history list.",
   "error": "Could not load. Names which read failed and leaves the order history untouched.",
   "emptyFirstRun": "No order history yet. Offers Create refund request (`createRefundRequest`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on since and the order history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
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
    "trigger": "onAction"
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
   },
   {
    "operationId": "listTaxInvoices",
    "contract": "finance",
    "purpose": "List tax invoices",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "issueTaxInvoice",
    "contract": "finance",
    "purpose": "Issue a tax invoice",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getTaxInvoice",
    "contract": "finance",
    "purpose": "Show a tax invoice",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listCreditMemos",
    "contract": "finance",
    "purpose": "List credit memos",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getTaxDocumentRendition",
    "contract": "finance",
    "purpose": "Download the invoice / credit memo PDF",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "documentId",
     "from": "navigation"
    },
    {
     "name": "invoiceId",
     "from": "navigation"
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
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-019",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → 'Order history'",
    "differences": "A list pane with toast-only actions; no order detail view. Refund request and transfer are rows, not flows."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateRefundRequest",
    "component": "modal",
    "trigger": "Create refund request",
    "body": "**Collects what `createRefundRequest` sends before it is called.** Required: `orderId`, `reason`. Optional: `lineIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create refund request",
     "operation": "createRefundRequest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "orderId",
      "reason",
      "lineIds"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formTransferOrderTickets",
    "component": "modal",
    "trigger": "Transfer order tickets",
    "body": "**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer order tickets",
     "operation": "transferOrderTickets"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ticketIds",
      "recipient",
      "message"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
      "subjectId"
     ],
     "provenance": "derived — WEB-016 declares entryState.params challengeId, subjectId and WEB-020 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "WEB-017",
     "trigger": "My Account Dashboard",
     "provenance": "derived — WEB-017 declares entryState.params deviceId, itemId, token and WEB-020 holds none of them, so the edge carries nothing and WEB-017 opens cold"
    },
    {
     "to": "WEB-018",
     "trigger": "My Tickets",
     "provenance": "derived — WEB-018 declares entryState.params entitlementId, orderId and WEB-020 holds none of them, so the edge carries nothing and WEB-018 opens cold"
    }
   ]
  },
  "notes": "Consent withdrawal must be as easy as granting it. Same screen, same number of clicks. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Profile and Preferences. **Wishlist and device operations removed; profile, consent and email verification added.** Deep listed exactly these. **Rewired on the 20 August review.**\n\n**29 September (W1).** *Complete your details* for a profile created by guest checkout.",
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
       "label": "Every consent purpose config",
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
      },
      {
       "kind": "banner",
       "label": "Complete your details",
       "operation": "updateMyProfile",
       "notes": "For a profile created by guest checkout (W1): asks for what the pop-up did not; never blocks.",
       "provenance": "decided 29 September 2026 (P29), W1"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected consent purpose config",
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
      },
      {
       "kind": "detailPanel",
       "label": "The guest profile",
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
        "GuestProfileDetail.mergedIntoSubjectId"
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
       "label": "Save my profile",
       "operation": "updateMyProfile",
       "provenance": "contract marketing-crm.yaml PATCH /guests/me/profile"
      },
      {
       "kind": "secondaryButton",
       "label": "Record consent",
       "operation": "recordConsent",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify guest email",
       "operation": "verifyGuestEmail",
       "provenance": "contract identity.yaml POST /auth/guest/verify-email"
      },
      {
       "kind": "secondaryButton",
       "label": "Save guest preferences",
       "operation": "updateGuestPreferences",
       "provenance": "contract marketing-crm.yaml PUT /guests/{subjectId}/preferences"
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
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
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
   },
   {
    "operationId": "getMyIdentityVerification",
    "contract": "identity",
    "purpose": "Show the guest's ID verification status",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "submitGuestIdentityDocument",
    "contract": "identity",
    "purpose": "Upload an ID document for verification",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
    "ConsentPurposeConfig.purpose",
    "ConsentPurposeConfig.displayName",
    "ConsentPurposeConfig.description",
    "ConsentPurposeConfig.channels",
    "ConsentPurposeConfig.noticeVersion"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-020",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → 'Personal details', 'Notifications', 'Accessibility'",
    "differences": "Split over three panes; fields are read-only with a 'Save changes' toast. No 'which level the current value came from' (YAML purpose). Consent purposes appear as two marketing toggles rather than the configured purpose list."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formUpdateGuestPreferences",
    "component": "modal",
    "trigger": "Save guest preferences",
    "body": "**Collects what `updateGuestPreferences` sends before it is called.** Nothing in the body is required. Optional: `id`, `subjectId`, `seatingPreference`, `drinkPreferences`, `dietary`, `accessibility`, `preferredChannel`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "GuestPreferences",
    "confirm": {
     "label": "Save guest preferences",
     "operation": "updateGuestPreferences"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subjectId",
      "seatingPreference",
      "drinkPreferences",
      "dietary",
      "accessibility",
      "preferredChannel"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formUpdateMyProfile",
    "component": "modal",
    "trigger": "Save my profile",
    "body": "**Collects what `updateMyProfile` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `email`, `phone`, `preferredLanguage`, `preferredChannel`, `dietary`, `accessibility`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save my profile",
     "operation": "updateMyProfile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "displayName",
      "email",
      "phone",
      "preferredLanguage",
      "preferredChannel",
      "dietary",
      "accessibility"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRecordConsent",
    "component": "modal",
    "trigger": "Record consent",
    "body": "**Collects what `recordConsent` sends before it is called.** Required: `purpose`, `decision`, `noticeVersion`, `source`, `recordedAt`. Optional: `channels`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RecordConsentRequest",
    "confirm": {
     "label": "Record consent",
     "operation": "recordConsent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "purpose",
      "decision",
      "noticeVersion",
      "source",
      "recordedAt",
      "channels"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formVerifyGuestEmail",
    "component": "modal",
    "trigger": "Verify guest email",
    "body": "**Collects what `verifyGuestEmail` sends before it is called.** Required: `mode`. Optional: `token`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Verify guest email",
     "operation": "verifyGuestEmail"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "mode",
      "token"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 "claimDeviceConsent": {
  "method": "POST",
  "path": "/guests/{subjectId}/consents/claim-device",
  "contract": "marketing-crm",
  "summary": "Attach a browser's cookie decision to the guest who turned out to own it",
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
  "requestBody": "ClaimDeviceConsentRequest",
  "responds": "ConsentState"
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
  "responds": null
 },
 "getMyIdentityVerification": {
  "method": "GET",
  "path": "/auth/guest/identity-verifications/current",
  "contract": "identity",
  "summary": "The guest's own latest identity verification",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "IdentityGuestVerification"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Order"
 },
 "getTaxDocumentRendition": {
  "method": "GET",
  "path": "/tax-documents/{documentId}/rendition",
  "contract": "finance",
  "summary": "The PDF of a tax invoice or credit memo, in a language",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "language",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FinTaxDocumentRendition"
 },
 "getTaxInvoice": {
  "method": "GET",
  "path": "/tax-invoices/{invoiceId}",
  "contract": "finance",
  "summary": "One tax invoice, with its lines, VAT per rate and credit memos",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "FinTaxInvoice"
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
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "allDevices",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "guestPasswordLogin": {
  "method": "POST",
  "path": "/auth/guest/password",
  "contract": "identity",
  "summary": "Sign in with an email or mobile and a password",
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
 "issueTaxInvoice": {
  "method": "POST",
  "path": "/tax-invoices",
  "contract": "finance",
  "summary": "Issue a tax invoice for one or more paid orders",
  "permission": "LEDGER_POST",
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
  "requestBody": "FinIssueTaxInvoiceRequest",
  "responds": "FinTaxInvoice"
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
  "responds": "Page"
 },
 "listCreditMemos": {
  "method": "GET",
  "path": "/credit-memos",
  "contract": "finance",
  "summary": "Credit memos issued, newest first",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "taxInvoiceId",
    "in": "query",
    "required": null
   },
   {
    "name": "refundId",
    "in": "query",
    "required": null
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedTo",
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
    "name": null,
    "in": null,
    "required": null
   },
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
  "responds": "Page"
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
  "responds": "Page"
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
    "name": null,
    "in": null,
    "required": null
   },
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
  "responds": "Page"
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
    "name": null,
    "in": null,
    "required": null
   },
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
  "responds": "Page"
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
 "listTaxInvoices": {
  "method": "GET",
  "path": "/tax-invoices",
  "contract": "finance",
  "summary": "Tax invoices issued, newest first",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "orderId",
    "in": "query",
    "required": null
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "invoiceType",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedTo",
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
  "responds": "EntitlementShare"
 },
 "submitGuestIdentityDocument": {
  "method": "POST",
  "path": "/auth/guest/identity-verifications",
  "contract": "identity",
  "summary": "Submit an identity document for verification",
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
  "requestBody": "IdentityGuestDocumentSubmission",
  "responds": "IdentityGuestVerification"
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
  "requestBody": "GuestPreferences",
  "responds": "GuestPreferences"
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
   "consentQuestions": {
    "type": "array",
    "readOnly": true,
    "description": "**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n",
    "items": {
     "allOf": [
      {
       "$ref": "../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"
      },
      {
       "type": "object",
       "properties": {
        "lineIds": {
         "type": "array",
         "description": "The cart lines that ask it. Empty for a question the flow asks.",
         "items": {
          "type": "string",
          "format": "uuid"
         }
        },
        "answered": {
         "type": "boolean",
         "description": "Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."
        }
       }
      }
     ]
    }
   },
   "subtotal": {
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
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
   "couponCodes": {
    "type": "array",
    "readOnly": true,
    "description": "The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n",
    "items": {
     "type": "string",
     "maxLength": 100
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
 "Challenge": {
  "type": "object",
  "x-ticvai-persistence": "marketing.challenge",
  "description": "BL-022, CF-137. **Section 22.6 is twenty requirements and 19.2.73–75 three more** — checked against the matrix on 18 August rather than assumed. It is asked for explicitly.\n**Gamification is not loyalty.** Loyalty pays for spend; a challenge pays for behaviour the venue wants and spend does not produce — a second visit, a quiet Tuesday, a ride nobody rides. **A challenge that only rewards spending is a loyalty programme with worse arithmetic.**\n",
  "required": [
   "id",
   "name",
   "kind",
   "goal",
   "status"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "description": "What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)): `scan` counts scans of a named code or point (a trail marker, a stand), `activity` counts completions of a named attraction or activity that is not a ride, and `purchase` counts purchases of named products or categories. **`purchase` is not `spend`**: `spend` counts money, whatever was bought; `purchase` counts items bought.\n",
    "enum": [
     "visit",
     "spend",
     "ride",
     "collection",
     "streak",
     "referral",
     "survey",
     "social",
     "milestone",
     "scan",
     "activity",
     "purchase"
    ]
   },
   "scope": {
    "type": "string",
    "enum": [
     "individual",
     "family",
     "group",
     "team"
    ],
    "default": "individual",
    "description": "22.6.7 and 22.6.8. **A family challenge is not a per-person challenge counted twice** — members contribute toward one shared goal, and a school competing against another school is a group scoring against a group.\n**This is the field that needs the portfolio work** (CF-132): a family challenge without a family is an individual challenge with a label.\n"
   },
   "goal": {
    "type": "object",
    "description": "What completes it.",
    "properties": {
     "metric": {
      "type": "string"
     },
     "target": {
      "type": "number"
     },
     "withinDays": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "rewardKind": {
    "type": "string",
    "enum": [
     "badge",
     "loyaltyPoints",
     "walletCredit",
     "voucher",
     "entitlement",
     "none"
    ],
    "description": "22.6.13. **A reward that issues wallet credit is money**, and it goes through the same stored-value mechanism as everything else rather than a parallel one.\n"
   },
   "rewardValue": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "description": "**Points, for `rewardKind: loyaltyPoints` only.** A count, not an amount — a money reward is `rewardAmount`, never this.\n"
   },
   "rewardAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "**The credit, for `rewardKind: walletCredit` only.** The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the region, because a wallet credit is money and naming-and-style 5.1 forbids money as a bare number.\n"
   },
   "badgeAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "readOnly": true,
    "type": "string",
    "enum": [
     "draft",
     "active",
     "paused",
     "ended",
     "archived"
    ]
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 "ClaimDeviceConsentRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "consentKey"
  ],
  "properties": {
   "consentKey": {
    "type": "string",
    "maxLength": 64
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
  "x-ticvai-persistence": "marketing.consent_purpose + marketing.consent_purpose_channel",
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
   "agentRecorded",
   "cookieBanner",
   "checkout"
  ],
  "description": "`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."
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
    "description": "A ULID, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The order's id, a ULID as in `/orders/{orderId}` (`orders.sales_order.id`)."
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
    "description": "**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"
   },
   "entriesUsed": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true
   },
   "lastEntryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"
   },
   "frozenDays": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"
   },
   "suspendedReason": {
    "type": "string",
    "nullable": true
   },
   "freezeReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "travelling",
     "injury",
     "personal",
     "seasonal",
     "other"
    ],
    "description": "The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."
   },
   "freezeNote": {
    "type": "string",
    "nullable": true,
    "maxLength": 500,
    "description": "The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"
   },
   "walletValueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"
   },
   "facePassEnrolmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"
   }
  }
 },
 "EntitlementShare": {
  "type": "object",
  "x-ticvai-persistence": "none — a view of the identity.delegated_access row shareEntitlement writes",
  "description": "**A second person's right to present an entitlement the owner still holds.** Returned by `shareEntitlement` and `revokeEntitlementShare`; its `id` is the delegated-access row the share is.\n",
  "required": [
   "id",
   "entitlementId",
   "toSubjectId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "entitlementId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "toSubjectId": {
    "type": "string",
    "format": "uuid",
    "description": "The guest it is shared with. They may present it; they may not share or transfer it on."
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null means until revoked or until the entitlement itself ends."
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "revoked",
     "expired"
    ]
   }
  }
 },
 "FinCreditMemo": {
  "x-ticvai-persistence": "ledger.credit_memo + ledger.credit_memo_line",
  "type": "object",
  "description": "5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.",
  "required": [
   "id",
   "creditMemoNumber",
   "taxInvoiceId",
   "kind",
   "reason",
   "legalEntityId",
   "issuedAt",
   "currency",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "creditMemoNumber": {
    "type": "string",
    "readOnly": true,
    "description": "Server-assigned from the legal entity's credit memo series, in sequence without gaps."
   },
   "taxInvoiceId": {
    "type": "string",
    "format": "uuid"
   },
   "taxInvoiceNumber": {
    "type": "string",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "full",
     "partial"
    ]
   },
   "reason": {
    "type": "string",
    "enum": [
     "refund",
     "cancellation",
     "priceAdjustment",
     "returnOfGoods",
     "billingError",
     "other"
    ]
   },
   "refundId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "cancelledOrderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "buyerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmountInLegalCurrency": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "renditionAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "eInvoiceStatus": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FinCreditMemoLine"
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "FinCreditMemoLine": {
  "type": "object",
  "required": [
   "invoiceLineNumber",
   "netAmount",
   "taxAmount",
   "grossAmount"
  ],
  "properties": {
   "invoiceLineNumber": {
    "type": "integer",
    "minimum": 1
   },
   "description": {
    "type": "string",
    "maxLength": 500
   },
   "quantity": {
    "type": "number",
    "nullable": true
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxRate": {
    "type": "number"
   },
   "taxCategory": {
    "$ref": "#/components/schemas/FinTaxCategory"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FinEInvoiceTransmissionStatus": {
  "type": "string",
  "description": "6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.",
  "enum": [
   "notRequired",
   "queued",
   "sent",
   "accepted",
   "rejected",
   "failed"
  ]
 },
 "FinIssueTaxInvoiceRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "invoiceType",
   "orderIds"
  ],
  "properties": {
   "invoiceType": {
    "$ref": "#/components/schemas/FinTaxInvoiceType"
   },
   "orderIds": {
    "type": "array",
    "minItems": 1,
    "description": "One order for `simplified` and `full`; one or more for `consolidated`. Every order must be paid, of one buyer, one legal entity and one currency.",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "recipient": {
    "$ref": "#/components/schemas/FinTaxInvoiceRecipient"
   },
   "languages": {
    "type": "array",
    "description": "Overrides the template's languages for this document, within those the template offers.",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}(-[A-Z]{2})?$"
    }
   },
   "supersedesInvoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A simplified invoice this full invoice replaces for the same supply. Refused unless the law allows it (make-or-break on issueTaxInvoice)."
   },
   "deliverToEmail": {
    "type": "string",
    "format": "email",
    "nullable": true,
    "description": "Sends the PDF on issue as well as returning it."
   }
  }
 },
 "FinTaxCategory": {
  "type": "string",
  "description": "How a line is treated for VAT. Taken from the tax code the line was posted with.",
  "enum": [
   "standardRated",
   "zeroRated",
   "exempt",
   "outOfScope",
   "reverseCharge"
  ]
 },
 "FinTaxDocumentRendition": {
  "x-ticvai-persistence": "none — a signed link to the stored PDF",
  "type": "object",
  "required": [
   "documentId",
   "documentKind",
   "url",
   "expiresAt"
  ],
  "properties": {
   "documentId": {
    "type": "string",
    "format": "uuid"
   },
   "documentKind": {
    "type": "string",
    "enum": [
     "taxInvoice",
     "creditMemo"
    ]
   },
   "documentNumber": {
    "type": "string"
   },
   "language": {
    "type": "string",
    "nullable": true
   },
   "contentType": {
    "type": "string",
    "default": "application/pdf"
   },
   "url": {
    "type": "string",
    "format": "uri"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "FinTaxInvoice": {
  "x-ticvai-persistence": "ledger.tax_invoice + ledger.tax_invoice_line",
  "type": "object",
  "description": "5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.",
  "required": [
   "id",
   "invoiceNumber",
   "invoiceType",
   "status",
   "legalEntityId",
   "issuedAt",
   "supplyDate",
   "currency",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "invoiceNumber": {
    "type": "string",
    "readOnly": true,
    "description": "Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."
   },
   "invoiceType": {
    "$ref": "#/components/schemas/FinTaxInvoiceType"
   },
   "status": {
    "$ref": "#/components/schemas/FinTaxInvoiceStatus"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "supplierName": {
    "type": "string"
   },
   "supplierAddress": {
    "type": "string",
    "nullable": true
   },
   "supplierTaxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "buyerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest the orders belong to; the key a guest's own reads filter on."
   },
   "buyerName": {
    "type": "string",
    "nullable": true
   },
   "buyerAddress": {
    "type": "string",
    "nullable": true
   },
   "buyerCountryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "buyerTaxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "customerAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "supplyDate": {
    "type": "string",
    "format": "date",
    "description": "The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmountInLegalCurrency": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs, at the rate the orders were stored at."
   },
   "creditedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "supersedesInvoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "renditionAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The PDF rendered at issue; read through getTaxDocumentRendition."
   },
   "eInvoiceStatus": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Null where the platform issued it."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FinTaxInvoiceLine"
    }
   },
   "taxSummary": {
    "type": "array",
    "x-ticvai-persisted": false,
    "description": "VAT per rate and category, summed from the lines for the response.",
    "items": {
     "type": "object",
     "properties": {
      "taxCategory": {
       "$ref": "#/components/schemas/FinTaxCategory"
      },
      "taxRate": {
       "type": "number"
      },
      "taxableAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "taxAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."
   }
  }
 },
 "FinTaxInvoiceLine": {
  "type": "object",
  "description": "One line as it was sold and taxed. Amounts are in the invoice currency.",
  "required": [
   "lineNumber",
   "description",
   "quantity",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "taxCategory"
  ],
  "properties": {
   "lineNumber": {
    "type": "integer",
    "minimum": 1
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderLineId": {
    "type": "string",
    "nullable": true
   },
   "description": {
    "type": "string",
    "maxLength": 500
   },
   "quantity": {
    "type": "number"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxCodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "taxRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "taxCategory": {
    "$ref": "#/components/schemas/FinTaxCategory"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "creditedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FinTaxInvoiceRecipient": {
  "x-ticvai-persistence": "none — copied onto the invoice as buyer columns",
  "type": "object",
  "description": "Who the invoice is addressed to. Required for `full` and `consolidated`.",
  "required": [
   "name"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 300
   },
   "address": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "taxRegistrationNumber": {
    "type": "string",
    "maxLength": 30,
    "nullable": true,
    "description": "The recipient's TRN where they are VAT-registered."
   },
   "customerAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The B2B credit account (payments `B2bCreditAccount`) where a company is invoiced."
   }
  }
 },
 "FinTaxInvoiceStatus": {
  "type": "string",
  "description": "`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).",
  "enum": [
   "issued",
   "partiallyCredited",
   "fullyCredited",
   "superseded"
  ]
 },
 "FinTaxInvoiceType": {
  "type": "string",
  "description": "5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.",
  "enum": [
   "simplified",
   "full",
   "consolidated"
  ]
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
   "tokenRef": {
    "type": "string",
    "writeOnly": true,
    "description": "**A vault reference to the push token**, written by the server from `registerGuestDevice.token` — the same pattern as `PaymentProvider.credentialRef`. Never the token and never returned; the sender resolves it at send time. Without it a registered device could not be sent to.\n"
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
 "GuestPreferences": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_preference",
  "description": "**What the guest likes, kept apart from what they permit** (consent) and from who they are (the profile). One row per subject. `dietary` and `accessibility` are here rather than as tags because BL-134 gives them their own consent purpose and retention.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "seatingPreference": {
    "type": "string",
    "nullable": true,
    "maxLength": 200
   },
   "drinkPreferences": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "dietary": {
    "type": "array",
    "description": "Also written by `updateMyProfile`.",
    "items": {
     "type": "string"
    }
   },
   "accessibility": {
    "type": "array",
    "description": "Also written by `updateMyProfile`.",
    "items": {
     "type": "string"
    }
   },
   "preferredChannel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "x-ticvai-persisted": false,
    "description": "**Stored on the profile** (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest.\n"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
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
   },
   "mergedIntoSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"
   },
   "mergedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
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
    "description": "False until an OTP or a verified provider identity confirms ownership. An unverified account may browse and fill a cart but not transact: the gate is the checkout page (ADR-0045), where `checkoutCart` refuses it until the guest verifies or proves the contact by code. UAE Pass returns a verified identity, so it starts true. Rule on `verifyGuestEmail`, decided 17 September 2026.\n"
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
   "requiresMfa": {
    "type": "boolean",
    "default": false,
    "description": "True only where the sign-in venue enabled guest two-step verification (`VenueSettings.identity.guestTwoStep`, in tenancy) and this guest has an active method (decided 29 September, rev 3 GAP-B1, per venue). The session is then not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge. Always false for a UAE Pass sign-in, which is already a verified two-factor identity (proposed, client to correct).\n"
   },
   "mfaMethods": {
    "type": "array",
    "description": "The guest's active methods, so the client can offer the right one. Empty when `requiresMfa` is false.",
    "items": {
     "$ref": "#/components/schemas/MfaMethod"
    }
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
    "description": "**30 days, sliding** (decided 28 September, audit R126 (2)): each use of the session moves this to 30 days from now, and 30 days unused ends it. **One session per device**: a guest may be signed in on a phone and a laptop at once, and a new sign-in on the same `deviceId` ends that device's previous session.\n"
   }
  }
 },
 "IdentityGuestDocumentSubmission": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the document goes to pii.subject_document and the verification to identity.guest_identity_verification",
  "required": [
   "documentKind",
   "documentNumber",
   "documentAssetId"
  ],
  "properties": {
   "documentKind": {
    "type": "string",
    "enum": [
     "passport",
     "emiratesId",
     "nationalId",
     "drivingLicence",
     "residencePermit",
     "other"
    ],
    "description": "The vocabulary of `pii.subject_document.kind`."
   },
   "documentNumber": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "maxLength": 64,
    "description": "**Write-only, never returned.** Hashed on arrival; only the last four are kept in clear."
   },
   "issuingCountry": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "expiresOn": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "documentAssetId": {
    "type": "string",
    "format": "uuid",
    "description": "The uploaded scan or photo of the document."
   },
   "selfieAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A live photo for the reviewer to compare, where the policy asks for one. Deleted with the scan."
   },
   "reason": {
    "type": "string",
    "enum": [
     "policyRequired",
     "ageRestrictedPurchase",
     "residentPricing",
     "accountRecovery"
    ],
    "default": "policyRequired",
    "description": "What the guest is verifying for; the review queue shows it."
   }
  }
 },
 "IdentityGuestVerification": {
  "type": "object",
  "x-ticvai-persistence": "identity.guest_identity_verification",
  "description": "**One guest identity-document verification** (5.3.21; decided 29 September, build pass): the document it checks, its status, the method and who decided. The document itself is `pii.subject_document`; this row holds no document number.",
  "required": [
   "id",
   "subjectId",
   "status",
   "submittedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectDocumentId": {
    "type": "string",
    "format": "uuid",
    "description": "The `pii.subject_document` row submitted."
   },
   "documentKind": {
    "type": "string",
    "enum": [
     "passport",
     "emiratesId",
     "nationalId",
     "drivingLicence",
     "residencePermit",
     "other"
    ]
   },
   "documentNumberLast4": {
    "type": "string",
    "maxLength": 4,
    "nullable": true,
    "readOnly": true
   },
   "reason": {
    "type": "string",
    "enum": [
     "policyRequired",
     "ageRestrictedPurchase",
     "residentPricing",
     "accountRecovery"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "verified",
     "rejected",
     "resubmissionRequested"
    ],
    "readOnly": true
   },
   "method": {
    "type": "string",
    "enum": [
     "manualReview",
     "documentScanner",
     "provider"
    ],
    "nullable": true,
    "readOnly": true
   },
   "decisionReason": {
    "type": "string",
    "maxLength": 300,
    "nullable": true,
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "documentImageDeletedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the scan (and any selfie) was deleted under the policy's retention."
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
   "leaderboardNickname": {
    "type": "string",
    "nullable": true,
    "maxLength": 24,
    "description": "BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"
   },
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
   "tierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The client ULID from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
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
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
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
  "x-ticvai-persistence": "orders.order_line + orders.order_line_eligibility + orders.order_line_discount",
  "x-ticvai-retired-columns": [
   "promotion_id",
   "name",
   "reason"
  ],
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
      "description": "The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.",
      "items": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     },
     "reprintCount": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "readOnly": true,
      "description": "How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."
     },
     "venueId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."
     },
     "discounts": {
      "type": "array",
      "readOnly": true,
      "description": "**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.",
      "items": {
       "$ref": "#/components/schemas/OrderLineDiscount"
      }
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
 "OrderSummary": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "id",
   "orderNumber",
   "status",
   "grossAmount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderNumber": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "The same vocabulary as `Order.channel`, which this projects."
   },
   "lineCount": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "The cashier who raised it — what the held-orders list shows."
   },
   "holdLabel": {
    "type": "string",
    "nullable": true,
    "description": "As `Order.holdLabel`."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
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
    "nullable": true,
    "description": "The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."
   },
   "providerIdempotencyKey": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal a till payment ran on (ECR flow, SD-034)."
   },
   "nextAction": {
    "type": "object",
    "nullable": true,
    "x-ticvai-persisted": false,
    "description": "**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.",
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "redirect",
       "terminal"
      ]
     },
     "url": {
      "type": "string",
      "format": "uri",
      "nullable": true
     },
     "expiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
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
    "writeOnly": true,
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "writeOnly": true,
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
       "x-ticvai-column": "list_price",
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the wire keeps `price`."
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
