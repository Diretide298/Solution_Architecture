# P10-credit-settlement-01 — P10 · Credit & Settlement

**2 screens · 7 operations · 4 schemas · 5 permissions**

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
- **2 of these operations work offline**: addTip, createPayment
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-012` | Checkout / Credit Purchase | configEditor | 4 | 0 | — |
| `PTR-013` | Credit Limit & Balance | statusTracker | 3 | 1 | — |

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
       "bindsTo": "CreatePaymentRequest.tenderedAmount",
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
       "label": "Create",
       "operation": "createPayment",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "secondaryButton",
       "label": "Add",
       "operation": "addTip",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/tip"
      },
      {
       "kind": "secondaryButton",
       "label": "Capture",
       "operation": "capturePayment",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/capture"
      },
      {
       "kind": "secondaryButton",
       "label": "Inquire",
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
   "emptyFirstRun": "No checkout credit purchase configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createPayment",
    "contract": "orders",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
       "label": "The selected credit limit balance",
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
       "label": "Override",
       "operation": "overrideCreditLimit",
       "provenance": "contract orders.yaml POST /b2b-accounts/{accountId}/credit/override"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setB2bCreditLimit",
       "provenance": "contract orders.yaml PUT /b2b-accounts/{accountId}/credit"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "overrideCreditLimit",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmOverrideCreditLimit",
    "component": "confirmDialog",
    "trigger": "Override",
    "body": "**Names what `overrideCreditLimit` changes and what it leaves alone**, in the consequence rather than the verb. A credit limit balance this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml POST /b2b-accounts/{accountId}/credit/override"
   }
  ],
  "states": {
   "loading": "The credit limit balance list.",
   "error": "Could not load. Names which read failed and leaves the credit limit balance untouched.",
   "emptyFirstRun": "No credit limit balance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credit limit balance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderedAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Cash only. Change is the difference."
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
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
 "TenderKind": {
  "type": "string",
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
