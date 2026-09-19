# P08-sell-04 — P08 · Sell (4 of 4)

**5 screens · 19 operations · 15 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `AI_AUDIT_VIEW, DEVICE_VIEW, INCIDENT_REPORT, PLATFORM_RELEASE_PROMOTE, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, ROLE_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE, WORKSTATION_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **6 of these operations work offline**: getVenueSettings, listDevices, listProducts, listRoles, listSaleBoards, reportIncident
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-124` | Layout & Journey Builder | listDetail | 6 | 0 | — |
| `BO-125` | Product & Category Button Configuration | listDetail | 6 | 0 | — |
| `BO-126` | Deployment, Preview & Audit | commandCentre | 7 | 0 | — |
| `BO-142` | Store Rules, Controls & Permissions | listDetail | 4 | 0 | — |
| `BO-143` | Retail Global Settings & Controls | statusTracker | 2 | 0 | — |

## Thin screens in this batch

**BO-143 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-124",
  "name": "Layout & Journey Builder",
  "module": "Sell",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/layout-journey-builder",
   "component": "apps/venue-management-web/src/routes/sell/LayoutJourneyBuilderList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-036",
    "BO-102"
   ],
   "exitTo": [
    "BO-102",
    "BO-125"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-125",
     "trigger": "Product & Category Button Configuration",
     "provenance": "flow F95 step 2→3"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-1D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 1.dc.html#pos-1d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAuditRecords` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Layout & Journey Builder — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "listAuditRecords",
    "why": "**2 declared operations reach no component on this screen**: listAuditRecords, listDevices. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createSaleBoard",
       "provenance": "contract tenancy.yaml POST /sale-boards"
      },
      {
       "kind": "secondaryButton",
       "label": "Deploy",
       "operation": "deployConfigurationProfile",
       "provenance": "contract tenancy.yaml POST /configuration-profiles/{profileId}/deploy"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordDeviceHeartbeat",
       "provenance": "contract tenancy.yaml POST /devices/{deviceId}/heartbeat"
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
       "label": "Search layout",
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
   "loading": "The layout journey list.",
   "error": "Could not load. Names which read failed and leaves the layout journey untouched.",
   "emptyFirstRun": "No layout journey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the layout journey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateSaleBoard",
    "contract": "tenancy",
    "purpose": "Update a sale board",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
    ]
   },
   {
    "operationId": "createSaleBoard",
    "contract": "tenancy",
    "purpose": "Create a sale board",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
    ]
   },
   {
    "operationId": "deployConfigurationProfile",
    "contract": "tenancy",
    "purpose": "deployConfigurationProfile",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
    ]
   },
   {
    "operationId": "listAuditRecords",
    "contract": "tenancy",
    "purpose": "Who did what, where, and when",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDevices",
    "contract": "tenancy",
    "purpose": "List registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordDeviceHeartbeat",
    "contract": "tenancy",
    "purpose": "Device heartbeat and status",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
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
     "name": "saleBoardId",
     "from": "deepLink"
    },
    {
     "name": "deviceId",
     "from": "deepLink"
    },
    {
     "name": "profileId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders. A device opened from the registry. A profile opened from the list."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-124",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-125",
  "name": "Product & Category Button Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/product-category-button-configuration",
   "component": "apps/venue-management-web/src/routes/sell/ProductCategoryButtonConfigurationList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102",
    "BO-124"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-1E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 1.dc.html#pos-1e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWorkstationHealth` reads one of them — list, select, act",
  "purpose": "Product & Category Button Configuration — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "getWorkstationHealth",
    "why": "**2 declared operations reach no component on this screen**: getWorkstationHealth, listAlerts. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every product category button",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
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
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordDeviceHeartbeat",
       "provenance": "contract tenancy.yaml POST /devices/{deviceId}/heartbeat"
      },
      {
       "kind": "secondaryButton",
       "label": "Report",
       "operation": "reportIncident",
       "provenance": "contract maintenance.yaml POST /incidents"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search product",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product category button list.",
   "error": "Could not load. Names which read failed and leaves the product category button untouched.",
   "emptyFirstRun": "No product category button yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product category button are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateSaleBoard",
    "contract": "tenancy",
    "purpose": "Update a sale board",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWorkstationHealth",
    "contract": "tenancy",
    "purpose": "getWorkstationHealth",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordDeviceHeartbeat",
    "contract": "tenancy",
    "purpose": "Device heartbeat and status",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "reportIncident",
    "contract": "maintenance",
    "purpose": "Report an incident",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
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
     "name": "saleBoardId",
     "from": "deepLink"
    },
    {
     "name": "deviceId",
     "from": "deepLink"
    },
    {
     "name": "workstationId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders. A device opened from the registry. Resolves from the session — a till is signed into."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-125",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-126",
  "name": "Deployment, Preview & Audit",
  "module": "Sell",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/deployment-preview-audit",
   "component": "apps/venue-management-web/src/routes/sell/DeploymentPreviewAuditList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102",
    "BO-118"
   ],
   "exitTo": [
    "BO-036",
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-036",
     "trigger": "Device Registry",
     "provenance": "flow F79 step 1→2"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-1F, POS-4F** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 1.dc.html#pos-1f",
   "POS Board 4.dc.html#pos-4f"
  ],
  "pattern": "commandCentre",
  "patternReason": "3 independent reads and no read of one record — the screen watches a population rather than working one",
  "purpose": "Deployment, Preview & Audit — from the client design board, 20 August.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Audit records",
       "bindsTo": null,
       "operation": "listAuditRecords",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "metricTile",
       "label": "Sale boards",
       "bindsTo": "SaleBoard",
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      },
      {
       "kind": "metricTile",
       "label": "Workstations",
       "bindsTo": "Workstation",
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
       "label": "Deploy",
       "operation": "deployConfigurationProfile",
       "provenance": "contract tenancy.yaml POST /configuration-profiles/{profileId}/deploy"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Start",
       "operation": "startRollout",
       "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/start"
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
       "label": "Search deployment, preview",
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
   "loading": "The deployment preview audit list.",
   "error": "Could not load. Names which read failed and leaves the deployment preview audit untouched.",
   "emptyFirstRun": "No deployment preview audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deployment preview audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "deployConfigurationProfile",
    "contract": "tenancy",
    "purpose": "deployConfigurationProfile",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
    ]
   },
   {
    "operationId": "updateSaleBoard",
    "contract": "tenancy",
    "purpose": "Update a sale board",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
    ]
   },
   {
    "operationId": "listAuditRecords",
    "contract": "tenancy",
    "purpose": "Who did what, where, and when",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSaleBoards",
    "contract": "tenancy",
    "purpose": "List sale boards",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWorkstations",
    "contract": "tenancy",
    "purpose": "List workstations",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
    ]
   },
   {
    "operationId": "startRollout",
    "contract": "platform-ops",
    "purpose": "Start or continue a rollout",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
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
     "name": "saleBoardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    },
    {
     "name": "rolloutId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-126",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-142",
  "name": "Store Rules, Controls & Permissions",
  "module": "Sell",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/store-rules-controls-permissions",
   "component": "apps/venue-management-web/src/routes/ops/StoreRulesControlsPermissionsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `Retail Board 1.dc.html` frame `ret-1j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Store Rules, Controls &amp; Permissions* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 1.dc.html#ret-1j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listRoles` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Store Rules, Controls & Permissions — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "listStoreRules",
    "why": "**1 declared operation reach no component on this screen**: listStoreRules. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every store rules controls",
       "bindsTo": "Role",
       "columns": [
        "Role.id",
        "Role.code",
        "Role.name",
        "Role.description",
        "Role.permissions",
        "Role.inheritsFromRoleId",
        "Role.isSystem",
        "Role.principalCount",
        "Role.grantCount"
       ],
       "operation": "listRoles",
       "provenance": "contract identity.yaml GET /roles"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected store rules controls",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
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
       "operation": "setStoreRules",
       "provenance": "contract retail.yaml PUT /store-rules"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search store rules, controls",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The store rules controls list.",
   "error": "Could not load. Names which read failed and leaves the store rules controls untouched.",
   "emptyFirstRun": "No store rules controls yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the store rules controls are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "Operational settings for this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listRoles",
    "contract": "identity",
    "purpose": "List roles",
    "trigger": "onLoad"
   },
   {
    "operationId": "listStoreRules",
    "contract": "retail",
    "purpose": "Rules and controls in force",
    "trigger": "onLoad"
   },
   {
    "operationId": "setStoreRules",
    "contract": "retail",
    "purpose": "Change a rule",
    "trigger": "onAction",
    "invalidates": [
     "listRoles"
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
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-142",
   "note": "**Drawn by Claude Design on `Retail Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-143",
  "name": "Retail Global Settings & Controls",
  "module": "Sell",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/retail-global-settings-controls",
   "component": "apps/venue-management-web/src/routes/ops/RetailGlobalSettingsControlsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `Retail Board 1.dc.html` frame `ret-1k`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Retail Global Settings &amp; Controls* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 1.dc.html#ret-1k"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getVenueSettings` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Retail Global Settings & Controls — from the client design board, 20 August.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected retail global settings",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
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
       "operation": "setVenueSettings",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search retail global settings",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retail global settings list.",
   "error": "Could not load. Names which read failed and leaves the retail global settings untouched.",
   "emptyFirstRun": "No retail global settings yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the retail global settings are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "Operational settings for this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "setVenueSettings",
    "contract": "tenancy",
    "purpose": "Set support hours, quiet hours, segregated access and alerti",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-143",
   "note": "**Drawn by Claude Design on `Retail Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
 "createSaleBoard": {
  "method": "POST",
  "path": "/sale-boards",
  "contract": "tenancy",
  "summary": "Create a sale board",
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
  "requestBody": "SaleBoard",
  "responds": "SaleBoard"
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
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
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
 "listRoles": {
  "method": "GET",
  "path": "/roles",
  "contract": "identity",
  "summary": "List roles",
  "permission": "ROLE_MANAGE",
  "offlineCapable": true,
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
 "listSaleBoards": {
  "method": "GET",
  "path": "/sale-boards",
  "contract": "tenancy",
  "summary": "List sale boards",
  "permission": "SCOPE_VIEW",
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
   }
  ],
  "requestBody": null,
  "responds": "SaleBoard"
 },
 "listStoreRules": {
  "method": "GET",
  "path": "/store-rules",
  "contract": "retail",
  "summary": "Rules and controls in force in the store",
  "permission": "PRODUCT_VIEW",
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
  "responds": "StoreRule"
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
 "recordDeviceHeartbeat": {
  "method": "POST",
  "path": "/devices/{deviceId}/heartbeat",
  "contract": "tenancy",
  "summary": "Device heartbeat and status",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": null
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
 "setStoreRules": {
  "method": "PUT",
  "path": "/store-rules",
  "contract": "retail",
  "summary": "Change a store rule",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "StoreRule",
  "responds": "StoreRule"
 },
 "setVenueSettings": {
  "method": "PUT",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Set support hours, quiet hours, segregated access and alerting",
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
  "requestBody": "VenueSettings",
  "responds": "VenueSettings"
 },
 "startRollout": {
  "method": "POST",
  "path": "/rollouts/{rolloutId}/start",
  "contract": "platform-ops",
  "summary": "Start or continue a rollout",
  "permission": "PLATFORM_RELEASE_PROMOTE",
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
 "updateSaleBoard": {
  "method": "PUT",
  "path": "/sale-boards/{saleBoardId}",
  "contract": "tenancy",
  "summary": "Update a sale board",
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
  "requestBody": "SaleBoard",
  "responds": "SaleBoard"
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
 "SaleBoard": {
  "x-ticvai-persistence": "platform.sale_board",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "kind",
   "pages"
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
   "kind": {
    "$ref": "#/components/schemas/SaleBoardKind"
   },
   "pages": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "name",
      "sortOrder",
      "tiles"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "sortOrder": {
       "type": "integer"
      },
      "tiles": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "position",
         "kind"
        ],
        "properties": {
         "position": {
          "type": "integer"
         },
         "kind": {
          "type": "string",
          "enum": [
           "product",
           "category",
           "action",
           "spacer"
          ]
         },
         "variantId": {
          "type": "string",
          "format": "uuid",
          "nullable": true
         },
         "label": {
          "type": "string"
         },
         "colour": {
          "type": "string",
          "nullable": true
         },
         "imageAssetRef": {
          "type": "string",
          "nullable": true
         }
        }
       }
      }
     }
    }
   },
   "isActive": {
    "type": "boolean"
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
 "StoreRule": {
  "type": "object",
  "x-ticvai-persistence": "retail.store_rule",
  "description": "**Drafted 4 September.** One rule or control in force in a store - a discount limit, a refund threshold, an age check, a manager override. **A row rather than a config value** because somebody has to be able to say who changed a limit and when.",
  "required": [
   "id"
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
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "discountLimit",
     "refundThreshold",
     "ageCheck",
     "managerOverride",
     "priceOverride"
    ]
   },
   "thresholdMinor": {
    "type": "integer"
   },
   "requiresPermission": {
    "type": "string",
    "description": "The permission a person needs to act past this rule."
   },
   "enabled": {
    "type": "boolean"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string"
     },
     "windows": {
      "type": "array",
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
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string"
     },
     "to": {
      "type": "string"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string"
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       false,
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": false,
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   }
  }
 }
}
```
