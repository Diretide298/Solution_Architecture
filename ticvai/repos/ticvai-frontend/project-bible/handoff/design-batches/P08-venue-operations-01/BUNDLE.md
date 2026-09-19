# P08-venue-operations-01 — P08 · Venue Operations (1 of 2)

**10 screens · 74 operations · 69 schemas · 31 permissions**

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

- **Every control that can be refused must be gated.** 31 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_POINT_CONFIGURE, ACCESS_VALIDATE, AI_AUDIT_VIEW, ASSET_VIEW, DEVELOPER_MANAGE, DEVELOPER_VIEW, DEVICE_CONFIGURE, DEVICE_VIEW, GUEST_MANAGE, GUEST_VIEW, INCIDENT_MANAGE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **18 of these operations work offline**: getAccessPoint, getHaccpStatus, getReturnPolicy, getTableMap, getVenueSettings, getWorkstation, listAccessPoints, listAssets
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-036` | Device Registry | listDetail | 20 | 1 | — |
| `BO-044` | F&B Outlets | listDetail | 15 | 0 | — |
| `BO-058` | Reporting Home | listDetail | 11 | 1 | — |
| `BO-060` | Attendance & Footfall | listDetail | 16 | 2 | — |
| `BO-064` | Zones & Areas | listDetail | 10 | 0 | — |
| `BO-067` | Integrations | commandCentre | 5 | 0 | — |
| `BO-100` | Venue Home | listDetail | 2 | 0 | — |
| `BO-108` | Venue Operations | listDetail | 4 | 0 | — |
| `BO-127` | Hardware & Peripherals Management | listDetail | 3 | 0 | — |
| `BO-128` | Live Workstation Health Monitor | listDetail | 3 | 0 | — |

## Thin screens in this batch

**BO-128 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-036",
  "name": "Device Registry",
  "module": "Venue Operations",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/device-registry",
   "component": "apps/venue-management-web/src/routes/venue-operations/DeviceRegistryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-124"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-108",
    "BO-126"
   ],
   "transitions": [
    {
     "to": "BO-124",
     "trigger": "Layout & Journey Builder",
     "provenance": "flow F79 step 2→3, F95 step 1→2"
    },
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
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 4 board screen(s): Workstation Overview Dashboard; Workstation Registry; Workstation Details & Configuration and 1 more. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Owns POS board frame(s) POS-1A, POS-1B, POS-1C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 1.dc.html#pos-1a",
   "POS Board 1.dc.html#pos-1b",
   "POS Board 1.dc.html#pos-1c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listDevices` reads the population and `getConsentHistory` reads one of them — list, select, act",
  "purpose": "Know which handheld is where, and whether it has synced.",
  "gaps": [
   {
    "operation": "listGuestDevices",
    "why": "**11 declared operations reach no component on this screen**: listGuestDevices, getGuestConsents, getGuestLoyalty, getGuestProfile, getWishlist, searchGuests, getWorkstation, getWorkstationHealth. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every device registry",
       "bindsTo": "RegisteredDevice",
       "columns": [
        "RegisteredDevice.id",
        "RegisteredDevice.kind",
        "RegisteredDevice.driver",
        "RegisteredDevice.identifier",
        "RegisteredDevice.workstationId",
        "RegisteredDevice.model",
        "RegisteredDevice.pushToken",
        "RegisteredDevice.pushPlatform",
        "RegisteredDevice.pushFailureCount",
        "RegisteredDevice.offlineScope",
        "RegisteredDevice.firmwareVersion",
        "RegisteredDevice.isRequired"
       ],
       "operation": "listDevices",
       "provenance": "contract tenancy.yaml GET /devices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected device registry",
       "bindsTo": "ConsentRecord",
       "columns": [
        "ConsentRecord.purpose",
        "ConsentRecord.decision",
        "ConsentRecord.channels",
        "ConsentRecord.noticeVersion",
        "ConsentRecord.source",
        "ConsentRecord.recordedAt",
        "ConsentRecord.id",
        "ConsentRecord.subjectId",
        "ConsentRecord.recordedByPrincipalId",
        "ConsentRecord.supersededAt"
       ],
       "operation": "getConsentHistory",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/consents/history"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Register",
       "operation": "registerDevice",
       "provenance": "contract tenancy.yaml POST /devices"
      },
      {
       "kind": "secondaryButton",
       "label": "Adjust",
       "operation": "adjustLoyaltyPoints",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/loyalty/adjust"
      },
      {
       "kind": "destructiveButton",
       "label": "Merge",
       "operation": "mergeGuestProfiles",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/merge"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateGuestProfile",
       "provenance": "contract marketing-crm.yaml PATCH /guests/{subjectId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Configure",
       "operation": "configureWorkstation",
       "provenance": "contract tenancy.yaml PUT /workstations/{workstationId}"
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
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listDevices",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "searchGuests",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "registerDevice",
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
  "overlays": [
   {
    "id": "confirmMergeGuestProfiles",
    "component": "confirmDialog",
    "trigger": "Merge",
    "body": "**Names what `mergeGuestProfiles` changes and what it leaves alone**, in the consequence rather than the verb. A device registry this affects should be identified in the dialog, not just counted.",
    "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/merge"
   }
  ],
  "states": {
   "loading": "The device registry list.",
   "error": "Could not load. Names which read failed and leaves the device registry untouched.",
   "emptyFirstRun": "No device registry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the device registry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDevices",
    "contract": "tenancy",
    "purpose": "List registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGuestDevices",
    "contract": "marketing-crm",
    "purpose": "A guest's registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "registerDevice",
    "contract": "tenancy",
    "purpose": "Register a device",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
    ]
   },
   {
    "operationId": "adjustLoyaltyPoints",
    "contract": "marketing-crm",
    "purpose": "Manually adjust points",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
    ]
   },
   {
    "operationId": "getConsentHistory",
    "contract": "marketing-crm",
    "purpose": "Full consent history",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestConsents",
    "contract": "marketing-crm",
    "purpose": "Read a guest's consent state",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestLoyalty",
    "contract": "marketing-crm",
    "purpose": "A guest's loyalty position",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Read a guest profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWishlist",
    "contract": "marketing-crm",
    "purpose": "Read a guest's saved items",
    "trigger": "onLoad"
   },
   {
    "operationId": "mergeGuestProfiles",
    "contract": "marketing-crm",
    "purpose": "Merge a duplicate profile into this one",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
    ]
   },
   {
    "operationId": "searchGuests",
    "contract": "marketing-crm",
    "purpose": "Search guest profiles",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Amend a guest profile",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
    ]
   },
   {
    "operationId": "configureWorkstation",
    "contract": "tenancy",
    "purpose": "Configure a workstation",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
    ]
   },
   {
    "operationId": "getWorkstation",
    "contract": "tenancy",
    "purpose": "Read a workstation",
    "trigger": "onLoad"
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
    "operationId": "deployConfigurationProfile",
    "contract": "tenancy",
    "purpose": "deployConfigurationProfile",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
    ]
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
    "operationId": "recordDeviceHeartbeat",
    "contract": "tenancy",
    "purpose": "Device heartbeat and status",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
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
     "name": "subjectId",
     "from": "deepLink"
    },
    {
     "name": "workstationId",
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
   "coldEntry": "A workstation opened from the registry or an alert. A device opened from the registry. A profile opened from the list.",
   "preloaded": [
    "ConsentRecord.purpose",
    "ConsentRecord.decision",
    "ConsentRecord.channels",
    "ConsentRecord.noticeVersion",
    "ConsentRecord.source"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-036",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 20 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-044",
  "name": "F&B Outlets",
  "module": "Venue Operations",
  "requiresModule": "fnb",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/f-b-outlets",
   "component": "apps/venue-management-web/src/routes/venue-operations/FBOutletsDetail.tsx",
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
   "entryFrom": [
    "BO-108"
   ],
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
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 9 board screen(s): F&B Command Center; Outlet Management; Create / Edit Outlet and 6 more. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.** **This screen owns 18 board frames — the whole of F&B board 1 and the whole of Retail board 1.** No flow could be derived from it because **a chain of nine frames that all resolve to one screen is not a journey**, it is one screen the client drew nine views of. **That is the module system working**: a venue configuring an outlet and a venue configuring a store are the same screen with a different licence, and `requiresModule` is what makes them look different. **Worth stating rather than papering over with a single-step flow.** **Five of the 74 board chains collapse to this one screen and no others do.** The client drew nine F&B views and nine retail views of one outlet configuration surface — **which is what makes it the strongest evidence in the package that the module system is the right shape.** Nine frames per domain, one screen, and `requiresModule` is the only difference a tenant sees.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 1.dc.html#fnb-1b",
   "FnB Board 1.dc.html#fnb-1c",
   "FnB Board 1.dc.html#fnb-1d",
   "FnB Board 1.dc.html#fnb-1e",
   "FnB Board 1.dc.html#fnb-1f",
   "FnB Board 1.dc.html#fnb-1g",
   "FnB Board 1.dc.html#fnb-1h",
   "FnB Board 1.dc.html#fnb-1j",
   "FnB Board 1.dc.html#fnb-1k",
   "Retail Board 1.dc.html#ret-1b",
   "Retail Board 1.dc.html#ret-1c",
   "Retail Board 1.dc.html#ret-1d",
   "Retail Board 1.dc.html#ret-1e",
   "Retail Board 1.dc.html#ret-1f",
   "Retail Board 1.dc.html#ret-1g",
   "Retail Board 1.dc.html#ret-1h",
   "Retail Board 1.dc.html#ret-1j",
   "Retail Board 1.dc.html#ret-1k"
  ],
  "pattern": "listDetail",
  "patternReason": "`listOutlets` reads the population and `getGuestMenu` reads one of them — list, select, act",
  "purpose": "See every outlet and whether it is trading.",
  "gaps": [
   {
    "operation": "getOutletStock",
    "why": "**6 declared operations reach no component on this screen**: getOutletStock, getReturnPolicy, getTableMap, listFnbOrders, listMerchandise, getHaccpStatus. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every outlets",
       "bindsTo": "Outlet",
       "columns": [
        "Outlet.id",
        "Outlet.code",
        "Outlet.name",
        "Outlet.venueId",
        "Outlet.kind",
        "Outlet.zone",
        "Outlet.stockLocationId",
        "Outlet.costCenterId",
        "Outlet.openingHours",
        "Outlet.isActive"
       ],
       "operation": "listOutlets",
       "provenance": "contract tenancy.yaml GET /outlets"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected outlets",
       "bindsTo": "GuestMenu",
       "columns": [
        "GuestMenu.outletId",
        "GuestMenu.menuId",
        "GuestMenu.name",
        "GuestMenu.inForceUntil",
        "GuestMenu.currency",
        "GuestMenu.currencyScale",
        "GuestMenu.sections"
       ],
       "operation": "getGuestMenu",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/guest-menu"
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
       "operation": "createOutlet",
       "provenance": "contract tenancy.yaml POST /outlets"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordWaste",
       "provenance": "contract fnb.yaml POST /outlets/{outletId}/waste"
      },
      {
       "kind": "secondaryButton",
       "label": "Reserve",
       "operation": "reserveMerchandise",
       "provenance": "contract retail.yaml POST /outlets/{outletId}/reserve"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setReturnPolicy",
       "provenance": "contract retail.yaml PUT /outlets/{outletId}/return-policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setTableLayout",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateOutlet",
       "provenance": "contract tenancy.yaml PATCH /outlets/{outletId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Sign",
       "operation": "signCorrectiveAction",
       "provenance": "contract fnb.yaml POST /food-safety/corrective-actions/{actionId}/sign"
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
       "impliedBy": "listOutlets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createOutlet",
       "label": "Create outlet",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createOutlet",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The outlets list.",
   "error": "Could not load. Names which read failed and leaves the outlets untouched.",
   "emptyFirstRun": "No outlets yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the outlets are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOutlets",
    "contract": "tenancy",
    "purpose": "List outlets",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestMenu",
    "contract": "fnb",
    "purpose": "The menu a guest sees",
    "trigger": "onLoad"
   },
   {
    "operationId": "createOutlet",
    "contract": "tenancy",
    "purpose": "Create an outlet",
    "trigger": "onAction",
    "invalidates": [
     "listOutlets"
    ]
   },
   {
    "operationId": "getOutletStock",
    "contract": "retail",
    "purpose": "Stock across an outlet",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReturnPolicy",
    "contract": "retail",
    "purpose": "Read the retail return policy",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTableMap",
    "contract": "fnb",
    "purpose": "Table map with live state",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordWaste",
    "contract": "fnb",
    "purpose": "Record waste",
    "trigger": "onAction",
    "invalidates": [
     "listOutlets"
    ]
   },
   {
    "operationId": "reserveMerchandise",
    "contract": "retail",
    "purpose": "Reserve an item for collection",
    "trigger": "onAction",
    "invalidates": [
     "listOutlets"
    ]
   },
   {
    "operationId": "setReturnPolicy",
    "contract": "retail",
    "purpose": "Set the retail return policy",
    "trigger": "onAction",
    "invalidates": [
     "listOutlets"
    ]
   },
   {
    "operationId": "setTableLayout",
    "contract": "fnb",
    "purpose": "Configure the table layout",
    "trigger": "onAction",
    "invalidates": [
     "listOutlets"
    ]
   },
   {
    "operationId": "updateOutlet",
    "contract": "tenancy",
    "purpose": "Amend an outlet",
    "trigger": "onAction",
    "invalidates": [
     "listOutlets"
    ]
   },
   {
    "operationId": "listFnbOrders",
    "contract": "fnb",
    "purpose": "List F&B orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMerchandise",
    "contract": "retail",
    "purpose": "List merchandise",
    "trigger": "onLoad"
   },
   {
    "operationId": "getHaccpStatus",
    "contract": "fnb",
    "purpose": "getHaccpStatus",
    "trigger": "onLoad"
   },
   {
    "operationId": "signCorrectiveAction",
    "contract": "fnb",
    "purpose": "signCorrectiveAction",
    "trigger": "onAction",
    "invalidates": [
     "listOutlets"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "outletId",
     "from": "deepLink"
    },
    {
     "name": "actionId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `outletId`, `actionId`.",
   "preloaded": [
    "GuestMenu.outletId",
    "GuestMenu.menuId",
    "GuestMenu.name",
    "GuestMenu.inForceUntil",
    "GuestMenu.currency"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-044",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 15 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-058",
  "name": "Reporting Home",
  "module": "Venue Operations",
  "requiresModule": "analytics",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/reporting-home",
   "component": "apps/venue-management-web/src/routes/venue-operations/ReportingHomeDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-061"
   ],
   "inferred": true,
   "fromFlows": true,
   "entryFrom": [
    "BO-108"
   ],
   "transitions": [
    {
     "to": "BO-061",
     "trigger": "Scheduled Reports",
     "provenance": "flow F107 step 1→2",
     "operation": "updateReport"
    },
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
    },
    {
     "to": "EMP-020",
     "trigger": "The answer arrives with its sources",
     "provenance": "flow F20 step 1→2",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Retail board operations wired 24 August.** **Cross-platform navigation removed 24 August**: EMP-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 6.dc.html#ret-6h"
  ],
  "pattern": "listDetail",
  "patternReason": "`listReports` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "Find the report rather than build it.",
  "gaps": [
   {
    "operation": "getReport",
    "why": "**2 declared operations reach no component on this screen**: getReport, listReportExecutions. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every reporting home",
       "bindsTo": "ReportDefinition",
       "columns": [
        "ReportDefinition.name",
        "ReportDefinition.description",
        "ReportDefinition.category",
        "ReportDefinition.dataSource",
        "ReportDefinition.columns",
        "ReportDefinition.filters",
        "ReportDefinition.groupBy",
        "ReportDefinition.parameters",
        "ReportDefinition.requiredPermission",
        "ReportDefinition.maxDateRangeDays",
        "ReportDefinition.id",
        "ReportDefinition.isSystem"
       ],
       "operation": "listReports",
       "provenance": "contract reporting.yaml GET /reports"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reporting home",
       "bindsTo": "FinancialReport",
       "columns": [
        "FinancialReport.report",
        "FinancialReport.fiscalPeriodId",
        "FinancialReport.legalEntityId",
        "FinancialReport.currency",
        "FinancialReport.currencyScale",
        "FinancialReport.generatedAt",
        "FinancialReport.sections"
       ],
       "operation": "getFinancialReport",
       "provenance": "contract finance.yaml GET /reports/financial"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save",
       "operation": "saveNaturalLanguageQuery",
       "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateReport",
       "provenance": "contract reporting.yaml PUT /reports/{reportId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createReportSchedule",
       "provenance": "contract reporting.yaml POST /report-schedules"
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
       "impliedBy": "listReports",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "deleteReport",
       "label": "Delete report",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "runReport",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteReport",
    "component": "confirmDialog",
    "trigger": "Delete",
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A reporting home this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
   }
  ],
  "states": {
   "loading": "The reporting home list.",
   "error": "Could not load. Names which read failed and leaves the reporting home untouched.",
   "emptyFirstRun": "No reporting home yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reporting home are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "List available report definitions",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Create a custom report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "deleteReport",
    "contract": "reporting",
    "purpose": "Retire a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "getFinancialReport",
    "contract": "finance",
    "purpose": "P&L, balance sheet or cash flow",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReport",
    "contract": "reporting",
    "purpose": "Read a report definition",
    "trigger": "onLoad"
   },
   {
    "operationId": "saveNaturalLanguageQuery",
    "contract": "reporting",
    "purpose": "Save a natural-language answer as a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Publish a new version of a definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "createReportSchedule",
    "contract": "reporting",
    "purpose": "Schedule a report",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "listReportExecutions",
    "contract": "reporting",
    "purpose": "List executions",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom.",
   "preloaded": [
    "FinancialReport.report",
    "FinancialReport.fiscalPeriodId",
    "FinancialReport.legalEntityId",
    "FinancialReport.currency",
    "FinancialReport.currencyScale"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-058",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-060",
  "name": "Attendance & Footfall",
  "module": "Venue Operations",
  "requiresModule": "analytics",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/attendance-footfall",
   "component": "apps/venue-management-web/src/routes/venue-operations/AttendanceFootfallDetail.tsx",
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
   "entryFrom": [
    "BO-061",
    "BO-108"
   ],
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
  "patternReason": "`listScans` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "See how many people actually came in.",
  "gaps": [
   {
    "operation": "getOfflinePackage",
    "why": "**3 declared operations reach no component on this screen**: getOfflinePackage, getReport, listReports. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every attendance footfall",
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
       "label": "The selected attendance footfall",
       "bindsTo": "FinancialReport",
       "columns": [
        "FinancialReport.report",
        "FinancialReport.fiscalPeriodId",
        "FinancialReport.legalEntityId",
        "FinancialReport.currency",
        "FinancialReport.currencyScale",
        "FinancialReport.generatedAt",
        "FinancialReport.sections"
       ],
       "operation": "getFinancialReport",
       "provenance": "contract finance.yaml GET /reports/financial"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
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
       "label": "Save",
       "operation": "saveNaturalLanguageQuery",
       "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateReport",
       "provenance": "contract reporting.yaml PUT /reports/{reportId}"
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
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "deleteReport",
       "label": "Delete report",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listReports",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
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
       "impliedBy": "runReport",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteReport",
    "component": "confirmDialog",
    "trigger": "Delete",
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A attendance footfall this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
   },
   {
    "id": "confirmOverrideAccess",
    "component": "confirmDialog",
    "trigger": "Override",
    "body": "**Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A attendance footfall this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml POST /access/override"
   }
  ],
  "states": {
   "loading": "The attendance footfall list.",
   "error": "Could not load. Names which read failed and leaves the attendance footfall untouched.",
   "emptyFirstRun": "No attendance footfall yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attendance footfall are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
    "trigger": "onLoad"
   },
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Create a custom report definition",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "deleteReport",
    "contract": "reporting",
    "purpose": "Retire a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   },
   {
    "operationId": "getFinancialReport",
    "contract": "finance",
    "purpose": "P&L, balance sheet or cash flow",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReport",
    "contract": "reporting",
    "purpose": "Read a report definition",
    "trigger": "onLoad"
   },
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "List available report definitions",
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
    "operationId": "saveNaturalLanguageQuery",
    "contract": "reporting",
    "purpose": "Save a natural-language answer as a report definition",
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
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Publish a new version of a definition",
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
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom.",
   "preloaded": [
    "FinancialReport.report",
    "FinancialReport.fiscalPeriodId",
    "FinancialReport.legalEntityId",
    "FinancialReport.currency",
    "FinancialReport.currencyScale"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-060"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 16 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-064",
  "name": "Zones & Areas",
  "module": "Venue Operations",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/zones-areas",
   "component": "apps/venue-management-web/src/routes/venue-operations/ZonesAreasDetail.tsx",
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
   "entryFrom": [
    "BO-108"
   ],
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
  "patternReason": "`listOrgUnits` reads the population and `getAccessPoint` reads one of them — list, select, act",
  "purpose": "Divide the venue into the things gates control.",
  "gaps": [
   {
    "operation": "listAccessPoints",
    "why": "**2 declared operations reach no component on this screen**: listAccessPoints, getOrgUnit. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every zones areas",
       "bindsTo": "OrgUnit",
       "columns": [
        "OrgUnit.id",
        "OrgUnit.level",
        "OrgUnit.parentId",
        "OrgUnit.path",
        "OrgUnit.code",
        "OrgUnit.name",
        "OrgUnit.isActive",
        "OrgUnit.childCount"
       ],
       "operation": "listOrgUnits",
       "provenance": "contract tenancy.yaml GET /org-units"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected zones areas",
       "bindsTo": "AccessPoint",
       "columns": [
        "AccessPoint.id",
        "AccessPoint.code",
        "AccessPoint.name",
        "AccessPoint.venueId",
        "AccessPoint.scopePath",
        "AccessPoint.externalCredentialSources",
        "AccessPoint.scanAnomalyRules",
        "AccessPoint.operatingMode",
        "AccessPoint.vehicleLocationCapture",
        "AccessPoint.mode",
        "AccessPoint.direction",
        "AccessPoint.antiPassbackEnabled",
        "AccessPoint.isActive",
        "AccessPoint.lastHeartbeatAt"
       ],
       "operation": "getAccessPoint",
       "provenance": "contract access.yaml GET /access-points/{accessPointId}"
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
       "operation": "createAccessPoint",
       "provenance": "contract access.yaml POST /access-points"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createOrgUnit",
       "provenance": "contract tenancy.yaml POST /org-units"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAccessPointGeofence",
       "provenance": "contract access.yaml PUT /access-points/{accessPointId}/geofence"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setTurnstileMode",
       "provenance": "contract access.yaml PUT /access-points/{accessPointId}/mode"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateAccessPoint",
       "provenance": "contract access.yaml PATCH /access-points/{accessPointId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateOrgUnit",
       "provenance": "contract tenancy.yaml PATCH /org-units/{orgUnitId}"
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
       "impliedBy": "listOrgUnits",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createAccessPoint",
       "label": "Create access point",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAccessPoint",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The zones areas list.",
   "error": "Could not load. Names which read failed and leaves the zones areas untouched.",
   "emptyFirstRun": "No zones areas yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the zones areas are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrgUnits",
    "contract": "tenancy",
    "purpose": "List scope nodes visible to the session",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "List access points",
    "trigger": "onLoad"
   },
   {
    "operationId": "createAccessPoint",
    "contract": "access",
    "purpose": "Create an access point",
    "trigger": "onAction",
    "invalidates": [
     "listOrgUnits"
    ]
   },
   {
    "operationId": "createOrgUnit",
    "contract": "tenancy",
    "purpose": "Create a scope node",
    "trigger": "onAction",
    "invalidates": [
     "listOrgUnits"
    ]
   },
   {
    "operationId": "getAccessPoint",
    "contract": "access",
    "purpose": "Read an access point",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrgUnit",
    "contract": "tenancy",
    "purpose": "Read a scope node",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAccessPointGeofence",
    "contract": "access",
    "purpose": "Set a geofence for handheld validation",
    "trigger": "onAction",
    "invalidates": [
     "listOrgUnits"
    ]
   },
   {
    "operationId": "setTurnstileMode",
    "contract": "access",
    "purpose": "Set the operating mode of an access point",
    "trigger": "onAction",
    "invalidates": [
     "listOrgUnits"
    ]
   },
   {
    "operationId": "updateAccessPoint",
    "contract": "access",
    "purpose": "Update an access point",
    "trigger": "onAction",
    "invalidates": [
     "listOrgUnits"
    ]
   },
   {
    "operationId": "updateOrgUnit",
    "contract": "tenancy",
    "purpose": "Rename or deactivate a scope node",
    "trigger": "onAction",
    "invalidates": [
     "listOrgUnits"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "accessPointId",
     "from": "deepLink"
    },
    {
     "name": "orgUnitId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `accessPointId`, `orgUnitId`.",
   "preloaded": [
    "AccessPoint.id",
    "AccessPoint.code",
    "AccessPoint.name",
    "AccessPoint.venueId",
    "AccessPoint.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-064"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-067",
  "name": "Integrations",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/integrations",
   "component": "apps/venue-management-web/src/routes/venue-operations/IntegrationsDetail.tsx",
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
   "entryFrom": [
    "BO-108"
   ],
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
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 31 August** — `Seat Platform Board 13.dc.html` frame `seatp-13d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Integrations* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "Seat Platform Board 13.dc.html#seatp-13d"
  ],
  "pattern": "commandCentre",
  "patternReason": "3 independent reads and no read of one record — the screen watches a population rather than working one",
  "purpose": "Connect the venue to the systems around it.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Api clients",
       "bindsTo": "ApiClient",
       "operation": "listApiClients",
       "provenance": "contract public-api.yaml GET /api-clients"
      },
      {
       "kind": "metricTile",
       "label": "Webhook subscriptions",
       "bindsTo": "WebhookSubscription",
       "operation": "listWebhookSubscriptions",
       "provenance": "contract public-api.yaml GET /webhook-subscriptions"
      },
      {
       "kind": "metricTile",
       "label": "Webhook deliveries",
       "bindsTo": "WebhookDelivery",
       "operation": "listWebhookDeliveries",
       "provenance": "contract public-api.yaml GET /webhook-subscriptions/{subscriptionId}/deliveries"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every integrations",
       "bindsTo": "ApiClient",
       "columns": [
        "ApiClient.id",
        "ApiClient.developerId",
        "ApiClient.name",
        "ApiClient.clientId",
        "ApiClient.environment",
        "ApiClient.scopes",
        "ApiClient.allowedTenantIds",
        "ApiClient.ipAllowList",
        "ApiClient.status",
        "ApiClient.lastUsedAt"
       ],
       "operation": "listApiClients",
       "provenance": "contract public-api.yaml GET /api-clients"
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
       "operation": "createApiClient",
       "provenance": "contract public-api.yaml POST /api-clients"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createWebhookSubscription",
       "provenance": "contract public-api.yaml POST /webhook-subscriptions"
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Detail loads",
   "error": "Could not load",
   "emptyFirstRun": "Not found — it may have been deleted or moved out of scope",
   "emptyNoResults": "The filter narrowed it and the integrations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "API clients this tenant has issued",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWebhookSubscriptions",
    "contract": "public-api",
    "purpose": "Subscriptions and their targets",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWebhookDeliveries",
    "contract": "public-api",
    "purpose": "Deliveries for one subscription, and which failed",
    "trigger": "onLoad"
   },
   {
    "operationId": "createApiClient",
    "contract": "public-api",
    "purpose": "Issue a client",
    "trigger": "onAction",
    "invalidates": [
     "listApiClients"
    ]
   },
   {
    "operationId": "createWebhookSubscription",
    "contract": "public-api",
    "purpose": "Subscribe an endpoint",
    "trigger": "onAction",
    "invalidates": [
     "listApiClients"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subscriptionId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Deliveries belong to a subscription**, so the list is reached from the subscription that owns them. Opened without one the screen shows the subscriptions and says so — never an empty delivery log, which reads as *nothing failed*."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-067",
   "note": "**Drawn by Claude Design on `Seat Platform Board 13.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-100",
  "name": "Venue Home",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/home",
   "component": "apps/venue-management-web/src/routes/home/VenueHomeDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "BO-101",
    "BO-102",
    "BO-103",
    "BO-104",
    "BO-105",
    "BO-106",
    "BO-107",
    "BO-108",
    "BO-364",
    "BO-374",
    "BO-384",
    "BO-394",
    "BO-404",
    "BO-414",
    "BO-424",
    "BO-434",
    "BO-444",
    "BO-454",
    "BO-464",
    "BO-474",
    "BO-484",
    "BO-494",
    "BO-504",
    "BO-514",
    "BO-524",
    "BO-534",
    "BO-544",
    "BO-554",
    "BO-564",
    "BO-574",
    "BO-584",
    "BO-594",
    "BO-595",
    "BO-605"
   ],
   "entryFrom": [
    "BO-108",
    "BO-594",
    "BO-595",
    "BO-605"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-374",
     "trigger": "Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-384",
     "trigger": "Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    },
    {
     "to": "BO-101",
     "trigger": "Orders & Money",
     "provenance": "structural — BO-100 is P08's home screen and its exits are its launcher"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "structural — BO-100 is P08's home screen and its exits are its launcher"
    },
    {
     "to": "BO-103",
     "trigger": "Access & Venue",
     "provenance": "structural — BO-100 is P08's home screen and its exits are its launcher"
    },
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "provenance": "structural — BO-100 is P08's home screen and its exits are its launcher"
    },
    {
     "to": "BO-105",
     "trigger": "Stock & Supply",
     "provenance": "structural — BO-100 is P08's home screen and its exits are its launcher"
    },
    {
     "to": "BO-106",
     "trigger": "People & Access Rights",
     "provenance": "structural — BO-100 is P08's home screen and its exits are its launcher"
    },
    {
     "to": "BO-107",
     "trigger": "Guests & Marketing",
     "provenance": "structural — BO-100 is P08's home screen and its exits are its launcher"
    },
    {
     "to": "BO-108",
     "trigger": "Venue Operations",
     "provenance": "structural — BO-100 is P08's home screen and its exits are its launcher"
    },
    {
     "to": "BO-394",
     "trigger": "Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-484",
     "trigger": "Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-404",
     "trigger": "Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-414",
     "trigger": "Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-424",
     "trigger": "Gameplay Validation Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-434",
     "trigger": "Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-444",
     "trigger": "Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-454",
     "trigger": "Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-464",
     "trigger": "Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-474",
     "trigger": "Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-494",
     "trigger": "Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-584",
     "trigger": "Rental Executive Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-504",
     "trigger": "Rental Inventory Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-514",
     "trigger": "Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-524",
     "trigger": "Rental Pricing Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "BO-534",
     "trigger": "Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-544",
     "trigger": "Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-554",
     "trigger": "Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-564",
     "trigger": "Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-574",
     "trigger": "Maintenance Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-595",
     "trigger": "AI Setup Command Center",
     "provenance": "structural — Subscription board 7 on P08, 11 September 2026"
    },
    {
     "to": "BO-605",
     "trigger": "Go-Live Readiness Command Center",
     "provenance": "structural — Subscription board 8 on P08, 11 September 2026"
    },
    {
     "to": "BO-594",
     "trigger": "Environment Ready & Handoff to AI Setup",
     "provenance": "structural — Subscription board 6 on P08, 11 September 2026"
    }
   ]
  },
  "notes": "**Built 20 August because P08 had none.** `BO-001 Queue Directory` was the declared entry point to a 99-screen back office — it exits to four queue screens, and **93 screens hung off nothing.** A back office entered through a queue list. **The module was also one bucket holding 72 of 99 screens**, so there was nothing for a home screen to point at; sections were derived from the contract each screen principally calls.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listShifts` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "The screen a venue manager opens in the morning, and the only way into everything else.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every venue home",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber"
       ],
       "operation": "listShifts",
       "provenance": "contract shift.yaml GET /shifts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected venue home",
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
     "name": "sideNav",
     "slot": "carried",
     "components": [
      {
       "kind": "treeNav",
       "bindsTo": "sections",
       "notes": "The eight sections. **Persistent — a back office is a place somebody works all day**, and a nav that disappears on every detail screen makes them use the browser back button as navigation.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "metricTile",
       "notes": "Today: takings, admissions, open shifts, items needing attention. **Four, not twelve** — a tile nobody acts on is a tile that trains people to ignore the row.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "bindsTo": "sections",
       "notes": "One card per section with its count of items needing attention. **The count is the point** — a section with nothing pending should look different from one with eleven approvals waiting.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Alerts that crossed a threshold, from VenueSettings.alerting. **On-platform and markable as read** (CF-134).",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tiles render in place; each resolves on its own so one slow source does not hold the page.",
   "error": "Could not load the summary. **Every section is still reachable** — this screen is a landing page, and a failed tile must not block navigation.",
   "emptyFirstRun": "**A venue on its first morning.** No shifts, no orders, no stock. The state links to the opening checklist rather than showing eight empty tiles — **a dashboard of zeroes teaches a new manager nothing.**",
   "emptyNoResults": "Nothing happened in the window selected. Yesterday and today are the useful defaults.",
   "emptyNoAccess": "**Sections you cannot open are not shown.** A manager with no finance permission sees seven sections, not eight greyed out — a menu that lists what you may not do is a menu that invites a support ticket."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What this venue is configured to do",
    "trigger": "onLoad"
   },
   {
    "operationId": "listShifts",
    "contract": "shift",
    "purpose": "Who is on and what has been taken",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-100"
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
  "id": "BO-108",
  "name": "Venue Operations",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations",
   "component": "apps/venue-management-web/src/routes/home/VenueOperationsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-036",
    "BO-044",
    "BO-058",
    "BO-060",
    "BO-064",
    "BO-067",
    "BO-100",
    "BO-127",
    "BO-128",
    "BO-129",
    "BO-130",
    "BO-131",
    "BO-132",
    "BO-133"
   ],
   "transitions": [
    {
     "to": "BO-036",
     "trigger": "Device Registry",
     "carries": [
      "deviceId",
      "profileId",
      "subjectId",
      "venueId",
      "workstationId"
     ],
     "provenance": "derived — BO-036 declares entryState.params deviceId, profileId, subjectId, venueId, workstationId, so an edge into it must carry them"
    },
    {
     "to": "BO-044",
     "trigger": "F&B Outlets",
     "carries": [
      "actionId",
      "outletId"
     ],
     "provenance": "derived — BO-044 declares entryState.params actionId, outletId, so an edge into it must carry them"
    },
    {
     "to": "BO-058",
     "trigger": "Reporting Home",
     "carries": [
      "conversationId",
      "reportId"
     ],
     "provenance": "derived — BO-058 declares entryState.params conversationId, reportId, so an edge into it must carry them"
    },
    {
     "to": "BO-060",
     "trigger": "Attendance & Footfall",
     "carries": [
      "conversationId",
      "reportId"
     ],
     "provenance": "derived — BO-060 declares entryState.params conversationId, reportId, so an edge into it must carry them"
    },
    {
     "to": "BO-064",
     "trigger": "Zones & Areas",
     "carries": [
      "accessPointId",
      "orgUnitId"
     ],
     "provenance": "derived — BO-064 declares entryState.params accessPointId, orgUnitId, so an edge into it must carry them"
    },
    {
     "to": "BO-067",
     "trigger": "Integrations",
     "carries": [
      "subscriptionId"
     ],
     "provenance": "derived — BO-067 declares entryState.params subscriptionId, so an edge into it must carry them"
    },
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-127",
     "trigger": "Hardware & Peripherals Management",
     "carries": [
      "deviceId",
      "venueId"
     ],
     "provenance": "derived — BO-127 declares entryState.params deviceId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-128",
     "trigger": "Live Workstation Health Monitor",
     "carries": [
      "venueId",
      "workstationId"
     ],
     "provenance": "derived — BO-128 declares entryState.params venueId, workstationId, so an edge into it must carry them"
    },
    {
     "to": "BO-129",
     "trigger": "Software, Configuration & Version Management",
     "carries": [
      "profileId",
      "venueId",
      "workstationId"
     ],
     "provenance": "derived — BO-129 declares entryState.params profileId, venueId, workstationId, so an edge into it must carry them"
    },
    {
     "to": "BO-130",
     "trigger": "Offline Policy & Rules Configuration",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-130 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-131",
     "trigger": "Connectivity & Auto-Switch Settings",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-131 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-132",
     "trigger": "Offline Transaction Monitor & Sync Queue",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-132 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-133",
     "trigger": "Offline Alerts, Limits & Audit",
     "carries": [
      "reportId",
      "requestId",
      "venueId"
     ],
     "provenance": "derived — BO-133 declares entryState.params reportId, requestId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Section landing. **6 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listWorkOrders` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in venue operations, and what in it needs attention.",
  "gaps": [
   {
    "operation": "listIncidents",
    "why": "**2 declared operations reach no component on this screen**: listIncidents, listAssets. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every venue operations",
       "bindsTo": "WorkOrder",
       "columns": [
        "WorkOrder.downtimeMinutes",
        "WorkOrder.rootCause",
        "WorkOrder.rootCauseNote",
        "WorkOrder.escalatedAt",
        "WorkOrder.escalationLevel",
        "WorkOrder.id",
        "WorkOrder.workOrderNumber",
        "WorkOrder.title",
        "WorkOrder.venueId",
        "WorkOrder.assetId",
        "WorkOrder.assetName",
        "WorkOrder.status"
       ],
       "operation": "listWorkOrders",
       "provenance": "contract maintenance.yaml GET /work-orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected venue operations",
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
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "6 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search venue operations",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in venue operations yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for venue operations. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWorkOrders",
    "contract": "maintenance",
    "purpose": "Work raised and its state",
    "trigger": "onLoad"
   },
   {
    "operationId": "listIncidents",
    "contract": "maintenance",
    "purpose": "Incidents open in the venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAssets",
    "contract": "maintenance",
    "purpose": "Assets and their condition",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-108"
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
  "id": "BO-127",
  "name": "Hardware & Peripherals Management",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/hardware-peripherals-management",
   "component": "apps/venue-management-web/src/routes/ops/HardwarePeripheralsManagementList.tsx",
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
  "patternReason": "`listDevices` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Hardware & Peripherals Management — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every hardware peripherals",
       "bindsTo": "RegisteredDevice",
       "columns": [
        "RegisteredDevice.id",
        "RegisteredDevice.kind",
        "RegisteredDevice.driver",
        "RegisteredDevice.identifier",
        "RegisteredDevice.workstationId",
        "RegisteredDevice.model",
        "RegisteredDevice.pushToken",
        "RegisteredDevice.pushPlatform",
        "RegisteredDevice.pushFailureCount",
        "RegisteredDevice.offlineScope",
        "RegisteredDevice.firmwareVersion",
        "RegisteredDevice.isRequired"
       ],
       "operation": "listDevices",
       "provenance": "contract tenancy.yaml GET /devices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected hardware peripherals",
       "bindsTo": "RegisteredDevice",
       "columns": [
        "RegisteredDevice.id",
        "RegisteredDevice.kind",
        "RegisteredDevice.driver",
        "RegisteredDevice.identifier",
        "RegisteredDevice.workstationId",
        "RegisteredDevice.model",
        "RegisteredDevice.pushToken",
        "RegisteredDevice.pushPlatform",
        "RegisteredDevice.pushFailureCount",
        "RegisteredDevice.offlineScope",
        "RegisteredDevice.firmwareVersion",
        "RegisteredDevice.isRequired",
        "RegisteredDevice.status",
        "RegisteredDevice.batteryPercent",
        "RegisteredDevice.lastCheckedAt",
        "RegisteredDevice.health"
       ],
       "operation": "listDevices",
       "provenance": "contract tenancy.yaml GET /devices"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Register",
       "operation": "registerDevice",
       "provenance": "contract tenancy.yaml POST /devices"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordDeviceHeartbeat",
       "provenance": "contract tenancy.yaml POST /devices/{deviceId}/heartbeat"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search hardware",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hardware peripherals list.",
   "error": "Could not load. Names which read failed and leaves the hardware peripherals untouched.",
   "emptyFirstRun": "No hardware peripherals yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hardware peripherals are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDevices",
    "contract": "tenancy",
    "purpose": "List registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "registerDevice",
    "contract": "tenancy",
    "purpose": "Register a device",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
    ]
   },
   {
    "operationId": "recordDeviceHeartbeat",
    "contract": "tenancy",
    "purpose": "Device heartbeat and status",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
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
     "name": "deviceId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first.",
   "preloaded": [
    "RegisteredDevice.id",
    "RegisteredDevice.kind",
    "RegisteredDevice.driver",
    "RegisteredDevice.identifier",
    "RegisteredDevice.workstationId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-127"
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
  "id": "BO-128",
  "name": "Live Workstation Health Monitor",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/live-workstation-health-monitor",
   "component": "apps/venue-management-web/src/routes/ops/LiveWorkstationHealthMonitorList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-037",
    "BO-108"
   ],
   "exitTo": [
    "BO-108",
    "BO-129"
   ],
   "inferred": false,
   "notes": "**Returns to BO-108.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-129",
     "trigger": "Software, Configuration & Version Management",
     "provenance": "flow F89 step 2→3",
     "operation": "setOfflinePolicy"
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
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-5B** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 5.dc.html#pos-5b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listWorkstations` reads the population and `getWorkstationHealth` reads one of them — list, select, act",
  "purpose": "Live Workstation Health Monitor — from the client design board, 20 August.",
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
       "label": "Every live workstation health",
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
       "operation": "setOfflinePolicy",
       "provenance": "contract tenancy.yaml PUT /offline-policy"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search live workstation health monitor",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live workstation health list.",
   "error": "Could not load. Names which read failed and leaves the live workstation health untouched.",
   "emptyFirstRun": "No live workstation health yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live workstation health are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
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
    "operationId": "setOfflinePolicy",
    "contract": "tenancy",
    "purpose": "setOfflinePolicy",
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
     "name": "workstationId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-128",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "adjustLoyaltyPoints": {
  "method": "POST",
  "path": "/guests/{subjectId}/loyalty/adjust",
  "contract": "marketing-crm",
  "summary": "Manually adjust points",
  "permission": "LEDGER_POST",
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
  "responds": "LoyaltyPosition"
 },
 "askReportingQuestion": {
  "method": "POST",
  "path": "/reports/ask",
  "contract": "reporting",
  "summary": "Natural-language reporting query",
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
  "requestBody": null,
  "responds": "NaturalLanguageAnswer"
 },
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
 "createAccessPoint": {
  "method": "POST",
  "path": "/access-points",
  "contract": "access",
  "summary": "Create an access point",
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
  "requestBody": "CreateAccessPointRequest",
  "responds": "AccessPoint"
 },
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
 "createOrgUnit": {
  "method": "POST",
  "path": "/org-units",
  "contract": "tenancy",
  "summary": "Create a scope node",
  "permission": "SCOPE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "brand",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateScopeNodeRequest",
  "responds": "OrgUnit"
 },
 "createOutlet": {
  "method": "POST",
  "path": "/outlets",
  "contract": "tenancy",
  "summary": "Create an outlet",
  "permission": "REGION_CONFIGURE",
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
  "requestBody": "Outlet",
  "responds": "Outlet"
 },
 "createReport": {
  "method": "POST",
  "path": "/reports",
  "contract": "reporting",
  "summary": "Create a custom report definition",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
 },
 "createReportSchedule": {
  "method": "POST",
  "path": "/report-schedules",
  "contract": "reporting",
  "summary": "Schedule a report",
  "permission": "REPORT_SCHEDULE",
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
  "requestBody": "CreateReportScheduleRequest",
  "responds": "ReportSchedule"
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
 "deleteReport": {
  "method": "DELETE",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Retire a report definition",
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
  "requestBody": null,
  "responds": null
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
 "getAccessPoint": {
  "method": "GET",
  "path": "/access-points/{accessPointId}",
  "contract": "access",
  "summary": "Read an access point",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessPoint"
 },
 "getConsentHistory": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents/history",
  "contract": "marketing-crm",
  "summary": "Full consent history",
  "permission": "GUEST_VIEW",
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
 "getFinancialReport": {
  "method": "GET",
  "path": "/reports/financial",
  "contract": "finance",
  "summary": "P&L, balance sheet or cash flow",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "report",
    "in": "query",
    "required": true
   },
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": true
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "costCenterId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FinancialReport"
 },
 "getGuestConsents": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Read a guest's consent state",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConsentState"
 },
 "getGuestLoyalty": {
  "method": "GET",
  "path": "/guests/{subjectId}/loyalty",
  "contract": "marketing-crm",
  "summary": "A guest's loyalty position",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "LoyaltyPosition"
 },
 "getGuestMenu": {
  "method": "GET",
  "path": "/outlets/{outletId}/guest-menu",
  "contract": "fnb",
  "summary": "The menu a guest sees",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "at",
    "in": "query",
    "required": null
   },
   {
    "name": "language",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestMenu"
 },
 "getGuestProfile": {
  "method": "GET",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Read a guest profile",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestProfileDetail"
 },
 "getHaccpStatus": {
  "method": "GET",
  "path": "/food-safety/status",
  "contract": "fnb",
  "summary": "Where this venue stands, right now",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
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
 "getOrgUnit": {
  "method": "GET",
  "path": "/org-units/{orgUnitId}",
  "contract": "tenancy",
  "summary": "Read a scope node",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrgUnit"
 },
 "getOutletStock": {
  "method": "GET",
  "path": "/outlets/{outletId}/stock-check",
  "contract": "retail",
  "summary": "Stock across an outlet",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "lowStockFirst",
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
 "getReport": {
  "method": "GET",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Read a report definition",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReportDefinition"
 },
 "getReturnPolicy": {
  "method": "GET",
  "path": "/outlets/{outletId}/return-policy",
  "contract": "retail",
  "summary": "Read the retail return policy",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReturnPolicy"
 },
 "getTableMap": {
  "method": "GET",
  "path": "/outlets/{outletId}/tables",
  "contract": "fnb",
  "summary": "Table map with live state",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TableMap"
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
 "getWishlist": {
  "method": "GET",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Read a guest's saved items",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [],
  "requestBody": null,
  "responds": "Wishlist"
 },
 "getWorkstation": {
  "method": "GET",
  "path": "/workstations/{workstationId}",
  "contract": "tenancy",
  "summary": "Read a workstation",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "Workstation"
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
 "listAccessPoints": {
  "method": "GET",
  "path": "/access-points",
  "contract": "access",
  "summary": "List access points",
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
 "listFnbOrders": {
  "method": "GET",
  "path": "/fnb-orders",
  "contract": "fnb",
  "summary": "List F&B orders",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "tableVisitId",
    "in": "query",
    "required": null
   },
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
 "listGuestDevices": {
  "method": "GET",
  "path": "/guests/{subjectId}/devices",
  "contract": "marketing-crm",
  "summary": "A guest's registered devices",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
  "responds": "GuestDevice"
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
 "listMerchandise": {
  "method": "GET",
  "path": "/merchandise",
  "contract": "retail",
  "summary": "List merchandise",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "inStockOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
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
 "listOrgUnits": {
  "method": "GET",
  "path": "/org-units",
  "contract": "tenancy",
  "summary": "List scope nodes visible to the session",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "under",
    "in": "query",
    "required": null
   },
   {
    "name": "level",
    "in": "query",
    "required": null
   },
   {
    "name": "includeInactive",
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
 "listOutlets": {
  "method": "GET",
  "path": "/outlets",
  "contract": "tenancy",
  "summary": "List outlets",
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
  "responds": "Outlet"
 },
 "listReportExecutions": {
  "method": "GET",
  "path": "/report-executions",
  "contract": "reporting",
  "summary": "List executions",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "reportId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "mineOnly",
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
 "listReports": {
  "method": "GET",
  "path": "/reports",
  "contract": "reporting",
  "summary": "List available report definitions",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "category",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
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
 "listShifts": {
  "method": "GET",
  "path": "/shifts",
  "contract": "shift",
  "summary": "List shifts",
  "permission": "REPORT_VIEW_WORKSTATION",
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
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "openedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "openedTo",
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
 "listWebhookDeliveries": {
  "method": "GET",
  "path": "/webhook-subscriptions/{subscriptionId}/deliveries",
  "contract": "public-api",
  "summary": "What was sent, what failed, and why",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "WebhookDelivery"
 },
 "listWebhookSubscriptions": {
  "method": "GET",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "What this client is subscribed to",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "WebhookSubscription"
 },
 "listWorkOrders": {
  "method": "GET",
  "path": "/work-orders",
  "contract": "maintenance",
  "summary": "List work orders",
  "permission": "WORK_ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToPrincipalId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "priority",
    "in": "query",
    "required": null
   },
   {
    "name": "assetId",
    "in": "query",
    "required": null
   },
   {
    "name": "overdueOnly",
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
 "mergeGuestProfiles": {
  "method": "POST",
  "path": "/guests/{subjectId}/merge",
  "contract": "marketing-crm",
  "summary": "Merge a duplicate profile into this one",
  "permission": "GUEST_MANAGE",
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
  "responds": "MergeResult"
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
 "recordWaste": {
  "method": "POST",
  "path": "/outlets/{outletId}/waste",
  "contract": "fnb",
  "summary": "Record waste",
  "permission": "ORDER_MODIFY",
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
  "responds": null
 },
 "registerDevice": {
  "method": "POST",
  "path": "/devices",
  "contract": "tenancy",
  "summary": "Register a device",
  "permission": "DEVICE_CONFIGURE",
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
  "requestBody": "RegisteredDevice",
  "responds": "RegisteredDevice"
 },
 "reserveMerchandise": {
  "method": "POST",
  "path": "/outlets/{outletId}/reserve",
  "contract": "retail",
  "summary": "Reserve an item for collection",
  "permission": "ORDER_CREATE",
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
  "responds": "MerchandiseReservation"
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
 "saveNaturalLanguageQuery": {
  "method": "POST",
  "path": "/reports/ask/{conversationId}/save",
  "contract": "reporting",
  "summary": "Save a natural-language answer as a report definition",
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
  "requestBody": null,
  "responds": "ReportDefinition"
 },
 "searchGuests": {
  "method": "GET",
  "path": "/guests",
  "contract": "marketing-crm",
  "summary": "Search guest profiles",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "segmentId",
    "in": "query",
    "required": null
   },
   {
    "name": "hasConsentFor",
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
 "setAccessPointGeofence": {
  "method": "PUT",
  "path": "/access-points/{accessPointId}/geofence",
  "contract": "access",
  "summary": "Set a geofence for handheld validation",
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
  "requestBody": null,
  "responds": "AccessPoint"
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
 "setReturnPolicy": {
  "method": "PUT",
  "path": "/outlets/{outletId}/return-policy",
  "contract": "retail",
  "summary": "Set the retail return policy",
  "permission": "REGION_CONFIGURE",
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
  "requestBody": "ReturnPolicy",
  "responds": "ReturnPolicy"
 },
 "setTableLayout": {
  "method": "PUT",
  "path": "/outlets/{outletId}/tables",
  "contract": "fnb",
  "summary": "Configure the table layout",
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
  "responds": "TableMap"
 },
 "setTurnstileMode": {
  "method": "PUT",
  "path": "/access-points/{accessPointId}/mode",
  "contract": "access",
  "summary": "Set the operating mode of an access point",
  "permission": "TURNSTILE_MODE_SET",
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
  "responds": "AccessPoint"
 },
 "signCorrectiveAction": {
  "method": "POST",
  "path": "/food-safety/corrective-actions/{actionId}/sign",
  "contract": "fnb",
  "summary": "Say what was done, and put a name to it",
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
  "responds": "CorrectiveAction"
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
 "updateAccessPoint": {
  "method": "PATCH",
  "path": "/access-points/{accessPointId}",
  "contract": "access",
  "summary": "Update an access point",
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
  "requestBody": null,
  "responds": "AccessPoint"
 },
 "updateGuestProfile": {
  "method": "PATCH",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Amend a guest profile",
  "permission": "GUEST_MANAGE",
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
  "responds": "GuestProfileDetail"
 },
 "updateOrgUnit": {
  "method": "PATCH",
  "path": "/org-units/{orgUnitId}",
  "contract": "tenancy",
  "summary": "Rename or deactivate a scope node",
  "permission": "SCOPE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "brand",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OrgUnit"
 },
 "updateOutlet": {
  "method": "PATCH",
  "path": "/outlets/{outletId}",
  "contract": "tenancy",
  "summary": "Amend an outlet",
  "permission": "REGION_CONFIGURE",
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
  "responds": "Outlet"
 },
 "updateReport": {
  "method": "PUT",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Publish a new version of a definition",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessPoint": {
  "x-ticvai-persistence": "access.access_point",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "mode",
   "isActive"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "externalCredentialSources": {
    "type": "array",
    "description": "BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "hotelRoomCard",
        "corporateBadge",
        "cityPass",
        "transitCard",
        "partnerToken"
       ]
      },
      "providerName": {
       "type": "string"
      },
      "endpoint": {
       "type": "string"
      },
      "credentialRef": {
       "type": "string"
      },
      "grantsProductId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "scanAnomalyRules": {
    "type": "array",
    "description": "BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n",
    "items": {
     "type": "object",
     "properties": {
      "rule": {
       "type": "string",
       "enum": [
        "simultaneousEntry",
        "impossibleTravelTime",
        "rapidReentry",
        "sharedDevice",
        "velocityBreach"
       ]
      },
      "action": {
       "type": "string",
       "enum": [
        "log",
        "flag",
        "requireSupervisor",
        "deny"
       ]
      },
      "thresholdSeconds": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "operatingMode": {
    "type": "string",
    "enum": [
     "normal",
     "freeFlow",
     "dropArm",
     "closed",
     "podium",
     "maintenance"
    ],
    "default": "normal",
    "description": "BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"
   },
   "vehicleLocationCapture": {
    "type": "boolean",
    "default": false,
    "description": "BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"
   },
   "mode": {
    "$ref": "#/components/schemas/TurnstileMode"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "antiPassbackEnabled": {
    "type": "boolean"
   },
   "isActive": {
    "type": "boolean"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
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
    "format": "uuid"
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
    ]
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
   }
  }
 },
 "Cadence": {
  "x-ticvai-persistence": "none — embedded in schedule",
  "type": "object",
  "required": [
   "frequency"
  ],
  "properties": {
   "frequency": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     "quarterly",
     "onShiftClose",
     "onPeriodClose"
    ]
   },
   "dayOfWeek": {
    "type": "integer",
    "minimum": 0,
    "maximum": 6
   },
   "dayOfMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 31
   },
   "timeOfDay": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "timeZone": {
    "type": "string"
   }
  }
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
 "ConsentDecision": {
  "type": "string",
  "enum": [
   "granted",
   "withdrawn",
   "notAsked"
  ]
 },
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "CorrectiveAction": {
  "type": "object",
  "x-ticvai-persistence": "fnb.corrective_action",
  "description": "What was done about a finding, and who signed it. **Opened automatically by an out-of-range reading or a cold-chain breach**, because an action that depends on somebody remembering to raise it is an action that is not raised.\n**Signed by a named principal, and the signature is the record.** *Discarded and reset* with nobody against it is not a corrective action.\n",
  "required": [
   "id",
   "raisedAt",
   "source",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "source": {
    "type": "string",
    "enum": [
     "temperatureExcursion",
     "coldChainBreach",
     "expiredStock",
     "contamination",
     "pestSighting",
     "equipmentFailure",
     "manual"
    ]
   },
   "sourceRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "severity": {
    "type": "string",
    "enum": [
     "observation",
     "minor",
     "major",
     "critical"
    ]
   },
   "actionTaken": {
    "type": "string",
    "nullable": true
   },
   "disposal": {
    "type": "string",
    "enum": [
     "none",
     "discarded",
     "reworked",
     "quarantined",
     "returned"
    ],
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "actioned",
     "signed",
     "escalated",
     "closed"
    ]
   },
   "signedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "signedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "escalatedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A critical finding a shift cannot close.** Escalation exists so a supervisor signs what a cook should not.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "CreateAccessPointRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "direction"
  ],
  "properties": {
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
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "antiPassbackEnabled": {
    "type": "boolean",
    "default": false
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false
   },
   "driver": {
    "type": "string"
   }
  }
 },
 "CreateReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "category",
   "dataSource",
   "columns",
   "requiredPermission"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "category": {
    "$ref": "#/components/schemas/ReportCategory"
   },
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/ReportColumn"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportFilter"
    }
   },
   "groupBy": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "parameters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportParameter"
    }
   },
   "requiredPermission": {
    "type": "string",
    "description": "Permission needed to run this report. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"
   },
   "maxDateRangeDays": {
    "type": "integer",
    "nullable": true,
    "description": "Guards against a query spanning years of scan events."
   }
  }
 },
 "CreateReportScheduleRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "reportId",
   "cadence",
   "recipients",
   "format"
  ],
  "properties": {
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "cadence": {
    "$ref": "#/components/schemas/Cadence"
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true
   },
   "recipients": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/Recipient"
    }
   },
   "format": {
    "$ref": "#/components/schemas/ExportFormat"
   },
   "includePersonalData": {
    "type": "boolean",
    "default": false
   },
   "skipIfEmpty": {
    "type": "boolean",
    "default": true,
    "description": "An empty report every morning trains people to ignore the report."
   }
  }
 },
 "CreateScopeNodeRequest": {
  "type": "object",
  "required": [
   "level",
   "parentId",
   "code",
   "name"
  ],
  "properties": {
   "level": {
    "$ref": "#/components/schemas/ScopeLevel"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "description": "Required for every level except tenant, which the cell creates at provisioning."
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[a-z0-9_]+$",
    "description": "Becomes the final ltree segment. Immutable once created."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   }
  }
 },
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n",
  "enum": [
   "orders",
   "orderLines",
   "payments",
   "refunds",
   "shifts",
   "scanEvents",
   "entitlements",
   "products",
   "inventory",
   "stockMovements",
   "stockCounts",
   "waste",
   "workstations",
   "devices",
   "principals",
   "loyalty",
   "reviews",
   "queueEntries",
   "guests",
   "campaigns",
   "cases",
   "ledgerEntries",
   "workOrders",
   "approvals",
   "purchaseOrders",
   "receipts",
   "requisitions",
   "stockBatches",
   "resourceBookings",
   "delegations",
   "forms",
   "challenges",
   "wallets",
   "resaleListings"
  ]
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
   "camera"
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
 "ExecutionStatus": {
  "type": "string",
  "enum": [
   "queued",
   "running",
   "completed",
   "failed",
   "cancelled",
   "expired"
  ]
 },
 "ExportFormat": {
  "type": "string",
  "enum": [
   "csv",
   "xlsx",
   "pdf",
   "json"
  ]
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
 "FinancialReport": {
  "x-ticvai-persistence": "none — computed from replica",
  "type": "object",
  "required": [
   "report",
   "fiscalPeriodId",
   "currency",
   "generatedAt",
   "sections"
  ],
  "properties": {
   "report": {
    "type": "string"
   },
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "name",
      "lines",
      "total"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "lines": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "accountCode": {
          "type": "string",
          "nullable": true
         },
         "amount": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         },
         "priorPeriodAmount": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         }
        }
       }
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "GuestDevice": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_device",
  "required": [
   "id",
   "subjectId",
   "platform",
   "status",
   "registeredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android",
     "web"
    ]
   },
   "tokenFingerprint": {
    "type": "string",
    "description": "Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"
   },
   "appVersion": {
    "type": "string",
    "nullable": true
   },
   "osVersion": {
    "type": "string",
    "nullable": true
   },
   "deviceModel": {
    "type": "string",
    "nullable": true
   },
   "locale": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "revoked",
     "failed"
    ]
   },
   "failureCount": {
    "type": "integer",
    "description": "Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"
   },
   "registeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastSeenAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GuestMenu": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over menu, item and availability",
  "required": [
   "outletId",
   "menuId",
   "name",
   "inForceUntil",
   "sections"
  ],
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "menuId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "inForceUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know.\n"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "name": {
       "type": "string"
      },
      "sortOrder": {
       "type": "integer"
      },
      "items": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "menuItemId",
         "name",
         "price",
         "isAvailable",
         "allergens"
        ],
        "properties": {
         "menuItemId": {
          "type": "string",
          "format": "uuid"
         },
         "name": {
          "type": "string"
         },
         "description": {
          "type": "string",
          "nullable": true
         },
         "price": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         },
         "imageAssetRef": {
          "type": "string",
          "nullable": true
         },
         "isAvailable": {
          "type": "boolean",
          "description": "Marked, not removed. A guest who saw a dish yesterday and cannot find it today assumes the app is broken; \"sold out\" is an answer.\n"
         },
         "unavailableReason": {
          "type": "string",
          "nullable": true
         },
         "allergens": {
          "type": "array",
          "description": "Always present. Not a field a tenant may choose to omit.",
          "items": {
           "type": "string"
          }
         },
         "preparationMinutes": {
          "type": "integer",
          "nullable": true
         },
         "modifierGroups": {
          "type": "array",
          "items": {
           "$ref": "#/components/schemas/ModifierGroup"
          }
         }
        }
       }
      }
     }
    }
   }
  }
 },
 "GuestProfile": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "type": "object",
  "required": [
   "subjectId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "nullable": true
   },
   "phone": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "preferredChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells. Marketing acts locally."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "engagementScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"
   },
   "engagementTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "new",
     "active",
     "occasional",
     "lapsing",
     "lapsed",
     "dormant"
    ],
    "description": "5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"
   },
   "lifetimeValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "visitCount": {
    "type": "integer"
   },
   "lastVisitAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "GuestProfileDetail": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "allOf": [
   {
    "$ref": "#/components/schemas/GuestProfile"
   },
   {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
     },
     "consents": {
      "$ref": "#/components/schemas/ConsentState"
     },
     "loyalty": {
      "$ref": "#/components/schemas/LoyaltyPosition"
     },
     "openCaseCount": {
      "type": "integer"
     },
     "recentOrderIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "membershipIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "notes": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
 },
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "MerchandiseReservation": {
  "x-ticvai-persistence": "retail.reservation + retail.reservation_line",
  "type": "object",
  "required": [
   "id",
   "outletId",
   "lines",
   "status",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "reservationNumber": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "merchandiseId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      }
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "reserved",
     "collected",
     "expired",
     "cancelled"
    ]
   },
   "collectionNote": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "collectedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MergeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "survivingSubjectId",
   "absorbedSubjectId",
   "transferred"
  ],
  "properties": {
   "survivingSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "absorbedSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "transferred": {
    "type": "object",
    "properties": {
     "orders": {
      "type": "integer"
     },
     "cases": {
      "type": "integer"
     },
     "loyaltyPoints": {
      "type": "integer"
     }
    }
   },
   "consentOutcome": {
    "type": "array",
    "description": "Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n",
    "items": {
     "type": "object",
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "result": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "wasRestricted": {
       "type": "boolean"
      }
     }
    }
   }
  }
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
 },
 "ModifierGroup": {
  "x-ticvai-persistence": "fnb.modifier_group + fnb.modifier_option",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "minSelections",
   "maxSelections",
   "options"
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
   "minSelections": {
    "type": "integer",
    "minimum": 0,
    "description": "Greater than zero makes the group required."
   },
   "maxSelections": {
    "type": "integer",
    "minimum": 1
   },
   "options": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "id",
      "name",
      "priceDelta"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "priceDelta": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "isDefault": {
       "type": "boolean"
      },
      "isAvailable": {
       "type": "boolean"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "NaturalLanguageAnswer": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "conversationId",
   "question",
   "interpretation",
   "result",
   "confidence"
  ],
  "properties": {
   "conversationId": {
    "type": "string"
   },
   "question": {
    "type": "string"
   },
   "interpretation": {
    "type": "string",
    "description": "What the question was understood to mean, in plain language."
   },
   "generatedQuery": {
    "type": "object",
    "description": "The structured query produced — data source, columns, filters, grouping. Returned so the answer can be checked. An answer nobody can verify is worse than no answer.\n",
    "properties": {
     "dataSource": {
      "$ref": "#/components/schemas/DataSource"
     },
     "columns": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ReportColumn"
      }
     },
     "filters": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ReportFilter"
      }
     },
     "groupBy": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "result": {
    "$ref": "#/components/schemas/ReportResult"
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "suggestedFollowUps": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modelVersion": {
    "type": "string"
   },
   "tokensUsed": {
    "type": "integer"
   }
  }
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
 "OrgUnit": {
  "x-ticvai-persistence": "platform.org_unit",
  "type": "object",
  "required": [
   "id",
   "level",
   "path",
   "code",
   "name",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "level": {
    "$ref": "#/components/schemas/ScopeLevel"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "path": {
    "type": "string",
    "description": "Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "isActive": {
    "type": "boolean",
    "description": "False causes every permission query at or beneath this node to resolve to DENY.\n"
   },
   "childCount": {
    "type": "integer",
    "minimum": 0
   }
  }
 },
 "Outlet": {
  "type": "object",
  "x-ticvai-persistence": "platform.outlet",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "kind"
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
    "$ref": "#/components/schemas/OutletKind"
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "stockLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"
   },
   "costCenterId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Revenue and cost attribution. Outlet is the natural grain for both."
   },
   "openingHours": {
    "type": "array",
    "items": {
     "type": "object"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "OutletKind": {
  "type": "string",
  "enum": [
   "shop",
   "restaurant",
   "bar",
   "cafe",
   "kiosk",
   "gameFloor",
   "ticketOffice",
   "mobile"
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
 "Recipient": {
  "x-ticvai-persistence": "reporting.schedule_recipient",
  "type": "object",
  "required": [
   "kind",
   "address"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "principal",
     "email",
     "sftp",
     "webhook"
    ]
   },
   "address": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "RegisteredDevice": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "required": [
   "id",
   "kind",
   "driver",
   "workstationId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
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
    "format": "uuid"
   },
   "model": {
    "type": "string",
    "nullable": true
   },
   "pushToken": {
    "type": "string",
    "format": "password",
    "nullable": true,
    "description": "BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"
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
    "nullable": true
   },
   "isRequired": {
    "type": "boolean",
    "description": "True blocks shift open when the device is unreachable."
   },
   "status": {
    "type": "string",
    "enum": [
     "online",
     "offline",
     "error",
     "consumableLow",
     "needsAttention",
     "unknown"
    ]
   },
   "batteryPercent": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
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
    "description": "**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ReportCategory": {
  "type": "string",
  "enum": [
   "sales",
   "admission",
   "financial",
   "inventory",
   "guest",
   "operations",
   "marketing",
   "workforce",
   "compliance",
   "custom"
  ]
 },
 "ReportColumn": {
  "x-ticvai-persistence": "reporting.report_column",
  "type": "object",
  "required": [
   "field"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "aggregation": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Aggregation"
     }
    ],
    "default": "none"
   },
   "sortOrder": {
    "type": "integer"
   },
   "sortDirection": {
    "type": "string",
    "enum": [
     "asc",
     "desc"
    ]
   },
   "format": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "ReportDefinition": {
  "x-ticvai-persistence": "reporting.report_definition + reporting.report_column + reporting.report_filter",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "isSystem",
     "isRetired",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "version": {
      "type": "string"
     },
     "isSystem": {
      "type": "boolean",
      "description": "Shipped with the platform. Cannot be amended, only cloned."
     },
     "isRetired": {
      "type": "boolean"
     },
     "estimatedCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Informs whether it may run inline or must be queued."
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "scopePath": {
      "type": "string",
      "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
     }
    }
   }
  ]
 },
 "ReportFilter": {
  "x-ticvai-persistence": "reporting.report_filter",
  "type": "object",
  "required": [
   "field",
   "operator"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "contains",
     "isNull",
     "isNotNull"
    ]
   },
   "value": {},
   "values": {
    "type": "array",
    "items": {}
   },
   "isParameter": {
    "type": "boolean",
    "default": false,
    "description": "Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"
   }
  }
 },
 "ReportParameter": {
  "x-ticvai-persistence": "reporting.report_parameter",
  "type": "object",
  "required": [
   "key",
   "label",
   "type",
   "isRequired"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "type": {
    "$ref": "#/components/schemas/FieldType"
   },
   "isRequired": {
    "type": "boolean"
   },
   "defaultValue": {}
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
 "ReportSchedule": {
  "x-ticvai-persistence": "reporting.schedule",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportScheduleRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "isPaused",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid",
      "description": "The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"
     },
     "isPaused": {
      "type": "boolean"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "lastRunStatus": {
      "$ref": "#/components/schemas/ExecutionStatus"
     },
     "nextRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "consecutiveFailures": {
      "type": "integer"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "ReturnCondition": {
  "type": "string",
  "description": "Determines whether stock is restored or written off.",
  "enum": [
   "resaleable",
   "opened",
   "damaged",
   "faulty",
   "missingParts"
  ]
 },
 "ReturnPolicy": {
  "x-ticvai-persistence": "retail.return_policy",
  "type": "object",
  "required": [
   "outletId",
   "defaultWindowDays",
   "requiresReceipt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "defaultWindowDays": {
    "type": "integer",
    "minimum": 0
   },
   "requiresReceipt": {
    "type": "boolean",
    "default": true
   },
   "allowCashRefundOnCardSale": {
    "type": "boolean",
    "default": false
   },
   "selfAuthoriseLimit": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Up to this, one cashier may accept a return alone."
   },
   "requiresSecondUserAbove": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "requiresApprovalAbove": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "restockableConditions": {
    "type": "array",
    "description": "Conditions that return stock to sale. Everything else is written off.",
    "items": {
     "$ref": "#/components/schemas/ReturnCondition"
    }
   },
   "nonReturnableCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
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
 "ScopeLevel": {
  "type": "string",
  "description": "**The eight organisational levels, and the shared copy of them.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition and this mirrors it so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n",
  "enum": [
   "tenant",
   "brand",
   "region",
   "venue",
   "department",
   "subDepartment",
   "workstation",
   "outlet",
   "subject"
  ]
 },
 "TableMap": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "outletId",
   "tables"
  ],
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "zones": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "tables": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/TableState"
    }
   }
  }
 },
 "TableState": {
  "x-ticvai-persistence": "none — projection over table and visit",
  "allOf": [
   {
    "$ref": "#/components/schemas/TableDefinition"
   },
   {
    "type": "object",
    "required": [
     "status"
    ],
    "properties": {
     "status": {
      "$ref": "#/components/schemas/TableStatus"
     },
     "visitId": {
      "type": "string",
      "nullable": true
     },
     "covers": {
      "type": "integer",
      "nullable": true
     },
     "seatedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "serverPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "billTotal": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    }
   }
  ]
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
 "TurnstileMode": {
  "type": "string",
  "enum": [
   "entry",
   "reentry",
   "crossover",
   "exit",
   "freeRotation",
   "closed"
  ]
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
    "format": "uuid"
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
    "description": "**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingVerification",
     "active",
     "paused",
     "failing",
     "disabled"
    ]
   },
   "consecutiveFailures": {
    "type": "integer",
    "readOnly": true
   },
   "disabledReason": {
    "type": "string",
    "nullable": true,
    "description": "13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"
   }
  }
 },
 "Wishlist": {
  "type": "object",
  "required": [
   "subjectId",
   "items"
  ],
  "x-ticvai-persistence": "none — wrapper. The items are the table, keyed by subject",
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "items": {
    "type": "array",
    "x-ticvai-persistence": "marketing.wishlist_item",
    "items": {
     "type": "object",
     "required": [
      "id",
      "variantId",
      "addedAt",
      "isAvailable"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "productName": {
       "type": "string"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceStartsAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "imageAssetRef": {
       "type": "string",
       "nullable": true
      },
      "isAvailable": {
       "type": "boolean",
       "description": "False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"
      },
      "unavailableReason": {
       "type": "string",
       "nullable": true
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
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
