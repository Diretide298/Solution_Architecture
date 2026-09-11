# WS07 — Access Control board 7

**10 screens · 10 operations · 12 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
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
| `BO-207` | Edge Package & Data Distribution | configEditor | 1 | 0 | — |
| `BO-208` | Offline Credential & Revocation Cache | listDetail | 1 | 0 | — |
| `BO-209` | Offline Entitlement & Usage Ledger | listDetail | 1 | 0 | — |
| `BO-210` | Connectivity Failure & Degraded Mode Policy | listDetail | 1 | 0 | — |
| `BO-211` | Reconnection, Synchronization & Conflict Resolution | listDetail | 1 | 0 | — |
| `BO-212` | Offline Simulation & Resilience Testing | listDetail | 1 | 0 | — |
| `BO-213` | Edge Security, Audit & Deployment | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-204, BO-206, BO-208, BO-209, BO-210, BO-211, BO-212, BO-213 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a real-time overview of offline readiness across the entire access-control estate.",
  "purposeNote": "Operations can immediately determine whether each venue, gate and device is capable of safely operating offline.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every offline edge operations",
       "columns": [
        "OfflineEdgeOperationsCommandCenterView.offlineReadyDevices",
        "OfflineEdgeOperationsCommandCenterView.currentlyOnline",
        "OfflineEdgeOperationsCommandCenterView.currentlyOffline",
        "OfflineEdgeOperationsCommandCenterView.devicesInDegradedMode",
        "OfflineEdgeOperationsCommandCenterView.edgeNodesOnline",
        "OfflineEdgeOperationsCommandCenterView.packagesCurrent",
        "OfflineEdgeOperationsCommandCenterView.packagesExpiring",
        "OfflineEdgeOperationsCommandCenterView.pendingOfflineTransactions",
        "Sync Conflicts",
        "OfflineEdgeOperationsCommandCenterView.offlineSecurityAlerts"
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
        "OfflineEdgeOperationsCommandCenterView.offlineReadyDevices",
        "OfflineEdgeOperationsCommandCenterView.currentlyOnline",
        "OfflineEdgeOperationsCommandCenterView.currentlyOffline",
        "OfflineEdgeOperationsCommandCenterView.devicesInDegradedMode",
        "OfflineEdgeOperationsCommandCenterView.edgeNodesOnline",
        "OfflineEdgeOperationsCommandCenterView.packagesCurrent",
        "OfflineEdgeOperationsCommandCenterView.packagesExpiring",
        "OfflineEdgeOperationsCommandCenterView.pendingOfflineTransactions",
        "Sync Conflicts",
        "OfflineEdgeOperationsCommandCenterView.offlineSecurityAlerts"
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
    "OfflineEdgeOperationsCommandCenterView.offlineReadyDevices",
    "OfflineEdgeOperationsCommandCenterView.currentlyOnline",
    "OfflineEdgeOperationsCommandCenterView.currentlyOffline",
    "OfflineEdgeOperationsCommandCenterView.devicesInDegradedMode",
    "OfflineEdgeOperationsCommandCenterView.edgeNodesOnline",
    "OfflineEdgeOperationsCommandCenterView.packagesCurrent"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-204"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Fields) and no display directory — it is settings, not a population",
  "purpose": "Configure where local access decisions are processed when central services cannot be reached.",
  "purposeNote": "Administrators can define which edge component is responsible for local access decisions for every deployed device.",
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
    "trigger": "onAction",
    "invalidates": [
     "setEdgeNodeLocal"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-205"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define exactly which access checks are allowed to run locally. The matrix identifies key offline criteria including eligible media, eligible site, eligible time, ticket validity and eligible access mode.",
  "purposeNote": "Administrators explicitly control which admission decisions may be performed without central connectivity.",
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
    "trigger": "onAction",
    "invalidates": [
     "setOfflinePolicy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-206"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Access Configuration; Credential Configuration) and no display directory — it is settings, not a population",
  "purpose": "Define what configuration and operational data is securely distributed to edge devices.",
  "purposeNote": "Only approved, intact and authorized edge packages can become active on access-control devices.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-207"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage the local information required to reject credentials that should no longer be usable. This is especially important because Board 3 requires refunded, cancelled, transferred, exchanged, upgraded and reissued credentials to be invalidated.",
  "purposeNote": "Offline devices have a controlled and measurable mechanism for receiving credential invalidations and security changes.",
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
    "operationId": "listOfflineCredentialRevocation",
    "contract": "access",
    "purpose": "Offline Credential & Revocation Cache",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflineCredentialRevocationCacheView.fraudLock",
    "OfflineCredentialRevocationCacheView.cancellation",
    "OfflineCredentialRevocationCacheView.lostCredential",
    "OfflineCredentialRevocationCacheView.manualInvalidation",
    "OfflineCredentialRevocationCacheView.canTrigger"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-208"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 90. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Track entitlement consumption while the central system is unavailable. This is necessary for tickets such as: 3 Fast Pass uses 1 park entry 1 meal 1 re-entry where usage can occur during an outage.",
  "purposeNote": "Offline usage is recorded locally and prevents repeated consumption within the available edge synchronization scope.",
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
    "OfflineEntitlementUsageLedgerView.fastPassRemaining3",
    "OfflineEntitlementUsageLedgerView.rideA1",
    "OfflineEntitlementUsageLedgerView.rideB1",
    "OfflineEntitlementUsageLedgerView.credential",
    "OfflineEntitlementUsageLedgerView.device"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-209"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how devices transition from normal online operation to offline/degraded operation.",
  "purposeNote": "Connectivity failures trigger predefined operating modes rather than unpredictable gate behavior.",
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
    "operationId": "listConnectivityFailureDegraded",
    "contract": "access",
    "purpose": "Connectivity Failure & Degraded Mode Policy",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ConnectivityFailureDegradedModePolicyView.centralServicesReachable",
    "ConnectivityFailureDegradedModePolicyView.someServicesUnavailable",
    "ConnectivityFailureDegradedModePolicyView.onlyDeviceLocalProcessingAvailable"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-210"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Synchronize everything that occurred offline when connectivity returns.",
  "purposeNote": "Offline events synchronize back to the central platform with deterministic reconciliation and a complete audit trail.",
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
       "columns": [
        "ReconnectionSynchronizationConflictResolutionView.pendingScans4821",
        "ReconnectionSynchronizationConflictResolutionView.entitlementEvents682",
        "ReconnectionSynchronizationConflictResolutionView.entries3240",
        "ReconnectionSynchronizationConflictResolutionView.exits1204",
        "ReconnectionSynchronizationConflictResolutionView.overrides18",
        "ReconnectionSynchronizationConflictResolutionView.securityEvents7"
       ],
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
       "columns": [
        "ReconnectionSynchronizationConflictResolutionView.pendingScans4821",
        "ReconnectionSynchronizationConflictResolutionView.entitlementEvents682",
        "ReconnectionSynchronizationConflictResolutionView.entries3240",
        "ReconnectionSynchronizationConflictResolutionView.exits1204",
        "ReconnectionSynchronizationConflictResolutionView.overrides18",
        "ReconnectionSynchronizationConflictResolutionView.securityEvents7"
       ],
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
   "preloaded": [
    "ReconnectionSynchronizationConflictResolutionView.pendingScans4821",
    "ReconnectionSynchronizationConflictResolutionView.entitlementEvents682",
    "ReconnectionSynchronizationConflictResolutionView.entries3240",
    "ReconnectionSynchronizationConflictResolutionView.exits1204",
    "ReconnectionSynchronizationConflictResolutionView.overrides18",
    "ReconnectionSynchronizationConflictResolutionView.securityEvents7"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-211"
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
    "trigger": "onAction",
    "invalidates": [
     "simulateOfflineResilienceTesting"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-212"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Govern the complete offline/edge environment.",
  "purposeNote": "Offline and edge configurations are version-controlled, secured, approved, deployable and fully auditable. Board 7 — Final 10-Screen Structure # Backend Screen Main Responsibility 7.1 Offline & Edge Operations Command Center Estate-wide offline readiness 7.2 Edge Node & Local Processing Configuration Venue/device edge architecture 7.3 Offline Validation Policy Builder Determine which rules work offline 7.4 Edge Package & Data Distribution Secure local configuration packages 7.5 Offline Credential & Revocation Cache Local invalidation/security state 7.6 Offline Entitlement & Usage Ledger Track",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every edge security audit",
       "columns": [
        "Edge certificates/credentials",
        "EdgeSecurityAuditDeploymentView.packageSignatures",
        "EdgeSecurityAuditDeploymentView.authorizedDevices",
        "EdgeSecurityAuditDeploymentView.revokedDevices",
        "EdgeSecurityAuditDeploymentView.failedPackageValidation",
        "EdgeSecurityAuditDeploymentView.unauthorizedConnectionAttempts",
        "EdgeSecurityAuditDeploymentView.configurationChanges"
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
        "Edge certificates/credentials",
        "EdgeSecurityAuditDeploymentView.packageSignatures",
        "EdgeSecurityAuditDeploymentView.authorizedDevices",
        "EdgeSecurityAuditDeploymentView.revokedDevices",
        "EdgeSecurityAuditDeploymentView.failedPackageValidation",
        "EdgeSecurityAuditDeploymentView.unauthorizedConnectionAttempts",
        "EdgeSecurityAuditDeploymentView.configurationChanges"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Draft”, “Deployment Scope”, “Current Production”, “Scheduled”, “Rollback”, “FORCE ONLINE-ONLY”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 96 §Show"
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
   }
  ],
  "entryState": {
   "preloaded": [
    "Edge certificates/credentials",
    "EdgeSecurityAuditDeploymentView.packageSignatures",
    "EdgeSecurityAuditDeploymentView.authorizedDevices",
    "EdgeSecurityAuditDeploymentView.revokedDevices",
    "EdgeSecurityAuditDeploymentView.failedPackageValidation",
    "EdgeSecurityAuditDeploymentView.unauthorizedConnectionAttempts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-213"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 96. 6 of 7 labels bound to a contract property; 7 of 76 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listConnectivityFailureDegraded": {
  "method": "GET",
  "path": "/connectivity-failure-degraded",
  "contract": "access",
  "summary": "Connectivity Failure & Degraded Mode Policy",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "EdgePackageDataDistributionView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "EdgeSecurityAuditDeploymentView"
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
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "OfflineEdgeOperationsCommandCenterView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "OfflineEntitlementUsageLedgerView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ReconnectionSynchronizationConflictResolutionView"
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
  "parameters": [],
  "requestBody": "EdgeNodeLocalProcessingConfigurationInput",
  "responds": "EdgeNodeLocalProcessingConfigurationView"
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
  "parameters": [],
  "requestBody": "OfflineSimulationResilienceTestingInput",
  "responds": "OfflineSimulationResilienceTestingView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ConnectivityFailureDegradedModePolicyView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Connectivity Failure & Degraded Mode Policy displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "centralServicesReachable": {
    "type": "string",
    "description": "Central services reachable"
   },
   "someServicesUnavailable": {
    "type": "string",
    "description": "Some services unavailable"
   },
   "onlyDeviceLocalProcessingAvailable": {
    "type": "string",
    "description": "Only device-local processing available"
   }
  }
 },
 "EdgeNodeLocalProcessingConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Edge Node & Local Processing Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "localProcessingAtGateLevel": {
    "type": "string",
    "description": "Local processing at gate level"
   },
   "embeddedDeviceProcessing": {
    "type": "string",
    "description": "Embedded device processing"
   },
   "mobileOfflineProcessing": {
    "type": "string",
    "description": "Mobile offline processing"
   },
   "edgeNodeId": {
    "type": "string",
    "description": "Edge Node ID"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
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
    "description": "last heartbeat"
   },
   "softwareVersion": {
    "type": "string",
    "description": "software version"
   },
   "securityStatus": {
    "type": "string",
    "description": "security status"
   },
   "failure": {
    "type": "string",
    "description": "failure"
   }
  }
 },
 "EdgeNodeLocalProcessingConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Edge Node & Local Processing Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "localProcessingAtGateLevel": {
    "type": "string",
    "description": "Local processing at gate level"
   },
   "embeddedDeviceProcessing": {
    "type": "string",
    "description": "Embedded device processing"
   },
   "mobileOfflineProcessing": {
    "type": "string",
    "description": "Mobile offline processing"
   },
   "edgeNodeId": {
    "type": "string",
    "description": "Edge Node ID"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
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
    "description": "last heartbeat"
   },
   "softwareVersion": {
    "type": "string",
    "description": "software version"
   },
   "securityStatus": {
    "type": "string",
    "description": "security status"
   },
   "failure": {
    "type": "string",
    "description": "failure"
   }
  }
 },
 "EdgePackageDataDistributionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Edge Package & Data Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venues": {
    "type": "string",
    "description": "venues"
   },
   "zones": {
    "type": "string",
    "description": "zones"
   },
   "gates": {
    "type": "string",
    "description": "gates"
   },
   "accessRules": {
    "type": "string",
    "description": "access rules"
   },
   "calendars": {
    "type": "string",
    "description": "calendars"
   },
   "mediaProfiles": {
    "type": "string",
    "description": "media profiles"
   },
   "verificationProfiles": {
    "type": "string",
    "description": "verification profiles"
   },
   "entitlementDefinitions": {
    "type": "string",
    "description": "entitlement definitions"
   },
   "trustedVerificationMaterial": {
    "type": "string",
    "description": "trusted verification material"
   },
   "revocationInformation": {
    "type": "string",
    "description": "revocation information"
   },
   "credentialSecurityParameters": {
    "type": "string",
    "description": "credential security parameters"
   },
   "reasonCodes": {
    "type": "string",
    "description": "reason codes"
   },
   "gateResponses": {
    "type": "string",
    "description": "gate responses"
   },
   "languages": {
    "type": "string",
    "description": "languages"
   },
   "operatorPermissions": {
    "type": "string",
    "description": "operator permissions"
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
    "type": "string",
    "description": "✓ Signature valid"
   },
   "packageComplete": {
    "type": "string",
    "description": "✓ Package complete"
   },
   "versionValid": {
    "type": "string",
    "description": "✓ Version valid"
   },
   "deviceAuthorized": {
    "type": "string",
    "description": "✓ Device authorized"
   }
  }
 },
 "EdgeSecurityAuditDeploymentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Edge Security, Audit & Deployment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
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
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "edgeCluster": {
    "type": "string",
    "description": "Edge Cluster"
   },
   "gateGroup": {
    "type": "string",
    "description": "Gate Group"
   },
   "deviceGroup": {
    "type": "string",
    "description": "Device Group"
   },
   "individualDevice": {
    "type": "string",
    "description": "Individual Device"
   },
   "v47": {
    "type": "string",
    "description": "V4.7"
   },
   "v48Tonight0200": {
    "type": "string",
    "description": "V4.8 — Tonight 02:00"
   },
   "rollbackToV47": {
    "type": "string",
    "description": "ROLLBACK TO V4.7"
   },
   "offlineRules": {
    "type": "integer",
    "description": "Offline rules"
   },
   "deviceConfiguration": {
    "type": "string",
    "description": "Device configuration"
   },
   "securityPolicy": {
    "type": "string",
    "description": "Security policy"
   },
   "edgePackageDefinitions": {
    "type": "string",
    "description": "edge package definitions"
   },
   "whereOperationallyAppropriate": {
    "type": "string",
    "description": "where operationally appropriate"
   },
   "theCloudGoesDown": {
    "type": "string",
    "description": "the cloud goes down"
   },
   "venueEdgeActive": {
    "type": "string",
    "description": "VENUE EDGE — ACTIVE ✓"
   },
   "venueExecutives": {
    "type": "string",
    "description": "venue executives"
   },
   "processesOnSpecialDates": {
    "type": "string",
    "description": "processes on special dates"
   },
   "definesTheUnderlyingRules": {
    "type": "string",
    "description": "defines the underlying rules"
   },
   "thisTicketAllows3Entries": {
    "type": "string",
    "description": "\"This ticket allows 3 entries.\""
   }
  }
 },
 "OfflineCredentialRevocationCacheView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline Credential & Revocation Cache displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fraudLock": {
    "type": "string",
    "description": "Fraud Lock"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "lostCredential": {
    "type": "string",
    "description": "Lost Credential"
   },
   "manualInvalidation": {
    "type": "string",
    "description": "Manual Invalidation"
   },
   "canTrigger": {
    "type": "boolean",
    "description": "can trigger"
   },
   "continue": {
    "type": "string",
    "description": "Continue"
   },
   "continueWithWarning": {
    "type": "string",
    "description": "Continue with warning"
   },
   "restrictedProductsOnly": {
    "type": "string",
    "description": "Restricted products only"
   },
   "supervisorMode": {
    "type": "string",
    "description": "Supervisor mode"
   },
   "denySelectedCredentialClasses": {
    "type": "string",
    "description": "Deny selected credential classes"
   },
   "failClosed": {
    "type": "integer",
    "description": "Fail closed"
   }
  }
 },
 "OfflineEdgeOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline & Edge Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
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
    "type": "string",
    "description": "Devices in Degraded Mode"
   },
   "edgeNodesOnline": {
    "type": "integer",
    "description": "Edge Nodes Online"
   },
   "packagesCurrent": {
    "type": "string",
    "description": "Packages Current"
   },
   "packagesExpiring": {
    "type": "string",
    "description": "Packages Expiring"
   },
   "pendingOfflineTransactions": {
    "type": "integer",
    "description": "Pending Offline Transactions"
   },
   "offlineSecurityAlerts": {
    "type": "integer",
    "description": "Offline Security Alerts"
   },
   "rulesCached": {
    "type": "string",
    "description": "✓ Rules cached"
   },
   "verificationMaterialCurrent": {
    "type": "string",
    "description": "✓ Verification material current"
   },
   "revocationDataCurrent": {
    "type": "string",
    "description": "✓ Revocation data current"
   },
   "credentialDefinitionsAvailable": {
    "type": "string",
    "description": "✓ Credential definitions available"
   },
   "deviceStorageHealthy": {
    "type": "string",
    "description": "✓ Device storage healthy"
   },
   "lastSynchronizationSuccessful": {
    "type": "string",
    "description": "✓ Last synchronization successful"
   }
  }
 },
 "OfflineEntitlementUsageLedgerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline Entitlement & Usage Ledger displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fastPassRemaining3": {
    "type": "string",
    "description": "Fast Pass Remaining: 3"
   },
   "rideA1": {
    "type": "string",
    "description": "Ride A → -1"
   },
   "rideB1": {
    "type": "string",
    "description": "Ride B → -1"
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
    "type": "string",
    "description": "local sequence"
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
   },
   "shareCurrentUsageState": {
    "type": "number",
    "description": "share current usage state"
   },
   "offlineAllowedMaximum1": {
    "type": "integer",
    "description": "Offline Allowed — Maximum 1"
   }
  }
 },
 "OfflinePolicy": {
  "type": "object",
  "x-ticvai-persistence": "platform.offline_policy",
  "description": "Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n",
  "required": [
   "id",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "maxOfflineHours": {
    "type": "integer",
    "default": 24,
    "description": "**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect.\n"
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
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "offlineTransactionCeiling": {
    "type": "integer",
    "nullable": true,
    "description": "**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second.\n"
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
   "dynamicQrVerifiedLocally": {
    "type": "string",
    "description": "✓ Dynamic QR verified locally"
   },
   "ticketDateVerified": {
    "type": "string",
    "format": "date-time",
    "description": "✓ Ticket date verified"
   },
   "entryEntitlementVerified": {
    "type": "string",
    "description": "✓ Entry entitlement verified"
   },
   "antiPassbackEnforced": {
    "type": "string",
    "description": "✓ Anti-passback enforced"
   },
   "gateOpens": {
    "type": "string",
    "description": "✓ Gate opens"
   },
   "attendanceStoredLocally": {
    "type": "integer",
    "description": "✓ Attendance stored locally"
   },
   "transactionQueued": {
    "type": "string",
    "description": "✓ Transaction queued"
   }
  }
 },
 "OfflineSimulationResilienceTestingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline Simulation & Resilience Testing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dynamicQrVerifiedLocally": {
    "type": "string",
    "description": "✓ Dynamic QR verified locally"
   },
   "ticketDateVerified": {
    "type": "string",
    "format": "date-time",
    "description": "✓ Ticket date verified"
   },
   "entryEntitlementVerified": {
    "type": "string",
    "description": "✓ Entry entitlement verified"
   },
   "antiPassbackEnforced": {
    "type": "string",
    "description": "✓ Anti-passback enforced"
   },
   "gateOpens": {
    "type": "string",
    "description": "✓ Gate opens"
   },
   "attendanceStoredLocally": {
    "type": "integer",
    "description": "✓ Attendance stored locally"
   },
   "transactionQueued": {
    "type": "string",
    "description": "✓ Transaction queued"
   }
  }
 },
 "ReconnectionSynchronizationConflictResolutionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Reconnection, Synchronization & Conflict Resolution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "returnOnline": {
    "type": "integer",
    "description": "Return Online"
   },
   "pendingScans4821": {
    "type": "integer",
    "description": "Pending Scans: 4,821"
   },
   "entitlementEvents682": {
    "type": "string",
    "description": "Entitlement Events: 682"
   },
   "entries3240": {
    "type": "string",
    "description": "Entries: 3,240"
   },
   "exits1204": {
    "type": "string",
    "description": "Exits: 1,204"
   },
   "overrides18": {
    "type": "string",
    "description": "Overrides: 18"
   },
   "securityEvents7": {
    "type": "string",
    "description": "Security Events: 7"
   },
   "centralRemainingBalanceBeforeOutage": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Central remaining balance before outage (the pack shows 1)"
   },
   "preserveBothFlag": {
    "type": "boolean",
    "description": "Preserve both + flag"
   },
   "earliestTransactionWins": {
    "type": "string",
    "description": "earliest transaction wins"
   },
   "configuredBusinessRule": {
    "type": "string",
    "description": "configured business rule"
   },
   "supervisorReview": {
    "type": "string",
    "description": "supervisor review"
   },
   "securityInvestigation": {
    "type": "string",
    "description": "security investigation"
   }
  }
 }
}
```
