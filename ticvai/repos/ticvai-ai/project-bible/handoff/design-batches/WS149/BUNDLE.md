# WS149 — Payment Payment Orchestration board 3

**10 screens · 14 operations · 18 schemas · 6 permissions**

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
  `DEVICE_MANAGE, DEVICE_VIEW, PAYMENT_CONFIGURE, PAYMENT_PROVIDER_MANAGE, PAYMENT_VIEW, WORK_ORDER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-579` | Terminal & Card-Present Command Center\t48 | commandCentre | 1 | 0 | — |
| `ADM-580` | Payment Terminal & Device Inventory\t49 | listDetail | 4 | 0 | — |
| `ADM-581` | Terminal Provisioning & Device Configuration\t51 | configEditor | 2 | 0 | — |
| `ADM-582` | POS, Kiosk & Terminal Assignment Manager\t52 | listDetail | 1 | 0 | — |
| `ADM-583` | EMV & Card-Present Processing Configuration\t53 | configEditor | 1 | 0 | — |
| `ADM-584` | Payment Server & Terminal Connectivity Manager\t54 | listDetail | 1 | 0 | — |
| `ADM-585` | Card-Present Transaction Monitor & Operations\t55 | listDetail | 1 | 0 | — |
| `ADM-586` | Degraded, Offline & Store-and-Forward Manager\t56 | listDetail | 2 | 0 | — |
| `ADM-587` | Terminal Health, Maintenance & Incident Center\t57 | listDetail | 5 | 0 | — |
| `ADM-588` | Terminal Simulator, Certification & AI Operations Advisor\t59 | configEditor | 3 | 0 | — |

## Thin screens in this batch

