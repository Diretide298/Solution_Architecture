# WS151 — Payment Payment Orchestration board 5

**10 screens · 16 operations · 16 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `CREDIT_MANAGE, ORDER_CREATE, ORDER_VIEW, PAYMENT_CONFIGURE, PAYMENT_VIEW, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-599` | Mixed Tender & Credit Command Center\t93 | commandCentre | 1 | 0 | — |
| `ADM-600` | Mixed Tender Rule & Combination Builder\t93 | listDetail | 1 | 0 | — |
| `ADM-601` | Split Payment & Tender Allocation Manager\t94 | listDetail | 3 | 0 | — |
| `ADM-602` | B2B Credit Account & Limit Manager\t95 | configEditor | 2 | 0 | — |
| `ADM-603` | B2B Invoice, On-Account & Payment Terms Configuration\t96 | configEditor | 3 | 0 | — |
| `ADM-604` | Stored Value, Gift Card & Voucher Tender Controls\t97 | configEditor | 2 | 0 | — |
| `ADM-605` | Advanced Payment Eligibility, Sequence & Restriction Rules\t98 | listDetail | 1 | 0 | — |
| `ADM-606` | Partial Payment, Failure & Recovery Manager\t100 | listDetail | 5 | 0 | — |
| `ADM-607` | Mixed Tender Transaction Trace & Allocation Audit\t100 | configEditor | 1 | 0 | — |
| `ADM-608` | Mixed Tender Simulator, Credit Exposure & AI Advisor\t102 | listDetail | 2 | 1 | — |

## Thin screens in this batch

