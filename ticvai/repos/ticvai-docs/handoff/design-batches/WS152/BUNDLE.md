# WS152 — Payment Payment Orchestration board 6

**10 screens · 12 operations · 11 schemas · 8 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_REFUND, ORDER_REFUND_APPROVE, ORDER_VIEW, PAYMENT_VOID, REGION_CONFIGURE, WALLET_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-609` | Refund & Payment Adjustment Command Center\t116 | commandCentre | 1 | 0 | — |
| `ADM-610` | Refund Request & Eligibility Workspace\t117 | listDetail | 2 | 0 | — |
| `ADM-611` | Refund Policy & Rule Configuration\t118 | configEditor | 1 | 0 | — |
| `ADM-612` | Refund Allocation & Original Tender Manager\t119 | listDetail | 1 | 0 | — |
| `ADM-613` | Void, Reversal & Cancellation Manager\t120 | listDetail | 1 | 1 | — |
| `ADM-614` | Refund Approval & Exception Workflow\t121 | listDetail | 3 | 0 | — |
| `ADM-615` | Refund Processing, Provider Status & Recovery Center\t122 | listDetail | 1 | 0 | — |
| `ADM-616` | Payment Adjustment & Financial Correction Manager\t123 | listDetail | 1 | 0 | — |
| `ADM-617` | Refund Transaction Trace & Audit Investigation\t124 | listDetail | 1 | 0 | — |
| `ADM-618` | Refund Simulator, Risk Analysis & AI Advisor\t126 | configEditor | 0 | 0 | — |

## Thin screens in this batch

**ADM-612, ADM-613, ADM-614, ADM-615, ADM-616, ADM-617 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-609",
  "name": "Refund & Payment Adjustment Command Center\\t116",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "1",
   "page": 115
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refund-payment-adjustment-command-center-t116-adm-609",
   "component": "apps/ticvai-web/src/routes/commercial/RefundPaymentAdjustmentCommandCenterT116.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-610",
    "ADM-611",
    "ADM-612",
    "ADM-613",
    "ADM-614",
    "ADM-615",
    "ADM-616",
    "ADM-617",
    "ADM-618"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-610",
     "trigger": "Refund Request & Eligibility Workspace\\t117",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-611",
     "trigger": "Refund Policy & Rule Configuration\\t118",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-612",
     "trigger": "Refund Allocation & Original Tender Manager\\t119",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-613",
     "trigger": "Void, Reversal & Cancellation Manager\\t120",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-614",
     "trigger": "Refund Approval & Exception Workflow\\t121",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "carries": [
      "refundId"
     ]
    },
    {
     "to": "ADM-615",
     "trigger": "Refund Processing, Provider Status & Recovery Center\\t122",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-616",
     "trigger": "Payment Adjustment & Financial Correction Manager\\t123",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "carries": [
      "orderId"
     ]
    },
    {
     "to": "ADM-617",
     "trigger": "Refund Transaction Trace & Audit Investigation\\t124",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-618",
     "trigger": "Refund Simulator, Risk Analysis & AI Advisor\\t126",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized visibility across refund, reversal, void and adjustment operations.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Refund Requests",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Refund Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Full Refunds",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Partial Refunds",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Refund Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Pending Refunds",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failed Refunds",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Voids",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Reversals",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Manual Adjustments",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Approval Pending",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Refund Exceptions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 115 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund payment adjustment list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the refund payment adjustment untouched.",
   "emptyFirstRun": "No refund payment adjustment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund payment adjustment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "Refunds in flight",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-609",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-609"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 115. 0 of 0 labels bound to a contract property; 12 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-610",
  "name": "Refund Request & Eligibility Workspace\\t117",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "2",
   "page": 116
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refund-request-eligibility-workspace-t117-adm-610",
   "component": "apps/ticvai-web/src/routes/commercial/RefundRequestEligibilityWorkspaceT117.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the operational workspace for creating and validating a refund request.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Entire transaction, Selected items, Selected tickets, Selected quantities, Specific monetary amount. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 116 §Allow"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 116 §Display"
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
       "label": "Every refund request eligibility",
       "columns": [
        "Order: ORD-847291",
        "Original Amount: AED 1,250",
        "Paid: AED 1,250",
        "Previously Refunded: AED 200",
        "Maximum Remaining Refundable: AED 1,050"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 116 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected refund request eligibility",
       "bindsTo": null,
       "columns": [
        "Order: ORD-847291",
        "Original Amount: AED 1,250",
        "Paid: AED 1,250",
        "Previously Refunded: AED 200",
        "Maximum Remaining Refundable: AED 1,050"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Find original transaction using”, “Before allowing the refund”, “Eligible for Refund”, “Refund Restricted”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 116 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Entire transaction",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 116 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected items",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 116 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected tickets",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 116 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected quantities",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 116 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Specific monetary amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 116 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund request eligibility list.",
   "error": "Could not load. Names which read failed and leaves the refund request eligibility untouched.",
   "emptyFirstRun": "No refund request eligibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund request eligibility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createRefundRequest",
    "contract": "orders",
    "purpose": "Raise a refund",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getRefundPolicy",
    "contract": "orders",
    "purpose": "What is eligible",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Order: ORD-847291",
    "Original Amount: AED 1,250",
    "Paid: AED 1,250",
    "Previously Refunded: AED 200",
    "Maximum Remaining Refundable: AED 1,050"
   ],
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-610",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-610"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 116. 0 of 5 labels bound to a contract property; 10 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-611",
  "name": "Refund Policy & Rule Configuration\\t118",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "3",
   "page": 117
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refund-policy-rule-configuration-t118-adm-611",
   "component": "apps/ticvai-web/src/routes/commercial/RefundPolicyRuleConfigurationT118.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the payment execution rules governing refunds without duplicating Ticket Service Policy. This boundary is important.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Full refund allowed",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial refund allowed",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      },
      {
       "kind": "textField",
       "label": "Multiple partial refunds allowed",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      },
      {
       "kind": "textField",
       "label": "Refund to original tender required",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Alternative tender permitted",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum refund amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund approval threshold",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund expiry/window",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      },
      {
       "kind": "textField",
       "label": "Automatic vs manual processing",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 117 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund policy rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the refund policy rule untouched.",
   "emptyFirstRun": "No refund policy rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setRefundPolicy",
    "contract": "orders",
    "purpose": "Set a venue's refund policy",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-611",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-611"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 117. 0 of 0 labels bound to a contract property; 9 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable."
  },
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-612",
  "name": "Refund Allocation & Original Tender Manager\\t119",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "4",
   "page": 118
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refund-allocation-original-tender-manager-t119-adm-612",
   "component": "apps/ticvai-web/src/routes/commercial/RefundAllocationOriginalTenderManagerT119.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine where the refunded value must be returned. This screen becomes particularly important for Board 5 mixed-tender transactions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Manual allocation with approval. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 118 §Support configurable approaches such as"
   },
   {
    "operation": null,
    "why": "**Refund Allocation & Original Tender Manager\\t119 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 118"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 118"
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
       "label": "Manual allocation with approval",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 118 §Support configurable approaches such as"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setWalletRefundPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund allocation original list.",
   "error": "Could not load. Names which read failed and leaves the refund allocation original untouched.",
   "emptyFirstRun": "No refund allocation original yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund allocation original are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWalletRefundPolicy",
    "contract": "wallet",
    "purpose": "Refund to wallet or original tender",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-612",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-612"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 118. 0 of 0 labels bound to a contract property; 1 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-613",
  "name": "Void, Reversal & Cancellation Manager\\t120",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "5",
   "page": 119
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/void-reversal-cancellation-manager-t120-adm-613",
   "component": "apps/ticvai-web/src/routes/commercial/VoidReversalCancellationManagerT120.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Clearly distinguish voids and reversals from refunds. These should not all be called “refund”.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Refund ✓, Void ✕, Reversal ✕. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 119 §Available Actions"
   },
   {
    "operation": null,
    "why": "**Void, Reversal & Cancellation Manager\\t120 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 119"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 119"
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
       "label": "Refund ✓",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 119 §Available Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Void ✕",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 119 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Reversal ✕",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 119 §Available Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoid",
    "component": "confirmDialog",
    "trigger": "Void ✕",
    "body": "**Void ✕ on a void reversal cancellation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Payment_Payment_Orchestration.pdf, page 119 §Available Actions"
   }
  ],
  "states": {
   "loading": "The void reversal cancellation list.",
   "error": "Could not load. Names which read failed and leaves the void reversal cancellation untouched.",
   "emptyFirstRun": "No void reversal cancellation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the void reversal cancellation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "voidPayment",
    "contract": "orders",
    "purpose": "Void or reverse",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-613",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-613"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 119. 0 of 0 labels bound to a contract property; 3 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "paymentId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-614",
  "name": "Refund Approval & Exception Workflow\\t121",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "6",
   "page": 120
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refund-approval-exception-workflow-t121-adm-614",
   "component": "apps/ticvai-web/src/routes/commercial/RefundApprovalExceptionWorkflowT121.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide governed approval for financially sensitive refund actions.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 120 §Show"
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
       "label": "Every refund approval exception",
       "columns": [
        "Request",
        "Order",
        "Customer",
        "Amount",
        "Reason",
        "Original payment",
        "Requested refund method",
        "Risk indicator",
        "Requester",
        "Age"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 120 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected refund approval exception",
       "bindsTo": null,
       "columns": [
        "Request",
        "Order",
        "Customer",
        "Amount",
        "Reason",
        "Original payment",
        "Requested refund method",
        "Risk indicator",
        "Requester",
        "Age"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Approval can depend on”, “AED 5,000”, “Requested”, “Approval Required”, “Approver”, “Approved / Rejected”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 120 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund approval exception list.",
   "error": "Could not load. Names which read failed and leaves the refund approval exception untouched.",
   "emptyFirstRun": "No refund approval exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund approval exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveRefund",
    "contract": "orders",
    "purpose": "Approve above threshold",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listFraudRules",
    "contract": "orders",
    "purpose": "Show refund-abuse and charge fraud rules",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setFraudRules",
    "contract": "orders",
    "purpose": "Edit refund-abuse and charge fraud rules",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Request",
    "Order",
    "Customer",
    "Amount",
    "Reason",
    "Original payment"
   ],
   "params": [
    {
     "name": "refundId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-614",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-614"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 120. 0 of 10 labels bound to a contract property; 10 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-615",
  "name": "Refund Processing, Provider Status & Recovery Center\\t122",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "7",
   "page": 121
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refund-processing-provider-status-recovery-center-t122-adm-615",
   "component": "apps/ticvai-web/src/routes/commercial/RefundProcessingProviderStatusRecoveryCenterT122.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Track refund execution through the appropriate provider and recover failed or uncertain operations.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 121 §Show"
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
       "label": "Every refund processing provider",
       "columns": [
        "Provider",
        "Merchant account",
        "Original provider transaction",
        "Refund transaction ID",
        "Refund amount",
        "Currency",
        "Submitted timestamp",
        "Provider status",
        "Provider response",
        "Expected completion"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 121 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected refund processing provider",
       "bindsTo": null,
       "columns": [
        "Provider",
        "Merchant account",
        "Original provider transaction",
        "Refund transaction ID",
        "Refund amount",
        "Currency",
        "Submitted timestamp",
        "Provider status",
        "Provider response",
        "Expected completion"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Refund Processing States”, “Verify Provider Status”, “Recovery Actions”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 121 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund processing provider list.",
   "error": "Could not load. Names which read failed and leaves the refund processing provider untouched.",
   "emptyFirstRun": "No refund processing provider yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund processing provider are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "inquirePaymentStatus",
    "contract": "orders",
    "purpose": "Provider status and recovery",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Provider",
    "Merchant account",
    "Original provider transaction",
    "Refund transaction ID",
    "Refund amount",
    "Currency"
   ],
   "params": [
    {
     "name": "paymentId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-615",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-615"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 121. 0 of 10 labels bound to a contract property; 10 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-616",
  "name": "Payment Adjustment & Financial Correction Manager\\t123",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "8",
   "page": 122
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-adjustment-financial-correction-manager-t123-adm-616",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentAdjustmentFinancialCorrectionManagerT123.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle governed payment corrections that are not normal customer refunds. This must be tightly controlled.",
  "gaps": [
   {
    "operation": null,
    "why": "**Payment Adjustment & Financial Correction Manager\\t123 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 122"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 122"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createRefund",
       "label": "Create refund",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createRefund"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment adjustment financial list.",
   "error": "Could not load. Names which read failed and leaves the payment adjustment financial untouched.",
   "emptyFirstRun": "No payment adjustment financial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment adjustment financial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createRefund",
    "contract": "orders",
    "purpose": "Adjustment and correction",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-616",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-616"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 122. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-617",
  "name": "Refund Transaction Trace & Audit Investigation\\t124",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "9",
   "page": 123
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refund-transaction-trace-audit-investigation-t124-adm-617",
   "component": "apps/ticvai-web/src/routes/commercial/RefundTransactionTraceAuditInvestigationT124.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card AED 800; Card AED 100; Show) and no metric row",
  "purpose": "Provide complete traceability from original sale through refund/reversal/adjustment.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 123 §Card AED 800"
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
       "label": "Every refund transaction trace",
       "columns": [
        "↓",
        "Who requested",
        "Why",
        "Policy applied",
        "Calculated amount",
        "Manual changes",
        "Approval",
        "Provider submission",
        "Provider result",
        "Wallet restoration",
        "Finance posting",
        "Final status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 123 §Card AED 800"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected refund transaction trace",
       "bindsTo": null,
       "columns": [
        "↓",
        "Who requested",
        "Why",
        "Policy applied",
        "Calculated amount",
        "Manual changes",
        "Approval",
        "Provider submission",
        "Provider result",
        "Wallet restoration",
        "Finance posting",
        "Final status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Search”, “AED 1,000”, “AED 300”, “Passed”, “Supervisor Approved”, “Execution”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 123 §Card AED 800"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund transaction trace list.",
   "error": "Could not load. Names which read failed and leaves the refund transaction trace untouched.",
   "emptyFirstRun": "No refund transaction trace yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund transaction trace are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderPaymentDetail",
    "contract": "orders",
    "purpose": "Trace and investigate",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓",
    "Who requested",
    "Why",
    "Policy applied",
    "Calculated amount",
    "Manual changes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-617",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-617"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 123. 0 of 12 labels bound to a contract property; 12 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
  "id": "ADM-618",
  "name": "Refund Simulator, Risk Analysis & AI Advisor\\t126",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "6",
   "number": "10",
   "page": 125
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refund-simulator-risk-analysis-ai-advisor-t126-adm-618",
   "component": "apps/ticvai-web/src/routes/commercial/RefundSimulatorRiskAnalysisAiAdvisorT126.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-609"
   ],
   "exitTo": [
    "ADM-609"
   ],
   "transitions": [
    {
     "to": "ADM-609",
     "trigger": "Back to Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select; Original Captured Amount; Configured rule) and no display directory — it is settings, not a population",
  "purpose": "Allow administrators to simulate refund outcomes before execution or rule publication.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Maximum refund amount, Supervisor approval, Cash balance impact. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 125 §Support"
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
       "label": "Order",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Payment",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Refund amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Selected items",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Refund reason",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Original tender",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "Refund date",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Select"
      },
      {
       "kind": "selectField",
       "label": "− Completed Refunds",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Original Captured Amount"
      },
      {
       "kind": "selectField",
       "label": "− Reserved/Pending Refunds",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Original Captured Amount"
      },
      {
       "kind": "textField",
       "label": "= Available Refundable Balance",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Original Captured Amount"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Maximum refund amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Supervisor approval",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Cash balance impact",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 125 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund simulator risk configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the refund simulator risk untouched.",
   "emptyFirstRun": "No refund simulator risk configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-618",
   "workshopBoard": "wireframes/WS92 Payment Payment Orchestration Board 6.dc.html#adm-618"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 125. 0 of 0 labels bound to a contract property; 16 of 145 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
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
 "approveRefund": {
  "method": "POST",
  "path": "/refunds/{refundId}/approve",
  "contract": "orders",
  "summary": "Approve a refund held for approval",
  "permission": "ORDER_REFUND_APPROVE",
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
  "responds": "Refund"
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
 "createRefundRequest": {
  "method": "POST",
  "path": "/refund-requests",
  "contract": "orders",
  "summary": "Guest-initiated refund request",
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
  "responds": null
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
 "listFraudRules": {
  "method": "GET",
  "path": "/fraud-rules",
  "contract": "orders",
  "summary": "The rules evaluated before a charge",
  "permission": "ORDER_VIEW",
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
  "responds": "Page"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OrderPaymentDetailTransactionLedgerView"
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
 "setFraudRules": {
  "method": "PUT",
  "path": "/fraud-rules",
  "contract": "orders",
  "summary": "Change what holds a transaction",
  "permission": "ORDER_MODIFY",
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
  "requestBody": "FraudRuleSet",
  "responds": "FraudRuleSet"
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
 "setWalletRefundPolicy": {
  "method": "PUT",
  "path": "/wallet-refund-policy",
  "contract": "wallet",
  "summary": "What a refund puts back, and where",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": null,
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
  "requestBody": "WalletRefundPolicy",
  "responds": "WalletRefundPolicy"
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
 "ExchangeRateDecimal": {
  "type": "string",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,6)",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n",
  "pattern": "^\\d+(\\.\\d{1,6})?$"
 },
 "FraudRule": {
  "type": "object",
  "x-ticvai-persistence": "orders.fraud_rule",
  "description": "BL-118. **Evaluated before the charge, and it holds rather than refuses.**\nA rule that declines outright turns a false positive into a lost sale with an angry guest. **A rule that flags for review turns it into a delay** — and at a gate, review means a supervisor rather than a rejection.\n",
  "required": [
   "id",
   "name",
   "condition",
   "action",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "condition": {
    "type": "object",
    "description": "Velocity, amount, issuer country, device reuse, mismatched billing.",
    "additionalProperties": true
   },
   "appliesTo": {
    "type": "string",
    "description": "**`refund` rules are evaluated on `createRefund` and `createRefundRequest`** (5.3.33, 29 September build pass), before the money moves: a hold sends the refund to approval rather than refusing it. `charge` rules are evaluated before a charge, as before.",
    "enum": [
     "charge",
     "refund"
    ],
    "default": "charge"
   },
   "signal": {
    "type": "string",
    "nullable": true,
    "description": "The measured signal where the rule is one of the named ones; `condition` carries anything else. **`refundCount`, `refundValue` and `refundRatio` detect excessive refunds by one guest** (or one payment card, per `subjectKey`) over `windowDays`: the number of refunds, their total value, or refunds as a share of what that guest bought in the window. **Counted over every sales channel** (5.3.33): tickets, F&B, retail (a retail return raises its refund here, `RetailReturn.refundId`) and every other line, because every refund is an `orders.refund` whichever channel sold it. The access `excessiveRefunds` signal is the gate-side view of ticket refunds only.",
    "enum": [
     "velocityCount",
     "velocityAmount",
     "issuerCountry",
     "deviceReuse",
     "billingMismatch",
     "refundCount",
     "refundValue",
     "refundRatio"
    ]
   },
   "subjectKey": {
    "type": "string",
    "enum": [
     "guest",
     "paymentToken",
     "device"
    ],
    "default": "guest"
   },
   "threshold": {
    "type": "number",
    "nullable": true
   },
   "windowDays": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "action": {
    "type": "string",
    "enum": [
     "allow",
     "flagForReview",
     "requireStepUp",
     "hold",
     "decline"
    ]
   },
   "riskWeight": {
    "type": "integer"
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
 "FraudRuleSet": {
  "type": "object",
  "x-ticvai-persistence": "none — the whole set of orders.fraud_rule rows, in evaluation order",
  "description": "**The whole set in one body**, as `setFraudRules` requires: a rule set edited one rule at a time spends time in states nobody intended. A rule left out of the set is deactivated, never deleted.\n",
  "required": [
   "rules"
  ],
  "properties": {
   "rules": {
    "type": "array",
    "description": "In evaluation order.",
    "items": {
     "$ref": "#/components/schemas/FraudRule"
    }
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
 "WalletRefundPolicy": {
  "type": "object",
  "x-ticvai-persistence": "wallet.refund_policy",
  "description": "Boards 7.4 and 7.5. **Restoration is to the lot, not to the balance.**",
  "properties": {
   "defaultDestination": {
    "type": "string",
    "enum": [
     "originalTender",
     "wallet",
     "guestChoice"
    ]
   },
   "walletRefundCreditTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "restoreToOriginalLots": {
    "type": "boolean",
    "default": true
   },
   "restoreOriginalExpiry": {
    "type": "boolean",
    "default": true,
    "description": "**Refunding into a new lot with a fresh expiry is a gift.** Sometimes intended, never by accident.\n"
   },
   "walletRefundBonusPercent": {
    "type": "number",
    "nullable": true,
    "description": "An incentive to take the refund as credit rather than to a card."
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
