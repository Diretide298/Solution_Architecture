# WS58 — Sales Channel Management board 2

**10 screens · 10 operations · 10 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-268` | Channel Operations Command Center | commandCentre | 1 | 0 | — |
| `ADM-269` | Channel Connection & Integration Manager | configEditor | 1 | 0 | — |
| `ADM-270` | Product, Price & Availability Synchronization | listDetail | 1 | 0 | — |
| `ADM-271` | Real-Time Channel Availability & Inventory Monitor | listDetail | 1 | 0 | — |
| `ADM-272` | Channel Allocation & Rebalancing Operations | listDetail | 1 | 0 | — |
| `ADM-273` | Channel Exceptions, Incidents & Recovery | configEditor | 1 | 0 | — |
| `ADM-274` | Channel Performance & Commercial Analytics | commandCentre | 1 | 0 | — |
| `ADM-275` | Channel Audit, Logs & Transaction Traceability | listDetail | 1 | 0 | — |
| `ADM-276` | Channel Governance, SLA & Partner Control | configEditor | 1 | 0 | — |
| `ADM-277` | AI Channel Optimization & Intelligence Center | listDetail | 1 | 0 | — |

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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each channel should display) — counts over a population, then the population",
  "purpose": "Provide a real-time operational view of all active TICVAI sales channels.",
  "purposeNote": "Operations teams can determine the health, commercial activity and current issues of every active sales channel from one central workspace.",
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
       "bindsTo": "ChannelOperationsCommandCenterView.activeChannels"
      },
      {
       "kind": "metricTile",
       "label": "Connected Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.connectedChannels"
      },
      {
       "kind": "metricTile",
       "label": "Degraded Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.degradedChannels"
      },
      {
       "kind": "metricTile",
       "label": "Offline Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.offlineChannels"
      },
      {
       "kind": "metricTile",
       "label": "Transactions Today",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.transactionsToday"
      },
      {
       "kind": "metricTile",
       "label": "Gross Sales",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.grossSales"
      },
      {
       "kind": "metricTile",
       "label": "Products Available",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.productsAvailable"
      },
      {
       "kind": "metricTile",
       "label": "Synchronization Errors",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.synchronizationErrors"
      },
      {
       "kind": "metricTile",
       "label": "Capacity Alerts",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.capacityAlerts"
      },
      {
       "kind": "metricTile",
       "label": "Pricing Errors",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.pricingErrors"
      },
      {
       "kind": "metricTile",
       "label": "Failed Transactions",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 20 §Display",
       "bindsTo": "ChannelOperationsCommandCenterView.failedTransactions"
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
    "operationId": "listChannel",
    "contract": "catalogue",
    "purpose": "Channel Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-268"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Configure and manage the technical connection between TICVAI and external or internal sales channels.",
  "purposeNote": "Authorized technical administrators can establish, test and monitor channel connections without modifying core TICVAI application code for supported connector types.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Webhook, Partner API. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
   },
   {
    "operation": null,
    "why": "**Channel Connection & Integration Manager declares no operation that writes anything** — its only declared call is `listChannelConnectionIntegration`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Webhook",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partner API",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 22 §Support"
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-269"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 16 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control how TICVAI distributes commercial information to connected channels and receives supported updates.",
  "purposeNote": "supported sales channels while clearly identifying failed or inconsistent records.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Channel → TICVAI, Sync Now, Retry Failed, Compare, Reprocess, Pause Sync, Resume, Export Error. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-270"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 23. 8 of 8 labels bound to a contract property; 21 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide operations with a live view of what each channel can currently sell.",
  "purposeNote": "Operations can understand current sellable availability across all channels without checking each channel independently.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-271"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow authorized users to operationally adjust inventory allocations as demand changes. Board 1 defines the allocation rules. Board 2 manages those allocations during live operations.",
  "purposeNote": "Authorized users can dynamically rebalance unsold channel capacity without affecting confirmed orders or exceeding underlying capacity.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-272"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide one operational workspace for resolving channel problems.",
  "purposeNote": "Channel incidents can be identified, assigned, investigated and recovered from a central operational workflow with complete traceability.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Connection Failure, Product Sync Failure, Pricing Mismatch, Order Failure, Payment Error, Duplicate Transaction, Partner Error. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-273"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 19 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Measure) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Compare the commercial effectiveness of TICVAI sales channels.",
  "purposeNote": "Management can objectively compare channel contribution and commercial efficiency using consistent TICVAI metrics.",
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
       "bindsTo": "ChannelPerformanceCommercialAnalyticsView.costOfSaleWhereAvailable"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-274"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Provide complete traceability across channel configuration, synchronization and transactions.",
  "purposeNote": "Any channel transaction or operational change can be reconstructed from initiation through final result.",
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
        "ChannelAuditLogsTransactionTraceabilityView.configurationChange",
        "ChannelAuditLogsTransactionTraceabilityView.activation",
        "ChannelAuditLogsTransactionTraceabilityView.suspension",
        "ChannelAuditLogsTransactionTraceabilityView.allocationChange",
        "ChannelAuditLogsTransactionTraceabilityView.priceAssignment",
        "Sync",
        "ChannelAuditLogsTransactionTraceabilityView.order",
        "ChannelAuditLogsTransactionTraceabilityView.cancellation",
        "ChannelAuditLogsTransactionTraceabilityView.error",
        "ChannelAuditLogsTransactionTraceabilityView.manualIntervention",
        "ChannelAuditLogsTransactionTraceabilityView.integrationChange"
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
        "ChannelAuditLogsTransactionTraceabilityView.configurationChange",
        "ChannelAuditLogsTransactionTraceabilityView.activation",
        "ChannelAuditLogsTransactionTraceabilityView.suspension",
        "ChannelAuditLogsTransactionTraceabilityView.allocationChange",
        "ChannelAuditLogsTransactionTraceabilityView.priceAssignment",
        "Sync",
        "ChannelAuditLogsTransactionTraceabilityView.order",
        "ChannelAuditLogsTransactionTraceabilityView.cancellation",
        "ChannelAuditLogsTransactionTraceabilityView.error",
        "ChannelAuditLogsTransactionTraceabilityView.manualIntervention",
        "ChannelAuditLogsTransactionTraceabilityView.integrationChange"
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
    "ChannelAuditLogsTransactionTraceabilityView.configurationChange",
    "ChannelAuditLogsTransactionTraceabilityView.activation",
    "ChannelAuditLogsTransactionTraceabilityView.suspension",
    "ChannelAuditLogsTransactionTraceabilityView.allocationChange",
    "ChannelAuditLogsTransactionTraceabilityView.priceAssignment",
    "Sync"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-275"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure/monitor) and no display directory — it is settings, not a population",
  "purpose": "Govern live channels and ensure that internal/external channels operate within approved commercial and service conditions.",
  "purposeNote": "governance obligations and can control channels that fall outside approved conditions.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-276"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze; Monitor) and no metric row",
  "purpose": "Create the AI intelligence layer that looks across all sales channels together rather than optimizing each channel in isolation.",
  "purposeNote": "administrators optimize revenue, capacity and channel performance while respecting commercial and governance controls. Board 2 — Final Screen Register",
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
        "AiChannelOptimizationIntelligenceCenterView.salesVelocity",
        "AiChannelOptimizationIntelligenceCenterView.conversion",
        "AiChannelOptimizationIntelligenceCenterView.capacity",
        "AiChannelOptimizationIntelligenceCenterView.allocation",
        "AiChannelOptimizationIntelligenceCenterView.revenue",
        "AiChannelOptimizationIntelligenceCenterView.netRevenue",
        "AiChannelOptimizationIntelligenceCenterView.pricing",
        "AiChannelOptimizationIntelligenceCenterView.channelFees",
        "AiChannelOptimizationIntelligenceCenterView.commission",
        "AiChannelOptimizationIntelligenceCenterView.customerDemand",
        "AiChannelOptimizationIntelligenceCenterView.timeToEvent",
        "AiChannelOptimizationIntelligenceCenterView.historicalPerformance",
        "AiChannelOptimizationIntelligenceCenterView.failures",
        "AiChannelOptimizationIntelligenceCenterView.availability",
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
        "AiChannelOptimizationIntelligenceCenterView.salesVelocity",
        "AiChannelOptimizationIntelligenceCenterView.conversion",
        "AiChannelOptimizationIntelligenceCenterView.capacity",
        "AiChannelOptimizationIntelligenceCenterView.allocation",
        "AiChannelOptimizationIntelligenceCenterView.revenue",
        "AiChannelOptimizationIntelligenceCenterView.netRevenue",
        "AiChannelOptimizationIntelligenceCenterView.pricing",
        "AiChannelOptimizationIntelligenceCenterView.channelFees",
        "AiChannelOptimizationIntelligenceCenterView.commission",
        "AiChannelOptimizationIntelligenceCenterView.customerDemand",
        "AiChannelOptimizationIntelligenceCenterView.timeToEvent",
        "AiChannelOptimizationIntelligenceCenterView.historicalPerformance",
        "AiChannelOptimizationIntelligenceCenterView.failures",
        "AiChannelOptimizationIntelligenceCenterView.availability",
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
   }
  ],
  "entryState": {
   "preloaded": [
    "AiChannelOptimizationIntelligenceCenterView.salesVelocity",
    "AiChannelOptimizationIntelligenceCenterView.conversion",
    "AiChannelOptimizationIntelligenceCenterView.capacity",
    "AiChannelOptimizationIntelligenceCenterView.allocation",
    "AiChannelOptimizationIntelligenceCenterView.revenue",
    "AiChannelOptimizationIntelligenceCenterView.netRevenue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-277"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 33. 14 of 16 labels bound to a contract property; 19 of 70 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listChannel": {
  "method": "GET",
  "path": "/channel",
  "contract": "catalogue",
  "summary": "Channel Operations Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelOperationsCommandCenterView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "AiChannelOptimizationIntelligenceCenterView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelAllocationRebalancingOperationsView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelConnectionIntegrationManagerView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelExceptionsIncidentsRecoveryView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelGovernanceSlaPartnerControlView"
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
   }
  ],
  "requestBody": null,
  "responds": "ChannelAuditLogsTransactionTraceabilityView"
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
    "name": "date",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ChannelPerformanceCommercialAnalyticsView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ProductPriceAvailabilitySynchronizationView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "RealTimeChannelAvailabilityInventoryMonitorView"
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
   "salesVelocity": {
    "type": "string",
    "description": "Sales velocity"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "allocation": {
    "type": "string",
    "description": "Allocation"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "netRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Net revenue"
   },
   "pricing": {
    "type": "string",
    "description": "Pricing"
   },
   "channelFees": {
    "type": "string",
    "description": "Channel fees"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "customerDemand": {
    "type": "string",
    "description": "Customer demand"
   },
   "timeToEvent": {
    "type": "string",
    "format": "date-time",
    "description": "Time to event"
   },
   "historicalPerformance": {
    "type": "string",
    "description": "Historical performance"
   },
   "failures": {
    "type": "string",
    "description": "Failures"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
   },
   "expectedUnitsSold": {
    "type": "string",
    "description": "Expected units sold"
   },
   "revenueImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue impact"
   },
   "channelUtilization": {
    "type": "number",
    "description": "Channel utilization"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "contractualConstraints": {
    "type": "string",
    "description": "Contractual constraints"
   },
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
    "type": "string",
    "description": "Confidence"
   },
   "constraints": {
    "type": "string",
    "description": "Constraints"
   },
   "requiredApproval": {
    "type": "string",
    "description": "Required Approval"
   },
   "realTimeChannelAvailabilityInventory": {
    "type": "string",
    "format": "date-time",
    "description": "Real-Time Channel Availability & Inventory"
   },
   "paymentFulfillmentValidatePublish": {
    "type": "string",
    "description": "Payment/Fulfillment → Validate → Publish"
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
    "description": "Channel"
   },
   "initialAllocation": {
    "type": "string",
    "description": "Initial Allocation"
   },
   "sold": {
    "type": "string",
    "description": "Sold"
   },
   "held": {
    "type": "string",
    "description": "Held"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization"
   },
   "salesVelocity": {
    "type": "string",
    "description": "Sales Velocity"
   },
   "forecast": {
    "type": "string",
    "description": "Forecast"
   },
   "recommendedAllocation": {
    "type": "string",
    "description": "Recommended Allocation"
   },
   "increaseAllocation": {
    "type": "string",
    "description": "Increase allocation"
   },
   "reduceAllocation": {
    "type": "string",
    "description": "Reduce allocation"
   },
   "returnInventory": {
    "type": "string",
    "description": "Return inventory"
   },
   "allocated1000": {
    "type": "string",
    "description": "Allocated: 1,000"
   },
   "sold280": {
    "type": "string",
    "description": "Sold: 280"
   },
   "remaining720": {
    "type": "string",
    "description": "Remaining: 720"
   },
   "allocated6000": {
    "type": "string",
    "description": "Allocated: 6,000"
   },
   "sold5880": {
    "type": "string",
    "description": "Sold: 5,880"
   },
   "remaining120": {
    "type": "string",
    "description": "Remaining: 120"
   },
   "contractualAllocation": {
    "type": "string",
    "description": "Contractual allocation"
   },
   "minimumGuaranteedInventory": {
    "type": "string",
    "description": "Minimum guaranteed inventory"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "existingHolds": {
    "type": "string",
    "description": "Existing holds"
   },
   "confirmedTransactions": {
    "type": "string",
    "description": "Confirmed transactions"
   },
   "approvalThresholds": {
    "type": "string",
    "description": "Approval thresholds"
   }
  }
 },
 "ChannelAuditLogsTransactionTraceabilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Audit, Logs & Transaction Traceability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "configurationChange": {
    "type": "string",
    "description": "Configuration Change"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "suspension": {
    "type": "string",
    "description": "Suspension"
   },
   "allocationChange": {
    "type": "string",
    "description": "Allocation Change"
   },
   "priceAssignment": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Assignment"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "error": {
    "type": "string",
    "description": "Error"
   },
   "manualIntervention": {
    "type": "string",
    "description": "Manual Intervention"
   },
   "integrationChange": {
    "type": "string",
    "description": "Integration Change"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "userSystem": {
    "type": "string",
    "description": "User/System"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "previousValue": {
    "type": "string",
    "description": "Previous Value"
   },
   "newValue": {
    "type": "integer",
    "description": "New Value"
   },
   "reference": {
    "type": "string",
    "description": "Reference"
   },
   "result": {
    "type": "string",
    "description": "Result"
   },
   "environment": {
    "type": "string",
    "description": "Environment"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "partnerDisputes": {
    "type": "string",
    "description": "Partner disputes"
   },
   "compliance": {
    "type": "string",
    "description": "Compliance"
   },
   "technicalInvestigation": {
    "type": "string",
    "description": "Technical investigation"
   }
  }
 },
 "ChannelConnectionIntegrationManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Connection & Integration Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticvaiNative": {
    "type": "string",
    "description": "TICVAI Native"
   },
   "restApi": {
    "type": "string",
    "description": "REST API"
   },
   "webhook": {
    "type": "string",
    "description": "Webhook"
   },
   "otaAdapter": {
    "type": "string",
    "description": "OTA Adapter"
   },
   "resellerApi": {
    "type": "string",
    "description": "Reseller API"
   },
   "partnerApi": {
    "type": "string",
    "description": "Partner API"
   },
   "middleware": {
    "type": "string",
    "description": "Middleware"
   },
   "fileSftpWhereRequired": {
    "type": "boolean",
    "description": "File/SFTP where required"
   },
   "customConnector": {
    "type": "string",
    "description": "Custom Connector"
   },
   "connectorName": {
    "type": "string",
    "description": "Connector Name"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "environment": {
    "type": "string",
    "description": "Environment"
   },
   "endpoint": {
    "type": "string",
    "description": "Endpoint"
   },
   "apiVersion": {
    "type": "string",
    "description": "API Version"
   },
   "authenticationType": {
    "type": "string",
    "description": "Authentication Type"
   },
   "credentialsReference": {
    "type": "string",
    "description": "Credentials reference"
   },
   "certificate": {
    "type": "string",
    "description": "Certificate"
   },
   "timeout": {
    "type": "string",
    "description": "Timeout"
   },
   "rateLimit": {
    "type": "integer",
    "description": "Rate Limit"
   },
   "ipRestrictions": {
    "type": "string",
    "description": "IP Restrictions"
   },
   "connectionStatus": {
    "type": "string",
    "description": "Connection Status"
   },
   "oauth": {
    "type": "string",
    "description": "OAuth"
   },
   "apiKey": {
    "type": "string",
    "description": "API Key"
   },
   "clientCredentials": {
    "type": "string",
    "description": "Client Credentials"
   },
   "certificates": {
    "type": "string",
    "description": "Certificates"
   },
   "signedRequests": {
    "type": "string",
    "description": "Signed Requests"
   },
   "testAuthentication": {
    "type": "string",
    "description": "Test Authentication"
   },
   "testConnectivity": {
    "type": "string",
    "description": "Test Connectivity"
   },
   "testProduct": {
    "type": "string",
    "description": "Test Product"
   },
   "testPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Test Price"
   },
   "testAvailability": {
    "type": "string",
    "description": "Test Availability"
   },
   "testOrder": {
    "type": "string",
    "description": "Test Order"
   },
   "testCancellationWhereSupported": {
    "type": "string",
    "description": "Test Cancellation where supported"
   },
   "thisScreenManagesChannelConnectivity": {
    "type": "string",
    "description": "This screen manages channel connectivity"
   }
  }
 },
 "ChannelExceptionsIncidentsRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Exceptions, Incidents & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "connectionFailure": {
    "type": "string",
    "description": "Connection Failure"
   },
   "authenticationFailure": {
    "type": "string",
    "description": "Authentication Failure"
   },
   "productSyncFailure": {
    "type": "string",
    "description": "Product Sync Failure"
   },
   "pricingMismatch": {
    "type": "string",
    "description": "Pricing Mismatch"
   },
   "inventoryMismatch": {
    "type": "string",
    "description": "Inventory Mismatch"
   },
   "orderFailure": {
    "type": "string",
    "description": "Order Failure"
   },
   "paymentError": {
    "type": "string",
    "description": "Payment Error"
   },
   "timeout": {
    "type": "string",
    "description": "Timeout"
   },
   "cancellationFailure": {
    "type": "string",
    "description": "Cancellation Failure"
   },
   "fulfillmentFailure": {
    "type": "string",
    "description": "Fulfillment Failure"
   },
   "rateLimit": {
    "type": "integer",
    "description": "Rate Limit"
   },
   "partnerError": {
    "type": "string",
    "description": "Partner Error"
   },
   "incidentId": {
    "type": "string",
    "description": "Incident ID"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "severity": {
    "type": "string",
    "description": "Severity"
   },
   "errorType": {
    "type": "string",
    "description": "Error Type"
   },
   "affectedProduct": {
    "type": "string",
    "description": "Affected Product"
   },
   "affectedEvent": {
    "type": "string",
    "description": "Affected Event"
   },
   "transactionsAffected": {
    "type": "string",
    "description": "Transactions Affected"
   },
   "businessImpact": {
    "type": "string",
    "description": "Business Impact"
   },
   "firstDetected": {
    "type": "string",
    "description": "First Detected"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "currentStatus": {
    "type": "string",
    "description": "Current Status"
   },
   "reSync": {
    "type": "string",
    "description": "Re-sync"
   },
   "reprocess": {
    "type": "string",
    "description": "Reprocess"
   },
   "switchToManual": {
    "type": "string",
    "description": "Switch to Manual"
   },
   "errorCode": {
    "type": "string",
    "description": "Error Code"
   },
   "apiRequestReference": {
    "type": "string",
    "description": "API Request Reference"
   },
   "response": {
    "type": "string",
    "description": "Response"
   },
   "correlationId": {
    "type": "string",
    "description": "Correlation ID"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
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
    "description": "Channel Owner"
   },
   "partnerOwner": {
    "type": "string",
    "description": "Partner Owner"
   },
   "commercialAgreementReference": {
    "type": "string",
    "description": "Commercial Agreement Reference"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "transactionLimits": {
    "type": "string",
    "description": "Transaction Limits"
   },
   "rateLimits": {
    "type": "number",
    "description": "Rate Limits"
   },
   "contractDates": {
    "type": "string",
    "description": "Contract Dates"
   },
   "renewalDate": {
    "type": "string",
    "format": "date-time",
    "description": "Renewal Date"
   },
   "supportContacts": {
    "type": "string",
    "description": "Support Contacts"
   },
   "escalationContacts": {
    "type": "string",
    "description": "Escalation Contacts"
   },
   "availability": {
    "type": "number",
    "description": "Availability %"
   },
   "apiResponseTime": {
    "type": "string",
    "format": "date-time",
    "description": "API Response Time"
   },
   "transactionSuccess": {
    "type": "number",
    "description": "Transaction Success %"
   },
   "errorRate": {
    "type": "number",
    "description": "Error Rate"
   },
   "incidentResolutionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Incident Resolution Time"
   },
   "availability999": {
    "type": "number",
    "description": "Availability: 99.9%"
   },
   "actual9972": {
    "type": "number",
    "description": "Actual: 99.72%"
   },
   "statusSlaBreach": {
    "type": "string",
    "description": "Status: SLA Breach"
   },
   "expiredAgreement": {
    "type": "integer",
    "description": "Expired agreement"
   },
   "expiredCertificate": {
    "type": "integer",
    "description": "Expired certificate"
   },
   "expiringApiCredentials": {
    "type": "string",
    "description": "Expiring API credentials"
   },
   "missingOwner": {
    "type": "string",
    "description": "Missing owner"
   },
   "unapprovedProductionIntegration": {
    "type": "string",
    "description": "Unapproved production integration"
   },
   "slaBreach": {
    "type": "string",
    "description": "SLA breach"
   },
   "excessiveTransactionFailures": {
    "type": "string",
    "description": "Excessive transaction failures"
   },
   "placeUnderReview": {
    "type": "string",
    "description": "Place Under Review"
   },
   "restrict": {
    "type": "string",
    "description": "Restrict"
   },
   "reactivate": {
    "type": "string",
    "description": "Reactivate"
   },
   "resellerOtaDistributionArea": {
    "type": "string",
    "description": "Reseller / OTA Distribution area"
   }
  }
 },
 "ChannelOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
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
    "type": "string",
    "description": "Transactions Today"
   },
   "grossSales": {
    "type": "integer",
    "description": "Gross Sales"
   },
   "productsAvailable": {
    "type": "string",
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
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "type": {
    "type": "string",
    "description": "Type"
   },
   "venueScope": {
    "type": "string",
    "description": "Venue/Scope"
   },
   "connectionStatus": {
    "type": "string",
    "description": "Connection Status"
   },
   "lastSync": {
    "type": "string",
    "format": "date-time",
    "description": "Last Sync"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "transactions": {
    "type": "string",
    "description": "Transactions"
   },
   "salesValue": {
    "type": "string",
    "description": "Sales Value"
   },
   "inventoryStatus": {
    "type": "string",
    "description": "Inventory Status"
   },
   "pricingStatus": {
    "type": "string",
    "description": "Pricing Status"
   },
   "errorCount": {
    "type": "integer",
    "description": "Error Count"
   },
   "healthScore": {
    "type": "number",
    "description": "Health Score"
   },
   "otaTiqtripInventorySynchronized1041": {
    "type": "string",
    "description": "OTA-TiqTrip inventory synchronized — 10:41"
   },
   "forceSync": {
    "type": "string",
    "description": "Force Sync"
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
    "type": "integer",
    "description": "Gross Sales"
   },
   "netSales": {
    "type": "integer",
    "description": "Net Sales"
   },
   "transactions": {
    "type": "integer",
    "description": "Transactions"
   },
   "ticketsSold": {
    "type": "string",
    "description": "Tickets Sold"
   },
   "averageOrderValue": {
    "type": "number",
    "description": "Average Order Value"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate"
   },
   "capacityUtilization": {
    "type": "integer",
    "description": "Capacity Utilization"
   },
   "revenuePerAvailableUnit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Available Unit"
   },
   "fees": {
    "type": "integer",
    "description": "Fees"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "costOfSaleWhereAvailable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost of Sale where available"
   },
   "allocation": {
    "type": "string",
    "description": "Allocation"
   },
   "sold": {
    "type": "string",
    "description": "Sold"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "settlement": {
    "type": "string",
    "description": "Settlement"
   },
   "growth": {
    "type": "string",
    "description": "Growth"
   }
  }
 },
 "ProductPriceAvailabilitySynchronizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product, Price & Availability Synchronization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productDescription": {
    "type": "string",
    "description": "Product Description"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "fees": {
    "type": "string",
    "description": "Fees"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "restrictions": {
    "type": "string",
    "description": "Restrictions"
   },
   "salesStatus": {
    "type": "string",
    "description": "Sales Status"
   },
   "channelTicvai": {
    "type": "string",
    "description": "Channel → TICVAI"
   },
   "realTime": {
    "type": "string",
    "format": "date-time",
    "description": "Real Time"
   },
   "nearRealTime": {
    "type": "string",
    "format": "date-time",
    "description": "Near Real Time"
   },
   "scheduled": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled"
   },
   "manual": {
    "type": "string",
    "description": "Manual"
   },
   "eventTriggered": {
    "type": "string",
    "description": "Event Triggered"
   },
   "lastSuccessfulSync": {
    "type": "string",
    "format": "date-time",
    "description": "Last Successful Sync"
   },
   "nextSync": {
    "type": "string",
    "format": "date-time",
    "description": "Next Sync"
   },
   "recordsProcessed": {
    "type": "string",
    "description": "Records Processed"
   },
   "successful": {
    "type": "string",
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
    "type": "string",
    "description": "Warning"
   },
   "duration": {
    "type": "string",
    "format": "date-time",
    "description": "Duration"
   },
   "reprocess": {
    "type": "string",
    "description": "Reprocess"
   }
  }
 },
 "RealTimeChannelAvailabilityInventoryMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Real-Time Channel Availability & Inventory Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ctBA": {
    "type": "string",
    "description": "ct B A"
   },
   "dD": {
    "type": "string",
    "description": "d d"
   },
   "available": {
    "type": "string",
    "description": "Available"
   },
   "lowAvailability": {
    "type": "string",
    "description": "Low Availability"
   },
   "soldOut": {
    "type": "string",
    "description": "Sold Out"
   },
   "closed": {
    "type": "integer",
    "description": "Closed"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "notAssigned": {
    "type": "string",
    "description": "Not Assigned"
   },
   "allocated": {
    "type": "string",
    "description": "Allocated"
   },
   "sold": {
    "type": "string",
    "description": "Sold"
   },
   "held": {
    "type": "string",
    "description": "Held"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization %"
   },
   "salesVelocity": {
    "type": "string",
    "description": "Sales Velocity"
   },
   "forecastedSellOut": {
    "type": "string",
    "description": "Forecasted Sell-Out"
   },
   "againstTheSeatMapCapacityPool": {
    "type": "integer",
    "description": "against the seat map/capacity pool"
   }
  }
 }
}
```
