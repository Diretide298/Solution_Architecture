# WS106 — Subscription Licensing AI Self Service board 9

**10 screens · 8 operations · 12 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-449` | Usage & License Command Center | listDetail | 1 | 0 | — |
| `ADM-450` | Entitlement & License Inventory | listDetail | 1 | 0 | — |
| `ADM-451` | Commercial Consumption & Billable Event Metering | listDetail | 1 | 0 | — |
| `ADM-452` | Operational Usage & Threshold Monitor | listDetail | 2 | 0 | — |
| `ADM-453` | License Enforcement & Decision Engine | listDetail | 1 | 0 | — |
| `ADM-454` | Minimum Guarantee & Variable Consumption Monitor | listDetail | 1 | 0 | — |
| `ADM-455` | Overage, Capacity & Temporary Exception Management | configEditor | 1 | 0 | — |
| `ADM-456` | Usage Alerts, Reconciliation & Exception Center | configEditor | 1 | 0 | — |
| `ADM-457` | AI Usage Forecast & Commercial Optimization | listDetail | 1 | 0 | — |
| `ADM-458` | License, Metering & Commercial Synchronization Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-449, ADM-450, ADM-451, ADM-452, ADM-453, ADM-454, ADM-457, ADM-458 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-449",
  "name": "Usage & License Command Center",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "1",
   "page": 109
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/usage-license-command-center-adm-449",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/UsageLicenseCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-450",
    "ADM-451",
    "ADM-452",
    "ADM-453",
    "ADM-454",
    "ADM-455",
    "ADM-456",
    "ADM-457",
    "ADM-458"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "ADM-450",
     "trigger": "Entitlement & License Inventory",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-451",
     "trigger": "Commercial Consumption & Billable Event Metering",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-452",
     "trigger": "Operational Usage & Threshold Monitor",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-453",
     "trigger": "License Enforcement & Decision Engine",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-454",
     "trigger": "Minimum Guarantee & Variable Consumption Monitor",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-455",
     "trigger": "Overage, Capacity & Temporary Exception Management",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-456",
     "trigger": "Usage Alerts, Reconciliation & Exception Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-457",
     "trigger": "AI Usage Forecast & Commercial Optimization",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-458",
     "trigger": "License, Metering & Commercial Synchronization Audit",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a real-time consolidated view of technical usage, commercial consumption and license health.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 109"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 109"
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
       "impliedBy": "getEntitlementUsage",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The usage license list.",
   "error": "Could not load. Names which read failed and leaves the usage license untouched.",
   "emptyFirstRun": "No usage license yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the usage license are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licence",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-449",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-449"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 109. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-450",
  "name": "Entitlement & License Inventory",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "2",
   "page": 110
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/entitlement-license-inventory-adm-450",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/EntitlementLicenseInventory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show exactly what the customer is technically entitled to use independently of the commercial charging model.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 110"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 110"
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
       "impliedBy": "getTenantLicences",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entitlement license inventory list.",
   "error": "Could not load. Names which read failed and leaves the entitlement license inventory untouched.",
   "emptyFirstRun": "No entitlement license inventory yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entitlement license inventory are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTenantLicences",
    "contract": "subscription",
    "purpose": "Entitlement inventory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-450",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-450"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 110. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-451",
  "name": "Commercial Consumption & Billable Event Metering",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "3",
   "page": 111
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/commercial-consumption-billable-event-metering-adm-451",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CommercialConsumptionBillableEventMetering.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "This is the major new Board 9 screen. Meter the events that determine the customer's variable commercial charges.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 111"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 111"
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
       "impliedBy": "getUsageMetering",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial consumption billable list.",
   "error": "Could not load. Names which read failed and leaves the commercial consumption billable untouched.",
   "emptyFirstRun": "No commercial consumption billable yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial consumption billable are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getUsageMetering",
    "contract": "subscription",
    "purpose": "Billable event metering",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-451",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-451"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 111. 0 of 0 labels bound to a contract property; 0 of 3 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-452",
  "name": "Operational Usage & Threshold Monitor",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "4",
   "page": 112
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/operational-usage-threshold-monitor-adm-452",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/OperationalUsageThresholdMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor technical and operational consumption against licensed capacity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 112"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 112"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The operational usage threshold list.",
   "error": "Could not load. Names which read failed and leaves the operational usage threshold untouched.",
   "emptyFirstRun": "No operational usage threshold yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational usage threshold are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getLicenceEnforcement",
    "contract": "subscription",
    "purpose": "Thresholds and position",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getPlanRecommendations",
    "contract": "subscription",
    "purpose": "What to do about a unit approaching or over its limit (tier versus capacity pack)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-452",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-452"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 112. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-453",
  "name": "License Enforcement & Decision Engine",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "5",
   "page": 113
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/license-enforcement-decision-engine-adm-453",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/LicenseEnforcementDecisionEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Apply the correct technical enforcement behavior when licensed resources reach or exceed limits.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 113 §Display"
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
       "label": "Every license enforcement decision",
       "columns": [
        "Requested Action",
        "Current Entitlement",
        "Current Consumption",
        "Rule",
        "Decision",
        "Reason",
        "Override Allowed",
        "Required Approval"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 113 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected license enforcement decision",
       "bindsTo": null,
       "columns": [
        "Requested Action",
        "Current Entitlement",
        "Current Consumption",
        "Rule",
        "Decision",
        "Reason",
        "Override Allowed",
        "Required Approval"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Overage”, “Approval”, “Transactions Soft / Overage”, “Modules Hard”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 113 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The license enforcement decision list.",
   "error": "Could not load. Names which read failed and leaves the license enforcement decision untouched.",
   "emptyFirstRun": "No license enforcement decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the license enforcement decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setLicenceEnforcementPolicy",
    "contract": "subscription",
    "purpose": "What happens at each threshold",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getLicenceEnforcement"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Requested Action",
    "Current Entitlement",
    "Current Consumption",
    "Rule",
    "Decision",
    "Reason"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-453",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-453"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 113. 0 of 8 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-454",
  "name": "Minimum Guarantee & Variable Consumption Monitor",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "6",
   "page": 114
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/minimum-guarantee-variable-consumption-monitor-adm-454",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/MinimumGuaranteeVariableConsumptionMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast) and no metric row",
  "purpose": "Track the commercial consumption position against contractual minimum guarantees. This screen does not issue the invoice. It provides Board 10 with the reconciled consumption basis.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 114 §Forecast"
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
       "label": "Every minimum guarantee variable",
       "columns": [
        "Projected month-end billable tickets: 43,800",
        "Projected variable billing basis: AED 32,850"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 114 §Forecast"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected minimum guarantee variable",
       "bindsTo": null,
       "columns": [
        "Projected month-end billable tickets: 43,800",
        "Projected variable billing basis: AED 32,850"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Rate”, “Billable Tickets”, “Current Position”, “Automatically calculate”, “Progress Visualization”, “Where applicable show”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 114 §Forecast"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The minimum guarantee variable list.",
   "error": "Could not load. Names which read failed and leaves the minimum guarantee variable untouched.",
   "emptyFirstRun": "No minimum guarantee variable yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the minimum guarantee variable are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getLicenceEnforcement",
    "contract": "subscription",
    "purpose": "Minimum guarantee and variable consumption",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Projected month-end billable tickets: 43,800",
    "Projected variable billing basis: AED 32,850"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-454",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-454"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 114. 0 of 2 labels bound to a contract property; 2 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-455",
  "name": "Overage, Capacity & Temporary Exception Management",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "7",
   "page": 115
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/overage-capacity-temporary-exception-management-adm-455",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/OverageCapacityTemporaryExceptionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Fields) and no display directory — it is settings, not a population",
  "purpose": "Manage technical capacity above standard entitlement and temporary operational requirements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Resource",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Start",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Requested By",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Commercial Treatment",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 115 §Fields"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The overage capacity temporary configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the overage capacity temporary untouched.",
   "emptyFirstRun": "No overage capacity temporary configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "addCapacityPack",
    "contract": "subscription",
    "purpose": "Overage and temporary exceptions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getLicenceEnforcement",
     "getEntitlementUsage"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-455",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-455"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 115. 0 of 0 labels bound to a contract property; 9 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-456",
  "name": "Usage Alerts, Reconciliation & Exception Center",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "8",
   "page": 117
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/usage-alerts-reconciliation-exception-center-adm-456",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/UsageAlertsReconciliationExceptionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure recipients) and no display directory — it is settings, not a population",
  "purpose": "Provide a central operational center for consumption alerts and commercial metering exceptions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Customer Admin",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 117 §Configure recipients"
      },
      {
       "kind": "selectField",
       "label": "TICVAI Commercial",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 117 §Configure recipients"
      },
      {
       "kind": "selectField",
       "label": "Finance",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 117 §Configure recipients"
      },
      {
       "kind": "selectField",
       "label": "Operations",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 117 §Configure recipients"
      },
      {
       "kind": "selectField",
       "label": "Technical Support",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 117 §Configure recipients"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The usage alerts reconciliation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the usage alerts reconciliation untouched.",
   "emptyFirstRun": "No usage alerts reconciliation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getBillingReconciliation",
    "contract": "subscription",
    "purpose": "Alerts and reconciliation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-456",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-456"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 117. 0 of 0 labels bound to a contract property; 5 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-457",
  "name": "AI Usage Forecast & Commercial Optimization",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "9",
   "page": 118
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/ai-usage-forecast-commercial-optimization-adm-457",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/AiUsageForecastCommercialOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use AI to forecast operational and commercial consumption and recommend appropriate action.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 118"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 118"
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
       "impliedBy": "getEntitlementUsage",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The usage forecast commercial list.",
   "error": "Could not load. Names which read failed and leaves the usage forecast commercial untouched.",
   "emptyFirstRun": "No usage forecast commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the usage forecast commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Consumption trend",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-457",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-457"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 118. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-458",
  "name": "License, Metering & Commercial Synchronization Audit",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "9",
   "number": "10",
   "page": 119
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/license-metering-commercial-synchronization-audit-adm-458",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/LicenseMeteringCommercialSynchronizationAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-449"
   ],
   "exitTo": [
    "ADM-449"
   ],
   "transitions": [
    {
     "to": "ADM-449",
     "trigger": "Back to Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Ensure that the approved contract, subscription, license and actual metering configuration remain synchronized.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 119 §Track"
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
       "label": "Every license metering commercial",
       "columns": [
        "Contract Version",
        "License Version",
        "Metering Rule Version",
        "Previous Value",
        "New Value",
        "Changed By",
        "Approved By",
        "Timestamp",
        "Effective Date"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 119 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected license metering commercial",
       "bindsTo": null,
       "columns": [
        "Contract Version",
        "License Version",
        "Metering Rule Version",
        "Previous Value",
        "New Value",
        "Changed By",
        "Approved By",
        "Timestamp",
        "Effective Date"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Approved Commercial Package”, “Contract”, “All Tickets Issued”, “Critical Board 9 Data Separation”, “Suppose during September”, “Contract says”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 119 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The license metering commercial list.",
   "error": "Could not load. Names which read failed and leaves the license metering commercial untouched.",
   "emptyFirstRun": "No license metering commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the license metering commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getUsageMetering",
    "contract": "subscription",
    "purpose": "Metering audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Contract Version",
    "License Version",
    "Metering Rule Version",
    "Previous Value",
    "New Value",
    "Changed By"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-458",
   "workshopBoard": "wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-458"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 119. 0 of 9 labels bound to a contract property; 9 of 84 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "addCapacityPack": {
  "method": "POST",
  "path": "/capacity-packs",
  "contract": "subscription",
  "summary": "Buy headroom without changing tier",
  "permission": "PLATFORM_BILLING_MANAGE",
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
  "requestBody": "CapacityPack",
  "responds": "CapacityPack"
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
 "getEntitlementUsage": {
  "method": "GET",
  "path": "/tenants/{tenantId}/entitlement-usage",
  "contract": "subscription",
  "summary": "Usage against licensed limits",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementUsage"
 },
 "getLicenceEnforcement": {
  "method": "GET",
  "path": "/licence-enforcement",
  "contract": "subscription",
  "summary": "Where a tenant stands against its entitlements, and what happens next",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "tenantId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "LicenceEnforcement"
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
 "getTenantLicences": {
  "method": "GET",
  "path": "/tenants/{tenantId}/licences",
  "contract": "subscription",
  "summary": "What a tenant is licensed to use",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "LicencePosition"
 },
 "getUsageMetering": {
  "method": "GET",
  "path": "/tenants/{tenantId}/usage",
  "contract": "subscription",
  "summary": "Metered usage for a period",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "periodStart",
    "in": "query",
    "required": true
   },
   {
    "name": "periodEnd",
    "in": "query",
    "required": true
   },
   {
    "name": "metric",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "UsageReport"
 },
 "setLicenceEnforcementPolicy": {
  "method": "PUT",
  "path": "/licence-enforcement",
  "contract": "subscription",
  "summary": "What happens at each threshold",
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
  "requestBody": "LicenceEnforcementPolicy",
  "responds": "LicenceEnforcementPolicy"
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
 "CapacityPack": {
  "type": "object",
  "x-ticvai-persistence": "subscription.capacity_pack",
  "description": "Board 3.8. **A good season should not require renegotiating a contract in August.**\n",
  "required": [
   "tenantId",
   "unit",
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "unit": {
    "type": "string"
   },
   "quantity": {
    "type": "integer"
   },
   "price": {
    "x-ticvai-column": "list_price",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "temporary": {
    "type": "boolean",
    "default": true
   },
   "approvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "invoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "EntitlementLimit": {
  "type": "object",
  "required": [
   "metric",
   "limit"
  ],
  "properties": {
   "metric": {
    "$ref": "#/components/schemas/UsageMetric"
   },
   "limit": {
    "type": "integer",
    "nullable": true,
    "x-ticvai-column": "limit_value",
    "description": "Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."
   },
   "overageAllowed": {
    "type": "boolean",
    "default": false
   },
   "overageUnitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "EntitlementUsage": {
  "x-ticvai-persistence": "none — aggregated from usage_record",
  "type": "object",
  "required": [
   "tenantId",
   "metrics"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "metrics": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "metric",
      "current",
      "isNearLimit"
     ],
     "properties": {
      "metric": {
       "$ref": "#/components/schemas/UsageMetric"
      },
      "current": {
       "type": "integer"
      },
      "limit": {
       "type": "integer",
       "nullable": true
      },
      "percentUsed": {
       "type": "number",
       "nullable": true
      },
      "isNearLimit": {
       "type": "boolean",
       "description": "Approaching a limit is an account conversation. Hitting one silently at a gate is an incident.\n"
      },
      "isExceeded": {
       "type": "boolean"
      }
     }
    }
   },
   "asAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "LicenceEnforcement": {
  "type": "object",
  "description": "Board 9.5. **Three states, three responses.**",
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "period": {
    "type": "string"
   },
   "units": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "unit": {
       "type": "string"
      },
      "allowance": {
       "type": "integer"
      },
      "consumed": {
       "type": "integer"
      },
      "percentUsed": {
       "type": "number"
      },
      "projectedAtPeriodEnd": {
       "type": "integer",
       "nullable": true
      },
      "state": {
       "type": "string",
       "enum": [
        "withinAllowance",
        "approaching",
        "atLimit",
        "overage"
       ]
      },
      "nextAction": {
       "type": "string",
       "nullable": true
      },
      "overageCharge": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "minimumGuaranteeMet": {
    "type": "boolean"
   },
   "alertsRaised": {
    "type": "integer"
   }
  }
 },
 "LicenceEnforcementPolicy": {
  "type": "object",
  "x-ticvai-persistence": "subscription.enforcement_policy",
  "description": "Board 9.5. **Refusing service to a paying customer mid-season is a commercial decision.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "thresholds": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "atPercentOfAllowance": {
       "type": "integer"
      },
      "action": {
       "type": "string",
       "enum": [
        "notify",
        "notifyAccountManager",
        "requireCapacityPack",
        "autoAddCapacityPack",
        "restrictNewConfiguration",
        "hardStop"
       ]
      },
      "notifyRoles": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "hardStopAllowed": {
    "type": "boolean",
    "default": false,
    "description": "**Off by default, and every enforcement action is alerted.**"
   },
   "graceDays": {
    "type": "integer",
    "default": 7
   }
  }
 },
 "LicencePosition": {
  "x-ticvai-persistence": "none — union of the tenant's plan (control.tenant.plan_id -> subscription.plan_module, subscription.plan_limit) and its add-ons (control.licence_add_on, control.licence_add_on_limit by tenant_id)",
  "type": "object",
  "required": [
   "tenantId",
   "licensedModules",
   "limits"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "licensedModules": {
    "type": "array",
    "description": "Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it.\n",
    "items": {
     "type": "object",
     "required": [
      "moduleKey",
      "source"
     ],
     "properties": {
      "moduleKey": {
       "type": "string"
      },
      "displayName": {
       "type": "string"
      },
      "source": {
       "type": "string",
       "enum": [
        "plan",
        "addOn"
       ]
      },
      "validTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "limits": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/EntitlementLimit"
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
 },
 "UsageReport": {
  "x-ticvai-persistence": "none — aggregated",
  "type": "object",
  "required": [
   "tenantId",
   "periodStart",
   "periodEnd",
   "metrics"
  ],
  "properties": {
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
   "metrics": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "metric": {
       "$ref": "#/components/schemas/UsageMetric"
      },
      "total": {
       "type": "number"
      },
      "included": {
       "type": "number",
       "nullable": true
      },
      "overage": {
       "type": "number"
      },
      "byVenue": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "venueId": {
          "type": "string",
          "format": "uuid"
         },
         "quantity": {
          "type": "number"
         }
        }
       }
      },
      "byCapability": {
       "type": "array",
       "description": "AI tokens only.",
       "items": {
        "type": "object",
        "properties": {
         "capability": {
          "type": "string"
         },
         "quantity": {
          "type": "number"
         }
        }
       }
      }
     }
    }
   }
  }
 }
}
```
