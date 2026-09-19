# P08-orders-money-03 — P08 · Orders & Money (3 of 3)

**9 screens · 55 operations · 51 schemas · 16 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 16 permissions apply here:
  `ACCOUNT_CONFIGURE, LEDGER_APPROVE, LEDGER_POST, LEDGER_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW, ORDER_VOID`…. A control nobody can use must say so,
  not sit enabled and fail.
- **13 of these operations work offline**: applyManualDiscount, createOrder, getOrder, getRefundPolicy, getVenueSettings, holdOrder, listFxRates, listOrderRefunds
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-065` | Venue Configuration | listDetail | 5 | 0 | — |
| `BO-070` | Work Orders | listDetail | 13 | 1 | — |
| `BO-074` | Chart of Accounts | listDetail | 8 | 0 | — |
| `BO-075` | Account Mapping | commandCentre | 7 | 0 | — |
| `BO-076` | Revenue Recognition | listDetail | 4 | 0 | — |
| `BO-077` | FX Rates & Variances | approvalInbox | 4 | 0 | — |
| `BO-089` | Journal Entries | approvalInbox | 6 | 2 | — |
| `BO-090` | Period Close | listDetail | 6 | 2 | — |
| `BO-101` | Orders & Money | listDetail | 3 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-065",
  "name": "Venue Configuration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/venue-configuration",
   "component": "apps/venue-management-web/src/routes/venue-operations/VenueConfigurationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads the population and `getRefundPolicy` reads one of them — list, select, act",
  "purpose": "Set the venue-level values everything inherits from.",
  "gaps": [
   {
    "operation": "listDeliveryLocations",
    "why": "**1 declared operation reach no component on this screen**: listDeliveryLocations. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every venue",
       "bindsTo": "DiningOutlet",
       "columns": [
        "DiningOutlet.outletId",
        "DiningOutlet.name",
        "DiningOutlet.kind",
        "DiningOutlet.zone",
        "DiningOutlet.cuisine",
        "DiningOutlet.isOpenNow",
        "DiningOutlet.opensAt",
        "DiningOutlet.closesAt",
        "DiningOutlet.orderingMethod",
        "DiningOutlet.estimatedWaitMinutes",
        "DiningOutlet.imageAssetRef",
        "DiningOutlet.menuId"
       ],
       "operation": "listDiningOutlets",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected venue",
       "bindsTo": "RefundPolicy",
       "columns": [
        "RefundPolicy.id",
        "RefundPolicy.venueId",
        "RefundPolicy.selfAuthoriseLimit",
        "RefundPolicy.requiresSecondUserAbove",
        "RefundPolicy.requiresApprovalAbove",
        "RefundPolicy.timeBands",
        "RefundPolicy.allowPartial",
        "RefundPolicy.refundWindowDays",
        "RefundPolicy.varianceThreshold"
       ],
       "operation": "getRefundPolicy",
       "provenance": "contract orders.yaml GET /venues/{venueId}/refund-policy"
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
       "operation": "setRefundPolicy",
       "provenance": "contract orders.yaml PUT /venues/{venueId}/refund-policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setVenueSettings",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listDiningOutlets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setRefundPolicy",
       "label": "Save refund policy",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setRefundPolicy",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue list.",
   "error": "Could not load. Names which read failed and leaves the venue untouched.",
   "emptyFirstRun": "No venue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRefundPolicy",
    "contract": "orders",
    "purpose": "Read a venue's refund policy",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDiningOutlets",
    "contract": "fnb",
    "purpose": "Where a guest can eat, right now",
    "trigger": "onLoad"
   },
   {
    "operationId": "setRefundPolicy",
    "contract": "orders",
    "purpose": "Set a venue's refund policy",
    "trigger": "onAction",
    "invalidates": [
     "listDiningOutlets"
    ]
   },
   {
    "operationId": "listDeliveryLocations",
    "contract": "fnb",
    "purpose": "Where an order can be delivered",
    "trigger": "onLoad"
   },
   {
    "operationId": "setVenueSettings",
    "contract": "tenancy",
    "purpose": "Save the venue's configuration",
    "trigger": "onAction",
    "invalidates": [
     "listDiningOutlets"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "RefundPolicy.id",
    "RefundPolicy.venueId",
    "RefundPolicy.selfAuthoriseLimit",
    "RefundPolicy.requiresSecondUserAbove",
    "RefundPolicy.requiresApprovalAbove"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-065"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-070",
  "name": "Work Orders",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/work-orders",
   "component": "apps/venue-management-web/src/routes/venue-operations/WorkOrdersDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **createRefund removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Get something fixed, and know it was.",
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
       "label": "Every work orders",
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
       "label": "The selected work orders",
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
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createOrder",
       "label": "Create order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "voidOrder",
       "label": "Void order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createOrder",
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
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A work orders this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   }
  ],
  "states": {
   "loading": "The work orders list.",
   "error": "Could not load. Names which read failed and leaves the work orders untouched.",
   "emptyFirstRun": "No work orders yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the work orders are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Create an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
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
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-070"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-074",
  "name": "Chart of Accounts",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/chart-of-accounts",
   "component": "apps/venue-management-web/src/routes/finance/ChartOfAccounts.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-075",
    "BO-076",
    "BO-077"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-075",
     "trigger": "Maps products to accounts",
     "provenance": "flow F16 step 5→6, F98 step 2→3"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-077",
     "trigger": "FX Rates & Variances",
     "carries": [
      "varianceId"
     ],
     "provenance": "derived — BO-077 declares entryState.params varianceId, so an edge into it must carry them"
    }
   ],
   "entryFrom": [
    "BO-043"
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. Pulled to Wave 1 (CF-101). **F16 says it itself** — no chart of accounts blocks the first sale, so it cannot be Wave 2 while venue provisioning is Wave 1.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAccounts` reads the population and `getAccount` reads one of them — list, select, act",
  "purpose": "Accounts, cost centres and legal entities.",
  "gaps": [
   {
    "operation": "listCostCenters",
    "why": "**2 declared operations reach no component on this screen**: listCostCenters, listLegalEntities. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every chart accounts",
       "bindsTo": "Account",
       "columns": [
        "Account.id",
        "Account.code",
        "Account.externalCode",
        "Account.isSuspense",
        "Account.subType",
        "Account.tags",
        "Account.notes",
        "Account.name",
        "Account.type",
        "Account.parentId",
        "Account.legalEntityId",
        "Account.currency"
       ],
       "operation": "listAccounts",
       "provenance": "contract finance.yaml GET /accounts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected chart accounts",
       "bindsTo": "Account",
       "columns": [
        "Account.id",
        "Account.code",
        "Account.externalCode",
        "Account.isSuspense",
        "Account.subType",
        "Account.tags",
        "Account.notes",
        "Account.name",
        "Account.type",
        "Account.parentId",
        "Account.legalEntityId",
        "Account.currency",
        "Account.isPostable",
        "Account.isActive",
        "Account.balance"
       ],
       "operation": "getAccount",
       "provenance": "contract finance.yaml GET /accounts/{accountId}"
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
       "operation": "createAccount",
       "provenance": "contract finance.yaml POST /accounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateAccount",
       "provenance": "contract finance.yaml PATCH /accounts/{accountId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCostCenter",
       "provenance": "contract finance.yaml POST /cost-centers"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createLegalEntity",
       "provenance": "contract finance.yaml POST /legal-entities"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The chart accounts list.",
   "error": "Could not load. Names which read failed and leaves the chart accounts untouched.",
   "emptyFirstRun": "No chart accounts yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the chart accounts are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccounts",
    "contract": "finance",
    "purpose": "List the chart of accounts",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAccount",
    "contract": "finance",
    "purpose": "Read an account",
    "trigger": "onLoad"
   },
   {
    "operationId": "createAccount",
    "contract": "finance",
    "purpose": "Create an account",
    "trigger": "onAction",
    "invalidates": [
     "listAccounts"
    ]
   },
   {
    "operationId": "updateAccount",
    "contract": "finance",
    "purpose": "Rename, remap or deactivate an account",
    "trigger": "onAction",
    "invalidates": [
     "listAccounts"
    ]
   },
   {
    "operationId": "listCostCenters",
    "contract": "finance",
    "purpose": "List cost centres",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCostCenter",
    "contract": "finance",
    "purpose": "Create a cost centre",
    "trigger": "onAction",
    "invalidates": [
     "listAccounts"
    ]
   },
   {
    "operationId": "listLegalEntities",
    "contract": "finance",
    "purpose": "List legal entities",
    "trigger": "onLoad"
   },
   {
    "operationId": "createLegalEntity",
    "contract": "finance",
    "purpose": "Create a legal entity",
    "trigger": "onAction",
    "invalidates": [
     "listAccounts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "accountId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `accountId`.",
   "preloaded": [
    "Account.id",
    "Account.code",
    "Account.externalCode",
    "Account.isSuspense",
    "Account.subType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-074"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-075",
  "name": "Account Mapping",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/account-mapping",
   "component": "apps/venue-management-web/src/routes/finance/AccountMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-074",
    "BO-076",
    "BO-077"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-076",
     "trigger": "Revenue Recognition",
     "provenance": "flow F98 step 3→4"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId, so an edge into it must carry them"
    },
    {
     "to": "BO-077",
     "trigger": "FX Rates & Variances",
     "carries": [
      "varianceId"
     ],
     "provenance": "derived — BO-077 declares entryState.params varianceId, so an edge into it must carry them"
    },
    {
     "to": "ADM-020",
     "trigger": "Creates the first venue manager",
     "provenance": "flow F16 step 6→7",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. Pulled to Wave 1 (CF-101). Without a mapping every sale posts to suspense. **Cross-platform navigation removed 24 August**: ADM-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "3 independent reads and no read of one record — the screen watches a population rather than working one",
  "purpose": "Which product or movement posts to which account.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Account mappings",
       "bindsTo": "AccountMapping",
       "operation": "listAccountMappings",
       "provenance": "contract finance.yaml GET /account-mappings"
      },
      {
       "kind": "metricTile",
       "label": "Tax codes",
       "bindsTo": "TaxCode",
       "operation": "listTaxCodes",
       "provenance": "contract finance.yaml GET /tax-codes"
      },
      {
       "kind": "metricTile",
       "label": "Tax exemptions",
       "bindsTo": "TaxExemption",
       "operation": "listTaxExemptions",
       "provenance": "contract finance.yaml GET /tax-exemptions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every account mapping",
       "bindsTo": "AccountMapping",
       "columns": [
        "AccountMapping.eventType",
        "AccountMapping.debitAccountId",
        "AccountMapping.creditAccountId",
        "AccountMapping.venueId"
       ],
       "operation": "listAccountMappings",
       "provenance": "contract finance.yaml GET /account-mappings"
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
       "operation": "setAccountMappings",
       "provenance": "contract finance.yaml PUT /account-mappings"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createTaxCode",
       "provenance": "contract finance.yaml POST /tax-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateTaxCode",
       "provenance": "contract finance.yaml PATCH /tax-codes/{taxCodeId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createTaxExemption",
       "provenance": "contract finance.yaml POST /tax-exemptions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The account mapping list.",
   "error": "Could not load. Names which read failed and leaves the account mapping untouched.",
   "emptyFirstRun": "No account mapping yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the account mapping are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccountMappings",
    "contract": "finance",
    "purpose": "Which account each transaction type posts to",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAccountMappings",
    "contract": "finance",
    "purpose": "Set posting mappings",
    "trigger": "onAction",
    "invalidates": [
     "listAccountMappings"
    ]
   },
   {
    "operationId": "listTaxCodes",
    "contract": "finance",
    "purpose": "List tax codes",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTaxCode",
    "contract": "finance",
    "purpose": "Create a tax code",
    "trigger": "onAction",
    "invalidates": [
     "listAccountMappings"
    ]
   },
   {
    "operationId": "updateTaxCode",
    "contract": "finance",
    "purpose": "Amend a tax code",
    "trigger": "onAction",
    "invalidates": [
     "listAccountMappings"
    ]
   },
   {
    "operationId": "listTaxExemptions",
    "contract": "finance",
    "purpose": "List tax exemptions",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTaxExemption",
    "contract": "finance",
    "purpose": "Grant a tax exemption",
    "trigger": "onAction",
    "invalidates": [
     "listAccountMappings"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "taxCodeId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `taxCodeId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-075"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-076",
  "name": "Revenue Recognition",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/revenue-recognition",
   "component": "apps/venue-management-web/src/routes/finance/RevenueRecognition.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-074",
    "BO-075",
    "BO-077"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId, so an edge into it must carry them"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "carries": [
      "taxCodeId"
     ],
     "provenance": "derived — BO-075 declares entryState.params taxCodeId, so an edge into it must carry them"
    },
    {
     "to": "BO-077",
     "trigger": "FX Rates & Variances",
     "carries": [
      "varianceId"
     ],
     "provenance": "derived — BO-077 declares entryState.params varianceId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listRecognitionSchedules` reads the population and `getDeferredRevenue` reads one of them — list, select, act",
  "purpose": "Deferred revenue, its ageing, and the schedules that release it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every revenue recognition",
       "bindsTo": "RecognitionSchedule",
       "columns": [
        "RecognitionSchedule.id",
        "RecognitionSchedule.name",
        "RecognitionSchedule.method",
        "RecognitionSchedule.priority",
        "RecognitionSchedule.recognitionSite",
        "RecognitionSchedule.frequency",
        "RecognitionSchedule.revalidateOnValidityChange",
        "RecognitionSchedule.productKinds",
        "RecognitionSchedule.deferredAccountId",
        "RecognitionSchedule.recognisedAccountId",
        "RecognitionSchedule.breakageAccountId",
        "RecognitionSchedule.noShowTrigger"
       ],
       "operation": "listRecognitionSchedules",
       "provenance": "contract finance.yaml GET /recognition-schedules"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected revenue recognition",
       "bindsTo": "DeferredRevenueReport",
       "columns": [
        "DeferredRevenueReport.asAt",
        "DeferredRevenueReport.total",
        "DeferredRevenueReport.buckets"
       ],
       "operation": "getDeferredRevenue",
       "provenance": "contract finance.yaml GET /deferred-revenue"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runRecognition",
       "provenance": "contract finance.yaml POST /recognition/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createRecognitionSchedule",
       "provenance": "contract finance.yaml POST /recognition-schedules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue recognition list.",
   "error": "Could not load. Names which read failed and leaves the revenue recognition untouched.",
   "emptyFirstRun": "No revenue recognition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue recognition are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getDeferredRevenue",
    "contract": "finance",
    "purpose": "Deferred revenue balance and ageing",
    "trigger": "onLoad"
   },
   {
    "operationId": "runRecognition",
    "contract": "finance",
    "purpose": "Recognise earned revenue for a period",
    "trigger": "onAction",
    "invalidates": [
     "listRecognitionSchedules"
    ]
   },
   {
    "operationId": "listRecognitionSchedules",
    "contract": "finance",
    "purpose": "List revenue recognition schedules",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRecognitionSchedule",
    "contract": "finance",
    "purpose": "Define how a product class recognises revenue",
    "trigger": "onAction",
    "invalidates": [
     "listRecognitionSchedules"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "DeferredRevenueReport.asAt",
    "DeferredRevenueReport.total",
    "DeferredRevenueReport.buckets"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-076"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-077",
  "name": "FX Rates & Variances",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/fx-rates-variances",
   "component": "apps/venue-management-web/src/routes/finance/FxRatesVariances.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-074",
    "BO-075",
    "BO-076"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId, so an edge into it must carry them"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "carries": [
      "taxCodeId"
     ],
     "provenance": "derived — BO-075 declares entryState.params taxCodeId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`reviewPriceVariance` decides items that `listFxRates` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Rates, and the price variances waiting for review.",
  "gaps": [
   {
    "operation": "listPriceVariances",
    "why": "**1 declared operation reach no component on this screen**: listPriceVariances. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "FxRate",
       "columns": [
        "FxRate.id",
        "FxRate.fromCurrency",
        "FxRate.toCurrency",
        "FxRate.rate",
        "FxRate.purpose",
        "FxRate.source",
        "FxRate.effectiveFrom",
        "FxRate.effectiveTo",
        "FxRate.setByPrincipalId",
        "FxRate.providerReference",
        "FxRate.fetchedAt"
       ],
       "operation": "listFxRates",
       "provenance": "contract finance.yaml GET /fx-rates"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rates variances",
       "bindsTo": "FxRate",
       "columns": [
        "FxRate.id",
        "FxRate.fromCurrency",
        "FxRate.toCurrency",
        "FxRate.rate",
        "FxRate.purpose",
        "FxRate.source",
        "FxRate.effectiveFrom",
        "FxRate.effectiveTo",
        "FxRate.setByPrincipalId",
        "FxRate.providerReference",
        "FxRate.fetchedAt"
       ],
       "operation": "listFxRates",
       "provenance": "contract finance.yaml GET /fx-rates"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setFxRate",
       "provenance": "contract finance.yaml PUT /fx-rates"
      },
      {
       "kind": "secondaryButton",
       "label": "Review",
       "operation": "reviewPriceVariance",
       "provenance": "contract finance.yaml POST /price-variances/{varianceId}/review"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rates variances list.",
   "error": "Could not load. Names which read failed and leaves the rates variances untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the rates variances are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFxRates",
    "contract": "finance",
    "purpose": "The rates in force",
    "trigger": "onLoad"
   },
   {
    "operationId": "setFxRate",
    "contract": "finance",
    "purpose": "Set a rate",
    "trigger": "onAction",
    "invalidates": [
     "listFxRates"
    ]
   },
   {
    "operationId": "listPriceVariances",
    "contract": "finance",
    "purpose": "List price variances",
    "trigger": "onLoad"
   },
   {
    "operationId": "reviewPriceVariance",
    "contract": "finance",
    "purpose": "Record a review decision on an exception variance",
    "trigger": "onAction",
    "invalidates": [
     "listFxRates"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "varianceId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `varianceId`.",
   "preloaded": [
    "FxRate.id",
    "FxRate.fromCurrency",
    "FxRate.toCurrency",
    "FxRate.rate",
    "FxRate.purpose"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-077"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-089",
  "name": "Journal Entries",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/journal-entries",
   "component": "apps/venue-management-web/src/routes/finance/JournalEntries.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-074",
    "BO-075",
    "BO-076",
    "BO-090"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-090",
     "trigger": "Begins the close",
     "provenance": "flow F13 step 3→4"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId, so an edge into it must carry them"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "carries": [
      "taxCodeId"
     ],
     "provenance": "derived — BO-075 declares entryState.params taxCodeId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`approveJournalEntry` decides items that `listJournalEntries` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Every posting, and the ones waiting for approval.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "JournalEntry",
       "columns": [
        "JournalEntry.id",
        "JournalEntry.entryNumber",
        "JournalEntry.fiscalPeriodId",
        "JournalEntry.status",
        "JournalEntry.source",
        "JournalEntry.sourceId",
        "JournalEntry.description",
        "JournalEntry.reference",
        "JournalEntry.lines",
        "JournalEntry.totalDebit",
        "JournalEntry.totalCredit",
        "JournalEntry.postedByPrincipalId"
       ],
       "operation": "listJournalEntries",
       "provenance": "contract finance.yaml GET /journal-entries"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected journal entries",
       "bindsTo": "JournalEntry",
       "columns": [
        "JournalEntry.id",
        "JournalEntry.entryNumber",
        "JournalEntry.fiscalPeriodId",
        "JournalEntry.status",
        "JournalEntry.source",
        "JournalEntry.sourceId",
        "JournalEntry.description",
        "JournalEntry.reference",
        "JournalEntry.lines",
        "JournalEntry.totalDebit",
        "JournalEntry.totalCredit",
        "JournalEntry.postedByPrincipalId",
        "JournalEntry.approvedByPrincipalId",
        "JournalEntry.reversalOfEntryId",
        "JournalEntry.reversedByEntryId",
        "JournalEntry.postedAt"
       ],
       "operation": "getJournalEntry",
       "provenance": "contract finance.yaml GET /journal-entries/{entryId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createJournalEntry",
       "provenance": "contract finance.yaml POST /journal-entries"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "operation": "approveJournalEntry",
       "provenance": "contract finance.yaml POST /journal-entries/{entryId}/approve"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "operation": "rejectJournal",
       "provenance": "contract finance.yaml POST /journal-entries/{entryId}/reject"
      },
      {
       "kind": "destructiveButton",
       "label": "Reverse",
       "operation": "reverseJournalEntry",
       "provenance": "contract finance.yaml POST /journal-entries/{entryId}/reverse"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectJournal",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Names what `rejectJournal` changes and what it leaves alone**, in the consequence rather than the verb. A journal entries this affects should be identified in the dialog, not just counted.",
    "provenance": "contract finance.yaml POST /journal-entries/{entryId}/reject"
   },
   {
    "id": "confirmReverseJournalEntry",
    "component": "confirmDialog",
    "trigger": "Reverse",
    "body": "**Names what `reverseJournalEntry` changes and what it leaves alone**, in the consequence rather than the verb. A journal entries this affects should be identified in the dialog, not just counted.",
    "provenance": "contract finance.yaml POST /journal-entries/{entryId}/reverse"
   }
  ],
  "states": {
   "loading": "The journal entries list.",
   "error": "Could not load. Names which read failed and leaves the journal entries untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the journal entries are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listJournalEntries",
    "contract": "finance",
    "purpose": "List journal entries",
    "trigger": "onLoad"
   },
   {
    "operationId": "getJournalEntry",
    "contract": "finance",
    "purpose": "Read a journal entry",
    "trigger": "onLoad"
   },
   {
    "operationId": "createJournalEntry",
    "contract": "finance",
    "purpose": "Post a manual journal voucher",
    "trigger": "onAction",
    "invalidates": [
     "listJournalEntries"
    ]
   },
   {
    "operationId": "approveJournalEntry",
    "contract": "finance",
    "purpose": "Approve a journal entry and post it",
    "trigger": "onAction",
    "invalidates": [
     "listJournalEntries"
    ]
   },
   {
    "operationId": "rejectJournal",
    "contract": "finance",
    "purpose": "Reject a journal awaiting approval",
    "trigger": "onAction",
    "invalidates": [
     "listJournalEntries"
    ]
   },
   {
    "operationId": "reverseJournalEntry",
    "contract": "finance",
    "purpose": "Reverse a posted entry",
    "trigger": "onAction",
    "invalidates": [
     "listJournalEntries"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entryId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `entryId`.",
   "preloaded": [
    "JournalEntry.id",
    "JournalEntry.entryNumber",
    "JournalEntry.fiscalPeriodId",
    "JournalEntry.status",
    "JournalEntry.source"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-089"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-090",
  "name": "Period Close",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/period-close",
   "component": "apps/venue-management-web/src/routes/finance/PeriodClose.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-040",
    "BO-074",
    "BO-075",
    "BO-076"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-040",
     "trigger": "Clears outstanding shift variances",
     "provenance": "flow F13 step 1→2"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId, so an edge into it must carry them"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "carries": [
      "taxCodeId"
     ],
     "provenance": "derived — BO-075 declares entryState.params taxCodeId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listFiscalPeriods` reads the population and `getTrialBalance` reads one of them — list, select, act",
  "purpose": "Close a fiscal period, and see what is stopping it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every period close",
       "bindsTo": "FiscalPeriod",
       "columns": [
        "FiscalPeriod.id",
        "FiscalPeriod.legalEntityId",
        "FiscalPeriod.name",
        "FiscalPeriod.startDate",
        "FiscalPeriod.endDate",
        "FiscalPeriod.status",
        "FiscalPeriod.closedByPrincipalId",
        "FiscalPeriod.closedAt"
       ],
       "operation": "listFiscalPeriods",
       "provenance": "contract finance.yaml GET /fiscal-periods"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected period close",
       "bindsTo": "TrialBalance",
       "columns": [
        "TrialBalance.fiscalPeriodId",
        "TrialBalance.isBalanced",
        "TrialBalance.totalDebit",
        "TrialBalance.totalCredit",
        "TrialBalance.accounts"
       ],
       "operation": "getTrialBalance",
       "provenance": "contract finance.yaml GET /ledger/trial-balance"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Begin",
       "operation": "beginPeriodClose",
       "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/begin-close"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeFiscalPeriod",
       "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/close"
      },
      {
       "kind": "destructiveButton",
       "label": "Abandon",
       "operation": "abandonPeriodClose",
       "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/abandon-close"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenPeriod",
       "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/reopen"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseFiscalPeriod",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeFiscalPeriod` changes and what it leaves alone**, in the consequence rather than the verb. A period close this affects should be identified in the dialog, not just counted.",
    "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/close"
   },
   {
    "id": "confirmAbandonPeriodClose",
    "component": "confirmDialog",
    "trigger": "Abandon",
    "body": "**Names what `abandonPeriodClose` changes and what it leaves alone**, in the consequence rather than the verb. A period close this affects should be identified in the dialog, not just counted.",
    "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/abandon-close"
   }
  ],
  "states": {
   "loading": "The period close list.",
   "error": "Could not load. Names which read failed and leaves the period close untouched.",
   "emptyFirstRun": "No period close yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the period close are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFiscalPeriods",
    "contract": "finance",
    "purpose": "List fiscal periods",
    "trigger": "onLoad"
   },
   {
    "operationId": "beginPeriodClose",
    "contract": "finance",
    "purpose": "Begin closing a period",
    "trigger": "onAction",
    "invalidates": [
     "listFiscalPeriods"
    ]
   },
   {
    "operationId": "closeFiscalPeriod",
    "contract": "finance",
    "purpose": "Close a period and lock postings",
    "trigger": "onAction",
    "invalidates": [
     "listFiscalPeriods"
    ]
   },
   {
    "operationId": "abandonPeriodClose",
    "contract": "finance",
    "purpose": "Abandon a close in progress",
    "trigger": "onAction",
    "invalidates": [
     "listFiscalPeriods"
    ]
   },
   {
    "operationId": "reopenPeriod",
    "contract": "finance",
    "purpose": "Reopen a closed period",
    "trigger": "onAction",
    "invalidates": [
     "listFiscalPeriods"
    ]
   },
   {
    "operationId": "getTrialBalance",
    "contract": "finance",
    "purpose": "Trial balance for a period",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "periodId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `periodId`.",
   "preloaded": [
    "TrialBalance.fiscalPeriodId",
    "TrialBalance.isBalanced",
    "TrialBalance.totalDebit",
    "TrialBalance.totalCredit",
    "TrialBalance.accounts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-090"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-101",
  "name": "Orders & Money",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money",
   "component": "apps/venue-management-web/src/routes/home/OrdersMoneyList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-008",
    "BO-022",
    "BO-023",
    "BO-024",
    "BO-025",
    "BO-026",
    "BO-027",
    "BO-028",
    "BO-029",
    "BO-039",
    "BO-040",
    "BO-041",
    "BO-042",
    "BO-043",
    "BO-047",
    "BO-048",
    "BO-051",
    "BO-059",
    "BO-061",
    "BO-062",
    "BO-065",
    "BO-070",
    "BO-074",
    "BO-075",
    "BO-076",
    "BO-077",
    "BO-089",
    "BO-090"
   ],
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-022",
     "trigger": "Order Detail",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — BO-022 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "BO-023",
     "trigger": "Refunds & Exchanges",
     "carries": [
      "orderId",
      "venueId"
     ],
     "provenance": "derived — BO-023 declares entryState.params orderId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-024",
     "trigger": "Payment Exceptions",
     "carries": [
      "depositId",
      "paymentId"
     ],
     "provenance": "derived — BO-024 declares entryState.params depositId, paymentId, so an edge into it must carry them"
    },
    {
     "to": "BO-025",
     "trigger": "Chargebacks & Disputes",
     "carries": [
      "settlementId"
     ],
     "provenance": "derived — BO-025 declares entryState.params settlementId, so an edge into it must carry them"
    },
    {
     "to": "BO-026",
     "trigger": "Group Bookings",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — BO-026 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "BO-027",
     "trigger": "Reissue & Media Replacement",
     "carries": [
      "mediaCode",
      "mediaId"
     ],
     "provenance": "derived — BO-027 declares entryState.params mediaCode, mediaId, so an edge into it must carry them"
    },
    {
     "to": "BO-029",
     "trigger": "Report Builder",
     "carries": [
      "conversationId",
      "reportId"
     ],
     "provenance": "derived — BO-029 declares entryState.params conversationId, reportId, so an edge into it must carry them"
    },
    {
     "to": "BO-039",
     "trigger": "Shift Directory",
     "carries": [
      "shiftId"
     ],
     "provenance": "derived — BO-039 declares entryState.params shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-040",
     "trigger": "Variance Approval",
     "carries": [
      "shiftId"
     ],
     "provenance": "derived — BO-040 declares entryState.params shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-041",
     "trigger": "Cash Movements",
     "carries": [
      "shiftId"
     ],
     "provenance": "derived — BO-041 declares entryState.params shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-042",
     "trigger": "Banking & Safe",
     "carries": [
      "shiftId"
     ],
     "provenance": "derived — BO-042 declares entryState.params shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-043",
     "trigger": "Daily Reconciliation",
     "carries": [
      "settlementId"
     ],
     "provenance": "derived — BO-043 declares entryState.params settlementId, so an edge into it must carry them"
    },
    {
     "to": "BO-047",
     "trigger": "Order Corrections & Exceptions",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — BO-047 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "BO-048",
     "trigger": "Retail Products",
     "carries": [
      "merchandiseId"
     ],
     "provenance": "derived — BO-048 declares entryState.params merchandiseId, so an edge into it must carry them"
    },
    {
     "to": "BO-051",
     "trigger": "Purchase Orders",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — BO-051 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "BO-059",
     "trigger": "Sales Reports",
     "carries": [
      "conversationId",
      "reportId"
     ],
     "provenance": "derived — BO-059 declares entryState.params conversationId, reportId, so an edge into it must carry them"
    },
    {
     "to": "BO-061",
     "trigger": "Scheduled Reports",
     "carries": [
      "conversationId",
      "reportId"
     ],
     "provenance": "derived — BO-061 declares entryState.params conversationId, reportId, so an edge into it must carry them"
    },
    {
     "to": "BO-062",
     "trigger": "Venue Profile",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-062 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-065",
     "trigger": "Venue Configuration",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-065 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-070",
     "trigger": "Work Orders",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — BO-070 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId, so an edge into it must carry them"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "carries": [
      "taxCodeId"
     ],
     "provenance": "derived — BO-075 declares entryState.params taxCodeId, so an edge into it must carry them"
    },
    {
     "to": "BO-077",
     "trigger": "FX Rates & Variances",
     "carries": [
      "varianceId"
     ],
     "provenance": "derived — BO-077 declares entryState.params varianceId, so an edge into it must carry them"
    },
    {
     "to": "BO-089",
     "trigger": "Journal Entries",
     "carries": [
      "entryId"
     ],
     "provenance": "derived — BO-089 declares entryState.params entryId, so an edge into it must carry them"
    },
    {
     "to": "BO-090",
     "trigger": "Period Close",
     "carries": [
      "periodId"
     ],
     "provenance": "derived — BO-090 declares entryState.params periodId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Section landing. **28 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in orders & money, and what in it needs attention.",
  "gaps": [
   {
    "operation": "listSettlements",
    "why": "**1 declared operation reach no component on this screen**: listSettlements. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every orders money",
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
       "label": "The selected orders money",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "28 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search orders & money",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in orders & money yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for orders & money. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "Orders taken in this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSettlements",
    "contract": "finance",
    "purpose": "Money settled and what is outstanding",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
   "preloaded": [
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-101"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
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
 "abandonPeriodClose": {
  "method": "POST",
  "path": "/fiscal-periods/{periodId}/abandon-close",
  "contract": "finance",
  "summary": "Abandon a close in progress",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "approveJournalEntry": {
  "method": "POST",
  "path": "/journal-entries/{entryId}/approve",
  "contract": "finance",
  "summary": "Approve a journal entry and post it",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "JournalEntry"
 },
 "beginPeriodClose": {
  "method": "POST",
  "path": "/fiscal-periods/{periodId}/begin-close",
  "contract": "finance",
  "summary": "Begin closing a period",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "closeFiscalPeriod": {
  "method": "POST",
  "path": "/fiscal-periods/{periodId}/close",
  "contract": "finance",
  "summary": "Close a period and lock postings",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PeriodCloseResult"
 },
 "createAccount": {
  "method": "POST",
  "path": "/accounts",
  "contract": "finance",
  "summary": "Create an account",
  "permission": "ACCOUNT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateAccountRequest",
  "responds": "Account"
 },
 "createCostCenter": {
  "method": "POST",
  "path": "/cost-centers",
  "contract": "finance",
  "summary": "Create a cost centre",
  "permission": "ACCOUNT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CostCenter"
 },
 "createJournalEntry": {
  "method": "POST",
  "path": "/journal-entries",
  "contract": "finance",
  "summary": "Post a manual journal voucher",
  "permission": "LEDGER_POST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateJournalEntryRequest",
  "responds": "JournalEntry"
 },
 "createLegalEntity": {
  "method": "POST",
  "path": "/legal-entities",
  "contract": "finance",
  "summary": "Create a legal entity",
  "permission": "ACCOUNT_CONFIGURE",
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
  "requestBody": "LegalEntity",
  "responds": "LegalEntity"
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
 "createRecognitionSchedule": {
  "method": "POST",
  "path": "/recognition-schedules",
  "contract": "finance",
  "summary": "Define how a product class recognises revenue",
  "permission": "ACCOUNT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecognitionSchedule",
  "responds": "RecognitionSchedule"
 },
 "createTaxCode": {
  "method": "POST",
  "path": "/tax-codes",
  "contract": "finance",
  "summary": "Create a tax code",
  "permission": "TAX_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateTaxCodeRequest",
  "responds": "TaxCode"
 },
 "createTaxExemption": {
  "method": "POST",
  "path": "/tax-exemptions",
  "contract": "finance",
  "summary": "DelegatedAccess a tax exemption",
  "permission": "TAX_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "TaxExemption",
  "responds": "TaxExemption"
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
 "getAccount": {
  "method": "GET",
  "path": "/accounts/{accountId}",
  "contract": "finance",
  "summary": "Read an account",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "Account"
 },
 "getDeferredRevenue": {
  "method": "GET",
  "path": "/deferred-revenue",
  "contract": "finance",
  "summary": "Deferred revenue balance and ageing",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DeferredRevenueReport"
 },
 "getJournalEntry": {
  "method": "GET",
  "path": "/journal-entries/{entryId}",
  "contract": "finance",
  "summary": "Read a journal entry",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "JournalEntry"
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
 "getRefundPolicy": {
  "method": "GET",
  "path": "/venues/{venueId}/refund-policy",
  "contract": "orders",
  "summary": "Read a venue's refund policy",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RefundPolicy"
 },
 "getTrialBalance": {
  "method": "GET",
  "path": "/ledger/trial-balance",
  "contract": "finance",
  "summary": "Trial balance for a period",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": true
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TrialBalance"
 },
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
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
 "listAccountMappings": {
  "method": "GET",
  "path": "/account-mappings",
  "contract": "finance",
  "summary": "Which account each transaction type posts to",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
  "responds": "AccountMapping"
 },
 "listAccounts": {
  "method": "GET",
  "path": "/accounts",
  "contract": "finance",
  "summary": "List the chart of accounts",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "type",
    "in": "query",
    "required": null
   },
   {
    "name": "isPostable",
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
 "listCostCenters": {
  "method": "GET",
  "path": "/cost-centers",
  "contract": "finance",
  "summary": "List cost centres",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "listDeliveryLocations": {
  "method": "GET",
  "path": "/venues/{venueId}/delivery-locations",
  "contract": "fnb",
  "summary": "Where an order can be delivered",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "servingOutletId",
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
  "responds": "DeliveryLocation"
 },
 "listDiningOutlets": {
  "method": "GET",
  "path": "/venues/{venueId}/dining",
  "contract": "fnb",
  "summary": "Where a guest can eat, right now",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "openNow",
    "in": "query",
    "required": null
   },
   {
    "name": "orderingMethod",
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
  "responds": "DiningOutlet"
 },
 "listFiscalPeriods": {
  "method": "GET",
  "path": "/fiscal-periods",
  "contract": "finance",
  "summary": "List fiscal periods",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
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
  "responds": "FiscalPeriod"
 },
 "listFxRates": {
  "method": "GET",
  "path": "/fx-rates",
  "contract": "finance",
  "summary": "The rates in force",
  "permission": "LEDGER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "purpose",
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
  "responds": "FxRate"
 },
 "listJournalEntries": {
  "method": "GET",
  "path": "/journal-entries",
  "contract": "finance",
  "summary": "List journal entries",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "source",
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
 "listLegalEntities": {
  "method": "GET",
  "path": "/legal-entities",
  "contract": "finance",
  "summary": "List legal entities",
  "permission": "LEDGER_VIEW",
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
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "LegalEntity"
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
 "listPriceVariances": {
  "method": "GET",
  "path": "/price-variances",
  "contract": "finance",
  "summary": "List price variances",
  "permission": "LEDGER_VIEW",
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
    "name": "exceptionsOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "reviewStatus",
    "in": "query",
    "required": null
   },
   {
    "name": "occurredFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "occurredTo",
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
 "listRecognitionSchedules": {
  "method": "GET",
  "path": "/recognition-schedules",
  "contract": "finance",
  "summary": "List revenue recognition schedules",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "listSettlements": {
  "method": "GET",
  "path": "/settlements",
  "contract": "finance",
  "summary": "List settlement batches",
  "permission": "SETTLEMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "providerName",
    "in": "query",
    "required": null
   },
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
 "listTaxCodes": {
  "method": "GET",
  "path": "/tax-codes",
  "contract": "finance",
  "summary": "List tax codes",
  "permission": "LEDGER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "countryCode",
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
 "listTaxExemptions": {
  "method": "GET",
  "path": "/tax-exemptions",
  "contract": "finance",
  "summary": "List tax exemptions",
  "permission": "LEDGER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
  "responds": "TaxExemption"
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
 "rejectJournal": {
  "method": "POST",
  "path": "/journal-entries/{entryId}/reject",
  "contract": "finance",
  "summary": "Reject a journal awaiting approval",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "reopenPeriod": {
  "method": "POST",
  "path": "/fiscal-periods/{periodId}/reopen",
  "contract": "finance",
  "summary": "Reopen a closed period",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "reverseJournalEntry": {
  "method": "POST",
  "path": "/journal-entries/{entryId}/reverse",
  "contract": "finance",
  "summary": "Reverse a posted entry",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "JournalEntry"
 },
 "reviewPriceVariance": {
  "method": "POST",
  "path": "/price-variances/{varianceId}/review",
  "contract": "finance",
  "summary": "Record a review decision on an exception variance",
  "permission": "LEDGER_APPROVE",
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
  "responds": "PriceVariance"
 },
 "runRecognition": {
  "method": "POST",
  "path": "/recognition/run",
  "contract": "finance",
  "summary": "Recognise earned revenue for a period",
  "permission": "LEDGER_POST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RecognitionRunResult"
 },
 "setAccountMappings": {
  "method": "PUT",
  "path": "/account-mappings",
  "contract": "finance",
  "summary": "Set posting mappings",
  "permission": "ACCOUNT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccountMapping"
 },
 "setFxRate": {
  "method": "PUT",
  "path": "/fx-rates",
  "contract": "finance",
  "summary": "Set a rate",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "FxRate",
  "responds": "FxRate"
 },
 "setRefundPolicy": {
  "method": "PUT",
  "path": "/venues/{venueId}/refund-policy",
  "contract": "orders",
  "summary": "Set a venue's refund policy",
  "permission": "REGION_CONFIGURE",
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
  "requestBody": "RefundPolicy",
  "responds": "RefundPolicy"
 },
 "setVenueSettings": {
  "method": "PUT",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Set support hours, quiet hours, segregated access and alerting",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "VenueSettings",
  "responds": "VenueSettings"
 },
 "updateAccount": {
  "method": "PATCH",
  "path": "/accounts/{accountId}",
  "contract": "finance",
  "summary": "Rename, remap or deactivate an account",
  "permission": "ACCOUNT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Account"
 },
 "updateTaxCode": {
  "method": "PATCH",
  "path": "/tax-codes/{taxCodeId}",
  "contract": "finance",
  "summary": "Amend a tax code",
  "permission": "TAX_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TaxCode"
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
 "Account": {
  "x-ticvai-persistence": "ledger.account",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "type",
   "legalEntityId",
   "isPostable",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "externalCode": {
    "type": "string",
    "nullable": true,
    "description": "Code in the client's own chart. Used on export so their team sees their codes."
   },
   "isSuspense": {
    "type": "boolean",
    "default": false,
    "description": "5.7.x. **Where a posting with no account mapping goes.** Today it has no destination, and a posting event that cannot be booked is a posting event that is silently dropped.\n**A suspense balance is a work queue, not a resting place.** It should trend to zero, and a balance that grows is the signal that a mapping is missing — which is the whole reason for having one rather than refusing the posting.\n"
   },
   "subType": {
    "type": "string",
    "nullable": true,
    "description": "5.7.27. **`AccountType` stays a closed enum of asset, liability, equity, revenue and expense because that is correct accounting**, and a venue wanting *Deferred Revenue — Annual Pass* is asking for a sub-type rather than a sixth type.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "How a venue groups accounts for its own reporting. Free-form, and outside the type."
   },
   "notes": {
    "type": "string",
    "nullable": true,
    "description": "5.7.27. Annotations on the account, which an auditor reads before the balance."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "type": {
    "$ref": "#/components/schemas/AccountType"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "isPostable": {
    "type": "boolean",
    "description": "False for parent accounts, which aggregate only."
   },
   "isActive": {
    "type": "boolean"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "AccountMapping": {
  "x-ticvai-persistence": "ledger.account_mapping",
  "type": "object",
  "required": [
   "eventType",
   "debitAccountId",
   "creditAccountId"
  ],
  "properties": {
   "eventType": {
    "$ref": "#/components/schemas/PostingEventType"
   },
   "debitAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "creditAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null applies the mapping to every venue in the region."
   }
  }
 },
 "AccountType": {
  "type": "string",
  "enum": [
   "asset",
   "liability",
   "equity",
   "revenue",
   "expense"
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
 "CostCenter": {
  "x-ticvai-persistence": "ledger.cost_center",
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
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "CreateAccountRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "type",
   "legalEntityId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9._-]+$"
   },
   "externalCode": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "type": {
    "$ref": "#/components/schemas/AccountType"
   },
   "parentId": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "isPostable": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "CreateJournalEntryRequest": {
  "type": "object",
  "required": [
   "id",
   "fiscalPeriodId",
   "description",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "postingDate": {
    "type": "string",
    "format": "date"
   },
   "description": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "reference": {
    "type": "string",
    "maxLength": 128
   },
   "lines": {
    "type": "array",
    "minItems": 2,
    "items": {
     "$ref": "#/components/schemas/JournalLine"
    }
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
 "CreateTaxCodeRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "countryCode",
   "rate",
   "effectiveFrom",
   "accountId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$"
   },
   "rate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "compoundOnTaxCodeId": {
    "type": "string",
    "format": "uuid"
   },
   "isInclusive": {
    "type": "boolean",
    "default": false
   },
   "accountId": {
    "type": "string",
    "format": "uuid"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   }
  }
 },
 "DeferredRevenueReport": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asAt",
   "total",
   "buckets"
  ],
  "properties": {
   "asAt": {
    "type": "string",
    "format": "date"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "buckets": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "label",
      "amount",
      "itemCount"
     ],
     "properties": {
      "label": {
       "type": "string",
       "description": "Ageing band by expected recognition date."
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "itemCount": {
       "type": "integer"
      },
      "method": {
       "$ref": "#/components/schemas/RecognitionMethod"
      }
     }
    }
   }
  }
 },
 "DeliveryLocation": {
  "type": "object",
  "x-ticvai-persistence": "fnb.delivery_location",
  "required": [
   "id",
   "venueId",
   "kind",
   "label",
   "isServiceable"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/DeliveryLocationKind"
   },
   "label": {
    "type": "string",
    "description": "What a runner is told. \"Cabana 12\", \"Row H Seat 4\", \"Lawn — north gate\"."
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "tableId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set where the location is a restaurant table, so it shares table state."
   },
   "seatId": {
    "type": "string",
    "nullable": true,
    "description": "Set where the seat is the address. References the seat map."
   },
   "servingOutletIds": {
    "type": "array",
    "description": "Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an address.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "isServiceable": {
    "type": "boolean",
    "description": "False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift.\n"
   },
   "unserviceableReason": {
    "type": "string",
    "nullable": true
   },
   "walkTimeMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen.\n"
   }
  }
 },
 "DeliveryLocationKind": {
  "type": "string",
  "description": "4.6.26. One concept, because a runner needs one instruction.",
  "enum": [
   "table",
   "seat",
   "cabana",
   "sunbed",
   "poolside",
   "box",
   "suite",
   "lawn",
   "collectionPoint",
   "namedLocation"
  ]
 },
 "DiningOutlet": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over outlet, menu and table state",
  "required": [
   "outletId",
   "name",
   "kind",
   "isOpenNow",
   "orderingMethod"
  ],
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "cuisine": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "isOpenNow": {
    "type": "boolean"
   },
   "opensAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closesAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "orderingMethod": {
    "$ref": "#/components/schemas/GuestOrderingMethod"
   },
   "estimatedWaitMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "From current kitchen ticket volume, not a fixed figure. Null where the outlet has no KDS reporting — an invented wait time is worse than none.\n"
   },
   "imageAssetRef": {
    "type": "string",
    "nullable": true
   },
   "menuId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
 "FiscalPeriod": {
  "x-ticvai-persistence": "ledger.fiscal_period",
  "type": "object",
  "required": [
   "id",
   "legalEntityId",
   "name",
   "startDate",
   "endDate",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "startDate": {
    "type": "string",
    "format": "date"
   },
   "endDate": {
    "type": "string",
    "format": "date"
   },
   "status": {
    "$ref": "#/components/schemas/PeriodStatus"
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "FxRate": {
  "type": "object",
  "x-ticvai-persistence": "ledger.fx_rate",
  "required": [
   "fromCurrency",
   "toCurrency",
   "rate",
   "purpose",
   "effectiveFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "fromCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "toCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "rate": {
    "type": "number",
    "description": "Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly.\n"
   },
   "purpose": {
    "$ref": "#/components/schemas/FxRatePurpose"
   },
   "source": {
    "$ref": "#/components/schemas/FxRateSource"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate.\n"
   },
   "setByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true,
    "description": "The provider's own identifier for this quote. **What makes a rate reproducible** — an auditor asking why a payment converted at 3.6725 gets an answer that is checkable against the source rather than a number somebody typed."
   },
   "fetchedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the rate was pulled. **Distinct from `effectiveFrom`**, which is when it applies — a rate fetched at 06:00 for a business day starting at 00:00 has two different times and conflating them makes a late feed look like a backdated rate."
   }
  }
 },
 "FxRatePurpose": {
  "type": "string",
  "description": "A venue does not accept dollars at the rate it books an intercompany balance at. Separating them is what stops a spread on the counter appearing as a loss in the accounts.\n",
  "enum": [
   "tender",
   "interEntity",
   "reporting",
   "revaluation"
  ]
 },
 "FxRateSource": {
  "type": "string",
  "description": "**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.",
  "enum": [
   "manual",
   "uaeCentralBank",
   "ecb",
   "openExchangeRates",
   "cardScheme",
   "provider"
  ]
 },
 "GuestOrderingMethod": {
  "x-ticvai-persistence": "none — enum",
  "type": "string",
  "description": "How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting.\n",
  "enum": [
   "tableService",
   "appToTable",
   "appToCollect",
   "counterOnly",
   "notAvailable"
  ]
 },
 "JournalEntry": {
  "x-ticvai-persistence": "ledger.journal_entry + ledger.journal_line",
  "type": "object",
  "required": [
   "id",
   "entryNumber",
   "fiscalPeriodId",
   "status",
   "source",
   "description",
   "lines",
   "totalDebit",
   "totalCredit",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "entryNumber": {
    "type": "string"
   },
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "$ref": "#/components/schemas/JournalStatus"
   },
   "source": {
    "$ref": "#/components/schemas/JournalSource"
   },
   "sourceId": {
    "type": "string",
    "nullable": true,
    "description": "The order, refund or run that generated this entry."
   },
   "description": {
    "type": "string"
   },
   "reference": {
    "type": "string",
    "nullable": true
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/JournalLine"
    }
   },
   "totalDebit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "postedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reversalOfEntryId": {
    "type": "string",
    "nullable": true
   },
   "reversedByEntryId": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "postedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "JournalLine": {
  "type": "object",
  "required": [
   "accountId",
   "debit",
   "credit"
  ],
  "properties": {
   "accountId": {
    "type": "string",
    "format": "uuid"
   },
   "debit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "credit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "costCenterId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "description": {
    "type": "string",
    "maxLength": 500
   }
  }
 },
 "JournalSource": {
  "type": "string",
  "enum": [
   "manual",
   "order",
   "refund",
   "void",
   "shift",
   "recognition",
   "settlement",
   "variance",
   "reversal"
  ]
 },
 "JournalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pendingApproval",
   "posted",
   "reversed"
  ]
 },
 "LegalEntity": {
  "x-ticvai-persistence": "ledger.legal_entity",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "countryCode",
   "currency",
   "currencyScale",
   "fiscalYearStartMonth"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$"
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
   "taxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "fiscalYearStartMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 12
   },
   "regionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
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
 "PeriodCloseResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fiscalPeriodId",
   "dryRun",
   "passed",
   "checks"
  ],
  "properties": {
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "dryRun": {
    "type": "boolean"
   },
   "passed": {
    "type": "boolean"
   },
   "checks": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "check",
      "passed"
     ],
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "trialBalanceBalances",
        "noUnapprovedJournals",
        "noOpenShifts",
        "settlementsReconciled",
        "recognitionRunComplete",
        "priorPeriodClosed",
        "varianceExceptionsReviewed"
       ]
      },
      "passed": {
       "type": "boolean"
      },
      "detail": {
       "type": "string"
      },
      "blockingCount": {
       "type": "integer"
      }
     }
    }
   }
  }
 },
 "PeriodStatus": {
  "type": "string",
  "enum": [
   "open",
   "closing",
   "closed"
  ]
 },
 "PostingEventType": {
  "type": "string",
  "description": "Every event that generates a ledger posting.",
  "enum": [
   "ticketRevenue",
   "fnbRevenue",
   "retailRevenue",
   "rentalRevenue",
   "taxPayable",
   "cashReceived",
   "cardReceived",
   "walletReceived",
   "refundIssued",
   "voidReversal",
   "deferredRevenue",
   "recognisedRevenue",
   "breakageRevenue",
   "priceVariance",
   "cashOverShort",
   "settlementFee",
   "settlementClearing"
  ]
 },
 "PriceVariance": {
  "x-ticvai-persistence": "ledger.price_variance",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "orderLineId",
   "venueId",
   "quotedPrice",
   "serverPrice",
   "variance",
   "isException",
   "occurredAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "orderLineId": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "quotedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "serverPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "catalogueBundleVersion": {
    "type": "string",
    "nullable": true,
    "description": "The bundle the terminal priced from. Turns \"the price was wrong\" into \"the terminal was two bundles behind\", which is actionable.\n"
   },
   "isException": {
    "type": "boolean",
    "description": "Above the venue's configured variance threshold."
   },
   "reviewStatus": {
    "$ref": "#/components/schemas/VarianceReviewStatus"
   },
   "reviewOutcome": {
    "type": "string",
    "nullable": true
   },
   "reviewedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "journalEntryId": {
    "type": "string",
    "nullable": true
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "RecognitionMethod": {
  "type": "string",
  "enum": [
   "immediate",
   "onRedemption",
   "straightLine",
   "perVisit",
   "onExpiry"
  ]
 },
 "RecognitionRunResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fiscalPeriodId",
   "dryRun",
   "recognisedTotal",
   "breakageTotal",
   "entryCount"
  ],
  "properties": {
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "dryRun": {
    "type": "boolean"
   },
   "recognisedTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "breakageTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "entryCount": {
    "type": "integer"
   },
   "byMethod": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "method": {
       "$ref": "#/components/schemas/RecognitionMethod"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "itemCount": {
       "type": "integer"
      }
     }
    }
   },
   "journalEntryIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "RecognitionSchedule": {
  "x-ticvai-persistence": "ledger.recognition_schedule",
  "type": "object",
  "required": [
   "id",
   "name",
   "method",
   "productKinds"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "method": {
    "$ref": "#/components/schemas/RecognitionMethod"
   },
   "priority": {
    "type": "integer",
    "default": 100,
    "description": "**Two schedules may both claim a product kind and nothing resolved which wins** — a silent double-recognition, which is the worst kind of accounting defect because the numbers look plausible.\nLowest priority wins, and **two schedules at the same priority claiming the same kind is refused at save** rather than resolved at run time.\n"
   },
   "recognitionSite": {
    "type": "string",
    "enum": [
     "sale",
     "admission",
     "consumption"
    ],
    "default": "sale",
    "description": "**Where revenue is earned, which is not always where it was sold.** A ticket sold at one venue and admitted at another earns at the gate, and recognising at the sale site puts the revenue in the wrong entity's books.\n`consumption` is for stored value — a wallet top-up is not revenue until it is spent.\n"
   },
   "frequency": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     "onEvent",
     "onPeriodClose"
    ],
    "default": "onPeriodClose",
    "description": "**Driven by the schedule rather than by whoever runs the job.** Recognition that happens when somebody remembers is recognition with no cut-off.\n"
   },
   "revalidateOnValidityChange": {
    "type": "boolean",
    "default": true,
    "description": "**Changing an entitlement's validity did not re-time its deferred balance.** A pass extended by three months has three more months of deferral, and a schedule that ignores that recognises revenue the venue has not yet earned.\n"
   },
   "productKinds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "deferredAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "recognisedAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "breakageAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "noShowTrigger": {
    "type": "string",
    "nullable": true,
    "enum": [
     "performanceEnd",
     "validityEnd",
     "none"
    ],
    "description": "8.1.1. **A no-show is breakage with a known moment**, and the mechanism already existed — `breakageAfterDays` moves deferred revenue to earned after a period. A ticket for a performance that has finished does not need a waiting period: **the guest cannot arrive any more.**\n`performanceEnd` recognises when the performance completes. `validityEnd` recognises when an open-dated entitlement lapses, which is where `breakageAfterDays` still applies.\n**`none` keeps the current behaviour** — recognise on the schedule and nothing else — so no existing schedule changes.\n"
   },
   "noShowAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where no-show revenue lands. **Separate from `recognisedAccountId` by default**, because revenue from a guest who came and revenue from one who did not are different lines to whoever reads the P&L — and 8.1.2 asks for a report on exactly that distinction.\n"
   },
   "breakageAfterDays": {
    "type": "integer",
    "nullable": true,
    "description": "Days after expiry at which unredeemed value becomes breakage."
   },
   "isActive": {
    "type": "boolean"
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
 "RefundPolicy": {
  "x-ticvai-persistence": "orders.refund_policy",
  "type": "object",
  "description": "Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n",
  "required": [
   "venueId",
   "selfAuthoriseLimit",
   "requiresApprovalAbove"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "selfAuthoriseLimit": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"
   },
   "requiresSecondUserAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"
   },
   "requiresApprovalAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above this, an ORDER_REFUND_APPROVE holder must approve."
   },
   "timeBands": {
    "type": "array",
    "description": "Refundable percentage by time before the performance. Evaluated most-specific first.\n",
    "items": {
     "type": "object",
     "required": [
      "hoursBefore",
      "percentage"
     ],
     "properties": {
      "hoursBefore": {
       "type": "integer",
       "minimum": 0
      },
      "percentage": {
       "type": "number",
       "minimum": 0,
       "maximum": 100
      }
     }
    }
   },
   "allowPartial": {
    "type": "boolean",
    "default": true
   },
   "refundWindowDays": {
    "type": "integer",
    "nullable": true
   },
   "varianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n"
   }
  }
 },
 "TaxCode": {
  "x-ticvai-persistence": "ledger.tax_code",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "countryCode",
   "rate",
   "effectiveFrom",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$"
   },
   "appliesTo": {
    "type": "array",
    "description": "**What this code covers, and `donation` is why the field exists** (CF-84). Donation tax treatment varies by jurisdiction — **0% is a valid rate, not an absence of one** — and it is set here rather than assumed in the posting.\nThe liability-account posting stays the default and is no longer the only option.\n",
    "items": {
     "type": "string",
     "enum": [
      "goods",
      "services",
      "admission",
      "food",
      "accommodation",
      "donation",
      "gratuity",
      "fee"
     ]
    }
   },
   "rate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "compoundOnTaxCodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "When set, this tax applies to the base **plus** the referenced tax, not to the base alone. Ordering is explicit rather than implied.\n"
   },
   "isInclusive": {
    "type": "boolean",
    "description": "True when the displayed price already contains this tax."
   },
   "accountId": {
    "type": "string",
    "format": "uuid"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "TaxExemption": {
  "x-ticvai-persistence": "ledger.tax_exemption",
  "type": "object",
  "required": [
   "id",
   "scope",
   "taxCodeId",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "scope": {
    "type": "string",
    "enum": [
     "account",
     "productKind",
     "channel",
     "legalEntity"
    ]
   },
   "scopeRef": {
    "type": "string",
    "description": "Identifier of the exempt subject, matching `scope`."
   },
   "taxCodeId": {
    "type": "string",
    "format": "uuid"
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "certificateReference": {
    "type": "string",
    "nullable": true
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   }
  }
 },
 "TrialBalance": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fiscalPeriodId",
   "isBalanced",
   "totalDebit",
   "totalCredit",
   "accounts"
  ],
  "properties": {
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "isBalanced": {
    "type": "boolean",
    "description": "False indicates a defect, not a business condition. Double-entry cannot be unbalanced by legitimate activity.\n"
   },
   "totalDebit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "accounts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "accountId",
      "accountCode",
      "accountName",
      "debit",
      "credit",
      "balance"
     ],
     "properties": {
      "accountId": {
       "type": "string",
       "format": "uuid"
      },
      "accountCode": {
       "type": "string"
      },
      "accountName": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/AccountType"
      },
      "debit": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "credit": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "balance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "VarianceReviewStatus": {
  "type": "string",
  "enum": [
   "notRequired",
   "pendingReview",
   "reviewed"
  ]
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string"
     },
     "to": {
      "type": "string"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string"
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       false,
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": false,
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   }
  }
 }
}
```
