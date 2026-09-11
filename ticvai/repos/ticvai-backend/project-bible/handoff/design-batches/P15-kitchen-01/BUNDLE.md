# P15-kitchen-01 — P15 · Kitchen

**10 screens · 24 operations · 18 schemas · 8 permissions**

Platform P15 Kitchen Display · ships as **venue-pos** ·
staff audience · kiosk ·
offline-capable

## Who this is for

**staff on kiosk.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `INCIDENT_REPORT, INCIDENT_VIEW, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **16 of these operations work offline**: chaseStation, fireCourse, getFnbOrder, getHaccpStatus, holdCourse, list86Events, listKitchenStations, listKitchenTickets
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `KIT-001` | Kitchen Operations Command Center | commandCentre | 3 | 0 | — |
| `KIT-002` | Kitchen Display System (KDS) | listDetail | 7 | 0 | — |
| `KIT-003` | Order Firing & Course Management | configEditor | 5 | 0 | — |
| `KIT-004` | Active Order Management & Fulfilment Journey | listDetail | 2 | 0 | — |
| `KIT-005` | Kitchen Station Workload & Dynamic Routing | listDetail | 2 | 0 | — |
| `KIT-006` | Expeditor & Order Assembly | listDetail | 5 | 0 | — |
| `KIT-007` | Guest Collection, Buzzer & Digital Notification | listDetail | 2 | 0 | — |
| `KIT-008` | Exceptions, Re-Fire & Unavailable Items | listDetail | 5 | 0 | — |
| `KIT-009` | SLA, Priority & Service Rules | configEditor | 2 | 0 | — |
| `KIT-010` | Kitchen Performance, AI & Operational Optimization | statusTracker | 2 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "KIT-001",
  "name": "Kitchen Operations Command Center",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/kitchen-operations-command-center",
   "component": "apps/kitchen-display/src/routes/kitchen/KitchenOperationsCommandCenterBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "KIT-002",
    "KIT-003",
    "KIT-004",
    "KIT-005",
    "KIT-006",
    "KIT-007",
    "KIT-008",
    "KIT-009",
    "KIT-010"
   ],
   "transitions": [
    {
     "to": "KIT-002",
     "trigger": "Kitchen Display System (KDS)",
     "provenance": "flow F83 step 1→2"
    },
    {
     "to": "KIT-003",
     "trigger": "Order Firing & Course Management",
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher"
    },
    {
     "to": "KIT-004",
     "trigger": "Active Order Management & Fulfilment Journey",
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher"
    },
    {
     "to": "KIT-005",
     "trigger": "Kitchen Station Workload & Dynamic Routing",
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher"
    },
    {
     "to": "KIT-006",
     "trigger": "Expeditor & Order Assembly",
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher"
    },
    {
     "to": "KIT-007",
     "trigger": "Guest Collection, Buzzer & Digital Notification",
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher"
    },
    {
     "to": "KIT-008",
     "trigger": "Exceptions, Re-Fire & Unavailable Items",
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher"
    },
    {
     "to": "KIT-009",
     "trigger": "SLA, Priority & Service Rules",
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher"
    },
    {
     "to": "KIT-010",
     "trigger": "Kitchen Performance, AI & Operational Optimization",
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3a` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **`wireframe.status` corrected 25 August.** When these screens were repointed from the client pack to their own board on 24 August, the status stayed `designed` — **which claimed a client had drawn a board this package generated.** `derivedFrom` keeps the pack frame, which is where the design came from; `status` describes the file being pointed at, and those are different facts. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3a`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen Operations Command Center* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3a"
  ],
  "pattern": "commandCentre",
  "patternReason": "3 independent reads and no read of one record — the screen watches a population rather than working one",
  "purpose": "Kitchen Operations Command Center — board 3 of the client F&B design set.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Kitchen tickets",
       "bindsTo": "KitchenTicket",
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "metricTile",
       "label": "Kitchen stations",
       "bindsTo": "KitchenStation",
       "operation": "listKitchenStations",
       "provenance": "contract fnb.yaml GET /kitchen/stations"
      },
      {
       "kind": "metricTile",
       "label": "Fnb orders",
       "bindsTo": "FnbOrder",
       "operation": "listFnbOrders",
       "provenance": "contract fnb.yaml GET /fnb-orders"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every kitchen operations",
       "bindsTo": "KitchenTicket",
       "columns": [
        "KitchenTicket.id",
        "KitchenTicket.orderId",
        "KitchenTicket.orderNumber",
        "KitchenTicket.outletId",
        "KitchenTicket.tableLabel",
        "KitchenTicket.serviceMode",
        "KitchenTicket.coursing",
        "KitchenTicket.buzzerCode",
        "KitchenTicket.status",
        "KitchenTicket.priority",
        "KitchenTicket.prioritisedByPrincipalId",
        "KitchenTicket.prioritiseReason"
       ],
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listKitchenStations",
    "contract": "fnb",
    "purpose": "List preparation stations and their routing",
    "trigger": "onLoad"
   },
   {
    "operationId": "listFnbOrders",
    "contract": "fnb",
    "purpose": "List F&B orders",
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
     "name": "stationId",
     "from": "session"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-001",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3a"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-002",
  "name": "Kitchen Display System (KDS)",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/kitchen-display-system-kds",
   "component": "apps/kitchen-display/src/routes/kitchen/KitchenDisplaySystemKdsBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001",
    "KIT-006"
   ],
   "exitTo": [
    "KIT-001",
    "KIT-003"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-003",
     "trigger": "Order Firing & Course Management",
     "provenance": "flow F83 step 2→3, F88 step 2→3"
    },
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "carries": [
      "stationId",
      "venueId"
     ],
     "provenance": "derived — KIT-001 declares entryState.params stationId, venueId, so an edge into it must carry them"
    },
    {
     "to": "EMP-058",
     "trigger": "Starters cleared",
     "provenance": "flow F29 step 4→5",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "EMP-059",
     "trigger": "The server comps the delayed dish",
     "provenance": "flow F29 step 6→7",
     "operation": "refireItem",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "POS-022",
     "trigger": "The guest is called and takes it",
     "provenance": "flow F108 step 5→6",
     "operation": "setKitchenTicketStatus",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **The screen the platform exists for.** Bumped, not tapped — a bump bar and a touch target sized for somebody wearing gloves. Nothing on it is more than one action deep. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Cross-platform navigation removed 24 August**: EMP-058. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3b` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen Display System (KDS)* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Kitchen Display System (KDS) — board 3 of the client F&B design set.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every kitchen display system",
       "bindsTo": "KitchenTicket",
       "columns": [
        "KitchenTicket.id",
        "KitchenTicket.orderId",
        "KitchenTicket.orderNumber",
        "KitchenTicket.outletId",
        "KitchenTicket.tableLabel",
        "KitchenTicket.serviceMode",
        "KitchenTicket.coursing",
        "KitchenTicket.buzzerCode",
        "KitchenTicket.status",
        "KitchenTicket.priority",
        "KitchenTicket.prioritisedByPrincipalId",
        "KitchenTicket.prioritiseReason"
       ],
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected kitchen display system",
       "bindsTo": "KitchenTicket",
       "columns": [
        "KitchenTicket.id",
        "KitchenTicket.orderId",
        "KitchenTicket.orderNumber",
        "KitchenTicket.outletId",
        "KitchenTicket.tableLabel",
        "KitchenTicket.serviceMode",
        "KitchenTicket.coursing",
        "KitchenTicket.buzzerCode",
        "KitchenTicket.status",
        "KitchenTicket.priority",
        "KitchenTicket.prioritisedByPrincipalId",
        "KitchenTicket.prioritiseReason",
        "KitchenTicket.lines",
        "KitchenTicket.targetReadyAt",
        "KitchenTicket.elapsedSeconds"
       ],
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
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
       "operation": "setKitchenTicketStatus",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Fire",
       "operation": "fireCourse",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/fire"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold",
       "operation": "holdCourse",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Refire",
       "operation": "refireItem",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/refire"
      },
      {
       "kind": "secondaryButton",
       "label": "Recall",
       "operation": "recallKitchenTicket",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/recall"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify",
       "operation": "notifyServer",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/notify-server"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue",
    "trigger": "onLoad"
   },
   {
    "operationId": "setKitchenTicketStatus",
    "contract": "fnb",
    "purpose": "Advance a kitchen ticket",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "fireCourse",
    "contract": "fnb",
    "purpose": "Send a held course to the pass",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "holdCourse",
    "contract": "fnb",
    "purpose": "Stop a course going out",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "refireItem",
    "contract": "fnb",
    "purpose": "Make it again",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "recallKitchenTicket",
    "contract": "fnb",
    "purpose": "Bring back a ticket that was bumped by mistake",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "notifyServer",
    "contract": "fnb",
    "purpose": "The kitchen calls the server to the pass",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
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
     "from": "session"
    },
    {
     "name": "ticketId",
     "from": "KIT-002"
    },
    {
     "name": "visitId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person. The table the ticket belongs to.",
   "preloaded": [
    "KitchenTicket.id",
    "KitchenTicket.orderId",
    "KitchenTicket.orderNumber",
    "KitchenTicket.outletId",
    "KitchenTicket.tableLabel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-002",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3b"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-003",
  "name": "Order Firing & Course Management",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/order-firing-course-management",
   "component": "apps/kitchen-display/src/routes/kitchen/OrderFiringCourseManagementBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001",
    "KIT-002"
   ],
   "exitTo": [
    "KIT-001",
    "KIT-004"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-004",
     "trigger": "Active Order Management & Fulfilment Journey",
     "provenance": "flow F83 step 3→4, F88 step 3→4"
    },
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "carries": [
      "stationId",
      "venueId"
     ],
     "provenance": "derived — KIT-001 declares entryState.params stationId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **Starters before mains is the entire job of a kitchen pass.** `KitchenTicket.coursing` carries `holdAndFire`, `phased` and `timed`; without it a table gets dessert while eating its starter. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3c` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3c`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Order Firing &amp; Course Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3c"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setKitchenTicketStatus`, `prioritiseKitchenTicket`, `fireCourse`) and no read of a population — it is settings, not a list",
  "purpose": "Order Firing & Course Management — board 3 of the client F&B design set.",
  "gaps": [
   {
    "operation": "setKitchenTicketStatus",
    "why": "**`setKitchenTicketStatus` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setKitchenTicketStatus",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Prioritise",
       "operation": "prioritiseKitchenTicket",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "secondaryButton",
       "label": "Fire",
       "operation": "fireCourse",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/fire"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold",
       "operation": "holdCourse",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setCourseRules",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/course-rules"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "setKitchenTicketStatus",
    "contract": "fnb",
    "purpose": "Advance a kitchen ticket",
    "trigger": "onAction"
   },
   {
    "operationId": "prioritiseKitchenTicket",
    "contract": "fnb",
    "purpose": "Move a ticket up the queue",
    "trigger": "onAction"
   },
   {
    "operationId": "fireCourse",
    "contract": "fnb",
    "purpose": "Send a held course to the pass",
    "trigger": "onAction"
   },
   {
    "operationId": "holdCourse",
    "contract": "fnb",
    "purpose": "Stop a course going out",
    "trigger": "onAction"
   },
   {
    "operationId": "setCourseRules",
    "contract": "fnb",
    "purpose": "How this outlet courses by default",
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
     "name": "stationId",
     "from": "session"
    },
    {
     "name": "ticketId",
     "from": "KIT-002"
    },
    {
     "name": "outletId",
     "from": "session"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person. Resolves from the station assignment. A kitchen display belongs to one outlet."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-003",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3c"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-004",
  "name": "Active Order Management & Fulfilment Journey",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/active-order-management-fulfilment-journey",
   "component": "apps/kitchen-display/src/routes/kitchen/ActiveOrderManagementFulfilmentJouBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001",
    "KIT-003"
   ],
   "exitTo": [
    "KIT-001",
    "KIT-008"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "provenance": "flow F88 step 4→5"
    },
    {
     "to": "KIT-008",
     "trigger": "Exceptions, Re-Fire & Unavailable Items",
     "provenance": "flow F83 step 4→5"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3d` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listKitchenTickets` reads the population and `getFnbOrder` reads one of them — list, select, act",
  "purpose": "Active Order Management & Fulfilment Journey — board 3 of the client F&B design set.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every active order fulfilment",
       "bindsTo": "KitchenTicket",
       "columns": [
        "KitchenTicket.id",
        "KitchenTicket.orderId",
        "KitchenTicket.orderNumber",
        "KitchenTicket.outletId",
        "KitchenTicket.tableLabel",
        "KitchenTicket.serviceMode",
        "KitchenTicket.coursing",
        "KitchenTicket.buzzerCode",
        "KitchenTicket.status",
        "KitchenTicket.priority",
        "KitchenTicket.prioritisedByPrincipalId",
        "KitchenTicket.prioritiseReason"
       ],
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected active order fulfilment",
       "bindsTo": "FnbOrder",
       "columns": [
        "FnbOrder.id",
        "FnbOrder.orderNumber",
        "FnbOrder.outletId",
        "FnbOrder.serviceMode",
        "FnbOrder.tableVisitId",
        "FnbOrder.status",
        "FnbOrder.lines",
        "FnbOrder.grossAmount",
        "FnbOrder.taxAmount",
        "FnbOrder.kitchenTicketId",
        "FnbOrder.estimatedReadyAt",
        "FnbOrder.recordedAt",
        "FnbOrder.syncedAt"
       ],
       "operation": "getFnbOrder",
       "provenance": "contract fnb.yaml GET /fnb-orders/{orderId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue",
    "trigger": "onLoad"
   },
   {
    "operationId": "getFnbOrder",
    "contract": "fnb",
    "purpose": "Read an F&B order",
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
     "name": "stationId",
     "from": "session"
    },
    {
     "name": "orderId",
     "from": "KIT-002"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person.",
   "preloaded": [
    "FnbOrder.id",
    "FnbOrder.orderNumber",
    "FnbOrder.outletId",
    "FnbOrder.serviceMode",
    "FnbOrder.tableVisitId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-004",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn as FNB-3D in the client pack.** The pack's frame is the specification for this screen — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3d"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-005",
  "name": "Kitchen Station Workload & Dynamic Routing",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/kitchen-station-workload-dynamic-routing",
   "component": "apps/kitchen-display/src/routes/kitchen/KitchenStationWorkloadDynamicRoutiBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001"
   ],
   "exitTo": [
    "KIT-001"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "carries": [
      "stationId",
      "venueId"
     ],
     "provenance": "derived — KIT-001 declares entryState.params stationId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Station Workload &amp; Dynamic Routing* matched at 0.89. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listKitchenStations` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Kitchen Station Workload & Dynamic Routing — board 3 of the client F&B design set.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every kitchen station workload",
       "bindsTo": "KitchenStation",
       "columns": [
        "KitchenStation.id",
        "KitchenStation.code",
        "KitchenStation.name",
        "KitchenStation.outletId",
        "KitchenStation.menuItemIds",
        "KitchenStation.displayEndpoint",
        "KitchenStation.isActive"
       ],
       "operation": "listKitchenStations",
       "provenance": "contract fnb.yaml GET /kitchen/stations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected kitchen station workload",
       "bindsTo": "KitchenStation",
       "columns": [
        "KitchenStation.id",
        "KitchenStation.code",
        "KitchenStation.name",
        "KitchenStation.outletId",
        "KitchenStation.menuItemIds",
        "KitchenStation.displayEndpoint",
        "KitchenStation.isActive"
       ],
       "operation": "listKitchenStations",
       "provenance": "contract fnb.yaml GET /kitchen/stations"
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
       "operation": "setKitchenStations",
       "provenance": "contract fnb.yaml PUT /kitchen/stations"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenStations",
    "contract": "fnb",
    "purpose": "List preparation stations and their routing",
    "trigger": "onLoad"
   },
   {
    "operationId": "setKitchenStations",
    "contract": "fnb",
    "purpose": "Configure stations and item routing",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenStations"
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
     "from": "session"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person.",
   "preloaded": [
    "KitchenStation.id",
    "KitchenStation.code",
    "KitchenStation.name",
    "KitchenStation.outletId",
    "KitchenStation.menuItemIds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-005",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3e"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-006",
  "name": "Expeditor & Order Assembly",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/expeditor-order-assembly",
   "component": "apps/kitchen-display/src/routes/kitchen/ExpeditorOrderAssemblyBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001"
   ],
   "exitTo": [
    "KIT-001",
    "KIT-002"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-002",
     "trigger": "Kitchen Display System (KDS)",
     "provenance": "flow F88 step 1→2"
    },
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "carries": [
      "stationId",
      "venueId"
     ],
     "provenance": "derived — KIT-001 declares entryState.params stationId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **No expeditor role is modelled** — this reads and sets ticket status like the KDS. Whether an expeditor needs their own state is a kitchen question rather than a contract one. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Expeditor &amp; Order Assembly* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3f"
  ],
  "pattern": "listDetail",
  "patternReason": "`listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Expeditor & Order Assembly — board 3 of the client F&B design set.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every expeditor order assembly",
       "bindsTo": "KitchenTicket",
       "columns": [
        "KitchenTicket.id",
        "KitchenTicket.orderId",
        "KitchenTicket.orderNumber",
        "KitchenTicket.outletId",
        "KitchenTicket.tableLabel",
        "KitchenTicket.serviceMode",
        "KitchenTicket.coursing",
        "KitchenTicket.buzzerCode",
        "KitchenTicket.status",
        "KitchenTicket.priority",
        "KitchenTicket.prioritisedByPrincipalId",
        "KitchenTicket.prioritiseReason"
       ],
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected expeditor order assembly",
       "bindsTo": "KitchenTicket",
       "columns": [
        "KitchenTicket.id",
        "KitchenTicket.orderId",
        "KitchenTicket.orderNumber",
        "KitchenTicket.outletId",
        "KitchenTicket.tableLabel",
        "KitchenTicket.serviceMode",
        "KitchenTicket.coursing",
        "KitchenTicket.buzzerCode",
        "KitchenTicket.status",
        "KitchenTicket.priority",
        "KitchenTicket.prioritisedByPrincipalId",
        "KitchenTicket.prioritiseReason",
        "KitchenTicket.lines",
        "KitchenTicket.targetReadyAt",
        "KitchenTicket.elapsedSeconds"
       ],
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
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
       "operation": "setKitchenTicketStatus",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Chase",
       "operation": "chaseStation",
       "provenance": "contract fnb.yaml POST /kitchen-stations/{stationId}/chase"
      },
      {
       "kind": "secondaryButton",
       "label": "Mark",
       "operation": "markOrderCollected",
       "provenance": "contract fnb.yaml POST /orders/{orderId}/collected"
      },
      {
       "kind": "secondaryButton",
       "label": "Print",
       "operation": "printOrderLabel",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/label"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue",
    "trigger": "onLoad"
   },
   {
    "operationId": "setKitchenTicketStatus",
    "contract": "fnb",
    "purpose": "Advance a kitchen ticket",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "chaseStation",
    "contract": "fnb",
    "purpose": "The pass asks a station where an item is",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "markOrderCollected",
    "contract": "fnb",
    "purpose": "The guest took it",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "printOrderLabel",
    "contract": "fnb",
    "purpose": "A label for the bag",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
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
     "from": "session"
    },
    {
     "name": "ticketId",
     "from": "KIT-002"
    },
    {
     "name": "orderId",
     "from": "session"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person. An order tapped on the rail.",
   "preloaded": [
    "KitchenTicket.id",
    "KitchenTicket.orderId",
    "KitchenTicket.orderNumber",
    "KitchenTicket.outletId",
    "KitchenTicket.tableLabel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-006",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3f"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-007",
  "name": "Guest Collection, Buzzer & Digital Notification",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/guest-collection-buzzer-digital-notification",
   "component": "apps/kitchen-display/src/routes/kitchen/GuestCollectionBuzzerDigitalNotifiBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001"
   ],
   "exitTo": [
    "KIT-001"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "carries": [
      "stationId",
      "venueId"
     ],
     "provenance": "derived — KIT-001 declares entryState.params stationId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **`buzzerCode` exists and nothing dispatches to a physical pager.** The digital half works; the buzzer half assumes a device driver the package does not model. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3g` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3g"
  ],
  "pattern": "listDetail",
  "patternReason": "`listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Guest Collection, Buzzer & Digital Notification — board 3 of the client F&B design set.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every guest collection buzzer",
       "bindsTo": "KitchenTicket",
       "columns": [
        "KitchenTicket.id",
        "KitchenTicket.orderId",
        "KitchenTicket.orderNumber",
        "KitchenTicket.outletId",
        "KitchenTicket.tableLabel",
        "KitchenTicket.serviceMode",
        "KitchenTicket.coursing",
        "KitchenTicket.buzzerCode",
        "KitchenTicket.status",
        "KitchenTicket.priority",
        "KitchenTicket.prioritisedByPrincipalId",
        "KitchenTicket.prioritiseReason"
       ],
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected guest collection buzzer",
       "bindsTo": "KitchenTicket",
       "columns": [
        "KitchenTicket.id",
        "KitchenTicket.orderId",
        "KitchenTicket.orderNumber",
        "KitchenTicket.outletId",
        "KitchenTicket.tableLabel",
        "KitchenTicket.serviceMode",
        "KitchenTicket.coursing",
        "KitchenTicket.buzzerCode",
        "KitchenTicket.status",
        "KitchenTicket.priority",
        "KitchenTicket.prioritisedByPrincipalId",
        "KitchenTicket.prioritiseReason",
        "KitchenTicket.lines",
        "KitchenTicket.targetReadyAt",
        "KitchenTicket.elapsedSeconds"
       ],
       "operation": "listKitchenTickets",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
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
       "operation": "recordOrderHandover",
       "provenance": "contract fnb.yaml POST /guest-orders/{orderId}/delivery"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordOrderHandover",
    "contract": "fnb",
    "purpose": "Record that an order reached the guest",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
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
     "from": "session"
    },
    {
     "name": "orderId",
     "from": "KIT-002"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person.",
   "preloaded": [
    "KitchenTicket.id",
    "KitchenTicket.orderId",
    "KitchenTicket.orderNumber",
    "KitchenTicket.outletId",
    "KitchenTicket.tableLabel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-007",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn as FNB-3G in the client pack.** The pack's frame is the specification for this screen — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3g"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-008",
  "name": "Exceptions, Re-Fire & Unavailable Items",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/exceptions-re-fire-unavailable-items",
   "component": "apps/kitchen-display/src/routes/kitchen/ExceptionsReFireUnavailableItemsBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001",
    "KIT-004"
   ],
   "exitTo": [
    "KIT-001"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "carries": [
      "stationId",
      "venueId"
     ],
     "provenance": "derived — KIT-001 declares entryState.params stationId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **86 is a kitchen word and a real state.** An item marked unavailable here stops selling at every till in the venue within seconds, which is the only reason to put it on a kitchen screen. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.** **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3h` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3h`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Exceptions, Re-Fire &amp; Unavailable Items* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3h"
  ],
  "pattern": "listDetail",
  "patternReason": "`list86Events` reads the population and `getHaccpStatus` reads one of them — list, select, act",
  "purpose": "Exceptions, Re-Fire & Unavailable Items — board 3 of the client F&B design set.",
  "gaps": [
   {
    "operation": "getHaccpStatus",
    "why": "**2 declared operations reach no component on this screen**: getHaccpStatus, list86Events. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setItemAvailability",
       "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setKitchenTicketStatus",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Log",
       "operation": "logKitchenException",
       "provenance": "contract fnb.yaml POST /kitchen-exceptions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "setItemAvailability",
    "contract": "fnb",
    "purpose": "Mark an item available or eighty-sixed",
    "trigger": "onAction",
    "invalidates": [
     "list86Events"
    ]
   },
   {
    "operationId": "setKitchenTicketStatus",
    "contract": "fnb",
    "purpose": "Advance a kitchen ticket",
    "trigger": "onAction",
    "invalidates": [
     "list86Events"
    ]
   },
   {
    "operationId": "getHaccpStatus",
    "contract": "fnb",
    "purpose": "getHaccpStatus",
    "trigger": "onLoad"
   },
   {
    "operationId": "list86Events",
    "contract": "fnb",
    "purpose": "What came off the menu today, when, and for how long",
    "trigger": "onLoad"
   },
   {
    "operationId": "logKitchenException",
    "contract": "fnb",
    "purpose": "Something went wrong that is not a refire",
    "trigger": "onAction",
    "invalidates": [
     "list86Events"
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
     "from": "session"
    },
    {
     "name": "itemId",
     "from": "KIT-002"
    },
    {
     "name": "ticketId",
     "from": "KIT-002"
    },
    {
     "name": "outletId",
     "from": "session"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person. Resolves from the station assignment. A kitchen display belongs to one outlet."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-008",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3h"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-009",
  "name": "SLA, Priority & Service Rules",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/sla-priority-service-rules",
   "component": "apps/kitchen-display/src/routes/kitchen/SlaPriorityServiceRulesBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001"
   ],
   "exitTo": [
    "KIT-001"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "carries": [
      "stationId",
      "venueId"
     ],
     "provenance": "derived — KIT-001 declares entryState.params stationId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3j` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `FnB Board 3.dc.html` frame `fnb-3j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *SLA, Priority &amp; Service Rules* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3j"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`prioritiseKitchenTicket`, `setVenueSettings`) and no read of a population — it is settings, not a list",
  "purpose": "SLA, Priority & Service Rules — board 3 of the client F&B design set.",
  "gaps": [
   {
    "operation": "prioritiseKitchenTicket",
    "why": "**`prioritiseKitchenTicket` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Prioritise",
       "operation": "prioritiseKitchenTicket",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setVenueSettings",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "prioritiseKitchenTicket",
    "contract": "fnb",
    "purpose": "Move a ticket up the queue",
    "trigger": "onAction"
   },
   {
    "operationId": "setVenueSettings",
    "contract": "tenancy",
    "purpose": "Set support hours, quiet hours, segregated access and alerti",
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
     "name": "stationId",
     "from": "session"
    },
    {
     "name": "ticketId",
     "from": "KIT-002"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-009",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn by Claude Design on `FnB Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3j"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KIT-010",
  "name": "Kitchen Performance, AI & Operational Optimization",
  "module": "Kitchen",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "kitchen-display",
   "route": "/kitchen/kitchen-performance-ai-operational-optimization",
   "component": "apps/kitchen-display/src/routes/kitchen/KitchenPerformanceAiOperationalOptBoard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KIT-001"
   ],
   "exitTo": [
    "KIT-001"
   ],
   "inferred": false,
   "notes": "**Returns to KIT-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "carries": [
      "stationId",
      "venueId"
     ],
     "provenance": "derived — KIT-001 declares entryState.params stationId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August from board 3 of the client F&B design set.** **Board repointed 24 August.** This screen pointed at `wireframes/FnB Board 3.dc.html#fnb-3k` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "touchLarge",
  "densityReason": "**Bumped by somebody with flour on their hands, read from two metres, in a room where nobody is sitting down.** A kitchen display is not a back office at a different width.",
  "boardFrames": [
   "FnB Board 3.dc.html#fnb-3k"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getDashboard` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Kitchen Performance, AI & Operational Optimization — board 3 of the client F&B design set.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected kitchen performance operational",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ask",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth, oldest ticket age, station load. **Three numbers, glanceable** — anything a chef has to read is a number they will not read.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows.",
   "offline": "**Not available offline.** `getDashboard` is an analytical read (ADR-0016) and there is nothing local to serve. The rail on KIT-001 is what survives a network loss. **Corrected 24 August**: the earlier wording described the kitchen rather than this screen, and a checker cannot tell those apart from prose."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
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
     "name": "stationId",
     "from": "session"
    },
    {
     "name": "dashboardId",
     "from": "KIT-002"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P15 Kitchen Display.dc.html#kit-010",
   "source": "Claude Design F&B pack, 20 August",
   "note": "**Drawn as FNB-3K in the client pack.** The pack's frame is the specification for this screen — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/FnB Board 3.dc.html#fnb-3k"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P15",
   "formFactor": "kiosk",
   "app": "kitchen-display",
   "operator": "venue",
   "name": "Kitchen Display — Pass and Stations",
   "shortName": "Kitchen Display",
   "audience": "staff",
   "offlineCapable": true,
   "targetApp": {
    "app": "venue-pos",
    "name": "TICVAI POS",
    "shell": "display",
    "siblings": [
     "P04"
    ],
    "note": "**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.",
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
 "askReportingQuestion": {
  "method": "POST",
  "path": "/reports/ask",
  "contract": "reporting",
  "summary": "Natural-language reporting query",
  "permission": "REPORT_VIEW_VENUE",
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
  "responds": "NaturalLanguageAnswer"
 },
 "chaseStation": {
  "method": "POST",
  "path": "/kitchen-stations/{stationId}/chase",
  "contract": "fnb",
  "summary": "The pass asks a station where an item is",
  "permission": "ORDER_MODIFY",
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
  "responds": null
 },
 "fireCourse": {
  "method": "POST",
  "path": "/kitchen-tickets/{ticketId}/fire",
  "contract": "fnb",
  "summary": "Send a held course to the pass",
  "permission": "ORDER_MODIFY",
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
  "responds": "KitchenTicket"
 },
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
 },
 "getFnbOrder": {
  "method": "GET",
  "path": "/fnb-orders/{orderId}",
  "contract": "fnb",
  "summary": "Read an F&B order",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FnbOrder"
 },
 "getHaccpStatus": {
  "method": "GET",
  "path": "/food-safety/status",
  "contract": "fnb",
  "summary": "Where this venue stands, right now",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "holdCourse": {
  "method": "POST",
  "path": "/kitchen-tickets/{ticketId}/hold",
  "contract": "fnb",
  "summary": "Stop a course going out",
  "permission": "ORDER_MODIFY",
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
  "responds": "KitchenTicket"
 },
 "list86Events": {
  "method": "GET",
  "path": "/outlets/{outletId}/86-events",
  "contract": "fnb",
  "summary": "What came off the menu today, when, and for how long",
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
  "responds": null
 },
 "listFnbOrders": {
  "method": "GET",
  "path": "/fnb-orders",
  "contract": "fnb",
  "summary": "List F&B orders",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "tableVisitId",
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
 "listKitchenStations": {
  "method": "GET",
  "path": "/kitchen/stations",
  "contract": "fnb",
  "summary": "List preparation stations and their routing",
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
  "responds": "KitchenStation"
 },
 "listKitchenTickets": {
  "method": "GET",
  "path": "/kitchen/tickets",
  "contract": "fnb",
  "summary": "Kitchen ticket queue",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "stationId",
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
  "responds": "KitchenTicket"
 },
 "logKitchenException": {
  "method": "POST",
  "path": "/kitchen-exceptions",
  "contract": "fnb",
  "summary": "Something went wrong that is not a refire",
  "permission": "INCIDENT_REPORT",
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
  "responds": null
 },
 "markOrderCollected": {
  "method": "POST",
  "path": "/orders/{orderId}/collected",
  "contract": "fnb",
  "summary": "The guest took it",
  "permission": "ORDER_MODIFY",
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
  "responds": null
 },
 "notifyServer": {
  "method": "POST",
  "path": "/table-visits/{visitId}/notify-server",
  "contract": "fnb",
  "summary": "The kitchen calls the server to the pass",
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
 "printOrderLabel": {
  "method": "POST",
  "path": "/kitchen-tickets/{ticketId}/label",
  "contract": "fnb",
  "summary": "A label for the bag",
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
  "responds": null
 },
 "prioritiseKitchenTicket": {
  "method": "POST",
  "path": "/kitchen/tickets/{ticketId}/prioritise",
  "contract": "fnb",
  "summary": "Move a ticket up the queue",
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
  "responds": "KitchenTicket"
 },
 "recallKitchenTicket": {
  "method": "POST",
  "path": "/kitchen-tickets/{ticketId}/recall",
  "contract": "fnb",
  "summary": "Bring back a ticket that was bumped by mistake",
  "permission": "ORDER_MODIFY",
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
  "responds": "KitchenTicket"
 },
 "recordOrderHandover": {
  "method": "POST",
  "path": "/guest-orders/{orderId}/delivery",
  "contract": "fnb",
  "summary": "Record that an order reached the guest",
  "permission": "ORDER_MODIFY",
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
  "responds": "GuestOrderStatus"
 },
 "refireItem": {
  "method": "POST",
  "path": "/kitchen-tickets/{ticketId}/refire",
  "contract": "fnb",
  "summary": "Make it again",
  "permission": "ORDER_MODIFY",
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
  "responds": "KitchenTicket"
 },
 "setCourseRules": {
  "method": "PUT",
  "path": "/outlets/{outletId}/course-rules",
  "contract": "fnb",
  "summary": "How this outlet courses by default",
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
 "setItemAvailability": {
  "method": "PUT",
  "path": "/menu-items/{itemId}/availability",
  "contract": "fnb",
  "summary": "Mark an item available or eighty-sixed",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": "MenuItem"
 },
 "setKitchenStations": {
  "method": "PUT",
  "path": "/kitchen/stations",
  "contract": "fnb",
  "summary": "Configure stations and item routing",
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
  "responds": "KitchenStation"
 },
 "setKitchenTicketStatus": {
  "method": "PUT",
  "path": "/kitchen/tickets/{ticketId}/status",
  "contract": "fnb",
  "summary": "Advance a kitchen ticket",
  "permission": "ORDER_MODIFY",
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
  "responds": "KitchenTicket"
 },
 "setVenueSettings": {
  "method": "PUT",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Set support hours, quiet hours, segregated access and alerting",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "VenueSettings",
  "responds": "VenueSettings"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreateFnbOrderLine": {
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
    "minimum": 1
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
    "description": "Free text to the kitchen. Allergy notes belong here and are surfaced prominently."
   },
   "seatNumber": {
    "type": "integer",
    "nullable": true,
    "description": "Which cover ordered it. Drives split-by-covers accurately."
   },
   "course": {
    "type": "integer",
    "nullable": true,
    "description": "Course grouping, so the kitchen fires in sequence."
   }
  }
 },
 "Dashboard": {
  "x-ticvai-persistence": "reporting.dashboard + reporting.dashboard_tile",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateDashboardRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "aggregateCost",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "aggregateCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Combined refresh load of every tile."
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
 },
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n",
  "enum": [
   "orders",
   "orderLines",
   "payments",
   "refunds",
   "shifts",
   "scanEvents",
   "entitlements",
   "products",
   "inventory",
   "stockMovements",
   "stockCounts",
   "waste",
   "workstations",
   "devices",
   "principals",
   "loyalty",
   "reviews",
   "queueEntries",
   "guests",
   "campaigns",
   "cases",
   "ledgerEntries",
   "workOrders",
   "approvals",
   "purchaseOrders",
   "receipts",
   "requisitions",
   "stockBatches",
   "resourceBookings",
   "delegations",
   "forms",
   "challenges",
   "wallets",
   "resaleListings"
  ]
 },
 "FnbOrder": {
  "x-ticvai-persistence": "fnb.fnb_order + fnb.fnb_order_line",
  "type": "object",
  "required": [
   "id",
   "orderNumber",
   "outletId",
   "serviceMode",
   "status",
   "lines",
   "grossAmount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "serviceMode": {
    "$ref": "#/components/schemas/ServiceMode"
   },
   "tableVisitId": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/FnbOrderStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "allOf": [
      {
       "$ref": "#/components/schemas/CreateFnbOrderLine"
      },
      {
       "type": "object",
       "properties": {
        "status": {
         "$ref": "#/components/schemas/FnbOrderStatus"
        },
        "unitPrice": {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        },
        "lineTotal": {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       }
      }
     ]
    }
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "kitchenTicketId": {
    "type": "string",
    "nullable": true
   },
   "estimatedReadyAt": {
    "type": "string",
    "format": "date-time",
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
 "KitchenStation": {
  "x-ticvai-persistence": "fnb.kitchen_station",
  "type": "object",
  "required": [
   "id",
   "code",
   "name"
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
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "menuItemIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Items routed to this station."
   },
   "displayEndpoint": {
    "type": "string",
    "nullable": true,
    "description": "Where the venue's KDS listens. Absent where a fallback screen is used instead.\n"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "KitchenTicket": {
  "x-ticvai-persistence": "fnb.kitchen_ticket + fnb.kitchen_ticket_line",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "outletId",
   "status",
   "lines",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "tableLabel": {
    "type": "string",
    "nullable": true
   },
   "serviceMode": {
    "$ref": "#/components/schemas/ServiceMode"
   },
   "coursing": {
    "type": "string",
    "nullable": true,
    "enum": [
     "fireAndForget",
     "holdAndFire",
     "phased",
     "timed",
     "delayed"
    ],
    "description": "BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"
   },
   "buzzerCode": {
    "type": "string",
    "nullable": true,
    "description": "BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"
   },
   "status": {
    "$ref": "#/components/schemas/KitchenTicketStatus"
   },
   "priority": {
    "type": "integer",
    "description": "Higher fires sooner. Raised by Fast Pass or supervisor override."
   },
   "prioritisedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "prioritiseReason": {
    "type": "string",
    "nullable": true
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "name",
      "quantity",
      "status"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "modifiers": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "allergens": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "course": {
       "type": "integer",
       "nullable": true
      },
      "stationId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "status": {
       "$ref": "#/components/schemas/KitchenTicketStatus"
      }
     }
    }
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "targetReadyAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "elapsedSeconds": {
    "type": "integer"
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
 "MenuItem": {
  "x-ticvai-persistence": "fnb.menu_item",
  "type": "object",
  "required": [
   "id",
   "productVariantId",
   "name",
   "price",
   "isAvailable"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productVariantId": {
    "type": "string",
    "format": "uuid",
    "description": "The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"
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
   "sortOrder": {
    "type": "integer"
   },
   "modifierGroupIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "stationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isStockTracked": {
    "type": "boolean",
    "description": "True where a recipe exists. Stock-tracked items cannot be sold offline."
   },
   "isAvailable": {
    "type": "boolean"
   },
   "unavailableReason": {
    "type": "string",
    "nullable": true
   },
   "preparationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "allergens": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "NaturalLanguageAnswer": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "conversationId",
   "question",
   "interpretation",
   "result",
   "confidence"
  ],
  "properties": {
   "conversationId": {
    "type": "string"
   },
   "question": {
    "type": "string"
   },
   "interpretation": {
    "type": "string",
    "description": "What the question was understood to mean, in plain language."
   },
   "generatedQuery": {
    "type": "object",
    "description": "The structured query produced — data source, columns, filters, grouping. Returned so the answer can be checked. An answer nobody can verify is worse than no answer.\n",
    "properties": {
     "dataSource": {
      "$ref": "#/components/schemas/DataSource"
     },
     "columns": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ReportColumn"
      }
     },
     "filters": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ReportFilter"
      }
     },
     "groupBy": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "result": {
    "$ref": "#/components/schemas/ReportResult"
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "suggestedFollowUps": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modelVersion": {
    "type": "string"
   },
   "tokensUsed": {
    "type": "integer"
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
 "ReportColumn": {
  "x-ticvai-persistence": "reporting.report_column",
  "type": "object",
  "required": [
   "field"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "aggregation": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Aggregation"
     }
    ],
    "default": "none"
   },
   "sortOrder": {
    "type": "integer"
   },
   "sortDirection": {
    "type": "string",
    "enum": [
     "asc",
     "desc"
    ]
   },
   "format": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "ReportFilter": {
  "x-ticvai-persistence": "reporting.report_filter",
  "type": "object",
  "required": [
   "field",
   "operator"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "contains",
     "isNull",
     "isNotNull"
    ]
   },
   "value": {},
   "values": {
    "type": "array",
    "items": {}
   },
   "isParameter": {
    "type": "boolean",
    "default": false,
    "description": "Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"
   }
  }
 },
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 },
 "ServiceMode": {
  "type": "string",
  "enum": [
   "quickService",
   "tableService",
   "roomService",
   "collection",
   "delivery"
  ]
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string"
     },
     "windows": {
      "type": "array",
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
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string"
     },
     "to": {
      "type": "string"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string"
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       false,
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": false,
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   }
  }
 }
}
```
