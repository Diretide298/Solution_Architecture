# WS33 — Order   Reservation Management board 3

**10 screens · 10 operations · 11 schemas · 2 permissions**

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
| `BO-324` | Payment & Order Financial Command Center | listDetail | 1 | 0 | — |
| `BO-325` | Order Payment Detail & Transaction Ledger | listDetail | 1 | 1 | — |
| `BO-326` | Multi-Payment, Split Tender & Payment Allocation Configuration | configEditor | 1 | 0 | — |
| `BO-327` | Deposit, Partial Payment & Outstanding Balance Management | listDetail | 1 | 0 | — |
| `BO-328` | Order Split, Merge & Transaction Relationship Management | listDetail | 1 | 0 | — |
| `BO-329` | Related Order & Transaction Relationship Explorer | listDetail | 1 | 0 | — |
| `BO-330` | External Payment, Partner & Settlement Reference Mapping | configEditor | 1 | 0 | — |
| `BO-331` | Payment Reconciliation & Exception Management | listDetail | 1 | 0 | — |
| `BO-332` | Financial Traceability, Control & Audit Explorer | configEditor | 1 | 0 | — |
| `BO-333` | Order Financial Analytics & AI Reconciliation Intelligence | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-327, BO-328, BO-331, BO-332 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-324",
  "name": "Payment & Order Financial Command Center",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.1",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/payment-order-financial-command-center-bo-324",
   "component": "apps/venue-management-web/src/routes/orders-money/PaymentOrderFinancialCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-325",
    "BO-326",
    "BO-327",
    "BO-328",
    "BO-329",
    "BO-330",
    "BO-331",
    "BO-332",
    "BO-333"
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
     "to": "BO-325",
     "trigger": "Works in Order Payment Detail & Transaction Ledger",
     "provenance": "flow F142 step 1→2",
     "operation": "listPaymentOrderFinancial"
    },
    {
     "to": "BO-326",
     "trigger": "Works in Multi-Payment, Split Tender & Payment Allocation Configuration",
     "provenance": "flow F142 step 3→4",
     "operation": "listPaymentOrderFinancial"
    },
    {
     "to": "BO-327",
     "trigger": "Works in Deposit, Partial Payment & Outstanding Balance Management",
     "provenance": "flow F142 step 5→6",
     "operation": "listPaymentOrderFinancial"
    },
    {
     "to": "BO-328",
     "trigger": "Works in Order Split, Merge & Transaction Relationship Management",
     "provenance": "flow F142 step 7→8",
     "operation": "listPaymentOrderFinancial"
    },
    {
     "to": "BO-329",
     "trigger": "Works in Related Order & Transaction Relationship Explorer",
     "provenance": "flow F142 step 9→10",
     "operation": "listPaymentOrderFinancial"
    },
    {
     "to": "BO-330",
     "trigger": "Works in External Payment, Partner & Settlement Reference Mapping",
     "provenance": "flow F142 step 11→12",
     "operation": "listPaymentOrderFinancial"
    },
    {
     "to": "BO-331",
     "trigger": "Works in Payment Reconciliation & Exception Management",
     "provenance": "flow F142 step 13→14",
     "operation": "listPaymentOrderFinancial"
    },
    {
     "to": "BO-332",
     "trigger": "Works in Financial Traceability, Control & Audit Explorer",
     "provenance": "flow F142 step 15→16",
     "operation": "listPaymentOrderFinancial"
    },
    {
     "to": "BO-333",
     "trigger": "Works in Order Financial Analytics & AI Reconciliation Intelligence",
     "provenance": "flow F142 step 17→18",
     "operation": "listPaymentOrderFinancial"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide operations and finance teams with a centralized view of the financial status of all",
  "purposeNote": "Authorized users can monitor the complete payment and financial condition of orders across all TICVAI channels from one workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Failed. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 40 §Support"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search payment order financial",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 40 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "PaymentOrderFinancialCommandCenterView.venue",
        "PaymentOrderFinancialCommandCenterView.channel",
        "PaymentOrderFinancialCommandCenterView.paymentMethod",
        "PaymentOrderFinancialCommandCenterView.paymentProvider",
        "PaymentOrderFinancialCommandCenterView.currency",
        "PaymentOrderFinancialCommandCenterView.orderStatus",
        "PaymentOrderFinancialCommandCenterView.paymentStatus",
        "PaymentOrderFinancialCommandCenterView.settlementStatus",
        "Date",
        "Exception Type"
       ],
       "notes": "The pack filters this screen by venue, channel, payment method, payment provider, currency, order status and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 40 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every payment order financial",
       "columns": [
        "PaymentOrderFinancialCommandCenterView.grossOrderValue",
        "PaymentOrderFinancialCommandCenterView.fullyPaidOrders",
        "PaymentOrderFinancialCommandCenterView.partiallyPaidOrders",
        "PaymentOrderFinancialCommandCenterView.unpaidOrders",
        "PaymentOrderFinancialCommandCenterView.outstandingBalance",
        "PaymentOrderFinancialCommandCenterView.paymentsToday",
        "PaymentOrderFinancialCommandCenterView.failedPayments",
        "PaymentOrderFinancialCommandCenterView.pendingPayments",
        "PaymentOrderFinancialCommandCenterView.refundsPending",
        "PaymentOrderFinancialCommandCenterView.reconciliationExceptions",
        "PaymentOrderFinancialCommandCenterView.unallocatedPayments",
        "PaymentOrderFinancialCommandCenterView.settlementVariance",
        "PaymentOrderFinancialCommandCenterView.orderId",
        "PaymentOrderFinancialCommandCenterView.customer",
        "PaymentOrderFinancialCommandCenterView.channel",
        "PaymentOrderFinancialCommandCenterView.orderValue",
        "PaymentOrderFinancialCommandCenterView.amountPaid",
        "PaymentOrderFinancialCommandCenterView.refunded",
        "PaymentOrderFinancialCommandCenterView.outstanding",
        "PaymentOrderFinancialCommandCenterView.paymentMethods",
        "PaymentOrderFinancialCommandCenterView.paymentStatus",
        "PaymentOrderFinancialCommandCenterView.settlementStatus",
        "PaymentOrderFinancialCommandCenterView.reconciliationStatus"
       ],
       "bindsTo": "PaymentOrderFinancialCommandCenterView",
       "operation": "listPaymentOrderFinancial",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 40 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment order financial",
       "bindsTo": "PaymentOrderFinancialCommandCenterView",
       "columns": [
        "PaymentOrderFinancialCommandCenterView.grossOrderValue",
        "PaymentOrderFinancialCommandCenterView.fullyPaidOrders",
        "PaymentOrderFinancialCommandCenterView.partiallyPaidOrders",
        "PaymentOrderFinancialCommandCenterView.unpaidOrders",
        "PaymentOrderFinancialCommandCenterView.outstandingBalance",
        "PaymentOrderFinancialCommandCenterView.paymentsToday",
        "PaymentOrderFinancialCommandCenterView.failedPayments",
        "PaymentOrderFinancialCommandCenterView.pendingPayments",
        "PaymentOrderFinancialCommandCenterView.refundsPending",
        "PaymentOrderFinancialCommandCenterView.reconciliationExceptions",
        "PaymentOrderFinancialCommandCenterView.unallocatedPayments",
        "PaymentOrderFinancialCommandCenterView.settlementVariance",
        "PaymentOrderFinancialCommandCenterView.orderId",
        "PaymentOrderFinancialCommandCenterView.customer",
        "PaymentOrderFinancialCommandCenterView.channel",
        "PaymentOrderFinancialCommandCenterView.orderValue",
        "PaymentOrderFinancialCommandCenterView.amountPaid",
        "PaymentOrderFinancialCommandCenterView.refunded",
        "PaymentOrderFinancialCommandCenterView.outstanding",
        "PaymentOrderFinancialCommandCenterView.paymentMethods",
        "PaymentOrderFinancialCommandCenterView.paymentStatus",
        "PaymentOrderFinancialCommandCenterView.settlementStatus",
        "PaymentOrderFinancialCommandCenterView.reconciliationStatus"
       ],
       "notes": null,
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 40 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Failed",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 40 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment order financial list.",
   "error": "Could not load. Names which read failed and leaves the payment order financial untouched.",
   "emptyFirstRun": "No payment order financial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment order financial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentOrderFinancial",
    "contract": "orders",
    "purpose": "Payment & Order Financial Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PaymentOrderFinancialCommandCenterView.grossOrderValue",
    "PaymentOrderFinancialCommandCenterView.fullyPaidOrders",
    "PaymentOrderFinancialCommandCenterView.partiallyPaidOrders",
    "PaymentOrderFinancialCommandCenterView.unpaidOrders",
    "PaymentOrderFinancialCommandCenterView.outstandingBalance",
    "PaymentOrderFinancialCommandCenterView.paymentsToday"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-324"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 40. 31 of 33 labels bound to a contract property; 34 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-325",
  "name": "Order Payment Detail & Transaction Ledger",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.2",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-payment-detail-transaction-ledger-bo-325",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderPaymentDetailTransactionLedger.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-324",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F142 step 2→3",
     "operation": "listOrderPaymentDetail"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the complete payment history associated with an individual order.",
  "purposeNote": "Users can reconstruct every financial movement associated with an order from initial authorization through final refund/reversal.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Capture, Additional Collection, Void. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
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
       "label": "Every order payment detail",
       "columns": [
        "OrderPaymentDetailTransactionLedgerView.orderNumber",
        "OrderPaymentDetailTransactionLedgerView.customer",
        "OrderPaymentDetailTransactionLedgerView.orderTotal",
        "OrderPaymentDetailTransactionLedgerView.currency",
        "OrderPaymentDetailTransactionLedgerView.paid",
        "OrderPaymentDetailTransactionLedgerView.refunded",
        "OrderPaymentDetailTransactionLedgerView.outstanding",
        "OrderPaymentDetailTransactionLedgerView.creditApplied",
        "OrderPaymentDetailTransactionLedgerView.paymentStatus",
        "OrderPaymentDetailTransactionLedgerView.settlementStatus"
       ],
       "bindsTo": "OrderPaymentDetailTransactionLedgerView",
       "operation": "listOrderPaymentDetail",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order payment detail",
       "bindsTo": "OrderPaymentDetailTransactionLedgerView",
       "columns": [
        "OrderPaymentDetailTransactionLedgerView.orderNumber",
        "OrderPaymentDetailTransactionLedgerView.customer",
        "OrderPaymentDetailTransactionLedgerView.orderTotal",
        "OrderPaymentDetailTransactionLedgerView.currency",
        "OrderPaymentDetailTransactionLedgerView.paid",
        "OrderPaymentDetailTransactionLedgerView.refunded",
        "OrderPaymentDetailTransactionLedgerView.outstanding",
        "OrderPaymentDetailTransactionLedgerView.creditApplied",
        "OrderPaymentDetailTransactionLedgerView.paymentStatus",
        "OrderPaymentDetailTransactionLedgerView.settlementStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Transaction Ledger”, “Type Status”, “PAY-001 Visa Settled”, “PAY-002 Wallet Settled”, “REF-001 Refund Visa”, “Immutable Financial History”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Capture",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Additional Collection",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoid",
    "component": "confirmDialog",
    "trigger": "Void",
    "body": "**Void on a order payment detail is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
   }
  ],
  "states": {
   "loading": "The order payment detail list.",
   "error": "Could not load. Names which read failed and leaves the order payment detail untouched.",
   "emptyFirstRun": "No order payment detail yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order payment detail are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderPaymentDetail",
    "contract": "orders",
    "purpose": "Order Payment Detail & Transaction Ledger",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OrderPaymentDetailTransactionLedgerView.orderNumber",
    "OrderPaymentDetailTransactionLedgerView.customer",
    "OrderPaymentDetailTransactionLedgerView.orderTotal",
    "OrderPaymentDetailTransactionLedgerView.currency",
    "OrderPaymentDetailTransactionLedgerView.paid",
    "OrderPaymentDetailTransactionLedgerView.refunded"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-325"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 41. 10 of 10 labels bound to a contract property; 20 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-326",
  "name": "Multi-Payment, Split Tender & Payment Allocation Configuration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.3",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/multi-payment-split-tender-payment-allocation-configurat-bo-326",
   "component": "apps/venue-management-web/src/routes/orders-money/MultiPaymentSplitTenderPaymentAllocationConfigur.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-324",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F142 step 4→5",
     "operation": "setMultiPaymentSplit"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Configure whether payment is allocated) and no display directory — it is settings, not a population",
  "purpose": "Support orders paid using multiple payment methods and determine how each payment is allocated.",
  "purposeNote": "every monetary amount to the relevant order components.",
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
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Terminal",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Order Type",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer Type",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Order Level",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure whether payment is allocated"
      },
      {
       "kind": "selectField",
       "label": "Order-Line Level",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure whether payment is allocated"
      },
      {
       "kind": "selectField",
       "label": "Product Level",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure whether payment is allocated"
      },
      {
       "kind": "selectField",
       "label": "Tax/Fee Component",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure whether payment is allocated"
      },
      {
       "kind": "selectField",
       "label": "Specific Ticket",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure whether payment is allocated"
      },
      {
       "kind": "selectField",
       "label": "Deposit",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 43 §Configure whether payment is allocated"
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
       "provenance": "contract operation setMultiPaymentSplit"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-payment split tender configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the multi-payment split tender untouched.",
   "emptyFirstRun": "No multi-payment split tender configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMultiPaymentSplit",
    "contract": "orders",
    "purpose": "Multi-Payment, Split Tender & Payment Allocation Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setMultiPaymentSplit"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-326"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 43. 0 of 0 labels bound to a contract property; 12 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-327",
  "name": "Deposit, Partial Payment & Outstanding Balance Management",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.4",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/deposit-partial-payment-outstanding-balance-management-bo-327",
   "component": "apps/venue-management-web/src/routes/orders-money/DepositPartialPaymentOutstandingBalanceManagemen.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-324",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F142 step 6→7",
     "operation": "listDepositPartialPayment"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Support commercial scenarios where an order may be confirmed or reserved without full immediate payment.",
  "purposeNote": "controlling reservation and fulfillment states.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every deposit partial payment",
       "columns": [
        "DepositPartialPaymentOutstandingBalanceManagementView.total",
        "DepositPartialPaymentOutstandingBalanceManagementView.depositRequired",
        "DepositPartialPaymentOutstandingBalanceManagementView.depositPaid",
        "DepositPartialPaymentOutstandingBalanceManagementView.remainingBalance",
        "DepositPartialPaymentOutstandingBalanceManagementView.dueDate",
        "DepositPartialPaymentOutstandingBalanceManagementView.daysRemaining",
        "DepositPartialPaymentOutstandingBalanceManagementView.status"
       ],
       "bindsTo": "DepositPartialPaymentOutstandingBalanceManagementView",
       "operation": "listDepositPartialPayment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected deposit partial payment",
       "bindsTo": "DepositPartialPaymentOutstandingBalanceManagementView",
       "columns": [
        "DepositPartialPaymentOutstandingBalanceManagementView.total",
        "DepositPartialPaymentOutstandingBalanceManagementView.depositRequired",
        "DepositPartialPaymentOutstandingBalanceManagementView.depositPaid",
        "DepositPartialPaymentOutstandingBalanceManagementView.remainingBalance",
        "DepositPartialPaymentOutstandingBalanceManagementView.dueDate",
        "DepositPartialPaymentOutstandingBalanceManagementView.daysRemaining",
        "DepositPartialPaymentOutstandingBalanceManagementView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Important for”, “Required Deposit”, “Due”, “Notifications”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The deposit partial payment list.",
   "error": "Could not load. Names which read failed and leaves the deposit partial payment untouched.",
   "emptyFirstRun": "No deposit partial payment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deposit partial payment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDepositPartialPayment",
    "contract": "orders",
    "purpose": "Deposit, Partial Payment & Outstanding Balance Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DepositPartialPaymentOutstandingBalanceManagementView.total",
    "DepositPartialPaymentOutstandingBalanceManagementView.depositRequired",
    "DepositPartialPaymentOutstandingBalanceManagementView.depositPaid",
    "DepositPartialPaymentOutstandingBalanceManagementView.remainingBalance",
    "DepositPartialPaymentOutstandingBalanceManagementView.dueDate",
    "DepositPartialPaymentOutstandingBalanceManagementView.daysRemaining"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-327"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 44. 7 of 7 labels bound to a contract property; 14 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-328",
  "name": "Order Split, Merge & Transaction Relationship Management",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.5",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-split-merge-transaction-relationship-management-bo-328",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderSplitMergeTransactionRelationshipManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-324",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F142 step 8→9",
     "operation": "listOrderSplitMerge"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow complex orders to be reorganized without destroying transaction history.",
  "purposeNote": "Orders can be split or merged while maintaining accurate financial, customer, product, payment and historical relationships.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Ticket. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 46 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 46"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ticket",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Order Line",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 46 §Support"
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
   "loading": "The order split merge list.",
   "error": "Could not load. Names which read failed and leaves the order split merge untouched.",
   "emptyFirstRun": "No order split merge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order split merge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderSplitMerge",
    "contract": "orders",
    "purpose": "Order Split, Merge & Transaction Relationship Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OrderSplitMergeTransactionRelationshipManagementView.orderA4Tickets",
    "OrderSplitMergeTransactionRelationshipManagementView.orderB2Tickets",
    "OrderSplitMergeTransactionRelationshipManagementView.ticket",
    "OrderSplitMergeTransactionRelationshipManagementView.attendee",
    "OrderSplitMergeTransactionRelationshipManagementView.product"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-328"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 46. 0 of 0 labels bound to a contract property; 2 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-329",
  "name": "Related Order & Transaction Relationship Explorer",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.6",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/related-order-transaction-relationship-explorer-bo-329",
   "component": "apps/venue-management-web/src/routes/orders-money/RelatedOrderTransactionRelationshipExplorer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-324",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F142 step 10→11",
     "operation": "listRelatedOrderTransaction"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a visual relationship map for complex transaction histories. This becomes especially useful after amendments, upgrades, exchanges, reissues, splits and refunds.",
  "purposeNote": "Users can understand complex transaction chains without manually searching multiple systems or screens.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search related order transaction",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 47 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Order",
        "Ticket",
        "Customer",
        "RelatedOrderTransactionRelationshipExplorerView.payment",
        "Refund",
        "External Reference",
        "Partner Booking"
       ],
       "notes": "The pack filters this screen by order, ticket, customer, payment, refund, external reference and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 47 §Search by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every related order transaction",
       "columns": [
        "RelatedOrderTransactionRelationshipExplorerView.original",
        "Amendment",
        "Upgrade",
        "RelatedOrderTransactionRelationshipExplorerView.conversion",
        "RelatedOrderTransactionRelationshipExplorerView.exchange",
        "Split",
        "Merge",
        "Reissue",
        "RelatedOrderTransactionRelationshipExplorerView.cancellation",
        "Refund",
        "RelatedOrderTransactionRelationshipExplorerView.payment",
        "RelatedOrderTransactionRelationshipExplorerView.chargebackWhereIntegrated",
        "RelatedOrderTransactionRelationshipExplorerView.externalTransaction"
       ],
       "bindsTo": "RelatedOrderTransactionRelationshipExplorerView",
       "operation": "listRelatedOrderTransaction",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 47 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected related order transaction",
       "bindsTo": "RelatedOrderTransactionRelationshipExplorerView",
       "columns": [
        "RelatedOrderTransactionRelationshipExplorerView.original",
        "Amendment",
        "Upgrade",
        "RelatedOrderTransactionRelationshipExplorerView.conversion",
        "RelatedOrderTransactionRelationshipExplorerView.exchange",
        "Split",
        "Merge",
        "Reissue",
        "RelatedOrderTransactionRelationshipExplorerView.cancellation",
        "Refund",
        "RelatedOrderTransactionRelationshipExplorerView.payment",
        "RelatedOrderTransactionRelationshipExplorerView.chargebackWhereIntegrated",
        "RelatedOrderTransactionRelationshipExplorerView.externalTransaction"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Original Order ORD-1001”, “ORD-1001-A”, “Upgrade TXN UPG-1042”, “PAY-2014”, “CAN-3021”, “Graph Interaction”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 47 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The related order transaction list.",
   "error": "Could not load. Names which read failed and leaves the related order transaction untouched.",
   "emptyFirstRun": "No related order transaction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the related order transaction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRelatedOrderTransaction",
    "contract": "orders",
    "purpose": "Related Order & Transaction Relationship Explorer",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RelatedOrderTransactionRelationshipExplorerView.original",
    "Amendment",
    "Upgrade",
    "RelatedOrderTransactionRelationshipExplorerView.conversion",
    "RelatedOrderTransactionRelationshipExplorerView.exchange",
    "Split"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-329"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 47. 8 of 20 labels bound to a contract property; 20 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-330",
  "name": "External Payment, Partner & Settlement Reference Mapping",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.7",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/external-payment-partner-settlement-reference-mapping-bo-330",
   "component": "apps/venue-management-web/src/routes/orders-money/ExternalPaymentPartnerSettlementReferenceMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-324",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F142 step 12→13",
     "operation": "listExternalPaymentPartner"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Maintain the relationship between TICVAI transactions and external financial/channel references.",
  "purposeNote": "relevant external transaction and settlement references.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "TICVAI Order ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "TICVAI Payment ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Merchant ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "External Transaction ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Authorization Code",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Partner Order ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Settlement Batch",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Settlement Date",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "ERP Reference",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Amount",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The external payment partner configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the external payment partner untouched.",
   "emptyFirstRun": "No external payment partner configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listExternalPaymentPartner",
    "contract": "orders",
    "purpose": "External Payment, Partner & Settlement Reference Mapping",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-330"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 49. 0 of 0 labels bound to a contract property; 12 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-331",
  "name": "Payment Reconciliation & Exception Management",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.8",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/payment-reconciliation-exception-management-bo-331",
   "component": "apps/venue-management-web/src/routes/orders-money/PaymentReconciliationExceptionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-324",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F142 step 14→15",
     "operation": "listPaymentReconciliationException"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare) and no metric row",
  "purpose": "Automatically compare TICVAI payment records with external payment and settlement records.",
  "purposeNote": "records and provide controlled exception-resolution workflows.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every payment reconciliation exception",
       "columns": [
        "PaymentReconciliationExceptionManagementView.paymentGateway",
        "PaymentReconciliationExceptionManagementView.acquirer",
        "PaymentReconciliationExceptionManagementView.bank",
        "PaymentReconciliationExceptionManagementView.pos",
        "PaymentReconciliationExceptionManagementView.ota",
        "PaymentReconciliationExceptionManagementView.reseller",
        "PaymentReconciliationExceptionManagementView.wallet",
        "PaymentReconciliationExceptionManagementView.erp"
       ],
       "bindsTo": "PaymentReconciliationExceptionManagementView",
       "operation": "listPaymentReconciliationException",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 50 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment reconciliation exception",
       "bindsTo": "PaymentReconciliationExceptionManagementView",
       "columns": [
        "PaymentReconciliationExceptionManagementView.paymentGateway",
        "PaymentReconciliationExceptionManagementView.acquirer",
        "PaymentReconciliationExceptionManagementView.bank",
        "PaymentReconciliationExceptionManagementView.pos",
        "PaymentReconciliationExceptionManagementView.ota",
        "PaymentReconciliationExceptionManagementView.reseller",
        "PaymentReconciliationExceptionManagementView.wallet",
        "PaymentReconciliationExceptionManagementView.erp"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Use”, “AED 20”, “Missing AED”, “Resolution Actions”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 50 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment reconciliation exception list.",
   "error": "Could not load. Names which read failed and leaves the payment reconciliation exception untouched.",
   "emptyFirstRun": "No payment reconciliation exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment reconciliation exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentReconciliationException",
    "contract": "orders",
    "purpose": "Payment Reconciliation & Exception Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PaymentReconciliationExceptionManagementView.paymentGateway",
    "PaymentReconciliationExceptionManagementView.acquirer",
    "PaymentReconciliationExceptionManagementView.bank",
    "PaymentReconciliationExceptionManagementView.pos",
    "PaymentReconciliationExceptionManagementView.ota",
    "PaymentReconciliationExceptionManagementView.reseller"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-331"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 50. 8 of 8 labels bound to a contract property; 8 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-332",
  "name": "Financial Traceability, Control & Audit Explorer",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.9",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/financial-traceability-control-audit-explorer-bo-332",
   "component": "apps/venue-management-web/src/routes/orders-money/FinancialTraceabilityControlAuditExplorer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-324",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F142 step 16→17",
     "operation": "listFinancialTraceability"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Where configured) and no display directory — it is settings, not a population",
  "purpose": "Provide a complete financial audit trail across the order lifecycle.",
  "purposeNote": "Every financial change affecting an order is attributable, reconstructable and linked to the responsible transaction, user, rule and approval.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Creator ≠ Approver",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 51 §Where configured"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listFinancialTraceability",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The financial traceability audit configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the financial traceability audit untouched.",
   "emptyFirstRun": "No financial traceability audit configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFinancialTraceability",
    "contract": "orders",
    "purpose": "Financial Traceability, Control & Audit Explorer",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-332"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 51. 0 of 0 labels bound to a contract property; 1 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-333",
  "name": "Order Financial Analytics & AI Reconciliation Intelligence",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "3",
   "number": "12.3.10",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-financial-analytics-ai-reconciliation-intelligence-bo-333",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderFinancialAnalyticsAiReconciliationIntellige.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-324"
   ],
   "exitTo": [
    "BO-324"
   ],
   "inferred": false,
   "notes": "**Reached from BO-324, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare) and no metric row",
  "purpose": "Provide management-level analytics across order payment performance, balances, settlement and reconciliation.",
  "purposeNote": "Management can analyze order-related financial performance and use AI-assisted intelligence to identify collection, payment and reconciliation issues. Board 3 — Final Screen Register # Backend Screen Core Responsibility 12.3. Financial operations Payment & Order Financial Command Center 1 overview 12.3. Complete payment Order Payment Detail & Transaction Ledger 2 history 12.3. Multi-Payment, Split Tender & Payment Multiple payment 3 Allocation Configuration methods 12.3. Deposit, Partial Payment & Outstanding Balance",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search order financial analytics",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 53 §Analyze By"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Event",
        "Product",
        "Channel",
        "Payment Method",
        "Gateway",
        "Customer Segment",
        "B2B Partner",
        "Reseller",
        "OTA",
        "Currency",
        "Period"
       ],
       "notes": "The pack filters this screen by venue, event, product, channel, payment method, gateway and 6 more — which are present is a decision the pack already made.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 53 §Analyze By"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every order financial analytics",
       "columns": [
        "OrderFinancialAnalyticsAiReconciliationIntelligenceView.approvalRate",
        "OrderFinancialAnalyticsAiReconciliationIntelligenceView.failureRate",
        "OrderFinancialAnalyticsAiReconciliationIntelligenceView.settlementDelay",
        "OrderFinancialAnalyticsAiReconciliationIntelligenceView.reconciliationExceptions",
        "Refund Processing Time"
       ],
       "bindsTo": "OrderFinancialAnalyticsAiReconciliationIntelligenceView",
       "operation": "listOrderFinancialReconciliation",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 53 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order financial analytics",
       "bindsTo": "OrderFinancialAnalyticsAiReconciliationIntelligenceView",
       "columns": [
        "OrderFinancialAnalyticsAiReconciliationIntelligenceView.approvalRate",
        "OrderFinancialAnalyticsAiReconciliationIntelligenceView.failureRate",
        "OrderFinancialAnalyticsAiReconciliationIntelligenceView.settlementDelay",
        "OrderFinancialAnalyticsAiReconciliationIntelligenceView.reconciliationExceptions",
        "Refund Processing Time"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Include”, “Payment Initiated”, “Buckets”, “Natural-Language Query”, “Creates and governs the core”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 53 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order financial analytics list.",
   "error": "Could not load. Names which read failed and leaves the order financial analytics untouched.",
   "emptyFirstRun": "No order financial analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order financial analytics are still there. The pack's own statuses are 4 Management — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderFinancialReconciliation",
    "contract": "orders",
    "purpose": "Order Financial Analytics & AI Reconciliation Intelligence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OrderFinancialAnalyticsAiReconciliationIntelligenceView.approvalRate",
    "OrderFinancialAnalyticsAiReconciliationIntelligenceView.failureRate",
    "OrderFinancialAnalyticsAiReconciliationIntelligenceView.settlementDelay",
    "OrderFinancialAnalyticsAiReconciliationIntelligenceView.reconciliationExceptions",
    "Refund Processing Time"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-333"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 53. 4 of 17 labels bound to a contract property; 28 of 94 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listDepositPartialPayment": {
  "method": "GET",
  "path": "/deposit-partial-payment",
  "contract": "orders",
  "summary": "Deposit, Partial Payment & Outstanding Balance Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DepositPartialPaymentOutstandingBalanceManagementView"
 },
 "listExternalPaymentPartner": {
  "method": "GET",
  "path": "/external-payment-partner",
  "contract": "orders",
  "summary": "External Payment, Partner & Settlement Reference Mapping",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ExternalPaymentPartnerSettlementReferenceMappingView"
 },
 "listFinancialTraceability": {
  "method": "GET",
  "path": "/financial-traceability",
  "contract": "orders",
  "summary": "Financial Traceability, Control & Audit Explorer",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FinancialTraceabilityControlAuditExplorerView"
 },
 "listOrderFinancialReconciliation": {
  "method": "GET",
  "path": "/order-financial-reconciliation",
  "contract": "orders",
  "summary": "Order Financial Analytics & AI Reconciliation Intelligence",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "paymentMethod",
    "in": "query",
    "required": false
   },
   {
    "name": "gateway",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "b2bPartner",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "OrderFinancialAnalyticsAiReconciliationIntelligenceView"
 },
 "listOrderPaymentDetail": {
  "method": "GET",
  "path": "/order-payment-detail",
  "contract": "orders",
  "summary": "Order Payment Detail & Transaction Ledger",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderPaymentDetailTransactionLedgerView"
 },
 "listOrderSplitMerge": {
  "method": "GET",
  "path": "/order-split-merge",
  "contract": "orders",
  "summary": "Order Split, Merge & Transaction Relationship Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderSplitMergeTransactionRelationshipManagementView"
 },
 "listPaymentOrderFinancial": {
  "method": "GET",
  "path": "/payment-order-financial",
  "contract": "orders",
  "summary": "Payment & Order Financial Command Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PaymentOrderFinancialCommandCenterView"
 },
 "listPaymentReconciliationException": {
  "method": "GET",
  "path": "/payment-reconciliation-exception",
  "contract": "orders",
  "summary": "Payment Reconciliation & Exception Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PaymentReconciliationExceptionManagementView"
 },
 "listRelatedOrderTransaction": {
  "method": "GET",
  "path": "/related-order-transaction",
  "contract": "orders",
  "summary": "Related Order & Transaction Relationship Explorer",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "order",
    "in": "query",
    "required": false
   },
   {
    "name": "ticket",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
    "in": "query",
    "required": false
   },
   {
    "name": "externalReference",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerBooking",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "RelatedOrderTransactionRelationshipExplorerView"
 },
 "setMultiPaymentSplit": {
  "method": "PUT",
  "path": "/multi-payment-split",
  "contract": "orders",
  "summary": "Multi-Payment, Split Tender & Payment Allocation Configuration",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "MultiPaymentSplitTenderPaymentAllocationConfiguratioInput",
  "responds": "MultiPaymentSplitTenderPaymentAllocationConfiguratioView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "DepositPartialPaymentOutstandingBalanceManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Deposit, Partial Payment & Outstanding Balance Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "groups": {
    "type": "string",
    "description": "Groups"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "corporateSales": {
    "type": "string",
    "description": "Corporate Sales"
   },
   "schools": {
    "type": "string",
    "description": "Schools"
   },
   "events": {
    "type": "string",
    "description": "Events"
   },
   "largeReservations": {
    "type": "string",
    "description": "Large Reservations"
   },
   "fullPayment": {
    "type": "string",
    "description": "Full Payment"
   },
   "fixedDeposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed Deposit"
   },
   "percentageDeposit": {
    "type": "number",
    "description": "Percentage Deposit"
   },
   "stagedPayment": {
    "type": "string",
    "description": "Staged Payment"
   },
   "balanceBeforeVisit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Balance Before Visit"
   },
   "balanceByFixedDate": {
    "type": "string",
    "format": "date-time",
    "description": "Balance by Fixed Date"
   },
   "creditAccount": {
    "type": "string",
    "description": "Credit Account"
   },
   "payOnCollectionWherePermitted": {
    "type": "string",
    "description": "Pay on Collection where permitted"
   },
   "requiredDeposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Required Deposit (the pack shows 20% = AED 5,000)"
   },
   "total": {
    "type": "integer",
    "description": "Total"
   },
   "depositRequired": {
    "type": "boolean",
    "description": "Deposit Required"
   },
   "depositPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit Paid"
   },
   "remainingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Remaining Balance"
   },
   "dueDate": {
    "type": "string",
    "format": "date-time",
    "description": "Due Date"
   },
   "daysRemaining": {
    "type": "string",
    "description": "Days Remaining"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "warning": {
    "type": "string",
    "description": "Warning"
   },
   "gracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Grace Period"
   },
   "requireApproval": {
    "type": "boolean",
    "description": "Require Approval"
   },
   "paymentReminder": {
    "type": "string",
    "description": "Payment Reminder"
   },
   "dueSoon": {
    "type": "string",
    "description": "Due Soon"
   },
   "overdue": {
    "type": "string",
    "description": "Overdue"
   },
   "finalNotice": {
    "type": "string",
    "description": "Final Notice"
   }
  }
 },
 "ExternalPaymentPartnerSettlementReferenceMappingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What External Payment, Partner & Settlement Reference Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "paymentGateways": {
    "type": "string",
    "description": "Payment Gateways"
   },
   "acquirers": {
    "type": "string",
    "description": "Acquirers"
   },
   "banks": {
    "type": "string",
    "description": "Banks"
   },
   "posTerminals": {
    "type": "string",
    "description": "POS Terminals"
   },
   "b2bPartners": {
    "type": "string",
    "description": "B2B Partners"
   },
   "resellers": {
    "type": "string",
    "description": "Resellers"
   },
   "otas": {
    "type": "string",
    "description": "OTAs"
   },
   "erp": {
    "type": "string",
    "description": "ERP"
   },
   "financeSystems": {
    "type": "string",
    "description": "Finance Systems"
   },
   "walletProviders": {
    "type": "string",
    "description": "Wallet Providers"
   },
   "ticvaiOrderId": {
    "type": "string",
    "description": "TICVAI Order ID"
   },
   "ticvaiPaymentId": {
    "type": "string",
    "description": "TICVAI Payment ID"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "merchantId": {
    "type": "string",
    "description": "Merchant ID"
   },
   "externalTransactionId": {
    "type": "string",
    "description": "External Transaction ID"
   },
   "authorizationCode": {
    "type": "string",
    "description": "Authorization Code"
   },
   "partnerOrderId": {
    "type": "string",
    "description": "Partner Order ID"
   },
   "settlementBatch": {
    "type": "string",
    "description": "Settlement Batch"
   },
   "settlementDate": {
    "type": "string",
    "format": "date-time",
    "description": "Settlement Date"
   },
   "erpReference": {
    "type": "string",
    "description": "ERP Reference"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "multiplePayments": {
    "type": "string",
    "description": "Multiple Payments"
   },
   "multipleGatewayTransactions": {
    "type": "string",
    "description": "Multiple Gateway Transactions"
   },
   "multipleRefunds": {
    "type": "string",
    "description": "Multiple Refunds"
   },
   "multiplePartnerReferences": {
    "type": "string",
    "description": "Multiple Partner References"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "approvalWhereRequired": {
    "type": "boolean",
    "description": "Approval where required"
   }
  }
 },
 "FinancialTraceabilityControlAuditExplorerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Financial Traceability, Control & Audit Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "priceVersion": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Version"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment Method"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "manualPaymentAdjustment": {
    "type": "string",
    "description": "Manual Payment Adjustment"
   },
   "manualAllocation": {
    "type": "string",
    "description": "Manual Allocation"
   },
   "manualReconciliation": {
    "type": "string",
    "description": "Manual Reconciliation"
   },
   "manualRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Manual Refund"
   },
   "feeWaiver": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Waiver"
   },
   "creditOverride": {
    "type": "string",
    "description": "Credit Override"
   },
   "manualSettlementMapping": {
    "type": "string",
    "description": "Manual Settlement Mapping"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "internalAudit": {
    "type": "string",
    "description": "Internal Audit"
   },
   "externalAudit": {
    "type": "string",
    "description": "External Audit"
   },
   "compliance": {
    "type": "string",
    "description": "Compliance"
   },
   "management": {
    "type": "string",
    "description": "Management"
   }
  }
 },
 "MultiPaymentSplitTenderPaymentAllocationConfiguratioInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Multi-Payment, Split Tender & Payment Allocation Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "terminal": {
    "type": "string",
    "description": "Terminal"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "orderType": {
    "type": "string",
    "description": "Order Type"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "walletAed250": {
    "type": "string",
    "description": "Wallet — AED 250"
   },
   "voucherAed150": {
    "type": "string",
    "description": "Voucher — AED 150"
   },
   "visaAed600": {
    "type": "string",
    "description": "Visa — AED 600"
   },
   "orderLevel": {
    "type": "string",
    "description": "Order Level"
   },
   "orderLineLevel": {
    "type": "string",
    "description": "Order-Line Level"
   },
   "productLevel": {
    "type": "string",
    "description": "Product Level"
   },
   "taxFeeComponent": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tax/Fee Component"
   },
   "specificTicket": {
    "type": "string",
    "description": "Specific Ticket"
   },
   "deposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit"
   },
   "destination": {
    "type": "string",
    "description": "destination"
   }
  }
 },
 "MultiPaymentSplitTenderPaymentAllocationConfiguratioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Multi-Payment, Split Tender & Payment Allocation Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "terminal": {
    "type": "string",
    "description": "Terminal"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "orderType": {
    "type": "string",
    "description": "Order Type"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "walletAed250": {
    "type": "string",
    "description": "Wallet — AED 250"
   },
   "voucherAed150": {
    "type": "string",
    "description": "Voucher — AED 150"
   },
   "visaAed600": {
    "type": "string",
    "description": "Visa — AED 600"
   },
   "orderLevel": {
    "type": "string",
    "description": "Order Level"
   },
   "orderLineLevel": {
    "type": "string",
    "description": "Order-Line Level"
   },
   "productLevel": {
    "type": "string",
    "description": "Product Level"
   },
   "taxFeeComponent": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tax/Fee Component"
   },
   "specificTicket": {
    "type": "string",
    "description": "Specific Ticket"
   },
   "deposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit"
   },
   "destination": {
    "type": "string",
    "description": "destination"
   }
  }
 },
 "OrderFinancialAnalyticsAiReconciliationIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Financial Analytics & AI Reconciliation Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "grossOrderValue": {
    "type": "string",
    "description": "Gross Order Value"
   },
   "netCollected": {
    "type": "string",
    "description": "Net Collected"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "collectionRate": {
    "type": "number",
    "description": "Collection Rate"
   },
   "paymentFailureRate": {
    "type": "number",
    "description": "Payment Failure Rate"
   },
   "reconciliationRate": {
    "type": "number",
    "description": "Reconciliation Rate"
   },
   "settlementVariance": {
    "type": "string",
    "description": "Settlement Variance"
   },
   "averagePaymentMethodsPerOrder": {
    "type": "number",
    "description": "Average Payment Methods per Order"
   },
   "depositExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit Exposure"
   },
   "overdueBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Overdue Balance"
   },
   "current": {
    "type": "string",
    "description": "Current"
   },
   "approvalRate": {
    "type": "number",
    "description": "Approval Rate"
   },
   "failureRate": {
    "type": "number",
    "description": "Failure Rate"
   },
   "settlementDelay": {
    "type": "string",
    "description": "Settlement Delay"
   },
   "reconciliationExceptions": {
    "type": "string",
    "description": "Reconciliation Exceptions"
   },
   "backendScreenCoreResponsibility": {
    "type": "string",
    "description": "# Backend Screen Core Responsibility"
   },
   "area12FinalArchitecture": {
    "type": "string",
    "description": "Area 12 — Final Architecture"
   },
   "orderReservation": {
    "type": "string",
    "description": "order/reservation"
   },
   "paymentGatewayModules": {
    "type": "string",
    "description": "Payment Gateway modules"
   },
   "sow": {
    "type": "string",
    "description": "SOW"
   }
  }
 },
 "OrderPaymentDetailTransactionLedgerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Payment Detail & Transaction Ledger displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "orderNumber": {
    "type": "string",
    "description": "Order Number"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "orderTotal": {
    "type": "string",
    "description": "Order Total"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "paid": {
    "type": "string",
    "description": "Paid"
   },
   "refunded": {
    "type": "string",
    "description": "Refunded"
   },
   "outstanding": {
    "type": "string",
    "description": "Outstanding"
   },
   "creditApplied": {
    "type": "string",
    "description": "Credit Applied"
   },
   "paymentStatus": {
    "type": "integer",
    "description": "Payment Status"
   },
   "settlementStatus": {
    "type": "integer",
    "description": "Settlement Status"
   },
   "onOdNt": {
    "type": "string",
    "description": "on od nt"
   },
   "nt300": {
    "type": "string",
    "description": "nt 300"
   },
   "nt100": {
    "type": "string",
    "description": "nt 100"
   },
   "aedComplete": {
    "type": "string",
    "description": "AED Complete"
   },
   "authorization": {
    "type": "string",
    "description": "Authorization"
   },
   "capture": {
    "type": "string",
    "description": "Capture"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "deposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit"
   },
   "additionalCollection": {
    "type": "string",
    "description": "Additional Collection"
   },
   "partialRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partial Refund"
   },
   "reversal": {
    "type": "string",
    "description": "Reversal"
   },
   "walletCredit": {
    "type": "string",
    "description": "Wallet Credit"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "creditNote": {
    "type": "string",
    "description": "Credit Note"
   },
   "adjustment": {
    "type": "string",
    "description": "Adjustment"
   },
   "gateway": {
    "type": "string",
    "description": "Gateway"
   },
   "merchant": {
    "type": "string",
    "description": "Merchant"
   },
   "terminal": {
    "type": "string",
    "description": "Terminal"
   },
   "authorizationCode": {
    "type": "string",
    "description": "Authorization Code"
   },
   "gatewayTransactionId": {
    "type": "string",
    "description": "Gateway Transaction ID"
   },
   "settlementReference": {
    "type": "string",
    "description": "Settlement Reference"
   },
   "externalReference": {
    "type": "string",
    "description": "External Reference"
   }
  }
 },
 "OrderSplitMergeTransactionRelationshipManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Split, Merge & Transaction Relationship Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "orderA4Tickets": {
    "type": "string",
    "description": "Order A — 4 Tickets"
   },
   "orderB2Tickets": {
    "type": "string",
    "description": "Order B — 2 Tickets"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "attendee": {
    "type": "string",
    "description": "Attendee"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "orderLine": {
    "type": "string",
    "description": "Order Line"
   },
   "paymentResponsibility": {
    "type": "string",
    "description": "Payment Responsibility"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "corporateCostCenter": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Corporate Cost Center"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "taxContext": {
    "type": "string",
    "description": "Tax Context"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment Status"
   },
   "productCompatibility": {
    "type": "string",
    "description": "Product Compatibility"
   },
   "parentOrder": {
    "type": "string",
    "description": "Parent Order"
   },
   "childOrder": {
    "type": "string",
    "description": "Child Order"
   },
   "mergedInto": {
    "type": "string",
    "description": "Merged Into"
   },
   "replacementOrder": {
    "type": "string",
    "description": "Replacement Order"
   },
   "amendedFrom": {
    "type": "string",
    "description": "Amended From"
   },
   "convertedFrom": {
    "type": "string",
    "description": "Converted From"
   },
   "reissuedFrom": {
    "type": "string",
    "description": "Reissued From"
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Base Price"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "fees": {
    "type": "string",
    "description": "Fees"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "payments": {
    "type": "string",
    "description": "Payments"
   },
   "refunds": {
    "type": "string",
    "description": "Refunds"
   },
   "credits": {
    "type": "string",
    "description": "Credits"
   },
   "correctlyAcrossDerivedOrders": {
    "type": "string",
    "description": "correctly across derived orders"
   },
   "neverEraseTheOriginalRelationship": {
    "type": "string",
    "description": "Never erase the original relationship"
   }
  }
 },
 "PaymentOrderFinancialCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Payment & Order Financial Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "grossOrderValue": {
    "type": "string",
    "description": "Gross Order Value"
   },
   "fullyPaidOrders": {
    "type": "integer",
    "description": "Fully Paid Orders"
   },
   "partiallyPaidOrders": {
    "type": "integer",
    "description": "Partially Paid Orders"
   },
   "unpaidOrders": {
    "type": "integer",
    "description": "Unpaid Orders"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "paymentsToday": {
    "type": "string",
    "description": "Payments Today"
   },
   "failedPayments": {
    "type": "integer",
    "description": "Failed Payments"
   },
   "pendingPayments": {
    "type": "integer",
    "description": "Pending Payments"
   },
   "refundsPending": {
    "type": "integer",
    "description": "Refunds Pending"
   },
   "reconciliationExceptions": {
    "type": "integer",
    "description": "Reconciliation Exceptions"
   },
   "unallocatedPayments": {
    "type": "integer",
    "description": "Unallocated Payments"
   },
   "settlementVariance": {
    "type": "string",
    "description": "Settlement Variance"
   },
   "orderId": {
    "type": "string",
    "description": "Order ID"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "orderValue": {
    "type": "string",
    "description": "Order Value"
   },
   "amountPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount Paid"
   },
   "refunded": {
    "type": "string",
    "description": "Refunded"
   },
   "outstanding": {
    "type": "string",
    "description": "Outstanding"
   },
   "paymentMethods": {
    "type": "integer",
    "description": "Payment Methods"
   },
   "paymentStatus": {
    "type": "integer",
    "description": "Payment Status"
   },
   "settlementStatus": {
    "type": "integer",
    "description": "Settlement Status"
   },
   "reconciliationStatus": {
    "type": "integer",
    "description": "Reconciliation Status"
   },
   "notRequired": {
    "type": "boolean",
    "description": "Not Required"
   },
   "unpaid": {
    "type": "string",
    "description": "Unpaid"
   },
   "paymentInitiated": {
    "type": "string",
    "description": "Payment Initiated"
   },
   "authorized": {
    "type": "string",
    "description": "Authorized"
   },
   "partiallyPaid": {
    "type": "string",
    "description": "Partially Paid"
   },
   "paid": {
    "type": "string",
    "description": "Paid"
   },
   "overpaid": {
    "type": "string",
    "description": "Overpaid"
   },
   "partiallyRefunded": {
    "type": "string",
    "description": "Partially Refunded"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "reversed": {
    "type": "string",
    "description": "Reversed"
   },
   "reconciliationRequired": {
    "type": "boolean",
    "description": "Reconciliation Required"
   },
   "by": {
    "type": "string",
    "description": "By"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment Method"
   },
   "paymentProvider": {
    "type": "string",
    "description": "Payment Provider"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "orderStatus": {
    "type": "string",
    "description": "Order Status"
   }
  }
 },
 "PaymentReconciliationExceptionManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Payment Reconciliation & Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "paymentGateway": {
    "type": "string",
    "description": "Payment Gateway"
   },
   "acquirer": {
    "type": "string",
    "description": "Acquirer"
   },
   "bank": {
    "type": "string",
    "description": "Bank"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "ota": {
    "type": "string",
    "description": "OTA"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "erp": {
    "type": "string",
    "description": "ERP"
   },
   "transactionId": {
    "type": "string",
    "description": "Transaction ID"
   },
   "externalReference": {
    "type": "string",
    "description": "External Reference"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "merchant": {
    "type": "string",
    "description": "Merchant"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "authorizationCode": {
    "type": "string",
    "description": "Authorization Code"
   },
   "mismatch500480": {
    "type": "string",
    "description": "mismatch 500 480"
   },
   "aed250": {
    "type": "string",
    "description": "AED 250"
   },
   "settlement250": {
    "type": "string",
    "description": "settlement 250"
   },
   "match": {
    "type": "string",
    "description": "Match"
   },
   "remap": {
    "type": "string",
    "description": "Remap"
   },
   "investigate": {
    "type": "string",
    "description": "Investigate"
   },
   "markPending": {
    "type": "integer",
    "description": "Mark Pending"
   }
  }
 },
 "RelatedOrderTransactionRelationshipExplorerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Related Order & Transaction Relationship Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "amendment": {
    "type": "string",
    "description": "↓ Amendment"
   },
   "ticketUpgrade": {
    "type": "string",
    "description": "↓ Ticket Upgrade"
   },
   "additionalPayment": {
    "type": "string",
    "description": "↓ Additional Payment"
   },
   "partialCancellation": {
    "type": "string",
    "description": "↓ Partial Cancellation"
   },
   "refund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "↓ Refund"
   },
   "original": {
    "type": "string",
    "description": "Original"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "exchange": {
    "type": "string",
    "description": "Exchange"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "chargebackWhereIntegrated": {
    "type": "string",
    "description": "Chargeback where integrated"
   },
   "externalTransaction": {
    "type": "string",
    "description": "External Transaction"
   }
  }
 }
}
```
