# WS153 — Payment Payment Orchestration board 7

**10 screens · 12 operations · 13 schemas · 6 permissions**

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
  `LEDGER_POST, LEDGER_VIEW, PAYMENT_CONFIGURE, PAYMENT_VIEW, SETTLEMENT_RECONCILE, SETTLEMENT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-619` | Reconciliation & Settlement Command Center\t139 | commandCentre | 2 | 0 | — |
| `ADM-620` | Reconciliation Source & Import Manager\t141 | listDetail | 2 | 0 | — |
| `ADM-621` | Transaction Matching & Reconciliation Engine\t142 | commandCentre | 1 | 0 | — |
| `ADM-622` | Reconciliation Exception & Investigation Center\t143 | listDetail | 2 | 0 | — |
| `ADM-623` | Settlement & Payout Manager\t144 | listDetail | 1 | 0 | — |
| `ADM-624` | Fees, Commission, FX & Settlement Economics\t145 | listDetail | 1 | 0 | — |
| `ADM-625` | Merchant Account & Settlement Calendar Manager\t146 | listDetail | 2 | 0 | — |
| `ADM-626` | Settlement Posting, Finance Handoff & Close Manager\t148 | listDetail | 1 | 0 | — |
| `ADM-627` | Reconciliation Audit, Trace & Evidence Center\t149 | configEditor | 1 | 0 | — |
| `ADM-628` | Reconciliation Simulator, Forecast & AI Operations Advisor\t150 | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-620, ADM-621, ADM-622, ADM-623, ADM-626, ADM-628 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-619",
  "name": "Reconciliation & Settlement Command Center\\t139",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "1",
   "page": 138
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/reconciliation-settlement-command-center-t139-adm-619",
   "component": "apps/ticvai-web/src/routes/commercial/ReconciliationSettlementCommandCenterT139.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-620",
    "ADM-621",
    "ADM-622",
    "ADM-623",
    "ADM-624",
    "ADM-625",
    "ADM-626",
    "ADM-627",
    "ADM-628"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-620",
     "trigger": "Reconciliation Source & Import Manager\\t141",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "ADM-621",
     "trigger": "Transaction Matching & Reconciliation Engine\\t142",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "ADM-622",
     "trigger": "Reconciliation Exception & Investigation Center\\t143",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "settlementId"
     ]
    },
    {
     "to": "ADM-623",
     "trigger": "Settlement & Payout Manager\\t144",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "ADM-624",
     "trigger": "Fees, Commission, FX & Settlement Economics\\t145",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "ADM-625",
     "trigger": "Merchant Account & Settlement Calendar Manager\\t146",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "ADM-626",
     "trigger": "Settlement Posting, Finance Handoff & Close Manager\\t148",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "ADM-627",
     "trigger": "Reconciliation Audit, Trace & Evidence Center\\t149",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "ADM-628",
     "trigger": "Reconciliation Simulator, Forecast & AI Operations Advisor\\t150",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Provide an executive and operational overview of payment reconciliation and settlement health.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 138 §Show"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "TICVAI Transaction Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Provider Transaction Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Matched Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Match Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Unmatched Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Unmatched Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Settlement Expected",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Settlement Received",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Settlement Variance",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Provider Fees",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Refund Settlement Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Open Exceptions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every reconciliation settlement \\t139",
       "columns": [
        "Expected",
        "Pending",
        "Received",
        "Partially Received",
        "Variance",
        "Overdue"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reconciliation settlement \\t139",
       "bindsTo": null,
       "columns": [
        "Expected",
        "Pending",
        "Received",
        "Partially Received",
        "Variance",
        "Overdue"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Matched”, “Match Rate”, “Breakdown”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 138 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconciliation settlement \\t139 list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the reconciliation settlement \\t139 untouched.",
   "emptyFirstRun": "No reconciliation settlement \\t139 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reconciliation settlement \\t139 are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSettlements",
    "contract": "finance",
    "purpose": "Settlements to date",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listReconciliationSources",
    "contract": "payments",
    "purpose": "Feeds and their freshness",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-619",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-619"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 138. 0 of 6 labels bound to a contract property; 18 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-620",
  "name": "Reconciliation Source & Import Manager\\t141",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "2",
   "page": 140
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/reconciliation-source-import-manager-t141-adm-620",
   "component": "apps/ticvai-web/src/routes/commercial/ReconciliationSourceImportManagerT141.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage all sources used to compare TICVAI payment records with external financial processing records.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Scheduled report imports. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 140 §Support provider-specific sources such as"
   },
   {
    "operation": null,
    "why": "**Reconciliation Source & Import Manager\\t141 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 140"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 140"
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
       "label": "Scheduled report imports",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 140 §Support provider-specific sources such as"
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
       "impliedBy": "setReconciliationSource"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconciliation source import list.",
   "error": "Could not load. Names which read failed and leaves the reconciliation source import untouched.",
   "emptyFirstRun": "No reconciliation source import yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reconciliation source import are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setReconciliationSource",
    "contract": "payments",
    "purpose": "Define a settlement feed",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReconciliationSources"
    ]
   },
   {
    "operationId": "ingestSettlementFile",
    "contract": "finance",
    "purpose": "Import one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-620",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-620"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 140. 0 of 0 labels bound to a contract property; 1 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-621",
  "name": "Transaction Matching & Reconciliation Engine\\t142",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "3",
   "page": 141
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/transaction-matching-reconciliation-engine-t142-adm-621",
   "component": "apps/ticvai-web/src/routes/commercial/TransactionMatchingReconciliationEngineT142.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Automatically match TICVAI payment transactions against provider/acquirer records.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Exact Match — 100%",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 141 §Display"
      },
      {
       "kind": "metricTile",
       "label": "High Confidence — 97%",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 141 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Potential Match — 82%",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 141 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The transaction matching reconciliation list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the transaction matching reconciliation untouched.",
   "emptyFirstRun": "No transaction matching reconciliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the transaction matching reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setReconciliationMatchingRules",
    "contract": "payments",
    "purpose": "How a match is made",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-621",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-621"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 141. 0 of 0 labels bound to a contract property; 3 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-622",
  "name": "Reconciliation Exception & Investigation Center\\t143",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "4",
   "page": 142
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/reconciliation-exception-investigation-center-t143-adm-622",
   "component": "apps/ticvai-web/src/routes/commercial/ReconciliationExceptionInvestigationCenterT143.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Centralize all payment discrepancies requiring operational or financial investigation.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 142 §Show"
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
       "label": "Every reconciliation exception investigation",
       "columns": [
        "Payment",
        "Order",
        "Provider transaction",
        "Provider",
        "Merchant account",
        "Amount",
        "Currency",
        "Date",
        "Settlement",
        "Related refund/reversal",
        "Match result"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 142 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reconciliation exception investigation",
       "bindsTo": null,
       "columns": [
        "Payment",
        "Order",
        "Provider transaction",
        "Provider",
        "Merchant account",
        "Amount",
        "Currency",
        "Date",
        "Settlement",
        "Related refund/reversal",
        "Match result"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Exception Types”, “Detected”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 142 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconciliation exception investigation list.",
   "error": "Could not load. Names which read failed and leaves the reconciliation exception investigation untouched.",
   "emptyFirstRun": "No reconciliation exception investigation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reconciliation exception investigation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSettlementExceptions",
    "contract": "finance",
    "purpose": "What did not match",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "resolveSettlementException",
    "contract": "finance",
    "purpose": "Resolve it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Payment",
    "Order",
    "Provider transaction",
    "Provider",
    "Merchant account",
    "Amount"
   ],
   "params": [
    {
     "name": "settlementId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-622",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-622"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 142. 0 of 11 labels bound to a contract property; 11 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-623",
  "name": "Settlement & Payout Manager\\t144",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "5",
   "page": 143
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/settlement-payout-manager-t144-adm-623",
   "component": "apps/ticvai-web/src/routes/commercial/SettlementPayoutManagerT144.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Track expected and actual settlements from payment providers/acquirers.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 143 §Display"
   },
   {
    "operation": null,
    "why": "**Settlement & Payout Manager\\t144 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every settlement payout \\t144",
       "columns": [
        "Settlement ID",
        "Provider",
        "Acquirer",
        "Merchant Account",
        "Legal Entity",
        "Settlement Period",
        "Gross Sales",
        "Refunds",
        "Chargebacks",
        "Fees",
        "Adjustments",
        "Reserve/Holdback",
        "Net Expected",
        "Net Received",
        "Currency",
        "Settlement Date"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 143 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected settlement payout \\t144",
       "bindsTo": null,
       "columns": [
        "Settlement ID",
        "Provider",
        "Acquirer",
        "Merchant Account",
        "Legal Entity",
        "Settlement Period",
        "Gross Sales",
        "Refunds",
        "Chargebacks",
        "Fees",
        "Adjustments",
        "Reserve/Holdback",
        "Net Expected",
        "Net Received",
        "Currency",
        "Settlement Date"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Refunds”, “Provider Fees”, “Chargebacks”, “Settlement States”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 143 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The settlement payout \\t144 list.",
   "error": "Could not load. Names which read failed and leaves the settlement payout \\t144 untouched.",
   "emptyFirstRun": "No settlement payout \\t144 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the settlement payout \\t144 are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSettlements",
    "contract": "finance",
    "purpose": "Settlement and payout",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Settlement ID",
    "Provider",
    "Acquirer",
    "Merchant Account",
    "Legal Entity",
    "Settlement Period"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-623",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-623"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 143. 0 of 16 labels bound to a contract property; 16 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-624",
  "name": "Fees, Commission, FX & Settlement Economics\\t145",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "6",
   "page": 144
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/fees-commission-fx-settlement-economics-t145-adm-624",
   "component": "apps/ticvai-web/src/routes/commercial/FeesCommissionFxSettlementEconomicsT145.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare) and no metric row",
  "purpose": "Provide visibility into the financial deductions and differences between gross payment value and net settlement.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: Fixed transaction fee, Percentage fee, Authorization fee, Capture fee, Refund fee, Chargeback fee, Cross-border fee, Wallet/APM fee …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 144 §Compare"
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
       "label": "Every fees commission settlement",
       "columns": [
        "Contracted fee",
        "Calculated expected fee",
        "Provider charged fee",
        "Variance",
        "FX"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected fees commission settlement",
       "bindsTo": null,
       "columns": [
        "Contracted fee",
        "Calculated expected fee",
        "Provider charged fee",
        "Variance",
        "FX"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Provider Fee”, “Where currencies differ, show”, “Important Boundary”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Compare"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Fixed transaction fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Percentage fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Authorization fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Capture fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Refund fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Chargeback fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Cross-border fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet/APM fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 144 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fees commission settlement list.",
   "error": "Could not load. Names which read failed and leaves the fees commission settlement untouched.",
   "emptyFirstRun": "No fees commission settlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the fees commission settlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getPaymentProviderEconomics",
    "contract": "payments",
    "purpose": "Fees, commission and FX",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Contracted fee",
    "Calculated expected fee",
    "Provider charged fee",
    "Variance",
    "FX"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-624",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-624"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 144. 0 of 5 labels bound to a contract property; 14 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-625",
  "name": "Merchant Account & Settlement Calendar Manager\\t146",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "7",
   "page": 145
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/merchant-account-settlement-calendar-manager-t146-adm-625",
   "component": "apps/ticvai-web/src/routes/commercial/MerchantAccountSettlementCalendarManagerT146.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row Rendered on the calendar template (M17-03, 29 September).",
  "purpose": "Manage operational settlement expectations across providers, merchant accounts and legal entities.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 145 §Display"
   },
   {
    "operation": null,
    "why": "**Merchant Account & Settlement Calendar Manager\\t146 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   }
  ],
  "layout": {
   "template": "calendar",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every merchant account settlement",
       "columns": [
        "Transaction period",
        "Expected settlement date",
        "Actual settlement date",
        "Status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 145 §Display"
      },
      {
       "kind": "selectField",
       "label": "View: day, week or month",
       "notes": "**Every calendar has day, week and month views, and the day view is broken into hours from the venue's day start hour** (17 September minutes, M17-03). Built on the shared calendar view (`calendarView`, to be added to the component library); until then a timeline per view.",
       "provenance": "29 September pass (P29 group A)"
      },
      {
       "kind": "multiSelect",
       "label": "Category",
       "notes": "**Filtered by category, so a team sees only what is theirs** (M17-03).",
       "provenance": "29 September pass (P29 group A)"
      },
      {
       "kind": "calendarView",
       "label": "Calendar",
       "operation": "listMerchantAccounts",
       "notes": "Entries of the view in force, placed by date and hour.",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected merchant account settlement",
       "bindsTo": null,
       "columns": [
        "Transaction period",
        "Expected settlement date",
        "Actual settlement date",
        "Status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Tenant”, “Legal Entity”, “Provider / Acquirer”, “Merchant Account”, “For each merchant account”, “Settlement”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 145 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The merchant account settlement list.",
   "error": "Could not load. Names which read failed and leaves the merchant account settlement untouched.",
   "emptyFirstRun": "No merchant account settlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the merchant account settlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMerchantAccounts",
    "contract": "payments",
    "purpose": "Merchant accounts and calendars",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setMerchantAccount",
    "contract": "payments",
    "purpose": "Bind one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listMerchantAccounts"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Transaction period",
    "Expected settlement date",
    "Actual settlement date",
    "Status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-625",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-625"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 145. 0 of 4 labels bound to a contract property; 4 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-626",
  "name": "Settlement Posting, Finance Handoff & Close Manager\\t148",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "8",
   "page": 147
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/settlement-posting-finance-handoff-close-manager-t148-adm-626",
   "component": "apps/ticvai-web/src/routes/commercial/SettlementPostingFinanceHandoffCloseManagerT148.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when reconciled payment information becomes ready for downstream financial posting and period close.",
  "gaps": [
   {
    "operation": null,
    "why": "**Settlement Posting, Finance Handoff & Close Manager\\t148 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 147"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 147"
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
       "impliedBy": "recordSettlement",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordSettlement"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The settlement posting finance list.",
   "error": "Could not load. Names which read failed and leaves the settlement posting finance untouched.",
   "emptyFirstRun": "No settlement posting finance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the settlement posting finance are still there. The pack's own statuses are Not Ready — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordSettlement",
    "contract": "finance",
    "purpose": "Post to the ledger",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-626",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-626"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 147. 0 of 0 labels bound to a contract property; 8 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "obligationId",
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
  "id": "ADM-627",
  "name": "Reconciliation Audit, Trace & Evidence Center\\t149",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "9",
   "page": 148
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/reconciliation-audit-trace-evidence-center-t149-adm-627",
   "component": "apps/ticvai-web/src/routes/commercial/ReconciliationAuditTraceEvidenceCenterT149.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide a complete audit trail explaining how any payment became reconciled and financially closed.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 148 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Action",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 148 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Previous state",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 148 §Capture"
      },
      {
       "kind": "selectField",
       "label": "New state",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 148 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 148 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Timestamp",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 148 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 148 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconciliation audit trace configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reconciliation audit trace untouched.",
   "emptyFirstRun": "No reconciliation audit trace configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getUnifiedReconciliation",
    "contract": "finance",
    "purpose": "Audit and evidence",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-627",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-627"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 148. 0 of 0 labels bound to a contract property; 7 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-628",
  "name": "Reconciliation Simulator, Forecast & AI Operations Advisor\\t150",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "7",
   "number": "10",
   "page": 149
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/reconciliation-simulator-forecast-ai-operations-advisor--adm-628",
   "component": "apps/ticvai-web/src/routes/commercial/ReconciliationSimulatorForecastAiOperationsAdvis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-619"
   ],
   "exitTo": [
    "ADM-619"
   ],
   "transitions": [
    {
     "to": "ADM-619",
     "trigger": "Back to Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast) and no metric row",
  "purpose": "Provide simulation, forecasting and AI-assisted analysis across reconciliation and settlement operations.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 149 §Forecast"
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
       "label": "Every reconciliation simulator forecast",
       "columns": [
        "Expected settlement",
        "Expected cash receipt",
        "Provider fees",
        "Refund deductions",
        "Chargeback deductions",
        "Currency conversion",
        "Merchant account payout"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 149 §Forecast"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reconciliation simulator forecast",
       "bindsTo": null,
       "columns": [
        "Expected settlement",
        "Expected cash receipt",
        "Provider fees",
        "Refund deductions",
        "Chargeback deductions",
        "Currency conversion",
        "Merchant account payout"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Chargebacks”, “Expected Settlement Date”, “Date”, “Sep 04AED 980K”, “Sep 06AED 760K”, “Refund”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 149 §Forecast"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconciliation simulator forecast list.",
   "error": "Could not load. Names which read failed and leaves the reconciliation simulator forecast untouched.",
   "emptyFirstRun": "No reconciliation simulator forecast yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reconciliation simulator forecast are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getUnifiedReconciliation",
    "contract": "finance",
    "purpose": "Forecast and trend",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Expected settlement",
    "Expected cash receipt",
    "Provider fees",
    "Refund deductions",
    "Chargeback deductions",
    "Currency conversion"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-628",
   "workshopBoard": "wireframes/WS93 Payment Payment Orchestration Board 7.dc.html#adm-628"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 149. 0 of 7 labels bound to a contract property; 18 of 179 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getPaymentProviderEconomics": {
  "method": "GET",
  "path": "/payment-providers/economics",
  "contract": "payments",
  "summary": "What each provider actually costs",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
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
  "responds": "ProviderEconomics"
 },
 "getUnifiedReconciliation": {
  "method": "GET",
  "path": "/reconciliation/unified",
  "contract": "finance",
  "summary": "Every money source against the ledger, in one view",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "UnifiedReconciliation"
 },
 "ingestSettlementFile": {
  "method": "POST",
  "path": "/settlements",
  "contract": "finance",
  "summary": "Ingest a provider settlement file",
  "permission": "SETTLEMENT_RECONCILE",
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
 "listMerchantAccounts": {
  "method": "GET",
  "path": "/merchant-accounts",
  "contract": "payments",
  "summary": "Merchant accounts, settlement calendars and payout routing",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MerchantAccount"
 },
 "listReconciliationSources": {
  "method": "GET",
  "path": "/reconciliation-sources",
  "contract": "payments",
  "summary": "The files and feeds reconciliation is run against",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ReconciliationSource"
 },
 "listSettlementExceptions": {
  "method": "GET",
  "path": "/settlements/{settlementId}/exceptions",
  "contract": "finance",
  "summary": "Unmatched or mismatched settlement lines",
  "permission": "SETTLEMENT_VIEW",
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
 "recordSettlement": {
  "method": "POST",
  "path": "/inter-entity-obligations/{obligationId}/settle",
  "contract": "finance",
  "summary": "One entity paid another",
  "permission": "LEDGER_POST",
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
  "requestBody": null,
  "responds": "InterEntityObligation"
 },
 "resolveSettlementException": {
  "method": "POST",
  "path": "/settlements/{settlementId}/exceptions",
  "contract": "finance",
  "summary": "Resolve a settlement exception",
  "permission": "SETTLEMENT_RECONCILE",
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
  "responds": "SettlementException"
 },
 "setMerchantAccount": {
  "method": "PUT",
  "path": "/merchant-accounts",
  "contract": "payments",
  "summary": "Bind a merchant account to entities, venues and a calendar",
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
  "requestBody": "MerchantAccount",
  "responds": "MerchantAccount"
 },
 "setReconciliationMatchingRules": {
  "method": "PUT",
  "path": "/reconciliation-rules",
  "contract": "payments",
  "summary": "How a platform transaction is matched to a settled one",
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
  "requestBody": "ReconciliationMatchingRules",
  "responds": "ReconciliationMatchingRules"
 },
 "setReconciliationSource": {
  "method": "PUT",
  "path": "/reconciliation-sources",
  "contract": "payments",
  "summary": "Define a settlement or statement feed",
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
  "requestBody": "ReconciliationSource",
  "responds": "ReconciliationSource"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "FxRateValue": {
  "x-ticvai-persistence-column": "numeric(18,6)",
  "type": "string",
  "pattern": "^\\d+(\\.\\d{1,6})?$",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"
 },
 "InterEntityObligation": {
  "type": "object",
  "x-ticvai-persistence": "ledger.inter_entity_obligation",
  "required": [
   "id",
   "fromLegalEntityId",
   "toLegalEntityId",
   "arisingAmount",
   "arisingAt",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Server-created when the obligation arises, so a UUID, as the `obligationId` path parameter types it."
   },
   "fromLegalEntityId": {
    "type": "string",
    "format": "uuid",
    "description": "The selling entity. Holds the liability, and therefore the FX exposure."
   },
   "toLegalEntityId": {
    "type": "string",
    "format": "uuid",
    "description": "The consuming entity, which provided the service at redemption."
   },
   "entitlementId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "arisingAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "In the **consuming** entity's base currency, at the rate in force on the redemption date. Neither entity ever holds a balance in a currency that is not its own.\n"
   },
   "rateApplied": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FxRateValue"
     }
    ]
   },
   "arisingAt": {
    "type": "string",
    "format": "date-time",
    "description": "Redemption. Not sale — the obligation exists when the service is given."
   },
   "status": {
    "type": "string",
    "enum": [
     "outstanding",
     "settled",
     "disputed"
    ]
   },
   "settledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "settlementRate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FxRateValue"
     }
    ],
    "nullable": true
   },
   "fxMovement": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Rate movement between arising and settling. Posts to FX gain and loss on the selling entity, which carried the balance.\n"
   }
  }
 },
 "MerchantAccount": {
  "type": "object",
  "x-ticvai-persistence": "payments.merchant_account",
  "description": "Board 7.7. **Which legal entity gets the money, and when.**",
  "required": [
   "code"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018). Region-scoped and not overridable below it, so a row in a UAE region is AED and cannot be anything else. Kept on the wire, removed from the table.\n"
   },
   "settlementCalendar": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     "custom"
    ]
   },
   "settlementDelayDays": {
    "type": "integer",
    "default": 1
   },
   "bankAccountReference": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
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
 "ProviderEconomics": {
  "type": "object",
  "description": "Board 2.9. **Cost per transaction is a routing input.**",
  "properties": {
   "connectionId": {
    "type": "string",
    "format": "uuid"
   },
   "providerName": {
    "type": "string"
   },
   "transactions": {
    "type": "integer"
   },
   "grossVolume": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "schemeFees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "interchange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "acquirerMargin": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "fxSpread": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "chargebackCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "effectiveRatePercent": {
    "type": "number"
   }
  }
 },
 "ReconciliationMatchingRules": {
  "type": "object",
  "x-ticvai-persistence": "payments.matching_rules",
  "description": "Board 7.3. **Exact matching was never enough.**",
  "properties": {
   "primaryKey": {
    "type": "string",
    "enum": [
     "providerReference",
     "platformReference",
     "authorisationCode",
     "retrievalReference"
    ]
   },
   "fallbackKeys": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "amountToleranceMinor": {
    "type": "integer",
    "default": 0
   },
   "dateWindowDays": {
    "type": "integer",
    "default": 2,
    "description": "**Acquirers batch across midnight.** A same-day-only match manufactures exceptions every night.\n"
   },
   "netOfFees": {
    "type": "boolean",
    "default": true
   },
   "autoResolveBelowMinor": {
    "type": "integer",
    "default": 0,
    "description": "**Rounding differences of a fil are not worth a person.** Above this they are."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ReconciliationSource": {
  "type": "object",
  "x-ticvai-persistence": "payments.reconciliation_source",
  "description": "Board 7.2. **A file that did not arrive looks like a day with no settlements.**",
  "required": [
   "code"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "connectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "transport": {
    "type": "string",
    "enum": [
     "sftp",
     "api",
     "email",
     "manualUpload"
    ]
   },
   "format": {
    "type": "string",
    "enum": [
     "csv",
     "fixedWidth",
     "json",
     "xml",
     "camt053"
    ]
   },
   "expectedSchedule": {
    "type": "string",
    "nullable": true,
    "default": "daily",
    "description": "How often a file is expected. **Daily by default, one per venue per trading day** (decided 28 September, audit R110 (b)), because settlement is reconciled daily per venue (`finance.ingestSettlementFile`)."
   },
   "expectedByTime": {
    "type": "string",
    "nullable": true
   },
   "alertIfMissing": {
    "type": "boolean",
    "default": true
   },
   "fieldMapping": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "Settlement": {
  "x-ticvai-persistence": "ledger.settlement",
  "type": "object",
  "required": [
   "id",
   "providerName",
   "periodStart",
   "periodEnd",
   "status",
   "ingestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"
   },
   "providerName": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."
   },
   "periodStart": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "periodEnd": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "fileReference": {
    "type": "string",
    "format": "uuid",
    "description": "The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"
   },
   "format": {
    "type": "string",
    "nullable": true,
    "enum": [
     "csv",
     "fixedWidth",
     "xml",
     "json"
    ],
    "description": "The file format given at ingest. Null when none was given."
   },
   "status": {
    "$ref": "#/components/schemas/SettlementStatus"
   },
   "lineCount": {
    "type": "integer"
   },
   "matchedCount": {
    "type": "integer"
   },
   "exceptionCount": {
    "type": "integer"
   },
   "providerGross": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providerFees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providerNet": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "ledgerGross": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "ingestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"
   }
  }
 },
 "SettlementException": {
  "x-ticvai-persistence": "ledger.settlement_exception",
  "type": "object",
  "required": [
   "id",
   "settlementId",
   "kind",
   "providerReference",
   "amount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Server-created when parsing finds the exception, so a UUID (naming-and-style 4)."
   },
   "settlementId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "unmatchedInProvider",
     "unmatchedInLedger",
     "amountMismatch",
     "duplicateInProvider",
     "feeUnexplained"
    ]
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "paymentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "expectedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "resolution": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SettlementResolution"
     }
    ],
    "nullable": true,
    "description": "Null while the exception is open."
   },
   "note": {
    "type": "string",
    "nullable": true,
    "description": "The `note` given to `resolveSettlementException`, stored with the resolution."
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "SettlementResolution": {
  "type": "string",
  "description": "How a settlement exception was explained. One vocabulary for the request and the stored exception.",
  "enum": [
   "matchedManually",
   "writeOff",
   "disputeRaised",
   "providerError",
   "timingDifference"
  ]
 },
 "SettlementStatus": {
  "type": "string",
  "enum": [
   "ingesting",
   "parsing",
   "matching",
   "matched",
   "hasExceptions",
   "resolved",
   "failed"
  ]
 },
 "UnifiedReconciliation": {
  "type": "object",
  "description": "4.2.19. **Four sources and the variances between them.** A view showing each balanced against itself has not reconciled anything.\n",
  "properties": {
   "from": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "to": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "pos",
        "gateway",
        "bank",
        "wallet",
        "ledger"
       ]
      },
      "providerName": {
       "type": "string",
       "nullable": true
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "transactionCount": {
       "type": "integer"
      }
     }
    }
   },
   "variances": {
    "type": "array",
    "description": "**Where two sources disagree, named.** A discrepancy is usually the gap between two of them rather than inside one, and *\"out by 240\"* without saying between what is not actionable.\n",
    "items": {
     "type": "object",
     "properties": {
      "between": {
       "type": "array",
       "description": "The two sources that disagree, as named in `sources[].source`.",
       "minItems": 2,
       "maxItems": 2,
       "items": {
        "type": "string",
        "enum": [
         "pos",
         "gateway",
         "bank",
         "wallet",
         "ledger"
        ]
       }
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "likelyCause": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 }
}
```
