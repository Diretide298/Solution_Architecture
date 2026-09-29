# WS195 — Wallet Configuration Backend Structure v1.0 board 10

**10 screens · 19 operations · 19 schemas · 7 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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
  `APPROVAL_REQUEST, DEVELOPER_MANAGE, DEVELOPER_VIEW, PERMISSION_VIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1173` | Wallet Integration Command Center | commandCentre | 6 | 1 | — |
| `BO-1174` | Wallet API Catalogue & Endpoint Configuration | configEditor | 1 | 0 | — |
| `BO-1175` | Integration Profile & System Mapping | configEditor | 2 | 0 | — |
| `BO-1176` | Wallet Events, Webhooks & Notification Orchestration | configEditor | 2 | 0 | — |
| `BO-1177` | API Security, Access & Integration Permissions | configEditor | 2 | 0 | — |
| `BO-1178` | Synchronization, Retry & Resilience Configuration | configEditor | 1 | 0 | — |
| `BO-1179` | Integration Monitoring & Exception Workbench | listDetail | 8 | 1 | — |
| `BO-1180` | Wallet Configuration Governance & Version Control | listDetail | 1 | 0 | — |
| `BO-1181` | Approval, Publication & Change Management | configEditor | 2 | 0 | — |
| `BO-1182` | Wallet Platform Health, Audit & Administration Center | commandCentre | 1 | 0 | — |

## Thin screens in this batch

