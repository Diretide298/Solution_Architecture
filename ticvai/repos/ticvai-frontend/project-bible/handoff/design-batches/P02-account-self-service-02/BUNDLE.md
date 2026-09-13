# P02-account-self-service-02 — P02 · Account & Self-Service (2 of 2)

**4 screens · 16 operations · 6 schemas · 6 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, LOYALTY_REDEEM, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: getWaiverStatus
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-067` | Refunds & Resale | statusTracker | 3 | 0 | — |
| `GST-069` | Face Pass | statusTracker | 3 | 1 | — |
| `GST-071` | Payment Methods | listDetail | 5 | 0 | — |
| `GST-073` | Security & Sign-in | configEditor | 5 | 0 | — |

## Thin screens in this batch

**GST-067, GST-069 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-067",
  "name": "Refunds & Resale",
  "module": "Account & Self-Service",
  "requiresModule": "core",
  "wave": 2,
  "capability": "read-write",
  "implementation": {
   "app": "guest-app",
   "route": "/account/refunds-resale",
   "component": "apps/guest-app/src/routes/account/RefundsResale.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "GST-039"
   ],
   "entryFrom": [
    "GST-008"
   ],
   "inferred": false,
   "notes": "**Reached from GST-008** — a refund starts from the ticket being refunded. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**A guest could buy a ticket and not ask for their money back.** `createRefundRequest` and `createResaleListing` were back-office only, so every refund began as a phone call.\n\n**The refund policy decides what is offered, not this screen.** `orders.refund_policy` is scoped, so a venue may be stricter than its tenant — the screen shows the answer rather than arguing with it.",
  "density": "comfortable",
  "offline": false,
  "pattern": "statusTracker",
  "patternReason": "`getWaiverStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "**A guest could buy a ticket and not ask for their money back.** `createRefundRequest` and `createResaleListing` were back-office only, so every refund began as a phone call.",
  "gaps": [
   {
    "operation": "getWaiverStatus",
    "why": "**1 declared operation reach no component on this screen**: getWaiverStatus. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createRefundRequest",
       "provenance": "contract orders.yaml POST /refund-requests"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createResaleListing",
       "provenance": "contract orders.yaml POST /resale-listings"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**No refunds or listings yet.** The venue's policy is shown regardless, so a guest knows the answer before they need it.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** Refunds and resale listings need the server — a queued refund request is a promise nobody made."
  },
  "apis": [
   {
    "operationId": "createRefundRequest",
    "contract": "orders",
    "purpose": "Guest-initiated refund request",
    "trigger": "onAction"
   },
   {
    "operationId": "createResaleListing",
    "contract": "orders",
    "purpose": "List an entitlement for resale",
    "trigger": "onAction"
   },
   {
    "operationId": "getWaiverStatus",
    "contract": "marketing-crm",
    "purpose": "Whether this guest may be issued a ticket that requires a wa",
    "trigger": "onLoad",
    "offline": false
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030)."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-067"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-069",
  "name": "Face Pass",
  "module": "Account & Self-Service",
  "requiresModule": "core",
  "wave": 2,
  "capability": "read-write",
  "implementation": {
   "app": "guest-app",
   "route": "/account/face-pass",
   "component": "apps/guest-app/src/routes/account/FacePass.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "GST-039"
   ],
   "entryFrom": [
    "GST-039"
   ],
   "inferred": false,
   "notes": "**Reached from GST-039** — enrolment is a setting on the profile. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "🔴 **Biometric enrolment had no guest-facing consent step.** `enrolFacePass` was callable by a guest and reachable from nowhere, which means enrolment was happening at a desk with somebody else operating the screen.\n\n**`pii.subject_biometric` is separate from contact and document precisely so consent and erasure differ per kind.** Revocation sits beside enrolment for the same reason — a face a guest cannot withdraw is a face they did not really consent to.",
  "density": "comfortable",
  "offline": false,
  "pattern": "statusTracker",
  "patternReason": "`getFacePassEnrolment` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "🔴 **Biometric enrolment had no guest-facing consent step.** `enrolFacePass` was callable by a guest and reachable from nowhere, which means enrolment was happening at a desk with somebody else operat",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected face pass",
       "bindsTo": "FacePassEnrolment",
       "columns": [
        "FacePassEnrolment.id",
        "FacePassEnrolment.subjectId",
        "FacePassEnrolment.entitlementId",
        "FacePassEnrolment.source",
        "FacePassEnrolment.capturedAt",
        "FacePassEnrolment.consentPurposeId",
        "FacePassEnrolment.consentGivenAt",
        "FacePassEnrolment.guardianSubjectId",
        "FacePassEnrolment.isActive",
        "FacePassEnrolment.expiresAt"
       ],
       "operation": "getFacePassEnrolment",
       "provenance": "contract access.yaml GET /face-pass/enrolments/{enrolmentId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Enrol",
       "operation": "enrolFacePass",
       "provenance": "contract access.yaml POST /face-pass/enrolments"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke",
       "operation": "revokeFacePass",
       "provenance": "contract access.yaml DELETE /face-pass/enrolments/{enrolmentId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRevokeFacePass",
    "component": "confirmDialog",
    "trigger": "Revoke",
    "body": "**Names what `revokeFacePass` changes and what it leaves alone**, in the consequence rather than the verb. A face pass this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml DELETE /face-pass/enrolments/{enrolmentId}"
   }
  ],
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**Not enrolled.** What a face pass is for, where it works, and what withdrawing it does — **before** the camera opens.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** Biometric enrolment never happens offline — a face captured and queued is a face the guest cannot withdraw until it uploads."
  },
  "apis": [
   {
    "operationId": "enrolFacePass",
    "contract": "access",
    "purpose": "Register a facial profile against an entitlement",
    "trigger": "onAction"
   },
   {
    "operationId": "getFacePassEnrolment",
    "contract": "access",
    "purpose": "Whether a pass has a face registered, and when",
    "trigger": "onLoad"
   },
   {
    "operationId": "revokeFacePass",
    "contract": "access",
    "purpose": "Remove a facial profile",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "enrolmentId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030)."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-069"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-071",
  "name": "Payment Methods",
  "module": "Account & Self-Service",
  "requiresModule": "core",
  "wave": 2,
  "capability": "read-write",
  "implementation": {
   "app": "guest-app",
   "route": "/account/payment-methods",
   "component": "apps/guest-app/src/routes/account/PaymentMethods.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "GST-039"
   ],
   "entryFrom": [
    "GST-039"
   ],
   "inferred": false,
   "notes": "**Reached from GST-039** — a payment method is a setting on the profile. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**A stored card a guest cannot see is a stored card they cannot remove.** `listPaymentTokens` and `storePaymentToken` were guest-callable with no guest screen.\n\n**Wallet transfer and loyalty redemption sit here** because to a guest they are all *how I pay*, whatever the contracts call them.",
  "density": "comfortable",
  "offline": false,
  "pattern": "listDetail",
  "patternReason": "`listPaymentTokens` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "**A stored card a guest cannot see is a stored card they cannot remove.** `listPaymentTokens` and `storePaymentToken` were guest-callable with no guest screen.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every payment methods",
       "bindsTo": "PaymentToken",
       "columns": [
        "PaymentToken.id",
        "PaymentToken.subjectId",
        "PaymentToken.providerId",
        "PaymentToken.token",
        "PaymentToken.method",
        "PaymentToken.maskedIdentifier",
        "PaymentToken.expiresAt",
        "PaymentToken.isDefault",
        "PaymentToken.consentPurposeId"
       ],
       "operation": "listPaymentTokens",
       "provenance": "contract orders.yaml GET /payment-tokens"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment methods",
       "bindsTo": "PaymentToken",
       "columns": [
        "PaymentToken.id",
        "PaymentToken.subjectId",
        "PaymentToken.providerId",
        "PaymentToken.token",
        "PaymentToken.method",
        "PaymentToken.maskedIdentifier",
        "PaymentToken.expiresAt",
        "PaymentToken.isDefault",
        "PaymentToken.consentPurposeId"
       ],
       "operation": "listPaymentTokens",
       "provenance": "contract orders.yaml GET /payment-tokens"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Store",
       "operation": "storePaymentToken",
       "provenance": "contract orders.yaml POST /payment-tokens"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer",
       "operation": "transferWalletBalance",
       "provenance": "contract retail.yaml POST /wallets/{walletId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Redeem",
       "operation": "redeemLoyaltyPoints",
       "provenance": "contract marketing-crm.yaml POST /loyalty/redemptions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**No stored cards.** A guest arrives here after a first purchase, so the empty state is the common one.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Balances and stored cards already loaded stay visible with their age, cards masked. Storing a card and transferring value need the server."
  },
  "apis": [
   {
    "operationId": "listPaymentTokens",
    "contract": "orders",
    "purpose": "A guest's saved payment methods",
    "trigger": "onLoad"
   },
   {
    "operationId": "storePaymentToken",
    "contract": "orders",
    "purpose": "Save a payment method for future use",
    "trigger": "onAction",
    "invalidates": [
     "listPaymentTokens"
    ]
   },
   {
    "operationId": "transferWalletBalance",
    "contract": "retail",
    "purpose": "Send balance to another guest",
    "trigger": "onAction",
    "invalidates": [
     "listPaymentTokens"
    ]
   },
   {
    "operationId": "redeemLoyaltyPoints",
    "contract": "marketing-crm",
    "purpose": "Spend points",
    "trigger": "onAction",
    "invalidates": [
     "listPaymentTokens"
    ]
   },
   {
    "operationId": "getGiftCard",
    "contract": "retail",
    "purpose": "Balance on a gift card",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "walletId",
     "from": "deepLink"
    },
    {
     "name": "cardCode",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030).",
   "preloaded": [
    "PaymentToken.id",
    "PaymentToken.subjectId",
    "PaymentToken.providerId",
    "PaymentToken.token",
    "PaymentToken.method"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-071"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-073",
  "name": "Security & Sign-in",
  "module": "Account & Self-Service",
  "requiresModule": "core",
  "wave": 2,
  "capability": "read-write",
  "implementation": {
   "app": "guest-app",
   "route": "/account/security-sign-in",
   "component": "apps/guest-app/src/routes/account/SecuritySignIn.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "GST-039"
   ],
   "entryFrom": [
    "GST-039"
   ],
   "inferred": false,
   "notes": "**Reached from GST-039** — sign-in security is a setting on the profile. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**A guest could enrol a second factor and not manage it.** Small screen, and it is the one a guest reaches after losing a phone.",
  "density": "comfortable",
  "offline": false,
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`createMfaChallenge`) and no read of a population — it is settings, not a list",
  "purpose": "**A guest could enrol a second factor and not manage it.** Small screen, and it is the one a guest reaches after losing a phone.",
  "gaps": [
   {
    "operation": "createMfaChallenge",
    "why": "**`createMfaChallenge` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract identity.yaml POST /auth/mfa/challenge"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createMfaChallenge",
       "provenance": "contract identity.yaml POST /auth/mfa/challenge"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listGuestDevices",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "revokeGuestDevice",
       "label": "Revoke guest device",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createMfaChallenge"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**No second factor enrolled.** Explains what one protects before asking for a phone number.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Nothing here is offered offline, and the banner says so.** An erasure request or a device change queued and never sent is worse than one that could not be made — the legal clock starts when the platform receives it, and a second factor set up offline is not a second factor."
  },
  "apis": [
   {
    "operationId": "createMfaChallenge",
    "contract": "identity",
    "purpose": "Step-up authentication for a sensitive action",
    "trigger": "onAction"
   },
   {
    "operationId": "listGuestDevices",
    "contract": "marketing-crm",
    "purpose": "Which devices hold this guest's credentials",
    "trigger": "onLoad"
   },
   {
    "operationId": "registerGuestDevice",
    "contract": "marketing-crm",
    "purpose": "Trust this device",
    "trigger": "onAction"
   },
   {
    "operationId": "revokeGuestDevice",
    "contract": "marketing-crm",
    "purpose": "Sign a lost device out",
    "trigger": "onAction"
   },
   {
    "operationId": "verifyGuestEmail",
    "contract": "identity",
    "purpose": "Confirm the address before it can recover an account",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "deviceId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030)."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-073"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
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
 "createResaleListing": {
  "method": "POST",
  "path": "/resale-listings",
  "contract": "orders",
  "summary": "List an entitlement for resale",
  "permission": "ORDER_CREATE",
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
  "requestBody": "ResaleListing",
  "responds": "ResaleListing"
 },
 "enrolFacePass": {
  "method": "POST",
  "path": "/face-pass/enrolments",
  "contract": "access",
  "summary": "Register a facial profile against an entitlement",
  "permission": "GUEST_MANAGE",
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
  "responds": "FacePassEnrolment"
 },
 "getFacePassEnrolment": {
  "method": "GET",
  "path": "/face-pass/enrolments/{enrolmentId}",
  "contract": "access",
  "summary": "Whether a pass has a face registered, and when",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FacePassEnrolment"
 },
 "getGiftCard": {
  "method": "GET",
  "path": "/gift-cards/{cardCode}",
  "contract": "retail",
  "summary": "Check a gift card balance",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GiftCard"
 },
 "getWaiverStatus": {
  "method": "GET",
  "path": "/guests/{subjectId}/waiver-status",
  "contract": "marketing-crm",
  "summary": "Whether this guest may be issued a ticket that requires a waiver",
  "permission": "GUEST_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
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
 "listPaymentTokens": {
  "method": "GET",
  "path": "/payment-tokens",
  "contract": "orders",
  "summary": "A guest's saved payment methods",
  "permission": "ORDER_VIEW",
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
  "responds": "PaymentToken"
 },
 "redeemLoyaltyPoints": {
  "method": "POST",
  "path": "/loyalty/redemptions",
  "contract": "marketing-crm",
  "summary": "Spend points",
  "permission": "LOYALTY_REDEEM",
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
  "responds": "LoyaltyPosition"
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
 "revokeFacePass": {
  "method": "DELETE",
  "path": "/face-pass/enrolments/{enrolmentId}",
  "contract": "access",
  "summary": "Remove a facial profile",
  "permission": "GUEST_MANAGE",
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
 "storePaymentToken": {
  "method": "POST",
  "path": "/payment-tokens",
  "contract": "orders",
  "summary": "Save a payment method for future use",
  "permission": "ORDER_CREATE",
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
  "responds": "PaymentToken"
 },
 "transferWalletBalance": {
  "method": "POST",
  "path": "/wallets/{walletId}/transfer",
  "contract": "retail",
  "summary": "Send balance to another guest",
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
  "responds": null
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "FacePassEnrolment": {
  "type": "object",
  "x-ticvai-persistence": "pii.subject_biometric",
  "description": "3.2.43. **Metadata about a facial profile. Never the profile.**\n",
  "required": [
   "id",
   "subjectId",
   "entitlementId",
   "source",
   "capturedAt"
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
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "source": {
    "type": "string",
    "enum": [
     "guestApp",
     "ticketCounter",
     "annualPassCounter"
    ]
   },
   "capturedAt": {
    "type": "string",
    "format": "date-time"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid"
   },
   "consentGivenAt": {
    "type": "string",
    "format": "date-time"
   },
   "guardianSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the subject is a minor (3.2.12)."
   },
   "isActive": {
    "type": "boolean",
    "readOnly": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Bounded by the entitlement it belongs to.** A face outliving the pass it was enrolled for is a biometric held for no stated purpose, which CF-64 has to settle.\n"
   }
  }
 },
 "GiftCard": {
  "x-ticvai-persistence": "retail.gift_card",
  "type": "object",
  "required": [
   "cardCode",
   "faceValue",
   "balance",
   "status",
   "issuedAt"
  ],
  "properties": {
   "cardCode": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "faceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "active",
     "partiallyRedeemed",
     "redeemed",
     "expired",
     "blocked"
    ]
   },
   "blockedReason": {
    "type": "string",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "PaymentToken": {
  "type": "object",
  "x-ticvai-persistence": "orders.payment_token",
  "description": "BL-116. **A stored credential, held by the provider and referenced here.** The platform never sees a card number, which is what keeps PCI scope where it belongs.\n**A token is provider-scoped.** A card tokenised with one gateway does not work with another, so a routing change does not silently move a guest's saved card — it means asking them again, and the model should make that visible rather than surprising.\n",
  "required": [
   "id",
   "subjectId",
   "providerId",
   "token",
   "isDefault"
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
   "providerId": {
    "type": "string",
    "format": "uuid"
   },
   "token": {
    "type": "string",
    "format": "password",
    "description": "**Write-only, never returned.** The provider's reference to a credential it holds.\n"
   },
   "method": {
    "type": "string"
   },
   "maskedIdentifier": {
    "type": "string",
    "description": "What a guest sees — the last four digits, the card brand. **Enough to choose between two saved cards and not enough to use one.**\n"
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "isDefault": {
    "type": "boolean"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Storing a card for future use is a purpose a guest consents to**, separate from the payment they are making now. A token taken without it is a card kept on a guest's behalf that they never agreed to.\n"
   }
  }
 },
 "ResaleListing": {
  "type": "object",
  "x-ticvai-persistence": "orders.resale_listing",
  "description": "BL-060. **Smaller than it first looked** — most of the machinery exists. An entitlement can already be transferred, an order can already be created, and payment already routes. What was missing is the listing itself and a cart line that can point at one.\n**A resale is a transfer with money attached**, and the venue is in the middle: the seller's entitlement is voided and a new one issued to the buyer, so **the ticket that admits is always one the venue issued.** That is what stops a screenshot at the gate.\n",
  "required": [
   "id",
   "entitlementId",
   "sellerSubjectId",
   "askPrice",
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
   "sellerSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "askPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "priceCapPercent": {
    "type": "number",
    "nullable": true,
    "description": "**A ceiling as a percentage of face value**, because uncapped resale is a venue watching its own tickets sold at four times the price with its name on them. Null means uncapped, which is a venue decision rather than a default.\n"
   },
   "sellerFeePercent": {
    "type": "number"
   },
   "buyerFeePercent": {
    "type": "number"
   },
   "status": {
    "type": "string",
    "enum": [
     "listed",
     "reserved",
     "sold",
     "withdrawn",
     "expired"
    ]
   },
   "listedAt": {
    "type": "string",
    "format": "date-time"
   },
   "soldToSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "payoutStatus": {
    "type": "string",
    "enum": [
     "pending",
     "held",
     "paid",
     "failed"
    ],
    "description": "**The seller is paid after the buyer is admitted, not after they pay.** A resale refunded at the gate for a void ticket cannot be clawed back from a seller who has already been paid.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 }
}
```
