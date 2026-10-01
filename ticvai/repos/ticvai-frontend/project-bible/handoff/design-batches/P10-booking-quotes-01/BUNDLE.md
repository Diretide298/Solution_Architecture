# P10-booking-quotes-01 — P10 · Booking & Quotes

**4 screens · 32 operations · 49 schemas · 14 permissions**

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

- **Every control that can be refused must be gated.** 14 permissions apply here:
  `CAPACITY_CONFIGURE, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW, ORDER_VOID, PARTNER_MANAGE, PARTNER_VIEW`…. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-008` | Booking Creation | listDetail | 14 | 9 | — |
| `PTR-009` | Group / Bulk Booking | listDetail | 4 | 3 | — |
| `PTR-010` | Cart & Quote | listDetail | 10 | 5 | — |
| `PTR-011` | Quote Management | listDetail | 4 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "PTR-008",
  "name": "Booking Creation",
  "module": "Booking & Quotes",
  "requiresModule": "partner",
  "wave": 2,
  "capability": "C02",
  "implementation": {
   "app": "partner-web",
   "route": "/general/booking-creation",
   "component": "apps/partner-web/src/routes/general/BookingCreationForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001",
    "PTR-007"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-002",
    "PTR-003",
    "PTR-016"
   ],
   "flowDerived": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId and PTR-008 holds orderId, so an edge into it carries them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-008 holds none of them. The edge carries nothing: PTR-003 needs nothing to open"
    },
    {
     "to": "SCN-003",
     "trigger": "A customer arrives and is admitted",
     "provenance": "flow F10 step 3→4",
     "operation": "listOrders",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "PTR-016",
     "trigger": "Downloads vouchers",
     "provenance": "flow F03 step 3→4",
     "operation": "createOrder",
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: SCN-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Add booking creation for this venue.",
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
       "operation": "listOrders",
       "notes": "Sends `?venueId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listOrders",
       "notes": "Sends `?principalId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listOrders",
       "notes": "Sends `?shiftId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listOrders",
       "notes": "Sends `?status=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created from",
       "operation": "listOrders",
       "notes": "Sends `?createdFrom=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created to",
       "operation": "listOrders",
       "notes": "Sends `?createdTo=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
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
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every refund",
       "bindsTo": "Refund",
       "columns": [
        "Refund.id",
        "Refund.orderId",
        "Refund.batchId",
        "Refund.fxRate",
        "Refund.taxReversalEntryId",
        "Refund.settleTo",
        "Refund.fxVariance",
        "Refund.amount",
        "Refund.appliedPercentage",
        "Refund.status",
        "Refund.reason",
        "Refund.requestedByPrincipalId"
       ],
       "operation": "listOrderRefunds",
       "provenance": "contract orders.yaml GET /orders/{orderId}/refunds"
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
      },
      {
       "kind": "detailPanel",
       "label": "The order statement",
       "bindsTo": "OrderStatement",
       "columns": [
        "OrderStatement.orderId",
        "OrderStatement.orderNumber",
        "OrderStatement.currency",
        "OrderStatement.currencyScale",
        "OrderStatement.entries",
        "OrderStatement.totalPaid",
        "OrderStatement.totalRefunded",
        "OrderStatement.currentBalance"
       ],
       "operation": "getOrderStatement",
       "provenance": "contract orders.yaml GET /orders/{orderId}/statement"
      },
      {
       "kind": "detailPanel",
       "label": "The order",
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
       "label": "Create order",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply manual discount",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create refund",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange order lines",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold order",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify order",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint order",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule order",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume order",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Void order",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void order",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A booking creation this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`.",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   },
   {
    "id": "formCreateOrder",
    "component": "modal",
    "trigger": "Create order",
    "body": "**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateOrderRequest",
    "confirm": {
     "label": "Create order",
     "operation": "createOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "channel",
      "lines",
      "recordedAt",
      "shiftId",
      "subjectId",
      "guestLinkId",
      "catalogueBundleVersion"
     ]
    },
    "provenance": "contract orders.yaml POST /orders"
   },
   {
    "id": "formApplyManualDiscount",
    "component": "modal",
    "trigger": "Apply manual discount",
    "body": "**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ManualDiscountRequest",
    "confirm": {
     "label": "Apply manual discount",
     "operation": "applyManualDiscount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "lineId",
      "amount",
      "percentage",
      "reasonCode",
      "approverPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
   },
   {
    "id": "formCreateRefund",
    "component": "modal",
    "trigger": "Create refund",
    "body": "**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateRefundRequest",
    "confirm": {
     "label": "Create refund",
     "operation": "createRefund"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "amount",
      "reason",
      "recordedAt",
      "lineIds",
      "secondaryAuthorisation",
      "refundToOriginalTender",
      "alternateTender"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
   },
   {
    "id": "formExchangeOrderLines",
    "component": "modal",
    "trigger": "Exchange order lines",
    "body": "**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ExchangeOrderRequest",
    "confirm": {
     "label": "Exchange order lines",
     "operation": "exchangeOrderLines"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outgoingLineIds",
      "incomingLines",
      "recordedAt",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
   },
   {
    "id": "formHoldOrder",
    "component": "modal",
    "trigger": "Hold order",
    "body": "**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold order",
     "operation": "holdOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "label",
      "holdUntil"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
   },
   {
    "id": "formModifyOrder",
    "component": "modal",
    "trigger": "Modify order",
    "body": "**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ModifyOrderRequest",
    "confirm": {
     "label": "Modify order",
     "operation": "modifyOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "recordedAt",
      "addLines",
      "removeLineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
   },
   {
    "id": "formReprintOrder",
    "component": "modal",
    "trigger": "Reprint order",
    "body": "**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reprint order",
     "operation": "reprintOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "delivery",
      "recordedAt",
      "destination",
      "lineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
   },
   {
    "id": "formRescheduleOrder",
    "component": "modal",
    "trigger": "Reschedule order",
    "body": "**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reschedule order",
     "operation": "rescheduleOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetPerformanceId",
      "recordedAt",
      "lineIds",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
   }
  ],
  "states": {
   "loading": "The booking creation list.",
   "error": "Could not load. Names which read failed and leaves the booking creation untouched.",
   "emptyFirstRun": "No booking creation yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the booking creation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "applyManualDiscount",
    "contract": "orders",
    "purpose": "Apply a discount a cashier chose",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "createRefund",
    "contract": "orders",
    "purpose": "Refund an order, wholly or in part",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onAction"
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onAction"
   },
   {
    "operationId": "holdOrder",
    "contract": "orders",
    "purpose": "Park a sale and free the till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "modifyOrder",
    "contract": "orders",
    "purpose": "Add or remove lines on an existing order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move an order to another performance",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "resumeOrder",
    "contract": "orders",
    "purpose": "Bring a parked sale back to a till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
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
    "OrderSummary.id",
    "OrderSummary.orderNumber",
    "OrderSummary.status",
    "OrderSummary.grossAmount",
    "OrderSummary.refundedAmount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 14 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "PTR-009",
  "name": "Group / Bulk Booking",
  "module": "Booking & Quotes",
  "requiresModule": "partner",
  "wave": 3,
  "capability": "C54",
  "implementation": {
   "app": "partner-web",
   "route": "/general/group-bulk-booking",
   "component": "apps/partner-web/src/routes/general/GroupBulkBookingDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-009 holds none of them. The edge carries nothing: PTR-003 needs nothing to open"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 26 August** — `Seat Board 3.dc.html` frame `seat-3d`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 3.dc.html#seat-3d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSeatBlocks` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Work with group / bulk booking for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Performance id",
       "operation": "listSeatBlocks",
       "notes": "Sends `?performanceId=` to `listSeatBlocks`.",
       "provenance": "contract seating.yaml GET /seat-blocks"
      },
      {
       "kind": "textField",
       "label": "Reason",
       "operation": "listSeatBlocks",
       "notes": "Sends `?reason=` to `listSeatBlocks`.",
       "provenance": "contract seating.yaml GET /seat-blocks"
      },
      {
       "kind": "dataTable",
       "label": "Every seat block",
       "bindsTo": "SeatBlock",
       "columns": [
        "SeatBlock.id",
        "SeatBlock.performanceId",
        "SeatBlock.seatIds",
        "SeatBlock.reason",
        "SeatBlock.note",
        "SeatBlock.createdByPrincipalId",
        "SeatBlock.releaseAt",
        "SeatBlock.releasedAt",
        "SeatBlock.scopePath"
       ],
       "operation": "listSeatBlocks",
       "provenance": "contract seating.yaml GET /seat-blocks"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
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
       "label": "The selected seat block",
       "bindsTo": "SeatBlock",
       "columns": [
        "SeatBlock.id",
        "SeatBlock.performanceId",
        "SeatBlock.seatIds",
        "SeatBlock.reason",
        "SeatBlock.note",
        "SeatBlock.createdByPrincipalId",
        "SeatBlock.releaseAt",
        "SeatBlock.releasedAt",
        "SeatBlock.scopePath"
       ],
       "operation": "listSeatBlocks",
       "provenance": "contract seating.yaml GET /seat-blocks"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Allocate blocked seats",
       "operation": "allocateBlockedSeats",
       "provenance": "contract seating.yaml POST /seat-blocks/{blockId}/allocate"
      },
      {
       "kind": "secondaryButton",
       "label": "Create seat block",
       "operation": "createSeatBlock",
       "provenance": "contract seating.yaml POST /seat-blocks"
      },
      {
       "kind": "secondaryButton",
       "label": "Release seat block",
       "operation": "relinquishSeatBlock",
       "provenance": "contract seating.yaml DELETE /seat-blocks/{blockId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group bulk booking list.",
   "error": "Could not load. Names which read failed and leaves the group bulk booking untouched.",
   "emptyFirstRun": "No group bulk booking yet. Offers Create seat block (`createSeatBlock`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on performanceId, reason and the group bulk booking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listSeatBlocks` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "allocateBlockedSeats",
    "contract": "seating",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "createSeatBlock",
    "contract": "seating",
    "purpose": "Block seats from sale",
    "trigger": "onAction",
    "invalidates": [
     "listSeatBlocks"
    ]
   },
   {
    "operationId": "listSeatBlocks",
    "contract": "seating",
    "purpose": "List seat blocks",
    "trigger": "onLoad"
   },
   {
    "operationId": "relinquishSeatBlock",
    "contract": "seating",
    "purpose": "Release a block back to sale",
    "trigger": "onAction",
    "invalidates": [
     "listSeatBlocks"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "blockId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `blockId`.",
   "preloaded": [
    "SeatBlock.id",
    "SeatBlock.performanceId",
    "SeatBlock.seatIds",
    "SeatBlock.reason",
    "SeatBlock.note"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-009",
   "derivedFrom": "wireframes/reference/Seat Board 3.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAllocateBlockedSeats",
    "component": "modal",
    "trigger": "Allocate blocked seats",
    "body": "**Collects what `allocateBlockedSeats` sends before it is called.** Required: `seatIds`. Optional: `subjectId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Allocate blocked seats",
     "operation": "allocateBlockedSeats"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "seatIds",
      "subjectId",
      "note"
     ]
    },
    "provenance": "contract seating.yaml POST /seat-blocks/{blockId}/allocate"
   },
   {
    "id": "formCreateSeatBlock",
    "component": "modal",
    "trigger": "Create seat block",
    "body": "**Collects what `createSeatBlock` sends before it is called.** Required: `performanceId`, `seatIds`, `reason`, `note`. Optional: `releaseAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateSeatBlockRequest",
    "confirm": {
     "label": "Create seat block",
     "operation": "createSeatBlock"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "performanceId",
      "seatIds",
      "reason",
      "note",
      "releaseAt"
     ]
    },
    "provenance": "contract seating.yaml POST /seat-blocks"
   },
   {
    "id": "formRelinquishSeatBlock",
    "component": "modal",
    "trigger": "Release seat block",
    "body": "**Collects what `relinquishSeatBlock` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Release seat block",
     "operation": "relinquishSeatBlock"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract seating.yaml DELETE /seat-blocks/{blockId}"
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
  "id": "PTR-010",
  "name": "Cart & Quote",
  "module": "Booking & Quotes",
  "requiresModule": "partner",
  "wave": 3,
  "capability": "C02",
  "implementation": {
   "app": "partner-web",
   "route": "/general/cart-and-quote",
   "component": "apps/partner-web/src/routes/general/CartAndQuoteDetail.tsx",
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
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId and PTR-010 holds orderId, so an edge into it carries them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-010 holds none of them. The edge carries nothing: PTR-003 needs nothing to open"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPromotions` reads the population and `getPromotion` reads one of them — list, select, act",
  "purpose": "Work with cart & quote for this venue.",
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
       "operation": "listPromotions",
       "notes": "Sends `?venueId=` to `listPromotions`.",
       "provenance": "contract promotions.yaml GET /promotions"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listPromotions",
       "notes": "Sends `?status=` to `listPromotions`.",
       "provenance": "contract promotions.yaml GET /promotions"
      },
      {
       "kind": "datePicker",
       "label": "Active at",
       "operation": "listPromotions",
       "notes": "Sends `?activeAt=` to `listPromotions`.",
       "provenance": "contract promotions.yaml GET /promotions"
      },
      {
       "kind": "dataTable",
       "label": "Every promotion",
       "bindsTo": "Promotion",
       "columns": [
        "Promotion.code",
        "Promotion.name",
        "Promotion.description",
        "Promotion.venueId",
        "Promotion.discount",
        "Promotion.conditions",
        "Promotion.stackingMode",
        "Promotion.stackingGroup",
        "Promotion.precedence",
        "Promotion.validFrom",
        "Promotion.validTo",
        "Promotion.maxRedemptions"
       ],
       "operation": "listPromotions",
       "provenance": "contract promotions.yaml GET /promotions"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
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
       "label": "The selected promotion",
       "bindsTo": "Promotion",
       "columns": [
        "Promotion.code",
        "Promotion.name",
        "Promotion.description",
        "Promotion.venueId",
        "Promotion.discount",
        "Promotion.conditions",
        "Promotion.stackingMode",
        "Promotion.stackingGroup",
        "Promotion.precedence",
        "Promotion.validFrom",
        "Promotion.validTo",
        "Promotion.maxRedemptions",
        "Promotion.maxRedemptionsPerGuest",
        "Promotion.budgetCap",
        "Promotion.id",
        "Promotion.status"
       ],
       "operation": "getPromotion",
       "provenance": "contract promotions.yaml GET /promotions/{promotionId}"
      },
      {
       "kind": "detailPanel",
       "label": "The promotion usage",
       "bindsTo": "PromotionUsage",
       "columns": [
        "PromotionUsage.promotionId",
        "PromotionUsage.redemptionCount",
        "PromotionUsage.discountGiven",
        "PromotionUsage.budgetCap",
        "PromotionUsage.budgetRemaining",
        "PromotionUsage.isBudgetExhausted",
        "PromotionUsage.byChannel"
       ],
       "operation": "getPromotionUsage",
       "provenance": "contract promotions.yaml GET /promotions/{promotionId}/usage"
      },
      {
       "kind": "detailPanel",
       "label": "The cart",
       "bindsTo": "Cart",
       "columns": [
        "Cart.id",
        "Cart.token",
        "Cart.venueId",
        "Cart.channel",
        "Cart.subjectId",
        "Cart.status",
        "Cart.lines",
        "Cart.conflicts",
        "Cart.subtotal",
        "Cart.discountTotal",
        "Cart.taxTotal",
        "Cart.total",
        "Cart.appliedPromotionIds",
        "Cart.expiresAt",
        "Cart.extensionsUsed",
        "Cart.maxExtensions"
       ],
       "operation": "getCart",
       "provenance": "contract orders.yaml GET /carts/{cartId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Evaluate promotions",
       "operation": "evaluatePromotions",
       "provenance": "contract promotions.yaml POST /promotions/evaluate"
      },
      {
       "kind": "secondaryButton",
       "label": "Analyse promotion conflicts",
       "operation": "analysePromotionConflicts",
       "provenance": "contract promotions.yaml GET /promotions/{promotionId}/conflicts"
      },
      {
       "kind": "secondaryButton",
       "label": "Add cart line",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Save cart line",
       "operation": "updateCartLine",
       "provenance": "contract orders.yaml PATCH /carts/{cartId}/lines/{lineId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove cart line",
       "operation": "removeCartLine",
       "provenance": "contract orders.yaml DELETE /carts/{cartId}/lines/{lineId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Checkout cart",
       "operation": "checkoutCart",
       "provenance": "contract orders.yaml POST /carts/{cartId}/checkout"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveCartLine",
    "component": "confirmDialog",
    "trigger": "Remove cart line",
    "body": "**Names what `removeCartLine` changes and what it leaves alone**, in the consequence rather than the verb. A cart quote this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml DELETE /carts/{cartId}/lines/{lineId}"
   },
   {
    "id": "formEvaluatePromotions",
    "component": "modal",
    "trigger": "Evaluate promotions",
    "body": "**Collects what `evaluatePromotions` sends before it is called.** Required: `venueId`, `channel`, `lines`. Optional: `subjectId`, `membershipTierId`, `couponCodes`, `evaluateAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "EvaluatePromotionsRequest",
    "confirm": {
     "label": "Evaluate promotions",
     "operation": "evaluatePromotions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "channel",
      "lines",
      "subjectId",
      "membershipTierId",
      "couponCodes",
      "evaluateAt"
     ]
    },
    "provenance": "contract promotions.yaml POST /promotions/evaluate"
   },
   {
    "id": "formAddCartLine",
    "component": "modal",
    "trigger": "Add cart line",
    "body": "**Collects what `addCartLine` sends before it is called.** Required: `variantId`, `quantity`. Optional: `performanceId`, `seatIds`, `parentLineId`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AddCartLineRequest",
    "confirm": {
     "label": "Add cart line",
     "operation": "addCartLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "variantId",
      "quantity",
      "performanceId",
      "seatIds",
      "parentLineId",
      "attributes"
     ]
    },
    "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
   },
   {
    "id": "formUpdateCartLine",
    "component": "modal",
    "trigger": "Save cart line",
    "body": "**Collects what `updateCartLine` sends before it is called.** Required: `quantity`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save cart line",
     "operation": "updateCartLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "quantity"
     ]
    },
    "provenance": "contract orders.yaml PATCH /carts/{cartId}/lines/{lineId}"
   },
   {
    "id": "formCheckoutCart",
    "component": "modal",
    "trigger": "Checkout cart",
    "body": "**Collects what `checkoutCart` sends before it is called.** Nothing in the body is required. Optional: `subjectId`, `attendees`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Checkout cart",
     "operation": "checkoutCart"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "subjectId",
      "attendees"
     ]
    },
    "provenance": "contract orders.yaml POST /carts/{cartId}/checkout"
   }
  ],
  "states": {
   "loading": "The cart quote list.",
   "error": "Could not load. Names which read failed and leaves the cart quote untouched.",
   "emptyFirstRun": "No cart quote yet. Offers Add cart line (`addCartLine`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, status, activeAt and the cart quote are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRICE_VIEW`, which `getPromotion` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "evaluatePromotions",
    "contract": "promotions",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "analysePromotionConflicts",
    "contract": "promotions",
    "purpose": "Analyse stacking against live promotions",
    "trigger": "onAction"
   },
   {
    "operationId": "getPromotion",
    "contract": "promotions",
    "purpose": "Read a promotion",
    "trigger": "onAction"
   },
   {
    "operationId": "getPromotionUsage",
    "contract": "promotions",
    "purpose": "Redemption count and discount given",
    "trigger": "onAction"
   },
   {
    "operationId": "listPromotions",
    "contract": "promotions",
    "purpose": "List promotions",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCart",
    "contract": "orders",
    "purpose": "The cart, priced and checked, right now",
    "trigger": "onLoad"
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "updateCartLine",
    "contract": "orders",
    "purpose": "Change a quantity",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "removeCartLine",
    "contract": "orders",
    "purpose": "Take something out",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "checkoutCart",
    "contract": "orders",
    "purpose": "Turn the cart into an order",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    },
    {
     "name": "lineId",
     "from": "deepLink"
    },
    {
     "name": "promotionId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `lineId`, `promotionId`.",
   "preloaded": [
    "Promotion.code",
    "Promotion.name",
    "Promotion.description",
    "Promotion.venueId",
    "Promotion.discount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-010"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "PTR-011",
  "name": "Quote Management",
  "module": "Booking & Quotes",
  "requiresModule": "partner",
  "wave": 3,
  "implementation": {
   "app": "partner-web",
   "route": "/general/quote-management",
   "component": "apps/partner-web/src/routes/general/QuoteManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-011 holds none of them. The edge carries nothing: PTR-003 needs nothing to open"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — quotes are procurement-side only"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPartnerAgreements` reads the population and `getCommissionStatement` reads one of them — list, select, act",
  "purpose": "Find quote management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "numberField",
       "label": "Expiring within days",
       "operation": "listPartnerAgreements",
       "notes": "Sends `?expiringWithinDays=` to `listPartnerAgreements`.",
       "provenance": "contract subscription.yaml GET /partner-agreements"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listPartnerAgreements",
       "notes": "Sends `?status=` to `listPartnerAgreements`.",
       "provenance": "contract subscription.yaml GET /partner-agreements"
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
      },
      {
       "kind": "dataTable",
       "label": "Every partner quote",
       "bindsTo": "PartnerQuote",
       "columns": [
        "PartnerQuote.id",
        "PartnerQuote.partnerId",
        "PartnerQuote.agreementId",
        "PartnerQuote.currency",
        "PartnerQuote.totalMinor",
        "PartnerQuote.state",
        "PartnerQuote.validUntil"
       ],
       "operation": "listPartnerQuotes",
       "provenance": "contract subscription.yaml GET /partner-quotes"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner agreement",
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
        "PartnerAgreement.storefrontSubdomain",
        "PartnerAgreement.sponsorship",
        "PartnerAgreement.netRates",
        "PartnerAgreement.creditTermDays",
        "PartnerAgreement.acceptedByPrincipalId"
       ],
       "operation": "listPartnerAgreements",
       "provenance": "contract subscription.yaml GET /partner-agreements"
      },
      {
       "kind": "detailPanel",
       "label": "The commission statement",
       "bindsTo": "CommissionStatement",
       "columns": [
        "CommissionStatement.agreementId",
        "CommissionStatement.partnerName",
        "CommissionStatement.from",
        "CommissionStatement.to",
        "CommissionStatement.currency",
        "CommissionStatement.grossSales",
        "CommissionStatement.refunds",
        "CommissionStatement.netSales",
        "CommissionStatement.commissionEarned",
        "CommissionStatement.amountDue",
        "CommissionStatement.lines"
       ],
       "operation": "getCommissionStatement",
       "provenance": "contract subscription.yaml GET /partner-agreements/{agreementId}/commission-statement"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create partner quote",
       "operation": "createPartnerQuote",
       "provenance": "contract subscription.yaml POST /partner-quotes"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The quote list.",
   "error": "Could not load. Names which read failed and leaves the quote untouched.",
   "emptyFirstRun": "No quote yet. Offers Create partner quote (`createPartnerQuote`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on expiringWithinDays, status and the quote are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PARTNER_MANAGE`, which `listPartnerAgreements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerAgreements",
    "contract": "subscription",
    "purpose": "Commercial agreements with B2B partners",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCommissionStatement",
    "contract": "subscription",
    "purpose": "What the partner earned and what is owed",
    "trigger": "onAction"
   },
   {
    "operationId": "listPartnerQuotes",
    "contract": "subscription",
    "purpose": "Quotes offered to this partner",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPartnerQuote",
    "contract": "subscription",
    "purpose": "Raise a quote",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerAgreements"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "agreementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `agreementId`.",
   "preloaded": [
    "PartnerAgreement.id",
    "PartnerAgreement.partnerId",
    "PartnerAgreement.partnerName",
    "PartnerAgreement.status",
    "PartnerAgreement.rateMode"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-011"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreatePartnerQuote",
    "component": "modal",
    "trigger": "Create partner quote",
    "body": "**Collects what `createPartnerQuote` sends before it is called.** Required: `id`. Optional: `partnerId`, `agreementId`, `currency`, `totalMinor`, `state`, `validUntil`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerQuote",
    "confirm": {
     "label": "Create partner quote",
     "operation": "createPartnerQuote"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "partnerId",
      "agreementId",
      "currency",
      "totalMinor",
      "state",
      "validUntil"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-quotes"
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "addCartLine": {
  "method": "POST",
  "path": "/carts/{cartId}/lines",
  "contract": "orders",
  "summary": "Add something",
  "permission": null,
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
  "requestBody": "AddCartLineRequest",
  "responds": "Cart"
 },
 "allocateBlockedSeats": {
  "method": "POST",
  "path": "/seat-blocks/{blockId}/allocate",
  "contract": "seating",
  "summary": "Issue seats from a block to a group",
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
  "responds": "SeatHold"
 },
 "analysePromotionConflicts": {
  "method": "GET",
  "path": "/promotions/{promotionId}/conflicts",
  "contract": "promotions",
  "summary": "Analyse stacking against live promotions",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConflictAnalysis"
 },
 "applyManualDiscount": {
  "method": "POST",
  "path": "/orders/{orderId}/discounts",
  "contract": "orders",
  "summary": "Apply a discount a cashier chose",
  "permission": "ORDER_DISCOUNT",
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
  "requestBody": "ManualDiscountRequest",
  "responds": "Order"
 },
 "checkoutCart": {
  "method": "POST",
  "path": "/carts/{cartId}/checkout",
  "contract": "orders",
  "summary": "Turn the cart into an order",
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
  "responds": "Order"
 },
 "createOrder": {
  "method": "POST",
  "path": "/orders",
  "contract": "orders",
  "summary": "Create an order",
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
  "requestBody": "CreateOrderRequest",
  "responds": "Order"
 },
 "createPartnerQuote": {
  "method": "POST",
  "path": "/partner-quotes",
  "contract": "subscription",
  "summary": "Raise a quote",
  "permission": "PARTNER_MANAGE",
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
  "requestBody": "PartnerQuote",
  "responds": "PartnerQuote"
 },
 "createRefund": {
  "method": "POST",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "Refund an order, wholly or in part",
  "permission": "ORDER_REFUND",
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
  "requestBody": "CreateRefundRequest",
  "responds": null
 },
 "createSeatBlock": {
  "method": "POST",
  "path": "/seat-blocks",
  "contract": "seating",
  "summary": "Block seats from sale",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "CreateSeatBlockRequest",
  "responds": "SeatBlock"
 },
 "evaluatePromotions": {
  "method": "POST",
  "path": "/promotions/evaluate",
  "contract": "promotions",
  "summary": "Evaluate promotions against a cart",
  "permission": "PRICE_VIEW",
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
  "requestBody": "EvaluatePromotionsRequest",
  "responds": "PromotionEvaluation"
 },
 "exchangeOrderLines": {
  "method": "POST",
  "path": "/orders/{orderId}/exchanges",
  "contract": "orders",
  "summary": "Exchange lines for different products or dates",
  "permission": "ORDER_EXCHANGE",
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
  "requestBody": "ExchangeOrderRequest",
  "responds": "OrderExchangeResult"
 },
 "getCart": {
  "method": "GET",
  "path": "/carts/{cartId}",
  "contract": "orders",
  "summary": "The cart, priced and checked, right now",
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
  "responds": "Cart"
 },
 "getCommissionStatement": {
  "method": "GET",
  "path": "/partner-agreements/{agreementId}/commission-statement",
  "contract": "subscription",
  "summary": "What the partner earned and what is owed",
  "permission": "PARTNER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CommissionStatement"
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
 "getOrderStatement": {
  "method": "GET",
  "path": "/orders/{orderId}/statement",
  "contract": "orders",
  "summary": "Full financial history of an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderStatement"
 },
 "getPromotion": {
  "method": "GET",
  "path": "/promotions/{promotionId}",
  "contract": "promotions",
  "summary": "Read a promotion",
  "permission": "PRICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Promotion"
 },
 "getPromotionUsage": {
  "method": "GET",
  "path": "/promotions/{promotionId}/usage",
  "contract": "promotions",
  "summary": "Redemption count and discount given",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionUsage"
 },
 "holdOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/hold",
  "contract": "orders",
  "summary": "Park a sale and free the till",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "workstation",
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
 "listOrderRefunds": {
  "method": "GET",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "List refunds against an order",
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
 "listPartnerQuotes": {
  "method": "GET",
  "path": "/partner-quotes",
  "contract": "subscription",
  "summary": "Quotes offered to this partner",
  "permission": "PARTNER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerQuote"
 },
 "listPromotions": {
  "method": "GET",
  "path": "/promotions",
  "contract": "promotions",
  "summary": "List promotions",
  "permission": "PRICE_VIEW",
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
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 "listSeatBlocks": {
  "method": "GET",
  "path": "/seat-blocks",
  "contract": "seating",
  "summary": "List seat blocks",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": null
   },
   {
    "name": "reason",
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
 "modifyOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/modify",
  "contract": "orders",
  "summary": "Add or remove lines on an existing order",
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
  "requestBody": "ModifyOrderRequest",
  "responds": "OrderModificationResult"
 },
 "relinquishSeatBlock": {
  "method": "DELETE",
  "path": "/seat-blocks/{blockId}",
  "contract": "seating",
  "summary": "Release a block back to sale",
  "permission": "CAPACITY_CONFIGURE",
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
 "removeCartLine": {
  "method": "DELETE",
  "path": "/carts/{cartId}/lines/{lineId}",
  "contract": "orders",
  "summary": "Take something out",
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
  "responds": "Cart"
 },
 "reprintOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reprints",
  "contract": "orders",
  "summary": "Reprint or resend tickets",
  "permission": "ORDER_REPRINT",
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
  "responds": null
 },
 "rescheduleOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reschedule",
  "contract": "orders",
  "summary": "Move an order to another performance",
  "permission": "ORDER_RESCHEDULE",
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
  "responds": "OrderExchangeResult"
 },
 "resumeOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/resume",
  "contract": "orders",
  "summary": "Bring a parked sale back to a till",
  "permission": "ORDER_MODIFY",
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
  "responds": "OrderResumeResult"
 },
 "updateCartLine": {
  "method": "PATCH",
  "path": "/carts/{cartId}/lines/{lineId}",
  "contract": "orders",
  "summary": "Change a quantity",
  "permission": null,
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
  "responds": "Cart"
 },
 "voidOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/voids",
  "contract": "orders",
  "summary": "Void an order",
  "permission": "ORDER_VOID",
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
  "responds": "Order"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AddCartLineRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "variantId",
   "quantity"
  ],
  "properties": {
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"
   },
   "tableReservationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "description": "At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   }
  }
 },
 "BlockReason": {
  "type": "string",
  "description": "`other` is allowed only with a note (decided 28 September, audit R222). Every block already requires `note`, so an `other` block always says why; the notes are reviewed quarterly to add the real reasons they reveal.\n",
  "enum": [
   "productionHold",
   "houseSeats",
   "groupAllocation",
   "maintenance",
   "accessibilityReserve",
   "distancing",
   "other"
  ]
 },
 "BookedWindow": {
  "type": "object",
  "nullable": true,
  "x-ticvai-persistence": "none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line",
  "description": "**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n",
  "required": [
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "description": "After `startsAt`, on the same venue day."
   }
  }
 },
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
 "CartConflict": {
  "type": "object",
  "x-ticvai-persistence": "none — computed on read",
  "description": "2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "overlappingTime",
     "sameSessionDifferentVenue",
     "exceedsPartySize",
     "requiresPrerequisite",
     "consentBlocksBooking"
    ]
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "message": {
    "type": "string"
   },
   "isBlocking": {
    "type": "boolean",
    "description": "Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"
   }
  }
 },
 "CartLine": {
  "type": "object",
  "x-ticvai-persistence": "orders.cart_line",
  "required": [
   "id",
   "variantId",
   "quantity"
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
    "type": "string",
    "readOnly": true
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"
   },
   "tableReservationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"
   },
   "overridePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "priceMatch",
     "serviceRecovery",
     "negotiated",
     "damagedGoods",
     "staffSale",
     "error"
    ],
    "description": "BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"
   },
   "feeKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "booking",
     "transaction",
     "service",
     "delivery",
     "convenience",
     "cancellation"
    ],
    "description": "**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lineTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"
   },
   "leaseExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"
   },
   "isAvailable": {
    "type": "boolean",
    "readOnly": true,
    "description": "Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"
   }
  }
 },
 "CartStatus": {
  "type": "string",
  "enum": [
   "active",
   "expiring",
   "expired",
   "abandoned",
   "checkedOut"
  ]
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "CommissionStatement": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from orders and control.partner_agreement",
  "properties": {
   "agreementId": {
    "type": "string",
    "format": "uuid"
   },
   "partnerName": {
    "type": "string"
   },
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "currency": {
    "type": "string"
   },
   "grossSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refunds": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "commissionEarned": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "amountDue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lines": {
    "type": "array",
    "description": "**Reconcilable order by order.** A statement a partner cannot check line by line is a statement they will dispute, and the dispute costs more than the detail.\n",
    "items": {
     "type": "object",
     "properties": {
      "orderId": {
       "type": "string",
       "format": "uuid"
      },
      "orderNumber": {
       "type": "string"
      },
      "soldAt": {
       "type": "string",
       "format": "date-time"
      },
      "agreementVersion": {
       "type": "integer",
       "description": "The version in force at the time of that sale, not the current one."
      },
      "gross": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "commission": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "isRefunded": {
       "type": "boolean"
      }
     }
    }
   }
  }
 },
 "ConflictAnalysis": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "promotionId",
   "conflicts",
   "worstCaseDiscount"
  ],
  "properties": {
   "promotionId": {
    "type": "string",
    "format": "uuid"
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "otherPromotionId",
      "otherPromotionCode",
      "overlap",
      "combinedDiscount"
     ],
     "properties": {
      "otherPromotionId": {
       "type": "string",
       "format": "uuid"
      },
      "otherPromotionCode": {
       "type": "string"
      },
      "overlap": {
       "type": "string",
       "enum": [
        "products",
        "period",
        "channel",
        "full"
       ]
      },
      "combinedDiscount": {
       "type": "number",
       "description": "Combined percentage where both apply to the same line."
      },
      "isBlocking": {
       "type": "boolean",
       "description": "True where the combination would produce a line price of zero or below (decided 28 September, audit R101)."
      },
      "isNearZero": {
       "type": "boolean",
       "description": "True where the combination leaves a net line price above zero but below the venue setting `promotions.nearZeroLinePrice` (proposed AED 1.00; decided 28 September, audit R096 (5)). A warning, not a refusal."
      }
     }
    }
   },
   "worstCaseDiscount": {
    "type": "number",
    "description": "Largest combined discount any single line could receive."
   }
  }
 },
 "CreateOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "variantId",
   "quantity",
   "quotedUnitPrice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "eligibilityDeclaration": {
    "type": "array",
    "nullable": true,
    "x-ticvai-note": "One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n",
    "items": {
     "type": "object",
     "properties": {
      "ageBand": {
       "type": "string",
       "enum": [
        "infant",
        "child",
        "junior",
        "adult",
        "senior"
       ],
       "description": "Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."
      },
      "ageYears": {
       "type": "integer",
       "nullable": true
      },
      "heightBandIndex": {
       "type": "integer",
       "nullable": true
      },
      "confidentSwimmer": {
       "type": "boolean",
       "nullable": true,
       "description": "**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"
      },
      "guardianSigned": {
       "type": "boolean"
      }
     }
    },
    "description": "What was declared for each guest on this line, kept as the record staff check at the gate."
   },
   "quotedUnitPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the client charged, from its local bundle."
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"
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
 "CreatePromotionRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "discount",
   "validFrom"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "discount": {
    "$ref": "#/components/schemas/Discount"
   },
   "conditions": {
    "$ref": "#/components/schemas/PromotionConditions"
   },
   "stackingMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/StackingMode"
     }
    ],
    "default": "bestOnly"
   },
   "stackingGroup": {
    "type": "string",
    "maxLength": 64
   },
   "precedence": {
    "type": "integer",
    "default": 0,
    "description": "Higher evaluates first where several could apply."
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "maxRedemptions": {
    "type": "integer",
    "nullable": true
   },
   "maxRedemptionsPerGuest": {
    "type": "integer",
    "nullable": true
   },
   "budgetCap": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Total discount value after which the promotion stops automatically. **Enforced at checkout**, where an order whose discount would take the total past the cap does not receive the promotion (decided 28 September, audit R101)."
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The commercial campaign (`promotions.campaign`) this promotion belongs to; null for a promotion run on its own. The directory, calendar and campaign budget screens group by it. (DM5, 29 September: data model for the agreed operations)"
   },
   "recommendable": {
    "type": "boolean",
    "default": false,
    "description": "**May the recommendation engine show this offer to a guest** (8.6.30 to 8.6.36; 29 September, build pass, group G2, from group G1's handoff). False keeps a promotion to the basket, where `evaluatePromotions` applies it as before. True makes a live promotion a candidate item of kind `offer` in `ai.decideRecommendations` for the guests its conditions and `recommendableSegmentIds` admit: while it is live, `promotions.recommendationStrategyPublished` (kind `offers`) keeps the engine's candidate cache current, and it leaves the cache when it is paused, ends or expires. **The engine shows the offer; the discount is still computed here at the basket**, never by ai."
   },
   "recommendableSegmentIds": {
    "type": "array",
    "nullable": true,
    "description": "The marketing-crm segments the offer may be recommended to; null means every guest its own conditions admit.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "CreateRefundRequest": {
  "type": "object",
  "required": [
   "id",
   "amount",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Omit to refund the whole order."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "secondaryAuthorisation": {
    "type": "object",
    "description": "Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n",
    "required": [
     "principalId",
     "credential"
    ],
    "properties": {
     "principalId": {
      "type": "string",
      "format": "uuid"
     },
     "credential": {
      "type": "string",
      "maxLength": 512,
      "description": "The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."
     }
    }
   },
   "refundToOriginalTender": {
    "type": "boolean",
    "default": true
   },
   "alternateTender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateSeatBlockRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "performanceId",
   "seatIds",
   "reason",
   "note"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "$ref": "#/components/schemas/BlockReason"
   },
   "note": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "description": "Automatic release, for production holds freed close to performance."
   }
  }
 },
 "Discount": {
  "x-ticvai-persistence": "none — embedded in promotion",
  "type": "object",
  "required": [
   "kind"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/DiscountKind"
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "fixedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "buyQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "getQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "getDiscountPercentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "description": "100 makes the free items actually free; lower values give a partial discount."
   },
   "tiers": {
    "type": "array",
    "description": "For `tieredPercentage` — more units, larger discount.",
    "items": {
     "type": "object",
     "required": [
      "minQuantity",
      "percentage"
     ],
     "properties": {
      "minQuantity": {
       "type": "integer",
       "minimum": 1
      },
      "percentage": {
       "type": "number",
       "minimum": 0,
       "maximum": 100
      }
     }
    }
   },
   "maxDiscountAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Cap on a percentage discount. Prevents an unbounded discount on a large basket."
   },
   "rewardVariantIds": {
    "type": "array",
    "nullable": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the \"different product\" of a `buyXGetY` (setGiftFreeProduct, setBuyGetBogo). Absent means the reward is taken from the qualifying lines. (DM5, 29 September: data model for the agreed operations)"
   },
   "maxApplicationsPerBasket": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "How many times the offer repeats in one basket: the \"maximum repetitions\" of an N-for-X offer (setFixedPriceOffer). Null repeats for every complete set. (DM5, 29 September: data model for the agreed operations)"
   }
  }
 },
 "EvaluatePromotionsRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "venueId",
   "channel",
   "lines"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "description": "Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipTierId": {
    "type": "string",
    "format": "uuid"
   },
   "couponCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "evaluateAt": {
    "type": "string",
    "format": "date-time",
    "description": "For back-office testing of a rule before publishing."
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one `promotions.promotion_evaluation_trace` row for it. (decided 29 September, writers pass)"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "variantId",
      "quantity",
      "unitPrice"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "ExchangeOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "outgoingLineIds",
   "incomingLines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "outgoingLineIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "incomingLines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "waiveFee": {
    "type": "boolean",
    "default": false
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
 "GuestPromotion": {
  "x-ticvai-persistence": "none — guest projection of promotions.promotion",
  "type": "object",
  "description": "**What a guest may see of a promotion.** `Promotion` carries the commercial internals (`budgetCap`, `maxRedemptions`, `redemptionCount`, `discountGiven`, `precedence`, `stackingGroup`), and `listPromotions` and `getPromotion` are guest-audience. A guest caller receives this shape instead. `additionalProperties: false` is the point: a server that adds an internal field to it fails validation instead of publishing the field.\n",
  "additionalProperties": false,
  "required": [
   "id",
   "code",
   "name",
   "discount",
   "validFrom"
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
   "description": {
    "type": "string"
   },
   "discount": {
    "$ref": "#/components/schemas/Discount"
   },
   "conditions": {
    "$ref": "#/components/schemas/PromotionConditions"
   },
   "stackingMode": {
    "$ref": "#/components/schemas/StackingMode"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "maxRedemptionsPerGuest": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "ManualDiscountRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Omit to discount the order rather than a line."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 300,
    "description": "Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"
   },
   "reasonCode": {
    "type": "string",
    "nullable": true,
    "description": "Optional alongside the free text, where the venue maintains a list."
   },
   "approverPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required above the venue threshold. May not be the requester."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ModifyOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"
   },
   "addLines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "removeLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
    "format": "uuid",
    "description": "The client UUIDv7 from `CreateOrderRequest.id`."
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
    "format": "uuid",
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
 "OrderExchangeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "orderId",
   "outgoingValue",
   "incomingValue",
   "difference"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "outgoingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "incomingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exchangeFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Only the difference settles. The replacement is held before the original is released, never the other way round.\n"
   },
   "newLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
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
       "format": "uuid"
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
 "OrderLineAttributes": {
  "type": "object",
  "nullable": true,
  "additionalProperties": true,
  "x-ticvai-persistence": "none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line",
  "description": "Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n",
  "properties": {
   "transport": {
    "$ref": "#/components/schemas/TransportLineAttributes"
   }
  }
 },
 "OrderModificationResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "order",
   "balanceDue"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "addedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "removedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceDue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest pays; negative means a refund is due."
   },
   "refundId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "OrderResumeResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "order",
   "hasChanged"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "hasChanged": {
    "type": "boolean",
    "description": "True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "priceChanged",
        "promotionExpired",
        "promotionNowApplies",
        "soldOut",
        "seatHoldExpired",
        "productWithdrawn"
       ]
      },
      "lineId": {
       "type": "string",
       "format": "uuid"
      },
      "detail": {
       "type": "string"
      },
      "wasAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "nowAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "OrderStatement": {
  "x-ticvai-persistence": "none — computed from order, payment, refund and ledger",
  "type": "object",
  "required": [
   "orderId",
   "orderNumber",
   "currency",
   "entries",
   "currentBalance"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "orderNumber": {
    "type": "string"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "entries": {
    "type": "array",
    "description": "Sequential. What an agent reads to a guest asking about a charge.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "amount",
      "runningBalance",
      "occurredAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "sale",
        "payment",
        "refund",
        "void",
        "modification",
        "exchange",
        "fee",
        "variance",
        "chargeback"
       ]
      },
      "description": {
       "type": "string"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "runningBalance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "referenceId": {
       "type": "string",
       "nullable": true
      },
      "principalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "occurredAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "totalPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalRefunded": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "currentBalance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest owes; negative means a refund is outstanding."
   }
  }
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
    "format": "uuid"
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
 "PartnerQuote": {
  "type": "object",
  "x-ticvai-persistence": "subscription.partner_quote",
  "description": "**Drafted 4 September.** A priced offer to a partner, with an expiry. **Not the same as a procurement quotation** - `inventory.quotation` is what a supplier offers this venue, and this is what this venue offers a reseller.",
  "required": [
   "id"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid"
   },
   "currency": {
    "type": "string",
    "x-ticvai-persisted": false,
    "description": "**Not stored on the row.** Currency is region-scoped and resolves from the scope walk (ADR-0018); a quote that carries its own copy is a quote that disagrees with the region the moment one of them changes."
   },
   "totalMinor": {
    "type": "integer"
   },
   "state": {
    "type": "string",
    "enum": [
     "draft",
     "sent",
     "accepted",
     "declined",
     "expired"
    ]
   },
   "validUntil": {
    "type": "string",
    "format": "date-time",
    "description": "**Stored, not calculated** - an offer whose expiry moves when you read it is not an offer."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "PartnerRateMode": {
  "type": "string",
  "description": "**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n",
  "enum": [
   "netRate",
   "commission"
  ]
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
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
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
 "Promotion": {
  "x-ticvai-persistence": "promotions.promotion",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreatePromotionRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "status": {
      "$ref": "#/components/schemas/PromotionStatus"
     },
     "isPaused": {
      "type": "boolean"
     },
     "redemptionCount": {
      "type": "integer"
     },
     "discountGiven": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "publishedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "version": {
      "type": "integer",
      "minimum": 1,
      "readOnly": true,
      "description": "Starts at 1 and goes up by one on every saved change. The version the directory, the audit history (`promotions.promotion_audit`) and the channel publication monitor (`promotions.promotion_channel_publication`) name. (DM5, 29 September: data model for the agreed operations)"
     }
    }
   }
  ]
 },
 "PromotionConditions": {
  "x-ticvai-persistence": "none — embedded in promotion",
  "type": "object",
  "description": "All conditions must hold. An empty object matches everything.",
  "properties": {
   "variantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "productKinds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "categoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "minQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "minBasketValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channels": {
    "type": "array",
    "description": "Empty or absent matches every channel.",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "purchaseGate": {
    "type": "boolean",
    "default": false,
    "description": "BL-037. **`evaluatePromotions` gates a price and nothing gated a sale.** A non-member could buy a member-only product at the member price refused, which is a discount failure rather than an eligibility one.\nTrue makes these conditions a **precondition of purchase**: fail them and the line cannot be added, not merely charged more. **Evaluated at add-to-cart**, because a guest told at payment has already entered a card.\n"
   },
   "paymentMethod": {
    "type": "array",
    "nullable": true,
    "description": "BL-113. **Card-issuer and payment-type promotions** — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible.\n**Evaluated at payment, not at cart**, which is the awkward part: the discount appears after the tender is chosen, and the basket total must be allowed to move at that point.\n",
    "items": {
     "type": "string"
    }
   },
   "issuerBins": {
    "type": "array",
    "nullable": true,
    "description": "Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. **The bank supplies these and they change**, so they are data rather than configuration.\n",
    "items": {
     "type": "string"
    }
   },
   "componentRedemption": {
    "type": "string",
    "nullable": true,
    "enum": [
     "allTogether",
     "independently",
     "sequenced"
    ],
    "description": "BL-112. **Per-component redemption inside a bundle was unstated.** A park-plus-lunch bundle where lunch may be used another day behaves differently from one where both must be used on the same visit, and **the difference is revenue recognition, not just convenience.**\n"
   },
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 0,
     "maximum": 6
    }
   },
   "startTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "endTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "membershipTierIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresCoupon": {
    "type": "boolean",
    "default": false
   },
   "firstPurchaseOnly": {
    "type": "boolean",
    "default": false
   },
   "performanceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "advanceDaysMin": {
    "type": "integer",
    "description": "Early-bird — booked at least this many days ahead."
   },
   "advanceDaysMax": {
    "type": "integer",
    "description": "Last-minute — booked no more than this many days ahead."
   },
   "eligibilityRuleIds": {
    "type": "array",
    "nullable": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own, saved by setEligibilityRule) that must also hold. Each is evaluated with its own `effect`. (DM5, 29 September: data model for the agreed operations)"
   }
  }
 },
 "PromotionEvaluation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "totalDiscount",
   "lines",
   "applied",
   "rejected"
  ],
  "properties": {
   "totalDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "originalPrice",
      "discountedPrice",
      "discount"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "originalPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "discountedPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "appliedPromotionIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "applied": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "promotionId",
      "promotionCode",
      "discount"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "promotionCode": {
       "type": "string"
      },
      "promotionName": {
       "type": "string"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "couponCode": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "rejected": {
    "type": "array",
    "description": "Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionCode",
      "reason"
     ],
     "properties": {
      "promotionCode": {
       "type": "string"
      },
      "promotionName": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "conditionsNotMet",
        "supersededByBetterOffer",
        "exclusivePromotionApplied",
        "redemptionLimitReached",
        "budgetExhausted",
        "outsideValidPeriod",
        "wrongChannel",
        "membershipRequired",
        "couponRequired"
       ]
      },
      "detail": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "PromotionStatus": {
  "type": "string",
  "enum": [
   "draft",
   "scheduled",
   "live",
   "paused",
   "expired",
   "ended"
  ]
 },
 "PromotionUsage": {
  "x-ticvai-persistence": "none — aggregated from ledger and orders",
  "type": "object",
  "required": [
   "promotionId",
   "redemptionCount",
   "discountGiven"
  ],
  "properties": {
   "promotionId": {
    "type": "string",
    "format": "uuid"
   },
   "redemptionCount": {
    "type": "integer"
   },
   "discountGiven": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "budgetCap": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "budgetRemaining": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "isBudgetExhausted": {
    "type": "boolean"
   },
   "byChannel": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
      },
      "redemptionCount": {
       "type": "integer"
      },
      "discountGiven": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "Refund": {
  "x-ticvai-persistence": "orders.refund",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "amount",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "batchId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."
   },
   "fxRate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
    "nullable": true,
    "readOnly": true,
    "description": "**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"
   },
   "taxReversalEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"
   },
   "settleTo": {
    "type": "string",
    "enum": [
     "originalTender",
     "advanceBalance",
     "wireTransfer",
     "storeCredit"
    ],
    "default": "originalTender",
    "description": "BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n"
   },
   "fxVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "appliedPercentage": {
    "type": "number",
    "description": "From the venue's time bands, or an approver override."
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingApproval",
     "pendingGateway",
     "completed",
     "declined",
     "failed"
    ]
   },
   "reason": {
    "type": "string"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "secondaryPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ledgerEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Written before the gateway is called."
   },
   "gatewayReference": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "SeatBlock": {
  "x-ticvai-persistence": "seating.seat_block",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "seatIds",
   "reason",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "$ref": "#/components/schemas/BlockReason"
   },
   "note": {
    "type": "string"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "releasedAt": {
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
 "SeatHold": {
  "x-ticvai-persistence": "seating.seat_hold",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "seatIds",
   "status",
   "createdAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "bufferedSeatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Neighbours implicitly held by a seating rule."
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "converted",
     "released",
     "expired"
    ]
   },
   "totalPrice": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "heldByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "extensionCount": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "StackingMode": {
  "type": "string",
  "description": "How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine into a free ticket.\n",
  "enum": [
   "exclusive",
   "stackable",
   "bestOnly",
   "stackWithGroup"
  ]
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
 },
 "VoidReason": {
  "type": "string",
  "description": "**The void reason list** (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. `other` requires a note (audit R222), and the notes are reviewed quarterly to add real reasons. Proposed, client to correct.\n",
  "enum": [
   "guestChangedMind",
   "enteredInError",
   "itemUnavailable",
   "qualityIssue",
   "duplicate",
   "other"
  ]
 }
}
```
