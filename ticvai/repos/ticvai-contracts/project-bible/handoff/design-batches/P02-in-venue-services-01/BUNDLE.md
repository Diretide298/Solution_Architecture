# P02-in-venue-services-01 — P02 · In-venue Services

**10 screens · 28 operations · 40 schemas · 7 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCESS_POINT_CONFIGURE, ORDER_MODIFY, PRODUCT_VIEW, QUEUE_VIEW, RESOURCE_BOOK, RESOURCE_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **8 of these operations work offline**: getTenantAppStatus, getVenueMap, getVenueMapGraph, getWaitTimes, joinRestaurantWaitlist, listParkingFacilities, listProducts, listQueues
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-021` | Interactive Map | listDetail | 4 | 0 | — |
| `GST-022` | Attraction Wait Times | statusTracker | 1 | 0 | — |
| `GST-023` | Virtual Queue | statusTracker | 5 | 0 | — |
| `GST-024` | F&B – Browse & Order | listDetail | 8 | 0 | — |
| `GST-025` | F&B – Order Tracking | statusTracker | 3 | 0 | — |
| `GST-027` | Parking – Reserve & Pay | listDetail | 3 | 0 | — |
| `GST-028` | Parking – Reservation Confirmed | listDetail | 2 | 0 | — |
| `GST-029` | Venue Info & Services | listDetail | 2 | 0 | — |
| `GST-038` | Digital Companion Mode | listDetail | 3 | 0 | — |
| `GST-070` | Reserve a Table or Cabana | statusTracker | 7 | 0 | — |

## Thin screens in this batch

**GST-022, GST-023, GST-025, GST-028, GST-029, GST-038 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-021",
  "name": "Interactive Map",
  "module": "In-venue Services",
  "requiresModule": "seating",
  "wave": 2,
  "capability": "C39",
  "implementation": {
   "app": "guest-app",
   "route": "/general/interactive-map",
   "component": "apps/guest-app/src/routes/general/InteractiveMapCanvas.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-022"
   ],
   "transitions": [
    {
     "to": "GST-022",
     "trigger": "They compare waits across attractions",
     "provenance": "flow F48 step 1→2"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    },
    {
     "to": "BO-096",
     "trigger": "The attendant checks what is free for the requested window",
     "provenance": "flow F25 step 1→2",
     "operation": "getVenueMap",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired to the venue map 18 August (CF-123).** The whole map arrives in one call and the client filters locally — which is also what makes it work with no signal in the middle of a park. **Routing happens on the device.** The platform guarantees the graph — connected, versioned, with step-free marked — and the client walks it, because a phone with the graph cached routes with no signal and a server round-trip per step does not. **The version is how a stale route is caught**: a guest holding a route across a path that closed this morning gets told, rather than walking into a barrier. **Drawn 26 August** — `Seat Board 4.dc.html` frame `seat-4b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "openQuestions": [
   "Inventory cites `GET /venue-map` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "boardFrames": [
   "Seat Board 4.dc.html#seat-4b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "See where things are in relation to each other.",
  "gaps": [
   {
    "operation": "getVenueMap",
    "why": "**2 declared operations reach no component on this screen**: getVenueMap, getVenueMapGraph. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every interactive map",
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
       "label": "The selected interactive map",
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
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listProducts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getVenueMap",
       "notes": "One record, read-only.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The interactive map list.",
   "error": "Could not load. Names which read failed and leaves the interactive map untouched.",
   "emptyFirstRun": "No interactive map yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the interactive map are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** A map and route graph already loaded stay usable, so directions do not need a signal. Wait times show their last reading marked out of date, never as live — a queue length from an hour ago sends a guest to the wrong ride. With no map loaded yet, the screen asks the guest to reconnect."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVenueMap",
    "contract": "venue-map",
    "purpose": "A map with its points and paths",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVenueMapGraph",
    "contract": "venue-map",
    "purpose": "The navigation graph, ready to route over",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mapId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `mapId`.",
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
   "board": "wireframes/P02 Guest App.dc.html#gst-021",
   "note": "**Drawn by Claude Design on `Seat Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-022",
  "name": "Attraction Wait Times",
  "module": "In-venue Services",
  "requiresModule": "queue",
  "wave": 2,
  "capability": "C82",
  "implementation": {
   "app": "guest-app",
   "route": "/general/attraction-wait-times",
   "component": "apps/guest-app/src/routes/general/AttractionWaitTimesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-021"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-023",
    "GST-059"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-003",
     "trigger": "Picks something shorter from the attractions list",
     "provenance": "flow F21 step 1→2",
     "operation": "getWaitTimes"
    },
    {
     "to": "GST-023",
     "trigger": "They join a virtual queue rather than stand in it",
     "provenance": "flow F48 step 2→3",
     "operation": "getWaitTimes"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-059",
     "trigger": "Plan My Day – In Progress",
     "carries": [
      "suggestionId"
     ],
     "provenance": "derived — GST-059 declares entryState.params suggestionId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Pulled to Wave 2 (CF-101) with the queue platform F21 runs on.",
  "openQuestions": [
   "Inventory cites `GET /queue/wait-times` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getWaitTimes` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See attraction wait times for this venue.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected attraction wait times",
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
    }
   ]
  },
  "states": {
   "loading": "The attraction wait times list.",
   "error": "Could not load. Names which read failed and leaves the attraction wait times untouched.",
   "emptyFirstRun": "No attraction wait times yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attraction wait times are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** A map and route graph already loaded stay usable, so directions do not need a signal. Wait times show their last reading marked out of date, never as live — a queue length from an hour ago sends a guest to the wrong ride. With no map loaded yet, the screen asks the guest to reconnect."
  },
  "apis": [
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-022"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-023",
  "name": "Virtual Queue",
  "module": "In-venue Services",
  "requiresModule": "queue",
  "wave": 3,
  "capability": "C82",
  "implementation": {
   "app": "guest-app",
   "route": "/general/virtual-queue-join-queue",
   "component": "apps/guest-app/src/routes/general/VirtualQueueJoinQueueDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-022"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-024"
   ],
   "transitions": [
    {
     "to": "GST-024",
     "trigger": "While waiting, they order food to where they are sitting",
     "provenance": "flow F48 step 3→4"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Renamed 31 August** from *Virtual Queue / Join Queue*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added getWaitTimes. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getWaitingGuest` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Find the right one quickly, and act on it without opening it.",
  "gaps": [
   {
    "operation": "getWaitTimes",
    "why": "**1 declared operation reach no component on this screen**: getWaitTimes. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected virtual queue",
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
       "operation": "getWaitingGuest",
       "provenance": "contract queue.yaml GET /waiting-guests/{entryId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Join",
       "operation": "joinQueue",
       "provenance": "contract queue.yaml POST /waiting-guests"
      },
      {
       "kind": "secondaryButton",
       "label": "Leave",
       "operation": "leaveQueue",
       "provenance": "contract queue.yaml DELETE /waiting-guests/{entryId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual queue list.",
   "error": "Could not load. Names which read failed and leaves the virtual queue untouched.",
   "emptyFirstRun": "No virtual queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the virtual queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** The guest's place stays on screen with its age, so they can see they hold it. Joining and leaving need the connection — a place taken offline is a place nobody else can see."
  },
  "apis": [
   {
    "operationId": "joinQueue",
    "contract": "queue",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaitingGuest",
    "contract": "queue",
    "purpose": "Read a queue entry",
    "trigger": "onLoad"
   },
   {
    "operationId": "leaveQueue",
    "contract": "queue",
    "purpose": "Leave a queue",
    "trigger": "onAction"
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "Which virtual queues are running",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entryId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `entryId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-023"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-024",
  "name": "F&B – Browse & Order",
  "module": "In-venue Services",
  "requiresModule": "fnb",
  "wave": 2,
  "capability": "C05",
  "implementation": {
   "app": "guest-app",
   "route": "/general/fandb-browse-and-order",
   "component": "apps/guest-app/src/routes/general/FandbBrowseAndOrderList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-023"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-009",
    "GST-025"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-009",
     "trigger": "Pays",
     "provenance": "flow F11 step 3→4",
     "operation": "createGuestFnbOrder"
    },
    {
     "to": "GST-025",
     "trigger": "They watch the order progress",
     "provenance": "flow F48 step 4→5"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "The inventory cited `GET /menu`, which never existed. Now getGuestMenu. Ordering to a cabana or a seat uses the same claimLocationSession as a table (4.6.26). States derived from the screen pattern on 17 August, not individually considered. **Cross-surface parity, 31 August**: added claimTableSession, listModifierGroups. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads the population and `getGuestMenu` reads one of them — list, select, act",
  "purpose": "Order food to where the guest is sitting, or for collection.",
  "gaps": [
   {
    "operation": "getGuestOrderStatus",
    "why": "**3 declared operations reach no component on this screen**: getGuestOrderStatus, listDeliveryLocations, listModifierGroups. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every browse order",
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
       "label": "The selected browse order",
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
       "label": "Claim",
       "operation": "claimLocationSession",
       "provenance": "contract fnb.yaml POST /location-sessions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createGuestFnbOrder",
       "provenance": "contract fnb.yaml POST /guest-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Claim",
       "operation": "claimTableSession",
       "provenance": "contract fnb.yaml POST /table-sessions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The browse order list.",
   "error": "Could not load. Names which read failed and leaves the browse order untouched.",
   "emptyFirstRun": "No browse order yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the browse order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** The menu already loaded stays with its age. Ordering, claiming a table and booking wait for the connection — an order placed offline is food nobody is making."
  },
  "apis": [
   {
    "operationId": "listDiningOutlets",
    "contract": "fnb",
    "purpose": "Outlets open now, with ordering method",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestMenu",
    "contract": "fnb",
    "purpose": "The menu in force at this moment",
    "trigger": "onLoad"
   },
   {
    "operationId": "claimLocationSession",
    "contract": "fnb",
    "purpose": "Scan the table, cabana or sunbed code",
    "trigger": "onLoad"
   },
   {
    "operationId": "createGuestFnbOrder",
    "contract": "fnb",
    "purpose": "Place the order",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestOrderStatus",
    "contract": "fnb",
    "purpose": "Track an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDeliveryLocations",
    "contract": "fnb",
    "purpose": "Where an order can be delivered",
    "trigger": "onLoad"
   },
   {
    "operationId": "claimTableSession",
    "contract": "fnb",
    "purpose": "Identify which table a guest is sitting at",
    "trigger": "onAction",
    "invalidates": [
     "listDiningOutlets"
    ]
   },
   {
    "operationId": "listModifierGroups",
    "contract": "fnb",
    "purpose": "List modifier groups",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "outletId",
     "from": "deepLink"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
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
   "board": "wireframes/P02 Guest App.dc.html#gst-024"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-025",
  "name": "F&B – Order Tracking",
  "module": "In-venue Services",
  "requiresModule": "fnb",
  "wave": 2,
  "capability": "C05",
  "implementation": {
   "app": "guest-app",
   "route": "/general/fandb-order-tracking",
   "component": "apps/guest-app/src/routes/general/FandbOrderTrackingDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-024"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-030"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-030",
     "trigger": "Their queue place comes up and they are told",
     "provenance": "flow F48 step 5→6"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    },
    {
     "to": "BO-021",
     "trigger": "Runner delivers to the lounger",
     "provenance": "flow F11 step 6→7",
     "operation": "getGuestOrderStatus",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Nine states from 4.6.35. Collected and delivered are distinct from served — a counter handover, a runner delivery and a server putting a plate down are three different events. States derived from the screen pattern on 17 August, not individually considered. **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted. **Cross-platform navigation removed 24 August**: BO-021. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Track an order to the point it reaches the guest.",
  "gaps": [
   {
    "operation": "getGuestBill",
    "why": "**1 declared operation reach no component on this screen**: getGuestBill. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order tracking",
       "bindsTo": "GuestOrderStatus",
       "columns": [
        "GuestOrderStatus.orderId",
        "GuestOrderStatus.orderNumber",
        "GuestOrderStatus.status",
        "GuestOrderStatus.estimatedReadyAt",
        "GuestOrderStatus.isReadyForCollection",
        "GuestOrderStatus.lines"
       ],
       "operation": "getGuestOrderStatus",
       "provenance": "contract fnb.yaml GET /guest-orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Claim",
       "operation": "claimTableSession",
       "provenance": "contract fnb.yaml POST /table-sessions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Availability is live, never cached",
   "error": "Availability unavailable. **Selection is blocked** — overselling is worse than waiting",
   "emptyFirstRun": "**Sold out is a real answer.** Offers the next available rather than a dead end",
   "emptyNoResults": "The filter narrowed it and the order tracking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** The last status stays on screen with its age and is never presented as current. Settling the bill waits for the connection."
  },
  "apis": [
   {
    "operationId": "getGuestOrderStatus",
    "contract": "fnb",
    "purpose": "Ordered → accepted → in preparation → ready → served, collected or delivered",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestBill",
    "contract": "fnb",
    "purpose": "Everything ordered at this location this sitting",
    "trigger": "onLoad"
   },
   {
    "operationId": "claimTableSession",
    "contract": "fnb",
    "purpose": "Identify which table a guest is sitting at",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "sessionId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-025"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-027",
  "name": "Parking – Reserve & Pay",
  "module": "In-venue Services",
  "requiresModule": "access",
  "wave": 3,
  "capability": "C23",
  "implementation": {
   "app": "guest-app",
   "route": "/general/parking-reserve-and-pay",
   "component": "apps/guest-app/src/routes/general/ParkingReserveAndPayDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-028"
   ],
   "transitions": [
    {
     "to": "GST-028",
     "trigger": "It is confirmed with a facility and a bay type",
     "provenance": "flow F50 step 1→2",
     "operation": "createParkingEntitlement"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`createParkingEntitlement` is declared `service` audience and this is a guest screen.** Either the guest calls it — in which case the audience is wrong — or a guest-scoped operation is missing and the screen is drawing an act it cannot perform. **Recorded 24 August rather than guessed**: `updateParkingEntitlement` is already `guest`, which makes the asymmetry look like an omission rather than a design. **Cross-surface parity, 31 August**: added listParkingFacilities. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.",
  "openQuestions": [
   "Inventory cites `POST /parking-reservations` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listParkingFacilities` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Take the money, and be unambiguous about whether it worked.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every parking reserve pay",
       "bindsTo": "ParkingFacility",
       "columns": [
        "ParkingFacility.id",
        "ParkingFacility.name",
        "ParkingFacility.venueId",
        "ParkingFacility.mode",
        "ParkingFacility.capacity",
        "ParkingFacility.takesPayment",
        "ParkingFacility.vendorSwapTargetDays",
        "ParkingFacility.vendorName",
        "ParkingFacility.endpoint",
        "ParkingFacility.credentialRef",
        "ParkingFacility.pushLeadMinutes",
        "ParkingFacility.accessPointIds"
       ],
       "operation": "listParkingFacilities",
       "provenance": "contract access.yaml GET /parking-facilities"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected parking reserve pay",
       "bindsTo": "ParkingFacility",
       "columns": [
        "ParkingFacility.id",
        "ParkingFacility.name",
        "ParkingFacility.venueId",
        "ParkingFacility.mode",
        "ParkingFacility.capacity",
        "ParkingFacility.takesPayment",
        "ParkingFacility.vendorSwapTargetDays",
        "ParkingFacility.vendorName",
        "ParkingFacility.endpoint",
        "ParkingFacility.credentialRef",
        "ParkingFacility.pushLeadMinutes",
        "ParkingFacility.accessPointIds",
        "ParkingFacility.isActive"
       ],
       "operation": "listParkingFacilities",
       "provenance": "contract access.yaml GET /parking-facilities"
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
       "operation": "createParkingEntitlement",
       "provenance": "contract access.yaml POST /parking-entitlements"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateParkingEntitlement",
       "provenance": "contract access.yaml PATCH /parking-entitlements/{entitlementId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Terminal or gateway state, shown plainly",
   "error": "**Declined reads differently from unresolved.** An unresolved payment inquires rather than retries, and nothing is issued until it resolves",
   "emptyFirstRun": "—",
   "emptyNoResults": "The filter narrowed it and the parking reserve pay are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection."
  },
  "apis": [
   {
    "operationId": "createParkingEntitlement",
    "contract": "access",
    "purpose": "A guest bought parking",
    "trigger": "onAction",
    "invalidates": [
     "listParkingFacilities"
    ]
   },
   {
    "operationId": "updateParkingEntitlement",
    "contract": "access",
    "purpose": "Change the plate, or revoke",
    "trigger": "onAction",
    "invalidates": [
     "listParkingFacilities"
    ]
   },
   {
    "operationId": "listParkingFacilities",
    "contract": "access",
    "purpose": "Car parks at a venue, and how each integrates",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entitlementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A ticket link opened after the event.** Shows the entitlement with its status — expired, used, transferred — because *not found* to somebody holding a ticket is the wrong answer.",
   "preloaded": [
    "ParkingFacility.id",
    "ParkingFacility.name",
    "ParkingFacility.venueId",
    "ParkingFacility.mode",
    "ParkingFacility.capacity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-027"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-028",
  "name": "Parking – Reservation Confirmed",
  "module": "In-venue Services",
  "requiresModule": "access",
  "wave": 3,
  "capability": "C23",
  "implementation": {
   "app": "guest-app",
   "route": "/general/parking-reservation-confirmed",
   "component": "apps/guest-app/src/routes/general/ParkingReservationConfirmedDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-027"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-012"
   ],
   "transitions": [
    {
     "to": "GST-012",
     "trigger": "They open their tickets",
     "provenance": "flow F50 step 2→3"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`createParkingEntitlement` is declared `service` audience and this is a guest screen.** Either the guest calls it — in which case the audience is wrong — or a guest-scoped operation is missing and the screen is drawing an act it cannot perform. **Recorded 24 August rather than guessed**: `updateParkingEntitlement` is already `guest`, which makes the asymmetry look like an omission rather than a design.",
  "openQuestions": [
   "Inventory cites `GET /parking-reservations/{id}` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listParkingFacilities` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Confirm it worked, and give them what they need to prove it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every parking reservation confirmed",
       "bindsTo": "ParkingFacility",
       "columns": [
        "ParkingFacility.id",
        "ParkingFacility.name",
        "ParkingFacility.venueId",
        "ParkingFacility.mode",
        "ParkingFacility.capacity",
        "ParkingFacility.takesPayment",
        "ParkingFacility.vendorSwapTargetDays",
        "ParkingFacility.vendorName",
        "ParkingFacility.endpoint",
        "ParkingFacility.credentialRef",
        "ParkingFacility.pushLeadMinutes",
        "ParkingFacility.accessPointIds"
       ],
       "operation": "listParkingFacilities",
       "provenance": "contract access.yaml GET /parking-facilities"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected parking reservation confirmed",
       "bindsTo": "ParkingFacility",
       "columns": [
        "ParkingFacility.id",
        "ParkingFacility.name",
        "ParkingFacility.venueId",
        "ParkingFacility.mode",
        "ParkingFacility.capacity",
        "ParkingFacility.takesPayment",
        "ParkingFacility.vendorSwapTargetDays",
        "ParkingFacility.vendorName",
        "ParkingFacility.endpoint",
        "ParkingFacility.credentialRef",
        "ParkingFacility.pushLeadMinutes",
        "ParkingFacility.accessPointIds",
        "ParkingFacility.isActive"
       ],
       "operation": "listParkingFacilities",
       "provenance": "contract access.yaml GET /parking-facilities"
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
       "operation": "createParkingEntitlement",
       "provenance": "contract access.yaml POST /parking-entitlements"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The parking reservation confirmed list.",
   "error": "Could not load. Names which read failed and leaves the parking reservation confirmed untouched.",
   "emptyFirstRun": "No parking reservation confirmed yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the parking reservation confirmed are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection."
  },
  "apis": [
   {
    "operationId": "createParkingEntitlement",
    "contract": "access",
    "purpose": "A guest bought parking",
    "trigger": "onAction",
    "invalidates": [
     "listParkingFacilities"
    ]
   },
   {
    "operationId": "listParkingFacilities",
    "contract": "access",
    "purpose": "Car parks at a venue, and how each integrates",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ParkingFacility.id",
    "ParkingFacility.name",
    "ParkingFacility.venueId",
    "ParkingFacility.mode",
    "ParkingFacility.capacity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-028"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-029",
  "name": "Venue Info & Services",
  "module": "In-venue Services",
  "requiresModule": "fnb",
  "wave": 2,
  "capability": "C17",
  "implementation": {
   "app": "guest-app",
   "route": "/general/venue-info-and-services",
   "component": "apps/guest-app/src/routes/general/VenueInfoAndServicesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "Inventory cites `GET /venue-info` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See venue info & services for this venue.",
  "gaps": [
   {
    "operation": "listDeliveryLocations",
    "why": "**1 declared operation reach no component on this screen**: listDeliveryLocations. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every venue info services",
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
       "label": "The selected venue info services",
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
    }
   ]
  },
  "states": {
   "loading": "The venue info services list.",
   "error": "Could not load. Names which read failed and leaves the venue info services untouched.",
   "emptyFirstRun": "No venue info services yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue info services are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
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
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
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
   "board": "wireframes/P02 Guest App.dc.html#gst-029"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-038",
  "name": "Digital Companion Mode",
  "module": "In-venue Services",
  "requiresModule": "queue",
  "wave": 3,
  "capability": "C105",
  "implementation": {
   "app": "guest-app",
   "route": "/general/digital-companion-mode",
   "component": "apps/guest-app/src/routes/general/DigitalCompanionModeDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Not minuted and not in the matrix.** The only unsourced screen of the eight audited on 17 August — it reads as a framing for the in-venue capabilities rather than a capability of its own, and CF-92 asks whether it is a real screen or a name for a mode.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getTenantAppStatus` reads one of them — list, select, act",
  "purpose": "The in-venue home: your tickets, the map, and what is near you.",
  "gaps": [
   {
    "operation": "getWaitTimes",
    "why": "**1 declared operation reach no component on this screen**: getWaitTimes. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every digital companion mode",
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
       "label": "The selected digital companion mode",
       "bindsTo": "TenantAppStatus",
       "columns": [
        "TenantAppStatus.isPublished",
        "TenantAppStatus.publishedVersion",
        "TenantAppStatus.publishedAt",
        "TenantAppStatus.draftVersion",
        "TenantAppStatus.hasUnpublishedChanges",
        "TenantAppStatus.activeModuleCount",
        "TenantAppStatus.licensedModuleCount",
        "TenantAppStatus.activePageCount",
        "TenantAppStatus.isInMaintenance",
        "TenantAppStatus.maintenanceMessage",
        "TenantAppStatus.expectedBackAt",
        "TenantAppStatus.recentChanges"
       ],
       "operation": "getTenantAppStatus",
       "provenance": "contract white-label.yaml GET /tenant-config/status"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital companion mode list.",
   "error": "Could not load. Names which read failed and leaves the digital companion mode untouched.",
   "emptyFirstRun": "No digital companion mode yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital companion mode are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "App status and recent changes",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "TenantAppStatus.isPublished",
    "TenantAppStatus.publishedVersion",
    "TenantAppStatus.publishedAt",
    "TenantAppStatus.draftVersion",
    "TenantAppStatus.hasUnpublishedChanges"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-038"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-070",
  "name": "Reserve a Table or Cabana",
  "module": "In-venue Services",
  "requiresModule": "core",
  "wave": 2,
  "capability": "read-write",
  "implementation": {
   "app": "guest-app",
   "route": "/account/reserve-table-cabana",
   "component": "apps/guest-app/src/routes/account/ReserveTableCabana.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "GST-039"
   ],
   "entryFrom": [
    "GST-001"
   ],
   "inferred": false,
   "notes": "**Reached from GST-001** — a top-level section of the app. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Staff could book a table and a guest could not.** Seven guest-callable operations with no guest surface — reservations, cabanas, and both waitlists.\n\n**Leaving a waitlist matters as much as joining one.** A guest who has given up and walked away still holds a place, and a queue full of people who left is a queue nobody trusts.",
  "density": "comfortable",
  "offline": false,
  "pattern": "statusTracker",
  "patternReason": "`getResourceAvailability` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "**Staff could book a table and a guest could not.** Seven guest-callable operations with no guest surface — reservations, cabanas, and both waitlists.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reserve table cabana",
       "bindsTo": "ResourceAvailability",
       "columns": [
        "ResourceAvailability.resourceId",
        "ResourceAvailability.freeWindows",
        "ResourceAvailability.blockedWindows"
       ],
       "operation": "getResourceAvailability",
       "provenance": "contract resources.yaml GET /resources/{resourceId}/availability"
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
       "operation": "createTableReservation",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateTableReservation",
       "provenance": "contract fnb.yaml PATCH /table-reservations/{reservationId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Book",
       "operation": "bookResource",
       "provenance": "contract resources.yaml POST /resource-bookings"
      },
      {
       "kind": "secondaryButton",
       "label": "Join",
       "operation": "joinRestaurantWaitlist",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "secondaryButton",
       "label": "Join",
       "operation": "joinWaitlist",
       "provenance": "contract catalogue.yaml POST /waitlist-entries"
      },
      {
       "kind": "secondaryButton",
       "label": "Leave",
       "operation": "leaveWaitlist",
       "provenance": "contract catalogue.yaml DELETE /waitlist-entries/{entryId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**Nothing reserved.** Availability shows regardless; a guest looking at an empty list should still see what is bookable.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Availability already loaded stays with its age. **Booking is not offered** — a table held offline is a table two people think they have."
  },
  "apis": [
   {
    "operationId": "createTableReservation",
    "contract": "fnb",
    "purpose": "Book a table in advance",
    "trigger": "onAction"
   },
   {
    "operationId": "updateTableReservation",
    "contract": "fnb",
    "purpose": "Change or cancel a booking",
    "trigger": "onAction"
   },
   {
    "operationId": "bookResource",
    "contract": "resources",
    "purpose": "Reserve a specific resource for a window",
    "trigger": "onAction"
   },
   {
    "operationId": "getResourceAvailability",
    "contract": "resources",
    "purpose": "When it is free, with conflicts already resolved",
    "trigger": "onLoad"
   },
   {
    "operationId": "joinRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Add a party to an outlet's waitlist",
    "trigger": "onAction",
    "offline": false
   },
   {
    "operationId": "joinWaitlist",
    "contract": "catalogue",
    "purpose": "Ask to be told if capacity frees up",
    "trigger": "onAction"
   },
   {
    "operationId": "leaveWaitlist",
    "contract": "catalogue",
    "purpose": "Stop waiting",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entryId",
     "from": "deepLink"
    },
    {
     "name": "reservationId",
     "from": "deepLink"
    },
    {
     "name": "resourceId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030)."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-070"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
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
 "bookResource": {
  "method": "POST",
  "path": "/resource-bookings",
  "contract": "resources",
  "summary": "Reserve a specific resource for a window",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "claimLocationSession": {
  "method": "POST",
  "path": "/location-sessions",
  "contract": "fnb",
  "summary": "Tell the platform where the guest is",
  "permission": null,
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
  "responds": "LocationSession"
 },
 "claimTableSession": {
  "method": "POST",
  "path": "/table-sessions",
  "contract": "fnb",
  "summary": "Identify which table a guest is sitting at",
  "permission": null,
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
  "responds": "TableSession"
 },
 "createGuestFnbOrder": {
  "method": "POST",
  "path": "/guest-orders",
  "contract": "fnb",
  "summary": "A guest orders food",
  "permission": null,
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
  "requestBody": "CreateGuestOrderRequest",
  "responds": "GuestOrderResult"
 },
 "createParkingEntitlement": {
  "method": "POST",
  "path": "/parking-entitlements",
  "contract": "access",
  "summary": "A guest bought parking",
  "permission": null,
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
  "requestBody": "ParkingEntitlement",
  "responds": "ParkingEntitlement"
 },
 "createTableReservation": {
  "method": "POST",
  "path": "/table-reservations",
  "contract": "fnb",
  "summary": "Book a table in advance",
  "permission": null,
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
  "requestBody": "TableReservation",
  "responds": "TableReservation"
 },
 "getGuestBill": {
  "method": "GET",
  "path": "/table-sessions/{sessionId}/bill",
  "contract": "fnb",
  "summary": "The bill for the guest's table",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Bill"
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
 "getGuestOrderStatus": {
  "method": "GET",
  "path": "/guest-orders/{orderId}",
  "contract": "fnb",
  "summary": "Track an order",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestOrderStatus"
 },
 "getResourceAvailability": {
  "method": "GET",
  "path": "/resources/{resourceId}/availability",
  "contract": "resources",
  "summary": "When it is free, with conflicts already resolved",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "ResourceAvailability"
 },
 "getTenantAppStatus": {
  "method": "GET",
  "path": "/tenant-config/status",
  "contract": "white-label",
  "summary": "App status and recent changes",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "TenantAppStatus"
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
 "getVenueMapGraph": {
  "method": "GET",
  "path": "/venue-maps/{mapId}/graph",
  "contract": "venue-map",
  "summary": "The navigation graph, ready to route over",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "stepFreeOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "VenueMapGraph"
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
 "getWaitingGuest": {
  "method": "GET",
  "path": "/waiting-guests/{entryId}",
  "contract": "queue",
  "summary": "Read a queue entry",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WaitingGuest"
 },
 "joinQueue": {
  "method": "POST",
  "path": "/waiting-guests",
  "contract": "queue",
  "summary": "Join a virtual queue",
  "permission": null,
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
  "requestBody": "JoinQueueRequest",
  "responds": "WaitingGuest"
 },
 "joinRestaurantWaitlist": {
  "method": "POST",
  "path": "/waitlist",
  "contract": "fnb",
  "summary": "Add a party to an outlet's waitlist",
  "permission": "ORDER_MODIFY",
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
  "requestBody": "RestaurantWaitlist",
  "responds": "RestaurantWaitlist"
 },
 "joinWaitlist": {
  "method": "POST",
  "path": "/waitlist-entries",
  "contract": "catalogue",
  "summary": "Ask to be told if capacity frees up",
  "permission": null,
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
  "requestBody": "WaitlistEntry",
  "responds": "WaitlistEntry"
 },
 "leaveQueue": {
  "method": "DELETE",
  "path": "/waiting-guests/{entryId}",
  "contract": "queue",
  "summary": "Leave a queue",
  "permission": null,
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
 "leaveWaitlist": {
  "method": "DELETE",
  "path": "/waitlist-entries/{entryId}",
  "contract": "catalogue",
  "summary": "Stop waiting",
  "permission": null,
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
 "listModifierGroups": {
  "method": "GET",
  "path": "/modifier-groups",
  "contract": "fnb",
  "summary": "List modifier groups",
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
  "responds": "ModifierGroup"
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
 "updateParkingEntitlement": {
  "method": "PATCH",
  "path": "/parking-entitlements/{entitlementId}",
  "contract": "access",
  "summary": "Change the plate, or revoke",
  "permission": null,
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
  "requestBody": "ParkingEntitlement",
  "responds": "ParkingEntitlement"
 },
 "updateTableReservation": {
  "method": "PATCH",
  "path": "/table-reservations/{reservationId}",
  "contract": "fnb",
  "summary": "Change or cancel a booking",
  "permission": null,
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
  "requestBody": "TableReservation",
  "responds": "TableReservation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Bill": {
  "x-ticvai-persistence": "none — computed from visit orders",
  "type": "object",
  "required": [
   "visitId",
   "lines",
   "subtotal",
   "taxAmount",
   "total"
  ],
  "properties": {
   "visitId": {
    "type": "string"
   },
   "covers": {
    "type": "integer"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "name",
      "quantity",
      "lineTotal"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "orderId": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "lineTotal": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "categoryCode": {
       "type": "string",
       "nullable": true
      },
      "seatNumber": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "serviceCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "CreateGuestOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "menuItemId",
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "menuItemId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "maximum": 20
   },
   "modifierOptionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "note": {
    "type": "string",
    "maxLength": 200,
    "description": "Free text to the kitchen. Allergy notes belong here and are surfaced prominently on the ticket.\n"
   }
  }
 },
 "CreateGuestOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "lines",
   "quotedTotal",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "locationSessionId": {
    "type": "string",
    "nullable": true,
    "description": "Where the order is going. Required for delivery to a table, seat, cabana or named location. Absent for collection, where the outlet is named instead.\n"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for collection. Ignored where a table session is supplied."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateGuestOrderLine"
    }
   },
   "quotedTotal": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the guest was shown. Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either direction.\n"
   },
   "paymentMethod": {
    "type": "string",
    "enum": [
     "card",
     "wallet",
     "roomCharge",
     "addToTab"
    ]
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
 "FnbOrderStatus": {
  "type": "string",
  "description": "The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n",
  "enum": [
   "ordered",
   "accepted",
   "inPreparation",
   "ready",
   "served",
   "collected",
   "delivered",
   "cancelled",
   "refunded"
  ]
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
 "GuestOrderResult": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over fnb_order",
  "required": [
   "orderId",
   "orderNumber",
   "status",
   "total"
  ],
  "properties": {
   "orderId": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string",
    "description": "Short and readable. It gets called out across a counter."
   },
   "fulfilment": {
    "type": "string",
    "enum": [
     "collect",
     "deliverToLocation",
     "tableService"
    ]
   },
   "deliveryLabel": {
    "type": "string",
    "nullable": true,
    "description": "Where it is going, as a runner would read it."
   },
   "status": {
    "$ref": "#/components/schemas/FnbOrderStatus"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "estimatedReadyAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "collectionPoint": {
    "type": "string",
    "nullable": true
   },
   "tableLabel": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "GuestOrderStatus": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over kitchen_ticket",
  "required": [
   "orderId",
   "status",
   "lines"
  ],
  "properties": {
   "orderId": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/FnbOrderStatus"
   },
   "estimatedReadyAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isReadyForCollection": {
    "type": "boolean"
   },
   "lines": {
    "type": "array",
    "description": "Per-line status. A guest waiting on one dish should see which.",
    "items": {
     "type": "object",
     "properties": {
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "status": {
       "$ref": "#/components/schemas/KitchenTicketStatus"
      }
     }
    }
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
 "JoinQueueRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "queueId",
   "partySize",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "partySize": {
    "type": "integer",
    "minimum": 1
   },
   "entitlementId": {
    "type": "string",
    "nullable": true,
    "description": "Fast Pass or priority entitlement. Owned by Product & Entitlement — this contract references it and never defines it.\n"
   },
   "partyHeightsCm": {
    "type": "array",
    "description": "Where the queue has a height requirement. Refusing here is far better than refusing at the ride, in front of a child who has already waited.\n",
    "items": {
     "type": "integer"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "KitchenTicketStatus": {
  "type": "string",
  "enum": [
   "received",
   "preparing",
   "ready",
   "served",
   "recalled",
   "cancelled"
  ]
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocationSession": {
  "type": "object",
  "x-ticvai-persistence": "fnb.location_session",
  "required": [
   "id",
   "locationId",
   "kind",
   "label",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/DeliveryLocationKind"
   },
   "label": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The outlet serving this location. Where several serve it, the guest chooses and this is set on the first order.\n"
   },
   "visitId": {
    "type": "string",
    "nullable": true,
    "description": "The table visit this session orders onto, where the location is a table. Absent for a cabana or a seat, which have no visit concept — the order stands alone.\n"
   },
   "joinedExistingVisit": {
    "type": "boolean"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Sessions expire so a guest who leaves cannot order to a lounger now occupied by someone else.\n"
   }
  }
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
 "ParkingEntitlement": {
  "type": "object",
  "x-ticvai-persistence": "access.parking_entitlement",
  "required": [
   "facilityId",
   "orderId",
   "validFrom",
   "validTo"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "facilityId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "plateNumber": {
    "type": "string",
    "nullable": true,
    "description": "Required in `plateWhitelist` mode, meaningless in the others. **Personal data** — a plate identifies a person, so it lives under the same rules as a contact point.\n"
   },
   "plateCountry": {
    "type": "string",
    "nullable": true
   },
   "mediaCode": {
    "type": "string",
    "nullable": true,
    "description": "The code presented in `none` and `qrHandoff` modes."
   },
   "status": {
    "$ref": "#/components/schemas/ParkingEntitlementStatus"
   },
   "pushedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "pushFailureReason": {
    "type": "string",
    "nullable": true
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ParkingEntitlementStatus": {
  "type": "string",
  "enum": [
   "pending",
   "pushed",
   "pushFailed",
   "active",
   "used",
   "expired",
   "revoked"
  ]
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
 "QueueStatus": {
  "type": "string",
  "enum": [
   "open",
   "paused",
   "closed",
   "atCapacity"
  ]
 },
 "ResourceAvailability": {
  "type": "object",
  "description": "**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "freeWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "blockedWindows": {
    "type": "array",
    "description": "**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string",
       "enum": [
        "booked",
        "setup",
        "teardown",
        "maintenance",
        "blackout",
        "closed"
       ]
      }
     }
    }
   }
  }
 },
 "ResourceBooking": {
  "type": "object",
  "x-ticvai-persistence": "resources.booking",
  "required": [
   "id",
   "resourceId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "reserved",
     "checkedOut",
     "returned",
     "overdue",
     "cancelled",
     "noShow"
    ]
   },
   "recurrenceGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "conditionOut": {
    "type": "string",
    "nullable": true
   },
   "conditionIn": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "RestaurantWaitlist": {
  "type": "object",
  "x-ticvai-persistence": "fnb.waitlist_entry",
  "description": "BL-130. **Distinct from `queue`, which is for rides.** A restaurant waitlist has a party size, a table preference and a walk-away point, and a guest who leaves is not the same as a guest who was served.\n",
  "required": [
   "id",
   "outletId",
   "partySize",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
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
   "partySize": {
    "type": "integer"
   },
   "quotedWaitMinutes": {
    "type": "integer",
    "nullable": true
   },
   "seatingPreference": {
    "type": "string",
    "enum": [
     "any",
     "indoor",
     "outdoor",
     "bar",
     "booth",
     "highChair"
    ],
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "waiting",
     "notified",
     "seated",
     "walkedAway",
     "noShow",
     "cancelled"
    ]
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "holdExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**How long a table waits for somebody who was called.** Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a setting rather than a constant.\n"
   }
  }
 },
 "TableReservation": {
  "type": "object",
  "x-ticvai-persistence": "fnb.table_reservation",
  "required": [
   "outletId",
   "startsAt",
   "partySize"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
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
   "guestName": {
    "type": "string"
   },
   "contactPoint": {
    "type": "string"
   },
   "partySize": {
    "type": "integer",
    "minimum": 1
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "durationMinutes": {
    "type": "integer",
    "description": "**How long the cover is held.** An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked.\n"
   },
   "tableIds": {
    "type": "array",
    "description": "Usually empty until seating. **Committing a specific table at booking time refuses later bookings against a constraint that did not need to exist.**\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "status": {
    "$ref": "#/components/schemas/TableReservationStatus"
   },
   "groupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "5.1.2. Several bookings managed as one party across adjacent tables."
   },
   "notes": {
    "type": "string",
    "description": "Allergies",
    "occasion": null,
    "accessibility.": null
   },
   "actualPartySize": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
   },
   "tableVisitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "TableReservationStatus": {
  "type": "string",
  "enum": [
   "booked",
   "confirmed",
   "seated",
   "completed",
   "cancelled",
   "noShow"
  ]
 },
 "TableSession": {
  "type": "object",
  "x-ticvai-persistence": "fnb.table_session",
  "required": [
   "id",
   "outletId",
   "tableId",
   "tableLabel",
   "visitId",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "outletName": {
    "type": "string"
   },
   "tableId": {
    "type": "string",
    "format": "uuid"
   },
   "tableLabel": {
    "type": "string"
   },
   "visitId": {
    "type": "string",
    "description": "The table visit this session orders onto. An existing open visit is joined rather than duplicated — a guest seated by a server and then ordering by app is one party, one bill.\n"
   },
   "joinedExistingVisit": {
    "type": "boolean"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Sessions expire so a guest who leaves cannot order to a table now occupied by someone else.\n"
   }
  }
 },
 "TenantAppStatus": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "tenantId",
   "isPublished",
   "isInMaintenance"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "isPublished": {
    "type": "boolean"
   },
   "publishedVersion": {
    "type": "string",
    "nullable": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "draftVersion": {
    "type": "string"
   },
   "hasUnpublishedChanges": {
    "type": "boolean"
   },
   "activeModuleCount": {
    "type": "integer"
   },
   "licensedModuleCount": {
    "type": "integer"
   },
   "activePageCount": {
    "type": "integer"
   },
   "isInMaintenance": {
    "type": "boolean"
   },
   "maintenanceMessage": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "expectedBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recentChanges": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
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
 "VenueMapGraph": {
  "type": "object",
  "description": "19.2.56. **What a client needs to route, and nothing more.** Small enough to cache, versioned so a stale route is detectable.\n",
  "required": [
   "mapId",
   "version",
   "nodes",
   "edges"
  ],
  "properties": {
   "mapId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "integer",
    "description": "**Bumped by a publish or a closure.** A client holding an older version knows its route may cross something that closed, and asking for the graph is cheaper than asking whether the graph changed.\n"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "nodes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "pointId": {
       "type": "string",
       "format": "uuid"
      },
      "x": {
       "type": "number"
      },
      "y": {
       "type": "number"
      },
      "kind": {
       "type": "string"
      },
      "isAccessible": {
       "type": "boolean"
      }
     }
    }
   },
   "edges": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "uuid"
      },
      "to": {
       "type": "string",
       "format": "uuid"
      },
      "distanceMetres": {
       "type": "number"
      },
      "isStepFree": {
       "type": "boolean"
      },
      "throughPointId": {
       "type": "string",
       "nullable": true,
       "description": "Where an access point restricts this edge. **The direction lives on that point**, not here, so a gate reconfigured to bidirectional changes routing without a map edit.\n"
      },
      "isClosed": {
       "type": "boolean"
      }
     }
    }
   },
   "components": {
    "type": "integer",
    "description": "How many disconnected parts. **One is the answer for a park.** More than one on a map that should be a single site means something is unreachable and the client can say so without walking the graph.\n"
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
 },
 "WaitingGuest": {
  "x-ticvai-persistence": "queue.waiting_guest",
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
    "type": "string"
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
 },
 "WaitlistEntry": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.waitlist_entry",
  "required": [
   "performanceId",
   "partySize"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "contactPoint": {
    "type": "string",
    "description": "**Where the offer goes.** An entry with no way to reach the guest is an entry that can never be honoured, so this is required even for an anonymous guest.\n"
   },
   "partySize": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "$ref": "#/components/schemas/WaitlistStatus"
   },
   "position": {
    "type": "integer",
    "readOnly": true,
    "description": "First in, first offered. Shown to the guest, because not knowing is worse than waiting."
   },
   "offeredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "offerExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**The offer moves on when this passes.** Notifying everyone at once produces a race the fastest guest wins; holding indefinitely for someone asleep leaves the seat unsold.\n"
   },
   "joinedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "WaitlistStatus": {
  "type": "string",
  "enum": [
   "waiting",
   "offered",
   "converted",
   "expired",
   "left"
  ]
 }
}
```
