# WS06 — Access Control board 6

**10 screens · 10 operations · 15 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-194` | Device & Gate Command Center | listDetail | 1 | 0 | — |
| `BO-195` | Device Type & Hardware Library | listDetail | 1 | 0 | — |
| `BO-196` | Physical Device Registration & Provisioning | configEditor | 1 | 0 | — |
| `BO-197` | Turnstile & Lane Behavior Configuration | configEditor | 1 | 0 | — |
| `BO-198` | Validation Outcome & Guest Feedback Designer | configEditor | 1 | 0 | — |
| `BO-199` | Reader, Scanner & Peripheral Configuration | listDetail | 1 | 0 | — |
| `BO-200` | Handheld & Mobile Access Device Configuration | configEditor | 1 | 1 | — |
| `BO-201` | Gate Modes, Free Spin & Emergency Controls | configEditor | 1 | 0 | — |
| `BO-202` | Device Software, Content & Remote Configuration | configEditor | 1 | 0 | — |
| `BO-203` | Hardware Compatibility, Health, Testing & Deployment | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-194, BO-195, BO-199, BO-203 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide the central operational/configuration view of the complete access-control hardware estate.",
  "purposeNote": "Operations can identify every access-control device and its current operational/configuration state from one screen.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every device gate",
       "columns": [
        "DeviceGateCommandCenterView.totalDevices",
        "DeviceGateCommandCenterView.online",
        "DeviceGateCommandCenterView.offline",
        "DeviceGateCommandCenterView.degraded",
        "DeviceGateCommandCenterView.turnstiles",
        "DeviceGateCommandCenterView.handhelds",
        "DeviceGateCommandCenterView.biometricReaders",
        "DeviceGateCommandCenterView.rfidNfcReaders",
        "DeviceGateCommandCenterView.gatesOpen",
        "DeviceGateCommandCenterView.gatesClosed",
        "DeviceGateCommandCenterView.devicesRequiringSync",
        "DeviceGateCommandCenterView.firmwareSoftwareExceptions",
        "DeviceGateCommandCenterView.hardwareAlerts",
        "DeviceGateCommandCenterView.connectivity",
        "DeviceGateCommandCenterView.lastHeartbeat",
        "DeviceGateCommandCenterView.configurationVersion",
        "DeviceGateCommandCenterView.localRuleVersion",
        "DeviceGateCommandCenterView.credentialSecurityPackageVersion",
        "DeviceGateCommandCenterView.scannerHealth",
        "DeviceGateCommandCenterView.controllerHealth",
        "DeviceGateCommandCenterView.ai"
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
        "DeviceGateCommandCenterView.totalDevices",
        "DeviceGateCommandCenterView.online",
        "DeviceGateCommandCenterView.offline",
        "DeviceGateCommandCenterView.degraded",
        "DeviceGateCommandCenterView.turnstiles",
        "DeviceGateCommandCenterView.handhelds",
        "DeviceGateCommandCenterView.biometricReaders",
        "DeviceGateCommandCenterView.rfidNfcReaders",
        "DeviceGateCommandCenterView.gatesOpen",
        "DeviceGateCommandCenterView.gatesClosed",
        "DeviceGateCommandCenterView.devicesRequiringSync",
        "DeviceGateCommandCenterView.firmwareSoftwareExceptions",
        "DeviceGateCommandCenterView.hardwareAlerts",
        "DeviceGateCommandCenterView.connectivity",
        "DeviceGateCommandCenterView.lastHeartbeat",
        "DeviceGateCommandCenterView.configurationVersion",
        "DeviceGateCommandCenterView.localRuleVersion",
        "DeviceGateCommandCenterView.credentialSecurityPackageVersion",
        "DeviceGateCommandCenterView.scannerHealth",
        "DeviceGateCommandCenterView.controllerHealth",
        "DeviceGateCommandCenterView.ai"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Device Directory”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 70 §Display"
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
   }
  ],
  "entryState": {
   "preloaded": [
    "DeviceGateCommandCenterView.totalDevices",
    "DeviceGateCommandCenterView.online",
    "DeviceGateCommandCenterView.offline",
    "DeviceGateCommandCenterView.degraded",
    "DeviceGateCommandCenterView.turnstiles",
    "DeviceGateCommandCenterView.handhelds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-194"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 70. 21 of 21 labels bound to a contract property; 21 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create reusable hardware definitions independently from physical deployed devices.",
  "purposeNote": "manufacturer-specific logic into admission policies.",
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
   }
  ],
  "entryState": {
   "preloaded": [
    "DeviceTypeHardwareLibraryView.standard",
    "DeviceTypeHardwareLibraryView.fullHeight",
    "DeviceTypeHardwareLibraryView.tripod",
    "DeviceTypeHardwareLibraryView.speedGate",
    "DeviceTypeHardwareLibraryView.wideLane"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-195"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 72. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "operation": "listPhysicalDeviceRegistration"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Register actual deployed hardware and connect it to the Board 1 topology.",
  "purposeNote": "Every physical access-control device is uniquely registered, authenticated and assigned to its correct topology location.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-196"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 73. 0 of 0 labels bound to a contract property; 12 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "operation": "setTurnstileLaneBehavior"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how each turnstile or lane behaves. The matrix specifically requires software on turnstiles to behave differently according to card/ticket type and supports different operating modes.",
  "purposeNote": "Each gate can execute different configured behaviors according to its mode and the validated credential.",
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
    "trigger": "onAction",
    "invalidates": [
     "setTurnstileLaneBehavior"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-197"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure what the physical access device does and displays after validation. The matrix explicitly requires valid/non-valid messages, lights, pictograms and sounds, including green/yellow/red behavior.",
  "purposeNote": "Every access decision produces a configurable and understandable physical response for the guest and operator.",
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
    "trigger": "onAction",
    "invalidates": [
     "setValidationOutcomeGuest"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-198"
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
     "operation": "setReaderScannerPeripheral"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the technologies attached to a gate/device.",
  "purposeNote": "Readers and peripherals can be independently associated with gates and checked against required admission capabilities.",
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
    "trigger": "onAction",
    "invalidates": [
     "setReaderScannerPeripheral"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-199"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure mobile access-control devices used by staff. The matrix explicitly requires handheld devices and Android/iOS dedicated mobile applications.",
  "purposeNote": "Mobile access devices can be centrally configured, restricted and revoked according to their operational role.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Scan Ticket, Search Ticket, Override, View History. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 78 §Enable/disable"
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
    "trigger": "onAction",
    "invalidates": [
     "setHandheldMobileAccess"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-200"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 78. 0 of 0 labels bound to a contract property; 12 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage non-standard operational modes. The source specifically requires Free Spin and Drop Arm/Emergency behavior.",
  "purposeNote": "Authorized operations personnel can rapidly change gate modes across individual devices or device groups while maintaining full auditability.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-201"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 79. 0 of 0 labels bound to a contract property; 6 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Centrally control access-control device software and guest-facing configuration. The source requires the ability to configure/manage software on turnstiles, add external webpages on supported screens, and enable payment technologies where available.",
  "purposeNote": "Device configuration and supported content can be centrally deployed without manually configuring each turnstile.",
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
    "trigger": "onAction",
    "invalidates": [
     "setDeviceSoftwareContent"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-202"
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
   "notes": "**Reached from BO-194, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the final testing and governance layer before hardware is used in production. The matrix says venues may select their hardware, while the provider must expose hardware limitations and recommendations.",
  "purposeNote": "No access device enters production until its required capabilities, connectivity, security configuration and physical responses have been successfully validated. Board 6 — Final 10-Screen Structure # Backend Screen Main Responsibility 6.1 Device & Gate Command Center Hardware estate and live health 6.2 Device Type & Hardware Library Reusable hardware/model definitions 6.3 Physical Device Registration & Provisioning Register and authenticate deployed devices 6.4 Turnstile & Lane Behavior Configuration Gate modes, direction and physical behavior # Backend Screen Main Responsibility",
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
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listHardwareCompatibilityHealth",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
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
   }
  ],
  "entryState": {
   "preloaded": [
    "HardwareCompatibilityHealthTestingDeploymentView.rfid",
    "HardwareCompatibilityHealthTestingDeploymentView.nfc",
    "HardwareCompatibilityHealthTestingDeploymentView.offline",
    "HardwareCompatibilityHealthTestingDeploymentView.pilotDeployment",
    "HardwareCompatibilityHealthTestingDeploymentView.selectedGates"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-203"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 82. 0 of 0 labels bound to a contract property; 0 of 76 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listDeviceGate": {
  "method": "GET",
  "path": "/device-gate",
  "contract": "access",
  "summary": "Device & Gate Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DeviceGateCommandCenterView"
 },
 "listDeviceTypeHardware": {
  "method": "GET",
  "path": "/device-type-hardware",
  "contract": "access",
  "summary": "Device Type & Hardware Library",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "GateModesFreeSpinEmergencyControlsView"
 },
 "listHardwareCompatibilityHealth": {
  "method": "GET",
  "path": "/hardware-compatibility-health",
  "contract": "access",
  "summary": "Hardware Compatibility, Health, Testing & Deployment",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "HardwareCompatibilityHealthTestingDeploymentView"
 },
 "listPhysicalDeviceRegistration": {
  "method": "GET",
  "path": "/physical-device-registration",
  "contract": "access",
  "summary": "Physical Device Registration & Provisioning",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PhysicalDeviceRegistrationProvisioningView"
 },
 "setDeviceSoftwareContent": {
  "method": "PUT",
  "path": "/device-software-content",
  "contract": "access",
  "summary": "Device Software, Content & Remote Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "DeviceSoftwareContentRemoteConfigurationInput",
  "responds": "DeviceSoftwareContentRemoteConfigurationView"
 },
 "setHandheldMobileAccess": {
  "method": "PUT",
  "path": "/handheld-mobile-access",
  "contract": "access",
  "summary": "Handheld & Mobile Access Device Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "HandheldMobileAccessDeviceConfigurationInput",
  "responds": "HandheldMobileAccessDeviceConfigurationView"
 },
 "setReaderScannerPeripheral": {
  "method": "PUT",
  "path": "/reader-scanner-peripheral",
  "contract": "access",
  "summary": "Reader, Scanner & Peripheral Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
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
  "parameters": [],
  "requestBody": "TurnstileLaneBehaviorConfigurationInput",
  "responds": "TurnstileLaneBehaviorConfigurationView"
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
  "parameters": [],
  "requestBody": "ValidationOutcomeGuestFeedbackDesignerInput",
  "responds": "ValidationOutcomeGuestFeedbackDesignerView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "DeviceGateCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Device & Gate Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
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
    "type": "string",
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
    "type": "string",
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
   "ai": {
    "type": "string",
    "description": "AI"
   }
  }
 },
 "DeviceSoftwareContentRemoteConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Device Software, Content & Remote Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
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
    "type": "string",
    "description": "Media profiles"
   },
   "outcomeProfiles": {
    "type": "string",
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
    "type": "integer",
    "description": "Offline security configuration"
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
   }
  }
 },
 "DeviceSoftwareContentRemoteConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Device Software, Content & Remote Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "type": "string",
    "description": "Media profiles"
   },
   "outcomeProfiles": {
    "type": "string",
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
    "type": "integer",
    "description": "Offline security configuration"
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
   }
  }
 },
 "DeviceTypeHardwareLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Device Type & Hardware Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "standard": {
    "type": "string",
    "description": "Standard"
   },
   "fullHeight": {
    "type": "string",
    "description": "Full Height"
   },
   "tripod": {
    "type": "string",
    "description": "Tripod"
   },
   "speedGate": {
    "type": "string",
    "description": "Speed Gate"
   },
   "wideLane": {
    "type": "string",
    "description": "Wide Lane"
   },
   "accessiblePodGate": {
    "type": "string",
    "description": "Accessible/POD Gate"
   },
   "buggyGate": {
    "type": "string",
    "description": "Buggy Gate"
   },
   "vipGate": {
    "type": "string",
    "description": "VIP Gate"
   },
   "staffGate": {
    "type": "string",
    "description": "Staff Gate"
   },
   "androidHandheld": {
    "type": "string",
    "description": "Android Handheld"
   },
   "iosDevice": {
    "type": "string",
    "description": "iOS Device"
   },
   "tablet": {
    "type": "string",
    "description": "Tablet"
   },
   "qrBarcode": {
    "type": "string",
    "description": "QR/Barcode"
   },
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "multiTechnology": {
    "type": "string",
    "description": "Multi-technology"
   },
   "biometric": {
    "type": "string",
    "description": "Biometric"
   },
   "podium": {
    "type": "string",
    "description": "Podium"
   },
   "counter": {
    "type": "string",
    "description": "Counter"
   },
   "beacon": {
    "type": "string",
    "description": "Beacon"
   },
   "cameraController": {
    "type": "string",
    "description": "camera/controller"
   },
   "supportedExternalAccessDevice": {
    "type": "string",
    "description": "supported external access device"
   },
   "standardTurnstiles": {
    "type": "string",
    "description": "standard turnstiles"
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
    "description": "Device Category"
   },
   "supportedTechnologies": {
    "type": "string",
    "description": "Supported technologies"
   },
   "connectivity": {
    "type": "string",
    "description": "Connectivity"
   },
   "offlineCapability": {
    "type": "integer",
    "description": "Offline capability"
   },
   "screenCapability": {
    "type": "string",
    "description": "Screen capability"
   },
   "soundCapability": {
    "type": "string",
    "description": "Sound capability"
   },
   "lightCapability": {
    "type": "string",
    "description": "Light capability"
   },
   "relayControllerSupport": {
    "type": "boolean",
    "description": "Relay/controller support"
   },
   "paymentCapabilityWhereAvailable": {
    "type": "string",
    "description": "payment capability where available"
   },
   "firmwareSoftwareInformation": {
    "type": "string",
    "description": "firmware/software information"
   }
  }
 },
 "GateModesFreeSpinEmergencyControlsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Gate Modes, Free Spin & Emergency Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   },
   "closed": {
    "type": "integer",
    "description": "Closed"
   },
   "credentialReadingOff": {
    "type": "string",
    "description": "Credential Reading: OFF"
   },
   "turnstileRotationCountOn": {
    "type": "integer",
    "description": "Turnstile Rotation Count: ON"
   },
   "whoCanActivate": {
    "type": "string",
    "description": "Who can activate"
   },
   "venueScope": {
    "type": "string",
    "description": "Venue scope"
   },
   "gateGroup": {
    "type": "string",
    "description": "Gate group"
   },
   "reason": {
    "type": "string",
    "description": "reason"
   },
   "emergencyCode": {
    "type": "string",
    "description": "emergency code"
   },
   "automaticNotification": {
    "type": "string",
    "description": "automatic notification"
   },
   "incidentRecord": {
    "type": "string",
    "description": "incident record"
   }
  }
 },
 "HandheldMobileAccessDeviceConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Handheld & Mobile Access Device Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "deviceType": {
    "type": "string",
    "description": "Device type"
   },
   "androidIos": {
    "type": "string",
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
    "type": "string",
    "description": "permitted operating modes"
   },
   "offlineCapability": {
    "type": "integer",
    "description": "offline capability"
   },
   "scannerSource": {
    "type": "string",
    "description": "scanner source"
   },
   "biometricCapabilityWhereSupported": {
    "type": "string",
    "description": "biometric capability where supported"
   },
   "scanTicket": {
    "type": "string",
    "description": "Scan Ticket"
   },
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   },
   "groupAdmission": {
    "type": "string",
    "description": "Group Admission"
   },
   "manualAttendance": {
    "type": "integer",
    "description": "Manual Attendance"
   },
   "changeDeviceMode": {
    "type": "string",
    "description": "Change Device Mode"
   },
   "scanGroupAdmission": {
    "type": "string",
    "description": "Scan + Group Admission"
   },
   "preventsFurtherTrustedAccessTransactions": {
    "type": "string",
    "description": "prevents further trusted access transactions"
   }
  }
 },
 "HandheldMobileAccessDeviceConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Handheld & Mobile Access Device Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "deviceType": {
    "type": "string",
    "description": "Device type"
   },
   "androidIos": {
    "type": "string",
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
    "type": "string",
    "description": "permitted operating modes"
   },
   "offlineCapability": {
    "type": "integer",
    "description": "offline capability"
   },
   "scannerSource": {
    "type": "string",
    "description": "scanner source"
   },
   "biometricCapabilityWhereSupported": {
    "type": "string",
    "description": "biometric capability where supported"
   },
   "scanTicket": {
    "type": "string",
    "description": "Scan Ticket"
   },
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   },
   "groupAdmission": {
    "type": "string",
    "description": "Group Admission"
   },
   "manualAttendance": {
    "type": "integer",
    "description": "Manual Attendance"
   },
   "changeDeviceMode": {
    "type": "string",
    "description": "Change Device Mode"
   },
   "scanGroupAdmission": {
    "type": "string",
    "description": "Scan + Group Admission"
   },
   "preventsFurtherTrustedAccessTransactions": {
    "type": "string",
    "description": "prevents further trusted access transactions"
   }
  }
 },
 "HardwareCompatibilityHealthTestingDeploymentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Hardware Compatibility, Health, Testing & Deployment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "rfid": {
    "type": "string",
    "description": "RFID ✓ ✓ ✓ ✓"
   },
   "nfc": {
    "type": "string",
    "description": "NFC ✓ — ✓ ✓"
   },
   "offline": {
    "type": "integer",
    "description": "Offline ✓ ✓ ✓ ✓"
   },
   "pilotDeployment": {
    "type": "string",
    "description": "Pilot deployment"
   },
   "selectedGates": {
    "type": "string",
    "description": "Selected gates"
   },
   "deviceGroup": {
    "type": "string",
    "description": "device group"
   },
   "venue": {
    "type": "string",
    "description": "venue"
   },
   "scheduledRollout": {
    "type": "string",
    "format": "date-time",
    "description": "scheduled rollout"
   },
   "rollback": {
    "type": "string",
    "description": "rollback"
   },
   "sounds": {
    "type": "string",
    "description": "sounds"
   },
   "board2AccessRules": {
    "type": "string",
    "description": "Board 2 — Access Rules"
   },
   "board6PhysicalExecution": {
    "type": "string",
    "description": "BOARD 6 — PHYSICAL EXECUTION"
   },
   "issues": {
    "type": "string",
    "description": "issues"
   },
   "disappears": {
    "type": "string",
    "description": "disappears?"
   },
   "distribute": {
    "type": "string",
    "description": "↓ Distribute"
   },
   "localValidation": {
    "type": "string",
    "description": "↓ Local validation"
   },
   "synchronize": {
    "type": "string",
    "description": "↑ Synchronize"
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
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "accessPoint": {
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
    "format": "date-time",
    "description": "installation date"
   },
   "useControlledDeviceCredentials": {
    "type": "string",
    "description": "Use controlled device credentials"
   },
   "useControlledDeviceCertificates": {
    "type": "string",
    "description": "Use controlled device certificates"
   },
   "whilePreserving": {
    "type": "string",
    "description": "while preserving"
   },
   "gateAssignment": {
    "type": "string",
    "description": "Gate assignment"
   },
   "configuration": {
    "type": "string",
    "description": "Configuration"
   },
   "accessRules": {
    "type": "string",
    "description": "Access rules"
   },
   "mediaProfiles": {
    "type": "string",
    "description": "Media profiles"
   },
   "operatingMode": {
    "type": "string",
    "description": "operating mode"
   }
  }
 },
 "ReaderScannerPeripheralConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Reader, Scanner & Peripheral Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "whereSupported": {
    "type": "string",
    "description": "where supported"
   },
   "yellowOperatorVerification": {
    "type": "string",
    "description": "Yellow → Operator Verification"
   }
  }
 },
 "ReaderScannerPeripheralConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Reader, Scanner & Peripheral Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "whereSupported": {
    "type": "string",
    "description": "where supported"
   },
   "yellowOperatorVerification": {
    "type": "string",
    "description": "Yellow → Operator Verification"
   }
  }
 },
 "TurnstileLaneBehaviorConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Turnstile & Lane Behavior Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "entryExit": {
    "type": "string",
    "description": "Entry/Exit"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "countOnly": {
    "type": "integer",
    "description": "Count Only"
   },
   "freeSpin": {
    "type": "string",
    "description": "Free Spin"
   },
   "closed": {
    "type": "integer",
    "description": "Closed"
   },
   "emergency": {
    "type": "string",
    "description": "Emergency"
   },
   "passThroughTimeout": {
    "type": "string",
    "description": "pass-through timeout"
   },
   "relockBehavior": {
    "type": "string",
    "description": "relock behavior"
   },
   "incompletePassageBehavior": {
    "type": "string",
    "description": "incomplete passage behavior"
   }
  }
 },
 "TurnstileLaneBehaviorConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Turnstile & Lane Behavior Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "entryExit": {
    "type": "string",
    "description": "Entry/Exit"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "countOnly": {
    "type": "integer",
    "description": "Count Only"
   },
   "freeSpin": {
    "type": "string",
    "description": "Free Spin"
   },
   "closed": {
    "type": "integer",
    "description": "Closed"
   },
   "emergency": {
    "type": "string",
    "description": "Emergency"
   },
   "passThroughTimeout": {
    "type": "string",
    "description": "pass-through timeout"
   },
   "relockBehavior": {
    "type": "string",
    "description": "relock behavior"
   },
   "incompletePassageBehavior": {
    "type": "string",
    "description": "incomplete passage behavior"
   }
  }
 },
 "ValidationOutcomeGuestFeedbackDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Validation Outcome & Guest Feedback Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "greenLight": {
    "type": "string",
    "description": "Green light"
   },
   "gateOpen": {
    "type": "integer",
    "description": "Gate open"
   },
   "successTone": {
    "type": "string",
    "description": "Success tone"
   },
   "pictogram": {
    "type": "string",
    "description": "✓ pictogram"
   },
   "customMessage": {
    "type": "string",
    "description": "Custom message"
   },
   "yellowLight": {
    "type": "string",
    "description": "Yellow light"
   },
   "alertSound": {
    "type": "string",
    "description": "Alert sound"
   },
   "gateRemainsControlled": {
    "type": "string",
    "description": "Gate remains controlled"
   },
   "operatorPrompt": {
    "type": "string",
    "description": "operator prompt"
   },
   "redLight": {
    "type": "string",
    "description": "Red light"
   },
   "denialSound": {
    "type": "string",
    "description": "Denial sound"
   },
   "gateRemainsLocked": {
    "type": "string",
    "description": "Gate remains locked"
   },
   "reasonCode": {
    "type": "string",
    "description": "reason code"
   },
   "redAccessDenied": {
    "type": "string",
    "description": "RED — ACCESS DENIED"
   }
  }
 },
 "ValidationOutcomeGuestFeedbackDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Validation Outcome & Guest Feedback Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "greenLight": {
    "type": "string",
    "description": "Green light"
   },
   "gateOpen": {
    "type": "integer",
    "description": "Gate open"
   },
   "successTone": {
    "type": "string",
    "description": "Success tone"
   },
   "pictogram": {
    "type": "string",
    "description": "✓ pictogram"
   },
   "customMessage": {
    "type": "string",
    "description": "Custom message"
   },
   "yellowLight": {
    "type": "string",
    "description": "Yellow light"
   },
   "alertSound": {
    "type": "string",
    "description": "Alert sound"
   },
   "gateRemainsControlled": {
    "type": "string",
    "description": "Gate remains controlled"
   },
   "operatorPrompt": {
    "type": "string",
    "description": "operator prompt"
   },
   "redLight": {
    "type": "string",
    "description": "Red light"
   },
   "denialSound": {
    "type": "string",
    "description": "Denial sound"
   },
   "gateRemainsLocked": {
    "type": "string",
    "description": "Gate remains locked"
   },
   "reasonCode": {
    "type": "string",
    "description": "reason code"
   },
   "redAccessDenied": {
    "type": "string",
    "description": "RED — ACCESS DENIED"
   }
  }
 }
}
```
