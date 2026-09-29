# P02-in-venue-services-01 — P02 · In-venue Services

**10 screens · 32 operations · 74 schemas · 7 permissions**

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
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PARKING_CONFIGURE, PRODUCT_VIEW, QUEUE_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **10 of these operations work offline**: createPayment, getOrder, getTenantAppStatus, getVenueMap, getVenueMapGraph, getWaitTimes, joinRestaurantWaitlist, listParkingFacilities
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
| `GST-023` | Virtual Queue | statusTracker | 5 | 1 | — |
| `GST-024` | F&B – Browse & Order | listDetail | 10 | 3 | — |
| `GST-025` | F&B – Order Tracking | statusTracker | 3 | 1 | — |
| `GST-027` | Parking – Reserve & Pay | listDetail | 5 | 2 | — |
| `GST-028` | Parking – Reservation Confirmed | listDetail | 2 | 0 | — |
| `GST-029` | Venue Info & Services | listDetail | 3 | 0 | — |
| `GST-038` | At the Venue | listDetail | 3 | 0 | — |
| `GST-070` | Reserve a Table | form | 7 | 5 | — |

## Thin screens in this batch

**GST-022, GST-025 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
    "GST-001",
    "GST-038"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
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
     "provenance": "derived — GST-001 declares entryState.params  and GST-021 holds none of them, so the edge carries nothing and GST-001 opens cold"
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
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired to the venue map 18 August (CF-123).** The whole map arrives in one call and the client filters locally — which is also what makes it work with no signal in the middle of a park. **Routing happens on the device.** The platform guarantees the graph — connected, versioned, with step-free marked — and the client walks it, because a phone with the graph cached routes with no signal and a server round-trip per step does not. **The version is how a stale route is caught**: a guest holding a route across a path that closed this morning gets told, rather than walking into a barrier. **Drawn 26 August** — `Seat Board 4.dc.html` frame `seat-4b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**\n\n**Mobile v4 (decided 29 September, MOB-1).** The **Map** view of GST-038 At the Venue: **one implementation with GST-038, the ids kept** (as GAP-D3).",
  "density": "comfortable",
  "boardFrames": [
   "Seat Board 4.dc.html#seat-4b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "See where things are in relation to each other.",
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
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
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
      },
      {
       "kind": "detailPanel",
       "label": "The venue map graph",
       "bindsTo": "VenueMapGraph",
       "columns": [
        "VenueMapGraph.mapId",
        "VenueMapGraph.generatedAt",
        "VenueMapGraph.nodes",
        "VenueMapGraph.edges",
        "VenueMapGraph.components"
       ],
       "operation": "getVenueMapGraph",
       "provenance": "contract venue-map.yaml GET /venue-maps/{mapId}/graph"
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
    }
   ]
  },
  "states": {
   "loading": "The interactive map list.",
   "error": "Could not load. Names which read failed and leaves the interactive map untouched.",
   "emptyFirstRun": "No interactive map yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the interactive map are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-021",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (29 September build)",
    "verified": "2026-09-29",
    "match": "exact",
    "view": "At the venue → Map"
   },
   "derivedFrom": "wireframes/reference/Seat Board 4.dc.html",
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
    "GST-021",
    "GST-038"
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
     "provenance": "derived — GST-001 declares entryState.params  and GST-022 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-059",
     "trigger": "Plan My Day – In Progress",
     "provenance": "derived — GST-059 declares entryState.params itemId, planId and GST-022 holds none of them, so the edge carries nothing and GST-059 opens cold"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Pulled to Wave 2 (CF-101) with the queue platform F21 runs on.\n\n**Mobile v4 (decided 29 September, MOB-1).** The **Waits** view of GST-038 At the Venue: **one implementation with GST-038, the ids kept** (as GAP-D3).",
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
       "label": "The wait time",
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
       "notes": "**A stale wait time is shown with a caveat, never hidden** (decided 28 September, audit R080 (b)): where `WaitTime.isStale` is true the minutes stay on screen marked out of date with their `asOf` time, as queue.yaml says.",
       "provenance": "contract queue.yaml GET /queues/wait-times"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attraction wait times, read by `getWaitTimes`.",
   "error": "Could not load. Names which read failed and leaves the attraction wait times untouched.",
   "emptyFirstRun": "No attraction wait times yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-022",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (29 September build)",
    "verified": "2026-09-29",
    "match": "exact",
    "view": "At the venue → Waits"
   }
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
    "GST-022",
    "GST-025"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
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
     "provenance": "derived — GST-001 declares entryState.params  and GST-023 holds none of them, so the edge carries nothing and GST-001 opens cold"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Renamed 31 August** from *Virtual Queue / Join Queue*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added getWaitTimes. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.\n\n**Rev 3 (decided 29 September).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (GAP-D2, open).",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getWaitingGuest` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Find the right one quickly, and act on it without opening it.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The waiting guest",
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
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Join queue",
       "operation": "joinQueue",
       "provenance": "contract queue.yaml POST /waiting-guests"
      },
      {
       "kind": "secondaryButton",
       "label": "Leave queue",
       "operation": "leaveQueue",
       "provenance": "contract queue.yaml DELETE /waiting-guests/{entryId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual queue, read by `getWaitingGuest`.",
   "error": "Could not load. Names which read failed and leaves the virtual queue untouched.",
   "emptyFirstRun": "No virtual queue yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** The guest's place stays on screen with its age, so they can see they hold it. Joining and leaving need the connection — a place taken offline is a place nobody else can see."
  },
  "apis": [
   {
    "operationId": "joinQueue",
    "contract": "queue",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "getWaitingGuest",
    "contract": "queue",
    "purpose": "The guest's place and the call to come forward, read on entry and polled while the screen is open; the queue call shows here, and in the in-venue notifications feed too, which is back in the first release (decided 29 September, rev 3 GAP-C1, reversing the deferral of audit R242)",
    "trigger": "onInterval"
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-023",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 3 → Virtual queue; also At-venue card \"Desert Coaster · queued\"",
    "differences": "Prototype allows two queues at once; the YAML states no limit."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formJoinQueue",
    "component": "modal",
    "trigger": "Join queue",
    "body": "**Collects what `joinQueue` sends before it is called.** Required: `id`, `queueId`, `partySize`, `recordedAt`. Optional: `entitlementId`, `partyHeightsCm`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "JoinQueueRequest",
    "confirm": {
     "label": "Join queue",
     "operation": "joinQueue"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "queueId",
      "partySize",
      "recordedAt",
      "entitlementId",
      "partyHeightsCm"
     ]
    },
    "provenance": "client-verified"
   }
  ],
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
    "GST-009",
    "GST-025"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-024 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-009",
     "trigger": "Pays",
     "provenance": "flow F11 step 3→4",
     "operation": "createGuestFnbOrder",
     "carries": [
      "orderId"
     ]
    },
    {
     "to": "GST-025",
     "trigger": "They watch the order progress",
     "provenance": "flow F48 step 4→5",
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "notes": "The inventory cited `GET /menu`, which never existed. Now getGuestMenu. Ordering to a cabana or a seat uses the same claimLocationSession as a table (4.6.26). States derived from the screen pattern on 17 August, not individually considered. **Cross-surface parity, 31 August**: added claimTableSession, listModifierGroups. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.\n\n**Rev 3 (decided 29 September).** Add on an item with modifier groups opens the modifier side panel (GST-061, REV3-9); delivery fee, minimum, area and full slots are unchanged (DG-5).",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads the population and `getGuestMenu` reads one of them — list, select, act",
  "purpose": "Order food to where the guest is sitting, or for collection.",
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
      },
      {
       "kind": "selectField",
       "label": "Mode",
       "operation": "listFulfilmentSlots",
       "notes": "Sends `?mode=` to `listFulfilmentSlots`.",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/fulfilment-slots"
      },
      {
       "kind": "datePicker",
       "label": "Date",
       "operation": "listFulfilmentSlots",
       "notes": "Sends `?date=` to `listFulfilmentSlots`.",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/fulfilment-slots"
      },
      {
       "kind": "dataTable",
       "label": "Every fulfilment slots",
       "bindsTo": "FulfilmentSlots",
       "columns": [
        "FulfilmentSlots.slots"
       ],
       "operation": "listFulfilmentSlots",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/fulfilment-slots"
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
      },
      {
       "kind": "dataTable",
       "label": "Every modifier group",
       "bindsTo": "ModifierGroup",
       "columns": [
        "ModifierGroup.id",
        "ModifierGroup.code",
        "ModifierGroup.name",
        "ModifierGroup.minSelections",
        "ModifierGroup.maxSelections",
        "ModifierGroup.options",
        "ModifierGroup.scopePath"
       ],
       "operation": "listModifierGroups",
       "provenance": "contract fnb.yaml GET /modifier-groups"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected fulfilment slots",
       "bindsTo": "FulfilmentSlots",
       "columns": [
        "FulfilmentSlots.slots"
       ],
       "operation": "listFulfilmentSlots",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/fulfilment-slots"
      },
      {
       "kind": "detailPanel",
       "label": "The F&B delivery policy",
       "bindsTo": "FnbDeliveryPolicy",
       "columns": [
        "FnbDeliveryPolicy.id",
        "FnbDeliveryPolicy.outletId",
        "FnbDeliveryPolicy.collectionEnabled",
        "FnbDeliveryPolicy.deliveryEnabled",
        "FnbDeliveryPolicy.collectionPoint",
        "FnbDeliveryPolicy.collectionHoldMinutes",
        "FnbDeliveryPolicy.asapCollectionMinutes",
        "FnbDeliveryPolicy.asapDeliveryMinutes",
        "FnbDeliveryPolicy.slotMinutes",
        "FnbDeliveryPolicy.minimumOrder",
        "FnbDeliveryPolicy.deliveryFee",
        "FnbDeliveryPolicy.freeDeliveryAbove",
        "FnbDeliveryPolicy.radiusKm",
        "FnbDeliveryPolicy.emiratesServed",
        "FnbDeliveryPolicy.cutleryOptIn",
        "FnbDeliveryPolicy.scopePath"
       ],
       "operation": "getFnbDeliveryPolicy",
       "provenance": "contract fnb.yaml GET /fnb-delivery-policy"
      },
      {
       "kind": "detailPanel",
       "label": "The guest order status",
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
      },
      {
       "kind": "detailPanel",
       "label": "The guest menu",
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
       "label": "Claim location session",
       "operation": "claimLocationSession",
       "provenance": "contract fnb.yaml POST /location-sessions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create guest F&B order",
       "operation": "createGuestFnbOrder",
       "provenance": "contract fnb.yaml POST /guest-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Claim table session",
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
   "emptyFirstRun": "No browse order yet. Offers Create guest F&B order (`createGuestFnbOrder`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on mode, date and the browse order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getFnbDeliveryPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** The menu already loaded stays with its age. Ordering, claiming a table and booking wait for the connection — an order placed offline is food nobody is making."
  },
  "apis": [
   {
    "operationId": "getFnbDeliveryPolicy",
    "contract": "fnb",
    "purpose": "Minimum order, delivery fee and area",
    "trigger": "onLoad"
   },
   {
    "operationId": "listFulfilmentSlots",
    "contract": "fnb",
    "purpose": "Collection times or delivery windows still open",
    "trigger": "onLoad"
   },
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
    "trigger": "onAction"
   },
   {
    "operationId": "createGuestFnbOrder",
    "contract": "fnb",
    "purpose": "Place the order",
    "trigger": "onAction"
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
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error. **`venueId` is the venue the guest picked on the home screen** (WEB-001 on the web, GST-001 in the app), remembered on the device and changeable there; it is not read from the sign-in (decided 28 September, audit R267).",
   "preloaded": [
    "FulfilmentSlots.slots"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-024",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → F&B – browse & order"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formClaimLocationSession",
    "component": "modal",
    "trigger": "Claim location session",
    "body": "**Collects what `claimLocationSession` sends before it is called.** Nothing in the body is required. Optional: `locationCode`, `seatReference`, `partySize`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Claim location session",
     "operation": "claimLocationSession"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "locationCode",
      "seatReference",
      "partySize"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formCreateGuestFnbOrder",
    "component": "modal",
    "trigger": "Create guest F&B order",
    "body": "**Collects what `createGuestFnbOrder` sends before it is called.** Required: `id`, `lines`, `quotedTotal`, `recordedAt`. Optional: `locationSessionId`, `outletId`, `fulfilment`, `paymentMethod`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateGuestOrderRequest",
    "confirm": {
     "label": "Create guest F&B order",
     "operation": "createGuestFnbOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "lines",
      "quotedTotal",
      "recordedAt",
      "locationSessionId",
      "outletId",
      "fulfilment",
      "paymentMethod"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formClaimTableSession",
    "component": "modal",
    "trigger": "Claim table session",
    "body": "**Collects what `claimTableSession` sends before it is called.** Required: `tableCode`. Optional: `partySize`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Claim table session",
     "operation": "claimTableSession"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tableCode",
      "partySize"
     ]
    },
    "provenance": "client-verified"
   }
  ],
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
    "GST-023",
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
     "provenance": "derived — GST-001 declares entryState.params  and GST-025 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-023",
     "trigger": "Their queue place comes up and the queue screen shows it",
     "provenance": "flow F48 step 5→6"
    },
    {
     "to": "BO-021",
     "trigger": "Runner delivers to the lounger",
     "provenance": "flow F11 step 6→7",
     "operation": "getGuestOrderStatus",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "notes": "Nine states from 4.6.35. Collected and delivered are distinct from served — a counter handover, a runner delivery and a server putting a plate down are three different events. States derived from the screen pattern on 17 August, not individually considered. **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted. **Cross-platform navigation removed 24 August**: BO-021. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Track an order to the point it reaches the guest.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The guest order status",
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
      },
      {
       "kind": "detailPanel",
       "label": "The bill",
       "bindsTo": "Bill",
       "columns": [
        "Bill.visitId",
        "Bill.covers",
        "Bill.lines",
        "Bill.subtotal",
        "Bill.serviceCharge",
        "Bill.taxAmount",
        "Bill.discountAmount",
        "Bill.total"
       ],
       "operation": "getGuestBill",
       "provenance": "contract fnb.yaml GET /table-sessions/{sessionId}/bill"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Claim table session",
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
   "offline": "**The offline banner shows.** The last status stays on screen with its age and is never presented as current. Settling the bill waits for the connection."
  },
  "apis": [
   {
    "operationId": "getGuestOrderStatus",
    "contract": "fnb",
    "purpose": "The order's status (ordered, accepted, in preparation, ready, served, collected or delivered), read on entry and polled while the screen is open; order updates show here, and in the in-venue notifications feed too, which is back in the first release (decided 29 September, rev 3 GAP-C1, reversing the deferral of audit R242)",
    "trigger": "onInterval"
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-025",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → F&B – order tracking",
    "differences": "The YAML states come from an availability template (\"Selection is blocked\") and do not fit order tracking."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formClaimTableSession",
    "component": "modal",
    "trigger": "Claim table session",
    "body": "**Collects what `claimTableSession` sends before it is called.** Required: `tableCode`. Optional: `partySize`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Claim table session",
     "operation": "claimTableSession"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tableCode",
      "partySize"
     ]
    },
    "provenance": "client-verified"
   }
  ],
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
    "GST-028"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-027 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-028",
     "trigger": "It is confirmed with a facility",
     "provenance": "flow F50 step 2→3",
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`createParkingEntitlement` is declared `service` audience and this is a guest screen.** Either the guest calls it — in which case the audience is wrong — or a guest-scoped operation is missing and the screen is drawing an act it cannot perform. **Recorded 24 August rather than guessed**: `updateParkingEntitlement` is already `guest`, which makes the asymmetry look like an omission rather than a design. **Cross-surface parity, 31 August**: added listParkingFacilities. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate. **Rebound 28 September** (decided 28 September, audit R166): parking is sold through the normal cart and checkout (`addCartLine`, `checkoutCart`, `createPayment`), so the entitlement gets its `orderId`; the guest no longer calls `createParkingEntitlement`, which the order service issues at payment. No live availability; a full car park is the `soldOutForDay` refusal.\n\n**Rev 3 (decided 29 September).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (GAP-D2, open).",
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
       "kind": "textField",
       "label": "Venue id",
       "operation": "listParkingFacilities",
       "notes": "Sends `?venueId=` to `listParkingFacilities`.",
       "provenance": "contract access.yaml GET /parking-facilities"
      },
      {
       "kind": "dataTable",
       "label": "Every parking facility",
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
       "label": "The selected parking facility",
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
       "label": "Add parking to my cart",
       "operation": "addCartLine",
       "notes": "**Parking is sold through the normal cart** (decided 28 September, audit R166): the car park's parking product goes in as a cart line, then checkout and payment as for a ticket, and the parking entitlement is issued at payment carrying the order's id — the guest never creates it. No live space count: a car park at capacity refuses the line with `soldOutForDay`.",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Check out",
       "operation": "checkoutCart",
       "provenance": "contract orders.yaml POST /carts/{cartId}/checkout"
      },
      {
       "kind": "primaryButton",
       "label": "Pay",
       "operation": "createPayment",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "secondaryButton",
       "label": "Save parking entitlement",
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
   "emptyNoResults": "Nothing matches the filter on venueId and the parking reserve pay are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PARKING_CONFIGURE`, which `listParkingFacilities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection.",
   "soldOutForDay": "**The car park is full.** `addCartLine` refused the parking line with `soldOutForDay`: issued entitlements have reached the facility's capacity for that day. Shown only then — there is no live space count in the first release, so the screen never promises spaces before the guest tries (decided 28 September, audit R166)."
  },
  "apis": [
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Put the car park's parking product in the cart; refused `soldOutForDay` when the car park is at capacity (decided 28 September, audit R166)",
    "trigger": "onAction"
   },
   {
    "operationId": "checkoutCart",
    "contract": "orders",
    "purpose": "Turn the cart into an order",
    "trigger": "onAction"
   },
   {
    "operationId": "createPayment",
    "contract": "orders",
    "purpose": "Pay for it; the parking entitlement is issued at payment with the order's id (audit R166)",
    "trigger": "onAction"
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
    },
    {
     "name": "cartId",
     "from": "session"
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-027",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 3 → Parking – reserve & pay"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAddCartLine",
    "component": "modal",
    "trigger": "Add parking to my cart",
    "body": "**Collects what `addCartLine` sends before it is called.** Required: `variantId` (the car park's parking product), `quantity`. Optional: `performanceId`, `attributes` (the plate). A 409 `soldOutForDay` is shown as **the car park is full** for that day — capacity reached, not a live count (decided 28 September, audit R166). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add to cart",
     "operation": "addCartLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "variantId",
      "quantity",
      "performanceId",
      "attributes"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formUpdateParkingEntitlement",
    "component": "modal",
    "trigger": "Save parking entitlement",
    "body": "**Collects what `updateParkingEntitlement` sends before it is called.** Nothing in the body is required. Optional: `plateNumber`, `plateCountry`, `status`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "UpdateParkingEntitlementRequest",
    "confirm": {
     "label": "Save parking entitlement",
     "operation": "updateParkingEntitlement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "plateNumber",
      "plateCountry",
      "status"
     ]
    },
    "provenance": "client-verified"
   }
  ],
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
    "GST-012"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-028 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-012",
     "trigger": "They open their tickets",
     "provenance": "flow F50 step 3→4",
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`createParkingEntitlement` is declared `service` audience and this is a guest screen.** Either the guest calls it — in which case the audience is wrong — or a guest-scoped operation is missing and the screen is drawing an act it cannot perform. **Recorded 24 August rather than guessed**: `updateParkingEntitlement` is already `guest`, which makes the asymmetry look like an omission rather than a design. **Rebound 28 September** (decided 28 September, audit R166): the guest no longer creates the parking entitlement; it is issued at payment of the cart order, and this screen reads that order (`getOrder`).\n\n**Rev 3 (decided 29 September).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (GAP-D2, open).",
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
       "kind": "textField",
       "label": "Venue id",
       "operation": "listParkingFacilities",
       "notes": "Sends `?venueId=` to `listParkingFacilities`.",
       "provenance": "contract access.yaml GET /parking-facilities"
      },
      {
       "kind": "dataTable",
       "label": "Every parking facility",
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
       "label": "The selected parking facility",
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
       "kind": "detailPanel",
       "label": "The order the parking was paid on",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.status"
       ],
       "operation": "getOrder",
       "notes": "**The parking entitlement is issued at payment, carrying this order's id** (decided 28 September, audit R166); this screen confirms the order and shows the car park and plate from it, and never creates the entitlement itself.",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The parking reservation confirmed list.",
   "error": "Could not load. Names which read failed and leaves the parking reservation confirmed untouched.",
   "emptyFirstRun": "**Paid, entitlement not yet shown.** The order is paid and the entitlement is issued at payment; until it appears the screen shows the order and says the car park pass follows (audit R166).",
   "emptyNoResults": "Nothing matches the filter on venueId and the parking reservation confirmed are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PARKING_CONFIGURE`, which `listParkingFacilities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection."
  },
  "apis": [
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "The paid order that carries the parking entitlement (audit R166)",
    "trigger": "onLoad"
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
     "name": "orderId",
     "from": "previousScreen"
    }
   ],
   "coldEntry": "**Opened cold, it needs the order.** Without `orderId` it sends the guest to their orders rather than showing an empty confirmation.",
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-028",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 3 → Parking – reservation confirmed"
   }
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
    "GST-002"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-029 holds none of them, so the edge carries nothing and GST-001 opens cold"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Contact added 28 September** from `getTenantAppStatus.contact`, as on the web's WEB-028 (decided 28 September, audit R073 (f)).",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See venue info & services for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "How to reach the venue",
       "bindsTo": "VenueContact",
       "columns": [
        "VenueContact.phone",
        "VenueContact.email",
        "VenueContact.whatsapp",
        "VenueContact.address",
        "VenueContact.openingHours"
       ],
       "operation": "getTenantAppStatus",
       "notes": "**From `getTenantAppStatus.contact`** (decided 28 September, audit R073 (f)): phone, email, WhatsApp, address and opening hours, set from CMS-001 through `setMaintenanceMode`. Each is optional and a missing one is left out rather than shown blank.",
       "provenance": "contract white-label.yaml GET /tenant-config/status"
      },
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue info services list.",
   "error": "Could not load. Names which read failed and leaves the venue info services untouched.",
   "emptyFirstRun": "No venue info services yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on openNow, orderingMethod and the venue info services are still there. Names the active filter and offers to clear it.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "How to reach the venue — phone, email, WhatsApp, address, opening hours (decided 28 September, audit R073 (f))",
    "trigger": "onLoad"
   },
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
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case. **`venueId` is the venue the guest picked on the home screen** (WEB-001 on the web, GST-001 in the app), remembered on the device and changeable there; it is not read from the sign-in (decided 28 September, audit R267).",
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-029",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → Venue info & services",
    "differences": "Prototype shows only dining and delivery points, no other venue services."
   }
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
  "name": "At the Venue",
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
    "GST-021",
    "GST-022",
    "GST-024",
    "GST-026",
    "GST-029",
    "GST-023"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-038 holds none of them, so the edge carries nothing and GST-001 opens cold"
    },
    {
     "to": "GST-021",
     "trigger": "Map view",
     "provenance": "decided 29 September 2026 (P29), MOB-1"
    },
    {
     "to": "GST-022",
     "trigger": "Waits view",
     "provenance": "decided 29 September 2026 (P29), MOB-1"
    },
    {
     "to": "GST-024",
     "trigger": "Food",
     "provenance": "decided 29 September 2026 (P29), MOB-1"
    },
    {
     "to": "GST-026",
     "trigger": "Shop",
     "provenance": "decided 29 September 2026 (P29), MOB-1"
    },
    {
     "to": "GST-029",
     "trigger": "Services",
     "provenance": "decided 29 September 2026 (P29), MOB-1"
    },
    {
     "to": "GST-023",
     "trigger": "Join a virtual queue",
     "provenance": "decided 29 September 2026 (P29), MOB-1"
    }
   ],
   "uses": [
    "appTabs"
   ]
  },
  "notes": "**Mobile v4 (decided 29 September, MOB-1).** Retitled **At the Venue**, the in-venue mode and the optional Map tab: views Map, Waits, Food, Shows, Shop and Services, plus a *Happening now* panel (live orders and queues). **GST-021 Interactive Map and GST-022 Attraction Wait Times are its Map and Waits views: one implementation, three ids** (as GAP-D3). Food opens GST-024, Shop GST-026, Services GST-029, a queue GST-023. This answers CF-92: it is a real screen. (Was: *Not minuted and not in the matrix* — the only unsourced screen of the eight audited on 17 August.)",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getTenantAppStatus` reads one of them — list, select, act",
  "purpose": "Everything live at the venue in one place: map, waits, food, shows, shop and services, with what is happening now.",
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
       "kind": "selectField",
       "label": "Map · Waits · Food · Shows · Shop · Services",
       "notes": "The view switcher. Map and Waits are GST-021 and GST-022 rendered in place.",
       "provenance": "decided 29 September 2026 (P29), MOB-1"
      },
      {
       "kind": "banner",
       "label": "Happening now",
       "operation": "getWaitTimes",
       "notes": "Live orders, queue calls and the next show, from the guest's own orders and queues.",
       "provenance": "decided 29 September 2026 (P29), MOB-1"
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
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
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
       "label": "The tenant app status",
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
   "emptyFirstRun": "No digital companion mode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the digital companion mode are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-038",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (29 September build)",
    "verified": "2026-09-29",
    "match": "exact",
    "view": "At the venue (Home → At the venue, or the Map tab where the venue shows it)"
   }
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
  "name": "Reserve a Table",
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
    "GST-039",
    "GST-041"
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
     "provenance": "derived — GST-039 declares entryState.params subjectId and GST-070 holds subjectId, so an edge into it carries them"
    },
    {
     "to": "GST-041",
     "trigger": "Pay the deposit (only when the venue requires one)",
     "operation": "addCartLine",
     "carries": [
      "cartId"
     ],
     "precondition": "the reservation is awaitingDeposit",
     "provenance": "decided 29 September, rev 3 REV3-8b: `createTableReservation` answered `awaitingDeposit`"
    }
   ]
  },
  "notes": "**Staff could book a table and a guest could not.** Seven guest-callable operations with no guest surface — reservations, cabanas, and both waitlists. **Table-only since 28 September** (decided 28 September, audit R073 (c)): the cabana wording, the `bookResource` button and `getResourceAvailability` left and the screen was renamed from *Reserve a Table or Cabana*. **R073 (c) is superseded on 29 September for resources on a venue map** (rev 3 REV3-15 and GAP-C2): guests pick a specific cabana, lounger or other spot — including non-dining tables placed on the map, sold like cabanas — on the map booking screen GST-074 and buy it. This screen stays the restaurant table reservation, the F&B flow. **Leave waitlist** is `leaveRestaurantWaitlist` (audit R073 (d)). **A table deposit is a venue option, off by default** (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a)): with it off, no card is needed and cancelling is free; with it on, the venue's `DepositPolicy.dining` sets the amount, the basis and the late-cancel and no-show terms.\n\n**Leaving a waitlist matters as much as joining one.** A guest who has given up and walked away still holds a place, and a queue full of people who left is a queue nobody trusts.\n\n**Rev 3 (decided 29 September).** **No basket without a deposit (REV3-8):** a table reservation and a waitlist place confirm straight after `createTableReservation` / `joinRestaurantWaitlist` with a *No card needed* confirmation; the prototype's basket line is prototype-only. **Deposit (REV3-8b):** when the venue enabled one, `createTableReservation` answers `awaitingDeposit`; the screen shows `deposit.amount` and basis, adds it to the cart (`addCartLine` with `deposit.variantId` and `tableReservationId`), pays through checkout (GST-041), and shows `deposit.refundableUntil` and the late-cancel and no-show terms. Never a hard-coded amount. Leaving a waitlist is unchanged (audit R073 (d)).",
  "density": "comfortable",
  "offline": false,
  "pattern": "form",
  "patternReason": "A booking form (outlet, party size, time) and the restaurant waitlist, each one act; no guest-callable read of table availability exists, so `createTableReservation` is what says a time is full. Changed from `statusTracker` on 28 September when the cabana availability read left (audit R073 (c)); cabanas and other spots on a venue map are booked on GST-074 since 29 September (rev 3 REV3-15).",
  "purpose": "**Book a restaurant table, or wait for one.** A guest reserves a table ahead, changes or cancels it, or joins and leaves a restaurant's waitlist. Tables only: cabanas, loungers and other spots on a venue map are booked on GST-074 (decided 29 September, rev 3 REV3-15 and GAP-C2, superseding audit R073 (c)). A deposit only where the venue enabled one (rev 3 REV3-8b, superseding audit R077 (a)).",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create table reservation",
       "operation": "createTableReservation",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save table reservation",
       "operation": "updateTableReservation",
       "provenance": "contract fnb.yaml PATCH /table-reservations/{reservationId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Join restaurant waitlist",
       "operation": "joinRestaurantWaitlist",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "destructiveButton",
       "label": "Leave restaurant waitlist",
       "operation": "leaveRestaurantWaitlist",
       "notes": "Leaves the guest's own entry (POST /waitlist/{entryId}/leave); the entry returns `cancelled` and the table goes to the next party (decided 28 September, audit R073 (d)).",
       "provenance": "contract fnb.yaml POST /waitlist/{entryId}/leave"
      },
      {
       "kind": "secondaryButton",
       "label": "Join waitlist",
       "operation": "joinWaitlist",
       "provenance": "contract catalogue.yaml POST /waitlist-entries"
      },
      {
       "kind": "secondaryButton",
       "label": "Leave waitlist",
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
   "emptyFirstRun": "**Nothing reserved.** The booking form is the screen: pick the restaurant, party size and time, and `createTableReservation` says if that time is full.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025). A guest who is not signed in is offered sign-in and brought back here.",
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
    "operationId": "joinRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Add a party to an outlet's waitlist",
    "trigger": "onAction",
    "offline": false
   },
   {
    "operationId": "leaveRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Leave the restaurant waitlist; the entry returns cancelled (decided 28 September, audit R073 (d))",
    "trigger": "onAction"
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
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add the table deposit to the cart when the venue requires one",
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
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "cartId",
     "from": "session",
     "optional": true
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030)."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-070",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → All screens → Wave 2 → Reserve a table or cabana; Rev 3 feedback → Book a table (fixed)",
    "differences": "The YAML covers tables only (cabanas are staff-booked, R073c) and has no deposit (R077a). The prototype also reserves cabanas and shows a deposit on the reservation, and the Rev 3 web flow has a deposit-hold variant at AED 100 per guest."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateTableReservation",
    "component": "modal",
    "trigger": "Create table reservation",
    "body": "**Collects what `createTableReservation` sends before it is called.** Required: `outletId`, `partySize`, `startsAt`. Optional: `id`, `subjectId`, `guestName`, `contactPoint`, `durationMinutes`, `tables`, `status`, `groupId`, `notes`, `actualPartySize`, `tableVisitId`. The form says **no card is needed** unless the venue enabled a dining deposit; then it shows the deposit amount and basis, when it stops being refundable and the late-cancel and no-show terms (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a)). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "TableReservation",
    "confirm": {
     "label": "Create table reservation",
     "operation": "createTableReservation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outletId",
      "partySize",
      "startsAt",
      "id",
      "subjectId",
      "guestName",
      "contactPoint",
      "durationMinutes",
      "tables",
      "status",
      "groupId",
      "notes",
      "actualPartySize",
      "tableVisitId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formUpdateTableReservation",
    "component": "modal",
    "trigger": "Save table reservation",
    "body": "**Collects what `updateTableReservation` sends before it is called.** Required: `outletId`, `partySize`, `startsAt`. Optional: `id`, `subjectId`, `guestName`, `contactPoint`, `durationMinutes`, `tables`, `status`, `groupId`, `notes`, `actualPartySize`, `tableVisitId`. Cancelling says **it is free** where no deposit was taken; where one was, whether it is returned or kept under the venue's terms (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a)). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "TableReservation",
    "confirm": {
     "label": "Save table reservation",
     "operation": "updateTableReservation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outletId",
      "partySize",
      "startsAt",
      "id",
      "subjectId",
      "guestName",
      "contactPoint",
      "durationMinutes",
      "tables",
      "status",
      "groupId",
      "notes",
      "actualPartySize",
      "tableVisitId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formJoinRestaurantWaitlist",
    "component": "modal",
    "trigger": "Join restaurant waitlist",
    "body": "**Collects what `joinRestaurantWaitlist` sends before it is called.** Required: `id`, `outletId`, `partySize`, `status`, `recordedAt`. Optional: `subjectId`, `quotedWaitMinutes`, `seatingPreference`, `notifiedAt`, `syncedAt`, `holdExpiresAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RestaurantWaitlist",
    "confirm": {
     "label": "Join restaurant waitlist",
     "operation": "joinRestaurantWaitlist"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outletId",
      "partySize",
      "status",
      "recordedAt",
      "subjectId",
      "quotedWaitMinutes",
      "seatingPreference",
      "notifiedAt",
      "syncedAt",
      "holdExpiresAt"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formJoinWaitlist",
    "component": "modal",
    "trigger": "Join waitlist",
    "body": "**Collects what `joinWaitlist` sends before it is called.** Required: `performanceId`, `partySize`. Optional: `id`, `variantId`, `subjectId`, `contactPoint`, `status`, `position`, `offeredAt`, `offerExpiresAt`, `joinedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "WaitlistEntry",
    "confirm": {
     "label": "Join waitlist",
     "operation": "joinWaitlist"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "performanceId",
      "partySize",
      "id",
      "variantId",
      "subjectId",
      "contactPoint",
      "status",
      "position",
      "offeredAt",
      "offerExpiresAt",
      "joinedAt"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "confirmLeaveRestaurantWaitlist",
    "component": "confirmDialog",
    "trigger": "Leave restaurant waitlist",
    "body": "**Says the place is given up and the next party moves up**, naming the restaurant and the party size. Leaving cannot be undone; joining again goes to the back (audit R073 (d)).",
    "provenance": "client-verified"
   }
  ],
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
 "addCartLine": {
  "method": "POST",
  "path": "/carts/{cartId}/lines",
  "contract": "orders",
  "summary": "Add something",
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
  "requestBody": "AddCartLineRequest",
  "responds": "Cart"
 },
 "checkoutCart": {
  "method": "POST",
  "path": "/carts/{cartId}/checkout",
  "contract": "orders",
  "summary": "Turn the cart into an order",
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
  "responds": "Order"
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
 "createPayment": {
  "method": "POST",
  "path": "/payments",
  "contract": "orders",
  "summary": "Take a payment against an order",
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
  "requestBody": "CreatePaymentRequest",
  "responds": "Payment"
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
 "getFnbDeliveryPolicy": {
  "method": "GET",
  "path": "/fnb-delivery-policy",
  "contract": "fnb",
  "summary": "How an outlet does takeaway and delivery",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "FnbDeliveryPolicy"
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
    "name": "draft",
    "in": "query",
    "required": null
   },
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
 "leaveRestaurantWaitlist": {
  "method": "POST",
  "path": "/waitlist/{entryId}/leave",
  "contract": "fnb",
  "summary": "Take a party off an outlet's waitlist",
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
  "responds": "RestaurantWaitlist"
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
 "listFulfilmentSlots": {
  "method": "GET",
  "path": "/outlets/{outletId}/fulfilment-slots",
  "contract": "fnb",
  "summary": "Collection times or delivery windows still open",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "path",
    "required": true
   },
   {
    "name": "mode",
    "in": "query",
    "required": true
   },
   {
    "name": "date",
    "in": "query",
    "required": false
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
  "responds": "Page"
 },
 "listParkingFacilities": {
  "method": "GET",
  "path": "/parking-facilities",
  "contract": "access",
  "summary": "Car parks at a venue, and how each integrates",
  "permission": "PARKING_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": false
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
  "requestBody": "UpdateParkingEntitlementRequest",
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
   },
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
 "AddCartLineRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "variantId",
   "quantity"
  ],
  "properties": {
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"
   },
   "tableReservationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "description": "At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   }
  }
 },
 "AllergenCode": {
  "type": "string",
  "description": "**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n",
  "enum": [
   "gluten",
   "crustaceans",
   "eggs",
   "fish",
   "peanuts",
   "soybeans",
   "milk",
   "nuts",
   "celery",
   "mustard",
   "sesame",
   "sulphites",
   "lupin",
   "molluscs"
  ]
 },
 "AppAvailability": {
  "type": "string",
  "description": "**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n",
  "enum": [
   "open",
   "soldOut",
   "closed"
  ],
  "default": "open"
 },
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
 "BookedWindow": {
  "type": "object",
  "nullable": true,
  "x-ticvai-persistence": "none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line",
  "description": "**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n",
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
    "format": "date-time",
    "description": "After `startsAt`, on the same venue day."
   }
  }
 },
 "Cart": {
  "type": "object",
  "x-ticvai-persistence": "orders.cart",
  "required": [
   "id",
   "venueId",
   "channel",
   "status",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "token": {
    "type": "string",
    "readOnly": true,
    "description": "**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null while anonymous. Set by `claimCart`."
   },
   "status": {
    "$ref": "#/components/schemas/CartStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CartLine"
    }
   },
   "conflicts": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CartConflict"
    }
   },
   "consentQuestions": {
    "type": "array",
    "readOnly": true,
    "description": "**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n",
    "items": {
     "allOf": [
      {
       "$ref": "../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"
      },
      {
       "type": "object",
       "properties": {
        "lineIds": {
         "type": "array",
         "description": "The cart lines that ask it. Empty for a question the flow asks.",
         "items": {
          "type": "string",
          "format": "uuid"
         }
        },
        "answered": {
         "type": "boolean",
         "description": "Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."
        }
       }
      }
     ]
    }
   },
   "subtotal": {
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "appliedPromotionIds": {
    "type": "array",
    "description": "**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "couponCodes": {
    "type": "array",
    "readOnly": true,
    "description": "The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n",
    "items": {
     "type": "string",
     "maxLength": 100
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "The earliest lease expiry in the cart, or the cart's own window where it holds none."
   },
   "extensionsUsed": {
    "type": "integer",
    "readOnly": true
   },
   "maxExtensions": {
    "type": "integer",
    "readOnly": true
   },
   "locale": {
    "type": "string"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CartConflict": {
  "type": "object",
  "x-ticvai-persistence": "none — computed on read",
  "description": "2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "overlappingTime",
     "sameSessionDifferentVenue",
     "exceedsPartySize",
     "requiresPrerequisite",
     "consentBlocksBooking"
    ]
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "message": {
    "type": "string"
   },
   "isBlocking": {
    "type": "boolean",
    "description": "Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"
   }
  }
 },
 "CartLine": {
  "type": "object",
  "x-ticvai-persistence": "orders.cart_line",
  "required": [
   "id",
   "variantId",
   "quantity"
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
    "type": "string",
    "readOnly": true
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"
   },
   "tableReservationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"
   },
   "overridePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "priceMatch",
     "serviceRecovery",
     "negotiated",
     "damagedGoods",
     "staffSale",
     "error"
    ],
    "description": "BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"
   },
   "feeKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "booking",
     "transaction",
     "service",
     "delivery",
     "convenience",
     "cancellation"
    ],
    "description": "**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lineTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"
   },
   "leaseExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"
   },
   "isAvailable": {
    "type": "boolean",
    "readOnly": true,
    "description": "Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"
   }
  }
 },
 "CartStatus": {
  "type": "string",
  "enum": [
   "active",
   "expiring",
   "expired",
   "abandoned",
   "checkedOut"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "From `claimLocationSession`. Where the order is going. Required for delivery to a table, seat, cabana or named location. Absent for collection, where the outlet is named instead.\n"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for collection. Ignored where a location session is supplied — the session names its outlet."
   },
   "fulfilment": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GuestOrderFulfilment"
     }
    ],
    "nullable": true,
    "description": "Required for takeaway and address delivery; refused with 422 when it breaks the outlet's `FnbDeliveryPolicy`."
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
 "CreatePaymentRequest": {
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."
   },
   "returnUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true,
    "description": "Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
 "ExchangeRateDecimal": {
  "type": "string",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,6)",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n",
  "pattern": "^\\d+(\\.\\d{1,6})?$"
 },
 "FnbDeliveryPolicy": {
  "type": "object",
  "x-ticvai-persistence": "fnb.delivery_policy",
  "required": [
   "outletId"
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
   "collectionEnabled": {
    "type": "boolean",
    "default": true
   },
   "deliveryEnabled": {
    "type": "boolean",
    "default": false
   },
   "collectionPoint": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "collectionHoldMinutes": {
    "type": "integer",
    "default": 20
   },
   "asapCollectionMinutes": {
    "type": "integer",
    "default": 25
   },
   "asapDeliveryMinutes": {
    "type": "integer",
    "default": 45
   },
   "slotMinutes": {
    "type": "integer",
    "default": 30
   },
   "minimumOrder": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "deliveryFee": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "freeDeliveryAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "radiusKm": {
    "type": "number",
    "minimum": 0,
    "nullable": true
   },
   "emiratesServed": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "cutleryOptIn": {
    "type": "boolean",
    "default": true,
    "description": "Cutlery only when asked for, as in the design."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
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
 "FnbReservationTable": {
  "type": "object",
  "x-ticvai-persistence": "fnb.reservation_table",
  "description": "**Taken from the backend workbook, 20 September.** Maps one or more dining tables assigned to a reservation.",
  "required": [
   "reservationId",
   "tableId",
   "createdAt"
  ],
  "properties": {
   "reservationId": {
    "type": "string",
    "format": "uuid"
   },
   "tableId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "FulfilmentSlots": {
  "type": "object",
  "x-ticvai-persistence": "none — computed per request",
  "properties": {
   "slots": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "start": {
       "type": "string",
       "format": "date-time"
      },
      "end": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "isAsap": {
       "type": "boolean"
      }
     }
    }
   }
  }
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
           "$ref": "#/components/schemas/AllergenCode"
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
 "GuestOrderFulfilment": {
  "type": "object",
  "x-ticvai-persistence": "fnb.order_fulfilment",
  "description": "How a guest's order leaves the kitchen: collected, delivered to an address, or taken to a place in the venue.",
  "required": [
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "readOnly": true,
    "x-ticvai-column": "service_order_id",
    "description": "The guest order this fulfils (`FnbOrder.id`). Set by the server from the order it arrives with."
   },
   "mode": {
    "type": "string",
    "enum": [
     "collection",
     "delivery",
     "inVenue"
    ],
    "description": "`collection` from a counter, `delivery` to an address outside the venue, `inVenue` to a table, seat, cabana or named location (the location session). `GuestOrderResult.fulfilment` reports the same choice."
   },
   "collectionAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "windowStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "windowEnd": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "deliveryAddress": {
    "type": "object",
    "nullable": true,
    "properties": {
     "building": {
      "type": "string",
      "maxLength": 200
     },
     "unit": {
      "type": "string",
      "maxLength": 60,
      "nullable": true
     },
     "emirate": {
      "type": "string",
      "maxLength": 60
     },
     "directions": {
      "type": "string",
      "maxLength": 500,
      "nullable": true
     }
    }
   },
   "deliveryFee": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true
   },
   "cutlery": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
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
     "tableService",
     "deliverToAddress"
    ],
    "description": "How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is `delivery`; `inVenue` is `tableService` where the location session is a table and `deliverToLocation` for a seat, cabana or named location. `KitchenTicket.serviceMode` is the kitchen's view and uses `ServiceMode`."
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
   "accessibilityNeedDeclared": {
    "type": "boolean",
    "default": false,
    "description": "The party declares an accessibility need (5.6.7; decided 29 September, build pass). Grants priority only on a lane whose `QueueFastPass.accessibilityPriority` is on, and is recorded on the entry either way.\n"
   },
   "promotionCode": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "description": "A promotion code the guest holds, checked against the lane's `QueueFastPass.promotionIds` (5.6.34). A code for a promotion the lane does not list grants nothing and is not an error.\n"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
 "MinimumAppVersion": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n",
  "properties": {
   "ios": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   },
   "android": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   }
  }
 },
 "ModifierGroup": {
  "x-ticvai-persistence": "fnb.modifier_group + fnb.modifier_option",
  "type": "object",
  "description": "**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n",
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
      },
      "allergens": {
       "type": "array",
       "description": "What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.",
       "items": {
        "$ref": "#/components/schemas/AllergenCode"
       }
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The client ULID from `CreateOrderRequest.id`."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "OrderLineAttributes": {
  "type": "object",
  "nullable": true,
  "additionalProperties": true,
  "x-ticvai-persistence": "none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line",
  "description": "Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n",
  "properties": {
   "transport": {
    "$ref": "#/components/schemas/TransportLineAttributes"
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
 "ParkingEntitlement": {
  "type": "object",
  "x-ticvai-persistence": "access.parking_entitlement",
  "description": "**Issued at payment of an order that contains a parking product** (decided 28 September, audit R166). Parking is sold through the normal cart and checkout (`orders.addCartLine`, `orders.checkoutCart`), so every entitlement carries that order's `orderId`. The guest pays for the parking right with their order; the facility's own system is never paid through the app (`ParkingFacility.takesPayment`). **No live availability in the first release**: the sale is refused as full only when the facility's issued entitlements reach its `capacity`.\n",
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The order's id, a ULID as in `/orders/{orderId}` (`orders.sales_order.id`)."
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
    "allOf": [
     {
      "$ref": "#/components/schemas/ParkingEntitlementStatus"
     }
    ],
    "readOnly": true,
    "description": "Server-owned. Moves as `states/parking-entitlement.yaml` says; a create body does not send it."
   },
   "pushedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "pushFailureReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
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
    "description": "**Server-assigned, and the upsert key of `setParkingFacility`.** Absent in a body, it creates; present, it names the facility being replaced. A client never mints one.\n"
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
    "nullable": true,
    "description": "**What \"full\" means in the first release** (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid for a time reach this number. There is no live space count from the car park; a guest sees *full* only when capacity is reached, never an availability figure. Null means no limit is enforced.\n"
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
    "nullable": true,
    "description": "Staff only — omitted from a guest's `listParkingFacilities` response."
   },
   "endpoint": {
    "type": "string",
    "nullable": true,
    "description": "Staff only — omitted from a guest's `listParkingFacilities` response."
   },
   "credentialRef": {
    "type": "string",
    "nullable": true,
    "description": "A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response."
   },
   "pushLeadMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. **Too early and the whitelist fills with cars that will not arrive; too late and the guest is at the barrier.**\n"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "RestaurantWaitlist": {
  "type": "object",
  "x-ticvai-persistence": "fnb.waitlist_entry",
  "description": "BL-130. **Distinct from `queue`, which is for rides.** A restaurant waitlist has a party size, a table preference and a walk-away point, and a guest who leaves is not the same as a guest who was served.\n",
  "required": [
   "id",
   "outletId",
   "partySize",
   "status",
   "recordedAt"
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
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "**When the party joined, on the device.** The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. Required on a join — the operation is offline-capable."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
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
  "x-ticvai-retired-columns": [
   "table_ids"
  ],
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
   "tables": {
    "type": "array",
    "description": "The dining tables assigned to this reservation, one row each.\n**Usually empty until seating.** Committing a specific table at booking time refuses later bookings against a constraint that did not need to exist — that was true of the `tableIds` array this replaces and it is still true, because it is about *when* a table is assigned rather than how the assignment is stored.\n**Replaces `tableIds`, retired 20 September.** An array cannot carry per-row state, which is the same reason this merge took `entry_rule_point`, `menu_item_modifier`, `seat_block_item`, `plan_benefit`, `payment_method_config` and `tier_module` from the backend workbook. A party seated across three tables that releases one early has nowhere to say so in an array, and *\"which reservations are on table 7 tonight\"* is a GIN scan over every reservation instead of an index seek.\n",
    "items": {
     "$ref": "#/components/schemas/FnbReservationTable"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "readOnly": true
   },
   "deposit": {
    "$ref": "#/components/schemas/TableReservationDeposit"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "TableReservationDeposit": {
  "type": "object",
  "nullable": true,
  "readOnly": true,
  "x-ticvai-persistence": "fnb.table_reservation",
  "description": "**The deposit this booking holds, snapshotted from `orders.DepositPolicy.dining` when it was made** (decided 29 September, rev 3 REV3-8b). Null where no deposit applied, which is every booking while the venue leaves `dining.enabled` false (the default). A later change to the policy does not re-price a booking already made.\n",
  "required": [
   "amount",
   "basis"
  ],
  "properties": {
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "basis": {
    "type": "string",
    "enum": [
     "fixedPerGuest",
     "fixedPerTable",
     "percentOfMinimumSpend"
    ]
   },
   "holdExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "While `awaitingDeposit`, when the held cover is released if the deposit has not been authorised. The cart lease of the deposit line (15 minutes, audit R169)."
   },
   "refundableUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "`startsAt` less `dining.refundableUntilHours`. Cancelling before it releases the deposit in full."
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "description": "The venue's table-deposit variant, `DepositPolicy.dining.depositVariantId`, which the client sends to `addCartLine` with this booking's id."
   },
   "cartLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `orders.CartLine` carrying the deposit, once added."
   },
   "depositId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `orders.deposit` row, once the payment is authorised."
   }
  }
 },
 "TableReservationStatus": {
  "type": "string",
  "description": "`awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`.",
  "enum": [
   "awaitingDeposit",
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
  "description": "Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n",
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
    "type": "boolean",
    "x-ticvai-derived": "onRead",
    "description": "True once any version has been published."
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
    "type": "string",
    "description": "Staff only."
   },
   "hasUnpublishedChanges": {
    "type": "boolean",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. The working draft differs from the current version's `snapshot`."
   },
   "activeModuleCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. `ModuleEnablement` rows with `isEnabled` true."
   },
   "licensedModuleCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. `ModuleEnablement` rows with `isLicensed` true."
   },
   "activePageCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. Content pages that are `published` and enabled."
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
   "minimumAppVersion": {
    "$ref": "#/components/schemas/MinimumAppVersion"
   },
   "contact": {
    "$ref": "#/components/schemas/VenueContact"
   },
   "availability": {
    "$ref": "#/components/schemas/AppAvailability"
   },
   "availabilityMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "What the sold-out or closed screen says (WEB-029). Null shows the default wording."
   },
   "venues": {
    "type": "array",
    "maxItems": 200,
    "x-ticvai-derived": "onRead",
    "description": "**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n",
    "items": {
     "type": "object",
     "required": [
      "venueId",
      "name"
     ],
     "properties": {
      "venueId": {
       "type": "string",
       "format": "uuid",
       "description": "**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."
      },
      "name": {
       "type": "string",
       "maxLength": 200,
       "description": "The venue's name (`tenancy.OrgUnit.name`)."
      },
      "city": {
       "type": "string",
       "maxLength": 120,
       "nullable": true,
       "description": "Shown under the name so two venues with similar names can be told apart."
      },
      "openingHoursToday": {
       "type": "object",
       "nullable": true,
       "description": "Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.",
       "properties": {
        "opens": {
         "type": "string",
         "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$"
        },
        "closes": {
         "type": "string",
         "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$"
        }
       }
      }
     }
    }
   },
   "whatsNew": {
    "type": "array",
    "maxItems": 10,
    "x-ticvai-derived": "onRead",
    "description": "**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n",
    "items": {
     "type": "object",
     "required": [
      "version",
      "publishedAt",
      "notes"
     ],
     "properties": {
      "version": {
       "type": "string",
       "description": "The release version."
      },
      "publishedAt": {
       "type": "string",
       "format": "date-time",
       "description": "When the release reached the tenant's cell."
      },
      "notes": {
       "$ref": "#/components/schemas/LocalisedText"
      }
     }
    }
   },
   "recentChanges": {
    "type": "array",
    "description": "Staff only. Names the principal behind each change, so it never reaches a public response.",
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
 "UpdateParkingEntitlementRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; applied to access.parking_entitlement",
  "description": "**The body of `updateParkingEntitlement`: only what changes.** A partial update, so a field left out keeps its stored value. Two changes are possible, one per call:\n- **A plate change** — `plateNumber`, and `plateCountry` where it differs. The new plate is re-pushed and the old one leaves the whitelist. Resending the current plate is how a failed push is retried.\n- **A revoke** — `status: revoked`. The plate leaves the whitelist and the entitlement is terminal.\nA body carrying both, or neither, is a `400`. Which states allow each change is `states/parking-entitlement.yaml`'s to say.\n",
  "minProperties": 1,
  "properties": {
   "plateNumber": {
    "type": "string",
    "description": "Personal data, under the same rules as `ParkingEntitlement.plateNumber`."
   },
   "plateCountry": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "revoked"
    ],
    "description": "The only status a caller may set. Every other move is the server's."
   }
  }
 },
 "VenueContact": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n",
  "properties": {
   "phone": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true
   },
   "whatsapp": {
    "type": "string",
    "nullable": true
   },
   "address": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "openingHours": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "Prose, as the guest reads it. The bookable hours are the catalogue's."
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
    "description": "**Bumped by a publish or a closure**, and stored as `VenueMap.graphVersion`. A client holding an older version knows its route may cross something that closed, and asking for the graph is cheaper than asking whether the graph changed.\n"
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
      "isStepFree": {
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
    "description": "**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag.\n",
    "items": {
     "type": "string",
     "maxLength": 30
    }
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The client-generated ULID from `JoinQueueRequest.id`, and the `entryId` every entry path takes. `listMyWaitingGuests` gives it back to a guest who has lost it.\n"
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
    "allOf": [
     {
      "$ref": "#/components/schemas/WaitlistStatus"
     }
    ],
    "readOnly": true,
    "description": "Set by the server. `joinWaitlist` does not take it; a new entry is `waiting`."
   },
   "position": {
    "type": "integer",
    "readOnly": true,
    "description": "First in, first offered. Shown to the guest, because not knowing is worse than waiting."
   },
   "offeredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "offerExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
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
