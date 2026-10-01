# WS07 — Access Control board 7

**10 screens · 15 operations · 24 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ACCESS_POINT_CONFIGURE, ACCESS_VALIDATE, INCIDENT_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-204` | Offline & Edge Operations Command Center | listDetail | 1 | 0 | — |
| `BO-205` | Edge Node & Local Processing Configuration | configEditor | 1 | 0 | — |
| `BO-206` | Offline Validation Policy Builder | listDetail | 1 | 0 | — |
| `BO-207` | Edge Package & Data Distribution | configEditor | 3 | 0 | — |
| `BO-208` | Offline Credential & Revocation Cache | listDetail | 3 | 1 | — |
| `BO-209` | Offline Entitlement & Usage Ledger | listDetail | 1 | 0 | — |
| `BO-210` | Connectivity Failure & Degraded Mode Policy | listDetail | 4 | 0 | — |
| `BO-211` | Reconnection, Synchronization & Conflict Resolution | listDetail | 1 | 0 | — |
| `BO-212` | Offline Simulation & Resilience Testing | listDetail | 1 | 0 | — |
| `BO-213` | Edge Security, Audit & Deployment | listDetail | 2 | 1 | — |

## Thin screens in this batch

**BO-206, BO-208, BO-209, BO-210, BO-211, BO-212 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-204",
  "name": "Offline & Edge Operations Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.1",
   "page": 86
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/offline-edge-operations-command-center-bo-204",
   "component": "apps/venue-management-web/src/routes/access-venue/OfflineEdgeOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-205",
    "BO-206",
    "BO-207",
    "BO-208",
    "BO-209",
    "BO-210",
    "BO-211",
    "BO-212",
    "BO-213"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "provenance": "derived — BO-100 declares entryState.params  and BO-204 holds none of them. The edge carries nothing: BO-204 is opened from BO-100, so this edge is the way back and BO-100 keeps its own state"
    },
    {
     "to": "BO-205",
     "trigger": "Works in Edge Node & Local Processing Configuration",
     "provenance": "flow F117 step 1→2",
     "operation": "listOfflineEdge"
    },
    {
     "to": "BO-206",
     "trigger": "Works in Offline Validation Policy Builder",
     "provenance": "flow F117 step 3→4",
     "operation": "listOfflineEdge"
    },
    {
     "to": "BO-207",
     "trigger": "Works in Edge Package & Data Distribution",
     "provenance": "flow F117 step 5→6",
     "operation": "listOfflineEdge"
    },
    {
     "to": "BO-208",
     "trigger": "Works in Offline Credential & Revocation Cache",
     "provenance": "flow F117 step 7→8",
     "operation": "listOfflineEdge"
    },
    {
     "to": "BO-209",
     "trigger": "Works in Offline Entitlement & Usage Ledger",
     "provenance": "flow F117 step 9→10",
     "operation": "listOfflineEdge"
    },
    {
     "to": "BO-210",
     "trigger": "Works in Connectivity Failure & Degraded Mode Policy",
     "provenance": "flow F117 step 11→12",
     "operation": "listOfflineEdge"
    },
    {
     "to": "BO-211",
     "trigger": "Works in Reconnection, Synchronization & Conflict Resolution",
     "provenance": "flow F117 step 13→14",
     "operation": "listOfflineEdge"
    },
    {
     "to": "BO-212",
     "trigger": "Works in Offline Simulation & Resilience Testing",
     "provenance": "flow F117 step 15→16",
     "operation": "listOfflineEdge"
    },
    {
     "to": "BO-213",
     "trigger": "Works in Edge Security, Audit & Deployment",
     "provenance": "flow F117 step 17→18",
     "operation": "listOfflineEdge"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can immediately determine whether each venue, gate and device is capable of safely operating offline.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a real-time overview of offline readiness across the entire access-control estate.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Offline-Ready Devices",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.offlineReadyDevices",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Currently Online",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.currentlyOnline",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Currently Offline",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.currentlyOffline",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Devices in Degraded Mode",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.devicesInDegradedMode",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Edge Nodes Online",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.edgeNodesOnline",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Packages Current",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.packagesCurrent",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Packages Expiring",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.packagesExpiring",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Pending Offline Transactions",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.pendingOfflineTransactions",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Offline Security Alerts",
       "bindsTo": "OfflineEdgeOperationsCommandCenterViewSummary.offlineSecurityAlerts",
       "operation": "listOfflineEdge",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every offline edge operations",
       "columns": [
        "Sync Conflicts"
       ],
       "bindsTo": "OfflineEdgeOperationsCommandCenterView",
       "operation": "listOfflineEdge",
       "provenance": "pack Access Control Module_Reference.pdf, page 86 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected offline edge operations",
       "bindsTo": "OfflineEdgeOperationsCommandCenterView",
       "columns": [
        "Sync Conflicts"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Venue Readiness”, “Checks”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 86 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline edge operations list.",
   "error": "Could not load. Names which read failed and leaves the offline edge operations untouched.",
   "emptyFirstRun": "No offline edge operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline edge operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOfflineEdge",
    "contract": "access",
    "purpose": "Offline & Edge Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflineEdgeOperationsCommandCenterViewSummary.offlineReadyDevices",
    "OfflineEdgeOperationsCommandCenterViewSummary.currentlyOnline",
    "OfflineEdgeOperationsCommandCenterViewSummary.currentlyOffline",
    "OfflineEdgeOperationsCommandCenterViewSummary.devicesInDegradedMode",
    "OfflineEdgeOperationsCommandCenterViewSummary.edgeNodesOnline",
    "OfflineEdgeOperationsCommandCenterViewSummary.packagesCurrent"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-204",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-204"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 86. 9 of 10 labels bound to a contract property; 10 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-205",
  "name": "Edge Node & Local Processing Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.2",
   "page": 87
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/edge-node-local-processing-configuration-bo-205",
   "component": "apps/venue-management-web/src/routes/access-venue/EdgeNodeLocalProcessingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-204",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F117 step 2→3",
     "operation": "setEdgeNodeLocal"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can define which edge component is responsible for local access decisions for every deployed device.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Fields) and no display directory — it is settings, not a population",
  "purpose": "Configure where local access decisions are processed when central services cannot be reached.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Edge Node ID",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Network",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Device Group",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Processing Mode",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "Storage allocation",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "redundancy",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "last heartbeat",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      },
      {
       "kind": "selectField",
       "label": "software version",
       "provenance": "pack Access Control Module_Reference.pdf, page 87 §Fields"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setEdgeNodeLocal"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The edge node local configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the edge node local untouched.",
   "emptyFirstRun": "No edge node local configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEdgeNodeLocal",
    "contract": "access",
    "purpose": "Edge Node & Local Processing Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-205",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-205"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 87. 0 of 0 labels bound to a contract property; 10 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-206",
  "name": "Offline Validation Policy Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.3",
   "page": 88
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/offline-validation-policy-builder-bo-206",
   "component": "apps/venue-management-web/src/routes/access-venue/OfflineValidationPolicyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-204",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F117 step 4→5",
     "operation": "setOfflinePolicy"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators explicitly control which admission decisions may be performed without central connectivity.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define exactly which access checks are allowed to run locally. The matrix identifies key offline criteria including eligible media, eligible site, eligible time, ticket validity and eligible access mode.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 88"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 88"
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
       "label": "Save changes",
       "provenance": "contract operation setOfflinePolicy"
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
       "impliedBy": "setOfflinePolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline validation policy list.",
   "error": "Could not load. Names which read failed and leaves the offline validation policy untouched.",
   "emptyFirstRun": "No offline validation policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline validation policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setOfflinePolicy",
    "contract": "tenancy",
    "purpose": "setOfflinePolicy",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-206",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-206"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 88. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-207",
  "name": "Edge Package & Data Distribution",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.4",
   "page": 89
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/edge-package-data-distribution-bo-207",
   "component": "apps/venue-management-web/src/routes/access-venue/EdgePackageDataDistribution.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-204",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F117 step 6→7",
     "operation": "listEdgePackageData"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Only approved, intact and authorized edge packages can become active on access-control devices.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Access Configuration; Credential Configuration) and no display directory — it is settings, not a population",
  "purpose": "Define what configuration and operational data is securely distributed to edge devices.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "venues",
       "provenance": "pack Access Control Module_Reference.pdf, page 89 §Access Configuration"
      },
      {
       "kind": "selectField",
       "label": "zones",
       "provenance": "pack Access Control Module_Reference.pdf, page 89 §Access Configuration"
      },
      {
       "kind": "selectField",
       "label": "gates",
       "provenance": "pack Access Control Module_Reference.pdf, page 89 §Access Configuration"
      },
      {
       "kind": "selectField",
       "label": "access rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 89 §Access Configuration"
      },
      {
       "kind": "selectField",
       "label": "calendars",
       "provenance": "pack Access Control Module_Reference.pdf, page 89 §Access Configuration"
      },
      {
       "kind": "selectField",
       "label": "media profiles",
       "provenance": "pack Access Control Module_Reference.pdf, page 89 §Credential Configuration"
      },
      {
       "kind": "selectField",
       "label": "verification profiles",
       "provenance": "pack Access Control Module_Reference.pdf, page 89 §Credential Configuration"
      },
      {
       "kind": "selectField",
       "label": "entitlement definitions",
       "provenance": "pack Access Control Module_Reference.pdf, page 89 §Credential Configuration"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "operation": "publishHardwareDeployment",
       "notes": "**Names the configuration version, the target (pilot, selected gates, device group or venue) and the devices that failed the compatibility test and will be skipped**, before it runs.",
       "provenance": "contract access.yaml POST /hardware-deployments (authored: required by check-screens)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The edge package data configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the edge package data untouched.",
   "emptyFirstRun": "No edge package data configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEdgePackageData",
    "contract": "access",
    "purpose": "Edge Package & Data Distribution",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "The access package an edge node holds, with its version",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "publishHardwareDeployment",
    "contract": "access",
    "purpose": "Publish a new offline package to the edge nodes: deploys the access configuration version, which devices pick up at their next package refresh (replaces publishBundle, a catalogue bundle, bound in error on 29 September)",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-207",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-207"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 89. 0 of 0 labels bound to a contract property; 8 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-208",
  "name": "Offline Credential & Revocation Cache",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.5",
   "page": 90
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/offline-credential-revocation-cache-bo-208",
   "component": "apps/venue-management-web/src/routes/access-venue/OfflineCredentialRevocationCache.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-204",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F117 step 8→9",
     "operation": "listOfflineCredentialRevocation"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Offline devices have a controlled and measurable mechanism for receiving credential invalidations and security changes.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage the local information required to reject credentials that should no longer be usable. This is especially important because Board 3 requires refunded, cancelled, transferred, exchanged, upgraded and reissued credentials to be invalidated.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 90"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 90"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listOfflineCredentialRevocation",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save offline policy",
       "operation": "setOfflinePolicy",
       "permission": "TENANT_CONFIGURE",
       "notes": "Board 5 of the client's POS set, and **one of only two things in 36 board screens the package could not do.** ADR-0013 makes the POS local-first and nothing configured the policy.",
       "provenance": "contract tenancy.yaml PUT /offline-policy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline credential revocation list.",
   "error": "Could not load. Names which read failed and leaves the offline credential revocation untouched.",
   "emptyFirstRun": "No offline credential revocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline credential revocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGateOfflinePolicy",
    "purpose": "Save the gate offline validation, revocation cache and degraded-mode policy (writers pass, 29 September)",
    "contract": "access"
   },
   {
    "operationId": "listOfflineCredentialRevocation",
    "contract": "access",
    "purpose": "Offline Credential & Revocation Cache",
    "trigger": "onLoad"
   },
   {
    "operationId": "setOfflinePolicy",
    "contract": "tenancy",
    "purpose": "What a workstation may do with no network, and for how long",
    "trigger": "onAction",
    "invalidates": [
     "listOfflineCredentialRevocation"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflineCredentialRevocationCacheView.triggerEvents"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-208",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-208"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 90. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetOfflinePolicy",
    "component": "modal",
    "trigger": "Save offline policy",
    "body": "**Collects what `setOfflinePolicy` sends before it is called.** Required: `scopePath`. Optional: `id`, `maxOfflineHours`, `allowedOffline`, `offlineValueCeiling`, `offlineTransactionCeiling`, `onCeilingBreach`, `requiresManagerToExtend`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "OfflinePolicy",
    "confirm": {
     "label": "Save offline policy",
     "operation": "setOfflinePolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "scopePath",
      "id",
      "maxOfflineHours",
      "allowedOffline",
      "offlineValueCeiling",
      "offlineTransactionCeiling",
      "onCeilingBreach",
      "requiresManagerToExtend"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /offline-policy"
   }
  ],
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
  "id": "BO-209",
  "name": "Offline Entitlement & Usage Ledger",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.6",
   "page": 91
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/offline-entitlement-usage-ledger-bo-209",
   "component": "apps/venue-management-web/src/routes/access-venue/OfflineEntitlementUsageLedger.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-204",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F117 step 10→11",
     "operation": "listOfflineEntitlementUsage"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Offline usage is recorded locally and prevents repeated consumption within the available edge synchronization scope.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Track entitlement consumption while the central system is unavailable. This is necessary for tickets such as: 3 Fast Pass uses 1 park entry 1 meal 1 re-entry where usage can occur during an outage.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 91"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 91"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listOfflineEntitlementUsage",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline entitlement usage list.",
   "error": "Could not load. Names which read failed and leaves the offline entitlement usage untouched.",
   "emptyFirstRun": "No offline entitlement usage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline entitlement usage are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOfflineEntitlementUsage",
    "contract": "access",
    "purpose": "Offline Entitlement & Usage Ledger",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflineEntitlementUsageLedgerView.credential",
    "OfflineEntitlementUsageLedgerView.device"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-209",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-209"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 91. 0 of 0 labels bound to a contract property; 0 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-210",
  "name": "Connectivity Failure & Degraded Mode Policy",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.7",
   "page": 93
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/connectivity-failure-degraded-mode-policy-bo-210",
   "component": "apps/venue-management-web/src/routes/access-venue/ConnectivityFailureDegradedModePolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-204",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F117 step 12→13",
     "operation": "listConnectivityFailureDegraded"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Connectivity failures trigger predefined operating modes rather than unpredictable gate behavior.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how devices transition from normal online operation to offline/degraded operation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 93"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 93"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listConnectivityFailureDegraded",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setOfflinePolicy",
       "label": "Save offline policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setOfflinePolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The connectivity failure degraded list.",
   "error": "Could not load. Names which read failed and leaves the connectivity failure degraded untouched.",
   "emptyFirstRun": "No connectivity failure degraded yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the connectivity failure degraded are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGateOfflinePolicy",
    "purpose": "Save the gate offline validation, revocation cache and degraded-mode policy (writers pass, 29 September)",
    "contract": "access"
   },
   {
    "operationId": "listConnectivityFailureDegraded",
    "contract": "access",
    "purpose": "Connectivity Failure & Degraded Mode Policy",
    "trigger": "onLoad"
   },
   {
    "operationId": "setOfflinePolicy",
    "contract": "tenancy",
    "purpose": "Save what a device may do with no network, and for how long",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setConnectivityThresholds",
    "contract": "tenancy",
    "purpose": "Save when a device switches to degraded mode",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "preloaded": [
    "ConnectivityFailureDegradedModePolicyView.operatingModes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-210",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-210"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 93. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-211",
  "name": "Reconnection, Synchronization & Conflict Resolution",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.8",
   "page": 94
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/reconnection-synchronization-conflict-resolution-bo-211",
   "component": "apps/venue-management-web/src/routes/access-venue/ReconnectionSynchronizationConflictResolution.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-204",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F117 step 14→15",
     "operation": "listReconnectionSynchronizationConflict"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Offline events synchronize back to the central platform with deterministic reconciliation and a complete audit trail.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Synchronize everything that occurred offline when connectivity returns.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every reconnection synchronization conflict",
       "bindsTo": "ReconnectionSynchronizationConflictResolutionView",
       "operation": "listReconnectionSynchronizationConflict",
       "provenance": "pack Access Control Module_Reference.pdf, page 94 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reconnection synchronization conflict",
       "bindsTo": "ReconnectionSynchronizationConflictResolutionView",
       "notes": "The pack groups this record's detail under its own headings: “Connectivity Restored”, “Authenticate”, “Upload Offline Transactions”, “Sequence Events”, “Reconcile Credential State”, “Reconcile Entitlements”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 94 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconnection synchronization conflict list.",
   "error": "Could not load. Names which read failed and leaves the reconnection synchronization conflict untouched.",
   "emptyFirstRun": "No reconnection synchronization conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reconnection synchronization conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReconnectionSynchronizationConflict",
    "contract": "access",
    "purpose": "Reconnection, Synchronization & Conflict Resolution",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-211",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-211"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 94. 6 of 6 labels bound to a contract property; 7 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-212",
  "name": "Offline Simulation & Resilience Testing",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.9",
   "page": 95
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/offline-simulation-resilience-testing-bo-212",
   "component": "apps/venue-management-web/src/routes/access-venue/OfflineSimulationResilienceTesting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-204",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F117 step 16→17",
     "operation": "simulateOfflineResilienceTesting"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow venues to prove that their access environment will survive outages before opening to guests.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 95"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 95"
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
       "label": "Run simulation",
       "provenance": "contract operation simulateOfflineResilienceTesting"
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
       "impliedBy": "simulateOfflineResilienceTesting"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline simulation resilience list.",
   "error": "Could not load. Names which read failed and leaves the offline simulation resilience untouched.",
   "emptyFirstRun": "No offline simulation resilience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline simulation resilience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateOfflineResilienceTesting",
    "contract": "access",
    "purpose": "Offline Simulation & Resilience Testing",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-212",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-212"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 95. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-213",
  "name": "Edge Security, Audit & Deployment",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "7",
   "number": "7.10",
   "page": 96
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/edge-security-audit-deployment-bo-213",
   "component": "apps/venue-management-web/src/routes/access-venue/EdgeSecurityAuditDeployment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-204"
   ],
   "exitTo": [
    "BO-204"
   ],
   "inferred": false,
   "notes": "**Reached from BO-204, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "Offline and edge configurations are version-controlled, secured, approved, deployable and fully auditable. Board 7 — Final 10-Screen Structure # Backend Screen Main Responsibility 7.1 Offline & Edge Operations Command Center Estate-wide offline readiness 7.2 Edge Node & Local Processing Configuration Venue/device edge architecture 7.3 Offline Validation Policy Builder Determine which rules work offline 7.4 Edge Package & Data Distribution Secure local configuration packages 7.5 Offline Credential & Revocation Cache Local invalidation/security state 7.6 Offline Entitlement & Usage Ledger Track",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Govern the complete offline/edge environment.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Package signatures",
       "bindsTo": "EdgeSecurityAuditDeploymentViewSummary.packageSignatures",
       "operation": "listEdgeSecurityDeployment",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Authorized devices",
       "bindsTo": "EdgeSecurityAuditDeploymentViewSummary.authorizedDevices",
       "operation": "listEdgeSecurityDeployment",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Revoked devices",
       "bindsTo": "EdgeSecurityAuditDeploymentViewSummary.revokedDevices",
       "operation": "listEdgeSecurityDeployment",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Failed package validation",
       "bindsTo": "EdgeSecurityAuditDeploymentViewSummary.failedPackageValidation",
       "operation": "listEdgeSecurityDeployment",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "unauthorized connection attempts",
       "bindsTo": "EdgeSecurityAuditDeploymentViewSummary.unauthorizedConnectionAttempts",
       "operation": "listEdgeSecurityDeployment",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "configuration changes",
       "bindsTo": "EdgeSecurityAuditDeploymentViewSummary.configurationChanges",
       "operation": "listEdgeSecurityDeployment",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every edge security audit",
       "columns": [
        "Edge certificates/credentials"
       ],
       "bindsTo": "EdgeSecurityAuditDeploymentView",
       "operation": "listEdgeSecurityDeployment",
       "provenance": "pack Access Control Module_Reference.pdf, page 96 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected edge security audit",
       "bindsTo": "EdgeSecurityAuditDeploymentView",
       "columns": [
        "Edge certificates/credentials"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Draft”, “Deployment Scope”, “Current Production”, “Scheduled”, “Rollback”, “FORCE ONLINE-ONLY”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 96 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save security alert",
       "operation": "updateSecurityAlert",
       "permission": "INCIDENT_MANAGE",
       "notes": "**The action on the security command centres** (BO-244, BO-246, BO-248, BO-213, BO-253): moves one alert raised by the detection jobs.",
       "provenance": "contract access.yaml POST /security-alerts/{alertId}/status"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The edge security audit list.",
   "error": "Could not load. Names which read failed and leaves the edge security audit untouched.",
   "emptyFirstRun": "No edge security audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the edge security audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEdgeSecurityDeployment",
    "contract": "access",
    "purpose": "Edge Security, Audit & Deployment",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateSecurityAlert",
    "contract": "access",
    "purpose": "Acknowledge, resolve or dismiss a security alert",
    "trigger": "onAction",
    "invalidates": [
     "listEdgeSecurityDeployment"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Edge certificates/credentials",
    "EdgeSecurityAuditDeploymentViewSummary.packageSignatures",
    "EdgeSecurityAuditDeploymentViewSummary.authorizedDevices",
    "EdgeSecurityAuditDeploymentViewSummary.revokedDevices",
    "EdgeSecurityAuditDeploymentViewSummary.failedPackageValidation",
    "EdgeSecurityAuditDeploymentViewSummary.unauthorizedConnectionAttempts"
   ],
   "params": [
    {
     "name": "alertId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-213",
   "workshopBoard": "wireframes/WS24 Access Control Board 7.dc.html#bo-213"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 96. 6 of 7 labels bound to a contract property; 7 of 76 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formUpdateSecurityAlert",
    "component": "modal",
    "trigger": "Save security alert",
    "body": "**Collects what `updateSecurityAlert` sends before it is called.** Required: `status`. Optional: `note`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save security alert",
     "operation": "updateSecurityAlert"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "note",
      "securityInvestigationId"
     ]
    },
    "provenance": "contract access.yaml POST /security-alerts/{alertId}/status"
   }
  ],
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
 "getOfflinePackage": {
  "method": "GET",
  "path": "/access/offline-package",
  "contract": "access",
  "summary": "Entitlement and rule set for offline validation",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": "sinceVersion",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "validFrom",
    "in": "query",
    "required": true
   },
   {
    "name": "validTo",
    "in": "query",
    "required": true
   },
   {
    "name": "If-None-Match",
    "in": "header",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OfflinePackage"
 },
 "listConnectivityFailureDegraded": {
  "method": "GET",
  "path": "/connectivity-failure-degraded",
  "contract": "access",
  "summary": "Connectivity Failure & Degraded Mode Policy",
  "permission": "SCOPE_VIEW",
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
  "responds": "ConnectivityFailureDegradedModePolicyView"
 },
 "listEdgePackageData": {
  "method": "GET",
  "path": "/edge-package-data",
  "contract": "access",
  "summary": "Edge Package & Data Distribution",
  "permission": "SCOPE_VIEW",
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
  "requestBody": null,
  "responds": "Page"
 },
 "listEdgeSecurityDeployment": {
  "method": "GET",
  "path": "/edge-security-deployment",
  "contract": "access",
  "summary": "Edge Security, Audit & Deployment",
  "permission": "SCOPE_VIEW",
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
  "requestBody": null,
  "responds": "Page"
 },
 "listOfflineCredentialRevocation": {
  "method": "GET",
  "path": "/offline-credential-revocation",
  "contract": "access",
  "summary": "Offline Credential & Revocation Cache",
  "permission": "SCOPE_VIEW",
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
  "responds": "OfflineCredentialRevocationCacheView"
 },
 "listOfflineEdge": {
  "method": "GET",
  "path": "/offline-edge",
  "contract": "access",
  "summary": "Offline & Edge Operations Command Center",
  "permission": "SCOPE_VIEW",
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
  "requestBody": null,
  "responds": "Page"
 },
 "listOfflineEntitlementUsage": {
  "method": "GET",
  "path": "/offline-entitlement-usage",
  "contract": "access",
  "summary": "Offline Entitlement & Usage Ledger",
  "permission": "SCOPE_VIEW",
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
  "requestBody": null,
  "responds": "Page"
 },
 "listReconnectionSynchronizationConflict": {
  "method": "GET",
  "path": "/reconnection-synchronization-conflict",
  "contract": "access",
  "summary": "Reconnection, Synchronization & Conflict Resolution",
  "permission": "SCOPE_VIEW",
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
  "requestBody": null,
  "responds": "Page"
 },
 "publishHardwareDeployment": {
  "method": "POST",
  "path": "/hardware-deployments",
  "contract": "access",
  "summary": "Deploy a gate configuration version",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "HardwareDeploymentInput",
  "responds": "HardwareDeploymentView"
 },
 "setConnectivityThresholds": {
  "method": "PUT",
  "path": "/connectivity-policy",
  "contract": "tenancy",
  "summary": "When a workstation decides it is offline, and when it is back",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "ConnectivityPolicy",
  "responds": "ConnectivityPolicy"
 },
 "setEdgeNodeLocal": {
  "method": "PUT",
  "path": "/edge-node-local",
  "contract": "access",
  "summary": "Edge Node & Local Processing Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "EdgeNodeLocalProcessingConfigurationInput",
  "responds": "EdgeNodeLocalProcessingConfigurationView"
 },
 "setGateOfflinePolicy": {
  "method": "PUT",
  "path": "/offline-policies",
  "contract": "access",
  "summary": "Set the offline policy of a venue",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "AccessOfflinePolicy",
  "responds": "AccessOfflinePolicy"
 },
 "setOfflinePolicy": {
  "method": "PUT",
  "path": "/offline-policy",
  "contract": "tenancy",
  "summary": "What a workstation may do with no network, and for how long",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "OfflinePolicy",
  "responds": "OfflinePolicy"
 },
 "simulateOfflineResilienceTesting": {
  "method": "PUT",
  "path": "/offline-resilience-testing",
  "contract": "access",
  "summary": "Offline Simulation & Resilience Testing",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "OfflineSimulationResilienceTestingInput",
  "responds": "OfflineSimulationResilienceTestingView"
 },
 "updateSecurityAlert": {
  "method": "POST",
  "path": "/security-alerts/{alertId}/status",
  "contract": "access",
  "summary": "Acknowledge, resolve or dismiss a security alert",
  "permission": "INCIDENT_MANAGE",
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
  "responds": "AccessSecurityAlert"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessAccreditationCredential": {
  "type": "object",
  "x-ticvai-persistence": "access.accreditation_credential",
  "x-ticvai-agreed": "29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer",
  "description": "**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.",
  "required": [
   "id",
   "holderId",
   "encodedIdentifier",
   "admits",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The accreditation credential's id (`credentialId` on the events)."
   },
   "holderId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "description": "printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."
   },
   "encodedIdentifier": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "What the gate reads from the credential. Never sent to webhook subscribers."
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "zoneIds": {
    "type": "array",
    "description": "The holder's effective zones, from the event (`effectiveZones`).",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "holderStatus": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked",
     "expired",
     "archived"
    ],
    "description": "The holder's status as last published; only `active` admits."
   },
   "admits": {
    "type": "boolean",
    "description": "False once the credential is replaced or the holder is not active."
   },
   "sourceChangedAt": {
    "type": "string",
    "format": "date-time",
    "description": "The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005), the accreditation programme's scope."
   }
  }
 },
 "AccessDynamicPolicy": {
  "type": "object",
  "x-ticvai-persistence": "access.dynamic_policy",
  "description": "One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.",
  "required": [
   "id",
   "scopePath",
   "name",
   "policyType",
   "conditionRule",
   "result",
   "status",
   "currentVersion"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The policyId"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node; where it applies further is access.policy_scope_assignment"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "policyType": {
    "type": "string",
    "enum": [
     "guestAttribute",
     "accreditation",
     "occupancy",
     "employee",
     "risk",
     "membership",
     "timeEvent"
    ]
   },
   "contextType": {
    "type": "string",
    "enum": [
     "date",
     "day",
     "time",
     "season",
     "event",
     "performance",
     "specialEvent",
     "holiday",
     "operatingCalendar",
     "occupancy",
     "attractionStatus"
    ],
    "nullable": true,
    "description": "Context/time/event policies (setContextTimeEvent)"
   },
   "identityType": {
    "type": "string",
    "enum": [
     "guest",
     "member",
     "annualPassHolder",
     "employee",
     "contractor",
     "vendor",
     "performer",
     "media",
     "vip",
     "security",
     "emergencyServices",
     "eventStaff"
    ],
    "nullable": true,
    "description": "Identity-based policies (listIdentityMembershipAccreditation)"
   },
   "conditionRule": {
    "$ref": "#/components/schemas/AdmissionRule",
    "description": "The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."
   },
   "result": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ]
   },
   "priority": {
    "type": "integer",
    "nullable": true
   },
   "allowedZoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "deniedZoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "monitorThresholdPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Occupancy policies. Percent at which the band becomes Monitor"
   },
   "restrictThresholdPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Occupancy policies. Percent at which the band becomes Restrict"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The grant expires automatically at validTo"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "inactive",
     "expired"
    ],
    "default": "draft"
   },
   "currentVersion": {
    "type": "integer",
    "minimum": 1,
    "description": "The version in force (access.dynamic_policy_version)"
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
 "AccessOfflinePolicy": {
  "type": "object",
  "x-ticvai-persistence": "access.offline_policy",
  "description": "The offline policy of one venue: what gates validate locally and for how long, how old the revocation cache may get, and how devices step down through degraded modes. Merges access.offline_validation_profile, access.revocation_cache_policy and access.degraded_mode_policy (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "venueId",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "maxOfflineDurationHours": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Hours a gate may validate offline"
   },
   "offlineChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialAuthenticity",
      "digitalSignature",
      "ticketId",
      "venue",
      "park",
      "zone",
      "visitDate",
      "timeWindow",
      "credentialStatusSnapshot",
      "ticketType",
      "guestCategory",
      "seat",
      "timeslot",
      "reservation",
      "entitlements",
      "reEntryPermissions",
      "validityPeriod"
     ]
    },
    "description": "What a gate may validate locally"
   },
   "afterThresholdBehavior": {
    "type": "string",
    "enum": [
     "continueRestrictedValidation",
     "operatorWarning",
     "supervisorMode",
     "failClosed",
     "fallback"
    ],
    "nullable": true
   },
   "revocationTriggerEvents": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "fraudLock",
      "refund",
      "cancellation",
      "lostCredential",
      "transfer",
      "reissue",
      "manualInvalidation"
     ]
    },
    "description": "Events that push an invalidation into the offline cache"
   },
   "revocationMaxAllowedAgeMinutes": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Maximum allowed revocation cache age"
   },
   "revocationStalenessAction": {
    "type": "string",
    "enum": [
     "continue",
     "continueWithWarning",
     "restrictedProductsOnly",
     "supervisorMode",
     "denySelectedCredentialClasses",
     "failClosed"
    ],
    "nullable": true,
    "description": "What devices do when the cache is older than the maximum allowed age"
   },
   "operatingModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "online",
      "degraded",
      "edgeMode",
      "localOffline",
      "unsafeExpired"
     ]
    },
    "description": "Operating modes a device moves through as connectivity fails"
   },
   "centralUnavailableAfterSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Seconds without central services before switching to edge mode"
   },
   "edgeUnavailableAfterSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Seconds without the venue edge before switching to local offline"
   },
   "automaticSwitch": {
    "type": "boolean",
    "default": true,
    "description": "Switch modes automatically without stopping guest flow"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
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
 "AccessSecurityAlert": {
  "type": "object",
  "x-ticvai-persistence": "access.security_alert",
  "description": "One access security or fraud alert - severity, what was detected, where and on which credential, identity or device - including biometric anomalies and edge security events (certificate, credential or package-signature failures, unauthorised connections, device authorisation and revocation). Merges the proposed access.security_alert and access.edge_security_event (declared 29 September, data-model close-out DM1). Created `open` by the detection jobs (fraud rules, sharing detection, biometric anomaly, edge security events) and moved by updateSecurityAlert; the lifecycle is states/access-security-alert.yaml (decided 29 September, writers pass).",
  "required": [
   "id",
   "scopePath",
   "category",
   "severity",
   "status",
   "detectedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The alertId / anomalyId the lists show"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
   },
   "category": {
    "type": "string",
    "enum": [
     "fraudSignal",
     "credentialSharing",
     "duplicateAccess",
     "blacklist",
     "biometric",
     "companion",
     "edgeSecurity"
    ]
   },
   "alertType": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "description": "The kind within the category - for fraudSignal the fraud rule's signal; for biometric one of faceChanged, reEnrollment, repeatedFaceMismatch, multipleFacesOneCredential, oneFaceMultipleCredentials, suspiciousEnrollmentFrequency, unusualVerificationFailures; for edgeSecurity one of certificateFailure, credentialFailure, packageSignatureFailure, unauthorizedConnection, deviceAuthorized, deviceRevoked"
   },
   "severity": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "description": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "e.g. Credential attempted simultaneous entry at two gates"
   },
   "fraudRuleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The access fraud rule that raised the alert, if one did"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The credential (the list's credentialId)"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity concerned, where known"
   },
   "zoneId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The gate (the list's gateId)"
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The device concerned, for device-sharing and edge events"
   },
   "faceReenrolmentAttemptId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Biometric alerts raised on a re-enrolment; the attempt holds the old and new references, operator, reason and review"
   },
   "faceProfileReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "Biometric alerts. Opaque Face Pass reference; never a template"
   },
   "securityInvestigationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "acknowledged",
     "resolved",
     "dismissed"
    ],
    "default": "open"
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time"
   },
   "acknowledgedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "acknowledgedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "ConnectivityFailureDegradedModePolicyView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Connectivity Failure & Degraded Mode Policy displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "operatingModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "online",
      "degraded",
      "edgeMode",
      "localOffline",
      "unsafeExpired"
     ]
    },
    "description": "Operating modes a device moves through as connectivity fails"
   },
   "centralUnavailableAfterSeconds": {
    "type": "integer",
    "description": "Seconds without central services before switching to edge mode"
   },
   "edgeUnavailableAfterSeconds": {
    "type": "integer",
    "description": "Seconds without the venue edge before switching to local offline"
   },
   "automaticSwitch": {
    "type": "boolean",
    "description": "Switch modes automatically without stopping guest flow"
   },
   "lastSyncAt": {
    "type": "string",
    "format": "date-time",
    "description": "Last successful synchronization"
   }
  },
  "required": [
   "venueId"
  ]
 },
 "ConnectivityPolicy": {
  "type": "object",
  "x-ticvai-persistence": "platform.connectivity_policy",
  "description": "Board 5 of the client's POS set, and the second of the two genuine gaps. **Nothing in the package held a threshold**, so a device that flips offline on one dropped packet and one that waits five minutes were the same product.\n**Going offline and coming back need different thresholds.** Symmetric ones produce a workstation that flaps — offline, online, offline — across a marginal connection, and each flap is a sync.\n**One per scope node, keyed on `scopePath`.** `id` is server-owned and absent where `getConnectivityPolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them, or a broken cross-field rule, is refused `400` with `errors[]` naming the field.\n",
  "required": [
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$",
    "description": "**The node these thresholds are for, and the key `setConnectivityThresholds` upserts on.** The body names its target here, because the path does not.\n"
   },
   "failuresBeforeOffline": {
    "type": "integer",
    "default": 3,
    "minimum": 1,
    "maximum": 10,
    "description": "**Consecutive, not cumulative.** One dropped request on a busy till is normal; three in a row is a network.\n"
   },
   "probeIntervalSeconds": {
    "type": "integer",
    "default": 15,
    "minimum": 5,
    "maximum": 300
   },
   "probeTimeoutMs": {
    "type": "integer",
    "default": 2000,
    "minimum": 500,
    "maximum": 30000,
    "description": "Shorter than `probeIntervalSeconds`, or the body is refused `400` (audit R129)."
   },
   "successesBeforeOnline": {
    "type": "integer",
    "default": 5,
    "minimum": 1,
    "maximum": 20,
    "description": "**Higher than the offline threshold, deliberately.** Coming back is where the cost is — a workstation that returns online and immediately fails has resynced for nothing. **Never below `failuresBeforeOffline`**, or the body is refused `400` (audit R129).\n"
   },
   "minimumStableSeconds": {
    "type": "integer",
    "default": 30,
    "minimum": 10,
    "maximum": 600,
    "description": "How long the connection must hold before the workstation trusts it. **This is what stops the flapping**, and it is the field a venue with poor wifi will actually tune.\n"
   },
   "autoSwitch": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "EdgeNodeLocalProcessingConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Edge Node & Local Processing Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "nodeType": {
    "type": "string",
    "enum": [
     "venueEdgeNode",
     "gateController",
     "turnstileLocalEngine",
     "handheldLocalEngine"
    ],
    "description": "Which edge component makes local access decisions"
   },
   "edgeNodeId": {
    "type": "string",
    "description": "Edge Node ID"
   },
   "tenantId": {
    "type": "string",
    "description": "Tenant"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "network": {
    "type": "string",
    "description": "Network"
   },
   "deviceGroup": {
    "type": "string",
    "description": "Device Group"
   },
   "processingMode": {
    "type": "string",
    "description": "Processing Mode"
   },
   "storageAllocation": {
    "type": "string",
    "description": "Storage allocation"
   },
   "redundancy": {
    "type": "string",
    "description": "redundancy"
   },
   "lastHeartbeat": {
    "type": "string",
    "format": "date-time",
    "description": "Last heartbeat, set by the node, read only"
   },
   "softwareVersion": {
    "type": "string",
    "description": "software version"
   },
   "securityStatus": {
    "type": "string",
    "description": "security status"
   }
  },
  "required": [
   "edgeNodeId",
   "venueId",
   "nodeType"
  ]
 },
 "EdgeNodeLocalProcessingConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Edge Node & Local Processing Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "nodeType": {
    "type": "string",
    "enum": [
     "venueEdgeNode",
     "gateController",
     "turnstileLocalEngine",
     "handheldLocalEngine"
    ],
    "description": "Which edge component makes local access decisions"
   },
   "edgeNodeId": {
    "type": "string",
    "description": "Edge Node ID"
   },
   "tenantId": {
    "type": "string",
    "description": "Tenant"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "network": {
    "type": "string",
    "description": "Network"
   },
   "deviceGroup": {
    "type": "string",
    "description": "Device Group"
   },
   "processingMode": {
    "type": "string",
    "description": "Processing Mode"
   },
   "storageAllocation": {
    "type": "string",
    "description": "Storage allocation"
   },
   "redundancy": {
    "type": "string",
    "description": "redundancy"
   },
   "lastHeartbeat": {
    "type": "string",
    "format": "date-time",
    "description": "Last heartbeat, set by the node, read only"
   },
   "softwareVersion": {
    "type": "string",
    "description": "software version"
   },
   "securityStatus": {
    "type": "string",
    "description": "security status"
   }
  },
  "required": [
   "edgeNodeId",
   "venueId",
   "nodeType"
  ]
 },
 "EdgePackageDataDistributionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Edge Package & Data Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "packageId": {
    "type": "string",
    "description": "Edge package identifier"
   },
   "contents": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "venues",
      "zones",
      "gates",
      "accessRules",
      "calendars",
      "mediaProfiles",
      "verificationProfiles",
      "entitlementDefinitions",
      "trustedVerificationMaterial",
      "revocationInformation",
      "credentialSecurityParameters",
      "reasonCodes",
      "gateResponses",
      "languages",
      "operatorPermissions"
     ]
    },
    "description": "Data sets included in this edge package"
   },
   "version": {
    "type": "string",
    "description": "Version (the pack shows 24.6, 89 | Pag e)"
   },
   "devices": {
    "type": "integer",
    "description": "Devices (the pack shows 84)"
   },
   "signatureValid": {
    "type": "boolean",
    "description": "✓ Signature valid"
   },
   "packageComplete": {
    "type": "boolean",
    "description": "✓ Package complete"
   },
   "versionValid": {
    "type": "boolean",
    "description": "✓ Version valid"
   },
   "deviceAuthorized": {
    "type": "boolean",
    "description": "✓ Device authorized"
   },
   "sizeBytes": {
    "type": "integer",
    "description": "Package size"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Valid from"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "Valid to"
   }
  },
  "required": [
   "packageId"
  ]
 },
 "EdgeSecurityAuditDeploymentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Edge Security, Audit & Deployment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "policyVersionId": {
    "type": "string",
    "description": "Edge policy version identifier"
   },
   "deploymentScope": {
    "type": "string",
    "enum": [
     "tenant",
     "venue",
     "park",
     "edgeCluster",
     "gateGroup",
     "deviceGroup",
     "individualDevice"
    ],
    "description": "Where this edge policy version deploys"
   },
   "version": {
    "type": "string",
    "description": "Version label, e.g. V4.8"
   },
   "stage": {
    "type": "string",
    "enum": [
     "draft",
     "validated",
     "securityTested",
     "offlineSimulated",
     "approved",
     "pilot",
     "published"
    ],
    "description": "Release stage"
   },
   "isProduction": {
    "type": "boolean",
    "description": "Currently in production"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled deployment time"
   }
  },
  "required": [
   "policyVersionId"
  ]
 },
 "EdgeSecurityAuditDeploymentViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "edgeCertificates": {
    "type": "integer",
    "description": "Edge certificates"
   },
   "edgeCredentials": {
    "type": "integer",
    "description": "Edge credentials"
   },
   "packageSignatures": {
    "type": "integer",
    "description": "Package signatures"
   },
   "authorizedDevices": {
    "type": "integer",
    "description": "Authorized devices"
   },
   "revokedDevices": {
    "type": "integer",
    "description": "Revoked devices"
   },
   "failedPackageValidation": {
    "type": "integer",
    "description": "Failed package validation"
   },
   "unauthorizedConnectionAttempts": {
    "type": "integer",
    "description": "unauthorized connection attempts"
   },
   "configurationChanges": {
    "type": "integer",
    "description": "configuration changes"
   },
   "offlineOverrideActivity": {
    "type": "integer",
    "description": "offline override activity"
   }
  }
 },
 "HardwareDeploymentInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "Deploy one gate configuration version to a target set (decided 29 September, VM close-out).",
  "required": [
   "id",
   "configurationVersion",
   "targetScope",
   "venueId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated deployment id"
   },
   "configurationVersion": {
    "type": "string",
    "description": "The access configuration version being deployed"
   },
   "targetScope": {
    "type": "string",
    "enum": [
     "pilot",
     "selectedGates",
     "deviceGroup",
     "venue"
    ]
   },
   "venueId": {
    "type": "string"
   },
   "gateIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Required for pilot and selectedGates"
   },
   "deviceGroupId": {
    "type": "string",
    "description": "Required for deviceGroup"
   },
   "runCompatibilityTestFirst": {
    "type": "boolean",
    "default": true,
    "description": "Devices that fail the compatibility test are skipped and named in the result"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "description": "Empty deploys now"
   }
  }
 },
 "HardwareDeploymentView": {
  "type": "object",
  "x-ticvai-persistence": "access.hardware_deployment",
  "description": "**One rollout of one gate configuration version to one target set** (decided 29 September, VM close-out). The lifecycle is the one `tenancy.ProfileDeployment` uses for configuration profiles, so a partial failure is visible and retried or rolled back, never an end state.",
  "required": [
   "id",
   "configurationVersion",
   "targetScope",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "configurationVersion": {
    "type": "string"
   },
   "targetScope": {
    "type": "string",
    "enum": [
     "pilot",
     "selectedGates",
     "deviceGroup",
     "venue"
    ]
   },
   "venueId": {
    "type": "string"
   },
   "gateIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "deviceGroupId": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "inProgress",
     "completed",
     "partiallyFailed",
     "rolledBack"
    ]
   },
   "devicesTargeted": {
    "type": "integer"
   },
   "devicesAcknowledged": {
    "type": "integer"
   },
   "failedDeviceIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Devices that failed the compatibility test or did not acknowledge"
   },
   "requestedByPrincipalId": {
    "type": "string"
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005). Written at venue scope"
   }
  }
 },
 "OfflineCredentialRevocationCacheView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline Credential & Revocation Cache displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "triggerEvents": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "fraudLock",
      "refund",
      "cancellation",
      "lostCredential",
      "transfer",
      "reissue",
      "manualInvalidation"
     ]
    },
    "description": "Events that push an invalidation into the offline cache"
   },
   "stalenessAction": {
    "type": "string",
    "enum": [
     "continue",
     "continueWithWarning",
     "restrictedProductsOnly",
     "supervisorMode",
     "denySelectedCredentialClasses",
     "failClosed"
    ],
    "description": "What devices do when the cache is older than the maximum allowed age"
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time",
    "description": "When the cache was last refreshed"
   },
   "ageSeconds": {
    "type": "integer",
    "description": "Current cache age"
   },
   "maxAllowedAgeMinutes": {
    "type": "integer",
    "description": "Maximum allowed cache age"
   }
  },
  "required": [
   "venueId"
  ]
 },
 "OfflineEdgeOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline & Edge Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "rulesCached": {
    "type": "boolean",
    "description": "✓ Rules cached"
   },
   "verificationMaterialCurrent": {
    "type": "boolean",
    "description": "✓ Verification material current"
   },
   "revocationDataCurrent": {
    "type": "boolean",
    "description": "✓ Revocation data current"
   },
   "credentialDefinitionsAvailable": {
    "type": "boolean",
    "description": "✓ Credential definitions available"
   },
   "deviceStorageHealthy": {
    "type": "boolean",
    "description": "✓ Device storage healthy"
   },
   "lastSynchronizationSuccessful": {
    "type": "boolean",
    "description": "✓ Last synchronization successful"
   },
   "venueName": {
    "type": "string",
    "description": "Venue name"
   },
   "devices": {
    "type": "integer",
    "description": "Devices at the venue"
   },
   "offlineReady": {
    "type": "integer",
    "description": "Devices ready to operate offline"
   },
   "readinessPercent": {
    "type": "number",
    "description": "Share of devices offline ready"
   },
   "packageStatus": {
    "type": "string",
    "enum": [
     "current",
     "expiring",
     "expired"
    ],
    "description": "Edge package status"
   },
   "pendingTransactions": {
    "type": "integer",
    "description": "Offline transactions not yet synchronized"
   },
   "readinessStatus": {
    "type": "string",
    "enum": [
     "ready",
     "warning",
     "notReady"
    ],
    "description": "Venue readiness"
   }
  },
  "required": [
   "venueId"
  ]
 },
 "OfflineEdgeOperationsCommandCenterViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "offlineReadyDevices": {
    "type": "integer",
    "description": "Offline-Ready Devices"
   },
   "currentlyOnline": {
    "type": "integer",
    "description": "Currently Online"
   },
   "currentlyOffline": {
    "type": "integer",
    "description": "Currently Offline"
   },
   "devicesInDegradedMode": {
    "type": "integer",
    "description": "Devices in Degraded Mode"
   },
   "edgeNodesOnline": {
    "type": "integer",
    "description": "Edge Nodes Online"
   },
   "packagesCurrent": {
    "type": "integer",
    "description": "Packages Current"
   },
   "packagesExpiring": {
    "type": "integer",
    "description": "Packages Expiring"
   },
   "pendingOfflineTransactions": {
    "type": "integer",
    "description": "Pending Offline Transactions"
   },
   "syncConflicts": {
    "type": "integer",
    "description": "Sync conflicts"
   },
   "offlineSecurityAlerts": {
    "type": "integer",
    "description": "Offline Security Alerts"
   }
  }
 },
 "OfflineEntitlementUsageLedgerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline Entitlement & Usage Ledger displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ledgerEntryId": {
    "type": "string",
    "description": "Ledger entry identifier"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "device": {
    "type": "string",
    "description": "Device"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "entitlement": {
    "type": "string",
    "description": "Entitlement"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "localSequence": {
    "type": "integer",
    "description": "Device-local sequence number"
   },
   "operator": {
    "type": "string",
    "description": "operator"
   },
   "decision": {
    "type": "string",
    "description": "decision"
   },
   "packageVersion": {
    "type": "string",
    "description": "package version"
   }
  },
  "required": [
   "ledgerEntryId"
  ]
 },
 "OfflinePackage": {
  "x-ticvai-persistence": "none — generated artefact in object storage",
  "type": "object",
  "required": [
   "etag",
   "generatedAt",
   "validFrom",
   "validTo",
   "accessPointId",
   "entitlements"
  ],
  "properties": {
   "etag": {
    "type": "string"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "entitlementsVersion": {
    "type": "integer",
    "description": "The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."
   },
   "policySetVersion": {
    "type": "string",
    "description": "**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."
   },
   "dynamicPolicies": {
    "type": "array",
    "description": "The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.",
    "items": {
     "$ref": "#/components/schemas/AccessDynamicPolicy"
    }
   },
   "entitlements": {
    "type": "array",
    "description": "Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.",
    "items": {
     "type": "object",
     "required": [
      "ticketId",
      "mediaCodes",
      "validFrom",
      "validTo",
      "entriesAllowed",
      "reentryAllowed"
     ],
     "properties": {
      "ticketId": {
       "type": "string",
       "format": "uuid",
       "description": "The `Entitlement.id`."
      },
      "mediaCodes": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "A ticket may carry several media over its life."
      },
      "validFrom": {
       "type": "string",
       "format": "date-time"
      },
      "validTo": {
       "type": "string",
       "format": "date-time"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "entriesUsed": {
       "type": "integer"
      },
      "reentryAllowed": {
       "type": "boolean"
      },
      "admissionRulesId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "delegatedRights": {
    "type": "array",
    "description": "Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n",
    "items": {
     "type": "object",
     "required": [
      "rightId",
      "ticketId",
      "issuingCellId",
      "validFrom",
      "validTo",
      "entriesAllowed",
      "entriesConsumed"
     ],
     "properties": {
      "rightId": {
       "type": "string"
      },
      "ticketId": {
       "type": "string",
       "format": "uuid",
       "description": "The `Entitlement.id` in the issuing cell."
      },
      "issuingCellId": {
       "type": "string"
      },
      "guestLinkId": {
       "type": "string",
       "nullable": true
      },
      "mediaCodes": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "validFrom": {
       "type": "string",
       "format": "date-time"
      },
      "validTo": {
       "type": "string",
       "format": "date-time"
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "entriesConsumed": {
       "type": "integer"
      },
      "admissionRulesId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "blacklist": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media codes to deny outright regardless of entitlement state."
   },
   "admissionRules": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "openMinutesBefore",
      "closeMinutesAfter"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "openMinutesBefore": {
       "type": "integer"
      },
      "closeMinutesAfter": {
       "type": "integer"
      },
      "maxDurationMinutes": {
       "type": "integer",
       "nullable": true
      },
      "requiresExitBeforeReentry": {
       "type": "boolean"
      }
     }
    }
   },
   "accreditationCredentials": {
    "type": "array",
    "description": "Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.",
    "items": {
     "$ref": "#/components/schemas/AccessAccreditationCredential"
    }
   }
  }
 },
 "OfflinePolicy": {
  "type": "object",
  "x-ticvai-persistence": "platform.offline_policy",
  "description": "Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n",
  "required": [
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$",
    "description": "**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"
   },
   "maxOfflineHours": {
    "type": "integer",
    "default": 24,
    "minimum": 1,
    "maximum": 72,
    "description": "**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"
   },
   "allowedOffline": {
    "type": "array",
    "description": "**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n",
    "items": {
     "type": "string",
     "enum": [
      "sale",
      "refund",
      "exchange",
      "entitlementIssue",
      "entitlementValidate",
      "loyaltyAccrual",
      "loyaltyRedemption",
      "walletSpend",
      "priceOverride",
      "discount",
      "voidLine",
      "noSale"
     ]
    }
   },
   "offlineValueCeiling": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"
   },
   "offlineTransactionCeiling": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 5000,
    "description": "**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"
   },
   "onCeilingBreach": {
    "type": "string",
    "enum": [
     "warn",
     "blockNewSales",
     "blockAll"
    ],
    "default": "blockNewSales"
   },
   "requiresManagerToExtend": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "OfflineSimulationResilienceTestingInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Offline Simulation & Resilience Testing submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "scenario": {
    "type": "string",
    "enum": [
     "centralOutage",
     "edgeOutage",
     "fullOffline"
    ],
    "description": "Outage scenario to simulate"
   },
   "venueId": {
    "type": "string",
    "description": "Venue under test"
   },
   "dynamicQrVerifiedLocally": {
    "type": "boolean",
    "description": "✓ Dynamic QR verified locally"
   },
   "ticketDateVerified": {
    "type": "boolean",
    "description": "✓ Ticket date verified"
   },
   "entryEntitlementVerified": {
    "type": "boolean",
    "description": "✓ Entry entitlement verified"
   },
   "antiPassbackEnforced": {
    "type": "boolean",
    "description": "✓ Anti-passback enforced"
   },
   "gateOpens": {
    "type": "boolean",
    "description": "✓ Gate opens"
   },
   "attendanceStoredLocally": {
    "type": "boolean",
    "description": "✓ Attendance stored locally"
   },
   "transactionQueued": {
    "type": "boolean",
    "description": "✓ Transaction queued"
   },
   "validationCount": {
    "type": "integer",
    "description": "Number of simulated validations"
   },
   "switchedToEdgeMode": {
    "type": "boolean",
    "description": "Gate switched to edge mode"
   },
   "result": {
    "type": "string",
    "enum": [
     "passed",
     "failed"
    ],
    "description": "Offline readiness result, read only"
   }
  },
  "required": [
   "venueId",
   "scenario"
  ]
 },
 "OfflineSimulationResilienceTestingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline Simulation & Resilience Testing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "scenario": {
    "type": "string",
    "enum": [
     "centralOutage",
     "edgeOutage",
     "fullOffline"
    ],
    "description": "Outage scenario to simulate"
   },
   "venueId": {
    "type": "string",
    "description": "Venue under test"
   },
   "dynamicQrVerifiedLocally": {
    "type": "boolean",
    "description": "✓ Dynamic QR verified locally"
   },
   "ticketDateVerified": {
    "type": "boolean",
    "description": "✓ Ticket date verified"
   },
   "entryEntitlementVerified": {
    "type": "boolean",
    "description": "✓ Entry entitlement verified"
   },
   "antiPassbackEnforced": {
    "type": "boolean",
    "description": "✓ Anti-passback enforced"
   },
   "gateOpens": {
    "type": "boolean",
    "description": "✓ Gate opens"
   },
   "attendanceStoredLocally": {
    "type": "boolean",
    "description": "✓ Attendance stored locally"
   },
   "transactionQueued": {
    "type": "boolean",
    "description": "✓ Transaction queued"
   },
   "validationCount": {
    "type": "integer",
    "description": "Number of simulated validations"
   },
   "switchedToEdgeMode": {
    "type": "boolean",
    "description": "Gate switched to edge mode"
   },
   "result": {
    "type": "string",
    "enum": [
     "passed",
     "failed"
    ],
    "description": "Offline readiness result, read only"
   }
  },
  "required": [
   "venueId",
   "scenario"
  ]
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
 "ReconnectionSynchronizationConflictResolutionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Reconnection, Synchronization & Conflict Resolution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "conflictId": {
    "type": "string",
    "description": "Conflict identifier"
   },
   "centralRemainingBalanceBeforeOutage": {
    "type": "integer",
    "description": "Entitlement uses remaining centrally before the outage (a count, not money)"
   },
   "resolutionPolicy": {
    "type": "string",
    "enum": [
     "preserveBothAndFlag",
     "earliestTransactionWins",
     "configuredBusinessRule",
     "supervisorReview",
     "securityInvestigation"
    ],
    "description": "How this conflict is resolved"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential involved"
   }
  },
  "required": [
   "conflictId"
  ]
 },
 "ReconnectionSynchronizationConflictResolutionViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "pendingScans": {
    "type": "integer",
    "description": "Pending scans"
   },
   "entitlementEvents": {
    "type": "integer",
    "description": "Entitlement events"
   },
   "entries": {
    "type": "integer",
    "description": "Entries"
   },
   "exits": {
    "type": "integer",
    "description": "Exits"
   },
   "overrides": {
    "type": "integer",
    "description": "Overrides"
   },
   "securityEvents": {
    "type": "integer",
    "description": "Security events"
   }
  }
 }
}
```
