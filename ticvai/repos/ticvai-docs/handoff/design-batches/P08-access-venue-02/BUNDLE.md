# P08-access-venue-02 — P08 · Access & Venue (2 of 3)

**10 screens · 50 operations · 47 schemas · 20 permissions**

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

- **Every control that can be refused must be gated.** 20 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, AI_AUDIT_VIEW, ASSET_MANAGE, ASSET_VIEW, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, QUEUE_MANAGE, QUEUE_VIEW`…. A control nobody can use must say so,
  not sit enabled and fail.
- **18 of these operations work offline**: getAsset, getQueue, getVenueMap, getVenueMapGraph, getWaitTimes, listAssets, listGames, listQueues
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-034` | Scan Activity | listDetail | 7 | 1 | — |
| `BO-035` | Override Audit | listDetail | 8 | 1 | — |
| `BO-038` | Reconciliation Queue | listDetail | 9 | 0 | — |
| `BO-069` | Asset Register | listDetail | 11 | 0 | — |
| `BO-071` | Planned Maintenance | listDetail | 4 | 0 | — |
| `BO-072` | Incident Log | listDetail | 5 | 0 | — |
| `BO-092` | Venue Maps | listDetail | 2 | 0 | — |
| `BO-093` | Map Import & Labelling | configEditor | 3 | 0 | — |
| `BO-094` | Map Editor & Publish | statusTracker | 6 | 0 | — |
| `BO-095` | Resources | listDetail | 2 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-034",
  "name": "Scan Activity",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/scan-activity",
   "component": "apps/venue-management-web/src/routes/venue-operations/ScanActivityDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "See what the gates have been doing.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every scan activity",
       "bindsTo": "ScanEvent",
       "columns": [
        "ScanEvent.id",
        "ScanEvent.accessPointId",
        "ScanEvent.venueId",
        "ScanEvent.scopePath",
        "ScanEvent.ticketId",
        "ScanEvent.mediaCode",
        "ScanEvent.outcome",
        "ScanEvent.denyReason",
        "ScanEvent.direction",
        "ScanEvent.operatorPrincipalId",
        "ScanEvent.deviceId",
        "ScanEvent.overriddenByPrincipalId"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected scan activity",
       "bindsTo": "OfflinePackage",
       "columns": [
        "OfflinePackage.generatedAt",
        "OfflinePackage.validFrom",
        "OfflinePackage.validTo",
        "OfflinePackage.accessPointId",
        "OfflinePackage.entitlements",
        "OfflinePackage.delegatedRights",
        "OfflinePackage.blacklist",
        "OfflinePackage.admissionRules"
       ],
       "operation": "getOfflinePackage",
       "provenance": "contract access.yaml GET /access/offline-package"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Sync",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup",
       "operation": "lookupTicket",
       "provenance": "contract access.yaml GET /access/lookup"
      },
      {
       "kind": "destructiveButton",
       "label": "Override",
       "operation": "overrideAccess",
       "provenance": "contract access.yaml POST /access/override"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateAccess",
       "provenance": "contract access.yaml POST /access/validate"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateGroupAccess",
       "provenance": "contract access.yaml POST /access/group-validate"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "scanTarget",
       "derived": true,
       "impliedBy": "listScans",
       "notes": "**A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or explain something.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupTicket",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "syncScans",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmOverrideAccess",
    "component": "confirmDialog",
    "trigger": "Override",
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A scan activity this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml POST /access/override"
   }
  ],
  "states": {
   "loading": "The scan activity list.",
   "error": "Could not load. Names which read failed and leaves the scan activity untouched.",
   "emptyFirstRun": "No scan activity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the scan activity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
    "trigger": "onLoad"
   },
   {
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupTicket",
    "contract": "access",
    "purpose": "Read-only validity check without admitting",
    "trigger": "onLoad"
   },
   {
    "operationId": "overrideAccess",
    "contract": "access",
    "purpose": "Admit against a failed validation",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "validateAccess",
    "contract": "access",
    "purpose": "Validate media at an access point and admit or deny",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "validateGroupAccess",
    "contract": "access",
    "purpose": "Admit a group on one read",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflinePackage.generatedAt",
    "OfflinePackage.validFrom",
    "OfflinePackage.validTo",
    "OfflinePackage.accessPointId",
    "OfflinePackage.entitlements"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-034"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-035",
  "name": "Override Audit",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/override-audit",
   "component": "apps/venue-management-web/src/routes/venue-operations/OverrideAuditDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "Review every admission that broke a rule.",
  "gaps": [
   {
    "operation": "listAuditRecords",
    "why": "**1 declared operation reach no component on this screen**: listAuditRecords. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every override audit",
       "bindsTo": "ScanEvent",
       "columns": [
        "ScanEvent.id",
        "ScanEvent.accessPointId",
        "ScanEvent.venueId",
        "ScanEvent.scopePath",
        "ScanEvent.ticketId",
        "ScanEvent.mediaCode",
        "ScanEvent.outcome",
        "ScanEvent.denyReason",
        "ScanEvent.direction",
        "ScanEvent.operatorPrincipalId",
        "ScanEvent.deviceId",
        "ScanEvent.overriddenByPrincipalId"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected override audit",
       "bindsTo": "OfflinePackage",
       "columns": [
        "OfflinePackage.generatedAt",
        "OfflinePackage.validFrom",
        "OfflinePackage.validTo",
        "OfflinePackage.accessPointId",
        "OfflinePackage.entitlements",
        "OfflinePackage.delegatedRights",
        "OfflinePackage.blacklist",
        "OfflinePackage.admissionRules"
       ],
       "operation": "getOfflinePackage",
       "provenance": "contract access.yaml GET /access/offline-package"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Lookup",
       "operation": "lookupTicket",
       "provenance": "contract access.yaml GET /access/lookup"
      },
      {
       "kind": "destructiveButton",
       "label": "Override",
       "operation": "overrideAccess",
       "provenance": "contract access.yaml POST /access/override"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateAccess",
       "provenance": "contract access.yaml POST /access/validate"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateGroupAccess",
       "provenance": "contract access.yaml POST /access/group-validate"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "scanTarget",
       "derived": true,
       "impliedBy": "listScans",
       "notes": "**A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or explain something.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupTicket",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAuditRecords",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "overrideAccess",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmOverrideAccess",
    "component": "confirmDialog",
    "trigger": "Override",
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A override audit this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml POST /access/override"
   }
  ],
  "states": {
   "loading": "The override audit list.",
   "error": "Could not load. Names which read failed and leaves the override audit untouched.",
   "emptyFirstRun": "No override audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the override audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupTicket",
    "contract": "access",
    "purpose": "Read-only validity check without admitting",
    "trigger": "onLoad"
   },
   {
    "operationId": "overrideAccess",
    "contract": "access",
    "purpose": "Admit against a failed validation",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "validateAccess",
    "contract": "access",
    "purpose": "Validate media at an access point and admit or deny",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "validateGroupAccess",
    "contract": "access",
    "purpose": "Admit a group on one read",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "listAuditRecords",
    "contract": "tenancy",
    "purpose": "Who did what, where, and when",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflinePackage.generatedAt",
    "OfflinePackage.validFrom",
    "OfflinePackage.validTo",
    "OfflinePackage.accessPointId",
    "OfflinePackage.entitlements"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-035"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-038",
  "name": "Reconciliation Queue",
  "module": "Access & Venue",
  "requiresModule": "queue",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/reconciliation-queue",
   "component": "apps/venue-management-web/src/routes/venue-operations/ReconciliationQueueDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listQueues` reads the population and `getQueue` reads one of them — list, select, act",
  "purpose": "Handle scans the server disagreed with.",
  "gaps": [
   {
    "operation": "getWaitTimes",
    "why": "**2 declared operations reach no component on this screen**: getWaitTimes, listQueueEntries. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every reconciliation queue",
       "bindsTo": "Queue",
       "columns": [
        "Queue.code",
        "Queue.name",
        "Queue.venueId",
        "Queue.attractionProductId",
        "Queue.assetId",
        "Queue.accessPointId",
        "Queue.kind",
        "Queue.operatingWindows",
        "Queue.parentQueueId",
        "Queue.loadBalanceWithQueueIds",
        "Queue.inQueueOfferEnabled",
        "Queue.notifyBeforeCallMinutes"
       ],
       "operation": "listQueues",
       "provenance": "contract queue.yaml GET /queues"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reconciliation queue",
       "bindsTo": "QueueDetail",
       "columns": [
        "QueueDetail.nowServingPartyNumber",
        "QueueDetail.lastCalledAt",
        "QueueDetail.throughputLastHour",
        "QueueDetail.noShowRatePercent",
        "QueueDetail.feed"
       ],
       "operation": "getQueue",
       "provenance": "contract queue.yaml GET /queues/{queueId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createQueue",
       "provenance": "contract queue.yaml POST /queues"
      },
      {
       "kind": "secondaryButton",
       "label": "Call",
       "operation": "callNextParties",
       "provenance": "contract queue.yaml POST /queues/{queueId}/call-next"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setQueueStatus",
       "provenance": "contract queue.yaml PUT /queues/{queueId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setWaitTime",
       "provenance": "contract queue.yaml PUT /queues/{queueId}/wait-time"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateQueue",
       "provenance": "contract queue.yaml PATCH /queues/{queueId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listQueues",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createQueue",
       "label": "Create queue",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createQueue",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconciliation queue list.",
   "error": "Could not load. Names which read failed and leaves the reconciliation queue untouched.",
   "emptyFirstRun": "No reconciliation queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reconciliation queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "List queues",
    "trigger": "onLoad"
   },
   {
    "operationId": "getQueue",
    "contract": "queue",
    "purpose": "Read a queue with live position",
    "trigger": "onLoad"
   },
   {
    "operationId": "createQueue",
    "contract": "queue",
    "purpose": "Create a queue",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "callNextParties",
    "contract": "queue",
    "purpose": "Call the next parties forward",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listQueueEntries",
    "contract": "queue",
    "purpose": "List entries in a queue",
    "trigger": "onLoad"
   },
   {
    "operationId": "setQueueStatus",
    "contract": "queue",
    "purpose": "Open, pause or close a queue",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "setWaitTime",
    "contract": "queue",
    "purpose": "Manually set a wait time",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "updateQueue",
    "contract": "queue",
    "purpose": "Amend queue configuration",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "queueId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `queueId`.",
   "preloaded": [
    "QueueDetail.nowServingPartyNumber",
    "QueueDetail.lastCalledAt",
    "QueueDetail.throughputLastHour",
    "QueueDetail.noShowRatePercent",
    "QueueDetail.feed"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-038"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-069",
  "name": "Asset Register",
  "module": "Access & Venue",
  "requiresModule": "maintenance",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/asset-register",
   "component": "apps/venue-management-web/src/routes/venue-operations/AssetRegisterDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAssets` reads the population and `getAsset` reads one of them — list, select, act",
  "purpose": "Know what equipment exists and where.",
  "gaps": [
   {
    "operation": "getAssetHistory",
    "why": "**2 declared operations reach no component on this screen**: getAssetHistory, listGames. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every asset register",
       "bindsTo": "Asset",
       "columns": [
        "Asset.assetTag",
        "Asset.name",
        "Asset.venueId",
        "Asset.categoryId",
        "Asset.locationDescription",
        "Asset.criticality",
        "Asset.manufacturer",
        "Asset.model",
        "Asset.serialNumber",
        "Asset.commissionedAt",
        "Asset.warrantyExpiresAt",
        "Asset.supplierId"
       ],
       "operation": "listAssets",
       "provenance": "contract maintenance.yaml GET /assets"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset register",
       "bindsTo": "AssetDetail",
       "columns": [
        "AssetDetail.openWorkOrders",
        "AssetDetail.maintenancePlans",
        "AssetDetail.documents"
       ],
       "operation": "getAsset",
       "provenance": "contract maintenance.yaml GET /assets/{assetId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createAsset",
       "provenance": "contract maintenance.yaml POST /assets"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup",
       "operation": "lookupAsset",
       "provenance": "contract maintenance.yaml GET /assets/lookup"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAssetStatus",
       "provenance": "contract maintenance.yaml PUT /assets/{assetId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateAsset",
       "provenance": "contract maintenance.yaml PATCH /assets/{assetId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateGame",
       "provenance": "contract games.yaml PATCH /games/{gameId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordGamePlay",
       "provenance": "contract games.yaml POST /game-plays"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync",
       "operation": "syncGamePlays",
       "provenance": "contract games.yaml POST /game-plays/sync"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAssets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createAsset",
       "label": "Create asset",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupAsset",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAsset",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset register list.",
   "error": "Could not load. Names which read failed and leaves the asset register untouched.",
   "emptyFirstRun": "No asset register yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset register are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAssets",
    "contract": "maintenance",
    "purpose": "List assets",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAsset",
    "contract": "maintenance",
    "purpose": "Read an asset with history and documents",
    "trigger": "onLoad"
   },
   {
    "operationId": "createAsset",
    "contract": "maintenance",
    "purpose": "Register an asset",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   },
   {
    "operationId": "getAssetHistory",
    "contract": "maintenance",
    "purpose": "Service history",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupAsset",
    "contract": "maintenance",
    "purpose": "Find an asset by tag or QR",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAssetStatus",
    "contract": "maintenance",
    "purpose": "Take an asset out of service or return it",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   },
   {
    "operationId": "updateAsset",
    "contract": "maintenance",
    "purpose": "Amend an asset",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   },
   {
    "operationId": "listGames",
    "contract": "games",
    "purpose": "List games",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateGame",
    "contract": "games",
    "purpose": "Amend a game",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   },
   {
    "operationId": "recordGamePlay",
    "contract": "games",
    "purpose": "Record a play",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   },
   {
    "operationId": "syncGamePlays",
    "contract": "games",
    "purpose": "Replay plays recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "deepLink"
    },
    {
     "name": "gameId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `assetId`, `gameId`.",
   "preloaded": [
    "AssetDetail.openWorkOrders",
    "AssetDetail.maintenancePlans",
    "AssetDetail.documents"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-069"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-071",
  "name": "Planned Maintenance",
  "module": "Access & Venue",
  "requiresModule": "maintenance",
  "wave": 3,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/planned-maintenance",
   "component": "apps/venue-management-web/src/routes/venue-operations/PlannedMaintenanceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMaintenancePlans` reads the population and `getDueMaintenance` reads one of them — list, select, act",
  "purpose": "Schedule the work that stops the emergencies.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every planned maintenance",
       "bindsTo": "MaintenancePlan",
       "columns": [
        "MaintenancePlan.id",
        "MaintenancePlan.name",
        "MaintenancePlan.assetId",
        "MaintenancePlan.assetCategoryId",
        "MaintenancePlan.intervalDays",
        "MaintenancePlan.usageInterval",
        "MaintenancePlan.leadTimeDays",
        "MaintenancePlan.taskTemplate",
        "MaintenancePlan.lastCompletedAt",
        "MaintenancePlan.nextDueAt",
        "MaintenancePlan.isActive"
       ],
       "operation": "listMaintenancePlans",
       "provenance": "contract maintenance.yaml GET /maintenance-plans"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected planned maintenance",
       "bindsTo": "DueMaintenanceTask",
       "columns": [
        "DueMaintenanceTask.planId",
        "DueMaintenanceTask.planName",
        "DueMaintenanceTask.assetId",
        "DueMaintenanceTask.assetName",
        "DueMaintenanceTask.criticality",
        "DueMaintenanceTask.dueAt",
        "DueMaintenanceTask.isOverdue",
        "DueMaintenanceTask.daysOverdue",
        "DueMaintenanceTask.triggeredBy",
        "DueMaintenanceTask.workOrderId"
       ],
       "operation": "getDueMaintenance",
       "provenance": "contract maintenance.yaml GET /maintenance-plans/due"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createMaintenancePlan",
       "provenance": "contract maintenance.yaml POST /maintenance-plans"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setRolePermissions",
       "provenance": "contract tenancy.yaml PUT /roles/{roleId}/permissions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMaintenancePlans",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createMaintenancePlan",
       "label": "Create maintenance plan",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createMaintenancePlan",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The planned maintenance list.",
   "error": "Could not load. Names which read failed and leaves the planned maintenance untouched.",
   "emptyFirstRun": "No planned maintenance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the planned maintenance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMaintenancePlans",
    "contract": "maintenance",
    "purpose": "List planned maintenance schedules",
    "trigger": "onLoad"
   },
   {
    "operationId": "createMaintenancePlan",
    "contract": "maintenance",
    "purpose": "Create a planned maintenance schedule",
    "trigger": "onAction",
    "invalidates": [
     "listMaintenancePlans"
    ]
   },
   {
    "operationId": "getDueMaintenance",
    "contract": "maintenance",
    "purpose": "Planned tasks due or overdue",
    "trigger": "onLoad"
   },
   {
    "operationId": "setRolePermissions",
    "contract": "tenancy",
    "purpose": "What this role may do",
    "trigger": "onAction",
    "invalidates": [
     "listMaintenancePlans"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "roleId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A role opened from the directory. **Permissions are set per role, not per person** — ADR-0002 makes authorisation user-driven through roles.",
   "preloaded": [
    "DueMaintenanceTask.planId",
    "DueMaintenanceTask.planName",
    "DueMaintenanceTask.assetId",
    "DueMaintenanceTask.assetName",
    "DueMaintenanceTask.criticality"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-071"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-072",
  "name": "Incident Log",
  "module": "Access & Venue",
  "requiresModule": "maintenance",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/incident-log",
   "component": "apps/venue-management-web/src/routes/venue-operations/IncidentLogDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listIncidents` reads the population and `getIncident` reads one of them — list, select, act",
  "purpose": "Record what happened, while it is fresh.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every incident log",
       "bindsTo": "Incident",
       "columns": [
        "Incident.id",
        "Incident.incidentNumber",
        "Incident.kind",
        "Incident.severity",
        "Incident.status",
        "Incident.venueId",
        "Incident.assetId",
        "Incident.locationDescription",
        "Incident.isReportable",
        "Incident.notificationDueAt",
        "Incident.notifiedAt",
        "Incident.assignedToPrincipalId"
       ],
       "operation": "listIncidents",
       "provenance": "contract maintenance.yaml GET /incidents"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected incident log",
       "bindsTo": "IncidentDetail",
       "columns": [
        "IncidentDetail.id",
        "IncidentDetail.incidentNumber",
        "IncidentDetail.kind",
        "IncidentDetail.severity",
        "IncidentDetail.status",
        "IncidentDetail.venueId",
        "IncidentDetail.assetId",
        "IncidentDetail.locationDescription",
        "IncidentDetail.isReportable",
        "IncidentDetail.notificationDueAt",
        "IncidentDetail.notifiedAt",
        "IncidentDetail.assignedToPrincipalId",
        "IncidentDetail.reportedByPrincipalId",
        "IncidentDetail.correctiveWorkOrderId",
        "IncidentDetail.occurredAt",
        "IncidentDetail.recordedAt"
       ],
       "operation": "getIncident",
       "provenance": "contract maintenance.yaml GET /incidents/{incidentId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Report",
       "operation": "reportIncident",
       "provenance": "contract maintenance.yaml POST /incidents"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordAuthorityNotification",
       "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateIncident",
       "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listIncidents",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "reportIncident",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The incident log list.",
   "error": "Could not load. Names which read failed and leaves the incident log untouched.",
   "emptyFirstRun": "No incident log yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the incident log are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listIncidents",
    "contract": "maintenance",
    "purpose": "List incidents",
    "trigger": "onLoad"
   },
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "Read an incident",
    "trigger": "onLoad"
   },
   {
    "operationId": "reportIncident",
    "contract": "maintenance",
    "purpose": "Report an incident",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "recordAuthorityNotification",
    "contract": "maintenance",
    "purpose": "Record notification to an external authority",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "updateIncident",
    "contract": "maintenance",
    "purpose": "Investigate, escalate or close an incident",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "incidentId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `incidentId`.",
   "preloaded": [
    "IncidentDetail.id",
    "IncidentDetail.incidentNumber",
    "IncidentDetail.kind",
    "IncidentDetail.severity",
    "IncidentDetail.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-072"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-092",
  "name": "Venue Maps",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-mapping/venue-maps",
   "component": "apps/venue-management-web/src/routes/venue-mapping/VenueMapList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-093",
    "BO-094"
   ],
   "transitions": [
    {
     "to": "BO-093",
     "trigger": "The plan is uploaded and read",
     "provenance": "flow F26 step 1→2",
     "operation": "createVenueMap"
    },
    {
     "to": "BO-094",
     "trigger": "Map Editor & Publish",
     "carries": [
      "mapId",
      "pathId"
     ],
     "provenance": "derived — BO-094 declares entryState.params mapId, pathId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "CF-123. **A venue may have several maps** — a park map and a floor plan per building are different maps, not layers of one, because a guest on the second floor should not be shown the ground floor toilets. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2e`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 2.dc.html#seat-2e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listVenueMaps` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Every map for this venue, and which is published.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every venue maps",
       "bindsTo": "VenueMap",
       "columns": [
        "VenueMap.id",
        "VenueMap.name",
        "VenueMap.venueId",
        "VenueMap.scopePath",
        "VenueMap.kind",
        "VenueMap.floorLevel",
        "VenueMap.status",
        "VenueMap.publishedVersion",
        "VenueMap.isGeoreferenced",
        "VenueMap.baseAssetId",
        "VenueMap.baseImageAlignment",
        "VenueMap.tileSetRef"
       ],
       "operation": "listVenueMaps",
       "provenance": "contract venue-map.yaml GET /venue-maps"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected venue maps",
       "bindsTo": "VenueMap",
       "columns": [
        "VenueMap.id",
        "VenueMap.name",
        "VenueMap.venueId",
        "VenueMap.scopePath",
        "VenueMap.kind",
        "VenueMap.floorLevel",
        "VenueMap.status",
        "VenueMap.publishedVersion",
        "VenueMap.isGeoreferenced",
        "VenueMap.baseAssetId",
        "VenueMap.baseImageAlignment",
        "VenueMap.tileSetRef",
        "VenueMap.boundsGeoJson",
        "VenueMap.graphStatus"
       ],
       "operation": "listVenueMaps",
       "provenance": "contract venue-map.yaml GET /venue-maps"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createVenueMap",
       "provenance": "contract venue-map.yaml POST /venue-maps"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listVenueMaps",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createVenueMap",
       "label": "Create venue map",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createVenueMap",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue maps list.",
   "error": "Could not load. Names which read failed and leaves the venue maps untouched.",
   "emptyFirstRun": "No venue maps yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue maps are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVenueMaps",
    "contract": "venue-map",
    "purpose": "Maps",
    "trigger": "onLoad"
   },
   {
    "operationId": "createVenueMap",
    "contract": "venue-map",
    "purpose": "Start one",
    "trigger": "onAction",
    "invalidates": [
     "listVenueMaps"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "VenueMap.id",
    "VenueMap.name",
    "VenueMap.venueId",
    "VenueMap.scopePath",
    "VenueMap.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-092",
   "note": "**Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-093",
  "name": "Map Import & Labelling",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-mapping/map-import",
   "component": "apps/venue-management-web/src/routes/venue-mapping/VenueMapImportForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-092",
    "BO-094"
   ],
   "transitions": [
    {
     "to": "BO-094",
     "trigger": "The operator places what the drawing did not carry and links each point to what it is",
     "provenance": "flow F26 step 3→4"
    }
   ]
  },
  "notes": "CF-123. **Two failure modes on one screen, kept visually apart.** Extraction is deterministic and reports which layers it found; labelling is a proposal with a confidence. **A mis-parsed layer and a bad suggestion look identical if the screen blurs them**, and the operator is left saying only that the map is wrong. **Low-confidence proposals are shown, not filtered** — the shape the assistant is unsure about is the one most worth a human looking at. **Drawn 26 August** — `Seat Board 1.dc.html` frame `seat-1a`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 1.dc.html#seat-1a"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`importVenueGeometry`, `proposeVenueLabels`, `acceptVenueLabelProposals`) and no read of a population — it is settings, not a list",
  "purpose": "Upload a plan, check what was read, and review what the assistant suggests.",
  "gaps": [
   {
    "operation": "importVenueGeometry",
    "why": "**`importVenueGeometry` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Import",
       "operation": "importVenueGeometry",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "secondaryButton",
       "label": "Propose",
       "operation": "proposeVenueLabels",
       "provenance": "contract ai.yaml POST /ai/venue-map/{mapId}/propose-labels"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept",
       "operation": "acceptVenueLabelProposals",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/proposals"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "fileUpload",
       "notes": "The geometry file being imported.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "progressIndicator",
       "notes": "Import is long enough to leave the screen. **A spinner with no proportion is a screen people reload**, and reloading an import is how a venue gets two of everything.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "importVenueGeometry",
       "label": "Import venue geometry",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "importVenueGeometry",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved map import labelling.",
   "error": "Could not load. Names which read failed and leaves the map import labelling untouched.",
   "emptyFirstRun": "No map import labelling configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "importVenueGeometry",
    "contract": "venue-map",
    "purpose": "Read the drawing",
    "trigger": "onAction"
   },
   {
    "operationId": "proposeVenueLabels",
    "contract": "ai",
    "purpose": "Suggest labels",
    "trigger": "onAction"
   },
   {
    "operationId": "acceptVenueLabelProposals",
    "contract": "venue-map",
    "purpose": "Accept or reject",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mapId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mapId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-093",
   "note": "**Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-094",
  "name": "Map Editor & Publish",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-mapping/map-editor",
   "component": "apps/venue-management-web/src/routes/venue-mapping/VenueMapEditorForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-092"
   ],
   "transitions": [
    {
     "to": "GST-021",
     "trigger": "A guest opens the map and is routed",
     "provenance": "flow F26 step 6→7",
     "operation": "publishVenueMap",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "CF-123. **Publishing is a separate act from saving**, and the screen makes that visible — editing a live map under a guest standing in front of it is how a route ends at a wall. **Refuses to publish a point linked to a closed outlet**, naming which one: a restaurant point pointing nowhere is worse than no point, because a guest walks there. **`isStepFree` on a path is the field to get right** — a wheelchair user routed up a staircase was failed by the map, not the venue. **Graph validation runs before publish and on demand.** The screen separates two findings that read the same and are not: **an unreachable point is a defect, and a point reachable only by steps is a map that works until a wheelchair user opens it.** **Critical points — first aid, emergency exits, assembly points — are listed apart**, because an unreachable gift shop and an unreachable assembly point should not sit in one list of two hundred. **Drawn 26 August** — `Seat Board 1.dc.html` frame `seat-1b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 1.dc.html#seat-1b"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getVenueMap` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Place booths, toilets, exits, rides and restaurants, then publish.",
  "gaps": [
   {
    "operation": "getVenueMapGraph",
    "why": "**1 declared operation reach no component on this screen**: getVenueMapGraph. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected map editor publish",
       "bindsTo": "VenueMapDetail",
       "columns": [
        "VenueMapDetail.map",
        "VenueMapDetail.points",
        "VenueMapDetail.paths"
       ],
       "operation": "getVenueMap",
       "provenance": "contract venue-map.yaml GET /venue-maps/{mapId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setVenuePoint",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/points"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishVenueMap",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateVenueMapGraph",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/validate-graph"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setPathClosure",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/paths/{pathId}/closure"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getVenueMap",
       "notes": "One record, read-only.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setVenuePoint",
       "label": "Save venue point",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishVenueMap",
       "notes": "**Publishing a map moves people.** The gate names what changes before it happens — which routes, which closures, which points become unreachable.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setVenuePoint",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The map editor publish list.",
   "error": "Could not load. Names which read failed and leaves the map editor publish untouched.",
   "emptyFirstRun": "No map editor publish yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the map editor publish are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getVenueMap",
    "contract": "venue-map",
    "purpose": "The draft",
    "trigger": "onLoad"
   },
   {
    "operationId": "setVenuePoint",
    "contract": "venue-map",
    "purpose": "Place a point",
    "trigger": "onAction"
   },
   {
    "operationId": "publishVenueMap",
    "contract": "venue-map",
    "purpose": "Publish",
    "trigger": "onAction"
   },
   {
    "operationId": "validateVenueMapGraph",
    "contract": "venue-map",
    "purpose": "What is unreachable, before anyone publishes it",
    "trigger": "onAction"
   },
   {
    "operationId": "setPathClosure",
    "contract": "venue-map",
    "purpose": "Close a route during works or an incident",
    "trigger": "onAction"
   },
   {
    "operationId": "getVenueMapGraph",
    "contract": "venue-map",
    "purpose": "The navigation graph, ready to route over",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mapId",
     "from": "deepLink"
    },
    {
     "name": "pathId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mapId`, `pathId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-094",
   "note": "**Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-095",
  "name": "Resources",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/directory",
   "component": "apps/venue-management-web/src/routes/resources/ResourceList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-096",
    "BO-097"
   ],
   "transitions": [
    {
     "to": "BO-096",
     "trigger": "Resource Calendar",
     "carries": [
      "resourceId"
     ],
     "provenance": "derived — BO-096 declares entryState.params resourceId, so an edge into it must carry them"
    },
    {
     "to": "BO-097",
     "trigger": "Check Out & Check In",
     "carries": [
      "authorisationId",
      "bookingId"
     ],
     "provenance": "derived — BO-097 declares entryState.params authorisationId, bookingId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "CF-125. **A resource is a specific object, not a quantity** — forty identical strollers are forty rows, because guest twelve returned stroller twelve.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listResources` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Every bookable object at this venue, and whether it is free.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every resources",
       "bindsTo": "Resource",
       "columns": [
        "Resource.id",
        "Resource.code",
        "Resource.name",
        "Resource.kind",
        "Resource.venueId",
        "Resource.scopePath",
        "Resource.parentResourceId",
        "Resource.principalId",
        "Resource.attributes",
        "Resource.setupMinutes",
        "Resource.teardownMinutes",
        "Resource.requiresQualification"
       ],
       "operation": "listResources",
       "provenance": "contract resources.yaml GET /resources"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resources",
       "bindsTo": "Resource",
       "columns": [
        "Resource.id",
        "Resource.code",
        "Resource.name",
        "Resource.kind",
        "Resource.venueId",
        "Resource.scopePath",
        "Resource.parentResourceId",
        "Resource.principalId",
        "Resource.attributes",
        "Resource.setupMinutes",
        "Resource.teardownMinutes",
        "Resource.requiresQualification",
        "Resource.depositAmount",
        "Resource.status",
        "Resource.isActive"
       ],
       "operation": "listResources",
       "provenance": "contract resources.yaml GET /resources"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createResource",
       "provenance": "contract resources.yaml POST /resources"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search resources",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "multiSelect",
       "label": "Kind",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "bindsTo": "Resource[]",
       "notes": "Status column carries the reason — **booked and under repair need different responses from somebody looking for something free**",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "List skeleton; the count renders first",
   "error": "Could not load resources. Existing bookings are unaffected.",
   "emptyFirstRun": "No bookable resources yet. **A cabana sold as a product sells a slot** — define the object here and it becomes something a guest can be handed and can return.",
   "emptyNoResults": "No resource matches this kind or window. Widen the window rather than the kind — availability moves, definitions do not.",
   "emptyNoAccess": "You do not have RESOURCE_VIEW. The list is not empty."
  },
  "apis": [
   {
    "operationId": "listResources",
    "contract": "resources",
    "purpose": "Resources with status",
    "trigger": "onLoad"
   },
   {
    "operationId": "createResource",
    "contract": "resources",
    "purpose": "Define one",
    "trigger": "onAction",
    "invalidates": [
     "listResources"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Resource.id",
    "Resource.code",
    "Resource.name",
    "Resource.kind",
    "Resource.venueId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-095"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "acceptVenueLabelProposals": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/proposals",
  "contract": "venue-map",
  "summary": "Accept, edit or reject what the assistant suggested",
  "permission": "VENUE_MAP_MANAGE",
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
  "responds": "VenuePoint"
 },
 "callNextParties": {
  "method": "POST",
  "path": "/queues/{queueId}/call-next",
  "contract": "queue",
  "summary": "Call the next parties forward",
  "permission": "QUEUE_MANAGE",
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
 "createAsset": {
  "method": "POST",
  "path": "/assets",
  "contract": "maintenance",
  "summary": "Register an asset",
  "permission": "ASSET_MANAGE",
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
  "requestBody": "CreateAssetRequest",
  "responds": "Asset"
 },
 "createMaintenancePlan": {
  "method": "POST",
  "path": "/maintenance-plans",
  "contract": "maintenance",
  "summary": "Create a planned maintenance schedule",
  "permission": "ASSET_MANAGE",
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
  "requestBody": "MaintenancePlan",
  "responds": "MaintenancePlan"
 },
 "createQueue": {
  "method": "POST",
  "path": "/queues",
  "contract": "queue",
  "summary": "Create a queue",
  "permission": "QUEUE_MANAGE",
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
  "requestBody": "CreateQueueRequest",
  "responds": "Queue"
 },
 "createResource": {
  "method": "POST",
  "path": "/resources",
  "contract": "resources",
  "summary": "Define a bookable resource",
  "permission": "RESOURCE_MANAGE",
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
  "requestBody": "Resource",
  "responds": "Resource"
 },
 "createVenueMap": {
  "method": "POST",
  "path": "/venue-maps",
  "contract": "venue-map",
  "summary": "Start a map",
  "permission": "VENUE_MAP_MANAGE",
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
  "requestBody": "VenueMap",
  "responds": "VenueMap"
 },
 "getAsset": {
  "method": "GET",
  "path": "/assets/{assetId}",
  "contract": "maintenance",
  "summary": "Read an asset with history and documents",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AssetDetail"
 },
 "getAssetHistory": {
  "method": "GET",
  "path": "/assets/{assetId}/history",
  "contract": "maintenance",
  "summary": "Service history",
  "permission": "ASSET_VIEW",
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
 "getDueMaintenance": {
  "method": "GET",
  "path": "/maintenance-plans/due",
  "contract": "maintenance",
  "summary": "Planned tasks due or overdue",
  "permission": "ASSET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "withinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DueMaintenanceTask"
 },
 "getIncident": {
  "method": "GET",
  "path": "/incidents/{incidentId}",
  "contract": "maintenance",
  "summary": "Read an incident",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "IncidentDetail"
 },
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
 "getQueue": {
  "method": "GET",
  "path": "/queues/{queueId}",
  "contract": "queue",
  "summary": "Read a queue with live position",
  "permission": "QUEUE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "QueueDetail"
 },
 "getVenueMap": {
  "method": "GET",
  "path": "/venue-maps/{mapId}",
  "contract": "venue-map",
  "summary": "A map with its points and paths",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "version",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "VenueMapDetail"
 },
 "getVenueMapGraph": {
  "method": "GET",
  "path": "/venue-maps/{mapId}/graph",
  "contract": "venue-map",
  "summary": "The navigation graph, ready to route over",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "stepFreeOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "VenueMapGraph"
 },
 "getWaitTimes": {
  "method": "GET",
  "path": "/queues/wait-times",
  "contract": "queue",
  "summary": "Wait times across a venue",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": true
   },
   {
    "name": "category",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WaitTime"
 },
 "importVenueGeometry": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/import",
  "contract": "venue-map",
  "summary": "Read a drawing into shapes",
  "permission": "VENUE_MAP_MANAGE",
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
 "listAssets": {
  "method": "GET",
  "path": "/assets",
  "contract": "maintenance",
  "summary": "List assets",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "maintenanceDue",
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
 "listAuditRecords": {
  "method": "GET",
  "path": "/audit-records",
  "contract": "tenancy",
  "summary": "Who did what, where, and when",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "orgUnitId",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "action",
    "in": "query",
    "required": null
   },
   {
    "name": "subjectRef",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "listGames": {
  "method": "GET",
  "path": "/games",
  "contract": "games",
  "summary": "List games",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Game"
 },
 "listIncidents": {
  "method": "GET",
  "path": "/incidents",
  "contract": "maintenance",
  "summary": "List incidents",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "severity",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "isReportable",
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
 "listMaintenancePlans": {
  "method": "GET",
  "path": "/maintenance-plans",
  "contract": "maintenance",
  "summary": "List planned maintenance schedules",
  "permission": "ASSET_VIEW",
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
 "listQueueEntries": {
  "method": "GET",
  "path": "/queues/{queueId}/entries",
  "contract": "queue",
  "summary": "List entries in a queue",
  "permission": "QUEUE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
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
 "listQueues": {
  "method": "GET",
  "path": "/queues",
  "contract": "queue",
  "summary": "List queues",
  "permission": "QUEUE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "openOnly",
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
 "listResources": {
  "method": "GET",
  "path": "/resources",
  "contract": "resources",
  "summary": "Resources at this venue",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "availableFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "availableTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 },
 "listScans": {
  "method": "GET",
  "path": "/access/scans",
  "contract": "access",
  "summary": "List scan events",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "accessPointId",
    "in": "query",
    "required": null
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedTo",
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
 "listVenueMaps": {
  "method": "GET",
  "path": "/venue-maps",
  "contract": "venue-map",
  "summary": "Maps for this venue",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueMap"
 },
 "lookupAsset": {
  "method": "GET",
  "path": "/assets/lookup",
  "contract": "maintenance",
  "summary": "Find an asset by tag or QR",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assetTag",
    "in": "query",
    "required": null
   },
   {
    "name": "serialNumber",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AssetDetail"
 },
 "lookupTicket": {
  "method": "GET",
  "path": "/access/lookup",
  "contract": "access",
  "summary": "Read-only validity check without admitting",
  "permission": "TICKET_LOOKUP",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "mediaCode",
    "in": "query",
    "required": null
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TicketStatus"
 },
 "overrideAccess": {
  "method": "POST",
  "path": "/access/override",
  "contract": "access",
  "summary": "Admit against a failed validation",
  "permission": "ACCESS_OVERRIDE",
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
  "requestBody": null,
  "responds": "ValidationResult"
 },
 "proposeVenueLabels": {
  "method": "POST",
  "path": "/ai/venue-map/{mapId}/propose-labels",
  "contract": "ai",
  "summary": "Suggest what each extracted shape is",
  "permission": "VENUE_MAP_MANAGE",
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
 "publishVenueMap": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/publish",
  "contract": "venue-map",
  "summary": "Make the draft the one guests see",
  "permission": "VENUE_MAP_PUBLISH",
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
  "responds": "VenueMap"
 },
 "recordAuthorityNotification": {
  "method": "POST",
  "path": "/incidents/{incidentId}/notify-authority",
  "contract": "maintenance",
  "summary": "Record notification to an external authority",
  "permission": "INCIDENT_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Incident"
 },
 "recordGamePlay": {
  "method": "POST",
  "path": "/game-plays",
  "contract": "games",
  "summary": "Record a play",
  "permission": null,
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
  "requestBody": "RecordPlayRequest",
  "responds": "PlayResult"
 },
 "reportIncident": {
  "method": "POST",
  "path": "/incidents",
  "contract": "maintenance",
  "summary": "Report an incident",
  "permission": "INCIDENT_REPORT",
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
  "requestBody": "ReportIncidentRequest",
  "responds": "Incident"
 },
 "setAssetStatus": {
  "method": "PUT",
  "path": "/assets/{assetId}/status",
  "contract": "maintenance",
  "summary": "Take an asset out of service or return it",
  "permission": "ASSET_MANAGE",
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
  "requestBody": "SetAssetStatusRequest",
  "responds": "AssetStatusResult"
 },
 "setPathClosure": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/paths/{pathId}/closure",
  "contract": "venue-map",
  "summary": "Close a route during works or an incident",
  "permission": "VENUE_MAP_MANAGE",
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
  "responds": "VenuePath"
 },
 "setQueueStatus": {
  "method": "PUT",
  "path": "/queues/{queueId}/status",
  "contract": "queue",
  "summary": "Open, pause or close a queue",
  "permission": "QUEUE_MANAGE",
  "offlineCapable": true,
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
  "responds": "QueueStatusResult"
 },
 "setRolePermissions": {
  "method": "PUT",
  "path": "/roles/{roleId}/permissions",
  "contract": "tenancy",
  "summary": "What this role may do",
  "permission": "ROLE_MANAGE",
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
 "setVenuePoint": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/points",
  "contract": "venue-map",
  "summary": "Place or amend a point of interest",
  "permission": "VENUE_MAP_MANAGE",
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
  "requestBody": "VenuePoint",
  "responds": "VenuePoint"
 },
 "setWaitTime": {
  "method": "PUT",
  "path": "/queues/{queueId}/wait-time",
  "contract": "queue",
  "summary": "Manually set a wait time",
  "permission": "QUEUE_MANAGE",
  "offlineCapable": true,
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
  "responds": "WaitTime"
 },
 "syncGamePlays": {
  "method": "POST",
  "path": "/game-plays/sync",
  "contract": "games",
  "summary": "Replay plays recorded offline",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "syncScans": {
  "method": "POST",
  "path": "/access/scans",
  "contract": "access",
  "summary": "Replay scans recorded offline",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "ScanSyncResult"
 },
 "updateAsset": {
  "method": "PATCH",
  "path": "/assets/{assetId}",
  "contract": "maintenance",
  "summary": "Amend an asset",
  "permission": "ASSET_MANAGE",
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
  "responds": "Asset"
 },
 "updateGame": {
  "method": "PATCH",
  "path": "/games/{gameId}",
  "contract": "games",
  "summary": "Amend a game",
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
  "responds": "Game"
 },
 "updateIncident": {
  "method": "PATCH",
  "path": "/incidents/{incidentId}",
  "contract": "maintenance",
  "summary": "Investigate, escalate or close an incident",
  "permission": "INCIDENT_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Incident"
 },
 "updateQueue": {
  "method": "PATCH",
  "path": "/queues/{queueId}",
  "contract": "queue",
  "summary": "Amend queue configuration",
  "permission": "QUEUE_MANAGE",
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
  "responds": "Queue"
 },
 "validateAccess": {
  "method": "POST",
  "path": "/access/validate",
  "contract": "access",
  "summary": "Validate media at an access point and admit or deny",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ValidateRequest",
  "responds": "ValidationResult"
 },
 "validateGroupAccess": {
  "method": "POST",
  "path": "/access/group-validate",
  "contract": "access",
  "summary": "Admit a group on one read",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ValidationResult"
 },
 "validateVenueMapGraph": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/validate-graph",
  "contract": "venue-map",
  "summary": "What is unreachable, before anyone publishes it",
  "permission": "VENUE_MAP_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GraphValidation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Asset": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateAssetRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "resourceId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"
     },
     "acquisitionCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "acquiredOn": {
      "type": "string",
      "format": "date",
      "nullable": true
     },
     "depreciation": {
      "type": "object",
      "nullable": true,
      "description": "**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n",
      "properties": {
       "method": {
        "type": "string",
        "enum": [
         "straightLine",
         "reducingBalance",
         "unitsOfProduction",
         "none"
        ]
       },
       "usefulLifeMonths": {
        "type": "integer"
       },
       "residualValue": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "accumulatedDepreciation": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     },
     "retiredOn": {
      "type": "string",
      "format": "date",
      "nullable": true,
      "description": "**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"
     },
     "disposalProceeds": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "status": {
      "$ref": "#/components/schemas/AssetStatus"
     },
     "statusReason": {
      "type": "string",
      "nullable": true
     },
     "openWorkOrderCount": {
      "type": "integer"
     },
     "nextMaintenanceDueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "isMaintenanceOverdue": {
      "type": "boolean"
     },
     "lastInspectionAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "usageCounter": {
      "type": "number",
      "nullable": true,
      "description": "Cycles, hours or kilometres. Drives usage-based maintenance."
     }
    }
   }
  ]
 },
 "AssetCriticality": {
  "type": "string",
  "enum": [
   "safetyCritical",
   "revenueCritical",
   "standard",
   "low"
  ]
 },
 "AssetDetail": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/Asset"
   },
   {
    "type": "object",
    "properties": {
     "openWorkOrders": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/WorkOrder"
      }
     },
     "maintenancePlans": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/MaintenancePlan"
      }
     },
     "documents": {
      "type": "array",
      "description": "Manuals, procedures, certificates. What a technician needs on site.",
      "items": {
       "type": "object",
       "properties": {
        "ref": {
         "type": "string"
        },
        "name": {
         "type": "string"
        },
        "kind": {
         "type": "string",
         "enum": [
          "manual",
          "sop",
          "certificate",
          "warranty",
          "drawing",
          "riskAssessment"
         ]
        }
       }
      }
     }
    }
   }
  ]
 },
 "AssetStatus": {
  "type": "string",
  "enum": [
   "inService",
   "outOfService",
   "underMaintenance",
   "awaitingParts",
   "retired",
   "disposed"
  ]
 },
 "AssetStatusResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asset",
   "downstreamEffects"
  ],
  "properties": {
   "asset": {
    "$ref": "#/components/schemas/Asset"
   },
   "downstreamEffects": {
    "type": "object",
    "description": "What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n",
    "properties": {
     "productsSuspended": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "accessPointBlocked": {
      "type": "boolean"
     },
     "performancesAffected": {
      "type": "integer"
     },
     "workOrderId": {
      "type": "string",
      "nullable": true
     }
    }
   }
  }
 },
 "CreateAssetRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "assetTag",
   "name",
   "venueId",
   "criticality"
  ],
  "properties": {
   "assetTag": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "criticality": {
    "$ref": "#/components/schemas/AssetCriticality"
   },
   "manufacturer": {
    "type": "string",
    "maxLength": 200
   },
   "model": {
    "type": "string",
    "maxLength": 200
   },
   "serialNumber": {
    "type": "string",
    "maxLength": 128
   },
   "commissionedAt": {
    "type": "string",
    "format": "date"
   },
   "warrantyExpiresAt": {
    "type": "string",
    "format": "date"
   },
   "supplierId": {
    "type": "string",
    "format": "uuid"
   },
   "linkedProductIds": {
    "type": "array",
    "description": "Products this asset delivers. A fault here can stop them selling.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "linkedAccessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Access point this asset controls. Out of service blocks it."
   },
   "requiresInspectionToReturn": {
    "type": "boolean",
    "default": false,
    "description": "True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"
   },
   "documentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "CreateQueueRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "capacityPerCycle",
   "cycleMinutes"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "attractionProductId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "standby",
     "singleRider",
     "fastPass",
     "virtual",
     "accessible",
     "groupOnly",
     "staffOnly"
    ],
    "default": "standby",
    "description": "5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"
   },
   "operatingWindows": {
    "type": "array",
    "description": "**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\n",
    "items": {
     "type": "object",
     "properties": {
      "day": {
       "type": "string",
       "enum": [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun"
       ]
      },
      "from": {
       "type": "string"
      },
      "to": {
       "type": "string"
      },
      "lastEntryMinutesBefore": {
       "type": "integer",
       "default": 0,
       "description": "**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"
      }
     }
    }
   },
   "parentQueueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"
   },
   "loadBalanceWithQueueIds": {
    "type": "array",
    "description": "BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "inQueueOfferEnabled": {
    "type": "boolean",
    "default": false,
    "description": "**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"
   },
   "notifyBeforeCallMinutes": {
    "type": "integer",
    "default": 5,
    "description": "BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"
   },
   "capacityPerCycle": {
    "type": "integer",
    "minimum": 1
   },
   "cycleMinutes": {
    "type": "number",
    "minimum": 0
   },
   "maxPartySize": {
    "type": "integer",
    "default": 6
   },
   "returnWindowMinutes": {
    "type": "integer",
    "default": 15,
    "description": "How long a called party has to arrive before the entry expires."
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "fastPassAllocationPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "default": 0,
    "description": "Share of each cycle reserved for Fast Pass holders."
   },
   "zone": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "DenyReason": {
  "type": "string",
  "description": "Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n",
  "enum": [
   "notFound",
   "notYetValid",
   "expired",
   "alreadyUsed",
   "reentryLimitReached",
   "exitRequiredBeforeReentry",
   "wrongAccessPoint",
   "wrongPerformance",
   "outsideAdmissionWindow",
   "entitlementSuspended",
   "blacklisted",
   "capacityReached",
   "waiverRequired",
   "accompanimentRequired",
   "mediaDeactivated",
   "unpaid",
   "delegatedRightExhausted",
   "delegatedRightRevoked"
  ]
 },
 "Direction": {
  "type": "string",
  "enum": [
   "entry",
   "exit",
   "reentry",
   "crossover"
  ]
 },
 "DueMaintenanceTask": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "planId",
   "assetId",
   "assetName",
   "dueAt",
   "isOverdue",
   "criticality"
  ],
  "properties": {
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planName": {
    "type": "string"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "assetName": {
    "type": "string"
   },
   "criticality": {
    "$ref": "#/components/schemas/AssetCriticality"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "isOverdue": {
    "type": "boolean"
   },
   "daysOverdue": {
    "type": "integer"
   },
   "triggeredBy": {
    "type": "string",
    "enum": [
     "interval",
     "usage"
    ]
   },
   "workOrderId": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "Game": {
  "x-ticvai-persistence": "games.game",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "creditCost",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The machine. Taken out of service by maintenance, the game stops accepting play rather than swallowing credits.\n"
   },
   "readerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "creditCost": {
    "type": "integer",
    "minimum": 1
   },
   "minPointsAwarded": {
    "type": "integer"
   },
   "maxPointsAwarded": {
    "type": "integer"
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/GameStatus"
   },
   "playsToday": {
    "type": "integer"
   },
   "creditsTakenToday": {
    "type": "integer"
   },
   "pointsAwardedToday": {
    "type": "integer"
   }
  }
 },
 "GameStatus": {
  "type": "string",
  "enum": [
   "inService",
   "outOfService",
   "maintenance",
   "retired"
  ]
 },
 "GraphValidation": {
  "type": "object",
  "description": "**What breaks before a guest finds it.** Run at publish and on demand.\n",
  "required": [
   "isValid",
   "components"
  ],
  "properties": {
   "isValid": {
    "type": "boolean"
   },
   "components": {
    "type": "integer"
   },
   "unreachablePoints": {
    "type": "array",
    "description": "No path at all. **Usually a point placed after the paths were drawn.**",
    "items": {
     "type": "object",
     "properties": {
      "pointId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "kind": {
       "type": "string"
      }
     }
    }
   },
   "stepOnlyPoints": {
    "type": "array",
    "description": "Reachable, and only by steps. **The map works perfectly until a wheelchair user opens it**, and nothing in the drawing makes this visible — which is the whole reason for this list.\n",
    "items": {
     "type": "object",
     "properties": {
      "pointId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      }
     }
    }
   },
   "deadEndPaths": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "criticalUnreachable": {
    "type": "array",
    "description": "**First aid, emergency exits and assembly points that cannot be reached.** Separated from the rest because an unreachable gift shop is a defect and an unreachable assembly point is a safety finding, and a single list of two hundred items buries it.\n",
    "items": {
     "type": "object",
     "properties": {
      "pointId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "kind": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "Incident": {
  "x-ticvai-persistence": "maintenance.incident",
  "type": "object",
  "required": [
   "id",
   "incidentNumber",
   "kind",
   "severity",
   "status",
   "venueId",
   "occurredAt",
   "reportedByPrincipalId"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "incidentNumber": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/IncidentKind"
   },
   "severity": {
    "$ref": "#/components/schemas/IncidentSeverity"
   },
   "status": {
    "$ref": "#/components/schemas/IncidentStatus"
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
   "locationDescription": {
    "type": "string",
    "nullable": true
   },
   "isReportable": {
    "type": "boolean",
    "description": "Requires notification to an external authority within a statutory window."
   },
   "notificationDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reportedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "correctiveWorkOrderId": {
    "type": "string",
    "nullable": true
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
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
 "IncidentDetail": {
  "x-ticvai-persistence": "maintenance.incident",
  "allOf": [
   {
    "$ref": "#/components/schemas/Incident"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string",
      "description": "The original report. Never edited — investigation adds to the record."
     },
     "investigationNote": {
      "type": "string",
      "nullable": true
     },
     "rootCause": {
      "type": "string",
      "nullable": true
     },
     "correctiveActions": {
      "type": "string",
      "nullable": true
     },
     "firstAidGiven": {
      "type": "boolean"
     },
     "emergencyServicesCalled": {
      "type": "boolean"
     },
     "witnessCount": {
      "type": "integer"
     },
     "attachmentRefs": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "authorityNotifications": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "authority": {
         "type": "string"
        },
        "reference": {
         "type": "string",
         "nullable": true
        },
        "notifiedAt": {
         "type": "string",
         "format": "date-time"
        },
        "notifiedByPrincipalId": {
         "type": "string",
         "format": "uuid"
        }
       }
      }
     }
    }
   }
  ]
 },
 "IncidentKind": {
  "type": "string",
  "enum": [
   "guestInjury",
   "staffInjury",
   "nearMiss",
   "propertyDamage",
   "equipmentFailure",
   "securityIncident",
   "fireOrEvacuation",
   "foodSafety",
   "environmental",
   "other"
  ]
 },
 "IncidentSeverity": {
  "type": "string",
  "enum": [
   "nearMiss",
   "minor",
   "moderate",
   "major",
   "critical"
  ]
 },
 "IncidentStatus": {
  "type": "string",
  "enum": [
   "reported",
   "underInvestigation",
   "actionRequired",
   "closed"
  ]
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MaintenancePlan": {
  "x-ticvai-persistence": "maintenance.maintenance_plan",
  "type": "object",
  "required": [
   "id",
   "name",
   "assetId",
   "taskTemplate"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "assetCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Applies to every asset in the category rather than one."
   },
   "intervalDays": {
    "type": "integer",
    "nullable": true,
    "description": "Elapsed-time trigger."
   },
   "usageInterval": {
    "type": "number",
    "nullable": true,
    "description": "Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"
   },
   "leadTimeDays": {
    "type": "integer",
    "default": 7,
    "description": "How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"
   },
   "taskTemplate": {
    "type": "object",
    "required": [
     "title",
     "priority"
    ],
    "properties": {
     "title": {
      "type": "string"
     },
     "description": {
      "type": "string"
     },
     "priority": {
      "$ref": "#/components/schemas/WorkOrderPriority"
     },
     "estimatedMinutes": {
      "type": "integer"
     },
     "inspectionTemplateId": {
      "type": "string",
      "format": "uuid"
     },
     "requiredPartIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "lastCompletedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "nextDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "MediaKind": {
  "type": "string",
  "enum": [
   "image",
   "video",
   "audio",
   "document",
   "vector",
   "font",
   "archive"
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
   "entitlements": {
    "type": "array",
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
       "type": "string"
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
       "type": "string"
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
 "PlayResult": {
  "x-ticvai-persistence": "games.play",
  "type": "object",
  "required": [
   "playId",
   "creditsUsed",
   "pointsAwarded",
   "creditsRemaining",
   "pointsBalance"
  ],
  "properties": {
   "playId": {
    "type": "string"
   },
   "cardCode": {
    "type": "string"
   },
   "gameId": {
    "type": "string",
    "format": "uuid"
   },
   "creditsUsed": {
    "type": "integer"
   },
   "pointsAwarded": {
    "type": "integer"
   },
   "creditsRemaining": {
    "type": "integer"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "Queue": {
  "x-ticvai-persistence": "queue.queue",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateQueueRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status",
     "waitingPartyCount"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "status": {
      "$ref": "#/components/schemas/QueueStatus"
     },
     "statusReason": {
      "type": "string",
      "nullable": true
     },
     "waitingPartyCount": {
      "type": "integer"
     },
     "waitingGuestCount": {
      "type": "integer"
     },
     "currentWaitMinutes": {
      "type": "integer",
      "nullable": true
     },
     "waitTimeSource": {
      "$ref": "#/components/schemas/WaitTimeSource"
     },
     "expectedReopenAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "QueueDetail": {
  "x-ticvai-persistence": "queue.queue",
  "allOf": [
   {
    "$ref": "#/components/schemas/Queue"
   },
   {
    "type": "object",
    "properties": {
     "nowServingPartyNumber": {
      "type": "integer",
      "nullable": true
     },
     "lastCalledAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "throughputLastHour": {
      "type": "integer"
     },
     "noShowRatePercent": {
      "type": "number"
     },
     "feed": {
      "$ref": "#/components/schemas/QueueFeedHealth"
     }
    }
   }
  ]
 },
 "QueueFeedHealth": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "feedId",
   "isHealthy",
   "isQuiet"
  ],
  "properties": {
   "feedId": {
    "type": "string",
    "format": "uuid"
   },
   "adaptor": {
    "$ref": "#/components/schemas/QueueFeedAdaptor"
   },
   "isHealthy": {
    "type": "boolean"
   },
   "isQuiet": {
    "type": "boolean",
    "description": "No reading within the expected interval. The wait time falls back to throughput-derived and is marked stale rather than freezing at the last value.\n"
   },
   "lastReadingAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "readingsLastHour": {
    "type": "integer"
   },
   "discardedLastHour": {
    "type": "integer",
    "description": "Out-of-order or duplicate readings rejected."
   }
  }
 },
 "QueueStatus": {
  "type": "string",
  "enum": [
   "open",
   "paused",
   "closed",
   "atCapacity"
  ]
 },
 "QueueStatusResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "queue",
   "affectedEntries"
  ],
  "properties": {
   "queue": {
    "$ref": "#/components/schemas/Queue"
   },
   "affectedEntries": {
    "type": "object",
    "description": "What happened to guests already waiting. Closing releases and notifies them — a guest holding a position for a ride that will not run should be told.\n",
    "properties": {
     "released": {
      "type": "integer"
     },
     "held": {
      "type": "integer"
     },
     "notified": {
      "type": "integer"
     }
    }
   }
  }
 },
 "RecordPlayRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "cardCode",
   "gameId",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "cardCode": {
    "type": "string"
   },
   "gameId": {
    "type": "string",
    "format": "uuid"
   },
   "creditsUsed": {
    "type": "integer",
    "minimum": 1
   },
   "pointsAwarded": {
    "type": "integer",
    "minimum": 0
   },
   "sequence": {
    "type": "integer",
    "description": "Monotonic per reader. Preserves order across an offline batch."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ReportIncidentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "kind",
   "severity",
   "venueId",
   "description",
   "occurredAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "kind": {
    "$ref": "#/components/schemas/IncidentKind"
   },
   "severity": {
    "$ref": "#/components/schemas/IncidentSeverity"
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
   "description": {
    "type": "string",
    "minLength": 3,
    "maxLength": 10000
   },
   "involvedSubjectIds": {
    "type": "array",
    "description": "Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "involvedStaffPrincipalIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "witnessCount": {
    "type": "integer"
   },
   "firstAidGiven": {
    "type": "boolean",
    "default": false
   },
   "emergencyServicesCalled": {
    "type": "boolean",
    "default": false
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Resource": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource",
  "description": "**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId"
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
   "kind": {
    "type": "string",
    "enum": [
     "cabana",
     "locker",
     "wheelchair",
     "stroller",
     "equipment",
     "room",
     "auditorium",
     "vehicle",
     "instructor",
     "staff",
     "table",
     "pitch",
     "studio",
     "mealPlan",
     "other"
    ],
    "description": "BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\n**`mealPlan` is the exception and is listed here to be refused**: 5.5.8b groups it with lockers and parking, and a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "parentResourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a person resource. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true,
    "description": "Configurable per kind — capacity, size, shade, power, poolside."
   },
   "setupMinutes": {
    "type": "integer",
    "default": 0,
    "description": "**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"
   },
   "teardownMinutes": {
    "type": "integer",
    "default": 0
   },
   "requiresQualification": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Qualification codes a person must hold to be assigned to this."
   },
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "booked",
     "checkedOut",
     "maintenance",
     "retired"
    ]
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ScanOutcome": {
  "type": "string",
  "enum": [
   "admitted",
   "denied",
   "overridden"
  ]
 },
 "ScanSyncResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "accepted",
   "results"
  ],
  "properties": {
   "accepted": {
    "type": "integer",
    "description": "Entries processed before any stop."
   },
   "stoppedAtSequence": {
    "type": "integer",
    "nullable": true,
    "description": "Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"
   },
   "results": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "sequence",
      "status"
     ],
     "properties": {
      "id": {
       "type": "string"
      },
      "sequence": {
       "type": "integer"
      },
      "status": {
       "type": "string",
       "enum": [
        "accepted",
        "duplicate",
        "reconciled",
        "rejected"
       ]
      },
      "serverOutcome": {
       "$ref": "#/components/schemas/ScanOutcome"
      },
      "divergence": {
       "type": "string",
       "nullable": true,
       "description": "Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"
      },
      "error": {
       "$ref": "../shared/common.yaml#/components/schemas/Problem"
      }
     }
    }
   }
  }
 },
 "SetAssetStatusRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "status",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "status": {
    "$ref": "#/components/schemas/AssetStatus"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 1000
   },
   "inspectionId": {
    "type": "string",
    "nullable": true,
    "description": "Required for return to service where the asset demands it."
   },
   "raiseWorkOrder": {
    "type": "boolean",
    "default": false
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "TicketStatus": {
  "x-ticvai-persistence": "none — computed from entitlement and scans",
  "description": "**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n",
  "type": "object",
  "required": [
   "ticketId",
   "isValid"
  ],
  "properties": {
   "ticketId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Stable for the life of the ticket, independent of the media carrying it."
   },
   "mediaCode": {
    "type": "string",
    "nullable": true
   },
   "productName": {
    "type": "string"
   },
   "holderName": {
    "type": "string",
    "nullable": true,
    "description": "Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"
   },
   "isValid": {
    "type": "boolean"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "entriesUsed": {
    "type": "integer"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true,
    "description": "Null means unlimited."
   },
   "reentryAllowed": {
    "type": "boolean"
   },
   "isInsideVenue": {
    "type": "boolean",
    "description": "Derived from the last scan. Drives anti-passback evaluation."
   },
   "issuingCellId": {
    "type": "string",
    "nullable": true,
    "description": "Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   }
  }
 },
 "ValidateRequest": {
  "type": "object",
  "required": [
   "id",
   "mediaCode",
   "mediaKind",
   "direction",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key and dedupe key."
   },
   "mediaCode": {
    "type": "string",
    "maxLength": 256,
    "description": "What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"
   },
   "mediaKind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "groupSize": {
    "type": "integer",
    "minimum": 1,
    "description": "For group media admitting several holders on one read."
   },
   "proximityToken": {
    "type": "string",
    "description": "BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time of the read. Authoritative for ordering, not for validity."
   }
  }
 },
 "ValidationResult": {
  "x-ticvai-persistence": "none — computed, persisted as scan_event",
  "type": "object",
  "required": [
   "scanId",
   "outcome",
   "accessPointId",
   "recordedAt"
  ],
  "properties": {
   "scanId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "outcome": {
    "$ref": "#/components/schemas/ScanOutcome"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   },
   "denyDetail": {
    "type": "string",
    "description": "Human-readable, localised. For operator display, never for logic."
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "ticket": {
    "$ref": "#/components/schemas/TicketStatus"
   },
   "admittedCount": {
    "type": "integer",
    "description": "Holders admitted on this read. Differs from groupSize on partial admission."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "serverEvaluatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "VenueMap": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.map",
  "description": "A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n",
  "required": [
   "id",
   "name",
   "venueId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "park",
     "floor",
     "zone",
     "parking"
    ]
   },
   "floorLevel": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "archived"
    ]
   },
   "publishedVersion": {
    "type": "integer",
    "nullable": true
   },
   "isGeoreferenced": {
    "type": "boolean",
    "readOnly": true,
    "description": "**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"
   },
   "baseAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n",
    "x-ticvai-references": "assets.MediaAsset"
   },
   "baseImageAlignment": {
    "type": "object",
    "nullable": true,
    "description": "**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n",
    "properties": {
     "imageWidthPx": {
      "type": "integer"
     },
     "imageHeightPx": {
      "type": "integer"
     },
     "anchors": {
      "type": "array",
      "minItems": 2,
      "maxItems": 4,
      "items": {
       "type": "object",
       "properties": {
        "planX": {
         "type": "number"
        },
        "planY": {
         "type": "number"
        },
        "imageX": {
         "type": "number"
        },
        "imageY": {
         "type": "number"
        }
       }
      }
     }
    }
   },
   "tileSetRef": {
    "type": "string",
    "nullable": true,
    "description": "Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"
   },
   "boundsGeoJson": {
    "type": "string",
    "nullable": true
   },
   "graphStatus": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "notBuilt",
     "connected",
     "disconnected",
     "partial"
    ],
    "description": "**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"
   }
  }
 },
 "VenueMapDetail": {
  "type": "object",
  "description": "19.2.55. **The whole map in one call**, so a client caches it and filters locally.",
  "properties": {
   "map": {
    "$ref": "#/components/schemas/VenueMap"
   },
   "points": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/VenuePoint"
    }
   },
   "paths": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/VenuePath"
    }
   }
  }
 },
 "VenueMapGraph": {
  "type": "object",
  "description": "19.2.56. **What a client needs to route, and nothing more.** Small enough to cache, versioned so a stale route is detectable.\n",
  "required": [
   "mapId",
   "version",
   "nodes",
   "edges"
  ],
  "properties": {
   "mapId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "integer",
    "description": "**Bumped by a publish or a closure.** A client holding an older version knows its route may cross something that closed, and asking for the graph is cheaper than asking whether the graph changed.\n"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "nodes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "pointId": {
       "type": "string",
       "format": "uuid"
      },
      "x": {
       "type": "number"
      },
      "y": {
       "type": "number"
      },
      "kind": {
       "type": "string"
      },
      "isAccessible": {
       "type": "boolean"
      }
     }
    }
   },
   "edges": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "uuid"
      },
      "to": {
       "type": "string",
       "format": "uuid"
      },
      "distanceMetres": {
       "type": "number"
      },
      "isStepFree": {
       "type": "boolean"
      },
      "throughPointId": {
       "type": "string",
       "nullable": true,
       "description": "Where an access point restricts this edge. **The direction lives on that point**, not here, so a gate reconfigured to bidirectional changes routing without a map edit.\n"
      },
      "isClosed": {
       "type": "boolean"
      }
     }
    }
   },
   "components": {
    "type": "integer",
    "description": "How many disconnected parts. **One is the answer for a park.** More than one on a map that should be a single site means something is unreachable and the client can say so without walking the graph.\n"
   }
  }
 },
 "VenuePath": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.path",
  "description": "19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n",
  "required": [
   "id",
   "mapId",
   "fromPointId",
   "toPointId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "mapId": {
    "type": "string",
    "format": "uuid"
   },
   "fromPointId": {
    "type": "string",
    "format": "uuid"
   },
   "toPointId": {
    "type": "string",
    "format": "uuid"
   },
   "geometry": {
    "type": "string",
    "nullable": true,
    "description": "The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"
   },
   "distanceMetres": {
    "type": "number",
    "nullable": true,
    "description": "**Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"
   },
   "isStepFree": {
    "type": "boolean",
    "default": true,
    "description": "**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"
   },
   "isIndoor": {
    "type": "boolean",
    "default": false
   },
   "restrictedByPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"
   },
   "closedReason": {
    "type": "string",
    "nullable": true,
    "description": "Set during works or an incident. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"
   }
  }
 },
 "VenuePoint": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.point",
  "description": "19.2.57 to 19.2.60. **What a venue places on the map**, and what a guest taps.\n",
  "required": [
   "id",
   "mapId",
   "kind",
   "name",
   "position"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "mapId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "ride",
     "attraction",
     "show",
     "restaurant",
     "cafe",
     "shop",
     "kiosk",
     "toilet",
     "babyCare",
     "prayerRoom",
     "firstAid",
     "atm",
     "lockers",
     "entrance",
     "exit",
     "emergencyExit",
     "assemblyPoint",
     "parking",
     "guestServices",
     "smokingArea",
     "waterFountain",
     "chargingPoint",
     "photoSpot",
     "junction",
     "other"
    ],
    "description": "**A closed set, and `emergencyExit` is separate from `exit` on purpose.** An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them apart is a map that routes a normal departure through a fire door.\n**`junction` is the one that is not a point of interest.** A path connects two points, so a fork in a walkway with nothing at it still needs a node — otherwise every bend has to be named as a destination, and a guest browsing the map sees forty entries called *Path junction 12*.\n**Junctions are hidden from guests and present in the graph.** Generated by extraction where paths meet; a venue never places one by hand.\n"
   },
   "name": {
    "type": "string"
   },
   "nameLocalised": {
    "type": "object",
    "nullable": true,
    "additionalProperties": {
     "type": "string"
    }
   },
   "position": {
    "type": "object",
    "required": [
     "x",
     "y"
    ],
    "description": "Drawing coordinates. **Latitude and longitude are derived from the georeference**, not stored, so a map that is re-georeferenced does not need every point moved.\n",
    "properties": {
     "x": {
      "type": "number"
     },
     "y": {
      "type": "number"
     }
    }
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a restaurant, cafe, shop or kiosk. **Tapping it should open the menu**, and that only works if the map knows which outlet it is.\n"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a ride or show — links to wait times and to booking."
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"
   },
   "isAccessible": {
    "type": "boolean",
    "default": true,
    "description": "Step-free. **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"
   },
   "openingHours": {
    "type": "string",
    "nullable": true
   },
   "iconRef": {
    "type": "string",
    "nullable": true
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "isNavigable": {
    "type": "boolean",
    "default": true,
    "description": "Whether a route may pass through it. **False for a point that marks a place without being reachable** — a stage a guest cannot walk onto, a zone label.\n"
   },
   "isDestination": {
    "type": "boolean",
    "default": true,
    "description": "**Whether a guest may be routed *to* it, and whether it appears in a list of places.** False for a `junction`, which exists in the graph and nowhere else.\nSeparate from `isNavigable` because the two differ: a junction is navigable and not a destination, and a fenced landmark is a destination you can be shown but not walked into.\n"
   }
  }
 },
 "WaitTime": {
  "x-ticvai-persistence": "none — computed from readings and throughput",
  "type": "object",
  "required": [
   "queueId",
   "waitMinutes",
   "source",
   "asOf",
   "isStale"
  ],
  "properties": {
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "queueName": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "attractionProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/QueueStatus"
   },
   "waitMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "Null where the queue is closed or no estimate is available."
   },
   "source": {
    "$ref": "#/components/schemas/WaitTimeSource"
   },
   "isStale": {
    "type": "boolean",
    "description": "The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current.\n"
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WaitTimeSource": {
  "type": "string",
  "description": "Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n",
  "enum": [
   "sensor",
   "throughput",
   "manual",
   "unavailable"
  ]
 },
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
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
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n"
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
    "type": "string"
   },
   "workOrderNumber": {
    "type": "string"
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
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
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
   "elapsedMinutes": {
    "type": "integer"
   },
   "isTimerRunning": {
    "type": "boolean"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean"
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
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
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
 "WorkOrderPriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent",
   "emergency"
  ]
 }
}
```
