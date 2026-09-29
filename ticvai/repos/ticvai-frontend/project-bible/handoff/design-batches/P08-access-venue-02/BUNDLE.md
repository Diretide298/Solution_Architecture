# P08-access-venue-02 — P08 · Access & Venue (2 of 3)

**10 screens · 56 operations · 83 schemas · 21 permissions**

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

- **Every control that can be refused must be gated.** 21 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, ASSET_LIBRARY_VIEW, ASSET_MANAGE, ASSET_VIEW, AUDIT_VIEW, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, QUEUE_MANAGE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-034` | Scan Activity | listDetail | 7 | 4 | — |
| `BO-035` | Override Audit | listDetail | 8 | 4 | — |
| `BO-038` | Reconciliation Queue | listDetail | 9 | 5 | — |
| `BO-069` | Asset Register | listDetail | 11 | 6 | — |
| `BO-071` | Planned Maintenance | listDetail | 4 | 2 | — |
| `BO-072` | Incident Log | listDetail | 5 | 3 | — |
| `BO-092` | Venue Maps | listDetail | 2 | 1 | — |
| `BO-093` | Map Import & Labelling | configEditor | 5 | 1 | — |
| `BO-094` | Map Editor & Publish | statusTracker | 10 | 4 | — |
| `BO-095` | Resources | listDetail | 2 | 1 | — |

## Thin screens in this batch

**BO-092 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
    "BO-001"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId and BO-034 holds none of them, so the edge carries nothing and BO-001 opens cold"
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
       "kind": "textField",
       "label": "Access point id",
       "operation": "listScans",
       "notes": "Sends `?accessPointId=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "textField",
       "label": "Ticket id",
       "operation": "listScans",
       "notes": "Sends `?ticketId=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "textField",
       "label": "Outcome",
       "operation": "listScans",
       "notes": "Sends `?outcome=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "datePicker",
       "label": "Recorded from",
       "operation": "listScans",
       "notes": "Sends `?recordedFrom=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "datePicker",
       "label": "Recorded to",
       "operation": "listScans",
       "notes": "Sends `?recordedTo=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "dataTable",
       "label": "Every scan event",
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
        "ScanEvent.overridesScanId"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected scan event",
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
        "ScanEvent.overridesScanId",
        "ScanEvent.overrideReason",
        "ScanEvent.recordedAt",
        "ScanEvent.syncedAt"
       ],
       "operation": "listScans",
       "notes": "**An override is its own row** (decided 28 September, audit R228): outcome `overridden`, `operatorPrincipalId` is the supervisor who overrode, and `overridesScanId` links it to the denied scan, which is never updated. Selecting either row shows the other.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "detailPanel",
       "label": "The offline package",
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
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup ticket",
       "operation": "lookupTicket",
       "provenance": "contract access.yaml GET /access/lookup"
      },
      {
       "kind": "destructiveButton",
       "label": "Override access",
       "operation": "overrideAccess",
       "provenance": "contract access.yaml POST /access/override"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate access",
       "operation": "validateAccess",
       "provenance": "contract access.yaml POST /access/validate"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate group access",
       "operation": "validateGroupAccess",
       "provenance": "contract access.yaml POST /access/group-validate"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmOverrideAccess",
    "component": "confirmDialog",
    "trigger": "Override access",
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A scan activity this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
    "provenance": "contract access.yaml POST /access/override"
   },
   {
    "id": "formSyncScans",
    "component": "modal",
    "trigger": "Sync scans",
    "body": "**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sync scans",
     "operation": "syncScans"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "deviceId",
      "scans"
     ]
    },
    "provenance": "contract access.yaml POST /access/scans"
   },
   {
    "id": "formValidateAccess",
    "component": "modal",
    "trigger": "Validate access",
    "body": "**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ValidateRequest",
    "confirm": {
     "label": "Validate access",
     "operation": "validateAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "mediaCode",
      "mediaKind",
      "direction",
      "recordedAt",
      "groupSize",
      "proximityToken"
     ]
    },
    "provenance": "contract access.yaml POST /access/validate"
   },
   {
    "id": "formValidateGroupAccess",
    "component": "modal",
    "trigger": "Validate group access",
    "body": "**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Validate group access",
     "operation": "validateGroupAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "mediaCode",
      "admitCount",
      "recordedAt",
      "direction"
     ]
    },
    "provenance": "contract access.yaml POST /access/group-validate"
   }
  ],
  "states": {
   "loading": "The scan activity list.",
   "error": "Could not load. Names which read failed and leaves the scan activity untouched.",
   "emptyFirstRun": "No scan activity yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the scan activity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "ScanEvent.id",
    "ScanEvent.accessPointId",
    "ScanEvent.venueId",
    "ScanEvent.scopePath",
    "ScanEvent.ticketId"
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
    "BO-001"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId and BO-035 holds none of them, so the edge carries nothing and BO-001 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act",
  "purpose": "Review every admission that broke a rule.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Access point id",
       "operation": "listScans",
       "notes": "Sends `?accessPointId=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "textField",
       "label": "Ticket id",
       "operation": "listScans",
       "notes": "Sends `?ticketId=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "textField",
       "label": "Outcome",
       "operation": "listScans",
       "notes": "Sends `?outcome=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "datePicker",
       "label": "Recorded from",
       "operation": "listScans",
       "notes": "Sends `?recordedFrom=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "datePicker",
       "label": "Recorded to",
       "operation": "listScans",
       "notes": "Sends `?recordedTo=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "dataTable",
       "label": "Every scan event",
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
        "ScanEvent.overridesScanId"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "dataTable",
       "label": "Every audit",
       "bindsTo": "AuditRecord",
       "columns": [
        "AuditRecord.id",
        "AuditRecord.principalId",
        "AuditRecord.orgUnitId",
        "AuditRecord.workstationId",
        "AuditRecord.action",
        "AuditRecord.subjectRef",
        "AuditRecord.occurredAt"
       ],
       "operation": "listAuditRecords",
       "provenance": "contract tenancy.yaml GET /audit-records"
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected scan event",
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
        "ScanEvent.overridesScanId",
        "ScanEvent.overrideReason",
        "ScanEvent.recordedAt",
        "ScanEvent.syncedAt"
       ],
       "operation": "listScans",
       "notes": "**An override is its own row** (decided 28 September, audit R228): outcome `overridden`, `operatorPrincipalId` is the supervisor who overrode, and `overridesScanId` links it to the denied scan, which is never updated. Selecting either row shows the other.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "detailPanel",
       "label": "The offline package",
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
       "label": "Lookup ticket",
       "operation": "lookupTicket",
       "provenance": "contract access.yaml GET /access/lookup"
      },
      {
       "kind": "destructiveButton",
       "label": "Override access",
       "operation": "overrideAccess",
       "provenance": "contract access.yaml POST /access/override"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate access",
       "operation": "validateAccess",
       "provenance": "contract access.yaml POST /access/validate"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate group access",
       "operation": "validateGroupAccess",
       "provenance": "contract access.yaml POST /access/group-validate"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmOverrideAccess",
    "component": "confirmDialog",
    "trigger": "Override access",
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A override audit this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.",
    "provenance": "contract access.yaml POST /access/override"
   },
   {
    "id": "formSyncScans",
    "component": "modal",
    "trigger": "Sync scans",
    "body": "**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sync scans",
     "operation": "syncScans"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "deviceId",
      "scans"
     ]
    },
    "provenance": "contract access.yaml POST /access/scans"
   },
   {
    "id": "formValidateAccess",
    "component": "modal",
    "trigger": "Validate access",
    "body": "**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ValidateRequest",
    "confirm": {
     "label": "Validate access",
     "operation": "validateAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "mediaCode",
      "mediaKind",
      "direction",
      "recordedAt",
      "groupSize",
      "proximityToken"
     ]
    },
    "provenance": "contract access.yaml POST /access/validate"
   },
   {
    "id": "formValidateGroupAccess",
    "component": "modal",
    "trigger": "Validate group access",
    "body": "**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Validate group access",
     "operation": "validateGroupAccess"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "mediaCode",
      "admitCount",
      "recordedAt",
      "direction"
     ]
    },
    "provenance": "contract access.yaml POST /access/group-validate"
   }
  ],
  "states": {
   "loading": "The override audit list.",
   "error": "Could not load. Names which read failed and leaves the override audit untouched.",
   "emptyFirstRun": "No override audit yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the override audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "ScanEvent.id",
    "ScanEvent.accessPointId",
    "ScanEvent.venueId",
    "ScanEvent.scopePath",
    "ScanEvent.ticketId"
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
    "BO-001"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId and BO-038 holds feedId, queueId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listQueues` reads the population and `getQueue` reads one of them — list, select, act",
  "purpose": "Handle scans the server disagreed with.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listQueues",
       "notes": "Sends `?venueId=` to `listQueues`.",
       "provenance": "contract queue.yaml GET /queues"
      },
      {
       "kind": "toggle",
       "label": "Open only",
       "operation": "listQueues",
       "notes": "Sends `?openOnly=` to `listQueues`.",
       "provenance": "contract queue.yaml GET /queues"
      },
      {
       "kind": "dataTable",
       "label": "Every queue",
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
      },
      {
       "kind": "dataTable",
       "label": "Every waiting guest",
       "bindsTo": "WaitingGuest",
       "columns": [
        "WaitingGuest.id",
        "WaitingGuest.queueId",
        "WaitingGuest.queueName",
        "WaitingGuest.subjectId",
        "WaitingGuest.partyNumber",
        "WaitingGuest.partySize",
        "WaitingGuest.status",
        "WaitingGuest.positionInQueue",
        "WaitingGuest.partiesAhead",
        "WaitingGuest.estimatedCallAt",
        "WaitingGuest.isFastPass",
        "WaitingGuest.entitlementId"
       ],
       "operation": "listQueueEntries",
       "provenance": "contract queue.yaml GET /queues/{queueId}/entries"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected queue",
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
        "Queue.notifyBeforeCallMinutes",
        "Queue.capacityPerCycle",
        "Queue.cycleMinutes",
        "Queue.maxPartySize",
        "Queue.returnWindowMinutes"
       ],
       "operation": "listQueues",
       "provenance": "contract queue.yaml GET /queues"
      },
      {
       "kind": "detailPanel",
       "label": "The wait time",
       "bindsTo": "WaitTime",
       "columns": [
        "WaitTime.queueId",
        "WaitTime.queueName",
        "WaitTime.attractionProductId",
        "WaitTime.attractionCategoryId",
        "WaitTime.status",
        "WaitTime.waitMinutes",
        "WaitTime.source",
        "WaitTime.isStale",
        "WaitTime.heightRequirementCm",
        "WaitTime.zone",
        "WaitTime.asOf"
       ],
       "operation": "getWaitTimes",
       "provenance": "contract queue.yaml GET /queues/wait-times"
      },
      {
       "kind": "detailPanel",
       "label": "The queue",
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
       "label": "Create queue",
       "operation": "createQueue",
       "provenance": "contract queue.yaml POST /queues"
      },
      {
       "kind": "secondaryButton",
       "label": "Call next parties",
       "operation": "callNextParties",
       "provenance": "contract queue.yaml POST /queues/{queueId}/call-next"
      },
      {
       "kind": "secondaryButton",
       "label": "Save queue status",
       "operation": "setQueueStatus",
       "provenance": "contract queue.yaml PUT /queues/{queueId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Save wait time",
       "operation": "setWaitTime",
       "provenance": "contract queue.yaml PUT /queues/{queueId}/wait-time"
      },
      {
       "kind": "secondaryButton",
       "label": "Save queue",
       "operation": "updateQueue",
       "provenance": "contract queue.yaml PATCH /queues/{queueId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconciliation queue list.",
   "error": "Could not load. Names which read failed and leaves the reconciliation queue untouched.",
   "emptyFirstRun": "No reconciliation queue yet. Offers Create queue (`createQueue`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, openOnly and the reconciliation queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
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
    "Queue.code",
    "Queue.name",
    "Queue.venueId",
    "Queue.attractionProductId",
    "Queue.assetId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-038"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateQueue",
    "component": "modal",
    "trigger": "Create queue",
    "body": "**Collects what `createQueue` sends before it is called.** Required: `code`, `name`, `venueId`, `capacityPerCycle`, `cycleMinutes`. Optional: `attractionProductId`, `assetId`, `accessPointId`, `kind`, `operatingWindows`, `parentQueueId`, `loadBalanceWithQueueIds`, `inQueueOfferEnabled`, `notifyBeforeCallMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm` and 2 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateQueueRequest",
    "confirm": {
     "label": "Create queue",
     "operation": "createQueue"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "capacityPerCycle",
      "cycleMinutes",
      "attractionProductId",
      "assetId",
      "accessPointId",
      "kind",
      "operatingWindows",
      "parentQueueId",
      "loadBalanceWithQueueIds",
      "inQueueOfferEnabled",
      "notifyBeforeCallMinutes",
      "maxPartySize",
      "returnWindowMinutes",
      "heightRequirementCm",
      "fastPassAllocationPercent"
     ]
    },
    "provenance": "contract queue.yaml POST /queues"
   },
   {
    "id": "formCallNextParties",
    "component": "modal",
    "trigger": "Call next parties",
    "body": "**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Call next parties",
     "operation": "callNextParties"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "partyCount"
     ]
    },
    "provenance": "contract queue.yaml POST /queues/{queueId}/call-next"
   },
   {
    "id": "formSetQueueStatus",
    "component": "modal",
    "trigger": "Save queue status",
    "body": "**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save queue status",
     "operation": "setQueueStatus"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "reason",
      "guestMessage",
      "expectedReopenAt"
     ]
    },
    "provenance": "contract queue.yaml PUT /queues/{queueId}/status"
   },
   {
    "id": "formSetWaitTime",
    "component": "modal",
    "trigger": "Save wait time",
    "body": "**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save wait time",
     "operation": "setWaitTime"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "waitMinutes",
      "expiresInMinutes",
      "note"
     ]
    },
    "provenance": "contract queue.yaml PUT /queues/{queueId}/wait-time"
   },
   {
    "id": "formUpdateQueue",
    "component": "modal",
    "trigger": "Save queue",
    "body": "**Collects what `updateQueue` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacityPerCycle`, `cycleMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm`, `fastPassAllocationPercent`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save queue",
     "operation": "updateQueue"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "capacityPerCycle",
      "cycleMinutes",
      "maxPartySize",
      "returnWindowMinutes",
      "heightRequirementCm",
      "fastPassAllocationPercent"
     ]
    },
    "provenance": "contract queue.yaml PATCH /queues/{queueId}"
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
    "BO-070"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-070",
     "trigger": "Work Orders",
     "provenance": "VM close-out 29 September: maintenance home",
     "carries": [
      "workOrderId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAssets` reads the population and `getAsset` reads one of them — list, select, act",
  "purpose": "Know what equipment exists and where.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listAssets",
       "notes": "Sends `?venueId=` to `listAssets`.",
       "provenance": "contract maintenance.yaml GET /assets"
      },
      {
       "kind": "textField",
       "label": "Category id",
       "operation": "listAssets",
       "notes": "Sends `?categoryId=` to `listAssets`.",
       "provenance": "contract maintenance.yaml GET /assets"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listAssets",
       "notes": "Sends `?status=` to `listAssets`.",
       "provenance": "contract maintenance.yaml GET /assets"
      },
      {
       "kind": "toggle",
       "label": "Maintenance due",
       "operation": "listAssets",
       "notes": "Sends `?maintenanceDue=` to `listAssets`.",
       "provenance": "contract maintenance.yaml GET /assets"
      },
      {
       "kind": "dataTable",
       "label": "Every asset",
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
      },
      {
       "kind": "dataTable",
       "label": "Every game",
       "bindsTo": "Game",
       "columns": [
        "Game.id",
        "Game.code",
        "Game.name",
        "Game.venueId",
        "Game.zone",
        "Game.assetId",
        "Game.readerId",
        "Game.creditCost",
        "Game.minPointsAwarded",
        "Game.maxPointsAwarded",
        "Game.heightRequirementCm",
        "Game.status"
       ],
       "operation": "listGames",
       "provenance": "contract games.yaml GET /games"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupAsset",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset",
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
        "Asset.supplierId",
        "Asset.linkedProductIds",
        "Asset.linkedAccessPointId",
        "Asset.requiresInspectionToReturn",
        "Asset.documents"
       ],
       "operation": "listAssets",
       "provenance": "contract maintenance.yaml GET /assets"
      },
      {
       "kind": "detailPanel",
       "label": "The asset history entry",
       "bindsTo": "AssetHistoryEntry",
       "columns": [
        "AssetHistoryEntry.kind",
        "AssetHistoryEntry.referenceId",
        "AssetHistoryEntry.summary",
        "AssetHistoryEntry.principalId",
        "AssetHistoryEntry.occurredAt"
       ],
       "operation": "getAssetHistory",
       "provenance": "contract maintenance.yaml GET /assets/{assetId}/history"
      },
      {
       "kind": "detailPanel",
       "label": "The asset",
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
       "label": "Create asset",
       "operation": "createAsset",
       "provenance": "contract maintenance.yaml POST /assets"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup asset",
       "operation": "lookupAsset",
       "provenance": "contract maintenance.yaml GET /assets/lookup"
      },
      {
       "kind": "secondaryButton",
       "label": "Save asset status",
       "operation": "setAssetStatus",
       "provenance": "contract maintenance.yaml PUT /assets/{assetId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Save asset",
       "operation": "updateAsset",
       "provenance": "contract maintenance.yaml PATCH /assets/{assetId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save game",
       "operation": "updateGame",
       "provenance": "contract games.yaml PATCH /games/{gameId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Record game play",
       "operation": "recordGamePlay",
       "provenance": "contract games.yaml POST /game-plays"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync game plays",
       "operation": "syncGamePlays",
       "provenance": "contract games.yaml POST /game-plays/sync"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "selectField",
       "label": "Fault priority override",
       "bindsTo": "Asset.priorityOverride",
       "operation": "updateAsset",
       "notes": "**\"If this goes down, raise this priority\"** (decided 17 September, M17-01). A fault raised on this asset takes this priority instead of the venue's score. Empty means the score decides.",
       "provenance": "contract maintenance.yaml Asset.priorityOverride"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset register list.",
   "error": "Could not load. Names which read failed and leaves the asset register untouched.",
   "emptyFirstRun": "No asset register yet. Offers Create asset (`createAsset`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, categoryId, status, maintenanceDue and the asset register are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ASSET_VIEW`, which `listAssets` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
   },
   {
    "operationId": "lookupAsset",
    "contract": "maintenance",
    "purpose": "Find an asset by tag or QR",
    "trigger": "onAction"
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
    "Asset.assetTag",
    "Asset.name",
    "Asset.venueId",
    "Asset.categoryId",
    "Asset.locationDescription"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-069"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateAsset",
    "component": "modal",
    "trigger": "Create asset",
    "body": "**Collects what `createAsset` sends before it is called.** Required: `assetTag`, `name`, `venueId`, `criticality`. Optional: `categoryId`, `locationDescription`, `manufacturer`, `model`, `serialNumber`, `commissionedAt`, `warrantyExpiresAt`, `supplierId`, `linkedProductIds`, `linkedAccessPointId`, `requiresInspectionToReturn`, `documents` and 1 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateAssetRequest",
    "confirm": {
     "label": "Create asset",
     "operation": "createAsset"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "assetTag",
      "name",
      "venueId",
      "criticality",
      "categoryId",
      "locationDescription",
      "manufacturer",
      "model",
      "serialNumber",
      "commissionedAt",
      "warrantyExpiresAt",
      "supplierId",
      "linkedProductIds",
      "linkedAccessPointId",
      "requiresInspectionToReturn",
      "documents",
      "documentRefs",
      "priorityOverride"
     ]
    },
    "provenance": "contract maintenance.yaml POST /assets"
   },
   {
    "id": "formSetAssetStatus",
    "component": "modal",
    "trigger": "Save asset status",
    "body": "**Collects what `setAssetStatus` sends before it is called.** Required: `status`, `reason`, `recordedAt`. Optional: `inspectionId`, `raiseWorkOrder`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SetAssetStatusRequest",
    "confirm": {
     "label": "Save asset status",
     "operation": "setAssetStatus"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "reason",
      "recordedAt",
      "inspectionId",
      "raiseWorkOrder"
     ]
    },
    "provenance": "contract maintenance.yaml PUT /assets/{assetId}/status"
   },
   {
    "id": "formUpdateAsset",
    "component": "modal",
    "trigger": "Save asset",
    "body": "**Collects what `updateAsset` sends before it is called.** Nothing in the body is required. Optional: `name`, `locationDescription`, `categoryId`, `warrantyExpiresAt`, `supplierId`, `documents`, `documentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save asset",
     "operation": "updateAsset"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "locationDescription",
      "categoryId",
      "warrantyExpiresAt",
      "supplierId",
      "documents",
      "documentRefs",
      "priorityOverride"
     ]
    },
    "provenance": "contract maintenance.yaml PATCH /assets/{assetId}"
   },
   {
    "id": "formUpdateGame",
    "component": "modal",
    "trigger": "Save game",
    "body": "**Collects what `updateGame` sends before it is called.** Nothing in the body is required. Optional: `name`, `creditCost`, `minPointsAwarded`, `maxPointsAwarded`, `status`, `heightRequirementCm`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save game",
     "operation": "updateGame"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "creditCost",
      "minPointsAwarded",
      "maxPointsAwarded",
      "status",
      "heightRequirementCm"
     ]
    },
    "provenance": "contract games.yaml PATCH /games/{gameId}"
   },
   {
    "id": "formRecordGamePlay",
    "component": "modal",
    "trigger": "Record game play",
    "body": "**Collects what `recordGamePlay` sends before it is called.** Required: `id`, `cardCode`, `gameId`, `recordedAt`. Optional: `creditsUsed`, `pointsAwarded`, `sequence`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RecordPlayRequest",
    "confirm": {
     "label": "Record game play",
     "operation": "recordGamePlay"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "cardCode",
      "gameId",
      "recordedAt",
      "creditsUsed",
      "pointsAwarded",
      "sequence"
     ]
    },
    "provenance": "contract games.yaml POST /game-plays"
   },
   {
    "id": "formSyncGamePlays",
    "component": "modal",
    "trigger": "Sync game plays",
    "body": "**Collects what `syncGamePlays` sends before it is called.** Required: `readerId`, `plays`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sync game plays",
     "operation": "syncGamePlays"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "readerId",
      "plays"
     ]
    },
    "provenance": "contract games.yaml POST /game-plays/sync"
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
    "BO-070"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-070",
     "trigger": "Work Orders",
     "provenance": "VM close-out 29 September: maintenance home",
     "carries": [
      "workOrderId"
     ]
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
       "label": "Every maintenance plan",
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
       "label": "The selected maintenance plan",
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
      },
      {
       "kind": "detailPanel",
       "label": "The due maintenance task",
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
       "label": "Create maintenance plan",
       "operation": "createMaintenancePlan",
       "provenance": "contract maintenance.yaml POST /maintenance-plans"
      },
      {
       "kind": "secondaryButton",
       "label": "Save role permissions",
       "operation": "setRolePermissions",
       "provenance": "contract tenancy.yaml PUT /roles/{roleId}/permissions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The planned maintenance list.",
   "error": "Could not load. Names which read failed and leaves the planned maintenance untouched.",
   "emptyFirstRun": "No planned maintenance yet. Offers Create maintenance plan (`createMaintenancePlan`).",
   "emptyNoResults": "Never shown: `listMaintenancePlans` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `ASSET_VIEW`, which `listMaintenancePlans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "MaintenancePlan.id",
    "MaintenancePlan.name",
    "MaintenancePlan.assetId",
    "MaintenancePlan.assetCategoryId",
    "MaintenancePlan.intervalDays"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-071"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateMaintenancePlan",
    "component": "modal",
    "trigger": "Create maintenance plan",
    "body": "**Collects what `createMaintenancePlan` sends before it is called.** Required: `id`, `name`, `assetId`, `taskTemplate`. Optional: `assetCategoryId`, `intervalDays`, `usageInterval`, `leadTimeDays`, `lastCompletedAt`, `nextDueAt`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "MaintenancePlan",
    "confirm": {
     "label": "Create maintenance plan",
     "operation": "createMaintenancePlan"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "name",
      "assetId",
      "taskTemplate",
      "assetCategoryId",
      "intervalDays",
      "usageInterval",
      "leadTimeDays",
      "lastCompletedAt",
      "nextDueAt",
      "isActive"
     ]
    },
    "provenance": "contract maintenance.yaml POST /maintenance-plans"
   },
   {
    "id": "formSetRolePermissions",
    "component": "modal",
    "trigger": "Save role permissions",
    "body": "**Collects what `setRolePermissions` sends before it is called.** Required: `permissions`. Optional: `inheritsFromRoleId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save role permissions",
     "operation": "setRolePermissions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permissions",
      "inheritsFromRoleId"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /roles/{roleId}/permissions"
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
    "BO-070"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-070",
     "trigger": "Work Orders",
     "provenance": "VM close-out 29 September: maintenance home"
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
       "kind": "textField",
       "label": "Severity",
       "operation": "listIncidents",
       "notes": "Sends `?severity=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listIncidents",
       "notes": "Sends `?status=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "toggle",
       "label": "Is reportable",
       "operation": "listIncidents",
       "notes": "Sends `?isReportable=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "dataTable",
       "label": "Every incident",
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
       "label": "The selected incident",
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
        "Incident.assignedToPrincipalId",
        "Incident.reportedByPrincipalId",
        "Incident.correctiveWorkOrderId",
        "Incident.occurredAt",
        "Incident.recordedAt"
       ],
       "operation": "listIncidents",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "detailPanel",
       "label": "The incident",
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
       "label": "Report incident",
       "operation": "reportIncident",
       "provenance": "contract maintenance.yaml POST /incidents"
      },
      {
       "kind": "secondaryButton",
       "label": "Record authority notification",
       "operation": "recordAuthorityNotification",
       "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
      },
      {
       "kind": "secondaryButton",
       "label": "Save incident",
       "operation": "updateIncident",
       "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The incident log list.",
   "error": "Could not load. Names which read failed and leaves the incident log untouched.",
   "emptyFirstRun": "No incident log yet. Offers Record authority notification (`recordAuthorityNotification`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on severity, status, isReportable and the incident log are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "Incident.id",
    "Incident.incidentNumber",
    "Incident.kind",
    "Incident.severity",
    "Incident.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-072"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formReportIncident",
    "component": "modal",
    "trigger": "Report incident",
    "body": "**Collects what `reportIncident` sends before it is called.** Required: `id`, `kind`, `severity`, `venueId`, `description`, `occurredAt`, `recordedAt`. Optional: `assetId`, `locationDescription`, `involvedSubjectIds`, `involvedStaffPrincipalIds`, `witnessCount`, `firstAidGiven`, `emergencyServicesCalled`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ReportIncidentRequest",
    "confirm": {
     "label": "Report incident",
     "operation": "reportIncident"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "severity",
      "venueId",
      "description",
      "occurredAt",
      "recordedAt",
      "assetId",
      "locationDescription",
      "involvedSubjectIds",
      "involvedStaffPrincipalIds",
      "witnessCount",
      "firstAidGiven",
      "emergencyServicesCalled",
      "attachmentRefs"
     ]
    },
    "provenance": "contract maintenance.yaml POST /incidents"
   },
   {
    "id": "formRecordAuthorityNotification",
    "component": "modal",
    "trigger": "Record authority notification",
    "body": "**Collects what `recordAuthorityNotification` sends before it is called.** Required: `authority`, `notifiedAt`. Optional: `reference`, `notifiedByPrincipalId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record authority notification",
     "operation": "recordAuthorityNotification"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "authority",
      "notifiedAt",
      "reference",
      "notifiedByPrincipalId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
   },
   {
    "id": "formUpdateIncident",
    "component": "modal",
    "trigger": "Save incident",
    "body": "**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save incident",
     "operation": "updateIncident"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "severity",
      "assignedToPrincipalId",
      "investigationNote",
      "rootCause",
      "correctiveActions",
      "correctiveWorkOrderId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
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
     "provenance": "derived — BO-094 declares entryState.params mapId, pathId and BO-092 holds none of them, so the edge carries nothing and BO-094 opens cold"
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
       "label": "Every venue map",
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
       "label": "The selected venue map",
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
       "label": "Create venue map",
       "operation": "createVenueMap",
       "provenance": "contract venue-map.yaml POST /venue-maps"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue maps list.",
   "error": "Could not load. Names which read failed and leaves the venue maps untouched.",
   "emptyFirstRun": "No venue maps yet. Offers Create venue map (`createVenueMap`).",
   "emptyNoResults": "Never shown: `listVenueMaps` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `VENUE_MAP_VIEW`, which `listVenueMaps` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "derivedFrom": "wireframes/reference/Seat Board 2.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateVenueMap",
    "component": "modal",
    "trigger": "Create venue map",
    "body": "**Collects what `createVenueMap` sends before it is called.** Required: `id`, `name`, `venueId`, `status`. Optional: `scopePath`, `kind`, `floorLevel`, `publishedVersion`, `graphVersion`, `isGeoreferenced`, `baseAssetId`, `baseImageAlignment`, `tileSetRef`, `boundsGeoJson`, `graphStatus`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "VenueMap",
    "confirm": {
     "label": "Create venue map",
     "operation": "createVenueMap"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "name",
      "venueId",
      "status",
      "scopePath",
      "kind",
      "floorLevel",
      "publishedVersion",
      "graphVersion",
      "isGeoreferenced",
      "baseAssetId",
      "baseImageAlignment",
      "tileSetRef",
      "boundsGeoJson",
      "graphStatus"
     ]
    },
    "provenance": "contract venue-map.yaml POST /venue-maps"
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
     "provenance": "flow F26 step 3→4",
     "carries": [
      "mapId"
     ]
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
  "purpose": "Upload a plan, check what was read, and review what the assistant suggests; on a map that carries bookable places, also read the cabanas, loungers and tables and join them to what they sell as (decided 29 September, rev 3 REV3-15 and GAP-C2).",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Import venue geometry",
       "operation": "importVenueGeometry",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "secondaryButton",
       "label": "Propose venue labels",
       "operation": "proposeVenueLabels",
       "notes": "**Block A, bound here** (decided 29 September, AI2 review finding on BO-093). No-data AI: it reads only the shapes the import extracted, proposes, and stops; `acceptVenueLabelProposals` is the human half. When AI is off the button is hidden and the operator labels by hand on BO-094.",
       "provenance": "contract ai.yaml POST /ai/venue-map/{mapId}/propose-labels"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept venue label proposals",
       "operation": "acceptVenueLabelProposals",
       "notes": "**Accept, edit or reject, per proposal** (decided 28 September, audit R275 (f)) — each row of the review carries its own decision; an edit sends the operator's corrected point.",
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
       "kind": "selectField",
       "label": "Format",
       "operation": "importVenueGeometry",
       "notes": "Required.",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "textField",
       "label": "Source ref",
       "operation": "importVenueGeometry",
       "notes": "Required.",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "textField",
       "label": "Layer mapping",
       "operation": "importVenueGeometry",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "toggle",
       "label": "Digit normalisation",
       "operation": "importVenueGeometry",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "textField",
       "label": "Georeference",
       "operation": "importVenueGeometry",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "textField",
       "label": "Manifest ref",
       "operation": "importVenueGeometry",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "textField",
       "label": "Resource layer",
       "operation": "importVenueGeometry",
       "notes": "`layerMapping.resourceLayer`: the drawing layers that hold the bookable places (decided 29 September, rev 3 REV3-15). Absent, the accepted names in the venue-map input spec are matched.",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "fileUpload",
       "label": "Resource manifest",
       "operation": "importVenueGeometry",
       "notes": "`resourceManifestRef`: one sheet, header on row 3, five columns (Label, Kind, Zone, Capacity, Price band), uploaded through the asset library like the drawing. **Kind is cabana, lounger, table, pitch or other**; a table here is a non-dining spot sold like a cabana, and a restaurant table stays an F&B reservation (decided 29 September, rev 3 GAP-C2).",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "dataTable",
       "label": "Price bands",
       "operation": "importVenueGeometry",
       "notes": "`priceBands`: each band code the manifest uses and the catalogue product variant that prices it (Family 6, Medium 10, Large 15, XL 20 on the Coastal Aqua map). **The price is the variant's**; the map holds none.",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "toggle",
       "label": "Create missing resources",
       "operation": "importVenueGeometry",
       "notes": "`createMissingResources`, **off by default**: where a manifest label has no resource with that code at this venue, create one instead of reporting `resourceCodeUnmatched`. Off, a mistyped label is a finding rather than a new cabana.",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/import"
      },
      {
       "kind": "detailPanel",
       "label": "What the import read",
       "bindsTo": "VenueMapImportJob",
       "columns": [
        "VenueMapImportJob.status",
        "VenueMapImportJob.outcome",
        "VenueMapImportJob.shapesFound",
        "VenueMapImportJob.layersFound",
        "VenueMapImportJob.unmappedLayers",
        "VenueMapImportJob.manifestRowsRead",
        "VenueMapImportJob.resourcesFound",
        "VenueMapImportJob.resourceRowsJoined",
        "VenueMapImportJob.manifestRowsJoined",
        "VenueMapImportJob.findings"
       ],
       "operation": "getVenueMapImportJob",
       "notes": "Polled while the import runs. **The resource findings are listed apart** from the geometry ones (a manifest row with no shape, a shape with no row, a label with no resource, a band with no variant), each naming the row or the label, so an operator can fix the sheet rather than guess.",
       "provenance": "contract venue-map.yaml GET /venue-maps/{mapId}/import/{jobId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved map import labelling.",
   "error": "Could not load. Names which read failed and leaves the map import labelling untouched.",
   "emptyNoResults": "An import that read no resources on a map meant to carry them says so (`resourcesFound` 0) and names the resource layer it looked for, rather than showing an empty price-band table.",
   "emptyFirstRun": "No map import labelling configured. The form opens empty and `importVenueGeometry` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `VENUE_MAP_MANAGE`, which `importVenueGeometry` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "purpose": "Accept, edit or reject each label proposal (audit R275 (f))",
    "trigger": "onAction"
   },
   {
    "operationId": "getVenueMapImportJob",
    "contract": "venue-map",
    "purpose": "What the import read, including the resources it found and joined (rev 3 REV3-15)",
    "trigger": "onAction"
   },
   {
    "operationId": "acceptWalkwayProposals",
    "contract": "venue-map",
    "purpose": "Accept or reject proposed walkways",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "getVenueMapImportJob"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mapId",
     "from": "deepLink"
    },
    {
     "name": "jobId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mapId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-093",
   "derivedFrom": "wireframes/reference/Seat Board 1.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAcceptVenueLabelProposals",
    "component": "modal",
    "trigger": "Accept venue label proposals",
    "body": "**Collects what `acceptVenueLabelProposals` sends before it is called.** Required: `decisions` — one per proposal, each `accept`, `edit` or `reject` (decided 28 September, audit R275 (f)). An `edit` carries the corrected `point`; a reject writes nothing to the map. Decisions are per proposal, never all-or-nothing. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Accept venue label proposals",
     "operation": "acceptVenueLabelProposals"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decisions"
     ]
    },
    "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/proposals"
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
     "back": false,
     "carries": [
      "mapId"
     ]
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
  "purpose": "Place booths, toilets, exits, rides and restaurants, and the cabanas, loungers and tables guests book from the map, then publish.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The venue map",
       "bindsTo": "VenueMapDetail",
       "columns": [
        "VenueMapDetail.map",
        "VenueMapDetail.points",
        "VenueMapDetail.paths"
       ],
       "operation": "getVenueMap",
       "provenance": "contract venue-map.yaml GET /venue-maps/{mapId}"
      },
      {
       "kind": "detailPanel",
       "label": "The venue map graph",
       "bindsTo": "VenueMapGraph",
       "columns": [
        "VenueMapGraph.mapId",
        "VenueMapGraph.generatedAt",
        "VenueMapGraph.nodes",
        "VenueMapGraph.edges",
        "VenueMapGraph.components"
       ],
       "operation": "getVenueMapGraph",
       "provenance": "contract venue-map.yaml GET /venue-maps/{mapId}/graph"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishVenueMap",
       "notes": "**Publishing a map moves people.** The gate names what changes before it happens — which routes, which closures, which points become unreachable.\n",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Bookable places on the map",
       "bindsTo": "VenueMapDetail",
       "columns": [
        "VenueMapDetail.resources"
       ],
       "operation": "getVenueMap",
       "notes": "**Each placed resource with its label, kind, zone, capacity and price band** (decided 29 September, rev 3 REV3-15, superseding audit R073 (c) for resources on an ingested map). Guests pick one of these on the map and buy it. A place with no linked resource or no price band is marked, because publishing will refuse it.",
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
       "label": "Save venue point",
       "operation": "setVenuePoint",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/points"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish venue map",
       "operation": "publishVenueMap",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate venue map graph",
       "operation": "validateVenueMapGraph",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/validate-graph"
      },
      {
       "kind": "secondaryButton",
       "label": "Save path closure",
       "operation": "setPathClosure",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/paths/{pathId}/closure"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save. **Lists the resource blockers apart** (decided 29 September, rev 3 REV3-15): `resourceUnlinked` (no resource), `resourcePriceBandMissing` (no band, or a band with no variant) and `duplicateResourceLabel`, each naming the place; `validateVenueMapGraph` reports the same as resource findings before anyone presses Publish.",
       "provenance": "authored — required by check-screens"
      },
      {
       "kind": "secondaryButton",
       "label": "Place resource",
       "operation": "setPlacedResource",
       "notes": "Places or amends a cabana, lounger, table (a non-dining spot; restaurant tables stay F&B reservations, rev 3 GAP-C2), pitch or other bookable place and links it to its `resources.Resource`. Bookings follow the resource, not the placement, so moving a cabana on a later version keeps its bookings.",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/resources"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "textField",
       "label": "Item description",
       "bindsTo": "VenuePoint.description",
       "operation": "setVenuePoint",
       "notes": "**What the guest reads on Item Detail** (decided 29 September, MOB-4): rides, shows, restaurants and shops. Per language.",
       "provenance": "agreed name venue-map VenuePoint.description (P29 brief)"
      },
      {
       "kind": "multiSelect",
       "label": "Photos and video",
       "bindsTo": "VenuePoint.media",
       "operation": "searchMedia",
       "notes": "From the asset library; the first is the gallery cover on GST-004 Item Detail (MOB-4).",
       "provenance": "agreed name venue-map VenuePoint.media (P29 brief)"
      },
      {
       "kind": "selectField",
       "label": "Featured offer",
       "bindsTo": "VenuePoint.featuredOffer",
       "operation": "listProducts",
       "notes": "**The product or bundle the item detail proposes** (decided 29 September, MOB-4), on any kind of point, e.g. a restaurant's *meal combo with admission* (a bundle from BO-011). Products from `listProducts`, bundles from `listCatalogueBundles`.",
       "provenance": "agreed name venue-map VenuePoint.featuredOffer (P29 brief)"
      },
      {
       "kind": "numberField",
       "label": "Typical visit (minutes)",
       "bindsTo": "VenuePoint.typicalDurationMinutes",
       "operation": "setVenuePoint",
       "notes": "What the Plan tab's planner allows for this stop (MOB-6).",
       "provenance": "agreed name venue-map VenuePoint.typicalDurationMinutes (P29 brief)"
      },
      {
       "kind": "multiSelect",
       "label": "Interests",
       "bindsTo": "VenuePoint.interestTags",
       "operation": "setVenuePoint",
       "notes": "Matched against the guest's interests on the Plan tab (MOB-6).",
       "provenance": "agreed name venue-map VenuePoint.interestTags (P29 brief)"
      },
      {
       "kind": "multiSelect",
       "label": "Cuisine",
       "bindsTo": "VenuePoint.cuisineTags",
       "operation": "setVenuePoint",
       "notes": "For restaurants and kiosks; matched against the guest's cuisine choice on the Plan tab (MOB-6).",
       "provenance": "agreed name venue-map VenuePoint.cuisineTags (P29 brief)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The map editor publish, read by `getVenueMap`.",
   "error": "Could not load. Names which read failed and leaves the map editor publish untouched.",
   "emptyFirstRun": "No map editor publish yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `VENUE_MAP_VIEW`, which `getVenueMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "Pick an item's photos and video (MOB-4)",
    "trigger": "onAction",
    "provenance": "decided 29 September, MOB-4 (P29)"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "Products a point can feature (MOB-4)",
    "trigger": "onAction",
    "provenance": "decided 29 September, MOB-4 (P29)"
   },
   {
    "operationId": "listCatalogueBundles",
    "contract": "catalogue",
    "purpose": "Bundles a point can feature, e.g. a meal combo (MOB-4)",
    "trigger": "onAction",
    "provenance": "decided 29 September, MOB-4 (P29)"
   },
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
   },
   {
    "operationId": "setPlacedResource",
    "contract": "venue-map",
    "purpose": "Place or amend a bookable place and link it to its resource (rev 3 REV3-15)",
    "trigger": "onAction",
    "invalidates": [
     "getVenueMap"
    ]
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
   "derivedFrom": "wireframes/reference/Seat Board 1.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetVenuePoint",
    "component": "modal",
    "trigger": "Save venue point",
    "body": "**Collects what `setVenuePoint` sends before it is called.** Required: `id`, `mapId`, `kind`, `name`, `position`. Optional: `nameLocalised`, `outletId`, `productId`, `accessPointId`, `isStepFree`, `openingHours`, `iconRef`, `isActive`, `isNavigable`, `isDestination`, `pointId`; and the item details decided 29 September (MOB-4, MOB-6): `description`, `media`, `featuredOffer` (a product or a bundle, on any kind of point), `typicalDurationMinutes`, `interestTags`, `cuisineTags`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SetVenuePointRequest",
    "confirm": {
     "label": "Save venue point",
     "operation": "setVenuePoint"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "mapId",
      "kind",
      "name",
      "position",
      "nameLocalised",
      "outletId",
      "productId",
      "accessPointId",
      "isStepFree",
      "openingHours",
      "iconRef",
      "isActive",
      "isNavigable",
      "isDestination",
      "pointId",
      "description",
      "media",
      "featuredOffer",
      "typicalDurationMinutes",
      "interestTags",
      "cuisineTags"
     ]
    },
    "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/points"
   },
   {
    "id": "formPublishVenueMap",
    "component": "modal",
    "trigger": "Publish venue map",
    "body": "**Collects what `publishVenueMap` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Publish venue map",
     "operation": "publishVenueMap"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "note"
     ]
    },
    "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/publish"
   },
   {
    "id": "formSetPathClosure",
    "component": "modal",
    "trigger": "Save path closure",
    "body": "**Collects what `setPathClosure` sends before it is called.** Required: `isClosed`. Optional: `reason` (maintenance, incident, event, weather, crowding, other), `note`, `force`, `expectedReopenAt`. **Choosing Other makes the note required** — the form will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save path closure",
     "operation": "setPathClosure"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "isClosed",
      "reason",
      "note",
      "force",
      "expectedReopenAt"
     ]
    },
    "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/paths/{pathId}/closure"
   },
   {
    "id": "formSetPlacedResource",
    "component": "modal",
    "trigger": "Place resource",
    "body": "**Collects what `setPlacedResource` sends before it is called.** `resourceId` (the resource it is), `label` (what the guest taps, e.g. B09; unique on the map), `kind` (cabana, lounger, table, pitch, other), `zone`, `capacity` (1 to 500, checked against the party at hold), `priceBandCode` (one of the bands given at import; its variant prices it), `position` or `boundary`, `isBookable`; `placedResourceId` to amend one. Decided 29 September, rev 3 REV3-15. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SetPlacedResourceRequest",
    "confirm": {
     "label": "Place resource",
     "operation": "setPlacedResource"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "resourceId",
      "label",
      "kind",
      "zone",
      "capacity",
      "priceBandCode",
      "position",
      "boundary",
      "isBookable",
      "placedResourceId"
     ]
    },
    "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/resources"
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
    "BO-097",
    "BO-098"
   ],
   "transitions": [
    {
     "to": "BO-096",
     "trigger": "Resource Calendar",
     "carries": [
      "resourceId"
     ],
     "provenance": "derived — BO-096 declares entryState.params resourceId and BO-095 holds resourceId, so an edge into it carries them"
    },
    {
     "to": "BO-097",
     "trigger": "Check Out & Check In",
     "provenance": "derived — BO-097 declares entryState.params authorisationId, bookingId and BO-095 holds none of them, so the edge carries nothing and BO-097 opens cold"
    },
    {
     "to": "BO-098",
     "trigger": "Qualifications",
     "carries": [
      "resourceId"
     ],
     "provenance": "derived — BO-098 declares entryState.params resourceId and BO-095 holds resourceId, so an edge into it carries them"
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
       "kind": "textField",
       "label": "Kind",
       "operation": "listResources",
       "notes": "Sends `?kind=` to `listResources`.",
       "provenance": "contract resources.yaml GET /resources"
      },
      {
       "kind": "datePicker",
       "label": "Available from",
       "operation": "listResources",
       "notes": "Sends `?availableFrom=` to `listResources`.",
       "provenance": "contract resources.yaml GET /resources"
      },
      {
       "kind": "datePicker",
       "label": "Available to",
       "operation": "listResources",
       "notes": "Sends `?availableTo=` to `listResources`.",
       "provenance": "contract resources.yaml GET /resources"
      },
      {
       "kind": "dataTable",
       "label": "Every resource",
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
      },
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
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource",
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
       "label": "Create resource",
       "operation": "createResource",
       "provenance": "contract resources.yaml POST /resources"
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
  "overlays": [
   {
    "id": "formCreateResource",
    "component": "modal",
    "trigger": "Create resource",
    "body": "**Collects what `createResource` sends before it is called.** Required: `id`, `code`, `name`, `kind`, `venueId`. Optional: `scopePath`, `parentResourceId`, `principalId`, `attributes`, `setupMinutes`, `teardownMinutes`, `requiresQualification`, `depositAmount`, `status`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Resource",
    "confirm": {
     "label": "Create resource",
     "operation": "createResource"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "kind",
      "venueId",
      "scopePath",
      "parentResourceId",
      "principalId",
      "attributes",
      "setupMinutes",
      "teardownMinutes",
      "requiresQualification",
      "depositAmount",
      "status",
      "isActive"
     ]
    },
    "provenance": "contract resources.yaml POST /resources"
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
 "acceptWalkwayProposals": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/walkway-proposals",
  "contract": "venue-map",
  "summary": "Accept or reject proposed walkways",
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
  "responds": "GraphValidation"
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
   },
   {
    "name": "categoryId",
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
   },
   {
    "name": "draft",
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
    "name": "draft",
    "in": "query",
    "required": null
   },
   {
    "name": "stepFreeOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "VenueMapGraph"
 },
 "getVenueMapImportJob": {
  "method": "GET",
  "path": "/venue-maps/{mapId}/import/{jobId}",
  "contract": "venue-map",
  "summary": "Import progress and findings",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueMapImportJob"
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
  "permission": "AUDIT_VIEW",
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
    "name": "platformStaffGrantId",
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
 "listCatalogueBundles": {
  "method": "GET",
  "path": "/catalogue/bundles",
  "contract": "catalogue",
  "summary": "List published catalogue bundles",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleSummary"
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
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
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
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "isSellable",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "segmentTag",
    "in": "query",
    "required": null
   },
   {
    "name": "guidedAnswerIds",
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
 "searchMedia": {
  "method": "GET",
  "path": "/media",
  "contract": "assets",
  "summary": "Search the asset library",
  "permission": "ASSET_LIBRARY_VIEW",
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
    "name": "tag",
    "in": "query",
    "required": null
   },
   {
    "name": "collectionId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "unusedOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "rightsExpiringWithinDays",
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
  "responds": "PathClosureResult"
 },
 "setPlacedResource": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/resources",
  "contract": "venue-map",
  "summary": "Place or amend a bookable resource on the map",
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
  "requestBody": "SetPlacedResourceRequest",
  "responds": "PlacedResource"
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
  "requestBody": "SetVenuePointRequest",
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
 "syncScans": {
  "method": "POST",
  "path": "/access/scans",
  "contract": "access",
  "summary": "Replay scans recorded offline",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": false,
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GraphValidation"
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
  "description": "One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.access_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AccessPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAccessPolicyEffectiveness` in identity.",
  "required": [
   "id",
   "scopePath",
   "name",
   "policyType",
   "conditionExpression",
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
   "conditionExpression": {
    "type": "string",
    "description": "Condition tree over access.access_attribute keys using AND, OR, NOT, IN and BETWEEN"
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
 "Asset": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateAssetRequest"
   },
   {
    "type": "object",
    "x-ticvai-retired-columns": [
     "is_maintenance_overdue",
     "document_refs"
    ],
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
     "deviceId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"
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
      "type": "integer",
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"
     },
     "nextMaintenanceDueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"
     },
     "isMaintenanceOverdue": {
      "type": "boolean",
      "readOnly": true,
      "x-ticvai-persisted": false,
      "x-ticvai-derived": "onRead",
      "description": "`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"
     },
     "lastInspectionAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"
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
      "description": "Manuals, procedures, certificates. What a technician needs on site. Read from `maintenance.asset_document`.\n",
      "items": {
       "$ref": "#/components/schemas/AssetDocument"
      }
     }
    }
   }
  ]
 },
 "AssetDocument": {
  "x-ticvai-persistence": "maintenance.asset_document",
  "type": "object",
  "description": "A document attached to an asset — manual, procedure, certificate — with the name and kind a technician needs on site. **One row per document**, because `AssetDetail.documents` returns a name and a kind for each and a `text[]` of refs has nowhere to hold either.\n",
  "required": [
   "id",
   "assetId",
   "ref"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "ref": {
    "type": "string",
    "description": "The document in the media store."
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AssetDocumentKind"
     }
    ],
    "nullable": true,
    "description": "Null where the document arrived as a bare ref in `documentRefs`."
   }
  }
 },
 "AssetDocumentInput": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "ref",
   "kind"
  ],
  "properties": {
   "ref": {
    "type": "string",
    "description": "The document in the media store."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "kind": {
    "$ref": "#/components/schemas/AssetDocumentKind"
   }
  }
 },
 "AssetDocumentKind": {
  "type": "string",
  "enum": [
   "manual",
   "sop",
   "certificate",
   "warranty",
   "drawing",
   "riskAssessment"
  ]
 },
 "AssetHistoryEntry": {
  "x-ticvai-persistence": "none — union view over work orders, inspections, incidents and asset status changes",
  "type": "object",
  "description": "**Every kind has a source.** `workOrder` is a work-order row, `inspection` an inspection, `incident` an incident, `statusChange` a `maintenance.asset_status_change` row. `partReplaced` is a completed work order whose `resolutionCode` is `partReplaced`, and `planCompleted` a completed work order with a `sourcePlanId` — both read from `maintenance.work_order`, not stored twice.\n",
  "required": [
   "kind",
   "occurredAt",
   "summary"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "workOrder",
     "inspection",
     "incident",
     "statusChange",
     "partReplaced",
     "planCompleted"
    ]
   },
   "referenceId": {
    "type": "string",
    "nullable": true,
    "description": "The source row's id: a work-order, inspection or incident ULID, or an `asset_status_change` id.\n"
   },
   "summary": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   }
  }
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
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
      "nullable": true
     }
    }
   }
  }
 },
 "AuditRecord": {
  "type": "object",
  "x-ticvai-persistence": "platform.audit_record",
  "description": "26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n",
  "required": [
   "id",
   "action",
   "occurredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "Who acted."
   },
   "orgUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The scope node the action happened in."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The workstation it was done from, where there was one."
   },
   "action": {
    "type": "string",
    "description": "What was done, as the writing operation names it."
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "description": "When. The list is ordered by this, most recent first."
   },
   "platformStaffGrantId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"
   }
  }
 },
 "BundleSummary": {
  "x-ticvai-persistence": "none — projection over bundle",
  "type": "object",
  "description": "One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.",
  "required": [
   "version",
   "venueId",
   "publishedAt",
   "publishedBy",
   "contentHash",
   "staleAfter",
   "sizeBytes"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid"
   },
   "contentHash": {
    "type": "string"
   },
   "signatureKeyId": {
    "type": "string",
    "description": "Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "note": {
    "type": "string"
   },
   "appliedByWorkstations": {
    "type": "integer"
   }
  }
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
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
    "maxLength": 64,
    "x-ticvai-unique": "venue",
    "description": "**Unique per venue** (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. Two venues may each have an `A-001`.\n"
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
   "priorityOverride": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderPriority"
     }
    ],
    "nullable": true,
    "description": "**\"If this device goes down, raise this priority\"** (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. Null means the score decides.\n"
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
   "documents": {
    "type": "array",
    "description": "Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from.\n",
    "items": {
     "$ref": "#/components/schemas/AssetDocumentInput"
    }
   },
   "documentRefs": {
    "type": "array",
    "x-ticvai-persisted": false,
    "description": "**The refs alone, kept for callers that predate `documents`.** Each ref sent here is stored as an `asset_document` row with no name and no kind. Returned as the refs of `documents`, computed on read — there is no second copy to fall out of step.\n",
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
    "description": "**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n",
    "items": {
     "type": "object",
     "required": [
      "day",
      "from",
      "to"
     ],
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
       "type": "string",
       "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
       "description": "Venue local time, 24-hour `HH:MM`, when the queue starts running."
      },
      "to": {
       "type": "string",
       "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
       "description": "Venue local time, 24-hour `HH:MM`, when the queue stops running."
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
   },
   "fastPass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/QueueFastPass"
     }
    ],
    "nullable": true,
    "description": "The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"
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
   "delegatedRightRevoked",
   "journeyNotCovered"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
   },
   "resourceFindings": {
    "type": "array",
    "description": "**Placed resources a guest could not buy** (rev 3 REV3-15), named by label. Any entry here makes `isValid` false, and `publishVenueMap` refuses with the matching blocker.\n",
    "items": {
     "type": "object",
     "required": [
      "placedResourceId",
      "label",
      "reason"
     ],
     "properties": {
      "placedResourceId": {
       "type": "string",
       "format": "uuid"
      },
      "label": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "resourceUnlinked",
        "resourcePriceBandMissing",
        "duplicateResourceLabel"
       ]
      }
     }
    }
   }
  }
 },
 "GuestListing": {
  "type": "string",
  "enum": [
   "bookable",
   "infoOnly",
   "hidden"
  ],
  "default": "bookable",
  "description": "**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "incidentNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
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
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
 "IncidentAuthorityNotification": {
  "x-ticvai-persistence": "maintenance.incident_authority_notification",
  "type": "object",
  "description": "**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n",
  "required": [
   "id",
   "incidentId",
   "authority",
   "notifiedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "authority": {
    "type": "string",
    "maxLength": 200
   },
   "reference": {
    "type": "string",
    "maxLength": 128,
    "nullable": true
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time"
   },
   "notifiedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
      "nullable": true,
      "readOnly": true,
      "description": "The latest entry of `investigationNotes`, kept for readers that show one line."
     },
     "investigationNotes": {
      "type": "array",
      "readOnly": true,
      "description": "**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n",
      "items": {
       "$ref": "#/components/schemas/IncidentInvestigationNote"
      }
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
     "involvedParties": {
      "type": "array",
      "description": "Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n",
      "items": {
       "$ref": "#/components/schemas/IncidentInvolvedParty"
      }
     },
     "authorityNotifications": {
      "type": "array",
      "description": "Read from `maintenance.incident_authority_notification`, oldest first.",
      "items": {
       "$ref": "#/components/schemas/IncidentAuthorityNotification"
      }
     }
    }
   }
  ]
 },
 "IncidentInvestigationNote": {
  "x-ticvai-persistence": "maintenance.incident_investigation_note",
  "type": "object",
  "description": "**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n",
  "required": [
   "id",
   "incidentId",
   "note",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "note": {
    "type": "string",
    "maxLength": 10000
   },
   "writtenByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "IncidentInvolvedParty": {
  "x-ticvai-persistence": "maintenance.incident_involved_party",
  "type": "object",
  "description": "**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n",
  "required": [
   "id",
   "incidentId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "kind": {
    "type": "string",
    "enum": [
     "subject",
     "staff"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `pii.subject` id where `kind` is `subject`."
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The staff principal where `kind` is `staff`."
   }
  }
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
  "x-ticvai-persistence": "maintenance.preventive_plan",
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
 "MediaAsset": {
  "x-ticvai-persistence": "assets.media_asset",
  "type": "object",
  "required": [
   "id",
   "kind",
   "status",
   "filename",
   "contentType",
   "sizeBytes",
   "referenceCount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "status": {
    "$ref": "#/components/schemas/MediaStatus"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Required before use in a guest-facing surface. WCAG 2.2 AA."
   },
   "width": {
    "type": "integer",
    "nullable": true
   },
   "height": {
    "type": "integer",
    "nullable": true
   },
   "durationSeconds": {
    "type": "number",
    "nullable": true
   },
   "customMetadata": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"
   },
   "sharedWithTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "url": {
    "type": "string",
    "description": "Signed and expiring for private assets; stable CDN URL for public ones."
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "referenceCount": {
    "type": "integer",
    "description": "How many surfaces reference this asset. Non-zero refuses deletion.\n"
   },
   "rights": {
    "$ref": "#/components/schemas/MediaRights"
   },
   "isRightsExpired": {
    "type": "boolean"
   },
   "version": {
    "type": "integer"
   },
   "uploadedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
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
 "MediaRights": {
  "x-ticvai-persistence": "none — embedded in asset",
  "type": "object",
  "description": "Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n",
  "properties": {
   "licenceKind": {
    "type": "string",
    "enum": [
     "owned",
     "royaltyFree",
     "rightsManaged",
     "creativeCommons",
     "editorialOnly",
     "unknown"
    ]
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "licenceReference": {
    "type": "string",
    "nullable": true
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
   "permittedUses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "web",
      "print",
      "socialMedia",
      "inVenue",
      "advertising",
      "internal"
     ]
    }
   },
   "attributionRequired": {
    "type": "boolean",
    "default": false
   },
   "attributionText": {
    "type": "string",
    "nullable": true
   },
   "permittedTerritories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"
   },
   "permittedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"
   },
   "modelReleaseHeld": {
    "type": "boolean",
    "default": false
   },
   "renewalOwner": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "MediaStatus": {
  "type": "string",
  "enum": [
   "processing",
   "ready",
   "quarantined",
   "failed",
   "archived"
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
   "dynamicPolicies": {
    "type": "array",
    "description": "The active guest-admission dynamic policies for this access point's zones (SD-052), so an offline gate applies the same rules as an online one.",
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
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
 "OfflineScan": {
  "x-ticvai-persistence": "none — client-side journal",
  "allOf": [
   {
    "$ref": "#/components/schemas/ValidateRequest"
   },
   {
    "type": "object",
    "required": [
     "sequence",
     "localOutcome"
    ],
    "properties": {
     "sequence": {
      "type": "integer",
      "minimum": 1,
      "description": "Monotonic per device. The server processes in this order."
     },
     "localOutcome": {
      "allOf": [
       {
        "$ref": "#/components/schemas/ScanOutcome"
       }
      ],
      "description": "What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"
     },
     "localDenyReason": {
      "$ref": "#/components/schemas/DenyReason"
     },
     "overriddenByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "overrideReason": {
      "type": "string",
      "nullable": true
     }
    }
   }
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
 "PathClosureResult": {
  "description": "What `setPathClosure` returns: the path, and **what a forced closure cut off**, named.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/VenuePath"
   },
   {
    "type": "object",
    "properties": {
     "strandedPoints": {
      "type": "array",
      "readOnly": true,
      "description": "Points no longer reachable because of this closure. Empty unless `force` was used.\n",
      "items": {
       "$ref": "#/components/schemas/StrandedPoint"
      }
     }
    }
   }
  ]
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
 "PlacedResource": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.placed_resource",
  "description": "**A bookable resource where it stands on the map** (decided 29 September, rev 3 REV3-15 and GAP-C2): cabana B09 on the Beach, 15 guests, Large. The resource itself, its bookings and its holds live in `resources`; this row says where it is drawn and what the guest sees. Written into the working draft by `importVenueGeometry` or `setPlacedResource`, copied into the `VenueMapVersion` snapshot at publish. A guest picks one on the published map, holds it with `resources.createResourceHold` and buys it. **Supersedes audit R073 (c) and the 26 August minute for resources on an ingested map.**\n",
  "required": [
   "id",
   "mapId",
   "resourceId",
   "label",
   "kind",
   "zone",
   "capacity",
   "priceBandCode",
   "position"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "mapId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of the operation that writes it."
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "resources.Resource",
    "description": "The `resources.Resource` this is. **Availability, holds and bookings are keyed by this**, so a republished map with the cabana moved keeps its bookings.\n"
   },
   "label": {
    "type": "string",
    "maxLength": 40,
    "x-ticvai-unique": "map",
    "description": "What the guest sees and taps, e.g. `B09`. **Unique on the map**, compared without case after digit normalisation; normally the resource's `code`.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "cabana",
     "lounger",
     "table",
     "pitch",
     "other"
    ],
    "description": "A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay `fnb` table reservations (decided 29 September, rev 3 GAP-C2)."
   },
   "zone": {
    "type": "string",
    "maxLength": 80,
    "description": "The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`."
   },
   "capacity": {
    "type": "integer",
    "minimum": 1,
    "maximum": 500,
    "description": "Guests it takes, e.g. 15. Shown on the map and checked against the party at hold."
   },
   "priceBandCode": {
    "type": "string",
    "maxLength": 40,
    "description": "The band it sells in, e.g. `Large`, one of the `priceBands` given at import. The band's `variantId` prices it; the map holds no price.\n"
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "catalogue.ProductVariant",
    "description": "Resolved from the price band. What a cart line for this resource names."
   },
   "position": {
    "type": "object",
    "required": [
     "x",
     "y"
    ],
    "description": "Drawing coordinates of its label anchor, as on `VenuePoint`.",
    "properties": {
     "x": {
      "type": "number"
     },
     "y": {
      "type": "number"
     }
    }
   },
   "boundary": {
    "type": "array",
    "nullable": true,
    "description": "The shape drawn, as a polygon in drawing coordinates. Null for a pin.",
    "items": {
     "type": "object",
     "properties": {
      "x": {
       "type": "number"
      },
      "y": {
       "type": "number"
      }
     }
    }
   },
   "isBookable": {
    "type": "boolean",
    "default": true,
    "description": "False keeps it on the map and off sale, e.g. a cabana kept for staff use. Shown greyed.\n"
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
 "Product": {
  "x-ticvai-persistence": "catalogue.product",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId",
   "scopePath",
   "isSellable",
   "hasVariants"
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
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ProductKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "responsibleDepartmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who owns this product commercially. A scope node at `department` level."
   },
   "onSaleFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"
   },
   "onSaleTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"
   },
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "readOnly": true,
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"
   },
   "isStockTracked": {
    "type": "boolean",
    "default": false,
    "description": "**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n",
    "items": {
     "type": "string"
    }
   },
   "codeSchema": {
    "type": "string",
    "readOnly": true,
    "description": "7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"
   },
   "blockedOffline": {
    "type": "boolean",
    "description": "True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "Custom fields. JSONB-backed, defined by the venue's data mask."
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    },
    "description": "**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    },
    "description": "**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"
   },
   "requiresTimeWindow": {
    "type": "boolean",
    "default": false,
    "description": "**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"
   },
   "productOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."
   },
   "operationalContact": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A principal id or a name, as the context screen takes it."
   },
   "businessUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `ledger.legal_entity`, read through finance."
   },
   "attractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "siteId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The brand, as the context screen names it (a catalogue brand category)."
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "salesTerritory": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   }
  }
 },
 "ProductDisplayTag": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "required": [
   "kind",
   "label"
  ],
  "description": "One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "clock",
     "height",
     "free",
     "calendar",
     "id"
    ],
    "description": "`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."
   },
   "label": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."
   },
   "derived": {
    "type": "boolean",
    "readOnly": true,
    "default": false,
    "description": "True on a tag the server derived on read because the venue set none. Never sent."
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProductLifecycleState": {
  "type": "string",
  "enum": [
   "draft",
   "inReview",
   "approved",
   "live",
   "withdrawn",
   "archived"
  ]
 },
 "ProductMedia": {
  "x-ticvai-persistence": "catalogue.product_media",
  "type": "object",
  "required": [
   "assetId",
   "kind",
   "isPrimary"
  ],
  "description": "One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid",
    "description": "A `MediaAsset` of `assets.yaml`, in status `ready`."
   },
   "kind": {
    "type": "string",
    "enum": [
     "image",
     "video"
    ]
   },
   "isPrimary": {
    "type": "boolean",
    "default": false,
    "description": "The item *Read more* opens on and a listing shows. Exactly one per product."
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   }
  }
 },
 "ProductSalesContact": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "description": "Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n",
  "minProperties": 1,
  "properties": {
   "phone": {
    "type": "string",
    "maxLength": 32,
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "maxLength": 254,
    "nullable": true
   },
   "note": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."
   }
  }
 },
 "Queue": {
  "x-ticvai-persistence": "queue.queue + queue.queue_operating_window",
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
     "waitTimeAsOf": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"
     },
     "manualWaitExpiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"
     },
     "manualWaitNote": {
      "type": "string",
      "maxLength": 200,
      "nullable": true,
      "readOnly": true,
      "description": "The `note` given with the current manual figure. Cleared when it expires."
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
 "QueueEntryStatus": {
  "type": "string",
  "enum": [
   "waiting",
   "called",
   "redeemed",
   "expired",
   "noShow",
   "cancelled",
   "released"
  ]
 },
 "QueueFastPass": {
  "x-ticvai-persistence": "queue.queue",
  "type": "object",
  "description": "**Which Fast Pass entitlements this lane accepts, and how** (decided 29 September, VM close-out; pack 'Access Control Module' p.109, BO-221 Fast Pass & Attraction Access Journey). Fast Pass stays an entitlement owned by Product & Entitlement; this block is the lane's side of it: which products it honours, the return window, a per-guest daily cap and the access points that redeem it. Stored on the queue row. Only meaningful where `kind` is `fastPass` or `fastPassAllocationPercent` is above 0.\n**Four ways into priority, not one** (decided 29 September, build pass; 5.6.7 and 5.6.34). A guest joins this lane as priority when they hold an entitlement from `entitlementProductIds` (VIP, annual pass, premium package), are a member of a tier in `loyaltyTierIds`, qualify for a live promotion in `promotionIds`, or declare an accessibility need where `accessibilityPriority` is on. The first criterion met is recorded on the entry as `WaitingGuest.priorityBasis`. Every criterion is resolved by the server at join time; nothing the request asserts about a tier or a promotion is trusted. All four draw on the same reserved `fastPassAllocationPercent`, so widening who qualifies never widens the share of the ride they take.\n",
  "required": [
   "entitlementProductIds"
  ],
  "properties": {
   "entitlementProductIds": {
    "type": "array",
    "description": "Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "loyaltyTierIds": {
    "type": "array",
    "description": "5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. Read from the guest's own loyalty position at join time, never from the request, so a guest cannot claim a tier they do not hold. Empty: tier grants nothing on this lane.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "promotionIds": {
    "type": "array",
    "description": "5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. A guest qualifies when the promotion's conditions hold for them at join (the evaluation `promotions` already makes for a price), or by presenting its code in `JoinQueueRequest.promotionCode`. A paused or expired promotion grants nothing.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "accessibilityPriority": {
    "type": "boolean",
    "default": false,
    "description": "5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. **Taken on trust**, because asking for proof at a ride entrance is worse than the occasional abuse; the declaration is on the entry, so the operator at the front sees it (`listQueueEntries`). A venue that wants proof sells or issues an accessibility pass and lists it in `entitlementProductIds` instead. **Not the `accessible` lane**: that is where a guest who cannot stand in a switchback waits; this moves them ahead in the lane they chose.\n"
   },
   "returnWindowMinutes": {
    "type": "integer",
    "minimum": 1,
    "maximum": 240,
    "default": 60,
    "description": "How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan.\n"
   },
   "maxPerGuestPerDay": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Fast Pass redemptions one guest may make on this lane per day; null is no cap."
   },
   "allowedAccessPointIds": {
    "type": "array",
    "description": "Access points that redeem Fast Pass for this lane; empty is the queue's own.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
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
    "type": "boolean",
    "description": "**Healthy means the last reading arrived within the feed's expected interval** (decided 28 September, audit R106 (1)): `lastReadingAt` is no older than `expectedIntervalSeconds`. It is the opposite of `isQuiet`, and nothing else (latency, discards) makes a reporting feed unhealthy.\n"
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
   "expectedIntervalSeconds": {
    "type": "integer",
    "description": "The feed's `expectedIntervalSeconds` — the interval `isQuiet` is judged against, returned here so a health panel does not need the feed row as well.\n"
   },
   "readingsLastHour": {
    "type": "integer"
   },
   "discardedLastHour": {
    "type": "integer",
    "description": "Out-of-order readings rejected in the last hour — rows of `queue.reading` for this feed with `disposition: discardedOutOfOrder`. Duplicates are not counted here: a duplicate has no row, and `submitQueueReading` reports it in its own `duplicates`.\n"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The play ID, generated on the reader, and returned as `PlayResult.playId`. Also the idempotency key: on `recordGamePlay` it must equal the `Idempotency-Key` header (a mismatch is the shared 409 `Conflict`); in a `syncGamePlays` batch it is the key on its own.\n"
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
   "playedOffline": {
    "type": "boolean",
    "default": false,
    "description": "**True where the reader recorded the play while offline** and is replaying it. Such a play is accepted even against too few credits and reported for reconciliation; a live play (false) is refused instead (decided 28 September, audit R106 (3)). Every play in a `syncGamePlays` batch is treated as offline.\n"
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
    "$ref": "#/components/schemas/ResourceKind"
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
    "description": "For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"
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
    "default": 0,
    "description": "After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"
   },
   "cleaningPolicy": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ResourceCleaningPolicy"
     }
    ],
    "nullable": true,
    "description": "How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."
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
 "ResourceCleaningPolicy": {
  "x-ticvai-persistence": "none — columns on resources.resource",
  "type": "object",
  "description": "**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n",
  "required": [
   "mode",
   "bufferMinutes"
  ],
  "properties": {
   "mode": {
    "type": "string",
    "enum": [
     "afterEveryBooking",
     "timesPerDay"
    ]
   },
   "bufferMinutes": {
    "type": "integer",
    "minimum": 5,
    "maximum": 240,
    "description": "Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."
   },
   "cleaningsPerDay": {
    "type": "integer",
    "minimum": 1,
    "maximum": 24,
    "nullable": true,
    "description": "Required for `timesPerDay`; ignored for `afterEveryBooking`."
   },
   "windowStart": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Venue-local time the cleaning window opens. Null means the resource's opening time."
   },
   "windowEnd": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Venue-local time the cleaning window closes. Null means the resource's closing time."
   }
  }
 },
 "ResourceKind": {
  "type": "string",
  "description": "BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n",
  "enum": [
   "cabana",
   "lounger",
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
   "other"
  ],
  "x-ticvai-refuses": {
   "mealPlan": "**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."
  }
 },
 "ScanEvent": {
  "x-ticvai-persistence": "access.scan_event",
  "type": "object",
  "required": [
   "id",
   "accessPointId",
   "venueId",
   "outcome",
   "direction",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The scan's client-generated ULID, the key offline replay deduplicates on."
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "ticketId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The `Entitlement.id` scanned; null where the media resolved to nothing."
   },
   "mediaCode": {
    "type": "string",
    "nullable": true
   },
   "outcome": {
    "$ref": "#/components/schemas/ScanOutcome"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "overridesScanId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "description": "The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."
   },
   "dynamicPolicyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."
   },
   "dynamicPolicyVersion": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "The version of that policy in force at the scan, so a report spanning a change counts each version apart."
   },
   "dynamicPolicyResult": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ],
    "nullable": true,
    "description": "What the policy decided, which for a step-up is not the same as the scan's outcome."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."
   },
   "localSequence": {
    "type": "integer",
    "nullable": true,
    "description": "The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."
   },
   "packageVersion": {
    "type": "string",
    "nullable": true,
    "description": "The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null while pending. Differs from recordedAt for offline scans."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
 "SetPlacedResourceRequest": {
  "description": "What `setPlacedResource` takes: a `PlacedResource` without its server-owned fields. **`placedResourceId` absent places a new one; present amends that one**, as `setVenuePoint`.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/PlacedResource"
   },
   {
    "type": "object",
    "properties": {
     "placedResourceId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The placed resource to amend. Absent or null places a new one."
     }
    }
   }
  ]
 },
 "SetVenuePointRequest": {
  "description": "What `setVenuePoint` takes: a `VenuePoint` without its server-owned fields, plus the point to amend. **`pointId` absent places a new point; present amends that one**, and it must be a point on the map in the path.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/VenuePoint"
   },
   {
    "type": "object",
    "properties": {
     "pointId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The point to amend. Absent or null places a new point."
     }
    }
   }
  ]
 },
 "StrandedPoint": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from the graph",
  "required": [
   "pointId",
   "name",
   "kind",
   "isCritical"
  ],
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
   },
   "isCritical": {
    "type": "boolean",
    "description": "First aid, an emergency exit or an assembly point, the same set as `GraphValidation.criticalUnreachable`. **The one the operator must read first.**\n"
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
   },
   "advisory": {
    "type": "object",
    "nullable": true,
    "description": "BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n",
    "properties": {
     "genderClassification": {
      "type": "string",
      "enum": [
       "women",
       "men",
       "undetermined"
      ],
      "description": "**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"
     },
     "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"
     },
     "reportedByDeviceId": {
      "type": "string",
      "format": "uuid",
      "description": "**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"
     }
    }
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
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "Derived from `venueId`. Not sent by a client."
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
    ],
    "readOnly": true,
    "description": "`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"
   },
   "publishedVersion": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "The `VenueMapVersion.version` guests are served. Null until the first publish.\n"
   },
   "graphVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"
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
    "readOnly": true,
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
   "version": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "**The published version these points and paths belong to**, which is the number a client caches and sends back as `version`. It can differ from `map.publishedVersion` when an older version was asked for. Null when the draft was read.\n"
   },
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
   },
   "resources": {
    "type": "array",
    "description": "The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none.\n",
    "items": {
     "$ref": "#/components/schemas/PlacedResource"
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
    "description": "**Bumped by a publish or a closure**, and stored as `VenueMap.graphVersion`. A client holding an older version knows its route may cross something that closed, and asking for the graph is cheaper than asking whether the graph changed.\n"
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
      "isStepFree": {
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
 "VenueMapImportJob": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.import_job",
  "description": "**Two-phase, following `seating.ImportJob`**, and carrying its lesson: a job that finds nothing is not a successful job.\n",
  "required": [
   "id",
   "status",
   "outcome"
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
   "status": {
    "type": "string",
    "enum": [
     "parsing",
     "previewReady",
     "committed",
     "failed"
    ]
   },
   "outcome": {
    "type": "string",
    "enum": [
     "parsed",
     "parsedWithFindings",
     "nothingFound",
     "noLayersMatched",
     "unreadable"
    ]
   },
   "shapesFound": {
    "type": "integer"
   },
   "layersFound": {
    "type": "array",
    "description": "**Every layer name in the source, decoded.** Shown whether or not extraction worked, so an operator maps a role by reading rather than guessing.\n",
    "items": {
     "type": "string"
    }
   },
   "unmappedLayers": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "manifestRowsRead": {
    "type": "integer",
    "nullable": true
   },
   "resourcesFound": {
    "type": "integer",
    "nullable": true,
    "description": "Bookable resource shapes found on the resource layer (rev 3 REV3-15). Null where the map has none.\n"
   },
   "resourceRowsJoined": {
    "type": "integer",
    "nullable": true,
    "description": "Resource manifest rows that joined a shape and a `resources.Resource`. **The number to check against your own count**, as `manifestRowsJoined` is for seats: 34 cabanas on the plan and 30 joined is four labels that differ.\n"
   },
   "manifestRowsJoined": {
    "type": "integer",
    "nullable": true,
    "description": "**The number to check against your own count.** A manifest of 396 seats that joins 220 is the digit problem in §4, or a section code that differs by a space — and both look like success without this figure.\n"
   },
   "findings": {
    "type": "array",
    "description": "**Named against the spec**, so a finding maps to a section of `handoff/venue-map-input-spec.md` rather than to a stack trace.\n",
    "items": {
     "type": "object",
     "required": [
      "code",
      "severity",
      "message"
     ],
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "duplicateLayerName",
        "geometryOnLayerZero",
        "unmappedLayer",
        "mixedLayerContent",
        "sectionCodeMismatch",
        "digitScriptMismatch",
        "mergedCells",
        "totalRowDetected",
        "manifestSectionMissingFromPlan",
        "planSectionMissingFromManifest",
        "exitLayerNotSplit",
        "noGeoreference",
        "layerNameUndecodable",
        "rasterOnly",
        "resourceLabelMissing",
        "resourceLabelDuplicate",
        "resourceManifestMissingFromPlan",
        "resourcePlanMissingFromManifest",
        "resourceCodeUnmatched",
        "resourcePriceBandUnknown"
       ],
       "description": "**A closed set, and each one names a rule in the spec.** Free-text findings are findings a drawing office cannot act on. The six `resource*` codes check placed resources (rev 3 REV3-15): a shape with no label, two with one label, a manifest row with no shape or the reverse, a label with no `resources.Resource`, and a price band not in `priceBands`.\n"
      },
      "severity": {
       "type": "string",
       "enum": [
        "error",
        "warning",
        "info"
       ],
       "description": "**`warning` is the important level here.** `rasterOnly` and `noGeoreference` are warnings — the map still works, with less — and treating them as errors would refuse a venue that sent everything it had.\n"
      },
      "message": {
       "type": "string"
      },
      "specSection": {
       "type": "string",
       "nullable": true,
       "description": "Which part of the spec covers it — `§2 Layers`, `§4 Digits`."
      },
      "affected": {
       "type": "array",
       "description": "The layers, sections or rows involved. **Named, not counted.**",
       "items": {
        "type": "string"
       }
      }
     }
    }
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
    "format": "uuid",
    "readOnly": true
   },
   "mapId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of the operation that writes the path."
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
    "readOnly": true,
    "description": "Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"
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
    "readOnly": true,
    "description": "Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"
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
    "format": "uuid",
    "readOnly": true
   },
   "mapId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of the operation that writes the point."
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
    "type": "string",
    "x-ticvai-unique": "venue",
    "description": "**Unique per venue** (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` refuses a duplicate with `409` `duplicate-code`. Junctions are named by extraction and are exempt.\n"
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
    "description": "For a ride or show — links to wait times and to booking. **What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer`** (29 September, MOB-4); this link stays for wait times.\n"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"
   },
   "isStepFree": {
    "type": "boolean",
    "default": true,
    "description": "Whether the point itself can be reached without steps. **The same name as `VenuePath.isStepFree`, because it is the same concept** (it was `isAccessible` until the 26 September audit). **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"
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
   },
   "description": {
    "type": "object",
    "nullable": true,
    "additionalProperties": {
     "type": "string",
     "maxLength": 1000
    },
    "description": "**What the guest reads on Item Detail** (29 September, MOB-4). Keyed by locale, like `nameLocalised`. One screen now serves rides, shows, restaurants and shops (GST-004 and GST-006 merged), and it opens from the map pin, so the point carries the words rather than each kind borrowing them from a different module. Set on BO-094.\n"
   },
   "media": {
    "type": "array",
    "maxItems": 12,
    "description": "**The gallery on Item Detail** (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. Assets are referenced, never copied, so a replaced photo changes everywhere.\n",
    "items": {
     "type": "object",
     "required": [
      "assetId",
      "kind"
     ],
     "properties": {
      "assetId": {
       "type": "string",
       "format": "uuid",
       "x-ticvai-references": "assets.media_asset"
      },
      "kind": {
       "type": "string",
       "enum": [
        "image",
        "video"
       ]
      },
      "isPrimary": {
       "type": "boolean",
       "default": false
      },
      "altText": {
       "type": "string",
       "nullable": true,
       "maxLength": 200
      }
     }
    }
   },
   "featuredOffer": {
    "type": "object",
    "nullable": true,
    "required": [
     "kind",
     "id"
    ],
    "description": "**The product card on Item Detail, for every kind of point** (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from the point, and it may be a bundle: a restaurant offers *meal combo with admission* (`promotions` bundle with an admission and a meal component), which checks out in about three steps (GST-004 → GST-056 → GST-041). A point with none shows no card. **Referenced, not priced here**: the card reads `catalogue.getProduct` or `promotions.getBundle` for the live price and availability.\n",
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "product",
       "bundle"
      ]
     },
     "id": {
      "type": "string",
      "format": "uuid",
      "description": "The `catalogue.product` id or the `promotions.bundle` id, by `kind`."
     },
     "label": {
      "type": "string",
      "nullable": true,
      "maxLength": 40,
      "description": "The button text, e.g. *Buy meal combo*. Null uses the product's own call to action."
     }
    }
   },
   "typicalDurationMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 600,
    "description": "**How long a visit to this point usually takes**, ride time and queue excluded (29 September, MOB-6). The visit planner lays out a day with it; the queue comes from `queue.getWaitTimes` on the day. Null for a point the planner never places (a toilet).\n"
   },
   "interestTags": {
    "type": "array",
    "maxItems": 12,
    "description": "**What a guest who says they like this would like here** (29 September, MOB-6): the planner matches the guest's interests against these. A closed list so that the Plan tab's interest chips and the venue's tags are the same words.\n",
    "items": {
     "type": "string",
     "enum": [
      "thrill",
      "family",
      "kids",
      "water",
      "animals",
      "shows",
      "culture",
      "shopping",
      "dining",
      "relaxing",
      "photo",
      "adventure",
      "sport",
      "nightlife",
      "indoor"
     ]
    }
   },
   "cuisineTags": {
    "type": "array",
    "maxItems": 8,
    "description": "**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag.\n",
    "items": {
     "type": "string",
     "maxLength": 30
    }
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
   "attractionCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"
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
    "description": "The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"
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
    "format": "date-time",
    "description": "When the figure was produced — the queue's `waitTimeAsOf`."
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
 "WaitingGuest": {
  "x-ticvai-persistence": "queue.entry",
  "type": "object",
  "required": [
   "id",
   "queueId",
   "partyNumber",
   "partySize",
   "status",
   "joinedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The client-generated ULID from `JoinQueueRequest.id`, and the `entryId` every entry path takes. `listMyWaitingGuests` gives it back to a guest who has lost it.\n"
   },
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "queueName": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "partyNumber": {
    "type": "integer",
    "description": "What the guest sees and what appears on signage."
   },
   "partySize": {
    "type": "integer"
   },
   "status": {
    "$ref": "#/components/schemas/QueueEntryStatus"
   },
   "positionInQueue": {
    "type": "integer",
    "nullable": true
   },
   "partiesAhead": {
    "type": "integer",
    "nullable": true
   },
   "estimatedCallAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isFastPass": {
    "type": "boolean"
   },
   "priorityBasis": {
    "type": "string",
    "enum": [
     "none",
     "entitlement",
     "loyaltyTier",
     "promotion",
     "accessibility"
    ],
    "default": "none",
    "description": "Why this party is priority, when it is (decided 29 September, build pass; 5.6.7, 5.6.34): the first `QueueFastPass` criterion met at join, in the order entitlement, loyalty tier, promotion, accessibility. `isFastPass` is true whenever this is not `none`. Kept on the entry so a disputed priority can be explained afterwards.\n"
   },
   "priorityTierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The loyalty tier that granted priority, where `priorityBasis` is `loyaltyTier`."
   },
   "priorityPromotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The promotion that granted priority, where `priorityBasis` is `promotion`."
   },
   "accessibilityNeedDeclared": {
    "type": "boolean",
    "default": false,
    "description": "What the party declared at join, shown to the operator at the front."
   },
   "entitlementId": {
    "type": "string",
    "nullable": true
   },
   "calledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnWindowEndsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "redeemedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "admittedCount": {
    "type": "integer",
    "nullable": true
   },
   "joinedAt": {
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
