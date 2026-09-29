# WS06 — Access Control board 6

**10 screens · 18 operations · 32 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, DEVICE_CONFIGURE, DEVICE_VIEW, SCOPE_VIEW, TURNSTILE_MODE_SET`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-194` | Device & Gate Command Center | listDetail | 5 | 1 | — |
| `BO-195` | Device Type & Hardware Library | listDetail | 2 | 1 | — |
| `BO-196` | Physical Device Registration & Provisioning | configEditor | 3 | 2 | — |
| `BO-197` | Turnstile & Lane Behavior Configuration | configEditor | 1 | 0 | — |
| `BO-198` | Validation Outcome & Guest Feedback Designer | configEditor | 1 | 0 | — |
| `BO-199` | Reader, Scanner & Peripheral Configuration | listDetail | 1 | 0 | — |
| `BO-200` | Handheld & Mobile Access Device Configuration | configEditor | 1 | 1 | — |
| `BO-201` | Gate Modes, Free Spin & Emergency Controls | configEditor | 2 | 1 | — |
| `BO-202` | Device Software, Content & Remote Configuration | configEditor | 1 | 0 | — |
| `BO-203` | Hardware Compatibility, Health, Testing & Deployment | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-195, BO-199 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-194",
  "name": "Device & Gate Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.1",
   "page": 70
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/device-gate-command-center-bo-194",
   "component": "apps/venue-management-web/src/routes/access-venue/DeviceGateCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-195",
    "BO-196",
    "BO-197",
    "BO-198",
    "BO-199",
    "BO-200",
    "BO-201",
    "BO-202",
    "BO-203"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "provenance": "derived — BO-100 declares entryState.params  and BO-194 holds none of them, so the edge carries nothing and BO-100 opens cold"
    },
    {
     "to": "BO-195",
     "trigger": "Works in Device Type & Hardware Library",
     "provenance": "flow F116 step 1→2",
     "operation": "listDeviceGate"
    },
    {
     "to": "BO-196",
     "trigger": "Works in Physical Device Registration & Provisioning",
     "provenance": "flow F116 step 3→4",
     "operation": "listDeviceGate"
    },
    {
     "to": "BO-197",
     "trigger": "Works in Turnstile & Lane Behavior Configuration",
     "provenance": "flow F116 step 5→6",
     "operation": "listDeviceGate"
    },
    {
     "to": "BO-198",
     "trigger": "Works in Validation Outcome & Guest Feedback Designer",
     "provenance": "flow F116 step 7→8",
     "operation": "listDeviceGate"
    },
    {
     "to": "BO-199",
     "trigger": "Works in Reader, Scanner & Peripheral Configuration",
     "provenance": "flow F116 step 9→10",
     "operation": "listDeviceGate"
    },
    {
     "to": "BO-200",
     "trigger": "Works in Handheld & Mobile Access Device Configuration",
     "provenance": "flow F116 step 11→12",
     "operation": "listDeviceGate"
    },
    {
     "to": "BO-201",
     "trigger": "Works in Gate Modes, Free Spin & Emergency Controls",
     "provenance": "flow F116 step 13→14",
     "operation": "listDeviceGate"
    },
    {
     "to": "BO-202",
     "trigger": "Works in Device Software, Content & Remote Configuration",
     "provenance": "flow F116 step 15→16",
     "operation": "listDeviceGate"
    },
    {
     "to": "BO-203",
     "trigger": "Works in Hardware Compatibility, Health, Testing & Deployment",
     "provenance": "flow F116 step 17→18",
     "operation": "listDeviceGate"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can identify every access-control device and its current operational/configuration state from one screen.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide the central operational/configuration view of the complete access-control hardware estate.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Devices",
       "bindsTo": "DeviceGateCommandCenterViewSummary.totalDevices",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Online",
       "bindsTo": "DeviceGateCommandCenterViewSummary.online",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Offline",
       "bindsTo": "DeviceGateCommandCenterViewSummary.offline",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Degraded",
       "bindsTo": "DeviceGateCommandCenterViewSummary.degraded",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Turnstiles",
       "bindsTo": "DeviceGateCommandCenterViewSummary.turnstiles",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Handhelds",
       "bindsTo": "DeviceGateCommandCenterViewSummary.handhelds",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Biometric Readers",
       "bindsTo": "DeviceGateCommandCenterViewSummary.biometricReaders",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "RFID/NFC Readers",
       "bindsTo": "DeviceGateCommandCenterViewSummary.rfidNfcReaders",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Gates Open",
       "bindsTo": "DeviceGateCommandCenterViewSummary.gatesOpen",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Gates Closed",
       "bindsTo": "DeviceGateCommandCenterViewSummary.gatesClosed",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Devices Requiring Sync",
       "bindsTo": "DeviceGateCommandCenterViewSummary.devicesRequiringSync",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Firmware/Software Exceptions",
       "bindsTo": "DeviceGateCommandCenterViewSummary.firmwareSoftwareExceptions",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Hardware Alerts",
       "bindsTo": "DeviceGateCommandCenterViewSummary.hardwareAlerts",
       "operation": "listDeviceGate",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Ai",
       "bindsTo": "DeviceGateCommandCenterViewSummary.ai",
       "operation": "listDeviceGate",
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
       "label": "Every device gate",
       "columns": [
        "DeviceGateCommandCenterView.connectivity",
        "DeviceGateCommandCenterView.lastHeartbeat",
        "DeviceGateCommandCenterView.configurationVersion",
        "DeviceGateCommandCenterView.localRuleVersion",
        "DeviceGateCommandCenterView.credentialSecurityPackageVersion",
        "DeviceGateCommandCenterView.scannerHealth",
        "DeviceGateCommandCenterView.controllerHealth"
       ],
       "bindsTo": "DeviceGateCommandCenterView",
       "operation": "listDeviceGate",
       "provenance": "pack Access Control Module_Reference.pdf, page 70 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected device gate",
       "bindsTo": "DeviceGateCommandCenterView",
       "columns": [
        "DeviceGateCommandCenterView.connectivity",
        "DeviceGateCommandCenterView.lastHeartbeat",
        "DeviceGateCommandCenterView.configurationVersion",
        "DeviceGateCommandCenterView.localRuleVersion",
        "DeviceGateCommandCenterView.credentialSecurityPackageVersion",
        "DeviceGateCommandCenterView.scannerHealth",
        "DeviceGateCommandCenterView.controllerHealth"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Device Directory”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 70 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save access device",
       "operation": "updateAccessDevice",
       "permission": "DEVICE_CONFIGURE",
       "notes": "Changes where a registered device sits and what it is: name, hardware model, area, access point, lane, group label, network references, capabilities and `isActive`.",
       "provenance": "contract access.yaml PUT /access-devices/{deviceId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The device gate list.",
   "error": "Could not load. Names which read failed and leaves the device gate untouched.",
   "emptyFirstRun": "No device gate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the device gate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDeviceGate",
    "contract": "access",
    "purpose": "Device & Gate Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "registerDevice",
    "contract": "tenancy",
    "purpose": "Register a gate device from the command centre",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setTurnstileMode",
    "contract": "access",
    "purpose": "Open, close or change the mode of a gate",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listDeviceGate"
    ]
   },
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "The gates and turnstiles whose mode is set",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateAccessDevice",
    "contract": "access",
    "purpose": "Replace a registered device's registration",
    "trigger": "onAction",
    "invalidates": [
     "listDeviceGate",
     "listAccessPoints"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "DeviceGateCommandCenterViewSummary.totalDevices",
    "DeviceGateCommandCenterViewSummary.online",
    "DeviceGateCommandCenterViewSummary.offline",
    "DeviceGateCommandCenterViewSummary.degraded",
    "DeviceGateCommandCenterViewSummary.turnstiles",
    "DeviceGateCommandCenterViewSummary.handhelds"
   ],
   "params": [
    {
     "name": "accessPointId",
     "from": "navigation"
    },
    {
     "name": "deviceId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-194",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-194"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 70. 21 of 21 labels bound to a contract property; 21 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formUpdateAccessDevice",
    "component": "modal",
    "trigger": "Save access device",
    "body": "**Collects what `updateAccessDevice` sends before it is called.** Required: `id`, `venueId`, `hardwareType`, `provisioningStage`, `isActive`, `scopePath`. Optional: `hardwareModelId`, `name`, `serialNumber`, `accessAreaId`, `accessPointId`, `gateLaneId`, `deviceGroupId`, `ipNetworkReference`, `controllerReference`, `installationDate`, `lifecycleStatus`, `capabilities` and 10 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessAccessDevice",
    "confirm": {
     "label": "Save access device",
     "operation": "updateAccessDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "hardwareType",
      "provisioningStage",
      "isActive",
      "scopePath",
      "hardwareModelId",
      "name",
      "serialNumber",
      "accessAreaId",
      "accessPointId",
      "gateLaneId",
      "deviceGroupId",
      "ipNetworkReference",
      "controllerReference",
      "installationDate",
      "lifecycleStatus",
      "capabilities"
     ]
    },
    "provenance": "contract access.yaml PUT /access-devices/{deviceId}"
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
  "id": "BO-195",
  "name": "Device Type & Hardware Library",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.2",
   "page": 72
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/device-type-hardware-library-bo-195",
   "component": "apps/venue-management-web/src/routes/access-venue/DeviceTypeHardwareLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F116 step 2→3",
     "operation": "listDeviceTypeHardware"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "manufacturer-specific logic into admission policies.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create reusable hardware definitions independently from physical deployed devices.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 72"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 72"
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
       "impliedBy": "listDeviceTypeHardware",
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
       "label": "Save hardware model",
       "operation": "setHardwareModel",
       "permission": "DEVICE_CONFIGURE",
       "notes": "**The write behind Device Type & Hardware Library** (BO-195): one hardware model (manufacturer, model, category, type, technologies, connectivity, capability flags, firmware), independent of the devices deployed.",
       "provenance": "contract access.yaml PUT /hardware-models"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The device type hardware list.",
   "error": "Could not load. Names which read failed and leaves the device type hardware untouched.",
   "emptyFirstRun": "No device type hardware yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the device type hardware are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDeviceTypeHardware",
    "contract": "access",
    "purpose": "Device Type & Hardware Library",
    "trigger": "onLoad"
   },
   {
    "operationId": "setHardwareModel",
    "contract": "access",
    "purpose": "Create or replace a hardware model in the library",
    "trigger": "onAction",
    "invalidates": [
     "listDeviceTypeHardware"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "DeviceTypeHardwareLibraryView.hardwareType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-195",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-195"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 72. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetHardwareModel",
    "component": "modal",
    "trigger": "Save hardware model",
    "body": "**Collects what `setHardwareModel` sends before it is called.** Required: `id`, `manufacturer`, `model`, `deviceCategory`, `hardwareType`, `scopePath`. Optional: `supportedTechnologies`, `connectivity`, `offlineCapability`, `screenCapability`, `soundCapability`, `lightCapability`, `relayControllerSupport`, `paymentCapability`, `firmwareSoftwareInformation`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessHardwareModel",
    "confirm": {
     "label": "Save hardware model",
     "operation": "setHardwareModel"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "manufacturer",
      "model",
      "deviceCategory",
      "hardwareType",
      "scopePath",
      "supportedTechnologies",
      "connectivity",
      "offlineCapability",
      "screenCapability",
      "soundCapability",
      "lightCapability",
      "relayControllerSupport",
      "paymentCapability",
      "firmwareSoftwareInformation"
     ]
    },
    "provenance": "contract access.yaml PUT /hardware-models"
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
  "id": "BO-196",
  "name": "Physical Device Registration & Provisioning",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.3",
   "page": 73
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/physical-device-registration-provisioning-bo-196",
   "component": "apps/venue-management-web/src/routes/access-venue/PhysicalDeviceRegistrationProvisioning.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F116 step 4→5",
     "operation": "listPhysicalDeviceRegistration",
     "carries": [
      "accessPointId",
      "deviceId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every physical access-control device is uniquely registered, authenticated and assigned to its correct topology location.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Register actual deployed hardware and connect it to the Board 1 topology.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Device ID",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Serial Number",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hardware Model",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Manufacturer",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Park",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Zone",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Access Point",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gate/Lane",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "IP/network reference",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      },
      {
       "kind": "selectField",
       "label": "controller reference",
       "provenance": "pack Access Control Module_Reference.pdf, page 73 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Register access device",
       "operation": "registerAccessDevice",
       "permission": "DEVICE_CONFIGURE",
       "notes": "**The write behind Physical Device Registration & Provisioning** (BO-196): registers one deployed device (a turnstile, reader, handheld, podium unit or beacon) against a hardware model and places it in the topology.",
       "provenance": "contract access.yaml POST /access-devices"
      },
      {
       "kind": "secondaryButton",
       "label": "Save access device",
       "operation": "updateAccessDevice",
       "permission": "DEVICE_CONFIGURE",
       "notes": "Changes where a registered device sits and what it is: name, hardware model, area, access point, lane, group label, network references, capabilities and `isActive`.",
       "provenance": "contract access.yaml PUT /access-devices/{deviceId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The physical device registration configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the physical device registration untouched.",
   "emptyFirstRun": "No physical device registration configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPhysicalDeviceRegistration",
    "contract": "access",
    "purpose": "Physical Device Registration & Provisioning",
    "trigger": "onLoad"
   },
   {
    "operationId": "registerAccessDevice",
    "contract": "access",
    "purpose": "Register a physical access-control device",
    "trigger": "onAction",
    "invalidates": [
     "listPhysicalDeviceRegistration"
    ]
   },
   {
    "operationId": "updateAccessDevice",
    "contract": "access",
    "purpose": "Replace a registered device's registration",
    "trigger": "onAction",
    "invalidates": [
     "listPhysicalDeviceRegistration"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-196",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-196"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 73. 0 of 0 labels bound to a contract property; 12 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formRegisterAccessDevice",
    "component": "modal",
    "trigger": "Register access device",
    "body": "**Collects what `registerAccessDevice` sends before it is called.** Required: `id`, `venueId`, `hardwareType`, `provisioningStage`, `isActive`, `scopePath`. Optional: `hardwareModelId`, `name`, `serialNumber`, `accessAreaId`, `accessPointId`, `gateLaneId`, `deviceGroupId`, `ipNetworkReference`, `controllerReference`, `installationDate`, `lifecycleStatus`, `capabilities` and 10 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessAccessDevice",
    "confirm": {
     "label": "Register access device",
     "operation": "registerAccessDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "hardwareType",
      "provisioningStage",
      "isActive",
      "scopePath",
      "hardwareModelId",
      "name",
      "serialNumber",
      "accessAreaId",
      "accessPointId",
      "gateLaneId",
      "deviceGroupId",
      "ipNetworkReference",
      "controllerReference",
      "installationDate",
      "lifecycleStatus",
      "capabilities"
     ]
    },
    "provenance": "contract access.yaml POST /access-devices"
   },
   {
    "id": "formUpdateAccessDevice",
    "component": "modal",
    "trigger": "Save access device",
    "body": "**Collects what `updateAccessDevice` sends before it is called.** Required: `id`, `venueId`, `hardwareType`, `provisioningStage`, `isActive`, `scopePath`. Optional: `hardwareModelId`, `name`, `serialNumber`, `accessAreaId`, `accessPointId`, `gateLaneId`, `deviceGroupId`, `ipNetworkReference`, `controllerReference`, `installationDate`, `lifecycleStatus`, `capabilities` and 10 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessAccessDevice",
    "confirm": {
     "label": "Save access device",
     "operation": "updateAccessDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "hardwareType",
      "provisioningStage",
      "isActive",
      "scopePath",
      "hardwareModelId",
      "name",
      "serialNumber",
      "accessAreaId",
      "accessPointId",
      "gateLaneId",
      "deviceGroupId",
      "ipNetworkReference",
      "controllerReference",
      "installationDate",
      "lifecycleStatus",
      "capabilities"
     ]
    },
    "provenance": "contract access.yaml PUT /access-devices/{deviceId}"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "deviceId",
     "from": "session"
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
  "id": "BO-197",
  "name": "Turnstile & Lane Behavior Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.4",
   "page": 74
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/turnstile-lane-behavior-configuration-bo-197",
   "component": "apps/venue-management-web/src/routes/access-venue/TurnstileLaneBehaviorConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F116 step 6→7",
     "operation": "setTurnstileLaneBehavior",
     "carries": [
      "accessPointId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Each gate can execute different configured behaviors according to its mode and the validated credential.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how each turnstile or lane behaves. The matrix specifically requires software on turnstiles to behave differently according to card/ticket type and supports different operating modes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Entry",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Exit",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Entry/Exit",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Re-entry",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Crossover",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fast Pass",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Attraction",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Group",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Count Only",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Free Spin",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Closed",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Unlock duration",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "pass-through timeout",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
      },
      {
       "kind": "selectField",
       "label": "relock behavior",
       "provenance": "pack Access Control Module_Reference.pdf, page 74 §Configure"
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
       "provenance": "contract operation setTurnstileLaneBehavior"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The turnstile lane behavior configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the turnstile lane behavior untouched.",
   "emptyFirstRun": "No turnstile lane behavior configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setTurnstileLaneBehavior",
    "contract": "access",
    "purpose": "Turnstile & Lane Behavior Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-197",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-197"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 74. 0 of 0 labels bound to a contract property; 14 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-198",
  "name": "Validation Outcome & Guest Feedback Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.5",
   "page": 76
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/validation-outcome-guest-feedback-designer-bo-198",
   "component": "apps/venue-management-web/src/routes/access-venue/ValidationOutcomeGuestFeedbackDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F116 step 8→9",
     "operation": "setValidationOutcomeGuest"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every access decision produces a configurable and understandable physical response for the guest and operator.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure what the physical access device does and displays after validation. The matrix explicitly requires valid/non-valid messages, lights, pictograms and sounds, including green/yellow/red behavior.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Green light",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gate open",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Success tone",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "✓ pictogram",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Custom message",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Yellow light",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Alert sound",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gate remains controlled",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Red light",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Denial sound",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gate remains locked",
       "provenance": "pack Access Control Module_Reference.pdf, page 76 §Configure"
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
       "provenance": "contract operation setValidationOutcomeGuest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validation outcome guest configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the validation outcome guest untouched.",
   "emptyFirstRun": "No validation outcome guest configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setValidationOutcomeGuest",
    "contract": "access",
    "purpose": "Validation Outcome & Guest Feedback Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-198",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-198"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 76. 0 of 0 labels bound to a contract property; 11 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-199",
  "name": "Reader, Scanner & Peripheral Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.6",
   "page": 77
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/reader-scanner-peripheral-configuration-bo-199",
   "component": "apps/venue-management-web/src/routes/access-venue/ReaderScannerPeripheralConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F116 step 10→11",
     "operation": "setReaderScannerPeripheral",
     "carries": [
      "accessPointId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Readers and peripherals can be independently associated with gates and checked against required admission capabilities.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the technologies attached to a gate/device.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 77"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 77"
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
       "provenance": "contract operation setReaderScannerPeripheral"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "scanTarget",
       "derived": true,
       "impliedBy": "setReaderScannerPeripheral",
       "notes": "**A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or explain something."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setReaderScannerPeripheral"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reader scanner peripheral list.",
   "error": "Could not load. Names which read failed and leaves the reader scanner peripheral untouched.",
   "emptyFirstRun": "No reader scanner peripheral yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader scanner peripheral are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setReaderScannerPeripheral",
    "contract": "access",
    "purpose": "Reader, Scanner & Peripheral Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-199",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-199"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-200",
  "name": "Handheld & Mobile Access Device Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.7",
   "page": 78
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/handheld-mobile-access-device-configuration-bo-200",
   "component": "apps/venue-management-web/src/routes/access-venue/HandheldMobileAccessDeviceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F116 step 12→13",
     "operation": "setHandheldMobileAccess"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Mobile access devices can be centrally configured, restricted and revoked according to their operational role.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure mobile access-control devices used by staff. The matrix explicitly requires handheld devices and Android/iOS dedicated mobile applications.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Device type",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Android/iOS",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Configure"
      },
      {
       "kind": "selectField",
       "label": "assigned venue",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Configure"
      },
      {
       "kind": "selectField",
       "label": "assigned zone",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Configure"
      },
      {
       "kind": "selectField",
       "label": "assigned operator group",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Configure"
      },
      {
       "kind": "selectField",
       "label": "permitted operating modes",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Configure"
      },
      {
       "kind": "selectField",
       "label": "offline capability",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Configure"
      },
      {
       "kind": "selectField",
       "label": "scanner source",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Scan Ticket",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Search Ticket",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Entry",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Manual Attendance",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Enable/disable"
      },
      {
       "kind": "destructiveButton",
       "label": "Override",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "View History",
       "provenance": "pack Access Control Module_Reference.pdf, page 78 §Enable/disable"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmOverride",
    "component": "confirmDialog",
    "trigger": "Override",
    "body": "**Override on a handheld mobile access is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Access Control Module_Reference.pdf, page 78 §Enable/disable"
   }
  ],
  "states": {
   "loading": "The handheld mobile access configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the handheld mobile access untouched.",
   "emptyFirstRun": "No handheld mobile access configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setHandheldMobileAccess",
    "contract": "access",
    "purpose": "Handheld & Mobile Access Device Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-200",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-200"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 78. 0 of 0 labels bound to a contract property; 14 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Scan Ticket, Search Ticket, Entry, Manual Attendance, Override, View History are choices sent by `setHandheldMobileAccess`.",
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
  "id": "BO-201",
  "name": "Gate Modes, Free Spin & Emergency Controls",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.8",
   "page": 79
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/gate-modes-free-spin-emergency-controls-bo-201",
   "component": "apps/venue-management-web/src/routes/access-venue/GateModesFreeSpinEmergencyControls.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F116 step 14→15",
     "operation": "listGateModeFree"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized operations personnel can rapidly change gate modes across individual devices or device groups while maintaining full auditability.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage non-standard operational modes. The source specifically requires Free Spin and Drop Arm/Emergency behavior.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Who can activate",
       "provenance": "pack Access Control Module_Reference.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue scope",
       "provenance": "pack Access Control Module_Reference.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gate group",
       "provenance": "pack Access Control Module_Reference.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "reason",
       "provenance": "pack Access Control Module_Reference.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "emergency code",
       "provenance": "pack Access Control Module_Reference.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "automatic notification",
       "provenance": "pack Access Control Module_Reference.pdf, page 79 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save gate mode policy",
       "operation": "setGateModePolicy",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind Gate Modes, Free Spin & Emergency Controls** (BO-201): for `freeFlow` or `dropArm` (R221 vocabulary), who may activate it, on which gate group, whether a reason is required, the emergency code, notification and whether activation opens an incident.",
       "provenance": "contract access.yaml PUT /gate-mode-policies"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gate modes free configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the gate modes free untouched.",
   "emptyFirstRun": "No gate modes free configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGateModeFree",
    "contract": "access",
    "purpose": "Gate Modes, Free Spin & Emergency Controls",
    "trigger": "onLoad"
   },
   {
    "operationId": "setGateModePolicy",
    "contract": "access",
    "purpose": "Set a policy for a non-standard gate mode",
    "trigger": "onAction",
    "invalidates": [
     "listGateModeFree"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-201",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-201"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 79. 0 of 0 labels bound to a contract property; 6 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetGateModePolicy",
    "component": "modal",
    "trigger": "Save gate mode policy",
    "body": "**Collects what `setGateModePolicy` sends before it is called.** Required: `id`, `venueId`, `mode`, `scopePath`. Optional: `whoCanActivate`, `accessPointGroupId`, `reasonRequired`, `emergencyCode`, `automaticNotification`, `createsIncident`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessGateModePolicy",
    "confirm": {
     "label": "Save gate mode policy",
     "operation": "setGateModePolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "mode",
      "scopePath",
      "whoCanActivate",
      "accessPointGroupId",
      "reasonRequired",
      "emergencyCode",
      "automaticNotification",
      "createsIncident"
     ]
    },
    "provenance": "contract access.yaml PUT /gate-mode-policies"
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
  "id": "BO-202",
  "name": "Device Software, Content & Remote Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.9",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/device-software-content-remote-configuration-bo-202",
   "component": "apps/venue-management-web/src/routes/access-venue/DeviceSoftwareContentRemoteConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F116 step 16→17",
     "operation": "setDeviceSoftwareContent"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Device configuration and supported content can be centrally deployed without manually configuring each turnstile.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Centrally control access-control device software and guest-facing configuration. The source requires the ability to configure/manage software on turnstiles, add external webpages on supported screens, and enable payment technologies where available.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Welcome page",
       "provenance": "pack Access Control Module_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Instructions",
       "provenance": "pack Access Control Module_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Ticket status",
       "provenance": "pack Access Control Module_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reason message",
       "provenance": "pack Access Control Module_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Promotional information",
       "provenance": "pack Access Control Module_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "External approved webpage",
       "provenance": "pack Access Control Module_Reference.pdf, page 81 §Configure"
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
       "provenance": "contract operation setDeviceSoftwareContent"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The device software content configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the device software content untouched.",
   "emptyFirstRun": "No device software content configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDeviceSoftwareContent",
    "contract": "access",
    "purpose": "Device Software, Content & Remote Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-202",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-202"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 81. 0 of 0 labels bound to a contract property; 6 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-203",
  "name": "Hardware Compatibility, Health, Testing & Deployment",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "6",
   "number": "6.10",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hardware-compatibility-health-testing-deployment-bo-203",
   "component": "apps/venue-management-web/src/routes/access-venue/HardwareCompatibilityHealthTestingDeployment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-194"
   ],
   "exitTo": [
    "BO-194"
   ],
   "inferred": false,
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-194",
     "trigger": "Device & Gate Command Center",
     "carries": [
      "deviceId"
     ],
     "provenance": "derived — BO-194 declares entryState.params accessPointId, deviceId and BO-203 holds deviceId, so an edge into it carries them"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "No access device enters production until its required capabilities, connectivity, security configuration and physical responses have been successfully validated. Board 6 — Final 10-Screen Structure # Backend Screen Main Responsibility 6.1 Device & Gate Command Center Hardware estate and live health 6.2 Device Type & Hardware Library Reusable hardware/model definitions 6.3 Physical Device Registration & Provisioning Register and authenticate deployed devices 6.4 Turnstile & Lane Behavior Configuration Gate modes, direction and physical behavior # Backend Screen Main Responsibility",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the final testing and governance layer before hardware is used in production. The matrix says venues may select their hardware, while the provider must expose hardware limitations and recommendations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 82"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 82"
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
       "label": "Selected gates",
       "provenance": "pack Access Control Module_Reference.pdf, page 82 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "device group",
       "provenance": "pack Access Control Module_Reference.pdf, page 82 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "venue",
       "provenance": "pack Access Control Module_Reference.pdf, page 82 §Support"
      },
      {
       "kind": "publishGate",
       "label": "Deploy configuration version",
       "operation": "publishHardwareDeployment",
       "notes": "**Names the version, the target (pilot, selected gates, device group or venue) and the devices that failed the compatibility test and will be skipped**, before it runs. Devices pick the version up at their next package refresh.",
       "provenance": "contract access.yaml POST /hardware-deployments (decided 29 September, VM close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The hardware compatibility health list.",
   "error": "Could not load. Names which read failed and leaves the hardware compatibility health untouched.",
   "emptyFirstRun": "No hardware compatibility health yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hardware compatibility health are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listHardwareCompatibilityHealth",
    "contract": "access",
    "purpose": "Hardware Compatibility, Health, Testing & Deployment",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishHardwareDeployment",
    "contract": "access",
    "purpose": "Deploy configuration version",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "HardwareCompatibilityHealthTestingDeploymentView.capabilities",
    "HardwareCompatibilityHealthTestingDeploymentView.rolloutScope"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-203",
   "workshopBoard": "wireframes/WS23 Access Control Board 6.dc.html#bo-203"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 82. 0 of 0 labels bound to a contract property; 3 of 76 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `publishHardwareDeployment`.",
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
 "listDeviceGate": {
  "method": "GET",
  "path": "/device-gate",
  "contract": "access",
  "summary": "Device & Gate Command Center",
  "permission": "DEVICE_VIEW",
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
 "listDeviceTypeHardware": {
  "method": "GET",
  "path": "/device-type-hardware",
  "contract": "access",
  "summary": "Device Type & Hardware Library",
  "permission": "DEVICE_VIEW",
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
  "responds": "DeviceTypeHardwareLibraryView"
 },
 "listGateModeFree": {
  "method": "GET",
  "path": "/gate-mode-free",
  "contract": "access",
  "summary": "Gate Modes, Free Spin & Emergency Controls",
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
  "responds": "GateModesFreeSpinEmergencyControlsView"
 },
 "listHardwareCompatibilityHealth": {
  "method": "GET",
  "path": "/hardware-compatibility-health",
  "contract": "access",
  "summary": "Hardware Compatibility, Health, Testing & Deployment",
  "permission": "DEVICE_VIEW",
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
 "listPhysicalDeviceRegistration": {
  "method": "GET",
  "path": "/physical-device-registration",
  "contract": "access",
  "summary": "Physical Device Registration & Provisioning",
  "permission": "DEVICE_VIEW",
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
 "registerAccessDevice": {
  "method": "POST",
  "path": "/access-devices",
  "contract": "access",
  "summary": "Register a physical access-control device",
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
  "requestBody": "AccessAccessDevice",
  "responds": "AccessAccessDevice"
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
 "setDeviceSoftwareContent": {
  "method": "PUT",
  "path": "/device-software-content",
  "contract": "access",
  "summary": "Device Software, Content & Remote Configuration",
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
  "requestBody": "DeviceSoftwareContentRemoteConfigurationInput",
  "responds": "DeviceSoftwareContentRemoteConfigurationView"
 },
 "setGateModePolicy": {
  "method": "PUT",
  "path": "/gate-mode-policies",
  "contract": "access",
  "summary": "Set a policy for a non-standard gate mode",
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
  "requestBody": "AccessGateModePolicy",
  "responds": "AccessGateModePolicy"
 },
 "setHandheldMobileAccess": {
  "method": "PUT",
  "path": "/handheld-mobile-access",
  "contract": "access",
  "summary": "Handheld & Mobile Access Device Configuration",
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
  "requestBody": "HandheldMobileAccessDeviceConfigurationInput",
  "responds": "HandheldMobileAccessDeviceConfigurationView"
 },
 "setHardwareModel": {
  "method": "PUT",
  "path": "/hardware-models",
  "contract": "access",
  "summary": "Create or replace a hardware model in the library",
  "permission": "DEVICE_CONFIGURE",
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
  "requestBody": "AccessHardwareModel",
  "responds": "AccessHardwareModel"
 },
 "setReaderScannerPeripheral": {
  "method": "PUT",
  "path": "/reader-scanner-peripheral",
  "contract": "access",
  "summary": "Reader, Scanner & Peripheral Configuration",
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
  "requestBody": "ReaderScannerPeripheralConfigurationInput",
  "responds": "ReaderScannerPeripheralConfigurationView"
 },
 "setTurnstileLaneBehavior": {
  "method": "PUT",
  "path": "/turnstile-lane-behavior",
  "contract": "access",
  "summary": "Turnstile & Lane Behavior Configuration",
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
  "requestBody": "TurnstileLaneBehaviorConfigurationInput",
  "responds": "TurnstileLaneBehaviorConfigurationView"
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
 "setValidationOutcomeGuest": {
  "method": "PUT",
  "path": "/validation-outcome-guest",
  "contract": "access",
  "summary": "Validation Outcome & Guest Feedback Designer",
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
  "requestBody": "ValidationOutcomeGuestFeedbackDesignerInput",
  "responds": "ValidationOutcomeGuestFeedbackDesignerView"
 },
 "updateAccessDevice": {
  "method": "PUT",
  "path": "/access-devices/{deviceId}",
  "contract": "access",
  "summary": "Replace a registered device's registration",
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
  "requestBody": "AccessAccessDevice",
  "responds": "AccessAccessDevice"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessAccessDevice": {
  "type": "object",
  "x-ticvai-persistence": "access.access_device",
  "description": "One physical access-control device registered in a venue: a turnstile, reader, handheld, podium unit or BLE beacon, with its model, location, network references, reported versions and health, and provisioning stage. Merges access.gate_device and access.ble_beacon (a beacon is a device with a proximity threshold) (declared 29 September, data-model close-out DM1) Registered with registerAccessDevice and changed with updateAccessDevice; provisioning stage, versions and health are reported by the device; deviceGroupId is a free deployment label, not a key (decided 29 September, writers pass). **tenancy platform.device is the register of record** (29 September, build): this is the topology placement, and lifecycleStatus follows the register through the device.enrolmentChanged event.",
  "required": [
   "id",
   "venueId",
   "hardwareType",
   "provisioningStage",
   "isActive",
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
   "hardwareModelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Model from the hardware library (access.hardware_model)"
   },
   "hardwareType": {
    "type": "string",
    "enum": [
     "standardTurnstile",
     "fullHeightTurnstile",
     "tripodTurnstile",
     "speedGate",
     "wideLane",
     "accessiblePodGate",
     "buggyGate",
     "vipGate",
     "staffGate",
     "androidHandheld",
     "iosDevice",
     "tablet",
     "qrBarcodeReader",
     "rfidReader",
     "nfcReader",
     "multiTechnologyReader",
     "biometricReader",
     "podium",
     "counter",
     "beacon",
     "cameraController",
     "externalAccessDevice"
    ],
    "description": "Specific hardware type, as in the hardware library"
   },
   "name": {
    "type": "string",
    "nullable": true,
    "description": "Device or beacon name, e.g. Gate A, HH-01"
   },
   "serialNumber": {
    "type": "string",
    "nullable": true
   },
   "accessAreaId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Most specific park, zone or attraction the device sits in (access.access_area)"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Access point (gate) the device serves"
   },
   "gateLaneId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Lane the device is mounted on (access.gate_lane)"
   },
   "deviceGroupId": {
    "type": "string",
    "nullable": true,
    "description": "Device group the device belongs to, as targeted by hardware deployments and device configurations"
   },
   "ipNetworkReference": {
    "type": "string",
    "nullable": true
   },
   "controllerReference": {
    "type": "string",
    "nullable": true
   },
   "installationDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "provisioningStage": {
    "type": "string",
    "enum": [
     "registered",
     "hardwareProfileAssigned",
     "locationAssigned",
     "authenticated",
     "configurationDownloaded",
     "securityPackageDownloaded",
     "connectivityTested",
     "active"
    ],
    "default": "registered"
   },
   "lifecycleStatus": {
    "type": "string",
    "enum": [
     "registered",
     "configured",
     "tested",
     "approved",
     "production"
    ],
    "default": "registered",
    "description": "Certification stage; no device enters production until validated"
   },
   "capabilities": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicQr",
      "rfid",
      "nfc",
      "facePass",
      "offline",
      "heightCheck"
     ]
    },
    "description": "Capabilities this device supports, from the compatibility matrix"
   },
   "proximityThresholdMeters": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Beacons only: activation distance in metres"
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "Active/inactive as configured (beacons: activeInactive)"
   },
   "status": {
    "type": "string",
    "enum": [
     "healthy",
     "active",
     "degraded",
     "offline",
     "localMode"
    ],
    "nullable": true,
    "description": "Health as reported by the device or vendor; TICVAI does not detect it"
   },
   "connectivity": {
    "type": "string",
    "nullable": true,
    "description": "Reported connectivity"
   },
   "scannerHealth": {
    "type": "string",
    "nullable": true
   },
   "controllerHealth": {
    "type": "string",
    "nullable": true
   },
   "cameraHealth": {
    "type": "string",
    "nullable": true,
    "description": "Where the device has a camera"
   },
   "configurationVersion": {
    "type": "string",
    "nullable": true,
    "description": "Configuration version the device reports running"
   },
   "localRuleVersion": {
    "type": "string",
    "nullable": true
   },
   "credentialSecurityPackageVersion": {
    "type": "string",
    "nullable": true
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Last heartbeat or, for a beacon, last detected"
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
 "AccessGateModePolicy": {
  "type": "object",
  "x-ticvai-persistence": "access.gate_mode_policy",
  "description": "One policy for a non-standard gate mode (free spin or count only as freeFlow, emergency as dropArm): who may activate it, on which gate group, whether a reason is required, emergency code, notification and incident creation (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "venueId",
   "mode",
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
   "mode": {
    "type": "string",
    "enum": [
     "freeFlow",
     "dropArm"
    ],
    "description": "Non-standard operating mode governed (R221 vocabulary)"
   },
   "whoCanActivate": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Roles allowed to activate this mode"
   },
   "accessPointGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Gate group the policy applies to (access.access_point_group); null for the whole venue"
   },
   "reasonRequired": {
    "type": "boolean",
    "default": true
   },
   "emergencyCode": {
    "type": "string",
    "nullable": true
   },
   "automaticNotification": {
    "type": "boolean",
    "default": false
   },
   "createsIncident": {
    "type": "boolean",
    "default": false,
    "description": "Activation creates an incident record"
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
 "AccessHardwareModel": {
  "type": "object",
  "x-ticvai-persistence": "access.hardware_model",
  "description": "One hardware model in the reusable library, independent of deployed devices: manufacturer, model, category and type, supported technologies, connectivity, capability flags and firmware information (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "manufacturer",
   "model",
   "deviceCategory",
   "hardwareType",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "manufacturer": {
    "type": "string"
   },
   "model": {
    "type": "string"
   },
   "deviceCategory": {
    "type": "string",
    "enum": [
     "turnstile",
     "specialGate",
     "mobile",
     "reader",
     "other"
    ]
   },
   "hardwareType": {
    "type": "string",
    "enum": [
     "standardTurnstile",
     "fullHeightTurnstile",
     "tripodTurnstile",
     "speedGate",
     "wideLane",
     "accessiblePodGate",
     "buggyGate",
     "vipGate",
     "staffGate",
     "androidHandheld",
     "iosDevice",
     "tablet",
     "qrBarcodeReader",
     "rfidReader",
     "nfcReader",
     "multiTechnologyReader",
     "biometricReader",
     "podium",
     "counter",
     "beacon",
     "cameraController",
     "externalAccessDevice"
    ]
   },
   "supportedTechnologies": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "connectivity": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "offlineCapability": {
    "type": "boolean",
    "default": false
   },
   "screenCapability": {
    "type": "boolean",
    "default": false
   },
   "soundCapability": {
    "type": "boolean",
    "default": false
   },
   "lightCapability": {
    "type": "boolean",
    "default": false
   },
   "relayControllerSupport": {
    "type": "boolean",
    "default": false
   },
   "paymentCapability": {
    "type": "boolean",
    "default": false,
    "description": "Payment capability where available"
   },
   "firmwareSoftwareInformation": {
    "type": "string",
    "nullable": true
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
 "AccessPoint": {
  "x-ticvai-persistence": "access.access_point",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "operatingMode",
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
    "allOf": [
     {
      "$ref": "#/components/schemas/ExternalCredentialSourceList"
     }
    ],
    "description": "BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"
   },
   "scanAnomalyRules": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ScanAnomalyRuleList"
     }
    ],
    "description": "BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"
   },
   "operatingMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "default": "normal",
    "description": "**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"
   },
   "vehicleLocationCapture": {
    "type": "boolean",
    "default": false,
    "description": "BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"
   },
   "mode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TurnstileMode"
     }
    ],
    "nullable": true,
    "description": "Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"
   },
   "direction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Direction"
     }
    ],
    "description": "**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"
   },
   "antiPassbackEnabled": {
    "type": "boolean"
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false,
    "description": "Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."
   },
   "driver": {
    "type": "string",
    "nullable": true,
    "description": "Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"
   },
   "geofence": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointGeofence"
     }
    ],
    "nullable": true,
    "description": "Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"
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
 "AccessPointGeofence": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n",
  "required": [
   "enforcement"
  ],
  "properties": {
   "latitude": {
    "type": "number"
   },
   "longitude": {
    "type": "number"
   },
   "radiusMetres": {
    "type": "integer",
    "minimum": 5,
    "maximum": 5000
   },
   "enforcement": {
    "type": "string",
    "enum": [
     "off",
     "warn",
     "deny"
    ],
    "description": "`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"
   },
   "allowProximityBeacon": {
    "type": "boolean",
    "description": "Accept a BLE proximity assertion in place of GPS. Better indoors."
   }
  }
 },
 "AccessPointOperatingMode": {
  "type": "string",
  "description": "BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n",
  "enum": [
   "normal",
   "freeFlow",
   "dropArm",
   "closed",
   "podium",
   "maintenance"
  ]
 },
 "DeviceCapability": {
  "type": "string",
  "description": "BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n",
  "enum": [
   "genderClassification"
  ]
 },
 "DeviceGateCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Device & Gate Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "connectivity": {
    "type": "string",
    "description": "connectivity"
   },
   "lastHeartbeat": {
    "type": "string",
    "format": "date-time",
    "description": "last heartbeat"
   },
   "configurationVersion": {
    "type": "string",
    "description": "configuration version"
   },
   "localRuleVersion": {
    "type": "string",
    "description": "local rule version"
   },
   "credentialSecurityPackageVersion": {
    "type": "string",
    "description": "credential/security package version"
   },
   "scannerHealth": {
    "type": "string",
    "description": "scanner health"
   },
   "controllerHealth": {
    "type": "string",
    "description": "controller health"
   },
   "cameraHealthWhereApplicable": {
    "type": "string",
    "description": "camera health where applicable"
   },
   "deviceId": {
    "type": "string"
   },
   "deviceType": {
    "type": "string",
    "description": "e.g. Turnstile, VIP Gate, Handheld, Reader"
   },
   "accessPointId": {
    "type": "string"
   },
   "mode": {
    "type": "string",
    "description": "Current operating mode"
   },
   "status": {
    "type": "string",
    "enum": [
     "healthy",
     "active",
     "degraded",
     "offline",
     "localMode"
    ]
   }
  }
 },
 "DeviceGateCommandCenterViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "totalDevices": {
    "type": "integer",
    "description": "Total Devices"
   },
   "online": {
    "type": "integer",
    "description": "Online"
   },
   "offline": {
    "type": "integer",
    "description": "Offline"
   },
   "degraded": {
    "type": "integer",
    "description": "Degraded"
   },
   "turnstiles": {
    "type": "integer",
    "description": "Turnstiles"
   },
   "handhelds": {
    "type": "integer",
    "description": "Handhelds"
   },
   "biometricReaders": {
    "type": "integer",
    "description": "Biometric Readers"
   },
   "rfidNfcReaders": {
    "type": "integer",
    "description": "RFID/NFC Readers"
   },
   "gatesOpen": {
    "type": "integer",
    "description": "Gates Open"
   },
   "gatesClosed": {
    "type": "integer",
    "description": "Gates Closed"
   },
   "devicesRequiringSync": {
    "type": "integer",
    "description": "Devices Requiring Sync"
   },
   "firmwareSoftwareExceptions": {
    "type": "integer",
    "description": "Firmware/Software Exceptions"
   },
   "hardwareAlerts": {
    "type": "integer",
    "description": "Hardware Alerts"
   },
   "ai": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI findings, e.g. a gate with a high scan-failure rate. Read-only."
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
   "camera",
   "mobileHandset"
  ],
  "description": "`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n"
 },
 "DeviceSoftwareContentRemoteConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Device Software, Content & Remote Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "deviceGroupId": {
    "type": "string",
    "description": "Target device group"
   },
   "venueId": {
    "type": "string"
   },
   "configurationId": {
    "type": "string"
   },
   "deviceSettings": {
    "type": "string",
    "description": "Device settings"
   },
   "gateMode": {
    "type": "string",
    "description": "Gate mode"
   },
   "readerSettings": {
    "type": "string",
    "description": "Reader settings"
   },
   "mediaProfiles": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media profiles"
   },
   "outcomeProfiles": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Outcome profiles"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "uiContent": {
    "type": "string",
    "description": "UI content"
   },
   "localRules": {
    "type": "string",
    "description": "Local rules"
   },
   "offlineSecurityConfiguration": {
    "type": "string",
    "description": "Offline security package reference"
   },
   "welcomePage": {
    "type": "string",
    "description": "Welcome page"
   },
   "instructions": {
    "type": "string",
    "description": "Instructions"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket status"
   },
   "reasonMessage": {
    "type": "string",
    "description": "Reason message"
   },
   "promotionalInformation": {
    "type": "string",
    "description": "Promotional information"
   },
   "externalApprovedWebpage": {
    "type": "string",
    "description": "External approved webpage"
   },
   "emergencyInformation": {
    "type": "string",
    "description": "Emergency information"
   },
   "version": {
    "type": "string",
    "description": "Configuration version, for rollback"
   },
   "deploymentStage": {
    "type": "string",
    "enum": [
     "draft",
     "testDevice",
     "deviceGroup",
     "venueRollout"
    ]
   }
  },
  "required": [
   "configurationId",
   "venueId",
   "deviceGroupId"
  ]
 },
 "DeviceSoftwareContentRemoteConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Device Software, Content & Remote Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "deviceGroupId": {
    "type": "string",
    "description": "Target device group"
   },
   "venueId": {
    "type": "string"
   },
   "configurationId": {
    "type": "string"
   },
   "deviceSettings": {
    "type": "string",
    "description": "Device settings"
   },
   "gateMode": {
    "type": "string",
    "description": "Gate mode"
   },
   "readerSettings": {
    "type": "string",
    "description": "Reader settings"
   },
   "mediaProfiles": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media profiles"
   },
   "outcomeProfiles": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Outcome profiles"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "uiContent": {
    "type": "string",
    "description": "UI content"
   },
   "localRules": {
    "type": "string",
    "description": "Local rules"
   },
   "offlineSecurityConfiguration": {
    "type": "string",
    "description": "Offline security package reference"
   },
   "welcomePage": {
    "type": "string",
    "description": "Welcome page"
   },
   "instructions": {
    "type": "string",
    "description": "Instructions"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket status"
   },
   "reasonMessage": {
    "type": "string",
    "description": "Reason message"
   },
   "promotionalInformation": {
    "type": "string",
    "description": "Promotional information"
   },
   "externalApprovedWebpage": {
    "type": "string",
    "description": "External approved webpage"
   },
   "emergencyInformation": {
    "type": "string",
    "description": "Emergency information"
   },
   "version": {
    "type": "string",
    "description": "Configuration version, for rollback"
   },
   "deploymentStage": {
    "type": "string",
    "enum": [
     "draft",
     "testDevice",
     "deviceGroup",
     "venueRollout"
    ]
   }
  },
  "required": [
   "configurationId",
   "venueId",
   "deviceGroupId"
  ]
 },
 "DeviceTypeHardwareLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Device Type & Hardware Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "hardwareType": {
    "type": "string",
    "enum": [
     "standardTurnstile",
     "fullHeightTurnstile",
     "tripodTurnstile",
     "speedGate",
     "wideLane",
     "accessiblePodGate",
     "buggyGate",
     "vipGate",
     "staffGate",
     "androidHandheld",
     "iosDevice",
     "tablet",
     "qrBarcodeReader",
     "rfidReader",
     "nfcReader",
     "multiTechnologyReader",
     "biometricReader",
     "podium",
     "counter",
     "beacon",
     "cameraController",
     "externalAccessDevice"
    ],
    "description": "Specific hardware type within the device category"
   },
   "manufacturer": {
    "type": "string",
    "description": "Manufacturer"
   },
   "model": {
    "type": "string",
    "description": "Model"
   },
   "deviceCategory": {
    "type": "string",
    "enum": [
     "turnstile",
     "specialGate",
     "mobile",
     "reader",
     "other"
    ],
    "description": "Device Category"
   },
   "supportedTechnologies": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Supported technologies"
   },
   "connectivity": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Connectivity"
   },
   "offlineCapability": {
    "type": "boolean",
    "description": "Offline capability"
   },
   "screenCapability": {
    "type": "boolean",
    "description": "Screen capability"
   },
   "soundCapability": {
    "type": "boolean",
    "description": "Sound capability"
   },
   "lightCapability": {
    "type": "boolean",
    "description": "Light capability"
   },
   "relayControllerSupport": {
    "type": "boolean",
    "description": "Relay/controller support"
   },
   "paymentCapabilityWhereAvailable": {
    "type": "boolean",
    "description": "payment capability where available"
   },
   "firmwareSoftwareInformation": {
    "type": "string",
    "description": "firmware/software information"
   },
   "hardwareModelId": {
    "type": "string"
   }
  }
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
 "ExternalCredentialSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n",
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
 "GateModesFreeSpinEmergencyControlsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Gate Modes, Free Spin & Emergency Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "whoCanActivate": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Roles allowed to activate this mode"
   },
   "venueScope": {
    "type": "string",
    "description": "Venue scope"
   },
   "gateGroup": {
    "type": "string",
    "description": "Gate group"
   },
   "reasonRequired": {
    "type": "string",
    "description": "reason"
   },
   "emergencyCode": {
    "type": "string",
    "description": "emergency code"
   },
   "automaticNotification": {
    "type": "boolean",
    "description": "automatic notification"
   },
   "incidentRecord": {
    "type": "boolean",
    "description": "Activation creates an incident record"
   },
   "policyId": {
    "type": "string"
   },
   "mode": {
    "type": "string",
    "enum": [
     "freeFlow",
     "dropArm"
    ],
    "description": "Non-standard operating mode this policy governs (R221 vocabulary): freeFlow covers free spin and count only, dropArm is the emergency mode"
   }
  }
 },
 "HandheldMobileAccessDeviceConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Handheld & Mobile Access Device Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "name": {
    "type": "string",
    "description": "e.g. Standard Attendant, Supervisor"
   },
   "profileId": {
    "type": "string",
    "description": "Handheld configuration profile identifier"
   },
   "deviceType": {
    "type": "string",
    "description": "Device type"
   },
   "platform": {
    "type": "string",
    "enum": [
     "android",
     "ios"
    ],
    "description": "Android/iOS"
   },
   "assignedVenue": {
    "type": "string",
    "description": "assigned venue"
   },
   "assignedZone": {
    "type": "string",
    "description": "assigned zone"
   },
   "assignedOperatorGroup": {
    "type": "string",
    "description": "assigned operator group"
   },
   "permittedOperatingModes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "permitted operating modes"
   },
   "offlineCapability": {
    "type": "boolean",
    "description": "offline capability"
   },
   "scannerSource": {
    "type": "string",
    "description": "scanner source"
   },
   "biometricCapabilityWhereSupported": {
    "type": "boolean",
    "description": "biometric capability where supported"
   },
   "enabledFunctions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "scanTicket",
      "searchTicket",
      "entry",
      "exit",
      "reEntry",
      "crossover",
      "groupAdmission",
      "manualAttendance",
      "override",
      "viewHistory",
      "changeDeviceMode"
     ]
    },
    "description": "Functions enabled for this device role"
   }
  },
  "required": [
   "profileId",
   "name"
  ]
 },
 "HandheldMobileAccessDeviceConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Handheld & Mobile Access Device Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "name": {
    "type": "string",
    "description": "e.g. Standard Attendant, Supervisor"
   },
   "profileId": {
    "type": "string",
    "description": "Handheld configuration profile identifier"
   },
   "deviceType": {
    "type": "string",
    "description": "Device type"
   },
   "platform": {
    "type": "string",
    "enum": [
     "android",
     "ios"
    ],
    "description": "Android/iOS"
   },
   "assignedVenue": {
    "type": "string",
    "description": "assigned venue"
   },
   "assignedZone": {
    "type": "string",
    "description": "assigned zone"
   },
   "assignedOperatorGroup": {
    "type": "string",
    "description": "assigned operator group"
   },
   "permittedOperatingModes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "permitted operating modes"
   },
   "offlineCapability": {
    "type": "boolean",
    "description": "offline capability"
   },
   "scannerSource": {
    "type": "string",
    "description": "scanner source"
   },
   "biometricCapabilityWhereSupported": {
    "type": "boolean",
    "description": "biometric capability where supported"
   },
   "enabledFunctions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "scanTicket",
      "searchTicket",
      "entry",
      "exit",
      "reEntry",
      "crossover",
      "groupAdmission",
      "manualAttendance",
      "override",
      "viewHistory",
      "changeDeviceMode"
     ]
    },
    "description": "Functions enabled for this device role"
   }
  },
  "required": [
   "profileId",
   "name"
  ]
 },
 "HardwareCompatibilityHealthTestingDeploymentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Hardware Compatibility, Health, Testing & Deployment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "deviceId": {
    "type": "string",
    "description": "Device identifier"
   },
   "capabilities": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicQr",
      "rfid",
      "nfc",
      "facePass",
      "offline",
      "heightCheck"
     ]
    },
    "description": "Capabilities this device supports, from the compatibility matrix"
   },
   "rolloutScope": {
    "type": "string",
    "enum": [
     "pilot",
     "selectedGates",
     "deviceGroup",
     "venue"
    ],
    "description": "How far the production rollout of this device reaches"
   },
   "deviceName": {
    "type": "string",
    "description": "Device or gate name, e.g. Gate A, HH-01"
   },
   "lifecycleStatus": {
    "type": "string",
    "enum": [
     "registered",
     "configured",
     "tested",
     "approved",
     "production"
    ],
    "description": "Certification stage; no device enters production until validated"
   }
  },
  "required": [
   "deviceId"
  ]
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "PhysicalDeviceRegistrationProvisioningView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Physical Device Registration & Provisioning displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "deviceId": {
    "type": "string",
    "description": "Device ID"
   },
   "serialNumber": {
    "type": "string",
    "description": "Serial Number"
   },
   "hardwareModel": {
    "type": "string",
    "description": "Hardware Model"
   },
   "manufacturer": {
    "type": "string",
    "description": "Manufacturer"
   },
   "tenantId": {
    "type": "string",
    "description": "Tenant"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "parkId": {
    "type": "string",
    "description": "Park"
   },
   "zoneId": {
    "type": "string",
    "description": "Zone"
   },
   "accessPointId": {
    "type": "string",
    "description": "Access Point"
   },
   "gateLane": {
    "type": "string",
    "description": "Gate/Lane"
   },
   "ipNetworkReference": {
    "type": "string",
    "description": "IP/network reference"
   },
   "controllerReference": {
    "type": "string",
    "description": "controller reference"
   },
   "installationDate": {
    "type": "string",
    "format": "date",
    "description": "installation date"
   },
   "provisioningStage": {
    "type": "string",
    "enum": [
     "registered",
     "hardwareProfileAssigned",
     "locationAssigned",
     "authenticated",
     "configurationDownloaded",
     "securityPackageDownloaded",
     "connectivityTested",
     "active"
    ]
   }
  }
 },
 "ReaderScannerPeripheralConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Reader, Scanner & Peripheral Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "accessPointId": {
    "type": "string",
    "description": "Gate or device the peripherals attach to"
   },
   "readers": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Attached readers, e.g. qrBarcode, rfid, nfc, biometricCamera, paymentReader, heightSensor"
   },
   "verificationPriority": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Order methods are tried, e.g. facePass, dynamicQr, rfid, nfc"
   },
   "rfidRange": {
    "type": "string",
    "enum": [
     "near",
     "medium",
     "far"
    ]
   },
   "heightVerificationEnabled": {
    "type": "boolean",
    "description": "Height check for junior tickets; without a supported sensor the result is yellow for operator verification"
   },
   "capabilityWarnings": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Configured checks the attached hardware cannot perform"
   }
  },
  "required": [
   "accessPointId"
  ]
 },
 "ReaderScannerPeripheralConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Reader, Scanner & Peripheral Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "accessPointId": {
    "type": "string",
    "description": "Gate or device the peripherals attach to"
   },
   "readers": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Attached readers, e.g. qrBarcode, rfid, nfc, biometricCamera, paymentReader, heightSensor"
   },
   "verificationPriority": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Order methods are tried, e.g. facePass, dynamicQr, rfid, nfc"
   },
   "rfidRange": {
    "type": "string",
    "enum": [
     "near",
     "medium",
     "far"
    ]
   },
   "heightVerificationEnabled": {
    "type": "boolean",
    "description": "Height check for junior tickets; without a supported sensor the result is yellow for operator verification"
   },
   "capabilityWarnings": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Configured checks the attached hardware cannot perform"
   }
  },
  "required": [
   "accessPointId"
  ]
 },
 "RegisteredDevice": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "description": "**The device register of record** (decided 29 September, build pass). Identity, enrolment, credential, firmware and push registration for every device in the estate live on this row. `access.access_device` places access-control devices in the gate topology and repeats serial, versions, health and lifecycle; the two are not merged yet, and where they disagree this row wins.\n",
  "required": [
   "id",
   "kind",
   "driver"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
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
    "format": "uuid",
    "nullable": true,
    "description": "Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September); `registerDevice` refuses either mistake with `422`.\n"
   },
   "model": {
    "type": "string",
    "nullable": true
   },
   "pushToken": {
    "type": "string",
    "format": "password",
    "nullable": true,
    "writeOnly": true,
    "description": "BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"
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
    "readOnly": true,
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
    "nullable": true,
    "readOnly": true,
    "description": "As the device last reported it on its heartbeat."
   },
   "isRequired": {
    "type": "boolean",
    "description": "True blocks shift open when the device is unreachable."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "online",
     "offline",
     "error",
     "consumableLow",
     "needsAttention",
     "unknown"
    ],
    "description": "What the device last said on its heartbeat; `unknown` until it has."
   },
   "batteryPercent": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "minimum": 0,
    "maximum": 100,
    "description": "Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
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
    "readOnly": true,
    "description": "**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "capabilities": {
    "type": "array",
    "readOnly": true,
    "items": {
     "$ref": "#/components/schemas/DeviceCapability"
    },
    "description": "BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"
   },
   "enrolmentState": {
    "type": "string",
    "enum": [
     "registered",
     "enrolled",
     "provisioned",
     "active",
     "deactivated",
     "retired"
    ],
    "default": "registered",
    "readOnly": true,
    "description": "BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"
   },
   "retiredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"
   }
  }
 },
 "ScanAnomalyRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n",
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
 "TurnstileLaneBehaviorConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Turnstile & Lane Behavior Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "accessPointId": {
    "type": "string",
    "description": "Turnstile or lane being configured"
   },
   "mode": {
    "type": "string",
    "enum": [
     "normal",
     "freeFlow",
     "dropArm",
     "closed",
     "podium",
     "maintenance"
    ],
    "description": "Default operating mode of the lane (AccessPointOperatingMode, R221). Direction is fixed per access point; re-entry, crossover, fast pass and group are admission rules, not lane modes"
   },
   "passThroughTimeout": {
    "type": "integer",
    "description": "Seconds"
   },
   "relockBehavior": {
    "type": "string",
    "description": "relock behavior"
   },
   "incompletePassageBehavior": {
    "type": "string",
    "description": "incomplete passage behavior"
   },
   "unlockDuration": {
    "type": "integer",
    "description": "Seconds"
   }
  },
  "required": [
   "accessPointId",
   "mode"
  ]
 },
 "TurnstileLaneBehaviorConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Turnstile & Lane Behavior Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "accessPointId": {
    "type": "string",
    "description": "Turnstile or lane being configured"
   },
   "mode": {
    "type": "string",
    "enum": [
     "normal",
     "freeFlow",
     "dropArm",
     "closed",
     "podium",
     "maintenance"
    ],
    "description": "Default operating mode of the lane (AccessPointOperatingMode, R221). Direction is fixed per access point; re-entry, crossover, fast pass and group are admission rules, not lane modes"
   },
   "passThroughTimeout": {
    "type": "integer",
    "description": "Seconds"
   },
   "relockBehavior": {
    "type": "string",
    "description": "relock behavior"
   },
   "incompletePassageBehavior": {
    "type": "string",
    "description": "incomplete passage behavior"
   },
   "unlockDuration": {
    "type": "integer",
    "description": "Seconds"
   }
  },
  "required": [
   "accessPointId",
   "mode"
  ]
 },
 "TurnstileMode": {
  "type": "string",
  "description": "**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n",
  "enum": [
   "freeRotation",
   "closed"
  ]
 },
 "ValidationOutcomeGuestFeedbackDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Validation Outcome & Guest Feedback Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "appliesTo": {
    "type": "string",
    "enum": [
     "adult",
     "child",
     "vip",
     "pod",
     "membership",
     "invalidCredential",
     "wrongVerificationMethod",
     "biometricReview",
     "reEntryException"
    ],
    "description": "Guest type or case this response is for"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "granted",
     "operatorAction",
     "denied"
    ]
   },
   "venueId": {
    "type": "string"
   },
   "outcomeProfileId": {
    "type": "string"
   },
   "lightColour": {
    "type": "string",
    "enum": [
     "green",
     "yellow",
     "red"
    ],
    "description": "Light shown"
   },
   "gateAction": {
    "type": "string",
    "enum": [
     "open",
     "remainsControlled",
     "remainsLocked"
    ],
    "description": "What the gate does"
   },
   "sound": {
    "type": "string",
    "enum": [
     "successTone",
     "alertSound",
     "denialSound"
    ],
    "description": "Sound played"
   },
   "pictogram": {
    "type": "string",
    "description": "✓ pictogram"
   },
   "customMessage": {
    "type": "string",
    "description": "Custom message"
   },
   "operatorPrompt": {
    "type": "string",
    "description": "operator prompt"
   },
   "reasonCode": {
    "type": "string",
    "description": "reason code"
   },
   "language": {
    "type": "string",
    "description": "Message language, e.g. ar, en"
   }
  },
  "required": [
   "outcomeProfileId",
   "venueId",
   "outcome",
   "appliesTo"
  ]
 },
 "ValidationOutcomeGuestFeedbackDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Validation Outcome & Guest Feedback Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "appliesTo": {
    "type": "string",
    "enum": [
     "adult",
     "child",
     "vip",
     "pod",
     "membership",
     "invalidCredential",
     "wrongVerificationMethod",
     "biometricReview",
     "reEntryException"
    ],
    "description": "Guest type or case this response is for"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "granted",
     "operatorAction",
     "denied"
    ]
   },
   "venueId": {
    "type": "string"
   },
   "outcomeProfileId": {
    "type": "string"
   },
   "lightColour": {
    "type": "string",
    "enum": [
     "green",
     "yellow",
     "red"
    ],
    "description": "Light shown"
   },
   "gateAction": {
    "type": "string",
    "enum": [
     "open",
     "remainsControlled",
     "remainsLocked"
    ],
    "description": "What the gate does"
   },
   "sound": {
    "type": "string",
    "enum": [
     "successTone",
     "alertSound",
     "denialSound"
    ],
    "description": "Sound played"
   },
   "pictogram": {
    "type": "string",
    "description": "✓ pictogram"
   },
   "customMessage": {
    "type": "string",
    "description": "Custom message"
   },
   "operatorPrompt": {
    "type": "string",
    "description": "operator prompt"
   },
   "reasonCode": {
    "type": "string",
    "description": "reason code"
   },
   "language": {
    "type": "string",
    "description": "Message language, e.g. ar, en"
   }
  },
  "required": [
   "outcomeProfileId",
   "venueId",
   "outcome",
   "appliesTo"
  ]
 }
}
```
