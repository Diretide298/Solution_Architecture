# P08-access-venue-01 — P08 · Access & Venue (1 of 3)

**10 screens · 62 operations · 57 schemas · 20 permissions**

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

- **Every control that can be refused must be gated.** 20 permissions apply here:
  `ACCESS_POINT_CONFIGURE, ASSET_MANAGE, ASSET_VIEW, EVENT_CONFIGURE, MAINTENANCE_APPROVE, MAINTENANCE_EXECUTE, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW, ORDER_REFUND_APPROVE, ORDER_REFUND_BULK, PARKING_CONFIGURE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **21 of these operations work offline**: acceptWorkOrder, attachWorkOrderEvidence, completeWorkOrder, createWorkOrder, getAsset, getPerformance, getQueue, getWaitTimes
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-001` | Queue Directory | listDetail | 19 | 0 | — |
| `BO-002` | Queue Configuration | listDetail | 14 | 1 | — |
| `BO-003` | Queue Integration Setup | listDetail | 4 | 0 | — |
| `BO-004` | Manual Wait Time Entry | approvalInbox | 11 | 0 | — |
| `BO-005` | Queue Monitor | listDetail | 19 | 1 | — |
| `BO-006` | Parking Configuration | listDetail | 4 | 0 | — |
| `BO-030` | Work Order Verification | listDetail | 9 | 2 | — |
| `BO-031` | Asset Register | listDetail | 7 | 0 | — |
| `BO-032` | Admission Profiles | listDetail | 3 | 0 | — |
| `BO-033` | Blacklist Management | listDetail | 3 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-001",
  "name": "Queue Directory",
  "module": "Access & Venue",
  "requiresModule": "queue",
  "wave": 1,
  "capability": "C05",
  "implementation": {
   "app": "venue-management-web",
   "route": "/queue-management/queue-directory",
   "component": "apps/venue-management-web/src/routes/queue-management/QueueDirectoryList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-002",
    "BO-003",
    "BO-004",
    "BO-005"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-002",
     "trigger": "Cancels it and states the reason",
     "provenance": "flow F09 step 1→2",
     "operation": "listPerformances"
    },
    {
     "to": "BO-003",
     "trigger": "Queue Integration Setup",
     "carries": [
      "feedId",
      "orderId",
      "venueId"
     ],
     "provenance": "derived — BO-003 declares entryState.params feedId, orderId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-004",
     "trigger": "Manual Wait Time Entry",
     "carries": [
      "queueId",
      "refundId"
     ],
     "provenance": "derived — BO-004 declares entryState.params queueId, refundId, so an edge into it must carry them"
    },
    {
     "to": "BO-005",
     "trigger": "Queue Monitor",
     "carries": [
      "campaignId",
      "queueId"
     ],
     "provenance": "derived — BO-005 declares entryState.params campaignId, queueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "A queue on the manual adaptor shows \"manual\" rather than \"no feed\". It is configured and working; treating it as unconfigured makes the health view lie. **Was the declared entry point to the whole back office until 20 August**, which is why 93 screens were unreachable. Now reached from BO-100 through its section.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listQueues` reads the population and `getEvent` reads one of them — list, select, act",
  "purpose": "See every queue in the venue and whether its data is arriving.",
  "gaps": [
   {
    "operation": "listQueueFeeds",
    "why": "**7 declared operations reach no component on this screen**: listQueueFeeds, listPerformances, getQueue, getQueueFeedHealth, getWaitTimes, listEvents, listQueueEntries. Either the screen is missing what calls them, or the declaration is residue.",
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
       "bindsTo": "Event",
       "columns": [
        "Event.id",
        "Event.code",
        "Event.name",
        "Event.venueId",
        "Event.scopePath",
        "Event.parentEventId",
        "Event.performanceCount",
        "Event.isActive"
       ],
       "operation": "getEvent",
       "provenance": "contract catalogue.yaml GET /events/{eventId}"
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
       "label": "Configure",
       "operation": "configureQueueFeed",
       "provenance": "contract queue.yaml PUT /queue-feeds"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createEvent",
       "provenance": "contract catalogue.yaml POST /events"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPerformances",
       "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createQueue",
       "provenance": "contract queue.yaml POST /queues"
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
      },
      {
       "kind": "secondaryButton",
       "label": "Test",
       "operation": "testQueueFeed",
       "provenance": "contract queue.yaml POST /queue-feeds/{feedId}/test"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateEvent",
       "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateQueue",
       "provenance": "contract queue.yaml PATCH /queues/{queueId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "bindsTo": "Queue[]",
       "notes": "Current wait, source, feed health, status",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Queues whose feed has gone quiet. The first thing a duty manager checks",
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
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "Every queue with its current wait",
    "trigger": "onLoad"
   },
   {
    "operationId": "listQueueFeeds",
    "contract": "queue",
    "purpose": "Feed health per queue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "From the flow it appears in",
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
    "operationId": "configureQueueFeed",
    "contract": "queue",
    "purpose": "Configure a sensor feed",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "createEvent",
    "contract": "catalogue",
    "purpose": "Create an event",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "createPerformances",
    "contract": "catalogue",
    "purpose": "Create performances, singly or by schedule",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
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
    "operationId": "getEvent",
    "contract": "catalogue",
    "purpose": "Read an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "getQueue",
    "contract": "queue",
    "purpose": "Read a queue with live position",
    "trigger": "onLoad"
   },
   {
    "operationId": "getQueueFeedHealth",
    "contract": "queue",
    "purpose": "Feed health",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEvents",
    "contract": "catalogue",
    "purpose": "List events",
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
   },
   {
    "operationId": "testQueueFeed",
    "contract": "queue",
    "purpose": "Test a feed before trusting it",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "updateEvent",
    "contract": "catalogue",
    "purpose": "Amend an event",
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
     "name": "eventId",
     "from": "deepLink"
    },
    {
     "name": "feedId",
     "from": "deepLink"
    },
    {
     "name": "queueId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `eventId`, `feedId`, `queueId`.",
   "preloaded": [
    "Event.id",
    "Event.code",
    "Event.name",
    "Event.venueId",
    "Event.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-001"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 19 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-002",
  "name": "Queue Configuration",
  "module": "Access & Venue",
  "requiresModule": "queue",
  "wave": 1,
  "capability": "C05",
  "implementation": {
   "app": "venue-management-web",
   "route": "/queue-management/queue-configuration",
   "component": "apps/venue-management-web/src/routes/queue-management/QueueConfigurationForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-001"
   ],
   "inferred": true,
   "exitTo": [
    "BO-001",
    "BO-003",
    "BO-004",
    "BO-023"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-023",
     "trigger": "Reviews the refund exposure",
     "provenance": "flow F09 step 2→3",
     "operation": "cancelPerformance"
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
     "to": "BO-003",
     "trigger": "Queue Integration Setup",
     "carries": [
      "feedId",
      "orderId",
      "venueId"
     ],
     "provenance": "derived — BO-003 declares entryState.params feedId, orderId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-004",
     "trigger": "Manual Wait Time Entry",
     "carries": [
      "queueId",
      "refundId"
     ],
     "provenance": "derived — BO-004 declares entryState.params queueId, refundId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 2.dc.html#seat-2c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listQueueEntries` reads the population and `getPerformance` reads one of them — list, select, act",
  "purpose": "Create a queue and set how it behaves.",
  "gaps": [
   {
    "operation": "getQueue",
    "why": "**4 declared operations reach no component on this screen**: getQueue, getSeatAvailability, getWaitTimes, listQueues. Either the screen is missing what calls them, or the declaration is residue.",
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
       "bindsTo": "Performance",
       "columns": [
        "Performance.id",
        "Performance.eventId",
        "Performance.startsAt",
        "Performance.endsAt",
        "Performance.approvalRequestId",
        "Performance.requiresApprovalToCancel",
        "Performance.status",
        "Performance.admissionRulesId",
        "Performance.seatMapId"
       ],
       "operation": "getPerformance",
       "provenance": "contract catalogue.yaml GET /performances/{performanceId}"
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
       "operation": "createQueue",
       "provenance": "contract queue.yaml POST /queues"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateQueue",
       "provenance": "contract queue.yaml PATCH /queues/{queueId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelPerformance",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Call",
       "operation": "callNextParties",
       "provenance": "contract queue.yaml POST /queues/{queueId}/call-next"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
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
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePerformance",
       "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "textField",
       "label": "Name",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "selectField",
       "label": "Attraction or resource",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "numberField",
       "label": "Capacity per call",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "toggle",
       "label": "Guests may join from the app",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "numberField",
       "label": "Redemption window (minutes)",
       "notes": "How long after being called before the entry expires",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelPerformance",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A queue this affects should be identified in the dialog, not just counted.",
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
   }
  ],
  "states": {
   "loading": "The queue list.",
   "error": "Could not load. Names which read failed and leaves the queue untouched.",
   "emptyFirstRun": "No queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createQueue",
    "contract": "queue",
    "purpose": "Create",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "updateQueue",
    "contract": "queue",
    "purpose": "Amend",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "cancelPerformance",
    "contract": "catalogue",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "callNextParties",
    "contract": "queue",
    "purpose": "Call the next parties forward",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "getPerformance",
    "contract": "catalogue",
    "purpose": "Read a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "getQueue",
    "contract": "queue",
    "purpose": "Read a queue with live position",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Seat status for a performance",
    "trigger": "onLoad"
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
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "List queues",
    "trigger": "onLoad"
   },
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Recommend seats for a party",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "setQueueStatus",
    "contract": "queue",
    "purpose": "Open, pause or close a queue",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
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
    "operationId": "updatePerformance",
    "contract": "catalogue",
    "purpose": "Amend a performance",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "performanceId",
     "from": "BO-001"
    },
    {
     "name": "queueId",
     "from": "BO-001"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Performance.id",
    "Performance.eventId",
    "Performance.startsAt",
    "Performance.endsAt",
    "Performance.approvalRequestId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-002",
   "note": "**Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 14 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-003",
  "name": "Queue Integration Setup",
  "module": "Access & Venue",
  "requiresModule": "queue",
  "wave": 1,
  "capability": "C05",
  "implementation": {
   "app": "venue-management-web",
   "route": "/queue-management/queue-integration-setup",
   "component": "apps/venue-management-web/src/routes/queue-management/QueueIntegrationSetupForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-001"
   ],
   "inferred": true,
   "exitTo": [
    "BO-001",
    "BO-002",
    "BO-004"
   ],
   "fromFlows": true,
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
     "to": "BO-002",
     "trigger": "Queue Configuration",
     "carries": [
      "performanceId",
      "queueId"
     ],
     "provenance": "derived — BO-002 declares entryState.params performanceId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-004",
     "trigger": "Manual Wait Time Entry",
     "carries": [
      "queueId",
      "refundId"
     ],
     "provenance": "derived — BO-004 declares entryState.params queueId, refundId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "ADR-0012, adaptor-first. A named vendor is a driver behind a stable inbound shape, so adding one is configuration plus a driver rather than a core change. Vendor selection is CF-33a and deliberately late. **createRefund removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Corrected 24 August**: removed applyManualDiscount, createOrder, exchangeOrderLines, getOrder, getOrderStatement, getRefundPolicy and 11 more. **A queue integration screen carried 15 order operations** — create an order, apply a discount, exchange lines, hold, refund — and four queue ones. Bulk-attach residue, and `requiresModule` was `ticketing` to match the operations rather than the screen.\n\n**Found by deriving the empty states.** `emptyNoAccess` came out reading *\"needs `ORDER_CREATE` to create orders\"* on a screen called Queue Integration Setup — **a generated sentence that was accurate to the data and absurd about the screen**, which is exactly what made it visible.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listQueueFeeds` reads the population and `getQueueFeedHealth` reads one of them — list, select, act",
  "purpose": "Connect a queue to an on-site system, or leave it on manual entry.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every queue integration",
       "bindsTo": "QueueFeed",
       "columns": [
        "QueueFeed.id",
        "QueueFeed.queueId",
        "QueueFeed.adaptor",
        "QueueFeed.adaptorName",
        "QueueFeed.credentialsRef",
        "QueueFeed.expectedIntervalSeconds",
        "QueueFeed.isEnabled"
       ],
       "operation": "listQueueFeeds",
       "provenance": "contract queue.yaml GET /queue-feeds"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected queue integration",
       "bindsTo": "QueueFeedHealth",
       "columns": [
        "QueueFeedHealth.feedId",
        "QueueFeedHealth.adaptor",
        "QueueFeedHealth.isHealthy",
        "QueueFeedHealth.isQuiet",
        "QueueFeedHealth.lastReadingAt",
        "QueueFeedHealth.readingsLastHour",
        "QueueFeedHealth.discardedLastHour"
       ],
       "operation": "getQueueFeedHealth",
       "provenance": "contract queue.yaml GET /queue-feeds/{feedId}/health"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Configure",
       "operation": "configureQueueFeed",
       "provenance": "contract queue.yaml PUT /queue-feeds"
      },
      {
       "kind": "secondaryButton",
       "label": "Test",
       "operation": "testQueueFeed",
       "provenance": "contract queue.yaml POST /queue-feeds/{feedId}/test"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "selectField",
       "label": "Source",
       "notes": "Manual, sensor API, webhook, MQTT, vendor poll, turnstile count, CV camera. Manual is the default and a valid end state",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Endpoint or topic",
       "notes": "Hidden when the source is manual",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Credential reference",
       "notes": "A key vault reference, never the secret. A secret typed into a form ends up in a screenshot",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "numberField",
       "label": "Expected interval (seconds)",
       "notes": "Drives the went-quiet alarm. Too tight and a duty manager learns to ignore it",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Test connection",
       "notes": "Runs testQueueFeed. Configuring an integration without a test is configuring it blind",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "bindsTo": "FeedTestResult",
       "notes": "Five checks, plus the mapped sample reading and the raw payload. A source that is reachable and returns a shape nobody mapped looks like silence, not an error",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "toggle",
       "label": "Enabled",
       "notes": "Disabled by default. A feed goes live only after a passing test",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The queue integration list.",
   "error": "Could not load. Names which read failed and leaves the queue integration untouched.",
   "emptyFirstRun": "No queue integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the queue integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "configureQueueFeed",
    "contract": "queue",
    "purpose": "Set the source",
    "trigger": "onAction",
    "invalidates": [
     "listQueueFeeds"
    ]
   },
   {
    "operationId": "testQueueFeed",
    "contract": "queue",
    "purpose": "One exchange with the configured source",
    "trigger": "onAction",
    "invalidates": [
     "listQueueFeeds"
    ]
   },
   {
    "operationId": "getQueueFeedHealth",
    "contract": "queue",
    "purpose": "Current feed state",
    "trigger": "onLoad"
   },
   {
    "operationId": "listQueueFeeds",
    "contract": "queue",
    "purpose": "List configured sensor feeds",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "feedId",
     "from": "BO-001"
    },
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "QueueFeedHealth.feedId",
    "QueueFeedHealth.adaptor",
    "QueueFeedHealth.isHealthy",
    "QueueFeedHealth.isQuiet",
    "QueueFeedHealth.lastReadingAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-003"
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
  "id": "BO-004",
  "name": "Manual Wait Time Entry",
  "module": "Access & Venue",
  "requiresModule": "queue",
  "wave": 1,
  "capability": "C05",
  "implementation": {
   "app": "venue-management-web",
   "route": "/queue-management/manual-wait-time-entry",
   "component": "apps/venue-management-web/src/routes/queue-management/ManualWaitTimeEntryForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-001",
    "BO-023"
   ],
   "inferred": true,
   "exitTo": [
    "BO-001",
    "BO-002",
    "BO-003",
    "BO-005"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-005",
     "trigger": "Confirms guests were notified",
     "provenance": "flow F09 step 4→5",
     "operation": "createBulkRefund"
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
     "to": "BO-002",
     "trigger": "Queue Configuration",
     "carries": [
      "performanceId",
      "queueId"
     ],
     "provenance": "derived — BO-002 declares entryState.params performanceId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-003",
     "trigger": "Queue Integration Setup",
     "carries": [
      "feedId",
      "orderId",
      "venueId"
     ],
     "provenance": "derived — BO-003 declares entryState.params feedId, orderId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "The screen the client asked for on 14 August. Available regardless of integration state — a venue with no sensors runs entirely from here, and a venue whose sensor failed falls back to it.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`approveRefund` decides items that `listQueues` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Set a wait time by hand, whether or not a feed exists.",
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
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
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
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected manual wait time",
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
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setWaitTime",
       "provenance": "contract queue.yaml PUT /queues/{queueId}/wait-time"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createBulkRefund",
       "provenance": "contract orders.yaml POST /refunds/bulk"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "operation": "approveRefund",
       "provenance": "contract orders.yaml POST /refunds/{refundId}/approve"
      },
      {
       "kind": "secondaryButton",
       "label": "Call",
       "operation": "callNextParties",
       "provenance": "contract queue.yaml POST /queues/{queueId}/call-next"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createQueue",
       "provenance": "contract queue.yaml POST /queues"
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
       "operation": "updateQueue",
       "provenance": "contract queue.yaml PATCH /queues/{queueId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "Queue[]",
       "notes": "One row per queue with a stepper and the current value",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Where a feed is live, a manual entry overrides it for a stated period and then reverts. A permanent silent override is how a broken sensor goes unnoticed for a season",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The manual wait time list.",
   "error": "Could not load. Names which read failed and leaves the manual wait time untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the manual wait time are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWaitTime",
    "contract": "queue",
    "purpose": "Set or override the wait",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "Current values",
    "trigger": "onLoad"
   },
   {
    "operationId": "createBulkRefund",
    "contract": "orders",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "approveRefund",
    "contract": "orders",
    "purpose": "Approve a refund held for approval",
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
    "operationId": "createQueue",
    "contract": "queue",
    "purpose": "Create a queue",
    "trigger": "onAction",
    "invalidates": [
     "listQueues"
    ]
   },
   {
    "operationId": "getQueue",
    "contract": "queue",
    "purpose": "Read a queue with live position",
    "trigger": "onLoad"
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
     "from": "BO-001"
    },
    {
     "name": "refundId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `refundId`.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-004"
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
  "id": "BO-005",
  "name": "Queue Monitor",
  "module": "Access & Venue",
  "requiresModule": "marketing",
  "wave": 1,
  "capability": "C05",
  "implementation": {
   "app": "venue-management-web",
   "route": "/queue-management/queue-monitor",
   "component": "apps/venue-management-web/src/routes/queue-management/QueueMonitorDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-001"
   ],
   "inferred": true,
   "exitTo": [
    "BO-001",
    "BO-002",
    "BO-003"
   ],
   "fromFlows": true,
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
     "to": "BO-002",
     "trigger": "Queue Configuration",
     "carries": [
      "performanceId",
      "queueId"
     ],
     "provenance": "derived — BO-002 declares entryState.params performanceId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-003",
     "trigger": "Queue Integration Setup",
     "carries": [
      "feedId",
      "orderId",
      "venueId"
     ],
     "provenance": "derived — BO-003 declares entryState.params feedId, orderId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-032",
     "trigger": "The feed dies and a supervisor types the wait",
     "provenance": "flow F21 step 3→4",
     "operation": "listQueues",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Pulled to Wave 1 on 17 August (CF-101): F09 closes a cancelled event’s queue, and a Wave 1 flow cannot step through a Wave 2 screen. **Cross-platform navigation removed 24 August**: EMP-032. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listQueueEntries` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Watch queues during operation and call parties forward.",
  "gaps": [
   {
    "operation": "listCampaigns",
    "why": "**5 declared operations reach no component on this screen**: listCampaigns, getCampaign, getCampaignPerformance, getQueue, listQueues. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Call",
       "operation": "callNextParties",
       "provenance": "contract queue.yaml POST /queues/{queueId}/call-next"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createQueue",
       "provenance": "contract queue.yaml POST /queues"
      },
      {
       "kind": "secondaryButton",
       "label": "Launch",
       "operation": "launchCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns/{campaignId}/launch"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause",
       "operation": "pauseCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns/{campaignId}/pause"
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
      },
      {
       "kind": "destructiveButton",
       "label": "Stop",
       "operation": "stopCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns/{campaignId}/stop"
      },
      {
       "kind": "secondaryButton",
       "label": "Test",
       "operation": "testSendCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns/{campaignId}/test-send"
      },
      {
       "kind": "secondaryButton",
       "label": "Unschedule",
       "operation": "unscheduleCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns/{campaignId}/unschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateCampaign",
       "provenance": "contract marketing-crm.yaml PATCH /campaigns/{campaignId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateQueue",
       "provenance": "contract queue.yaml PATCH /queues/{queueId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "metricTile",
       "notes": "Waiting, called, expired, average wait",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "Wait over the day. Stale where the feed has gone quiet",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Call next",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmStopCampaign",
    "component": "confirmDialog",
    "trigger": "Stop",
    "body": "**Names what `stopCampaign` changes and what it leaves alone**, in the consequence rather than the verb. A queue this affects should be identified in the dialog, not just counted.",
    "provenance": "contract marketing-crm.yaml POST /campaigns/{campaignId}/stop"
   }
  ],
  "states": {
   "loading": "The queue list.",
   "error": "Could not load. Names which read failed and leaves the queue untouched.",
   "emptyFirstRun": "No queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQueueEntries",
    "contract": "queue",
    "purpose": "Who is waiting",
    "trigger": "onInterval"
   },
   {
    "operationId": "callNextParties",
    "contract": "queue",
    "purpose": "Call forward",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Current waits",
    "trigger": "onInterval"
   },
   {
    "operationId": "listCampaigns",
    "contract": "marketing-crm",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCampaign",
    "contract": "marketing-crm",
    "purpose": "Create a campaign",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "createQueue",
    "contract": "queue",
    "purpose": "Create a queue",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "getCampaign",
    "contract": "marketing-crm",
    "purpose": "Read a campaign with performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCampaignPerformance",
    "contract": "marketing-crm",
    "purpose": "Delivery and engagement",
    "trigger": "onLoad"
   },
   {
    "operationId": "getQueue",
    "contract": "queue",
    "purpose": "Read a queue with live position",
    "trigger": "onLoad"
   },
   {
    "operationId": "launchCampaign",
    "contract": "marketing-crm",
    "purpose": "Launch or schedule a campaign",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "List queues",
    "trigger": "onLoad"
   },
   {
    "operationId": "pauseCampaign",
    "contract": "marketing-crm",
    "purpose": "Pause a campaign mid-send",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "setQueueStatus",
    "contract": "queue",
    "purpose": "Open, pause or close a queue",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
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
    "operationId": "stopCampaign",
    "contract": "marketing-crm",
    "purpose": "Stop a campaign mid-send",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "testSendCampaign",
    "contract": "marketing-crm",
    "purpose": "Send a test to named recipients",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "unscheduleCampaign",
    "contract": "marketing-crm",
    "purpose": "Pull a scheduled campaign before it sends",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "updateCampaign",
    "contract": "marketing-crm",
    "purpose": "Amend, pause or resume a campaign",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   },
   {
    "operationId": "updateQueue",
    "contract": "queue",
    "purpose": "Amend queue configuration",
    "trigger": "onAction",
    "invalidates": [
     "listQueueEntries"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "campaignId",
     "from": "deepLink"
    },
    {
     "name": "queueId",
     "from": "BO-001"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `campaignId`.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-005"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 19 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-006",
  "name": "Parking Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 2,
  "capability": "C39",
  "implementation": {
   "app": "venue-management-web",
   "route": "/parking/parking-configuration",
   "component": "apps/venue-management-web/src/routes/parking/ParkingConfigurationForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-001"
   ],
   "inferred": true,
   "exitTo": [
    "BO-001"
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
    }
   ]
  },
  "notes": "Placeholder. Parking was discussed on 14 August and the MoM has not yet been received. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "Answered by the 14 August MoM section 10, which this question was waiting for. Parking is barrier integration, in three models, and it is not space counting. (1) No integration - TICVAI issues its own QR and on-site security verifies it manually; (2) ANPR - the guest enters a plate at checkout and TICVAI pushes it to the parking system's whitelist so the barrier opens; (3) QR handoff - TICVAI sends a QR to the barrier for validation. Pay-per-hour parking is explicitly out of scope, handled by the parking vendor's own POS. So this is one configuration screen choosing a model and binding a vendor adaptor, not the three different screens the question feared - and ADR-0012's adaptor-first rule is what the minute asks for when it says a new parking vendor should take days rather than weeks. The `parking` module key in the White Label Builder now has something behind it."
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAccessPoints` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Change how parking behaves here, and see which level the current value came from.",
  "gaps": [
   {
    "operation": "listParkingFacilities",
    "why": "**1 declared operation reach no component on this screen**: listParkingFacilities. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every parking",
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
       "label": "The selected parking",
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
       "operation": "listAccessPoints",
       "provenance": "contract access.yaml GET /access-points"
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
       "operation": "updateAccessPoint",
       "provenance": "contract access.yaml PATCH /access-points/{accessPointId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setParkingFacility",
       "provenance": "contract access.yaml PUT /parking-facilities"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "TODO",
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
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateAccessPoint",
       "label": "Save access point",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateAccessPoint",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The parking list.",
   "error": "Could not load. Names which read failed and leaves the parking untouched.",
   "emptyFirstRun": "No parking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the parking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "List access points",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateAccessPoint",
    "contract": "access",
    "purpose": "Update an access point",
    "trigger": "onAction",
    "invalidates": [
     "listAccessPoints"
    ]
   },
   {
    "operationId": "listParkingFacilities",
    "contract": "access",
    "purpose": "Car parks at a venue, and how each integrates",
    "trigger": "onLoad"
   },
   {
    "operationId": "setParkingFacility",
    "contract": "access",
    "purpose": "Configure a car park and its integration",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-006"
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
  "id": "BO-030",
  "name": "Work Order Verification",
  "module": "Access & Venue",
  "requiresModule": "maintenance",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/access-point-directory",
   "component": "apps/venue-management-web/src/routes/venue-operations/AccessPointDirectoryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-031"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-031",
     "trigger": "Asset returns to service",
     "provenance": "flow F12 step 4→5",
     "operation": "verifyWorkOrder"
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
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried eight work-order operations.** An access point directory is `access`, not `maintenance` — the two share the word *point* and nothing else. **Rewired 20 August.** **Named `Access Point Directory` and carried nine work-order operations.** On 20 August I rewired it to access points; **F12 step 4 then refused, because a supervisor verifies a work order here.** The operations were right and the name was wrong — **the flow knew what the screen was for and the name did not.**",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act",
  "purpose": "See every gate and what it is doing.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every work order verification",
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
       "label": "The selected work order verification",
       "bindsTo": "WorkOrderDetail",
       "columns": [
        "WorkOrderDetail.downtimeMinutes",
        "WorkOrderDetail.rootCause",
        "WorkOrderDetail.rootCauseNote",
        "WorkOrderDetail.escalatedAt",
        "WorkOrderDetail.escalationLevel",
        "WorkOrderDetail.id",
        "WorkOrderDetail.workOrderNumber",
        "WorkOrderDetail.title",
        "WorkOrderDetail.venueId",
        "WorkOrderDetail.assetId",
        "WorkOrderDetail.assetName",
        "WorkOrderDetail.status",
        "WorkOrderDetail.priority",
        "WorkOrderDetail.kind",
        "WorkOrderDetail.assignedToPrincipalId",
        "WorkOrderDetail.raisedByPrincipalId"
       ],
       "operation": "getWorkOrder",
       "provenance": "contract maintenance.yaml GET /work-orders/{workOrderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Verify",
       "operation": "verifyWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/verify"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept",
       "operation": "acceptWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/accept"
      },
      {
       "kind": "secondaryButton",
       "label": "Attach",
       "operation": "attachWorkOrderEvidence",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/attachments"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createWorkOrder",
       "provenance": "contract maintenance.yaml POST /work-orders"
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
       "impliedBy": "verifyWorkOrder",
       "label": "Verify work order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelWorkOrder",
       "label": "Cancel work order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listWorkOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "verifyWorkOrder",
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
    "id": "confirmCancelWorkOrder",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A work order verification this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/cancel"
   },
   {
    "id": "confirmCloseWorkOrder",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A work order verification this affects should be identified in the dialog, not just counted.",
    "provenance": "contract maintenance.yaml POST /work-orders/{workOrderId}/close"
   }
  ],
  "states": {
   "loading": "The work order verification list.",
   "error": "Could not load. Names which read failed and leaves the work order verification untouched.",
   "emptyFirstRun": "No work order verification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the work order verification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "verifyWorkOrder",
    "contract": "maintenance",
    "purpose": "Supervisor verification",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "acceptWorkOrder",
    "contract": "maintenance",
    "purpose": "The assignee takes the job",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "attachWorkOrderEvidence",
    "contract": "maintenance",
    "purpose": "Photo, video, document, note or signature",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "cancelWorkOrder",
    "contract": "maintenance",
    "purpose": "Cancel a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "closeWorkOrder",
    "contract": "maintenance",
    "purpose": "Administratively closed",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "completeWorkOrder",
    "contract": "maintenance",
    "purpose": "Complete a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "createWorkOrder",
    "contract": "maintenance",
    "purpose": "Raise a work order",
    "trigger": "onAction",
    "invalidates": [
     "listWorkOrders"
    ]
   },
   {
    "operationId": "getWorkOrder",
    "contract": "maintenance",
    "purpose": "Read a work order",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWorkOrders",
    "contract": "maintenance",
    "purpose": "List work orders",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "workOrderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A work order opened from a queue or an alert.",
   "preloaded": [
    "WorkOrderDetail.downtimeMinutes",
    "WorkOrderDetail.rootCause",
    "WorkOrderDetail.rootCauseNote",
    "WorkOrderDetail.escalatedAt",
    "WorkOrderDetail.escalationLevel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-030"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-031",
  "name": "Asset Register",
  "module": "Access & Venue",
  "requiresModule": "maintenance",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/access-point-configuration",
   "component": "apps/venue-management-web/src/routes/venue-operations/AccessPointConfigurationDetail.tsx",
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
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried seven asset operations.** A turnstile is an asset and configuring an access point is not asset management. **Rewired 20 August.** **Named `Access Point Configuration` and carried seven asset operations.** Same correction as BO-030 — F12 step 5 returns an asset to service here.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAssets` reads the population and `getAsset` reads one of them — list, select, act",
  "purpose": "Define what a gate is and where it is.",
  "gaps": [
   {
    "operation": "getAssetHistory",
    "why": "**1 declared operation reach no component on this screen**: getAssetHistory. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every asset register",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset register",
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
       "label": "Save changes",
       "operation": "updateAsset",
       "provenance": "contract maintenance.yaml PATCH /assets/{assetId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createAsset",
       "provenance": "contract maintenance.yaml POST /assets"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup",
       "operation": "lookupAsset",
       "provenance": "contract maintenance.yaml GET /assets/lookup"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAssetStatus",
       "provenance": "contract maintenance.yaml PUT /assets/{assetId}/status"
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
       "impliedBy": "updateAsset",
       "label": "Save asset",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAssets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupAsset",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateAsset",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset register list.",
   "error": "Could not load. Names which read failed and leaves the asset register untouched.",
   "emptyFirstRun": "No asset register yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset register are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
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
    "operationId": "createAsset",
    "contract": "maintenance",
    "purpose": "Register an asset",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
    ]
   },
   {
    "operationId": "getAsset",
    "contract": "maintenance",
    "purpose": "Read an asset with history and documents",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAssetHistory",
    "contract": "maintenance",
    "purpose": "Service history",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAssets",
    "contract": "maintenance",
    "purpose": "List assets",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupAsset",
    "contract": "maintenance",
    "purpose": "Find an asset by tag or QR",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAssetStatus",
    "contract": "maintenance",
    "purpose": "Take an asset out of service or return it",
    "trigger": "onAction",
    "invalidates": [
     "listAssets"
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
     "name": "assetId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "An asset opened from the register or a work order.",
   "preloaded": [
    "AssetDetail.openWorkOrders",
    "AssetDetail.maintenancePlans",
    "AssetDetail.documents"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-031"
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
  "id": "BO-032",
  "name": "Admission Profiles",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/admission-rules",
   "component": "apps/venue-management-web/src/routes/venue-operations/AdmissionProfilesDetail.tsx",
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
  "patternReason": "`listAdmissionRules` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Set the rules a gate enforces, including offline.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every admission profiles",
       "bindsTo": "AdmissionRules",
       "columns": [
        "AdmissionRules.id",
        "AdmissionRules.code",
        "AdmissionRules.perProductRules",
        "AdmissionRules.name",
        "AdmissionRules.openMinutesBefore",
        "AdmissionRules.closeMinutesAfter",
        "AdmissionRules.maxDurationMinutes",
        "AdmissionRules.requiresExitBeforeReentry",
        "AdmissionRules.maxReentries",
        "AdmissionRules.allowedAccessPointIds",
        "AdmissionRules.scopePath"
       ],
       "operation": "listAdmissionRules",
       "provenance": "contract access.yaml GET /admission-rules"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected admission profiles",
       "bindsTo": "AdmissionRules",
       "columns": [
        "AdmissionRules.id",
        "AdmissionRules.code",
        "AdmissionRules.perProductRules",
        "AdmissionRules.name",
        "AdmissionRules.openMinutesBefore",
        "AdmissionRules.closeMinutesAfter",
        "AdmissionRules.maxDurationMinutes",
        "AdmissionRules.requiresExitBeforeReentry",
        "AdmissionRules.maxReentries",
        "AdmissionRules.allowedAccessPointIds",
        "AdmissionRules.scopePath"
       ],
       "operation": "listAdmissionRules",
       "provenance": "contract access.yaml GET /admission-rules"
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
       "operation": "createAdmissionRules",
       "provenance": "contract access.yaml POST /admission-rules"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateAdmissionRules",
       "provenance": "contract access.yaml PUT /admission-rules/{profileId}"
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
       "impliedBy": "listAdmissionRules",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createAdmissionRules",
       "label": "Create admission profile",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAdmissionRules",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The admission profiles list.",
   "error": "Could not load. Names which read failed and leaves the admission profiles untouched.",
   "emptyFirstRun": "No admission profiles yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the admission profiles are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAdmissionRules",
    "contract": "access",
    "purpose": "List admission profiles",
    "trigger": "onLoad"
   },
   {
    "operationId": "createAdmissionRules",
    "contract": "access",
    "purpose": "Create an admission profile",
    "trigger": "onAction",
    "invalidates": [
     "listAdmissionRules"
    ]
   },
   {
    "operationId": "updateAdmissionRules",
    "contract": "access",
    "purpose": "Update an admission profile",
    "trigger": "onAction",
    "invalidates": [
     "listAdmissionRules"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "profileId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `profileId`.",
   "preloaded": [
    "AdmissionRules.id",
    "AdmissionRules.code",
    "AdmissionRules.perProductRules",
    "AdmissionRules.name",
    "AdmissionRules.openMinutesBefore"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-032"
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
  "id": "BO-033",
  "name": "Blacklist Management",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/blacklist-management",
   "component": "apps/venue-management-web/src/routes/venue-operations/BlacklistManagementDetail.tsx",
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
  "patternReason": "`listBlacklist` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Bar a media code outright.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every blacklist",
       "bindsTo": "BlacklistEntry",
       "columns": [
        "BlacklistEntry.mediaCode",
        "BlacklistEntry.reason",
        "BlacklistEntry.addedAt",
        "BlacklistEntry.addedByPrincipalId",
        "BlacklistEntry.expiresAt",
        "BlacklistEntry.scopePath"
       ],
       "operation": "listBlacklist",
       "provenance": "contract access.yaml GET /blacklist"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected blacklist",
       "bindsTo": "BlacklistEntry",
       "columns": [
        "BlacklistEntry.mediaCode",
        "BlacklistEntry.reason",
        "BlacklistEntry.addedAt",
        "BlacklistEntry.addedByPrincipalId",
        "BlacklistEntry.expiresAt",
        "BlacklistEntry.scopePath"
       ],
       "operation": "listBlacklist",
       "provenance": "contract access.yaml GET /blacklist"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add",
       "operation": "addBlacklistEntry",
       "provenance": "contract access.yaml POST /blacklist"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove",
       "operation": "removeBlacklistEntry",
       "provenance": "contract access.yaml DELETE /blacklist/{mediaCode}"
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
       "impliedBy": "listBlacklist",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "addBlacklistEntry",
       "label": "Add blacklist entry",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "removeBlacklistEntry",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "label": "Remove blacklist entry",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "addBlacklistEntry",
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
    "id": "confirmRemoveBlacklistEntry",
    "component": "confirmDialog",
    "trigger": "Remove",
    "body": "**Names what `removeBlacklistEntry` changes and what it leaves alone**, in the consequence rather than the verb. A blacklist this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml DELETE /blacklist/{mediaCode}"
   }
  ],
  "states": {
   "loading": "The blacklist list.",
   "error": "Could not load. Names which read failed and leaves the blacklist untouched.",
   "emptyFirstRun": "No blacklist yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the blacklist are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBlacklist",
    "contract": "access",
    "purpose": "List blacklisted media",
    "trigger": "onLoad"
   },
   {
    "operationId": "addBlacklistEntry",
    "contract": "access",
    "purpose": "Blacklist a media code",
    "trigger": "onAction",
    "invalidates": [
     "listBlacklist"
    ]
   },
   {
    "operationId": "removeBlacklistEntry",
    "contract": "access",
    "purpose": "Remove a blacklist entry",
    "trigger": "onAction",
    "invalidates": [
     "listBlacklist"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mediaCode",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mediaCode`.",
   "preloaded": [
    "BlacklistEntry.mediaCode",
    "BlacklistEntry.reason",
    "BlacklistEntry.addedAt",
    "BlacklistEntry.addedByPrincipalId",
    "BlacklistEntry.expiresAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-033"
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
 "acceptWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/accept",
  "contract": "maintenance",
  "summary": "The assignee takes the job",
  "permission": "MAINTENANCE_EXECUTE",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkOrder"
 },
 "addBlacklistEntry": {
  "method": "POST",
  "path": "/blacklist",
  "contract": "access",
  "summary": "Blacklist a media code",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "responds": "BlacklistEntry"
 },
 "approveRefund": {
  "method": "POST",
  "path": "/refunds/{refundId}/approve",
  "contract": "orders",
  "summary": "Approve a refund held for approval",
  "permission": "ORDER_REFUND_APPROVE",
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
  "responds": "Refund"
 },
 "attachWorkOrderEvidence": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/attachments",
  "contract": "maintenance",
  "summary": "Photo, video, document, note or signature",
  "permission": "MAINTENANCE_EXECUTE",
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
  "responds": "WorkOrderAttachment"
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
 "cancelPerformance": {
  "method": "POST",
  "path": "/performances/{performanceId}/cancel",
  "contract": "catalogue",
  "summary": "Cancel a performance",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "responds": "PerformanceCancellationResult"
 },
 "cancelWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/cancel",
  "contract": "maintenance",
  "summary": "Cancel a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
 },
 "closeWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/close",
  "contract": "maintenance",
  "summary": "Administratively closed",
  "permission": "MAINTENANCE_APPROVE",
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
  "responds": "WorkOrder"
 },
 "completeWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/complete",
  "contract": "maintenance",
  "summary": "Complete a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "responds": "WorkOrder"
 },
 "configureQueueFeed": {
  "method": "PUT",
  "path": "/queue-feeds",
  "contract": "queue",
  "summary": "Configure a sensor feed",
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
  "requestBody": "QueueFeed",
  "responds": "QueueFeed"
 },
 "createAdmissionRules": {
  "method": "POST",
  "path": "/admission-rules",
  "contract": "access",
  "summary": "Create an admission profile",
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
  "requestBody": "AdmissionRules",
  "responds": "AdmissionRules"
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
 "createBulkRefund": {
  "method": "POST",
  "path": "/refunds/bulk",
  "contract": "orders",
  "summary": "Refund every order against an event, performance or date",
  "permission": "ORDER_REFUND_BULK",
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
 "createCampaign": {
  "method": "POST",
  "path": "/campaigns",
  "contract": "marketing-crm",
  "summary": "Create a campaign",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "CreateCampaignRequest",
  "responds": "Campaign"
 },
 "createEvent": {
  "method": "POST",
  "path": "/events",
  "contract": "catalogue",
  "summary": "Create an event",
  "permission": "EVENT_CONFIGURE",
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
  "requestBody": "CreateEventRequest",
  "responds": "Event"
 },
 "createPerformances": {
  "method": "POST",
  "path": "/events/{eventId}/performances",
  "contract": "catalogue",
  "summary": "Create performances, singly or by schedule",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "requestBody": "CreatePerformancesRequest",
  "responds": null
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
 "createWorkOrder": {
  "method": "POST",
  "path": "/work-orders",
  "contract": "maintenance",
  "summary": "Raise a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "requestBody": "CreateWorkOrderRequest",
  "responds": "WorkOrder"
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
 "getCampaign": {
  "method": "GET",
  "path": "/campaigns/{campaignId}",
  "contract": "marketing-crm",
  "summary": "Read a campaign with performance",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CampaignDetail"
 },
 "getCampaignPerformance": {
  "method": "GET",
  "path": "/campaigns/{campaignId}/performance",
  "contract": "marketing-crm",
  "summary": "Delivery and engagement",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CampaignPerformance"
 },
 "getEvent": {
  "method": "GET",
  "path": "/events/{eventId}",
  "contract": "catalogue",
  "summary": "Read an event",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Event"
 },
 "getPerformance": {
  "method": "GET",
  "path": "/performances/{performanceId}",
  "contract": "catalogue",
  "summary": "Read a performance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Performance"
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
 "getQueueFeedHealth": {
  "method": "GET",
  "path": "/queue-feeds/{feedId}/health",
  "contract": "queue",
  "summary": "Feed health",
  "permission": "QUEUE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "QueueFeedHealth"
 },
 "getSeatAvailability": {
  "method": "GET",
  "path": "/performances/{performanceId}/seat-availability",
  "contract": "seating",
  "summary": "Seat status for a performance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "sectionCode",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "availableOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "mode",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatAvailability"
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
 "getWorkOrder": {
  "method": "GET",
  "path": "/work-orders/{workOrderId}",
  "contract": "maintenance",
  "summary": "Read a work order",
  "permission": "WORK_ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WorkOrderDetail"
 },
 "launchCampaign": {
  "method": "POST",
  "path": "/campaigns/{campaignId}/launch",
  "contract": "marketing-crm",
  "summary": "Launch or schedule a campaign",
  "permission": "MARKETING_SEND",
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
 "listAdmissionRules": {
  "method": "GET",
  "path": "/admission-rules",
  "contract": "access",
  "summary": "List admission profiles",
  "permission": "SCOPE_VIEW",
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
 "listBlacklist": {
  "method": "GET",
  "path": "/blacklist",
  "contract": "access",
  "summary": "List blacklisted media",
  "permission": "SCOPE_VIEW",
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
 "listCampaigns": {
  "method": "GET",
  "path": "/campaigns",
  "contract": "marketing-crm",
  "summary": "List campaigns",
  "permission": "MARKETING_VIEW",
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
 "listEvents": {
  "method": "GET",
  "path": "/events",
  "contract": "catalogue",
  "summary": "List events",
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
  "responds": "Page"
 },
 "listParkingFacilities": {
  "method": "GET",
  "path": "/parking-facilities",
  "contract": "access",
  "summary": "Car parks at a venue, and how each integrates",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "responds": "ParkingFacility"
 },
 "listPerformances": {
  "method": "GET",
  "path": "/events/{eventId}/performances",
  "contract": "catalogue",
  "summary": "List performances of an event",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "listQueueFeeds": {
  "method": "GET",
  "path": "/queue-feeds",
  "contract": "queue",
  "summary": "List configured sensor feeds",
  "permission": "QUEUE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "QueueFeed"
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
 "pauseCampaign": {
  "method": "POST",
  "path": "/campaigns/{campaignId}/pause",
  "contract": "marketing-crm",
  "summary": "Pause a campaign mid-send",
  "permission": "MARKETING_MANAGE",
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
 "recommendSeats": {
  "method": "POST",
  "path": "/performances/{performanceId}/seat-recommendations",
  "contract": "seating",
  "summary": "Recommend seats for a party",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "SeatRecommendationRequest",
  "responds": null
 },
 "removeBlacklistEntry": {
  "method": "DELETE",
  "path": "/blacklist/{mediaCode}",
  "contract": "access",
  "summary": "Remove a blacklist entry",
  "permission": "ACCESS_POINT_CONFIGURE",
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
 "setParkingFacility": {
  "method": "PUT",
  "path": "/parking-facilities",
  "contract": "access",
  "summary": "Configure a car park and its integration",
  "permission": "PARKING_CONFIGURE",
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
  "requestBody": "ParkingFacility",
  "responds": "ParkingFacility"
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
 "stopCampaign": {
  "method": "POST",
  "path": "/campaigns/{campaignId}/stop",
  "contract": "marketing-crm",
  "summary": "Stop a campaign mid-send",
  "permission": "MARKETING_SEND",
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
  "responds": "Campaign"
 },
 "testQueueFeed": {
  "method": "POST",
  "path": "/queue-feeds/{feedId}/test",
  "contract": "queue",
  "summary": "Test a feed before trusting it",
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
  "responds": "FeedTestResult"
 },
 "testSendCampaign": {
  "method": "POST",
  "path": "/campaigns/{campaignId}/test-send",
  "contract": "marketing-crm",
  "summary": "Send a test to named recipients",
  "permission": "MARKETING_MANAGE",
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
 "unscheduleCampaign": {
  "method": "POST",
  "path": "/campaigns/{campaignId}/unschedule",
  "contract": "marketing-crm",
  "summary": "Pull a scheduled campaign before it sends",
  "permission": "MARKETING_MANAGE",
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
 "updateAdmissionRules": {
  "method": "PUT",
  "path": "/admission-rules/{profileId}",
  "contract": "access",
  "summary": "Update an admission profile",
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
  "requestBody": "AdmissionRules",
  "responds": "AdmissionRules"
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
 "updateCampaign": {
  "method": "PATCH",
  "path": "/campaigns/{campaignId}",
  "contract": "marketing-crm",
  "summary": "Amend, pause or resume a campaign",
  "permission": "MARKETING_MANAGE",
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
  "responds": "Campaign"
 },
 "updateEvent": {
  "method": "PATCH",
  "path": "/events/{eventId}",
  "contract": "catalogue",
  "summary": "Amend an event",
  "permission": "EVENT_CONFIGURE",
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
  "responds": "Event"
 },
 "updatePerformance": {
  "method": "PATCH",
  "path": "/performances/{performanceId}",
  "contract": "catalogue",
  "summary": "Amend a performance",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "responds": "Performance"
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
 "verifyWorkOrder": {
  "method": "POST",
  "path": "/work-orders/{workOrderId}/verify",
  "contract": "maintenance",
  "summary": "Supervisor verification",
  "permission": "WORK_ORDER_VERIFY",
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
  "responds": "WorkOrder"
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
 "AdmissionRules": {
  "x-ticvai-persistence": "access.admission_rules",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "openMinutesBefore",
   "closeMinutesAfter"
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
   "perProductRules": {
    "type": "array",
    "description": "BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "entriesPerDay": {
       "type": "integer",
       "nullable": true
      },
      "minimumGapMinutes": {
       "type": "integer",
       "nullable": true,
       "description": "**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"
      },
      "allowedAccessPointIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "openMinutesBefore": {
    "type": "integer",
    "description": "How long before a performance validation opens."
   },
   "closeMinutesAfter": {
    "type": "integer"
   },
   "maxDurationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false
   },
   "maxReentries": {
    "type": "integer",
    "nullable": true
   },
   "allowedAccessPointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Empty means any access point in the venue."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
      "type": "integer"
     },
     "nextMaintenanceDueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "isMaintenanceOverdue": {
      "type": "boolean"
     },
     "lastInspectionAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
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
      "description": "Manuals, procedures, certificates. What a technician needs on site.",
      "items": {
       "type": "object",
       "properties": {
        "ref": {
         "type": "string"
        },
        "name": {
         "type": "string"
        },
        "kind": {
         "type": "string",
         "enum": [
          "manual",
          "sop",
          "certificate",
          "warranty",
          "drawing",
          "riskAssessment"
         ]
        }
       }
      }
     }
    }
   }
  ]
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
      "nullable": true
     }
    }
   }
  }
 },
 "BlacklistEntry": {
  "x-ticvai-persistence": "access.blacklist",
  "type": "object",
  "required": [
   "mediaCode",
   "reason",
   "addedAt",
   "addedByPrincipalId"
  ],
  "properties": {
   "mediaCode": {
    "type": "string"
   },
   "reason": {
    "type": "string"
   },
   "addedAt": {
    "type": "string",
    "format": "date-time"
   },
   "addedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "Campaign": {
  "x-ticvai-persistence": "marketing.campaign",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateCampaignRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "budgetCap": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "budgetSpent": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "readOnly": true,
      "description": "BL-169. **A campaign could spend without limit** — following the promotions `budgetCap` precedent. **Sending stops at the cap rather than overspending and reporting it**, because a marketing budget discovered after it was exceeded is a budget nobody set.\n"
     },
     "status": {
      "$ref": "#/components/schemas/CampaignStatus"
     },
     "isPaused": {
      "type": "boolean"
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "launchedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "completedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "CampaignContent": {
  "x-ticvai-persistence": "none — embedded in campaign",
  "type": "object",
  "required": [
   "templateId"
  ],
  "properties": {
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectOverride": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "mergeDefaults": {
    "type": "object",
    "additionalProperties": true
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Offer carried by the campaign. Coupon codes are issued from it."
   }
  }
 },
 "CampaignDetail": {
  "x-ticvai-persistence": "marketing.campaign",
  "allOf": [
   {
    "$ref": "#/components/schemas/Campaign"
   },
   {
    "type": "object",
    "properties": {
     "performance": {
      "$ref": "#/components/schemas/CampaignPerformance"
     }
    }
   }
  ]
 },
 "CampaignKind": {
  "type": "string",
  "enum": [
   "oneOff",
   "scheduled",
   "triggered",
   "recurring"
  ]
 },
 "CampaignPerformance": {
  "x-ticvai-persistence": "none — aggregated from dispatch",
  "type": "object",
  "required": [
   "campaignId",
   "sent",
   "delivered"
  ],
  "properties": {
   "campaignId": {
    "type": "string",
    "format": "uuid"
   },
   "sent": {
    "type": "integer"
   },
   "delivered": {
    "type": "integer"
   },
   "opened": {
    "type": "integer"
   },
   "clicked": {
    "type": "integer"
   },
   "bounced": {
    "type": "integer"
   },
   "complained": {
    "type": "integer"
   },
   "unsubscribed": {
    "type": "integer"
   },
   "attributedOrders": {
    "type": "integer"
   },
   "attributedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "attributionWindowDays": {
    "type": "integer"
   }
  }
 },
 "CampaignStatus": {
  "type": "string",
  "enum": [
   "draft",
   "scheduled",
   "sending",
   "paused",
   "completed",
   "stopped",
   "failed"
  ]
 },
 "CampaignTrigger": {
  "x-ticvai-persistence": "none — embedded in campaign",
  "type": "object",
  "properties": {
   "event": {
    "type": "string",
    "enum": [
     "bookingConfirmed",
     "visitCompleted",
     "membershipExpiring",
     "birthday",
     "abandonedCart",
     "firstVisit",
     "inactivity"
    ]
   },
   "delayHours": {
    "type": "integer"
   },
   "conditions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/SegmentCriterion"
    }
   }
  }
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
   "documentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "CreateCampaignRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "kind",
   "channel",
   "segmentId",
   "content"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "kind": {
    "$ref": "#/components/schemas/CampaignKind"
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "segmentId": {
    "type": "string",
    "format": "uuid"
   },
   "content": {
    "$ref": "#/components/schemas/CampaignContent"
   },
   "trigger": {
    "$ref": "#/components/schemas/CampaignTrigger"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time"
   },
   "consentPurpose": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ConsentPurpose"
     }
    ],
    "default": "marketing"
   },
   "sendWindow": {
    "type": "object",
    "description": "Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen.\n",
    "properties": {
     "startTime": {
      "type": "string"
     },
     "endTime": {
      "type": "string"
     },
     "timeZone": {
      "type": "string"
     }
    }
   }
  }
 },
 "CreateEventRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId"
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
   "parentEventId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "CreatePerformancesRequest": {
  "type": "object",
  "required": [
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "recurrence": {
    "type": "object",
    "description": "Generate a series rather than a single performance.",
    "properties": {
     "intervalMinutes": {
      "type": "integer",
      "minimum": 1
     },
     "until": {
      "type": "string",
      "format": "date-time"
     },
     "daysOfWeek": {
      "type": "array",
      "items": {
       "type": "integer",
       "minimum": 0,
       "maximum": 6
      }
     }
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
    "description": "**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\n",
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
   }
  }
 },
 "CreateWorkOrderRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "title",
   "venueId",
   "priority",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "title": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 5000
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
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderKind"
     }
    ],
    "default": "corrective"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "attachmentRefs": {
    "type": "array",
    "description": "Photo-first. Expected at creation, not added later from memory.",
    "items": {
     "type": "string"
    }
   },
   "takeAssetOutOfService": {
    "type": "boolean",
    "default": false,
    "description": "Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
 "Event": {
  "x-ticvai-persistence": "catalogue.event",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "scopePath"
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
   "parentEventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For grouped events."
   },
   "performanceCount": {
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "FeedTestResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed, discarded",
  "required": [
   "succeeded",
   "checks",
   "testedAt"
  ],
  "properties": {
   "succeeded": {
    "type": "boolean"
   },
   "checks": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "check",
      "passed"
     ],
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "reachable",
        "authenticated",
        "payloadParsed",
        "readingMapped",
        "withinInterval"
       ]
      },
      "passed": {
       "type": "boolean"
      },
      "detail": {
       "type": "string"
      },
      "latencyMs": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "sampleReading": {
    "allOf": [
     {
      "$ref": "#/components/schemas/QueueReading"
     }
    ],
    "description": "What the source actually returned, mapped. Shown so a configurer can see whether \"people count 4\" means four people or four groups before it drives a board.\n"
   },
   "rawSample": {
    "type": "string",
    "nullable": true,
    "description": "Truncated raw payload. The only way to diagnose a source that is reachable and returning a shape nobody mapped.\n"
   },
   "testedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MaintenancePlan": {
  "x-ticvai-persistence": "maintenance.maintenance_plan",
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
 "ParkingFacility": {
  "type": "object",
  "x-ticvai-persistence": "access.parking_facility",
  "required": [
   "name",
   "venueId",
   "mode"
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
   "mode": {
    "$ref": "#/components/schemas/ParkingIntegrationMode"
   },
   "capacity": {
    "type": "integer",
    "nullable": true
   },
   "takesPayment": {
    "type": "boolean",
    "readOnly": true,
    "default": false,
    "description": "**Always false, and stated rather than assumed** (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client decided on 14 August that it does not.\nAll three integration models are entitlement-based — the ticket carries the parking right and the platform pushes a plate or a code. **Pay-per-hour parking unrelated to a ticket runs on the parking system's own POS**, because taking that money here would make the venue an acquirer for parking, with a settlement path and a tax treatment nobody has designed.\nThe field exists so that a future reversal is a value change with a visible blast radius, rather than a silent gap somebody rediscovers.\n"
   },
   "vendorSwapTargetDays": {
    "type": "integer",
    "readOnly": true,
    "default": 5,
    "description": "**A new parking vendor should take days, not weeks** — Qossai, 14 August. The team has integrated parking APIs before and the architecture is expected to make the next one cheap.\nRecorded as a design constraint rather than a runtime value: **everything vendor-specific lives in `vendorName`, `endpoint` and `credentialRef`**, and the three modes are the adaptor surface (ADR-0012). A vendor needing a fourth mode is the signal this has been violated.\n"
   },
   "vendorName": {
    "type": "string",
    "nullable": true
   },
   "endpoint": {
    "type": "string",
    "nullable": true
   },
   "credentialRef": {
    "type": "string",
    "nullable": true,
    "description": "A vault reference, never the credential."
   },
   "pushLeadMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "How far ahead of the visit a plate is pushed. **Too early and the whitelist fills with cars that will not arrive; too late and the guest is at the barrier.**\n"
   },
   "accessPointIds": {
    "type": "array",
    "description": "Where the platform validates its own code, in `none` and `qrHandoff` modes.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ParkingIntegrationMode": {
  "type": "string",
  "description": "CF-52, settled 14 August. **Not variations of one thing** — each decides what happens at sale and what a guest presents at the barrier.\n",
  "enum": [
   "none",
   "plateWhitelist",
   "qrHandoff"
  ]
 },
 "Performance": {
  "x-ticvai-persistence": "catalogue.performance",
  "type": "object",
  "required": [
   "id",
   "eventId",
   "startsAt",
   "endsAt",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"
   },
   "requiresApprovalToCancel": {
    "type": "boolean",
    "default": true,
    "description": "**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "scheduled",
     "onSale",
     "soldOut",
     "suspended",
     "cancelled",
     "completed"
    ]
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "PerformanceCancellationResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "performanceId",
   "dryRun",
   "affectedOrders",
   "refundExposure"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "dryRun": {
    "type": "boolean"
   },
   "affectedOrders": {
    "type": "integer"
   },
   "affectedGuests": {
    "type": "integer"
   },
   "refundExposure": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the cancellation costs. Returned before committing, so the person cancelling sees the number at the moment they decide.\n"
   },
   "bulkRefundBatchId": {
    "type": "string",
    "nullable": true,
    "description": "Queued for approval. Refunds are not issued automatically."
   },
   "notificationsQueued": {
    "type": "integer"
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
 "QueueFeed": {
  "x-ticvai-persistence": "queue.feed",
  "type": "object",
  "required": [
   "id",
   "queueId",
   "adaptor",
   "isEnabled"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "adaptor": {
    "$ref": "#/components/schemas/QueueFeedAdaptor"
   },
   "adaptorName": {
    "type": "string",
    "nullable": true,
    "description": "Named vendor where `adaptor` is `vendorAdaptor`."
   },
   "credentialsRef": {
    "type": "string",
    "nullable": true,
    "description": "Key vault reference. Credentials are never returned."
   },
   "expectedIntervalSeconds": {
    "type": "integer",
    "default": 60,
    "description": "Beyond this without a reading, the feed is considered quiet."
   },
   "isEnabled": {
    "type": "boolean"
   }
  }
 },
 "QueueFeedAdaptor": {
  "type": "string",
  "description": "Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and demonstrated with no vendor at all.\n",
  "enum": [
   "generic",
   "mock",
   "vendorAdaptor"
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
 "QueueReading": {
  "x-ticvai-persistence": "queue.reading",
  "type": "object",
  "required": [
   "id",
   "kind",
   "value",
   "observedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "kind": {
    "type": "string",
    "description": "Deliberately narrow. Anything richer would couple the platform to one vendor's model of a queue.\n",
    "enum": [
     "peopleCount",
     "dwellSeconds",
     "throughputPerHour",
     "queueLengthMetres"
    ]
   },
   "value": {
    "type": "number",
    "minimum": 0
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "observedAt": {
    "type": "string",
    "format": "date-time"
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
 "ResolutionCode": {
  "type": "string",
  "enum": [
   "repaired",
   "partReplaced",
   "adjusted",
   "cleaned",
   "noFaultFound",
   "referredExternal",
   "replaced",
   "deferred"
  ]
 },
 "SeatAvailability": {
  "x-ticvai-persistence": "none — computed from seat, hold and block",
  "type": "object",
  "required": [
   "performanceId",
   "seatMapId",
   "totals",
   "seats"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "totals": {
    "type": "object",
    "properties": {
     "total": {
      "type": "integer"
     },
     "available": {
      "type": "integer"
     },
     "held": {
      "type": "integer"
     },
     "sold": {
      "type": "integer"
     },
     "blocked": {
      "type": "integer"
     },
     "buffered": {
      "type": "integer"
     }
    }
   },
   "byCategory": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "categoryId": {
       "type": "string",
       "format": "uuid"
      },
      "available": {
       "type": "integer"
      },
      "sold": {
       "type": "integer"
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "seats": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "seatId",
      "status"
     ],
     "properties": {
      "seatId": {
       "type": "string"
      },
      "status": {
       "$ref": "#/components/schemas/SeatStatus"
      },
      "categoryId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "SeatRecommendationRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "partySize",
   "strategy"
  ],
  "properties": {
   "partySize": {
    "type": "integer",
    "minimum": 1,
    "maximum": 50
   },
   "strategy": {
    "$ref": "#/components/schemas/SeatRecommendationStrategy"
   },
   "categoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "maxPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "accessibleCount": {
    "type": "integer",
    "default": 0,
    "description": "Wheelchair spaces in the party. Companions are added automatically."
   },
   "maxOptions": {
    "type": "integer",
    "default": 3,
    "maximum": 10
   }
  }
 },
 "SeatRecommendationStrategy": {
  "type": "string",
  "enum": [
   "bestAvailable",
   "bestValue",
   "closestToStage",
   "accessible",
   "contiguous"
  ]
 },
 "SeatStatus": {
  "type": "string",
  "enum": [
   "available",
   "held",
   "sold",
   "blocked",
   "buffered",
   "unavailable"
  ]
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
 },
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
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
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n"
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
    "type": "string"
   },
   "workOrderNumber": {
    "type": "string"
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
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
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
   "elapsedMinutes": {
    "type": "integer"
   },
   "isTimerRunning": {
    "type": "boolean"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean"
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
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
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
 "WorkOrderAttachment": {
  "type": "object",
  "x-ticvai-persistence": "maintenance.work_order_attachment",
  "required": [
   "id",
   "workOrderId",
   "kind",
   "capturedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "workOrderId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "photo",
     "video",
     "document",
     "note",
     "signature"
    ]
   },
   "assetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "text": {
    "type": "string",
    "nullable": true
   },
   "stage": {
    "type": "string",
    "enum": [
     "before",
     "during",
     "after",
     "signOff"
    ],
    "nullable": true
   },
   "capturedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "capturedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time. **Distinct from when it synced** — a photo taken at 09:14 in a basement and uploaded at 11:40 is evidence of the first, not the second.\n"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkOrderDetail": {
  "x-ticvai-persistence": "maintenance.work_order",
  "allOf": [
   {
    "$ref": "#/components/schemas/WorkOrder"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string",
      "nullable": true
     },
     "resolution": {
      "type": "string",
      "nullable": true
     },
     "resolutionCode": {
      "$ref": "#/components/schemas/ResolutionCode"
     },
     "attachmentRefs": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "timeEntries": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "action": {
         "type": "string"
        },
        "principalId": {
         "type": "string",
         "format": "uuid"
        },
        "pauseReason": {
         "type": "string",
         "nullable": true
        },
        "recordedAt": {
         "type": "string",
         "format": "date-time"
        }
       }
      }
     },
     "parts": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "inventoryItemId": {
         "type": "string",
         "format": "uuid"
        },
        "itemName": {
         "type": "string"
        },
        "quantity": {
         "type": "number"
        },
        "cost": {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       }
      }
     },
     "labourCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "partsCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "totalCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "verifiedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   }
  ]
 },
 "WorkOrderKind": {
  "type": "string",
  "enum": [
   "corrective",
   "planned",
   "inspectionFollowUp",
   "incidentCorrective",
   "improvement"
  ]
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
 },
 "WorkOrderStatus": {
  "type": "string",
  "enum": [
   "open",
   "assigned",
   "inProgress",
   "paused",
   "awaitingParts",
   "completed",
   "verified",
   "closed",
   "cancelled"
  ]
 }
}
```