**ADM-582, ADM-584, ADM-586, ADM-587 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-579",
  "name": "Terminal & Card-Present Command Center\\t48",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "1",
   "page": 47
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/terminal-card-present-command-center-t48-adm-579",
   "component": "apps/ticvai-web/src/routes/commercial/TerminalCardPresentCommandCenterT48.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-580",
    "ADM-581",
    "ADM-582",
    "ADM-583",
    "ADM-584",
    "ADM-585",
    "ADM-586",
    "ADM-587",
    "ADM-588"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-580",
     "trigger": "Payment Terminal & Device Inventory\\t49",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-581",
     "trigger": "Terminal Provisioning & Device Configuration\\t51",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-582",
     "trigger": "POS, Kiosk & Terminal Assignment Manager\\t52",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-583",
     "trigger": "EMV & Card-Present Processing Configuration\\t53",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-584",
     "trigger": "Payment Server & Terminal Connectivity Manager\\t54",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-585",
     "trigger": "Card-Present Transaction Monitor & Operations\\t55",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-586",
     "trigger": "Degraded, Offline & Store-and-Forward Manager\\t56",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-587",
     "trigger": "Terminal Health, Maintenance & Incident Center\\t57",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-588",
     "trigger": "Terminal Simulator, Certification & AI Operations Advisor\\t59",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide real-time operational visibility over all card-present payment infrastructure.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search terminal card-present \\t48",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Location",
        "Terminal",
        "POS",
        "Acquirer",
        "Payment method",
        "Card scheme",
        "Device model"
       ],
       "notes": "The pack filters this screen by venue, location, terminal, pos, acquirer, payment method and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Terminals",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Online Terminals",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Offline Terminals",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Degraded Terminals",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active POS Assignments",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Card-Present Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Authorization Rate",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Card-Present Value",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failed Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Processing Time",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Terminal Alerts",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Offline/Pending Transactions",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 47 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The terminal card-present \\t48 list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the terminal card-present \\t48 untouched.",
   "emptyFirstRun": "No terminal card-present \\t48 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the terminal card-present \\t48 are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentTerminals",
    "contract": "payments",
    "purpose": "Terminals across venues",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-579",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-579"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 47. 0 of 8 labels bound to a contract property; 20 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-580",
  "name": "Payment Terminal & Device Inventory\\t49",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "2",
   "page": 48
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-terminal-device-inventory-t49-adm-580",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentTerminalDeviceInventoryT49.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the centralized inventory of all payment terminals connected to TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Fixed POS terminal, SoftPOS where supported, Device owner, Last service, Replacement date. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 48 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 48"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 48"
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
       "label": "Fixed POS terminal",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "SoftPOS where supported",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Device owner",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Last service",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Replacement date",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 48 §Support"
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
   "loading": "The payment terminal device list.",
   "error": "Could not load. Names which read failed and leaves the payment terminal device untouched.",
   "emptyFirstRun": "No payment terminal device yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment terminal device are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentTerminals",
    "contract": "payments",
    "purpose": "The inventory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listDevices",
    "contract": "tenancy",
    "purpose": "The device register behind it",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listPaymentTerminalCertifications",
    "contract": "payments",
    "purpose": "Terminal model certifications",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordPaymentTerminalCertification",
    "contract": "payments",
    "purpose": "Record a terminal model certification",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-580",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-580"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 48. 0 of 0 labels bound to a contract property; 5 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "modelCode",
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
  "id": "ADM-581",
  "name": "Terminal Provisioning & Device Configuration\\t51",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "3",
   "page": 50
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/terminal-provisioning-device-configuration-t51-adm-581",
   "component": "apps/ticvai-web/src/routes/commercial/TerminalProvisioningDeviceConfigurationT51.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Configure and activate a physical terminal for TICVAI use.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Device reference, Receipt configuration, Connection profile. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 50 §Support"
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
       "label": "Tenant",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Location",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "POS",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Acquirer",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Merchant Account",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Terminal Profile",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Select"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Device reference",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Receipt configuration",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Connection profile",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 50 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The terminal provisioning device configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the terminal provisioning device untouched.",
   "emptyFirstRun": "No terminal provisioning device configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "enrolDevice",
    "contract": "tenancy",
    "purpose": "Provision the device",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setPaymentTerminalConfiguration",
    "contract": "payments",
    "purpose": "Its payment configuration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentTerminals"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-581",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-581"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 50. 0 of 0 labels bound to a contract property; 12 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "deviceId",
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
  "id": "ADM-582",
  "name": "POS, Kiosk & Terminal Assignment Manager\\t52",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "4",
   "page": 51
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pos-kiosk-terminal-assignment-manager-t52-adm-582",
   "component": "apps/ticvai-web/src/routes/commercial/PosKioskTerminalAssignmentManagerT52.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control which terminal is connected or assigned to each TICVAI selling device.",
  "gaps": [
   {
    "operation": null,
    "why": "**POS, Kiosk & Terminal Assignment Manager\\t52 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 51"
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
       "impliedBy": "setDeviceAssignment",
       "label": "Save device assignment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setDeviceAssignment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pos kiosk terminal list.",
   "error": "Could not load. Names which read failed and leaves the pos kiosk terminal untouched.",
   "emptyFirstRun": "No pos kiosk terminal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pos kiosk terminal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDeviceAssignment",
    "contract": "tenancy",
    "purpose": "Assign it to a workstation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-582",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-582"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "deviceId",
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
  "id": "ADM-583",
  "name": "EMV & Card-Present Processing Configuration\\t53",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "5",
   "page": 52
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/emv-card-present-processing-configuration-t53-adm-583",
   "component": "apps/ticvai-web/src/routes/commercial/EmvCardPresentProcessingConfigurationT53.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure card-present transaction capabilities without exposing sensitive cardholder data.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Sale",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authorization",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Capture",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Void",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reversal",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Preauthorization where supported",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Completion where supported",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 52 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The emv card-present processing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the emv card-present processing untouched.",
   "emptyFirstRun": "No emv card-present processing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setPaymentTerminalConfiguration",
    "contract": "payments",
    "purpose": "EMV and card-present settings",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentTerminals"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-583",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-583"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 52. 0 of 0 labels bound to a contract property; 8 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-584",
  "name": "Payment Server & Terminal Connectivity Manager\\t54",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "6",
   "page": 53
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-server-terminal-connectivity-manager-t54-adm-584",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentServerTerminalConnectivityManagerT54.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Monitor and configure the communication path between TICVAI POS, payment terminal, payment server and payment provider.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 53 §Show"
   },
   {
    "operation": null,
    "why": "**Payment Server & Terminal Connectivity Manager\\t54 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Every payment server terminal",
       "columns": [
        "POS ↔ Terminal",
        "Terminal ↔ Payment Server",
        "Payment Server ↔ Provider",
        "Provider ↔ Acquirer"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 53 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment server terminal",
       "bindsTo": null,
       "columns": [
        "POS ↔ Terminal",
        "Terminal ↔ Payment Server",
        "Payment Server ↔ Provider",
        "Provider ↔ Acquirer"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Architecture Example”, “Terminal Integration Layer”, “Payment Terminal”, “Payment Server / Provider”, “Depending on integration”, “Health Indicators”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 53 §Show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Connectivity test, Terminal ping/health test where supported, Provider reachability, Merchant validation, Configuration validation. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 53 §Authorized users can run"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment server terminal list.",
   "error": "Could not load. Names which read failed and leaves the payment server terminal untouched.",
   "emptyFirstRun": "No payment server terminal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment server terminal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getDeviceTelemetry",
    "contract": "tenancy",
    "purpose": "Connectivity over time",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "POS ↔ Terminal",
    "Terminal ↔ Payment Server",
    "Payment Server ↔ Provider",
    "Provider ↔ Acquirer"
   ],
   "params": [
    {
     "name": "deviceId",
     "from": "session"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-584",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-584"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 53. 0 of 4 labels bound to a contract property; 9 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-585",
  "name": "Card-Present Transaction Monitor & Operations\\t55",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "7",
   "page": 54
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/card-present-transaction-monitor-operations-t55-adm-585",
   "component": "apps/ticvai-web/src/routes/commercial/CardPresentTransactionMonitorOperationsT55.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide operations teams with real-time visibility into card-present payment attempts.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 54 §Display"
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
       "label": "Search card-present transaction operations\\t55",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 54 §Search/filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "TICVAI Payment ID",
        "Order",
        "POS",
        "Terminal",
        "Venue",
        "Provider",
        "Acquirer",
        "Date/time",
        "Amount",
        "Currency",
        "Status",
        "Operator"
       ],
       "notes": "The pack filters this screen by ticvai payment id, order, pos, terminal, venue, provider and 6 more — which are present is a decision the pack already made.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 54 §Search/filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every card-present transaction operations\\t55",
       "columns": [
        "Payment ID",
        "Order ID",
        "Terminal",
        "POS",
        "Amount",
        "Currency",
        "Provider",
        "Merchant account",
        "Card scheme",
        "Entry method",
        "Authorization result",
        "Processing duration",
        "Status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 54 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected card-present transaction operations\\t55",
       "bindsTo": null,
       "columns": [
        "Payment ID",
        "Order ID",
        "Terminal",
        "POS",
        "Amount",
        "Currency",
        "Provider",
        "Merchant account",
        "Card scheme",
        "Entry method",
        "Authorization result",
        "Processing duration",
        "Status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Important”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 54 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The card-present transaction operations\\t55 list.",
   "error": "Could not load. Names which read failed and leaves the card-present transaction operations\\t55 untouched.",
   "emptyFirstRun": "No card-present transaction operations\\t55 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the card-present transaction operations\\t55 are still there. The pack's own statuses are Initiated — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentTerminals",
    "contract": "payments",
    "purpose": "Live card-present operations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Payment ID",
    "Order ID",
    "Terminal",
    "POS",
    "Amount",
    "Currency"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-585",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-585"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 54. 0 of 25 labels bound to a contract property; 36 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-586",
  "name": "Degraded, Offline & Store-and-Forward Manager\\t56",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "8",
   "page": 55
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/degraded-offline-store-and-forward-manager-t56-adm-586",
   "component": "apps/ticvai-web/src/routes/commercial/DegradedOfflineStoreAndForwardManagerT56.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Manage card-present operations when normal connectivity is unavailable. This directly addresses the degraded-mode requirement in the payment matrix.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 55 §Show"
   },
   {
    "operation": null,
    "why": "**Degraded, Offline & Store-and-Forward Manager\\t56 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Every degraded offline store-and-forward",
       "columns": [
        "Terminal",
        "Transaction",
        "Amount",
        "Timestamp",
        "Offline reason",
        "Retry status",
        "Synchronization state"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 55 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected degraded offline store-and-forward",
       "bindsTo": null,
       "columns": [
        "Terminal",
        "Transaction",
        "Amount",
        "Timestamp",
        "Offline reason",
        "Retry status",
        "Synchronization state"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Important Principle”, “Synchronization”.",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 55 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The degraded offline store-and-forward list.",
   "error": "Could not load. Names which read failed and leaves the degraded offline store-and-forward untouched.",
   "emptyFirstRun": "No degraded offline store-and-forward yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the degraded offline store-and-forward are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStoredForwardTransactions",
    "contract": "payments",
    "purpose": "What is held offline",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setPaymentTerminalConfiguration",
    "contract": "payments",
    "purpose": "Store-and-forward limits",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentTerminals"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Terminal",
    "Transaction",
    "Amount",
    "Timestamp",
    "Offline reason",
    "Retry status"
   ],
   "params": [
    {
     "name": "terminalId",
     "from": "session"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-586",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-586"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 55. 0 of 7 labels bound to a contract property; 15 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-587",
  "name": "Terminal Health, Maintenance & Incident Center\\t57",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "9",
   "page": 56
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/terminal-health-maintenance-incident-center-t57-adm-587",
   "component": "apps/ticvai-web/src/routes/commercial/TerminalHealthMaintenanceIncidentCenterT57.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide centralized lifecycle monitoring and operational maintenance of terminal hardware.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Device replacement, Certification update. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 56 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 56"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 56"
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
       "label": "Device replacement",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 56 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Certification update",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 56 §Support"
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
   "loading": "The terminal health maintenance list.",
   "error": "Could not load. Names which read failed and leaves the terminal health maintenance untouched.",
   "emptyFirstRun": "No terminal health maintenance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the terminal health maintenance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getDeviceTelemetry",
    "contract": "tenancy",
    "purpose": "Terminal health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createWorkOrder",
    "contract": "maintenance",
    "purpose": "Raise a repair",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listDeviceFirmware",
    "contract": "tenancy",
    "purpose": "Terminal firmware versions across the fleet",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getDeviceFirmware",
    "contract": "tenancy",
    "purpose": "Open a release",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "createDeviceFirmware",
    "contract": "tenancy",
    "purpose": "Register a terminal firmware release",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-587",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-587"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 56. 0 of 0 labels bound to a contract property; 2 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "deviceId",
     "from": "session"
    },
    {
     "name": "firmwareId",
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
  "id": "ADM-588",
  "name": "Terminal Simulator, Certification & AI Operations Advisor\\t59",
  "module": "Commercial",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Payment_Payment_Orchestration.pdf",
   "board": "3",
   "number": "10",
   "page": 58
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/terminal-simulator-certification-ai-operations-advisor-t-adm-588",
   "component": "apps/ticvai-web/src/routes/commercial/TerminalSimulatorCertificationAiOperationsAdviso.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-579"
   ],
   "exitTo": [
    "ADM-579"
   ],
   "transitions": [
    {
     "to": "ADM-579",
     "trigger": "Back to Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select; Terminal Receipt Configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide a controlled environment to validate terminal configuration and payment flows before production activation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Successful payment, Card decline, Lost connection, Reversal, Duplicate request, Temporary assignment, Venue, Assignment history. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Payment_Payment_Orchestration.pdf, page 58 §Support simulation/test flows for"
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
       "label": "Tenant",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "POS",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Terminal",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Merchant account",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Transaction amount",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Transaction type",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Connectivity state",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Merchant receipt",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Terminal Receipt Configuration"
      },
      {
       "kind": "selectField",
       "label": "Customer receipt",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Terminal Receipt Configuration"
      },
      {
       "kind": "selectField",
       "label": "Printed",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Terminal Receipt Configuration"
      },
      {
       "kind": "selectField",
       "label": "Digital",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Terminal Receipt Configuration"
      },
      {
       "kind": "selectField",
       "label": "Combined TICVAI receipt",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Terminal Receipt Configuration"
      },
      {
       "kind": "selectField",
       "label": "Terminal-only receipt",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Terminal Receipt Configuration"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Successful payment",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Support simulation/test flows for"
      },
      {
       "kind": "secondaryButton",
       "label": "Card decline",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Support simulation/test flows for"
      },
      {
       "kind": "secondaryButton",
       "label": "Lost connection",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Support simulation/test flows for"
      },
      {
       "kind": "secondaryButton",
       "label": "Reversal",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Support simulation/test flows for"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate request",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Support simulation/test flows for"
      },
      {
       "kind": "secondaryButton",
       "label": "Temporary assignment",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Assignment history",
       "provenance": "pack Payment_Payment_Orchestration.pdf, page 58 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The terminal simulator certification configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the terminal simulator certification untouched.",
   "emptyFirstRun": "No terminal simulator certification configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "testPaymentProviderConnection",
    "contract": "payments",
    "purpose": "Certify the terminal path",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPaymentProviderConnections"
    ]
   },
   {
    "operationId": "listPaymentTerminalCertifications",
    "contract": "payments",
    "purpose": "Terminal model certifications",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordPaymentTerminalCertification",
    "contract": "payments",
    "purpose": "Record a terminal model certification",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-588",
   "workshopBoard": "wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-588"
  },
  "apisNote": "Regenerated 9 September 2026 from Payment_Payment_Orchestration.pdf page 58. 0 of 0 labels bound to a contract property; 24 of 232 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "connectionId",
     "from": "navigation"
    },
    {
     "name": "modelCode",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "createDeviceFirmware": {
  "method": "POST",
  "path": "/device-firmware",
  "contract": "tenancy",
  "summary": "Register a firmware or software release before it is deployed",
  "permission": "DEVICE_MANAGE",
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
  "requestBody": "DeviceFirmware",
  "responds": "DeviceFirmware"
 },
 "createWorkOrder": {
  "method": "POST",
  "path": "/work-orders",
  "contract": "maintenance",
  "summary": "Raise a work order",
  "permission": "WORK_ORDER_MANAGE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateWorkOrderRequest",
  "responds": "WorkOrder"
 },
 "enrolDevice": {
  "method": "POST",
  "path": "/devices/{deviceId}/enrolment",
  "contract": "tenancy",
  "summary": "Take a registered device through enrolment to activation",
  "permission": "DEVICE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "DeviceEnrolment",
  "responds": "RegisteredDevice"
 },
 "getDeviceFirmware": {
  "method": "GET",
  "path": "/device-firmware/{firmwareId}",
  "contract": "tenancy",
  "summary": "Read one firmware release, and how much of the fleet is on it",
  "permission": "DEVICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "DeviceFirmware"
 },
 "getDeviceTelemetry": {
  "method": "GET",
  "path": "/devices/{deviceId}/telemetry",
  "contract": "tenancy",
  "summary": "Battery, performance and consumables over time",
  "permission": "DEVICE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
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
   },
   {
    "name": "metric",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DeviceTelemetryPoint"
 },
 "listDeviceFirmware": {
  "method": "GET",
  "path": "/device-firmware",
  "contract": "tenancy",
  "summary": "Firmware and software versions, and what is running where",
  "permission": "DEVICE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "deviceKind",
    "in": "query",
    "required": null
   },
   {
    "name": "version",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DeviceFirmware"
 },
 "listDevices": {
  "method": "GET",
  "path": "/devices",
  "contract": "tenancy",
  "summary": "List registered devices",
  "permission": "DEVICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
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
 "listPaymentTerminalCertifications": {
  "method": "GET",
  "path": "/payment-terminal-certifications",
  "contract": "payments",
  "summary": "EMV and PCI certification of each terminal model and kernel",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "modelCode",
    "in": "query",
    "required": null
   },
   {
    "name": "expiringBefore",
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
 "listPaymentTerminals": {
  "method": "GET",
  "path": "/payment-terminals",
  "contract": "payments",
  "summary": "Terminals, and the payment configuration on each",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PaymentTerminal"
 },
 "listStoredForwardTransactions": {
  "method": "GET",
  "path": "/payment-terminals/{terminalId}/forwarded",
  "contract": "payments",
  "summary": "What a terminal took offline and has not yet sent",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "StoredForwardTransaction"
 },
 "recordPaymentTerminalCertification": {
  "method": "PUT",
  "path": "/payment-terminal-certifications/{modelCode}",
  "contract": "payments",
  "summary": "Record a terminal model's EMV and PCI certification",
  "permission": "PAYMENT_PROVIDER_MANAGE",
  "offlineCapable": false,
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
  "requestBody": "PayTerminalCertification",
  "responds": "PayTerminalCertification"
 },
 "setDeviceAssignment": {
  "method": "PUT",
  "path": "/devices/{deviceId}/assignment",
  "contract": "tenancy",
  "summary": "Who owns it, who holds it, and where it is",
  "permission": "DEVICE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "DeviceAssignment",
  "responds": "DeviceAssignment"
 },
 "setPaymentTerminalConfiguration": {
  "method": "PUT",
  "path": "/payment-terminals",
  "contract": "payments",
  "summary": "Merchant account, acquirer, EMV and offline behaviour",
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
  "requestBody": "PaymentTerminal",
  "responds": "PaymentTerminal"
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
 "CreateWorkOrderRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "title",
   "venueId",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "title": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 5000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderKind"
     }
    ],
    "default": "corrective"
   },
   "priority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderPriority"
     }
    ],
    "description": "**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"
   },
   "faultAssessment": {
    "$ref": "#/components/schemas/WorkOrderFaultAssessment"
   },
   "requiredQualificationCodes": {
    "type": "array",
    "maxItems": 10,
    "items": {
     "type": "string"
    },
    "description": "Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "attachmentRefs": {
    "type": "array",
    "description": "Photo-first. Expected at creation, not added later from memory.",
    "items": {
     "type": "string"
    }
   },
   "takeAssetOutOfService": {
    "type": "boolean",
    "default": false,
    "description": "Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DeviceAssignment": {
  "type": "object",
  "x-ticvai-persistence": "tenancy.device_assignment",
  "description": "16.2.9 to 16.2.11. **Ownership, custody and location are three facts, not one.**",
  "properties": {
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `setDeviceAssignment`."
   },
   "ownerOrgUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who the device belongs to — the cost centre that replaces it when it breaks."
   },
   "custodianPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Who is holding it right now.** The fact a loss investigation needs."
   },
   "assignedWorkstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationScopePath": {
    "type": "string",
    "nullable": true
   },
   "lastSeenLocation": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Reported by the heartbeat; distinct from where it is supposed to be."
   },
   "assetTag": {
    "type": "string",
    "nullable": true
   },
   "acquiredAt": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "A calendar date in the region's time zone."
   },
   "warrantyExpiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "A calendar date in the region's time zone."
   },
   "assignedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "DeviceCapability": {
  "type": "string",
  "description": "BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n",
  "enum": [
   "genderClassification"
  ]
 },
 "DeviceEnrolment": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "description": "BL-160. **The body `enrolDevice` accepts, named so that it writes.**\nIt was an anonymous inline object, and `derive-lineage` reads writes from the schema an operation accepts — so the one operation that moves a device through its whole lifecycle recorded no writes at all, and `platform.device` looked like a table only `registerDevice` touched.\n**Provisioning is inside enrolment rather than beside it**, which is why `configurationProfileId` is here: a device that is enrolled but unprovisioned is a device that will fail at the gate on its first morning.\n",
  "required": [
   "state"
  ],
  "properties": {
   "state": {
    "type": "string",
    "enum": [
     "enrolled",
     "provisioned",
     "active",
     "deactivated",
     "retired"
    ],
    "description": "**The target state, not the current one.** `registered` is absent because `registerDevice` is what produces it and nothing transitions back to it.\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "description": "**Recorded on the `tenancy.device_audit` row, not on the device.** Required in practice for `deactivated` and `retired`, where an investigation six months later needs to know why a gate stopped working.\n"
   }
  }
 },
 "DeviceFirmware": {
  "type": "object",
  "x-ticvai-persistence": "tenancy.device_firmware",
  "description": "16.6.30 and 16.6.32. **A release, and how much of the fleet is on it.** Written by `createDeviceFirmware` and moved through its life by `setDeviceFirmwareStatus` (29 September, build pass); `startDeviceFirmwareRollout` deploys only a `released` one.\n",
  "required": [
   "deviceKind",
   "version"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "deviceKind": {
    "type": "string"
   },
   "version": {
    "type": "string"
   },
   "vendor": {
    "type": "string",
    "nullable": true,
    "description": "Who built the image, as the device's driver names its maker."
   },
   "checksumAlgorithm": {
    "type": "string",
    "enum": [
     "sha256",
     "sha512"
    ],
    "default": "sha256"
   },
   "releaseNotes": {
    "type": "string",
    "nullable": true
   },
   "artefactAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "checksum": {
    "type": "string",
    "nullable": true
   },
   "minimumPreviousVersion": {
    "type": "string",
    "nullable": true,
    "description": "**Some updates cannot be applied from any starting point.** Naming the floor is how a two-step upgrade stays possible instead of bricking the devices that skipped one.\n"
   },
   "releasedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "Set when `setDeviceFirmwareStatus` first makes the release `released`."
   },
   "installedCount": {
    "type": "integer",
    "readOnly": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "default": "draft",
    "enum": [
     "draft",
     "released",
     "deprecated",
     "withdrawn"
    ]
   },
   "statusReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The `reason` given when the release was deprecated or withdrawn."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant the release belongs to. Releases are tenant-wide; rollouts narrow them."
   }
  }
 },
 "DeviceKind": {
  "type": "string",
  "enum": [
   "receiptPrinter",
   "ticketPrinter",
   "labelPrinter",
   "cashDrawer",
   "barcodeScanner",
   "rfidReader",
   "nfcReader",
   "cardReader",
   "idReader",
   "biometricReader",
   "accessReader",
   "paymentTerminal",
   "customerDisplay",
   "signageDisplay",
   "kitchenDisplay",
   "turnstileController",
   "wristbandEncoder",
   "signaturePad",
   "scale",
   "camera",
   "mobileHandset"
  ],
  "description": "`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n"
 },
 "DeviceTelemetryPoint": {
  "type": "object",
  "x-ticvai-persistence": "tenancy.device_telemetry",
  "description": "16.4.21 and 16.4.22. **A series, because degradation is not visible in a point-in-time reading.**\n",
  "properties": {
   "deviceId": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "batteryPercent": {
    "type": "integer",
    "nullable": true
   },
   "batteryHealthPercent": {
    "type": "integer",
    "nullable": true
   },
   "charging": {
    "type": "boolean",
    "nullable": true
   },
   "signalStrength": {
    "type": "integer",
    "nullable": true
   },
   "cpuPercent": {
    "type": "number",
    "nullable": true
   },
   "memoryPercent": {
    "type": "number",
    "nullable": true
   },
   "storageFreeMb": {
    "type": "integer",
    "nullable": true
   },
   "consumables": {
    "type": "object",
    "additionalProperties": true,
    "description": "Paper, ribbon, wristband stock — whatever the device kind reports."
   },
   "uptimeSeconds": {
    "type": "integer",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
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
 "PayTerminalCertification": {
  "type": "object",
  "x-ticvai-persistence": "payments.terminal_certification + payments.terminal_certification_level3",
  "description": "4.3.1. Also the `recordPaymentTerminalCertification` body. **One per terminal model**; a terminal names its model in `PaymentTerminal.terminalModelCode`.",
  "required": [
   "modelCode",
   "manufacturer"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "modelCode": {
    "type": "string",
    "maxLength": 100
   },
   "manufacturer": {
    "type": "string",
    "maxLength": 200
   },
   "emvLevel1ApprovalReference": {
    "type": "string",
    "nullable": true
   },
   "emvLevel1ExpiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "emvLevel2KernelVersions": {
    "type": "array",
    "description": "Contact and contactless kernels with their EMVCo approval, e.g. `EMV Contact 4.3 / ref`.",
    "items": {
     "type": "string"
    }
   },
   "emvLevel2ExpiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "level3Certifications": {
    "type": "array",
    "description": "Per acquirer and card scheme; a terminal is activated only against an acquirer listed here and not expired.",
    "items": {
     "type": "object",
     "properties": {
      "acquirerConnectionId": {
       "type": "string",
       "format": "uuid"
      },
      "cardScheme": {
       "type": "string"
      },
      "reference": {
       "type": "string"
      },
      "certifiedAt": {
       "type": "string",
       "format": "date"
      },
      "expiresAt": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "pciPtsApprovalNumber": {
    "type": "string",
    "nullable": true
   },
   "pciPtsExpiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "documentAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `tenant` scope."
   }
  }
 },
 "PaymentTerminal": {
  "type": "object",
  "x-ticvai-persistence": "payments.terminal",
  "description": "Board 3. **The payment layer on a `tenancy` device**, not a second device register.",
  "required": [
   "deviceId"
  ],
  "properties": {
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "description": "The `tenancy.RegisteredDevice`. **Enrolment, credentials, firmware and tamper state live there.**"
   },
   "merchantAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "acquirerConnectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "terminalIdentifier": {
    "type": "string",
    "nullable": true
   },
   "emvConfigurationVersion": {
    "type": "string",
    "nullable": true
   },
   "terminalModelCode": {
    "type": "string",
    "nullable": true,
    "description": "4.3.1. The model whose EMV and PCI certification applies (`listPaymentTerminalCertifications`)."
   },
   "entryModes": {
    "type": "array",
    "description": "4.3.2. The card entry modes this terminal accepts. **`magstripe` (swipe) is off unless listed**, since a swiped card carries no chip cryptogram; it stays available as a fallback where the acquirer allows it.",
    "items": {
     "type": "string",
     "enum": [
      "chip",
      "contactless",
      "magstripe",
      "manualEntry",
      "mobileWallet"
     ]
    }
   },
   "dccEnabled": {
    "type": "boolean",
    "default": false,
    "description": "4.3.2. Offer Dynamic Currency Conversion on a foreign card at this terminal. The rate is the provider's and is recorded on the payment (`fxRateSource` `cardScheme`); the ledger still holds the base currency."
   },
   "dccProviderConnectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "contactlessLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "pinBypassAllowed": {
    "type": "boolean",
    "default": false
   },
   "storeAndForward": {
    "type": "object",
    "description": "**A risk decision, not a technical one.**",
    "properties": {
     "enabled": {
      "type": "boolean",
      "default": false
     },
     "floorLimit": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "maximumHeldTotal": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "maximumAgeMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "unconfigured",
     "active",
     "offline",
     "suspended"
    ]
   },
   "scopePath": {
    "type": "string"
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
 "RegisteredDevice": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "description": "**The device register of record** (decided 29 September, build pass). Identity, enrolment, credential, firmware and push registration for every device in the estate live on this row. `access.access_device` places access-control devices in the gate topology and repeats serial, versions, health and lifecycle; the two are not merged yet, and where they disagree this row wins.\n",
  "required": [
   "id",
   "kind",
   "driver"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/DeviceKind"
   },
   "driver": {
    "type": "string",
    "description": "Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"
   },
   "identifier": {
    "type": "string",
    "nullable": true
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September); `registerDevice` refuses either mistake with `422`.\n"
   },
   "model": {
    "type": "string",
    "nullable": true
   },
   "pushToken": {
    "type": "string",
    "format": "password",
    "nullable": true,
    "writeOnly": true,
    "description": "BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"
   },
   "pushPlatform": {
    "type": "string",
    "nullable": true,
    "enum": [
     "ios",
     "android",
     "web",
     "windows"
    ]
   },
   "pushFailureCount": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "description": "**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"
   },
   "offlineScope": {
    "type": "string",
    "nullable": true,
    "enum": [
     "none",
     "readOnly",
     "sellAndScan",
     "fullVenue"
    ],
    "description": "BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"
   },
   "firmwareVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "As the device last reported it on its heartbeat."
   },
   "isRequired": {
    "type": "boolean",
    "description": "True blocks shift open when the device is unreachable."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "online",
     "offline",
     "error",
     "consumableLow",
     "needsAttention",
     "unknown"
    ],
    "description": "What the device last said on its heartbeat; `unknown` until it has."
   },
   "batteryPercent": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "minimum": 0,
    "maximum": 100,
    "description": "Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"
   },
   "health": {
    "type": "string",
    "enum": [
     "healthy",
     "warning",
     "degraded",
     "offline",
     "unknown"
    ],
    "default": "unknown",
    "readOnly": true,
    "description": "**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "capabilities": {
    "type": "array",
    "readOnly": true,
    "items": {
     "$ref": "#/components/schemas/DeviceCapability"
    },
    "description": "BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"
   },
   "enrolmentState": {
    "type": "string",
    "enum": [
     "registered",
     "enrolled",
     "provisioned",
     "active",
     "deactivated",
     "retired"
    ],
    "default": "registered",
    "readOnly": true,
    "description": "BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"
   },
   "retiredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"
   }
  }
 },
 "StoredForwardTransaction": {
  "type": "object",
  "x-ticvai-persistence": "payments.stored_forward",
  "description": "Board 3.8. **Money taken that the platform does not yet know about.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "deviceId": {
    "type": "string",
    "format": "uuid"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "takenAt": {
    "type": "string",
    "format": "date-time"
   },
   "maskedPan": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "forwarding",
     "accepted",
     "rejected",
     "expired"
    ]
   },
   "attempts": {
    "type": "integer",
    "default": 0
   },
   "rejectionReason": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
  "x-ticvai-retired-columns": [
   "is_overdue"
  ],
  "type": "object",
  "required": [
   "id",
   "workOrderNumber",
   "title",
   "venueId",
   "status",
   "priority",
   "kind",
   "createdAt"
  ],
  "properties": {
   "downtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"
   },
   "rootCause": {
    "type": "string",
    "nullable": true,
    "enum": [
     "wearAndTear",
     "operatorError",
     "guestDamage",
     "manufacturingDefect",
     "environmental",
     "softwareFault",
     "powerFailure",
     "deferredMaintenance",
     "unknown"
    ],
    "description": "**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"
   },
   "rootCauseNote": {
    "type": "string",
    "nullable": true
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "escalationLevel": {
    "type": "integer",
    "default": 0,
    "description": "**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"
   },
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "workOrderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
   },
   "title": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "readOnly": true,
    "description": "The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."
   },
   "prioritySource": {
    "type": "string",
    "enum": [
     "scored",
     "assetOverride",
     "manual"
    ],
    "readOnly": true,
    "description": "Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."
   },
   "faultAssessment": {
    "$ref": "#/components/schemas/WorkOrderFaultAssessment"
   },
   "requiredQualificationCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Skills the job needs (M17-13)."
   },
   "kind": {
    "$ref": "#/components/schemas/WorkOrderKind"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"
   },
   "elapsedMinutes": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"
   },
   "isTimerRunning": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"
   },
   "requiresVerification": {
    "type": "boolean"
   },
   "sourcePlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceInspectionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkOrderFaultAssessment": {
  "x-ticvai-persistence": "none — columns on maintenance.work_order",
  "type": "object",
  "description": "What the person raising a fault says about it, which the priority score reads (M17-01).",
  "properties": {
   "safetyRisk": {
    "type": "boolean",
    "default": false
   },
   "guestImpact": {
    "type": "string",
    "enum": [
     "none",
     "degraded",
     "closed"
    ],
    "default": "none"
   }
  }
 },
 "WorkOrderKind": {
  "type": "string",
  "enum": [
   "corrective",
   "planned",
   "inspectionFollowUp",
   "incidentCorrective",
   "improvement"
  ]
 },
 "WorkOrderPriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent",
   "emergency"
  ]
 },
 "WorkOrderStatus": {
  "type": "string",
  "enum": [
   "open",
   "assigned",
   "inProgress",
   "paused",
   "awaitingParts",
   "completed",
   "verified",
   "closed",
   "cancelled"
  ]
 }
}
```
