# WS107 — Subscription Licensing AI Self Service board 10

**10 screens · 15 operations · 20 schemas · 6 permissions**

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
  `PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-459` | Billing & Commercial Command Center | commandCentre | 1 | 0 | — |
| `ADM-460` | Billing Calculation & Charge Breakdown | listDetail | 1 | 0 | — |
| `ADM-461` | Consumption Reconciliation & Billing Approval | listDetail | 2 | 0 | — |
| `ADM-462` | Invoice & Payment Management | listDetail | 4 | 0 | — |
| `ADM-463` | Subscription & Commercial Change Management | listDetail | 2 | 0 | — |
| `ADM-464` | Renewal Management Center | commandCentre | 2 | 0 | — |
| `ADM-465` | AI Upgrade, Downgrade & Commercial Right-Sizing | listDetail | 2 | 0 | — |
| `ADM-466` | Commercial Scenario Simulator | commandCentre | 1 | 0 | — |
| `ADM-467` | Discount, Credit & Commercial Override Management | configEditor | 4 | 0 | — |
| `ADM-468` | Renewal Approval, Activation & Commercial Handoff | listDetail | 1 | 0 | — |

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
  "apis": [
   {
    "operationId": "listSubscriptionInvoices",
    "contract": "subscription",
    "purpose": "Billing at a glance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Current Billing Period",
    "Current Charge",
    "MRR / Monthly Equivalent",
    "ACV",
    "YTD Revenue",
    "Outstanding Balance"
   ],
   "params": [
    {
     "name": "tenantId",
     "from": "session"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-459",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-459"
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "generateInvoice",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "generateInvoice"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The billing calculation charge list.",
   "error": "Could not load. Names which read failed and leaves the billing calculation charge untouched.",
   "emptyFirstRun": "No billing calculation charge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the billing calculation charge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "generateInvoice",
    "contract": "subscription",
    "purpose": "Calculate the charge",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-460",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-460"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 124. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "session"
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "settleAiUsage",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "settleAiUsage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consumption reconciliation billing list.",
   "error": "Could not load. Names which read failed and leaves the consumption reconciliation billing untouched.",
   "emptyFirstRun": "No consumption reconciliation billing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the consumption reconciliation billing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getBillingReconciliation",
    "contract": "subscription",
    "purpose": "Consumption against invoice",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "settleAiUsage",
    "contract": "subscription",
    "purpose": "Settle the period's AI token usage into metered billing lines",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-461",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-461"
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "recordInvoicePayment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSubscriptionInvoices",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordInvoicePayment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The invoice payment list.",
   "error": "Could not load. Names which read failed and leaves the invoice payment untouched.",
   "emptyFirstRun": "No invoice payment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the invoice payment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordInvoicePayment",
    "contract": "subscription",
    "purpose": "Invoice and payment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSubscriptionInvoices",
    "contract": "subscription",
    "purpose": "Invoices raised",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "issueCreditNote",
    "contract": "subscription",
    "purpose": "Issue a full or partial credit note",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listCreditNotes",
    "contract": "subscription",
    "purpose": "Credit notes issued",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-462",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-462"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 126. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "invoiceId",
     "from": "navigation"
    },
    {
     "name": "tenantId",
     "from": "session"
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
  "apis": [
   {
    "operationId": "previewSubscriptionChange",
    "contract": "subscription",
    "purpose": "Model a change",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setSubscription",
    "contract": "subscription",
    "purpose": "Apply it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Current Monthly Equivalent",
    "Proposed Monthly Equivalent",
    "Proration",
    "Customer Impact",
    "TICVAI Revenue Impact",
    "Contract Value Change"
   ],
   "params": [
    {
     "name": "tenantId",
     "from": "session"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-463",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-463"
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
  "apis": [
   {
    "operationId": "listRenewalAuto",
    "contract": "subscription",
    "purpose": "Renewals",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setRenewalAutoMembership",
    "contract": "subscription",
    "purpose": "Set auto-renewal",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-464",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-464"
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "simulateCommercialPackage",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateCommercialPackage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade downgrade commercial list.",
   "error": "Could not load. Names which read failed and leaves the upgrade downgrade commercial untouched.",
   "emptyFirstRun": "No upgrade downgrade commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upgrade downgrade commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateCommercialPackage",
    "contract": "subscription",
    "purpose": "Right-sizing options",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getPlanRecommendations",
    "contract": "subscription",
    "purpose": "Upgrade, downgrade and right-sizing recommendations for the tenant, priced",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-465",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-465"
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
  "apis": [
   {
    "operationId": "simulateCommercialPackage",
    "contract": "subscription",
    "purpose": "Scenario simulation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-466",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-466"
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
  "apis": [
   {
    "operationId": "cancelInvoice",
    "contract": "subscription",
    "purpose": "Credit or cancel",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "disputeInvoice",
    "contract": "subscription",
    "purpose": "Raise a dispute",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "issueCreditNote",
    "contract": "subscription",
    "purpose": "Credit an invoice in full or in part",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listCreditNotes",
    "contract": "subscription",
    "purpose": "Credits against the tenant's invoices",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-467",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-467"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 132. 0 of 0 labels bound to a contract property; 10 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "invoiceId",
     "from": "navigation"
    },
    {
     "name": "tenantId",
     "from": "session"
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
    },
    {
     "name": "contentBody",
     "components": []
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
  "apis": [
   {
    "operationId": "getBillingReconciliation",
    "contract": "subscription",
    "purpose": "Billing audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-468",
   "workshopBoard": "wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-468"
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
{
 "cancelInvoice": {
  "method": "POST",
  "path": "/invoices/{invoiceId}/cancel",
  "contract": "subscription",
  "summary": "Cancel or credit an invoice",
  "permission": "PLATFORM_BILLING_MANAGE",
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
  "responds": null
 },
 "disputeInvoice": {
  "method": "POST",
  "path": "/invoices/{invoiceId}/dispute",
  "contract": "subscription",
  "summary": "Raise a dispute",
  "permission": "PLATFORM_BILLING_MANAGE",
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
  "responds": null
 },
 "generateInvoice": {
  "method": "POST",
  "path": "/tenants/{tenantId}/invoices",
  "contract": "subscription",
  "summary": "Generate an invoice for a period",
  "permission": "PLATFORM_BILLING_MANAGE",
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
  "responds": "SubscriptionInvoice"
 },
 "getBillingReconciliation": {
  "method": "GET",
  "path": "/billing-reconciliation",
  "contract": "subscription",
  "summary": "Metered consumption against what was invoiced",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "tenantId",
    "in": "query",
    "required": true
   },
   {
    "name": "period",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "BillingReconciliation"
 },
 "getPlanRecommendations": {
  "method": "GET",
  "path": "/plan-recommendations",
  "contract": "subscription",
  "summary": "Which plan, module or pack would fit this tenant better, and what it would cost or save",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "tenantId",
    "in": "query",
    "required": true
   },
   {
    "name": "horizonMonths",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
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
 "issueCreditNote": {
  "method": "POST",
  "path": "/invoices/{invoiceId}/credit-notes",
  "contract": "subscription",
  "summary": "Issue a credit note against a tenant invoice, in full or in part",
  "permission": "PLATFORM_BILLING_MANAGE",
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
  "requestBody": "IssueCreditNoteRequest",
  "responds": "SubscriptionCreditNote"
 },
 "listCreditNotes": {
  "method": "GET",
  "path": "/tenants/{tenantId}/credit-notes",
  "contract": "subscription",
  "summary": "List a tenant's credit notes",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "invoiceId",
    "in": "query",
    "required": false
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
 "listRenewalAuto": {
  "method": "GET",
  "path": "/renewal-auto",
  "contract": "subscription",
  "summary": "Renewal Operations & Auto-Renewal Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "renewalStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "tier",
    "in": "query",
    "required": false
   },
   {
    "name": "autoRenew",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringTo",
    "in": "query",
    "required": false
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
 "listSubscriptionInvoices": {
  "method": "GET",
  "path": "/tenants/{tenantId}/invoices",
  "contract": "subscription",
  "summary": "List subscription invoices",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
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
 "previewSubscriptionChange": {
  "method": "POST",
  "path": "/tenants/{tenantId}/subscription/preview",
  "contract": "subscription",
  "summary": "Preview the effect of a plan change",
  "permission": "PLATFORM_TENANT_VIEW",
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
  "requestBody": "SetSubscriptionRequest",
  "responds": "SubscriptionPreview"
 },
 "recordInvoicePayment": {
  "method": "POST",
  "path": "/invoices/{invoiceId}/payment",
  "contract": "subscription",
  "summary": "Record payment against an invoice",
  "permission": "PLATFORM_BILLING_MANAGE",
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
  "responds": null
 },
 "setRenewalAutoMembership": {
  "method": "PUT",
  "path": "/renewal-auto-membership",
  "contract": "subscription",
  "summary": "Renewal, Auto-Renewal & Membership Continuity Configuration",
  "permission": "PLATFORM_CELL_MANAGE",
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
  "requestBody": "RenewalAutoRenewalMembershipContinuityConfigurationInput",
  "responds": "RenewalAutoRenewalMembershipContinuityConfigurationView"
 },
 "setSubscription": {
  "method": "PUT",
  "path": "/tenants/{tenantId}/subscription",
  "contract": "subscription",
  "summary": "Assign or change a subscription",
  "permission": "PLATFORM_TENANT_MANAGE",
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
  "requestBody": "SetSubscriptionRequest",
  "responds": "Subscription"
 },
 "settleAiUsage": {
  "method": "POST",
  "path": "/ai-usage/settle",
  "contract": "subscription",
  "summary": "Turn metered AI interactions into a billable usage record",
  "permission": "PLATFORM_BILLING_MANAGE",
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
  "responds": null
 },
 "simulateCommercialPackage": {
  "method": "POST",
  "path": "/package-simulations",
  "contract": "subscription",
  "summary": "What this package would cost, and what it would provision",
  "permission": "PLATFORM_PLAN_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PackageSimulationRequest",
  "responds": "PackageSimulation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BillingReconciliation": {
  "type": "object",
  "description": "Boards 10.2 and 10.3. **The first invoice sets the tone for the relationship.**",
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "period": {
    "type": "string"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "unit": {
       "type": "string"
      },
      "meteredQuantity": {
       "type": "integer"
      },
      "billedQuantity": {
       "type": "integer"
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "variance": {
       "type": "integer"
      }
     }
    }
   },
   "meteredNotBilled": {
    "type": "integer"
   },
   "billedNotMetered": {
    "type": "integer"
   },
   "invoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "CellTier": {
  "type": "string",
  "enum": [
   "shared",
   "dedicated",
   "isolated",
   "clientHosted"
  ]
 },
 "DowngradeConflictProblem": {
  "x-ticvai-persistence": "none — error shape",
  "allOf": [
   {
    "$ref": "../shared/common.yaml#/components/schemas/Problem"
   },
   {
    "type": "object",
    "properties": {
     "modulesInUse": {
      "type": "array",
      "description": "Enabled by the tenant but not licensed by the target plan.",
      "items": {
       "type": "object",
       "properties": {
        "moduleKey": {
         "type": "string"
        },
        "displayName": {
         "type": "string"
        },
        "isEnabled": {
         "type": "boolean"
        }
       }
      }
     },
     "limitsExceeded": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "metric": {
         "$ref": "#/components/schemas/UsageMetric"
        },
        "currentUsage": {
         "type": "integer"
        },
        "targetLimit": {
         "type": "integer"
        }
       }
      }
     }
    }
   }
  ]
 },
 "InvoiceStatus": {
  "type": "string",
  "enum": [
   "draft",
   "issued",
   "paid",
   "overdue",
   "disputed",
   "cancelled"
  ]
 },
 "IssueCreditNoteRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "reasonCode",
   "settlement",
   "lines"
  ],
  "properties": {
   "reasonCode": {
    "type": "string",
    "enum": [
     "billingError",
     "serviceCredit",
     "disputeResolution",
     "goodwill",
     "other"
    ]
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "settlement": {
    "type": "string",
    "enum": [
     "offsetNextInvoice",
     "refund"
    ]
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "invoiceLineIndex"
     ],
     "properties": {
      "invoiceLineIndex": {
       "type": "integer",
       "minimum": 0,
       "description": "The line of the invoice being credited, by its position in `SubscriptionInvoice.lines`."
      },
      "quantity": {
       "type": "number",
       "minimum": 0,
       "nullable": true,
       "description": "Part of the line's quantity; null with `amount`, or for the whole line."
      },
      "amount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "nullable": true,
       "description": "Part of the line's amount, net of tax; null with `quantity`, or for the whole line."
      }
     }
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
 "PackageSimulation": {
  "type": "object",
  "description": "Boards 3.9 and 4.8. **Refused at quote time rather than at go-live.**",
  "properties": {
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "baseTier",
        "module",
        "addOn",
        "capacityPack",
        "overage",
        "professionalServices",
        "discount"
       ]
      },
      "label": {
       "type": "string"
      },
      "quantity": {
       "type": "number",
       "nullable": true
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "recurringTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "oneOffTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "contractTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "minimumGuarantee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
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
        "warning",
        "advisory"
       ]
      },
      "code": {
       "type": "string"
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "provisionable": {
    "type": "boolean"
   }
  }
 },
 "PackageSimulationRequest": {
  "type": "object",
  "required": [
   "tierCode"
  ],
  "properties": {
   "tierCode": {
    "type": "string"
   },
   "licensingModelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "moduleCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "venueCount": {
    "type": "integer",
    "default": 1
   },
   "projectedVolumes": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    }
   },
   "contractMonths": {
    "type": "integer",
    "default": 12
   },
   "billingCycle": {
    "type": "string",
    "nullable": true
   },
   "currency": {
    "type": "string",
    "nullable": true
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
 "RenewalAutoRenewalMembershipContinuityConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_renewal_policy (MembershipRenewalPolicy) (decided 29 September, data model DM4)",
  "description": "**What Renewal, Auto-Renewal & Membership Continuity Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "autoRenewEligible": {
    "type": "boolean",
    "description": "Eligible Products: this product may be auto-renewed. Default false (decided 29 September, readiness close-out)"
   },
   "autoRenewTermsVersion": {
    "type": "string",
    "description": "Consent Requirement: version of the auto-renewal terms the member accepts when opting in. Auto-renew is only ever switched on by the member's own explicit opt-in (MoM 25 Aug: subject to consent on terms and conditions), never pre-selected (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "cardOnFileRequired": {
    "type": "boolean",
    "description": "Payment Method Requirement: a tokenised card on file held by the payments module is required before auto-renew can be scheduled (MoM 25 Aug); the membership engine never holds card data. Default true (decided 29 September, readiness close-out)"
   },
   "preRenewalNoticeDays": {
    "type": "integer",
    "description": "Pre-Renewal Notification: days before the charge that the member is reminded, with the amount and how to opt out. Default 14, minimum 7 (decided 29 September, readiness close-out)"
   },
   "failureHandling": {
    "type": "string",
    "enum": [
     "gracePeriod",
     "manualAction",
     "expire"
    ],
    "description": "Failure Handling after the final retry (pack p.16: Payment Failed -> Retry -> Grace Period -> Manual Action -> Expired). Default gracePeriod (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "renewalModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "manual",
      "customerSelfService",
      "agentAssisted",
      "autoRenewal",
      "invitationOnly",
      "nonRenewable"
     ]
    },
    "description": "Renewal Modes (pack p.15); nonRenewable excludes the others"
   },
   "renewalWindowOpensDaysBefore": {
    "type": "integer",
    "description": "Renewal Window opens this many days before expiry. Default 60, the pack's example"
   },
   "renewalWindowClosesDaysAfter": {
    "type": "integer",
    "description": "Renewal Window closes this many days after expiry. Default 30, the pack's example"
   },
   "earlyRenewalStart": {
    "type": "string",
    "enum": [
     "immediately",
     "afterCurrentExpiry"
    ],
    "description": "Early Renewal (pack p.16): when the new period starts. Default afterCurrentExpiry, preserving remaining validity as the pack advises"
   },
   "renewalPriceBasis": {
    "type": "string",
    "enum": [
     "currentMembershipPrice",
     "protectedRenewalPrice",
     "renewalDiscount",
     "loyaltyRate",
     "fixedRenewalRate"
    ],
    "description": "Renewal Pricing (pack p.16); calculated by pricing (Area 10). Default currentMembershipPrice (decided 29 September, readiness close-out)"
   },
   "renewalPricingProfile": {
    "type": "string",
    "description": "Renewal pricing profile id in pricing (Area 10)",
    "nullable": true
   },
   "retryIntervalsDays": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "description": "Retry Policy: days between failed auto-renew payment attempts. Default [2, 3], the pack's example (p.31)"
   },
   "renewalGraceDays": {
    "type": "integer",
    "description": "Days a failed renewal stays in Renewal Grace before failureHandling applies. Default 7 (decided 29 September, readiness close-out)"
   },
   "revalidateOnRenewal": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "age",
      "residency",
      "membershipStatus",
      "outstandingBalance",
      "qualification",
      "corporateAssociation"
     ]
    },
    "description": "Renewal Eligibility (pack p.16): what is revalidated at renewal"
   },
   "tierMovementAtRenewal": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "sameTierOnly",
      "upgradeAllowed",
      "downgradeAllowed",
      "suggestedTier"
     ]
    },
    "description": "Tier Movement (pack p.16)"
   },
   "cancellationPolicyId": {
    "type": "string",
    "description": "Cancellation/refund policy from the central policy management (MoM 25 Aug: refund and cancellation rules are managed centrally). Empty means no refund on cancellation unless the commercial team configures one; cancelling always stops the next auto-renew charge (decided 29 September, readiness close-out)",
    "nullable": true
   }
  }
 },
 "RenewalAutoRenewalMembershipContinuityConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Renewal, Auto-Renewal & Membership Continuity Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "autoRenewEligible": {
    "type": "boolean",
    "description": "Eligible Products: this product may be auto-renewed. Default false (decided 29 September, readiness close-out)"
   },
   "autoRenewTermsVersion": {
    "type": "string",
    "description": "Consent Requirement: version of the auto-renewal terms the member accepts when opting in. Auto-renew is only ever switched on by the member's own explicit opt-in (MoM 25 Aug: subject to consent on terms and conditions), never pre-selected (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "cardOnFileRequired": {
    "type": "boolean",
    "description": "Payment Method Requirement: a tokenised card on file held by the payments module is required before auto-renew can be scheduled (MoM 25 Aug); the membership engine never holds card data. Default true (decided 29 September, readiness close-out)"
   },
   "preRenewalNoticeDays": {
    "type": "integer",
    "description": "Pre-Renewal Notification: days before the charge that the member is reminded, with the amount and how to opt out. Default 14, minimum 7 (decided 29 September, readiness close-out)"
   },
   "failureHandling": {
    "type": "string",
    "enum": [
     "gracePeriod",
     "manualAction",
     "expire"
    ],
    "description": "Failure Handling after the final retry (pack p.16: Payment Failed -> Retry -> Grace Period -> Manual Action -> Expired). Default gracePeriod (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "renewalModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "manual",
      "customerSelfService",
      "agentAssisted",
      "autoRenewal",
      "invitationOnly",
      "nonRenewable"
     ]
    },
    "description": "Renewal Modes (pack p.15); nonRenewable excludes the others"
   },
   "renewalWindowOpensDaysBefore": {
    "type": "integer",
    "description": "Renewal Window opens this many days before expiry. Default 60, the pack's example"
   },
   "renewalWindowClosesDaysAfter": {
    "type": "integer",
    "description": "Renewal Window closes this many days after expiry. Default 30, the pack's example"
   },
   "earlyRenewalStart": {
    "type": "string",
    "enum": [
     "immediately",
     "afterCurrentExpiry"
    ],
    "description": "Early Renewal (pack p.16): when the new period starts. Default afterCurrentExpiry, preserving remaining validity as the pack advises"
   },
   "renewalPriceBasis": {
    "type": "string",
    "enum": [
     "currentMembershipPrice",
     "protectedRenewalPrice",
     "renewalDiscount",
     "loyaltyRate",
     "fixedRenewalRate"
    ],
    "description": "Renewal Pricing (pack p.16); calculated by pricing (Area 10). Default currentMembershipPrice (decided 29 September, readiness close-out)"
   },
   "renewalPricingProfile": {
    "type": "string",
    "description": "Renewal pricing profile id in pricing (Area 10)",
    "nullable": true
   },
   "retryIntervalsDays": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "description": "Retry Policy: days between failed auto-renew payment attempts. Default [2, 3], the pack's example (p.31)"
   },
   "renewalGraceDays": {
    "type": "integer",
    "description": "Days a failed renewal stays in Renewal Grace before failureHandling applies. Default 7 (decided 29 September, readiness close-out)"
   },
   "revalidateOnRenewal": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "age",
      "residency",
      "membershipStatus",
      "outstandingBalance",
      "qualification",
      "corporateAssociation"
     ]
    },
    "description": "Renewal Eligibility (pack p.16): what is revalidated at renewal"
   },
   "tierMovementAtRenewal": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "sameTierOnly",
      "upgradeAllowed",
      "downgradeAllowed",
      "suggestedTier"
     ]
    },
    "description": "Tier Movement (pack p.16)"
   },
   "cancellationPolicyId": {
    "type": "string",
    "description": "Cancellation/refund policy from the central policy management (MoM 25 Aug: refund and cancellation rules are managed centrally). Empty means no refund on cancellation unless the commercial team configures one; cancelling always stops the next auto-renew charge (decided 29 September, readiness close-out)",
    "nullable": true
   }
  }
 },
 "RenewalOperationsAutoRenewalManagementSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Renewal Operations & Auto-Renewal Management.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "renewalNotOpen": {
    "type": "integer",
    "description": "Renewal Not Open"
   },
   "renewalEligible": {
    "type": "integer",
    "description": "Renewal Eligible"
   },
   "renewalInvitationSent": {
    "type": "integer",
    "description": "Renewal Invitation Sent"
   },
   "renewalStarted": {
    "type": "integer",
    "description": "Renewal Started"
   },
   "paymentPending": {
    "type": "integer",
    "description": "Payment Pending"
   },
   "renewed": {
    "type": "integer",
    "description": "Renewed"
   },
   "autoRenewScheduled": {
    "type": "integer",
    "description": "Auto-Renew Scheduled"
   },
   "autoRenewFailed": {
    "type": "integer",
    "description": "Auto-Renew Failed"
   },
   "gracePeriod": {
    "type": "integer",
    "description": "Grace Period"
   },
   "expiredWithoutRenewal": {
    "type": "integer",
    "description": "Expired Without Renewal"
   }
  }
 },
 "RenewalOperationsAutoRenewalManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Renewal Operations & Auto-Renewal Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "member": {
    "type": "string",
    "description": "Member"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "tier": {
    "type": "string",
    "description": "Tier"
   },
   "expiry": {
    "type": "string",
    "format": "date",
    "description": "Expiry"
   },
   "renewalWindow": {
    "type": "object",
    "description": "Renewal Window",
    "properties": {
     "opens": {
      "type": "string",
      "format": "date"
     },
     "closes": {
      "type": "string",
      "format": "date"
     }
    }
   },
   "renewalPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Renewal Price from pricing (Area 10)"
   },
   "autoRenew": {
    "type": "boolean",
    "description": "Auto-Renew: the member has explicitly opted in"
   },
   "paymentMethodStatus": {
    "type": "string",
    "description": "Payment Method Status: none, valid, expiringSoon, expired or failed"
   },
   "eligibility": {
    "type": "string",
    "enum": [
     "eligible",
     "notEligible",
     "reviewRequired"
    ],
    "description": "Eligibility for renewal"
   },
   "renewalStatus": {
    "type": "string",
    "description": "Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled, autoRenewFailed, gracePeriod or expiredWithoutRenewal (pack p.30 Renewal Pipeline)"
   },
   "membershipStatus": {
    "type": "string",
    "description": "Current membership status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue GuestMembership.status; states/guest-membership-status.yaml): frozen is the member's pause and extends validity, suspended is a sanction and does not"
   },
   "outstandingIssues": {
    "type": "string",
    "description": "Outstanding Issues",
    "nullable": true
   },
   "autoRenewConsentAt": {
    "type": "string",
    "format": "date-time",
    "description": "Consent: when the member accepted the auto-renewal terms; empty means no consent and auto-renew will not run",
    "nullable": true
   },
   "membershipVersion": {
    "type": "integer",
    "description": "Membership Version the renewal will be on"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "preNotificationSentAt": {
    "type": "string",
    "format": "date-time",
    "description": "Pre-renewal reminder sent",
    "nullable": true
   },
   "paymentAttempts": {
    "type": "integer",
    "description": "Auto-renew payment attempts so far"
   },
   "nextAttemptAt": {
    "type": "string",
    "format": "date-time",
    "description": "Next scheduled payment attempt",
    "nullable": true
   }
  }
 },
 "SetSubscriptionRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "planId"
  ],
  "properties": {
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planVersion": {
    "type": "string",
    "description": "Defaults to the current version."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1))."
   },
   "prorate": {
    "type": "boolean",
    "default": true,
    "description": "An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). Kept so a preview can show the unprorated figure; `setSubscription` applies the rule whatever is sent."
   },
   "note": {
    "type": "string",
    "maxLength": 500
   }
  }
 },
 "Subscription": {
  "x-ticvai-persistence": "subscription.contract",
  "type": "object",
  "required": [
   "tenantId",
   "planId",
   "planVersion",
   "status",
   "startsAt"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planName": {
    "type": "string"
   },
   "planVersion": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "trial",
     "active",
     "pastDue",
     "cancelled",
     "expired"
    ]
   },
   "startsAt": {
    "type": "string",
    "format": "date"
   },
   "renewsAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "cancelledAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "scheduledChange": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.",
    "properties": {
     "planId": {
      "type": "string",
      "format": "uuid"
     },
     "planVersion": {
      "type": "string"
     },
     "effectiveFrom": {
      "type": "string",
      "format": "date",
      "description": "Always the `renewsAt` it was scheduled against."
     }
    }
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingPeriod": {
    "type": "string"
   }
  }
 },
 "SubscriptionCreditNote": {
  "type": "object",
  "x-ticvai-persistence": "control.credit_note + control.credit_note_line",
  "description": "**A credit note against one tenant invoice** (20.7.7, 29 September build): its own number, lines, tax and total. The invoice it credits is never edited.",
  "required": [
   "id",
   "creditNoteNumber",
   "invoiceId",
   "tenantId",
   "reasonCode",
   "settlement",
   "total",
   "issuedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "creditNoteNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Gapless, per issuing legal entity, in its own sequence** (the R152 rule for invoices, decided 28 September, applied to credit notes): assigned at issue, never reused."
   },
   "invoiceId": {
    "type": "string",
    "description": "The invoice credited."
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "reasonCode": {
    "type": "string",
    "enum": [
     "billingError",
     "serviceCredit",
     "disputeResolution",
     "goodwill",
     "other"
    ]
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "settlement": {
    "type": "string",
    "enum": [
     "offsetNextInvoice",
     "refund"
    ]
   },
   "settlementStatus": {
    "type": "string",
    "enum": [
     "pending",
     "offset",
     "refunded"
    ],
    "readOnly": true,
    "description": "`offset` once a later invoice has taken it; `refunded` once the refund is recorded."
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "invoiceLineIndex": {
       "type": "integer"
      },
      "description": {
       "type": "string"
      },
      "quantity": {
       "type": "number",
       "nullable": true
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "subtotal": {
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   }
  }
 },
 "SubscriptionInvoice": {
  "x-ticvai-persistence": "control.invoice + control.invoice_line",
  "type": "object",
  "required": [
   "id",
   "invoiceNumber",
   "tenantId",
   "periodStart",
   "periodEnd",
   "status",
   "total"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "invoiceNumber": {
    "type": "string",
    "readOnly": true,
    "description": "A tax invoice number, so **gapless, per legal entity** (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity that issues it, assigned when the invoice is issued, never reused. A cancelled invoice keeps its number.\n"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "periodStart": {
    "type": "string",
    "format": "date"
   },
   "periodEnd": {
    "type": "string",
    "format": "date"
   },
   "status": {
    "$ref": "#/components/schemas/InvoiceStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "description": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "basePlan",
        "module",
        "addOn",
        "overage",
        "metered",
        "oneOff",
        "credit"
       ],
       "description": "`module`, one per licensed module at its platform price, and `metered`, usage such as AI tokens (decided 29 September)."
      },
      "moduleCode": {
       "type": "string",
       "nullable": true,
       "description": "The module a `module` or `metered` line charges for."
      },
      "audience": {
       "type": "string",
       "enum": [
        "staff",
        "guest"
       ],
       "nullable": true,
       "description": "For an AI `metered` line, whose usage it is."
      },
      "metric": {
       "$ref": "#/components/schemas/UsageMetric"
      },
      "quantity": {
       "type": "number"
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "subtotal": {
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "planVersionUsed": {
    "type": "string",
    "description": "Priced against the version the tenant is subscribed to, not the latest."
   },
   "creditedTotal": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "The sum of the credit notes issued against this invoice (`issueCreditNote`); the invoice itself is never edited. Null with none."
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "paidAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "SubscriptionPlanRecommendation": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from control.usage_record, the plan, tier and add-on limits and capacity packs, priced as simulateCommercialPackage prices",
  "description": "One plan-fit move for a tenant, priced against staying as it is (20.8.4, 20.8.5; decided 29 September, build pass, group G2).",
  "required": [
   "kind",
   "reason",
   "projectedMonthlyCost"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "upgrade",
     "downgrade",
     "addModule",
     "removeModule",
     "removeAddOn",
     "capacityPack"
    ]
   },
   "targetPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The tier to move to, for `upgrade` and `downgrade`."
   },
   "moduleCode": {
    "type": "string",
    "nullable": true,
    "description": "For `addModule` and `removeModule`."
   },
   "addOnCode": {
    "type": "string",
    "nullable": true,
    "description": "For `removeAddOn`."
   },
   "billableUnit": {
    "type": "string",
    "nullable": true,
    "description": "The unit that drives it (for `upgrade`, `downgrade` and `capacityPack`), as `getLicenceEnforcement` names it."
   },
   "capacityPackSize": {
    "type": "integer",
    "nullable": true,
    "description": "For `capacityPack`, the pack size that covers the projected overage."
   },
   "projectedMonthlyCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "projectedSaving": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Against staying as it is over the horizon, monthly. Set where the move saves money."
   },
   "projectedAddedCost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Where the move costs more than today but less than the alternative named in `comparedWith`."
   },
   "comparedWith": {
    "type": "string",
    "enum": [
     "currentPackage",
     "projectedOverage",
     "nextTier",
     "capacityPack"
    ],
    "description": "What the move is cheaper than. An `upgrade` is compared with paying the projected overage; a `capacityPack` with the next tier."
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "description": "One sentence a person can repeat to the customer."
   },
   "basis": {
    "type": "object",
    "description": "The numbers it rests on.",
    "properties": {
     "usageWindowDays": {
      "type": "integer"
     },
     "usedAverage": {
      "type": "number",
      "nullable": true
     },
     "usedPeak": {
      "type": "number",
      "nullable": true
     },
     "projectedPeak": {
      "type": "number",
      "nullable": true
     },
     "currentLimit": {
      "type": "number",
      "nullable": true
     },
     "targetLimit": {
      "type": "number",
      "nullable": true
     },
     "lastUsedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "For `removeModule` and `removeAddOn`, the last metered use; null for never."
     }
    }
   },
   "applyWith": {
    "type": "string",
    "enum": [
     "setSubscription",
     "addCapacityPack"
    ],
    "description": "The operation a person uses to carry it out (after `previewSubscriptionChange` for `setSubscription`)."
   }
  }
 },
 "SubscriptionPreview": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "canApply",
   "priceChange"
  ],
  "properties": {
   "canApply": {
    "type": "boolean"
   },
   "priceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "proratedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "modulesGained": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modulesLost": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "conflicts": {
    "$ref": "#/components/schemas/DowngradeConflictProblem"
   },
   "cellTierChange": {
    "type": "object",
    "nullable": true,
    "properties": {
     "from": {
      "$ref": "#/components/schemas/CellTier"
     },
     "to": {
      "$ref": "#/components/schemas/CellTier"
     },
     "requiresMigration": {
      "type": "boolean"
     }
    }
   }
  }
 },
 "UsageMetric": {
  "type": "string",
  "enum": [
   "venues",
   "workstations",
   "activeUsers",
   "devices",
   "brandedApps",
   "aiTokens",
   "apiCalls",
   "storageGb",
   "transactions",
   "guestProfiles"
  ]
 }
}
```
