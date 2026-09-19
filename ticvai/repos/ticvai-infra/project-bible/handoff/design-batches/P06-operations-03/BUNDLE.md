# P06-operations-03 — P06 · Operations (3 of 5)

**10 screens · 53 operations · 58 schemas · 22 permissions**

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

- **Every control that can be refused must be gated.** 22 permissions apply here:
  `ATTENDANCE_RECORD, CAPACITY_CONFIGURE, CASE_MANAGE, CASE_VIEW, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND`…. A control nobody can use must say so,
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
| `EMP-031` | Queue monitor | listDetail | 7 | 0 | — |
| `EMP-032` | Manual wait entry | listDetail | 5 | 0 | — |
| `EMP-033` | Capacity view | listDetail | 6 | 0 | — |
| `EMP-034` | Walk-up sale | listDetail | 22 | 1 | — |
| `EMP-025` | Break management | listDetail | 2 | 0 | — |
| `EMP-026` | Incident report | listDetail | 5 | 0 | — |
| `EMP-027` | Incident detail | listDetail | 3 | 0 | — |
| `EMP-028` | Lost & found | listDetail | 7 | 0 | — |
| `EMP-029` | Guest assistance | listDetail | 12 | 0 | — |
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
     "to": "EMP-032",
     "trigger": "The sensor is wrong, so a wait is entered by hand",
     "provenance": "flow F67 step 1→2"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createQueue, updateQueue. **A handheld reads a queue and records a wait; it does not create one.** A queue is a venue configuration — bulk-attach residue, and `EMP-031` and `EMP-032` carried identical sets.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listQueues` reads the population and `getQueue` reads one of them — list, select, act",
  "purpose": "See the queue from the floor.",
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
       "label": "The selected queue",
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
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "callNextParties",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The queue list.",
   "error": "Could not load. Names which read failed and leaves the queue untouched.",
   "emptyFirstRun": "No queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onLoad"
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-031"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    },
    {
     "to": "BO-005",
     "trigger": "Parties are called",
     "provenance": "flow F21 step 4→5",
     "operation": "setWaitTime",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: BO-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: callNextParties, createQueue, setQueueStatus, updateQueue. **A handheld reads a queue and records a wait; it does not create one.** A queue is a venue configuration — bulk-attach residue, and `EMP-031` and `EMP-032` carried identical sets.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listQueueEntries` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Take over when the wait feed dies.",
  "gaps": [
   {
    "operation": "getQueue",
    "why": "**2 declared operations reach no component on this screen**: getQueue, listQueues. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every manual wait entry",
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
       "label": "The selected manual wait entry",
       "bindsTo": "WaitTime",
       "columns": [
        "WaitTime.queueId",
        "WaitTime.queueName",
        "WaitTime.attractionProductId",
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
       "label": "Save changes",
       "operation": "setWaitTime",
       "provenance": "contract queue.yaml PUT /queues/{queueId}/wait-time"
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
       "impliedBy": "setWaitTime",
       "label": "Save wait time",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listQueueEntries",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setWaitTime",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The manual wait entry list.",
   "error": "Could not load. Names which read failed and leaves the manual wait entry untouched.",
   "emptyFirstRun": "No manual wait entry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the manual wait entry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onLoad"
   },
   {
    "operationId": "listQueueEntries",
    "contract": "queue",
    "purpose": "List entries in a queue",
    "trigger": "onLoad"
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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every capacity",
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
       "label": "The selected capacity",
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
       "label": "Create",
       "operation": "createChannelCapacity",
       "provenance": "contract catalogue.yaml POST /channel-capacities"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishChannelAllocation",
       "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setChannelAllocations",
       "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateChannelCapacity",
       "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
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
       "impliedBy": "listChannelCapacities",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createChannelCapacity",
       "label": "Create envelope",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createChannelCapacity",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity list.",
   "error": "Could not load. Names which read failed and leaves the capacity untouched.",
   "emptyFirstRun": "No capacity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onLoad"
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
    "ChannelAllocationSet.channelCapacityId",
    "ChannelAllocationSet.capacity",
    "ChannelAllocationSet.allocations",
    "ChannelAllocationSet.generalPoolUnits",
    "ChannelAllocationSet.totalSold"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-033"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "EMP-035"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-035",
     "trigger": "The guest taps a card on the device",
     "provenance": "flow F66 step 1→2"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createProduct, updateProduct. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Sell at the gate without a till.",
  "gaps": [
   {
    "operation": "getOrderStatement",
    "why": "**6 declared operations reach no component on this screen**: getOrderStatement, getProduct, listAlternativeCodes, listOrderRefunds, listOrders, listProductVariants. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every walk-up sale",
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
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected walk-up sale",
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
       "label": "Create",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve",
       "operation": "resolveProductByCode",
       "provenance": "contract catalogue.yaml GET /products/resolve"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAlternativeCodes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition",
       "operation": "transitionProductLifecycle",
       "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
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
       "impliedBy": "createOrder",
       "label": "Create order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listProducts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "voidOrder",
       "label": "Void order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createOrder",
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
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A walk-up sale this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   }
  ],
  "states": {
   "loading": "The walk-up sale list.",
   "error": "Could not load. Names which read failed and leaves the walk-up sale untouched.",
   "emptyFirstRun": "No walk-up sale yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the walk-up sale are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
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
    "trigger": "onLoad"
   },
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onLoad"
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
    "trigger": "onLoad"
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
    "trigger": "onLoad"
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
    "Order.id",
    "Order.orderNumber",
    "Order.channel",
    "Order.venueId",
    "Order.scopePath"
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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every break",
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
       "label": "The selected break",
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
       "label": "Record",
       "operation": "recordAttendance",
       "provenance": "contract workforce.yaml POST /attendance/clock"
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
       "impliedBy": "listAttendance",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordAttendance",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The break list.",
   "error": "Could not load. Names which read failed and leaves the break untouched.",
   "emptyFirstRun": "No break yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the break are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
     "to": "EMP-027",
     "trigger": "A supervisor reads it and adds detail",
     "provenance": "flow F69 step 1→2",
     "operation": "reportIncident"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every incident report",
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
       "label": "The selected incident report",
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
   "loading": "The incident report list.",
   "error": "Could not load. Names which read failed and leaves the incident report untouched.",
   "emptyFirstRun": "No incident report yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the incident report are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Queues locally with the highest sync priority"
  },
  "apis": [
   {
    "operationId": "reportIncident",
    "contract": "maintenance",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "Read an incident",
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-026"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "to": "EMP-050",
     "trigger": "Where required, the authorities are notified",
     "provenance": "flow F69 step 2→3"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
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
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateIncident",
       "label": "Save incident",
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
       "impliedBy": "updateIncident",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The incident list.",
   "error": "Could not load. Names which read failed and leaves the incident untouched.",
   "emptyFirstRun": "No incident yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the incident are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached; updates queue"
  },
  "apis": [
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateIncident",
    "contract": "maintenance",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
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
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-027"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every lost found",
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
       "label": "The selected lost found",
       "bindsTo": "CaseDetail",
       "columns": [
        "CaseDetail.id",
        "CaseDetail.caseNumber",
        "CaseDetail.subjectId",
        "CaseDetail.guestName",
        "CaseDetail.subject",
        "CaseDetail.categoryId",
        "CaseDetail.status",
        "CaseDetail.priority",
        "CaseDetail.assignedToPrincipalId",
        "CaseDetail.venueId",
        "CaseDetail.relatedOrderId",
        "CaseDetail.slaDueAt",
        "CaseDetail.isSlaBreached",
        "CaseDetail.slaPausedSeconds",
        "CaseDetail.escalationCount",
        "CaseDetail.resolvedAt"
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
       "label": "Create",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Add",
       "operation": "addCaseMessage",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "operation": "escalateCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateCase",
       "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
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
       "impliedBy": "createCase",
       "label": "Create case",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCases",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createCase",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lost found list.",
   "error": "Could not load. Names which read failed and leaves the lost found untouched.",
   "emptyFirstRun": "No lost found yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the lost found are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onLoad"
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
    "CaseDetail.id",
    "CaseDetail.caseNumber",
    "CaseDetail.subjectId",
    "CaseDetail.guestName",
    "CaseDetail.subject"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-028"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listCases` reads the population and `getCase` reads one of them — list, select, act",
  "purpose": "Help a guest without leaving the floor.",
  "gaps": [
   {
    "operation": "getIncident",
    "why": "**2 declared operations reach no component on this screen**: getIncident, listIncidents. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every guest assistance",
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
       "label": "The selected guest assistance",
       "bindsTo": "CaseDetail",
       "columns": [
        "CaseDetail.id",
        "CaseDetail.caseNumber",
        "CaseDetail.subjectId",
        "CaseDetail.guestName",
        "CaseDetail.subject",
        "CaseDetail.categoryId",
        "CaseDetail.status",
        "CaseDetail.priority",
        "CaseDetail.assignedToPrincipalId",
        "CaseDetail.venueId",
        "CaseDetail.relatedOrderId",
        "CaseDetail.slaDueAt",
        "CaseDetail.isSlaBreached",
        "CaseDetail.slaPausedSeconds",
        "CaseDetail.escalationCount",
        "CaseDetail.resolvedAt"
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
       "label": "Report",
       "operation": "reportIncident",
       "provenance": "contract maintenance.yaml POST /incidents"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Add",
       "operation": "addCaseMessage",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "operation": "escalateCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordAuthorityNotification",
       "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateCase",
       "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
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
       "impliedBy": "listCases",
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
   "loading": "The guest assistance list.",
   "error": "Could not load. Names which read failed and leaves the guest assistance untouched.",
   "emptyFirstRun": "No guest assistance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest assistance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "trigger": "onLoad"
   },
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "Read an incident",
    "trigger": "onLoad"
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
    "CaseDetail.id",
    "CaseDetail.caseNumber",
    "CaseDetail.subjectId",
    "CaseDetail.guestName",
    "CaseDetail.subject"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-029"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — EMP-002 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId",
      "shiftId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId, shiftId, so an edge into it must carry them"
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
    "operation": "listDeliveryLocations",
    "why": "**2 declared operations reach no component on this screen**: listDeliveryLocations, getVenueMapLive. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every venue map",
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
       "impliedBy": "listDiningOutlets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue map list.",
   "error": "Could not load. Names which read failed and leaves the venue map untouched.",
   "emptyFirstRun": "No venue map yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue map are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "VenueMapDetail.map",
    "VenueMapDetail.points",
    "VenueMapDetail.paths"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-030",
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
  "summary": "Create a capacity envelope",
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
  "parameters": [],
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
  "summary": "List capacity envelopes",
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
  "responds": "DeliveryLocation"
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
  "responds": "DiningOutlet"
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
  "responds": "Refund"
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
  "summary": "Allocate envelope capacity across channels",
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
  "summary": "Amend an envelope",
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
    "nullable": true
   },
   "amendmentReason": {
    "type": "string",
    "nullable": true
   },
   "originalOccurredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"
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
    "type": "string"
   },
   "caseNumber": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true
   },
   "subject": {
    "type": "string"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
    "type": "boolean"
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
    "format": "date-time"
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
    "type": "integer"
   },
   "leased": {
    "type": "integer"
   },
   "remaining": {
    "type": "integer"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
   "priority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CasePriority"
     }
    ],
    "default": "normal"
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
 "CreateEnvelopeRequest": {
  "type": "object",
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string"
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
      "maxLength": 512
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
    "description": "From current kitchen ticket volume, not a fixed figure. Null where the outlet has no KDS reporting — an invented wait time is worse than none.\n"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "outgoingLineIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lineId": {
    "type": "string",
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
     "type": "string"
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
    "type": "string"
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
     "type": "string"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
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
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
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
       "type": "string"
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
    "type": "string"
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
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n",
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
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n",
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
   "isActive": {
    "type": "boolean",
    "description": "False when retired. Retired variants are never deleted — orders reference them."
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
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "fxRate": {
    "type": "number",
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
 "TenderKind": {
  "type": "string",
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
 }
}
```
