# P06-operations-03 — P06 · Operations (3 of 5)

**10 screens · 55 operations · 79 schemas · 23 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 23 permissions apply here:
  `AI_USE, ATTENDANCE_RECORD, CAPACITY_CONFIGURE, CASE_MANAGE, CASE_VIEW, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY`…. A control nobody can use must say so,
  not sit enabled and fail.
- **21 of these operations work offline**: addCaseMessage, applyManualDiscount, createCase, createOrder, getOrder, getProduct, getQueue, getVenueMap
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-031` | Queue monitor | listDetail | 8 | 3 | — |
| `EMP-032` | Manual wait entry | listDetail | 5 | 1 | — |
| `EMP-033` | Capacity view | listDetail | 6 | 4 | — |
| `EMP-034` | Walk-up sale | listDetail | 23 | 13 | — |
| `EMP-025` | Break management | listDetail | 2 | 1 | — |
| `EMP-026` | Incident report | listDetail | 5 | 3 | — |
| `EMP-027` | Incident detail | listDetail | 3 | 1 | — |
| `EMP-028` | Lost & found | listDetail | 7 | 5 | — |
| `EMP-029` | Guest assistance | listDetail | 12 | 8 | — |
| `EMP-030` | Venue map | listDetail | 4 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-031",
  "name": "Queue monitor",
  "module": "Operations",
  "requiresModule": "queue",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/queue-monitor",
   "component": "apps/venue-staff-app/src/routes/operations/QueueMonitorDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-032"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-031 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-031 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-031 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    },
    {
     "to": "EMP-032",
     "trigger": "The sensor is wrong, so a wait is entered by hand",
     "provenance": "flow F67 step 1→2",
     "carries": [
      "queueId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createQueue, updateQueue. **A handheld reads a queue and records a wait; it does not create one.** A queue is a venue configuration — bulk-attach residue, and `EMP-031` and `EMP-032` carried identical sets.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listQueues` reads the population and `getQueue` reads one of them — list, select, act",
  "purpose": "See the queue from the floor.",
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The queue list.",
   "error": "Could not load. Names which read failed and leaves the queue untouched.",
   "emptyFirstRun": "No queue yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, openOnly and the queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Last synced view with its age"
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
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "Queue-balancing suggestion (kind queueBalancing): return-slot allocation and redirection",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-031"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-032",
  "name": "Manual wait entry",
  "module": "Operations",
  "requiresModule": "queue",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/manual-wait-entry",
   "component": "apps/venue-staff-app/src/routes/operations/ManualWaitEntryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-033"
   ],
   "inferred": false,
   "fromFlows": true,
   "entryFrom": [
    "EMP-031"
   ],
   "notes": "**Reached from EMP-031** — a manual wait is entered from the queue that is not counting it. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-033",
     "trigger": "Capacity is checked against occupancy",
     "provenance": "flow F67 step 2→3"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-032 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-032 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-032 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    },
    {
     "to": "BO-005",
     "trigger": "Parties are called",
     "provenance": "flow F21 step 4→5",
     "operation": "setWaitTime",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "queueId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: BO-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: callNextParties, createQueue, setQueueStatus, updateQueue. **A handheld reads a queue and records a wait; it does not create one.** A queue is a venue configuration — bulk-attach residue, and `EMP-031` and `EMP-032` carried identical sets.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listQueueEntries` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Take over when the wait feed dies.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listQueueEntries",
       "notes": "Sends `?status=` to `listQueueEntries`.",
       "provenance": "contract queue.yaml GET /queues/{queueId}/entries"
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected waiting guest",
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
        "WaitingGuest.entitlementId",
        "WaitingGuest.calledAt",
        "WaitingGuest.returnWindowEndsAt",
        "WaitingGuest.redeemedAt",
        "WaitingGuest.admittedCount"
       ],
       "operation": "listQueueEntries",
       "provenance": "contract queue.yaml GET /queues/{queueId}/entries"
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save wait time",
       "operation": "setWaitTime",
       "provenance": "contract queue.yaml PUT /queues/{queueId}/wait-time"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The manual wait entry list.",
   "error": "Could not load. Names which read failed and leaves the manual wait entry untouched.",
   "emptyFirstRun": "No manual wait entry yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on status and the manual wait entry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `QUEUE_VIEW`, which `getQueue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Queues locally.** Manual entry exists because a feed died, so it must not need the network the feed lost"
  },
  "apis": [
   {
    "operationId": "setWaitTime",
    "contract": "queue",
    "purpose": "Manually set a wait time",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "getQueue",
    "contract": "queue",
    "purpose": "Read a queue with live position",
    "trigger": "onAction"
   },
   {
    "operationId": "listQueueEntries",
    "contract": "queue",
    "purpose": "List entries in a queue",
    "trigger": "onAction"
   },
   {
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "List queues",
    "trigger": "onLoad"
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
    "WaitTime.queueId",
    "WaitTime.queueName",
    "WaitTime.attractionProductId",
    "WaitTime.status",
    "WaitTime.waitMinutes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-032"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-033",
  "name": "Capacity view",
  "module": "Operations",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/capacity-view",
   "component": "apps/venue-staff-app/src/routes/operations/CapacityViewDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003",
    "EMP-032"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-033 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-033 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-033 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act",
  "purpose": "Know whether the next session can take a walk-up.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Performance id",
       "operation": "listChannelCapacities",
       "notes": "Sends `?performanceId=` to `listChannelCapacities`.",
       "provenance": "contract catalogue.yaml GET /channel-capacities"
      },
      {
       "kind": "dataTable",
       "label": "Every channel capacity",
       "bindsTo": "ChannelCapacity",
       "columns": [
        "ChannelCapacity.id",
        "ChannelCapacity.performanceId",
        "ChannelCapacity.name",
        "ChannelCapacity.seatCategoryId",
        "ChannelCapacity.oversellAllowance",
        "ChannelCapacity.oversellBasis",
        "ChannelCapacity.capacity",
        "ChannelCapacity.sold",
        "ChannelCapacity.leased",
        "ChannelCapacity.remaining",
        "ChannelCapacity.hasChannelAllocations",
        "ChannelCapacity.isSeated"
       ],
       "operation": "listChannelCapacities",
       "provenance": "contract catalogue.yaml GET /channel-capacities"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel capacity",
       "bindsTo": "ChannelCapacity",
       "columns": [
        "ChannelCapacity.id",
        "ChannelCapacity.performanceId",
        "ChannelCapacity.name",
        "ChannelCapacity.seatCategoryId",
        "ChannelCapacity.oversellAllowance",
        "ChannelCapacity.oversellBasis",
        "ChannelCapacity.capacity",
        "ChannelCapacity.sold",
        "ChannelCapacity.leased",
        "ChannelCapacity.remaining",
        "ChannelCapacity.hasChannelAllocations",
        "ChannelCapacity.isSeated"
       ],
       "operation": "listChannelCapacities",
       "provenance": "contract catalogue.yaml GET /channel-capacities"
      },
      {
       "kind": "detailPanel",
       "label": "The channel allocation set",
       "bindsTo": "ChannelAllocationSet",
       "columns": [
        "ChannelAllocationSet.channelCapacityId",
        "ChannelAllocationSet.capacity",
        "ChannelAllocationSet.allocations",
        "ChannelAllocationSet.generalPoolUnits",
        "ChannelAllocationSet.totalSold",
        "ChannelAllocationSet.totalRemaining"
       ],
       "operation": "getChannelAllocations",
       "provenance": "contract catalogue.yaml GET /channel-capacities/{channelCapacityId}/channel-allocations"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create channel capacity",
       "operation": "createChannelCapacity",
       "provenance": "contract catalogue.yaml POST /channel-capacities"
      },
      {
       "kind": "secondaryButton",
       "label": "Release channel allocation",
       "operation": "relinquishChannelAllocation",
       "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel allocations",
       "operation": "setChannelAllocations",
       "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel capacity",
       "operation": "updateChannelCapacity",
       "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity list.",
   "error": "Could not load. Names which read failed and leaves the capacity untouched.",
   "emptyFirstRun": "No capacity yet. Offers Create channel capacity (`createChannelCapacity`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on performanceId and the capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Last synced, with age"
  },
  "apis": [
   {
    "operationId": "listChannelCapacities",
    "contract": "catalogue",
    "purpose": "List capacity envelopes",
    "trigger": "onLoad"
   },
   {
    "operationId": "getChannelAllocations",
    "contract": "catalogue",
    "purpose": "Capacity allocated to each channel",
    "trigger": "onAction"
   },
   {
    "operationId": "createChannelCapacity",
    "contract": "catalogue",
    "purpose": "Create a capacity envelope",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "relinquishChannelAllocation",
    "contract": "catalogue",
    "purpose": "Return unsold channel allocation to the general pool",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "setChannelAllocations",
    "contract": "catalogue",
    "purpose": "Allocate envelope capacity across channels",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "updateChannelCapacity",
    "contract": "catalogue",
    "purpose": "Amend an envelope",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "channelCapacityId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `channelCapacityId`.",
   "preloaded": [
    "ChannelCapacity.id",
    "ChannelCapacity.performanceId",
    "ChannelCapacity.name",
    "ChannelCapacity.seatCategoryId",
    "ChannelCapacity.oversellAllowance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-033"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateChannelCapacity",
    "component": "modal",
    "trigger": "Create channel capacity",
    "body": "**Collects what `createChannelCapacity` sends before it is called.** Required: `performanceId`, `name`, `capacity`. Optional: `seatCategoryId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateEnvelopeRequest",
    "confirm": {
     "label": "Create channel capacity",
     "operation": "createChannelCapacity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "performanceId",
      "name",
      "capacity",
      "seatCategoryId"
     ]
    },
    "provenance": "contract catalogue.yaml POST /channel-capacities"
   },
   {
    "id": "formRelinquishChannelAllocation",
    "component": "modal",
    "trigger": "Release channel allocation",
    "body": "**Collects what `relinquishChannelAllocation` sends before it is called.** Required: `channels`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Release channel allocation",
     "operation": "relinquishChannelAllocation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "channels",
      "reason"
     ]
    },
    "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
   },
   {
    "id": "formSetChannelAllocations",
    "component": "modal",
    "trigger": "Save channel allocations",
    "body": "**Collects what `setChannelAllocations` sends before it is called.** Required: `allocations`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save channel allocations",
     "operation": "setChannelAllocations"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "allocations"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
   },
   {
    "id": "formUpdateChannelCapacity",
    "component": "modal",
    "trigger": "Save channel capacity",
    "body": "**Collects what `updateChannelCapacity` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacity`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save channel capacity",
     "operation": "updateChannelCapacity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "capacity"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-034",
  "name": "Walk-up sale",
  "module": "Operations",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/walk-up-sale",
   "component": "apps/venue-staff-app/src/routes/operations/WalkUpSaleDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-035",
    "EMP-036"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-034 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-034 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-034 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    },
    {
     "to": "EMP-036",
     "trigger": "Issue media",
     "provenance": "derived — EMP-036 declares entryState.params mediaCode, mediaId and EMP-034 holds none of them, so the edge carries nothing and EMP-036 opens cold"
    },
    {
     "to": "EMP-035",
     "trigger": "The guest taps a card on the device",
     "provenance": "flow F66 step 1→2",
     "carries": [
      "paymentId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createProduct, updateProduct. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Sell at the gate without a till.",
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
       "operation": "listProducts",
       "notes": "Sends `?venueId=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listProducts",
       "notes": "Sends `?kind=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "toggle",
       "label": "Is sellable",
       "operation": "listProducts",
       "notes": "Sends `?isSellable=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "dataTable",
       "label": "Every product",
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
      },
      {
       "kind": "dataTable",
       "label": "Every alternative code",
       "bindsTo": "AlternativeCode",
       "columns": [
        "AlternativeCode.code",
        "AlternativeCode.partnerId",
        "AlternativeCode.partnerName",
        "AlternativeCode.variantId",
        "AlternativeCode.note"
       ],
       "operation": "listAlternativeCodes",
       "provenance": "contract catalogue.yaml GET /products/{productId}/alternative-codes"
      },
      {
       "kind": "dataTable",
       "label": "Every refund",
       "bindsTo": "Refund",
       "columns": [
        "Refund.id",
        "Refund.orderId",
        "Refund.batchId",
        "Refund.fxRate",
        "Refund.taxReversalEntryId",
        "Refund.settleTo",
        "Refund.fxVariance",
        "Refund.amount",
        "Refund.appliedPercentage",
        "Refund.status",
        "Refund.reason",
        "Refund.requestedByPrincipalId"
       ],
       "operation": "listOrderRefunds",
       "provenance": "contract orders.yaml GET /orders/{orderId}/refunds"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every product variant",
       "bindsTo": "ProductVariant",
       "columns": [
        "ProductVariant.id",
        "ProductVariant.productId",
        "ProductVariant.sku",
        "ProductVariant.axisValues",
        "ProductVariant.name",
        "ProductVariant.barcode",
        "ProductVariant.isDefault",
        "ProductVariant.isActive"
       ],
       "operation": "listProductVariants",
       "provenance": "contract catalogue.yaml GET /products/{productId}/variants"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
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
       "label": "The selected product",
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
        "Product.onSaleTo",
        "Product.categoryId",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.isStockTracked"
       ],
       "operation": "getProduct",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      },
      {
       "kind": "detailPanel",
       "label": "The order statement",
       "bindsTo": "OrderStatement",
       "columns": [
        "OrderStatement.orderId",
        "OrderStatement.orderNumber",
        "OrderStatement.currency",
        "OrderStatement.currencyScale",
        "OrderStatement.entries",
        "OrderStatement.totalPaid",
        "OrderStatement.totalRefunded",
        "OrderStatement.currentBalance"
       ],
       "operation": "getOrderStatement",
       "provenance": "contract orders.yaml GET /orders/{orderId}/statement"
      },
      {
       "kind": "detailPanel",
       "label": "The order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create order",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply manual discount",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create refund",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange order lines",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold order",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify order",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint order",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule order",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve product by code",
       "operation": "resolveProductByCode",
       "provenance": "contract catalogue.yaml GET /products/resolve"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume order",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "secondaryButton",
       "label": "Save alternative codes",
       "operation": "setAlternativeCodes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save product attributes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition product lifecycle",
       "operation": "transitionProductLifecycle",
       "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
      },
      {
       "kind": "destructiveButton",
       "label": "Void order",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      },
      {
       "kind": "secondaryButton",
       "label": "Split order",
       "operation": "splitOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/split"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void order",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A walk-up sale this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is picked from the void reason list (guestChangedMind, enteredInError, itemUnavailable, qualityIssue, duplicate, other); **`note` is required when the reason is other**, refused 400 without it (decided 28 September, audit R125 (4), R222).",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   },
   {
    "id": "formSplitOrder",
    "component": "modal",
    "trigger": "Split order",
    "body": "**Collects what `splitOrder` sends before it is called.** Required: `groups`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Split order",
     "operation": "splitOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "groups"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/split"
   },
   {
    "id": "formCreateOrder",
    "component": "modal",
    "trigger": "Create order",
    "body": "**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateOrderRequest",
    "confirm": {
     "label": "Create order",
     "operation": "createOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "channel",
      "lines",
      "recordedAt",
      "shiftId",
      "subjectId",
      "guestLinkId",
      "catalogueBundleVersion"
     ]
    },
    "provenance": "contract orders.yaml POST /orders"
   },
   {
    "id": "formApplyManualDiscount",
    "component": "modal",
    "trigger": "Apply manual discount",
    "body": "**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ManualDiscountRequest",
    "confirm": {
     "label": "Apply manual discount",
     "operation": "applyManualDiscount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "lineId",
      "amount",
      "percentage",
      "reasonCode",
      "approverPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
   },
   {
    "id": "formCreateRefund",
    "component": "modal",
    "trigger": "Create refund",
    "body": "**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateRefundRequest",
    "confirm": {
     "label": "Create refund",
     "operation": "createRefund"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "amount",
      "reason",
      "recordedAt",
      "lineIds",
      "secondaryAuthorisation",
      "refundToOriginalTender",
      "alternateTender"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
   },
   {
    "id": "formExchangeOrderLines",
    "component": "modal",
    "trigger": "Exchange order lines",
    "body": "**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ExchangeOrderRequest",
    "confirm": {
     "label": "Exchange order lines",
     "operation": "exchangeOrderLines"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outgoingLineIds",
      "incomingLines",
      "recordedAt",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
   },
   {
    "id": "formHoldOrder",
    "component": "modal",
    "trigger": "Hold order",
    "body": "**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold order",
     "operation": "holdOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "label",
      "holdUntil"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
   },
   {
    "id": "formModifyOrder",
    "component": "modal",
    "trigger": "Modify order",
    "body": "**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ModifyOrderRequest",
    "confirm": {
     "label": "Modify order",
     "operation": "modifyOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "recordedAt",
      "addLines",
      "removeLineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
   },
   {
    "id": "formReprintOrder",
    "component": "modal",
    "trigger": "Reprint order",
    "body": "**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reprint order",
     "operation": "reprintOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "delivery",
      "recordedAt",
      "destination",
      "lineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
   },
   {
    "id": "formRescheduleOrder",
    "component": "modal",
    "trigger": "Reschedule order",
    "body": "**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reschedule order",
     "operation": "rescheduleOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetPerformanceId",
      "recordedAt",
      "lineIds",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
   },
   {
    "id": "formSetAlternativeCodes",
    "component": "modal",
    "trigger": "Save alternative codes",
    "body": "**Collects what `setAlternativeCodes` sends before it is called.** Required: `codes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save alternative codes",
     "operation": "setAlternativeCodes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "codes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
   },
   {
    "id": "formSetProductAttributes",
    "component": "modal",
    "trigger": "Save product attributes",
    "body": "**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save product attributes",
     "operation": "setProductAttributes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "axes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
   },
   {
    "id": "formTransitionProductLifecycle",
    "component": "modal",
    "trigger": "Transition product lifecycle",
    "body": "**Collects what `transitionProductLifecycle` sends before it is called.** Required: `transition`, `reason`. Optional: `effectiveAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transition product lifecycle",
     "operation": "transitionProductLifecycle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "transition",
      "reason",
      "effectiveAt"
     ]
    },
    "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
   }
  ],
  "states": {
   "loading": "The walk-up sale list.",
   "error": "Could not load. Names which read failed and leaves the walk-up sale untouched.",
   "emptyFirstRun": "No walk-up sale yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the walk-up sale are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Cash only offline.** Card completes nowhere the acquirer saw it"
  },
  "apis": [
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Create an order",
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
    "operationId": "applyManualDiscount",
    "contract": "orders",
    "purpose": "Apply a discount a cashier chose",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "createRefund",
    "contract": "orders",
    "purpose": "Refund an order, wholly or in part",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onAction"
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onAction"
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onAction"
   },
   {
    "operationId": "holdOrder",
    "contract": "orders",
    "purpose": "Park a sale and free the till",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listAlternativeCodes",
    "contract": "catalogue",
    "purpose": "External identifiers for a product",
    "trigger": "onAction"
   },
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onAction"
   },
   {
    "operationId": "modifyOrder",
    "contract": "orders",
    "purpose": "Add or remove lines on an existing order",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move an order to another performance",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "resolveProductByCode",
    "contract": "catalogue",
    "purpose": "Resolve a partner code to a product",
    "trigger": "onAction"
   },
   {
    "operationId": "resumeOrder",
    "contract": "orders",
    "purpose": "Bring a parked sale back to a till",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "setAlternativeCodes",
    "contract": "catalogue",
    "purpose": "Set external identifiers",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "setProductAttributes",
    "contract": "catalogue",
    "purpose": "Set the attribute axes for a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "transitionProductLifecycle",
    "contract": "catalogue",
    "purpose": "Move a product through its lifecycle",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void an order",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "splitOrder",
    "contract": "orders",
    "purpose": "Break one order into independent orders",
    "trigger": "onAction",
    "provenance": "wiring gap, 19 September 2026 — the screen showed the noun and could not act on it",
    "invalidates": [
     "getOrder"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "productId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error. **A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does.",
   "preloaded": [
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-034"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 22 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-025",
  "name": "Break management",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/break-management",
   "component": "apps/venue-staff-app/src/routes/operations/BreakManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003",
    "EMP-024"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-025 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-025 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-025 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: amendAttendance. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listAttendance` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Take a break without leaving a gate unstaffed.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "datePicker",
       "label": "Date",
       "operation": "listAttendance",
       "notes": "Sends `?date=` to `listAttendance`.",
       "provenance": "contract workforce.yaml GET /attendance"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listAttendance",
       "notes": "Sends `?principalId=` to `listAttendance`.",
       "provenance": "contract workforce.yaml GET /attendance"
      },
      {
       "kind": "toggle",
       "label": "Exceptions only",
       "operation": "listAttendance",
       "notes": "Sends `?exceptionsOnly=` to `listAttendance`.",
       "provenance": "contract workforce.yaml GET /attendance"
      },
      {
       "kind": "dataTable",
       "label": "Every attendance",
       "bindsTo": "AttendanceRecord",
       "columns": [
        "AttendanceRecord.id",
        "AttendanceRecord.principalId",
        "AttendanceRecord.assignmentId",
        "AttendanceRecord.venueId",
        "AttendanceRecord.kind",
        "AttendanceRecord.occurredAt",
        "AttendanceRecord.recordedAt",
        "AttendanceRecord.accessPointId",
        "AttendanceRecord.latitude",
        "AttendanceRecord.longitude",
        "AttendanceRecord.isAmended",
        "AttendanceRecord.amendedByPrincipalId"
       ],
       "operation": "listAttendance",
       "provenance": "contract workforce.yaml GET /attendance"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected attendance",
       "bindsTo": "AttendanceRecord",
       "columns": [
        "AttendanceRecord.id",
        "AttendanceRecord.principalId",
        "AttendanceRecord.assignmentId",
        "AttendanceRecord.venueId",
        "AttendanceRecord.kind",
        "AttendanceRecord.occurredAt",
        "AttendanceRecord.recordedAt",
        "AttendanceRecord.accessPointId",
        "AttendanceRecord.latitude",
        "AttendanceRecord.longitude",
        "AttendanceRecord.isAmended",
        "AttendanceRecord.amendedByPrincipalId",
        "AttendanceRecord.amendmentReason",
        "AttendanceRecord.originalOccurredAt",
        "AttendanceRecord.exception"
       ],
       "operation": "listAttendance",
       "provenance": "contract workforce.yaml GET /attendance"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Record attendance",
       "operation": "recordAttendance",
       "provenance": "contract workforce.yaml POST /attendance/clock"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The break list.",
   "error": "Could not load. Names which read failed and leaves the break untouched.",
   "emptyFirstRun": "No break yet. Offers Record attendance (`recordAttendance`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on date, principalId, exceptionsOnly and the break are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Queues locally"
  },
  "apis": [
   {
    "operationId": "recordAttendance",
    "contract": "workforce",
    "purpose": "Clock in, clock out, or take a break",
    "trigger": "onAction",
    "invalidates": [
     "listAttendance"
    ]
   },
   {
    "operationId": "listAttendance",
    "contract": "workforce",
    "purpose": "Who was here",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "recordId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `recordId`.",
   "preloaded": [
    "AttendanceRecord.id",
    "AttendanceRecord.principalId",
    "AttendanceRecord.assignmentId",
    "AttendanceRecord.venueId",
    "AttendanceRecord.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-025"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRecordAttendance",
    "component": "modal",
    "trigger": "Record attendance",
    "body": "**Collects what `recordAttendance` sends before it is called.** Required: `kind`, `occurredAt`. Optional: `assignmentId`, `accessPointId`, `latitude`, `longitude`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record attendance",
     "operation": "recordAttendance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "occurredAt",
      "assignmentId",
      "accessPointId",
      "latitude",
      "longitude"
     ]
    },
    "provenance": "contract workforce.yaml POST /attendance/clock"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-026",
  "name": "Incident report",
  "module": "Operations",
  "requiresModule": "maintenance",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/incident-report",
   "component": "apps/venue-staff-app/src/routes/operations/IncidentReportDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-004",
    "EMP-027"
   ],
   "inferred": false,
   "fromFlows": true,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-004",
     "trigger": "Technician picks up the work order",
     "provenance": "flow F12 step 1→2",
     "operation": "reportIncident"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-026 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-026 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-026 holds incidentId, so an edge into it carries them"
    },
    {
     "to": "EMP-027",
     "trigger": "A supervisor reads it and adds detail",
     "provenance": "flow F69 step 1→2",
     "operation": "reportIncident",
     "carries": [
      "incidentId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listIncidents` reads the population and `getIncident` reads one of them — list, select, act",
  "purpose": "Record what happened while it is fresh.",
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
   "loading": "The incident report list.",
   "error": "Could not load. Names which read failed and leaves the incident report untouched.",
   "emptyFirstRun": "No incident report yet. Offers Record authority notification (`recordAuthorityNotification`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on severity, status, isReportable and the incident report are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `INCIDENT_VIEW`, which `getIncident` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Queues locally with the highest sync priority"
  },
  "apis": [
   {
    "operationId": "reportIncident",
    "contract": "maintenance",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "Read an incident",
    "trigger": "onAction"
   },
   {
    "operationId": "listIncidents",
    "contract": "maintenance",
    "purpose": "List incidents",
    "trigger": "onLoad"
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-026"
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
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-027",
  "name": "Incident detail",
  "module": "Operations",
  "requiresModule": "maintenance",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/incident-detail",
   "component": "apps/venue-staff-app/src/routes/operations/IncidentDetailDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-050"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-026"
   ],
   "notes": "**Reached from EMP-026** — a detail is reached from the incident it details. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-027 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-027 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-027 holds incidentId, so an edge into it carries them"
    },
    {
     "to": "EMP-050",
     "trigger": "Where required, the authorities are notified",
     "provenance": "flow F69 step 2→3",
     "carries": [
      "incidentId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: reportIncident. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Removed 24 August**: recordAuthorityNotification. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listIncidents` reads the population and `getIncident` reads one of them — list, select, act",
  "purpose": "Follow up on something already reported.",
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
       "label": "Save incident",
       "operation": "updateIncident",
       "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The incident list.",
   "error": "Could not load. Names which read failed and leaves the incident untouched.",
   "emptyFirstRun": "No incident yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on severity, status, isReportable and the incident are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `INCIDENT_VIEW`, which `getIncident` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached; updates queue"
  },
  "apis": [
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "updateIncident",
    "contract": "maintenance",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "listIncidents",
    "contract": "maintenance",
    "purpose": "List incidents",
    "trigger": "onLoad"
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-027"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-028",
  "name": "Lost & found",
  "module": "Operations",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/lost-found",
   "component": "apps/venue-staff-app/src/routes/operations/LostFoundDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003",
    "EMP-030"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-028 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-028 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-028 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listCases` reads the population and `getCase` reads one of them — list, select, act",
  "purpose": "Log something handed in.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listCases",
       "notes": "Sends `?status=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Assigned to principal id",
       "operation": "listCases",
       "notes": "Sends `?assignedToPrincipalId=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "toggle",
       "label": "Breached sla",
       "operation": "listCases",
       "notes": "Sends `?breachedSla=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Priority",
       "operation": "listCases",
       "notes": "Sends `?priority=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "dataTable",
       "label": "Every case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.kind",
        "Case.channel",
        "Case.recordedAt",
        "Case.syncedAt",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "detailPanel",
       "label": "The case",
       "bindsTo": "CaseDetail",
       "columns": [
        "CaseDetail.id",
        "CaseDetail.caseNumber",
        "CaseDetail.subjectId",
        "CaseDetail.guestName",
        "CaseDetail.subject",
        "CaseDetail.kind",
        "CaseDetail.channel",
        "CaseDetail.recordedAt",
        "CaseDetail.syncedAt",
        "CaseDetail.categoryId",
        "CaseDetail.status",
        "CaseDetail.priority",
        "CaseDetail.assignedToPrincipalId",
        "CaseDetail.venueId",
        "CaseDetail.relatedOrderId",
        "CaseDetail.slaDueAt"
       ],
       "operation": "getCase",
       "provenance": "contract marketing-crm.yaml GET /cases/{caseId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create case",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Add case message",
       "operation": "addCaseMessage",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate case",
       "operation": "escalateCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen case",
       "operation": "reopenCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Save case",
       "operation": "updateCase",
       "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lost found list.",
   "error": "Could not load. Names which read failed and leaves the lost found untouched.",
   "emptyFirstRun": "No lost found yet. Offers Create case (`createCase`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the lost found are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `CASE_VIEW`, which `getCase` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Queues locally and syncs on reconnect. The pending count is always current because it is local"
  },
  "apis": [
   {
    "operationId": "createCase",
    "contract": "marketing-crm",
    "purpose": "Raise a service case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "addCaseMessage",
    "contract": "marketing-crm",
    "purpose": "Add a message or internal note",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "escalateCase",
    "contract": "marketing-crm",
    "purpose": "Escalate a case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "getCase",
    "contract": "marketing-crm",
    "purpose": "Read a case with its thread",
    "trigger": "onAction"
   },
   {
    "operationId": "listCases",
    "contract": "marketing-crm",
    "purpose": "List service cases",
    "trigger": "onLoad"
   },
   {
    "operationId": "reopenCase",
    "contract": "marketing-crm",
    "purpose": "Reopen a resolved case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "updateCase",
    "contract": "marketing-crm",
    "purpose": "Assign, reprioritise or resolve a case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "caseId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `caseId`.",
   "preloaded": [
    "Case.id",
    "Case.caseNumber",
    "Case.subjectId",
    "Case.guestName",
    "Case.subject"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-028"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateCase",
    "component": "modal",
    "trigger": "Create case",
    "body": "**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCaseRequest",
    "confirm": {
     "label": "Create case",
     "operation": "createCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subject",
      "description",
      "channel",
      "recordedAt",
      "subjectId",
      "categoryId",
      "priority",
      "kind",
      "venueId",
      "relatedOrderId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases"
   },
   {
    "id": "formAddCaseMessage",
    "component": "modal",
    "trigger": "Add case message",
    "body": "**Collects what `addCaseMessage` sends before it is called.** Required: `id`, `body`, `isInternal`, `recordedAt`. Optional: `channel`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add case message",
     "operation": "addCaseMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "body",
      "isInternal",
      "recordedAt",
      "channel",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
   },
   {
    "id": "formEscalateCase",
    "component": "modal",
    "trigger": "Escalate case",
    "body": "**Collects what `escalateCase` sends before it is called.** Required: `reason`. Optional: `assignToPrincipalId`, `newPriority`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Escalate case",
     "operation": "escalateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "assignToPrincipalId",
      "newPriority"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
   },
   {
    "id": "formReopenCase",
    "component": "modal",
    "trigger": "Reopen case",
    "body": "**Collects what `reopenCase` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen case",
     "operation": "reopenCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
   },
   {
    "id": "formUpdateCase",
    "component": "modal",
    "trigger": "Save case",
    "body": "**Collects what `updateCase` sends before it is called.** Nothing in the body is required. Optional: `status`, `priority`, `assignedToPrincipalId`, `categoryId`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save case",
     "operation": "updateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "priority",
      "assignedToPrincipalId",
      "categoryId",
      "resolutionNote"
     ]
    },
    "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-029",
  "name": "Guest assistance",
  "module": "Operations",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/guest-assistance",
   "component": "apps/venue-staff-app/src/routes/operations/GuestAssistanceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-030"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-030",
     "trigger": "They show the guest where to go",
     "provenance": "flow F70 step 1→2"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-029 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-029 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-029 holds incidentId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listCases` reads the population and `getCase` reads one of them — list, select, act",
  "purpose": "Help a guest without leaving the floor.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listCases",
       "notes": "Sends `?status=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Assigned to principal id",
       "operation": "listCases",
       "notes": "Sends `?assignedToPrincipalId=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "toggle",
       "label": "Breached sla",
       "operation": "listCases",
       "notes": "Sends `?breachedSla=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Priority",
       "operation": "listCases",
       "notes": "Sends `?priority=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "dataTable",
       "label": "Every case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
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
       "label": "The selected case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.kind",
        "Case.channel",
        "Case.recordedAt",
        "Case.syncedAt",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
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
      },
      {
       "kind": "detailPanel",
       "label": "The case",
       "bindsTo": "CaseDetail",
       "columns": [
        "CaseDetail.id",
        "CaseDetail.caseNumber",
        "CaseDetail.subjectId",
        "CaseDetail.guestName",
        "CaseDetail.subject",
        "CaseDetail.kind",
        "CaseDetail.channel",
        "CaseDetail.recordedAt",
        "CaseDetail.syncedAt",
        "CaseDetail.categoryId",
        "CaseDetail.status",
        "CaseDetail.priority",
        "CaseDetail.assignedToPrincipalId",
        "CaseDetail.venueId",
        "CaseDetail.relatedOrderId",
        "CaseDetail.slaDueAt"
       ],
       "operation": "getCase",
       "provenance": "contract marketing-crm.yaml GET /cases/{caseId}"
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
       "label": "Create case",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Add case message",
       "operation": "addCaseMessage",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate case",
       "operation": "escalateCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
      },
      {
       "kind": "secondaryButton",
       "label": "Record authority notification",
       "operation": "recordAuthorityNotification",
       "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen case",
       "operation": "reopenCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Save case",
       "operation": "updateCase",
       "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
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
   "loading": "The guest assistance list.",
   "error": "Could not load. Names which read failed and leaves the guest assistance untouched.",
   "emptyFirstRun": "No guest assistance yet. Offers Create case (`createCase`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the guest assistance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `CASE_VIEW`, which `getCase` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Queues locally and syncs on reconnect. The pending count is always current because it is local"
  },
  "apis": [
   {
    "operationId": "reportIncident",
    "contract": "maintenance",
    "purpose": "Report an incident",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "createCase",
    "contract": "marketing-crm",
    "purpose": "Raise a service case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "addCaseMessage",
    "contract": "marketing-crm",
    "purpose": "Add a message or internal note",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "escalateCase",
    "contract": "marketing-crm",
    "purpose": "Escalate a case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "getCase",
    "contract": "marketing-crm",
    "purpose": "Read a case with its thread",
    "trigger": "onAction"
   },
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "Read an incident",
    "trigger": "onAction"
   },
   {
    "operationId": "listCases",
    "contract": "marketing-crm",
    "purpose": "List service cases",
    "trigger": "onLoad"
   },
   {
    "operationId": "listIncidents",
    "contract": "maintenance",
    "purpose": "List incidents",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordAuthorityNotification",
    "contract": "maintenance",
    "purpose": "Record notification to an external authority",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "reopenCase",
    "contract": "marketing-crm",
    "purpose": "Reopen a resolved case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "updateCase",
    "contract": "marketing-crm",
    "purpose": "Assign, reprioritise or resolve a case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "updateIncident",
    "contract": "maintenance",
    "purpose": "Investigate, escalate or close an incident",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "caseId",
     "from": "deepLink"
    },
    {
     "name": "incidentId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `caseId`, `incidentId`.",
   "preloaded": [
    "Case.id",
    "Case.caseNumber",
    "Case.subjectId",
    "Case.guestName",
    "Case.subject"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-029"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "id": "formCreateCase",
    "component": "modal",
    "trigger": "Create case",
    "body": "**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCaseRequest",
    "confirm": {
     "label": "Create case",
     "operation": "createCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subject",
      "description",
      "channel",
      "recordedAt",
      "subjectId",
      "categoryId",
      "priority",
      "kind",
      "venueId",
      "relatedOrderId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases"
   },
   {
    "id": "formAddCaseMessage",
    "component": "modal",
    "trigger": "Add case message",
    "body": "**Collects what `addCaseMessage` sends before it is called.** Required: `id`, `body`, `isInternal`, `recordedAt`. Optional: `channel`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add case message",
     "operation": "addCaseMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "body",
      "isInternal",
      "recordedAt",
      "channel",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
   },
   {
    "id": "formEscalateCase",
    "component": "modal",
    "trigger": "Escalate case",
    "body": "**Collects what `escalateCase` sends before it is called.** Required: `reason`. Optional: `assignToPrincipalId`, `newPriority`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Escalate case",
     "operation": "escalateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "assignToPrincipalId",
      "newPriority"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
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
    "id": "formReopenCase",
    "component": "modal",
    "trigger": "Reopen case",
    "body": "**Collects what `reopenCase` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen case",
     "operation": "reopenCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
   },
   {
    "id": "formUpdateCase",
    "component": "modal",
    "trigger": "Save case",
    "body": "**Collects what `updateCase` sends before it is called.** Nothing in the body is required. Optional: `status`, `priority`, `assignedToPrincipalId`, `categoryId`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save case",
     "operation": "updateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "priority",
      "assignedToPrincipalId",
      "categoryId",
      "resolutionNote"
     ]
    },
    "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
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
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-030",
  "name": "Venue map",
  "module": "Operations",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/venue-map",
   "component": "apps/venue-staff-app/src/routes/operations/VenueMapDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-028"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003",
    "EMP-029"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-028",
     "trigger": "A lost item is logged",
     "provenance": "flow F70 step 2→3"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-030 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-030 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-030 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Wired to the venue map 18 August (CF-123).** The published map with live state on it: 3.2.64 asks for access-control statistics drawn on a graphical map, and the same view carries wait times and closed rides. **The map changes monthly and the state changes every few seconds**, so they are separate calls. **Removed 24 August**: getRefundPolicy, setRefundPolicy. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Drawn 26 August** — `Seat Board 4.dc.html` frame `seat-4c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "comfortable",
  "boardFrames": [
   "Seat Board 4.dc.html#seat-4c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads the population and `getVenueMap` reads one of them — list, select, act",
  "purpose": "Find a gate, an exit or a colleague.",
  "gaps": [
   {
    "operation": "getVenueMapLive",
    "why": "**1 declared operation reach no component on this screen**: getVenueMapLive. Either the screen is missing what calls them, or the declaration is residue.",
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
       "kind": "toggle",
       "label": "Open now",
       "operation": "listDiningOutlets",
       "notes": "Sends `?openNow=` to `listDiningOutlets`.",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      },
      {
       "kind": "textField",
       "label": "Ordering method",
       "operation": "listDiningOutlets",
       "notes": "Sends `?orderingMethod=` to `listDiningOutlets`.",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      },
      {
       "kind": "dataTable",
       "label": "Every dining outlet",
       "bindsTo": "DiningOutlet",
       "columns": [
        "DiningOutlet.outletId",
        "DiningOutlet.name",
        "DiningOutlet.kind",
        "DiningOutlet.zone",
        "DiningOutlet.cuisine",
        "DiningOutlet.isOpenNow",
        "DiningOutlet.opensAt",
        "DiningOutlet.closesAt",
        "DiningOutlet.orderingMethod",
        "DiningOutlet.estimatedWaitMinutes",
        "DiningOutlet.imageAssetRef",
        "DiningOutlet.menuId"
       ],
       "operation": "listDiningOutlets",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      },
      {
       "kind": "dataTable",
       "label": "Every delivery location",
       "bindsTo": "DeliveryLocation",
       "columns": [
        "DeliveryLocation.id",
        "DeliveryLocation.venueId",
        "DeliveryLocation.kind",
        "DeliveryLocation.label",
        "DeliveryLocation.zone",
        "DeliveryLocation.tableId",
        "DeliveryLocation.seatId",
        "DeliveryLocation.servingOutletIds",
        "DeliveryLocation.isServiceable",
        "DeliveryLocation.unserviceableReason",
        "DeliveryLocation.walkTimeMinutes"
       ],
       "operation": "listDeliveryLocations",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/delivery-locations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dining outlet",
       "bindsTo": "DiningOutlet",
       "columns": [
        "DiningOutlet.outletId",
        "DiningOutlet.name",
        "DiningOutlet.kind",
        "DiningOutlet.zone",
        "DiningOutlet.cuisine",
        "DiningOutlet.isOpenNow",
        "DiningOutlet.opensAt",
        "DiningOutlet.closesAt",
        "DiningOutlet.orderingMethod",
        "DiningOutlet.estimatedWaitMinutes",
        "DiningOutlet.imageAssetRef",
        "DiningOutlet.menuId"
       ],
       "operation": "listDiningOutlets",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      },
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue map list.",
   "error": "Could not load. Names which read failed and leaves the venue map untouched.",
   "emptyFirstRun": "No venue map yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on openNow, orderingMethod and the venue map are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `VENUE_MAP_VIEW`, which `getVenueMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached map. **The zone list always works** because it is text"
  },
  "apis": [
   {
    "operationId": "listDiningOutlets",
    "contract": "fnb",
    "purpose": "Where a guest can eat, right now",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDeliveryLocations",
    "contract": "fnb",
    "purpose": "Where an order can be delivered",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVenueMap",
    "contract": "venue-map",
    "purpose": "A map with its points and paths",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVenueMapLive",
    "contract": "venue-map",
    "purpose": "The map with live operational state on it",
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
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mapId`.",
   "preloaded": [
    "DiningOutlet.outletId",
    "DiningOutlet.name",
    "DiningOutlet.kind",
    "DiningOutlet.zone",
    "DiningOutlet.cuisine"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-030",
   "derivedFrom": "wireframes/reference/Seat Board 4.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
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
 "addCaseMessage": {
  "method": "POST",
  "path": "/cases/{caseId}/messages",
  "contract": "marketing-crm",
  "summary": "Add a message or internal note",
  "permission": "CASE_MANAGE",
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
  "responds": "CaseMessage"
 },
 "applyManualDiscount": {
  "method": "POST",
  "path": "/orders/{orderId}/discounts",
  "contract": "orders",
  "summary": "Apply a discount a cashier chose",
  "permission": "ORDER_DISCOUNT",
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
  "requestBody": "ManualDiscountRequest",
  "responds": "Order"
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
 "createCase": {
  "method": "POST",
  "path": "/cases",
  "contract": "marketing-crm",
  "summary": "Raise a service case",
  "permission": "CASE_MANAGE",
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
  "requestBody": "CreateCaseRequest",
  "responds": "Case"
 },
 "createChannelCapacity": {
  "method": "POST",
  "path": "/channel-capacities",
  "contract": "catalogue",
  "summary": "Create a channel capacity",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "CreateEnvelopeRequest",
  "responds": "ChannelCapacity"
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
 "createRefund": {
  "method": "POST",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "Refund an order, wholly or in part",
  "permission": "ORDER_REFUND",
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
  "requestBody": "CreateRefundRequest",
  "responds": null
 },
 "escalateCase": {
  "method": "POST",
  "path": "/cases/{caseId}/escalate",
  "contract": "marketing-crm",
  "summary": "Escalate a case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
 },
 "exchangeOrderLines": {
  "method": "POST",
  "path": "/orders/{orderId}/exchanges",
  "contract": "orders",
  "summary": "Exchange lines for different products or dates",
  "permission": "ORDER_EXCHANGE",
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
  "requestBody": "ExchangeOrderRequest",
  "responds": "OrderExchangeResult"
 },
 "getCase": {
  "method": "GET",
  "path": "/cases/{caseId}",
  "contract": "marketing-crm",
  "summary": "Read a case with its thread",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CaseDetail"
 },
 "getChannelAllocations": {
  "method": "GET",
  "path": "/channel-capacities/{channelCapacityId}/channel-allocations",
  "contract": "catalogue",
  "summary": "Capacity allocated to each channel",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelAllocationSet"
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
 "getOrder": {
  "method": "GET",
  "path": "/orders/{orderId}",
  "contract": "orders",
  "summary": "Read an order",
  "permission": "ORDER_VIEW",
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
  "responds": "Order"
 },
 "getOrderStatement": {
  "method": "GET",
  "path": "/orders/{orderId}/statement",
  "contract": "orders",
  "summary": "Full financial history of an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderStatement"
 },
 "getProduct": {
  "method": "GET",
  "path": "/products/{productId}",
  "contract": "catalogue",
  "summary": "Read a product",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Product"
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
 "getVenueMapLive": {
  "method": "GET",
  "path": "/venue-maps/{mapId}/live",
  "contract": "venue-map",
  "summary": "The map with live operational state on it",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
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
 "holdOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/hold",
  "contract": "orders",
  "summary": "Park a sale and free the till",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Order"
 },
 "listAlternativeCodes": {
  "method": "GET",
  "path": "/products/{productId}/alternative-codes",
  "contract": "catalogue",
  "summary": "External identifiers for a product",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AlternativeCode"
 },
 "listAttendance": {
  "method": "GET",
  "path": "/attendance",
  "contract": "workforce",
  "summary": "Who was here",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "date",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "exceptionsOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AttendanceRecord"
 },
 "listCases": {
  "method": "GET",
  "path": "/cases",
  "contract": "marketing-crm",
  "summary": "List service cases",
  "permission": "CASE_VIEW",
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
    "name": "assignedToPrincipalId",
    "in": "query",
    "required": null
   },
   {
    "name": "breachedSla",
    "in": "query",
    "required": null
   },
   {
    "name": "priority",
    "in": "query",
    "required": null
   },
   {
    "name": "membershipId",
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
 "listChannelCapacities": {
  "method": "GET",
  "path": "/channel-capacities",
  "contract": "catalogue",
  "summary": "List channel capacities",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
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
 "listDeliveryLocations": {
  "method": "GET",
  "path": "/venues/{venueId}/delivery-locations",
  "contract": "fnb",
  "summary": "Where an order can be delivered",
  "permission": null,
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
    "name": "servingOutletId",
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
 "listDiningOutlets": {
  "method": "GET",
  "path": "/venues/{venueId}/dining",
  "contract": "fnb",
  "summary": "Where a guest can eat, right now",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "openNow",
    "in": "query",
    "required": null
   },
   {
    "name": "orderingMethod",
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
 "listOrderRefunds": {
  "method": "GET",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "List refunds against an order",
  "permission": "ORDER_VIEW",
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
 "listOrders": {
  "method": "GET",
  "path": "/orders",
  "contract": "orders",
  "summary": "List orders",
  "permission": "ORDER_VIEW",
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
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "createdTo",
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
 "listProductVariants": {
  "method": "GET",
  "path": "/products/{productId}/variants",
  "contract": "catalogue",
  "summary": "List generated variants",
  "permission": "PRODUCT_VIEW",
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
 "modifyOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/modify",
  "contract": "orders",
  "summary": "Add or remove lines on an existing order",
  "permission": "ORDER_MODIFY",
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
  "requestBody": "ModifyOrderRequest",
  "responds": "OrderModificationResult"
 },
 "recordAttendance": {
  "method": "POST",
  "path": "/attendance/clock",
  "contract": "workforce",
  "summary": "Clock in, clock out, or take a break",
  "permission": "ATTENDANCE_RECORD",
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
  "responds": "AttendanceRecord"
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
 "relinquishChannelAllocation": {
  "method": "POST",
  "path": "/channel-capacities/{channelCapacityId}/channel-allocations/release",
  "contract": "catalogue",
  "summary": "Return unsold channel allocation to the general pool",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "ChannelAllocationSet"
 },
 "reopenCase": {
  "method": "POST",
  "path": "/cases/{caseId}/reopen",
  "contract": "marketing-crm",
  "summary": "Reopen a resolved case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
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
 "reprintOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reprints",
  "contract": "orders",
  "summary": "Reprint or resend tickets",
  "permission": "ORDER_REPRINT",
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
 "requestSuggestion": {
  "method": "POST",
  "path": "/ai/suggestions",
  "contract": "ai",
  "summary": "Ask for an answer, however it is currently produced",
  "permission": "AI_USE",
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
  "responds": "Suggestion"
 },
 "rescheduleOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reschedule",
  "contract": "orders",
  "summary": "Move an order to another performance",
  "permission": "ORDER_RESCHEDULE",
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
  "responds": "OrderExchangeResult"
 },
 "resolveProductByCode": {
  "method": "GET",
  "path": "/products/resolve",
  "contract": "catalogue",
  "summary": "Resolve a partner code to a product",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "code",
    "in": "query",
    "required": true
   },
   {
    "name": "partnerId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ProductVariant"
 },
 "resumeOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/resume",
  "contract": "orders",
  "summary": "Bring a parked sale back to a till",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OrderResumeResult"
 },
 "setAlternativeCodes": {
  "method": "PUT",
  "path": "/products/{productId}/alternative-codes",
  "contract": "catalogue",
  "summary": "Set external identifiers",
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
  "responds": "AlternativeCode"
 },
 "setChannelAllocations": {
  "method": "PUT",
  "path": "/channel-capacities/{channelCapacityId}/channel-allocations",
  "contract": "catalogue",
  "summary": "Allocate a channel capacity across sales channels",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "ChannelAllocationSet"
 },
 "setProductAttributes": {
  "method": "PUT",
  "path": "/products/{productId}/attributes",
  "contract": "catalogue",
  "summary": "Set the attribute axes for a product",
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
  "responds": null
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
 "splitOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/split",
  "contract": "orders",
  "summary": "Break one order into independent orders",
  "permission": "ORDER_MODIFY",
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
 "transitionProductLifecycle": {
  "method": "POST",
  "path": "/products/{productId}/lifecycle",
  "contract": "catalogue",
  "summary": "Move a product through its lifecycle",
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
  "responds": "Product"
 },
 "updateCase": {
  "method": "PATCH",
  "path": "/cases/{caseId}",
  "contract": "marketing-crm",
  "summary": "Assign, reprioritise or resolve a case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
 },
 "updateChannelCapacity": {
  "method": "PATCH",
  "path": "/channel-capacities/{channelCapacityId}",
  "contract": "catalogue",
  "summary": "Amend a channel capacity",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "ChannelCapacity"
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
 "voidOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/voids",
  "contract": "orders",
  "summary": "Void an order",
  "permission": "ORDER_VOID",
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
  "responds": "Order"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiMaturity": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded as jsonb on ai.suggestion and ai.forecast_version",
  "description": "**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.",
  "required": [
   "stage",
   "basedOn"
  ],
  "properties": {
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ],
    "description": "`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."
   },
   "basedOn": {
    "type": "string",
    "description": "The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "source"
     ],
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "venueSettings",
        "startingPattern",
        "calendar",
        "weather",
        "bookingsOnHand",
        "ownHistory",
        "importedHistory",
        "configuration",
        "trainedModel"
       ]
      },
      "detail": {
       "type": "string",
       "nullable": true,
       "description": "e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."
      },
      "observations": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ownDataShare": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."
   },
   "limitedHistory": {
    "type": "boolean"
   },
   "nextStage": {
    "type": "object",
    "nullable": true,
    "description": "What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.",
    "properties": {
     "stage": {
      "type": "string",
      "enum": [
       "learning",
       "established",
       "learned"
      ]
     },
     "needs": {
      "type": "string"
     },
     "expectedBy": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   }
  }
 },
 "AlternativeCode": {
  "x-ticvai-persistence": "catalogue.alternative_code",
  "type": "object",
  "required": [
   "code",
   "partnerId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 128
   },
   "partnerId": {
    "type": "string",
    "format": "uuid"
   },
   "partnerName": {
    "type": "string"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "note": {
    "type": "string",
    "maxLength": 200
   }
  }
 },
 "AttendanceAmendment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.attendance_amendment",
  "description": "One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n",
  "required": [
   "id",
   "attendanceRecordId",
   "amendedByPrincipalId",
   "amendedAt",
   "occurredAtBefore",
   "occurredAtAfter",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "attendanceRecordId": {
    "type": "string",
    "format": "uuid"
   },
   "amendedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "amendedAt": {
    "type": "string",
    "format": "date-time"
   },
   "occurredAtBefore": {
    "type": "string",
    "format": "date-time",
    "description": "The record's time before this correction."
   },
   "occurredAtAfter": {
    "type": "string",
    "format": "date-time",
    "description": "The time this correction set (`correctedAt` on the request)."
   },
   "reason": {
    "type": "string",
    "maxLength": 300
   }
  }
 },
 "AttendanceRecord": {
  "type": "object",
  "x-ticvai-persistence": "workforce.attendance",
  "required": [
   "id",
   "principalId",
   "kind",
   "occurredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "assignmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "clockIn",
     "clockOut",
     "breakStart",
     "breakEnd"
    ]
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time — when it happened."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "latitude": {
    "type": "number",
    "nullable": true
   },
   "longitude": {
    "type": "number",
    "nullable": true
   },
   "isAmended": {
    "type": "boolean",
    "readOnly": true
   },
   "amendedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Who made the latest amendment. The full history is `amendments` (audit R129 (7))."
   },
   "amendmentReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The latest amendment's reason. The full history is `amendments` (audit R129 (7))."
   },
   "originalOccurredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"
   },
   "amendments": {
    "type": "array",
    "readOnly": true,
    "description": "**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n",
    "items": {
     "$ref": "#/components/schemas/AttendanceAmendment"
    }
   },
   "exception": {
    "type": "string",
    "nullable": true,
    "enum": [
     "late",
     "earlyLeave",
     "missingClockOut",
     "noShow",
     "outOfGeofence",
     "unscheduled"
    ],
    "description": "Computed against the rota. Null where the record matches what was expected."
   }
  }
 },
 "Case": {
  "x-ticvai-persistence": "marketing.case",
  "x-ticvai-retired-columns": [
   "guest_name",
   "subject",
   "is_sla_breached"
  ],
  "type": "object",
  "required": [
   "id",
   "caseNumber",
   "subject",
   "status",
   "priority",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."
   },
   "caseNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"
   },
   "subject": {
    "type": "string",
    "x-ticvai-column": "title",
    "description": "**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CaseKind"
     }
    ],
    "nullable": true,
    "description": "What the guest said it was about, where the guest raised it."
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "description": "How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time the case was raised — the start of the SLA clock."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the case arrived. Equal to `recordedAt` for a case raised online."
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"
   },
   "status": {
    "$ref": "#/components/schemas/CaseStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "relatedOrderId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isSlaBreached": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"
   },
   "slaPausedSeconds": {
    "type": "integer",
    "description": "Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"
   },
   "escalationCount": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CaseDetail": {
  "x-ticvai-persistence": "marketing.case",
  "allOf": [
   {
    "$ref": "#/components/schemas/Case"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string"
     },
     "resolutionNote": {
      "type": "string",
      "nullable": true
     },
     "messages": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CaseMessage"
      }
     }
    }
   }
  ]
 },
 "CaseKind": {
  "type": "string",
  "description": "**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n",
  "enum": [
   "lostProperty",
   "complaint",
   "question",
   "accessibility",
   "refundRequest",
   "other"
  ]
 },
 "CaseMessage": {
  "x-ticvai-persistence": "marketing.case_message",
  "type": "object",
  "required": [
   "id",
   "body",
   "isInternal",
   "authorKind",
   "recordedAt"
  ],
  "properties": {
   "resolution": {
    "type": "string",
    "description": "**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"
   },
   "id": {
    "type": "string"
   },
   "body": {
    "type": "string"
   },
   "isInternal": {
    "type": "boolean"
   },
   "authorKind": {
    "type": "string",
    "enum": [
     "agent",
     "guest",
     "system",
     "ai"
    ]
   },
   "authorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time — `addCaseMessage` is offline-capable."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the message arrived."
   }
  }
 },
 "CasePriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent"
  ]
 },
 "CaseStatus": {
  "type": "string",
  "enum": [
   "open",
   "inProgress",
   "awaitingGuest",
   "escalated",
   "resolved",
   "closed"
  ]
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
 "ChannelAllocation": {
  "x-ticvai-persistence": "catalogue.channel_allocation",
  "type": "object",
  "required": [
   "channel",
   "allocatedUnits"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "allocatedUnits": {
    "type": "integer",
    "minimum": 0
   },
   "soldUnits": {
    "type": "integer",
    "readOnly": true
   },
   "leasedUnits": {
    "type": "integer",
    "readOnly": true,
    "description": "Held by terminals on this channel but not yet sold."
   },
   "remainingUnits": {
    "type": "integer",
    "readOnly": true
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it.\n"
   },
   "salesChannelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3)."
   },
   "allocationType": {
    "type": "string",
    "enum": [
     "sharedPool",
     "dedicated",
     "percentage",
     "dynamic"
    ],
    "default": "dedicated",
    "description": "How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row."
   },
   "minimumUnits": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "maximumUnits": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "replenishmentRule": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`."
   },
   "waitlistBehavior": {
    "type": "string",
    "enum": [
     "none",
     "joinWaitlist",
     "notifyOnRelease"
    ],
    "default": "none"
   },
   "releaseThresholdUnits": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "releaseHoursBeforeEvent": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "description": "Alternative to `releaseAt`, relative to the performance start."
   },
   "contractualUnits": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "description": "Units a partner agreement guarantees; rebalancing never goes below it."
   },
   "minimumGuaranteedUnits": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "isFrozen": {
    "type": "boolean",
    "default": false,
    "description": "Excluded from rebalancing."
   }
  }
 },
 "ChannelAllocationSet": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "channelCapacityId",
   "capacity",
   "allocations",
   "generalPoolUnits"
  ],
  "properties": {
   "channelCapacityId": {
    "type": "string",
    "format": "uuid"
   },
   "capacity": {
    "type": "integer"
   },
   "allocations": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ChannelAllocation"
    }
   },
   "generalPoolUnits": {
    "type": "integer",
    "description": "Unallocated remainder. Any channel may draw from it once its own allocation is exhausted.\n"
   },
   "totalSold": {
    "type": "integer"
   },
   "totalRemaining": {
    "type": "integer"
   }
  }
 },
 "ChannelCapacity": {
  "x-ticvai-persistence": "catalogue.channel_capacity",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "capacity",
   "sold",
   "leased",
   "remaining",
   "isSeated"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "seatCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "oversellAllowance": {
    "type": "integer",
    "default": 0,
    "description": "BL-046, 1.3.13. **The guard existed in one direction** — an envelope could be raised freely and refused reduction below what had sold.\n**Free events oversell deliberately because no-show rates are known.** An allowance on the envelope rather than an admission policy, because **the gate must still refuse when actual capacity is reached** — overselling is a sales decision and admission is a safety one, and they must not share a number.\n"
   },
   "oversellBasis": {
    "type": "string",
    "nullable": true,
    "enum": [
     "fixedCount",
     "historicNoShowRate",
     "percentage"
    ]
   },
   "capacity": {
    "type": "integer",
    "minimum": 0
   },
   "sold": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Units sold. **Maintained on write** (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by consumption a workstation reports on `renewInventoryHold` or `relinquishInventoryHold`, lowered when a refund or cancellation returns the units. Always `capacity + oversellAllowance = sold + leased + remaining`.\n"
   },
   "leased": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023)."
   },
   "remaining": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "What can still be held. **Decremented at the hold with a guarded statement** (`remaining >= n`) under the row lock, never at the sale, so two buyers cannot both take the last unit (SD-023, 29 September).\n"
   },
   "hasChannelAllocations": {
    "type": "boolean",
    "description": "True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity.\n"
   },
   "isSeated": {
    "type": "boolean",
    "description": "Seated envelopes cannot be leased and are blocked offline. A seat map is not a count.\n"
   }
  }
 },
 "CreateCaseRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "subject",
   "description",
   "channel",
   "recordedAt"
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
   "subject": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 10000
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"
   },
   "priority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CasePriority"
     }
    ],
    "default": "normal"
   },
   "kind": {
    "$ref": "#/components/schemas/CaseKind"
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "relatedOrderId": {
    "type": "string"
   },
   "attachmentRefs": {
    "type": "array",
    "description": "Stored on the opening `CaseMessage`, not on the case.",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time the case was raised. The server stamps `Case.syncedAt` on arrival."
   }
  }
 },
 "CreateEnvelopeRequest": {
  "type": "object",
  "description": "The body of `createChannelCapacity`. **Named before the 26 August rename** (envelope to `ChannelCapacity`); the name stays because generated code is keyed on it.",
  "required": [
   "performanceId",
   "name",
   "capacity"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "seatCategoryId": {
    "type": "string",
    "format": "uuid"
   },
   "capacity": {
    "type": "integer",
    "minimum": 0
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
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "eligibilityDeclaration": {
    "type": "array",
    "nullable": true,
    "x-ticvai-note": "One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n",
    "items": {
     "type": "object",
     "properties": {
      "ageBand": {
       "type": "string",
       "enum": [
        "infant",
        "child",
        "junior",
        "adult",
        "senior"
       ],
       "description": "Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."
      },
      "ageYears": {
       "type": "integer",
       "nullable": true
      },
      "heightBandIndex": {
       "type": "integer",
       "nullable": true
      },
      "confidentSwimmer": {
       "type": "boolean",
       "nullable": true,
       "description": "**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"
      },
      "guardianSigned": {
       "type": "boolean"
      }
     }
    },
    "description": "What was declared for each guest on this line, kept as the record staff check at the gate."
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
    "additionalProperties": true,
    "description": "**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"
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
    "format": "uuid",
    "description": "Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string",
    "format": "uuid"
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
 "CreateRefundRequest": {
  "type": "object",
  "required": [
   "id",
   "amount",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Omit to refund the whole order."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "secondaryAuthorisation": {
    "type": "object",
    "description": "Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n",
    "required": [
     "principalId",
     "credential"
    ],
    "properties": {
     "principalId": {
      "type": "string",
      "format": "uuid"
     },
     "credential": {
      "type": "string",
      "maxLength": 512,
      "description": "The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."
     }
    }
   },
   "refundToOriginalTender": {
    "type": "boolean",
    "default": true
   },
   "alternateTender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DeliveryLocation": {
  "type": "object",
  "x-ticvai-persistence": "fnb.delivery_location",
  "required": [
   "id",
   "venueId",
   "kind",
   "label",
   "isServiceable"
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
   "kind": {
    "$ref": "#/components/schemas/DeliveryLocationKind"
   },
   "label": {
    "type": "string",
    "description": "What a runner is told. \"Cabana 12\", \"Row H Seat 4\", \"Lawn — north gate\"."
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "tableId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set where the location is a restaurant table, so it shares table state."
   },
   "seatId": {
    "type": "string",
    "nullable": true,
    "description": "Set where the seat is the address. References the seat map."
   },
   "servingOutletIds": {
    "type": "array",
    "description": "Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an address.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "isServiceable": {
    "type": "boolean",
    "description": "False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift.\n"
   },
   "unserviceableReason": {
    "type": "string",
    "nullable": true
   },
   "walkTimeMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen.\n"
   }
  }
 },
 "DeliveryLocationKind": {
  "type": "string",
  "description": "4.6.26. One concept, because a runner needs one instruction.",
  "enum": [
   "table",
   "seat",
   "cabana",
   "sunbed",
   "poolside",
   "box",
   "suite",
   "lawn",
   "collectionPoint",
   "namedLocation"
  ]
 },
 "DiningOutlet": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over outlet, menu and table state",
  "required": [
   "outletId",
   "name",
   "kind",
   "isOpenNow",
   "orderingMethod"
  ],
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "cuisine": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "isOpenNow": {
    "type": "boolean"
   },
   "opensAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closesAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "orderingMethod": {
    "$ref": "#/components/schemas/GuestOrderingMethod"
   },
   "estimatedWaitMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "From current kitchen ticket volume, not a fixed figure. Null where the outlet has no kitchen display reporting ticket status — an invented wait time is worse than none.\n"
   },
   "imageAssetRef": {
    "type": "string",
    "nullable": true
   },
   "menuId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "ExchangeOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "outgoingLineIds",
   "incomingLines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "outgoingLineIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "incomingLines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "waiveFee": {
    "type": "boolean",
    "default": false
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ExchangeRateDecimal": {
  "type": "string",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,6)",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n",
  "pattern": "^\\d+(\\.\\d{1,6})?$"
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
 "GuestOrderingMethod": {
  "x-ticvai-persistence": "none — enum",
  "type": "string",
  "description": "How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting.\n",
  "enum": [
   "tableService",
   "appToTable",
   "appToCollect",
   "counterOnly",
   "notAvailable"
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
    "type": "string",
    "format": "uuid"
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
    "format": "uuid",
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
    "format": "uuid"
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
    "format": "uuid"
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
    "format": "uuid"
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
 "ManualDiscountRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Omit to discount the order rather than a line."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 300,
    "description": "Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"
   },
   "reasonCode": {
    "type": "string",
    "nullable": true,
    "description": "Optional alongside the free text, where the venue maintains a list."
   },
   "approverPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required above the venue threshold. May not be the requester."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
 "ModifyOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"
   },
   "addLines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "removeLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
    "type": "string",
    "format": "uuid",
    "description": "The client UUIDv7 from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
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
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
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
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
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
 "OrderExchangeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "orderId",
   "outgoingValue",
   "incomingValue",
   "difference"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "outgoingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "incomingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exchangeFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Only the difference settles. The replacement is held before the original is released, never the other way round.\n"
   },
   "newLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line + orders.order_line_eligibility + orders.order_line_discount",
  "x-ticvai-retired-columns": [
   "promotion_id",
   "name",
   "reason"
  ],
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
      "description": "The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     },
     "reprintCount": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "readOnly": true,
      "description": "How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."
     },
     "venueId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."
     },
     "discounts": {
      "type": "array",
      "readOnly": true,
      "description": "**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.",
      "items": {
       "$ref": "#/components/schemas/OrderLineDiscount"
      }
     }
    }
   }
  ]
 },
 "OrderModificationResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "order",
   "balanceDue"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "addedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "removedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceDue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest pays; negative means a refund is due."
   },
   "refundId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "OrderResumeResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "order",
   "hasChanged"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "hasChanged": {
    "type": "boolean",
    "description": "True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "priceChanged",
        "promotionExpired",
        "promotionNowApplies",
        "soldOut",
        "seatHoldExpired",
        "productWithdrawn"
       ]
      },
      "lineId": {
       "type": "string",
       "format": "uuid"
      },
      "detail": {
       "type": "string"
      },
      "wasAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "nowAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "OrderStatement": {
  "x-ticvai-persistence": "none — computed from order, payment, refund and ledger",
  "type": "object",
  "required": [
   "orderId",
   "orderNumber",
   "currency",
   "entries",
   "currentBalance"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "orderNumber": {
    "type": "string"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "entries": {
    "type": "array",
    "description": "Sequential. What an agent reads to a guest asking about a charge.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "amount",
      "runningBalance",
      "occurredAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "sale",
        "payment",
        "refund",
        "void",
        "modification",
        "exchange",
        "fee",
        "variance",
        "chargeback"
       ]
      },
      "description": {
       "type": "string"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "runningBalance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "referenceId": {
       "type": "string",
       "nullable": true
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
    }
   },
   "totalPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalRefunded": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "currentBalance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest owes; negative means a refund is outstanding."
   }
  }
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
 "OrderSummary": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "id",
   "orderNumber",
   "status",
   "grossAmount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderNumber": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "The same vocabulary as `Order.channel`, which this projects."
   },
   "lineCount": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "The cashier who raised it — what the held-orders list shows."
   },
   "holdLabel": {
    "type": "string",
    "nullable": true,
    "description": "As `Order.holdLabel`."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
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
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
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
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
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
    "nullable": true,
    "description": "The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."
   },
   "providerIdempotencyKey": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal a till payment ran on (ECR flow, SD-034)."
   },
   "nextAction": {
    "type": "object",
    "nullable": true,
    "x-ticvai-persisted": false,
    "description": "**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.",
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "redirect",
       "terminal"
      ]
     },
     "url": {
      "type": "string",
      "format": "uri",
      "nullable": true
     },
     "expiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
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
 "ProductVariant": {
  "x-ticvai-persistence": "catalogue.variant",
  "type": "object",
  "required": [
   "id",
   "productId",
   "sku",
   "axisValues",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "axisValues": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "name": {
    "type": "string",
    "maxLength": 150,
    "nullable": true,
    "description": "**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"
   },
   "barcode": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "description": "**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"
   },
   "isDefault": {
    "type": "boolean",
    "default": false,
    "description": "Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"
   },
   "isActive": {
    "type": "boolean",
    "description": "False when retired. Retired variants are never deleted — orders reference them."
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"
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
 "Refund": {
  "x-ticvai-persistence": "orders.refund",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "amount",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "batchId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."
   },
   "fxRate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
    "nullable": true,
    "readOnly": true,
    "description": "**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"
   },
   "taxReversalEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"
   },
   "settleTo": {
    "type": "string",
    "enum": [
     "originalTender",
     "advanceBalance",
     "wireTransfer",
     "storeCredit"
    ],
    "default": "originalTender",
    "description": "BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n"
   },
   "fxVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "appliedPercentage": {
    "type": "number",
    "description": "From the venue's time bands, or an approver override."
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingApproval",
     "pendingGateway",
     "completed",
     "declined",
     "failed"
    ]
   },
   "reason": {
    "type": "string"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "secondaryPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ledgerEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Written before the gateway is called."
   },
   "gatewayReference": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
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
    "format": "uuid"
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
 "Suggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion",
  "description": "One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n",
  "required": [
   "id",
   "kind",
   "basis",
   "maturity",
   "producedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SuggestionKind"
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "scopePath": {
    "type": "string"
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "What it is about — a product, an outlet, an item, a party."
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "description": "The suggestion itself. Shape depends on `kind`."
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1,
    "description": "**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"
   },
   "explanation": {
    "type": "string",
    "description": "**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"
   },
   "inputs": {
    "type": "object",
    "additionalProperties": true,
    "description": "What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"
   },
   "producerRef": {
    "type": "string",
    "description": "The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"
   }
  }
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario",
   "sendTime",
   "wasteRisk",
   "queueBalancing",
   "itinerary"
  ]
 },
 "TenderKind": {
  "type": "string",
  "description": "`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n",
  "enum": [
   "cash",
   "card",
   "wallet",
   "voucher",
   "bankTransfer",
   "hotelCharge",
   "installment",
   "giftCard",
   "complimentary"
  ]
 },
 "VariantDimension": {
  "x-ticvai-persistence": "catalogue.variant_dimension",
  "type": "object",
  "description": "**A length is an axis like any other** (decided 29 September, rev 3 REV3-13). A meeting room type sold by the hour has an axis `length` with values `1h`, `2h`, `halfDay`, `fullDay`, each carrying `durationMinutes` (proposed 60, 120, 240 and 480, client to correct), and each generated variant is priced on its own, so a half day need not cost four single hours.\n",
  "required": [
   "code",
   "name",
   "values"
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
   "values": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "code",
      "label"
     ],
     "properties": {
      "code": {
       "type": "string",
       "maxLength": 64
      },
      "label": {
       "type": "string",
       "maxLength": 200
      },
      "priceDelta": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "durationMinutes": {
       "type": "integer",
       "minimum": 15,
       "maximum": 1440,
       "nullable": true,
       "description": "How long a variant carrying this value books its space for, on a `length` axis of a product with `requiresTimeWindow` (decided 29 September, rev 3 REV3-13). Null on any other axis. One axis per product at most may carry it; a second is a `400`."
      }
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
    "description": "**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag. **Read per venue**: the planner matches a guest's cuisine only against the points of the venue that day is at (30 September, MoM 4.7).\n",
    "items": {
     "type": "string",
     "maxLength": 30
    }
   },
   "retailTags": {
    "type": "array",
    "maxItems": 8,
    "description": "**For retail points** (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). The planner places a shop stop at points whose tags the party chose, on the day of this point's venue only. Free text codes such as `souvenirs`, `toys`, `apparel`, `photo`, `essentials`, for the same reason as `cuisineTags`. A kiosk may carry both lists.\n",
    "items": {
     "type": "string",
     "maxLength": 30
    }
   }
  }
 },
 "VoidReason": {
  "type": "string",
  "description": "**The void reason list** (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. `other` requires a note (audit R222), and the notes are reviewed quarterly to add real reasons. Proposed, client to correct.\n",
  "enum": [
   "guestChangedMind",
   "enteredInError",
   "itemUnavailable",
   "qualityIssue",
   "duplicate",
   "other"
  ]
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
    "format": "uuid",
    "description": "The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. `listMyWaitingGuests` gives it back to a guest who has lost it.\n"
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
 }
}
```
