# WS32 — Order   Reservation Management board 2

**9 screens · 14 operations · 27 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `ORDER_CREATE, ORDER_VIEW, ORDER_VOID, PAYMENT_VOID, PRODUCT_CONFIGURE, REGION_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-314` | Amendment & After-Sales Command Center | listDetail | 2 | 0 | — |
| `BO-315` | Order Amendment Workspace | listDetail | 1 | 0 | — |
| `BO-316` | Amendment Eligibility & Policy Rule Builder | configEditor | 1 | 0 | — |
| `BO-317` | Cancellation & Partial Cancellation Policy Configuration | listDetail | 1 | 0 | — |
| `BO-318` | Refund Policy & Refund Calculation Configuration | configEditor | 2 | 0 | — |
| `BO-319` | Void, Reversal & Same-Day Correction Management | configEditor | 5 | 0 | — |
| `BO-321` | After-Sales Financial Settlement & Adjustment Workspace | listDetail | 1 | 0 | — |
| `BO-322` | Approval, Exception & Service Recovery Management | configEditor | 1 | 0 | — |
| `BO-323` | Amendment History, Audit & After-Sales Analytics | configEditor | 2 | 0 | — |

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
    "BO-027",
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
     "provenance": "derived — BO-100 declares entryState.params  and BO-314 holds none of them. The edge carries nothing: BO-314 is opened from BO-100, so this edge is the way back and BO-100 keeps its own state"
    },
    {
     "to": "BO-318",
     "trigger": "Refund Policy & Refund Calculation Configuration",
     "provenance": "derived — BO-318 declares entryState.params venueId and BO-314 holds none of them, so the edge carries nothing and BO-318 opens cold"
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
    },
    {
     "to": "BO-027",
     "trigger": "Works in Reissue & Media Replacement (Ticket Reissue & Fulfillment Regeneration, merged into it on 28…",
     "provenance": "flow F141 step 11→12",
     "operation": "listAmendmentAfterSale"
    },
    {
     "to": "BO-319",
     "trigger": "Works in Void, Reversal & Same-Day Correction Management",
     "provenance": "flow F141 step 9→10",
     "operation": "listAmendmentAfterSale",
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can monitor and manage all after-sales order activities from one centralized operational workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide one operational workspace for all post-sale activities affecting confirmed orders and reservations.",
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
       "kind": "secondaryButton",
       "label": "Refund",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 20 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The amendment after-sales list.",
   "error": "Could not load. Names which read failed and leaves the amendment after-sales untouched.",
   "emptyFirstRun": "No amendment after-sales yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the amendment after-sales are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAmendmentAfterSale2",
    "contract": "orders",
    "purpose": "Amendment History, Audit & After-Sales Analytics",
    "trigger": "onLoad"
   },
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-314",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-314"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 20. 25 of 34 labels bound to a contract property; 43 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Order Amendment, Reservation Amendment, Date Change, Timeslot Change, Performance Change, Quantity Change, Attendee Change, Refund … are choices sent by `listAmendmentAfterSale`.",
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
  "purposeNote": "Authorized users can amend eligible order attributes through a controlled transaction while preserving the original order and validating all affected services.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide agents with a controlled workspace for modifying an existing order without directly editing historical transaction records. The original order must always remain reconstructable.",
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
       "label": "Timeslot",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Allow authorized changes to"
      },
      {
       "kind": "secondaryButton",
       "label": "Quantity",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Allow authorized changes to"
      },
      {
       "kind": "secondaryButton",
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
       "label": "Eligible Product Attributes",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Allow authorized changes to"
      },
      {
       "kind": "secondaryButton",
       "label": "Seat where applicable",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 22 §Allow authorized changes to"
      },
      {
       "kind": "secondaryButton",
       "label": "Save Draft",
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
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-315",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-315"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 22. 10 of 10 labels bound to a contract property; 23 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Timeslot, Quantity, Ticket Holder, Customer Details, Delivery Method, Eligible Product Attributes, Seat where applicable, Save Draft … are choices sent by `setOrderAmendment`.",
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
  "purposeNote": "centrally configured after-sales policies.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define when an order or reservation may be amended and which changes are permitted.",
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
       "label": "Quantity Reduction",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-316",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-316"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 23 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Date Change, Timeslot Change, Performance Change, Quantity Increase, Quantity Reduction, Seat Change, Attendee Change, Delivery Change are choices sent by `setAmendmentEligibilityPolicy`.",
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
       "label": "Entire Reservation",
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
       "label": "Selected Quantity",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Add-On Only",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Package Component where permitted",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-317",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-317"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 7 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Entire Order, Entire Reservation, Individual Ticket, Selected Order Lines, Selected Quantity, Add-On Only, Package Component where permitted are choices sent by `setCancellationPartialPolicy`.",
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
  "purposeNote": "duplicating payment execution or central pricing logic.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure separately) and no display directory — it is settings, not a population",
  "purpose": "Define when a cancellation/amendment creates a refundable amount and how refund entitlement is determined.",
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
       "label": "Full Refund",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partial Refund",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Percentage Refund",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Pro-Rata Refund",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Original Value Less Fees",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Credit",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Voucher/Credit Note",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save refund policy",
       "operation": "setRefundCalculationPolicy",
       "provenance": "contract orders.yaml PUT /refund-calculation-policy (decided 29 September, VM close-out)"
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
    "trigger": "onAction"
   },
   {
    "operationId": "setRefundCalculationPolicy",
    "contract": "orders",
    "purpose": "Save refund policy",
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-318",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-318"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 16 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setRefundCalculationPolicy`.",
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
  "purposeNote": "normal cancellation/refund transactions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Separate genuine void/correction operations from normal customer cancellations and refunds. This is important financially and operationally.",
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
       "operation": "voidEntitlement",
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
       "operation": "cleanupFailedPayment",
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
   },
   {
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void the order same-day (reason enteredInError or duplicate)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Order Void, Accidental Sale Reversal, Duplicate Transaction Correction; Payment Void Request",
    "invalidates": [
     "listVoidReversalSame"
    ]
   },
   {
    "operationId": "voidPayment",
    "contract": "orders",
    "purpose": "Void the payment",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Order Void, Accidental Sale Reversal, Duplicate Transaction Correction; Payment Void Request",
    "invalidates": [
     "listVoidReversalSame"
    ]
   },
   {
    "operationId": "voidEntitlement",
    "contract": "orders",
    "purpose": "Void ticket",
    "trigger": "onAction"
   },
   {
    "operationId": "cleanupFailedPayment",
    "contract": "orders",
    "purpose": "Clear failed payment",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "navigation"
    },
    {
     "name": "paymentId",
     "from": "navigation"
    },
    {
     "name": "entitlementId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-314 with the order picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the order no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-319",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-319"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 12 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Order Void, Accidental Sale Reversal, Duplicate Transaction Correction: `voidOrder`; Payment Void Request: `voidPayment`; still owed by a contract change: `voidEntitlement`, `cleanupFailedPayment`.",
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
  "purposeNote": "Every after-sales operation has a reconciled financial outcome linked to the corresponding order change.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Track) and no metric row",
  "purpose": "Provide a consolidated view of the financial consequences of amendments, cancellations, refunds, exchanges and corrections. This is not the payment engine; it is the after-sales financial orchestration layer.",
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
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.paymentStatus",
        "Refund Pending",
        "Refund Complete"
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
        "AfterSalesFinancialSettlementAdjustmentWorkspaceView.paymentStatus",
        "Refund Pending",
        "Refund Complete"
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
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-321",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-321"
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
  "purposeNote": "Out-of-policy and high-risk after-sales actions are routed through configurable approval and service-recovery workflows with appropriate segregation of duties.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Govern after-sales actions that fall outside normal policies or exceed financial/operational authority.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Partial Refund",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Allow governed remedies"
      },
      {
       "kind": "secondaryButton",
       "label": "Voucher",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Allow governed remedies"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Credit",
       "provenance": "pack Order___Reservation_Management_Reference.pdf, page 33 §Allow governed remedies"
      },
      {
       "kind": "secondaryButton",
       "label": "Alternative Event",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-322",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-322"
  },
  "apisNote": "Regenerated 9 September 2026 from Order___Reservation_Management_Reference.pdf page 33. 0 of 0 labels bound to a contract property; 14 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Fee Waiver, Partial Refund, Voucher, Wallet Credit, Alternative Event are choices sent by `approveExceptionServiceRecovery`.",
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
  "purposeNote": "through the final commercial, financial and credential state. Board 2 — Final Screen Register # Backend Screen Core Responsibility 12.2. Central after-sales",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide complete traceability and analytical visibility across all changes made after original order creation.",
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
   },
   {
    "operationId": "listAmendmentAfterSale",
    "contract": "orders",
    "purpose": "Amendment & After-Sales Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-323",
   "workshopBoard": "wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-323"
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
  "requestBody": "ApprovalExceptionServiceRecoveryManagementInput",
  "responds": "ApprovalExceptionServiceRecoveryManagementView"
 },
 "cleanupFailedPayment": {
  "method": "POST",
  "path": "/payments/{paymentId}/cleanup",
  "contract": "orders",
  "summary": "Clear a failed or orphaned payment",
  "permission": "ORDER_VOID",
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
  "requestBody": "FailedPaymentCleanupInput",
  "responds": "Payment"
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
    "name": null,
    "in": null,
    "required": null
   },
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
   },
   {
    "name": "requestType",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
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
    "name": null,
    "in": null,
    "required": null
   },
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
 "listVoidReversalSame": {
  "method": "GET",
  "path": "/void-reversal-same",
  "contract": "orders",
  "summary": "Void, Reversal & Same-Day Correction Management",
  "permission": "ORDER_VIEW",
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
  "requestBody": "OrderAmendmentWorkspaceInput",
  "responds": "OrderAmendmentWorkspaceView"
 },
 "setRefundCalculationPolicy": {
  "method": "PUT",
  "path": "/refund-calculation-policy",
  "contract": "orders",
  "summary": "Set how a venue calculates a refund and where it goes",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "RefundCalculationPolicyInput",
  "responds": "RefundCalculationPolicyView"
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RefundPolicy",
  "responds": "RefundPolicy"
 },
 "voidEntitlement": {
  "method": "POST",
  "path": "/entitlements/{entitlementId}/void",
  "contract": "orders",
  "summary": "Void a single ticket",
  "permission": "ORDER_VOID",
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
  "requestBody": "VoidEntitlementInput",
  "responds": "Entitlement"
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
 },
 "voidPayment": {
  "method": "POST",
  "path": "/payments/{paymentId}/void",
  "contract": "orders",
  "summary": "Release an authorisation before it is captured",
  "permission": "PAYMENT_VOID",
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
  "responds": "Payment"
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
   "commitPolicy": {
    "type": "string",
    "enum": [
     "beforePayment",
     "afterSuccessfulPayment"
    ],
    "description": "Whether the change commits before payment or only after successful payment; default afterSuccessfulPayment"
   },
   "orderId": {
    "type": "string",
    "description": "Order ID"
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
   "paymentStatus": {
    "type": "string",
    "enum": [
     "collectionRequired",
     "paymentPending",
     "paymentComplete",
     "failed",
     "reconciliationRequired"
    ],
    "description": "After-sales payment status."
   },
   "refundDue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Refund due, subject to policy"
   },
   "commitPolicy": {
    "type": "string",
    "enum": [
     "beforePayment",
     "afterSuccessfulPayment"
    ],
    "description": "Whether the change commits before payment or only after successful payment; default afterSuccessfulPayment (pack: calculate, collect, commit)"
   },
   "orderId": {
    "type": "string",
    "description": "Order ID"
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
   "requestType": {
    "type": "string",
    "enum": [
     "orderAmendment",
     "reservationAmendment",
     "dateChange",
     "timeslotChange",
     "performanceChange",
     "quantityChange",
     "attendeeChange"
    ],
    "description": "Request type."
   },
   "requestTypeCancellation": {
    "type": "boolean",
    "description": "The request is a full or partial cancellation"
   }
  }
 },
 "AmendmentEligibilityPolicyRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in the amendment columns of `orders.after_sale_policy` (DM5, 29 September)",
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
   "eligibleTicketStatuses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "unused",
      "partiallyUsed",
      "fullyUsed",
      "expired",
      "cancelled",
      "suspended"
     ]
    },
    "description": "Ticket usage statuses from which amendment is allowed."
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
   "eligibleTicketStatuses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "unused",
      "partiallyUsed",
      "fullyUsed",
      "expired",
      "cancelled",
      "suspended"
     ]
    },
    "description": "Ticket usage statuses from which amendment is allowed."
   },
   "exceptionRole": {
    "type": "string",
    "enum": [
     "agent",
     "supervisor",
     "manager"
    ],
    "description": "Lowest role that may make an out-of-policy exception"
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
   "anomalyType": {
    "type": "string",
    "enum": [
     "excessiveVoids",
     "repeatedManualRefunds",
     "frequentFeeWaivers",
     "highReissueFrequency",
     "repeatedOutOfPolicyExceptions"
    ],
    "description": "Unusual pattern surfaced."
   }
  }
 },
 "ApprovalExceptionServiceRecoveryManagementInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in `orders.after_sale_request` (DM5, 29 September)",
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
   "remedy": {
    "type": "string",
    "enum": [
     "complimentaryReissue",
     "feeWaiver",
     "partialRefund",
     "voucher",
     "walletCredit",
     "alternativeDate",
     "alternativeEvent",
     "complimentaryAddOn"
    ],
    "description": "Governed remedy granted."
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "escalate"
    ],
    "description": "Approver decision"
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
   "remedy": {
    "type": "string",
    "enum": [
     "complimentaryReissue",
     "feeWaiver",
     "partialRefund",
     "voucher",
     "walletCredit",
     "alternativeDate",
     "alternativeEvent",
     "complimentaryAddOn"
    ],
    "description": "Governed remedy granted."
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "escalate"
    ],
    "description": "Approver decision"
   },
   "approvalLevel": {
    "type": "string",
    "enum": [
     "supervisor",
     "manager",
     "finance",
     "director"
    ],
    "description": "Approval level reached"
   }
  }
 },
 "CancellationPartialCancellationPolicyConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in `orders.after_sale_policy` and its `orders.after_sale_policy_window` rows (DM5, 29 September)",
  "description": "**What Cancellation & Partial Cancellation Policy Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "permittedScopes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "entireOrder",
      "entireReservation",
      "individualTicket",
      "selectedOrderLines",
      "selectedQuantity",
      "addOnOnly",
      "groupMember",
      "packageComponent"
     ]
    },
    "description": "What may be cancelled."
   },
   "evaluatedConditions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "orderStatus",
      "paymentStatus",
      "ticketStatus",
      "usage",
      "eventDate",
      "cancellationWindow",
      "product",
      "channel",
      "customerSegment"
     ]
    },
    "description": "What the policy evaluates."
   },
   "windows": {
    "type": "array",
    "description": "Cancellation windows; thresholds ascend (audit R123 (6))",
    "items": {
     "type": "object",
     "properties": {
      "minHoursBefore": {
       "type": "integer",
       "description": "Window starts this many hours before the event"
      },
      "maxHoursBefore": {
       "type": "integer",
       "description": "Window ends this many hours before the event (empty = no upper bound)"
      },
      "outcome": {
       "type": "string",
       "enum": [
        "permitted",
        "permittedWithFee",
        "notPermitted"
       ],
       "description": "Outcome in this window"
      },
      "feePercent": {
       "type": "number",
       "description": "Cancellation fee, percent"
      },
      "feeAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Cancellation fee, fixed"
      },
      "supervisorExceptionAllowed": {
       "type": "boolean",
       "description": "A supervisor may override notPermitted"
      }
     }
    }
   },
   "reasonCodes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "customerRequest",
      "eventCancelled",
      "operationalIssue",
      "duplicateOrder",
      "weather",
      "serviceRecovery",
      "fraudReview",
      "other"
     ]
    },
    "description": "Cancellation reason codes offered"
   }
  }
 },
 "CancellationPartialCancellationPolicyConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Cancellation & Partial Cancellation Policy Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "permittedScopes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "entireOrder",
      "entireReservation",
      "individualTicket",
      "selectedOrderLines",
      "selectedQuantity",
      "addOnOnly",
      "groupMember",
      "packageComponent"
     ]
    },
    "description": "What may be cancelled."
   },
   "evaluatedConditions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "orderStatus",
      "paymentStatus",
      "ticketStatus",
      "usage",
      "eventDate",
      "cancellationWindow",
      "product",
      "channel",
      "customerSegment"
     ]
    },
    "description": "What the policy evaluates."
   },
   "windows": {
    "type": "array",
    "description": "Cancellation windows, e.g. over 72 hours permitted; 24-72 hours with fee; under 24 hours not permitted except supervisor exception. Thresholds ascend (audit R123 (6))",
    "items": {
     "type": "object",
     "properties": {
      "minHoursBefore": {
       "type": "integer",
       "description": "Window starts this many hours before the event"
      },
      "maxHoursBefore": {
       "type": "integer",
       "description": "Window ends this many hours before the event (empty = no upper bound)"
      },
      "outcome": {
       "type": "string",
       "enum": [
        "permitted",
        "permittedWithFee",
        "notPermitted"
       ],
       "description": "Outcome in this window"
      },
      "feePercent": {
       "type": "number",
       "description": "Cancellation fee, percent"
      },
      "feeAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Cancellation fee, fixed"
      },
      "supervisorExceptionAllowed": {
       "type": "boolean",
       "description": "A supervisor may override notPermitted"
      }
     }
    }
   },
   "reasonCodes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "customerRequest",
      "eventCancelled",
      "operationalIssue",
      "duplicateOrder",
      "weather",
      "serviceRecovery",
      "fraudReview",
      "other"
     ]
    },
    "description": "Cancellation reason codes offered"
   }
  }
 },
 "Entitlement": {
  "type": "object",
  "x-ticvai-persistence": "access.entitlement",
  "description": "**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n",
  "required": [
   "id",
   "templateId",
   "productId",
   "orderId",
   "subjectId",
   "status",
   "validFrom",
   "validTo"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "description": "The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "mediaCode": {
    "type": "string",
    "description": "What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"
   },
   "status": {
    "$ref": "../spine/orders.yaml#/components/schemas/EntitlementStatus"
   },
   "statusNote": {
    "type": "string",
    "nullable": true,
    "description": "**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"
   },
   "entriesUsed": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true
   },
   "lastEntryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"
   },
   "frozenDays": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"
   },
   "suspendedReason": {
    "type": "string",
    "nullable": true
   },
   "freezeReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "travelling",
     "injury",
     "personal",
     "seasonal",
     "other"
    ],
    "description": "The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."
   },
   "freezeNote": {
    "type": "string",
    "nullable": true,
    "maxLength": 500,
    "description": "The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."
   },
   "isNameBound": {
    "type": "boolean",
    "default": false
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "sharedWithSubjectIds": {
    "type": "array",
    "description": "`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedVia": {
    "type": "string",
    "enum": [
     "sale",
     "invitation",
     "reissue",
     "transfer",
     "resale",
     "membership",
     "groupBooking"
    ],
    "description": "**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"
   },
   "supersedesEntitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"
   },
   "walletValueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"
   },
   "facePassEnrolmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"
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
 "FailedPaymentCleanupInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `cleanupFailedPayment` takes (decided 29 September, readiness close-out).",
  "required": [
   "action",
   "reason"
  ],
  "properties": {
   "action": {
    "type": "string",
    "description": "How the payment is cleared (decided 29 September, readiness close-out).",
    "enum": [
     "releaseHold",
     "cancelPending",
     "markAbandoned"
    ]
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
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
 "OrderAmendmentWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in `orders.after_sale_request`, and the change itself in the order lines (DM5, 29 September)",
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
   "seat": {
    "type": "string",
    "description": "Seat where applicable"
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
   "seat": {
    "type": "string",
    "description": "Seat where applicable"
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
 "RefundCalculationPolicyInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `setRefundCalculationPolicy` takes (decided 29 September, readiness close-out).",
  "required": [
   "refundTypes",
   "refundDestinations"
  ],
  "properties": {
   "refundTypes": {
    "type": "array",
    "minItems": 1,
    "description": "The calculations a refund may use (decided 29 September, readiness close-out).",
    "items": {
     "type": "string",
     "enum": [
      "fullRefund",
      "partialRefund",
      "percentageRefund",
      "proRataRefund",
      "originalValueLessFees"
     ]
    }
   },
   "refundDestinations": {
    "type": "array",
    "minItems": 1,
    "description": "Where refunded money may go (decided 29 September, readiness close-out).",
    "items": {
     "type": "string",
     "enum": [
      "originalPayment",
      "walletCredit",
      "voucherCreditNote"
     ]
    }
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Required when `percentageRefund` is allowed."
   },
   "nonRefundableFees": {
    "type": "array",
    "description": "Order-fee categories (`orders.order_fee.category`) that `originalValueLessFees` keeps back.",
    "items": {
     "type": "string",
     "maxLength": 20
    }
   },
   "scope": {
    "type": "object",
    "nullable": true,
    "description": "Narrows the policy; null applies it venue-wide.",
    "properties": {
     "productIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "channels": {
      "type": "array",
      "items": {
       "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
      }
     }
    }
   }
  }
 },
 "RefundCalculationPolicyView": {
  "type": "object",
  "x-ticvai-persistence": "orders.refund_calculation_policy",
  "description": "**How a venue calculates a refund and where the money goes.** Set by `setRefundCalculationPolicy` (decided 29 September, readiness close-out). The authority limits and time bands stay on `RefundPolicy`.\n",
  "required": [
   "refundTypes",
   "refundDestinations"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "refundTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "fullRefund",
      "partialRefund",
      "percentageRefund",
      "proRataRefund",
      "originalValueLessFees"
     ]
    }
   },
   "refundDestinations": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "originalPayment",
      "walletCredit",
      "voucherCreditNote"
     ]
    }
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true
   },
   "nonRefundableFees": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 20
    }
   },
   "scope": {
    "type": "object",
    "nullable": true,
    "properties": {
     "productIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "channels": {
      "type": "array",
      "items": {
       "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
      }
     }
    }
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "RefundPolicy": {
  "x-ticvai-persistence": "orders.refund_policy + orders.refund_policy_time_band",
  "type": "object",
  "description": "Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n",
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
    "format": "uuid",
    "readOnly": true,
    "description": "The venue in the path. Not taken from a `setRefundPolicy` body."
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
    "nullable": true,
    "minimum": 0,
    "description": "Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."
   },
   "varianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"
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
 },
 "VoidEntitlementInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `voidEntitlement` takes. The reason comes from the void reason list, as for `voidOrder` (decided 29 September, readiness close-out).",
  "required": [
   "reason",
   "recordedAt"
  ],
  "properties": {
   "reason": {
    "$ref": "#/components/schemas/VoidReason"
   },
   "note": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500,
    "nullable": true,
    "description": "Required when `reason` is `other`; optional otherwise."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
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
 },
 "VoidReversalSameDayCorrectionManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Void, Reversal & Same-Day Correction Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "rolePermission": {
    "type": "string",
    "description": "Role Permission"
   },
   "supervisorApproval": {
    "type": "string",
    "description": "Supervisor Approval"
   },
   "optionalDualAuthorization": {
    "type": "string",
    "description": "Optional Dual Authorization"
   },
   "voidType": {
    "type": "string",
    "enum": [
     "orderVoid",
     "paymentVoidRequest",
     "ticketVoid",
     "accidentalSaleReversal",
     "sameDayCorrection",
     "failedTransactionCleanup"
    ],
    "description": "What is voided or reversed."
   },
   "reasonCode": {
    "type": "string",
    "enum": [
     "operatorError",
     "wrongProduct",
     "wrongQuantity",
     "wrongPayment",
     "technicalFailure"
    ],
    "description": "Mandatory reason."
   }
  }
 }
}
```
