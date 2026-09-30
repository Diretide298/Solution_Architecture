# WS148 — Payment Payment Orchestration board 2

**10 screens · 9 operations · 8 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `PAYMENT_CONFIGURE, PAYMENT_PROVIDER_MANAGE, PAYMENT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-569` | Payment Orchestration Command Center\t27 | commandCentre | 2 | 0 | — |
| `ADM-570` | Gateway, PSP & Acquirer Directory\t28 | listDetail | 2 | 0 | — |
| `ADM-571` | Provider Connection & Adapter Configuration\t29 | listDetail | 2 | 0 | — |
| `ADM-572` | Gateway Capability & Payment Method Mapping\t30 | listDetail | 1 | 0 | — |
| `ADM-573` | Payment Routing Rule Builder\t31 | listDetail | 2 | 0 | — |
| `ADM-574` | Routing Strategy, Priority & Load Distribution\t33 | commandCentre | 1 | 0 | — |
| `ADM-575` | Failover, Retry & Resilience Manager\t34 | configEditor | 1 | 0 | — |
| `ADM-576` | Provider Health, SLA & Performance Monitor\t35 | commandCentre | 1 | 0 | — |
| `ADM-577` | Provider Cost, Commercial & Routing Economics\t36 | configEditor | 1 | 0 | — |
| `ADM-578` | Payment Routing Simulator, Decision Trace & AI Advisor\t37 | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-570, ADM-572, ADM-574, ADM-578 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-569",
  "name": "Payment Orchestration Command Center\\t27",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "1",
   "page": 25
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-orchestration-command-center-t27-adm-569",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentOrchestrationCommandCenterT27.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-570",
    "ADM-571",
    "ADM-572",
    "ADM-573",
    "ADM-574",
    "ADM-575",
    "ADM-576",
    "ADM-577",
    "ADM-578"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-570",
     "trigger": "Gateway, PSP & Acquirer Directory\\t28",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-571",
     "trigger": "Provider Connection & Adapter Configuration\\t29",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "connectionId"
     ]
    },
    {
     "to": "ADM-572",
     "trigger": "Gateway Capability & Payment Method Mapping\\t30",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-573",
     "trigger": "Payment Routing Rule Builder\\t31",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-574",
     "trigger": "Routing Strategy, Priority & Load Distribution\\t33",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-575",
     "trigger": "Failover, Retry & Resilience Manager\\t34",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-576",
     "trigger": "Provider Health, SLA & Performance Monitor\\t35",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-577",
     "trigger": "Provider Cost, Commercial & Routing Economics\\t36",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-578",
     "trigger": "Payment Routing Simulator, Decision Trace & AI Advisor\\t37",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Display) — counts over a population, then the population",
  "purpose": "Provide real-time operational visibility across all payment gateways, PSPs and acquirers.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 25 §Display"
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
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Successful Authorizations",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Authorization Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Successful Captures",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Declined Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Technical Failures",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Routed Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Rerouted Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failover Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Providers",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Provider Incidents",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Processing Time",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every payment orchestration \\t27",
       "columns": [
        "Attempted Value",
        "Authorized Value",
        "Captured Value",
        "Failed Value",
        "Rerouted Value"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment orchestration \\t27",
       "bindsTo": null,
       "columns": [
        "Attempted Value",
        "Authorized Value",
        "Captured Value",
        "Failed Value",
        "Rerouted Value"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Provider Value Success Status”, “Provider AED”, “Provider AED Warnin”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 25 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment orchestration \\t27 list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the payment orchestration \\t27 untouched.",
   "emptyFirstRun": "No payment orchestration \\t27 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment orchestration \\t27 are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getPaymentProviderHealth",
    "contract": "payments",
    "purpose": "Provider health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listPaymentProviderConnections",
    "contract": "payments",
    "purpose": "Providers connected",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-569",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-569"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 25. 0 of 5 labels bound to a contract property; 17 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-570",
  "name": "Gateway, PSP & Acquirer Directory\\t28",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "2",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/gateway-psp-acquirer-directory-t28-adm-570",
   "component": "apps/ticvai-web/src/routes/commercial/GatewayPspAcquirerDirectoryT28.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the centralized directory of payment-processing providers connected to TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Payment Gateway, Wallet Provider, Alternative Payment Provider. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 26 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 26"
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
       "label": "Payment Gateway",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Alternative Payment Provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 26 §Support"
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
   "loading": "The gateway psp acquirer list.",
   "error": "Could not load. Names which read failed and leaves the gateway psp acquirer untouched.",
   "emptyFirstRun": "No gateway psp acquirer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gateway psp acquirer are still there. The pack's own statuses are Draft — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentProviderConnections",
    "contract": "payments",
    "purpose": "The directory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createPaymentProviderConnection",
    "contract": "payments",
    "purpose": "Connect one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentProviderConnections"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-570",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-570"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 26. 0 of 0 labels bound to a contract property; 10 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-571",
  "name": "Provider Connection & Adapter Configuration\\t29",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "3",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/provider-connection-adapter-configuration-t29-adm-571",
   "component": "apps/ticvai-web/src/routes/commercial/ProviderConnectionAdapterConfigurationT29.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Configure how TICVAI technically connects to each payment provider.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: API endpoint reference, Webhook configuration, Callback configuration, Retry configuration. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 27 §Support"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 27 §Display"
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
       "label": "Every provider connection adapter",
       "columns": [
        "TICVAI Adapter",
        "Adapter Version",
        "Provider API Version",
        "Deployment Version",
        "Last Certification/Test",
        "Status",
        "Credential status",
        "Last rotation",
        "Expiry",
        "Certificate expiry",
        "Owner"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 27 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected provider connection adapter",
       "bindsTo": null,
       "columns": [
        "TICVAI Adapter",
        "Adapter Version",
        "Provider API Version",
        "Deployment Version",
        "Last Certification/Test",
        "Status",
        "Credential status",
        "Last rotation",
        "Expiry",
        "Certificate expiry",
        "Owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Credential Management”, “Never expose full”, “Result”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 27 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "API endpoint reference",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Webhook configuration",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Callback configuration",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry configuration",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 27 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The provider connection adapter list.",
   "error": "Could not load. Names which read failed and leaves the provider connection adapter untouched.",
   "emptyFirstRun": "No provider connection adapter yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the provider connection adapter are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createPaymentProviderConnection",
    "contract": "payments",
    "purpose": "Adapter configuration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentProviderConnections"
    ]
   },
   {
    "operationId": "testPaymentProviderConnection",
    "contract": "payments",
    "purpose": "Prove it works",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentProviderConnections"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "TICVAI Adapter",
    "Adapter Version",
    "Provider API Version",
    "Deployment Version",
    "Last Certification/Test",
    "Status"
   ],
   "params": [
    {
     "name": "connectionId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-571",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-571"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 27. 0 of 11 labels bound to a contract property; 15 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-572",
  "name": "Gateway Capability & Payment Method Mapping\\t30",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "4",
   "page": 28
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/gateway-capability-payment-method-mapping-t30-adm-572",
   "component": "apps/ticvai-web/src/routes/commercial/GatewayCapabilityPaymentMethodMappingT30.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Map Board 1 payment methods to providers capable of processing them.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 28"
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
       "impliedBy": "listPaymentProviderConnections",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gateway capability payment list.",
   "error": "Could not load. Names which read failed and leaves the gateway capability payment untouched.",
   "emptyFirstRun": "No gateway capability payment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gateway capability payment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentProviderConnections",
    "contract": "payments",
    "purpose": "Capability against method",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-572",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-572"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-573",
  "name": "Payment Routing Rule Builder\\t31",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "5",
   "page": 29
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-routing-rule-builder-t31-adm-573",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentRoutingRuleBuilderT31.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the rules that determine which provider should receive each payment transaction.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Venue, Legal entity, Channel, Payment method, Transaction amount, Transaction type, Customer type where appropriate, Weighted distribution. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
   },
   {
    "operation": null,
    "why": "**Payment Routing Rule Builder\\t31 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 29"
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
       "label": "Venue",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Legal entity",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment method",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Transaction amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Transaction type",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer type where appropriate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Weighted distribution",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 29 §Support"
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
   "loading": "The payment routing rule list.",
   "error": "Could not load. Names which read failed and leaves the payment routing rule untouched.",
   "emptyFirstRun": "No payment routing rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment routing rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPaymentRoutingRules",
    "contract": "payments",
    "purpose": "Build the routing rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentRoutingRules"
    ]
   },
   {
    "operationId": "listPaymentRoutingRules",
    "contract": "payments",
    "purpose": "Rules in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-573",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-573"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 29. 0 of 0 labels bound to a contract property; 8 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-574",
  "name": "Routing Strategy, Priority & Load Distribution\\t33",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "6",
   "page": 31
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/routing-strategy-priority-load-distribution-t33-adm-574",
   "component": "apps/ticvai-web/src/routes/commercial/RoutingStrategyPriorityLoadDistributionT33.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§AED Card / B2C) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Manage how payment traffic is distributed when several valid providers are available.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Provider A: 60%",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 31 §AED Card / B2C"
      },
      {
       "kind": "metricTile",
       "label": "Provider B: 30%",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 31 §AED Card / B2C"
      },
      {
       "kind": "metricTile",
       "label": "Provider C: 10%",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 31 §AED Card / B2C"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The routing strategy priority list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the routing strategy priority untouched.",
   "emptyFirstRun": "No routing strategy priority yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the routing strategy priority are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPaymentRoutingRules",
    "contract": "payments",
    "purpose": "Priority and load distribution",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentRoutingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-574",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-574"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 31. 0 of 0 labels bound to a contract property; 3 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-575",
  "name": "Failover, Retry & Resilience Manager\\t34",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "7",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/failover-retry-resilience-manager-t34-adm-575",
   "component": "apps/ticvai-web/src/routes/commercial/FailoverRetryResilienceManagerT34.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Maintain payment availability when a provider experiences a technical problem. This is one of the most important screens in the Payment Orchestration module.",
  "gaps": [
   {
    "operation": null,
    "why": "**Failover, Retry & Resilience Manager\\t34 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Primary provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Secondary provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tertiary provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Trigger condition",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retry limit",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Timeout",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cooldown",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Recovery behavior",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 32 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The failover retry resilience configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the failover retry resilience untouched.",
   "emptyFirstRun": "No failover retry resilience configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setPaymentFailoverPolicy",
    "contract": "payments",
    "purpose": "Retry, failover and circuit breaking",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getPaymentProviderHealth"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-575",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-575"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 32. 0 of 0 labels bound to a contract property; 8 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-576",
  "name": "Provider Health, SLA & Performance Monitor\\t35",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "8",
   "page": 33
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/provider-health-sla-performance-monitor-t35-adm-576",
   "component": "apps/ticvai-web/src/routes/commercial/ProviderHealthSlaPerformanceMonitorT35.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Health Metrics) and a per-row directory (§Compare) — counts over a population, then the population",
  "purpose": "Monitor each provider's technical and transactional health.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 33 §Compare"
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
       "label": "Availability",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Authorization rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Capture rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Decline rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Technical error rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Timeout rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Average latency",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "95th and 99th percentile latency where available",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Webhook delay",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Refund API health",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Health Metrics"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every provider health sla",
       "columns": [
        "Today",
        "Yesterday",
        "7 Days",
        "30 Days",
        "Historical baseline"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected provider health sla",
       "bindsTo": null,
       "columns": [
        "Today",
        "Yesterday",
        "7 Days",
        "30 Days",
        "Historical baseline"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Health State”, “Authorization Rate”, “Normal Baseline”, “Change”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 33 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The provider health sla list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the provider health sla untouched.",
   "emptyFirstRun": "No provider health sla yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the provider health sla are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getPaymentProviderHealth",
    "contract": "payments",
    "purpose": "Authorisation rate and latency",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-576",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-576"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 33. 0 of 5 labels bound to a contract property; 19 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-577",
  "name": "Provider Cost, Commercial & Routing Economics\\t36",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "9",
   "page": 34
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/provider-cost-commercial-routing-economics-t36-adm-577",
   "component": "apps/ticvai-web/src/routes/commercial/ProviderCostCommercialRoutingEconomicsT36.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrator may define) and no display directory — it is settings, not a population",
  "purpose": "Allow TICVAI to understand the commercial cost of routing transactions through different providers.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Maximize Authorization",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 34 §Administrator may define"
      },
      {
       "kind": "selectField",
       "label": "Minimize Cost",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 34 §Administrator may define"
      },
      {
       "kind": "selectField",
       "label": "Minimize Latency",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 34 §Administrator may define"
      },
      {
       "kind": "selectField",
       "label": "Balanced",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 34 §Administrator may define"
      },
      {
       "kind": "selectField",
       "label": "Custom Governed Strategy",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 34 §Administrator may define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The provider cost commercial configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the provider cost commercial untouched.",
   "emptyFirstRun": "No provider cost commercial configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getPaymentProviderEconomics",
    "contract": "payments",
    "purpose": "What each provider costs",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-577",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-577"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 34. 0 of 0 labels bound to a contract property; 5 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-578",
  "name": "Payment Routing Simulator, Decision Trace & AI Advisor\\t37",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "2",
   "number": "10",
   "page": 35
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-routing-simulator-decision-trace-ai-advisor-t37-adm-578",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentRoutingSimulatorDecisionTraceAiAdvisorT37.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-569"
   ],
   "exitTo": [
    "ADM-569"
   ],
   "transitions": [
    {
     "to": "ADM-569",
     "trigger": "Back to Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Credit Card can route through) and no metric row",
  "purpose": "Allow administrators to test exactly how a payment will be routed before deploying routing changes.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 35 §Credit Card can route through"
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
       "label": "Every payment routing simulator",
       "columns": [
        "Provider A",
        "Provider B",
        "Provider C"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 35 §Credit Card can route through"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment routing simulator",
       "bindsTo": null,
       "columns": [
        "Provider A",
        "Provider B",
        "Provider C"
       ],
       "notes": "The pack groups this record's detail under its own headings: “AED 720”, “Provider A”, “Provider B”, “Provider C”, “Payment Request”, “Payment Method”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 35 §Credit Card can route through"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment routing simulator list.",
   "error": "Could not load. Names which read failed and leaves the payment routing simulator untouched.",
   "emptyFirstRun": "No payment routing simulator yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment routing simulator are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulatePaymentRouting",
    "contract": "payments",
    "purpose": "Where would this go, and why",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Provider A",
    "Provider B",
    "Provider C"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-578",
   "workshopBoard": "wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-578"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 35. 0 of 3 labels bound to a contract property; 13 of 238 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createPaymentProviderConnection": {
  "method": "POST",
  "path": "/payment-providers",
  "contract": "payments",
  "summary": "Connect a provider",
  "permission": "PAYMENT_PROVIDER_MANAGE",
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
  "requestBody": "PaymentProviderConnection",
  "responds": "PaymentProviderConnection"
 },
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
 "getPaymentProviderHealth": {
  "method": "GET",
  "path": "/payment-providers/health",
  "contract": "payments",
  "summary": "Authorisation rate, latency and availability, per provider",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ProviderHealth"
 },
 "listPaymentProviderConnections": {
  "method": "GET",
  "path": "/payment-providers",
  "contract": "payments",
  "summary": "Gateways, PSPs and acquirers, and what each can do",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PaymentProviderConnection"
 },
 "listPaymentRoutingRules": {
  "method": "GET",
  "path": "/payment-routing-rules",
  "contract": "payments",
  "summary": "Which provider takes which transaction",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PaymentRoutingRule"
 },
 "setPaymentFailoverPolicy": {
  "method": "PUT",
  "path": "/payment-failover-policy",
  "contract": "payments",
  "summary": "What happens when a provider fails, and when to stop trying",
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
  "requestBody": "PaymentFailoverPolicy",
  "responds": "PaymentFailoverPolicy"
 },
 "setPaymentRoutingRules": {
  "method": "PUT",
  "path": "/payment-routing-rules",
  "contract": "payments",
  "summary": "Route by method, currency, venue, amount, cost or share",
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
  "requestBody": null,
  "responds": "PaymentRoutingRule"
 },
 "simulatePaymentRouting": {
  "method": "POST",
  "path": "/payment-routing/simulate",
  "contract": "payments",
  "summary": "Where would this transaction go, and why",
  "permission": "PAYMENT_VIEW",
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
  "responds": "RoutingDecision"
 },
 "testPaymentProviderConnection": {
  "method": "POST",
  "path": "/payment-providers/{connectionId}/test",
  "contract": "payments",
  "summary": "Prove the connection works before anybody pays through it",
  "permission": "PAYMENT_PROVIDER_MANAGE",
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
  "requestBody": null,
  "responds": "ProviderTestResult"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "PaymentFailoverPolicy": {
  "type": "object",
  "x-ticvai-persistence": "payments.failover_policy",
  "description": "Board 2.7. **A decline is final; a timeout is not. Retrying the first is how a guest gets charged twice.**\n",
  "properties": {
   "retryableOutcomes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "timeout",
      "connectionRefused",
      "providerError5xx",
      "rateLimited",
      "issuerUnavailable"
     ]
    },
    "description": "**Explicit, rather than \"anything that was not a success\".**"
   },
   "maxAttempts": {
    "type": "integer",
    "default": 2
   },
   "backoffMs": {
    "type": "integer",
    "default": 500
   },
   "failoverToNextProvider": {
    "type": "boolean",
    "default": true
   },
   "circuitBreaker": {
    "type": "object",
    "description": "**A hundred tills each discovering an outage independently is a hundred queues.**\n",
    "properties": {
     "failureThresholdPercent": {
      "type": "number",
      "default": 25
     },
     "windowSeconds": {
      "type": "integer",
      "default": 60
     },
     "minimumSample": {
      "type": "integer",
      "default": 20
     },
     "openForSeconds": {
      "type": "integer",
      "default": 300
     },
     "alertOnOpen": {
      "type": "boolean",
      "default": true
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "PaymentProviderConnection": {
  "type": "object",
  "x-ticvai-persistence": "payments.provider_connection",
  "description": "Boards 2.2 and 2.4. **Capability mapping is the part that gets skipped.**",
  "required": [
   "code",
   "providerKind"
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
   "providerKind": {
    "type": "string",
    "enum": [
     "gateway",
     "psp",
     "acquirer",
     "walletProvider",
     "bnplProvider"
    ]
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "production"
    ]
   },
   "credentialFingerprint": {
    "type": "string",
    "readOnly": true,
    "description": "**Written, never read back.** Enough to confirm which key is in use without the key being retrievable from a screen.\n"
   },
   "capabilities": {
    "type": "object",
    "properties": {
     "methods": {
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
     "partialCapture": {
      "type": "boolean",
      "default": false
     },
     "multipleCapture": {
      "type": "boolean",
      "default": false
     },
     "refundWindowDays": {
      "type": "integer",
      "nullable": true
     },
     "tokenisation": {
      "type": "boolean",
      "default": false
     },
     "threeDSecure": {
      "type": "boolean",
      "default": false
     },
     "cardPresent": {
      "type": "boolean",
      "default": false
     }
    }
   },
   "merchantAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "testing",
     "active",
     "degraded",
     "disabled"
    ]
   },
   "lastTestedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "PaymentRoutingRule": {
  "type": "object",
  "x-ticvai-persistence": "payments.routing_rule",
  "description": "Boards 2.5 and 2.6. **Priority and distribution are both needed.**",
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
   "priority": {
    "type": "integer",
    "default": 0
   },
   "conditions": {
    "type": "object",
    "properties": {
     "methodIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "currencies": {
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
     "channels": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "minimumAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "maximumAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "cardSchemes": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "cardIssuerCountries": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "targets": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "connectionId": {
       "type": "string",
       "format": "uuid"
      },
      "sharePercent": {
       "type": "integer",
       "nullable": true
      },
      "rank": {
       "type": "integer"
      }
     }
    }
   },
   "strategy": {
    "type": "string",
    "enum": [
     "priorityOrder",
     "loadShare",
     "lowestCost",
     "highestAuthRate"
    ],
    "default": "priorityOrder"
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
 "ProviderHealth": {
  "type": "object",
  "description": "Board 2.8. **Authorisation rate is the number, and it is not uptime.**",
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
   "authorisationRate": {
    "type": "number"
   },
   "baselineAuthorisationRate": {
    "type": "number",
    "nullable": true
   },
   "declineRate": {
    "type": "number"
   },
   "errorRate": {
    "type": "number"
   },
   "p50LatencyMs": {
    "type": "integer"
   },
   "p95LatencyMs": {
    "type": "integer"
   },
   "circuitState": {
    "type": "string",
    "enum": [
     "closed",
     "open",
     "halfOpen"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "healthy",
     "degraded",
     "failing",
     "disabled"
    ]
   }
  }
 },
 "ProviderTestResult": {
  "type": "object",
  "description": "Board 3.10. **A provider configured and never tested fails on the first real transaction.**\n",
  "properties": {
   "connectionId": {
    "type": "string",
    "format": "uuid"
   },
   "testedAt": {
    "type": "string",
    "format": "date-time"
   },
   "checks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "credentials",
        "authorise",
        "capture",
        "refund",
        "void",
        "tokenise",
        "webhook"
       ]
      },
      "passed": {
       "type": "boolean"
      },
      "latencyMs": {
       "type": "integer",
       "nullable": true
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "overall": {
    "type": "string",
    "enum": [
     "pass",
     "partial",
     "fail"
    ]
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
 "RoutingDecision": {
  "type": "object",
  "description": "Board 2.10. **Includes the rules that did not match**, because routing that is subtly wrong still succeeds.\n",
  "properties": {
   "chosenConnectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "chosenProviderName": {
    "type": "string",
    "nullable": true
   },
   "estimatedCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "trace": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "ruleCode": {
       "type": "string"
      },
      "matched": {
       "type": "boolean"
      },
      "skippedBecause": {
       "type": "string",
       "nullable": true
      },
      "candidateConnectionId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "fallbackChain": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 }
}
```
