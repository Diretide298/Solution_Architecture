# P01-transport-01 — P01 · Transport

**1 screens · 13 operations · 24 schemas · 0 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-049` | Transport — Route & Schedule | listDetail | 13 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-049",
  "name": "Transport — Route & Schedule",
  "module": "Transport",
  "requiresModule": "transport",
  "wave": 3,
  "implementation": {
   "app": "guest-web",
   "route": "/transport/route-and-schedule",
   "component": "apps/guest-web/src/routes/transport/RouteAndScheduleSplit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-007",
    "WEB-010",
    "WEB-016"
   ],
   "transitions": [
    {
     "to": "WEB-007",
     "trigger": "Choose seats on this departure",
     "carries": [
      "performanceId"
     ],
     "precondition": "the departure has a seat map",
     "provenance": "decided 29 September, rev 3 REV3-21: seat selection reuses the seat map on the departure's performanceId (step 2 of 3)"
    },
    {
     "to": "WEB-010",
     "trigger": "Continue to payment",
     "operation": "addCartLine",
     "carries": [
      "cartId"
     ],
     "provenance": "decided 29 September, rev 3 REV3-21 (step 3 of 3)"
    },
    {
     "to": "WEB-016",
     "trigger": "Sign in to save or see favourite routes",
     "returnsTo": "WEB-049",
     "provenance": "decided 29 September, rev 3 REV3-21",
     "carries": [
      "subjectId"
     ]
    },
    {
     "to": "WEB-001",
     "trigger": "Home",
     "back": true,
     "provenance": "decided 29 September, rev 3 REV3-21"
    }
   ]
  },
  "notes": "**New 29 September** (decided 29 September, rev 3 REV3-21: transport ticketing is in scope — stations, routes, timetabled departures, one-way trips, multi-trip passes, favourite routes and a route map). **One-way:** From and To stations with a swap, the travel date (timetables are released 30 days ahead), the passengers (adult; child and student half fare; a person of determination travels free — proof is checked by the driver at boarding), a time period with its departure count, then departure cards (departs, arrives, duration, seats left, fare). **Next Available Trip** jumps to the first departure with room. A chosen departure shows a price card and the stop list with *Show full route* and a street map. **The street map needs the internet** and a third-party tile provider approved under audit R038; the stop list and schematic line need neither. Buying a trip is `addCartLine` with `attributes.transport` (route, stations, passenger type); the price comes from `quoteTransportFare`, and a departure with a seat map goes through seat selection on its `performanceId`. **Multi-trip:** 5- and 10-trip cards and weekly or monthly unlimited passes for the station pair, with the saving. **Favourites:** saved routes, *Book this route* prefills one-way; remove. *Change your trip free up to two hours before departure* is the proposed default of the venue's modification policy, client to correct. **The real network (stations, fares, timetable) is an open value from the client**; the prototype's Emirates Link data is illustrative.\n**30 September (client feedback, CLIENT-RESPONSE-30SEP 5 and 6).** **A route opens with its stations filled in:** entered from a route (a transport product or a route card), From and To are that route's first and last stops (for example E201: Abu Dhabi Central Bus Station to Al Ain Central Bus Station); the guest can still change or swap them. **Departures show straight away** for those stations and the date (`searchTransportDepartures` on load and on every change), with no need to press *Search Trips*; the time-period buttons filter the departures listed, and pressing the chosen period again shows them all. **Passengers appear only after a departure is chosen** (the departure first, then the tickets). The client build also has a *Popular routes* card view (route cards with a from-fare and *Book*, then the date, the departures and the passengers; on the app the first transport product); a route list with a from-fare is not in the contract yet (a question of 1 October), so it is not specified here.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`searchTransportDepartures` reads the population of departures and one is chosen for a price card and a route — list, select, act; the prototype draws one-way, multi-trip and favourites as tabs of one view",
  "purpose": "Find a departure between two stations and buy a trip, a multi-trip or unlimited pass, or rebook a saved route.",
  "openQuestions": [
   "The real network — stations, routes, fares and timetable — is an open value from the client (decided 29 September, rev 3 REV3-21); the prototype's Emirates Link stations and prices are illustrative.",
   "The street-map tile provider needs approval under audit R038; the approver is still to be named by the client."
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Trip type",
       "notes": "One-way trip, Multi-trip, Favourites (tabs).",
       "provenance": "decided 29 September, rev 3 REV3-21; prototype tabs"
      },
      {
       "kind": "selectField",
       "label": "From",
       "bindsTo": "Station",
       "operation": "listTransportStations",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "selectField",
       "label": "To",
       "bindsTo": "Station",
       "operation": "listTransportStations",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "iconButton",
       "label": "Swap stations",
       "notes": "Swaps From and To and picks the paired route the other way.",
       "operation": "listTransportRoutes",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "datePicker",
       "label": "Travel date",
       "notes": "Timetables are released 30 days ahead.",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "numberField",
       "label": "Passengers",
       "bindsTo": "PassengerType",
       "notes": "Adult, child 5-11 and student at half fare, person of determination free (one companion at the adult fare); proof is checked at boarding.",
       "operation": "getTransportFareTable",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "selectField",
       "label": "Time period",
       "notes": "Morning, Afternoon, Evening, Night, each with its count of departures.",
       "operation": "searchTransportDepartures",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "cardList",
       "label": "Departures",
       "bindsTo": "DepartureOffer",
       "columns": [
        "DepartureOffer.routeCode",
        "DepartureOffer.departsAt",
        "DepartureOffer.arrivesAt",
        "DepartureOffer.durationMinutes",
        "DepartureOffer.seatsLeft",
        "DepartureOffer.fare"
       ],
       "operation": "searchTransportDepartures",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "cardList",
       "label": "Multi-trip cards",
       "bindsTo": "PassOffer",
       "columns": [
        "PassOffer.name",
        "PassOffer.trips",
        "PassOffer.validityDays",
        "PassOffer.price",
        "PassOffer.saving"
       ],
       "notes": "The Multi-trip tab.",
       "operation": "listTransportPassOffers",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "cardList",
       "label": "Favourite routes",
       "bindsTo": "FavouriteRoute",
       "columns": [
        "FavouriteRoute.fromStationName",
        "FavouriteRoute.toStationName",
        "FavouriteRoute.adultFare"
       ],
       "notes": "The Favourites tab; *Book this route* prefills the one-way tab. Signed-in guests only.",
       "operation": "listMyFavouriteRoutes",
       "provenance": "decided 29 September, rev 3 REV3-21"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Price card",
       "bindsTo": "FareQuote",
       "notes": "Line code and direction (e.g. E101-Out), departs, arrives, seats available, fare per passenger type and total.",
       "operation": "quoteTransportFare",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "timeline",
       "label": "Stops",
       "bindsTo": "RouteMap.stops",
       "notes": "From and To with the stops between folded: *Show full route (n stops)*.",
       "operation": "getTransportRouteMap",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "detailPanel",
       "label": "Street map",
       "bindsTo": "RouteMap",
       "notes": "Needs the internet and a third-party tile provider approved under audit R038; hidden offline, where the stop list and schematic line remain.",
       "operation": "getTransportRouteMap",
       "provenance": "decided 29 September, rev 3 REV3-21"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Search Trips",
       "operation": "searchTransportDepartures",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "secondaryButton",
       "label": "Next Available Trip",
       "operation": "getNextTransportDeparture",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "primaryButton",
       "label": "Add to basket",
       "notes": "A trip: the passenger type's `variantId`, the departure's `performanceId` and `attributes.transport`. A pass: the pass product's `variantId`, no performance.",
       "operation": "addCartLine",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "secondaryButton",
       "label": "Save route",
       "operation": "saveFavouriteRoute",
       "provenance": "decided 29 September, rev 3 REV3-21"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove favourite",
       "operation": "deleteFavouriteRoute",
       "provenance": "decided 29 September, rev 3 REV3-21"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stations, routes and passenger types.",
   "error": "Could not load. Names which read failed; nothing is bought.",
   "emptyFirstRun": "**No routes are published for this venue yet.** Says so; the client still owes the real network (stations, fares, timetable).",
   "emptyNoResults": "No departure in that period. Names the period and offers **Next Available Trip** or another period or date.",
   "emptyNoAccess": "Searching and buying need no account. **Favourites need a signed-in guest**: a guest who is not signed in is offered sign-in and brought back, never shown an empty list.",
   "offline": "**The offline banner shows.** A route's stop list and schematic line already loaded stay readable with their age; the street map needs the connection. Searching departures, buying a trip or a pass and saving a favourite route need the connection."
  },
  "apis": [
   {
    "operationId": "listTransportStations",
    "contract": "transport",
    "purpose": "The stations to pick From and To",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTransportRoutes",
    "contract": "transport",
    "purpose": "The routes between two stations (the swap uses the paired route)",
    "trigger": "onAction"
   },
   {
    "operationId": "getTransportFareTable",
    "contract": "transport",
    "purpose": "Passenger types and fares of the route",
    "trigger": "onLoad"
   },
   {
    "operationId": "searchTransportDepartures",
    "contract": "transport",
    "purpose": "Departures for the stations, date, period and party, with counts per period",
    "trigger": "onLoad"
   },
   {
    "operationId": "getNextTransportDeparture",
    "contract": "transport",
    "purpose": "The next departure with room for the party",
    "trigger": "onAction"
   },
   {
    "operationId": "getTransportRoute",
    "contract": "transport",
    "purpose": "The route and its stops",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTransportRouteMap",
    "contract": "transport",
    "purpose": "Stop list, line and bounds for the map",
    "trigger": "onLoad"
   },
   {
    "operationId": "quoteTransportFare",
    "contract": "transport",
    "purpose": "The price for the stations and passengers",
    "trigger": "onAction"
   },
   {
    "operationId": "listTransportPassOffers",
    "contract": "transport",
    "purpose": "Multi-trip and unlimited passes for the station pair",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMyFavouriteRoutes",
    "contract": "transport",
    "purpose": "The guest's saved routes",
    "trigger": "onLoad"
   },
   {
    "operationId": "saveFavouriteRoute",
    "contract": "transport",
    "purpose": "Save this route",
    "trigger": "onAction",
    "invalidates": [
     "listMyFavouriteRoutes"
    ]
   },
   {
    "operationId": "deleteFavouriteRoute",
    "contract": "transport",
    "purpose": "Remove a saved route",
    "trigger": "onAction",
    "invalidates": [
     "listMyFavouriteRoutes"
    ]
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add the trip or pass to the basket (`attributes.transport`)",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    },
    {
     "name": "favouriteId",
     "from": "navigation",
     "optional": true
    },
    {
     "name": "routeId",
     "from": "navigation",
     "optional": true
    }
   ],
   "coldEntry": "Arrives with nothing; the venue comes from the site. **Opened from a route** (a route card or a transport product, client feedback 30 September), `routeId` fills From and To with that route's first and last stops, and the departures show at once; the guest can still change or swap them. A saved route (`favouriteId`) prefills the same way. A shared link with stations prefills From and To if both still exist, and says which one does not."
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-049",
   "prototype": {
    "file": "sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3 (30 September build)",
    "verified": "2026-10-01",
    "match": "exact",
    "view": "Engine controls → Transport → Route & schedule · one-way, multi-trip, favourites → Book → Fri (stations filled in, departures without a search)",
    "differences": "30 September: the route opens with its stations filled in and the departures listed without a search; the time-period buttons filter them. The engine's other transport flow, Popular routes (card view), is route cards with a from-fare and Book, then the date, the departures and the passengers. The route map needs a street-map tile provider (audit R038)."
   }
  },
  "apisNote": "Authored 29 September 2026 from the rev 3 decisions and the client prototype view named in `wireframe.prototype`; every operation exists in the contracts (decided 29 September, rev 3).",
  "overlays": [
   {
    "id": "confirmDeleteFavouriteRoute",
    "component": "confirmDialog",
    "trigger": "Remove favourite",
    "body": "**Remove this saved route?** It leaves Favourites; nothing already booked on it changes.",
    "confirm": {
     "label": "Remove",
     "operation": "deleteFavouriteRoute"
    },
    "dismiss": {
     "label": "Keep it",
     "discards": []
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AddCartLineRequest",
  "responds": "Cart"
 },
 "deleteFavouriteRoute": {
  "method": "DELETE",
  "path": "/transport/favourite-routes/{favouriteId}",
  "contract": "transport",
  "summary": "Remove a saved route",
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
 "getNextTransportDeparture": {
  "method": "GET",
  "path": "/transport/departures/next",
  "contract": "transport",
  "summary": "Next Available Trip",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "fromStationId",
    "in": "query",
    "required": true
   },
   {
    "name": "toStationId",
    "in": "query",
    "required": true
   },
   {
    "name": "after",
    "in": "query",
    "required": null
   },
   {
    "name": "passengers",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DepartureOffer"
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
 "getTransportRouteMap": {
  "method": "GET",
  "path": "/transport/routes/{routeId}/map",
  "contract": "transport",
  "summary": "The route drawn for a map, with the journey highlighted",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "fromStationId",
    "in": "query",
    "required": null
   },
   {
    "name": "toStationId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RouteMap"
 },
 "listMyFavouriteRoutes": {
  "method": "GET",
  "path": "/transport/favourite-routes",
  "contract": "transport",
  "summary": "The caller's saved routes",
  "permission": null,
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
 "listTransportPassOffers": {
  "method": "GET",
  "path": "/transport/pass-offers",
  "contract": "transport",
  "summary": "Multi-trip passes for a pair of stations, priced, with the saving",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "fromStationId",
    "in": "query",
    "required": true
   },
   {
    "name": "toStationId",
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
 "saveFavouriteRoute": {
  "method": "POST",
  "path": "/transport/favourite-routes",
  "contract": "transport",
  "summary": "Save route",
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
  "responds": "FavouriteRoute"
 },
 "searchTransportDepartures": {
  "method": "GET",
  "path": "/transport/departures",
  "contract": "transport",
  "summary": "Search Trips — departures between two stations on a date",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "fromStationId",
    "in": "query",
    "required": true
   },
   {
    "name": "toStationId",
    "in": "query",
    "required": true
   },
   {
    "name": "date",
    "in": "query",
    "required": true
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "passengers",
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
     "format": "uuid"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
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
     "format": "uuid"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
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
    "format": "uuid",
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
 "DepartureOffer": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "departureId",
   "performanceId",
   "routeId",
   "departsAt",
   "arrivesAt",
   "durationMinutes",
   "seatsLeft",
   "fare",
   "period"
  ],
  "properties": {
   "departureId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "routeId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "routeCode": {
    "type": "string",
    "description": "The price card's label, e.g. `E101-Out`."
   },
   "departsAt": {
    "type": "string",
    "format": "date-time",
    "description": "At the boarding stop."
   },
   "arrivesAt": {
    "type": "string",
    "format": "date-time",
    "description": "At the alighting stop."
   },
   "durationMinutes": {
    "type": "integer",
    "minimum": 0
   },
   "period": {
    "$ref": "#/components/schemas/TimePeriod"
   },
   "seatsLeft": {
    "type": "integer",
    "minimum": 0,
    "description": "Catalogue availability for the performance. Display only; the hold decides the sale."
   },
   "fitsParty": {
    "type": "boolean"
   },
   "fare": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "One adult, one way."
   },
   "partyTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
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
    "$ref": "../shared/common.yaml#/components/schemas/Id"
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
    "$ref": "../shared/common.yaml#/components/schemas/Id"
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
    "$ref": "../shared/common.yaml#/components/schemas/Id",
    "description": "Omitted, the active route serving the two stations in this order."
   },
   "fromStationId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "toStationId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
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
    "$ref": "../shared/common.yaml#/components/schemas/Id"
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
      "$ref": "../shared/common.yaml#/components/schemas/Id"
     },
     "routeId": {
      "$ref": "../shared/common.yaml#/components/schemas/Id"
     }
    }
   }
  ]
 },
 "FavouriteRoute": {
  "x-ticvai-persistence": "transport.favourite_route",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "fromStationId",
   "toStationId",
   "createdAt"
  ],
  "description": "Unique per guest, venue and ordered pair of stations.",
  "properties": {
   "id": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "fromStationId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "toStationId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "fromStationName": {
    "type": "string",
    "readOnly": true
   },
   "toStationName": {
    "type": "string",
    "readOnly": true
   },
   "label": {
    "type": "string",
    "nullable": true
   },
   "adultFare": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The current fare, read on list."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
   }
  }
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
 "PassOffer": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "passTypeId",
   "catalogueProductId",
   "name",
   "price",
   "validityDays"
  ],
  "properties": {
   "passTypeId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "catalogueProductId": {
    "type": "string",
    "format": "uuid"
   },
   "routeId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string"
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
    "nullable": true
   },
   "validityDays": {
    "type": "integer"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "saving": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "RouteMap": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "routeId",
   "stops"
  ],
  "properties": {
   "routeId": {
    "$ref": "../shared/common.yaml#/components/schemas/Id"
   },
   "lineCode": {
    "type": "string"
   },
   "colour": {
    "type": "string"
   },
   "stops": {
    "type": "array",
    "description": "Every stop in route order.",
    "items": {
     "type": "object",
     "required": [
      "stationId",
      "sequence",
      "name",
      "onJourney"
     ],
     "properties": {
      "stationId": {
       "$ref": "../shared/common.yaml#/components/schemas/Id"
      },
      "sequence": {
       "type": "integer"
      },
      "name": {
       "type": "string",
       "description": "Localised to the caller."
      },
      "shortName": {
       "type": "string"
      },
      "latitude": {
       "type": "number",
       "nullable": true
      },
      "longitude": {
       "type": "number",
       "nullable": true
      },
      "offsetMinutes": {
       "type": "integer"
      },
      "onJourney": {
       "type": "boolean",
       "description": "Between the boarding and alighting stops",
       "inclusive.": null
      },
      "isBoarding": {
       "type": "boolean"
      },
      "isAlighting": {
       "type": "boolean"
      }
     }
    }
   },
   "intermediateStopCount": {
    "type": "integer",
    "description": "Stops between boarding and alighting — the number behind \"Show full route (n stops)\"."
   },
   "bounds": {
    "type": "object",
    "nullable": true,
    "description": "The box around the stops with coordinates, for the map's initial view.",
    "properties": {
     "south": {
      "type": "number"
     },
     "west": {
      "type": "number"
     },
     "north": {
      "type": "number"
     },
     "east": {
      "type": "number"
     }
    }
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
      "$ref": "../shared/common.yaml#/components/schemas/Id"
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
       "$ref": "../shared/common.yaml#/components/schemas/Id"
      },
      "toStationId": {
       "$ref": "../shared/common.yaml#/components/schemas/Id"
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
      "$ref": "../shared/common.yaml#/components/schemas/Id"
     },
     "active": {
      "type": "boolean",
      "default": true
     }
    }
   }
  ]
 },
 "TimePeriod": {
  "type": "string",
  "description": "Proposed, client to correct (rev 3 REV3-21): `morning` 05:00–11:59, `afternoon` 12:00–16:59, `evening` 17:00–20:59, `night` 21:00–04:59.\n",
  "enum": [
   "morning",
   "afternoon",
   "evening",
   "night"
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
      "$ref": "../shared/common.yaml#/components/schemas/Id"
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
 }
}
```
