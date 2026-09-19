# WS107 — Subscription Licensing AI Self Service board 10

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-459` | Billing & Commercial Command Center | commandCentre | 0 | 0 | — |
| `ADM-460` | Billing Calculation & Charge Breakdown | listDetail | 0 | 0 | — |
| `ADM-461` | Consumption Reconciliation & Billing Approval | listDetail | 0 | 0 | — |
| `ADM-462` | Invoice & Payment Management | listDetail | 0 | 0 | — |
| `ADM-463` | Subscription & Commercial Change Management | listDetail | 0 | 0 | — |
| `ADM-464` | Renewal Management Center | commandCentre | 0 | 0 | — |
| `ADM-465` | AI Upgrade, Downgrade & Commercial Right-Sizing | listDetail | 0 | 0 | — |
| `ADM-466` | Commercial Scenario Simulator | commandCentre | 0 | 0 | — |
| `ADM-467` | Discount, Credit & Commercial Override Management | configEditor | 0 | 0 | — |
| `ADM-468` | Renewal Approval, Activation & Commercial Handoff | listDetail | 0 | 0 | — |

## Thin screens in this batch

**ADM-460, ADM-461, ADM-462, ADM-463, ADM-465, ADM-468 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-459",
  "name": "Billing & Commercial Command Center",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "1",
   "page": 122
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/billing-commercial-command-center-adm-459",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/BillingCommercialCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-460",
    "ADM-461",
    "ADM-462",
    "ADM-463",
    "ADM-464",
    "ADM-465",
    "ADM-466",
    "ADM-467",
    "ADM-468"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "ADM-460",
     "trigger": "Billing Calculation & Charge Breakdown",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-461",
     "trigger": "Consumption Reconciliation & Billing Approval",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-462",
     "trigger": "Invoice & Payment Management",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-463",
     "trigger": "Subscription & Commercial Change Management",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-464",
     "trigger": "Renewal Management Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-465",
     "trigger": "AI Upgrade, Downgrade & Commercial Right-Sizing",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-466",
     "trigger": "Commercial Scenario Simulator",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-467",
     "trigger": "Discount, Credit & Commercial Override Management",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-468",
     "trigger": "Renewal Approval, Activation & Commercial Handoff",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Financial KPIs) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Provide finance, commercial and subscription teams with a consolidated view of the customer's financial position.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Show"
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
       "label": "Current Billing Period",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Current Charge",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "MRR / Monthly Equivalent",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "ACV",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "YTD Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Outstanding Balance",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Next Invoice",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Minimum Guarantee",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Variable Consumption",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Payment Status",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Financial KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every billing commercial",
       "columns": [
        "Platform Fee",
        "Module Fees",
        "Ticket/Transaction Charges",
        "Minimum Guarantee",
        "Overage",
        "Capacity",
        "Services",
        "Discounts/Credits",
        "Tax"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected billing commercial",
       "bindsTo": null,
       "columns": [
        "Platform Fee",
        "Module Fees",
        "Ticket/Transaction Charges",
        "Minimum Guarantee",
        "Overage",
        "Capacity",
        "Services",
        "Discounts/Credits",
        "Tax"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Dubai Discovery Museum”, “Billable Tickets”, “Rate”, “Commercial Health”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 122 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The billing commercial list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the billing commercial untouched.",
   "emptyFirstRun": "No billing commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the billing commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Current Billing Period",
    "Current Charge",
    "MRR / Monthly Equivalent",
    "ACV",
    "YTD Revenue",
    "Outstanding Balance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-459"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 122. 0 of 9 labels bound to a contract property; 19 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-460",
  "name": "Billing Calculation & Charge Breakdown",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "2",
   "page": 124
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/billing-calculation-charge-breakdown-adm-460",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/BillingCalculationChargeBreakdown.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Calculate exactly what TICVAI should charge for the billing period. This screen must dynamically change according to the commercial model.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 124"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 124"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The billing calculation charge list.",
   "error": "Could not load. Names which read failed and leaves the billing calculation charge untouched.",
   "emptyFirstRun": "No billing calculation charge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the billing calculation charge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-460"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 124. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-461",
  "name": "Consumption Reconciliation & Billing Approval",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "3",
   "page": 125
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/consumption-reconciliation-billing-approval-adm-461",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ConsumptionReconciliationBillingApproval.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "This is an important new screen following the introduction of transaction-based contracts. Finance must be able to reconcile the commercial consumption received from Board 9 before invoicing.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 125"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 125"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The consumption reconciliation billing list.",
   "error": "Could not load. Names which read failed and leaves the consumption reconciliation billing untouched.",
   "emptyFirstRun": "No consumption reconciliation billing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the consumption reconciliation billing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-461"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 125. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-462",
  "name": "Invoice & Payment Management",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "4",
   "page": 126
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/invoice-payment-management-adm-462",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/InvoicePaymentManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Generate, issue and track customer invoices and payments.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 126"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 126"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The invoice payment list.",
   "error": "Could not load. Names which read failed and leaves the invoice payment untouched.",
   "emptyFirstRun": "No invoice payment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the invoice payment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-462"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 126. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-463",
  "name": "Subscription & Commercial Change Management",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "5",
   "page": 127
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/subscription-commercial-change-management-adm-463",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/SubscriptionCommercialChangeManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Manage changes to an active commercial agreement without losing contractual history.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 127 §Show"
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
       "label": "Every subscription commercial change",
       "columns": [
        "Current Monthly Equivalent",
        "Proposed Monthly Equivalent",
        "Proration",
        "Customer Impact",
        "TICVAI Revenue Impact",
        "Contract Value Change"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 127 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected subscription commercial change",
       "bindsTo": null,
       "columns": [
        "Current Monthly Equivalent",
        "Proposed Monthly Equivalent",
        "Proration",
        "Customer Impact",
        "TICVAI Revenue Impact",
        "Contract Value Change"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Change Types”, “Current”, “Proposed”, “Effective Timing”, “Draft Change”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 127 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The subscription commercial change list.",
   "error": "Could not load. Names which read failed and leaves the subscription commercial change untouched.",
   "emptyFirstRun": "No subscription commercial change yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription commercial change are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Current Monthly Equivalent",
    "Proposed Monthly Equivalent",
    "Proration",
    "Customer Impact",
    "TICVAI Revenue Impact",
    "Contract Value Change"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-463"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 127. 0 of 6 labels bound to a contract property; 6 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-464",
  "name": "Renewal Management Center",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "6",
   "page": 129
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/renewal-management-center-adm-464",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/RenewalManagementCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Renewal KPIs) and a per-row directory (§Analyze) — counts over a population, then the population",
  "purpose": "Manage the complete customer renewal pipeline.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Analyze"
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
       "label": "Renewals Due",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Renewal KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Renewal ARR / Contract Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Renewal KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Rate",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Renewal KPIs"
      },
      {
       "kind": "metricTile",
       "label": "At-Risk Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Renewal KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Auto-Renew Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Renewal KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Expansion Opportunity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Renewal KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Cost Optimization Opportunity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Renewal KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every renewal",
       "columns": [
        "Ticket Growth",
        "Transaction Growth",
        "Technical Usage",
        "Overage",
        "Minimum Guarantee Utilization",
        "Module Adoption",
        "Payment History",
        "Support Activity",
        "Contract Exceptions",
        "Customer Growth/Decline"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected renewal",
       "bindsTo": null,
       "columns": [
        "Ticket Growth",
        "Transaction Growth",
        "Technical Usage",
        "Overage",
        "Minimum Guarantee Utilization",
        "Module Adoption",
        "Payment History",
        "Support Activity",
        "Contract Exceptions",
        "Customer Growth/Decline"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Renewal Windows”, “Customer Renewal Table”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 129 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The renewal list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the renewal untouched.",
   "emptyFirstRun": "No renewal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the renewal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Renewals Due",
    "Renewal ARR / Contract Value",
    "Renewal Rate",
    "At-Risk Revenue",
    "Auto-Renew Value",
    "Expansion Opportunity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-464"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 129. 0 of 10 labels bound to a contract property; 17 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-465",
  "name": "AI Upgrade, Downgrade & Commercial Right-Sizing",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "7",
   "page": 130
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/ai-upgrade-downgrade-commercial-right-sizing-adm-465",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/AiUpgradeDowngradeCommercialRightSizing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use AI to recommend the best future commercial structure, not simply the most expensive package. This remains a fundamental TICVAI AI principle.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 130"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 130"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The upgrade downgrade commercial list.",
   "error": "Could not load. Names which read failed and leaves the upgrade downgrade commercial untouched.",
   "emptyFirstRun": "No upgrade downgrade commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upgrade downgrade commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-465"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 130. 0 of 0 labels bound to a contract property; 0 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-466",
  "name": "Commercial Scenario Simulator",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "8",
   "page": 131
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/commercial-scenario-simulator-adm-466",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CommercialScenarioSimulator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Comparison Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow commercial and finance teams to model different renewal or contract scenarios before making an offer.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Customer Cost",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      },
      {
       "kind": "metricTile",
       "label": "TICVAI Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Minimum Revenue Protection",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Variable Revenue Exposure",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Margin",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Expected Overage",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Customer Saving/Increase",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Contract Predictability",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Growth/Contraction",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 131 §Comparison Metrics"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial scenario simulator list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the commercial scenario simulator untouched.",
   "emptyFirstRun": "No commercial scenario simulator yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial scenario simulator are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Customer Cost",
    "TICVAI Revenue",
    "Minimum Revenue Protection",
    "Variable Revenue Exposure",
    "Margin",
    "Expected Overage"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-466"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 131. 0 of 0 labels bound to a contract property; 9 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-467",
  "name": "Discount, Credit & Commercial Override Management",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "9",
   "page": 132
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/discount-credit-commercial-override-management-adm-467",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/DiscountCreditCommercialOverrideManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Required Fields) and no display directory — it is settings, not a population",
  "purpose": "Govern non-standard commercial terms.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Override Type",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Standard Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Proposed Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Financial Impact",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Start Date",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Contract",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Requested By",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      },
      {
       "kind": "selectField",
       "label": "Required Approval",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 132 §Required Fields"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The discount credit commercial configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the discount credit commercial untouched.",
   "emptyFirstRun": "No discount credit commercial configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-467"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 132. 0 of 0 labels bound to a contract property; 10 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-468",
  "name": "Renewal Approval, Activation & Commercial Handoff",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "10",
   "number": "10",
   "page": 133
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/renewal-approval-activation-commercial-handoff-adm-468",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/RenewalApprovalActivationCommercialHandoff.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-459"
   ],
   "exitTo": [
    "ADM-459"
   ],
   "transitions": [
    {
     "to": "ADM-459",
     "trigger": "Back to Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Finalize renewal and synchronize the approved future commercial agreement across TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Revised Board 10 — Commercial Model Calculation. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 133 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 133"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 133"
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
       "label": "Revised Board 10 — Commercial Model Calculation",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 133 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The renewal approval activation list.",
   "error": "Could not load. Names which read failed and leaves the renewal approval activation untouched.",
   "emptyFirstRun": "No renewal approval activation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the renewal approval activation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-468"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 133. 0 of 0 labels bound to a contract property; 1 of 119 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
