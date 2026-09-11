# P17-purchase-activation-01 — P17 · Purchase & Activation

**7 screens · 0 operations · 0 schemas · 0 permissions**

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
| `SGN-018` | Purchase / Trial Journey Selection | listDetail | 0 | 0 | — |
| `SGN-019` | Contract & Billing Cycle Selection | listDetail | 0 | 0 | — |
| `SGN-020` | Billing & Legal Entity Information | listDetail | 0 | 0 | — |
| `SGN-021` | Payment Method & Settlement Setup | listDetail | 0 | 0 | — |
| `SGN-022` | Order & Commercial Pricing Review | listDetail | 0 | 0 | — |
| `SGN-023` | Commercial Agreement, Billable Definition & Customer Acceptance | listDetail | 0 | 0 | — |
| `SGN-024` | Subscription Confirmation & Commercial Activation | listDetail | 0 | 0 | — |

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
   "regions": []
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
  "apis": [],
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
  "apis": [],
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
  "apis": [],
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
   "sameAs": "ADM-412",
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
  "notes": "The self-service form of `ADM-412`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.",
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
   "emptyNoAccess": "TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it."
  },
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
  "apis": [],
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
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 64. 0 of 5 labels bound to a contract property; 5 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "preloaded": [
    "Discount Type",
    "Value",
    "Period",
    "Approved By",
    "Expiry"
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
  "apis": [],
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
   "regions": []
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
  "apis": [],
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