**BO-1180 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1173",
  "name": "Wallet Integration Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "01",
   "page": 115
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-integration-command-center-bo-1173",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletIntegrationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1174",
    "BO-1175",
    "BO-1176",
    "BO-1177",
    "BO-1178",
    "BO-1179",
    "BO-1180",
    "BO-1181",
    "BO-1182"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1174",
     "trigger": "Wallet API Catalogue & Endpoint Configuration",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1175",
     "trigger": "Integration Profile & System Mapping",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1176",
     "trigger": "Wallet Events, Webhooks & Notification Orchestration",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1177",
     "trigger": "API Security, Access & Integration Permissions",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1178",
     "trigger": "Synchronization, Retry & Resilience Configuration",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1179",
     "trigger": "Integration Monitoring & Exception Workbench",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "carries": [
      "clientId",
      "subscriptionId"
     ]
    },
    {
     "to": "BO-1180",
     "trigger": "Wallet Configuration Governance & Version Control",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1181",
     "trigger": "Approval, Publication & Change Management",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1182",
     "trigger": "Wallet Platform Health, Audit & Administration Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each integration displays) — counts over a population, then the population",
  "purpose": "Provide administrators and technical operations teams with a centralized view of all Wallet integrations and API activity.",
  "purposeNote": "Authorized administrators can monitor Wallet connectivity and identify failed, degraded or delayed integrations from a centralized workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Each integration displays"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search wallet integration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Integration",
        "API",
        "Environment",
        "Status",
        "Transaction type",
        "Date/time"
       ],
       "notes": "The pack filters this screen by tenant, venue, integration, api, environment, status and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Filters"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Takes effect at every till and reader immediately.** Credit types, consumption order and funding rules change for balances that already exist, not only for new ones.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Integrations",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Connected TICVAI Modules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "External Integrations",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "API Requests Today",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Successful API Requests",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Failed API Requests",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "API Success Rate",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Average Response Time",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Webhook Events",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Failed Webhooks",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Synchronization Failures",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Integration Alerts",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Connected TICVAI Domains",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Display"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every wallet integration",
       "columns": [
        "Healthy",
        "Degraded",
        "Delayed",
        "Failed",
        "Suspended",
        "Maintenance"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Each integration displays"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet integration",
       "bindsTo": null,
       "columns": [
        "Healthy",
        "Degraded",
        "Delayed",
        "Failed",
        "Suspended",
        "Maintenance"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Display connectivity with”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Each integration displays"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create Integration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View API Health",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry Failed Event",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Open Error Log",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Quick Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend Integration",
       "operation": "setApiClientStatus",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Test Connection",
       "operation": "testWebhookSubscription",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Quick Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendIntegration",
    "component": "confirmDialog",
    "trigger": "Suspend Integration",
    "body": "**Suspend Integration on a wallet integration is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 115 §Quick Actions"
   }
  ],
  "states": {
   "loading": "The wallet integration list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the wallet integration untouched.",
   "emptyFirstRun": "No wallet integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishWalletConfiguration",
    "contract": "wallet",
    "purpose": "Configuration state",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes",
     "listCreditTypes"
    ]
   },
   {
    "operationId": "createApiClient",
    "contract": "public-api",
    "purpose": "Register a new wallet integration with its scopes",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Create Integration; Retry Failed Event"
   },
   {
    "operationId": "replayEvents",
    "contract": "public-api",
    "purpose": "Re-deliver failed wallet events",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Create Integration; Retry Failed Event"
   },
   {
    "operationId": "listWebhookSubscriptions",
    "contract": "public-api",
    "purpose": "The webhook subscriptions to test or replay",
    "trigger": "onLoad"
   },
   {
    "operationId": "setApiClientStatus",
    "contract": "public-api",
    "purpose": "Suspend integration",
    "trigger": "onAction"
   },
   {
    "operationId": "testWebhookSubscription",
    "contract": "public-api",
    "purpose": "Test connection",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1173",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1173"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 115. 0 of 14 labels bound to a contract property; 33 of 54 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Create Integration: `createApiClient`; Retry Failed Event: `replayEvents`; View API Health, Open Error Log dropped (navigation); still owed by a contract change: `setApiClientStatus`, `testWebhookSubscription`.",
  "entryState": {
   "params": [
    {
     "name": "clientId",
     "from": "navigation"
    },
    {
     "name": "subscriptionId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1174",
  "name": "Wallet API Catalogue & Endpoint Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "02",
   "page": 117
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-api-catalogue-endpoint-configuration-bo-1174",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletApiCatalogueEndpointConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure APIs for; For each API define) and no display directory — it is settings, not a population",
  "purpose": "Define and govern the API services exposed by the TICVAI Wallet Engine. Requirement 4.3.34 explicitly requires APIs supporting wallet operations. Core Wallet APIs",
  "purposeNote": "Every wallet capability exposed externally is registered, secured, versioned and governed through the Wallet API catalogue.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet Management",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Create Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Retrieve Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Update Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Block Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Unblock Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Balance Inquiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "textField",
       "label": "Balance by Credit Type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Available Balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Reserved Balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Transaction History",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Transaction Detail",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Wallet Payment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Wallet Redemption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Fund Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Top-Up",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Auto-Reload",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Transfers",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Wallet-to-Wallet Transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Transfer Status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Refunds",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Refund to Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Refund Status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "textField",
       "label": "Gift Cards / Benefits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Gift Card Balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Voucher Validation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      },
      {
       "kind": "selectField",
       "label": "Benefit Inquiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 117 §Configure APIs for"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet api catalogue configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet api catalogue untouched.",
   "emptyFirstRun": "No wallet api catalogue configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listWalletTypes",
    "contract": "wallet",
    "purpose": "What the API exposes",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1174",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1174"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 117. 0 of 0 labels bound to a contract property; 46 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1175",
  "name": "Integration Profile & System Mapping",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "03",
   "page": 118
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/integration-profile-system-mapping-bo-1175",
   "component": "apps/venue-management-web/src/routes/orders-money/IntegrationProfileSystemMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how TICVAI Wallet communicates with internal modules and approved external systems. Requirement 4.3.20 requires wallet integration with both internal and external systems through APIs.",
  "purposeNote": "Each connected platform has an explicit integration profile and controlled mapping to TICVAI wallet objects.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Integration name",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "System type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Environment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Base endpoint",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authentication profile",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supported operations",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Timeout",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retry policy",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Error handling",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Data mapping",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Field mapping",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Currency mapping",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Status mapping",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Credit-type mapping",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Date/time mapping",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 118 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save mapping",
       "operation": "setWalletIntegrationMapping",
       "provenance": "contract wallet.yaml PUT /wallet-integration-mappings (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The integration profile system configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the integration profile system untouched.",
   "emptyFirstRun": "No integration profile system configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "Integration profile",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   },
   {
    "operationId": "setWalletIntegrationMapping",
    "contract": "wallet",
    "purpose": "Save mapping",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1175",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1175"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 118. 0 of 0 labels bound to a contract property; 20 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setWalletIntegrationMapping`.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1176",
  "name": "Wallet Events, Webhooks & Notification Orchestration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "04",
   "page": 119
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-events-webhooks-notification-orchestration-bo-1176",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletEventsWebhooksNotificationOrchestration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "clientId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For each subscriber configure) and no display directory — it is settings, not a population",
  "purpose": "Configure event-driven communication when something changes in Wallet.",
  "purposeNote": "Wallet events are reliably distributed to authorized subscribing systems with complete delivery and retry history.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Destination",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Authentication",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Payload version",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Retry count",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Retry interval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Timeout",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Signing/security",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      },
      {
       "kind": "selectField",
       "label": "Failure behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §For each subscriber configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Wallet Created",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §Support events such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Activated",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §Support events such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Blocked",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §Support events such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Unblocked",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §Support events such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Balance Changed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §Support events such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Top-Up Failed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §Support events such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Completed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §Support events such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Declined",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 119 §Support events such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet events webhooks configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet events webhooks untouched.",
   "emptyFirstRun": "No wallet events webhooks configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletRiskRules",
    "contract": "wallet",
    "purpose": "Events and notifications",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createWebhookSubscription",
    "contract": "public-api",
    "purpose": "Subscribe an integration to the chosen wallet events",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Wallet Created, Wallet Activated, Wallet Blocked, Wallet Unblocked, Balance Changed, Top-Up Failed, Payment Completed, Payment Declined …"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1176",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1176"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 119. 0 of 0 labels bound to a contract property; 29 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Wallet Created, Wallet Activated, Wallet Blocked, Wallet Unblocked, Balance Changed, Top-Up Failed, Payment Completed, Payment Declined …: `createWebhookSubscription`.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1177",
  "name": "API Security, Access & Integration Permissions",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "05",
   "page": 120
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/api-security-access-integration-permissions-bo-1177",
   "component": "apps/venue-management-web/src/routes/orders-money/ApiSecurityAccessIntegrationPermissions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "clientId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Ensure integrations receive only the wallet permissions and data required for their function.",
  "purposeNote": "Every API request is authenticated and authorized against explicit integration, tenant, venue and operation-level permissions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Integration identity",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Application/client",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant scope",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue scope",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "API scope",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed operations",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed wallet types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Environment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "textField",
       "label": "IP/network restrictions where applicable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Secret/key rotation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "MFA for administration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Certificate configuration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Access Models",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Read Only",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Finance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partner",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Internal Service",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "High-Risk Operations",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Balance Adjustment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Operations such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Block",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Operations such as"
      },
      {
       "kind": "secondaryButton",
       "label": "High-Value Refund",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 120 §Operations such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The api security access configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the api security access untouched.",
   "emptyFirstRun": "No api security access configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listAccessPolicies",
    "contract": "identity",
    "purpose": "API access and permissions",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createApiClient",
    "contract": "public-api",
    "purpose": "Grant an integration only the wallet scopes it needs",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Read Only, Finance, Partner, Internal Service, High-Risk Operations, Balance Adjustment, Wallet Block, High-Value Refund …"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1177",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1177"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 120. 0 of 0 labels bound to a contract property; 29 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Read Only, Finance, Partner, Internal Service, High-Risk Operations, Balance Adjustment, Wallet Block, High-Value Refund …: `createApiClient`.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1178",
  "name": "Synchronization, Retry & Resilience Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "06",
   "page": 121
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/synchronization-retry-resilience-configuration-bo-1178",
   "component": "apps/venue-management-web/src/routes/orders-money/SynchronizationRetryResilienceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how Wallet behaves when dependent services or external systems are temporarily unavailable.",
  "purposeNote": "Temporary integration failures do not cause duplicate financial transactions, lost wallet events or inconsistent wallet balances.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Retry attempts",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retry interval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Exponential backoff",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Timeout",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Idempotency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Duplicate prevention",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Queue behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dead-letter queue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event retention",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Replay permission",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dependency priority",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Example",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 121 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The synchronization retry resilience configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the synchronization retry resilience untouched.",
   "emptyFirstRun": "No synchronization retry resilience configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getWalletReconciliation",
    "contract": "wallet",
    "purpose": "Synchronisation state",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1178",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1178"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 121. 0 of 0 labels bound to a contract property; 12 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1179",
  "name": "Integration Monitoring & Exception Workbench",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "07",
   "page": 122
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/integration-monitoring-exception-workbench-bo-1179",
   "component": "apps/venue-management-web/src/routes/orders-money/IntegrationMonitoringExceptionWorkbench.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "clientId",
      "subscriptionId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Give technical and operational teams a dedicated workspace for failed integrations.",
  "purposeNote": "Every integration failure is traceable through a controlled exception workflow without modifying the original financial transaction.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Display"
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
       "label": "Every integration monitoring exception",
       "columns": [
        "Exception ID",
        "Integration",
        "Wallet",
        "Transaction",
        "Endpoint/event",
        "Error code",
        "Error message",
        "Attempt count",
        "First failure",
        "Last retry",
        "Priority",
        "Owner",
        "Status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected integration monitoring exception",
       "bindsTo": null,
       "columns": [
        "Exception ID",
        "Integration",
        "Wallet",
        "Transaction",
        "Endpoint/event",
        "Error code",
        "Error message",
        "Attempt count",
        "First failure",
        "Last retry",
        "Priority",
        "Owner",
        "Status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Exception Categories”, “Workflow”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Retry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Replay",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Correct mapping",
       "operation": "setWalletIntegrationMapping",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprocess",
       "operation": "resolveWalletDispute",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "operation": "resolveWalletDispute",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend integration",
       "operation": "setApiClientStatus",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Mark resolved",
       "operation": "resolveWalletDispute",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Actions"
      },
      {
       "kind": "primaryButton",
       "label": "Withdraw dispute",
       "operation": "withdrawWalletDispute",
       "provenance": "contract wallet.yaml POST /wallet-disputes/{disputeId}/withdraw (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendIntegration",
    "component": "confirmDialog",
    "trigger": "Suspend integration",
    "body": "**Suspend integration on a integration monitoring exception is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 122 §Actions"
   }
  ],
  "states": {
   "loading": "The integration monitoring exception list.",
   "error": "Could not load. Names which read failed and leaves the integration monitoring exception untouched.",
   "emptyFirstRun": "No integration monitoring exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration monitoring exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWalletDisputes",
    "contract": "wallet",
    "purpose": "Integration exceptions",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "replayEvents",
    "contract": "public-api",
    "purpose": "Retry or replay failed outbound wallet events",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Retry, Replay"
   },
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "The integrations whose exceptions are worked here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWebhookSubscriptions",
    "contract": "public-api",
    "purpose": "The webhook subscriptions whose events are replayed",
    "trigger": "onLoad"
   },
   {
    "operationId": "setWalletIntegrationMapping",
    "contract": "wallet",
    "purpose": "Correct mapping",
    "trigger": "onAction"
   },
   {
    "operationId": "resolveWalletDispute",
    "contract": "wallet",
    "purpose": "Resolve",
    "trigger": "onAction"
   },
   {
    "operationId": "withdrawWalletDispute",
    "contract": "wallet",
    "purpose": "Withdraw dispute",
    "trigger": "onAction"
   },
   {
    "operationId": "setApiClientStatus",
    "contract": "public-api",
    "purpose": "Suspend integration",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "Exception ID",
    "Integration",
    "Wallet",
    "Transaction",
    "Endpoint/event",
    "Error code"
   ],
   "params": [
    {
     "name": "clientId",
     "from": "navigation"
    },
    {
     "name": "disputeId",
     "from": "navigation"
    },
    {
     "name": "subscriptionId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1179",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1179"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 122. 0 of 13 labels bound to a contract property; 20 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Retry, Replay: `replayEvents`; still owed by a contract change: `resolveWalletDispute`, `setWalletIntegrationMapping`, `setApiClientStatus`.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1180",
  "name": "Wallet Configuration Governance & Version Control",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "08",
   "page": 123
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-configuration-governance-version-control-bo-1180",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletConfigurationGovernanceVersionControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide centralized governance for configuration changes across all ten Wallet boards. This screen becomes the master configuration governance layer for the entire Wallet module.",
  "purposeNote": "Every material Wallet configuration change is version-controlled and historical configurations remain available for audit and investigation.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 123 §Show"
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
       "label": "Every wallet governance version",
       "columns": [
        "Cash Priority: 3 → 5",
        "Bonus Priority: 2 → 1",
        "FEFO: Enabled → Enabled",
        "Gift Card Priority: 4 → 3"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 123 §Show"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Takes effect at every till and reader immediately.** Credit types, consumption order and funding rules change for balances that already exist, not only for new ones.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet governance version",
       "bindsTo": null,
       "columns": [
        "Cash Priority: 3 → 5",
        "Bonus Priority: 2 → 1",
        "FEFO: Enabled → Enabled",
        "Gift Card Priority: 4 → 3"
       ],
       "notes": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 123 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet governance version list.",
   "error": "Could not load. Names which read failed and leaves the wallet governance version untouched.",
   "emptyFirstRun": "No wallet governance version yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet governance version are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishWalletConfiguration",
    "contract": "wallet",
    "purpose": "Governance and version control",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes",
     "listCreditTypes"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Cash Priority: 3 → 5",
    "Bonus Priority: 2 → 1",
    "FEFO: Enabled → Enabled",
    "Gift Card Priority: 4 → 3"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1180",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1180"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 123. 0 of 4 labels bound to a contract property; 36 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1181",
  "name": "Approval, Publication & Change Management",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "09",
   "page": 124
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/approval-publication-change-management-bo-1181",
   "component": "apps/venue-management-web/src/routes/orders-money/ApprovalPublicationChangeManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control how Wallet configuration moves safely from draft into production.",
  "purposeNote": "No governed Wallet configuration enters production without satisfying its required validation, approval and publication workflow.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Immediate publication",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 124 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Scheduled publication",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 124 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant-specific rollout",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 124 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue-specific rollout",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 124 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 124 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Pilot rollout",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 124 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Emergency rollback",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 124 §Configure"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Takes effect at every till and reader immediately.** Credit types, consumption order and funding rules change for balances that already exist, not only for new ones.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval publication change configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval publication change untouched.",
   "emptyFirstRun": "No approval publication change configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "publishWalletConfiguration",
    "contract": "wallet",
    "purpose": "Approval and publication",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes",
     "listCreditTypes"
    ]
   },
   {
    "operationId": "createApprovalRequest",
    "contract": "approvals",
    "purpose": "Send for approval",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1181",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1181"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 124. 0 of 0 labels bound to a contract property; 17 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-1182",
  "name": "Wallet Platform Health, Audit & Administration Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "10",
   "number": "10",
   "page": 125
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-platform-health-audit-administration-center-bo-1182",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletPlatformHealthAuditAdministrationCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1173"
   ],
   "exitTo": [
    "BO-1173"
   ],
   "transitions": [
    {
     "to": "BO-1173",
     "trigger": "Back to Wallet Integration Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Master Health KPIs) and a per-row directory (§Display) — counts over a population, then the population",
  "purpose": "Provide the final master-administration screen for the entire TICVAI Wallet ecosystem. This should become the control tower for all ten Wallet boards.",
  "purposeNote": "Authorized administrators can assess end-to-end Wallet health, trace material actions across the platform and navigate directly to affected configuration, transactions, integrations or exceptions. Board 10 — End-to-End Architecture The final integration architecture should look like: Customer / Employee / Corporate Account ↓ TICVAI Wallet Engine Wallet Foundation → Funding → Credit & Consumption → Family / Corporate → Gift Cards & Benefits → Channels & Wearables → Transfers & Refunds → Fraud & Risk → Finance & Liability ↓ Wallet API & Event Layer ↙︎ Ticketing ↙︎ Membership ↙︎ CRM ↙︎ Pricing &",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Display"
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
       "label": "Wallet Service Availability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      },
      {
       "kind": "metricTile",
       "label": "API Success Rate",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Authorization Time",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Failed Transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Pending Events",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Reconciliation Exceptions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Fraud Alerts",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Ledger Integrity",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Configuration Errors",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Master Health KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every wallet platform health",
       "columns": [
        "Wallet Engine"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet platform health",
       "bindsTo": null,
       "columns": [
        "Wallet Engine"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Healthy”, “Search across”, “Every record should contain”, “Authorized super administrators can”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 125 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet platform health list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the wallet platform health untouched.",
   "emptyFirstRun": "No wallet platform health yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet platform health are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWalletLiability",
    "contract": "wallet",
    "purpose": "Platform health and audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1182",
   "workshopBoard": "wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1182"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 125. 0 of 1 labels bound to a contract property; 19 of 117 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
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
 "createApiClient": {
  "method": "POST",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Create a client with scopes and an environment",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "ApiClient",
  "responds": null
 },
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
 "createWebhookSubscription": {
  "method": "POST",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "Subscribe to business events",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "WebhookSubscription",
  "responds": "WebhookSubscription"
 },
 "getWalletLiability": {
  "method": "GET",
  "path": "/wallet-liability",
  "contract": "wallet",
  "summary": "What is outstanding, and what is breakage",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "asOf",
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
  "responds": "WalletLiabilityRow"
 },
 "getWalletReconciliation": {
  "method": "GET",
  "path": "/wallet-reconciliation",
  "contract": "wallet",
  "summary": "The wallet sub-ledger against the general ledger and the acquirer",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "WalletReconciliation"
 },
 "listAccessPolicies": {
  "method": "GET",
  "path": "/access-policies",
  "contract": "identity",
  "summary": "Attribute-based access policies",
  "permission": "PERMISSION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccessPolicy"
 },
 "listApiClients": {
  "method": "GET",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Registered clients for this developer",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApiClient"
 },
 "listWalletDisputes": {
  "method": "GET",
  "path": "/wallet-disputes",
  "contract": "wallet",
  "summary": "Contested transactions and operational exceptions",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WalletDispute"
 },
 "listWalletTypes": {
  "method": "GET",
  "path": "/wallet-types",
  "contract": "wallet",
  "summary": "The kinds of wallet that may exist — who owns one",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "WalletType"
 },
 "listWebhookSubscriptions": {
  "method": "GET",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "The tenant's webhook subscriptions, filterable by API client",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "clientId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WebhookSubscription"
 },
 "publishWalletConfiguration": {
  "method": "POST",
  "path": "/wallet-configuration/publish",
  "contract": "wallet",
  "summary": "Validate and publish the wallet configuration as a version",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WalletConfigurationVersion"
 },
 "replayEvents": {
  "method": "POST",
  "path": "/webhook-subscriptions/{subscriptionId}/replay",
  "contract": "public-api",
  "summary": "Re-deliver events from a point in time",
  "permission": "DEVELOPER_MANAGE",
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
 "resolveWalletDispute": {
  "method": "POST",
  "path": "/wallet-disputes/{disputeId}/resolve",
  "contract": "wallet",
  "summary": "Work a wallet dispute or integration exception",
  "permission": "WALLET_OPERATE",
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
  "requestBody": null,
  "responds": "WalletDispute"
 },
 "setApiClientStatus": {
  "method": "POST",
  "path": "/api-clients/{clientId}/status",
  "contract": "public-api",
  "summary": "Suspend or reactivate an integration, reversibly",
  "permission": "DEVELOPER_MANAGE",
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
  "responds": "ApiClient"
 },
 "setWalletChannelRules": {
  "method": "PUT",
  "path": "/wallet-channel-rules",
  "contract": "wallet",
  "summary": "Where a wallet may be used, on what, and when it may not",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "WalletChannelRules",
  "responds": "WalletChannelRules"
 },
 "setWalletIntegrationMapping": {
  "method": "PUT",
  "path": "/wallet-integration-mappings",
  "contract": "wallet",
  "summary": "How one integration's fields, currencies, statuses and credit types map onto the wallet",
  "permission": "WALLET_CONFIGURE",
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
  "requestBody": "WalletIntegrationMapping",
  "responds": "WalletIntegrationMapping"
 },
 "setWalletRiskRules": {
  "method": "PUT",
  "path": "/wallet-risk-rules",
  "contract": "wallet",
  "summary": "Velocity, behaviour and what happens when a rule trips",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "WalletRiskRules",
  "responds": "WalletRiskRules"
 },
 "testWebhookSubscription": {
  "method": "POST",
  "path": "/webhook-subscriptions/{subscriptionId}/test",
  "contract": "public-api",
  "summary": "Send a signed test event to the endpoint, now",
  "permission": "DEVELOPER_MANAGE",
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
  "responds": "WebhookDelivery"
 },
 "withdrawWalletDispute": {
  "method": "POST",
  "path": "/wallet-disputes/{disputeId}/withdraw",
  "contract": "wallet",
  "summary": "Withdraw a wallet dispute that is still open or under review",
  "permission": "WALLET_OPERATE",
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
  "requestBody": null,
  "responds": "WalletDispute"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessCondition": {
  "type": "object",
  "description": "**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n",
  "required": [
   "attribute",
   "operator"
  ],
  "properties": {
   "attribute": {
    "type": "string",
    "enum": [
     "user.attribute",
     "employee.attribute",
     "employee.onShift",
     "membership.tier",
     "membership.status",
     "accreditation.type",
     "accreditation.status",
     "customer.segment",
     "resource.classification",
     "venue.attribute",
     "venue.id",
     "attraction.attribute",
     "device.kind",
     "device.id",
     "device.trusted",
     "time.ofDay",
     "time.dayOfWeek",
     "time.season",
     "time.withinOperatingHours",
     "event.id",
     "event.status",
     "capacity.utilisationPercent",
     "occupancy.level",
     "risk.score",
     "ticket.status",
     "location.scopePath"
    ]
   },
   "key": {
    "type": "string",
    "nullable": true,
    "description": "For the `*.attribute` forms — which attribute, by code."
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "in",
     "notIn",
     "greaterThan",
     "lessThan",
     "between",
     "contains",
     "startsWith",
     "exists"
    ]
   },
   "value": {
    "nullable": true,
    "description": "The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"
   },
   "values": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "AccessPolicy": {
  "type": "object",
  "x-ticvai-persistence": "identity.access_policy",
  "description": "3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n",
  "required": [
   "code",
   "name",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server on `createAccessPolicy`; the path names the policy on update."
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "isTemplate": {
    "type": "boolean",
    "default": false
   },
   "permissions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"
   },
   "conditions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AccessCondition"
    }
   },
   "combining": {
    "type": "string",
    "enum": [
     "allMustMatch",
     "anyMayMatch"
    ],
    "default": "allMustMatch"
   },
   "effect": {
    "type": "string",
    "enum": [
     "permit",
     "deny"
    ],
    "description": "**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string",
    "description": "3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"
   },
   "appliesToRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "description": "**Moved only by `setAccessPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "suspended",
     "retired"
    ]
   },
   "version": {
    "type": "integer",
    "default": 1,
    "readOnly": true,
    "description": "Set by the server; every `updateAccessPolicy` writes a new version."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "delegatedAdminRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"
   }
  }
 },
 "ApiClient": {
  "type": "object",
  "x-ticvai-persistence": "control.api_client",
  "description": "CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n",
  "required": [
   "id",
   "developerId",
   "name",
   "environment",
   "scopes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "clientId": {
    "type": "string",
    "readOnly": true
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "production"
    ],
    "description": "**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"
   },
   "scopes": {
    "type": "array",
    "description": "**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing.\n",
    "items": {
     "type": "string"
    }
   },
   "allowedTenantIds": {
    "type": "array",
    "description": "13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "description": "13.1.38. Optional, and the strongest control available where an integrator has fixed egress.",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked"
    ],
    "readOnly": true
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
   }
  }
 },
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "WalletChannelRules": {
  "type": "object",
  "x-ticvai-persistence": "wallet.channel_rules",
  "description": "Board 6. **The offline rule is stated once, not per device.**",
  "properties": {
   "allowedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "allowedCredentialKinds": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "card",
      "wristband",
      "nfc",
      "rfid",
      "qr",
      "mobileApp",
      "digitalKey"
     ]
    }
   },
   "requiresPin": {
    "type": "boolean",
    "default": false
   },
   "pinAboveAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "offlineAllowed": {
    "type": "boolean",
    "default": false
   },
   "offlineFloorLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "offlineMaximumAgeMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "**How stale a cached balance may be before the device refuses.** Without a ceiling an offline terminal spends a balance that ran out yesterday.\n"
   },
   "acceptancePointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletConfigurationVersion": {
  "type": "object",
  "x-ticvai-persistence": "wallet.configuration_version",
  "description": "Boards 1.10 and 10.8. **Ten boards of configuration that interact.**",
  "properties": {
   "version": {
    "type": "integer"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
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
      "code": {
       "type": "string"
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletDispute": {
  "type": "object",
  "x-ticvai-persistence": "wallet.dispute",
  "description": "Board 7.9. **Internal, and the venue decides it** — unlike a card chargeback.",
  "required": [
   "walletId",
   "description"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "walletId": {
    "type": "string",
    "format": "uuid"
   },
   "transactionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "description": {
    "type": "string"
   },
   "raisedBy": {
    "type": "string",
    "format": "uuid"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "escalated",
     "upheld",
     "rejected",
     "withdrawn"
    ],
    "description": "`escalated` added with `resolveWalletDispute` (VM close-out, 29 September). `upheld`, `rejected` and `withdrawn` are closed."
   },
   "resolution": {
    "type": "string",
    "nullable": true
   },
   "escalatedToRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "reprocessedTransactionIds": {
    "type": "array",
    "readOnly": true,
    "description": "Transactions created by a `reprocess` action.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "resolvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "adjustmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletIntegrationMapping": {
  "type": "object",
  "x-ticvai-persistence": "wallet.integration_mapping",
  "description": "Board 10, pp.118 and 122. **One per integration**, keyed by the `public-api` client. An unmapped inbound value is parked as an exception, never guessed.",
  "required": [
   "apiClientId"
  ],
  "properties": {
   "apiClientId": {
    "type": "string",
    "format": "uuid",
    "description": "The `public-api` ApiClient the integration authenticates as."
   },
   "fieldMappings": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "externalField",
      "walletField"
     ],
     "properties": {
      "externalField": {
       "type": "string"
      },
      "walletField": {
       "type": "string"
      },
      "transform": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "currencyMappings": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "externalCode",
      "currency"
     ],
     "properties": {
      "externalCode": {
       "type": "string"
      },
      "currency": {
       "type": "string",
       "pattern": "^[A-Z]{3}$"
      }
     }
    }
   },
   "statusMappings": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "externalStatus",
      "walletStatus"
     ],
     "properties": {
      "externalStatus": {
       "type": "string"
      },
      "walletStatus": {
       "type": "string"
      }
     }
    }
   },
   "creditTypeMappings": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "externalCode",
      "creditTypeId"
     ],
     "properties": {
      "externalCode": {
       "type": "string"
      },
      "creditTypeId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "dateTimeFormat": {
    "type": "string",
    "default": "ISO-8601",
    "description": "The format the integration sends, e.g. ISO-8601 or a pattern such as dd/MM/yyyy HH:mm."
   },
   "timeZone": {
    "type": "string",
    "nullable": true,
    "description": "IANA zone the integration's local times are in. Null means UTC offsets are sent."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletLiabilityRow": {
  "type": "object",
  "description": "Boards 9.5 and 9.6. **The number the finance director asks for.**",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "outstanding": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "expiringThisPeriod": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "breakageRecognised": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "walletCount": {
    "type": "integer"
   },
   "oldestLotAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   }
  }
 },
 "WalletReconciliation": {
  "type": "object",
  "description": "Board 9.4. **Three sources, and the exception names which pair disagrees.**",
  "properties": {
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "subLedgerTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "generalLedgerTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "acquirerTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exceptions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "pair": {
       "type": "string",
       "enum": [
        "subLedgerVsGeneralLedger",
        "subLedgerVsAcquirer",
        "generalLedgerVsAcquirer"
       ]
      },
      "difference": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "transactionIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "likelyCause": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "WalletRiskRules": {
  "type": "object",
  "x-ticvai-persistence": "wallet.risk_rules",
  "description": "Boards 8.2 to 8.7. **A risk rule with no action is a report.**",
  "properties": {
   "rules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "signal": {
       "type": "string",
       "enum": [
        "velocityCount",
        "velocityAmount",
        "newCredential",
        "geographyJump",
        "deviceChange",
        "dormantThenLarge",
        "repeatedFailure",
        "refundPattern"
       ]
      },
      "threshold": {
       "type": "number"
      },
      "windowMinutes": {
       "type": "integer"
      },
      "action": {
       "type": "string",
       "enum": [
        "scoreOnly",
        "challenge",
        "holdTransaction",
        "freezeWallet",
        "raiseCase"
       ]
      },
      "minimumConfidence": {
       "type": "number",
       "nullable": true,
       "description": "**Required before an automated freeze.** A rule that freezes on a false positive will eventually freeze a family in a queue.\n"
      },
      "alertOnAction": {
       "type": "boolean",
       "default": true
      },
      "status": {
       "type": "string",
       "readOnly": true,
       "enum": [
        "active",
        "suspended",
        "emergencyDisabled"
       ],
       "default": "active",
       "description": "Set by `setWalletRiskRuleStatus`, not by publishing the rule set. A rule not `active` is evaluated for nothing (VM close-out, 29 September)."
      },
      "statusReason": {
       "type": "string",
       "nullable": true,
       "readOnly": true
      },
      "statusUntil": {
       "type": "string",
       "format": "date-time",
       "nullable": true,
       "readOnly": true,
       "description": "When a `suspended` rule returns to `active` by itself."
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletType": {
  "type": "object",
  "x-ticvai-persistence": "wallet.wallet_type",
  "description": "Board 1.2. **Who owns a wallet** — the first of the two vocabularies.",
  "required": [
   "code",
   "name"
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
   "ownerKind": {
    "type": "string",
    "enum": [
     "guest",
     "registeredCustomer",
     "family",
     "parent",
     "child",
     "corporate",
     "school",
     "employee"
    ]
   },
   "storedValueCapability": {
    "type": "boolean",
    "default": true,
    "description": "Board 1.2. Whether this wallet holds a balance at all. A pure entitlement wallet — passes and vouchers, no money — does not.\n"
   },
   "topUpCapability": {
    "type": "boolean",
    "default": false
   },
   "transferCapability": {
    "type": "boolean",
    "default": false
   },
   "refundCapability": {
    "type": "boolean",
    "default": false
   },
   "giftCardSupport": {
    "type": "boolean",
    "default": false
   },
   "voucherSupport": {
    "type": "boolean",
    "default": false
   },
   "membershipCreditSupport": {
    "type": "boolean",
    "default": false
   },
   "wearableSupport": {
    "type": "boolean",
    "default": false
   },
   "usageChannels": {
    "type": "array",
    "description": "**Where this wallet may be used, declared on the type itself.** Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and this is what lets one `topUpWallet` serve every caller: the operation is shared and the type says which channel may reach it. `WalletChannelRules` still governs the per-credential detail — PIN thresholds, offline floor limits — and this governs whether the channel is open at all.\n",
    "items": {
     "type": "string",
     "enum": [
      "online",
      "pos",
      "mobileApp",
      "api",
      "kiosk",
      "reader"
     ]
    }
   },
   "presetName": {
    "type": "string",
    "description": "**The client's own name for this composition** — \"Resort Wallet\", \"Cashless Venue Wallet\", \"Closed-Loop Wallet\". Board 1.2 lists thirteen such names as examples, not as kinds: they are combinations of `ownerKind`, `allowedCreditTypeIds` and `scopePath`. Naming the preset keeps the client's vocabulary without hard-coding it into an enum.\n"
   },
   "holderMayDifferFromOwner": {
    "type": "boolean",
    "default": false,
    "description": "**A child wallet's owner is the parent.** Without this the model has to pretend a seven-year-old holds an account.\n"
   },
   "requiresIdentification": {
    "type": "boolean",
    "default": false
   },
   "maximumBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "allowedCreditTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "allowNegativeBalance": {
    "type": "boolean",
    "default": false
   },
   "sharedStructureAllowed": {
    "type": "boolean",
    "default": false
   },
   "lifecycleStates": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "numberingPattern": {
    "type": "string",
    "nullable": true
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
 "WebhookDelivery": {
  "type": "object",
  "x-ticvai-persistence": "control.webhook_delivery",
  "description": "13.1.30. **The log a developer needs most**, and without it every question becomes a support ticket.\n",
  "required": [
   "id",
   "subscriptionId",
   "eventType",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subscriptionId": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "eventType": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "delivered",
     "failed",
     "retrying",
     "abandoned"
    ]
   },
   "attemptCount": {
    "type": "integer"
   },
   "responseCode": {
    "type": "integer",
    "nullable": true
   },
   "responseBodyExcerpt": {
    "type": "string",
    "nullable": true,
    "description": "**Truncated, and it is what makes the log useful** — a 500 with the receiver's own error message in it answers the question without a conversation.\n"
   },
   "isReplay": {
    "type": "boolean",
    "default": false
   },
   "isTest": {
    "type": "boolean",
    "default": false,
    "description": "Sent by `testWebhookSubscription` (VM close-out, 29 September). Marked in the payload so a receiver never books it, and never counted towards `consecutiveFailures`.\n"
   },
   "deliveredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WebhookSubscription": {
  "type": "object",
  "x-ticvai-persistence": "control.webhook_subscription",
  "description": "13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n",
  "required": [
   "id",
   "clientId",
   "endpointUrl",
   "eventTypes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "clientId": {
    "type": "string",
    "format": "uuid"
   },
   "endpointUrl": {
    "type": "string"
   },
   "eventTypes": {
    "type": "array",
    "description": "**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to.\n",
    "items": {
     "type": "string"
    }
   },
   "filters": {
    "type": "object",
    "nullable": true,
    "description": "13.3.22. Tenant, venue, or a business condition on the payload.",
    "additionalProperties": true
   },
   "signingSecret": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingVerification",
     "active",
     "paused",
     "failing",
     "disabled"
    ],
    "readOnly": true
   },
   "consecutiveFailures": {
    "type": "integer",
    "readOnly": true
   },
   "disabledReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"
   }
  }
 }
}
```