**ADM-600, ADM-606 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-599",
  "name": "Mixed Tender & Credit Command Center\\t93",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "1",
   "page": 92
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/mixed-tender-credit-command-center-t93-adm-599",
   "component": "apps/ticvai-web/src/routes/commercial/MixedTenderCreditCommandCenterT93.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-600",
    "ADM-601",
    "ADM-602",
    "ADM-603",
    "ADM-604",
    "ADM-605",
    "ADM-606",
    "ADM-607",
    "ADM-608"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-600",
     "trigger": "Mixed Tender Rule & Combination Builder\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-601",
     "trigger": "Split Payment & Tender Allocation Manager\\t94",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-602",
     "trigger": "B2B Credit Account & Limit Manager\\t95",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-603",
     "trigger": "B2B Invoice, On-Account & Payment Terms Configuration\\t96",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-604",
     "trigger": "Stored Value, Gift Card & Voucher Tender Controls\\t97",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-605",
     "trigger": "Advanced Payment Eligibility, Sequence & Restriction Rules\\t98",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-606",
     "trigger": "Partial Payment, Failure & Recovery Manager\\t100",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-607",
     "trigger": "Mixed Tender Transaction Trace & Allocation Audit\\t100",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-608",
     "trigger": "Mixed Tender Simulator, Credit Exposure & AI Advisor\\t102",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized operational visibility over mixed-tender and account-credit transactions.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Mixed-Tender Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Mixed-Tender Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Tenders per Transaction",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "B2B Credit Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "B2B Credit Utilized",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Outstanding B2B Credit",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Invoice / On-Account Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Gift Card Contributions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Stored-Value Contributions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Split Payment Failures",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Partially Paid Orders",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Payment Allocation Exceptions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The mixed tender credit list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the mixed tender credit untouched.",
   "emptyFirstRun": "No mixed tender credit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mixed tender credit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMixedTenderRules",
    "contract": "payments",
    "purpose": "Tender rules in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-599",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-599"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 92. 0 of 0 labels bound to a contract property; 12 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-600",
  "name": "Mixed Tender Rule & Combination Builder\\t93",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "2",
   "page": 92
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/mixed-tender-rule-combination-builder-t93-adm-600",
   "component": "apps/ticvai-web/src/routes/commercial/MixedTenderRuleCombinationBuilderT93.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card r t Credit; Card) and no metric row",
  "purpose": "Define which payment methods may be combined within a single transaction.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 92 §Card r t Credit"
   },
   {
    "operation": null,
    "why": "**Mixed Tender Rule & Combination Builder\\t93 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Every mixed tender rule",
       "columns": [
        "Card ✓ ✓ ✓ ✓ ✓ ✓",
        "Cash ✓ — ✓ ✓ ✓ ✓",
        "Voucher ✓ ✓ ✓* — ✓ ✓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §Card r t Credit"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected mixed tender rule",
       "bindsTo": null,
       "columns": [
        "Card ✓ ✓ ✓ ✓ ✓ ✓",
        "Cash ✓ — ✓ ✓ ✓ ✓",
        "Voucher ✓ ✓ ✓* — ✓ ✓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Gift”, “Maximum”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 92 §Card r t Credit"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The mixed tender rule list.",
   "error": "Could not load. Names which read failed and leaves the mixed tender rule untouched.",
   "emptyFirstRun": "No mixed tender rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mixed tender rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMixedTenderRules",
    "contract": "payments",
    "purpose": "Which combinations are allowed",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMixedTenderRules"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Card ✓ ✓ ✓ ✓ ✓ ✓",
    "Cash ✓ — ✓ ✓ ✓ ✓",
    "Voucher ✓ ✓ ✓* — ✓ ✓"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-600",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-600"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 92. 0 of 3 labels bound to a contract property; 13 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-601",
  "name": "Split Payment & Tender Allocation Manager\\t94",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "3",
   "page": 93
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/split-payment-tender-allocation-manager-t94-adm-601",
   "component": "apps/ticvai-web/src/routes/commercial/SplitPaymentTenderAllocationManagerT94.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine how an order total is allocated across several payment methods.",
  "gaps": [
   {
    "operation": null,
    "why": "**Split Payment & Tender Allocation Manager\\t94 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 93"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 93"
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
       "impliedBy": "setMultiPaymentSplit",
       "label": "Save multi payment split",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMultiPaymentSplit"
      },
      {
       "kind": "textField",
       "label": "Channel",
       "operation": "listPaymentAllocationRules",
       "notes": "Sends `?channel=` to `listPaymentAllocationRules`.",
       "provenance": "contract orders.yaml GET /payment-allocation-rules"
      },
      {
       "kind": "textField",
       "label": "Terminal id",
       "operation": "listPaymentAllocationRules",
       "notes": "Sends `?terminalId=` to `listPaymentAllocationRules`.",
       "provenance": "contract orders.yaml GET /payment-allocation-rules"
      },
      {
       "kind": "textField",
       "label": "Product id",
       "operation": "listPaymentAllocationRules",
       "notes": "Sends `?productId=` to `listPaymentAllocationRules`.",
       "provenance": "contract orders.yaml GET /payment-allocation-rules"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listPaymentAllocationRules",
       "notes": "Sends `?isActive=` to `listPaymentAllocationRules`.",
       "provenance": "contract orders.yaml GET /payment-allocation-rules"
      },
      {
       "kind": "dataTable",
       "label": "Every payment allocation rule",
       "bindsTo": "PaymentAllocationRule",
       "columns": [
        "PaymentAllocationRule.id",
        "PaymentAllocationRule.channel",
        "PaymentAllocationRule.terminalId",
        "PaymentAllocationRule.productId",
        "PaymentAllocationRule.orderType",
        "PaymentAllocationRule.customerType",
        "PaymentAllocationRule.allocationLevel",
        "PaymentAllocationRule.isActive",
        "PaymentAllocationRule.scopePath"
       ],
       "operation": "listPaymentAllocationRules",
       "provenance": "contract orders.yaml GET /payment-allocation-rules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The split payment tender list.",
   "error": "Could not load. Names which read failed and leaves the split payment tender untouched.",
   "emptyFirstRun": "No split payment tender yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the split payment tender are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMultiPaymentSplit",
    "contract": "orders",
    "purpose": "Allocate a split payment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setMixedTenderRules",
    "contract": "payments",
    "purpose": "The sequence rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMixedTenderRules"
    ]
   },
   {
    "operationId": "listPaymentAllocationRules",
    "contract": "orders",
    "purpose": "The venue's split-tender allocation rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-601",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-601"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 93. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-602",
  "name": "B2B Credit Account & Limit Manager\\t95",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "4",
   "page": 94
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/b2b-credit-account-limit-manager-t95-adm-602",
   "component": "apps/ticvai-web/src/routes/commercial/B2bCreditAccountLimitManagerT95.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage payment credit facilities granted to authorized B2B customers, resellers, corporate clients or partners. This is not the general B2B customer profile. The B2B/CRM module remains authoritative for the customer/account itself. Board 5 owns the payment-credit capability.",
  "gaps": [
   {
    "operation": null,
    "why": "**B2B Credit Account & Limit Manager\\t95 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Credit limit",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 94 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 94 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 94 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed business units",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 94 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed channels",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 94 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Payment terms",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 94 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval level",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 94 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The b2b credit account configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the b2b credit account untouched.",
   "emptyFirstRun": "No b2b credit account configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listB2bCreditAccounts",
    "contract": "payments",
    "purpose": "On-account customers",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createB2bCreditAccount",
    "contract": "payments",
    "purpose": "Open an account",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listB2bCreditAccounts"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-602",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-602"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 94. 0 of 0 labels bound to a contract property; 17 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-603",
  "name": "B2B Invoice, On-Account & Payment Terms Configuration\\t96",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "5",
   "page": 95
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/b2b-invoice-on-account-payment-terms-configuration-t96-adm-603",
   "component": "apps/ticvai-web/src/routes/commercial/B2bInvoiceOnAccountPaymentTermsConfigurationT96.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Define) and no display directory — it is settings, not a population",
  "purpose": "Configure how approved B2B customers can transact without immediate full payment.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Customer/account",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Credit agreement",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Payment term",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Billing cycle",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Invoice requirement",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Purchase order requirement",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Approval requirement",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Transaction maximum",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      },
      {
       "kind": "selectField",
       "label": "Outstanding balance limit",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 95 §Define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The b2b invoice on-account configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the b2b invoice on-account untouched.",
   "emptyFirstRun": "No b2b invoice on-account configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setB2bPaymentTerms",
    "contract": "payments",
    "purpose": "Limit, terms and billing cycle",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listB2bCreditAccounts"
    ]
   },
   {
    "operationId": "getInstalmentPolicy",
    "contract": "payments",
    "purpose": "Show the instalment policy",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setInstalmentPolicy",
    "contract": "payments",
    "purpose": "Edit the instalment policy",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-603",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-603"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 95. 0 of 0 labels bound to a contract property; 10 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "accountId",
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
  "id": "ADM-604",
  "name": "Stored Value, Gift Card & Voucher Tender Controls\\t97",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "6",
   "page": 96
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/stored-value-gift-card-voucher-tender-controls-t97-adm-604",
   "component": "apps/ticvai-web/src/routes/commercial/StoredValueGiftCardVoucherTenderControlsT97.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage how stored-value instruments participate in payment without duplicating the Wallet or Voucher modules.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Can be used as tender",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "textField",
       "label": "Can combine with card",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "textField",
       "label": "Can combine with cash",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "textField",
       "label": "Can combine with B2B credit",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum redemption",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum redemption",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full/partial balance usage",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency restrictions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product restrictions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue restrictions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel restrictions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 96 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stored value gift configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the stored value gift untouched.",
   "emptyFirstRun": "No stored value gift configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setMixedTenderRules",
    "contract": "payments",
    "purpose": "Stored value and voucher tenders",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMixedTenderRules"
    ]
   },
   {
    "operationId": "getCreditConsumptionPolicy",
    "contract": "wallet",
    "purpose": "The order within stored value",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-604",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-604"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 96. 0 of 0 labels bound to a contract property; 11 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-605",
  "name": "Advanced Payment Eligibility, Sequence & Restriction Rules\\t98",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "7",
   "page": 97
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/advanced-payment-eligibility-sequence-restriction-rules--adm-605",
   "component": "apps/ticvai-web/src/routes/commercial/AdvancedPaymentEligibilitySequenceRestrictionRul.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Gift Card second) and no metric row",
  "purpose": "Provide advanced transaction-level payment rules beyond the general method availability configured in Board 1.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Minimum card amount, Credit restriction, Voucher exclusivity. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 97 §Support"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 97 §Gift Card second"
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
       "label": "Every advanced payment eligibility",
       "columns": [
        "↓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 97 §Gift Card second"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected advanced payment eligibility",
       "bindsTo": null,
       "columns": [
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Board 1 answers”, “Board 5 answers”, “AND”, “Voucher first”, “B2B Credit third”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 97 §Gift Card second"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Minimum card amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 97 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Credit restriction",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 97 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Voucher exclusivity",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 97 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The advanced payment eligibility list.",
   "error": "Could not load. Names which read failed and leaves the advanced payment eligibility untouched.",
   "emptyFirstRun": "No advanced payment eligibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the advanced payment eligibility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMixedTenderRules",
    "contract": "payments",
    "purpose": "Sequence and restrictions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMixedTenderRules"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "↓"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-605",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-605"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 97. 0 of 1 labels bound to a contract property; 4 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-606",
  "name": "Partial Payment, Failure & Recovery Manager\\t100",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "8",
   "page": 99
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/partial-payment-failure-recovery-manager-t100-adm-606",
   "component": "apps/ticvai-web/src/routes/commercial/PartialPaymentFailureRecoveryManagerT100.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Gift Card; Card) and no metric row",
  "purpose": "Handle situations where some tenders succeed but another tender fails. This is one of the most important screens in Board 5.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 99 §Gift Card"
   },
   {
    "operation": null,
    "why": "**Partial Payment, Failure & Recovery Manager\\t100 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Every partial payment failure",
       "columns": [
        "AED 200 ✓",
        "AED 800 ✕"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 99 §Gift Card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partial payment failure",
       "bindsTo": null,
       "columns": [
        "AED 200 ✓",
        "AED 800 ✕"
       ],
       "notes": "The pack groups this record's detail under its own headings: “AED 200 successfully consumed”, “Partial Payment States”, “Timeout”, “Partially Paid”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 99 §Gift Card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partial payment failure list.",
   "error": "Could not load. Names which read failed and leaves the partial payment failure untouched.",
   "emptyFirstRun": "No partial payment failure yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partial payment failure are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMixedTenderRules",
    "contract": "payments",
    "purpose": "Partial payment and recovery",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMixedTenderRules"
    ]
   },
   {
    "operationId": "getDunningPolicy",
    "contract": "payments",
    "purpose": "Read the retry schedule this venue runs",
    "trigger": "onLoad"
   },
   {
    "operationId": "setDunningPolicy",
    "contract": "payments",
    "purpose": "Set attempts, spacing and what happens when they run out",
    "trigger": "onSave"
   },
   {
    "operationId": "listDunningCases",
    "contract": "payments",
    "purpose": "The queue, ordered by attempts remaining",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolveDunningCase",
    "contract": "payments",
    "purpose": "Stop chasing, with a reason",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "AED 200 ✓",
    "AED 800 ✕"
   ],
   "params": [
    {
     "name": "caseId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-606",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-606"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 99. 0 of 2 labels bound to a contract property; 2 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-607",
  "name": "Mixed Tender Transaction Trace & Allocation Audit\\t100",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "9",
   "page": 100
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/mixed-tender-transaction-trace-allocation-audit-t100-adm-607",
   "component": "apps/ticvai-web/src/routes/commercial/MixedTenderTransactionTraceAllocationAuditT100.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide a complete financial and operational explanation of every multi-tender transaction.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Operator/customer",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Rules applied",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Payment IDs",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Tender references",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Amounts",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Timestamps",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Overrides",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reversal/refund relationship",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 100 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The mixed tender transaction configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the mixed tender transaction untouched.",
   "emptyFirstRun": "No mixed tender transaction configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listOrderPaymentDetail",
    "contract": "orders",
    "purpose": "Trace the allocation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-607",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-607"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 100. 0 of 0 labels bound to a contract property; 11 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-608",
  "name": "Mixed Tender Simulator, Credit Exposure & AI Advisor\\t102",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "5",
   "number": "10",
   "page": 101
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/mixed-tender-simulator-credit-exposure-ai-advisor-t102-adm-608",
   "component": "apps/ticvai-web/src/routes/commercial/MixedTenderSimulatorCreditExposureAiAdvisorT102.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-599"
   ],
   "exitTo": [
    "ADM-599"
   ],
   "transitions": [
    {
     "to": "ADM-599",
     "trigger": "Back to Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Gift Card; Card; Gift Card AED 200) and no metric row",
  "purpose": "Allow administrators to test complex tender combinations before activating rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Require card for excess, Request approval, Reject B2B credit, Reduce credit allocation. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 101 §Available actions according to policy"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 101 §Gift Card"
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
       "label": "Every mixed tender simulator",
       "columns": [
        "↓",
        "AED 200 deducted",
        "No ticket/order",
        "No clear recovery process",
        "→ Cash"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 101 §Gift Card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected mixed tender simulator",
       "bindsTo": null,
       "columns": [
        "↓",
        "AED 200 deducted",
        "No ticket/order",
        "No clear recovery process",
        "→ Cash"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Order”, “AED 1,000 order”, “AED 1,000”, “Validate Tender Combination”, “Validate Balances / Credit”, “Process Tenders”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 101 §Gift Card"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Require card for excess",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 101 §Available actions according to policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Request approval",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 101 §Available actions according to policy"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject B2B credit",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 101 §Available actions according to policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Reduce credit allocation",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 101 §Available actions according to policy"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectBBCredit",
    "component": "confirmDialog",
    "trigger": "Reject B2B credit",
    "body": "**Reject B2B credit on a mixed tender simulator is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Payment_Payment_Orchestration.pdf, page 101 §Available actions according to policy"
   }
  ],
  "states": {
   "loading": "The mixed tender simulator list.",
   "error": "Could not load. Names which read failed and leaves the mixed tender simulator untouched.",
   "emptyFirstRun": "No mixed tender simulator yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mixed tender simulator are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulatePaymentConfiguration",
    "contract": "payments",
    "purpose": "Simulate mixed tender",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listB2bCreditAccounts",
    "contract": "payments",
    "purpose": "Credit exposure",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓",
    "AED 200 deducted",
    "No ticket/order",
    "No clear recovery process",
    "→ Cash"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-608",
   "workshopBoard": "wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-608"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 101. 0 of 5 labels bound to a contract property; 25 of 178 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createB2bCreditAccount": {
  "method": "POST",
  "path": "/b2b-credit-accounts",
  "contract": "payments",
  "summary": "Open an on-account relationship",
  "permission": "CREDIT_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "B2bCreditAccount",
  "responds": "B2bCreditAccount"
 },
 "getCreditConsumptionPolicy": {
  "method": "GET",
  "path": "/credit-consumption-policy",
  "contract": "wallet",
  "summary": "Which credit is spent first",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CreditConsumptionPolicy"
 },
 "getDunningPolicy": {
  "method": "GET",
  "path": "/dunning-policy",
  "contract": "payments",
  "summary": "How a failed recurring charge is chased",
  "permission": "PAYMENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "DunningPolicy"
 },
 "getInstalmentPolicy": {
  "method": "GET",
  "path": "/instalment-policy",
  "contract": "payments",
  "summary": "What may be paid in instalments, and on what terms",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PayInstalmentPolicy"
 },
 "getMixedTenderRules": {
  "method": "GET",
  "path": "/mixed-tender-rules",
  "contract": "payments",
  "summary": "Which tenders may be combined, and in what order",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MixedTenderRules"
 },
 "listB2bCreditAccounts": {
  "method": "GET",
  "path": "/b2b-credit-accounts",
  "contract": "payments",
  "summary": "On-account customers, their limits and their exposure",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "overLimitOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "B2bCreditAccount"
 },
 "listDunningCases": {
  "method": "GET",
  "path": "/dunning-cases",
  "contract": "payments",
  "summary": "Recurring charges currently being chased",
  "permission": "PAYMENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "state",
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
 "listPaymentAllocationRules": {
  "method": "GET",
  "path": "/payment-allocation-rules",
  "contract": "orders",
  "summary": "The venue's split-tender allocation rules",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": null
   },
   {
    "name": "terminalId",
    "in": "query",
    "required": null
   },
   {
    "name": "productId",
    "in": "query",
    "required": null
   },
   {
    "name": "isActive",
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
 "resolveDunningCase": {
  "method": "POST",
  "path": "/dunning-cases/{caseId}/resolve",
  "contract": "payments",
  "summary": "Stop chasing, with a reason",
  "permission": "PAYMENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "caseId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DunningCase"
 },
 "setB2bPaymentTerms": {
  "method": "PUT",
  "path": "/b2b-credit-accounts/{accountId}/terms",
  "contract": "payments",
  "summary": "Limit, terms, billing cycle and what happens at the limit",
  "permission": "CREDIT_MANAGE",
  "offlineCapable": null,
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
  "requestBody": "B2bPaymentTerms",
  "responds": "B2bPaymentTerms"
 },
 "setDunningPolicy": {
  "method": "PUT",
  "path": "/dunning-policy",
  "contract": "payments",
  "summary": "Set the retry schedule and what happens when it runs out",
  "permission": "PAYMENT_CONFIGURE",
  "offlineCapable": null,
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
  "requestBody": "DunningPolicy",
  "responds": "DunningPolicy"
 },
 "setInstalmentPolicy": {
  "method": "PUT",
  "path": "/instalment-policy",
  "contract": "payments",
  "summary": "Set which products may be paid in instalments, how many and how often",
  "permission": "PAYMENT_CONFIGURE",
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
  "requestBody": "PayInstalmentPolicy",
  "responds": "PayInstalmentPolicy"
 },
 "setMixedTenderRules": {
  "method": "PUT",
  "path": "/mixed-tender-rules",
  "contract": "payments",
  "summary": "Split payment, tender sequence and restrictions",
  "permission": "PAYMENT_CONFIGURE",
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
  "requestBody": "MixedTenderRules",
  "responds": "MixedTenderRules"
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "MultiPaymentSplitTenderPaymentAllocationConfiguratioInput",
  "responds": "MultiPaymentSplitTenderPaymentAllocationConfiguratioView"
 },
 "simulatePaymentConfiguration": {
  "method": "POST",
  "path": "/payment-configuration/simulate",
  "contract": "payments",
  "summary": "What a guest would be offered, and what it would cost",
  "permission": "PAYMENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RoutingContext",
  "responds": "PaymentConfigurationSimulation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "B2bCreditAccount": {
  "type": "object",
  "x-ticvai-persistence": "payments.credit_account",
  "description": "Board 5.4. **Exposure includes unbilled bookings, not just unpaid invoices.**",
  "required": [
   "organisationId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "organisationId": {
    "type": "string",
    "format": "uuid"
   },
   "accountCode": {
    "type": "string"
   },
   "creditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "outstandingInvoiced": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "outstandingUnbilled": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "availableCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "onHold",
     "suspended",
     "closed"
    ]
   },
   "overLimit": {
    "type": "boolean",
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "B2bPaymentTerms": {
  "type": "object",
  "x-ticvai-persistence": "payments.payment_terms",
  "description": "Board 5.5. **What happens at the limit is the decision.**",
  "properties": {
   "accountId": {
    "type": "string",
    "format": "uuid"
   },
   "creditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "paymentTermDays": {
    "type": "integer",
    "default": 30
   },
   "billingCycle": {
    "type": "string",
    "enum": [
     "perBooking",
     "weekly",
     "fortnightly",
     "monthly"
    ]
   },
   "purchaseOrderRequired": {
    "type": "boolean",
    "default": false
   },
   "depositPercent": {
    "type": "number",
    "nullable": true,
    "description": "1 September: *\"partial payment/deposit is supported for bulk bookings such as schools and corporates — e.g. a 20–30% deposit upfront with the balance due on or before arrival.\"*\n"
   },
   "balanceDue": {
    "type": "string",
    "enum": [
     "onArrival",
     "beforeArrival",
     "onTerms"
    ],
    "default": "beforeArrival"
   },
   "atLimit": {
    "type": "string",
    "enum": [
     "refuse",
     "warn",
     "allowWithOverride"
    ],
    "default": "allowWithOverride"
   },
   "overrideApprovalRole": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "CreditConsumptionPolicy": {
  "type": "object",
  "x-ticvai-persistence": "wallet.consumption_policy",
  "description": "Boards 3.5 and 3.7. **There is no neutral default**, which is why this is configuration.\n",
  "properties": {
   "strategy": {
    "type": "string",
    "enum": [
     "expiringFirst",
     "typePriority",
     "nonRefundableFirst",
     "manual"
    ],
    "default": "expiringFirst",
    "description": "**`expiringFirst` is the default because it is the one that does not quietly profit from the guest forgetting.**\n"
   },
   "typeOrder": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "withinTypeOrder": {
    "type": "string",
    "enum": [
     "fefo",
     "fifo",
     "lifo"
    ],
    "default": "fefo"
   },
   "allowSplitTender": {
    "type": "boolean",
    "default": true
   },
   "allowGuestChoice": {
    "type": "boolean",
    "default": false,
    "description": "**Whether a guest may override the order at the till.** Rarely enabled, and the venues that want it want it badly.\n"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "DeclineClass": {
  "type": "string",
  "description": "BL-100. **Whether a failed charge may be tried again at all**, and the distinction is a merchant-account risk rather than a courtesy.\n`soft` — insufficient funds, a temporary hold, an issuer timeout. **Worth another attempt on another day**, and the whole reason a dunning schedule exists.\n`hard` — closed account, stolen card, do-not-honour, invalid number. **Never retried.** A hard decline put on a timetable is how a merchant ID gets flagged by the scheme, and the venue finds out when its acquirer calls.\n`unknown` — the provider gave no usable code. **Treated as `hard`**, because guessing `soft` optimises for one more attempt and risks the thing that cannot be undone.\n",
  "enum": [
   "soft",
   "hard",
   "unknown"
  ]
 },
 "DunningCase": {
  "x-ticvai-persistence": "payments.dunning_case",
  "type": "object",
  "description": "BL-100. **One recurring charge being chased**, and the row a venue works from.\n",
  "required": [
   "id",
   "state",
   "attemptsMade",
   "firstFailedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "description": "The order whose renewal failed."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "state": {
    "$ref": "#/components/schemas/DunningState"
   },
   "declineClass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/DeclineClass"
     }
    ],
    "description": "**From the most recent attempt.** A case that begins `soft` and turns `hard` stops immediately rather than finishing its schedule — the card changed underneath it.\n"
   },
   "attemptsMade": {
    "type": "integer"
   },
   "nextAttemptAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Null where the case has ended or the decline is hard.** A scheduled time on a case nothing will act on is the field that makes a queue untrustworthy.\n"
   },
   "firstFailedAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "resolution": {
    "type": "string",
    "nullable": true,
    "enum": [
     "paidByOtherMeans",
     "cardReplaced",
     "writeOff",
     "cancelledByGuest",
     null
    ]
   },
   "resolutionNote": {
    "type": "string",
    "nullable": true,
    "maxLength": 500,
    "description": "**What `resolveDunningCase` was told, which had nowhere to land until now.** The enum above tells `writeOff` from `cardReplaced`; **which invoice, whose phone call and on what authority is the sentence beside it**, and the operation's own reasoning — that these reasons must be told apart afterwards — only works if the sentence survives.\n**Same shape as `marketing.case.resolution_note`**, which is a RAG source for exactly this reason: a resolution note is the most useful free text a support record holds.\n"
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**Who closed it.** A write-off with no name against it is the one resolution nobody can follow up, and it is also the one that moves money.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Written at `venue` scope.\n"
   }
  }
 },
 "DunningPolicy": {
  "x-ticvai-persistence": "payments.dunning_policy",
  "type": "object",
  "description": "2.14.19-2.14.23, BL-100. **How a failed recurring charge is chased, as a tenant policy rather than a platform constant.** A season pass at AED 300 a month and a locker subscription at AED 15 do not deserve the same number of attempts.\n",
  "required": [
   "maxAttempts",
   "terminalAction"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "maxAttempts": {
    "type": "integer",
    "minimum": 1,
    "maximum": 8,
    "default": 4,
    "description": "**Capped at eight and defaulted to four.** The ceiling is not arbitrary: past a handful of attempts the recovery rate is close to nothing and the cost is a guest watching their bank app light up repeatedly for a charge they already know failed.\n"
   },
   "attemptOffsetDays": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 0
    },
    "default": [
     0,
     3,
     7,
     14
    ],
    "description": "**Days after the first failure, and the spacing is the part that matters.** Retrying at the same hour each day hits the same daily limit on the same card and tells the venue nothing it did not already know — **attempts spaced across the month straddle a payday**, which is the single thing that changes the answer for a soft decline.\n**Must be non-decreasing and no longer than `maxAttempts`**, enforced with 422 rather than by silently truncating a list somebody meant.\n"
   },
   "minimumHoursBetweenAttempts": {
    "type": "integer",
    "default": 24,
    "description": "**A floor under the offsets, because a schedule is edited by hand.** Two offsets on the same day are a typo that reads as a policy.\n"
   },
   "retryableDeclineClasses": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/DeclineClass"
    },
    "default": [
     "soft"
    ],
    "description": "**`soft` alone, and widening it is a deliberate act.** The field exists rather than being implied so that a venue that adds `unknown` has chosen to, and so an auditor can see that it did.\n"
   },
   "notifyGuestOnEachAttempt": {
    "type": "boolean",
    "default": false,
    "description": "**False by default.** A guest told four times about one failed renewal reads it as four failures. The first and the last are the ones that mean something — the first because they can fix it, the last because their pass is about to change.\n"
   },
   "terminalAction": {
    "type": "string",
    "enum": [
     "suspendBilling",
     "cancelRenewal"
    ],
    "default": "suspendBilling",
    "description": "**What happens when the attempts run out, and it deliberately stops short of admission.** `suspendBilling` stops charging and leaves the entitlement as it is; `cancelRenewal` also stops the next term. **Neither revokes entry.**\n`graceDays` on the renewal model already governs how long a pass keeps working, and the failure this separation prevents is concrete: **a guest at a gate on a family day out, refused because a card expired and a retry ran at 3am.** Ending somebody's access stays a staff decision with a name on it.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Written at `tenant` scope.\n"
   }
  }
 },
 "DunningState": {
  "type": "string",
  "enum": [
   "scheduled",
   "inProgress",
   "exhausted",
   "recovered",
   "resolvedManually"
  ],
  "description": "BL-100. **`exhausted` and `recovered` are both endings and only one of them is a failure.** A schedule with a single terminal state cannot tell a venue whether dunning is working, which is the only question a venue asks of it.\n"
 },
 "MixedTenderRules": {
  "type": "object",
  "x-ticvai-persistence": "payments.mixed_tender_rules",
  "description": "Boards 5.2 and 5.7. **Sequence is not cosmetic.**",
  "properties": {
   "splitPaymentAllowed": {
    "type": "boolean",
    "default": true
   },
   "maximumTenders": {
    "type": "integer",
    "default": 3
   },
   "tenderOrder": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "**Across tender kinds.** `wallet` decides the order within stored value."
   },
   "allowedCombinations": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "methodKinds": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "allowed": {
       "type": "boolean"
      },
      "reason": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "partialPaymentAllowed": {
    "type": "boolean",
    "default": false
   },
   "onPartialFailure": {
    "type": "string",
    "enum": [
     "reverseAll",
     "keepAndRetry",
     "keepAndHold"
    ],
    "default": "reverseAll",
    "description": "**Three tenders in, the fourth fails.** Reversing all of it is the only answer that leaves the guest and the ledger in a state anybody can explain.\n"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "MultiPaymentSplitTenderPaymentAllocationConfiguratioInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in `orders.payment_allocation_rule` (DM5, 29 September)",
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
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "False retires the rule for this match key (decided 29 September, writers pass)."
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
 "PayInstalmentPolicy": {
  "type": "object",
  "x-ticvai-persistence": "payments.instalment_policy",
  "description": "4.2.17, 2.14.19. Also the `setInstalmentPolicy` body.",
  "properties": {
   "enabled": {
    "type": "boolean",
    "default": false
   },
   "eligibleProductKinds": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "membership",
      "annualPass",
      "seasonPass",
      "groupBooking",
      "event"
     ]
    }
   },
   "minimumOrderValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "allowedFrequencies": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "monthly",
      "quarterly",
      "custom"
     ]
    }
   },
   "maximumInstalments": {
    "type": "integer",
    "minimum": 2
   },
   "dueAtPurchasePercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "instalmentFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "requireStoredCard": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `tenant` scope."
   }
  }
 },
 "PaymentAllocationRule": {
  "type": "object",
  "x-ticvai-persistence": "orders.payment_allocation_rule",
  "description": "**At what level a split-tender payment is allocated, per channel, terminal, product, order type or customer type** (DM5, 29 September: data model for the agreed operations; written by `setMultiPaymentSplit`). The tender limits themselves stay in `payments.mixed_tender_rules`; this row says what each tender is allocated against. Narrowest match wins; a row naming nothing is the venue default.",
  "required": [
   "id",
   "allocationLevel",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "channel": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderType": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "customerType": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
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
    ]
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "PaymentConfigurationSimulation": {
  "type": "object",
  "description": "Boards 1.10 and 5.10. **Eight boards of configuration that compose, silently.**",
  "properties": {
   "offeredMethods": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "methodId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "routesTo": {
       "type": "string",
       "nullable": true
      },
      "estimatedCost": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "surcharge": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "suppressedMethods": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "methodId": {
       "type": "string",
       "format": "uuid"
      },
      "reason": {
       "type": "string"
      }
     }
    }
   },
   "findings": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "severity": {
       "type": "string",
       "enum": [
        "blocking",
        "warning"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "RoutingContext": {
  "type": "object",
  "required": [
   "amount"
  ],
  "properties": {
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "methodId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "type": "string",
    "nullable": true
   },
   "cardScheme": {
    "type": "string",
    "nullable": true
   },
   "cardIssuerCountry": {
    "type": "string",
    "nullable": true
   },
   "cardPresent": {
    "type": "boolean",
    "default": false
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 }
}
```
