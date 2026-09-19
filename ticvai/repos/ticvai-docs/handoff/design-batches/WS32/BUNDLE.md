# WS32 — Order   Reservation Management board 2

**10 screens · 10 operations · 15 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ORDER_CREATE, ORDER_VIEW, REGION_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-314` | Amendment & After-Sales Command Center | listDetail | 1 | 1 | — |
| `BO-315` | Order Amendment Workspace | listDetail | 1 | 0 | — |
| `BO-316` | Amendment Eligibility & Policy Rule Builder | configEditor | 1 | 0 | — |
| `BO-317` | Cancellation & Partial Cancellation Policy Configuration | listDetail | 1 | 0 | — |
| `BO-318` | Refund Policy & Refund Calculation Configuration | configEditor | 1 | 0 | — |
| `BO-319` | Void, Reversal & Same-Day Correction Management | configEditor | 1 | 0 | — |
| `BO-320` | Ticket Reissue & Fulfillment Regeneration | configEditor | 1 | 0 | — |
| `BO-321` | After-Sales Financial Settlement & Adjustment Workspace | listDetail | 1 | 0 | — |
| `BO-322` | Approval, Exception & Service Recovery Management | configEditor | 1 | 0 | — |
| `BO-323` | Amendment History, Audit & After-Sales Analytics | configEditor | 1 | 0 | — |

## Thin screens in this batch

**BO-321 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-314",
  "name": "Amendment & After-Sales Command Center",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.1",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/amendment-after-sales-command-center-bo-314",
   "component": "apps/venue-management-web/src/routes/orders-money/AmendmentAfterSalesCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-315",
    "BO-316",
    "BO-317",
    "BO-318",
    "BO-319",
    "BO-320",
    "BO-321",
    "BO-322",
    "BO-323"
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
     "to": "BO-318",
     "trigger": "Refund Policy & Refund Calculation Configuration",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-318 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-315",
     "trigger": "Works in Order Amendment Workspace",
     "provenance": "flow F141 step 1→2",
     "operation": "listAmendmentAfterSale"
    },
    {
     "to": "BO-316",
     "trigger": "Works in Amendment Eligibility & Policy Rule Builder",
     "provenance": "flow F141 step 3→4",
     "operation": "listAmendmentAfterSale"
    },
    {
     "to": "BO-317",
     "trigger": "Works in Cancellation & Partial Cancellation Policy Configuration",
     "provenance": "flow F141 step 5→6",
     "operation": "listAmendmentAfterSale"
    },
    {
     "to": "BO-319",
     "trigger": "Works in Void, Reversal & Same-Day Correction Management",
     "provenance": "flow F141 step 9→10",
     "operation": "listAmendmentAfterSale"
    },
    {
     "to": "BO-320",
     "trigger": "Works in Ticket Reissue & Fulfillment Regeneration",
     "provenance": "flow F141 step 11→12",
     "operation": "listAmendmentAfterSale"
    },
    {
     "to": "BO-321",
     "trigger": "Works in After-Sales Financial Settlement & Adjustment Workspace",
     "provenance": "flow F141 step 13→14",
     "operation": "listAmendmentAfterSale"
    },
    {
     "to": "BO-322",
     "trigger": "Works in Approval, Exception & Service Recovery Management",
     "provenance": "flow F141 step 15→16",
     "operation": "listAmendmentAfterSale"
    },
    {
     "to": "BO-323",
     "trigger": "Works in Amendment History, Audit & After-Sales Analytics",
     "provenance": "flow F141 step 17→18",
     "operation": "listAmendmentAfterSale"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide one operational workspace for all post-sale activities affecting confirmed orders and reservations.",
  "purposeNote": "Authorized users can monitor and manage all after-sales order activities from one centralized operational workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Order Amendment, Reservation Amendment, Date Change, Timeslot Change, Performance Change, Quantity Change, Attendee Change, Void. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
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
       "label": "Search amendment after-sales",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Event",
        "Product",
        "AmendmentAfterSalesCommandCenterView.requestType",
        "AmendmentAfterSalesCommandCenterView.channel",
        "AmendmentAfterSalesCommandCenterView.customer",
        "Agent",
        "Status",
        "Approval",
        "Date"
       ],
       "notes": "The pack filters this screen by venue, event, product, request type, channel, customer and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every amendment after-sales",
       "columns": [
        "AmendmentAfterSalesCommandCenterView.amendmentsToday",
        "AmendmentAfterSalesCommandCenterView.pendingAmendments",
        "AmendmentAfterSalesCommandCenterView.cancellations",
        "Refund Requests",
        "Refund Value",
        "AmendmentAfterSalesCommandCenterView.voids",
        "AmendmentAfterSalesCommandCenterView.reissues",
        "AmendmentAfterSalesCommandCenterView.dateTimeChanges",
        "AmendmentAfterSalesCommandCenterView.partialCancellations",
        "AmendmentAfterSalesCommandCenterView.pendingApprovals",
        "AmendmentAfterSalesCommandCenterView.failedActions",
        "AmendmentAfterSalesCommandCenterView.slaBreaches",
        "AmendmentAfterSalesCommandCenterView.requestId",
        "AmendmentAfterSalesCommandCenterView.orderNumber",
        "AmendmentAfterSalesCommandCenterView.customer",
        "AmendmentAfterSalesCommandCenterView.requestType",
        "AmendmentAfterSalesCommandCenterView.productEvent",
        "AmendmentAfterSalesCommandCenterView.originalValue",
        "AmendmentAfterSalesCommandCenterView.financialImpact",
        "AmendmentAfterSalesCommandCenterView.channel",
        "AmendmentAfterSalesCommandCenterView.requestedBy",
        "AmendmentAfterSalesCommandCenterView.approvalStatus",
        "AmendmentAfterSalesCommandCenterView.processingStatus",
        "AmendmentAfterSalesCommandCenterView.createdTime"
       ],
       "bindsTo": "AmendmentAfterSalesCommandCenterView",
       "operation": "listAmendmentAfterSale",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected amendment after-sales",
       "bindsTo": "AmendmentAfterSalesCommandCenterView",
       "columns": [
        "AmendmentAfterSalesCommandCenterView.amendmentsToday",
        "AmendmentAfterSalesCommandCenterView.pendingAmendments",
        "AmendmentAfterSalesCommandCenterView.cancellations",
        "Refund Requests",
        "Refund Value",
        "AmendmentAfterSalesCommandCenterView.voids",
        "AmendmentAfterSalesCommandCenterView.reissues",
        "AmendmentAfterSalesCommandCenterView.dateTimeChanges",
        "AmendmentAfterSalesCommandCenterView.partialCancellations",
        "AmendmentAfterSalesCommandCenterView.pendingApprovals",
        "AmendmentAfterSalesCommandCenterView.failedActions",
        "AmendmentAfterSalesCommandCenterView.slaBreaches",
        "AmendmentAfterSalesCommandCenterView.requestId",
        "AmendmentAfterSalesCommandCenterView.orderNumber",
        "AmendmentAfterSalesCommandCenterView.customer",
        "AmendmentAfterSalesCommandCenterView.requestType",
        "AmendmentAfterSalesCommandCenterView.productEvent",
        "AmendmentAfterSalesCommandCenterView.originalValue",
        "AmendmentAfterSalesCommandCenterView.financialImpact",
        "AmendmentAfterSalesCommandCenterView.channel",
        "AmendmentAfterSalesCommandCenterView.requestedBy",
        "AmendmentAfterSalesCommandCenterView.approvalStatus",
        "AmendmentAfterSalesCommandCenterView.processingStatus",
        "AmendmentAfterSalesCommandCenterView.createdTime"
       ],
       "notes": null,
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Order Amendment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Reservation Amendment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Date Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Timeslot Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Performance Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Quantity Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Attendee Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
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
    "body": "**Void on a amendment after-sales is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
   }
  ],
  "states": {
   "loading": "The amendment after-sales list.",
   "error": "Could not load. Names which read failed and leaves the amendment after-sales untouched.",
   "emptyFirstRun": "No amendment after-sales yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the amendment after-sales are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAmendmentAfterSale",
    "contract": "orders",
    "purpose": "Amendment & After-Sales Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AmendmentAfterSalesCommandCenterView.amendmentsToday",
    "AmendmentAfterSalesCommandCenterView.pendingAmendments",
    "AmendmentAfterSalesCommandCenterView.cancellations",
    "Refund Requests",
    "Refund Value",
    "AmendmentAfterSalesCommandCenterView.voids"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-314"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 20. 25 of 34 labels bound to a contract property; 42 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-315",
  "name": "Order Amendment Workspace",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.2",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/order-amendment-workspace-bo-315",
   "component": "apps/venue-management-web/src/routes/orders-money/OrderAmendmentWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F141 step 2→3",
     "operation": "setOrderAmendment"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide agents with a controlled workspace for modifying an existing order without directly editing historical transaction records. The original order must always remain reconstructable.",
  "purposeNote": "Authorized users can amend eligible order attributes through a controlled transaction while preserving the original order and validating all affected services.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Holder, Customer Details, Delivery Method, Save Draft, Validate, Calculate, Submit for Approval, Execute Amendment …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 22 §Allow authorized changes to"
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
       "label": "Every order amendment",
       "columns": [
        "OrderAmendmentWorkspaceView.orderId",
        "OrderAmendmentWorkspaceView.customer",
        "OrderAmendmentWorkspaceView.originalChannel",
        "OrderAmendmentWorkspaceView.venue",
        "OrderAmendmentWorkspaceView.orderDate",
        "OrderAmendmentWorkspaceView.paymentStatus",
        "OrderAmendmentWorkspaceView.fulfillmentStatus",
        "OrderAmendmentWorkspaceView.total",
        "OrderAmendmentWorkspaceView.tickets",
        "OrderAmendmentWorkspaceView.currentReservation"
       ],
       "bindsTo": "OrderAmendmentWorkspaceView",
       "operation": "setOrderAmendment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order amendment",
       "bindsTo": "OrderAmendmentWorkspaceView",
       "columns": [
        "OrderAmendmentWorkspaceView.orderId",
        "OrderAmendmentWorkspaceView.customer",
        "OrderAmendmentWorkspaceView.originalChannel",
        "OrderAmendmentWorkspaceView.venue",
        "OrderAmendmentWorkspaceView.orderDate",
        "OrderAmendmentWorkspaceView.paymentStatus",
        "OrderAmendmentWorkspaceView.fulfillmentStatus",
        "OrderAmendmentWorkspaceView.total",
        "OrderAmendmentWorkspaceView.tickets",
        "OrderAmendmentWorkspaceView.currentReservation"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Original Proposed”, “Before committing, validate”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ticket Holder",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Allow authorized changes to"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Details",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Allow authorized changes to"
      },
      {
       "kind": "secondaryButton",
       "label": "Delivery Method",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Allow authorized changes to"
      },
      {
       "kind": "secondaryButton",
       "label": "Save Draft",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Calculate",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Submit for Approval",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Execute Amendment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order amendment list.",
   "error": "Could not load. Names which read failed and leaves the order amendment untouched.",
   "emptyFirstRun": "No order amendment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order amendment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setOrderAmendment",
    "contract": "orders",
    "purpose": "Order Amendment Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setOrderAmendment"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "OrderAmendmentWorkspaceView.orderId",
    "OrderAmendmentWorkspaceView.customer",
    "OrderAmendmentWorkspaceView.originalChannel",
    "OrderAmendmentWorkspaceView.venue",
    "OrderAmendmentWorkspaceView.orderDate",
    "OrderAmendmentWorkspaceView.paymentStatus"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-315"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 22. 10 of 10 labels bound to a contract property; 19 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-316",
  "name": "Amendment Eligibility & Policy Rule Builder",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.3",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/amendment-eligibility-policy-rule-builder-bo-316",
   "component": "apps/venue-management-web/src/routes/orders-money/AmendmentEligibilityPolicyRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F141 step 4→5",
     "operation": "setAmendmentEligibilityPolicy"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define when an order or reservation may be amended and which changes are permitted.",
  "purposeNote": "centrally configured after-sales policies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Date Change, Timeslot Change, Performance Change, Quantity Increase, Seat Change, Attendee Change, Delivery Change. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 24 §Enable/disable"
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
       "label": "Tenant",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Ticket Type",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Performance",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer Segment",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Order Status",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Ticket Status",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure by"
      },
      {
       "kind": "textField",
       "label": "Maximum Amendments per Order",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum Amendments per Ticket",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Date Changes",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cooling Period",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Date Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Timeslot Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Performance Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Quantity Increase",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Seat Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Attendee Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Delivery Change",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 24 §Enable/disable"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The amendment eligibility policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the amendment eligibility policy untouched.",
   "emptyFirstRun": "No amendment eligibility policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAmendmentEligibilityPolicy",
    "contract": "orders",
    "purpose": "Amendment Eligibility & Policy Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setAmendmentEligibilityPolicy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-316"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 22 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-317",
  "name": "Cancellation & Partial Cancellation Policy Configuration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.4",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/cancellation-partial-cancellation-policy-configuration-bo-317",
   "component": "apps/venue-management-web/src/routes/orders-money/CancellationPartialCancellationPolicyConfigurati.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F141 step 6→7",
     "operation": "setCancellationPartialPolicy"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure whether an order, reservation, or selected order lines may be cancelled.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Entire Order, Individual Ticket, Selected Order Lines, Add-On Only. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 26 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 26"
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
       "label": "Entire Order",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Individual Ticket",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Order Lines",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Add-On Only",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 26 §Support"
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
   "loading": "The cancellation partial cancellation list.",
   "error": "Could not load. Names which read failed and leaves the cancellation partial cancellation untouched.",
   "emptyFirstRun": "No cancellation partial cancellation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cancellation partial cancellation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCancellationPartialPolicy",
    "contract": "orders",
    "purpose": "Cancellation & Partial Cancellation Policy Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setCancellationPartialPolicy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-317"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 4 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-318",
  "name": "Refund Policy & Refund Calculation Configuration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.5",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/refund-policy-refund-calculation-configuration-bo-318",
   "component": "apps/venue-management-web/src/routes/orders-money/RefundPolicyRefundCalculationConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F141 step 8→9",
     "operation": "setRefundPolicy"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure separately) and no display directory — it is settings, not a population",
  "purpose": "Define when a cancellation/amendment creates a refundable amount and how refund entitlement is determined.",
  "purposeNote": "duplicating payment execution or central pricing logic.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Base Price",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
      },
      {
       "kind": "selectField",
       "label": "Tax",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
      },
      {
       "kind": "selectField",
       "label": "Booking Fee",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
      },
      {
       "kind": "selectField",
       "label": "Service Fee",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
      },
      {
       "kind": "selectField",
       "label": "Delivery Fee",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
      },
      {
       "kind": "selectField",
       "label": "Add-On",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
      },
      {
       "kind": "selectField",
       "label": "Discount",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
      },
      {
       "kind": "selectField",
       "label": "Promotion",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
      },
      {
       "kind": "selectField",
       "label": "Convenience Fee",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Configure separately"
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
       "provenance": "contract operation setRefundPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund policy refund configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the refund policy refund untouched.",
   "emptyFirstRun": "No refund policy refund configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRefundPolicy",
    "contract": "orders",
    "purpose": "Set a venue's refund policy",
    "trigger": "onAction",
    "invalidates": [
     "setRefundPolicy"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-318"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 9 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-319",
  "name": "Void, Reversal & Same-Day Correction Management",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.6",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/void-reversal-same-day-correction-management-bo-319",
   "component": "apps/venue-management-web/src/routes/orders-money/VoidReversalSameDayCorrectionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F141 step 10→11",
     "operation": "listVoidReversalSame"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Separate genuine void/correction operations from normal customer cancellations and refunds. This is important financially and operationally.",
  "purposeNote": "normal cancellation/refund transactions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Order Void, Payment Void Request, Ticket Void, Accidental Sale Reversal, Duplicate Transaction Correction, Failed Transaction Cleanup. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 29 §Support"
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
       "kind": "textField",
       "label": "Same Business Day Only",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Before Settlement",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Before Ticket Use",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Before Fiscal Closure",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supervisor Required",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Specific Channels Only",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Order Void",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Void Request",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket Void",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Accidental Sale Reversal",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate Transaction Correction",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Failed Transaction Cleanup",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 29 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The void reversal same-day configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the void reversal same-day untouched.",
   "emptyFirstRun": "No void reversal same-day configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVoidReversalSame",
    "contract": "orders",
    "purpose": "Void, Reversal & Same-Day Correction Management",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-319"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 12 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-320",
  "name": "Ticket Reissue & Fulfillment Regeneration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.7",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/ticket-reissue-fulfillment-regeneration-bo-320",
   "component": "apps/venue-management-web/src/routes/orders-money/TicketReissueFulfillmentRegeneration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F141 step 12→13",
     "operation": "listTicketReissueFulfillment"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Options) and no display directory — it is settings, not a population",
  "purpose": "Manage ticket/media regeneration following an amendment, correction, loss, delivery failure, or other authorized event.",
  "purposeNote": "Authorized reissues regenerate the appropriate ticket/credential while preventing duplicate valid credentials and preserving full history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Lost Ticket, Printing Error, SMS/WhatsApp link, Wallet Update. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 30 §Support"
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
       "label": "Maximum Reissues",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reissue Fee",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Free Reissue Count",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supervisor Threshold",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Immediately Invalidate",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Options"
      },
      {
       "kind": "selectField",
       "label": "Supersede",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Options"
      },
      {
       "kind": "textField",
       "label": "Retain Until New Credential Activated",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Options"
      },
      {
       "kind": "textField",
       "label": "Preserve where credential remains unchanged",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Options"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Lost Ticket",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Printing Error",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "SMS/WhatsApp link",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Update",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 30 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket reissue fulfillment configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the ticket reissue fulfillment untouched.",
   "emptyFirstRun": "No ticket reissue fulfillment configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTicketReissueFulfillment",
    "contract": "orders",
    "purpose": "Ticket Reissue & Fulfillment Regeneration",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-320"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 12 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-321",
  "name": "After-Sales Financial Settlement & Adjustment Workspace",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.8",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/after-sales-financial-settlement-adjustment-workspace-bo-321",
   "component": "apps/venue-management-web/src/routes/orders-money/AfterSalesFinancialSettlementAdjustmentWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F141 step 14→15",
     "operation": "setAfterSaleFinancial"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Track) and no metric row",
  "purpose": "Provide a consolidated view of the financial consequences of amendments, cancellations, refunds, exchanges and corrections. This is not the payment engine; it is the after-sales financial orchestration layer.",
  "purposeNote": "Every after-sales operation has a reconciled financial outcome linked to the corresponding order change.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every after-sales financial settlement",
       "columns": [
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.originalOrderValue",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.currentOrderValue",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.additionalCharge",
        "Refund Due",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.fees",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.taxAdjustment",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.credits",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.alreadyRefunded",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.outstandingBalance",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.netTransactionImpact",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.collectionRequired",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.paymentPending",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.paymentComplete",
        "Refund Pending",
        "Refund Complete",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.failed",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.reconciliationRequired"
       ],
       "bindsTo": "AfterSalesFinancialSettlementAdjustmentWorkspaceView",
       "operation": "setAfterSaleFinancial",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 32 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected after-sales financial settlement",
       "bindsTo": "AfterSalesFinancialSettlementAdjustmentWorkspaceView",
       "columns": [
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.originalOrderValue",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.currentOrderValue",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.additionalCharge",
        "Refund Due",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.fees",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.taxAdjustment",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.credits",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.alreadyRefunded",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.outstandingBalance",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.netTransactionImpact",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.collectionRequired",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.paymentPending",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.paymentComplete",
        "Refund Pending",
        "Refund Complete",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.failed",
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.reconciliationRequired"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Customer Receives Refund”, “No Financial Difference”, “Commit Control”, “Before payment”, “Only after successful payment”, “Trigger relevant”.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 32 §Display"
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
       "provenance": "contract operation setAfterSaleFinancial"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The after-sales financial settlement list.",
   "error": "Could not load. Names which read failed and leaves the after-sales financial settlement untouched.",
   "emptyFirstRun": "No after-sales financial settlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the after-sales financial settlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAfterSaleFinancial",
    "contract": "orders",
    "purpose": "After-Sales Financial Settlement & Adjustment Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setAfterSaleFinancial"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "AfterSalesFinancialSettlementAdjustmentWorkspaceView.originalOrderValue",
    "AfterSalesFinancialSettlementAdjustmentWorkspaceView.currentOrderValue",
    "AfterSalesFinancialSettlementAdjustmentWorkspaceView.additionalCharge",
    "Refund Due",
    "AfterSalesFinancialSettlementAdjustmentWorkspaceView.fees",
    "AfterSalesFinancialSettlementAdjustmentWorkspaceView.taxAdjustment"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-321"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 32. 14 of 17 labels bound to a contract property; 17 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-322",
  "name": "Approval, Exception & Service Recovery Management",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.9",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/approval-exception-service-recovery-management-bo-322",
   "component": "apps/venue-management-web/src/routes/orders-money/ApprovalExceptionServiceRecoveryManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F141 step 16→17",
     "operation": "approveExceptionServiceRecovery"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Govern after-sales actions that fall outside normal policies or exceed financial/operational authority.",
  "purposeNote": "Out-of-policy and high-risk after-sales actions are routed through configurable approval and service-recovery workflows with appropriate segregation of duties.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Fee Waiver. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Order___Reservation_Management_Reference.pdf, page 33 §Allow governed remedies"
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
       "label": "Requested Action",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Order",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Standard Policy Result",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requested Exception",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Financial Impact",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Supporting Documents",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requestor",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Fee Waiver",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Allow governed remedies"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval exception service configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval exception service untouched.",
   "emptyFirstRun": "No approval exception service configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveExceptionServiceRecovery",
    "contract": "orders",
    "purpose": "Approval, Exception & Service Recovery Management",
    "trigger": "onAction",
    "invalidates": [
     "approveExceptionServiceRecovery"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-322"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 33. 0 of 0 labels bound to a contract property; 10 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-323",
  "name": "Amendment History, Audit & After-Sales Analytics",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Order___Reservation_Management_Reference.pdf",
   "board": "2",
   "number": "12.2.10",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/amendment-history-audit-after-sales-analytics-bo-323",
   "component": "apps/venue-management-web/src/routes/orders-money/AmendmentHistoryAuditAfterSalesAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-314"
   ],
   "exitTo": [
    "BO-314"
   ],
   "inferred": false,
   "notes": "**Reached from BO-314, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide complete traceability and analytical visibility across all changes made after original order creation.",
  "purposeNote": "through the final commercial, financial and credential state. Board 2 — Final Screen Register # Backend Screen Core Responsibility 12.2. Central after-sales",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search amendment history audit",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Product",
        "Event",
        "AmendmentHistoryAuditAfterSalesAnalyticsView.channel",
        "Agent",
        "Customer Segment",
        "Reason",
        "Period"
       ],
       "notes": "The pack filters this screen by venue, product, event, channel, agent, customer segment and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Request ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Order ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Ticket ID",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Action",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Before Value",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "After Value",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Financial Impact",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Rule Applied",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Exception",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Timestamp",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Result",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 35 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The amendment history audit configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the amendment history audit untouched.",
   "emptyFirstRun": "No amendment history audit configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoResults": "The filter narrowed it and the amendment history audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAmendmentAfterSale2",
    "contract": "orders",
    "purpose": "Amendment History, Audit & After-Sales Analytics",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-323"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 35. 1 of 8 labels bound to a contract property; 23 of 109 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveExceptionServiceRecovery": {
  "method": "PUT",
  "path": "/exception-service-recovery",
  "contract": "orders",
  "summary": "Approval, Exception & Service Recovery Management",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ApprovalExceptionServiceRecoveryManagementInput",
  "responds": "ApprovalExceptionServiceRecoveryManagementView"
 },
 "listAmendmentAfterSale": {
  "method": "GET",
  "path": "/amendment-after-sale",
  "contract": "orders",
  "summary": "Amendment & After-Sales Command Center",
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
    "name": "agent",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "approval",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "AmendmentAfterSalesCommandCenterView"
 },
 "listAmendmentAfterSale2": {
  "method": "GET",
  "path": "/amendment-after-sale-2",
  "contract": "orders",
  "summary": "Amendment History, Audit & After-Sales Analytics",
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
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "agent",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "reason",
    "in": "query",
    "required": false
   },
   {
    "name": "period",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "AmendmentHistoryAuditAfterSalesAnalyticsView"
 },
 "listTicketReissueFulfillment": {
  "method": "GET",
  "path": "/ticket-reissue-fulfillment",
  "contract": "orders",
  "summary": "Ticket Reissue & Fulfillment Regeneration",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TicketReissueFulfillmentRegenerationView"
 },
 "listVoidReversalSame": {
  "method": "GET",
  "path": "/void-reversal-same",
  "contract": "orders",
  "summary": "Void, Reversal & Same-Day Correction Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VoidReversalSameDayCorrectionManagementView"
 },
 "setAfterSaleFinancial": {
  "method": "PUT",
  "path": "/after-sale-financial",
  "contract": "orders",
  "summary": "After-Sales Financial Settlement & Adjustment Workspace",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AfterSalesFinancialSettlementAdjustmentWorkspaceInput",
  "responds": "AfterSalesFinancialSettlementAdjustmentWorkspaceView"
 },
 "setAmendmentEligibilityPolicy": {
  "method": "PUT",
  "path": "/amendment-eligibility-policy",
  "contract": "orders",
  "summary": "Amendment Eligibility & Policy Rule Builder",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AmendmentEligibilityPolicyRuleBuilderInput",
  "responds": "AmendmentEligibilityPolicyRuleBuilderView"
 },
 "setCancellationPartialPolicy": {
  "method": "PUT",
  "path": "/cancellation-partial-policy",
  "contract": "orders",
  "summary": "Cancellation & Partial Cancellation Policy Configuration",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "CancellationPartialCancellationPolicyConfigurationInput",
  "responds": "CancellationPartialCancellationPolicyConfigurationView"
 },
 "setOrderAmendment": {
  "method": "PUT",
  "path": "/order-amendment",
  "contract": "orders",
  "summary": "Order Amendment Workspace",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "OrderAmendmentWorkspaceInput",
  "responds": "OrderAmendmentWorkspaceView"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AfterSalesFinancialSettlementAdjustmentWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What After-Sales Financial Settlement & Adjustment Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "updatedReceipt": {
    "type": "string",
    "format": "date-time",
    "description": "Updated Receipt"
   },
   "invoiceAdjustment": {
    "type": "string",
    "description": "Invoice Adjustment"
   },
   "creditNote": {
    "type": "string",
    "description": "Credit Note"
   },
   "throughTheFinanceDocumentServices": {
    "type": "string",
    "description": "through the finance/document services"
   }
  }
 },
 "AfterSalesFinancialSettlementAdjustmentWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What After-Sales Financial Settlement & Adjustment Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "originalOrderValue": {
    "type": "string",
    "description": "Original Order Value"
   },
   "currentOrderValue": {
    "type": "string",
    "description": "Current Order Value"
   },
   "additionalCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Additional Charge"
   },
   "fees": {
    "type": "integer",
    "description": "Fees"
   },
   "taxAdjustment": {
    "type": "string",
    "description": "Tax Adjustment"
   },
   "credits": {
    "type": "integer",
    "description": "Credits"
   },
   "alreadyRefunded": {
    "type": "string",
    "description": "Already Refunded"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "netTransactionImpact": {
    "type": "string",
    "description": "Net Transaction Impact"
   },
   "noFinancialDifference": {
    "type": "string",
    "description": "No Financial Difference (the pack shows AED 0.)"
   },
   "collectionRequired": {
    "type": "boolean",
    "description": "Collection Required"
   },
   "paymentPending": {
    "type": "integer",
    "description": "Payment Pending"
   },
   "paymentComplete": {
    "type": "string",
    "description": "Payment Complete"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "reconciliationRequired": {
    "type": "boolean",
    "description": "Reconciliation Required"
   },
   "updatedReceipt": {
    "type": "string",
    "format": "date-time",
    "description": "Updated Receipt"
   },
   "invoiceAdjustment": {
    "type": "string",
    "description": "Invoice Adjustment"
   },
   "creditNote": {
    "type": "string",
    "description": "Credit Note"
   },
   "throughTheFinanceDocumentServices": {
    "type": "string",
    "description": "through the finance/document services"
   }
  }
 },
 "AmendmentAfterSalesCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Amendment & After-Sales Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "amendmentsToday": {
    "type": "string",
    "description": "Amendments Today"
   },
   "pendingAmendments": {
    "type": "integer",
    "description": "Pending Amendments"
   },
   "cancellations": {
    "type": "integer",
    "description": "Cancellations"
   },
   "voids": {
    "type": "integer",
    "description": "Voids"
   },
   "reissues": {
    "type": "integer",
    "description": "Reissues"
   },
   "dateTimeChanges": {
    "type": "integer",
    "description": "Date/Time Changes"
   },
   "partialCancellations": {
    "type": "integer",
    "description": "Partial Cancellations"
   },
   "pendingApprovals": {
    "type": "integer",
    "description": "Pending Approvals"
   },
   "failedActions": {
    "type": "integer",
    "description": "Failed Actions"
   },
   "slaBreaches": {
    "type": "integer",
    "description": "SLA Breaches"
   },
   "requestId": {
    "type": "string",
    "description": "Request ID"
   },
   "orderNumber": {
    "type": "string",
    "description": "Order Number"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "requestType": {
    "type": "string",
    "description": "Request Type"
   },
   "productEvent": {
    "type": "string",
    "description": "Product/Event"
   },
   "originalValue": {
    "type": "string",
    "description": "Original Value"
   },
   "financialImpact": {
    "type": "string",
    "description": "Financial Impact"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested By"
   },
   "approvalStatus": {
    "type": "integer",
    "description": "Approval Status"
   },
   "processingStatus": {
    "type": "integer",
    "description": "Processing Status"
   },
   "createdTime": {
    "type": "string",
    "format": "date-time",
    "description": "Created Time"
   },
   "orderAmendment": {
    "type": "string",
    "description": "Order Amendment"
   },
   "reservationAmendment": {
    "type": "string",
    "description": "Reservation Amendment"
   },
   "dateChange": {
    "type": "string",
    "format": "date-time",
    "description": "Date Change"
   },
   "timeslotChange": {
    "type": "string",
    "description": "Timeslot Change"
   },
   "performanceChange": {
    "type": "string",
    "description": "Performance Change"
   },
   "quantityChange": {
    "type": "integer",
    "description": "Quantity Change"
   },
   "attendeeChange": {
    "type": "string",
    "description": "Attendee Change"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "partialCancellation": {
    "type": "string",
    "description": "Partial Cancellation"
   }
  }
 },
 "AmendmentEligibilityPolicyRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Amendment Eligibility & Policy Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
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
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "orderStatus": {
    "type": "string",
    "description": "Order Status"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket Status"
   },
   "dateChange": {
    "type": "string",
    "format": "date-time",
    "description": "Date Change"
   },
   "timeslotChange": {
    "type": "string",
    "description": "Timeslot Change"
   },
   "performanceChange": {
    "type": "string",
    "description": "Performance Change"
   },
   "quantityIncrease": {
    "type": "integer",
    "description": "Quantity Increase"
   },
   "quantityReduction": {
    "type": "integer",
    "description": "Quantity Reduction"
   },
   "seatChange": {
    "type": "string",
    "description": "Seat Change"
   },
   "attendeeChange": {
    "type": "string",
    "description": "Attendee Change"
   },
   "deliveryChange": {
    "type": "string",
    "description": "Delivery Change"
   },
   "otherPermittedModifications": {
    "type": "string",
    "description": "Other permitted modifications"
   },
   "unused": {
    "type": "string",
    "description": "Unused"
   },
   "partiallyUsed": {
    "type": "string",
    "description": "Partially Used"
   },
   "fullyUsed": {
    "type": "string",
    "description": "Fully Used"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "cancelled": {
    "type": "integer",
    "description": "Cancelled"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "maximumAmendmentsPerOrder": {
    "type": "string",
    "description": "Maximum Amendments per Order"
   },
   "maximumAmendmentsPerTicket": {
    "type": "string",
    "description": "Maximum Amendments per Ticket"
   },
   "maximumDateChanges": {
    "type": "string",
    "format": "date-time",
    "description": "Maximum Date Changes"
   },
   "coolingPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Cooling Period"
   },
   "dateTimeChangeOnly": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time change only"
   },
   "dateTimeAttendeeChanges": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time + attendee changes"
   },
   "broaderExceptionPermissions": {
    "type": "string",
    "description": "Broader exception permissions"
   }
  }
 },
 "AmendmentEligibilityPolicyRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Amendment Eligibility & Policy Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
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
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "orderStatus": {
    "type": "string",
    "description": "Order Status"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket Status"
   },
   "dateChange": {
    "type": "string",
    "format": "date-time",
    "description": "Date Change"
   },
   "timeslotChange": {
    "type": "string",
    "description": "Timeslot Change"
   },
   "performanceChange": {
    "type": "string",
    "description": "Performance Change"
   },
   "quantityIncrease": {
    "type": "integer",
    "description": "Quantity Increase"
   },
   "quantityReduction": {
    "type": "integer",
    "description": "Quantity Reduction"
   },
   "seatChange": {
    "type": "string",
    "description": "Seat Change"
   },
   "attendeeChange": {
    "type": "string",
    "description": "Attendee Change"
   },
   "deliveryChange": {
    "type": "string",
    "description": "Delivery Change"
   },
   "otherPermittedModifications": {
    "type": "string",
    "description": "Other permitted modifications"
   },
   "unused": {
    "type": "string",
    "description": "Unused"
   },
   "partiallyUsed": {
    "type": "string",
    "description": "Partially Used"
   },
   "fullyUsed": {
    "type": "string",
    "description": "Fully Used"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "cancelled": {
    "type": "integer",
    "description": "Cancelled"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "maximumAmendmentsPerOrder": {
    "type": "string",
    "description": "Maximum Amendments per Order"
   },
   "maximumAmendmentsPerTicket": {
    "type": "string",
    "description": "Maximum Amendments per Ticket"
   },
   "maximumDateChanges": {
    "type": "string",
    "format": "date-time",
    "description": "Maximum Date Changes"
   },
   "coolingPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Cooling Period"
   },
   "dateTimeChangeOnly": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time change only"
   },
   "dateTimeAttendeeChanges": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time + attendee changes"
   },
   "broaderExceptionPermissions": {
    "type": "string",
    "description": "Broader exception permissions"
   }
  }
 },
 "AmendmentHistoryAuditAfterSalesAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Amendment History, Audit & After-Sales Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "requestId": {
    "type": "string",
    "description": "Request ID"
   },
   "orderId": {
    "type": "string",
    "description": "Order ID"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket ID"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "beforeValue": {
    "type": "string",
    "description": "Before Value"
   },
   "afterValue": {
    "type": "string",
    "description": "After Value"
   },
   "financialImpact": {
    "type": "string",
    "description": "Financial Impact"
   },
   "ruleApplied": {
    "type": "string",
    "description": "Rule Applied"
   },
   "exception": {
    "type": "string",
    "description": "Exception"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
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
   "result": {
    "type": "string",
    "description": "Result"
   },
   "preserveSnapshotsForSignificantAmendments": {
    "type": "string",
    "description": "Preserve snapshots for significant amendments"
   },
   "visit02Sep1800": {
    "type": "string",
    "description": "Visit: 02 Sep 18:00"
   },
   "seatB12": {
    "type": "string",
    "description": "Seat: B-12"
   },
   "valueAed250": {
    "type": "string",
    "description": "Value: AED 250"
   },
   "visit03Sep1900": {
    "type": "string",
    "description": "Visit: 03 Sep 19:00"
   },
   "seatC08": {
    "type": "string",
    "description": "Seat: C-08"
   },
   "valueAed280": {
    "type": "string",
    "description": "Value: AED 280"
   },
   "amendmentRate": {
    "type": "number",
    "description": "Amendment Rate"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate"
   },
   "averageRefund": {
    "type": "number",
    "description": "Average Refund"
   },
   "exceptionRate": {
    "type": "number",
    "description": "Exception Rate"
   },
   "approvalRate": {
    "type": "number",
    "description": "Approval Rate"
   },
   "serviceRecoveryCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Service-Recovery Cost"
   },
   "excessiveVoids": {
    "type": "string",
    "description": "Excessive Voids"
   },
   "repeatedManualRefunds": {
    "type": "string",
    "description": "Repeated Manual Refunds"
   },
   "frequentFeeWaivers": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Frequent Fee Waivers"
   },
   "highReissueFrequency": {
    "type": "string",
    "description": "High Reissue Frequency"
   },
   "repeatedOutOfPolicyExceptions": {
    "type": "string",
    "description": "Repeated Out-of-Policy Exceptions"
   },
   "usersOfMisconduct": {
    "type": "string",
    "description": "users of misconduct"
   },
   "neverOverwriteTheOriginalOrder": {
    "type": "string",
    "description": "Never overwrite the original order"
   },
   "to": {
    "type": "string",
    "description": "to"
   },
   "board3CompletesArea12": {
    "type": "string",
    "description": "Board 3 completes Area 12"
   },
   "traceability": {
    "type": "string",
    "description": "traceability"
   }
  }
 },
 "ApprovalExceptionServiceRecoveryManagementInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is orders.cash_movement at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Approval, Exception & Service Recovery Management submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "requestedAction": {
    "type": "string",
    "description": "Requested Action"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "standardPolicyResult": {
    "type": "string",
    "description": "Standard Policy Result"
   },
   "requestedException": {
    "type": "string",
    "description": "Requested Exception"
   },
   "financialImpact": {
    "type": "string",
    "description": "Financial Impact"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "supportingDocuments": {
    "type": "string",
    "description": "Supporting Documents"
   },
   "requestor": {
    "type": "string",
    "description": "Requestor"
   },
   "complimentaryReissue": {
    "type": "string",
    "description": "Complimentary Reissue"
   },
   "feeWaiver": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Waiver"
   },
   "partialRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partial Refund"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "walletCredit": {
    "type": "string",
    "description": "Wallet Credit"
   },
   "alternativeDate": {
    "type": "string",
    "format": "date-time",
    "description": "Alternative Date"
   },
   "alternativeEvent": {
    "type": "string",
    "description": "Alternative Event"
   },
   "complimentaryAddOn": {
    "type": "string",
    "description": "Complimentary Add-On"
   }
  }
 },
 "ApprovalExceptionServiceRecoveryManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Approval, Exception & Service Recovery Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "requestedAction": {
    "type": "string",
    "description": "Requested Action"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "standardPolicyResult": {
    "type": "string",
    "description": "Standard Policy Result"
   },
   "requestedException": {
    "type": "string",
    "description": "Requested Exception"
   },
   "financialImpact": {
    "type": "string",
    "description": "Financial Impact"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "supportingDocuments": {
    "type": "string",
    "description": "Supporting Documents"
   },
   "requestor": {
    "type": "string",
    "description": "Requestor"
   },
   "complimentaryReissue": {
    "type": "string",
    "description": "Complimentary Reissue"
   },
   "feeWaiver": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Waiver"
   },
   "partialRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partial Refund"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "walletCredit": {
    "type": "string",
    "description": "Wallet Credit"
   },
   "alternativeDate": {
    "type": "string",
    "format": "date-time",
    "description": "Alternative Date"
   },
   "alternativeEvent": {
    "type": "string",
    "description": "Alternative Event"
   },
   "complimentaryAddOn": {
    "type": "string",
    "description": "Complimentary Add-On"
   }
  }
 },
 "CancellationPartialCancellationPolicyConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Cancellation & Partial Cancellation Policy Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "entireOrder": {
    "type": "string",
    "description": "Entire Order"
   },
   "entireReservation": {
    "type": "string",
    "description": "Entire Reservation"
   },
   "individualTicket": {
    "type": "string",
    "description": "Individual Ticket"
   },
   "selectedOrderLines": {
    "type": "string",
    "description": "Selected Order Lines"
   },
   "selectedQuantity": {
    "type": "integer",
    "description": "Selected Quantity"
   },
   "addOnOnly": {
    "type": "string",
    "description": "Add-On Only"
   },
   "groupMember": {
    "type": "string",
    "description": "Group Member"
   },
   "packageComponentWherePermitted": {
    "type": "string",
    "description": "Package Component where permitted"
   },
   "orderStatus": {
    "type": "string",
    "description": "Order Status"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment Status"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket Status"
   },
   "usage": {
    "type": "string",
    "description": "Usage"
   },
   "eventDate": {
    "type": "string",
    "format": "date-time",
    "description": "Event Date"
   },
   "cancellationWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Cancellation Window"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "notPermittedExceptSupervisorException": {
    "type": "string",
    "description": "Not permitted except supervisor exception"
   }
  }
 },
 "CancellationPartialCancellationPolicyConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Cancellation & Partial Cancellation Policy Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "entireOrder": {
    "type": "string",
    "description": "Entire Order"
   },
   "entireReservation": {
    "type": "string",
    "description": "Entire Reservation"
   },
   "individualTicket": {
    "type": "string",
    "description": "Individual Ticket"
   },
   "selectedOrderLines": {
    "type": "string",
    "description": "Selected Order Lines"
   },
   "selectedQuantity": {
    "type": "integer",
    "description": "Selected Quantity"
   },
   "addOnOnly": {
    "type": "string",
    "description": "Add-On Only"
   },
   "groupMember": {
    "type": "string",
    "description": "Group Member"
   },
   "packageComponentWherePermitted": {
    "type": "string",
    "description": "Package Component where permitted"
   },
   "orderStatus": {
    "type": "string",
    "description": "Order Status"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment Status"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket Status"
   },
   "usage": {
    "type": "string",
    "description": "Usage"
   },
   "eventDate": {
    "type": "string",
    "format": "date-time",
    "description": "Event Date"
   },
   "cancellationWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Cancellation Window"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "notPermittedExceptSupervisorException": {
    "type": "string",
    "description": "Not permitted except supervisor exception"
   }
  }
 },
 "OrderAmendmentWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_capacity at 5%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Order Amendment Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "customerDetails": {
    "type": "string",
    "description": "Customer Details"
   },
   "deliveryMethod": {
    "type": "string",
    "description": "Delivery Method"
   },
   "fulfillmentMethod": {
    "type": "string",
    "description": "Fulfillment Method"
   },
   "eligibleProductAttributes": {
    "type": "string",
    "description": "Eligible Product Attributes"
   },
   "seatWhereApplicable": {
    "type": "string",
    "description": "Seat where applicable"
   },
   "productRules": {
    "type": "string",
    "description": "Product Rules"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "seatAvailability": {
    "type": "string",
    "description": "Seat Availability"
   },
   "customerEligibility": {
    "type": "string",
    "description": "Customer Eligibility"
   },
   "amendmentPolicy": {
    "type": "string",
    "description": "Amendment Policy"
   },
   "pricing": {
    "type": "string",
    "description": "Pricing"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "waiver": {
    "type": "string",
    "description": "Waiver"
   },
   "credentialImpact": {
    "type": "string",
    "description": "Credential Impact"
   },
   "calculate": {
    "type": "string",
    "description": "Calculate"
   },
   "executeAmendment": {
    "type": "string",
    "description": "Execute Amendment"
   }
  }
 },
 "OrderAmendmentWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Order Amendment Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "orderId": {
    "type": "string",
    "description": "Order ID"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "originalChannel": {
    "type": "string",
    "description": "Original Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "orderDate": {
    "type": "string",
    "format": "date-time",
    "description": "Order Date"
   },
   "paymentStatus": {
    "type": "integer",
    "description": "Payment Status"
   },
   "fulfillmentStatus": {
    "type": "integer",
    "description": "Fulfillment Status"
   },
   "total": {
    "type": "integer",
    "description": "Total"
   },
   "tickets": {
    "type": "integer",
    "description": "Tickets"
   },
   "currentReservation": {
    "type": "string",
    "description": "Current Reservation"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "customerDetails": {
    "type": "string",
    "description": "Customer Details"
   },
   "deliveryMethod": {
    "type": "string",
    "description": "Delivery Method"
   },
   "fulfillmentMethod": {
    "type": "string",
    "description": "Fulfillment Method"
   },
   "eligibleProductAttributes": {
    "type": "string",
    "description": "Eligible Product Attributes"
   },
   "seatWhereApplicable": {
    "type": "string",
    "description": "Seat where applicable"
   },
   "productRules": {
    "type": "string",
    "description": "Product Rules"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "seatAvailability": {
    "type": "string",
    "description": "Seat Availability"
   },
   "customerEligibility": {
    "type": "string",
    "description": "Customer Eligibility"
   },
   "amendmentPolicy": {
    "type": "string",
    "description": "Amendment Policy"
   },
   "pricing": {
    "type": "string",
    "description": "Pricing"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "waiver": {
    "type": "string",
    "description": "Waiver"
   },
   "credentialImpact": {
    "type": "string",
    "description": "Credential Impact"
   },
   "calculate": {
    "type": "string",
    "description": "Calculate"
   },
   "executeAmendment": {
    "type": "string",
    "description": "Execute Amendment"
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
 "TicketReissueFulfillmentRegenerationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Ticket Reissue & Fulfillment Regeneration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dateChanged": {
    "type": "string",
    "format": "date-time",
    "description": "Date Changed"
   },
   "timeslotChanged": {
    "type": "string",
    "description": "Timeslot Changed"
   },
   "seatChanged": {
    "type": "string",
    "description": "Seat Changed"
   },
   "attendeeChanged": {
    "type": "string",
    "description": "Attendee Changed"
   },
   "lostTicket": {
    "type": "string",
    "description": "Lost Ticket"
   },
   "damagedCredential": {
    "type": "string",
    "description": "Damaged Credential"
   },
   "emailNotReceived": {
    "type": "string",
    "description": "Email Not Received"
   },
   "walletPassIssue": {
    "type": "string",
    "description": "Wallet Pass Issue"
   },
   "printingError": {
    "type": "string",
    "description": "Printing Error"
   },
   "credentialCompromised": {
    "type": "string",
    "description": "Credential Compromised"
   },
   "administrativeCorrection": {
    "type": "string",
    "description": "Administrative Correction"
   },
   "maximumReissues": {
    "type": "string",
    "description": "Maximum Reissues"
   },
   "freeReissueCount": {
    "type": "integer",
    "description": "Free Reissue Count"
   },
   "supervisorThreshold": {
    "type": "integer",
    "description": "Supervisor Threshold"
   },
   "optionsType": {
    "type": "string",
    "enum": [
     "immediatelyInvalidate",
     "supersede",
     "retainUntilNewCredentialActivated",
     "preserveWhereCredentialRemainsUnchanged"
    ],
    "description": "Vocabulary listed under Options."
   },
   "qr": {
    "type": "string",
    "description": "QR"
   },
   "dynamicQr": {
    "type": "string",
    "description": "Dynamic QR"
   },
   "barcode": {
    "type": "string",
    "description": "Barcode"
   },
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "walletPass": {
    "type": "string",
    "description": "Wallet Pass"
   },
   "printedTicket": {
    "type": "string",
    "description": "Printed Ticket"
   },
   "wearable": {
    "type": "string",
    "description": "Wearable"
   },
   "active": {
    "type": "integer",
    "description": "active"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "smsWhatsappLink": {
    "type": "string",
    "description": "SMS/WhatsApp link"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "walletUpdate": {
    "type": "string",
    "description": "Wallet Update"
   },
   "posPrint": {
    "type": "string",
    "description": "POS Print"
   },
   "boxOfficeCollection": {
    "type": "string",
    "description": "Box Office Collection"
   }
  }
 },
 "VoidReversalSameDayCorrectionManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Void, Reversal & Same-Day Correction Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "orderVoid": {
    "type": "string",
    "description": "Order Void"
   },
   "paymentVoidRequest": {
    "type": "string",
    "description": "Payment Void Request"
   },
   "ticketVoid": {
    "type": "string",
    "description": "Ticket Void"
   },
   "accidentalSaleReversal": {
    "type": "string",
    "description": "Accidental Sale Reversal"
   },
   "sameDayCorrection": {
    "type": "string",
    "description": "Same-Day Correction"
   },
   "failedTransactionCleanup": {
    "type": "integer",
    "description": "Failed Transaction Cleanup"
   },
   "finalAccountingTreatment": {
    "type": "string",
    "description": "final accounting treatment"
   },
   "sameBusinessDayOnly": {
    "type": "string",
    "description": "Same Business Day Only"
   },
   "beforeSettlement": {
    "type": "string",
    "description": "Before Settlement"
   },
   "beforeTicketUse": {
    "type": "string",
    "description": "Before Ticket Use"
   },
   "beforeFiscalClosure": {
    "type": "string",
    "description": "Before Fiscal Closure"
   },
   "supervisorRequired": {
    "type": "boolean",
    "description": "Supervisor Required"
   },
   "specificChannelsOnly": {
    "type": "string",
    "description": "Specific Channels Only"
   },
   "insteadOf": {
    "type": "string",
    "description": "instead of"
   },
   "operatorError": {
    "type": "string",
    "description": "Operator Error"
   },
   "wrongProduct": {
    "type": "string",
    "description": "Wrong Product"
   },
   "wrongQuantity": {
    "type": "integer",
    "description": "Wrong Quantity"
   },
   "wrongPayment": {
    "type": "string",
    "description": "Wrong Payment"
   },
   "technicalFailure": {
    "type": "string",
    "description": "Technical Failure"
   },
   "paymentGateway": {
    "type": "string",
    "description": "Payment Gateway"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "fiscalTaxServiceWhereApplicable": {
    "type": "string",
    "description": "Fiscal/Tax Service where applicable"
   },
   "rolePermission": {
    "type": "string",
    "description": "Role Permission"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "supervisorApproval": {
    "type": "string",
    "description": "Supervisor Approval"
   },
   "optionalDualAuthorization": {
    "type": "string",
    "description": "Optional Dual Authorization"
   }
  }
 }
}
```
