# WS154 — Payment Payment Orchestration board 8

**10 screens · 23 operations · 22 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `AI_CONFIGURE, ORDER_MODIFY, ORDER_REFUND_APPROVE, ORDER_VIEW, PAYMENT_CONFIGURE, PAYMENT_DISPUTE, PAYMENT_VIEW, RISK_INVESTIGATE, RISK_REVIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-629` | Payment Risk & Fraud Command Center\t166 | commandCentre | 1 | 0 | — |
| `ADM-630` | Payment Risk Rule & Decision Engine\t167 | listDetail | 3 | 0 | — |
| `ADM-631` | Velocity, Behavioral & Transaction Risk Controls\t168 | listDetail | 1 | 0 | — |
| `ADM-632` | Risk Lists, Signals & Payment Control Center\t169 | listDetail | 1 | 0 | — |
| `ADM-633` | Fraud Alert, Investigation & Case Management\t170 | listDetail | 12 | 0 | — |
| `ADM-634` | Chargeback & Dispute Command Center\t172 | commandCentre | 7 | 0 | — |
| `ADM-635` | Chargeback Evidence & Representment Workspace\t173 | listDetail | 1 | 0 | — |
| `ADM-636` | Payment Performance & Conversion Analytics\t174 | configEditor | 1 | 0 | — |
| `ADM-637` | AI Fraud, Anomaly & Payment Intelligence Center\t175 | listDetail | 6 | 0 | — |
| `ADM-638` | Payment Executive Intelligence, Risk Simulator & AI Advisor\t176 | commandCentre | 2 | 0 | — |

## Thin screens in this batch

