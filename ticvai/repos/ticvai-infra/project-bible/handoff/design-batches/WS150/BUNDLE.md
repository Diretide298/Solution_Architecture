# WS150 — Payment Payment Orchestration board 4

**10 screens · 10 operations · 15 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PAYMENT_CONFIGURE, PAYMENT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-589` | Digital Payments Command Center\t71 | commandCentre | 1 | 0 | — |
| `ADM-590` | Digital & Alternative Payment Method Manager\t71 | listDetail | 2 | 0 | — |
| `ADM-591` | Digital Wallet & Mobile Payment Configuration\t72 | listDetail | 1 | 0 | — |
| `ADM-592` | Payment Link Builder & Configuration\t73 | configEditor | 1 | 0 | — |
| `ADM-593` | Payment Link Distribution & Customer Journey Manager\t74 | listDetail | 2 | 0 | — |
| `ADM-594` | Hosted Checkout, Redirect & Return Flow Configuration\t75 | configEditor | 1 | 0 | — |
| `ADM-595` | Digital Payment Session & Transaction Monitor\t76 | listDetail | 1 | 0 | — |
| `ADM-596` | Authentication, Tokenization & Recurring Payment Controls\t78 | listDetail | 1 | 0 | — |
| `ADM-597` | Digital Payment Exception, Recovery & Expiry Center\t79 | listDetail | 2 | 0 | — |
| `ADM-598` | Digital Payment Simulator, Conversion & AI Advisor\t80 | configEditor | 1 | 0 | — |

## Thin screens in this batch

**ADM-591, ADM-597 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-589",
  "name": "Digital Payments Command Center\\t71",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "1",
   "page": 70
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/digital-payments-command-center-t71-adm-589",
   "component": "apps/ticvai-web/src/routes/commercial/DigitalPaymentsCommandCenterT71.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-590",
    "ADM-591",
    "ADM-592",
    "ADM-593",
    "ADM-594",
    "ADM-595",
    "ADM-596",
    "ADM-597",
    "ADM-598"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-590",
     "trigger": "Digital & Alternative Payment Method Manager\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-591",
     "trigger": "Digital Wallet & Mobile Payment Configuration\\t72",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-592",
     "trigger": "Payment Link Builder & Configuration\\t73",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-593",
     "trigger": "Payment Link Distribution & Customer Journey Manager\\t74",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-594",
     "trigger": "Hosted Checkout, Redirect & Return Flow Configuration\\t75",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-595",
     "trigger": "Digital Payment Session & Transaction Monitor\\t76",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-596",
     "trigger": "Authentication, Tokenization & Recurring Payment Controls\\t78",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-597",
     "trigger": "Digital Payment Exception, Recovery & Expiry Center\\t79",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-598",
     "trigger": "Digital Payment Simulator, Conversion & AI Advisor\\t80",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Compare) — counts over a population, then the population",
  "purpose": "Provide centralized operational visibility across all digital and alternative payment journeys.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 70 §Compare"
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
       "label": "Digital Payment Attempts",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Successful Payments",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Digital Payment Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Success Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Payment Links Generated",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Payment Links Paid",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Payment Link Conversion",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Wallet Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Alternative Payment Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Pending Payments",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Expired Payment Requests",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failed Digital Payments",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every digital payments \\t71",
       "columns": [
        "B2C",
        "Mobile App",
        "Call Center",
        "B2B",
        "POS Payment Link",
        "Partner/API"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected digital payments \\t71",
       "bindsTo": null,
       "columns": [
        "B2C",
        "Mobile App",
        "Call Center",
        "B2B",
        "POS Payment Link",
        "Partner/API"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Show by”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital payments \\t71 list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the digital payments \\t71 untouched.",
   "emptyFirstRun": "No digital payments \\t71 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital payments \\t71 are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getPaymentPerformance",
    "contract": "payments",
    "purpose": "Digital payment performance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-589",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-589"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 70. 0 of 6 labels bound to a contract property; 18 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-590",
  "name": "Digital & Alternative Payment Method Manager\\t71",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "2",
   "page": 70
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/digital-alternative-payment-method-manager-t71-adm-590",
   "component": "apps/ticvai-web/src/routes/commercial/DigitalAlternativePaymentMethodManagerT71.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the digital payment experiences available through TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Online card, Mobile/digital wallets, Redirect payments, Stored-value wallet, Future payment methods through adapters. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 70 §Support provider-enabled methods such as"
   },
   {
    "operation": null,
    "why": "**Digital & Alternative Payment Method Manager\\t71 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 70"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 70"
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
       "label": "Online card",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §Support provider-enabled methods such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Mobile/digital wallets",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §Support provider-enabled methods such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Redirect payments",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §Support provider-enabled methods such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Stored-value wallet",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §Support provider-enabled methods such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Future payment methods through adapters",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 70 §Support provider-enabled methods such as"
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
   "loading": "The digital alternative payment list.",
   "error": "Could not load. Names which read failed and leaves the digital alternative payment untouched.",
   "emptyFirstRun": "No digital alternative payment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital alternative payment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentMethods",
    "contract": "payments",
    "purpose": "Alternative methods",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updatePaymentMethod",
    "contract": "payments",
    "purpose": "Configure one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-590",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-590"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 70. 0 of 0 labels bound to a contract property; 5 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "methodId",
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
  "id": "ADM-591",
  "name": "Digital Wallet & Mobile Payment Configuration\\t72",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "3",
   "page": 71
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/digital-wallet-mobile-payment-configuration-t72-adm-591",
   "component": "apps/ticvai-web/src/routes/commercial/DigitalWalletMobilePaymentConfigurationT72.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage wallet-based and mobile digital payment methods.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 71"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 71"
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
       "impliedBy": "updatePaymentMethod",
       "label": "Save payment method",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updatePaymentMethod"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital wallet mobile list.",
   "error": "Could not load. Names which read failed and leaves the digital wallet mobile untouched.",
   "emptyFirstRun": "No digital wallet mobile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital wallet mobile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updatePaymentMethod",
    "contract": "payments",
    "purpose": "Digital wallet configuration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-591",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-591"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 71. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "methodId",
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
  "id": "ADM-592",
  "name": "Payment Link Builder & Configuration\\t73",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "4",
   "page": 72
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-link-builder-configuration-t73-adm-592",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentLinkBuilderConfigurationT73.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow authorized users and systems to generate secure payment requests without requiring the customer to be physically present at a POS.",
  "gaps": [
   {
    "operation": null,
    "why": "**Payment Link Builder & Configuration\\t73 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "kind": "textField",
       "label": "Order / transaction reference",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer reference",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Payment methods",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial payment policy",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Return destination",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business unit",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel/source",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 72 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment link \\t73 configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the payment link \\t73 untouched.",
   "emptyFirstRun": "No payment link \\t73 configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createPaymentLink",
    "contract": "orders",
    "purpose": "Build a payment link",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-592",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-592"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 72. 0 of 0 labels bound to a contract property; 13 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-593",
  "name": "Payment Link Distribution & Customer Journey Manager\\t74",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "5",
   "page": 73
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-link-distribution-customer-journey-manager-t74-adm-593",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentLinkDistributionCustomerJourneyManagerT74.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage how a generated payment request is delivered and how its lifecycle progresses.",
  "gaps": [
   {
    "operation": null,
    "why": "**Payment Link Distribution & Customer Journey Manager\\t74 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 73"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 73"
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
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Resend, Change approved delivery channel, Extend expiry, Cancel. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 73 §Authorized users can"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "resendPaymentLink",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getPaymentLink",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "resendPaymentLink"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment link distribution list.",
   "error": "Could not load. Names which read failed and leaves the payment link distribution untouched.",
   "emptyFirstRun": "No payment link distribution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment link distribution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "resendPaymentLink",
    "contract": "orders",
    "purpose": "Distribute or resend",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getPaymentLink",
    "contract": "orders",
    "purpose": "Its state",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-593",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-593"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 73. 0 of 0 labels bound to a contract property; 4 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "linkId",
     "from": "navigation"
    },
    {
     "name": "token",
     "from": "deepLink"
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
  "id": "ADM-594",
  "name": "Hosted Checkout, Redirect & Return Flow Configuration\\t75",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "6",
   "page": 74
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/hosted-checkout-redirect-return-flow-configuration-t75-adm-594",
   "component": "apps/ticvai-web/src/routes/commercial/HostedCheckoutRedirectReturnFlowConfigurationT75.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure digital payment flows that require provider-hosted payment pages, redirects, SDKs, or asynchronous customer journeys.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Hosted checkout, External payment authorization. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 74 §Support"
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
       "label": "Provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Success return",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Failure return",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cancel return",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Timeout",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Session expiry",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Callback",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Webhook",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed domains/apps",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Branding profile reference",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Hosted checkout",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "External payment authorization",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 74 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hosted checkout redirect configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the hosted checkout redirect untouched.",
   "emptyFirstRun": "No hosted checkout redirect configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setHostedCheckoutConfiguration",
    "contract": "payments",
    "purpose": "Redirect and return",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-594",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-594"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 74. 0 of 0 labels bound to a contract property; 12 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-595",
  "name": "Digital Payment Session & Transaction Monitor\\t76",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "7",
   "page": 75
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/digital-payment-session-transaction-monitor-t76-adm-595",
   "component": "apps/ticvai-web/src/routes/commercial/DigitalPaymentSessionTransactionMonitorT76.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide operational teams with real-time visibility into digital payment sessions.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 75 §Show"
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
       "label": "Search digital payment session",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 75 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Payment ID",
        "Order",
        "Payment link",
        "Customer reference",
        "Provider transaction",
        "Channel",
        "Payment method",
        "Amount",
        "Currency",
        "Status",
        "Date/time"
       ],
       "notes": "The pack filters this screen by payment id, order, payment link, customer reference, provider transaction, channel and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 75 §Search by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every digital payment session",
       "columns": [
        "TICVAI Payment ID",
        "Order ID",
        "Payment method",
        "Provider",
        "Gateway",
        "Amount",
        "Currency",
        "Created",
        "Session expiry",
        "Customer journey stage",
        "Provider status",
        "TICVAI status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 75 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected digital payment session",
       "bindsTo": null,
       "columns": [
        "TICVAI Payment ID",
        "Order ID",
        "Payment method",
        "Provider",
        "Gateway",
        "Amount",
        "Currency",
        "Created",
        "Session expiry",
        "Customer journey stage",
        "Provider status",
        "TICVAI status"
       ],
       "notes": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 75 §Show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Check Status, Cancel Session, Regenerate Link, View Provider Events, View Decision Trace. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 75 §Depending on permissions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital payment session list.",
   "error": "Could not load. Names which read failed and leaves the digital payment session untouched.",
   "emptyFirstRun": "No digital payment session yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital payment session are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "inquirePaymentStatus",
    "contract": "orders",
    "purpose": "Session and transaction state",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "TICVAI Payment ID",
    "Order ID",
    "Payment method",
    "Provider",
    "Gateway",
    "Amount"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-595",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-595"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 75. 0 of 23 labels bound to a contract property; 28 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-596",
  "name": "Authentication, Tokenization & Recurring Payment Controls\\t78",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "8",
   "page": 77
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/authentication-tokenization-recurring-payment-controls-t-adm-596",
   "component": "apps/ticvai-web/src/routes/commercial/AuthenticationTokenizationRecurringPaymentContro.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage digital-payment security capabilities and reusable payment references without turning TICVAI into a card vault.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: 3-D Secure, Strong Customer Authentication where applicable, Provider risk authentication. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 77 §Support provider capabilities such as"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 77 §Display"
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
       "label": "Every authentication tokenization recurring",
       "columns": [
        "Payment Instrument Reference",
        "Provider",
        "Token Status",
        "Masked Identifier where allowed",
        "Card/Instrument Type",
        "Expiry metadata where provided",
        "Customer/account relationship",
        "Created",
        "Last Used"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 77 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected authentication tokenization recurring",
       "bindsTo": null,
       "columns": [
        "Payment Instrument Reference",
        "Provider",
        "Token Status",
        "Masked Identifier where allowed",
        "Card/Instrument Type",
        "Expiry metadata where provided",
        "Customer/account relationship",
        "Created",
        "Last Used"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Tokenization”, “Token States”, “Consent / Mandate Reference”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 77 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "3-D Secure",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 77 §Support provider capabilities such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Strong Customer Authentication where applicable",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 77 §Support provider capabilities such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Provider risk authentication",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 77 §Support provider capabilities such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The authentication tokenization recurring list.",
   "error": "Could not load. Names which read failed and leaves the authentication tokenization recurring untouched.",
   "emptyFirstRun": "No authentication tokenization recurring yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the authentication tokenization recurring are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPaymentAuthenticationPolicy",
    "contract": "payments",
    "purpose": "3-D Secure, tokens and mandates",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Payment Instrument Reference",
    "Provider",
    "Token Status",
    "Masked Identifier where allowed",
    "Card/Instrument Type",
    "Expiry metadata where provided"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-596",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-596"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 77. 0 of 9 labels bound to a contract property; 16 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-597",
  "name": "Digital Payment Exception, Recovery & Expiry Center\\t79",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "9",
   "page": 78
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/digital-payment-exception-recovery-expiry-center-t79-adm-597",
   "component": "apps/ticvai-web/src/routes/commercial/DigitalPaymentExceptionRecoveryExpiryCenterT79.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Centralize operational handling of incomplete or abnormal digital-payment journeys.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 78 §Show"
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
       "label": "Every digital payment exception",
       "columns": [
        "Age",
        "Severity",
        "Owner",
        "Status",
        "Resolution"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 78 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected digital payment exception",
       "bindsTo": null,
       "columns": [
        "Age",
        "Severity",
        "Owner",
        "Status",
        "Resolution"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Exception Types”, “Timed Out”, “Depending on condition”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 78 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital payment exception list.",
   "error": "Could not load. Names which read failed and leaves the digital payment exception untouched.",
   "emptyFirstRun": "No digital payment exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital payment exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setHostedCheckoutConfiguration",
    "contract": "payments",
    "purpose": "Expiry and orphan recovery",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "inquirePaymentStatus",
    "contract": "orders",
    "purpose": "Recover a session",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Age",
    "Severity",
    "Owner",
    "Status",
    "Resolution"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-597",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-597"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 78. 0 of 5 labels bound to a contract property; 5 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-598",
  "name": "Digital Payment Simulator, Conversion & AI Advisor\\t80",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "4",
   "number": "10",
   "page": 79
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/digital-payment-simulator-conversion-ai-advisor-t80-adm-598",
   "component": "apps/ticvai-web/src/routes/commercial/DigitalPaymentSimulatorConversionAiAdvisorT80.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-589"
   ],
   "exitTo": [
    "ADM-589"
   ],
   "transitions": [
    {
     "to": "ADM-589",
     "trigger": "Back to Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select; Merchant Configuration; Captured) and no display directory — it is settings, not a population",
  "purpose": "Allow administrators to validate digital payment journeys and identify conversion opportunities before deploying configuration changes.",
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
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Payment method",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Customer type",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Device context",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "Transaction type",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Select"
      },
      {
       "kind": "selectField",
       "label": "✓",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Merchant Configuration"
      },
      {
       "kind": "selectField",
       "label": "↓",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 79 §Merchant Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital payment simulator configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the digital payment simulator untouched.",
   "emptyFirstRun": "No digital payment simulator configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "simulatePaymentConfiguration",
    "contract": "payments",
    "purpose": "Simulate the digital path",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-598",
   "workshopBoard": "wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-598"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 79. 0 of 0 labels bound to a contract property; 13 of 235 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createPaymentLink": {
  "method": "POST",
  "path": "/payment-links",
  "contract": "orders",
  "summary": "Send a guest a link to pay later",
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
  "requestBody": null,
  "responds": "PaymentLink"
 },
 "getPaymentLink": {
  "method": "GET",
  "path": "/payment-links/{token}",
  "contract": "orders",
  "summary": "What a guest holding a link is being asked to pay for",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
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
 "listPaymentMethods": {
  "method": "GET",
  "path": "/payment-methods",
  "contract": "payments",
  "summary": "The methods this tenant can offer, and where",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "channel",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PaymentMethod"
 },
 "resendPaymentLink": {
  "method": "POST",
  "path": "/payment-links/{linkId}/resend",
  "contract": "orders",
  "summary": "Send it again, and retire the old one",
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
  "responds": "PaymentLink"
 },
 "setHostedCheckoutConfiguration": {
  "method": "PUT",
  "path": "/hosted-checkout-config",
  "contract": "payments",
  "summary": "Redirect, return and the journey back",
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
  "requestBody": "HostedCheckoutConfig",
  "responds": "HostedCheckoutConfig"
 },
 "setPaymentAuthenticationPolicy": {
  "method": "PUT",
  "path": "/payment-authentication-policy",
  "contract": "payments",
  "summary": "3-D Secure, tokenisation and recurring mandates",
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
  "requestBody": "PaymentAuthenticationPolicy",
  "responds": "PaymentAuthenticationPolicy"
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
 "updatePaymentMethod": {
  "method": "PUT",
  "path": "/payment-methods/{methodId}",
  "contract": "payments",
  "summary": "Change availability, fees and eligibility",
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
  "requestBody": "PaymentMethod",
  "responds": "PaymentMethod"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the line. `lineIds` everywhere in this contract are these."
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    },
    "description": "Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."
   },
   "resourceHoldId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "eligibilityDeclaration": {
    "type": "array",
    "nullable": true,
    "x-ticvai-note": "One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n",
    "items": {
     "type": "object",
     "properties": {
      "ageBand": {
       "type": "string",
       "enum": [
        "infant",
        "child",
        "junior",
        "adult",
        "senior"
       ],
       "description": "Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."
      },
      "ageYears": {
       "type": "integer",
       "nullable": true
      },
      "heightBandIndex": {
       "type": "integer",
       "nullable": true
      },
      "confidentSwimmer": {
       "type": "boolean",
       "nullable": true,
       "description": "**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"
      },
      "guardianSigned": {
       "type": "boolean"
      }
     }
    },
    "description": "What was declared for each guest on this line, kept as the record staff check at the gate."
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
    "additionalProperties": true,
    "description": "**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"
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
 "HostedCheckoutConfig": {
  "type": "object",
  "x-ticvai-persistence": "payments.hosted_checkout",
  "description": "Board 4.6. **The return leg is where hosted checkout goes wrong.**",
  "properties": {
   "returnUrl": {
    "type": "string"
   },
   "cancelUrl": {
    "type": "string"
   },
   "webhookUrl": {
    "type": "string",
    "description": "**The authoritative settle path**, because a guest who closes the tab has still paid.\n"
   },
   "webhookSecretFingerprint": {
    "type": "string",
    "readOnly": true
   },
   "sessionTimeoutMinutes": {
    "type": "integer",
    "default": 15
   },
   "orphanReconciliationWindowMinutes": {
    "type": "integer",
    "default": 60,
    "description": "For the ones that fall through both the redirect and the webhook."
   },
   "brandingAssetId": {
    "type": "string",
    "format": "uuid",
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
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "OrderLineDiscount": {
  "type": "object",
  "description": "One discount applied to one order line (SD-008). Rows of `orders.order_line_discount`.",
  "required": [
   "id",
   "amount",
   "source"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "promotions.promotion",
    "description": "The promotion that gave it. Null for a manual discount."
   },
   "source": {
    "type": "string",
    "enum": [
     "promotion",
     "promoCode",
     "manual",
     "bundle",
     "member"
    ]
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A cashier's reason for a manual discount."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "PaymentAuthenticationPolicy": {
  "type": "object",
  "x-ticvai-persistence": "payments.authentication_policy",
  "description": "Board 4.8. **A commercial trade as much as a security one.**",
  "properties": {
   "threeDSecureMode": {
    "type": "string",
    "enum": [
     "never",
     "whenRequired",
     "aboveThreshold",
     "always"
    ],
    "default": "whenRequired"
   },
   "threeDSecureThreshold": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "claimedExemptions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "lowValue",
      "trustedBeneficiary",
      "transactionRiskAnalysis",
      "recurring",
      "merchantInitiated"
     ]
    }
   },
   "tokenisationEnabled": {
    "type": "boolean",
    "default": false
   },
   "tokenRetentionMonths": {
    "type": "integer",
    "nullable": true
   },
   "recurringMandateRequired": {
    "type": "boolean",
    "default": true,
    "description": "**A card stored for a renewal without a mandate is a renewal the venue cannot defend.**\n"
   },
   "mandateTextAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
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
 "PaymentLink": {
  "type": "object",
  "x-ticvai-persistence": "orders.payment_link",
  "description": "BL-072. **A booking taken at POS could not be paid later by the guest**, so a phone booking either took a card over the phone or was not taken.\n`createPaymentLink` was contracted on 18 August with no schema behind it and no guest-facing path. **The link existed and nobody could open it** — found on 20 August by walking the journey rather than the contract.\n**The link is the credential.** A guest holding one is anonymous: not signed in, and quite possibly without an account, because a phone booking is exactly the case where they have not registered. The token grants read of one order and payment against it, and nothing else.\n",
  "required": [
   "id",
   "orderId",
   "token",
   "status",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "reservationId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "Where the link was issued against a reservation rather than an order. **A reservation holds inventory and carries no money**, which is the whole reason a link is needed.\n"
   },
   "token": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**Write-only, single purpose, and it is the only thing the guest presents.** Long enough not to be guessed and scoped to one order — **a token that can read a second order is a token that read somebody else's booking.**\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "viewed",
     "paid",
     "expired",
     "cancelled",
     "superseded"
    ]
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "sms",
     "whatsapp",
     "printed"
    ]
   },
   "sentTo": {
    "type": "string",
    "nullable": true,
    "description": "Masked. **The address it went to is how an operator answers *I never got it*** — and it is personal data, so it is masked here and resolved from `pii` when somebody with permission asks.\n"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "**The expiry releases the hold, not just the link.** An unpaid link holding inventory is inventory nobody can sell, and a link that outlives its hold sells a seat twice.\n"
   },
   "releaseHoldOnExpiry": {
    "type": "boolean",
    "default": true
   },
   "viewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "paidAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "resendCount": {
    "type": "integer",
    "default": 0,
    "description": "**A resend supersedes rather than duplicates.** Two live links against one order is two guests paying for the same booking, and the second payment is a refund somebody has to make.\n"
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "PaymentLinkView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection of orders.payment_link for its holder",
  "description": "What an anonymous holder of a payment link is shown about the link itself.",
  "required": [
   "status",
   "expiresAt"
  ],
  "properties": {
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "viewed",
     "paid",
     "expired",
     "cancelled",
     "superseded"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "releaseHoldOnExpiry": {
    "type": "boolean"
   }
  }
 },
 "PaymentMethod": {
  "type": "object",
  "x-ticvai-persistence": "payments.method",
  "description": "Board 1.2. **A method is not a provider.**",
  "required": [
   "code",
   "name",
   "kind"
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
   "kind": {
    "type": "string",
    "enum": [
     "card",
     "digitalWallet",
     "bankTransfer",
     "cash",
     "storedValue",
     "giftCard",
     "voucher",
     "onAccount",
     "buyNowPayLater",
     "paymentLink"
    ]
   },
   "cardSchemes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "currencies": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "minimumAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maximumAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "surcharge": {
    "type": "object",
    "nullable": true,
    "properties": {
     "percent": {
      "type": "number",
      "nullable": true
     },
     "fixed": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "disclosedToGuest": {
      "type": "boolean",
      "default": true,
      "description": "**Undisclosed surcharging is illegal in several of the markets this platform sells into.** The flag exists so the answer is a configuration somebody chose rather than a template nobody read.\n"
     }
    }
   },
   "refundable": {
    "type": "boolean",
    "default": true
   },
   "partialRefundSupported": {
    "type": "boolean",
    "default": true
   },
   "displayOrder": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
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
 }
}
```
