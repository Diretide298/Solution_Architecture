# WS102 — Subscription Licensing AI Self Service board 5

**10 screens · 10 operations · 23 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCOUNT_CONFIGURE, PLATFORM_CELL_MANAGE, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-409` | Purchase / Trial Journey Selection | listDetail | 1 | 0 | — |
| `ADM-410` | Contract & Billing Cycle Selection | listDetail | 1 | 0 | — |
| `ADM-411` | Billing & Legal Entity Information | listDetail | 1 | 0 | — |
| `ADM-412` | Payment Method & Settlement Setup | listDetail | 3 | 1 | — |
| `ADM-413` | Trial Configuration & Conversion Rules | configEditor | 1 | 0 | — |
| `ADM-414` | Order & Commercial Pricing Review | listDetail | 1 | 0 | — |
| `ADM-415` | Commercial Agreement, Billable Definition & Customer Acceptance | listDetail | 1 | 0 | — |
| `ADM-416` | Payment, Contract & Commercial Validation | listDetail | 1 | 0 | — |
| `ADM-417` | Subscription Confirmation & Commercial Activation | listDetail | 1 | 0 | — |
| `ADM-418` | Subscription Lifecycle & Trial-to-Paid Handoff | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-409, ADM-410, ADM-411, ADM-414, ADM-415, ADM-416, ADM-417 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setTrialConfiguration",
    "contract": "subscription",
    "purpose": "Purchase or trial",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-409",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-409"
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
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSubscription",
    "contract": "subscription",
    "purpose": "Contract and billing cycle",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-410",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-410"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 59. 0 of 0 labels bound to a contract property; 1 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createLegalEntity",
    "contract": "finance",
    "purpose": "Billing and legal entity",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-411",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-411"
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
     "components": [
      {
       "kind": "selectField",
       "label": "Tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status"
       ],
       "operation": "listTenants",
       "notes": "**Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant into it is open.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "Open grant into this tenant",
       "bindsTo": "PlatformStaffGrant",
       "columns": [
        "PlatformStaffGrant.id",
        "PlatformStaffGrant.operatorDisplayName",
        "PlatformStaffGrant.permissions",
        "PlatformStaffGrant.reason",
        "PlatformStaffGrant.ticketRef",
        "PlatformStaffGrant.openedAt",
        "PlatformStaffGrant.expiresAt"
       ],
       "operation": "openPlatformStaffGrant",
       "notes": "**Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "primaryButton",
       "label": "Open access grant",
       "operation": "openPlatformStaffGrant",
       "notes": "Shown until a grant into the picked tenant is open; asks for the second factor first (step-up, audit R135).",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formOpenPlatformStaffGrant",
    "component": "modal",
    "trigger": "Open access grant",
    "body": "**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Open access grant",
     "operation": "openPlatformStaffGrant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permissions",
      "reason",
      "ticketRef",
      "expiresAt"
     ]
    },
    "provenance": "contract identity.yaml POST /platform-staff-grants"
   }
  ],
  "states": {
   "loading": "The payment method settlement list.",
   "error": "Could not load. Names which read failed and leaves the payment method settlement untouched.",
   "emptyFirstRun": "No payment method settlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment method settlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "grantRequired": "**No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098)."
  },
  "apis": [
   {
    "operationId": "openPlatformStaffGrant",
    "contract": "identity",
    "purpose": "Open a time-boxed, audited platform-staff grant into the picked tenant before any tenant-scoped operation here; the tenant sees it (decided 28 September, audit R098)",
    "trigger": "onAction"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "The tenant picker — the operator picks a tenant before acting in its cell (audit R098)",
    "trigger": "onLoad"
   },
   {
    "operationId": "setPaymentProvider",
    "contract": "orders",
    "purpose": "Payment and settlement setup",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-412",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-412"
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
  "apis": [
   {
    "operationId": "setTrialConfiguration",
    "contract": "subscription",
    "purpose": "Trial and conversion rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-413",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-413"
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
  "apis": [
   {
    "operationId": "previewSubscriptionChange",
    "contract": "subscription",
    "purpose": "Order and pricing review",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-414",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-414"
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
  "apis": [
   {
    "operationId": "setAgreementContractTerm",
    "contract": "subscription",
    "purpose": "Agreement and acceptance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-415",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-415"
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
   "loading": "The payment contract commercial list.",
   "error": "Could not load. Names which read failed and leaves the payment contract commercial untouched.",
   "emptyFirstRun": "No payment contract commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment contract commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateCommercialPackage",
    "contract": "subscription",
    "purpose": "Validate before committing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-416",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-416"
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
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSubscription",
    "contract": "subscription",
    "purpose": "Create the subscription",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-417",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-417"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 67. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purpose": "Manage the immediate commercial lifecycle after purchase or trial activation and ensure clean handoff to operational provisioning. Automatically provision the customer's TICVAI tenant, organization, venue structure, administrator, licensed modules, entitlements, quotas, security baseline and venue template after subscription/trial activation.",
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
  "apis": [
   {
    "operationId": "getSubscription",
    "contract": "subscription",
    "purpose": "Confirmation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Trial Usage",
    "Trial Ticket Volume",
    "Trial Expiry",
    "Conversion Package",
    "Commercial Model",
    "Paid Start Date"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-418",
   "workshopBoard": "wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-418"
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
 "getSubscription": {
  "method": "GET",
  "path": "/tenants/{tenantId}/subscription",
  "contract": "subscription",
  "summary": "Read the current subscription",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Subscription"
 },
 "listTenants": {
  "method": "GET",
  "path": "/tenants",
  "contract": "subscription",
  "summary": "List tenants",
  "permission": "PLATFORM_TENANT_VIEW",
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
    "name": "planId",
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
 "openPlatformStaffGrant": {
  "method": "POST",
  "path": "/platform-staff-grants",
  "contract": "identity",
  "summary": "A platform operator opens a time-boxed grant into this tenant",
  "permission": "PLATFORM_TENANT_ACCESS",
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
  "responds": "PlatformStaffGrant"
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
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
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
 "Permission": {
  "type": "string",
  "enum": [
   "SESSION_FORCE_LOGOUT",
   "USER_MANAGE",
   "ROLE_MANAGE",
   "PERMISSION_GRANT",
   "PERMISSION_VIEW",
   "PERMISSION_MANAGE",
   "PLATFORM_TENANT_VIEW",
   "PLATFORM_TENANT_MANAGE",
   "PLATFORM_TENANT_TERMINATE",
   "PLATFORM_PLAN_MANAGE",
   "PLATFORM_CELL_VIEW",
   "PLATFORM_CELL_MANAGE",
   "PLATFORM_BILLING_VIEW",
   "PLATFORM_AI_MANAGE",
   "PLATFORM_BILLING_MANAGE",
   "PLATFORM_RELEASE_VIEW",
   "PLATFORM_RELEASE_MANAGE",
   "PLATFORM_RELEASE_PROMOTE",
   "PLATFORM_MIGRATION_VIEW",
   "PLATFORM_MIGRATION_APPLY",
   "PLATFORM_TENANT_ACCESS",
   "TENANT_CONFIGURE",
   "TENANT_VIEW",
   "TENANT_PUBLISH",
   "SCOPE_VIEW",
   "SCOPE_MANAGE",
   "REGION_CONFIGURE",
   "WORKSTATION_CONFIGURE",
   "PRODUCT_VIEW",
   "PRODUCT_CONFIGURE",
   "PRODUCT_APPROVE",
   "PRODUCT_PUBLISH",
   "PRICE_VIEW",
   "PRICE_CONFIGURE",
   "EVENT_CONFIGURE",
   "PERFORMANCE_CONFIGURE",
   "CAPACITY_CONFIGURE",
   "ORDER_VIEW",
   "ORDER_VIEW_OTHER",
   "ORDER_CREATE",
   "ORDER_MODIFY",
   "ORDER_DISCOUNT",
   "ORDER_CANCEL",
   "ORDER_VOID",
   "ORDER_REFUND",
   "ORDER_REFUND_APPROVE",
   "ORDER_REFUND_BULK",
   "ORDER_EXCHANGE",
   "ORDER_RESCHEDULE",
   "ORDER_REPRINT",
   "PRICE_OVERRIDE",
   "DISCOUNT_APPLY",
   "CREDIT_MANAGE",
   "CREDIT_OVERRIDE",
   "WALLET_VIEW",
   "WALLET_OPERATE",
   "WALLET_CONFIGURE",
   "PAYMENT_VIEW",
   "PAYMENT_CONFIGURE",
   "PAYMENT_PROVIDER_MANAGE",
   "PAYMENT_DISPUTE",
   "SHIFT_OPEN",
   "SHIFT_CLOSE",
   "SHIFT_SUSPEND",
   "SHIFT_CLOSE_OTHER",
   "SHIFT_APPROVE_OPEN",
   "SHIFT_APPROVE_CLOSE",
   "SHIFT_REOPEN",
   "CASH_LIFT",
   "CASH_ADD",
   "CASH_NO_SALE",
   "DEPOSIT_BOX_MODIFY_OWN",
   "DEPOSIT_BOX_MODIFY_OTHER",
   "OVERSHORT_ACCEPT",
   "ACCESS_VALIDATE",
   "ACCESS_OVERRIDE",
   "ACCESS_POINT_CONFIGURE",
   "TURNSTILE_MODE_SET",
   "TICKET_LOOKUP",
   "ACCREDITATION_VIEW",
   "ACCREDITATION_APPLY",
   "ACCREDITATION_APPROVE",
   "ACCREDITATION_ISSUE",
   "ACCREDITATION_MANAGE",
   "ACCREDITATION_CONFIGURE",
   "REPORT_VIEW_OWN",
   "REPORT_VIEW_WORKSTATION",
   "REPORT_VIEW_VENUE",
   "REPORT_VIEW_REGION",
   "REPORT_VIEW_TENANT",
   "REPORT_EXPORT",
   "REPORT_EXPORT_PII",
   "REPORT_MANAGE",
   "REPORT_SCHEDULE",
   "LEDGER_VIEW",
   "LEDGER_POST",
   "LEDGER_APPROVE",
   "TAX_CONFIGURE",
   "ACCOUNT_CONFIGURE",
   "SETTLEMENT_VIEW",
   "SETTLEMENT_RECONCILE",
   "GUEST_VIEW",
   "GUEST_VIEW_PII",
   "GUEST_MANAGE",
   "VENUE_MAP_VIEW",
   "VENUE_MAP_MANAGE",
   "VENUE_MAP_PUBLISH",
   "RESOURCE_VIEW",
   "RESOURCE_BOOK",
   "RESOURCE_MANAGE",
   "RESOURCE_CONFIGURE",
   "RENTAL_VIEW",
   "RENTAL_BOOK",
   "RENTAL_OPERATE",
   "RENTAL_MANAGE",
   "RENTAL_CONFIGURE",
   "RENTAL_PRICE",
   "RENTAL_APPROVE",
   "RENTAL_OVERRIDE",
   "DEVELOPER_VIEW",
   "DEVELOPER_MANAGE",
   "DEVELOPER_ADMIN",
   "LOYALTY_ACCRUE",
   "LOYALTY_REDEEM",
   "LOYALTY_ADJUST",
   "MARKETING_VIEW",
   "MARKETING_MANAGE",
   "MARKETING_SEND",
   "CASE_VIEW",
   "CASE_MANAGE",
   "ASSET_LIBRARY_VIEW",
   "ASSET_LIBRARY_MANAGE",
   "ASSET_LIBRARY_APPROVE",
   "ASSET_LIBRARY_SHARE",
   "QUEUE_VIEW",
   "QUEUE_MANAGE",
   "QUEUE_REDEEM",
   "QUEUE_OVERRIDE",
   "TRANSPORT_VIEW",
   "TRANSPORT_MANAGE",
   "TRANSPORT_PRICE",
   "ASSET_VIEW",
   "ASSET_MANAGE",
   "WORK_ORDER_VIEW",
   "WORK_ORDER_MANAGE",
   "WORK_ORDER_VERIFY",
   "INSPECTION_VIEW",
   "INSPECTION_SUBMIT",
   "INSPECTION_MANAGE",
   "INCIDENT_REPORT",
   "INCIDENT_VIEW",
   "INCIDENT_MANAGE",
   "KIOSK_ATTEND",
   "DEVICE_VIEW",
   "DEVICE_CONFIGURE",
   "DEVICE_MANAGE",
   "APPROVAL_ACT",
   "APPROVAL_DELEGATE",
   "AI_USE",
   "AI_CONFIGURE",
   "AI_APPROVE",
   "AI_AUDIT_VIEW",
   "RISK_REVIEW",
   "RISK_INVESTIGATE",
   "AUDIT_VIEW",
   "APPROVAL_VIEW",
   "APPROVAL_REQUEST",
   "APPROVAL_DECIDE",
   "APPROVAL_CONFIGURE",
   "MAINTENANCE_EXECUTE",
   "MAINTENANCE_APPROVE",
   "WORKFORCE_VIEW",
   "WORKFORCE_MANAGE",
   "ATTENDANCE_RECORD",
   "ANNOUNCEMENT_PUBLISH",
   "ANNOUNCEMENT_EMERGENCY",
   "PARTNER_VIEW",
   "PARTNER_MANAGE",
   "PARKING_CONFIGURE",
   "PAYMENT_VOID",
   "PROCUREMENT_VIEW",
   "PROCUREMENT_REQUEST",
   "PROCUREMENT_MANAGE",
   "PROCUREMENT_RECEIVE"
  ]
 },
 "PlatformStaffGrant": {
  "type": "object",
  "x-ticvai-persistence": "identity.platform_staff_grant",
  "description": "**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n",
  "required": [
   "id",
   "operatorPrincipalId",
   "permissions",
   "reason",
   "openedAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The platform operator, from the Control Plane token. Set by the server."
   },
   "operatorDisplayName": {
    "type": "string",
    "readOnly": true
   },
   "permissions": {
    "type": "array",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
    }
   },
   "reason": {
    "type": "string"
   },
   "ticketRef": {
    "type": "string",
    "nullable": true
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant root. **Operations write it at `tenant` scope**; the server sets it."
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
 "SuspensionMode": {
  "type": "string",
  "description": "Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n",
  "enum": [
   "readOnly",
   "noNewSales",
   "fullLockout"
  ]
 },
 "Tenant": {
  "x-ticvai-persistence": "control.tenant",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "status",
   "createdAt"
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
   "status": {
    "$ref": "#/components/schemas/TenantStatus"
   },
   "suspensionMode": {
    "$ref": "#/components/schemas/SuspensionMode"
   },
   "suspensionReason": {
    "type": "string",
    "nullable": true
   },
   "suspensionEffectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."
   },
   "suspensionNoticeMessage": {
    "$ref": "#/components/schemas/LocalisedText",
    "description": "The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."
   },
   "terminationScheduledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When `terminateTenant` started the retention window. Null when no termination is under way."
   },
   "terminationRetentionUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."
   },
   "terminationReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "terminationRequestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planName": {
    "type": "string",
    "nullable": true
   },
   "cellCount": {
    "type": "integer"
   },
   "venueCount": {
    "type": "integer"
   },
   "regionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"
   },
   "billingEmail": {
    "type": "string"
   },
   "billingAddress": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."
   },
   "accountManagerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "TenantStatus": {
  "type": "string",
  "enum": [
   "onboarding",
   "active",
   "suspended",
   "terminating",
   "terminated"
  ]
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
