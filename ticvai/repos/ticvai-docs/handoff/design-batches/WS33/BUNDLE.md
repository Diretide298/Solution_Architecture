# WS33 — Order   Reservation Management board 3

**10 screens · 15 operations · 14 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PAYMENT_CONFIGURE, PAYMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
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
| `BO-327` | Deposit, Partial Payment & Outstanding Balance Management | listDetail | 5 | 1 | — |
| `BO-328` | Order Split, Merge & Transaction Relationship Management | listDetail | 2 | 0 | — |
| `BO-329` | Related Order & Transaction Relationship Explorer | listDetail | 1 | 0 | — |
| `BO-330` | External Payment, Partner & Settlement Reference Mapping | configEditor | 1 | 0 | — |
| `BO-331` | Payment Reconciliation & Exception Management | listDetail | 1 | 0 | — |
| `BO-332` | Financial Traceability, Control & Audit Explorer | configEditor | 1 | 0 | — |
| `BO-333` | Order Financial Analytics & AI Reconciliation Intelligence | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-331, BO-332 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-324 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
    },
    {
     "to": "BO-328",
     "trigger": "Works in Order Split, Merge & Transaction Relationship Management",
     "provenance": "flow F142 step 7→8",
     "operation": "listPaymentOrderFinancial",
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can monitor the complete payment and financial condition of orders across all TICVAI channels from one workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide operations and finance teams with a centralized view of the financial status of all",
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
        "PaymentOrderFinancialCommandCenterView.channel",
        "PaymentOrderFinancialCommandCenterView.paymentMethods",
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
       "label": "Payment Initiated",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 40 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Authorized",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 40 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Failed",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 40 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Reconciliation Required",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-324",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-324"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 40. 31 of 33 labels bound to a contract property; 37 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Authorized, Failed, Reconciliation Required are choices sent by `listPaymentOrderFinancial`.",
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
  "purposeNote": "Users can reconstruct every financial movement associated with an order from initial authorization through final refund/reversal.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the complete payment history associated with an individual order.",
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
       "label": "Payment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Deposit",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Additional Collection",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Refund",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partial Refund",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Reversal",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-325",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-325"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 41. 10 of 10 labels bound to a contract property; 28 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Capture, Deposit, Additional Collection, Refund, Partial Refund, Void, Reversal, Wallet Credit … are choices sent by `listOrderPaymentDetail`.",
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
  "purposeNote": "every monetary amount to the relevant order components.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Configure whether payment is allocated) and no display directory — it is settings, not a population",
  "purpose": "Support orders paid using multiple payment methods and determine how each payment is allocated.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-326",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-326"
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
  "purposeNote": "controlling reservation and fulfillment states.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Support commercial scenarios where an order may be confirmed or reserved without full immediate payment.",
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
      },
      {
       "kind": "detailPanel",
       "label": "Table deposit (dining)",
       "bindsTo": "DiningDepositPolicy",
       "columns": [
        "DiningDepositPolicy.enabled",
        "DiningDepositPolicy.basis",
        "DiningDepositPolicy.amount",
        "DiningDepositPolicy.percent",
        "DiningDepositPolicy.minimumSpendPerGuest",
        "DiningDepositPolicy.appliesFromPartySize",
        "DiningDepositPolicy.outletIds",
        "DiningDepositPolicy.collection",
        "DiningDepositPolicy.depositVariantId",
        "DiningDepositPolicy.refundableUntilHours",
        "DiningDepositPolicy.onLateCancelOrNoShow",
        "DiningDepositPolicy.onArrival"
       ],
       "operation": "getDepositPolicy",
       "notes": "**A venue option, off unless the venue switches it on here** (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a) \"no table deposit in the first release\": the capability ships, disabled by default). The venue sets from what party size it applies, the basis (per guest, per table, or a percentage of a minimum spend) and the amount; nothing about the amount is fixed in code. While it is off a table booking takes no payment and the guest sees a \"no card needed\" confirmation (REV3-8).",
       "provenance": "contract orders.yaml GET /deposit-policy"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Full Payment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Fixed Deposit",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Percentage Deposit",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Staged Payment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Balance Before Visit",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Balance by Fixed Date",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Credit Account",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save table deposit",
       "operation": "setDepositPolicy",
       "provenance": "contract orders.yaml PUT /deposit-policy"
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
    "operationId": "getDepositPolicy",
    "contract": "orders",
    "purpose": "How deposits work",
    "trigger": "onLoad"
   },
   {
    "operationId": "setDepositPolicy",
    "contract": "orders",
    "purpose": "Set deposit amount, balance due and refund cut-off",
    "trigger": "onAction"
   },
   {
    "operationId": "listDepositPartialPayment",
    "contract": "orders",
    "purpose": "Deposit, Partial Payment & Outstanding Balance Management",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDepositActivity",
    "contract": "payments",
    "purpose": "What has happened against this deposit",
    "trigger": "onAction"
   },
   {
    "operationId": "recordDepositActivity",
    "contract": "payments",
    "purpose": "Record a capture, release or adjustment",
    "trigger": "onAction"
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
   ],
   "params": [
    {
     "name": "depositId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-327",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-327"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 44. 7 of 7 labels bound to a contract property; 21 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Full Payment, Fixed Deposit, Percentage Deposit, Staged Payment, Balance Before Visit, Balance by Fixed Date, Credit Account are choices sent by `setDepositPolicy`.",
  "overlays": [
   {
    "id": "formSetDiningDeposit",
    "component": "modal",
    "trigger": "Save table deposit",
    "body": "**Collects the `dining` block of what `setDepositPolicy` sends before it is called** (decided 29 September, rev 3 REV3-8b). `enabled` (off by default), `basis` (`fixedPerGuest`, `fixedPerTable` or `percentOfMinimumSpend`), `amount` for the fixed bases, `percent` and `minimumSpendPerGuest` for the percentage basis, `appliesFromPartySize`, `outletIds` (empty means every outlet that takes bookings), `collection` (authorise and capture only on a late cancel or no-show, or charge), `depositVariantId`, `refundableUntilHours`, `onLateCancelOrNoShow`, `onArrival`. **Switched on with no amount or percent for its basis, or no deposit variant, it is refused `400`** and the modal stays open with the field marked. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "DepositPolicy",
    "confirm": {
     "label": "Save table deposit",
     "operation": "setDepositPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "dining"
     ]
    },
    "provenance": "contract orders.yaml PUT /deposit-policy"
   }
  ],
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
  "purposeNote": "Orders can be split or merged while maintaining accurate financial, customer, product, payment and historical relationships.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow complex orders to be reorganized without destroying transaction history.",
  "gaps": [
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
       "label": "Product",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Order Line",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Responsibility",
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
   },
   {
    "operationId": "splitOrder",
    "contract": "orders",
    "purpose": "Split the order by ticket, product or payment responsibility",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Ticket, Product, Payment Responsibility",
    "invalidates": [
     "listOrderSplitMerge"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "OrderSplitMergeTransactionRelationshipManagementView.splitBasis"
   ],
   "coldEntry": "Opened from BO-324 with the order picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the order no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-328",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-328"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 46. 0 of 0 labels bound to a contract property; 4 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Ticket, Product, Payment Responsibility: `splitOrder`.",
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
  "purposeNote": "Users can understand complex transaction chains without manually searching multiple systems or screens.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a visual relationship map for complex transaction histories. This becomes especially useful after amendments, upgrades, exchanges, reissues, splits and refunds.",
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
        "RelatedOrderTransactionRelationshipExplorerView.relationshipType",
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
        "RelatedOrderTransactionRelationshipExplorerView.relationshipType",
        "Amendment",
        "Upgrade",
        "Split",
        "Merge",
        "Reissue",
        "Refund"
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
        "RelatedOrderTransactionRelationshipExplorerView.relationshipType",
        "Amendment",
        "Upgrade",
        "Split",
        "Merge",
        "Reissue",
        "Refund"
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
    "RelatedOrderTransactionRelationshipExplorerView.relationshipType",
    "Amendment",
    "Upgrade",
    "Split"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-329",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-329"
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
  "purposeNote": "relevant external transaction and settlement references.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Maintain the relationship between TICVAI transactions and external financial/channel references.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Payment Gateways",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Support references from"
      },
      {
       "kind": "secondaryButton",
       "label": "POS Terminals",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Support references from"
      },
      {
       "kind": "secondaryButton",
       "label": "Finance Systems",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Support references from"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Providers",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 49 §Support references from"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-330",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-330"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 49. 0 of 0 labels bound to a contract property; 16 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** POS Terminals, Finance Systems, Wallet Providers are choices sent by `listExternalPaymentPartner`.",
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
  "purposeNote": "records and provide controlled exception-resolution workflows.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare) and no metric row",
  "purpose": "Automatically compare TICVAI payment records with external payment and settlement records.",
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
        "PaymentReconciliationExceptionManagementView.sourceSystem"
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
        "PaymentReconciliationExceptionManagementView.sourceSystem"
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
    "PaymentReconciliationExceptionManagementView.sourceSystem"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-331",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-331"
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
  "purposeNote": "Every financial change affecting an order is attributable, reconstructable and linked to the responsible transaction, user, rule and approval.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Where configured) and no display directory — it is settings, not a population",
  "purpose": "Provide a complete financial audit trail across the order lifecycle.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-332",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-332"
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
  "purposeNote": "Management can analyze order-related financial performance and use AI-assisted intelligence to identify collection, payment and reconciliation issues. Board 3 — Final Screen Register # Backend Screen Core Responsibility 12.3. Financial operations Payment & Order Financial Command Center 1 overview 12.3. Complete payment Order Payment Detail & Transaction Ledger 2 history 12.3. Multi-Payment, Split Tender & Payment Multiple payment 3 Allocation Configuration methods 12.3. Deposit, Partial Payment & Outstanding Balance",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare) and no metric row",
  "purpose": "Provide management-level analytics across order payment performance, balances, settlement and reconciliation.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-333",
   "workshopBoard": "wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-333"
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
 "getDepositPolicy": {
  "method": "GET",
  "path": "/deposit-policy",
  "contract": "orders",
  "summary": "What a deposit booking takes now and when the rest is due",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DepositPolicy"
 },
 "listDepositActivity": {
  "method": "GET",
  "path": "/deposits/{depositId}/activity",
  "contract": "payments",
  "summary": "Movements on a deposit",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "depositId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "PaymentsDepositActivity"
 },
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
  "parameters": [
   {
    "name": "export",
    "in": "query",
    "required": false
   }
  ],
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
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "paymentProvider",
    "in": "query",
    "required": false
   },
   {
    "name": "currency",
    "in": "query",
    "required": false
   },
   {
    "name": "orderStatus",
    "in": "query",
    "required": false
   }
  ],
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
   },
   {
    "name": "payment",
    "in": "query",
    "required": false
   },
   {
    "name": "refund",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "RelatedOrderTransactionRelationshipExplorerView"
 },
 "recordDepositActivity": {
  "method": "POST",
  "path": "/deposits/{depositId}/activity",
  "contract": "payments",
  "summary": "Record a movement on a deposit",
  "permission": "PAYMENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "depositId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PaymentsDepositActivity",
  "responds": "PaymentsDepositActivity"
 },
 "setDepositPolicy": {
  "method": "PUT",
  "path": "/deposit-policy",
  "contract": "orders",
  "summary": "Set how deposits work",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "DepositPolicy",
  "responds": "DepositPolicy"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "MultiPaymentSplitTenderPaymentAllocationConfiguratioInput",
  "responds": "MultiPaymentSplitTenderPaymentAllocationConfiguratioView"
 },
 "splitOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/split",
  "contract": "orders",
  "summary": "Break one order into independent orders",
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
   "appliesTo": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "groups",
      "b2b",
      "corporateSales",
      "schools",
      "events",
      "largeReservations"
     ]
    },
    "description": "Bookings this deposit model applies to."
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "fullPayment",
     "fixedDeposit",
     "percentageDeposit",
     "stagedPayment",
     "balanceBeforeVisit",
     "balanceByFixedDate",
     "creditAccount",
     "payOnCollection"
    ],
    "description": "Payment model."
   },
   "reminderStage": {
    "type": "string",
    "enum": [
     "paymentReminder",
     "dueSoon",
     "overdue",
     "finalNotice"
    ],
    "description": "Balance reminder stage."
   }
  }
 },
 "DepositPolicy": {
  "type": "object",
  "x-ticvai-persistence": "orders.deposit_policy",
  "required": [
   "basis"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "appliesTo": {
    "type": "array",
    "description": "Which bookings the top-level `basis` covers. **`dining` is deprecated here since 29 September** (rev 3 REV3-8b): a table deposit is the `dining` block below, with its own switch, basis and amount, and `setDepositPolicy` refuses `dining` in this list with 400.\n",
    "items": {
     "type": "string",
     "enum": [
      "party",
      "dining",
      "school",
      "event"
     ]
    }
   },
   "dining": {
    "$ref": "#/components/schemas/DiningDepositPolicy"
   },
   "basis": {
    "type": "string",
    "enum": [
     "fixedPerBooking",
     "fixedPerGuest",
     "percentOfTotal",
     "perBand"
    ]
   },
   "amount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "percent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true
   },
   "bandSize": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "`perBand`: one `amount` per this much of the total, e.g. AED 100 per AED 400."
   },
   "balanceDue": {
    "type": "string",
    "enum": [
     "onTheDay",
     "daysBefore"
    ],
    "default": "onTheDay"
   },
   "balanceDueDaysBefore": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "refundableUntilHours": {
    "type": "integer",
    "minimum": 0,
    "default": 24
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   }
  }
 },
 "DiningDepositPolicy": {
  "type": "object",
  "x-ticvai-persistence": "orders.deposit_policy (dining_* columns)",
  "description": "**The table deposit hold: a venue option, off unless the venue enables it** (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a) \"no table deposit in the first release\"; the capability ships, disabled by default). Set in Venue Management through `setDepositPolicy` and read by `fnb.createTableReservation`. **Nothing about the amount is in code**: the AED 100 per guest in the rev 3 prototype is an example a venue may type, not a default. With `enabled` false a table booking takes no payment and never enters the cart (rev 3 REV3-8).\n",
  "properties": {
   "enabled": {
    "type": "boolean",
    "default": false,
    "description": "Off unless the venue enables it. While false every other field is kept but not applied."
   },
   "basis": {
    "type": "string",
    "enum": [
     "fixedPerGuest",
     "fixedPerTable",
     "percentOfMinimumSpend"
    ],
    "default": "fixedPerGuest",
    "description": "`fixedPerGuest`, `amount` times the party size; `fixedPerTable`, `amount` once per booking; `percentOfMinimumSpend`, `percent` of `minimumSpendPerGuest` times the party size.\n"
   },
   "amount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Required for the two fixed bases."
   },
   "percent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Required for `percentOfMinimumSpend`."
   },
   "minimumSpendPerGuest": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Required for `percentOfMinimumSpend`."
   },
   "appliesFromPartySize": {
    "type": "integer",
    "minimum": 1,
    "maximum": 50,
    "default": 1,
    "description": "A party smaller than this books with no deposit. Proposed default, client to correct."
   },
   "outletIds": {
    "type": "array",
    "description": "The outlets it applies to. Empty means every outlet of the venue that takes bookings.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "collection": {
    "type": "string",
    "enum": [
     "authorisationHold",
     "charge"
    ],
    "default": "authorisationHold",
    "description": "`authorisationHold` authorises the card and captures only on a late cancel or no-show; `charge` takes the money now and holds it as a deposit. Either way it is an `orders.deposit` row, not a sale. A hold the card network would let lapse before the booking date is taken as `charge` instead, and the guest is told so.\n"
   },
   "depositVariantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The catalogue variant the deposit line is sold as: a non-inventory product the venue set up whose ledger mapping posts to deposit liability, not revenue. Required while `enabled` is true.\n"
   },
   "refundableUntilHours": {
    "type": "integer",
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Cancelling at least this long before the booking releases the deposit in full. Proposed default, client to correct."
   },
   "onLateCancelOrNoShow": {
    "type": "string",
    "enum": [
     "forfeit",
     "release"
    ],
    "default": "forfeit",
    "description": "What happens to the deposit on a later cancel or a `noShow`. Settled through `finance.settleDeposit`."
   },
   "onArrival": {
    "type": "string",
    "enum": [
     "releaseHold",
     "applyToBill"
    ],
    "default": "releaseHold",
    "description": "When the party is seated, release the deposit or put it towards the bill."
   }
  }
 },
 "ExternalPaymentPartnerSettlementReferenceMappingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What External Payment, Partner & Settlement Reference Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "approvalReference": {
    "type": "boolean",
    "description": "Approval where required"
   },
   "sourceSystem": {
    "type": "string",
    "enum": [
     "paymentGateways",
     "acquirers",
     "banks",
     "posTerminals",
     "b2bPartners",
     "resellers",
     "otas",
     "erp",
     "financeSystems",
     "walletProviders"
    ],
    "description": "External system the reference comes from."
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
   "interventionType": {
    "type": "string",
    "enum": [
     "manualPaymentAdjustment",
     "manualAllocation",
     "manualReconciliation",
     "manualRefund",
     "feeWaiver",
     "creditOverride",
     "manualSettlementMapping"
    ],
    "description": "Manual intervention recorded."
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
   "allocationLevel": {
    "type": "string",
    "enum": [
     "orderLevel",
     "orderLineLevel",
     "productLevel",
     "taxFeeComponent",
     "specificTicket",
     "deposit"
    ],
    "description": "What a payment is allocated against."
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
   "allocationLevel": {
    "type": "string",
    "enum": [
     "orderLevel",
     "orderLineLevel",
     "productLevel",
     "taxFeeComponent",
     "specificTicket",
     "deposit"
    ],
    "description": "What a payment is allocated against."
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
   "transactions": {
    "type": "array",
    "description": "Every financial transaction on the order, one entry each",
    "items": {
     "type": "object",
     "properties": {
      "type": {
       "type": "string",
       "enum": [
        "authorization",
        "capture",
        "payment",
        "deposit",
        "additionalCollection",
        "partialRefund",
        "reversal",
        "walletCredit",
        "voucher",
        "creditNote",
        "adjustment"
       ],
       "description": "Transaction type"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Amount"
      },
      "status": {
       "type": "string",
       "description": "Status"
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
       "description": "Authorization code"
      },
      "gatewayTransactionId": {
       "type": "string",
       "description": "Gateway transaction ID"
      },
      "settlementReference": {
       "type": "string",
       "description": "Settlement reference"
      },
      "externalReference": {
       "type": "string",
       "description": "External reference"
      },
      "occurredAt": {
       "type": "string",
       "format": "date-time",
       "description": "When"
      }
     }
    }
   }
  }
 },
 "OrderSplitMergeTransactionRelationshipManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Split, Merge & Transaction Relationship Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "splitBasis": {
    "type": "string",
    "enum": [
     "ticket",
     "attendee",
     "product",
     "orderLine",
     "paymentResponsibility",
     "department",
     "corporateCostCenter",
     "customer"
    ],
    "description": "What the order is split by."
   },
   "relationshipType": {
    "type": "string",
    "enum": [
     "parentOrder",
     "childOrder",
     "mergedInto",
     "replacementOrder",
     "amendedFrom",
     "convertedFrom",
     "reissuedFrom"
    ],
    "description": "How the orders relate."
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
   "settlementStatus": {
    "type": "integer",
    "description": "Settlement Status"
   },
   "reconciliationStatus": {
    "type": "integer",
    "description": "Reconciliation Status"
   },
   "paymentStatus": {
    "type": "string",
    "enum": [
     "notRequired",
     "unpaid",
     "paymentInitiated",
     "authorized",
     "partiallyPaid",
     "paid",
     "overpaid",
     "partiallyRefunded",
     "refunded",
     "failed",
     "reversed",
     "reconciliationRequired"
    ],
    "description": "Payment status"
   }
  }
 },
 "PaymentReconciliationExceptionManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Payment Reconciliation & Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "sourceSystem": {
    "type": "string",
    "enum": [
     "paymentGateway",
     "acquirer",
     "bank",
     "pos",
     "ota",
     "reseller",
     "wallet",
     "erp"
    ],
    "description": "Source system."
   },
   "exceptionType": {
    "type": "string",
    "description": "Exception, e.g. amount mismatch, unmatched settlement"
   },
   "expectedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected amount"
   },
   "actualAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Actual amount"
   }
  }
 },
 "PaymentsDepositActivity": {
  "type": "object",
  "x-ticvai-persistence": "payments.deposit_activity",
  "description": "**Taken from the backend workbook, 20 September.** NEW TABLE. Provides an auditable history of every deposit authorization, hold, capture, release, forfeiture, refund, or adjustment.",
  "required": [
   "depositId",
   "type",
   "amount",
   "occurredAt",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "depositId": {
    "type": "string",
    "format": "uuid"
   },
   "paymentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "type": {
    "type": "string",
    "maxLength": 30
   },
   "amount": {
    "type": "number"
   },
   "reason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "RelatedOrderTransactionRelationshipExplorerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Related Order & Transaction Relationship Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "relationshipType": {
    "type": "string",
    "enum": [
     "original",
     "amendment",
     "ticketUpgrade",
     "additionalPayment",
     "partialCancellation",
     "conversion",
     "exchange",
     "cancellation",
     "payment",
     "chargebackWhereIntegrated",
     "externalTransaction"
    ],
    "description": "Relationship to the original."
   },
   "orderId": {
    "type": "string",
    "description": "Order ID"
   },
   "relatedOrderId": {
    "type": "string",
    "description": "Related order or transaction ID"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   }
  }
 }
}
```
