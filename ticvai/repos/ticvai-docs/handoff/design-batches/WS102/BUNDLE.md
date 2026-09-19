# WS102 — Subscription Licensing AI Self Service board 5

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
| `ADM-409` | Purchase / Trial Journey Selection | listDetail | 0 | 0 | — |
| `ADM-410` | Contract & Billing Cycle Selection | listDetail | 0 | 0 | — |
| `ADM-411` | Billing & Legal Entity Information | listDetail | 0 | 0 | — |
| `ADM-412` | Payment Method & Settlement Setup | listDetail | 0 | 0 | — |
| `ADM-413` | Trial Configuration & Conversion Rules | configEditor | 0 | 0 | — |
| `ADM-414` | Order & Commercial Pricing Review | listDetail | 0 | 0 | — |
| `ADM-415` | Commercial Agreement, Billable Definition & Customer Acceptance | listDetail | 0 | 0 | — |
| `ADM-416` | Payment, Contract & Commercial Validation | listDetail | 0 | 0 | — |
| `ADM-417` | Subscription Confirmation & Commercial Activation | listDetail | 0 | 0 | — |
| `ADM-418` | Subscription Lifecycle & Trial-to-Paid Handoff | listDetail | 0 | 0 | — |

## Thin screens in this batch

**ADM-409, ADM-410, ADM-411, ADM-412, ADM-414, ADM-415, ADM-416, ADM-417 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-409",
  "name": "Purchase / Trial Journey Selection",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "1",
   "page": 58
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/purchase-trial-journey-selection-adm-409",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/PurchaseTrialJourneySelection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-410",
    "ADM-411",
    "ADM-412",
    "ADM-413",
    "ADM-414",
    "ADM-415",
    "ADM-416",
    "ADM-417",
    "ADM-418"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "ADM-410",
     "trigger": "Contract & Billing Cycle Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-411",
     "trigger": "Billing & Legal Entity Information",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-412",
     "trigger": "Payment Method & Settlement Setup",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-413",
     "trigger": "Trial Configuration & Conversion Rules",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-414",
     "trigger": "Order & Commercial Pricing Review",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-415",
     "trigger": "Commercial Agreement, Billable Definition & Customer Acceptance",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-416",
     "trigger": "Payment, Contract & Commercial Validation",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-417",
     "trigger": "Subscription Confirmation & Commercial Activation",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-418",
     "trigger": "Subscription Lifecycle & Trial-to-Paid Handoff",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine how the customer enters the commercial activation journey.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 58"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 58"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The purchase trial journey list.",
   "error": "Could not load. Names which read failed and leaves the purchase trial journey untouched.",
   "emptyFirstRun": "No purchase trial journey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the purchase trial journey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-409"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-410",
  "name": "Contract & Billing Cycle Selection",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "2",
   "page": 59
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/contract-billing-cycle-selection-adm-410",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ContractBillingCycleSelection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the contractual duration and billing/reconciliation cycle.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Custom Term. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 59 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 59"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 59"
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
       "label": "Custom Term",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 59 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The contract billing cycle list.",
   "error": "Could not load. Names which read failed and leaves the contract billing cycle untouched.",
   "emptyFirstRun": "No contract billing cycle yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the contract billing cycle are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-410"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 59. 0 of 0 labels bound to a contract property; 1 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-411",
  "name": "Billing & Legal Entity Information",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "3",
   "page": 60
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/billing-legal-entity-information-adm-411",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/BillingLegalEntityInformation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Capture the legally correct customer and billing information.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Commercial Customer ≠ Operating Venue, Validate Entity / Save / Continue. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 60 §Allow"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 60"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 60"
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
       "label": "Commercial Customer ≠ Operating Venue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 60 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate Entity / Save / Continue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 60 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The billing legal entity list.",
   "error": "Could not load. Names which read failed and leaves the billing legal entity untouched.",
   "emptyFirstRun": "No billing legal entity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the billing legal entity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-411"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 60. 0 of 0 labels bound to a contract property; 2 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-412",
  "name": "Payment Method & Settlement Setup",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "4",
   "page": 61
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/payment-method-settlement-setup-adm-412",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/PaymentMethodSettlementSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how TICVAI collects its fees.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Credit / Debit Card, Bank Transfer, Other Approved Method. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 61 §Support"
   },
   {
    "operation": null,
    "why": "**Payment Method & Settlement Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 61"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 61"
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
       "label": "Credit / Debit Card",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 61 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Bank Transfer",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 61 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Other Approved Method",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 61 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment method settlement list.",
   "error": "Could not load. Names which read failed and leaves the payment method settlement untouched.",
   "emptyFirstRun": "No payment method settlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment method settlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-412"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 61. 0 of 0 labels bound to a contract property; 3 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-413",
  "name": "Trial Configuration & Conversion Rules",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "5",
   "page": 62
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/trial-configuration-conversion-rules-adm-413",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/TrialConfigurationConversionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Trial Configuration; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure trial terms where the selected package is trial-eligible. Not every commercial model needs to support trials.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Trial Start",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Trial End",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Duration",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Modules Enabled",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "POS Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Access Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "User Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Transaction Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Ticket Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "API Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Storage Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Trial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Free Trial",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Paid Trial",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Trial Credit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Limited Usage",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full Package Trial",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 62 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The trial conversion rules configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the trial conversion rules untouched.",
   "emptyFirstRun": "No trial conversion rules configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-413"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 62. 0 of 0 labels bound to a contract property; 16 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-414",
  "name": "Order & Commercial Pricing Review",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "6",
   "page": 64
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/order-commercial-pricing-review-adm-414",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/OrderCommercialPricingReview.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Show the complete financial arrangement before contractual acceptance. This screen must adapt dynamically to the commercial model. Example — Per Ticket + Minimum Guarantee",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 64 §Show"
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
       "label": "Every order commercial pricing",
       "columns": [
        "Discount Type",
        "Value",
        "Period",
        "Approved By",
        "Expiry"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 64 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order commercial pricing",
       "bindsTo": null,
       "columns": [
        "Discount Type",
        "Value",
        "Period",
        "Approved By",
        "Expiry"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Rate”, “Expected Volume”, “Included Modules”, “Technical Capacity”, “Show where applicable”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 64 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order commercial pricing list.",
   "error": "Could not load. Names which read failed and leaves the order commercial pricing untouched.",
   "emptyFirstRun": "No order commercial pricing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order commercial pricing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Discount Type",
    "Value",
    "Period",
    "Approved By",
    "Expiry"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-414"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 64. 0 of 5 labels bound to a contract property; 5 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-415",
  "name": "Commercial Agreement, Billable Definition & Customer Acceptance",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "7",
   "page": 65
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/commercial-agreement-billable-definition-customer-accept-adm-415",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CommercialAgreementBillableDefinitionCustomerAcc.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "This becomes one of the most important revised screens. The customer must understand and formally accept what TICVAI considers billable.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 65 §Display"
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
       "label": "Every commercial agreement billable",
       "columns": [
        "Commercial Model",
        "Contracted Rate",
        "Minimum Guarantee",
        "Guarantee Period",
        "Billing Cycle",
        "Contract Duration",
        "Renewal",
        "Payment Terms"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 65 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected commercial agreement billable",
       "bindsTo": null,
       "columns": [
        "Commercial Model",
        "Contracted Rate",
        "Minimum Guarantee",
        "Guarantee Period",
        "Billing Cycle",
        "Contract Duration",
        "Renewal",
        "Payment Terms"
       ],
       "notes": "The pack groups this record's detail under its own headings: “For a transaction contract”, “For a per-ticket contract”, “Customer confirms”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 65 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial agreement billable list.",
   "error": "Could not load. Names which read failed and leaves the commercial agreement billable untouched.",
   "emptyFirstRun": "No commercial agreement billable yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial agreement billable are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Commercial Model",
    "Contracted Rate",
    "Minimum Guarantee",
    "Guarantee Period",
    "Billing Cycle",
    "Contract Duration"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-415"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 65. 0 of 8 labels bound to a contract property; 14 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-416",
  "name": "Payment, Contract & Commercial Validation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "8",
   "page": 66
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/payment-contract-commercial-validation-adm-416",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/PaymentContractCommercialValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Perform final checks before creating the active subscription.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 66"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 66"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The payment contract commercial list.",
   "error": "Could not load. Names which read failed and leaves the payment contract commercial untouched.",
   "emptyFirstRun": "No payment contract commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment contract commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-416"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 66. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-417",
  "name": "Subscription Confirmation & Commercial Activation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "9",
   "page": 67
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/subscription-confirmation-commercial-activation-adm-417",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/SubscriptionConfirmationCommercialActivation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the formal active subscription/contract record after successful validation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 67"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 67"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The subscription confirmation commercial list.",
   "error": "Could not load. Names which read failed and leaves the subscription confirmation commercial untouched.",
   "emptyFirstRun": "No subscription confirmation commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription confirmation commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-417"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 67. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-418",
  "name": "Subscription Lifecycle & Trial-to-Paid Handoff",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "10",
   "page": 69
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/subscription-lifecycle-trial-to-paid-handoff-adm-418",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/SubscriptionLifecycleTrialToPaidHandoff.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-409"
   ],
   "exitTo": [
    "ADM-409"
   ],
   "transitions": [
    {
     "to": "ADM-409",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show; Track) and no metric row",
  "purpose": "Manage the immediate commercial lifecycle after purchase or trial activation and ensure clean handoff to operational provisioning.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Retry / Investigate / Assign / Escalate, Revised Board 5 — Commercial Model Behavior. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 69 §Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 69 §Show"
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
       "label": "Every subscription lifecycle trial-to-paid",
       "columns": [
        "Trial Usage",
        "Trial Ticket Volume",
        "Trial Expiry",
        "Conversion Package",
        "Commercial Model",
        "Paid Start Date",
        "First Billing Date",
        "Package Approval",
        "Customer Acceptance",
        "Payment",
        "Subscription Creation",
        "Commercial Activation",
        "License Request",
        "Provisioning Request"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 69 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected subscription lifecycle trial-to-paid",
       "bindsTo": null,
       "columns": [
        "Trial Usage",
        "Trial Ticket Volume",
        "Trial Expiry",
        "Conversion Package",
        "Commercial Model",
        "Paid Start Date",
        "First Billing Date",
        "Package Approval",
        "Customer Acceptance",
        "Payment",
        "Subscription Creation",
        "Commercial Activation",
        "License Request",
        "Provisioning Request"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Draft”, “Tier-Based Fixed recurring subscription”, “Fixed Fixed contractual value”, “For example”, “The key principle is”, “Board Flow”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 69 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Retry / Investigate / Assign / Escalate",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 69 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Revised Board 5 — Commercial Model Behavior",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 69 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The subscription lifecycle trial-to-paid list.",
   "error": "Could not load. Names which read failed and leaves the subscription lifecycle trial-to-paid untouched.",
   "emptyFirstRun": "No subscription lifecycle trial-to-paid yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription lifecycle trial-to-paid are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Trial Usage",
    "Trial Ticket Volume",
    "Trial Expiry",
    "Conversion Package",
    "Commercial Model",
    "Paid Start Date"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-418"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 69. 0 of 14 labels bound to a contract property; 16 of 88 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
