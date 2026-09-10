# P01-in-venue-services-01 — P01 · In-venue Services

**6 screens · 23 operations · 37 schemas · 5 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## What to build

**A working surface, not a drawing of one.** The reference is `sources/designs/TICVAI_POS_Terminal_client_approved.html` — a Claude Design
build from these same sources, and the one the client responded to. Open it and match its depth:
real state, seeded data, controls that do something. Do not describe it, read it.

## What is in this folder

| file | what it is |
|---|---|
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ACCESS_POINT_CONFIGURE, ORDER_MODIFY, PRODUCT_VIEW, QUEUE_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **6 of these operations work offline**: getVenueMap, getVenueMapGraph, getWaitTimes, joinRestaurantWaitlist, listParkingFacilities, listQueues
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-036` | F&B – Browse & Order | listDetail | 10 | 0 | — |
| `WEB-037` | Menu Item Detail | listDetail | 2 | 0 | — |
| `WEB-038` | F&B – Order Tracking | statusTracker | 3 | 0 | — |
| `WEB-039` | Venue Map & Wait Times | listDetail | 4 | 0 | — |
| `WEB-040` | Virtual Queue | statusTracker | 6 | 0 | — |
| `WEB-041` | Parking – Reserve & Pay | listDetail | 3 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-036",
  "name": "F&B – Browse & Order",
  "module": "In-venue Services",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/fandb--browse-and-order",
   "component": "apps/guest-web/src/routes/FBBrowseOrder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "**A guest scans a QR on a table and lands in a browser.** That is the single most common F&B ordering pattern anywhere, and until 24 August it was the one thing this surface could not do — `claimTableSession` and `claimLocationSession` were app-only. **Nobody installs an app to order a coffee.** **Renamed 31 August** from *F&B — Browse & Order*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added getGuestOrderStatus. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads the population and `getGuestMenu` reads one of them — list, select, act",
  "purpose": "Order food from a table, a lounger or a seat.",
  "gaps": [
   {
    "operation": "listModifierGroups",
    "why": "**3 declared operations reach no component on this screen**: listModifierGroups, listDeliveryLocations, getGuestOrderStatus. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Claim",
       "operation": "claimTableSession",
       "provenance": "contract fnb.yaml POST /table-sessions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createGuestFnbOrder",
       "provenance": "contract fnb.yaml POST /guest-orders"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "label": "F&B — Browse & Order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Detail",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content resolves in place.",
   "error": "Could not load. **The rest of the site is unaffected.**",
   "emptyFirstRun": "**Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel.",
   "emptyNoResults": "Nothing matches.",
   "emptyNoAccess": "**Sign in to see this.** A guest who is not signed in is offered the door, not refused."
  },
  "apis": [
   {
    "operationId": "getGuestMenu",
    "contract": "fnb",
    "purpose": "The menu a guest sees",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDiningOutlets",
    "contract": "fnb",
    "purpose": "Where a guest can eat, right now",
    "trigger": "onLoad"
   },
   {
    "operationId": "listModifierGroups",
    "contract": "fnb",
    "purpose": "List modifier groups",
    "trigger": "onLoad"
   },
   {
    "operationId": "claimLocationSession",
    "contract": "fnb",
    "purpose": "Tell the platform where the guest is",
    "trigger": "onAction",
    "invalidates": [
     "listDiningOutlets"
    ]
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
    "operationId": "createGuestFnbOrder",
    "contract": "fnb",
    "purpose": "A guest orders food",
    "trigger": "onAction",
    "invalidates": [
     "listDiningOutlets"
    ]
   },
   {
    "operationId": "listDeliveryLocations",
    "contract": "fnb",
    "purpose": "Where an order can be delivered",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestOrderStatus",
    "contract": "fnb",
    "purpose": "Track an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTableReservation",
    "contract": "fnb",
    "purpose": "Reserve a table",
    "trigger": "onAction"
   },
   {
    "operationId": "joinRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Join the waitlist when nothing is free",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "outletId",
     "from": "deepLink"
    },
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a forwarded confirmation all land here, and the person holding it did nothing wrong. Arrives with `outletId`.",
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
   "board": "wireframes/P01 Guest Web.dc.html#web-036"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
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
 },
 {
  "id": "WEB-037",
  "name": "Menu Item Detail",
  "module": "In-venue Services",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/menu-item-detail",
   "component": "apps/guest-web/src/routes/MenuItemDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "**Allergens are read here more often than anywhere else in the platform**, and a guest checking one on a phone browser is the ordinary case rather than the exception.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listModifierGroups` reads the population and `getGuestMenu` reads one of them — list, select, act",
  "purpose": "What is in it, and what may be changed.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every menu item",
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
       "label": "The selected menu item",
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
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "label": "Menu Item Detail",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Detail",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content resolves in place.",
   "error": "Could not load. **The rest of the site is unaffected.**",
   "emptyFirstRun": "**Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel.",
   "emptyNoResults": "Nothing matches.",
   "emptyNoAccess": "**Sign in to see this.** A guest who is not signed in is offered the door, not refused."
  },
  "apis": [
   {
    "operationId": "getGuestMenu",
    "contract": "fnb",
    "purpose": "The menu a guest sees",
    "trigger": "onLoad"
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
     "name": "outletId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a forwarded confirmation all land here, and the person holding it did nothing wrong. Arrives with `outletId`.",
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
   "board": "wireframes/P01 Guest Web.dc.html#web-037"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
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
 },
 {
  "id": "WEB-038",
  "name": "F&B – Order Tracking",
  "module": "In-venue Services",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/fandb--order-tracking",
   "component": "apps/guest-web/src/routes/FBOrderTracking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "**Order to ready is the kitchen's number; ready to collected is the counter's.** A guest watching a status that never changes walks to the counter. **Renamed 31 August** from *F&B — Order Tracking*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Watch it being made, and settle the bill.",
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
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "label": "F&B — Order Tracking",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Detail",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content resolves in place.",
   "error": "Could not load. **The rest of the site is unaffected.**",
   "emptyFirstRun": "**Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel.",
   "emptyNoResults": "Nothing matches.",
   "emptyNoAccess": "**Sign in to see this.** A guest who is not signed in is offered the door, not refused."
  },
  "apis": [
   {
    "operationId": "getGuestOrderStatus",
    "contract": "fnb",
    "purpose": "Track an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestBill",
    "contract": "fnb",
    "purpose": "The bill for the guest's table",
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
     "from": "deepLink"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a forwarded confirmation all land here, and the person holding it did nothing wrong. Arrives with `orderId`, `sessionId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-038"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
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
 },
 {
  "id": "WEB-039",
  "name": "Venue Map & Wait Times",
  "module": "In-venue Services",
  "requiresModule": "queue",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/venue-map-and-wait-times",
   "component": "apps/guest-web/src/routes/VenueMapWaitTimes.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "**`getVenueMap` was already `guest` audience and offline-capable and no web screen drew it.** A map in a browser is a map. **Drawn 26 August** — `Seat Board 3.dc.html` frame `seat-3c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 3.dc.html#seat-3c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listQueues` reads the population and `getVenueMap` reads one of them — list, select, act",
  "purpose": "Where things are, and how long they take.",
  "gaps": [
   {
    "operation": "getVenueMapGraph",
    "why": "**2 declared operations reach no component on this screen**: getVenueMapGraph, getWaitTimes. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every venue map wait",
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
       "label": "The selected venue map wait",
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
       "kind": "cardList",
       "label": "Venue Map & Wait Times",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Detail",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content resolves in place.",
   "error": "Could not load. **The rest of the site is unaffected.**",
   "emptyFirstRun": "**Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel.",
   "emptyNoResults": "Nothing matches.",
   "emptyNoAccess": "**Sign in to see this.** A guest who is not signed in is offered the door, not refused."
  },
  "apis": [
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
    "purpose": "List queues",
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
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a forwarded confirmation all land here, and the person holding it did nothing wrong. Arrives with `mapId`.",
   "preloaded": [
    "VenueMapDetail.map",
    "VenueMapDetail.points",
    "VenueMapDetail.paths"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-039",
   "note": "**Drawn by Claude Design on `Seat Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
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
 },
 {
  "id": "WEB-040",
  "name": "Virtual Queue",
  "module": "In-venue Services",
  "requiresModule": "queue",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/virtual-queue",
   "component": "apps/guest-web/src/routes/VirtualQueue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "**The point of a virtual queue is that the guest walks away** — which works the same in a browser tab as in an app.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getWaitingGuest` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Hold a place without standing in one.",
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
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "label": "Virtual Queue",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Detail",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content resolves in place.",
   "error": "Could not load. **The rest of the site is unaffected.**",
   "emptyFirstRun": "**Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel.",
   "emptyNoResults": "Nothing matches.",
   "emptyNoAccess": "**Sign in to see this.** A guest who is not signed in is offered the door, not refused."
  },
  "apis": [
   {
    "operationId": "joinQueue",
    "contract": "queue",
    "purpose": "Join a virtual queue",
    "trigger": "onAction"
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
    "operationId": "joinWaitlist",
    "contract": "catalogue",
    "purpose": "Join a virtual queue",
    "trigger": "onAction"
   },
   {
    "operationId": "leaveWaitlist",
    "contract": "catalogue",
    "purpose": "Leave it",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entryId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a forwarded confirmation all land here, and the person holding it did nothing wrong. Arrives with `entryId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-040"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
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
 },
 {
  "id": "WEB-041",
  "name": "Parking – Reserve & Pay",
  "module": "In-venue Services",
  "requiresModule": "access",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/parking--reserve-and-pay",
   "component": "apps/guest-web/src/routes/ParkingReservePay.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "**A guest reserves parking on the drive, from whatever is open on their phone.** Requiring an install for a car park is requiring an install to arrive. **Renamed 31 August** from *Parking — Reserve & Pay*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listParkingFacilities` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Reserve a facility before arriving.",
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
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "label": "Parking — Reserve & Pay",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Detail",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content resolves in place.",
   "error": "Could not load. **The rest of the site is unaffected.**",
   "emptyFirstRun": "**Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel.",
   "emptyNoResults": "Nothing matches.",
   "emptyNoAccess": "**Sign in to see this.** A guest who is not signed in is offered the door, not refused."
  },
  "apis": [
   {
    "operationId": "listParkingFacilities",
    "contract": "access",
    "purpose": "Car parks at a venue, and how each integrates",
    "trigger": "onLoad"
   },
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
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entitlementId",
     "from": "deepLink"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a forwarded confirmation all land here, and the person holding it did nothing wrong. Arrives with `entitlementId`.",
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
   "board": "wireframes/P01 Guest Web.dc.html#web-041"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
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
