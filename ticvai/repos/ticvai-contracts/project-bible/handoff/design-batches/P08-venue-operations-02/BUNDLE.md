# P08-venue-operations-02 — P08 · Venue Operations (2 of 2)

**5 screens · 15 operations · 31 schemas · 10 permissions**

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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `AI_AUDIT_VIEW, APPROVAL_DECIDE, DEVICE_VIEW, ORDER_CREATE, ORDER_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE, SCOPE_VIEW, TENANT_CONFIGURE, WORKSTATION_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: createOrder
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-129` | Software, Configuration & Version Management | listDetail | 6 | 0 | — |
| `BO-130` | Offline Policy & Rules Configuration | listDetail | 4 | 0 | — |
| `BO-131` | Connectivity & Auto-Switch Settings | configEditor | 1 | 0 | — |
| `BO-132` | Offline Transaction Monitor & Sync Queue | listDetail | 2 | 0 | — |
| `BO-133` | Offline Alerts, Limits & Audit | approvalInbox | 6 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-129",
  "name": "Software, Configuration & Version Management",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/software-configuration-version-management",
   "component": "apps/venue-management-web/src/routes/ops/SoftwareConfigurationVersionManagementList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-108",
    "BO-128"
   ],
   "exitTo": [
    "BO-108",
    "BO-130"
   ],
   "inferred": false,
   "notes": "**Returns to BO-108.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-130",
     "trigger": "Offline Policy & Rules Configuration",
     "provenance": "flow F89 step 3→4"
    },
    {
     "to": "BO-108",
     "trigger": "Venue Operations",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-108 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-5D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 5.dc.html#pos-5d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listWorkstations` reads the population and `getWorkstationHealth` reads one of them — list, select, act",
  "purpose": "Software, Configuration & Version Management — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "getWorkstationHealth",
    "why": "**1 declared operation reach no component on this screen**: getWorkstationHealth. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every software version",
       "bindsTo": "Workstation",
       "columns": [
        "Workstation.id",
        "Workstation.code",
        "Workstation.name",
        "Workstation.venueId",
        "Workstation.regionId",
        "Workstation.departmentId",
        "Workstation.scopePath",
        "Workstation.saleBoard",
        "Workstation.accessPointId",
        "Workstation.devices",
        "Workstation.currency",
        "Workstation.currencyScale"
       ],
       "operation": "listWorkstations",
       "provenance": "contract tenancy.yaml GET /workstations"
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
       "operation": "setConfigurationProfile",
       "provenance": "contract tenancy.yaml PUT /configuration-profiles"
      },
      {
       "kind": "secondaryButton",
       "label": "Deploy",
       "operation": "deployConfigurationProfile",
       "provenance": "contract tenancy.yaml POST /configuration-profiles/{profileId}/deploy"
      },
      {
       "kind": "secondaryButton",
       "label": "Configure",
       "operation": "configureWorkstation",
       "provenance": "contract tenancy.yaml PUT /workstations/{workstationId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setConnectivityThresholds",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
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
       "kind": "searchField",
       "label": "Search software, configuration",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "deployConfigurationProfile",
       "notes": "Declares `deployConfigurationProfile`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The software version list.",
   "error": "Could not load. Names which read failed and leaves the software version untouched.",
   "emptyFirstRun": "No software version yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the software version are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setConfigurationProfile",
    "contract": "tenancy",
    "purpose": "setConfigurationProfile",
    "trigger": "onAction",
    "invalidates": [
     "listWorkstations"
    ]
   },
   {
    "operationId": "deployConfigurationProfile",
    "contract": "tenancy",
    "purpose": "deployConfigurationProfile",
    "trigger": "onAction",
    "invalidates": [
     "listWorkstations"
    ]
   },
   {
    "operationId": "configureWorkstation",
    "contract": "tenancy",
    "purpose": "Configure a workstation",
    "trigger": "onAction",
    "invalidates": [
     "listWorkstations"
    ]
   },
   {
    "operationId": "getWorkstationHealth",
    "contract": "tenancy",
    "purpose": "getWorkstationHealth",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWorkstations",
    "contract": "tenancy",
    "purpose": "List workstations",
    "trigger": "onLoad"
   },
   {
    "operationId": "setConnectivityThresholds",
    "contract": "tenancy",
    "purpose": "setConnectivityThresholds",
    "trigger": "onAction",
    "invalidates": [
     "listWorkstations"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "profileId",
     "from": "deepLink"
    },
    {
     "name": "workstationId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first. Resolves from the session — a till is signed into."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-129",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-130",
  "name": "Offline Policy & Rules Configuration",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/offline-policy-rules-configuration",
   "component": "apps/venue-management-web/src/routes/ops/OfflinePolicyRulesConfigurationList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-108",
    "BO-129"
   ],
   "exitTo": [
    "BO-108"
   ],
   "inferred": false,
   "notes": "**Returns to BO-108.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-108",
     "trigger": "Venue Operations",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-108 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-5E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Moved to wave 1 on 24 August.** F33 walks a till going offline and coming back, which is a wave-1 journey — ADR-0013 makes the POS local-first from the first release. **A venue that can trade offline and cannot resolve a sync rejection has an unbounded journal and no way to clear it**, and `check-flows` refused the flow rather than let that ship. **Resolved remotely by design.**  is venue-scoped and this is a web screen — **a supervisor at the main venue clears a mall kiosk's rejections without going there.** An IT technician restores the connection; **deciding whether a sale stands is a commercial act and they have the access without the authority.**",
  "density": "compact",
  "boardFrames": [
   "POS Board 5.dc.html#pos-5e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSyncRejections` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Offline Policy & Rules Configuration — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every offline policy rules",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected offline policy rules",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
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
       "operation": "setOfflinePolicy",
       "provenance": "contract tenancy.yaml PUT /offline-policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync",
       "operation": "syncOrders",
       "provenance": "contract orders.yaml POST /sync/orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search offline policy",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline policy rules list.",
   "error": "Could not load. Names which read failed and leaves the offline policy rules untouched.",
   "emptyFirstRun": "No offline policy rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline policy rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setOfflinePolicy",
    "contract": "tenancy",
    "purpose": "setOfflinePolicy",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   },
   {
    "operationId": "listSyncRejections",
    "contract": "orders",
    "purpose": "Entries the server refused",
    "trigger": "onLoad"
   },
   {
    "operationId": "syncOrders",
    "contract": "orders",
    "purpose": "Replay orders recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Post a rejected transaction at the price the guest paid",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first.",
   "preloaded": [
    "SyncRejection.id",
    "SyncRejection.workstationId",
    "SyncRejection.kind",
    "SyncRejection.recordedAt",
    "SyncRejection.rejectedAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-130",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-131",
  "name": "Connectivity & Auto-Switch Settings",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/connectivity-auto-switch-settings",
   "component": "apps/venue-management-web/src/routes/ops/ConnectivityAutoSwitchSettingsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-108"
   ],
   "exitTo": [
    "BO-108"
   ],
   "inferred": false,
   "notes": "**Returns to BO-108.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-108",
     "trigger": "Venue Operations",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-108 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setConnectivityThresholds`) and no read of a population — it is settings, not a list",
  "purpose": "Connectivity & Auto-Switch Settings — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "ConnectivityPolicy.id",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
      },
      {
       "kind": "textField",
       "label": "scopePath",
       "bindsTo": "ConnectivityPolicy.scopePath",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
      },
      {
       "kind": "textField",
       "label": "failuresBeforeOffline",
       "bindsTo": "ConnectivityPolicy.failuresBeforeOffline",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
      },
      {
       "kind": "textField",
       "label": "probeIntervalSeconds",
       "bindsTo": "ConnectivityPolicy.probeIntervalSeconds",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
      },
      {
       "kind": "textField",
       "label": "probeTimeoutMs",
       "bindsTo": "ConnectivityPolicy.probeTimeoutMs",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
      },
      {
       "kind": "textField",
       "label": "successesBeforeOnline",
       "bindsTo": "ConnectivityPolicy.successesBeforeOnline",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
      },
      {
       "kind": "textField",
       "label": "minimumStableSeconds",
       "bindsTo": "ConnectivityPolicy.minimumStableSeconds",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
      },
      {
       "kind": "textField",
       "label": "autoSwitch",
       "bindsTo": "ConnectivityPolicy.autoSwitch",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
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
       "operation": "setConnectivityThresholds",
       "provenance": "contract tenancy.yaml PUT /connectivity-policy"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search connectivity",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved connectivity auto-switch settings.",
   "error": "Could not load. Names which read failed and leaves the connectivity auto-switch settings untouched.",
   "emptyFirstRun": "No connectivity auto-switch settings configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setConnectivityThresholds",
    "contract": "tenancy",
    "purpose": "setConnectivityThresholds",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-131"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-132",
  "name": "Offline Transaction Monitor & Sync Queue",
  "module": "Venue Operations",
  "requiresModule": "ticketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/offline-transaction-monitor-sync-queue",
   "component": "apps/venue-management-web/src/routes/ops/OfflineTransactionMonitorSyncQueueList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-108"
   ],
   "exitTo": [
    "BO-108"
   ],
   "inferred": false,
   "notes": "**Returns to BO-108.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-108",
     "trigger": "Venue Operations",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-108 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSyncRejections` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Offline Transaction Monitor & Sync Queue — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every offline transaction sync",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected offline transaction sync",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
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
       "operation": "syncOrders",
       "provenance": "contract orders.yaml POST /sync/orders"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search offline transaction monitor",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline transaction sync list.",
   "error": "Could not load. Names which read failed and leaves the offline transaction sync untouched.",
   "emptyFirstRun": "No offline transaction sync yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline transaction sync are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSyncRejections",
    "contract": "orders",
    "purpose": "Entries the server refused",
    "trigger": "onLoad"
   },
   {
    "operationId": "syncOrders",
    "contract": "orders",
    "purpose": "Replay orders recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first.",
   "preloaded": [
    "SyncRejection.id",
    "SyncRejection.workstationId",
    "SyncRejection.kind",
    "SyncRejection.recordedAt",
    "SyncRejection.rejectedAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-132"
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
  "id": "BO-133",
  "name": "Offline Alerts, Limits & Audit",
  "module": "Venue Operations",
  "requiresModule": "ticketing",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/offline-alerts-limits-audit",
   "component": "apps/venue-management-web/src/routes/ops/OfflineAlertsLimitsAuditList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-108"
   ],
   "exitTo": [
    "BO-108"
   ],
   "inferred": false,
   "notes": "**Returns to BO-108.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-108",
     "trigger": "Venue Operations",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-108 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "POS-002",
     "trigger": "The connection returns",
     "provenance": "flow F33 step 4→5",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-5F** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Moved to wave 1 on 24 August.** F33 walks a till going offline and coming back, which is a wave-1 journey — ADR-0013 makes the POS local-first from the first release. **A venue that can trade offline and cannot resolve a sync rejection has an unbounded journal and no way to clear it**, and `check-flows` refused the flow rather than let that ship.",
  "density": "compact",
  "boardFrames": [
   "POS Board 5.dc.html#pos-5f"
  ],
  "pattern": "approvalInbox",
  "patternReason": "`decideApprovalRequest` decides items that `listSyncRejections` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Offline Alerts, Limits & Audit — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "listAlerts",
    "why": "**2 declared operations reach no component on this screen**: listAlerts, listAuditRecords. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected offline alerts limits",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Decide",
       "operation": "decideApprovalRequest",
       "provenance": "contract approvals.yaml POST /approval-requests/{requestId}/decide"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAlertRule",
       "provenance": "contract reporting.yaml PUT /alert-rules"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search offline alerts, limits",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline alerts limits list.",
   "error": "Could not load. Names which read failed and leaves the offline alerts limits untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the offline alerts limits are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSyncRejections",
    "contract": "orders",
    "purpose": "Entries the server refused",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAuditRecords",
    "contract": "tenancy",
    "purpose": "Who did what, where, and when",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve or reject",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   },
   {
    "operationId": "setAlertRule",
    "contract": "reporting",
    "purpose": "Raise an alert when a number leaves a range",
    "trigger": "onAction",
    "invalidates": [
     "listSyncRejections"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    },
    {
     "name": "requestId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first. An approval request opened from the queue.",
   "preloaded": [
    "SyncRejection.id",
    "SyncRejection.workstationId",
    "SyncRejection.kind",
    "SyncRejection.recordedAt",
    "SyncRejection.rejectedAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-133",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "configureWorkstation": {
  "method": "PUT",
  "path": "/workstations/{workstationId}",
  "contract": "tenancy",
  "summary": "Configure a workstation",
  "permission": "WORKSTATION_CONFIGURE",
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
  "requestBody": "ConfigureWorkstationRequest",
  "responds": "Workstation"
 },
 "createOrder": {
  "method": "POST",
  "path": "/orders",
  "contract": "orders",
  "summary": "Create an order",
  "permission": "ORDER_CREATE",
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
  "requestBody": "CreateOrderRequest",
  "responds": "Order"
 },
 "decideApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/decide",
  "contract": "approvals",
  "summary": "Approve or reject",
  "permission": "APPROVAL_DECIDE",
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
  "responds": "ApprovalRequest"
 },
 "deployConfigurationProfile": {
  "method": "POST",
  "path": "/configuration-profiles/{profileId}/deploy",
  "contract": "tenancy",
  "summary": "Push a version to a fleet, in stages",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "ProfileDeployment",
  "responds": null
 },
 "getWorkstationHealth": {
  "method": "GET",
  "path": "/workstations/{workstationId}/health",
  "contract": "tenancy",
  "summary": "A score a manager can sort by, and what is dragging it down",
  "permission": "DEVICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "listAlerts": {
  "method": "GET",
  "path": "/alerts",
  "contract": "reporting",
  "summary": "What is currently wrong",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Alert"
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
 "listSyncRejections": {
  "method": "GET",
  "path": "/sync/rejections",
  "contract": "orders",
  "summary": "Entries the server refused",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
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
 "listWorkstations": {
  "method": "GET",
  "path": "/workstations",
  "contract": "tenancy",
  "summary": "List workstations",
  "permission": "SCOPE_VIEW",
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
    "name": "saleBoardKind",
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
 "runReport": {
  "method": "POST",
  "path": "/reports/{reportId}/run",
  "contract": "reporting",
  "summary": "Run a report",
  "permission": "REPORT_VIEW_VENUE",
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
  "requestBody": "RunReportRequest",
  "responds": "ReportResult"
 },
 "setAlertRule": {
  "method": "PUT",
  "path": "/alert-rules",
  "contract": "reporting",
  "summary": "Watch a metric and tell somebody",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "AlertRule",
  "responds": "AlertRule"
 },
 "setConfigurationProfile": {
  "method": "PUT",
  "path": "/configuration-profiles",
  "contract": "tenancy",
  "summary": "What a class of workstation is configured to be",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "ConfigurationProfile",
  "responds": "ConfigurationProfile"
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
 "syncOrders": {
  "method": "POST",
  "path": "/sync/orders",
  "contract": "orders",
  "summary": "Replay orders recorded offline",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderSyncResult"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Alert": {
  "type": "object",
  "x-ticvai-persistence": "reporting.alert",
  "description": "A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n",
  "required": [
   "id",
   "ruleId",
   "raisedAt",
   "severity",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "ruleId": {
    "type": "string",
    "format": "uuid"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "severity": {
    "type": "string",
    "enum": [
     "info",
     "warning",
     "critical"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "raised",
     "acknowledged",
     "resolved",
     "expired"
    ]
   },
   "observedValue": {
    "type": "number"
   },
   "threshold": {
    "type": "number"
   },
   "scopePath": {
    "type": "string"
   },
   "acknowledgedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "acknowledgedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"
   }
  }
 },
 "AlertRule": {
  "type": "object",
  "x-ticvai-persistence": "reporting.alert_rule",
  "description": "BL-152, CF-134. **Six contracts detect their own trouble and none told a person.**\nFive sections ask for this and it is the same gap as `MessageTrigger`, seen from the operational side — **that one tells a guest something happened; this one tells an operator something is wrong.**\n**A threshold that nobody is watching is a threshold nobody set.** 6.1.57 wants an exception when a KPI leaves range, and an exception that arrives in a nightly report is an exception nobody acted on.\n",
  "required": [
   "id",
   "name",
   "metric",
   "comparator",
   "threshold",
   "severity",
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
   "metric": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricSource"
     }
    ],
    "description": "**From the closed set**, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for.\n"
   },
   "comparator": {
    "type": "string",
    "enum": [
     "above",
     "below",
     "outsideRange",
     "changesBy",
     "equals"
    ]
   },
   "threshold": {
    "type": "number"
   },
   "thresholdUpper": {
    "type": "number",
    "nullable": true
   },
   "windowMinutes": {
    "type": "integer",
    "default": 15,
    "description": "**The window is what stops an alert firing on noise.** A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes within a week.\n"
   },
   "severity": {
    "type": "string",
    "enum": [
     "info",
     "warning",
     "critical"
    ]
   },
   "deliverTo": {
    "type": "array",
    "description": "CF-134. **The dashboard panel is the default and the only one that always applies.** Email or WhatsApp where the matrix names them — an operational alert arriving by email is an alert nobody sees in time.\n",
    "items": {
     "type": "string",
     "enum": [
      "dashboardPanel",
      "email",
      "whatsapp",
      "sms"
     ]
    }
   },
   "recipientRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "cooldownMinutes": {
    "type": "integer",
    "default": 30,
    "description": "**How long before the same rule may fire again.** Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close.\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "shiftVariance",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodReopen",
   "tenantMigration"
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
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
 "CatalogueState": {
  "x-ticvai-persistence": "none — computed from workstation bundle_version",
  "type": "object",
  "description": "The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n",
  "required": [
   "appliedBundleVersion",
   "appliedAt",
   "staleAfter",
   "isStale"
  ],
  "properties": {
   "appliedBundleVersion": {
    "type": "string"
   },
   "appliedAt": {
    "type": "string",
    "format": "date-time"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time",
    "description": "Beyond this the terminal refuses to trade."
   },
   "isStale": {
    "type": "boolean"
   },
   "pendingBundleVersion": {
    "type": "string",
    "nullable": true,
    "description": "Published but not yet applied."
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
 "ConfigurationProfile": {
  "type": "object",
  "x-ticvai-persistence": "platform.configuration_profile",
  "description": "Board 1 of the client's POS design set, 20 August. **The board shows 1,248 workstations across four versions and the package modelled none of it** — a firmware version field on the workstation, and nothing that says what a workstation is configured to be.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks alone*, which is the only reason to version a profile at all.\n",
  "required": [
   "id",
   "name",
   "venueKindScope",
   "version",
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
   "scopePath": {
    "type": "string"
   },
   "venueKindScope": {
    "type": "array",
    "description": "Which workstation types it applies to. **A ticketing counter and a kitchen display do not share a profile**, and a profile that claims to is a profile somebody deploys to the wrong fleet.\n",
    "items": {
     "type": "string"
    }
   },
   "version": {
    "type": "integer",
    "description": "**Immutable once deployed anywhere.** A change makes a new version, and the old one stays readable — a workstation still running v2.3 must be able to say what v2.3 was.\n"
   },
   "settings": {
    "type": "object",
    "additionalProperties": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "deploying",
     "deployed",
     "superseded",
     "rolledBack"
    ]
   },
   "deployedCount": {
    "type": "integer",
    "readOnly": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ConfigureWorkstationRequest": {
  "type": "object",
  "required": [
   "name",
   "saleBoardId"
  ],
  "properties": {
   "cashierInputMode": {
    "type": "string",
    "enum": [
     "keyboard",
     "touch",
     "scanner",
     "hybrid"
    ],
    "default": "hybrid",
    "description": "BL-061. **A till operator who touch-types is slower on a touchscreen and a new starter is faster.** The mode is per workstation because the operator is.\n"
   },
   "guestDisplayContent": {
    "type": "array",
    "description": "**What the guest-facing screen shows while a sale is in progress.** Line items always; the rest is the venue's choice — and **a second screen showing nothing is a second screen the guest ignores when it does show something that matters.**\n",
    "items": {
     "type": "string",
     "enum": [
      "lineItems",
      "total",
      "loyaltyBalance",
      "promotions",
      "branding",
      "upsell",
      "queuePosition"
     ]
    }
   },
   "loadedMediaStockId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-095. **Neither which stock a printer is loaded with nor how much is left.** A till that runs out of wristbands mid-queue is an outage nobody predicted, and the stock is inventory like anything else — this names which.\n"
   },
   "mediaStockRemaining": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "Decremented on issue. **The number that turns a surprise into a reorder**, and it is read-only because the count comes from what was printed rather than from somebody's estimate.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "saleBoardId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "devices": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/DeviceBinding"
    }
   },
   "deploymentProfile": {
    "$ref": "#/components/schemas/DeploymentProfile"
   },
   "edgeNodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ConnectivityPolicy": {
  "type": "object",
  "x-ticvai-persistence": "platform.connectivity_policy",
  "description": "Board 5 of the client's POS set, and the second of the two genuine gaps. **Nothing in the package held a threshold**, so a device that flips offline on one dropped packet and one that waits five minutes were the same product.\n**Going offline and coming back need different thresholds.** Symmetric ones produce a workstation that flaps — offline, online, offline — across a marginal connection, and each flap is a sync.\n",
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
   "failuresBeforeOffline": {
    "type": "integer",
    "default": 3,
    "description": "**Consecutive, not cumulative.** One dropped request on a busy till is normal; three in a row is a network.\n"
   },
   "probeIntervalSeconds": {
    "type": "integer",
    "default": 15
   },
   "probeTimeoutMs": {
    "type": "integer",
    "default": 2000
   },
   "successesBeforeOnline": {
    "type": "integer",
    "default": 5,
    "description": "**Higher than the offline threshold, deliberately.** Coming back is where the cost is — a workstation that returns online and immediately fails has resynced for nothing.\n"
   },
   "minimumStableSeconds": {
    "type": "integer",
    "default": 30,
    "description": "How long the connection must hold before the workstation trusts it. **This is what stops the flapping**, and it is the field a venue with poor wifi will actually tune.\n"
   },
   "autoSwitch": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "CreateOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "variantId",
   "quantity",
   "quotedUnitPrice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Seated products only. Not available offline."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "quotedUnitPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the client charged, from its local bundle."
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true
   }
  }
 },
 "CreateOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "venueId",
   "channel",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key."
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for an anonymous sale. Identity and entitlement are separate."
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells."
   },
   "catalogueBundleVersion": {
    "type": "string",
    "description": "The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DeploymentProfile": {
  "type": "string",
  "description": "How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n",
  "enum": [
   "terminalLocal",
   "venueEdge",
   "thin"
  ]
 },
 "DeviceBinding": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "required": [
   "kind",
   "driver"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/DeviceKind"
   },
   "driver": {
    "type": "string",
    "description": "Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"
   },
   "identifier": {
    "type": "string",
    "description": "Serial",
    "port or network address.": null
   },
   "isRequired": {
    "type": "boolean",
    "default": false,
    "description": "When true, the workstation refuses to open a shift if the device is absent.\n"
   }
  }
 },
 "FieldType": {
  "type": "string",
  "enum": [
   "string",
   "integer",
   "decimal",
   "money",
   "boolean",
   "date",
   "dateTime",
   "uuid",
   "enum"
  ]
 },
 "MetricSource": {
  "type": "string",
  "description": "**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` is deliberately absent.** It needs the staff-assignment link that CL-01 covers, and naming a metric with no source is the defect this enum exists to prevent.\n",
  "enum": [
   "occupancy",
   "capacityUtilisation",
   "admissionRate",
   "noShowRate",
   "conversion",
   "salesByOperator",
   "salesByWorkstation",
   "waitTime",
   "throughput",
   "abandonmentRate",
   "inventoryValuation",
   "stockTurnover",
   "stockAgeing",
   "wastageRate",
   "resaleVolume",
   "resaleCommission",
   "salesByInstructor",
   "resourceUtilisation",
   "allocationUtilisation",
   "channelAllocationBurn",
   "membershipChurn",
   "membershipRenewalRate",
   "supplierDeliveryPerformance",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "assetDowntime",
   "meanTimeToRepair",
   "challengeCompletionRate",
   "attributedRevenue"
  ],
  "x-ticvai-extended": "18 August 2026",
  "x-ticvai-extension-note": "**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"
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
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
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
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderLine"
   },
   {
    "type": "object",
    "required": [
     "serverUnitPrice",
     "taxAmount",
     "netAmount",
     "grossAmount"
    ],
    "properties": {
     "serverUnitPrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "What the server computed on ingest."
     },
     "priceVariance": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"
     },
     "taxAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "netAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "grossAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "entitlementIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     }
    }
   }
  ]
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
 },
 "OrderSyncResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "accepted",
   "results"
  ],
  "properties": {
   "accepted": {
    "type": "integer"
   },
   "stoppedAtSequence": {
    "type": "integer",
    "nullable": true,
    "description": "First entry that could not be processed. Null when the batch succeeded. The client retries from here and never past it.\n"
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
        "rejected"
       ]
      },
      "orderNumber": {
       "type": "string",
       "nullable": true
      },
      "priceVariance": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Posted to the variance account. Not surfaced to the cashier."
      },
      "varianceExceedsThreshold": {
       "type": "boolean",
       "description": "True when review is required per the venue's variance threshold."
      },
      "error": {
       "$ref": "../shared/common.yaml#/components/schemas/Problem"
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
 "Payment": {
  "x-ticvai-persistence": "orders.payment",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "status",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "The amount in `tenderCurrency`, at that currency's own scale."
   },
   "fxRate": {
    "type": "number",
    "nullable": true,
    "description": "The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"
   },
   "fxRateSource": {
    "type": "string",
    "nullable": true,
    "enum": [
     "manual",
     "feed",
     "cardScheme"
    ],
    "description": "4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"
   },
   "changeCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "changeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "authorised",
     "captured",
     "pendingConfirmation",
     "declined",
     "failed",
     "voided",
     "refunded"
    ]
   },
   "providerName": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "lastInquiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "ProfileDeployment": {
  "type": "object",
  "x-ticvai-persistence": "platform.profile_deployment",
  "description": "**A deployment is an event with a date, a target and an outcome** — the client's board shows recent deployments with all three and the package had no record of any.\n**Staged rather than all-at-once by default.** Pushing a profile to 1,248 workstations simultaneously is how a venue discovers a bad profile at every till at the same moment.\n",
  "required": [
   "id",
   "profileId",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "profileId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "integer"
   },
   "targetWorkstationIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "targetFilter": {
    "type": "object",
    "nullable": true,
    "description": "By department, type or venue, where the target is a set rather than a list.",
    "additionalProperties": true
   },
   "strategy": {
    "type": "string",
    "enum": [
     "immediate",
     "staged",
     "onNextIdle"
    ],
    "default": "onNextIdle"
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
   "succeededCount": {
    "type": "integer",
    "readOnly": true
   },
   "failedCount": {
    "type": "integer",
    "readOnly": true
   },
   "failureReasons": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    },
    "description": "**Grouped, because 40 workstations failing for one reason is one problem** and a list of 40 rows is forty.\n"
   },
   "startedAt": {
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
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 },
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date"
   },
   "dateTo": {
    "type": "string",
    "format": "date"
   },
   "forceAsync": {
    "type": "boolean",
    "default": false,
    "description": "Queue regardless of size, for a result to be collected later."
   }
  }
 },
 "SaleBoardKind": {
  "type": "string",
  "enum": [
   "ticketing",
   "fnb",
   "retail",
   "mixed"
  ]
 },
 "Workstation": {
  "x-ticvai-persistence": "platform.workstation",
  "parameters": [
   {
    "$ref": "../shared/common.yaml#/components/parameters/IdempotencyKey"
   }
  ],
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "regionId",
   "scopePath",
   "saleBoard",
   "currency",
   "currencyScale",
   "timeZone"
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
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "saleBoard": {
    "type": "object",
    "description": "Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n",
    "required": [
     "id",
     "kind"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "kind": {
      "$ref": "#/components/schemas/SaleBoardKind"
     },
     "name": {
      "type": "string"
     }
    }
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"
   },
   "devices": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/DeviceBinding"
    }
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "timeZone": {
    "type": "string"
   },
   "deploymentProfile": {
    "$ref": "#/components/schemas/DeploymentProfile"
   },
   "edgeNodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Present when `deploymentProfile` is `venueEdge`."
   },
   "healthScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "readOnly": true,
    "description": "Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"
   },
   "catalogueState": {
    "$ref": "#/components/schemas/CatalogueState"
   },
   "offlineCapable": {
    "type": "boolean",
    "description": "Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 }
}
```
