# WS31 — Order   Reservation Management board 1

**10 screens · 10 operations · 15 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ORDER_CREATE, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-304` | Order & Reservation Command Center | listDetail | 1 | 0 | — |
| `BO-305` | Order Detail & Transaction Workspace | commandCentre | 1 | 0 | — |
| `BO-306` | Reservation & Hold Policy Configuration | configEditor | 1 | 0 | — |
| `BO-307` | Order & Reservation Status Lifecycle Configuration | configEditor | 1 | 0 | — |
| `BO-308` | Order Creation & Source/Channel Configuration | configEditor | 1 | 0 | — |
| `BO-309` | Customer, Guest & Account Assignment | configEditor | 1 | 0 | — |
| `BO-310` | Order Line, Product & Entitlement Composition | configEditor | 1 | 0 | — |
| `BO-311` | Capacity Reservation & Inventory Commitment | listDetail | 1 | 0 | — |
| `BO-312` | Reservation Confirmation, Expiry & Fulfillment Readiness | configEditor | 1 | 0 | — |
| `BO-313` | Order Lifecycle Timeline, SLA, Exceptions & AI Operations | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-304, BO-311, BO-313 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-304",
  "name": "Order & Reservation Command Center",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.1",
   "page": 3
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-reservation-command-center-bo-304",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderReservationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-305",
    "BO-306",
    "BO-307",
    "BO-308",
    "BO-309",
    "BO-310",
    "BO-311",
    "BO-312",
    "BO-313"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-305",
     "trigger": "Works in Order Detail & Transaction Workspace",
     "provenance": "flow F140 step 1→2",
     "operation": "listOrderReservation"
    },
    {
     "to": "BO-306",
     "trigger": "Works in Reservation & Hold Policy Configuration",
     "provenance": "flow F140 step 3→4",
     "operation": "listOrderReservation"
    },
    {
     "to": "BO-307",
     "trigger": "Works in Order & Reservation Status Lifecycle Configuration",
     "provenance": "flow F140 step 5→6",
     "operation": "listOrderReservation"
    },
    {
     "to": "BO-308",
     "trigger": "Works in Order Creation & Source/Channel Configuration",
     "provenance": "flow F140 step 7→8",
     "operation": "listOrderReservation"
    },
    {
     "to": "BO-309",
     "trigger": "Works in Customer, Guest & Account Assignment",
     "provenance": "flow F140 step 9→10",
     "operation": "listOrderReservation"
    },
    {
     "to": "BO-310",
     "trigger": "Works in Order Line, Product & Entitlement Composition",
     "provenance": "flow F140 step 11→12",
     "operation": "listOrderReservation"
    },
    {
     "to": "BO-311",
     "trigger": "Works in Capacity Reservation & Inventory Commitment",
     "provenance": "flow F140 step 13→14",
     "operation": "listOrderReservation"
    },
    {
     "to": "BO-312",
     "trigger": "Works in Reservation Confirmation, Expiry & Fulfillment Readiness",
     "provenance": "flow F140 step 15→16",
     "operation": "listOrderReservation"
    },
    {
     "to": "BO-313",
     "trigger": "Works in Order Lifecycle Timeline, SLA, Exceptions & AI Operations",
     "provenance": "flow F140 step 17→18",
     "operation": "listOrderReservation"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the central operational workspace for searching, monitoring, opening, and managing every order and reservation across TICVAI.",
  "purposeNote": "Authorized users can locate and monitor any TICVAI order/reservation across all channels from one centralized operational workspace.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every order reservation",
       "columns": [
        "OrderReservationCommandCenterView.ordersToday",
        "OrderReservationCommandCenterView.confirmedOrders",
        "OrderReservationCommandCenterView.activeReservations",
        "OrderReservationCommandCenterView.temporaryHolds",
        "OrderReservationCommandCenterView.pendingPayment",
        "OrderReservationCommandCenterView.expiringReservations",
        "OrderReservationCommandCenterView.failedOrders",
        "OrderReservationCommandCenterView.partiallyFulfilled",
        "OrderReservationCommandCenterView.completedOrders",
        "OrderReservationCommandCenterView.cancelledOrders",
        "OrderReservationCommandCenterView.ordersRequiringAttention",
        "OrderReservationCommandCenterView.grossOrderValue",
        "OrderReservationCommandCenterView.orderId",
        "OrderReservationCommandCenterView.reservationId",
        "OrderReservationCommandCenterView.customer",
        "OrderReservationCommandCenterView.channel",
        "OrderReservationCommandCenterView.venue",
        "OrderReservationCommandCenterView.productEvent",
        "OrderReservationCommandCenterView.orderValue",
        "OrderReservationCommandCenterView.paymentStatus",
        "OrderReservationCommandCenterView.reservationStatus",
        "OrderReservationCommandCenterView.fulfillmentStatus",
        "OrderReservationCommandCenterView.createdDate",
        "OrderReservationCommandCenterView.expiry",
        "OrderReservationCommandCenterView.ownerAgent"
       ],
       "bindsTo": "OrderReservationCommandCenterView",
       "operation": "listOrderReservation",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 3 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order reservation",
       "bindsTo": "OrderReservationCommandCenterView",
       "columns": [
        "OrderReservationCommandCenterView.ordersToday",
        "OrderReservationCommandCenterView.confirmedOrders",
        "OrderReservationCommandCenterView.activeReservations",
        "OrderReservationCommandCenterView.temporaryHolds",
        "OrderReservationCommandCenterView.pendingPayment",
        "OrderReservationCommandCenterView.expiringReservations",
        "OrderReservationCommandCenterView.failedOrders",
        "OrderReservationCommandCenterView.partiallyFulfilled",
        "OrderReservationCommandCenterView.completedOrders",
        "OrderReservationCommandCenterView.cancelledOrders",
        "OrderReservationCommandCenterView.ordersRequiringAttention",
        "OrderReservationCommandCenterView.grossOrderValue",
        "OrderReservationCommandCenterView.orderId",
        "OrderReservationCommandCenterView.reservationId",
        "OrderReservationCommandCenterView.customer",
        "OrderReservationCommandCenterView.channel",
        "OrderReservationCommandCenterView.venue",
        "OrderReservationCommandCenterView.productEvent",
        "OrderReservationCommandCenterView.orderValue",
        "OrderReservationCommandCenterView.paymentStatus",
        "OrderReservationCommandCenterView.reservationStatus",
        "OrderReservationCommandCenterView.fulfillmentStatus",
        "OrderReservationCommandCenterView.createdDate",
        "OrderReservationCommandCenterView.expiry",
        "OrderReservationCommandCenterView.ownerAgent"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Search using”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 3 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Open Order, Open Reservation, Extend Hold, Resend Confirmation, Collect Payment, Add Note, View Timeline. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 3 §Depending on permission"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order reservation list.",
   "error": "Could not load. Names which read failed and leaves the order reservation untouched.",
   "emptyFirstRun": "No order reservation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order reservation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderReservation",
    "contract": "orders",
    "purpose": "Order & Reservation Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OrderReservationCommandCenterView.ordersToday",
    "OrderReservationCommandCenterView.confirmedOrders",
    "OrderReservationCommandCenterView.activeReservations",
    "OrderReservationCommandCenterView.temporaryHolds",
    "OrderReservationCommandCenterView.pendingPayment",
    "OrderReservationCommandCenterView.expiringReservations"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-304"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 3. 25 of 25 labels bound to a contract property; 32 of 57 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-305",
  "name": "Order Detail & Transaction Workspace",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.2",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-detail-transaction-workspace-bo-305",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderDetailTransactionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-304",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F140 step 2→3",
     "operation": "setOrderDetailTransaction"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display; Show) and a per-row directory (§Each line should display) — counts over a population, then the population",
  "purpose": "Provide the authoritative 360-degree view of a single order. This should become one of the most important operational screens in TICVAI.",
  "purposeNote": "The complete commercial, operational, customer, payment, ticket and fulfillment context of an order can be understood from one screen.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Order Number",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.orderNumber"
      },
      {
       "kind": "metricTile",
       "label": "Order Date/Time",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Order Status",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.orderStatus"
      },
      {
       "kind": "metricTile",
       "label": "Reservation Status",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.reservationStatus"
      },
      {
       "kind": "metricTile",
       "label": "Customer",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.customer"
      },
      {
       "kind": "metricTile",
       "label": "Channel",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.channel"
      },
      {
       "kind": "metricTile",
       "label": "Sales Location",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.salesLocation"
      },
      {
       "kind": "metricTile",
       "label": "Cashier/Agent",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.cashierAgent"
      },
      {
       "kind": "metricTile",
       "label": "Currency",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.currency"
      },
      {
       "kind": "metricTile",
       "label": "Total",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.total"
      },
      {
       "kind": "metricTile",
       "label": "Payment Status",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.paymentStatus"
      },
      {
       "kind": "metricTile",
       "label": "Fulfillment Status",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Display",
       "bindsTo": "OrderDetailTransactionWorkspaceView.fulfillmentStatus"
      },
      {
       "kind": "metricTile",
       "label": "Tickets",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.tickets"
      },
      {
       "kind": "metricTile",
       "label": "Reservations",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.reservations"
      },
      {
       "kind": "metricTile",
       "label": "Payments",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.payments"
      },
      {
       "kind": "metricTile",
       "label": "Refunds",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.refunds"
      },
      {
       "kind": "metricTile",
       "label": "Invoices",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.invoices"
      },
      {
       "kind": "metricTile",
       "label": "Credentials",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.credentials"
      },
      {
       "kind": "metricTile",
       "label": "Membership",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.membership"
      },
      {
       "kind": "metricTile",
       "label": "Waivers",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.waivers"
      },
      {
       "kind": "metricTile",
       "label": "Related Orders",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Show",
       "bindsTo": "OrderDetailTransactionWorkspaceView.relatedOrders"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every order detail transaction",
       "columns": [
        "OrderDetailTransactionWorkspaceView.product",
        "OrderDetailTransactionWorkspaceView.ticketType",
        "OrderDetailTransactionWorkspaceView.event",
        "OrderDetailTransactionWorkspaceView.performance",
        "OrderDetailTransactionWorkspaceView.date",
        "OrderDetailTransactionWorkspaceView.timeslot",
        "OrderDetailTransactionWorkspaceView.quantity",
        "OrderDetailTransactionWorkspaceView.personType",
        "OrderDetailTransactionWorkspaceView.seat",
        "OrderDetailTransactionWorkspaceView.unitPrice",
        "OrderDetailTransactionWorkspaceView.discount",
        "OrderDetailTransactionWorkspaceView.tax",
        "OrderDetailTransactionWorkspaceView.fee",
        "OrderDetailTransactionWorkspaceView.total",
        "OrderDetailTransactionWorkspaceView.ticketStatus"
       ],
       "bindsTo": "OrderDetailTransactionWorkspaceView",
       "operation": "setOrderDetailTransaction",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Each line should display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order detail transaction",
       "bindsTo": "OrderDetailTransactionWorkspaceView",
       "columns": [
        "OrderDetailTransactionWorkspaceView.product",
        "OrderDetailTransactionWorkspaceView.ticketType",
        "OrderDetailTransactionWorkspaceView.event",
        "OrderDetailTransactionWorkspaceView.performance",
        "OrderDetailTransactionWorkspaceView.date",
        "OrderDetailTransactionWorkspaceView.timeslot",
        "OrderDetailTransactionWorkspaceView.quantity",
        "OrderDetailTransactionWorkspaceView.personType",
        "OrderDetailTransactionWorkspaceView.seat",
        "OrderDetailTransactionWorkspaceView.unitPrice",
        "OrderDetailTransactionWorkspaceView.discount",
        "OrderDetailTransactionWorkspaceView.tax",
        "OrderDetailTransactionWorkspaceView.fee",
        "OrderDetailTransactionWorkspaceView.total",
        "OrderDetailTransactionWorkspaceView.ticketStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Order Total”, “Internal Notes”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 5 §Each line should display"
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
       "provenance": "contract operation setOrderDetailTransaction"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order detail transaction list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the order detail transaction untouched.",
   "emptyFirstRun": "No order detail transaction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order detail transaction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setOrderDetailTransaction",
    "contract": "orders",
    "purpose": "Order Detail & Transaction Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setOrderDetailTransaction"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-305"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 5. 35 of 35 labels bound to a contract property; 36 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-306",
  "name": "Reservation & Hold Policy Configuration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.3",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/reservation-hold-policy-configuration-bo-306",
   "component": "apps/venue-management-web/src/routes/orders-money/ReservationHoldPolicyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-304",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F140 step 4→5",
     "operation": "setReservationHoldPolicy"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how TICVAI temporarily reserves inventory before an order is fully confirmed.",
  "purposeNote": "overselling or orphaning inventory.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Cart Hold, Checkout Hold, Manual Hold, Payment Hold, Seat Hold, Inventory Hold. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 7 §Support"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Performance",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Ticket Type",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer Segment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Reservation Type",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Extension Allowed",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Extensions",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Extension Duration",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authorized Role",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval Requirement",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Cart Hold",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Checkout Hold",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Manual Hold",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Hold",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Seat Hold",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Inventory Hold",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 7 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation hold policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reservation hold policy untouched.",
   "emptyFirstRun": "No reservation hold policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setReservationHoldPolicy",
    "contract": "orders",
    "purpose": "Reservation & Hold Policy Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setReservationHoldPolicy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-306"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 18 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-307",
  "name": "Order & Reservation Status Lifecycle Configuration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.4",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-reservation-status-lifecycle-configuration-bo-307",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderReservationStatusLifecycleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-304",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F140 step 6→7",
     "operation": "setOrderReservationStatus"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For each transition define) and no display directory — it is settings, not a population",
  "purpose": "Define the governed state machine for orders and reservations. SoftLab should not hard-code status transitions independently in every channel.",
  "purposeNote": "Every order and reservation follows a centralized, controlled and auditable lifecycle regardless of originating sales channel.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "From Status",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 9 §For each transition define"
      },
      {
       "kind": "selectField",
       "label": "Trigger",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 9 §For each transition define"
      },
      {
       "kind": "selectField",
       "label": "Required Conditions",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 9 §For each transition define"
      },
      {
       "kind": "selectField",
       "label": "User/System Action",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 9 §For each transition define"
      },
      {
       "kind": "selectField",
       "label": "Allowed Role",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 9 §For each transition define"
      },
      {
       "kind": "selectField",
       "label": "Integration Requirement",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 9 §For each transition define"
      },
      {
       "kind": "selectField",
       "label": "Notification",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 9 §For each transition define"
      },
      {
       "kind": "selectField",
       "label": "Audit Requirement",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 9 §For each transition define"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setOrderReservationStatus"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order reservation status configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the order reservation status untouched.",
   "emptyFirstRun": "No order reservation status configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setOrderReservationStatus",
    "contract": "orders",
    "purpose": "Order & Reservation Status Lifecycle Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setOrderReservationStatus"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-307"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 8 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-308",
  "name": "Order Creation & Source/Channel Configuration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.5",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-creation-source-channel-configuration-bo-308",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderCreationSourceChannelConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-304",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F140 step 8→9",
     "operation": "createOrderSourceChannel"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure numbering rules; Configure whether a channel may) and no display directory — it is settings, not a population",
  "purpose": "Configure how orders can originate from different TICVAI sales channels while using one common transaction engine.",
  "purposeNote": "Orders from all TICVAI and external sales channels are created consistently while preserving complete source and attribution metadata.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: OTA Booking Reference, Reseller Order ID. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 10 §Support partner identifiers such as"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Sub-Channel",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Sales Location",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Terminal",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Device",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Agent",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Partner",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reseller",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Campaign",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Affiliate",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "API Consumer",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "External Reference",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Global Sequence",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure numbering rules"
      },
      {
       "kind": "selectField",
       "label": "Tenant Sequence",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure numbering rules"
      },
      {
       "kind": "selectField",
       "label": "Venue Sequence",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure numbering rules"
      },
      {
       "kind": "selectField",
       "label": "Channel Prefix",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure numbering rules"
      },
      {
       "kind": "selectField",
       "label": "Year/Month Prefix",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure numbering rules"
      },
      {
       "kind": "selectField",
       "label": "Custom Pattern",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure numbering rules"
      },
      {
       "kind": "selectField",
       "label": "Create Reservation",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure whether a channel may"
      },
      {
       "kind": "selectField",
       "label": "Create Immediate Order",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure whether a channel may"
      },
      {
       "kind": "selectField",
       "label": "Create Unpaid Order",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure whether a channel may"
      },
      {
       "kind": "selectField",
       "label": "Create Group Order",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure whether a channel may"
      },
      {
       "kind": "selectField",
       "label": "Hold Inventory",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure whether a channel may"
      },
      {
       "kind": "selectField",
       "label": "Issue Ticket Immediately",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Configure whether a channel may"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "OTA Booking Reference",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Support partner identifiers such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Reseller Order ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 10 §Support partner identifiers such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order creation source configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the order creation source untouched.",
   "emptyFirstRun": "No order creation source configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createOrderSourceChannel",
    "contract": "orders",
    "purpose": "Order Creation & Source/Channel Configuration",
    "trigger": "onAction",
    "invalidates": [
     "createOrderSourceChannel"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-308"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 26 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-309",
  "name": "Customer, Guest & Account Assignment",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.6",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/customer-guest-account-assignment-bo-309",
   "component": "apps/venue-management-web/src/routes/orders-money/CustomerGuestAccountAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-304",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F140 step 10→11",
     "operation": "setCustomerGuestAccount"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Depending on configuration) and no display directory — it is settings, not a population",
  "purpose": "Define how customers are identified and associated with orders/reservations.",
  "purposeNote": "Every order can correctly identify purchaser, attendee, member, corporate or partner relationships without creating unnecessary duplicate customer records.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Registered Customer, Anonymous Sale where permitted, Link Existing, Continue Guest, Review Match. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 11 §Support"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Name",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Email",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Mobile",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Date of Birth",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Customer ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Membership ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Company",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Tax Details",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Depending on configuration"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Guest Checkout",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Registered Customer",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Anonymous Sale where permitted",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Link Existing",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Continue Guest",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Review Match",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 11 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer guest account configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the customer guest account untouched.",
   "emptyFirstRun": "No customer guest account configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCustomerGuestAccount",
    "contract": "orders",
    "purpose": "Customer, Guest & Account Assignment",
    "trigger": "onAction",
    "invalidates": [
     "setCustomerGuestAccount"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-309"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 16 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-310",
  "name": "Order Line, Product & Entitlement Composition",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.7",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-line-product-entitlement-composition-bo-310",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderLineProductEntitlementComposition.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-304",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F140 step 12→13",
     "operation": "listOrderLineProduct"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each line captures) and no display directory — it is settings, not a population",
  "purpose": "Manage the products and commercial components contained within an order.",
  "purposeNote": "entitlements, commercial calculations and fulfillment requirements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Variant",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Person Type",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Performance",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Date",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Timeslot",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Seat",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Entitlement",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Price",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Discount",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Tax",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Fee",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      },
      {
       "kind": "selectField",
       "label": "Fulfillment Method",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 13 §Each line captures"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order line product configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the order line product untouched.",
   "emptyFirstRun": "No order line product configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderLineProduct",
    "contract": "orders",
    "purpose": "Order Line, Product & Entitlement Composition",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-310"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 15 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-311",
  "name": "Capacity Reservation & Inventory Commitment",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.8",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/capacity-reservation-inventory-commitment-bo-311",
   "component": "apps/venue-management-web/src/routes/orders-money/CapacityReservationInventoryCommitment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-304",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F140 step 14→15",
     "operation": "listCapacityReservationInventory"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when and how order activity consumes real capacity/inventory. This is the transactional bridge between the Order Engine and the Capacity/Inventory Engines.",
  "purposeNote": "Order and reservation activity commits and releases capacity consistently without double- selling, lost inventory, or inconsistent transaction states.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 14"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCapacityReservationInventory",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity reservation inventory list.",
   "error": "Could not load. Names which read failed and leaves the capacity reservation inventory untouched.",
   "emptyFirstRun": "No capacity reservation inventory yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the capacity reservation inventory are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCapacityReservationInventory",
    "contract": "orders",
    "purpose": "Capacity Reservation & Inventory Commitment",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CapacityReservationInventoryCommitmentView.temporaryAvailabilityProtection",
    "CapacityReservationInventoryCommitmentView.confirmedInventoryConsumption",
    "CapacityReservationInventoryCommitmentView.generalAdmissionCapacity",
    "CapacityReservationInventoryCommitmentView.seatInventory",
    "CapacityReservationInventoryCommitmentView.timeslotCapacity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-311"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-312",
  "name": "Reservation Confirmation, Expiry & Fulfillment Readiness",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.9",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/reservation-confirmation-expiry-fulfillment-readiness-bo-312",
   "component": "apps/venue-management-web/src/routes/orders-money/ReservationConfirmationExpiryFulfillmentReadines.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-304",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F140 step 16→17",
     "operation": "listReservationConfirmationExpiry"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure combinations of) and no display directory — it is settings, not a population",
  "purpose": "Determine when a reservation becomes a confirmed order and when it is ready for ticket/media fulfillment.",
  "purposeNote": "and compliance conditions have been satisfied.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Payment Complete",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      },
      {
       "kind": "selectField",
       "label": "Deposit Received",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      },
      {
       "kind": "selectField",
       "label": "Credit Approved",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      },
      {
       "kind": "selectField",
       "label": "Capacity Confirmed",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      },
      {
       "kind": "selectField",
       "label": "Customer Data Complete",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      },
      {
       "kind": "selectField",
       "label": "Required Waiver Complete",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      },
      {
       "kind": "selectField",
       "label": "Required Approval Complete",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      },
      {
       "kind": "selectField",
       "label": "Partner Confirmation Received",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      },
      {
       "kind": "selectField",
       "label": "Example — B2C",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 15 §Configure combinations of"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation confirmation expiry configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reservation confirmation expiry untouched.",
   "emptyFirstRun": "No reservation confirmation expiry configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReservationConfirmationExpiry",
    "contract": "orders",
    "purpose": "Reservation Confirmation, Expiry & Fulfillment Readiness",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-312"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 9 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-313",
  "name": "Order Lifecycle Timeline, SLA, Exceptions & AI Operations",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "1",
   "number": "12.1.10",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-lifecycle-timeline-sla-exceptions-ai-operations-bo-313",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderLifecycleTimelineSlaExceptionsAiOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-304"
   ],
   "exitTo": [
    "BO-304"
   ],
   "inferred": false,
   "notes": "**Reached from BO-304, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Provide complete lifecycle visibility and proactively identify orders/reservations that require operational intervention.",
  "purposeNote": "Operations teams can reconstruct the complete lifecycle of an order, identify abnormal transactions and safely recover exceptions through controlled actions. Board 1 — Final Screen Register # Backend Screen Core Responsibility 12.1. Central order/reservation",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every order lifecycle timeline",
       "columns": [
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.stuckOrder",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.orphanReservation",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.paymentOrderMismatch",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.capacityMismatch",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.missingCustomerData",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.fulfillmentFailure",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.externalSynchronizationFailure",
        "Duplicate Transaction Risk"
       ],
       "bindsTo": "OrderLifecycleTimelineSlaExceptionsAiOperationsView",
       "operation": "listOrderLifecycleTimeline",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 17 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order lifecycle timeline",
       "bindsTo": "OrderLifecycleTimelineSlaExceptionsAiOperationsView",
       "columns": [
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.stuckOrder",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.orphanReservation",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.paymentOrderMismatch",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.capacityMismatch",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.missingCustomerData",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.fulfillmentFailure",
        "OrderLifecycleTimelineSlaExceptionsAiOperationsView.externalSynchronizationFailure",
        "Duplicate Transaction Risk"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Prioritize by”, “Depending on exception”, “Order & Reservation Command Center”, “Transaction state machine”, “Omnichannel order creation”, “Customer, Guest & Account Assignment”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 17 §Detect"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order lifecycle timeline list.",
   "error": "Could not load. Names which read failed and leaves the order lifecycle timeline untouched.",
   "emptyFirstRun": "No order lifecycle timeline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order lifecycle timeline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderLifecycleTimeline",
    "contract": "orders",
    "purpose": "Order Lifecycle Timeline, SLA, Exceptions & AI Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OrderLifecycleTimelineSlaExceptionsAiOperationsView.stuckOrder",
    "OrderLifecycleTimelineSlaExceptionsAiOperationsView.orphanReservation",
    "OrderLifecycleTimelineSlaExceptionsAiOperationsView.paymentOrderMismatch",
    "OrderLifecycleTimelineSlaExceptionsAiOperationsView.capacityMismatch",
    "OrderLifecycleTimelineSlaExceptionsAiOperationsView.missingCustomerData",
    "OrderLifecycleTimelineSlaExceptionsAiOperationsView.fulfillmentFailure"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-313"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 17. 7 of 8 labels bound to a contract property; 17 of 93 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createOrderSourceChannel": {
  "method": "POST",
  "path": "/order-source-channel",
  "contract": "orders",
  "summary": "Order Creation & Source/Channel Configuration",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "OrderCreationSourceChannelConfigurationInput",
  "responds": "OrderCreationSourceChannelConfigurationView"
 },
 "listCapacityReservationInventory": {
  "method": "GET",
  "path": "/capacity-reservation-inventory",
  "contract": "orders",
  "summary": "Capacity Reservation & Inventory Commitment",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CapacityReservationInventoryCommitmentView"
 },
 "listOrderLifecycleTimeline": {
  "method": "GET",
  "path": "/order-lifecycle-timeline",
  "contract": "orders",
  "summary": "Order Lifecycle Timeline, SLA, Exceptions & AI Operations",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderLifecycleTimelineSlaExceptionsAiOperationsView"
 },
 "listOrderLineProduct": {
  "method": "GET",
  "path": "/order-line-product",
  "contract": "orders",
  "summary": "Order Line, Product & Entitlement Composition",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderLineProductEntitlementCompositionView"
 },
 "listOrderReservation": {
  "method": "GET",
  "path": "/order-reservation",
  "contract": "orders",
  "summary": "Order & Reservation Command Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "orderNumber",
    "in": "query",
    "required": false
   },
   {
    "name": "reservationNumber",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketNumber",
    "in": "query",
    "required": false
   },
   {
    "name": "customerName",
    "in": "query",
    "required": false
   },
   {
    "name": "email",
    "in": "query",
    "required": false
   },
   {
    "name": "mobile",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipId",
    "in": "query",
    "required": false
   },
   {
    "name": "transactionReference",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "OrderReservationCommandCenterView"
 },
 "listReservationConfirmationExpiry": {
  "method": "GET",
  "path": "/reservation-confirmation-expiry",
  "contract": "orders",
  "summary": "Reservation Confirmation, Expiry & Fulfillment Readiness",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReservationConfirmationExpiryFulfillmentReadinessView"
 },
 "setCustomerGuestAccount": {
  "method": "PUT",
  "path": "/customer-guest-account",
  "contract": "orders",
  "summary": "Customer, Guest & Account Assignment",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "CustomerGuestAccountAssignmentInput",
  "responds": "CustomerGuestAccountAssignmentView"
 },
 "setOrderDetailTransaction": {
  "method": "PUT",
  "path": "/order-detail-transaction",
  "contract": "orders",
  "summary": "Order Detail & Transaction Workspace",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "OrderDetailTransactionWorkspaceInput",
  "responds": "OrderDetailTransactionWorkspaceView"
 },
 "setOrderReservationStatus": {
  "method": "PUT",
  "path": "/order-reservation-statu",
  "contract": "orders",
  "summary": "Order & Reservation Status Lifecycle Configuration",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "OrderReservationStatusLifecycleConfigurationInput",
  "responds": "OrderReservationStatusLifecycleConfigurationView"
 },
 "setReservationHoldPolicy": {
  "method": "PUT",
  "path": "/reservation-hold-policy",
  "contract": "orders",
  "summary": "Reservation & Hold Policy Configuration",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ReservationHoldPolicyConfigurationInput",
  "responds": "ReservationHoldPolicyConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CapacityReservationInventoryCommitmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Capacity Reservation & Inventory Commitment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "temporaryAvailabilityProtection": {
    "type": "string",
    "description": "Temporary availability protection"
   },
   "confirmedInventoryConsumption": {
    "type": "string",
    "description": "Confirmed inventory consumption"
   },
   "generalAdmissionCapacity": {
    "type": "integer",
    "description": "General Admission Capacity"
   },
   "seatInventory": {
    "type": "string",
    "description": "Seat Inventory"
   },
   "timeslotCapacity": {
    "type": "integer",
    "description": "Timeslot Capacity"
   },
   "eventCapacity": {
    "type": "integer",
    "description": "Event Capacity"
   },
   "productInventory": {
    "type": "string",
    "description": "Product Inventory"
   },
   "rentalInventory": {
    "type": "string",
    "description": "Rental Inventory"
   },
   "fBRetailInventoryWhereApplicable": {
    "type": "string",
    "description": "F&B/Retail inventory where applicable"
   },
   "returnAControlledException": {
    "type": "string",
    "description": "return a controlled exception"
   },
   "holdExpires": {
    "type": "string",
    "format": "date-time",
    "description": "Hold Expires"
   },
   "reservationCancels": {
    "type": "string",
    "description": "Reservation Cancels"
   },
   "paymentFailsAccordingToPolicy": {
    "type": "string",
    "description": "Payment Fails according to policy"
   },
   "orderFails": {
    "type": "string",
    "description": "Order Fails"
   },
   "authorizedAmendmentRemovesProduct": {
    "type": "string",
    "description": "Authorized amendment removes product"
   }
  }
 },
 "CustomerGuestAccountAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Customer, Guest & Account Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "guestCheckout": {
    "type": "string",
    "description": "Guest Checkout"
   },
   "registeredCustomer": {
    "type": "string",
    "description": "Registered Customer"
   },
   "member": {
    "type": "string",
    "description": "Member"
   },
   "corporateAccount": {
    "type": "string",
    "description": "Corporate Account"
   },
   "b2bAccount": {
    "type": "string",
    "description": "B2B Account"
   },
   "groupOrganizer": {
    "type": "string",
    "description": "Group Organizer"
   },
   "anonymousSaleWherePermitted": {
    "type": "string",
    "description": "Anonymous Sale where permitted"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "mobile": {
    "type": "string",
    "description": "Mobile"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date-time",
    "description": "Date of Birth"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "company": {
    "type": "string",
    "description": "Company"
   },
   "taxDetails": {
    "type": "string",
    "description": "Tax Details"
   },
   "from": {
    "type": "string",
    "description": "from"
   },
   "continueGuest": {
    "type": "string",
    "description": "Continue Guest"
   },
   "dependingOnPolicy": {
    "type": "string",
    "description": "depending on policy"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "agent": {
    "type": "string",
    "description": "Agent"
   },
   "costCenterWhereApplicable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost Center where applicable"
   }
  }
 },
 "CustomerGuestAccountAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Customer, Guest & Account Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestCheckout": {
    "type": "string",
    "description": "Guest Checkout"
   },
   "registeredCustomer": {
    "type": "string",
    "description": "Registered Customer"
   },
   "member": {
    "type": "string",
    "description": "Member"
   },
   "corporateAccount": {
    "type": "string",
    "description": "Corporate Account"
   },
   "b2bAccount": {
    "type": "string",
    "description": "B2B Account"
   },
   "groupOrganizer": {
    "type": "string",
    "description": "Group Organizer"
   },
   "anonymousSaleWherePermitted": {
    "type": "string",
    "description": "Anonymous Sale where permitted"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "mobile": {
    "type": "string",
    "description": "Mobile"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date-time",
    "description": "Date of Birth"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "company": {
    "type": "string",
    "description": "Company"
   },
   "taxDetails": {
    "type": "string",
    "description": "Tax Details"
   },
   "from": {
    "type": "string",
    "description": "from"
   },
   "continueGuest": {
    "type": "string",
    "description": "Continue Guest"
   },
   "dependingOnPolicy": {
    "type": "string",
    "description": "depending on policy"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "agent": {
    "type": "string",
    "description": "Agent"
   },
   "costCenterWhereApplicable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost Center where applicable"
   }
  }
 },
 "OrderCreationSourceChannelConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Order Creation & Source/Channel Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "b2cWeb": {
    "type": "string",
    "description": "B2C Web"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "mobileFlyingPos": {
    "type": "string",
    "description": "Mobile/Flying POS"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "boxOffice": {
    "type": "string",
    "description": "Box Office"
   },
   "b2bPortal": {
    "type": "string",
    "description": "B2B Portal"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "ota": {
    "type": "string",
    "description": "OTA"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "administrativeBackend": {
    "type": "string",
    "description": "Administrative Backend"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "subChannel": {
    "type": "string",
    "description": "Sub-Channel"
   },
   "salesLocation": {
    "type": "string",
    "description": "Sales Location"
   },
   "terminal": {
    "type": "string",
    "description": "Terminal"
   },
   "device": {
    "type": "string",
    "description": "Device"
   },
   "agent": {
    "type": "string",
    "description": "Agent"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "affiliate": {
    "type": "string",
    "description": "Affiliate"
   },
   "apiConsumer": {
    "type": "string",
    "description": "API Consumer"
   },
   "externalReference": {
    "type": "string",
    "description": "External Reference"
   },
   "globalSequence": {
    "type": "string",
    "description": "Global Sequence"
   },
   "tenantSequence": {
    "type": "string",
    "description": "Tenant Sequence"
   },
   "venueSequence": {
    "type": "string",
    "description": "Venue Sequence"
   },
   "channelPrefix": {
    "type": "string",
    "description": "Channel Prefix"
   },
   "yearMonthPrefix": {
    "type": "string",
    "description": "Year/Month Prefix"
   },
   "customPattern": {
    "type": "string",
    "description": "Custom Pattern"
   },
   "otaBookingReference": {
    "type": "string",
    "description": "OTA Booking Reference"
   },
   "resellerOrderId": {
    "type": "string",
    "description": "Reseller Order ID"
   },
   "erpReference": {
    "type": "string",
    "description": "ERP Reference"
   },
   "externalCrmReference": {
    "type": "string",
    "description": "External CRM Reference"
   },
   "holdInventory": {
    "type": "string",
    "description": "Hold Inventory"
   },
   "repeatedRequests": {
    "type": "string",
    "description": "repeated requests"
   }
  }
 },
 "OrderCreationSourceChannelConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Creation & Source/Channel Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "b2cWeb": {
    "type": "string",
    "description": "B2C Web"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "mobileFlyingPos": {
    "type": "string",
    "description": "Mobile/Flying POS"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "boxOffice": {
    "type": "string",
    "description": "Box Office"
   },
   "b2bPortal": {
    "type": "string",
    "description": "B2B Portal"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "ota": {
    "type": "string",
    "description": "OTA"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "administrativeBackend": {
    "type": "string",
    "description": "Administrative Backend"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "subChannel": {
    "type": "string",
    "description": "Sub-Channel"
   },
   "salesLocation": {
    "type": "string",
    "description": "Sales Location"
   },
   "terminal": {
    "type": "string",
    "description": "Terminal"
   },
   "device": {
    "type": "string",
    "description": "Device"
   },
   "agent": {
    "type": "string",
    "description": "Agent"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "affiliate": {
    "type": "string",
    "description": "Affiliate"
   },
   "apiConsumer": {
    "type": "string",
    "description": "API Consumer"
   },
   "externalReference": {
    "type": "string",
    "description": "External Reference"
   },
   "globalSequence": {
    "type": "string",
    "description": "Global Sequence"
   },
   "tenantSequence": {
    "type": "string",
    "description": "Tenant Sequence"
   },
   "venueSequence": {
    "type": "string",
    "description": "Venue Sequence"
   },
   "channelPrefix": {
    "type": "string",
    "description": "Channel Prefix"
   },
   "yearMonthPrefix": {
    "type": "string",
    "description": "Year/Month Prefix"
   },
   "customPattern": {
    "type": "string",
    "description": "Custom Pattern"
   },
   "otaBookingReference": {
    "type": "string",
    "description": "OTA Booking Reference"
   },
   "resellerOrderId": {
    "type": "string",
    "description": "Reseller Order ID"
   },
   "erpReference": {
    "type": "string",
    "description": "ERP Reference"
   },
   "externalCrmReference": {
    "type": "string",
    "description": "External CRM Reference"
   },
   "holdInventory": {
    "type": "string",
    "description": "Hold Inventory"
   },
   "repeatedRequests": {
    "type": "string",
    "description": "repeated requests"
   }
  }
 },
 "OrderDetailTransactionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is orders.cart_line at 14%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Order Detail & Transaction Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each line should display* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "personType": {
    "type": "string",
    "description": "Person Type"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Unit Price"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket Status"
   }
  },
  "x-ticvai-record-definition": "Each line should display"
 },
 "OrderDetailTransactionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Detail & Transaction Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "orderNumber": {
    "type": "string",
    "description": "Order Number"
   },
   "orderDate": {
    "type": "string",
    "format": "date-time",
    "description": "Order Date"
   },
   "orderTime": {
    "type": "string",
    "format": "date-time",
    "description": "Order Time"
   },
   "orderStatus": {
    "type": "integer",
    "description": "Order Status"
   },
   "reservationStatus": {
    "type": "integer",
    "description": "Reservation Status"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "salesLocation": {
    "type": "string",
    "description": "Sales Location"
   },
   "cashierAgent": {
    "type": "string",
    "description": "Cashier/Agent"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "total": {
    "type": "integer",
    "description": "Total"
   },
   "paymentStatus": {
    "type": "integer",
    "description": "Payment Status"
   },
   "fulfillmentStatus": {
    "type": "integer",
    "description": "Fulfillment Status"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "personType": {
    "type": "string",
    "description": "Person Type"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Unit Price"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket Status"
   },
   "tickets": {
    "type": "integer",
    "description": "Tickets"
   },
   "reservations": {
    "type": "integer",
    "description": "Reservations"
   },
   "payments": {
    "type": "integer",
    "description": "Payments"
   },
   "refunds": {
    "type": "integer",
    "description": "Refunds"
   },
   "invoices": {
    "type": "integer",
    "description": "Invoices"
   },
   "credentials": {
    "type": "integer",
    "description": "Credentials"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "waivers": {
    "type": "integer",
    "description": "Waivers"
   },
   "relatedOrders": {
    "type": "integer",
    "description": "Related Orders"
   }
  }
 },
 "OrderLifecycleTimelineSlaExceptionsAiOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Lifecycle Timeline, SLA, Exceptions & AI Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "eventType": {
    "type": "string",
    "description": "Event Type"
   },
   "userSystem": {
    "type": "string",
    "description": "User/System"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "previousState": {
    "type": "string",
    "description": "Previous State"
   },
   "newState": {
    "type": "integer",
    "description": "New State"
   },
   "relatedTransaction": {
    "type": "string",
    "description": "Related Transaction"
   },
   "correlationId": {
    "type": "string",
    "description": "Correlation ID"
   },
   "result": {
    "type": "string",
    "description": "Result"
   },
   "stuckOrder": {
    "type": "string",
    "description": "Stuck Order"
   },
   "orphanReservation": {
    "type": "string",
    "description": "Orphan Reservation"
   },
   "paymentOrderMismatch": {
    "type": "string",
    "description": "Payment/Order Mismatch"
   },
   "capacityMismatch": {
    "type": "integer",
    "description": "Capacity Mismatch"
   },
   "missingCustomerData": {
    "type": "string",
    "description": "Missing Customer Data"
   },
   "fulfillmentFailure": {
    "type": "string",
    "description": "Fulfillment Failure"
   },
   "externalSynchronizationFailure": {
    "type": "string",
    "description": "External Synchronization Failure"
   },
   "revalidate": {
    "type": "string",
    "description": "Revalidate"
   },
   "reprocessFulfillment": {
    "type": "string",
    "description": "Reprocess Fulfillment"
   },
   "importantArchitectureDecisionsToFreeze": {
    "type": "string",
    "description": "Important Architecture Decisions to Freeze"
   },
   "governedCommercialTransaction": {
    "type": "string",
    "description": "governed commercial transaction"
   },
   "board2AmendmentsCancellations": {
    "type": "string",
    "description": "Board 2 — Amendments, Cancellations"
   },
   "created": {
    "type": "string",
    "format": "date-time",
    "description": "created"
   }
  }
 },
 "OrderLineProductEntitlementCompositionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Line, Product & Entitlement Composition displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tickets": {
    "type": "string",
    "description": "Tickets"
   },
   "memberships": {
    "type": "string",
    "description": "Memberships"
   },
   "addOns": {
    "type": "string",
    "description": "Add-Ons"
   },
   "fB": {
    "type": "string",
    "description": "F&B"
   },
   "retail": {
    "type": "string",
    "description": "Retail"
   },
   "rental": {
    "type": "string",
    "description": "Rental"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "experiences": {
    "type": "string",
    "description": "Experiences"
   },
   "packages": {
    "type": "string",
    "description": "Packages"
   },
   "vouchers": {
    "type": "string",
    "description": "Vouchers"
   },
   "otherConfiguredProducts": {
    "type": "string",
    "description": "Other configured products"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "variant": {
    "type": "string",
    "description": "Variant"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "personType": {
    "type": "string",
    "description": "Person Type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "entitlement": {
    "type": "string",
    "description": "Entitlement"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "fulfillmentMethod": {
    "type": "string",
    "description": "Fulfillment Method"
   },
   "productLimits": {
    "type": "string",
    "description": "Product Limits"
   },
   "channelLimits": {
    "type": "string",
    "description": "Channel Limits"
   },
   "customerLimits": {
    "type": "string",
    "description": "Customer Limits"
   },
   "eventLimits": {
    "type": "string",
    "description": "Event Limits"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "moment": {
    "type": "string",
    "description": "moment"
   }
  }
 },
 "OrderReservationCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order & Reservation Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ordersToday": {
    "type": "string",
    "description": "Orders Today"
   },
   "confirmedOrders": {
    "type": "integer",
    "description": "Confirmed Orders"
   },
   "activeReservations": {
    "type": "integer",
    "description": "Active Reservations"
   },
   "temporaryHolds": {
    "type": "integer",
    "description": "Temporary Holds"
   },
   "pendingPayment": {
    "type": "integer",
    "description": "Pending Payment"
   },
   "expiringReservations": {
    "type": "integer",
    "description": "Expiring Reservations"
   },
   "failedOrders": {
    "type": "integer",
    "description": "Failed Orders"
   },
   "partiallyFulfilled": {
    "type": "string",
    "description": "Partially Fulfilled"
   },
   "completedOrders": {
    "type": "integer",
    "description": "Completed Orders"
   },
   "cancelledOrders": {
    "type": "integer",
    "description": "Cancelled Orders"
   },
   "ordersRequiringAttention": {
    "type": "string",
    "description": "Orders Requiring Attention"
   },
   "grossOrderValue": {
    "type": "string",
    "description": "Gross Order Value"
   },
   "orderId": {
    "type": "string",
    "description": "Order ID"
   },
   "reservationId": {
    "type": "string",
    "description": "Reservation ID"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "productEvent": {
    "type": "string",
    "description": "Product/Event"
   },
   "orderValue": {
    "type": "string",
    "description": "Order Value"
   },
   "paymentStatus": {
    "type": "integer",
    "description": "Payment Status"
   },
   "reservationStatus": {
    "type": "integer",
    "description": "Reservation Status"
   },
   "fulfillmentStatus": {
    "type": "integer",
    "description": "Fulfillment Status"
   },
   "createdDate": {
    "type": "string",
    "format": "date-time",
    "description": "Created Date"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "ownerAgent": {
    "type": "string",
    "description": "Owner/Agent"
   },
   "collectPayment": {
    "type": "string",
    "description": "Collect Payment"
   }
  }
 },
 "OrderReservationStatusLifecycleConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Order & Reservation Status Lifecycle Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each transition define* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "fromStatus": {
    "type": "string",
    "description": "From Status"
   },
   "toStatus": {
    "type": "string",
    "description": "To Status"
   },
   "requiredConditions": {
    "type": "string",
    "description": "Required Conditions"
   },
   "userSystemAction": {
    "type": "string",
    "description": "User/System Action"
   },
   "allowedRole": {
    "type": "string",
    "description": "Allowed Role"
   },
   "integrationRequirement": {
    "type": "string",
    "description": "Integration Requirement"
   },
   "notification": {
    "type": "string",
    "description": "Notification"
   },
   "auditRequirement": {
    "type": "string",
    "description": "Audit Requirement"
   },
   "systemControlledStatus": {
    "type": "string",
    "description": "System-Controlled Status"
   },
   "operationalStatus": {
    "type": "string",
    "description": "Operational Status"
   },
   "userEditableStatus": {
    "type": "string",
    "description": "User-Editable Status"
   }
  },
  "x-ticvai-record-definition": "For each transition define"
 },
 "OrderReservationStatusLifecycleConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order & Reservation Status Lifecycle Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fromStatus": {
    "type": "string",
    "description": "From Status"
   },
   "toStatus": {
    "type": "string",
    "description": "To Status"
   },
   "requiredConditions": {
    "type": "string",
    "description": "Required Conditions"
   },
   "userSystemAction": {
    "type": "string",
    "description": "User/System Action"
   },
   "allowedRole": {
    "type": "string",
    "description": "Allowed Role"
   },
   "integrationRequirement": {
    "type": "string",
    "description": "Integration Requirement"
   },
   "notification": {
    "type": "string",
    "description": "Notification"
   },
   "auditRequirement": {
    "type": "string",
    "description": "Audit Requirement"
   },
   "systemControlledStatus": {
    "type": "string",
    "description": "System-Controlled Status"
   },
   "operationalStatus": {
    "type": "string",
    "description": "Operational Status"
   },
   "userEditableStatus": {
    "type": "string",
    "description": "User-Editable Status"
   }
  }
 },
 "ReservationConfirmationExpiryFulfillmentReadinessView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Reservation Confirmation, Expiry & Fulfillment Readiness displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "paymentComplete": {
    "type": "string",
    "description": "Payment Complete"
   },
   "depositReceived": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit Received"
   },
   "creditApproved": {
    "type": "string",
    "description": "Credit Approved"
   },
   "capacityConfirmed": {
    "type": "integer",
    "description": "Capacity Confirmed"
   },
   "customerDataComplete": {
    "type": "string",
    "description": "Customer Data Complete"
   },
   "requiredWaiverComplete": {
    "type": "string",
    "description": "Required Waiver Complete"
   },
   "requiredApprovalComplete": {
    "type": "string",
    "description": "Required Approval Complete"
   },
   "partnerConfirmationReceived": {
    "type": "string",
    "description": "Partner Confirmation Received"
   },
   "exampleB2c": {
    "type": "string",
    "description": "Example — B2C"
   },
   "exampleB2b": {
    "type": "string",
    "description": "Example — B2B"
   },
   "partnerAuthorized": {
    "type": "string",
    "description": "Partner Authorized"
   },
   "orderConfirmed": {
    "type": "string",
    "description": "Order Confirmed"
   },
   "paymentConditionMet": {
    "type": "string",
    "description": "Payment Condition Met"
   },
   "requiredCustomerData": {
    "type": "string",
    "description": "Required Customer Data"
   },
   "entitlementValid": {
    "type": "string",
    "description": "Entitlement Valid"
   },
   "waiverRequirement": {
    "type": "string",
    "description": "Waiver Requirement"
   },
   "credentialConfiguration": {
    "type": "string",
    "description": "Credential Configuration"
   },
   "deliveryMethod": {
    "type": "string",
    "description": "Delivery Method"
   },
   "expire": {
    "type": "string",
    "format": "date-time",
    "description": "Expire"
   },
   "preserveHistory": {
    "type": "string",
    "description": "Preserve history"
   },
   "ticketMedia": {
    "type": "string",
    "description": "Ticket Media"
   },
   "walletPass": {
    "type": "string",
    "description": "Wallet Pass"
   },
   "rfidNfc": {
    "type": "string",
    "description": "RFID/NFC"
   },
   "emailDelivery": {
    "type": "string",
    "description": "Email Delivery"
   },
   "otherCredentialServices": {
    "type": "string",
    "description": "Other credential services"
   }
  }
 },
 "ReservationHoldPolicyConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Reservation & Hold Policy Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "cartHold": {
    "type": "string",
    "description": "Cart Hold"
   },
   "checkoutHold": {
    "type": "string",
    "description": "Checkout Hold"
   },
   "agentReservation": {
    "type": "string",
    "description": "Agent Reservation"
   },
   "groupReservation": {
    "type": "string",
    "description": "Group Reservation"
   },
   "b2bReservation": {
    "type": "string",
    "description": "B2B Reservation"
   },
   "corporateReservation": {
    "type": "string",
    "description": "Corporate Reservation"
   },
   "manualHold": {
    "type": "string",
    "description": "Manual Hold"
   },
   "paymentHold": {
    "type": "string",
    "description": "Payment Hold"
   },
   "seatHold": {
    "type": "string",
    "description": "Seat Hold"
   },
   "inventoryHold": {
    "type": "string",
    "description": "Inventory Hold"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "reservationType": {
    "type": "string",
    "description": "Reservation Type"
   },
   "maintainAuditRecord": {
    "type": "string",
    "description": "Maintain Audit Record"
   },
   "extensionAllowed": {
    "type": "boolean",
    "description": "Extension Allowed"
   },
   "maximumExtensions": {
    "type": "string",
    "description": "Maximum Extensions"
   },
   "extensionDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Extension Duration"
   },
   "authorizedRole": {
    "type": "string",
    "description": "Authorized Role"
   },
   "approvalRequirement": {
    "type": "string",
    "description": "Approval Requirement"
   },
   "admissionCapacity": {
    "type": "integer",
    "description": "Admission Capacity"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "inventory": {
    "type": "string",
    "description": "Inventory"
   },
   "timeslotCapacity": {
    "type": "integer",
    "description": "Timeslot Capacity"
   },
   "entitlementCapacity": {
    "type": "integer",
    "description": "Entitlement Capacity"
   },
   "throughTheCentralCapacityInventoryServices": {
    "type": "integer",
    "description": "through the central capacity/inventory services"
   }
  }
 },
 "ReservationHoldPolicyConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Reservation & Hold Policy Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "cartHold": {
    "type": "string",
    "description": "Cart Hold"
   },
   "checkoutHold": {
    "type": "string",
    "description": "Checkout Hold"
   },
   "agentReservation": {
    "type": "string",
    "description": "Agent Reservation"
   },
   "groupReservation": {
    "type": "string",
    "description": "Group Reservation"
   },
   "b2bReservation": {
    "type": "string",
    "description": "B2B Reservation"
   },
   "corporateReservation": {
    "type": "string",
    "description": "Corporate Reservation"
   },
   "manualHold": {
    "type": "string",
    "description": "Manual Hold"
   },
   "paymentHold": {
    "type": "string",
    "description": "Payment Hold"
   },
   "seatHold": {
    "type": "string",
    "description": "Seat Hold"
   },
   "inventoryHold": {
    "type": "string",
    "description": "Inventory Hold"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "reservationType": {
    "type": "string",
    "description": "Reservation Type"
   },
   "maintainAuditRecord": {
    "type": "string",
    "description": "Maintain Audit Record"
   },
   "extensionAllowed": {
    "type": "boolean",
    "description": "Extension Allowed"
   },
   "maximumExtensions": {
    "type": "string",
    "description": "Maximum Extensions"
   },
   "extensionDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Extension Duration"
   },
   "authorizedRole": {
    "type": "string",
    "description": "Authorized Role"
   },
   "approvalRequirement": {
    "type": "string",
    "description": "Approval Requirement"
   },
   "admissionCapacity": {
    "type": "integer",
    "description": "Admission Capacity"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "inventory": {
    "type": "string",
    "description": "Inventory"
   },
   "timeslotCapacity": {
    "type": "integer",
    "description": "Timeslot Capacity"
   },
   "entitlementCapacity": {
    "type": "integer",
    "description": "Entitlement Capacity"
   },
   "throughTheCentralCapacityInventoryServices": {
    "type": "integer",
    "description": "through the central capacity/inventory services"
   }
  }
 }
}
```
