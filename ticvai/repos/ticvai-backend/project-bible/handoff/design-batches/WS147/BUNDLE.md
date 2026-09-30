# WS147 — Payment Payment Orchestration board 1

**10 screens · 8 operations · 14 schemas · 3 permissions**

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
  `APPROVAL_REQUEST, PAYMENT_CONFIGURE, PAYMENT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-559` | Payment Command Center\t7 | commandCentre | 2 | 0 | — |
| `ADM-560` | Payment Method Catalogue\t8 | listDetail | 2 | 0 | — |
| `ADM-561` | Payment Method Configuration\t9 | configEditor | 1 | 0 | — |
| `ADM-562` | Channel & Touchpoint Payment Configuration\t10 | listDetail | 1 | 0 | — |
| `ADM-563` | Venue, Location & Business Unit Payment Assignment\t11 | configEditor | 1 | 0 | — |
| `ADM-564` | Currency & Payment Currency Configuration\t12 | configEditor | 1 | 0 | — |
| `ADM-565` | Payment Eligibility & Availability Rule Builder\t13 | listDetail | 1 | 0 | — |
| `ADM-566` | Payment Fees, Surcharges & Commercial Rules\t14 | listDetail | 1 | 0 | — |
| `ADM-567` | Payment Policy, Governance & Approval Manager\t15 | configEditor | 4 | 0 | — |
| `ADM-568` | Payment Configuration Simulator & Validation Center\t16 | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-560, ADM-562, ADM-568 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-559",
  "name": "Payment Command Center\\t7",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "1",
   "page": 5
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-command-center-t7-adm-559",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentCommandCenterT7.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-560",
    "ADM-561",
    "ADM-562",
    "ADM-563",
    "ADM-564",
    "ADM-565",
    "ADM-566",
    "ADM-567",
    "ADM-568"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-560",
     "trigger": "Payment Method Catalogue\\t8",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-561",
     "trigger": "Payment Method Configuration\\t9",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-562",
     "trigger": "Channel & Touchpoint Payment Configuration\\t10",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-563",
     "trigger": "Venue, Location & Business Unit Payment Assignment\\t11",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-564",
     "trigger": "Currency & Payment Currency Configuration\\t12",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-565",
     "trigger": "Payment Eligibility & Availability Rule Builder\\t13",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-566",
     "trigger": "Payment Fees, Surcharges & Commercial Rules\\t14",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-567",
     "trigger": "Payment Policy, Governance & Approval Manager\\t15",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-568",
     "trigger": "Payment Configuration Simulator & Validation Center\\t16",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized visibility into payment operations and configuration across the tenant.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Payment Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Successful Payments",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failed Payments",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Payment Success Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Payment Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Refund Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Payment Methods",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Gateways",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Terminals",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Currencies",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Payment Exceptions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Configuration Alerts",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 5 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment \\t7 list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the payment \\t7 untouched.",
   "emptyFirstRun": "No payment \\t7 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment \\t7 are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentMethods",
    "contract": "payments",
    "purpose": "Methods in use",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getPaymentPerformance",
    "contract": "payments",
    "purpose": "How they are performing",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-559",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-559"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 5. 0 of 0 labels bound to a contract property; 12 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-560",
  "name": "Payment Method Catalogue\\t8",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "2",
   "page": 6
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-method-catalogue-t8-adm-560",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentMethodCatalogueT8.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Cards) and no metric row",
  "purpose": "Maintain the centralized catalogue of payment/tender types supported by TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 6 §Cards"
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
       "label": "Every payment method catalogue\\t8",
       "columns": [
        "Credit card",
        "Debit card"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 6 §Cards"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment method catalogue\\t8",
       "bindsTo": null,
       "columns": [
        "Credit card",
        "Debit card"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Cash”, “Digital Payments”, “Stored / Controlled Value”, “Commercial / B2B”, “Other”, “Each method should contain”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 6 §Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment method catalogue\\t8 list.",
   "error": "Could not load. Names which read failed and leaves the payment method catalogue\\t8 untouched.",
   "emptyFirstRun": "No payment method catalogue\\t8 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment method catalogue\\t8 are still there. The pack's own statuses are Draft — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentMethods",
    "contract": "payments",
    "purpose": "The catalogue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createPaymentMethod",
    "contract": "payments",
    "purpose": "Add a method",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Credit card",
    "Debit card"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-560",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-560"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 6. 0 of 2 labels bound to a contract property; 7 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-561",
  "name": "Payment Method Configuration\\t9",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "3",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-method-configuration-t9-adm-561",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentMethodConfigurationT9.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§General Configuration; Configure whether the method allows) and no display directory — it is settings, not a population",
  "purpose": "Configure detailed behavior for each payment method.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Payment method name",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §General Configuration"
      },
      {
       "kind": "selectField",
       "label": "Internal code",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §General Configuration"
      },
      {
       "kind": "selectField",
       "label": "Customer-facing label",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §General Configuration"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §General Configuration"
      },
      {
       "kind": "selectField",
       "label": "Icon",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §General Configuration"
      },
      {
       "kind": "selectField",
       "label": "Tender category",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §General Configuration"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §General Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §General Configuration"
      },
      {
       "kind": "selectField",
       "label": "Sale",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §Configure whether the method allows"
      },
      {
       "kind": "selectField",
       "label": "Refund",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §Configure whether the method allows"
      },
      {
       "kind": "selectField",
       "label": "Partial refund",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §Configure whether the method allows"
      },
      {
       "kind": "selectField",
       "label": "Void",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §Configure whether the method allows"
      },
      {
       "kind": "selectField",
       "label": "Reversal",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §Configure whether the method allows"
      },
      {
       "kind": "selectField",
       "label": "Recurring payment",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §Configure whether the method allows"
      },
      {
       "kind": "selectField",
       "label": "Preauthorization where supported",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §Configure whether the method allows"
      },
      {
       "kind": "selectField",
       "label": "Capture where supported",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 7 §Configure whether the method allows"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment method \\t9 configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the payment method \\t9 untouched.",
   "emptyFirstRun": "No payment method \\t9 configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updatePaymentMethod",
    "contract": "payments",
    "purpose": "Configure a method",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-561",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-561"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 7. 0 of 0 labels bound to a contract property; 16 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-562",
  "name": "Channel & Touchpoint Payment Configuration\\t10",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "4",
   "page": 8
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-touchpoint-payment-configuration-t10-adm-562",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelTouchpointPaymentConfigurationT10.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control which payment methods are available on each sales channel.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 8"
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
   "loading": "The channel touchpoint payment list.",
   "error": "Could not load. Names which read failed and leaves the channel touchpoint payment untouched.",
   "emptyFirstRun": "No channel touchpoint payment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel touchpoint payment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updatePaymentMethod",
    "contract": "payments",
    "purpose": "Per channel and touchpoint",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-562",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-562"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-563",
  "name": "Venue, Location & Business Unit Payment Assignment\\t11",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "5",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/venue-location-business-unit-payment-assignment-t11-adm-563",
   "component": "apps/ticvai-web/src/routes/commercial/VenueLocationBusinessUnitPaymentAssignmentT11.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Business Area Configuration) and no display directory — it is settings, not a population",
  "purpose": "Allow different venues and business units to operate different payment configurations. This is important for TICVAI's multi-venue architecture.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Digital Wallet, Gift Card, Card. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 9 §Supports"
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
       "label": "Ticketing",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Business Area Configuration"
      },
      {
       "kind": "selectField",
       "label": "F&B",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Business Area Configuration"
      },
      {
       "kind": "selectField",
       "label": "Retail",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Business Area Configuration"
      },
      {
       "kind": "selectField",
       "label": "Rental",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Business Area Configuration"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Business Area Configuration"
      },
      {
       "kind": "selectField",
       "label": "Parking",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Business Area Configuration"
      },
      {
       "kind": "selectField",
       "label": "Other TICVAI modules",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Business Area Configuration"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Digital Wallet",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Supports"
      },
      {
       "kind": "secondaryButton",
       "label": "Gift Card",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Supports"
      },
      {
       "kind": "secondaryButton",
       "label": "Card",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 9 §Supports"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue location business configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the venue location business untouched.",
   "emptyFirstRun": "No venue location business configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updatePaymentMethod",
    "contract": "payments",
    "purpose": "Per venue and business unit",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-563",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-563"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 9. 0 of 0 labels bound to a contract property; 10 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-564",
  "name": "Currency & Payment Currency Configuration\\t12",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "6",
   "page": 10
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/currency-payment-currency-configuration-t12-adm-564",
   "component": "apps/ticvai-web/src/routes/commercial/CurrencyPaymentCurrencyConfigurationT12.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define which currencies can be used for payment and how payment currencies interact with TICVAI's selling and accounting currencies.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Accepted currencies by channel",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 10 §Configure"
      },
      {
       "kind": "textField",
       "label": "Accepted currencies by payment method",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue restrictions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gateway compatibility",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency conversion requirement",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 10 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The currency payment currency configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the currency payment currency untouched.",
   "emptyFirstRun": "No currency payment currency configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updatePaymentMethod",
    "contract": "payments",
    "purpose": "Currencies accepted",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-564",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-564"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 10. 0 of 0 labels bound to a contract property; 5 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-565",
  "name": "Payment Eligibility & Availability Rule Builder\\t13",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "7",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-eligibility-availability-rule-builder-t13-adm-565",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentEligibilityAvailabilityRuleBuilderT13.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine whether a payment method should be available for a particular transaction.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: Channel, Venue, Product, Product category, Transaction amount, Customer type, Membership, Country/market where applicable …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
   },
   {
    "operation": null,
    "why": "**Payment Eligibility & Availability Rule Builder\\t13 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 11"
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
       "label": "Channel",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Product",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Product category",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Transaction amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer type",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Country/market where applicable",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 11 §Support conditions such as"
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
   "loading": "The payment eligibility availability list.",
   "error": "Could not load. Names which read failed and leaves the payment eligibility availability untouched.",
   "emptyFirstRun": "No payment eligibility availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment eligibility availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updatePaymentMethod",
    "contract": "payments",
    "purpose": "Eligibility and availability rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-565",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-565"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 11. 0 of 0 labels bound to a contract property; 9 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-566",
  "name": "Payment Fees, Surcharges & Commercial Rules\\t14",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "8",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-fees-surcharges-commercial-rules-t14-adm-566",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentFeesSurchargesCommercialRulesT14.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure payment-related commercial rules where legally and contractually permitted.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Fixed payment fee, Percentage fee, Minimum fee, Maximum fee, Payment-method-specific fee, Channel-specific fee, Currency-specific fee, Waiver rule. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 12"
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
       "label": "Fixed payment fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Percentage fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Minimum fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Maximum fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment-method-specific fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel-specific fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Currency-specific fee",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Waiver rule",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 12 §Support"
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
   "loading": "The payment fees surcharges list.",
   "error": "Could not load. Names which read failed and leaves the payment fees surcharges untouched.",
   "emptyFirstRun": "No payment fees surcharges yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment fees surcharges are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updatePaymentMethod",
    "contract": "payments",
    "purpose": "Fees and surcharges",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentMethods"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-566",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-566"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 12. 0 of 0 labels bound to a contract property; 8 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-567",
  "name": "Payment Policy, Governance & Approval Manager\\t15",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "9",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-policy-governance-approval-manager-t15-adm-567",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentPolicyGovernanceApprovalManagerT15.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide governance over sensitive payment configuration changes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Effective from, Scheduled expiry. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 13 §Support"
   },
   {
    "operation": null,
    "why": "**Payment Policy, Governance & Approval Manager\\t15 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Changed by",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Old value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "New value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective date",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Effective from",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Scheduled expiry",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 13 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment policy governance configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the payment policy governance untouched.",
   "emptyFirstRun": "No payment policy governance configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createApprovalRequest",
    "contract": "approvals",
    "purpose": "Send a change for approval",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listPaymentMethods",
    "contract": "payments",
    "purpose": "What is being changed",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getPaymentRules",
    "contract": "payments",
    "purpose": "The rules currently in force",
    "trigger": "onLoad"
   },
   {
    "operationId": "setPaymentRules",
    "contract": "payments",
    "purpose": "Amend them",
    "trigger": "onSave"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-567",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-567"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 13. 0 of 0 labels bound to a contract property; 9 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-568",
  "name": "Payment Configuration Simulator & Validation Center\\t16",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "1",
   "number": "10",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-configuration-simulator-validation-center-t16-adm-568",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentConfigurationSimulatorValidationCenterT16.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-559"
   ],
   "exitTo": [
    "ADM-559"
   ],
   "transitions": [
    {
     "to": "ADM-559",
     "trigger": "Back to Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Credit Card) and no metric row",
  "purpose": "Allow administrators to test payment configuration before publishing it. This is especially important because payment configuration errors can immediately stop sales.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 14 §Credit Card"
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
       "label": "Every payment simulator validation",
       "columns": [
        "↓",
        "Gateway A — Primary",
        "Gateway B — Secondary",
        "Gateway C — Regional"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 14 §Credit Card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment simulator validation",
       "bindsTo": null,
       "columns": [
        "↓",
        "Gateway A — Primary",
        "Gateway B — Secondary",
        "Gateway C — Regional"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Venue”, “Channel”, “B2C”, “Customer”, “Available payment methods”, “Unavailable”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 14 §Credit Card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment simulator validation list.",
   "error": "Could not load. Names which read failed and leaves the payment simulator validation untouched.",
   "emptyFirstRun": "No payment simulator validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment simulator validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulatePaymentConfiguration",
    "contract": "payments",
    "purpose": "What a guest would be offered",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓",
    "Gateway A — Primary",
    "Gateway B — Secondary",
    "Gateway C — Regional"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-568",
   "workshopBoard": "wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-568"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 14. 0 of 4 labels bound to a contract property; 20 of 184 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Raise a request",
  "permission": "APPROVAL_REQUEST",
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
  "requestBody": "CreateApprovalRequest",
  "responds": "ApprovalRequest"
 },
 "createPaymentMethod": {
  "method": "POST",
  "path": "/payment-methods",
  "contract": "payments",
  "summary": "Add a payment method to the catalogue",
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
  "requestBody": "PaymentMethod",
  "responds": "PaymentMethod"
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
 "getPaymentRules": {
  "method": "GET",
  "path": "/payments/rules",
  "contract": "payments",
  "summary": "Currency, eligibility and fee rules as one set",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PaymentRuleSet"
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
 "setPaymentRules": {
  "method": "PUT",
  "path": "/payments/rules",
  "contract": "payments",
  "summary": "Replace the payment rule set",
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
  "requestBody": "PaymentRuleSet",
  "responds": "PaymentRuleSet"
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
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration",
   "productChange",
   "pricingChange"
  ]
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.",
    "properties": {
     "riskScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "riskBand": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "priorityScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "escalationSuggestion": {
      "type": "object",
      "description": "A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.",
      "properties": {
       "action": {
        "type": "string",
        "enum": [
         "escalate",
         "addBackupApprover",
         "none"
        ]
       },
       "reason": {
        "type": "string",
        "nullable": true
       }
      }
     },
     "signals": {
      "type": "array",
      "maxItems": 10,
      "description": "The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.",
      "items": {
       "type": "object",
       "properties": {
        "code": {
         "type": "string"
        },
        "contribution": {
         "type": "number"
        },
        "detail": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "scoreId": {
      "type": "string",
      "format": "uuid",
      "description": "The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."
     },
     "decisionRecordId": {
      "type": "string",
      "description": "The ai decision record, for the audit of what the AI said and why."
     },
     "assessedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "returned",
   "informationRequested",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
 "CreateApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "kind",
   "subjectContract",
   "subjectType",
   "subjectId",
   "scopePath",
   "summary"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "subjectContract": {
    "type": "string",
    "description": "Which contract owns the thing being approved."
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "description": "**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string",
    "maxLength": 300,
    "description": "What the approver sees in their queue before opening it."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
   },
   "justification": {
    "type": "string",
    "maxLength": 1000
   },
   "isDraft": {
    "type": "boolean",
    "default": false,
    "description": "True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"
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
 "PaymentRuleSet": {
  "type": "object",
  "x-ticvai-persistence": "none — composed from the three payment rule tables",
  "description": "**Three tables, one decision.** Whether a guest may pay with this method, in this currency, and what it costs the venue are evaluated together at checkout. An administrator changing one without seeing the others is how a method becomes eligible in a currency it cannot settle.\n",
  "properties": {
   "currencyRules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/PaymentsCurrencyRule"
    }
   },
   "eligibilityRules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/PaymentsEligibilityRule"
    }
   },
   "feeRules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/PaymentsFeeRule"
    }
   }
  }
 },
 "PaymentsCurrencyRule": {
  "type": "object",
  "x-ticvai-persistence": "payments.currency_rule",
  "description": "**Taken from the backend workbook, 20 September.** NEW TABLE. Defines payment-level currency rules such as accepted/settlement currency, min/max payment amount and rounding.",
  "required": [
   "paymentPolicyId",
   "code",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "paymentPolicyId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   },
   "channelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "code": {
    "type": "string",
    "maxLength": 10
   },
   "settlementCurrencyCode": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "minPaymentAmount": {
    "type": "number",
    "nullable": true
   },
   "maxPaymentAmount": {
    "type": "number",
    "nullable": true
   },
   "roundingIncrement": {
    "type": "number",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "PaymentsEligibilityRule": {
  "type": "object",
  "x-ticvai-persistence": "payments.eligibility_rule",
  "description": "**Taken from the backend workbook, 20 September.** NEW TABLE. Defines when a payment method is allowed or denied for a transaction.",
  "required": [
   "paymentPolicyId",
   "paymentMethodId",
   "effect",
   "priority",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "paymentPolicyId": {
    "type": "string",
    "format": "uuid"
   },
   "paymentMethodId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   },
   "channelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "businessArea": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "currencyCode": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "minOrderAmount": {
    "type": "number",
    "nullable": true
   },
   "maxOrderAmount": {
    "type": "number",
    "nullable": true
   },
   "effect": {
    "type": "string",
    "maxLength": 10
   },
   "priority": {
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "PaymentsFeeRule": {
  "type": "object",
  "x-ticvai-persistence": "payments.fee_rule",
  "description": "**Taken from the backend workbook, 20 September.** NEW TABLE. Defines payment-related fees or surcharges that may be applied to an order.",
  "required": [
   "paymentPolicyId",
   "name",
   "category",
   "calculationType",
   "value",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "paymentPolicyId": {
    "type": "string",
    "format": "uuid"
   },
   "paymentMethodId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "providerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "businessArea": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "currencyCode": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "category": {
    "type": "string",
    "maxLength": 20
   },
   "calculationType": {
    "type": "string",
    "maxLength": 20
   },
   "value": {
    "type": "number"
   },
   "minFee": {
    "type": "number",
    "nullable": true
   },
   "maxFee": {
    "type": "number",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
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
 }
}
```
