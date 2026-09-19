# P07-access-02 — P07 · Access (2 of 2)

**1 screens · 3 operations · 4 schemas · 2 permissions**

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
| `SCN-016` | Gate mode | listDetail | 3 | 0 | — |

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
     "carries": [
      "sessionId",
      "shiftId"
     ],
     "provenance": "derived — SCN-001 declares entryState.params sessionId, shiftId, so an edge into it must carry them"
    },
    {
     "to": "SCN-002",
     "trigger": "Access point & direction",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — SCN-002 declares entryState.params accessPointId, so an edge into it must carry them"
    },
    {
     "to": "SCN-003",
     "trigger": "Ready to scan",
     "carries": [
      "mediaCode",
      "rightId"
     ],
     "provenance": "derived — SCN-003 declares entryState.params mediaCode, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Authoring operations removed 24 August**: createAccessPoint, setAccessPointGeofence, updateAccessPoint. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere.",
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
       "kind": "dataTable",
       "label": "Every gate mode",
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
       "label": "The selected gate mode",
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
       "label": "Save changes",
       "operation": "setTurnstileMode",
       "provenance": "contract access.yaml PUT /access-points/{accessPointId}/mode"
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
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setTurnstileMode",
       "label": "Save turnstile mode",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAccessPoints",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setTurnstileMode",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gate mode list.",
   "error": "Could not load. Names which read failed and leaves the gate mode untouched.",
   "emptyFirstRun": "No gate mode yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gate mode are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Requests only.** Hardware control is out of contract and the vendor SDK is outstanding (CF-33)"
  },
  "apis": [
   {
    "operationId": "setTurnstileMode",
    "contract": "access",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAccessPoint",
    "contract": "access",
    "purpose": "Read an access point",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "List access points",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "accessPointId",
     "from": "deepLink"
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
 "Direction": {
  "type": "string",
  "enum": [
   "entry",
   "exit",
   "reentry",
   "crossover"
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
 }
}
```
