# WS58 — Sales Channel Management board 2

**10 screens · 17 operations · 17 schemas · 4 permissions**

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
  `AI_APPROVE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-268` | Channel Operations Command Center | commandCentre | 2 | 0 | — |
| `ADM-269` | Channel Connection & Integration Manager | configEditor | 3 | 2 | — |
| `ADM-270` | Product, Price & Availability Synchronization | listDetail | 2 | 1 | — |
| `ADM-271` | Real-Time Channel Availability & Inventory Monitor | listDetail | 2 | 0 | — |
| `ADM-272` | Channel Allocation & Rebalancing Operations | listDetail | 1 | 0 | — |
| `ADM-273` | Channel Exceptions, Incidents & Recovery | configEditor | 3 | 1 | — |
| `ADM-274` | Channel Performance & Commercial Analytics | commandCentre | 1 | 0 | — |
| `ADM-275` | Channel Audit, Logs & Transaction Traceability | listDetail | 1 | 0 | — |
| `ADM-276` | Channel Governance, SLA & Partner Control | configEditor | 1 | 0 | — |
| `ADM-277` | AI Channel Optimization & Intelligence Center | listDetail | 3 | 1 | — |

## Thin screens in this batch

**ADM-271, ADM-272 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-268",
  "name": "Channel Operations Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.1",
   "page": 20
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-operations-command-center-adm-268",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-269",
    "ADM-270",
    "ADM-271",
    "ADM-272",
    "ADM-273",
    "ADM-274",
    "ADM-275",
    "ADM-276",
    "ADM-277"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-268 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-269",
     "trigger": "Works in Channel Connection & Integration Manager",
     "provenance": "flow F167 step 1→2",
     "operation": "listChannel"
    },
    {
     "to": "ADM-270",
     "trigger": "Works in Product, Price & Availability Synchronization",
     "provenance": "flow F167 step 3→4",
     "operation": "listChannel"
    },
    {
     "to": "ADM-271",
     "trigger": "Works in Real-Time Channel Availability & Inventory Monitor",
     "provenance": "flow F167 step 5→6",
     "operation": "listChannel"
    },
    {
     "to": "ADM-272",
     "trigger": "Works in Channel Allocation & Rebalancing Operations",
     "provenance": "flow F167 step 7→8",
     "operation": "listChannel"
    },
    {
     "to": "ADM-273",
     "trigger": "Works in Channel Exceptions, Incidents & Recovery",
     "provenance": "flow F167 step 9→10",
     "operation": "listChannel"
    },
    {
     "to": "ADM-274",
     "trigger": "Works in Channel Performance & Commercial Analytics",
     "provenance": "flow F167 step 11→12",
     "operation": "listChannel"
    },
    {
     "to": "ADM-275",
     "trigger": "Works in Channel Audit, Logs & Transaction Traceability",
     "provenance": "flow F167 step 13→14",
     "operation": "listChannel"
    },
    {
     "to": "ADM-276",
     "trigger": "Works in Channel Governance, SLA & Partner Control",
     "provenance": "flow F167 step 15→16",
     "operation": "listChannel"
    },
    {
     "to": "ADM-277",
     "trigger": "Works in AI Channel Optimization & Intelligence Center",
     "provenance": "flow F167 step 17→18",
     "operation": "listChannel"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations teams can determine the health, commercial activity and current issues of every active sales channel from one central workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each channel should display) — counts over a population, then the population",
  "purpose": "Provide a real-time operational view of all active TICVAI sales channels.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.activeChannels"
      },
      {
       "kind": "metricTile",
       "label": "Connected Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.connectedChannels"
      },
      {
       "kind": "metricTile",
       "label": "Degraded Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.degradedChannels"
      },
      {
       "kind": "metricTile",
       "label": "Offline Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.offlineChannels"
      },
      {
       "kind": "metricTile",
       "label": "Transactions Today",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.transactionsToday"
      },
      {
       "kind": "metricTile",
       "label": "Gross Sales",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.grossSales"
      },
      {
       "kind": "metricTile",
       "label": "Products Available",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.productsAvailable"
      },
      {
       "kind": "metricTile",
       "label": "Synchronization Errors",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.synchronizationErrors"
      },
      {
       "kind": "metricTile",
       "label": "Capacity Alerts",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.capacityAlerts"
      },
      {
       "kind": "metricTile",
       "label": "Pricing Errors",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.pricingErrors"
      },
      {
       "kind": "metricTile",
       "label": "Failed Transactions",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterSummary.failedTransactions"
      },
      {
       "kind": "metricTile",
       "label": "Open Operational Incidents",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every channel operations",
       "columns": [
        "ChannelOperationsCommandCenterView.channel",
        "ChannelOperationsCommandCenterView.type",
        "ChannelOperationsCommandCenterView.venueScope",
        "ChannelOperationsCommandCenterView.connectionStatus",
        "ChannelOperationsCommandCenterView.lastSync",
        "ChannelOperationsCommandCenterView.products",
        "ChannelOperationsCommandCenterView.transactions",
        "ChannelOperationsCommandCenterView.salesValue",
        "ChannelOperationsCommandCenterView.inventoryStatus",
        "ChannelOperationsCommandCenterView.pricingStatus",
        "ChannelOperationsCommandCenterView.errorCount",
        "ChannelOperationsCommandCenterView.healthScore"
       ],
       "bindsTo": "ChannelOperationsCommandCenterView",
       "operation": "listChannel",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Each channel should display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel operations",
       "bindsTo": "ChannelOperationsCommandCenterView",
       "columns": [
        "ChannelOperationsCommandCenterView.channel",
        "ChannelOperationsCommandCenterView.type",
        "ChannelOperationsCommandCenterView.venueScope",
        "ChannelOperationsCommandCenterView.connectionStatus",
        "ChannelOperationsCommandCenterView.lastSync",
        "ChannelOperationsCommandCenterView.products",
        "ChannelOperationsCommandCenterView.transactions",
        "ChannelOperationsCommandCenterView.salesValue",
        "ChannelOperationsCommandCenterView.inventoryStatus",
        "ChannelOperationsCommandCenterView.pricingStatus",
        "ChannelOperationsCommandCenterView.errorCount",
        "ChannelOperationsCommandCenterView.healthScore"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Use”, “Show important events such as”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Each channel should display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Open Channel, Force Sync, Pause Channel, Resume Channel, Open Incident, View Logs, View Transactions, View Performance. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the channel operations untouched.",
   "emptyFirstRun": "No channel operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannel2",
    "contract": "catalogue",
    "purpose": "AI Channel Optimization & Intelligence Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listChannel",
    "contract": "catalogue",
    "purpose": "Channel Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-268",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-268"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 20. 23 of 23 labels bound to a contract property; 32 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-269",
  "name": "Channel Connection & Integration Manager",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.2",
   "page": 22
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-connection-integration-manager-adm-269",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelConnectionIntegrationManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-268",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F167 step 2→3",
     "operation": "listChannelConnectionIntegration"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized technical administrators can establish, test and monitor channel connections without modifying core TICVAI application code for supported connector types.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Configure and manage the technical connection between TICVAI and external or internal sales channels.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Connector Name",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Partner",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Environment",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Endpoint",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "API Version",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Authentication Type",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Credentials reference",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Certificate",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Timeout",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Retry Policy",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Rate Limit",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "IP Restrictions",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Connection Status",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Configure/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "TICVAI Native",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "REST API",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Webhook",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Reseller API",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partner API",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "File/SFTP where required",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel connection configuration",
       "operation": "setChannelConnectionConfiguration",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**How TICVAI reaches one channel, per environment** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /channel-connections"
      },
      {
       "kind": "secondaryButton",
       "label": "Test channel connection",
       "operation": "testChannelConnection",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**Runs the connection tests and records the result** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /channel-connections/{connectionId}/test"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel connection integration configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel connection integration untouched.",
   "emptyFirstRun": "No channel connection integration configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelConnectionIntegration",
    "contract": "catalogue",
    "purpose": "Channel Connection & Integration Manager",
    "trigger": "onLoad"
   },
   {
    "operationId": "setChannelConnectionConfiguration",
    "contract": "catalogue",
    "purpose": "Create or update a channel connection",
    "trigger": "onAction",
    "invalidates": [
     "listChannelConnectionIntegration"
    ]
   },
   {
    "operationId": "testChannelConnection",
    "contract": "catalogue",
    "purpose": "Test a channel connection now",
    "trigger": "onAction",
    "invalidates": [
     "listChannelConnectionIntegration"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-269",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-269"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 20 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetChannelConnectionConfiguration",
    "component": "modal",
    "trigger": "Save channel connection configuration",
    "body": "**Collects what `setChannelConnectionConfiguration` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `connectorName`, `environment`, `connectionType`. Optional: `partner`, `direction`, `endpoint`, `apiVersion`, `authenticationType`, `credentialsReference`, `certificateReference`, `certificateExpiresAt`, `timeoutMs`, `rateLimitPerMinute`, `ipRestrictions`, `retryPolicy` and 3 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ChannelConnection",
    "confirm": {
     "label": "Save channel connection configuration",
     "operation": "setChannelConnectionConfiguration"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "salesChannelId",
      "connectorName",
      "environment",
      "connectionType",
      "partner",
      "direction",
      "endpoint",
      "apiVersion",
      "authenticationType",
      "credentialsReference",
      "certificateReference",
      "certificateExpiresAt",
      "timeoutMs",
      "rateLimitPerMinute",
      "ipRestrictions",
      "retryPolicy"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /channel-connections"
   },
   {
    "id": "formTestChannelConnection",
    "component": "modal",
    "trigger": "Test channel connection",
    "body": "**Collects what `testChannelConnection` sends before it is called.** Nothing in the body is required. Optional: `tests`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Test channel connection",
     "operation": "testChannelConnection"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tests"
     ]
    },
    "provenance": "contract catalogue.yaml POST /channel-connections/{connectionId}/test"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "connectionId",
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
  "id": "ADM-270",
  "name": "Product, Price & Availability Synchronization",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.3",
   "page": 23
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/product-price-availability-synchronization-adm-270",
   "component": "apps/ticvai-web/src/routes/commercial/ProductPriceAvailabilitySynchronization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-268",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F167 step 4→5",
     "operation": "listProductPriceAvailability"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "supported sales channels while clearly identifying failed or inconsistent records.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control how TICVAI distributes commercial information to connected channels and receives supported updates.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen; 1 are served since the writers pass (29 September): Channel → TICVAI by `setChannelSyncSetting`.** Still unserved: Sync Now, Retry Failed, Compare, Reprocess, Pause Sync, Resume, Export Error. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Sales_Channel_Management_Reference.pdf, page 23 §Support as appropriate"
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
       "label": "Every product price availability",
       "columns": [
        "ProductPriceAvailabilitySynchronizationView.lastSuccessfulSync",
        "ProductPriceAvailabilitySynchronizationView.nextSync",
        "ProductPriceAvailabilitySynchronizationView.recordsProcessed",
        "ProductPriceAvailabilitySynchronizationView.successful",
        "ProductPriceAvailabilitySynchronizationView.failed",
        "ProductPriceAvailabilitySynchronizationView.pending",
        "ProductPriceAvailabilitySynchronizationView.warning",
        "ProductPriceAvailabilitySynchronizationView.duration"
       ],
       "bindsTo": "ProductPriceAvailabilitySynchronizationView",
       "operation": "listProductPriceAvailability",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product price availability",
       "bindsTo": "ProductPriceAvailabilitySynchronizationView",
       "columns": [
        "ProductPriceAvailabilitySynchronizationView.lastSuccessfulSync",
        "ProductPriceAvailabilitySynchronizationView.nextSync",
        "ProductPriceAvailabilitySynchronizationView.recordsProcessed",
        "ProductPriceAvailabilitySynchronizationView.successful",
        "ProductPriceAvailabilitySynchronizationView.failed",
        "ProductPriceAvailabilitySynchronizationView.pending",
        "ProductPriceAvailabilitySynchronizationView.warning",
        "ProductPriceAvailabilitySynchronizationView.duration"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Manage”, “Bidirectional”, “Mismatch”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Channel → TICVAI",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Support as appropriate"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync Now",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry Failed",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Compare",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprocess",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause Sync",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Export Error",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 23 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel sync setting",
       "operation": "setChannelSyncSetting",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**The person's half of `catalogue.channel_sync`** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /channel-syncs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product price availability list.",
   "error": "Could not load. Names which read failed and leaves the product price availability untouched.",
   "emptyFirstRun": "No product price availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product price availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductPriceAvailability",
    "contract": "catalogue",
    "purpose": "Product, Price & Availability Synchronization",
    "trigger": "onLoad"
   },
   {
    "operationId": "setChannelSyncSetting",
    "contract": "catalogue",
    "purpose": "Set how one kind of data synchronises with a channel",
    "trigger": "onAction",
    "invalidates": [
     "listProductPriceAvailability"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ProductPriceAvailabilitySynchronizationView.lastSuccessfulSync",
    "ProductPriceAvailabilitySynchronizationView.nextSync",
    "ProductPriceAvailabilitySynchronizationView.recordsProcessed",
    "ProductPriceAvailabilitySynchronizationView.successful",
    "ProductPriceAvailabilitySynchronizationView.failed",
    "ProductPriceAvailabilitySynchronizationView.pending"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-270",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-270"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 23. 8 of 8 labels bound to a contract property; 21 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetChannelSyncSetting",
    "component": "modal",
    "trigger": "Save channel sync setting",
    "body": "**Collects what `setChannelSyncSetting` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `domain`. Optional: `channelConnectionId`, `direction`, `frequency`, `isPaused`, `lastSuccessfulSyncAt`, `nextSyncAt`, `recordsProcessed`, `successful`, `failed`, `pending`, `warnings`, `durationMs` and 1 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ChannelSync",
    "confirm": {
     "label": "Save channel sync setting",
     "operation": "setChannelSyncSetting"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "salesChannelId",
      "domain",
      "channelConnectionId",
      "direction",
      "frequency",
      "isPaused",
      "lastSuccessfulSyncAt",
      "nextSyncAt",
      "recordsProcessed",
      "successful",
      "failed",
      "pending",
      "warnings",
      "durationMs",
      "mismatchCount"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /channel-syncs"
   }
  ],
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
  "id": "ADM-271",
  "name": "Real-Time Channel Availability & Inventory Monitor",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.4",
   "page": 25
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/real-time-channel-availability-inventory-monitor-adm-271",
   "component": "apps/ticvai-web/src/routes/commercial/RealTimeChannelAvailabilityInventoryMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-268",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F167 step 6→7",
     "operation": "listRealTimeChannel"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can understand current sellable availability across all channels without checking each channel independently.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide operations with a live view of what each channel can currently sell.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every real-time channel availability",
       "columns": [
        "RealTimeChannelAvailabilityInventoryMonitorView.allocated",
        "RealTimeChannelAvailabilityInventoryMonitorView.sold",
        "RealTimeChannelAvailabilityInventoryMonitorView.held",
        "RealTimeChannelAvailabilityInventoryMonitorView.remaining",
        "RealTimeChannelAvailabilityInventoryMonitorView.utilization",
        "RealTimeChannelAvailabilityInventoryMonitorView.salesVelocity",
        "RealTimeChannelAvailabilityInventoryMonitorView.forecastedSellOut"
       ],
       "bindsTo": "RealTimeChannelAvailabilityInventoryMonitorView",
       "operation": "listRealTimeChannel",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 25 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected real-time channel availability",
       "bindsTo": "RealTimeChannelAvailabilityInventoryMonitorView",
       "columns": [
        "RealTimeChannelAvailabilityInventoryMonitorView.allocated",
        "RealTimeChannelAvailabilityInventoryMonitorView.sold",
        "RealTimeChannelAvailabilityInventoryMonitorView.held",
        "RealTimeChannelAvailabilityInventoryMonitorView.remaining",
        "RealTimeChannelAvailabilityInventoryMonitorView.utilization",
        "RealTimeChannelAvailabilityInventoryMonitorView.salesVelocity",
        "RealTimeChannelAvailabilityInventoryMonitorView.forecastedSellOut"
       ],
       "notes": "The pack groups this record's detail under its own headings: “B2C POS Kiosk”, “Adult 420 180”, “Child 610 160 75”, “For every product/channel combination”, “Seat Map”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 25 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The real-time channel availability list.",
   "error": "Could not load. Names which read failed and leaves the real-time channel availability untouched.",
   "emptyFirstRun": "No real-time channel availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the real-time channel availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRealTimeChannel",
    "contract": "catalogue",
    "purpose": "Real-Time Channel Availability & Inventory Monitor",
    "trigger": "onLoad"
   },
   {
    "operationId": "listRealTimeAvailability",
    "contract": "promotions",
    "purpose": "Real-Time Availability & Checkout Validation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RealTimeChannelAvailabilityInventoryMonitorView.allocated",
    "RealTimeChannelAvailabilityInventoryMonitorView.sold",
    "RealTimeChannelAvailabilityInventoryMonitorView.held",
    "RealTimeChannelAvailabilityInventoryMonitorView.remaining",
    "RealTimeChannelAvailabilityInventoryMonitorView.utilization",
    "RealTimeChannelAvailabilityInventoryMonitorView.salesVelocity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-271",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-271"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 25. 7 of 7 labels bound to a contract property; 7 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-272",
  "name": "Channel Allocation & Rebalancing Operations",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.5",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-allocation-rebalancing-operations-adm-272",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelAllocationRebalancingOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-268",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F167 step 8→9",
     "operation": "listChannelAllocationRebalancing"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can dynamically rebalance unsold channel capacity without affecting confirmed orders or exceeding underlying capacity.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow authorized users to operationally adjust inventory allocations as demand changes. Board 1 defines the allocation rules. Board 2 manages those allocations during live operations.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every channel allocation rebalancing",
       "columns": [
        "ChannelAllocationRebalancingOperationsView.channel",
        "ChannelAllocationRebalancingOperationsView.initialAllocation",
        "ChannelAllocationRebalancingOperationsView.sold",
        "ChannelAllocationRebalancingOperationsView.held",
        "ChannelAllocationRebalancingOperationsView.remaining",
        "ChannelAllocationRebalancingOperationsView.utilization",
        "ChannelAllocationRebalancingOperationsView.salesVelocity",
        "ChannelAllocationRebalancingOperationsView.forecast",
        "ChannelAllocationRebalancingOperationsView.recommendedAllocation"
       ],
       "bindsTo": "ChannelAllocationRebalancingOperationsView",
       "operation": "listChannelAllocationRebalancing",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 26 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel allocation rebalancing",
       "bindsTo": "ChannelAllocationRebalancingOperationsView",
       "columns": [
        "ChannelAllocationRebalancingOperationsView.channel",
        "ChannelAllocationRebalancingOperationsView.initialAllocation",
        "ChannelAllocationRebalancingOperationsView.sold",
        "ChannelAllocationRebalancingOperationsView.held",
        "ChannelAllocationRebalancingOperationsView.remaining",
        "ChannelAllocationRebalancingOperationsView.utilization",
        "ChannelAllocationRebalancingOperationsView.salesVelocity",
        "ChannelAllocationRebalancingOperationsView.forecast",
        "ChannelAllocationRebalancingOperationsView.recommendedAllocation"
       ],
       "notes": "The pack groups this record's detail under its own headings: “OTA”, “B2C”, “Reallocation must respect”, “Approval”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 26 §Show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Increase allocation, Reduce allocation, Return inventory, Transfer allocation, Release hold, Move to shared pool, Freeze allocation. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 26 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel allocation rebalancing list.",
   "error": "Could not load. Names which read failed and leaves the channel allocation rebalancing untouched.",
   "emptyFirstRun": "No channel allocation rebalancing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel allocation rebalancing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelAllocationRebalancing",
    "contract": "catalogue",
    "purpose": "Channel Allocation & Rebalancing Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ChannelAllocationRebalancingOperationsView.channel",
    "ChannelAllocationRebalancingOperationsView.initialAllocation",
    "ChannelAllocationRebalancingOperationsView.sold",
    "ChannelAllocationRebalancingOperationsView.held",
    "ChannelAllocationRebalancingOperationsView.remaining",
    "ChannelAllocationRebalancingOperationsView.utilization"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-272",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-272"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 26. 9 of 9 labels bound to a contract property; 16 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-273",
  "name": "Channel Exceptions, Incidents & Recovery",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.6",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-exceptions-incidents-recovery-adm-273",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelExceptionsIncidentsRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-268",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F167 step 10→11",
     "operation": "listChannelExceptionIncident"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Channel incidents can be identified, assigned, investigated and recovered from a central operational workflow with complete traceability.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide one operational workspace for resolving channel problems.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Connection Failure, Product Sync Failure, Pricing Mismatch, Inventory Mismatch, Order Failure, Payment Error, Duplicate Transaction, Partner Error. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
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
       "label": "Incident ID",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Partner",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Severity",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Error Type",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Affected Product/Event",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Transactions Affected",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Business Impact",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "First Detected",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "SLA",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Current Status",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Connection Failure",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Product Sync Failure",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Pricing Mismatch",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Inventory Mismatch",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Order Failure",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Error",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate Transaction",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partner Error",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel incident",
       "operation": "updateChannelIncident",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**The person's moves on a channel incident** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PATCH /channel-incidents/{incidentId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry channel incident",
       "operation": "retryChannelIncident",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**Retry, as a call** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /channel-incidents/{incidentId}/retry"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel exceptions incidents configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel exceptions incidents untouched.",
   "emptyFirstRun": "No channel exceptions incidents configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelExceptionIncident",
    "contract": "catalogue",
    "purpose": "Channel Exceptions, Incidents & Recovery",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateChannelIncident",
    "contract": "catalogue",
    "purpose": "Own, investigate, resolve or close a channel incident",
    "trigger": "onAction",
    "invalidates": [
     "listChannelExceptionIncident"
    ]
   },
   {
    "operationId": "retryChannelIncident",
    "contract": "catalogue",
    "purpose": "Retry the failed channel call behind an incident",
    "trigger": "onAction",
    "invalidates": [
     "listChannelExceptionIncident"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-273",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-273"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 20 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formUpdateChannelIncident",
    "component": "modal",
    "trigger": "Save channel incident",
    "body": "**Collects what `updateChannelIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `ownerPrincipalId`, `slaDueAt`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save channel incident",
     "operation": "updateChannelIncident"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "ownerPrincipalId",
      "slaDueAt",
      "resolutionNote"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /channel-incidents/{incidentId}"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "incidentId",
     "from": "navigation",
     "optional": true
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
  "id": "ADM-274",
  "name": "Channel Performance & Commercial Analytics",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.7",
   "page": 29
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-performance-commercial-analytics-adm-274",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelPerformanceCommercialAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-268",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F167 step 12→13",
     "operation": "listChannelPerformanceCommercial"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can objectively compare channel contribution and commercial efficiency using consistent TICVAI metrics.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Measure) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Compare the commercial effectiveness of TICVAI sales channels.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search channel performance commercial",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Event",
        "Product",
        "Channel",
        "Partner",
        "Country",
        "Customer segment",
        "Date",
        "Time",
        "Currency"
       ],
       "notes": "The pack filters this screen by venue, event, product, channel, partner, country and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Gross Sales",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.grossSales"
      },
      {
       "kind": "metricTile",
       "label": "Net Sales",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.netSales"
      },
      {
       "kind": "metricTile",
       "label": "Transactions",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.transactions"
      },
      {
       "kind": "metricTile",
       "label": "Tickets Sold",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.ticketsSold"
      },
      {
       "kind": "metricTile",
       "label": "Average Order Value",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.averageOrderValue"
      },
      {
       "kind": "metricTile",
       "label": "Conversion Rate",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.conversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Cancellation Rate",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.cancellationRate"
      },
      {
       "kind": "metricTile",
       "label": "Refund Rate",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure"
      },
      {
       "kind": "metricTile",
       "label": "Capacity Utilization",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.capacityUtilization"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per Available Unit",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.revenuePerAvailableUnit"
      },
      {
       "kind": "metricTile",
       "label": "Fees",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.fees"
      },
      {
       "kind": "metricTile",
       "label": "Commission",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.commission"
      },
      {
       "kind": "metricTile",
       "label": "Cost of Sale where available",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 29 §Measure",
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.costOfSale"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel performance commercial list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the channel performance commercial untouched.",
   "emptyFirstRun": "No channel performance commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel performance commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelPerformanceCommercial",
    "contract": "catalogue",
    "purpose": "Channel Performance & Commercial Analytics",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-274",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-274"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 29. 12 of 22 labels bound to a contract property; 23 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-275",
  "name": "Channel Audit, Logs & Transaction Traceability",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.8",
   "page": 30
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-audit-logs-transaction-traceability-adm-275",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelAuditLogsTransactionTraceability.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-268",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F167 step 14→15",
     "operation": "listChannelLogTransaction"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Any channel transaction or operational change can be reconstructed from initiation through final result.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Provide complete traceability across channel configuration, synchronization and transactions.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search channel audit logs",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 30 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Channel",
        "Order ID",
        "Transaction ID",
        "Ticket",
        "Partner Reference",
        "Product",
        "Customer",
        "Correlation ID",
        "API Request",
        "User"
       ],
       "notes": "The pack filters this screen by channel, order id, transaction id, ticket, partner reference, product and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 30 §Search by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every channel audit logs",
       "columns": [
        "ChannelAuditLogsTransactionTraceabilityView.category",
        "Sync"
       ],
       "bindsTo": "ChannelAuditLogsTransactionTraceabilityView",
       "operation": "listChannelLogTransaction",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 30 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel audit logs",
       "bindsTo": "ChannelAuditLogsTransactionTraceabilityView",
       "columns": [
        "ChannelAuditLogsTransactionTraceabilityView.category",
        "Sync"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Transaction Trace”, “Partner Request”, “Export”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 30 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel audit logs list.",
   "error": "Could not load. Names which read failed and leaves the channel audit logs untouched.",
   "emptyFirstRun": "No channel audit logs yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel audit logs are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelLogTransaction",
    "contract": "catalogue",
    "purpose": "Channel Audit, Logs & Transaction Traceability",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ChannelAuditLogsTransactionTraceabilityView.category",
    "Sync"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-275",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-275"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 30. 10 of 21 labels bound to a contract property; 30 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-276",
  "name": "Channel Governance, SLA & Partner Control",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.9",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-governance-sla-partner-control-adm-276",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelGovernanceSlaPartnerControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-268",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F167 step 16→17",
     "operation": "listChannelGovernanceSla"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "governance obligations and can control channels that fall outside approved conditions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure/monitor) and no display directory — it is settings, not a population",
  "purpose": "Govern live channels and ensure that internal/external channels operate within approved commercial and service conditions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Channel Owner",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Partner Owner",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Commercial Agreement Reference",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "SLA",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Transaction Limits",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Rate Limits",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Contract Dates",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Renewal Date",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Support Contacts",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Escalation Contacts",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      },
      {
       "kind": "selectField",
       "label": "Review Frequency",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 32 §Configure/monitor"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel governance sla configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel governance sla untouched.",
   "emptyFirstRun": "No channel governance sla configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelGovernanceSla",
    "contract": "catalogue",
    "purpose": "Channel Governance, SLA & Partner Control",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-276",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-276"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 17 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-277",
  "name": "AI Channel Optimization & Intelligence Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "2",
   "number": "4.2.10",
   "page": 33
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-channel-optimization-intelligence-center-adm-277",
   "component": "apps/ticvai-web/src/routes/commercial/AiChannelOptimizationIntelligenceCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-268"
   ],
   "exitTo": [
    "ADM-268"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-268, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "administrators optimize revenue, capacity and channel performance while respecting commercial and governance controls. Board 2 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze; Monitor) and no metric row",
  "purpose": "Create the AI intelligence layer that looks across all sales channels together rather than optimizing each channel in isolation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Revenue impact, Risk. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Sales_Channel_Management_Reference.pdf, page 33 §Allow management to ask"
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
       "label": "Every channel optimization intelligence",
       "columns": [
        "AiChannelOptimizationIntelligenceCenterView.signals",
        "Channel Allocation & Rebalancing Operational capacity",
        "4.2.5"
       ],
       "bindsTo": "AiChannelOptimizationIntelligenceCenterView",
       "operation": "listChannel2",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 33 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel optimization intelligence",
       "bindsTo": "AiChannelOptimizationIntelligenceCenterView",
       "columns": [
        "AiChannelOptimizationIntelligenceCenterView.signals",
        "Channel Allocation & Rebalancing Operational capacity",
        "4.2.5"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Backend Screen Primary Responsibility”, “Product, Price & Availability”, “Synchronization”, “Channel Performance & Commercial”, “Channel Audit, Logs & Transaction”, “Channel Governance, SLA & Partner”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 33 §Analyze"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Revenue impact",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 33 §Allow management to ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel utilization",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 33 §Allow management to ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Risk",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 33 §Allow management to ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Decide catalogue AI finding",
       "operation": "decideCatalogueAiFinding",
       "permission": "AI_APPROVE",
       "notes": "**The human control on a governance risk or a channel recommendation** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /ai-findings/{findingId}/decision"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel optimization intelligence list.",
   "error": "Could not load. Names which read failed and leaves the channel optimization intelligence untouched.",
   "emptyFirstRun": "No channel optimization intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel optimization intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannel2",
    "contract": "catalogue",
    "purpose": "AI Channel Optimization & Intelligence Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listChannel",
    "contract": "catalogue",
    "purpose": "Channel Operations Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideCatalogueAiFinding",
    "contract": "catalogue",
    "purpose": "Acknowledge, accept, dismiss or resolve an AI finding",
    "trigger": "onAction",
    "invalidates": [
     "listChannel2",
     "listChannel"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "AiChannelOptimizationIntelligenceCenterView.signals"
   ],
   "params": [
    {
     "name": "findingId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-277",
   "workshopBoard": "wireframes/WS139 Sales Channel Management Board 2.dc.html#adm-277"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 33. 14 of 16 labels bound to a contract property; 19 of 70 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formDecideCatalogueAiFinding",
    "component": "modal",
    "trigger": "Decide catalogue AI finding",
    "body": "**Collects what `decideCatalogueAiFinding` sends before it is called.** Required: `decision`. Optional: `comment`, `ownerPrincipalId`, `dueDate`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decide catalogue AI finding",
     "operation": "decideCatalogueAiFinding"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "comment",
      "ownerPrincipalId",
      "dueDate"
     ]
    },
    "provenance": "contract catalogue.yaml POST /ai-findings/{findingId}/decision"
   }
  ],
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
 "decideCatalogueAiFinding": {
  "method": "POST",
  "path": "/ai-findings/{findingId}/decision",
  "contract": "catalogue",
  "summary": "Acknowledge, accept, dismiss or resolve an AI finding",
  "permission": "AI_APPROVE",
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
  "responds": "CatalogueAiFinding"
 },
 "listChannel": {
  "method": "GET",
  "path": "/channel",
  "contract": "catalogue",
  "summary": "Channel Operations Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "type",
    "in": "query",
    "required": false
   },
   {
    "name": "healthStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
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
 "listChannel2": {
  "method": "GET",
  "path": "/channel-2",
  "contract": "catalogue",
  "summary": "AI Channel Optimization & Intelligence Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "category",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listChannelAllocationRebalancing": {
  "method": "GET",
  "path": "/channel-allocation-rebalancing",
  "contract": "catalogue",
  "summary": "Channel Allocation & Rebalancing Operations",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
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
 "listChannelConnectionIntegration": {
  "method": "GET",
  "path": "/channel-connection-integration",
  "contract": "catalogue",
  "summary": "Channel Connection & Integration Manager",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   },
   {
    "name": "connectionType",
    "in": "query",
    "required": false
   },
   {
    "name": "environment",
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
 "listChannelExceptionIncident": {
  "method": "GET",
  "path": "/channel-exception-incident",
  "contract": "catalogue",
  "summary": "Channel Exceptions, Incidents & Recovery",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   },
   {
    "name": "severity",
    "in": "query",
    "required": false
   },
   {
    "name": "errorType",
    "in": "query",
    "required": false
   },
   {
    "name": "currentStatus",
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
 "listChannelGovernanceSla": {
  "method": "GET",
  "path": "/channel-governance-sla",
  "contract": "catalogue",
  "summary": "Channel Governance, SLA & Partner Control",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   },
   {
    "name": "complianceFlag",
    "in": "query",
    "required": false
   },
   {
    "name": "governanceStatus",
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
 "listChannelLogTransaction": {
  "method": "GET",
  "path": "/channel-log-transaction",
  "contract": "catalogue",
  "summary": "Channel Audit, Logs & Transaction Traceability",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "transactionId",
    "in": "query",
    "required": false
   },
   {
    "name": "ticket",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerReference",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
    "in": "query",
    "required": false
   },
   {
    "name": "correlationId",
    "in": "query",
    "required": false
   },
   {
    "name": "apiRequest",
    "in": "query",
    "required": false
   },
   {
    "name": "user",
    "in": "query",
    "required": false
   },
   {
    "name": "category",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
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
 "listChannelPerformanceCommercial": {
  "method": "GET",
  "path": "/channel-performance-commercial",
  "contract": "catalogue",
  "summary": "Channel Performance & Commercial Analytics",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "dateFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "dateTo",
    "in": "query",
    "required": false
   },
   {
    "name": "timeFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "timeTo",
    "in": "query",
    "required": false
   },
   {
    "name": "currency",
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
 "listProductPriceAvailability": {
  "method": "GET",
  "path": "/product-price-availability",
  "contract": "catalogue",
  "summary": "Product, Price & Availability Synchronization",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "domain",
    "in": "query",
    "required": false
   },
   {
    "name": "frequency",
    "in": "query",
    "required": false
   },
   {
    "name": "hasFailures",
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
 "listRealTimeAvailability": {
  "method": "GET",
  "path": "/real-time-availability",
  "contract": "promotions",
  "summary": "Real-Time Availability & Checkout Validation",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RealTimeAvailabilityCheckoutValidationView"
 },
 "listRealTimeChannel": {
  "method": "GET",
  "path": "/real-time-channel",
  "contract": "catalogue",
  "summary": "Real-Time Channel Availability & Inventory Monitor",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "availabilityStatus",
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
 "retryChannelIncident": {
  "method": "POST",
  "path": "/channel-incidents/{incidentId}/retry",
  "contract": "catalogue",
  "summary": "Retry the failed channel call behind an incident",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": null
 },
 "setChannelConnectionConfiguration": {
  "method": "PUT",
  "path": "/channel-connections",
  "contract": "catalogue",
  "summary": "Create or update a channel connection",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ChannelConnection",
  "responds": "ChannelConnection"
 },
 "setChannelSyncSetting": {
  "method": "PUT",
  "path": "/channel-syncs",
  "contract": "catalogue",
  "summary": "Set how one kind of data synchronises with a channel",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ChannelSync",
  "responds": "ChannelSync"
 },
 "testChannelConnection": {
  "method": "POST",
  "path": "/channel-connections/{connectionId}/test",
  "contract": "catalogue",
  "summary": "Test a channel connection now",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": "ChannelConnection"
 },
 "updateChannelIncident": {
  "method": "PATCH",
  "path": "/channel-incidents/{incidentId}",
  "contract": "catalogue",
  "summary": "Own, investigate, resolve or close a channel incident",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": "ChannelIncident"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiChannelOptimizationIntelligenceCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Channel Optimization & Intelligence Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "recommendation": {
    "type": "string",
    "description": "Recommendation"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "expectedImpact": {
    "type": "string",
    "description": "Expected Impact"
   },
   "confidence": {
    "type": "number",
    "description": "Confidence, 0-1",
    "minimum": 0,
    "maximum": 1
   },
   "constraints": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Constraints (contractual, capacity, approval)"
   },
   "requiredApproval": {
    "type": "string",
    "description": "Required Approval: the role that must approve",
    "nullable": true
   },
   "recommendationId": {
    "type": "string",
    "description": "Recommendation ID"
   },
   "category": {
    "type": "string",
    "enum": [
     "capacity",
     "channel",
     "schedule",
     "commercial",
     "operational"
    ],
    "description": "Recommendation Category (pack p.34)"
   },
   "channelIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Channels the recommendation concerns"
   },
   "signals": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "salesVelocity",
      "conversion",
      "capacity",
      "allocation",
      "revenue",
      "netRevenue",
      "pricing",
      "channelFees",
      "commission",
      "customerDemand",
      "timeToEvent",
      "historicalPerformance",
      "failures",
      "availability"
     ]
    },
    "description": "AI Analysis signals behind the recommendation (pack p.33-34)"
   },
   "simulation": {
    "type": "object",
    "nullable": true,
    "description": "Scenario Simulation estimate (pack p.34)",
    "properties": {
     "expectedUnitsSold": {
      "type": "integer"
     },
     "revenueImpact": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "channelUtilization": {
      "type": "number"
     },
     "risk": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ]
     },
     "contractualConstraints": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "status": {
    "type": "string",
    "description": "Status: proposed, accepted, modified, rejected, scheduled or assigned (decided 29 September, readiness close-out)"
   }
  }
 },
 "CatalogueAiFinding": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.ai_finding",
  "description": "**Something the AI noticed about the catalogue or its channels, for a person to act on** (29 September, data model DM3). Merges governance risks (ADM-137) and channel optimisation recommendations (ADM-272). Advisory only: a finding never changes configuration; acting on it goes through the ordinary operations and their approvals. **Created by the AI monitoring job** (29 September, writers pass); a person acknowledges, accepts, dismisses or resolves it with `decideCatalogueAiFinding`, and the job resolves one whose condition has cleared (`states/catalogue-ai-finding.yaml`).",
  "required": [
   "id",
   "scopePath",
   "domain",
   "findingType",
   "status",
   "detectedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "domain": {
    "type": "string",
    "enum": [
     "productGovernance",
     "channel"
    ]
   },
   "findingType": {
    "type": "string",
    "maxLength": 60,
    "description": "Governance: the `risk` value; channel: the recommendation `category`."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "salesChannelIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "severity": {
    "type": "string",
    "enum": [
     "critical",
     "high",
     "medium",
     "low",
     null
    ],
    "nullable": true
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1
   },
   "summary": {
    "type": "string",
    "description": "The recommendation, or the risk in one line."
   },
   "explanation": {
    "type": "string",
    "nullable": true
   },
   "businessImpact": {
    "type": "string",
    "nullable": true
   },
   "recommendedAction": {
    "type": "string",
    "nullable": true
   },
   "constraints": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "signals": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "simulation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Channel findings: `{expectedUnitsSold, revenueImpact, channelUtilization, risk, contractualConstraints}`."
   },
   "requiredApproval": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "dueDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "acknowledged",
     "accepted",
     "dismissed",
     "resolved"
    ],
    "default": "open"
   },
   "modelVersion": {
    "type": "string",
    "maxLength": 60,
    "nullable": true
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ChannelAllocationRebalancingOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Allocation & Rebalancing Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channel": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "initialAllocation": {
    "type": "integer",
    "description": "Initial Allocation"
   },
   "sold": {
    "type": "integer",
    "description": "Sold"
   },
   "held": {
    "type": "integer",
    "description": "Held"
   },
   "remaining": {
    "type": "integer",
    "description": "Remaining"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization %: sold plus held over allocated, 0-100",
    "minimum": 0,
    "maximum": 100
   },
   "salesVelocity": {
    "type": "number",
    "description": "Sales Velocity: units per hour over the last 24 hours (decided 29 September, readiness close-out)"
   },
   "forecast": {
    "type": "integer",
    "description": "Forecast: units the channel is expected to sell by the event"
   },
   "recommendedAllocation": {
    "type": "integer",
    "description": "Recommended Allocation (advisory)",
    "nullable": true
   },
   "contractualAllocation": {
    "type": "integer",
    "description": "Contractual allocation from the partner agreement",
    "nullable": true
   },
   "minimumGuaranteedInventory": {
    "type": "integer",
    "description": "Minimum guaranteed inventory",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event or performance ID"
   },
   "product": {
    "type": "string",
    "description": "Product ID",
    "nullable": true
   },
   "frozen": {
    "type": "boolean",
    "description": "Allocation frozen"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI allocation recommendations (pack p.27, e.g. transfer 500 units from OTA to B2C). Advisory only: nothing is changed until a user acts."
   }
  }
 },
 "ChannelAuditLogsTransactionTraceabilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Audit, Logs & Transaction Traceability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "userSystem": {
    "type": "string",
    "description": "User/System: user ID or the system component that acted"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "previousValue": {
    "type": "string",
    "description": "Previous Value (as text)",
    "nullable": true
   },
   "newValue": {
    "type": "string",
    "description": "New Value (as text)",
    "nullable": true
   },
   "reference": {
    "type": "string",
    "description": "Reference: order, transaction, ticket or partner reference",
    "nullable": true
   },
   "result": {
    "type": "string",
    "enum": [
     "success",
     "failure",
     "partial"
    ],
    "description": "Result"
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "uat",
     "production"
    ],
    "description": "Environment"
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "category": {
    "type": "string",
    "enum": [
     "configurationChange",
     "activation",
     "suspension",
     "allocationChange",
     "priceAssignment",
     "sync",
     "order",
     "cancellation",
     "error",
     "manualIntervention",
     "integrationChange"
    ],
    "description": "Audit Category (pack p.31)"
   },
   "trace": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "step": {
       "type": "string",
       "enum": [
        "partnerRequest",
        "requestReceived",
        "productValidation",
        "priceValidation",
        "capacityHold",
        "orderCreation",
        "paymentHandling",
        "ticketIssuance",
        "responseSent"
       ]
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "result": {
       "type": "string",
       "enum": [
        "success",
        "failure",
        "skipped"
       ]
      }
     }
    },
    "description": "Transaction Trace for an external order (pack p.31); empty for other records"
   }
  }
 },
 "ChannelConnection": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.channel_connection",
  "description": "**How TICVAI technically reaches a channel** (29 September, data model DM3). ADM-266. One row per connector and environment. **Credentials are never stored here**: `credentialsReference` names the secret in the vault. `control.integration_listing` is the marketplace entry an adapter comes from; this row is the tenant's connection using it.",
  "required": [
   "id",
   "scopePath",
   "salesChannelId",
   "connectorName",
   "environment",
   "connectionType"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "salesChannelId": {
    "type": "string",
    "format": "uuid"
   },
   "connectorName": {
    "type": "string",
    "maxLength": 200
   },
   "partner": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "uat",
     "production"
    ]
   },
   "connectionType": {
    "type": "string",
    "enum": [
     "ticvaiNative",
     "restApi",
     "webhook",
     "otaAdapter",
     "resellerApi",
     "partnerApi",
     "middleware",
     "fileSftp",
     "customConnector"
    ]
   },
   "direction": {
    "type": "string",
    "enum": [
     "outbound",
     "inbound",
     "bidirectional"
    ],
    "default": "outbound"
   },
   "endpoint": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "apiVersion": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "authenticationType": {
    "type": "string",
    "enum": [
     "none",
     "oauth",
     "apiKey",
     "clientCredentials",
     "certificate",
     "signedRequest"
    ]
   },
   "credentialsReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A vault reference, never the secret."
   },
   "certificateReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "certificateExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "timeoutMs": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "rateLimitPerMinute": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "ipRestrictions": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "retryPolicy": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`{maxAttempts, backoffSeconds}`."
   },
   "adapterId": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "connectionStatus": {
    "type": "string",
    "enum": [
     "notTested",
     "connected",
     "degraded",
     "offline",
     "disabled"
    ],
    "default": "notTested"
   },
   "lastTests": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "`[{test, result, testedAt}]`, the latest result per test."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "ChannelConnectionIntegrationManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Connection & Integration Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "connectorName": {
    "type": "string",
    "description": "Connector Name"
   },
   "channel": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "partner": {
    "type": "string",
    "description": "Partner ID (the B2B/OTA partner record)",
    "nullable": true
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "uat",
     "production"
    ],
    "description": "Environment (pack p.23)"
   },
   "endpoint": {
    "type": "string",
    "description": "Endpoint URL",
    "format": "uri",
    "nullable": true
   },
   "apiVersion": {
    "type": "string",
    "description": "API Version",
    "nullable": true
   },
   "authenticationType": {
    "type": "string",
    "enum": [
     "none",
     "oauth",
     "apiKey",
     "clientCredentials",
     "certificate",
     "signedRequest"
    ],
    "description": "Authentication Type (pack p.23 Security)"
   },
   "credentialsReference": {
    "type": "string",
    "description": "Credentials reference: the secret-store key; the secret itself is never returned"
   },
   "certificate": {
    "type": "string",
    "description": "Certificate reference (secret-store key)",
    "nullable": true
   },
   "timeout": {
    "type": "integer",
    "description": "Timeout in seconds",
    "minimum": 1,
    "default": 30
   },
   "rateLimit": {
    "type": "integer",
    "description": "Rate Limit: requests per minute",
    "minimum": 1,
    "nullable": true
   },
   "ipRestrictions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "IP Restrictions: allowed CIDR ranges"
   },
   "connectionStatus": {
    "type": "string",
    "description": "Connection Status: notTested, connected, degraded, failed or disabled (decided 29 September, readiness close-out)"
   },
   "connectionType": {
    "type": "string",
    "enum": [
     "ticvaiNative",
     "restApi",
     "webhook",
     "otaAdapter",
     "resellerApi",
     "partnerApi",
     "middleware",
     "fileSftp",
     "customConnector"
    ],
    "description": "Connection Type (pack p.22)"
   },
   "direction": {
    "type": "string",
    "enum": [
     "outbound",
     "inbound",
     "bidirectional"
    ],
    "description": "Who calls whom: TICVAI calls the partner's API, the partner calls TICVAI, or both (MoM 31 Aug §4.3)"
   },
   "adapterId": {
    "type": "string",
    "description": "Reusable adapter for an external platform; the platform is named as data on the adapter. Enabling it for a new tenant needs no rebuild (MoM 31 Aug §4.3)",
    "nullable": true
   },
   "retryPolicy": {
    "type": "object",
    "description": "Retry Policy (pack p.23)",
    "properties": {
     "maxAttempts": {
      "type": "integer",
      "minimum": 0
     },
     "backoffSeconds": {
      "type": "integer",
      "minimum": 0
     }
    }
   },
   "certificateExpiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Certificate expiry, for governance alerts",
    "nullable": true
   },
   "lastTests": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "test": {
       "type": "string",
       "enum": [
        "authentication",
        "connectivity",
        "product",
        "price",
        "availability",
        "order",
        "cancellation"
       ]
      },
      "result": {
       "type": "string",
       "enum": [
        "passed",
        "failed",
        "notSupported"
       ]
      },
      "testedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    },
    "description": "Connection Testing results, latest per test (pack p.23)"
   }
  }
 },
 "ChannelExceptionsIncidentsRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Exceptions, Incidents & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "incidentId": {
    "type": "string",
    "description": "Incident ID"
   },
   "channel": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "partner": {
    "type": "string",
    "description": "Partner ID",
    "nullable": true
   },
   "severity": {
    "type": "string",
    "enum": [
     "critical",
     "high",
     "medium",
     "low"
    ],
    "description": "Severity (pack p.28)"
   },
   "errorType": {
    "type": "string",
    "enum": [
     "connectionFailure",
     "authenticationFailure",
     "productSyncFailure",
     "pricingMismatch",
     "inventoryMismatch",
     "orderFailure",
     "paymentError",
     "timeout",
     "cancellationFailure",
     "duplicateTransaction",
     "fulfillmentFailure",
     "rateLimit",
     "partnerError"
    ],
    "description": "Error Type (pack p.27-28 Exception Categories)"
   },
   "affectedProductEvent": {
    "type": "string",
    "description": "Affected Product/Event: product or event ID",
    "nullable": true
   },
   "transactionsAffected": {
    "type": "integer",
    "description": "Transactions Affected"
   },
   "businessImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Business Impact: estimated sales value at risk"
   },
   "firstDetected": {
    "type": "string",
    "format": "date-time",
    "description": "First Detected"
   },
   "owner": {
    "type": "string",
    "description": "Owner (user ID)",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "description": "SLA: resolution due time",
    "nullable": true
   },
   "currentStatus": {
    "type": "string",
    "description": "Current Status: open, assigned, investigating, recovering, resolved or closed (decided 29 September, readiness close-out)"
   },
   "errorCode": {
    "type": "string",
    "description": "Error Code",
    "nullable": true
   },
   "apiRequestReference": {
    "type": "string",
    "description": "API Request Reference",
    "nullable": true
   },
   "response": {
    "type": "string",
    "description": "Response body, sensitive data masked",
    "nullable": true
   },
   "correlationId": {
    "type": "string",
    "description": "Correlation ID",
    "nullable": true
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp of the last failing call",
    "nullable": true
   },
   "retryCount": {
    "type": "integer",
    "description": "Retry Count"
   },
   "aiSummary": {
    "type": "string",
    "description": "AI summary of the incident in business language (pack p.29); advisory",
    "nullable": true
   }
  }
 },
 "ChannelGovernanceSlaPartnerControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Governance, SLA & Partner Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channelOwner": {
    "type": "string",
    "description": "Channel Owner (user ID)",
    "nullable": true
   },
   "partnerOwner": {
    "type": "string",
    "description": "Partner Owner (user ID)",
    "nullable": true
   },
   "commercialAgreementReference": {
    "type": "string",
    "description": "Commercial Agreement Reference: the B2B/OTA agreement ID",
    "nullable": true
   },
   "sla": {
    "type": "object",
    "description": "SLA targets",
    "properties": {
     "availabilityPercent": {
      "type": "number"
     },
     "responseTimeMs": {
      "type": "integer"
     },
     "resolutionHours": {
      "type": "number"
     }
    }
   },
   "transactionLimits": {
    "type": "integer",
    "description": "Transaction Limits: maximum transactions per day",
    "nullable": true
   },
   "rateLimits": {
    "type": "integer",
    "description": "Rate Limits: requests per minute",
    "nullable": true
   },
   "contractDates": {
    "type": "object",
    "description": "Contract Dates",
    "properties": {
     "start": {
      "type": "string",
      "format": "date"
     },
     "end": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   },
   "renewalDate": {
    "type": "string",
    "format": "date",
    "description": "Renewal Date",
    "nullable": true
   },
   "supportContacts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Support Contacts"
   },
   "escalationContacts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Escalation Contacts"
   },
   "availability": {
    "type": "number",
    "description": "Availability % measured"
   },
   "apiResponseTime": {
    "type": "integer",
    "description": "API Response Time, milliseconds (p95) (decided 29 September, readiness close-out)"
   },
   "transactionSuccess": {
    "type": "number",
    "description": "Transaction Success %"
   },
   "errorRate": {
    "type": "number",
    "description": "Error Rate %"
   },
   "incidentResolutionTime": {
    "type": "number",
    "description": "Incident Resolution Time, average hours"
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "reviewFrequency": {
    "type": "string",
    "enum": [
     "monthly",
     "quarterly",
     "semiAnnual",
     "annual"
    ],
    "description": "Review Frequency"
   },
   "syncSuccess": {
    "type": "number",
    "description": "Sync Success %"
   },
   "complianceFlags": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "expiredAgreement",
      "expiredCertificate",
      "expiringApiCredentials",
      "missingOwner",
      "unapprovedProductionIntegration",
      "slaBreach",
      "excessiveTransactionFailures"
     ]
    },
    "description": "Compliance Controls raised (pack p.32-33)"
   },
   "governanceStatus": {
    "type": "string",
    "description": "Governance status: normal, underReview, restricted or suspended (decided 29 September, readiness close-out)"
   }
  }
 },
 "ChannelIncident": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.channel_incident",
  "description": "**A channel failure someone has to resolve** (29 September, data model DM3). ADM-269. Opened by the sync and order paths when a call to or from a channel fails; retried, owned and closed here. The per-call trace is in `catalogue.audit_entry` (`domain: channel`). **Opened by the channel sync and order jobs, never through the API** (29 September, writers pass); owned and closed with `updateChannelIncident`, retried with `retryChannelIncident` (`states/channel-incident.yaml`).",
  "required": [
   "id",
   "scopePath",
   "salesChannelId",
   "severity",
   "errorType",
   "status",
   "firstDetectedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "salesChannelId": {
    "type": "string",
    "format": "uuid"
   },
   "channelConnectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "partner": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "severity": {
    "type": "string",
    "enum": [
     "critical",
     "high",
     "medium",
     "low"
    ]
   },
   "errorType": {
    "type": "string",
    "enum": [
     "connectionFailure",
     "authenticationFailure",
     "productSyncFailure",
     "pricingMismatch",
     "inventoryMismatch",
     "orderFailure",
     "paymentError",
     "timeout",
     "cancellationFailure",
     "duplicateTransaction",
     "fulfillmentFailure",
     "rateLimit",
     "partnerError"
    ]
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "transactionsAffected": {
    "type": "integer",
    "default": 0
   },
   "businessImpact": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "firstDetectedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "retrying",
     "resolved",
     "closed"
    ],
    "default": "open"
   },
   "errorCode": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "apiRequestReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "responseExcerpt": {
    "type": "string",
    "nullable": true,
    "description": "The partner response, truncated and scrubbed of personal data."
   },
   "correlationId": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "retryCount": {
    "type": "integer",
    "default": 0
   },
   "aiSummary": {
    "type": "string",
    "nullable": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "ChannelOperationsCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Channel Operations Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activeChannels": {
    "type": "integer",
    "description": "Active Channels"
   },
   "connectedChannels": {
    "type": "integer",
    "description": "Connected Channels"
   },
   "degradedChannels": {
    "type": "integer",
    "description": "Degraded Channels"
   },
   "offlineChannels": {
    "type": "integer",
    "description": "Offline Channels"
   },
   "transactionsToday": {
    "type": "integer",
    "description": "Transactions Today"
   },
   "grossSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross Sales today"
   },
   "productsAvailable": {
    "type": "integer",
    "description": "Products Available"
   },
   "synchronizationErrors": {
    "type": "integer",
    "description": "Synchronization Errors"
   },
   "capacityAlerts": {
    "type": "integer",
    "description": "Capacity Alerts"
   },
   "pricingErrors": {
    "type": "integer",
    "description": "Pricing Errors"
   },
   "failedTransactions": {
    "type": "integer",
    "description": "Failed Transactions"
   },
   "openOperationalIncidents": {
    "type": "integer",
    "description": "Open Operational Incidents"
   },
   "liveActivity": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "occurredAt": {
       "type": "string",
       "format": "date-time"
      },
      "channelId": {
       "type": "string"
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Live Activity: latest important channel events, newest first (the 50 most recent (decided 29 September, readiness close-out))"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Operational problems prioritised by business impact (pack p.22). Advisory only: nothing is changed until a user acts."
   }
  }
 },
 "ChannelOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channel": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "type": {
    "type": "string",
    "enum": [
     "b2cWeb",
     "b2cMobileApp",
     "pos",
     "mobilePos",
     "flyingPos",
     "kiosk",
     "callCentre",
     "b2bPortal",
     "reseller",
     "ota",
     "api",
     "partnerPortal",
     "marketplace",
     "thirdPartyChannel",
     "customChannel"
    ],
    "description": "Type: the channel type"
   },
   "venueScope": {
    "type": "string",
    "description": "Venue/Scope"
   },
   "connectionStatus": {
    "type": "string",
    "description": "Connection Status: connected, degraded, offline or maintenance"
   },
   "lastSync": {
    "type": "string",
    "format": "date-time",
    "description": "Last Sync",
    "nullable": true
   },
   "products": {
    "type": "integer",
    "description": "Products available on the channel"
   },
   "transactions": {
    "type": "integer",
    "description": "Transactions today"
   },
   "salesValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sales Value today"
   },
   "inventoryStatus": {
    "type": "string",
    "description": "Inventory Status: ok, low, soldOut or syncError (decided 29 September, readiness close-out)"
   },
   "pricingStatus": {
    "type": "string",
    "description": "Pricing Status: ok, mismatch or error (decided 29 September, readiness close-out)"
   },
   "errorCount": {
    "type": "integer",
    "description": "Error Count today"
   },
   "healthScore": {
    "type": "number",
    "description": "Health Score, 0-100",
    "minimum": 0,
    "maximum": 100
   },
   "healthStatus": {
    "type": "string",
    "description": "Health Status: healthy, warning, degraded, critical, offline or maintenance (pack p.21)"
   }
  }
 },
 "ChannelPerformanceCommercialAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Performance & Commercial Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "grossSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross Sales"
   },
   "netSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Net Sales"
   },
   "transactions": {
    "type": "integer",
    "description": "Transactions"
   },
   "ticketsSold": {
    "type": "integer",
    "description": "Tickets Sold"
   },
   "averageOrderValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Average Order Value"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate %",
    "nullable": true
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate %"
   },
   "capacityUtilization": {
    "type": "number",
    "description": "Capacity Utilization %"
   },
   "revenuePerAvailableUnit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Available Unit"
   },
   "fees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fees"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "costOfSale": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost of Sale where available"
   },
   "allocation": {
    "type": "integer",
    "description": "Partner Comparison: Allocation",
    "nullable": true
   },
   "sold": {
    "type": "integer",
    "description": "Partner Comparison: Sold",
    "nullable": true
   },
   "utilization": {
    "type": "number",
    "description": "Partner Comparison: Utilization %",
    "nullable": true
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Comparison: Revenue"
   },
   "cancellations": {
    "type": "integer",
    "description": "Partner Comparison: Cancellations",
    "nullable": true
   },
   "settlement": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Comparison: Settlement, amount settled in the period"
   },
   "growth": {
    "type": "number",
    "description": "Partner Comparison: Growth % against the previous equal period",
    "nullable": true
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "partner": {
    "type": "string",
    "description": "Partner ID for a B2B/OTA row",
    "nullable": true
   },
   "refundRate": {
    "type": "number",
    "description": "Refund Rate %"
   },
   "funnel": {
    "type": "object",
    "nullable": true,
    "description": "Channel Funnel for digital channels (pack p.30)",
    "properties": {
     "available": {
      "type": "integer"
     },
     "viewed": {
      "type": "integer"
     },
     "selected": {
      "type": "integer"
     },
     "checkout": {
      "type": "integer"
     },
     "paid": {
      "type": "integer"
     }
    }
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Insights (pack p.30). Advisory only: nothing is changed until a user acts."
   }
  }
 },
 "ChannelSync": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.channel_sync",
  "description": "**The synchronisation state of one channel for one kind of data** (29 September, data model DM3). ADM-267. One row per channel and domain (product, price, availability ...); counts are the latest run's, overwritten by the sync job. **Two writers** (29 September, writers pass): the sync job writes the counts and timestamps (the `readOnly` fields); a person sets `direction`, `frequency` and `isPaused` with `setChannelSyncSetting`.",
  "required": [
   "id",
   "scopePath",
   "salesChannelId",
   "domain"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "salesChannelId": {
    "type": "string",
    "format": "uuid"
   },
   "channelConnectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "domain": {
    "type": "string",
    "enum": [
     "product",
     "productDescription",
     "schedule",
     "availability",
     "capacity",
     "price",
     "tax",
     "fees",
     "media",
     "restrictions",
     "salesStatus"
    ]
   },
   "direction": {
    "type": "string",
    "enum": [
     "ticvaiToChannel",
     "channelToTicvai",
     "bidirectional"
    ],
    "default": "ticvaiToChannel"
   },
   "frequency": {
    "type": "string",
    "enum": [
     "realTime",
     "nearRealTime",
     "scheduled",
     "manual",
     "eventTriggered"
    ],
    "default": "nearRealTime"
   },
   "isPaused": {
    "type": "boolean",
    "default": false
   },
   "lastSuccessfulSyncAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "nextSyncAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "recordsProcessed": {
    "type": "integer",
    "readOnly": true
   },
   "successful": {
    "type": "integer",
    "readOnly": true
   },
   "failed": {
    "type": "integer",
    "readOnly": true
   },
   "pending": {
    "type": "integer",
    "readOnly": true
   },
   "warnings": {
    "type": "integer",
    "readOnly": true
   },
   "durationMs": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
   },
   "mismatchCount": {
    "type": "integer",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
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
 "ProductPriceAvailabilitySynchronizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product, Price & Availability Synchronization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "lastSuccessfulSync": {
    "type": "string",
    "format": "date-time",
    "description": "Last Successful Sync",
    "nullable": true
   },
   "nextSync": {
    "type": "string",
    "format": "date-time",
    "description": "Next Sync; empty for manual",
    "nullable": true
   },
   "recordsProcessed": {
    "type": "integer",
    "description": "Records Processed in the last run"
   },
   "successful": {
    "type": "integer",
    "description": "Successful"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "pending": {
    "type": "integer",
    "description": "Pending"
   },
   "warning": {
    "type": "integer",
    "description": "Warning: records synced with a warning"
   },
   "duration": {
    "type": "integer",
    "description": "Duration of the last run in seconds"
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "connectorId": {
    "type": "string",
    "description": "Connector ID (ADM-269)",
    "nullable": true
   },
   "domain": {
    "type": "string",
    "enum": [
     "product",
     "productDescription",
     "schedule",
     "availability",
     "capacity",
     "price",
     "tax",
     "fees",
     "media",
     "restrictions",
     "salesStatus"
    ],
    "description": "Synchronization Domain (pack p.23-24)"
   },
   "direction": {
    "type": "string",
    "enum": [
     "ticvaiToChannel",
     "channelToTicvai",
     "bidirectional"
    ],
    "description": "Synchronization Direction (pack p.24)"
   },
   "frequency": {
    "type": "string",
    "enum": [
     "realTime",
     "nearRealTime",
     "scheduled",
     "manual",
     "eventTriggered"
    ],
    "description": "Sync Frequency (pack p.24)"
   },
   "paused": {
    "type": "boolean",
    "description": "Sync paused"
   },
   "mismatchCount": {
    "type": "integer",
    "description": "Difference Detection: records whose channel value differs from TICVAI's"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Grouped repetitive failures and probable root causes (pack p.25). Advisory only: nothing is changed until a user acts."
   }
  }
 },
 "RealTimeAvailabilityCheckoutValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Real-Time Availability & Checkout Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "failedChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "productInactive",
      "inventoryUnavailable",
      "capacityUnavailable",
      "timeslotUnavailable",
      "resourceUnavailable",
      "priceInvalid",
      "promotionInvalid",
      "partnerComponentInvalid",
      "componentMappingInvalid"
     ]
    },
    "description": "Checkout validations that failed; empty means the bundle is sellable."
   },
   "bundleId": {
    "type": "string",
    "description": "Bundle ID"
   },
   "sellable": {
    "type": "boolean",
    "description": "Whether the bundle can be sold now"
   }
  }
 },
 "RealTimeChannelAvailabilityInventoryMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Real-Time Channel Availability & Inventory Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "allocated": {
    "type": "integer",
    "description": "Allocated; empty when the channel sells from the shared pool",
    "nullable": true
   },
   "sold": {
    "type": "integer",
    "description": "Sold"
   },
   "held": {
    "type": "integer",
    "description": "Held"
   },
   "remaining": {
    "type": "integer",
    "description": "Remaining sellable units"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization %: sold plus held over allocated, 0-100",
    "minimum": 0,
    "maximum": 100
   },
   "salesVelocity": {
    "type": "number",
    "description": "Sales Velocity: units sold per hour over the last 24 hours (decided 29 September, readiness close-out)"
   },
   "forecastedSellOut": {
    "type": "string",
    "format": "date-time",
    "description": "Forecasted Sell-Out; empty when no sell-out is forecast",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Product ID"
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "event": {
    "type": "string",
    "description": "Event or performance ID",
    "nullable": true
   },
   "sharedPool": {
    "type": "boolean",
    "description": "The channel sells from the shared pool (shown as Shared in the matrix)"
   },
   "availabilityStatus": {
    "type": "string",
    "description": "Status for this product/channel: available, lowAvailability, soldOut, closed, suspended, notAssigned or syncError (pack p.25)"
   }
  }
 }
}
```
