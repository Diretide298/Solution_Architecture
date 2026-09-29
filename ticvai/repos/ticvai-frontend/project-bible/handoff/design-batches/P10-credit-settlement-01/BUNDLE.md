# P10-credit-settlement-01 — P10 · Credit & Settlement

**2 screens · 7 operations · 6 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `CREDIT_MANAGE, CREDIT_OVERRIDE, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-012` | Checkout / Credit Purchase | configEditor | 4 | 2 | — |
| `PTR-013` | Credit Limit & Balance | statusTracker | 3 | 2 | — |

## Thin screens in this batch

**PTR-013 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "PTR-012",
  "name": "Checkout / Credit Purchase",
  "module": "Credit & Settlement",
  "requiresModule": "partner",
  "wave": 2,
  "capability": "C04",
  "implementation": {
   "app": "partner-web",
   "route": "/general/checkout-credit-purchase",
   "component": "apps/partner-web/src/routes/general/CheckoutCreditPurchaseWizard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-002",
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId and PTR-012 holds orderId, so an edge into it carries them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-012 holds none of them, so the edge carries nothing and PTR-003 opens cold"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **The strongest multi-currency case in the platform.** A partner is billed in `PartnerAgreement.settlementCurrency`, which is often not the venue's — a UK operator selling a Dubai attraction is invoiced in GBP against sales booked in AED. **`creditLimit` is in the settlement currency**, so a limit in the wrong currency is a limit that moves with the exchange rate. Which rate converts the sale is `fxPolicy` and it is a commercial term, not a default.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`createPayment`, `addTip`, `capturePayment`) and no read of a population — it is settings, not a list",
  "purpose": "Take the money, and be unambiguous about whether it worked.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "CreatePaymentRequest.id",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "orderId",
       "bindsTo": "CreatePaymentRequest.orderId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "tender",
       "bindsTo": "CreatePaymentRequest.tender",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "amount",
       "bindsTo": "CreatePaymentRequest.amount",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "tenderedAmount",
       "bindsTo": "CreatePaymentRequest.tenderAmount",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "walletAuthorisationId",
       "bindsTo": "CreatePaymentRequest.walletAuthorisationId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "deviceId",
       "bindsTo": "CreatePaymentRequest.deviceId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "recordedAt",
       "bindsTo": "CreatePaymentRequest.recordedAt",
       "provenance": "contract orders.yaml POST /payments"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create payment",
       "operation": "createPayment",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "secondaryButton",
       "label": "Add tip",
       "operation": "addTip",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/tip"
      },
      {
       "kind": "secondaryButton",
       "label": "Capture payment",
       "operation": "capturePayment",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/capture"
      },
      {
       "kind": "secondaryButton",
       "label": "Inquire payment status",
       "operation": "inquirePaymentStatus",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/inquiry"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved checkout credit purchase.",
   "error": "Could not load. Names which read failed and leaves the checkout credit purchase untouched.",
   "emptyFirstRun": "No checkout credit purchase configured. The form opens empty and `createPayment` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_CREATE`, which `createPayment` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createPayment",
    "contract": "orders",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "addTip",
    "contract": "orders",
    "purpose": "Record a tip against a payment",
    "trigger": "onAction"
   },
   {
    "operationId": "capturePayment",
    "contract": "orders",
    "purpose": "Capture a previously authorised payment",
    "trigger": "onAction"
   },
   {
    "operationId": "inquirePaymentStatus",
    "contract": "orders",
    "purpose": "Ask the provider what actually happened",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "paymentId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `paymentId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-012"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAddTip",
    "component": "modal",
    "trigger": "Add tip",
    "body": "**Collects what `addTip` sends before it is called.** Required: `amount`, `source`, `recordedAt`. Optional: `allocateToPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add tip",
     "operation": "addTip"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount",
      "source",
      "recordedAt",
      "allocateToPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /payments/{paymentId}/tip"
   },
   {
    "id": "formCapturePayment",
    "component": "modal",
    "trigger": "Capture payment",
    "body": "**Collects what `capturePayment` sends before it is called.** Required: `amount`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Capture payment",
     "operation": "capturePayment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount"
     ]
    },
    "provenance": "contract orders.yaml POST /payments/{paymentId}/capture"
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
  "id": "PTR-013",
  "name": "Credit Limit & Balance",
  "module": "Credit & Settlement",
  "requiresModule": "partner",
  "wave": 2,
  "capability": "C34",
  "implementation": {
   "app": "partner-web",
   "route": "/general/credit-limit-and-balance",
   "component": "apps/partner-web/src/routes/general/CreditLimitAndBalanceDetail.tsx",
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
      "accountId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, challengeId and PTR-013 holds accountId, so an edge into it carries them"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "accountId",
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId and PTR-013 holds accountId, orderId, so an edge into it carries them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-013 holds none of them, so the edge carries nothing and PTR-003 opens cold"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getB2bCredit` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See credit limit & balance for this venue.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
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
       "kind": "destructiveButton",
       "label": "Override credit limit",
       "operation": "overrideCreditLimit",
       "provenance": "contract orders.yaml POST /b2b-accounts/{accountId}/credit/override"
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
    "id": "confirmOverrideCreditLimit",
    "component": "confirmDialog",
    "trigger": "Override credit limit",
    "body": "**Names what `overrideCreditLimit` changes and what it leaves alone**, in the consequence rather than the verb. A credit limit balance this affects should be identified in the dialog, not just counted. **Collects what `overrideCreditLimit` sends before it is called.** Required: `orderId`, `amount`, `reason`. Optional: `expiresAt`.",
    "provenance": "contract orders.yaml POST /b2b-accounts/{accountId}/credit/override"
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
   "loading": "The credit limit balance, read by `getB2bCredit`.",
   "error": "Could not load. Names which read failed and leaves the credit limit balance untouched.",
   "emptyFirstRun": "No credit limit balance yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getB2bCredit` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getB2bCredit",
    "contract": "orders",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "overrideCreditLimit",
    "contract": "orders",
    "purpose": "Authorise an order beyond the credit limit",
    "trigger": "onAction"
   },
   {
    "operationId": "setB2bCreditLimit",
    "contract": "orders",
    "purpose": "Set a partner credit limit",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "accountId",
     "from": "PTR-001"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-013"
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
 "addTip": {
  "method": "POST",
  "path": "/payments/{paymentId}/tip",
  "contract": "orders",
  "summary": "Record a tip against a payment",
  "permission": "ORDER_MODIFY",
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
  "responds": "Payment"
 },
 "capturePayment": {
  "method": "POST",
  "path": "/payments/{paymentId}/capture",
  "contract": "orders",
  "summary": "Capture a previously authorised payment",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Payment"
 },
 "createPayment": {
  "method": "POST",
  "path": "/payments",
  "contract": "orders",
  "summary": "Take a payment against an order",
  "permission": "ORDER_CREATE",
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
  "requestBody": "CreatePaymentRequest",
  "responds": "Payment"
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
 "inquirePaymentStatus": {
  "method": "POST",
  "path": "/payments/{paymentId}/inquiry",
  "contract": "orders",
  "summary": "Ask the provider what actually happened",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Payment"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "ExchangeRateDecimal": {
  "type": "string",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,6)",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n",
  "pattern": "^\\d+(\\.\\d{1,6})?$"
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
 "TenderKind": {
  "type": "string",
  "description": "`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n",
  "enum": [
   "cash",
   "card",
   "wallet",
   "voucher",
   "bankTransfer",
   "hotelCharge",
   "installment",
   "giftCard",
   "complimentary"
  ]
 }
}
```