**ADM-633, ADM-635, ADM-636 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-629",
  "name": "Payment Risk & Fraud Command Center\\t166",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "1",
   "page": 165
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-risk-fraud-command-center-t166-adm-629",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentRiskFraudCommandCenterT166.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-630",
    "ADM-631",
    "ADM-632",
    "ADM-633",
    "ADM-634",
    "ADM-635",
    "ADM-636",
    "ADM-637",
    "ADM-638"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-630",
     "trigger": "Payment Risk Rule & Decision Engine\\t167",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-631",
     "trigger": "Velocity, Behavioral & Transaction Risk Controls\\t168",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-632",
     "trigger": "Risk Lists, Signals & Payment Control Center\\t169",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-633",
     "trigger": "Fraud Alert, Investigation & Case Management\\t170",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-634",
     "trigger": "Chargeback & Dispute Command Center\\t172",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-635",
     "trigger": "Chargeback Evidence & Representment Workspace\\t173",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-636",
     "trigger": "Payment Performance & Conversion Analytics\\t174",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-637",
     "trigger": "AI Fraud, Anomaly & Payment Intelligence Center\\t175",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-638",
     "trigger": "Payment Executive Intelligence, Risk Simulator & AI Advisor\\t176",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show; Analyze) — counts over a population, then the population",
  "purpose": "Provide real-time operational visibility over fraud, suspicious transactions, payment risk and chargebacks across the TICVAI ecosystem.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 165 §Show"
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
       "label": "Payment Attempts",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Approved Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Declined Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Risk-Blocked Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Risk-Review Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Suspected Fraud Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Confirmed Fraud Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Chargebacks",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Chargeback Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Chargeback Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Open Disputes",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "High-Risk Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every payment risk fraud",
       "columns": [
        "Low Risk",
        "Medium Risk",
        "High Risk",
        "Critical Risk",
        "Fraud attempts",
        "Blocked fraud",
        "Confirmed fraud",
        "Chargebacks",
        "False positives"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment risk fraud",
       "bindsTo": null,
       "columns": [
        "Low Risk",
        "Medium Risk",
        "High Risk",
        "Critical Risk",
        "Fraud attempts",
        "Blocked fraud",
        "Confirmed fraud",
        "Chargebacks",
        "False positives"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Breakdown”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 165 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment risk fraud list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the payment risk fraud untouched.",
   "emptyFirstRun": "No payment risk fraud yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment risk fraud are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getPaymentPerformance",
    "contract": "payments",
    "purpose": "Risk and fraud at a glance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-629",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-629"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 165. 0 of 9 labels bound to a contract property; 21 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-630",
  "name": "Payment Risk Rule & Decision Engine\\t167",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "2",
   "page": 166
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-risk-rule-decision-engine-t167-adm-630",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentRiskRuleDecisionEngineT167.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to configure deterministic payment risk rules and actions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Allow, Monitor, Require additional verification, Route to manual review, Block, Trigger alert. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 166 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 166"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 166"
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
       "label": "Allow",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 166 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Monitor",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 166 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Require additional verification",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 166 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Route to manual review",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 166 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Block",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 166 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Trigger alert",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 166 §Support"
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
   "loading": "The payment risk rule list.",
   "error": "Could not load. Names which read failed and leaves the payment risk rule untouched.",
   "emptyFirstRun": "No payment risk rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment risk rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPaymentRiskRules",
    "contract": "payments",
    "purpose": "Rules and decisions",
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-630",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-630"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 166. 0 of 0 labels bound to a contract property; 6 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-631",
  "name": "Velocity, Behavioral & Transaction Risk Controls\\t168",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "3",
   "page": 167
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/velocity-behavioral-transaction-risk-controls-t168-adm-631",
   "component": "apps/ticvai-web/src/routes/commercial/VelocityBehavioralTransactionRiskControlsT168.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage high-frequency and abnormal payment activity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Customer, Device, Payment instrument reference/token, Venue, POS. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 167 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 167"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 167"
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
       "label": "Customer",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 167 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Device",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 167 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment instrument reference/token",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 167 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 167 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "POS",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 167 §Support"
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
   "loading": "The velocity behavioral transaction list.",
   "error": "Could not load. Names which read failed and leaves the velocity behavioral transaction untouched.",
   "emptyFirstRun": "No velocity behavioral transaction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the velocity behavioral transaction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPaymentRiskRules",
    "contract": "payments",
    "purpose": "Velocity and behaviour",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-631",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-631"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 167. 0 of 0 labels bound to a contract property; 5 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-632",
  "name": "Risk Lists, Signals & Payment Control Center\\t169",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "4",
   "page": 168
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/risk-lists-signals-payment-control-center-t169-adm-632",
   "component": "apps/ticvai-web/src/routes/commercial/RiskListsSignalsPaymentControlCenterT169.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide centralized management of approved payment risk lists and signals.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Trusted device, Blocked instrument reference, High-risk device, Review list. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 168 §Support controlled lists such as"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 168"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 168"
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
       "label": "Trusted device",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 168 §Support controlled lists such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Blocked instrument reference",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 168 §Support controlled lists such as"
      },
      {
       "kind": "secondaryButton",
       "label": "High-risk device",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 168 §Support controlled lists such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Review list",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 168 §Support controlled lists such as"
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
   "loading": "The risk lists signals list.",
   "error": "Could not load. Names which read failed and leaves the risk lists signals untouched.",
   "emptyFirstRun": "No risk lists signals yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the risk lists signals are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPaymentRiskRules",
    "contract": "payments",
    "purpose": "Lists and signals",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-632",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-632"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 168. 0 of 0 labels bound to a contract property; 4 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-633",
  "name": "Fraud Alert, Investigation & Case Management\\t170",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "5",
   "page": 169
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/fraud-alert-investigation-case-management-t170-adm-633",
   "component": "apps/ticvai-web/src/routes/commercial/FraudAlertInvestigationCaseManagementT170.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Convert suspicious activity into controlled investigation cases.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 169 §Display"
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
       "label": "Every fraud alert investigation",
       "columns": [
        "Case ID",
        "Risk level",
        "Customer",
        "Transaction",
        "Order",
        "Payment method",
        "Provider",
        "Amount",
        "Currency",
        "Device",
        "Channel",
        "Risk score",
        "Rules triggered",
        "AI signals",
        "Related transactions",
        "Previous transactions",
        "Failed payments",
        "Refunds",
        "Chargebacks",
        "Devices",
        "Payment instruments",
        "Customer accounts"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 169 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected fraud alert investigation",
       "bindsTo": null,
       "columns": [
        "Case ID",
        "Risk level",
        "Customer",
        "Transaction",
        "Order",
        "Payment method",
        "Provider",
        "Amount",
        "Currency",
        "Device",
        "Channel",
        "Risk score",
        "Rules triggered",
        "AI signals",
        "Related transactions",
        "Previous transactions",
        "Failed payments",
        "Refunds",
        "Chargebacks",
        "Devices",
        "Payment instruments",
        "Customer accounts"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Detected”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 169 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Add note, Link transactions, Link customers/accounts, Request additional review, Mark confirmed fraud, Mark legitimate, Add risk-list entry, Escalate, Close case. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 169 §Authorized users may"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fraud alert investigation list.",
   "error": "Could not load. Names which read failed and leaves the fraud alert investigation untouched.",
   "emptyFirstRun": "No fraud alert investigation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the fraud alert investigation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChargebacks",
    "contract": "orders",
    "purpose": "Cases to investigate",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getEntityRisk",
    "contract": "ai",
    "purpose": "Current risk of an entity",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listRiskAlerts",
    "contract": "ai",
    "purpose": "Risk alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideRiskAlert",
    "contract": "ai",
    "purpose": "Dismiss, monitor, mark false positive, or escalate",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "createRiskCase",
    "contract": "ai",
    "purpose": "Open an investigation",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getRiskCase",
    "contract": "ai",
    "purpose": "A case with its evidence and actions",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "addRiskCaseEvidence",
    "contract": "ai",
    "purpose": "Add evidence to a case",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "expandRiskNetwork",
    "contract": "ai",
    "purpose": "Expand the relationship graph around an entity",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "proposeRiskAction",
    "contract": "ai",
    "purpose": "Propose a restrictive action from a case",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "closeRiskCase",
    "contract": "ai",
    "purpose": "Close a case with an outcome",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "assignChargeback",
    "contract": "orders",
    "purpose": "Assign a chargeback to an investigator",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getChargebackAnalytics",
    "contract": "orders",
    "purpose": "Customers with repeated chargebacks (groupBy=customer, minChargebacks)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Case ID",
    "Risk level",
    "Customer",
    "Transaction",
    "Order",
    "Payment method"
   ],
   "params": [
    {
     "name": "alertId",
     "from": "navigation"
    },
    {
     "name": "caseId",
     "from": "navigation"
    },
    {
     "name": "chargebackId",
     "from": "navigation"
    },
    {
     "name": "entityRef",
     "from": "navigation"
    },
    {
     "name": "entityType",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-633",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-633"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 169. 0 of 22 labels bound to a contract property; 31 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-634",
  "name": "Chargeback & Dispute Command Center\\t172",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "6",
   "page": 171
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/chargeback-dispute-command-center-t172-adm-634",
   "component": "apps/ticvai-web/src/routes/commercial/ChargebackDisputeCommandCenterT172.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Display) — counts over a population, then the population",
  "purpose": "Provide centralized operational management for provider/acquirer chargebacks and payment disputes.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 171 §Display"
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
       "label": "New Chargebacks",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Open Chargebacks",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Chargeback Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Chargeback Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Response Due",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Won",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Lost",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Accepted",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Represented",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Recovery Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every chargeback dispute \\t172",
       "columns": [
        "Chargeback ID",
        "Original Payment",
        "Order",
        "Customer",
        "Provider",
        "Acquirer",
        "Merchant account",
        "Amount",
        "Currency",
        "Reason code",
        "Received date",
        "Response deadline",
        "Status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected chargeback dispute \\t172",
       "bindsTo": null,
       "columns": [
        "Chargeback ID",
        "Original Payment",
        "Order",
        "Customer",
        "Provider",
        "Acquirer",
        "Merchant account",
        "Amount",
        "Currency",
        "Reason code",
        "Received date",
        "Response deadline",
        "Status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Important”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 171 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The chargeback dispute \\t172 list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the chargeback dispute \\t172 untouched.",
   "emptyFirstRun": "No chargeback dispute \\t172 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the chargeback dispute \\t172 are still there. The pack's own statuses are Received — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChargebacks",
    "contract": "orders",
    "purpose": "Chargebacks and disputes",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "respondToChargeback",
    "contract": "orders",
    "purpose": "Respond",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "recordChargeback",
    "contract": "orders",
    "purpose": "Record a chargeback read from an acquirer portal",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "assignChargeback",
    "contract": "orders",
    "purpose": "Assign a chargeback to an investigator",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordChargebackOutcome",
    "contract": "orders",
    "purpose": "Record the bank decision on a chargeback",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getChargebackAnalytics",
    "contract": "orders",
    "purpose": "Chargeback analytics panel",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getChargebackAnalytics",
    "contract": "orders",
    "purpose": "Chargeback analytics, groupBy product/customer",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-634",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-634"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 171. 0 of 13 labels bound to a contract property; 33 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "chargebackId",
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
  "id": "ADM-635",
  "name": "Chargeback Evidence & Representment Workspace\\t173",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "7",
   "page": 172
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/chargeback-evidence-representment-workspace-t173-adm-635",
   "component": "apps/ticvai-web/src/routes/commercial/ChargebackEvidenceRepresentmentWorkspaceT173.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Help Payment Operations collect, review and submit the evidence needed to respond to disputes. This is particularly important for TICVAI because ticketing transactions generate strong operational evidence.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 172"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 172"
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
       "impliedBy": "submitChargebackEvidence",
       "label": "Submit chargeback evidence",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "submitChargebackEvidence"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The chargeback evidence representment list.",
   "error": "Could not load. Names which read failed and leaves the chargeback evidence representment untouched.",
   "emptyFirstRun": "No chargeback evidence representment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the chargeback evidence representment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "submitChargebackEvidence",
    "contract": "payments",
    "purpose": "Assemble a representment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listChargebacks"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-635",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-635"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 172. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "chargebackId",
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
  "id": "ADM-636",
  "name": "Payment Performance & Conversion Analytics\\t174",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "8",
   "page": 173
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-performance-conversion-analytics-t174-adm-636",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentPerformanceConversionAnalyticsT174.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Captured) and no display directory — it is settings, not a population",
  "purpose": "Provide comprehensive analytics across the complete Payment & Payment Orchestration module. This screen is not only fraud analytics. It provides payment-business performance intelligence.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search payment performance conversion",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 173 §Analyze By"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Provider",
        "Acquirer",
        "Payment method",
        "Card scheme",
        "Digital wallet",
        "Venue",
        "Channel",
        "Merchant account",
        "Currency",
        "Country/market",
        "Device/terminal type"
       ],
       "notes": "The pack filters this screen by provider, acquirer, payment method, card scheme, digital wallet, venue and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 173 §Analyze By"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "78%",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 173 §Captured"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment performance conversion configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the payment performance conversion untouched.",
   "emptyFirstRun": "No payment performance conversion configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoResults": "The filter narrowed it and the payment performance conversion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getPaymentPerformance",
    "contract": "payments",
    "purpose": "Conversion and where sales are lost",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-636",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-636"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 173. 0 of 11 labels bound to a contract property; 24 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-637",
  "name": "AI Fraud, Anomaly & Payment Intelligence Center\\t175",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "9",
   "page": 174
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-fraud-anomaly-payment-intelligence-center-t175-adm-637",
   "component": "apps/ticvai-web/src/routes/commercial/AiFraudAnomalyPaymentIntelligenceCenterT175.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide governed AI/ML capabilities for fraud detection and payment anomaly identification.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 174"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 174"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getEntityRisk",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "configureRiskStrategy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listRiskAlerts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "configureRiskStrategy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fraud anomaly payment list.",
   "error": "Could not load. Names which read failed and leaves the fraud anomaly payment untouched.",
   "emptyFirstRun": "No fraud anomaly payment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the fraud anomaly payment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getPaymentPerformance",
    "contract": "payments",
    "purpose": "Anomalies in payment behaviour",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getEntityRisk",
    "contract": "ai",
    "purpose": "Current risk of an entity",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "configureRiskStrategy",
    "contract": "ai",
    "purpose": "Set the risk strategy",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listRiskAlerts",
    "contract": "ai",
    "purpose": "Risk alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getChargebackAnalytics",
    "contract": "orders",
    "purpose": "Chargeback analytics panel",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getChargebackAnalytics",
    "contract": "orders",
    "purpose": "Chargeback trend beside payment risk",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-637",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-637"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 174. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "entityRef",
     "from": "navigation"
    },
    {
     "name": "entityType",
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
  "id": "ADM-638",
  "name": "Payment Executive Intelligence, Risk Simulator & AI Advisor\\t176",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "8",
   "number": "10",
   "page": 175
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-executive-intelligence-risk-simulator-ai-advisor-adm-638",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentExecutiveIntelligenceRiskSimulatorAiAdvis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-629"
   ],
   "exitTo": [
    "ADM-629"
   ],
   "transitions": [
    {
     "to": "ADM-629",
     "trigger": "Back to Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Show; Monitor) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide executive-level intelligence and a safe simulation environment for payment, fraud and risk strategies.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Payment Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Payment Success Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Authorization Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Payment Cost",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Refund Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Fraud Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Chargeback Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Settlement Accuracy",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Provider Performance",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Payment Conversion",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Show"
      },
      {
       "kind": "metricTile",
       "label": "↓",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 175 §Monitor"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment executive intelligence list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the payment executive intelligence untouched.",
   "emptyFirstRun": "No payment executive intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment executive intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulatePaymentConfiguration",
    "contract": "payments",
    "purpose": "Executive simulation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "backtestRiskStrategy",
    "contract": "ai",
    "purpose": "Backtest a draft strategy",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-638",
   "workshopBoard": "wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-638"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 175. 0 of 0 labels bound to a contract property; 11 of 117 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "addRiskCaseEvidence": {
  "method": "POST",
  "path": "/risk/cases/{caseId}/evidence",
  "contract": "ai",
  "summary": "Add evidence to a case",
  "permission": "RISK_INVESTIGATE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AiRiskCaseEvidence",
  "responds": "AiRiskCaseEvidence"
 },
 "assignChargeback": {
  "method": "POST",
  "path": "/chargebacks/{chargebackId}/assign",
  "contract": "orders",
  "summary": "Give a chargeback to an investigator, with a note",
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
  "responds": "Chargeback"
 },
 "backtestRiskStrategy": {
  "method": "POST",
  "path": "/risk/strategy/backtest",
  "contract": "ai",
  "summary": "Backtest a draft strategy",
  "permission": "AI_CONFIGURE",
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
  "responds": "AiRiskBacktest"
 },
 "closeRiskCase": {
  "method": "POST",
  "path": "/risk/cases/{caseId}/close",
  "contract": "ai",
  "summary": "Close a case with an outcome",
  "permission": "RISK_INVESTIGATE",
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
  "responds": "AiRiskCase"
 },
 "configureRiskStrategy": {
  "method": "PUT",
  "path": "/risk/strategy",
  "contract": "ai",
  "summary": "Set the risk strategy",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "AiRiskStrategy",
  "responds": "AiRiskStrategy"
 },
 "createRiskCase": {
  "method": "POST",
  "path": "/risk/cases",
  "contract": "ai",
  "summary": "Open an investigation",
  "permission": "RISK_INVESTIGATE",
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
  "responds": "AiRiskCase"
 },
 "decideRiskAlert": {
  "method": "POST",
  "path": "/risk/alerts/{alertId}/decide",
  "contract": "ai",
  "summary": "Dismiss, monitor, mark false positive, or escalate",
  "permission": "RISK_REVIEW",
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
  "responds": "AiRiskAlert"
 },
 "expandRiskNetwork": {
  "method": "GET",
  "path": "/risk/network",
  "contract": "ai",
  "summary": "Expand the relationship graph around an entity",
  "permission": "RISK_INVESTIGATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "entityType",
    "in": "query",
    "required": true
   },
   {
    "name": "entityRef",
    "in": "query",
    "required": true
   },
   {
    "name": "hops",
    "in": "query",
    "required": null
   },
   {
    "name": "maxNodes",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiRiskNetwork"
 },
 "getChargebackAnalytics": {
  "method": "GET",
  "path": "/chargebacks/analytics",
  "contract": "orders",
  "summary": "Chargeback rate, win and loss, by reason, provider, outcome and period",
  "permission": "ORDER_REFUND_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "periodFrom",
    "in": "query",
    "required": true
   },
   {
    "name": "periodTo",
    "in": "query",
    "required": true
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   },
   {
    "name": "minChargebacks",
    "in": "query",
    "required": null
   },
   {
    "name": "productId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "providerId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OrdChargebackAnalytics"
 },
 "getEntityRisk": {
  "method": "GET",
  "path": "/risk/entities/{entityType}/{entityRef}",
  "contract": "ai",
  "summary": "Current risk of an entity",
  "permission": "RISK_REVIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AiEntityRisk"
 },
 "getPaymentPerformance": {
  "method": "GET",
  "path": "/payment-performance",
  "contract": "payments",
  "summary": "Authorisation rate, conversion and where payments are lost",
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
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PaymentPerformanceRow"
 },
 "getRiskCase": {
  "method": "GET",
  "path": "/risk/cases/{caseId}",
  "contract": "ai",
  "summary": "A case with its evidence and actions",
  "permission": "RISK_INVESTIGATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiRiskCaseDetail"
 },
 "listChargebacks": {
  "method": "GET",
  "path": "/chargebacks",
  "contract": "orders",
  "summary": "Open disputes, by deadline",
  "permission": "ORDER_REFUND_APPROVE",
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
  "requestBody": null,
  "responds": "Page"
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
 "listRiskAlerts": {
  "method": "GET",
  "path": "/risk/alerts",
  "contract": "ai",
  "summary": "Risk alerts",
  "permission": "RISK_REVIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "band",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "entityType",
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
 "proposeRiskAction": {
  "method": "POST",
  "path": "/risk/cases/{caseId}/actions",
  "contract": "ai",
  "summary": "Propose a restrictive action from a case",
  "permission": "RISK_INVESTIGATE",
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
  "responds": "AiRiskCaseAction"
 },
 "recordChargeback": {
  "method": "POST",
  "path": "/chargebacks/intake",
  "contract": "orders",
  "summary": "Take in a chargeback notified by a provider",
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
  "responds": "Chargeback"
 },
 "recordChargebackOutcome": {
  "method": "POST",
  "path": "/chargebacks/{chargebackId}/outcome",
  "contract": "orders",
  "summary": "Record the bank's decision and adjust the ledger",
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
  "responds": "Chargeback"
 },
 "respondToChargeback": {
  "method": "POST",
  "path": "/chargebacks/{chargebackId}/respond",
  "contract": "orders",
  "summary": "Submit evidence, or accept the loss",
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
  "responds": "Chargeback"
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
 "setPaymentRiskRules": {
  "method": "PUT",
  "path": "/payment-risk-rules",
  "contract": "payments",
  "summary": "Velocity, behaviour, lists and what a hit does",
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
  "requestBody": "PaymentRiskRules",
  "responds": "PaymentRiskRules"
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
 },
 "submitChargebackEvidence": {
  "method": "POST",
  "path": "/chargebacks/{chargebackId}/evidence",
  "contract": "payments",
  "summary": "Assemble and send a representment",
  "permission": "PAYMENT_DISPUTE",
  "offlineCapable": null,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ChargebackEvidence",
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiEntityRisk": {
  "type": "object",
  "x-ticvai-persistence": "ai.entity_risk",
  "description": "**Current risk per entity** (design 5.3, AIP-128): customer, account, device, payment token, credential, cluster or staff member, computed asynchronously from composite signals — no single signal decides (M21).",
  "required": [
   "entityType",
   "entityRef",
   "score",
   "band"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "entityType": {
    "type": "string",
    "enum": [
     "customer",
     "account",
     "device",
     "paymentToken",
     "credential",
     "cluster",
     "staff",
     "ipAddress"
    ]
   },
   "entityRef": {
    "type": "string",
    "description": "The entity id, or a hashed device id, hashed IP address or provider token reference. Never a card number or a raw IP address."
   },
   "score": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100
   },
   "band": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Design 5.6: a risk score and band, never a probability."
   },
   "signals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Contributing signals with their weights and freshness. Since 29 September (build) they include chargeback count and rate (`order.chargebackRecorded`), password resets (`identity.credentialResetRequested`), IP velocity and country mismatch, and storefront browsing features (`storefront.sessionEvent`)."
   },
   "lastEventAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRiskAlert": {
  "type": "object",
  "x-ticvai-persistence": "ai.risk_alert",
  "description": "**A risk alert** (AIP-109): raised by scoring or re-scoring. **Alert, case and confirmed fraud are kept distinct** (AIP-163): an alert is a signal to look, not a finding.",
  "required": [
   "kind",
   "entityType",
   "entityRef",
   "band",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "transaction",
     "velocity",
     "entity",
     "network",
     "staffLeakage",
     "scanAbuse",
     "accountTakeover",
     "chargeback"
    ]
   },
   "entityType": {
    "type": "string",
    "enum": [
     "customer",
     "account",
     "device",
     "paymentToken",
     "credential",
     "cluster",
     "staff",
     "wallet",
     "ipAddress"
    ]
   },
   "entityRef": {
    "type": "string"
   },
   "score": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100
   },
   "band": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Design 5.6: a risk score and band, never a probability."
   },
   "reasonCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "correlationKey": {
    "type": "string",
    "nullable": true
   },
   "assessmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "monitoring",
     "dismissed",
     "falsePositive",
     "escalated"
    ],
    "readOnly": true
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.risk_case"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "decisionNote": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRiskBacktest": {
  "type": "object",
  "x-ticvai-persistence": "none — computed over ai.risk_assessment and labelled outcomes",
  "description": "What a draft strategy would have done over a past window: review rate, recall and precision against analyst-labelled outcomes, and false-positive rate by segment (AIP-143).",
  "required": [
   "evaluated"
  ],
  "properties": {
   "evaluated": {
    "type": "integer"
   },
   "reviewRate": {
    "type": "number"
   },
   "recall": {
    "type": "number",
    "nullable": true
   },
   "precision": {
    "type": "number",
    "nullable": true
   },
   "bySegment": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "segment": {
       "type": "string",
       "enum": [
        "family",
        "b2b",
        "reseller",
        "member",
        "other"
       ]
      },
      "falsePositiveRate": {
       "type": "number"
      }
     }
    }
   },
   "outcomeCounts": {
    "type": "object",
    "additionalProperties": true
   }
  }
 },
 "AiRiskCase": {
  "type": "object",
  "x-ticvai-persistence": "ai.risk_case",
  "description": "**An investigation** (AIP-150..160). Its evidence and actions are `ai.case_evidence` and `ai.case_action`. The summary is written by a model from structured evidence only (AIP-153); the outcome is a person's.",
  "required": [
   "reference",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "reference": {
    "type": "string",
    "readOnly": true
   },
   "title": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "pendingAction",
     "closed"
    ],
    "readOnly": true
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "entities": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entityType": {
       "type": "string",
       "enum": [
        "customer",
        "account",
        "device",
        "paymentToken",
        "credential",
        "cluster",
        "staff"
       ]
      },
      "entityRef": {
       "type": "string"
      }
     }
    }
   },
   "alertIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "assigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal"
   },
   "summary": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "outcome": {
    "type": "string",
    "enum": [
     "confirmedFraud",
     "notFraud",
     "inconclusive"
    ],
    "nullable": true,
    "readOnly": true
   },
   "closureNote": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "openedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRiskCaseAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.case_action",
  "description": "**A restrictive action proposed from a case** (AIP-136). It goes to the owning module through the action pipeline, never straight from review; at the first-release ceiling (L1 advisory, design 3.8) it is a recommendation the owning module's operator applies. **Scoped through its case.**",
  "required": [
   "caseId",
   "action",
   "targetContract"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.risk_case"
   },
   "action": {
    "type": "string",
    "enum": [
     "blockPaymentToken",
     "suspendAccount",
     "restrictWallet",
     "revokeEntitlement",
     "flagCustomer",
     "requireStepUp",
     "holdRefunds",
     "lockIdentity"
    ]
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "targetRef": {
    "type": "string"
   },
   "rationale": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "recommended",
     "planned",
     "awaitingApproval",
     "applied",
     "rejected",
     "failed"
    ],
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan"
   },
   "proposedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AiRiskCaseDetail": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.risk_case with its evidence, actions and alerts",
  "description": "A case with everything attached to it.",
  "required": [
   "case"
  ],
  "properties": {
   "case": {
    "$ref": "#/components/schemas/AiRiskCase"
   },
   "evidence": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRiskCaseEvidence"
    }
   },
   "actions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRiskCaseAction"
    }
   },
   "alerts": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRiskAlert"
    }
   }
  }
 },
 "AiRiskCaseEvidence": {
  "type": "object",
  "x-ticvai-persistence": "ai.case_evidence",
  "description": "**Case evidence** (AIP-155): `jsonb` plus an immutable Blob copy. **Scoped through its case** (`platform.apply_parent_rls`). Never edited; a correction is new evidence.",
  "required": [
   "caseId",
   "kind",
   "label"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.risk_case"
   },
   "kind": {
    "type": "string",
    "enum": [
     "assessment",
     "alert",
     "transaction",
     "networkSnapshot",
     "note",
     "document"
    ]
   },
   "ref": {
    "type": "string",
    "nullable": true
   },
   "content": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "blobRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The immutable (WORM) copy."
   },
   "label": {
    "type": "string",
    "enum": [
     "source",
     "derived",
     "modelInferred"
    ]
   },
   "contentHash": {
    "type": "string",
    "readOnly": true
   },
   "addedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "addedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AiRiskEdge": {
  "type": "object",
  "x-ticvai-persistence": "ai.risk_edge",
  "description": "**A relationship-graph edge** (design 2.4, AIP-111): shared device, token or account, with strength. Queried 1 to 3 hops by `expandRiskNetwork`; no graph database.",
  "required": [
   "fromEntityType",
   "fromEntityRef",
   "toEntityType",
   "toEntityRef",
   "relation"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "fromEntityType": {
    "type": "string",
    "enum": [
     "customer",
     "account",
     "device",
     "paymentToken",
     "credential",
     "cluster",
     "staff",
     "ipAddress"
    ]
   },
   "fromEntityRef": {
    "type": "string"
   },
   "toEntityType": {
    "type": "string",
    "enum": [
     "customer",
     "account",
     "device",
     "paymentToken",
     "credential",
     "cluster",
     "staff",
     "ipAddress"
    ]
   },
   "toEntityRef": {
    "type": "string"
   },
   "relation": {
    "type": "string",
    "enum": [
     "sharedDevice",
     "sharedToken",
     "sharedAccount",
     "sharedContact",
     "sharedIp",
     "transfer",
     "companion",
     "staffCustomer"
    ]
   },
   "strength": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "firstSeenAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastSeenAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRiskNetwork": {
  "type": "object",
  "x-ticvai-persistence": "none — read from ai.risk_edge and ai.entity_risk",
  "description": "A bounded 1..3-hop neighbourhood of an entity (AIP-111).",
  "required": [
   "nodes",
   "edges"
  ],
  "properties": {
   "nodes": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiEntityRisk"
    }
   },
   "edges": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRiskEdge"
    }
   },
   "truncated": {
    "type": "boolean",
    "description": "The hop or node limit cut the result."
   }
  }
 },
 "AiRiskStrategy": {
  "type": "object",
  "x-ticvai-persistence": "ai.risk_strategy",
  "description": "**The tenant's risk strategy** (C10, AIP-096..165): weighted rule contributions, thresholds, modes and the map from band to outcome by channel and value (AIP-100). **Fail-open with holds, not declines, by default** (decided 29 September, decision 6): `decline` appears in `outcomeMap` only where the tenant governed it.",
  "required": [
   "version",
   "mode",
   "thresholds"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true
   },
   "mode": {
    "type": "string",
    "enum": [
     "monitor",
     "enforce"
    ],
    "description": "Monitor records outcomes without acting; how a new strategy earns trust."
   },
   "weights": {
    "type": "object",
    "additionalProperties": true,
    "description": "Contribution of each rule and signal to the composite 0..100 score."
   },
   "thresholds": {
    "type": "object",
    "properties": {
     "monitor": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "stepUp": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "holdForReview": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "decline": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "nullable": true
     }
    }
   },
   "outcomeMap": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "band": {
       "type": "string",
       "enum": [
        "low",
        "medium",
        "high",
        "critical"
       ]
      },
      "channel": {
       "type": "string",
       "nullable": true
      },
      "minAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "nullable": true
      },
      "outcome": {
       "type": "string",
       "enum": [
        "allow",
        "monitor",
        "stepUp",
        "holdForReview",
        "decline"
       ]
      }
     }
    }
   },
   "failMode": {
    "type": "string",
    "enum": [
     "open",
     "holdForReview"
    ],
    "default": "open",
    "description": "On timeout or AI down. Never a silent decline (AIP-110)."
   },
   "declineGoverned": {
    "type": "boolean",
    "default": false,
    "description": "Set only through `configureRiskStrategy` by `AI_APPROVE`; without it no `decline` outcome is accepted."
   },
   "modelEnabled": {
    "type": "boolean",
    "default": false,
    "readOnly": true,
    "description": "Adds the promoted model's score where one is promoted for this tenant (design 3.5)."
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "active",
     "superseded"
    ],
    "readOnly": true
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "Chargeback": {
  "type": "object",
  "x-ticvai-persistence": "orders.chargeback + orders.chargeback_evidence + orders.chargeback_investigation_log",
  "description": "BL-118, CF-144. **A chargeback is not a refund**, and treating it as one is how a venue loses them by default.\nA refund is a decision the venue makes. **A chargeback is a decision a bank makes, on a clock the venue does not control** — evidence is due in days, a deadline missed is a case lost regardless of merit, and there is a fee either way.\nThe money is already gone when this record is created. **Representment is an argument, not a reversal.**\n",
  "required": [
   "id",
   "paymentId",
   "amount",
   "reason",
   "status",
   "evidenceDueBy"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "paymentId": {
    "type": "string",
    "format": "uuid"
   },
   "providerId": {
    "type": "string",
    "format": "uuid"
   },
   "providerCaseReference": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "feeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "enum": [
     "fraudulent",
     "productNotReceived",
     "productUnacceptable",
     "duplicate",
     "subscriptionCancelled",
     "creditNotProcessed",
     "unrecognised",
     "other"
    ],
    "description": "**The scheme's reason code, mapped.** Which evidence wins depends entirely on it — a *product not received* case is answered by a scan record and a *fraudulent* case is not.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "received",
     "underReview",
     "evidenceSubmitted",
     "won",
     "lost",
     "accepted",
     "expired"
    ]
   },
   "evidenceDueBy": {
    "type": "string",
    "format": "date-time",
    "description": "**The field the whole record exists for.** A deadline missed is a case lost on merit nobody read, and it is the one date that must reach a person rather than a report.\n"
   },
   "evidenceSubmittedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "evidence": {
    "type": "array",
    "description": "**What the platform can prove**, assembled rather than typed: the order, the scan that admitted them, the delivery, the terms accepted, the IP and device. A venue answering a chargeback by hand is a venue answering it late.\nHeld as rows of `orders.chargeback_evidence`, one per item (29 September, build: a list of objects needs its own table to be stored at all).\n",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "order",
        "scanRecord",
        "deliveryProof",
        "termsAccepted",
        "communication",
        "deviceFingerprint",
        "other"
       ]
      },
      "reference": {
       "type": "string"
      }
     }
    }
   },
   "outcomeAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "schemeReasonCode": {
    "type": "string",
    "nullable": true,
    "description": "The card scheme's own reason code as notified, beside the mapped `reason` (5.7.92)."
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the provider notified the case; the date its debit posts to (`recordChargeback`)."
   },
   "assigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who is investigating (`assignChargeback`)."
   },
   "investigationLog": {
    "type": "array",
    "description": "Notes from `assignChargeback` and `recordChargebackOutcome`, oldest first, with who wrote each and when. Append-only. Held as rows of `orders.chargeback_investigation_log` (29 September, build).",
    "items": {
     "type": "object",
     "properties": {
      "note": {
       "type": "string"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "debitJournalEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `chargebackDebit` (and `chargebackFee`) entry posted at intake."
   },
   "outcomeJournalEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `chargebackReversal` entry posted when the case is won, or the additional fee when lost."
   }
  }
 },
 "ChargebackEvidence": {
  "type": "object",
  "x-ticvai-persistence": "payments.chargeback_evidence",
  "description": "Board 8.7. **The platform holds every document already.**",
  "required": [
   "chargebackId"
  ],
  "properties": {
   "chargebackId": {
    "type": "string",
    "format": "uuid"
   },
   "narrative": {
    "type": "string",
    "nullable": true
   },
   "documents": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "authorisationRecord",
        "receipt",
        "termsAccepted",
        "admissionScan",
        "deliveryProof",
        "communicationLog",
        "refundPolicy",
        "other"
       ]
      },
      "assetId": {
       "type": "string",
       "format": "uuid"
      },
      "autoAssembled": {
       "type": "boolean",
       "default": true
      }
     }
    }
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "deadlineAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "outcome": {
    "type": "string",
    "enum": [
     "pending",
     "won",
     "lost",
     "withdrawn"
    ],
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
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
 "OrdChargebackAnalytics": {
  "x-ticvai-persistence": "none — computed from orders.chargeback and orders.payment on the reporting replica",
  "type": "object",
  "description": "4.2.21. Chargeback measures for a period, in total and per group.",
  "required": [
   "periodFrom",
   "periodTo",
   "groupBy",
   "totals",
   "groups"
  ],
  "properties": {
   "periodFrom": {
    "type": "string",
    "format": "date"
   },
   "periodTo": {
    "type": "string",
    "format": "date"
   },
   "groupBy": {
    "type": "string"
   },
   "totals": {
    "$ref": "#/components/schemas/OrdChargebackMeasures"
   },
   "groups": {
    "type": "array",
    "items": {
     "allOf": [
      {
       "$ref": "#/components/schemas/OrdChargebackMeasures"
      },
      {
       "type": "object",
       "required": [
        "key"
       ],
       "properties": {
        "key": {
         "type": "string",
         "description": "The reason, provider id, outcome, venue id, month (`YYYY-MM`), product id, product category id, or guest `subjectId` (`anonymous` for purchases with no guest) of the group."
        },
        "label": {
         "type": "string",
         "nullable": true,
         "description": "The display name of the group's key. Null for `customer` unless the caller holds `GUEST_VIEW_PII`."
        }
       }
      }
     ]
    }
   }
  }
 },
 "OrdChargebackMeasures": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "properties": {
   "chargebackCount": {
    "type": "integer"
   },
   "chargebackAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "cardPaymentCount": {
    "type": "integer"
   },
   "chargebackRateByCount": {
    "type": "number",
    "description": "Chargebacks received per card payment captured in the period, as a fraction."
   },
   "chargebackRateByValue": {
    "type": "number"
   },
   "decidedCount": {
    "type": "integer"
   },
   "wonCount": {
    "type": "integer"
   },
   "lostCount": {
    "type": "integer"
   },
   "acceptedCount": {
    "type": "integer"
   },
   "expiredCount": {
    "type": "integer",
    "description": "Lost to a missed evidence deadline."
   },
   "winRate": {
    "type": "number",
    "nullable": true,
    "description": "Won over decided (won, lost, expired); null with none decided."
   },
   "recoveredAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "feeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "openCount": {
    "type": "integer"
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
 "PaymentPerformanceRow": {
  "type": "object",
  "description": "Board 8.8. **The last and most expensive place a venue loses a sale.**",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "attempts": {
    "type": "integer"
   },
   "authorised": {
    "type": "integer"
   },
   "declined": {
    "type": "integer"
   },
   "errored": {
    "type": "integer"
   },
   "abandoned": {
    "type": "integer"
   },
   "authorisationRate": {
    "type": "number"
   },
   "conversionRate": {
    "type": "number"
   },
   "averageValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "topDeclineReason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "PaymentRiskRules": {
  "type": "object",
  "x-ticvai-persistence": "payments.risk_rules",
  "description": "Boards 8.2 to 8.4. **Distinct from `wallet` risk** — this watches card presentation.\n",
  "properties": {
   "rules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "signal": {
       "type": "string",
       "enum": [
        "cardAcrossAccounts",
        "accountAcrossCards",
        "deviceAcrossCards",
        "velocityCount",
        "velocityAmount",
        "issuerCountryMismatch",
        "highRiskBin",
        "listHit",
        "repeatedDecline"
       ]
      },
      "threshold": {
       "type": "number",
       "nullable": true
      },
      "windowMinutes": {
       "type": "integer",
       "nullable": true
      },
      "listCode": {
       "type": "string",
       "nullable": true
      },
      "action": {
       "type": "string",
       "enum": [
        "scoreOnly",
        "challenge",
        "refuse",
        "allowAndFlag",
        "raiseCase"
       ]
      }
     }
    }
   },
   "lists": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "blockCard",
        "blockBin",
        "blockEmail",
        "blockDevice",
        "blockIp",
        "allowAlways"
       ],
       "description": "`blockIp` entries are IPv4 or IPv6 addresses or CIDR ranges (no wider than /16 for IPv4 or /32 for IPv6, so one entry cannot block a country's mobile network), matched at the edge (29 September, build pass; 8.3.8)."
      },
      "entries": {
       "type": "integer",
       "readOnly": true
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
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
