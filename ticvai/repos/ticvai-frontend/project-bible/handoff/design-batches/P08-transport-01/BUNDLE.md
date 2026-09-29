# P08-transport-01 — P08 · Transport

**7 screens · 27 operations · 34 schemas · 5 permissions**

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
  `ASSET_LIBRARY_MANAGE, PERFORMANCE_CONFIGURE, TRANSPORT_MANAGE, TRANSPORT_PRICE, TRANSPORT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1183` | Transport Stations | listDetail | 3 | 2 | — |
| `BO-1184` | Transport Routes & Stops | listDetail | 6 | 3 | — |
| `BO-1185` | Transport Fares & Passenger Types | configEditor | 4 | 1 | — |
| `BO-1186` | Transport Timetables | listDetail | 6 | 3 | — |
| `BO-1187` | Transport Departure Board | listDetail | 4 | 2 | — |
| `BO-1188` | Transport Pass Types | listDetail | 4 | 1 | — |
| `BO-1189` | Transport Network Import | configEditor | 5 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1183",
  "name": "Transport Stations",
  "module": "Transport",
  "requiresModule": "transport",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/transport/stations",
   "component": "apps/venue-management-web/src/routes/transport/TransportStations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-108",
    "BO-1184"
   ],
   "exitTo": [
    "BO-1184",
    "BO-1189"
   ],
   "inferred": false,
   "notes": "Part of the transport setup set (BO-1183 to BO-1189), reached from BO-108 Venue Operations and from the routes screen.",
   "transitions": [
    {
     "to": "BO-1184",
     "trigger": "Routes and stops",
     "provenance": "authored 29 September, rev 3 REV3-21"
    },
    {
     "to": "BO-1189",
     "trigger": "Import stations, routes and timetables",
     "provenance": "authored 29 September, rev 3 REV3-21"
    }
   ]
  },
  "notes": "**Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). Stations come first: a route is an ordered list of them. **A station carries coordinates** because the route map places it; one without them is listed in the stop list and left off the map.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTransportStations` reads the population and the panel acts on one of them — list, select, act",
  "purpose": "Create, edit and retire the stations a venue's routes stop at.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Station code or name",
       "notes": "Filters the loaded page by code and name, in either language.",
       "provenance": "authored 29 September, rev 3 REV3-21"
      },
      {
       "kind": "toggle",
       "label": "Include retired stations",
       "operation": "listTransportStations",
       "notes": "Sends `?includeInactive=true`; retired stations are shown greyed.",
       "provenance": "contract transport.yaml GET /transport/stations"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every station at this venue",
       "bindsTo": "Station",
       "columns": [
        "Station.code",
        "Station.name",
        "Station.shortName",
        "Station.latitude",
        "Station.longitude",
        "Station.active"
       ],
       "operation": "listTransportStations",
       "notes": "A station with no coordinates is marked \"not on the map\".",
       "provenance": "contract transport.yaml GET /transport/stations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected station",
       "bindsTo": "Station",
       "columns": [
        "Station.id",
        "Station.code",
        "Station.name",
        "Station.shortName",
        "Station.latitude",
        "Station.longitude",
        "Station.active"
       ],
       "operation": "listTransportStations",
       "provenance": "contract transport.yaml GET /transport/stations"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "New station",
       "operation": "createTransportStation",
       "provenance": "contract transport.yaml POST /transport/stations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save station",
       "operation": "updateTransportStation",
       "provenance": "contract transport.yaml PATCH /transport/stations/{stationId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Reactivate station",
       "operation": "updateTransportStation",
       "notes": "Sends `active` true.",
       "provenance": "contract transport.yaml PATCH /transport/stations/{stationId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Retire station",
       "operation": "updateTransportStation",
       "notes": "Sends `active` false. **Refused `409` while the station is a stop on an active route**; the refusal names the routes, and the screen offers to open them.",
       "provenance": "contract transport.yaml PATCH /transport/stations/{stationId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue's stations, read by `listTransportStations`.",
   "error": "Could not load. Names which read failed and leaves the stations untouched.",
   "emptyFirstRun": "**No stations yet, so no route can be built.** Offers New station and Import stations, routes and timetables (BO-1189).",
   "emptyNoResults": "The search or the retired filter matched nothing and the stations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TRANSPORT_MANAGE`, which `createTransportStation` requires, and names that permission. **Never an empty table** — that reads as *there is no data*.",
   "validation": "`400` on a missing code or name or a coordinate out of range, marked on the field; `409` on a code already used at this venue, naming the station that holds it; `409` on retiring a station an active route stops at, naming the routes."
  },
  "apis": [
   {
    "operationId": "listTransportStations",
    "contract": "transport",
    "purpose": "The venue's stations, retired ones on request",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTransportStation",
    "contract": "transport",
    "purpose": "Add a station with its code, names and coordinates",
    "trigger": "onAction",
    "invalidates": [
     "listTransportStations"
    ]
   },
   {
    "operationId": "updateTransportStation",
    "contract": "transport",
    "purpose": "Rename, move, retire or reactivate a station",
    "trigger": "onAction",
    "invalidates": [
     "listTransportStations"
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
     "name": "stationId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the venue from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1183"
  },
  "overlays": [
   {
    "id": "formCreateTransportStation",
    "component": "modal",
    "trigger": "New station",
    "body": "**Collects what `createTransportStation` sends before it is called.** Required: `code` (unique at this venue), `name` (every tenant language). Optional: `shortName`, `latitude`, `longitude`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateStationRequest",
    "confirm": {
     "label": "Create station",
     "operation": "createTransportStation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "shortName",
      "latitude",
      "longitude"
     ]
    },
    "provenance": "contract transport.yaml POST /transport/stations"
   },
   {
    "id": "confirmRetireTransportStation",
    "component": "confirmDialog",
    "trigger": "Retire station",
    "body": "Names the station and says it stops being offered as a stop. Refused while an active route stops there; the dialog then lists those routes instead of retiring.",
    "confirm": {
     "label": "Retire station",
     "operation": "updateTransportStation"
    },
    "dismiss": {
     "label": "Keep it"
    },
    "provenance": "contract transport.yaml PATCH /transport/stations/{stationId}"
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
  "id": "BO-1184",
  "name": "Transport Routes & Stops",
  "module": "Transport",
  "requiresModule": "transport",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/transport/routes",
   "component": "apps/venue-management-web/src/routes/transport/TransportRoutes.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-108"
   ],
   "exitTo": [
    "BO-108",
    "BO-1183",
    "BO-1185",
    "BO-1186",
    "BO-1187",
    "BO-1188",
    "BO-1189"
   ],
   "inferred": false,
   "notes": "**The hub of the transport setup set.** Every other transport setup screen is one route away from here.",
   "transitions": [
    {
     "to": "BO-108",
     "trigger": "Venue Operations",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "back": true
    },
    {
     "to": "BO-1183",
     "trigger": "Stations",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "carries": [
      "stationId"
     ]
    },
    {
     "to": "BO-1185",
     "trigger": "Fares and passenger types",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "carries": [
      "routeId"
     ]
    },
    {
     "to": "BO-1186",
     "trigger": "Timetables",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "carries": [
      "routeId"
     ]
    },
    {
     "to": "BO-1187",
     "trigger": "Departure board",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "carries": [
      "routeId"
     ]
    },
    {
     "to": "BO-1188",
     "trigger": "Pass types",
     "provenance": "authored 29 September, rev 3 REV3-21"
    },
    {
     "to": "BO-1189",
     "trigger": "Import stations, routes and timetables",
     "provenance": "authored 29 September, rev 3 REV3-21"
    }
   ]
  },
  "notes": "**Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). A line run both ways is two routes (outbound and inbound) paired by `pairedRouteId`, which is what the guest's swap button lands on. **Creating a route creates its catalogue side** (an event its departures become performances of, and a timed-admission product whose variants are the passenger types), so a one-way ticket sells through the ordinary cart. Lifecycle draft, active, suspended, retired (states/transport-route.yaml).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTransportRoutes` reads the population and `getTransportRoute` reads one of them — list, select, act",
  "purpose": "Create, edit, activate, suspend and retire a venue's routes and their ordered stops.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Status",
       "operation": "listTransportRoutes",
       "notes": "Sends `?status=`, draft, active, suspended or retired. Defaults to everything but retired.",
       "provenance": "contract transport.yaml GET /transport/routes"
      },
      {
       "kind": "selectField",
       "label": "Serves station",
       "operation": "listTransportRoutes",
       "notes": "Sends `?fromStationId=`; stations from `listTransportStations`.",
       "provenance": "contract transport.yaml GET /transport/routes"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every route at this venue",
       "bindsTo": "TransportRoute",
       "columns": [
        "TransportRoute.code",
        "TransportRoute.lineCode",
        "TransportRoute.name",
        "TransportRoute.colour",
        "TransportRoute.status",
        "TransportRoute.pairedRouteId",
        "TransportRoute.totalMinutes",
        "TransportRoute.bookingCutoffMinutes"
       ],
       "operation": "listTransportRoutes",
       "notes": "A draft route shows what it still needs before it can go live (a fare table, two stops).",
       "provenance": "contract transport.yaml GET /transport/routes"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected route and its stops",
       "bindsTo": "TransportRoute",
       "columns": [
        "TransportRoute.code",
        "TransportRoute.lineCode",
        "TransportRoute.name",
        "TransportRoute.status",
        "TransportRoute.pairedRouteId",
        "TransportRoute.bookingCutoffMinutes",
        "TransportRoute.stops",
        "TransportRoute.totalMinutes",
        "TransportRoute.catalogueEventId",
        "TransportRoute.catalogueProductId"
       ],
       "operation": "getTransportRoute",
       "notes": "**Stops in order with their offset in minutes from the first**, which starts at 0 and strictly increases; arrival time and duration on a departure card are the difference of two offsets.",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}"
      },
      {
       "kind": "publishGate",
       "label": "What activating the route changes",
       "impliedBy": "setTransportRouteStatus",
       "notes": "Activating needs a fare table and at least two stops, and makes the route searchable by guests; its departures go on sale when a timetable is published (BO-1186). Suspending stops new sales and keeps sold tickets valid. Retiring is refused while a departure on sale has sold seats.",
       "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/status"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "New route",
       "operation": "createTransportRoute",
       "provenance": "contract transport.yaml POST /transport/routes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save route",
       "operation": "updateTransportRoute",
       "notes": "Name, colour, pairing and booking cut-off change at any time. **Stops change only while no published timetable covers a future date** (`409`): withdraw the timetable first.",
       "provenance": "contract transport.yaml PATCH /transport/routes/{routeId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Activate, suspend or reactivate",
       "operation": "setTransportRouteStatus",
       "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/status"
      },
      {
       "kind": "destructiveButton",
       "label": "Retire route",
       "operation": "setTransportRouteStatus",
       "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/status"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue's routes, read by `listTransportRoutes`.",
   "error": "Could not load. Names which read failed and leaves the routes untouched.",
   "emptyFirstRun": "**No routes yet.** Offers New route (needs at least two stations, BO-1183) and Import stations, routes and timetables (BO-1189).",
   "emptyNoResults": "The status or station filter matched nothing and the routes are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportTimetables` and the setup screens require, and names that permission. **Never an empty table**.",
   "validation": "`422` on fewer than two stops, a station repeated, a station inactive or not at this venue, or offsets that do not start at 0 and strictly increase, each marked on the stop row; `409` on a code already used; `409` on a stop change under a published timetable; `409` on a status change the route cannot make (no fare table, or retiring with sold seats), naming what is missing."
  },
  "apis": [
   {
    "operationId": "listTransportRoutes",
    "contract": "transport",
    "purpose": "The venue's routes, by status and station",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTransportRoute",
    "contract": "transport",
    "purpose": "One route with its ordered stops",
    "trigger": "onAction"
   },
   {
    "operationId": "listTransportStations",
    "contract": "transport",
    "purpose": "Stations to build stops from",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTransportRoute",
    "contract": "transport",
    "purpose": "Create a route as a draft, with its stops; creates its catalogue event and product",
    "trigger": "onAction",
    "invalidates": [
     "listTransportRoutes"
    ]
   },
   {
    "operationId": "updateTransportRoute",
    "contract": "transport",
    "purpose": "Change name, colour, pairing, cut-off, or stops while no published timetable covers a future date",
    "trigger": "onAction",
    "invalidates": [
     "listTransportRoutes",
     "getTransportRoute"
    ]
   },
   {
    "operationId": "setTransportRouteStatus",
    "contract": "transport",
    "purpose": "Activate, suspend, reactivate or retire a route",
    "trigger": "onAction",
    "invalidates": [
     "listTransportRoutes",
     "getTransportRoute"
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
     "name": "routeId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the venue from the session and opens on the route list; a route id that is gone says so."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1184"
  },
  "overlays": [
   {
    "id": "formCreateTransportRoute",
    "component": "modal",
    "trigger": "New route",
    "body": "**Collects what `createTransportRoute` sends before it is called.** Required: `code`, `name`, `stops` (stations in order, each with its offset in minutes; the first is 0). Optional: `lineCode`, `colour`, `pairedRouteId` (the same line the other way), `bookingCutoffMinutes`. Created as a draft; nothing is on sale. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateTransportRouteRequest",
    "confirm": {
     "label": "Create route",
     "operation": "createTransportRoute"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "lineCode",
      "name",
      "colour",
      "pairedRouteId",
      "bookingCutoffMinutes",
      "stops"
     ]
    },
    "provenance": "contract transport.yaml POST /transport/routes"
   },
   {
    "id": "confirmSetTransportRouteStatus",
    "component": "confirmDialog",
    "trigger": "Activate, suspend or reactivate",
    "body": "Names the route and the consequence of the new status for guests and for tickets already sold. Captures a `reason` for a suspension.",
    "confirm": {
     "label": "Change status",
     "operation": "setTransportRouteStatus"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/status"
   },
   {
    "id": "confirmRetireTransportRoute",
    "component": "confirmDialog",
    "trigger": "Retire route",
    "body": "**Retiring is final.** Refused while a departure still on sale has sold seats; the dialog then names those departures and offers the departure board (BO-1187) to cancel them first.",
    "confirm": {
     "label": "Retire route",
     "operation": "setTransportRouteStatus"
    },
    "dismiss": {
     "label": "Keep it"
    },
    "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/status"
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
  "id": "BO-1185",
  "name": "Transport Fares & Passenger Types",
  "module": "Transport",
  "requiresModule": "transport",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/transport/fares",
   "component": "apps/venue-management-web/src/routes/transport/TransportFares.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1184"
   ],
   "exitTo": [
    "BO-1184"
   ],
   "inferred": false,
   "transitions": [
    {
     "to": "BO-1184",
     "trigger": "Routes and stops",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "back": true,
     "carries": [
      "routeId"
     ]
    }
   ]
  },
  "notes": "**Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). **The fares are the venue's, set by a holder of `TRANSPORT_PRICE`**, a separate permission from the timetable because the person who edits a timetable is not the one who sets fares. A route has no fare table until one is set here, and cannot be activated without one. The prototype's values (base AED 5, AED 2.50 per stop; child and student half fare, person of determination free) are seed data for the demo tenant, not a default.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "one fare table per route, replaced as a whole — settings that take effect on sales from a date, not a list",
  "purpose": "Set a route's fares and the passenger types it sells, and preview what a trip costs.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "filters",
     "slot": "scope",
     "components": [
      {
       "kind": "selectField",
       "label": "Route",
       "operation": "listTransportRoutes",
       "notes": "The route whose fare table is edited; path `routeId`.",
       "provenance": "contract transport.yaml GET /transport/routes"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Fare model",
       "bindsTo": "FareTable.model",
       "operation": "setTransportFareTable",
       "notes": "`stopCount` (a base fare plus a fare per stop travelled) or `matrix` (a fare per ordered station pair). A matrix must cover every pair the route serves (`422`, naming the missing pairs).",
       "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/fare-table"
      },
      {
       "kind": "numberField",
       "label": "Base fare",
       "bindsTo": "FareTable.baseFare",
       "operation": "setTransportFareTable",
       "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/fare-table"
      },
      {
       "kind": "numberField",
       "label": "Fare per stop",
       "bindsTo": "FareTable.perStopFare",
       "operation": "setTransportFareTable",
       "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/fare-table"
      },
      {
       "kind": "dataTable",
       "label": "Fares by station pair",
       "bindsTo": "FareTable.matrix",
       "operation": "getTransportFareTable",
       "notes": "Shown for the `matrix` model only.",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/fare-table"
      },
      {
       "kind": "dataTable",
       "label": "Passenger types",
       "bindsTo": "FareTable.passengerTypes",
       "operation": "getTransportFareTable",
       "notes": "**Each type with its multiplier (0 to 1), age band and the proof the driver checks** (student card, Sanad card). Codes unique, exactly one default. Adding or removing a type adds or retires the matching variant on the route's catalogue product.",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/fare-table"
      },
      {
       "kind": "datePicker",
       "label": "Applies to sales from",
       "bindsTo": "FareTable.effectiveFrom",
       "operation": "setTransportFareTable",
       "notes": "A ticket already sold keeps its price.",
       "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/fare-table"
      },
      {
       "kind": "detailPanel",
       "label": "Fare preview",
       "bindsTo": "FareQuote",
       "columns": [
        "FareQuote.stopsTravelled",
        "FareQuote.adultFare",
        "FareQuote.lines",
        "FareQuote.total"
       ],
       "operation": "quoteTransportFare",
       "notes": "Pick two stations and a party; shows what the guest will pay, from the same pricing rule the cart uses. Previews the saved table; save first to preview a change.",
       "provenance": "contract transport.yaml POST /transport/fare-quotes"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save fare table",
       "operation": "setTransportFareTable",
       "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/fare-table"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "provenance": "authored 29 September, rev 3 REV3-21"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The route's fare table, read by `getTransportFareTable`.",
   "error": "Could not load. Names which read failed and leaves the fare table untouched.",
   "emptyNoResults": "A route picked with no fare table opens the empty form, named as the first-run state for that route.",
   "emptyFirstRun": "**This route has no fares yet, so it cannot be activated or sold.** The form opens empty with the fare models explained.",
   "emptyNoAccess": "Shown when the caller lacks `TRANSPORT_PRICE`, which `setTransportFareTable` requires, and names that permission; a `TRANSPORT_VIEW` holder sees the table read-only.",
   "validation": "`422` on a matrix missing a station pair, a passenger type code repeated, no default type or a multiplier outside 0 to 1, each marked on its row."
  },
  "apis": [
   {
    "operationId": "listTransportRoutes",
    "contract": "transport",
    "purpose": "The route picker",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTransportFareTable",
    "contract": "transport",
    "purpose": "The route's fare table and passenger types",
    "trigger": "onLoad"
   },
   {
    "operationId": "setTransportFareTable",
    "contract": "transport",
    "purpose": "Replace the route's fare table from a date",
    "trigger": "onAction",
    "invalidates": [
     "getTransportFareTable"
    ]
   },
   {
    "operationId": "quoteTransportFare",
    "contract": "transport",
    "purpose": "Preview a trip's price for a party",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "routeId",
     "from": "BO-1184"
    }
   ],
   "coldEntry": "Opens on the route picker when no route is carried."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1185"
  },
  "overlays": [
   {
    "id": "confirmSetTransportFareTable",
    "component": "confirmDialog",
    "trigger": "Save fare table",
    "body": "**Names the route and the date the new fares apply from**, and that tickets already sold keep their price. Lists passenger types added or removed, since each adds or retires a ticket variant.",
    "confirm": {
     "label": "Save fares",
     "operation": "setTransportFareTable"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract transport.yaml PUT /transport/routes/{routeId}/fare-table"
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
  "id": "BO-1186",
  "name": "Transport Timetables",
  "module": "Transport",
  "requiresModule": "transport",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/transport/timetables",
   "component": "apps/venue-management-web/src/routes/transport/TransportTimetables.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1184"
   ],
   "exitTo": [
    "BO-1184",
    "BO-1187"
   ],
   "inferred": false,
   "transitions": [
    {
     "to": "BO-1184",
     "trigger": "Routes and stops",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "back": true,
     "carries": [
      "routeId"
     ]
    },
    {
     "to": "BO-1187",
     "trigger": "Departure board",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "carries": [
      "routeId"
     ]
    }
   ]
  },
  "notes": "**Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). A timetable is departure times from the route's origin by day of week, valid over a date range. **Nothing is on sale until it is published**; publishing generates the departures up to the release horizon (proposed 30 days, client to correct) as catalogue performances, and a nightly job releases one more day. A published timetable is never edited: a new one drafted from a later date supersedes it from that date (states/transport-timetable.yaml).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTransportTimetables` reads the route's timetables and the panel acts on one of them — list, select, act",
  "purpose": "Draft, publish and withdraw a route's timetables.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Route",
       "operation": "listTransportRoutes",
       "notes": "Path `routeId` of `listTransportTimetables`.",
       "provenance": "contract transport.yaml GET /transport/routes"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "operation": "listTransportTimetables",
       "notes": "Sends `?status=`, draft, published, superseded or withdrawn.",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/timetables"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every timetable on this route",
       "bindsTo": "Timetable",
       "columns": [
        "Timetable.name",
        "Timetable.status",
        "Timetable.validFrom",
        "Timetable.validTo",
        "Timetable.releaseHorizonDays",
        "Timetable.seatCapacity",
        "Timetable.publishedAt",
        "Timetable.releasedThrough",
        "Timetable.supersededById"
       ],
       "operation": "listTransportTimetables",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/timetables"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected timetable",
       "bindsTo": "Timetable",
       "columns": [
        "Timetable.name",
        "Timetable.status",
        "Timetable.validFrom",
        "Timetable.validTo",
        "Timetable.releaseHorizonDays",
        "Timetable.seatCapacity",
        "Timetable.seatMapId",
        "Timetable.runs"
       ],
       "operation": "listTransportTimetables",
       "notes": "`runs`: departure times by day of week, shown as a week grid.",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/timetables"
      },
      {
       "kind": "publishGate",
       "label": "What publishing puts on sale",
       "impliedBy": "publishTransportTimetable",
       "notes": "**Names the departures it creates and the dates they cover**, and the published timetable it supersedes from `validFrom`, whose unsold departures on or after that date are removed. Refused `409` when the route is not active or has no fare table, or when a superseded departure with sold seats falls on or after `validFrom`.",
       "provenance": "contract transport.yaml POST /transport/timetables/{timetableId}/publish"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "New timetable",
       "operation": "createTransportTimetable",
       "provenance": "contract transport.yaml POST /transport/routes/{routeId}/timetables"
      },
      {
       "kind": "secondaryButton",
       "label": "Save draft",
       "operation": "updateTransportTimetable",
       "notes": "A draft only; a published timetable is refused `409`. Draft a new one from a later date instead.",
       "provenance": "contract transport.yaml PATCH /transport/timetables/{timetableId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishTransportTimetable",
       "provenance": "contract transport.yaml POST /transport/timetables/{timetableId}/publish"
      },
      {
       "kind": "destructiveButton",
       "label": "Withdraw",
       "operation": "withdrawTransportTimetable",
       "notes": "Removes its unsold future departures and stops releasing new ones. Refused `409` while a future departure has sold seats; cancel those on the departure board first.",
       "provenance": "contract transport.yaml POST /transport/timetables/{timetableId}/withdraw"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The route's timetables, read by `listTransportTimetables`.",
   "error": "Could not load. Names which read failed and leaves the timetables untouched.",
   "emptyFirstRun": "**No timetable on this route, so nothing is on sale.** Offers New timetable and Import stations, routes and timetables (BO-1189).",
   "emptyNoResults": "The status filter matched nothing and the route's other timetables are still there. Names the filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportTimetables` requires, and names that permission. **Never an empty table**.",
   "validation": "`400` on a missing name, start date, capacity or run, or a run time out of order, marked on the field; `409` on editing a published timetable, on publishing against an inactive route or one with no fare table, and on withdrawing with sold seats, each naming the cause."
  },
  "apis": [
   {
    "operationId": "listTransportRoutes",
    "contract": "transport",
    "purpose": "The route picker",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTransportTimetables",
    "contract": "transport",
    "purpose": "The route's timetables, by status",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTransportTimetable",
    "contract": "transport",
    "purpose": "Draft a timetable",
    "trigger": "onAction",
    "invalidates": [
     "listTransportTimetables"
    ]
   },
   {
    "operationId": "updateTransportTimetable",
    "contract": "transport",
    "purpose": "Edit a draft timetable",
    "trigger": "onAction",
    "invalidates": [
     "listTransportTimetables"
    ]
   },
   {
    "operationId": "publishTransportTimetable",
    "contract": "transport",
    "purpose": "Publish, generating the departures and putting them on sale",
    "trigger": "onAction",
    "invalidates": [
     "listTransportTimetables"
    ]
   },
   {
    "operationId": "withdrawTransportTimetable",
    "contract": "transport",
    "purpose": "Stop a timetable; its unsold future departures are removed",
    "trigger": "onAction",
    "invalidates": [
     "listTransportTimetables"
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
     "name": "routeId",
     "from": "BO-1184"
    },
    {
     "name": "timetableId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opens on the route picker when no route is carried."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1186"
  },
  "overlays": [
   {
    "id": "formCreateTransportTimetable",
    "component": "modal",
    "trigger": "New timetable",
    "body": "**Collects what `createTransportTimetable` sends before it is called.** Required: `name`, `validFrom`, `seatCapacity`, `runs` (departure times from the origin by day of week). Optional: `validTo`, `releaseHorizonDays` (proposed 30), `seatMapId` for a coach with numbered seats. Created as a draft. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateTimetableRequest",
    "confirm": {
     "label": "Create draft",
     "operation": "createTransportTimetable"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "validFrom",
      "validTo",
      "releaseHorizonDays",
      "seatCapacity",
      "seatMapId",
      "runs"
     ]
    },
    "provenance": "contract transport.yaml POST /transport/routes/{routeId}/timetables"
   },
   {
    "id": "confirmPublishTransportTimetable",
    "component": "confirmDialog",
    "trigger": "Publish",
    "body": "Names the dates and the number of departures that go on sale, and the timetable it supersedes and from when.",
    "confirm": {
     "label": "Publish and put on sale",
     "operation": "publishTransportTimetable"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract transport.yaml POST /transport/timetables/{timetableId}/publish"
   },
   {
    "id": "confirmWithdrawTransportTimetable",
    "component": "confirmDialog",
    "trigger": "Withdraw",
    "body": "**Collects the `reason`** and names the unsold departures that are removed. Refused while a future departure has sold seats.",
    "confirm": {
     "label": "Withdraw timetable",
     "operation": "withdrawTransportTimetable"
    },
    "dismiss": {
     "label": "Keep it"
    },
    "provenance": "contract transport.yaml POST /transport/timetables/{timetableId}/withdraw"
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
  "id": "BO-1187",
  "name": "Transport Departure Board",
  "module": "Transport",
  "requiresModule": "transport",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/transport/departures",
   "component": "apps/venue-management-web/src/routes/transport/TransportDepartureBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1184",
    "BO-1186"
   ],
   "exitTo": [
    "BO-1184"
   ],
   "inferred": false,
   "transitions": [
    {
     "to": "BO-1184",
     "trigger": "Routes and stops",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "back": true,
     "carries": [
      "routeId"
     ]
    }
   ]
  },
  "notes": "**Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). Every departure the published timetables generated, in every status, with seats sold and the vehicle. A bigger or smaller coach on one run is changed here; **a departure is cancelled through its catalogue performance** (`cancelPerformance`), so every guest affected is refunded and told through the ordinary performance-cancelled path (states/transport-departure.yaml).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTransportRouteDepartures` reads the population and the panel acts on one departure — list, select, act",
  "purpose": "See every departure on a route with seats sold, change a run's coach or capacity, and cancel a run.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Route",
       "operation": "listTransportRoutes",
       "notes": "Path `routeId` of `listTransportRouteDepartures`.",
       "provenance": "contract transport.yaml GET /transport/routes"
      },
      {
       "kind": "datePicker",
       "label": "From and to",
       "operation": "listTransportRouteDepartures",
       "notes": "Sends `?from=` and `?to=`; defaults to today and the next seven days.",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/departures"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "operation": "listTransportRouteDepartures",
       "notes": "Sends `?status=`.",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/departures"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every departure in the range",
       "bindsTo": "Departure",
       "columns": [
        "Departure.serviceDate",
        "Departure.departsAt",
        "Departure.status",
        "Departure.seatCapacity",
        "Departure.seatsSold",
        "Departure.vehicleResourceId",
        "Departure.timetableId",
        "Departure.note"
       ],
       "operation": "listTransportRouteDepartures",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/departures"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected departure",
       "bindsTo": "Departure",
       "columns": [
        "Departure.id",
        "Departure.serviceDate",
        "Departure.departsAt",
        "Departure.status",
        "Departure.seatCapacity",
        "Departure.seatsSold",
        "Departure.vehicleResourceId",
        "Departure.performanceId",
        "Departure.note"
       ],
       "operation": "listTransportRouteDepartures",
       "provenance": "contract transport.yaml GET /transport/routes/{routeId}/departures"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save departure",
       "operation": "updateTransportDeparture",
       "notes": "Capacity, vehicle and note. **Capacity cannot go below the seats already sold** (`422`).",
       "provenance": "contract transport.yaml PATCH /transport/departures/{departureId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel departure",
       "operation": "cancelPerformance",
       "notes": "Cancels the departure's catalogue performance; guests holding tickets are refunded and told.",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The route's departures, read by `listTransportRouteDepartures`.",
   "error": "Could not load. Names which read failed and leaves the departures untouched.",
   "emptyFirstRun": "**No departures on this route**, because no timetable is published. Offers Timetables (BO-1186).",
   "emptyNoResults": "The date range or status matched nothing and the route's other departures are still there. Names the filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportRouteDepartures` requires, and names that permission. **Never an empty table**.",
   "validation": "`422` on a capacity below the seats sold, naming the count; a cancellation follows the performance cancel rules (reason required, supervisor step-up for a real run)."
  },
  "apis": [
   {
    "operationId": "listTransportRoutes",
    "contract": "transport",
    "purpose": "The route picker",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTransportRouteDepartures",
    "contract": "transport",
    "purpose": "Every departure on the route with seats sold",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateTransportDeparture",
    "contract": "transport",
    "purpose": "Change one run's capacity, vehicle or note",
    "trigger": "onAction",
    "invalidates": [
     "listTransportRouteDepartures"
    ]
   },
   {
    "operationId": "cancelPerformance",
    "contract": "catalogue",
    "purpose": "Cancel a departure through its performance, refunding and telling guests",
    "trigger": "onAction",
    "invalidates": [
     "listTransportRouteDepartures"
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
     "name": "routeId",
     "from": "BO-1184"
    },
    {
     "name": "departureId",
     "from": "navigation"
    },
    {
     "name": "performanceId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opens on the route picker when no route is carried."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1187"
  },
  "overlays": [
   {
    "id": "formUpdateTransportDeparture",
    "component": "modal",
    "trigger": "Save departure",
    "body": "**Collects what `updateTransportDeparture` sends before it is called.** Optional: `seatCapacity` (not below seats sold), `vehicleResourceId`, `note`. The new capacity is written to the performance's channel capacity. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save departure",
     "operation": "updateTransportDeparture"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "seatCapacity",
      "vehicleResourceId",
      "note"
     ]
    },
    "provenance": "contract transport.yaml PATCH /transport/departures/{departureId}"
   },
   {
    "id": "confirmCancelDeparture",
    "component": "confirmDialog",
    "trigger": "Cancel departure",
    "body": "**Names the departure and the passengers affected**, and that each is refunded and told. Collects what `cancelPerformance` needs: a `reason`, an optional guest message, and a supervisor PIN for a real run (audit R144).",
    "confirm": {
     "label": "Cancel departure",
     "operation": "cancelPerformance"
    },
    "dismiss": {
     "label": "Keep it"
    },
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
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
  "id": "BO-1188",
  "name": "Transport Pass Types",
  "module": "Transport",
  "requiresModule": "transport",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/transport/pass-types",
   "component": "apps/venue-management-web/src/routes/transport/TransportPassTypes.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1184"
   ],
   "exitTo": [
    "BO-1184"
   ],
   "inferred": false,
   "transitions": [
    {
     "to": "BO-1184",
     "trigger": "Routes and stops",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "back": true
    }
   ]
  },
  "notes": "**Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). Multi-trip carnets and unlimited passes. **Creating a pass type creates its catalogue product** (open-dated, with entries allowed equal to the trips, or unlimited), so a pass sells through the ordinary cart and each boarding consumes an entry at the driver's scan. A pass already sold keeps its trips, validity and price. The prototype's four (5-trip, 10-trip, weekly and monthly unlimited) are seed data for the demo tenant, not a default.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listTransportPassTypes` reads the population and the panel acts on one of them — list, select, act",
  "purpose": "Create, edit, stop and resume selling a venue's transport passes.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pass type at this venue",
       "bindsTo": "PassType",
       "columns": [
        "PassType.code",
        "PassType.name",
        "PassType.kind",
        "PassType.trips",
        "PassType.fareMultiplier",
        "PassType.referenceTrips",
        "PassType.validityDays",
        "PassType.routeIds",
        "PassType.active"
       ],
       "operation": "listTransportPassTypes",
       "notes": "Shows each pass's saving against single fares (fare multiplier against reference trips).",
       "provenance": "contract transport.yaml GET /transport/pass-types"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pass type",
       "bindsTo": "PassType",
       "columns": [
        "PassType.code",
        "PassType.name",
        "PassType.description",
        "PassType.kind",
        "PassType.trips",
        "PassType.fareMultiplier",
        "PassType.referenceTrips",
        "PassType.validityDays",
        "PassType.routeIds",
        "PassType.sortOrder",
        "PassType.active",
        "PassType.catalogueProductId"
       ],
       "operation": "listTransportPassTypes",
       "provenance": "contract transport.yaml GET /transport/pass-types"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "New pass type",
       "operation": "createTransportPassType",
       "provenance": "contract transport.yaml POST /transport/pass-types"
      },
      {
       "kind": "secondaryButton",
       "label": "Save pass type",
       "operation": "updateTransportPassType",
       "notes": "Applies to passes sold after the change; a pass already sold keeps its terms.",
       "provenance": "contract transport.yaml PATCH /transport/pass-types/{passTypeId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume selling",
       "operation": "updateTransportPassType",
       "notes": "Sends `active` true.",
       "provenance": "contract transport.yaml PATCH /transport/pass-types/{passTypeId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Stop selling",
       "operation": "updateTransportPassType",
       "notes": "Sends `active` false. Passes already sold stay valid.",
       "provenance": "contract transport.yaml PATCH /transport/pass-types/{passTypeId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue's pass types, read by `listTransportPassTypes`.",
   "error": "Could not load. Names which read failed and leaves the pass types untouched.",
   "emptyNoResults": "Never shown: `listTransportPassTypes` takes no filter beyond the venue, so an empty list is the first-run state.",
   "emptyFirstRun": "**No passes on sale.** Guests can buy one-way trips only. Offers New pass type.",
   "emptyNoAccess": "Shown when the caller lacks `TRANSPORT_VIEW`, which `listTransportPassTypes` requires; creating and editing need `TRANSPORT_PRICE`, named on the disabled buttons.",
   "validation": "`400` on a missing field, a multi-trip pass with no trip count or an unlimited one with one, marked on the field; `409` on a code already used at this venue."
  },
  "apis": [
   {
    "operationId": "listTransportPassTypes",
    "contract": "transport",
    "purpose": "The venue's pass types",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTransportPassType",
    "contract": "transport",
    "purpose": "Create a pass type and its catalogue product",
    "trigger": "onAction",
    "invalidates": [
     "listTransportPassTypes"
    ]
   },
   {
    "operationId": "updateTransportPassType",
    "contract": "transport",
    "purpose": "Change a pass type for future sales, or stop or resume selling it",
    "trigger": "onAction",
    "invalidates": [
     "listTransportPassTypes"
    ]
   },
   {
    "operationId": "listTransportRoutes",
    "contract": "transport",
    "purpose": "Routes a pass can be limited to",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "passTypeId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the venue from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1188"
  },
  "overlays": [
   {
    "id": "formCreateTransportPassType",
    "component": "modal",
    "trigger": "New pass type",
    "body": "**Collects what `createTransportPassType` sends before it is called.** Required: `code`, `name`, `kind` (multi-trip or unlimited), `fareMultiplier` (the price as a multiple of the single adult fare), `referenceTrips` (what the saving is compared with), `validityDays`. Optional: `trips` (multi-trip only), `description`, `routeIds` (empty means every route), `sortOrder`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePassTypeRequest",
    "confirm": {
     "label": "Create pass type",
     "operation": "createTransportPassType"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "description",
      "kind",
      "trips",
      "fareMultiplier",
      "referenceTrips",
      "validityDays",
      "routeIds",
      "sortOrder"
     ]
    },
    "provenance": "contract transport.yaml POST /transport/pass-types"
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
  "id": "BO-1189",
  "name": "Transport Network Import",
  "module": "Transport",
  "requiresModule": "transport",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/transport/import",
   "component": "apps/venue-management-web/src/routes/transport/TransportNetworkImport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1184",
    "BO-1183"
   ],
   "exitTo": [
    "BO-1184"
   ],
   "inferred": false,
   "transitions": [
    {
     "to": "BO-1184",
     "trigger": "Routes and stops",
     "provenance": "authored 29 September, rev 3 REV3-21",
     "back": true
    }
   ]
  },
  "notes": "**Transport setup is the venue's own configuration** (decided 29 September, rev 3 REV3-21: the network is configured by the venue in Venue Management, not supplied by the client). **Bulk entry for an operator with more than a handful of stations to type**, on the venue-map pattern: upload, validate, review the preview and the findings, then a person applies. **Nothing is written until the preview is applied, and applying never puts anything on sale**: routes arrive as drafts, still need a fare table and activation, and timetables still need publishing. An active route's stops are never changed by an import.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "an upload, a preview and one apply — a staged change to the network, not a list",
  "purpose": "Upload a file of stations, routes and timetables, review what it would change and every finding, and apply it.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "fileUpload",
       "label": "Network file",
       "operation": "createUpload",
       "notes": "Uploaded to the asset library first (`createUpload`, then `completeUpload`); the import takes its asset id. `csvBundle` is a zip of four CSV files (stations, routes, route stops, timetables), header on row 1, UTF-8; `gtfs` is a GTFS static feed.",
       "provenance": "contract assets.yaml POST /media/uploads"
      },
      {
       "kind": "selectField",
       "label": "Format",
       "operation": "importTransportNetwork",
       "notes": "`csvBundle` or `gtfs`. Required.",
       "provenance": "contract transport.yaml POST /transport/network-imports"
      },
      {
       "kind": "multiSelect",
       "label": "Read",
       "operation": "importTransportNetwork",
       "notes": "`include`: stations, routes, timetables. Absent reads all three.",
       "provenance": "contract transport.yaml POST /transport/network-imports"
      },
      {
       "kind": "progressIndicator",
       "label": "Validating",
       "operation": "getTransportNetworkImport",
       "notes": "Polled while the status is `validating`; the operator may leave and come back.",
       "provenance": "contract transport.yaml GET /transport/network-imports/{importId}"
      },
      {
       "kind": "detailPanel",
       "label": "What the file would change",
       "bindsTo": "TransportNetworkImport",
       "columns": [
        "TransportNetworkImport.status",
        "TransportNetworkImport.preview",
        "TransportNetworkImport.findings",
        "TransportNetworkImport.createdBy",
        "TransportNetworkImport.createdAt",
        "TransportNetworkImport.appliedBy",
        "TransportNetworkImport.appliedAt"
       ],
       "operation": "getTransportNetworkImport",
       "notes": "**The preview lists stations, routes, stops and timetables to create and to update; the findings list each problem with its file, row and severity.** An error finding blocks Apply; a warning (such as `routeActiveStopsChanged`, whose stops the apply skips) is shown and does not.",
       "provenance": "contract transport.yaml GET /transport/network-imports/{importId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Validate file",
       "operation": "importTransportNetwork",
       "provenance": "contract transport.yaml POST /transport/network-imports"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply",
       "operation": "applyTransportNetworkImport",
       "notes": "Live only when the status is `previewReady` and there is no error finding. Refused `409` when the network changed since validation; validate again.",
       "provenance": "contract transport.yaml POST /transport/network-imports/{importId}/apply"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.** An unapplied preview expires after 7 days (proposed).",
       "provenance": "authored 29 September, rev 3 REV3-21"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The import, read by `getTransportNetworkImport`.",
   "error": "Could not load. Names which read failed; nothing has been written to the network.",
   "emptyFirstRun": "No import in progress. The form opens empty, with the two file formats explained and a template to download.",
   "emptyNoAccess": "Shown when the caller lacks `TRANSPORT_MANAGE`, which `importTransportNetwork` requires, and names that permission.",
   "validation": "`422` on a file that is not ready, not at this venue or not a zip; a `failed` import names why; error findings block Apply row by row; `409` on Apply when the network changed since validation."
  },
  "apis": [
   {
    "operationId": "createUpload",
    "contract": "assets",
    "purpose": "Upload the network file",
    "trigger": "onAction"
   },
   {
    "operationId": "completeUpload",
    "contract": "assets",
    "purpose": "Finish the upload so the import can read it",
    "trigger": "onAction"
   },
   {
    "operationId": "importTransportNetwork",
    "contract": "transport",
    "purpose": "Validate the file into a preview; writes nothing to the network",
    "trigger": "onAction"
   },
   {
    "operationId": "getTransportNetworkImport",
    "contract": "transport",
    "purpose": "The preview and every finding, polled while it validates",
    "trigger": "onAction"
   },
   {
    "operationId": "applyTransportNetworkImport",
    "contract": "transport",
    "purpose": "Apply the reviewed preview; nothing goes on sale",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "importId",
     "from": "deepLink"
    },
    {
     "name": "uploadId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A link to an import opened cold shows where it stands**: still validating, ready for review, failed, applied, or expired and needing a new upload."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1189"
  },
  "overlays": [
   {
    "id": "confirmApplyTransportNetworkImport",
    "component": "confirmDialog",
    "trigger": "Apply",
    "body": "**Names what is created and what is updated**, and that routes arrive as drafts and timetables unpublished: nothing goes on sale until a route is activated with a fare table and its timetable is published.",
    "confirm": {
     "label": "Apply to the network",
     "operation": "applyTransportNetworkImport"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract transport.yaml POST /transport/network-imports/{importId}/apply"
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "applyTransportNetworkImport": {
  "method": "POST",
  "path": "/transport/network-imports/{importId}/apply",
  "contract": "transport",
  "summary": "Apply a previewed import to the network",
  "permission": "TRANSPORT_MANAGE",
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
  "responds": "TransportNetworkImport"
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
 "completeUpload": {
  "method": "POST",
  "path": "/media/uploads/{uploadId}/complete",
  "contract": "assets",
  "summary": "Confirm an upload and create the asset",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "MediaAsset"
 },
 "createTransportPassType": {
  "method": "POST",
  "path": "/transport/pass-types",
  "contract": "transport",
  "summary": "Define a multi-trip or unlimited pass",
  "permission": "TRANSPORT_PRICE",
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
  "requestBody": "CreatePassTypeRequest",
  "responds": "PassType"
 },
 "createTransportRoute": {
  "method": "POST",
  "path": "/transport/routes",
  "contract": "transport",
  "summary": "Define a route with its ordered stops",
  "permission": "TRANSPORT_MANAGE",
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
  "requestBody": "CreateTransportRouteRequest",
  "responds": "TransportRoute"
 },
 "createTransportStation": {
  "method": "POST",
  "path": "/transport/stations",
  "contract": "transport",
  "summary": "Add a station",
  "permission": "TRANSPORT_MANAGE",
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
  "requestBody": "CreateStationRequest",
  "responds": "Station"
 },
 "createTransportTimetable": {
  "method": "POST",
  "path": "/transport/routes/{routeId}/timetables",
  "contract": "transport",
  "summary": "Draft a timetable for a route",
  "permission": "TRANSPORT_MANAGE",
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
  "requestBody": "CreateTimetableRequest",
  "responds": "Timetable"
 },
 "createUpload": {
  "method": "POST",
  "path": "/media/uploads",
  "contract": "assets",
  "summary": "Request a signed upload URL",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "UploadTicket"
 },
 "getTransportFareTable": {
  "method": "GET",
  "path": "/transport/routes/{routeId}/fare-table",
  "contract": "transport",
  "summary": "A route's fares and passenger types",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FareTable"
 },
 "getTransportNetworkImport": {
  "method": "GET",
  "path": "/transport/network-imports/{importId}",
  "contract": "transport",
  "summary": "An import's status, preview counts and findings",
  "permission": "TRANSPORT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TransportNetworkImport"
 },
 "getTransportRoute": {
  "method": "GET",
  "path": "/transport/routes/{routeId}",
  "contract": "transport",
  "summary": "A route with its stops",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TransportRoute"
 },
 "importTransportNetwork": {
  "method": "POST",
  "path": "/transport/network-imports",
  "contract": "transport",
  "summary": "Read a network file into a preview",
  "permission": "TRANSPORT_MANAGE",
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
  "requestBody": "ImportTransportNetworkRequest",
  "responds": null
 },
 "listTransportPassTypes": {
  "method": "GET",
  "path": "/transport/pass-types",
  "contract": "transport",
  "summary": "The venue's multi-trip pass types",
  "permission": "TRANSPORT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": true
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
 "listTransportRouteDepartures": {
  "method": "GET",
  "path": "/transport/routes/{routeId}/departures",
  "contract": "transport",
  "summary": "A route's departures, for operations",
  "permission": "TRANSPORT_VIEW",
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
 "listTransportRoutes": {
  "method": "GET",
  "path": "/transport/routes",
  "contract": "transport",
  "summary": "Routes, optionally those serving a pair of stations",
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
    "name": "fromStationId",
    "in": "query",
    "required": null
   },
   {
    "name": "toStationId",
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
 "listTransportStations": {
  "method": "GET",
  "path": "/transport/stations",
  "contract": "transport",
  "summary": "Stations of a venue's transport network",
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
 "listTransportTimetables": {
  "method": "GET",
  "path": "/transport/routes/{routeId}/timetables",
  "contract": "transport",
  "summary": "A route's timetables",
  "permission": "TRANSPORT_VIEW",
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
 "publishTransportTimetable": {
  "method": "POST",
  "path": "/transport/timetables/{timetableId}/publish",
  "contract": "transport",
  "summary": "Publish a timetable and release its departures",
  "permission": "TRANSPORT_MANAGE",
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
  "responds": "Timetable"
 },
 "quoteTransportFare": {
  "method": "POST",
  "path": "/transport/fare-quotes",
  "contract": "transport",
  "summary": "Price a one-way trip or a pass for a party",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "FareQuoteRequest",
  "responds": "FareQuote"
 },
 "setTransportFareTable": {
  "method": "PUT",
  "path": "/transport/routes/{routeId}/fare-table",
  "contract": "transport",
  "summary": "Set a route's fares and passenger types",
  "permission": "TRANSPORT_PRICE",
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
  "requestBody": "SetFareTableRequest",
  "responds": "FareTable"
 },
 "setTransportRouteStatus": {
  "method": "PUT",
  "path": "/transport/routes/{routeId}/status",
  "contract": "transport",
  "summary": "Activate, suspend or retire a route",
  "permission": "TRANSPORT_MANAGE",
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
  "responds": "TransportRoute"
 },
 "updateTransportDeparture": {
  "method": "PATCH",
  "path": "/transport/departures/{departureId}",
  "contract": "transport",
  "summary": "Change a departure's coach or capacity",
  "permission": "TRANSPORT_MANAGE",
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
  "responds": "Departure"
 },
 "updateTransportPassType": {
  "method": "PATCH",
  "path": "/transport/pass-types/{passTypeId}",
  "contract": "transport",
  "summary": "Amend or retire a pass type",
  "permission": "TRANSPORT_PRICE",
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
  "responds": "PassType"
 },
 "updateTransportRoute": {
  "method": "PATCH",
  "path": "/transport/routes/{routeId}",
  "contract": "transport",
  "summary": "Amend a route",
  "permission": "TRANSPORT_MANAGE",
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
  "responds": "TransportRoute"
 },
 "updateTransportStation": {
  "method": "PATCH",
  "path": "/transport/stations/{stationId}",
  "contract": "transport",
  "summary": "Amend or deactivate a station",
  "permission": "TRANSPORT_MANAGE",
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
  "responds": "Station"
 },
 "updateTransportTimetable": {
  "method": "PATCH",
  "path": "/transport/timetables/{timetableId}",
  "contract": "transport",
  "summary": "Amend a draft timetable",
  "permission": "TRANSPORT_MANAGE",
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
  "responds": "Timetable"
 },
 "withdrawTransportTimetable": {
  "method": "POST",
  "path": "/transport/timetables/{timetableId}/withdraw",
  "contract": "transport",
  "summary": "Withdraw a published timetable",
  "permission": "TRANSPORT_MANAGE",
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
  "responds": "Timetable"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreatePassTypeRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "venueId",
   "code",
   "name",
   "kind",
   "fareMultiplier",
   "referenceTrips",
   "validityDays"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 32,
    "x-ticvai-unique": "venue"
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "kind": {
    "type": "string",
    "enum": [
     "multiTrip",
     "unlimited"
    ]
   },
   "trips": {
    "type": "integer",
    "minimum": 2,
    "maximum": 100,
    "nullable": true,
    "description": "Journeys included. Required for `multiTrip`; null for `unlimited`."
   },
   "fareMultiplier": {
    "type": "number",
    "minimum": 0,
    "maximum": 1000,
    "description": "The pass price as a multiple of the single adult fare between its two stations."
   },
   "referenceTrips": {
    "type": "integer",
    "minimum": 1,
    "maximum": 1000,
    "description": "The single trips the saving is measured against — `trips` for a multi-trip card, an number the venue sets for unlimited (14 a week, 60 a month in the demo seed data).\n"
   },
   "validityDays": {
    "type": "integer",
    "minimum": 1,
    "maximum": 366
   },
   "routeIds": {
    "type": "array",
    "description": "Routes it is sold on. Empty means every active route in the venue.",
    "items": {
     "$ref": "#/components/schemas/Ulid"
    }
   },
   "sortOrder": {
    "type": "integer",
    "minimum": 0,
    "default": 0
   }
  }
 },
 "CreateStationRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "venueId",
   "code",
   "name"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 32,
    "x-ticvai-unique": "venue",
    "description": "Short operator code, e.g. `SHJ-JUB`. Unique in the venue."
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "shortName": {
    "$ref": "#/components/schemas/LocalisedText",
    "description": "The label on the route diagram and the map pin (`Union Sq`, `MoE`)."
   },
   "latitude": {
    "type": "number",
    "minimum": -90,
    "maximum": 90,
    "nullable": true
   },
   "longitude": {
    "type": "number",
    "minimum": -180,
    "maximum": 180,
    "nullable": true
   }
  }
 },
 "CreateTimetableRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "validFrom",
   "seatCapacity",
   "runs"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 120
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "releaseHorizonDays": {
    "type": "integer",
    "minimum": 1,
    "maximum": 365,
    "default": 30,
    "description": "How many days ahead departures go on sale. Proposed default 30, from the prototype, client to correct (rev 3 REV3-21).\n"
   },
   "seatCapacity": {
    "type": "integer",
    "minimum": 1,
    "maximum": 200,
    "description": "Seats per departure, unless a departure overrides it."
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The coach seat map for Seat Selection (`seating`). Null sells unallocated seats."
   },
   "runs": {
    "type": "array",
    "minItems": 1,
    "maxItems": 500,
    "items": {
     "$ref": "#/components/schemas/TimetableRun"
    }
   }
  }
 },
 "CreateTransportRouteRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "venueId",
   "code",
   "name",
   "stops"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 32,
    "x-ticvai-unique": "venue",
    "description": "The line and direction, e.g. `E101-Out`. Unique in the venue."
   },
   "lineCode": {
    "type": "string",
    "maxLength": 16,
    "description": "The public line number shared by both directions, e.g. `E101`."
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "colour": {
    "type": "string",
    "pattern": "^#[0-9a-fA-F]{6}$"
   },
   "pairedRouteId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The same line run the other way. The swap button lands on it."
   },
   "bookingCutoffMinutes": {
    "type": "integer",
    "minimum": 0,
    "maximum": 1440,
    "default": 5,
    "description": "How long before a departure leaves the boarding stop that online sale stops. Proposed default 5, from the prototype's \"Boarding closes five minutes before departure\", client to correct (rev 3 REV3-21).\n"
   },
   "stops": {
    "type": "array",
    "minItems": 2,
    "maxItems": 100,
    "items": {
     "$ref": "#/components/schemas/RouteStopInput"
    }
   }
  }
 },
 "Departure": {
  "x-ticvai-persistence": "transport.departure",
  "type": "object",
  "required": [
   "id",
   "routeId",
   "timetableId",
   "performanceId",
   "serviceDate",
   "departsAt",
   "status",
   "seatCapacity"
  ],
  "properties": {
   "id": {
    "$ref": "#/components/schemas/Ulid"
   },
   "routeId": {
    "$ref": "#/components/schemas/Ulid"
   },
   "timetableId": {
    "$ref": "#/components/schemas/Ulid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "description": "The catalogue performance this departure is sold as. Cart lines carry it."
   },
   "serviceDate": {
    "type": "string",
    "format": "date"
   },
   "departsAt": {
    "type": "string",
    "format": "date-time",
    "description": "At the route's first stop."
   },
   "status": {
    "$ref": "#/components/schemas/TransportDepartureStatus"
   },
   "seatCapacity": {
    "type": "integer",
    "minimum": 1
   },
   "seatsSold": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "From catalogue availability on read; not stored here."
   },
   "vehicleResourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "FareModel": {
  "type": "string",
  "description": "`stopCount`: base plus an amount per stop travelled — the prototype's rule. `matrix`: a fare for each pair of stops, for a network whose fares are zonal or negotiated. Which one a route uses is the venue's choice in `setTransportFareTable` (rev 3 REV3-21).\n",
  "enum": [
   "stopCount",
   "matrix"
  ]
 },
 "FareQuote": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "routeId",
   "stopsTravelled",
   "adultFare",
   "total"
  ],
  "properties": {
   "routeId": {
    "$ref": "#/components/schemas/Ulid"
   },
   "stopsTravelled": {
    "type": "integer",
    "minimum": 1
   },
   "adultFare": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "code",
      "count",
      "unitPrice",
      "lineTotal"
     ],
     "properties": {
      "code": {
       "type": "string"
      },
      "catalogueVariantId": {
       "type": "string",
       "format": "uuid"
      },
      "count": {
       "type": "integer"
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "lineTotal": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "passTypeId": {
    "$ref": "#/components/schemas/Ulid"
   },
   "saving": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "With `passTypeId`, single adult fare × `referenceTrips` minus the pass price."
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FareQuoteRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "fromStationId",
   "toStationId"
  ],
  "properties": {
   "routeId": {
    "$ref": "#/components/schemas/Ulid",
    "description": "Omitted, the active route serving the two stations in this order."
   },
   "fromStationId": {
    "$ref": "#/components/schemas/Ulid"
   },
   "toStationId": {
    "$ref": "#/components/schemas/Ulid"
   },
   "passengers": {
    "type": "array",
    "maxItems": 10,
    "description": "Omitted, one of the default type. Ignored with `passTypeId`.",
    "items": {
     "type": "object",
     "required": [
      "code",
      "count"
     ],
     "properties": {
      "code": {
       "type": "string"
      },
      "count": {
       "type": "integer",
       "minimum": 0,
       "maximum": 99
      }
     }
    }
   },
   "passTypeId": {
    "$ref": "#/components/schemas/Ulid"
   },
   "at": {
    "type": "string",
    "format": "date-time",
    "description": "The sale instant the fare table is read at. Default now."
   }
  }
 },
 "FareTable": {
  "x-ticvai-persistence": "transport.fare_table + transport.fare_passenger_type + transport.fare_matrix_cell",
  "allOf": [
   {
    "$ref": "#/components/schemas/SetFareTableRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "routeId"
    ],
    "properties": {
     "id": {
      "$ref": "#/components/schemas/Ulid"
     },
     "routeId": {
      "$ref": "#/components/schemas/Ulid"
     }
    }
   }
  ]
 },
 "ImportTransportNetworkRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "format",
   "sourceRef"
  ],
  "properties": {
   "format": {
    "type": "string",
    "enum": [
     "csvBundle",
     "gtfs"
    ],
    "description": "A zip of the four CSV files described on `importTransportNetwork`, or a GTFS static feed."
   },
   "sourceRef": {
    "type": "string",
    "format": "uuid",
    "description": "The uploaded file, as the `MediaAsset.id` from `assets.completeUpload`. Never a URL.",
    "x-ticvai-references": "assets.MediaAsset"
   },
   "include": {
    "type": "array",
    "uniqueItems": true,
    "description": "Which parts of the file to read. Absent reads all three.",
    "items": {
     "type": "string",
     "enum": [
      "stations",
      "routes",
      "timetables"
     ]
    }
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
 "MediaAsset": {
  "x-ticvai-persistence": "assets.media_asset",
  "type": "object",
  "required": [
   "id",
   "kind",
   "status",
   "filename",
   "contentType",
   "sizeBytes",
   "referenceCount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "status": {
    "$ref": "#/components/schemas/MediaStatus"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Required before use in a guest-facing surface. WCAG 2.2 AA."
   },
   "width": {
    "type": "integer",
    "nullable": true
   },
   "height": {
    "type": "integer",
    "nullable": true
   },
   "durationSeconds": {
    "type": "number",
    "nullable": true
   },
   "customMetadata": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"
   },
   "sharedWithTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "url": {
    "type": "string",
    "description": "Signed and expiring for private assets; stable CDN URL for public ones."
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "referenceCount": {
    "type": "integer",
    "description": "How many surfaces reference this asset. Non-zero refuses deletion.\n"
   },
   "rights": {
    "$ref": "#/components/schemas/MediaRights"
   },
   "isRightsExpired": {
    "type": "boolean"
   },
   "version": {
    "type": "integer"
   },
   "uploadedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
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
 "MediaRights": {
  "x-ticvai-persistence": "none — embedded in asset",
  "type": "object",
  "description": "Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n",
  "properties": {
   "licenceKind": {
    "type": "string",
    "enum": [
     "owned",
     "royaltyFree",
     "rightsManaged",
     "creativeCommons",
     "editorialOnly",
     "unknown"
    ]
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "licenceReference": {
    "type": "string",
    "nullable": true
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "permittedUses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "web",
      "print",
      "socialMedia",
      "inVenue",
      "advertising",
      "internal"
     ]
    }
   },
   "attributionRequired": {
    "type": "boolean",
    "default": false
   },
   "attributionText": {
    "type": "string",
    "nullable": true
   },
   "permittedTerritories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"
   },
   "permittedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"
   },
   "modelReleaseHeld": {
    "type": "boolean",
    "default": false
   },
   "renewalOwner": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "MediaStatus": {
  "type": "string",
  "enum": [
   "processing",
   "ready",
   "quarantined",
   "failed",
   "archived"
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
 "PassType": {
  "x-ticvai-persistence": "transport.pass_type",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreatePassTypeRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "active"
    ],
    "properties": {
     "id": {
      "$ref": "#/components/schemas/Ulid"
     },
     "active": {
      "type": "boolean",
      "default": true
     },
     "catalogueProductId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "The catalogue `openDated` product this pass is sold as."
     }
    }
   }
  ]
 },
 "PassengerType": {
  "x-ticvai-persistence": "transport.fare_passenger_type",
  "type": "object",
  "required": [
   "code",
   "name",
   "fareMultiplier"
  ],
  "properties": {
   "code": {
    "type": "string",
    "pattern": "^[a-z][a-zA-Z0-9]{0,31}$",
    "description": "`adult`, `child`, `student`, `determination`. Unique in the fare table."
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "$ref": "#/components/schemas/LocalisedText",
    "description": "What the picker shows under the name (\"Age 5–11 · half fare\")."
   },
   "fareMultiplier": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Share of the adult fare, set by the venue. The demo tenant's seed is 1 adult, 0.5 child and student, 0 person of determination (seed data, not a default)."
   },
   "minAge": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "maxAge": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "proofRequired": {
    "$ref": "#/components/schemas/LocalisedText",
    "nullable": true,
    "description": "Checked by the driver at boarding (\"Valid student card\", \"Sanad card\")."
   },
   "isDefault": {
    "type": "boolean",
    "default": false,
    "description": "The type a new search starts with, one of it. Exactly one per table."
   },
   "catalogueVariantId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The variant of the route's trip product this type is sold as."
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
    "description": "**Null on this response.** The refund batch is created by `orders` when it consumes `performance.cancelled` (F09), after this call has returned, and is queued there for approval — refunds are not issued automatically. Read it from orders, not from here.\n"
   },
   "notificationsQueued": {
    "type": "integer"
   }
  }
 },
 "RouteStop": {
  "x-ticvai-persistence": "transport.route_stop",
  "allOf": [
   {
    "$ref": "#/components/schemas/RouteStopInput"
   },
   {
    "type": "object",
    "required": [
     "id",
     "sequence"
    ],
    "properties": {
     "id": {
      "$ref": "#/components/schemas/Ulid"
     },
     "sequence": {
      "type": "integer",
      "minimum": 1,
      "description": "1 for the origin."
     },
     "station": {
      "$ref": "#/components/schemas/Station"
     }
    }
   }
  ]
 },
 "RouteStopInput": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "stationId",
   "offsetMinutes"
  ],
  "properties": {
   "stationId": {
    "$ref": "#/components/schemas/Ulid"
   },
   "offsetMinutes": {
    "type": "integer",
    "minimum": 0,
    "maximum": 1440,
    "description": "Minutes after the departure from the first stop that the coach leaves this one. 0 on the first stop; strictly increasing along the route.\n"
   },
   "boardingAllowed": {
    "type": "boolean",
    "default": true
   },
   "alightingAllowed": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "SetFareTableRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "model",
   "passengerTypes",
   "effectiveFrom"
  ],
  "properties": {
   "model": {
    "$ref": "#/components/schemas/FareModel"
   },
   "baseFare": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "`stopCount` only. Set by the venue; AED 5 in the demo tenant's seed data, not a default (rev 3 REV3-21)."
   },
   "perStopFare": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "`stopCount` only. Set by the venue; AED 2.50 in the demo tenant's seed data, not a default (rev 3 REV3-21)."
   },
   "matrix": {
    "type": "array",
    "description": "`matrix` only. One adult fare per ordered pair of stops the route serves; the reverse pair is its own row.",
    "items": {
     "type": "object",
     "required": [
      "fromStationId",
      "toStationId",
      "fare"
     ],
     "properties": {
      "fromStationId": {
       "$ref": "#/components/schemas/Ulid"
      },
      "toStationId": {
       "$ref": "#/components/schemas/Ulid"
      },
      "fare": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "passengerTypes": {
    "type": "array",
    "minItems": 1,
    "maxItems": 10,
    "items": {
     "$ref": "#/components/schemas/PassengerType"
    }
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Station": {
  "x-ticvai-persistence": "transport.station",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateStationRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "active"
    ],
    "properties": {
     "id": {
      "$ref": "#/components/schemas/Ulid"
     },
     "active": {
      "type": "boolean",
      "default": true
     }
    }
   }
  ]
 },
 "Timetable": {
  "x-ticvai-persistence": "transport.timetable + transport.timetable_run",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateTimetableRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "routeId",
     "status"
    ],
    "properties": {
     "id": {
      "$ref": "#/components/schemas/Ulid"
     },
     "routeId": {
      "$ref": "#/components/schemas/Ulid"
     },
     "status": {
      "$ref": "#/components/schemas/TransportTimetableStatus"
     },
     "publishedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true
     },
     "releasedThrough": {
      "type": "string",
      "format": "date",
      "nullable": true,
      "readOnly": true,
      "description": "The last date whose departures have been generated."
     },
     "supersededById": {
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
      "nullable": true,
      "readOnly": true
     }
    }
   }
  ]
 },
 "TimetableRun": {
  "x-ticvai-persistence": "transport.timetable_run",
  "type": "object",
  "required": [
   "departsAt",
   "days"
  ],
  "properties": {
   "departsAt": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "Venue local time, 24-hour `HH:MM`, at the route's first stop."
   },
   "days": {
    "type": "array",
    "minItems": 1,
    "uniqueItems": true,
    "items": {
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
    }
   }
  }
 },
 "TransportDepartureStatus": {
  "type": "string",
  "description": "Mirrors the catalogue performance behind the departure, in the words a coach operator uses. `soldOut` is computed from availability, never set.\n",
  "enum": [
   "scheduled",
   "onSale",
   "soldOut",
   "departed",
   "cancelled"
  ]
 },
 "TransportNetworkImport": {
  "x-ticvai-persistence": "transport.network_import",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "format",
   "sourceRef",
   "status"
  ],
  "properties": {
   "id": {
    "$ref": "#/components/schemas/Ulid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "format": {
    "type": "string",
    "enum": [
     "csvBundle",
     "gtfs"
    ]
   },
   "sourceRef": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "assets.MediaAsset"
   },
   "status": {
    "$ref": "#/components/schemas/TransportNetworkImportStatus"
   },
   "preview": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "What applying would write. Null until `previewReady`.",
    "properties": {
     "stationsToCreate": {
      "type": "integer",
      "minimum": 0
     },
     "stationsToUpdate": {
      "type": "integer",
      "minimum": 0
     },
     "routesToCreate": {
      "type": "integer",
      "minimum": 0
     },
     "routesToUpdate": {
      "type": "integer",
      "minimum": 0
     },
     "stopsToWrite": {
      "type": "integer",
      "minimum": 0
     },
     "timetablesToCreate": {
      "type": "integer",
      "minimum": 0
     }
    }
   },
   "findings": {
    "type": "array",
    "readOnly": true,
    "maxItems": 1000,
    "items": {
     "$ref": "#/components/schemas/TransportNetworkImportFinding"
    }
   },
   "createdBy": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "appliedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "appliedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "TransportNetworkImportFinding": {
  "x-ticvai-persistence": "none — stored as jsonb on transport.network_import.findings",
  "type": "object",
  "required": [
   "code",
   "severity",
   "message"
  ],
  "properties": {
   "code": {
    "type": "string",
    "enum": [
     "nothingFound",
     "fileMissing",
     "headerMismatch",
     "stationCodeDuplicate",
     "stationCoordinatesMissing",
     "routeCodeDuplicate",
     "routeStopUnknownStation",
     "routeOffsetsNotIncreasing",
     "routePairUnknown",
     "routeActiveStopsChanged",
     "timetableRouteUnknown",
     "timetableTimeInvalid",
     "timetableDatesInvalid",
     "gtfsCalendarUnsupported"
    ],
    "description": "`stationCoordinatesMissing` is a warning (the station is listed and left off the map); `routeActiveStopsChanged` is a warning (those stops are skipped); every other code is an error and blocks the apply.\n"
   },
   "severity": {
    "type": "string",
    "enum": [
     "error",
     "warning"
    ]
   },
   "file": {
    "type": "string",
    "nullable": true,
    "description": "e.g. `route_stops.csv` or `stop_times.txt`."
   },
   "row": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "reference": {
    "type": "string",
    "nullable": true,
    "description": "The station",
    "route or timetable code concerned.": null
   },
   "message": {
    "type": "string",
    "maxLength": 500
   }
  }
 },
 "TransportNetworkImportStatus": {
  "type": "string",
  "description": "`validating` → `previewReady` or `failed`; `previewReady` → `applied`, or `expired` after 7 days unapplied (proposed, client to correct). States in `states/transport-network-import.yaml` (rev 3 REV3-21).\n",
  "enum": [
   "validating",
   "previewReady",
   "failed",
   "applied",
   "expired"
  ]
 },
 "TransportRoute": {
  "x-ticvai-persistence": "transport.route + transport.route_stop",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateTransportRouteRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status"
    ],
    "properties": {
     "id": {
      "$ref": "#/components/schemas/Ulid"
     },
     "status": {
      "$ref": "#/components/schemas/TransportRouteStatus"
     },
     "stops": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/RouteStop"
      }
     },
     "totalMinutes": {
      "type": "integer",
      "readOnly": true,
      "description": "The last stop's offset."
     },
     "catalogueEventId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "The catalogue event its departures are performances of. Created with the route."
     },
     "catalogueProductId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "The one-way trip product (kind `timedAdmission`); one variant per passenger type. Created with the route.\n"
     }
    }
   }
  ]
 },
 "TransportRouteStatus": {
  "type": "string",
  "enum": [
   "draft",
   "active",
   "suspended",
   "retired"
  ]
 },
 "TransportTimetableStatus": {
  "type": "string",
  "enum": [
   "draft",
   "published",
   "superseded",
   "withdrawn"
  ]
 },
 "Ulid": {
  "type": "string",
  "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
 },
 "UploadTicket": {
  "x-ticvai-persistence": "assets.media_upload",
  "type": "object",
  "required": [
   "uploadId",
   "uploadUrl",
   "method",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "uploadId": {
    "type": "string",
    "format": "uuid"
   },
   "uploadUrl": {
    "type": "string",
    "description": "Signed. PUT the file here, then confirm with `/complete`."
   },
   "method": {
    "type": "string",
    "enum": [
     "PUT",
     "POST"
    ]
   },
   "headers": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "maxSizeBytes": {
    "type": "integer"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"
   }
  }
 }
}
```
