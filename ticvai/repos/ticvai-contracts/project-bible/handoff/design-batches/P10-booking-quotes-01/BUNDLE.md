# P10-booking-quotes-01 — P10 · Booking & Quotes

**4 screens · 32 operations · 40 schemas · 14 permissions**

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
- **11 of these operations work offline**: applyManualDiscount, createOrder, evaluatePromotions, getOrder, getPromotion, holdOrder, listOrderRefunds, listOrders
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-008` | Booking Creation | listDetail | 14 | 1 | — |
| `PTR-009` | Group / Bulk Booking | listDetail | 4 | 0 | — |
| `PTR-010` | Cart & Quote | listDetail | 10 | 1 | — |
| `PTR-011` | Quote Management | listDetail | 4 | 0 | — |

## Thin screens in this batch

**PTR-011 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
    "PTR-001",
    "PTR-002",
    "PTR-003",
    "PTR-016"
   ],
   "flowDerived": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "PTR-016",
     "trigger": "Downloads vouchers",
     "provenance": "flow F03 step 3→4",
     "operation": "createOrder"
    },
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
    },
    {
     "to": "SCN-003",
     "trigger": "A customer arrives and is admitted",
     "provenance": "flow F10 step 3→4",
     "operation": "listOrders",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: SCN-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Add booking creation for this venue.",
  "gaps": [
   {
    "operation": "getOrderStatement",
    "why": "**2 declared operations reach no component on this screen**: getOrderStatement, listOrderRefunds. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every booking creation",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected booking creation",
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
       "label": "Create",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
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
    "trigger": "Void",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A booking creation this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   }
  ],
  "states": {
   "loading": "The booking creation list.",
   "error": "Could not load. Names which read failed and leaves the booking creation untouched.",
   "emptyFirstRun": "No booking creation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the booking creation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onLoad"
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
    "trigger": "onLoad"
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
       "kind": "dataTable",
       "label": "Every group bulk booking",
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
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group bulk booking",
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
       "label": "Allocate",
       "operation": "allocateBlockedSeats",
       "provenance": "contract seating.yaml POST /seat-blocks/{blockId}/allocate"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createSeatBlock",
       "provenance": "contract seating.yaml POST /seat-blocks"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishSeatBlock",
       "provenance": "contract seating.yaml DELETE /seat-blocks/{blockId}"
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
       "impliedBy": "listSeatBlocks",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "relinquishSeatBlock",
       "label": "Release seat block",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "allocateBlockedSeats",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group bulk booking list.",
   "error": "Could not load. Names which read failed and leaves the group bulk booking untouched.",
   "emptyFirstRun": "No group bulk booking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group bulk booking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "allocateBlockedSeats",
    "contract": "seating",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
   "note": "**Drawn by Claude Design on `Seat Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "patternReason": "`listPromotions` reads the population and `getPromotion` reads one of them — list, select, act",
  "purpose": "Work with cart & quote for this venue.",
  "gaps": [
   {
    "operation": "getPromotionUsage",
    "why": "**2 declared operations reach no component on this screen**: getPromotionUsage, getCart. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every cart quote",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cart quote",
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Evaluate",
       "operation": "evaluatePromotions",
       "provenance": "contract promotions.yaml POST /promotions/evaluate"
      },
      {
       "kind": "secondaryButton",
       "label": "Analyse",
       "operation": "analysePromotionConflicts",
       "provenance": "contract promotions.yaml GET /promotions/{promotionId}/conflicts"
      },
      {
       "kind": "secondaryButton",
       "label": "Add",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateCartLine",
       "provenance": "contract orders.yaml PATCH /carts/{cartId}/lines/{lineId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove",
       "operation": "removeCartLine",
       "provenance": "contract orders.yaml DELETE /carts/{cartId}/lines/{lineId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Checkout",
       "operation": "checkoutCart",
       "provenance": "contract orders.yaml POST /carts/{cartId}/checkout"
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
       "impliedBy": "listPromotions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "removeCartLine",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "label": "Remove cart line",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "evaluatePromotions",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveCartLine",
    "component": "confirmDialog",
    "trigger": "Remove",
    "body": "**Names what `removeCartLine` changes and what it leaves alone**, in the consequence rather than the verb. A cart quote this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml DELETE /carts/{cartId}/lines/{lineId}"
   }
  ],
  "states": {
   "loading": "The cart quote list.",
   "error": "Could not load. Names which read failed and leaves the cart quote untouched.",
   "emptyFirstRun": "No cart quote yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cart quote are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
   },
   {
    "operationId": "getPromotion",
    "contract": "promotions",
    "purpose": "Read a promotion",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPromotionUsage",
    "contract": "promotions",
    "purpose": "Redemption count and discount given",
    "trigger": "onLoad"
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
  "openQuestions": [
   "No contract — quotes are procurement-side only"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPartnerAgreements` reads the population and `getCommissionStatement` reads one of them — list, select, act",
  "purpose": "Find quote management for this venue.",
  "gaps": [
   {
    "operation": "listPartnerQuotes",
    "why": "**1 declared operation reach no component on this screen**: listPartnerQuotes. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every quote",
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
       "label": "The selected quote",
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
       "label": "Create",
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
   "emptyFirstRun": "No quote yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the quote are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
    "CommissionStatement.agreementId",
    "CommissionStatement.partnerName",
    "CommissionStatement.from",
    "CommissionStatement.to",
    "CommissionStatement.currency"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-011"
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
  "parameters": [],
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
  "parameters": [],
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
  "parameters": [],
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
  "responds": "Refund"
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
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
   }
  }
 },
 "BlockReason": {
  "type": "string",
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
     "requiresPrerequisite"
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
    "description": "Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold.\n"
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
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
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
    "format": "uuid",
    "nullable": true,
    "description": "The capacity held for this line. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"
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
       "description": "True where the combination would produce a negative or near-zero price."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Seated products only. Not available offline."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
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
    "additionalProperties": true
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key."
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string"
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
    "description": "Total discount value after which the promotion stops automatically."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string"
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
      "maxLength": 512
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
    "type": "string"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "outgoingLineIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lineId": {
    "type": "string",
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
     "type": "string"
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
    "type": "string"
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
     "type": "string"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
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
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
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
       "type": "string"
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
    "type": "string"
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
     }
    }
   }
  ]
 },
 "PromotionEvaluation": {
  "x-ticvai-persistence": "none — computed",
  "parameters": [
   {
    "$ref": "../shared/common.yaml#/components/parameters/IdempotencyKey"
   }
  ],
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
       "type": "string"
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
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "fxRate": {
    "type": "number",
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
