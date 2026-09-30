# P17-purchase-activation-01 — P17 · Purchase & Activation

**7 screens · 6 operations · 14 schemas · 6 permissions**

Platform P17 TICVAI Sign-up · ships as **ticvai-control** ·
public audience · web ·
online only

## Who this is for

**public on web.** Everything below is how you know what is
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
  `ACCOUNT_CONFIGURE, PLATFORM_CELL_MANAGE, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SGN-018` | Purchase / Trial Journey Selection | listDetail | 1 | 0 | — |
| `SGN-019` | Contract & Billing Cycle Selection | listDetail | 1 | 0 | — |
| `SGN-020` | Billing & Legal Entity Information | listDetail | 1 | 0 | — |
| `SGN-021` | Payment Method & Settlement Setup | listDetail | 1 | 0 | — |
| `SGN-022` | Order & Commercial Pricing Review | listDetail | 1 | 0 | — |
| `SGN-023` | Commercial Agreement, Billable Definition & Customer Acceptance | listDetail | 1 | 0 | — |
| `SGN-024` | Subscription Confirmation & Commercial Activation | listDetail | 1 | 0 | — |

## Thin screens in this batch

**SGN-018, SGN-019, SGN-020, SGN-021, SGN-022, SGN-023, SGN-024 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SGN-018",
  "name": "Purchase / Trial Journey Selection",
  "module": "Purchase & Activation",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-409",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "1",
   "page": 58
  },
  "implementation": {
   "app": "signup-web",
   "route": "/purchase-activation/purchase-trial-journey-selection-sgn-018",
   "component": "apps/signup-web/src/routes/purchase-activation/PurchaseTrialJourneySelection.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-409`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-018"
  },
  "purpose": "Determine how the customer enters the commercial activation journey.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setTrialConfiguration",
       "label": "Save trial configuration",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setTrialConfiguration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The purchase trial journey list.",
   "error": "Could not load. Names which read failed and leaves the purchase trial journey untouched.",
   "emptyFirstRun": "No purchase trial journey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the purchase trial journey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [
   {
    "operationId": "setTrialConfiguration",
    "contract": "subscription",
    "purpose": "Purchase or trial",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-011",
    "SGN-019"
   ],
   "exitTo": [
    "SGN-011",
    "SGN-019"
   ],
   "transitions": [
    {
     "to": "SGN-011",
     "trigger": "Back to Recommended Package Overview",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-019",
     "trigger": "Contract & Billing Cycle Selection",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-019",
  "name": "Contract & Billing Cycle Selection",
  "module": "Purchase & Activation",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-410",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "2",
   "page": 59
  },
  "implementation": {
   "app": "signup-web",
   "route": "/purchase-activation/contract-billing-cycle-selection-sgn-019",
   "component": "apps/signup-web/src/routes/purchase-activation/ContractBillingCycleSelection.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-410`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-019"
  },
  "purpose": "Define the contractual duration and billing/reconciliation cycle.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
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
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSubscription"
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
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [
   {
    "operationId": "setSubscription",
    "contract": "subscription",
    "purpose": "Contract and billing cycle",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 59. 0 of 0 labels bound to a contract property; 1 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-018",
    "SGN-020"
   ],
   "exitTo": [
    "SGN-018",
    "SGN-020"
   ],
   "transitions": [
    {
     "to": "SGN-018",
     "trigger": "Back to Purchase / Trial Journey Selection",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-020",
     "trigger": "Billing & Legal Entity Information",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "session"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-020",
  "name": "Billing & Legal Entity Information",
  "module": "Purchase & Activation",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-411",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "3",
   "page": 60
  },
  "implementation": {
   "app": "signup-web",
   "route": "/purchase-activation/billing-legal-entity-information-sgn-020",
   "component": "apps/signup-web/src/routes/purchase-activation/BillingLegalEntityInformation.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-411`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-020"
  },
  "purpose": "Capture the legally correct customer and billing information.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
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
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The billing legal entity list.",
   "error": "Could not load. Names which read failed and leaves the billing legal entity untouched.",
   "emptyFirstRun": "No billing legal entity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the billing legal entity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [
   {
    "operationId": "createLegalEntity",
    "contract": "finance",
    "purpose": "Billing and legal entity",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 60. 0 of 0 labels bound to a contract property; 2 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-019",
    "SGN-021"
   ],
   "exitTo": [
    "SGN-019",
    "SGN-021"
   ],
   "transitions": [
    {
     "to": "SGN-019",
     "trigger": "Back to Contract & Billing Cycle Selection",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-021",
     "trigger": "Payment Method & Settlement Setup",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-021",
  "name": "Payment Method & Settlement Setup",
  "module": "Purchase & Activation",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "4",
   "page": 61
  },
  "implementation": {
   "app": "signup-web",
   "route": "/purchase-activation/payment-method-settlement-setup-sgn-021",
   "component": "apps/signup-web/src/routes/purchase-activation/PaymentMethodSettlementSetup.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-412`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165).\n\n**Diverged from ADM-412 on 28 September; no longer `sameAs`.** ADM-412 gained the platform-staff tenant picker and grant step (audit R098), which does not apply to a prospect with no account and no tenant yet, so `tools/applied/apply-subscription-placement.py` no longer keeps the two in step. The payment-methods change of audit R275 (a) is applied here by hand.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-021"
  },
  "purpose": "Configure how TICVAI collects its fees.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Payment methods",
       "bindsTo": "PaymentProvider",
       "columns": [
        "PaymentProvider.supportedMethods"
       ],
       "operation": "setPaymentProvider",
       "notes": "**The methods follow the contract (decided 28 September, audit R275 (a))**: the options are the `PaymentProvider.supportedMethods` enum that `setPaymentProvider` accepts. The pack's Credit / Debit Card is `card` and its Bank Transfer is `bankTransfer`; its Other Approved Method is not in the contract and is dropped.",
       "provenance": "contract orders.yaml PUT /payment-providers"
      },
      {
       "kind": "primaryButton",
       "label": "Save payment provider",
       "operation": "setPaymentProvider",
       "provenance": "contract orders.yaml PUT /payment-providers"
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
   "loading": "The payment method settlement list.",
   "error": "Could not load. Names which read failed and leaves the payment method settlement untouched.",
   "emptyFirstRun": "No payment method settlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment method settlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
  "gaps": [
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
  "apis": [
   {
    "operationId": "setPaymentProvider",
    "contract": "orders",
    "purpose": "Payment and settlement setup",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 61. 0 of 0 labels bound to a contract property; 3 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-020",
    "SGN-022"
   ],
   "exitTo": [
    "SGN-020",
    "SGN-022"
   ],
   "transitions": [
    {
     "to": "SGN-020",
     "trigger": "Back to Billing & Legal Entity Information",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-022",
     "trigger": "Order & Commercial Pricing Review",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-022",
  "name": "Order & Commercial Pricing Review",
  "module": "Purchase & Activation",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-414",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "6",
   "page": 64
  },
  "implementation": {
   "app": "signup-web",
   "route": "/purchase-activation/order-commercial-pricing-review-sgn-022",
   "component": "apps/signup-web/src/routes/purchase-activation/OrderCommercialPricingReview.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-414`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-022"
  },
  "purpose": "Show the complete financial arrangement before contractual acceptance. This screen must adapt dynamically to the commercial model. Example — Per Ticket + Minimum Guarantee",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
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
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 64 §Show"
   }
  ],
  "apis": [
   {
    "operationId": "previewSubscriptionChange",
    "contract": "subscription",
    "purpose": "Order and pricing review",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 64. 0 of 5 labels bound to a contract property; 5 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "preloaded": [
    "Discount Type",
    "Value",
    "Period",
    "Approved By",
    "Expiry"
   ],
   "params": [
    {
     "name": "tenantId",
     "from": "session"
    }
   ]
  },
  "navigation": {
   "entryFrom": [
    "SGN-021",
    "SGN-023"
   ],
   "exitTo": [
    "SGN-021",
    "SGN-023"
   ],
   "transitions": [
    {
     "to": "SGN-021",
     "trigger": "Back to Payment Method & Settlement Setup",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-023",
     "trigger": "Commercial Agreement, Billable Definition & Customer Acceptance",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-023",
  "name": "Commercial Agreement, Billable Definition & Customer Acceptance",
  "module": "Purchase & Activation",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-415",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "7",
   "page": 65
  },
  "implementation": {
   "app": "signup-web",
   "route": "/purchase-activation/commercial-agreement-billable-definition-customer-accept-sgn-023",
   "component": "apps/signup-web/src/routes/purchase-activation/CommercialAgreementBillableDefinitionCustomerAcc.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-415`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-023"
  },
  "purpose": "This becomes one of the most important revised screens. The customer must understand and formally accept what TICVAI considers billable.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
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
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 65 §Display"
   }
  ],
  "apis": [
   {
    "operationId": "setAgreementContractTerm",
    "contract": "subscription",
    "purpose": "Agreement and acceptance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 65. 0 of 8 labels bound to a contract property; 14 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "navigation": {
   "entryFrom": [
    "SGN-022"
   ],
   "exitTo": [
    "SGN-022",
    "SGN-024"
   ],
   "transitions": [
    {
     "to": "SGN-022",
     "trigger": "Back to Order & Commercial Pricing Review",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026",
     "back": true
    },
    {
     "to": "SGN-024",
     "trigger": "Subscription Confirmation & Commercial Activation",
     "provenance": "structural — the book's own journey, 2.1 \"Journey Preview\", 11 September 2026"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SGN-024",
  "name": "Subscription Confirmation & Commercial Activation",
  "module": "Purchase & Activation",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "sameAs": "ADM-417",
   "book": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "5",
   "number": "9",
   "page": 67
  },
  "implementation": {
   "app": "signup-web",
   "route": "/purchase-activation/subscription-confirmation-commercial-activation-sgn-024",
   "component": "apps/signup-web/src/routes/purchase-activation/SubscriptionConfirmationCommercialActivation.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "notes": "The self-service form of `ADM-417`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P17 TICVAI Sign-up.dc.html#sgn-024"
  },
  "purpose": "Create the formal active subscription/contract record after successful validation.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setSubscription",
       "label": "Save subscription",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSubscription"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The subscription confirmation commercial list.",
   "error": "Could not load. Names which read failed and leaves the subscription confirmation commercial untouched.",
   "emptyFirstRun": "No subscription confirmation commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription confirmation commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [
   {
    "operationId": "setSubscription",
    "contract": "subscription",
    "purpose": "Create the subscription",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 67. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "SGN-023"
   ],
   "transitions": [
    {
     "to": "BO-594",
     "trigger": "Environment Ready & Handoff to AI Setup",
     "provenance": "structural — the book's board flow, \"Board 5 — Subscription Activated → Board 6 → Board 7\", 11 September 2026",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "session"
    }
   ]
  },
  "_platform": {
   "code": "P17",
   "audience": "public",
   "formFactor": "web",
   "shortName": "TICVAI Sign-up",
   "name": "TICVAI Sign-up — Onboarding & Purchase",
   "offlineCapable": false,
   "app": "signup-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P11",
     "P14"
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
 "createLegalEntity": {
  "method": "POST",
  "path": "/legal-entities",
  "contract": "finance",
  "summary": "Create a legal entity",
  "permission": "ACCOUNT_CONFIGURE",
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
  "requestBody": "LegalEntity",
  "responds": "LegalEntity"
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
 "setAgreementContractTerm": {
  "method": "PUT",
  "path": "/agreement-contract-term",
  "contract": "subscription",
  "summary": "Agreement & Contract Terms Builder",
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
  "requestBody": "AgreementContractTermsBuilderInput",
  "responds": "AgreementContractTermsBuilderView"
 },
 "setPaymentProvider": {
  "method": "PUT",
  "path": "/payment-providers",
  "contract": "orders",
  "summary": "Configure a gateway and its routing",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "SetPaymentProviderRequest",
  "responds": "PaymentProvider"
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
 "setTrialConfiguration": {
  "method": "PUT",
  "path": "/trial-configurations",
  "contract": "subscription",
  "summary": "What a trial includes, how long it lasts and how it converts",
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
  "requestBody": "TrialConfiguration",
  "responds": "TrialConfiguration"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AgreementContractTermsBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as control.partner_agreement (PartnerAgreement), a new version per amendment; documents are control.partner_document rows with agreementId; legalEntity, commercialOwner and financeOwner land in legalEntityId, commercialOwnerPrincipalId and financeOwnerPrincipalId (data model DM4)",
  "description": "**What Agreement & Contract Terms Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement ID; omit to create"
   },
   "agreementName": {
    "type": "string",
    "description": "Agreement Name"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementType": {
    "type": "string",
    "description": "Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"
   },
   "contractReference": {
    "type": "string",
    "description": "Contract Reference"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "brandId": {
    "type": "string",
    "description": "Brand id",
    "nullable": true
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Venues the agreement covers"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "settlementCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Settlement currency, ISO 4217"
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "renewalType": {
    "type": "string",
    "enum": [
     "manual",
     "auto"
    ],
    "description": "Renewal Type"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner: staff principal id"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner: staff principal id"
   },
   "creditTermDays": {
    "type": "integer",
    "description": "Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"
   },
   "commissionTerms": {
    "type": "string",
    "description": "Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)",
    "nullable": true
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "description": "Pricing Basis (pack p.27 pricing models)"
   },
   "creditTerms": {
    "type": "string",
    "description": "Credit Terms",
    "nullable": true
   },
   "allocationTerms": {
    "type": "string",
    "description": "Allocation Terms",
    "nullable": true
   },
   "cancellationConditions": {
    "type": "string",
    "description": "Cancellation Conditions",
    "nullable": true
   },
   "bookingRestrictions": {
    "type": "string",
    "description": "Booking Restrictions",
    "nullable": true
   },
   "settlementTerms": {
    "type": "string",
    "description": "Settlement Terms",
    "nullable": true
   },
   "minimumCommitment": {
    "type": "integer",
    "description": "Minimum Commitment: tickets over the agreement term",
    "nullable": true
   },
   "salesTarget": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sales Target over the agreement term"
   },
   "renewalNoticeDays": {
    "type": "integer",
    "description": "Renewal Notice Period in days",
    "nullable": true
   },
   "renegotiationRequired": {
    "type": "boolean",
    "description": "Renegotiation Required"
   },
   "renewalRequiresApproval": {
    "type": "boolean",
    "description": "Renewal Approval: renewal needs approval"
   },
   "rateMode": {
    "$ref": "#/components/schemas/PartnerRateMode",
    "description": "Net rate or commission, as on PartnerAgreement"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"
   },
   "refundConditions": {
    "type": "string",
    "description": "Refund Conditions (pack p.26)",
    "nullable": true
   },
   "agreementValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"
   },
   "documents": {
    "type": "array",
    "description": "Document Association",
    "items": {
     "type": "object",
     "properties": {
      "documentType": {
       "type": "string",
       "enum": [
        "signedContract",
        "addendum",
        "rateSheet",
        "sla",
        "nda",
        "commercialAnnex"
       ]
      },
      "documentId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   }
  }
 },
 "AgreementContractTermsBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_agreement and control.partner_document and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Agreement & Contract Terms Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement ID; omit to create"
   },
   "agreementName": {
    "type": "string",
    "description": "Agreement Name"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementType": {
    "type": "string",
    "description": "Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"
   },
   "contractReference": {
    "type": "string",
    "description": "Contract Reference"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "brandId": {
    "type": "string",
    "description": "Brand id",
    "nullable": true
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Venues the agreement covers"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "settlementCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Settlement currency, ISO 4217"
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "renewalType": {
    "type": "string",
    "enum": [
     "manual",
     "auto"
    ],
    "description": "Renewal Type"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner: staff principal id"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner: staff principal id"
   },
   "creditTermDays": {
    "type": "integer",
    "description": "Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"
   },
   "commissionTerms": {
    "type": "string",
    "description": "Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)",
    "nullable": true
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "description": "Pricing Basis (pack p.27 pricing models)"
   },
   "creditTerms": {
    "type": "string",
    "description": "Credit Terms",
    "nullable": true
   },
   "allocationTerms": {
    "type": "string",
    "description": "Allocation Terms",
    "nullable": true
   },
   "cancellationConditions": {
    "type": "string",
    "description": "Cancellation Conditions",
    "nullable": true
   },
   "bookingRestrictions": {
    "type": "string",
    "description": "Booking Restrictions",
    "nullable": true
   },
   "settlementTerms": {
    "type": "string",
    "description": "Settlement Terms",
    "nullable": true
   },
   "minimumCommitment": {
    "type": "integer",
    "description": "Minimum Commitment: tickets over the agreement term",
    "nullable": true
   },
   "salesTarget": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sales Target over the agreement term"
   },
   "renewalNoticeDays": {
    "type": "integer",
    "description": "Renewal Notice Period in days",
    "nullable": true
   },
   "renegotiationRequired": {
    "type": "boolean",
    "description": "Renegotiation Required"
   },
   "renewalRequiresApproval": {
    "type": "boolean",
    "description": "Renewal Approval: renewal needs approval"
   },
   "rateMode": {
    "$ref": "#/components/schemas/PartnerRateMode",
    "description": "Net rate or commission, as on PartnerAgreement"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"
   },
   "refundConditions": {
    "type": "string",
    "description": "Refund Conditions (pack p.26)",
    "nullable": true
   },
   "agreementValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"
   },
   "documents": {
    "type": "array",
    "description": "Document Association",
    "items": {
     "type": "object",
     "properties": {
      "documentType": {
       "type": "string",
       "enum": [
        "signedContract",
        "addendum",
        "rateSheet",
        "sla",
        "nda",
        "commercialAnnex"
       ]
      },
      "documentId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "version": {
    "type": "integer",
    "description": "Agreement version; amendments create a new one"
   },
   "status": {
    "$ref": "#/components/schemas/PartnerAgreementStatus",
    "description": "Agreement status"
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
 "LegalEntity": {
  "x-ticvai-persistence": "ledger.legal_entity",
  "type": "object",
  "description": "Also the `createLegalEntity` body. **`id` and `scopePath` are server-owned** (`readOnly`) and ignored if sent.\n",
  "required": [
   "id",
   "code",
   "name",
   "countryCode",
   "currency",
   "currencyScale",
   "fiscalYearStartMonth"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4
   },
   "taxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "fiscalYearStartMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 12
   },
   "regionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "PartnerAgreementStatus": {
  "type": "string",
  "enum": [
   "pendingApproval",
   "active",
   "expiringSoon",
   "expired",
   "suspended",
   "terminated"
  ]
 },
 "PartnerRateMode": {
  "type": "string",
  "description": "**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n",
  "enum": [
   "netRate",
   "commission"
  ]
 },
 "PaymentProvider": {
  "type": "object",
  "x-ticvai-persistence": "payments.provider",
  "description": "BL-116, CF-131. **`Payment` carried `providerName` and `providerReference`, which records a provider and does not abstract one.**\nTwo gateways are confirmed for Phase 1 — **Network International and Stripe** — and that is exactly the number that forces this: **one gateway can be hard-coded and two cannot.**\nCredentials live in the vault and never here, following `ai.AiProvider` (ADR-0020's rule applied outside AI): **no surface ever holds a provider key.**\n",
  "required": [
   "id",
   "name",
   "kind",
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
   "kind": {
    "type": "string",
    "enum": [
     "networkInternational",
     "stripe",
     "adyen",
     "checkout",
     "cash",
     "wallet",
     "other"
    ]
   },
   "supportedMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "card",
      "applePay",
      "googlePay",
      "samsungPay",
      "wallet",
      "bankTransfer",
      "cash",
      "bnpl"
     ]
    }
   },
   "supportedCurrencies": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "supportsTokenisation": {
    "type": "boolean",
    "description": "**The keystone.** Recurring billing, wallet auto-reload, one-click checkout and payment links all require a stored credential, and none of them can be designed until this is answered per provider.\n"
   },
   "supportsPartialCapture": {
    "type": "boolean",
    "default": true
   },
   "acceptedOnChannels": {
    "type": "array",
    "description": "BL-115. **Which channels may use this provider.** A kiosk taking cash and a website taking cards is not a policy either could infer, and a venue that accepts cash at a till and not online had no way to say so.\n",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "presentmentCurrencies": {
    "type": "array",
    "description": "BL-070. **What a storefront may quote in**, distinct from what it settles in. A guest sees GBP and the venue books AED — the display currency is the provider's capability and the settlement currency is the venue's (CF-114 on multi-currency).\n",
    "items": {
     "type": "string"
    }
   },
   "supports3ds": {
    "type": "boolean",
    "default": true
   },
   "terminal": {
    "type": "object",
    "nullable": true,
    "description": "BL-119. **Terminal behaviour, where this provider drives a physical device.** Unstated until now, and every field here is one a certification body asks about.\n",
    "properties": {
     "emvCertificationRef": {
      "type": "string",
      "nullable": true
     },
     "offlineFloorLimit": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "**What a terminal may approve with no connection.** Above it the sale waits; below it the venue carries the risk knowingly — and a floor limit of zero means a till stops when the line does.\n"
     },
     "supportsOfflineApproval": {
      "type": "boolean",
      "default": false
     },
     "receiptSignatureRequired": {
      "type": "boolean",
      "default": false
     },
     "supportsTipOnTerminal": {
      "type": "boolean",
      "default": false
     }
    }
   },
   "credentialRef": {
    "type": "string",
    "writeOnly": true,
    "description": "A vault reference. **Never the credential**, never returned, and rotated without a contract change.\n"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "PaymentRouting": {
  "type": "object",
  "x-ticvai-persistence": "payments.routing_rule",
  "description": "**Which provider takes a given payment, and why.** With two gateways the question is live from day one: a UAE card may cost less through one and an international card less through the other.\n**Ordered rules, first match wins, and a fallback that is not optional.** A gateway outage with no fallback is a venue that cannot sell.\n",
  "required": [
   "id",
   "priority",
   "providerId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "priority": {
    "type": "integer"
   },
   "providerId": {
    "type": "string",
    "format": "uuid"
   },
   "conditions": {
    "type": "object",
    "description": "**Match on what is known before the charge** — channel, currency, method, issuer country, amount band. Not on anything that requires asking the provider first.\n",
    "properties": {
     "channel": {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     },
     "currency": {
      "type": "string",
      "nullable": true,
      "x-ticvai-persisted": false,
      "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
     },
     "method": {
      "type": "string",
      "nullable": true
     },
     "issuerCountry": {
      "type": "string",
      "nullable": true
     },
     "minAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "maxAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    }
   },
   "fallbackProviderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Where this provider declines or is unreachable.** A decline is not always a fallback case — an insufficient-funds decline should not be retried elsewhere, and a gateway timeout should.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "SetPaymentProviderRequest": {
  "x-ticvai-persistence": "none — request only; the provider lands in payments.provider and its rules in payments.routing_rule",
  "description": "Request only. **A provider and the rules that route to it**, because `setPaymentProvider` is *\"configure a gateway and its routing\"* and writes both tables — and the provider schema alone carried no routing field, so the routing half had nothing to arrive in.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/PaymentProvider"
   },
   {
    "type": "object",
    "properties": {
     "routing": {
      "type": "array",
      "description": "The ordered rules that send payments to this provider. `providerId` on each is this provider's `id`.",
      "items": {
       "$ref": "#/components/schemas/PaymentRouting"
      }
     }
    }
   }
  ]
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
 "TrialConfiguration": {
  "type": "object",
  "x-ticvai-persistence": "subscription.trial_config",
  "description": "Board 5.5. **A trial that expires with no conversion path is a tenant full of real data nobody can bill.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tierCode": {
    "type": "string",
    "nullable": true
   },
   "durationDays": {
    "type": "integer",
    "default": 30
   },
   "includedModules": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "usageCaps": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    }
   },
   "paymentMethodRequiredUpFront": {
    "type": "boolean",
    "default": false
   },
   "conversionOfferPercent": {
    "type": "number",
    "nullable": true
   },
   "noticeDaysBeforeExpiry": {
    "type": "array",
    "items": {
     "type": "integer"
    }
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "suspend",
     "convert",
     "decommission"
    ],
    "default": "suspend",
    "description": "**Suspension is the humane default.** Customers routinely let a trial lapse and come back a week later.\n"
   },
   "retainDataDays": {
    "type": "integer",
    "default": 90
   }
  }
 }
}
```
