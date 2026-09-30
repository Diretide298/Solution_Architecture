# P02-account-self-service-02 — P02 · Account & Self-Service (2 of 2)

**4 screens · 26 operations · 23 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, LOYALTY_REDEEM, ORDER_CREATE, ORDER_VIEW, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **2 of these operations work offline**: getGuestSession, getWaiverStatus
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-067` | Refunds & Resale | statusTracker | 3 | 2 | — |
| `GST-069` | Face Pass | statusTracker | 4 | 2 | — |
| `GST-071` | Payment Methods | listDetail | 5 | 3 | — |
| `GST-073` | Security & Sign-in | configEditor | 14 | 4 | — |

## Thin screens in this batch

**GST-067 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
    "GST-019"
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
     "provenance": "derived — GST-039 declares entryState.params subjectId and GST-067 holds subjectId, so an edge into it carries them"
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
    "why": "**`getWaiverStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract marketing-crm.yaml GET /guests/{subjectId}/waiver-status"
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
       "label": "Create refund request",
       "operation": "createRefundRequest",
       "provenance": "contract orders.yaml POST /refund-requests"
      },
      {
       "kind": "secondaryButton",
       "label": "Create resale listing",
       "operation": "createResaleListing",
       "provenance": "contract orders.yaml POST /resale-listings"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Waiver status",
       "operation": "getWaiverStatus",
       "notes": "Shows `isSatisfied`, `missingFormIds`, `expiringWithinDays` from `getWaiverStatus`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/waiver-status"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**No refunds or listings yet.** The venue's policy is shown regardless, so a guest knows the answer before they need it.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW`, which `getWaiverStatus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-067",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → Refunds & resale"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "id": "formCreateResaleListing",
    "component": "modal",
    "trigger": "Create resale listing",
    "body": "**Collects what `createResaleListing` sends before it is called.** Required: `entitlementId`, `askPrice`. Optional: `sellerSubjectId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateResaleListingRequest",
    "confirm": {
     "label": "Create resale listing",
     "operation": "createResaleListing"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "entitlementId",
      "askPrice",
      "sellerSubjectId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
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
     "provenance": "derived — GST-039 declares entryState.params subjectId and GST-069 holds subjectId, so an edge into it carries them"
    }
   ]
  },
  "notes": "🔴 **Biometric enrolment had no guest-facing consent step.** `enrolFacePass` was callable by a guest and reachable from nowhere, which means enrolment was happening at a desk with somebody else operating the screen.\n\n**`pii.subject_biometric` is separate from contact and document precisely so consent and erasure differ per kind.** Revocation sits beside enrolment for the same reason — a face a guest cannot withdraw is a face they did not really consent to.\n\n**Who is this for** (decided 28 September, audit R205): the signed-in adult enrols themselves or a linked child, and is recorded as guardian by the server. The age below which a subject is a minor is an open value client counsel sets.",
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
       "kind": "selectField",
       "label": "Who is this for",
       "bindsTo": "DelegatedAccess",
       "columns": [
        "DelegatedAccess.overSubjectId",
        "DelegatedAccess.delegationKind"
       ],
       "operation": "listDelegations",
       "notes": "**The first step of enrolment** (decided 28 September, audit R205): the signed-in guest, then each child linked to them — the `heldByThisGuest` grants whose `delegationKind` is `familyMember` or `primaryHolder`. The chosen person's id is the `subjectId` that `enrolFacePass` sends. **No guardian field is collected**: the server records the caller as guardian.",
       "provenance": "contract identity.yaml GET /guests/{subjectId}/delegations"
      },
      {
       "kind": "detailPanel",
       "label": "The face pass enrolment",
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
       "label": "Enrol face pass",
       "operation": "enrolFacePass",
       "provenance": "contract access.yaml POST /face-pass/enrolments"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke face pass",
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
    "trigger": "Revoke face pass",
    "body": "**Names what `revokeFacePass` changes and what it leaves alone**, in the consequence rather than the verb. A face pass this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formEnrolFacePass",
    "component": "modal",
    "trigger": "Enrol face pass",
    "body": "**Collects what `enrolFacePass` sends before it is called.** Required: `subjectId`, `entitlementId`, `template`, `capturedAt`, `source`, `consent`. `subjectId` is the person picked in **Who is this for** (the guest or a linked child), not typed; **no guardian is asked for** — the server sets `consent.guardianSubjectId` to the signed-in guest (decided 28 September, audit R205). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Enrol face pass",
     "operation": "enrolFacePass"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "subjectId",
      "entitlementId",
      "template",
      "capturedAt",
      "source",
      "consent"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**Not enrolled.** What a face pass is for, where it works, and what withdrawing it does — **before** the camera opens.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW`, which `getFacePassEnrolment` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** Biometric enrolment never happens offline — a face captured and queued is a face the guest cannot withdraw until it uploads.",
   "subjectNotLinked": "**Refused: that person is not linked to you** (403 `subject-not-linked`). A guest may enrol only themselves or a child linked to them by a family-member or primary-holder delegation; the screen says so and returns to **Who is this for**, which is refreshed in case the link was just removed (decided 28 September, audit R205)."
  },
  "apis": [
   {
    "operationId": "listDelegations",
    "contract": "identity",
    "purpose": "Who this guest may enrol — themselves and the children linked to them (heldByThisGuest, familyMember or primaryHolder) (decided 28 September, audit R205)",
    "trigger": "onLoad"
   },
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-069",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → Face Pass (also Account → Face Pass)"
   }
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
     "provenance": "derived — GST-039 declares entryState.params subjectId and GST-071 holds subjectId, so an edge into it carries them"
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
       "label": "Every payment token",
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
       "label": "The selected payment token",
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
      },
      {
       "kind": "detailPanel",
       "label": "The gift card",
       "bindsTo": "GiftCard",
       "columns": [
        "GiftCard.cardCode",
        "GiftCard.kind",
        "GiftCard.faceValue",
        "GiftCard.balance",
        "GiftCard.status",
        "GiftCard.blockedReason",
        "GiftCard.issuedAt",
        "GiftCard.activatedAt",
        "GiftCard.expiresAt"
       ],
       "operation": "getGiftCard",
       "provenance": "contract wallet.yaml GET /gift-cards/{cardCode}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Store payment token",
       "operation": "storePaymentToken",
       "provenance": "contract orders.yaml POST /payment-tokens"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer wallet balance",
       "operation": "transferWalletBalance",
       "provenance": "contract retail.yaml POST /wallets/{walletId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Redeem loyalty points",
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
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listPaymentTokens` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "contract": "wallet",
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
    "contract": "wallet",
    "purpose": "Balance on a gift card",
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-071",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → Payment methods",
    "differences": "The Account → \"Payment methods\" row opens Engine settings instead of this screen."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formStorePaymentToken",
    "component": "modal",
    "trigger": "Store payment token",
    "body": "**Collects what `storePaymentToken` sends before it is called.** Required: `providerId`, `providerToken`, `consentPurposeId`. Optional: `setDefault`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Store payment token",
     "operation": "storePaymentToken"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "providerId",
      "providerToken",
      "consentPurposeId",
      "setDefault"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formTransferWalletBalance",
    "component": "modal",
    "trigger": "Transfer wallet balance",
    "body": "**Collects what `transferWalletBalance` sends before it is called.** Required: `amount`. Optional: `toSubjectId`, `toWalletId`, `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer wallet balance",
     "operation": "transferWalletBalance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount",
      "toSubjectId",
      "toWalletId",
      "message"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRedeemLoyaltyPoints",
    "component": "modal",
    "trigger": "Redeem loyalty points",
    "body": "**Collects what `redeemLoyaltyPoints` sends before it is called.** Required: `subjectId`, `programmeId`, `points`. Optional: `rewardId`, `orderId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Redeem loyalty points",
     "operation": "redeemLoyaltyPoints"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "subjectId",
      "programmeId",
      "points",
      "rewardId",
      "orderId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
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
     "provenance": "derived — GST-039 declares entryState.params subjectId and GST-073 holds subjectId, so an edge into it carries them"
    }
   ]
  },
  "notes": "**A guest could enrol a second factor and not manage it.** Small screen, and it is the one a guest reaches after losing a phone. **Two-step verification, per venue** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, which had removed it on 28 September): a guest may enrol a method on their account (`listMfaMethods`, `enrolMfaMethod`, `verifyMfaEnrolment`, `removeMfaMethod`; an authenticator, with an email code as fallback), **offered only when at least one venue of the tenant has `VenueSettings.identity.guestTwoStep.enabled` on** — when none has, the section is not shown. The code is then asked only when signing in or acting at a venue that has it on (step-up before that venue's `guestTwoStep.stepUpActions`: `createMfaChallenge`, `verifyMfaChallenge`). No enterprise SSO for guests (R167, first part, stands). What the screen offers instead: the sign-in methods linked to the account (`GuestSession.identityProviders`), confirming the email that recovers it (`verifyGuestEmail`), the devices that hold its credentials and signing a lost one out (`listGuestDevices`, `revokeGuestDevice`), and signing out here (`guestLogout`). The contract has no guest operation that lists sessions, so \"your sessions\" is the device list.",
  "density": "comfortable",
  "offline": false,
  "pattern": "configEditor",
  "patternReason": "settings for the guest's own sign-in — the linked sign-in methods (`getGuestSession`) and the devices that hold the account (`listGuestDevices`), each with one act; not a list to browse",
  "purpose": "**How this guest signs in, and where.** The sign-in methods linked to the account, the email that recovers it, and the devices signed in, with a way to sign a lost phone out. Small screen, and it is the one a guest reaches after losing a phone. Two-step verification where a venue of the tenant enabled it (decided 29 September, rev 3 GAP-B1, per venue).",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Sign out on this device",
       "operation": "guestLogout",
       "provenance": "contract identity.yaml DELETE /auth/guest/session"
      },
      {
       "kind": "secondaryButton",
       "label": "Register guest device",
       "operation": "registerGuestDevice",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/devices"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke guest device",
       "operation": "revokeGuestDevice",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/devices/{deviceId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify guest email",
       "operation": "verifyGuestEmail",
       "provenance": "contract identity.yaml POST /auth/guest/verify-email"
      },
      {
       "kind": "secondaryButton",
       "label": "Set up two-step verification",
       "operation": "enrolMfaMethod",
       "provenance": "decided 29 September, rev 3 GAP-B1"
      }
     ]
    },
    {
     "name": "contentBody",
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
        "GuestDevice.tokenRef",
        "GuestDevice.appVersion",
        "GuestDevice.osVersion",
        "GuestDevice.deviceModel",
        "GuestDevice.locale",
        "GuestDevice.status",
        "GuestDevice.failureCount",
        "GuestDevice.registeredAt"
       ],
       "operation": "listGuestDevices",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/devices"
      },
      {
       "kind": "detailPanel",
       "label": "How you sign in",
       "bindsTo": "GuestSession",
       "columns": [
        "GuestSession.displayName",
        "GuestSession.isVerified",
        "GuestSession.identityProviders"
       ],
       "operation": "getGuestSession",
       "notes": "The sign-in methods linked to this account (code, password, Apple, Google, UAE Pass) and whether its contact is verified. A second factor is listed only when a venue of the tenant enabled guest two-step verification (decided 29 September, rev 3 GAP-B1, per venue).",
       "provenance": "contract identity.yaml GET /auth/guest/session"
      },
      {
       "kind": "cardList",
       "label": "Two-step verification",
       "notes": "Enrol, verify, remove. **Shown only when a venue of the tenant has guest two-step verification on.**",
       "operation": "listMfaMethods",
       "provenance": "decided 29 September, rev 3 GAP-B1 (per venue)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**Only this device is signed in.** The device list holds one row, this one, and the screen says that signing in elsewhere will add a row here.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW`, which `verifyGuestEmail` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Nothing here is offered offline, and the banner says so.** An erasure request or a device change queued and never sent is worse than one that could not be made — the legal clock starts when the platform receives it, and a device signed out offline is still signed in."
  },
  "apis": [
   {
    "operationId": "getGuestSession",
    "contract": "identity",
    "purpose": "The sign-in methods linked to the account and whether it is verified",
    "trigger": "onLoad"
   },
   {
    "operationId": "guestLogout",
    "contract": "identity",
    "purpose": "Sign out on this device",
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
   },
   {
    "operationId": "listMfaMethods",
    "contract": "identity",
    "purpose": "The guest's enrolled methods",
    "trigger": "onLoad"
   },
   {
    "operationId": "enrolMfaMethod",
    "contract": "identity",
    "purpose": "Enrol an authenticator (email code as fallback)",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "verifyMfaEnrolment",
    "contract": "identity",
    "purpose": "Confirm the enrolment with a first code",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "removeMfaMethod",
    "contract": "identity",
    "purpose": "Remove a method",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "createMfaChallenge",
    "contract": "identity",
    "purpose": "Step-up before a sensitive act at a venue that has it on",
    "trigger": "onAction"
   },
   {
    "operationId": "verifyMfaChallenge",
    "contract": "identity",
    "purpose": "Check the step-up code",
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
    },
    {
     "name": "deviceId",
     "from": "session"
    },
    {
     "name": "challengeId",
     "from": "navigation"
    },
    {
     "name": "methodId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030)."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-073",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-073.html, and #GST-073 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 2 → Security & sign-in (partial). What v2 did differently: Prototype offers two-step verification and a trusted-device skip, but the YAML says guests have no second factor (R167). Either remove the toggle from the prototype or reopen the decision."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
   },
   {
    "id": "confirmRevokeGuestDevice",
    "component": "confirmDialog",
    "trigger": "Revoke guest device",
    "body": "**Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A security sign-in this affects should be identified in the dialog, not just counted.",
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
   },
   {
    "id": "formEnrolMfaMethod",
    "component": "modal",
    "trigger": "Set up two-step verification",
    "body": "**Collects what `enrolMfaMethod` sends**, then asks for the first code (`verifyMfaEnrolment`). The guest is told the code will be asked only at venues that turned it on. Dismissing enrols nothing.",
    "confirm": {
     "label": "Turn on",
     "operation": "verifyMfaEnrolment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "methodId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
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
  "requestBody": "CreateResaleListingRequest",
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
  "contract": "wallet",
  "summary": "Check a gift card balance",
  "permission": "WALLET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GiftCard"
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
 "listDelegations": {
  "method": "GET",
  "path": "/guests/{subjectId}/delegations",
  "contract": "identity",
  "summary": "Who may act for this guest, and for whom they may act",
  "permission": "GUEST_VIEW",
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
  "responds": "Page"
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
 "transferWalletBalance": {
  "method": "POST",
  "path": "/wallets/{walletId}/transfer",
  "contract": "wallet",
  "summary": "Send balance to another guest",
  "permission": "WALLET_OPERATE",
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
  "responds": "WalletTransaction"
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
 "BiometricKind": {
  "type": "string",
  "description": "BL-106, CF-35. **Two different legal postures, not two settings on one record.** 3.2.44 describes a temporary facial model taken at a counter or a gate and deleted when the ticket expires; 3.2.43 describes an enduring Face Pass enrolled deliberately on three surfaces. **Storing both as one record with a date makes the stricter rule depend on a field nobody enforces**, which is what BL-106 was raised to stop.\n`facePass` — enduring, explicit consent, revocable by the guest, anchored to the validity of the entitlement it belongs to.\n`faceTag` — same-visit, **consent still explicit and still recorded**, anchored to the ticket and purged at close of the operating day. **PDPL Article 4 is a closed list of exceptions with no legitimate-interests basis**, so a short life does not remove the need for consent — it only shortens what the consent is for.\n",
  "enum": [
   "facePass",
   "faceTag"
  ]
 },
 "BiometricRetentionAnchor": {
  "type": "string",
  "readOnly": true,
  "description": "BL-106, ADR-0047. **What the expiry is measured from, derived from the kind rather than chosen.** A retention period a person can type is a retention period somebody will type wrongly; the anchor follows the kind, and the kind follows how the biometric was taken.\n`entitlementValidity` — `facePass`. The face cannot outlive the pass it was enrolled for.\n`ticketValidity` — `faceTag` against a dated ticket.\n`operatingDayClose` — `faceTag` where the ticket has no end of its own, plus `VenueSettings.biometrics.faceTagPurgeMinutesAfterClose`.\n",
  "enum": [
   "entitlementValidity",
   "ticketValidity",
   "operatingDayClose"
  ]
 },
 "CreateResaleListingRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "Request only; persisted as `ResaleListing`. **What a seller decides**: which entitlement, and at what price. The id, the status, the fee snapshot and the partition key are the server's, which is why `createResaleListing` no longer takes the whole listing.\n",
  "required": [
   "entitlementId",
   "askPrice"
  ],
  "properties": {
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "askPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "sellerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The holder listing it. A guest caller is always the seller and may name only themselves; a member of staff listing on a guest's behalf names the guest."
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
 "FacePassEnrolment": {
  "type": "object",
  "x-ticvai-persistence": "pii.subject_biometric",
  "description": "3.2.43. **Metadata about a facial profile. Never the profile.**\n",
  "required": [
   "id",
   "kind",
   "subjectId",
   "entitlementId",
   "source",
   "capturedAt"
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
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "description": "The `Entitlement.id`, a UUIDv7 (`pii.subject_biometric.entitlement_id`)."
   },
   "kind": {
    "$ref": "#/components/schemas/BiometricKind"
   },
   "retentionAnchor": {
    "allOf": [
     {
      "$ref": "#/components/schemas/BiometricRetentionAnchor"
     }
    ],
    "x-ticvai-derived": "onWrite",
    "description": "BL-106. **Derived from `kind`, never sent.** `facePass` anchors to the entitlement, `faceTag` to the ticket or to the close of the operating day.\n"
   },
   "source": {
    "type": "string",
    "enum": [
     "guestApp",
     "ticketCounter",
     "annualPassCounter",
     "entryGate"
    ],
    "description": "**`entryGate` is valid for `faceTag` only**, and 3.2.43's omission of it from Face Pass is deliberate: an enduring enrolment is a considered act with consent attached, not something done in a queue. 3.2.44 puts a Face Tag at a gate precisely because it dies the same day.\n"
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
    "description": "**Bounded by whatever `retentionAnchor` names**, and a face outliving it is a biometric held for no stated purpose.\n**Settled 20 September by ADR-0047**, which CF-64 had been carrying since 6 August: a `facePass` cannot outlive its entitlement and a `faceTag` does not survive the close of the operating day. **These are ceilings rather than defaults** — they cannot be configured upward, because a retention that a tenant can extend without limit is the breach ADR-0047 gave the platform a ceiling to prevent.\n"
   }
  }
 },
 "GiftCard": {
  "x-ticvai-persistence": "wallet.gift_card",
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
 "PaymentToken": {
  "type": "object",
  "x-ticvai-persistence": "payments.token",
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
    "writeOnly": true,
    "description": "**Write-only, never returned.** The provider's reference to a credential it holds. Required on the stored row; absent from every response.\n"
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
  "description": "BL-060. **Smaller than it first looked** — most of the machinery exists. An entitlement can already be transferred, an order can already be created, and payment already routes. What was missing is the listing itself and a cart line that can point at one.\n**A resale is a transfer with money attached**, and the venue is in the middle: the buyer becomes the owner of the same entitlement (the virtual ticket ID is preserved, MoM 1 Sep 4.14), its media is re-issued and the transfer is logged, so **the media that admits is always one the venue issued.** That is what stops a screenshot at the gate.\n",
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
    "format": "uuid",
    "readOnly": true
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
    "readOnly": true,
    "description": "**A ceiling as a percentage of face value**, because uncapped resale is a venue watching its own tickets sold at four times the price with its name on them. Null means uncapped, which is a venue decision rather than a default. Snapshotted from `ResaleFeePolicy` at listing.\n"
   },
   "sellerFeePercent": {
    "type": "number",
    "readOnly": true,
    "description": "Snapshotted from `ResaleFeePolicy` at listing."
   },
   "buyerFeePercent": {
    "type": "number",
    "readOnly": true,
    "description": "Snapshotted from `ResaleFeePolicy` at listing."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "pendingReview",
     "listed",
     "reserved",
     "sold",
     "withdrawn",
     "expired",
     "rejected"
    ],
    "description": "`pendingReview` and `rejected` added 29 September (DM5): a listing the marketplace's `moderationMode` sends to review waits there until `approveListingModeration` lists or rejects it."
   },
   "listedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "soldToSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "reviewReasons": {
    "type": "array",
    "readOnly": true,
    "description": "Why the listing was sent to review (DM5, 29 September).",
    "items": {
     "type": "string",
     "enum": [
      "highResalePrice",
      "unusualDiscount",
      "highValueTicket",
      "vipTicket",
      "sellerRisk",
      "newSeller",
      "multipleListings",
      "identityIssue",
      "paymentIssue",
      "ticketOwnershipConcern",
      "fraudIndicator"
     ]
    }
   },
   "moderatedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "moderatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "moderationReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "readOnly": true
   },
   "payoutStatus": {
    "type": "string",
    "readOnly": true,
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
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 "WalletTransaction": {
  "x-ticvai-persistence": "wallet.wallet_transaction",
  "type": "object",
  "required": [
   "id",
   "kind",
   "amount",
   "balanceAfter",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "walletId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "wallet.wallet",
    "description": "The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "wallet.hold",
    "description": "The hold a spend settled, where it came through `holdWalletFunds`."
   },
   "kind": {
    "$ref": "#/components/schemas/WalletTransactionKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceAfter": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "orderId": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "principalId": {
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
 "WalletTransactionKind": {
  "type": "string",
  "enum": [
   "topUp",
   "spend",
   "refund",
   "adjustment",
   "bonus",
   "expiry",
   "transfer"
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
