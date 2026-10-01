# P07-access-02 — P07 · Access (2 of 2)

**1 screens · 4 operations · 9 schemas · 2 permissions**

Platform P07 Venue Scanner · ships as **venue-staff-mobile** ·
staff audience · handheld ·
offline-capable

## Who this is for

**staff on handheld.** Everything below is how you know what is
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
  `SCOPE_VIEW, TURNSTILE_MODE_SET`. A control nobody can use must say so,
  not sit enabled and fail.
- **3 of these operations work offline**: getAccessPoint, listAccessPoints, setTurnstileMode
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SCN-016` | Gate mode | listDetail | 4 | 2 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SCN-016",
  "name": "Gate mode",
  "module": "Access",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-scanner",
   "route": "/access/gate-mode",
   "component": "apps/venue-scanner/src/routes/access/GateModeDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "SCN-001",
    "SCN-002",
    "SCN-003"
   ],
   "inferred": false,
   "entryFrom": [
    "SCN-002"
   ],
   "notes": "**Reached from SCN-002** — gate mode is set for the access point being worked. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "SCN-001",
     "trigger": "Sign in",
     "provenance": "derived — SCN-001 declares entryState.params challengeId and SCN-016 holds none of them. The edge carries nothing: SCN-001 finds challengeId (createMfaChallenge) itself, and SCN-001 opens on its own"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId and SCN-016 holds accessPointId, so an edge into it carries them"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "provenance": "derived — SCN-003 declares entryState.params mediaCode, rightId and SCN-016 holds none of them. The edge carries nothing: mediaCode, rightId only pre-select (deep link or optional), and SCN-003 opens on its own"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Authoring operations removed 24 August**: createAccessPoint, setAccessPointGeofence, updateAccessPoint. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere. **The podium sets the operating mode** (normal, freeFlow, dropArm, closed, podium, maintenance), required on every save; the turnstile mode (freeRotation or closed) is optional and offered only under normal or podium. **Direction is display-only here**: it is fixed per access point and set in the back office (BO-064) (decided 28 September, audit R221).",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listAccessPoints` reads the population and `getAccessPoint` reads one of them — list, select, act",
  "purpose": "Podium operation. Changes what the gate does.",
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
       "operation": "listAccessPoints",
       "notes": "Sends `?venueId=` to `listAccessPoints`.",
       "provenance": "contract access.yaml GET /access-points"
      },
      {
       "kind": "dataTable",
       "label": "Every access point",
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
        "AccessPoint.antiPassbackEnabled"
       ],
       "operation": "listAccessPoints",
       "provenance": "contract access.yaml GET /access-points"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access point",
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
       "label": "Save gate mode",
       "operation": "setTurnstileMode",
       "provenance": "contract access.yaml PUT /access-points/{accessPointId}/mode"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel gate mode change",
       "operation": "cancelGateModeChange",
       "permission": "TURNSTILE_MODE_SET",
       "notes": "Cancels a `pending` gate mode change, one `setTurnstileMode` scheduled with a future `effectiveAt`.",
       "provenance": "contract access.yaml POST /gate-mode-changes/{changeId}/cancel"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gate mode list.",
   "error": "Could not load. Names which read failed and leaves the gate mode untouched.",
   "emptyFirstRun": "No gate mode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId and the gate mode are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `SCOPE_VIEW`, which `getAccessPoint` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Requests only.** Hardware control is out of contract and the vendor SDK is outstanding (CF-33)"
  },
  "apis": [
   {
    "operationId": "setTurnstileMode",
    "contract": "access",
    "purpose": "Podium sets the operating mode (required), optionally narrowed by the turnstile mode under normal or podium; direction is display-only (audit R221)",
    "trigger": "onAction"
   },
   {
    "operationId": "getAccessPoint",
    "contract": "access",
    "purpose": "Read an access point",
    "trigger": "onAction"
   },
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "List access points",
    "trigger": "onLoad"
   },
   {
    "operationId": "cancelGateModeChange",
    "contract": "access",
    "purpose": "Cancel a scheduled gate mode change",
    "trigger": "onAction",
    "invalidates": [
     "listAccessPoints"
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
     "name": "changeId",
     "from": "navigation",
     "optional": true
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `accessPointId`.",
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
   "board": "wireframes/P07 Venue Scanner.dc.html#scn-016"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetTurnstileMode",
    "component": "modal",
    "trigger": "Save gate mode",
    "body": "**Collects what `setTurnstileMode` sends before it is called.** Required: `operatingMode` (normal, freeFlow, dropArm, closed, podium, maintenance). Optional: `mode` (freeRotation or closed), offered only with normal or podium, since the other four already decide the arm and the server refuses it 400; and `reason`. **Direction is not on this form**: it is fixed per access point and set in the back office (BO-064) with createAccessPoint/updateAccessPoint (decided 28 September, audit R221). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save gate mode",
     "operation": "setTurnstileMode"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "operatingMode",
      "mode",
      "reason"
     ]
    },
    "provenance": "contract access.yaml PUT /access-points/{accessPointId}/mode"
   },
   {
    "id": "confirmCancelGateModeChange",
    "component": "confirmDialog",
    "trigger": "Cancel gate mode change",
    "body": "**Names what `cancelGateModeChange` changes and what it leaves alone**, in the consequence rather than the verb. A access gate mode change this affects should be identified in the dialog, not just counted. **Collects what `cancelGateModeChange` sends before it is called.** Nothing in the body is required. Optional: `reason`.",
    "provenance": "contract access.yaml POST /gate-mode-changes/{changeId}/cancel"
   }
  ],
  "_platform": {
   "code": "P07",
   "audience": "staff",
   "formFactor": "handheld",
   "shortName": "Venue Scanner",
   "name": "Venue Scanner — Access Control",
   "app": "venue-scanner",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "handheld",
    "siblings": [
     "P06"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
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
 "cancelGateModeChange": {
  "method": "POST",
  "path": "/gate-mode-changes/{changeId}/cancel",
  "contract": "access",
  "summary": "Cancel a scheduled gate mode change",
  "permission": "TURNSTILE_MODE_SET",
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
  "responds": "AccessGateModeChange"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessGateModeChange": {
  "type": "object",
  "x-ticvai-persistence": "access.gate_mode_change",
  "description": "One gate mode change on an access point, pending or applied: from and target mode, operator, reason and effective time. Append-only history (declared 29 September, data-model close-out DM1) Written by setTurnstileMode (applied at once, or pending until a future effectiveAt) and cancelGateModeChange; a timer applies a pending change at its effective time (decided 29 September, writers pass).",
  "required": [
   "id",
   "venueId",
   "accessPointId",
   "targetMode",
   "status",
   "changedByPrincipalId",
   "changedAt",
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
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "fromMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "nullable": true
   },
   "targetMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "applied",
     "cancelled"
    ]
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "effectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "changedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "Operator"
   },
   "changedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
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
 "TurnstileMode": {
  "type": "string",
  "description": "**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n",
  "enum": [
   "freeRotation",
   "closed"
  ]
 }
}
```
