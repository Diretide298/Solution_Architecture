# P15-kitchen-01 — P15 · Kitchen

**10 screens · 27 operations · 28 schemas · 8 permissions**

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
| `KIT-002` | Kitchen Display System (KDS) | listDetail | 7 | 6 | — |
| `KIT-003` | Order Firing & Course Management | configEditor | 6 | 4 | — |
| `KIT-004` | Active Order Management & Fulfilment Journey | listDetail | 2 | 0 | — |
| `KIT-005` | Kitchen Station Workload & Dynamic Routing | listDetail | 4 | 1 | — |
| `KIT-006` | Expeditor & Order Assembly | listDetail | 5 | 3 | — |
| `KIT-007` | Guest Collection, Buzzer & Digital Notification | listDetail | 2 | 1 | — |
| `KIT-008` | Exceptions, Re-Fire & Unavailable Items | listDetail | 6 | 3 | — |
| `KIT-009` | SLA, Priority & Service Rules | configEditor | 3 | 1 | — |
| `KIT-010` | Kitchen Performance, AI & Operational Optimization | statusTracker | 3 | 1 | — |

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
  "permission": "ORDER_VIEW",
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
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher",
     "carries": [
      "orderId"
     ]
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
     "provenance": "structural — KIT-001 is P15's home screen and its exits are its launcher",
     "carries": [
      "orderId"
     ]
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
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "metricTile",
       "label": "Kitchen stations",
       "bindsTo": "KitchenStation",
       "operation": "listKitchenStations",
       "permission": "PRODUCT_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/stations"
      },
      {
       "kind": "metricTile",
       "label": "Fnb orders",
       "bindsTo": "FnbOrder",
       "operation": "listFnbOrders",
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml GET /fnb-orders"
      },
      {
       "kind": "numberField",
       "label": "Course",
       "operation": "listKitchenTickets",
       "notes": "Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in station setup) and the display sends no `stationId` (decided 28 September, audit R277).",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listKitchenTickets",
       "notes": "Sends `?status=` to `listKitchenTickets`.",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "dataTable",
       "label": "Every kitchen ticket",
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
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).",
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
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
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
  "permission": "ORDER_VIEW",
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
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "provenance": "derived — KIT-001 declares entryState.params  and KIT-002 holds none of them, so the edge carries nothing and KIT-001 opens cold"
    },
    {
     "to": "KIT-003",
     "trigger": "Order Firing & Course Management",
     "provenance": "flow F83 step 2→3, F88 step 2→3",
     "carries": [
      "ticketId"
     ]
    },
    {
     "to": "EMP-058",
     "trigger": "Starters cleared",
     "provenance": "flow F29 step 4→5",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "ticketId",
      "visitId"
     ]
    },
    {
     "to": "EMP-059",
     "trigger": "The server comps the delayed dish",
     "provenance": "flow F29 step 6→7",
     "operation": "refireItem",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "visitId"
     ]
    },
    {
     "to": "POS-022",
     "trigger": "The guest is called and takes it",
     "provenance": "flow F108 step 5→6",
     "operation": "setKitchenTicketStatus",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "orderId",
      "ticketId"
     ]
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
       "kind": "numberField",
       "label": "Course",
       "operation": "listKitchenTickets",
       "notes": "Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in station setup) and the display sends no `stationId` (decided 28 September, audit R277).",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listKitchenTickets",
       "notes": "Sends `?status=` to `listKitchenTickets`.",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "dataTable",
       "label": "Every kitchen ticket",
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
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
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
       "label": "The selected kitchen ticket",
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
       "permission": "ORDER_VIEW",
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
       "label": "Save kitchen ticket status",
       "operation": "setKitchenTicketStatus",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Fire course",
       "operation": "fireCourse",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/fire"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold course",
       "operation": "holdCourse",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Refire item",
       "operation": "refireItem",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/refire"
      },
      {
       "kind": "secondaryButton",
       "label": "Recall kitchen ticket",
       "operation": "recallKitchenTicket",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/recall"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify server",
       "operation": "notifyServer",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/notify-server"
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
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
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
  "overlays": [
   {
    "id": "formSetKitchenTicketStatus",
    "component": "modal",
    "trigger": "Save kitchen ticket status",
    "body": "**Collects what `setKitchenTicketStatus` sends before it is called.** Required: `status`, `recordedAt`. Optional: `lineIds`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save kitchen ticket status",
     "operation": "setKitchenTicketStatus"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "recordedAt",
      "lineIds",
      "stationId"
     ]
    },
    "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
   },
   {
    "id": "formFireCourse",
    "component": "modal",
    "trigger": "Fire course",
    "body": "**Collects what `fireCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `fireAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Fire course",
     "operation": "fireCourse"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "course",
      "fireAt"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/fire"
   },
   {
    "id": "formHoldCourse",
    "component": "modal",
    "trigger": "Hold course",
    "body": "**Collects what `holdCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold course",
     "operation": "holdCourse"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "course",
      "reason"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/hold"
   },
   {
    "id": "formRefireItem",
    "component": "modal",
    "trigger": "Refire item",
    "body": "**Collects what `refireItem` sends before it is called.** Required: `lineId`, `reason`, `recordedAt`. Optional: `chargeable`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Refire item",
     "operation": "refireItem"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "lineId",
      "reason",
      "recordedAt",
      "chargeable"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/refire"
   },
   {
    "id": "formRecallKitchenTicket",
    "component": "modal",
    "trigger": "Recall kitchen ticket",
    "body": "**Collects what `recallKitchenTicket` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Recall kitchen ticket",
     "operation": "recallKitchenTicket"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/recall"
   },
   {
    "id": "formNotifyServer",
    "component": "modal",
    "trigger": "Notify server",
    "body": "**Collects what `notifyServer` sends before it is called.** Nothing in the body is required. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Notify server",
     "operation": "notifyServer"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/notify-server"
   }
  ],
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
  "permission": "ORDER_MODIFY",
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
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "provenance": "derived — KIT-001 declares entryState.params  and KIT-003 holds none of them, so the edge carries nothing and KIT-001 opens cold"
    },
    {
     "to": "KIT-004",
     "trigger": "Active Order Management & Fulfilment Journey",
     "provenance": "flow F83 step 3→4, F88 step 3→4",
     "carries": [
      "orderId"
     ]
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
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save kitchen ticket status",
       "operation": "setKitchenTicketStatus",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Prioritise kitchen ticket",
       "operation": "prioritiseKitchenTicket",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "secondaryButton",
       "label": "Fire course",
       "operation": "fireCourse",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/fire"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold course",
       "operation": "holdCourse",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Save course rules",
       "operation": "setCourseRules",
       "permission": "PRODUCT_CONFIGURE",
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
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277)."
      },
      {
       "kind": "numberField",
       "label": "Course",
       "operation": "listKitchenTickets",
       "notes": "Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in station setup) and the display sends no `stationId` (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "setKitchenTicketStatus",
       "notes": "Required.",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "datePicker",
       "label": "Recorded at",
       "operation": "setKitchenTicketStatus",
       "notes": "Required.",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "multiSelect",
       "label": "Line ids",
       "operation": "setKitchenTicketStatus",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "textField",
       "label": "Station id",
       "operation": "setKitchenTicketStatus",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status",
       "notes": "Filled from this display's station assignment (`KitchenStation.displayWorkstationIds`), not typed or picked (audit R277)."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic (audit R277).",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_MODIFY` gets this state naming `ORDER_MODIFY`**, the screen's `permission` and the one its fire, hold, status and prioritise actions need (the screen has no read); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue, filtered by course (audit R277)",
    "trigger": "onLoad"
   },
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
  "overlays": [
   {
    "id": "formPrioritiseKitchenTicket",
    "component": "modal",
    "trigger": "Prioritise kitchen ticket",
    "body": "**Collects what `prioritiseKitchenTicket` sends before it is called.** Required: `reason`. Optional: `priority`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Prioritise kitchen ticket",
     "operation": "prioritiseKitchenTicket"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "priority"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
   },
   {
    "id": "formFireCourse",
    "component": "modal",
    "trigger": "Fire course",
    "body": "**Collects what `fireCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `fireAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Fire course",
     "operation": "fireCourse"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "course",
      "fireAt"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/fire"
   },
   {
    "id": "formHoldCourse",
    "component": "modal",
    "trigger": "Hold course",
    "body": "**Collects what `holdCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `reason`, `note`. **When the reason is Other, the note is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold course",
     "operation": "holdCourse"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "course",
      "reason",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/hold"
   },
   {
    "id": "formSetCourseRules",
    "component": "modal",
    "trigger": "Save course rules",
    "body": "**Collects what `setCourseRules` sends before it is called.** Nothing in the body is required. Optional: `outletId`, `defaultCoursing`, `courseNames`, `autoFireMinutes`, `serviceModeOverrides`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CourseRules",
    "confirm": {
     "label": "Save course rules",
     "operation": "setCourseRules"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outletId",
      "defaultCoursing",
      "courseNames",
      "autoFireMinutes",
      "serviceModeOverrides",
      "scopePath"
     ]
    },
    "provenance": "contract fnb.yaml PUT /outlets/{outletId}/course-rules"
   }
  ],
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
  "permission": "ORDER_VIEW",
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
       "kind": "numberField",
       "label": "Course",
       "operation": "listKitchenTickets",
       "notes": "Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in station setup) and the display sends no `stationId` (decided 28 September, audit R277).",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listKitchenTickets",
       "notes": "Sends `?status=` to `listKitchenTickets`.",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "dataTable",
       "label": "Every kitchen ticket",
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
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
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
       "label": "The selected kitchen ticket",
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
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "detailPanel",
       "label": "The F&B order",
       "bindsTo": "FnbOrder",
       "columns": [
        "FnbOrder.id",
        "FnbOrder.orderNumber",
        "FnbOrder.outletId",
        "FnbOrder.serviceMode",
        "FnbOrder.tableVisitId",
        "FnbOrder.status",
        "FnbOrder.lines",
        "FnbOrder.salesOrderId",
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
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoResults": "Nothing matches this station or course filter. **The rail is not empty** — the filter is narrow, and on a kitchen screen that distinction is the difference between calm and panic.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
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
  "permission": "PRODUCT_VIEW",
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
     "provenance": "derived — KIT-001 declares entryState.params  and KIT-005 holds none of them, so the edge carries nothing and KIT-001 opens cold"
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
       "kind": "textField",
       "label": "Outlet id",
       "operation": "listKitchenStations",
       "notes": "Sends `?outletId=` to `listKitchenStations`.",
       "provenance": "contract fnb.yaml GET /kitchen/stations"
      },
      {
       "kind": "dataTable",
       "label": "Every kitchen station",
       "bindsTo": "KitchenStation",
       "columns": [
        "KitchenStation.id",
        "KitchenStation.code",
        "KitchenStation.name",
        "KitchenStation.outletId",
        "KitchenStation.menuItemIds",
        "KitchenStation.displayEndpoint",
        "KitchenStation.displayWorkstationIds",
        "KitchenStation.isActive"
       ],
       "operation": "listKitchenStations",
       "permission": "PRODUCT_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/stations"
      },
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277)."
      },
      {
       "kind": "numberField",
       "label": "Course",
       "operation": "listKitchenTickets",
       "notes": "Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in station setup) and the display sends no `stationId` (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
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
       "label": "The selected kitchen station",
       "bindsTo": "KitchenStation",
       "columns": [
        "KitchenStation.id",
        "KitchenStation.code",
        "KitchenStation.name",
        "KitchenStation.outletId",
        "KitchenStation.menuItemIds",
        "KitchenStation.displayEndpoint",
        "KitchenStation.displayWorkstationIds",
        "KitchenStation.isActive"
       ],
       "operation": "listKitchenStations",
       "permission": "PRODUCT_VIEW",
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
       "label": "Save kitchen stations",
       "operation": "setKitchenStations",
       "permission": "PRODUCT_CONFIGURE",
       "provenance": "contract fnb.yaml PUT /kitchen/stations",
       "notes": "Includes each station's display assignment (`displayWorkstationIds`); a workstation assigned to two stations is refused 400 (decided 28 September, audit R277)."
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
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue, filtered by course (audit R277)",
    "trigger": "onLoad"
   },
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
   },
   {
    "operationId": "rebalanceStationLoad",
    "contract": "fnb",
    "purpose": "Move work between stations mid-service",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
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
  "overlays": [
   {
    "id": "formSetKitchenStations",
    "component": "modal",
    "trigger": "Save kitchen stations",
    "body": "**Collects what `setKitchenStations` sends before it is called.** Required: `stations`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save kitchen stations",
     "operation": "setKitchenStations"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "stations"
     ]
    },
    "provenance": "contract fnb.yaml PUT /kitchen/stations"
   }
  ],
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
  "permission": "ORDER_VIEW",
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
     "to": "KIT-001",
     "trigger": "Kitchen Operations Command Center",
     "provenance": "derived — KIT-001 declares entryState.params  and KIT-006 holds none of them, so the edge carries nothing and KIT-001 opens cold"
    },
    {
     "to": "KIT-002",
     "trigger": "Kitchen Display System (KDS)",
     "provenance": "flow F88 step 1→2",
     "carries": [
      "ticketId"
     ]
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
       "kind": "numberField",
       "label": "Course",
       "operation": "listKitchenTickets",
       "notes": "Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in station setup) and the display sends no `stationId` (decided 28 September, audit R277).",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listKitchenTickets",
       "notes": "Sends `?status=` to `listKitchenTickets`.",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "dataTable",
       "label": "Every kitchen ticket",
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
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
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
       "label": "The selected kitchen ticket",
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
       "permission": "ORDER_VIEW",
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
       "label": "Save kitchen ticket status",
       "operation": "setKitchenTicketStatus",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Chase station",
       "operation": "chaseStation",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen-stations/{stationId}/chase"
      },
      {
       "kind": "secondaryButton",
       "label": "Mark order collected",
       "operation": "markOrderCollected",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /orders/{orderId}/collected"
      },
      {
       "kind": "secondaryButton",
       "label": "Print order label",
       "operation": "printOrderLabel",
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/label"
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
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
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
  "overlays": [
   {
    "id": "formSetKitchenTicketStatus",
    "component": "modal",
    "trigger": "Save kitchen ticket status",
    "body": "**Collects what `setKitchenTicketStatus` sends before it is called.** Required: `status`, `recordedAt`. Optional: `lineIds`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save kitchen ticket status",
     "operation": "setKitchenTicketStatus"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "recordedAt",
      "lineIds",
      "stationId"
     ]
    },
    "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
   },
   {
    "id": "formChaseStation",
    "component": "modal",
    "trigger": "Chase station",
    "body": "**Collects what `chaseStation` sends before it is called.** Required: `ticketId`, `recordedAt`. Optional: `lineId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Chase station",
     "operation": "chaseStation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ticketId",
      "recordedAt",
      "lineId"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-stations/{stationId}/chase"
   },
   {
    "id": "formMarkOrderCollected",
    "component": "modal",
    "trigger": "Mark order collected",
    "body": "**Collects what `markOrderCollected` sends before it is called.** Required: `recordedAt`. Optional: `verifiedBy`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Mark order collected",
     "operation": "markOrderCollected"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "verifiedBy"
     ]
    },
    "provenance": "contract fnb.yaml POST /orders/{orderId}/collected"
   }
  ],
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
  "permission": "ORDER_VIEW",
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
     "provenance": "derived — KIT-001 declares entryState.params  and KIT-007 holds none of them, so the edge carries nothing and KIT-001 opens cold"
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
       "kind": "numberField",
       "label": "Course",
       "operation": "listKitchenTickets",
       "notes": "Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in station setup) and the display sends no `stationId` (decided 28 September, audit R277).",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listKitchenTickets",
       "notes": "Sends `?status=` to `listKitchenTickets`.",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "dataTable",
       "label": "Every kitchen ticket",
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
       "permission": "ORDER_VIEW",
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
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
       "label": "The selected kitchen ticket",
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
       "permission": "ORDER_VIEW",
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
       "label": "Record order handover",
       "operation": "recordOrderHandover",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /guest-orders/{orderId}/delivery"
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
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_VIEW` gets this state naming `ORDER_VIEW`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
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
  "overlays": [
   {
    "id": "formRecordOrderHandover",
    "component": "modal",
    "trigger": "Record order handover",
    "body": "**Collects what `recordOrderHandover` sends before it is called.** Required: `outcome`, `recordedAt`. Optional: `deliveredToLocationId`, `runnerPrincipalId`, `note`. **Only the outcome that fits the order's service mode is offered**: tableService `served`; quickService or collection `collected`; delivery or roomService `delivered`, with `deliveredToLocationId` required. `guestNotFound` and `refused` are offered for every mode. Any other pairing is refused 422 `outcomeNotForServiceMode` (decided 28 September, audit R125 (1)). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record order handover",
     "operation": "recordOrderHandover"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outcome",
      "recordedAt",
      "deliveredToLocationId",
      "runnerPrincipalId",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /guest-orders/{orderId}/delivery"
   }
  ],
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
  "permission": "PRODUCT_VIEW",
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
     "provenance": "derived — KIT-001 declares entryState.params  and KIT-008 holds none of them, so the edge carries nothing and KIT-001 opens cold"
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
    "why": "**`getHaccpStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract fnb.yaml GET /food-safety/status"
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
       "label": "Save item availability",
       "operation": "setItemAvailability",
       "permission": "PRODUCT_CONFIGURE",
       "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
      },
      {
       "kind": "secondaryButton",
       "label": "Save kitchen ticket status",
       "operation": "setKitchenTicketStatus",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Log kitchen exception",
       "operation": "logKitchenException",
       "permission": "INCIDENT_REPORT",
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
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277)."
      },
      {
       "kind": "numberField",
       "label": "Course",
       "operation": "listKitchenTickets",
       "notes": "Sends `?course=` to `listKitchenTickets`; only that course's lines come back. **No station picker**: the display's station comes from its assignment (`KitchenStation.displayWorkstationIds`, set in station setup) and the display sends no `stationId` (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "list86Events",
       "notes": "Sends `?from=` to `list86Events`.",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/86-events"
      },
      {
       "kind": "dataTable",
       "label": "Every eighty six event",
       "bindsTo": "EightySixEvent",
       "columns": [
        "EightySixEvent.id",
        "EightySixEvent.outletId",
        "EightySixEvent.menuItemId",
        "EightySixEvent.offAt",
        "EightySixEvent.backAt",
        "EightySixEvent.reason",
        "EightySixEvent.calledByPrincipalId",
        "EightySixEvent.refusedOrderCount"
       ],
       "operation": "list86Events",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/86-events"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "reads",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Haccp status",
       "operation": "getHaccpStatus",
       "notes": "Shows `checksDue`, `checksMissed`, `openActions`, `unsignedActions`, `oldestOpenActionAgeHours`, `lastInspectionAt` from `getHaccpStatus`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract fnb.yaml GET /food-safety/status"
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
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `PRODUCT_VIEW` gets this state naming `PRODUCT_VIEW`**, the screen's `permission` and the one `list86Events`, the population it reads, enforces (`getHaccpStatus` needs `INCIDENT_VIEW` and reaches no component yet, see `gaps`); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
   "offline": "**Amber, and it keeps working.** The kitchen still has to send food out — a display that blanks mid-service is worse than one that says it is behind, and every bump journals locally and syncs when the network returns."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue, filtered by course (audit R277)",
    "trigger": "onLoad"
   },
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
  "overlays": [
   {
    "id": "formSetItemAvailability",
    "component": "modal",
    "trigger": "Save item availability",
    "body": "**Collects what `setItemAvailability` sends before it is called.** Required: `isAvailable`, `recordedAt`. Optional: `reason`, `note`, `restoreAt`. **When the reason is Other, the note is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save item availability",
     "operation": "setItemAvailability"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "isAvailable",
      "recordedAt",
      "reason",
      "note",
      "restoreAt"
     ]
    },
    "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
   },
   {
    "id": "formSetKitchenTicketStatus",
    "component": "modal",
    "trigger": "Save kitchen ticket status",
    "body": "**Collects what `setKitchenTicketStatus` sends before it is called.** Required: `status`, `recordedAt`. Optional: `lineIds`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save kitchen ticket status",
     "operation": "setKitchenTicketStatus"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "recordedAt",
      "lineIds",
      "stationId"
     ]
    },
    "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
   },
   {
    "id": "formLogKitchenException",
    "component": "modal",
    "trigger": "Log kitchen exception",
    "body": "**Collects what `logKitchenException` sends before it is called.** Required: `kind`, `outletId`, `recordedAt`. Optional: `stationId`, `ticketId`, `durationMinutes`, `note`. **When the kind is Other, the note is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Log kitchen exception",
     "operation": "logKitchenException"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "outletId",
      "recordedAt",
      "stationId",
      "ticketId",
      "durationMinutes",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-exceptions"
   }
  ],
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
  "permission": "ORDER_MODIFY",
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
     "provenance": "derived — KIT-001 declares entryState.params  and KIT-009 holds none of them, so the edge carries nothing and KIT-001 opens cold"
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
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Prioritise kitchen ticket",
       "operation": "prioritiseKitchenTicket",
       "permission": "ORDER_MODIFY",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "secondaryButton",
       "label": "Save venue settings",
       "operation": "setVenueSettings",
       "permission": "TENANT_CONFIGURE",
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
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Reason",
       "operation": "prioritiseKitchenTicket",
       "notes": "Required.",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "numberField",
       "label": "Priority",
       "operation": "prioritiseKitchenTicket",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rail, oldest ticket first. **The count renders before the tickets** — a kitchen wants to know how deep it is before it reads anything.",
   "error": "Could not reach the platform. **The rail is still live from cache** and every bump is queued.",
   "emptyFirstRun": "**No tickets. The kitchen is clear**, and that is worth saying plainly rather than showing a blank rail — a screen that looks broken and a screen that means nothing to do are the same picture otherwise.",
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `ORDER_MODIFY` gets this state naming `ORDER_MODIFY`**, the screen's `permission` and the one prioritising needs (the screen has no read); a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
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
   },
   {
    "operationId": "setKitchenSla",
    "contract": "fnb",
    "purpose": "The outlet's kitchen service-time targets",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
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
     "name": "outletId",
     "from": "session"
    },
    {
     "name": "ticketId",
     "from": "KIT-002"
    }
   ],
   "coldEntry": "**Cold is the only way in.** Nobody logs into a kitchen display — it is on when the kitchen is open, and it resolves its station from the device assignment rather than from a person. **`outletId` comes from that assignment too** (confirmed 29 September, readiness close-out): the display is a tenancy `Workstation` listed in its station's `KitchenStation.displayWorkstationIds`, and the station carries `outletId`, so `setKitchenSla` (per outlet) needs nothing the session does not already hold, as KIT-003 and KIT-008 already take it."
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
  "overlays": [
   {
    "id": "formSetVenueSettings",
    "component": "modal",
    "trigger": "Save venue settings",
    "body": "**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `id`, `venueId`, `currencyCode`, `currencyScale`, `supportHours`, `quietHours`, `biometrics`, `segregatedAccess`, `alerting`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "VenueSettings",
    "confirm": {
     "label": "Save venue settings",
     "operation": "setVenueSettings"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "currencyCode",
      "currencyScale",
      "supportHours",
      "quietHours",
      "biometrics",
      "segregatedAccess",
      "alerting"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
   }
  ],
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
  "permission": "REPORT_VIEW_VENUE",
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
     "provenance": "derived — KIT-001 declares entryState.params  and KIT-010 holds none of them, so the edge carries nothing and KIT-001 opens cold"
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
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "permission": "REPORT_VIEW_VENUE",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      },
      {
       "kind": "cardList",
       "bindsTo": "KitchenTicket[]",
       "notes": "**One ticket per card, ordered by promise time not arrival.** A ticket due in two minutes sits above one that arrived first, because a kitchen works to when food is wanted.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "metricTile",
       "notes": "Depth and oldest ticket age. **Two numbers, glanceable** — anything a chef has to read is a number they will not read. The station-load tile is not in the first release (decided 28 September, audit R277).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Bump",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ask reporting question",
       "operation": "askReportingQuestion",
       "permission": "REPORT_VIEW_VENUE",
       "provenance": "contract reporting.yaml POST /reports/ask"
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
   "emptyNoAccess": "This display is not assigned to a station. **Assignment is a back-office act** — a kitchen screen does not choose what it shows. **A principal without `REPORT_VIEW_VENUE` gets this state naming `REPORT_VIEW_VENUE`**, the screen's `permission` and the one its read enforces; a button whose own `permission` the principal lacks is hidden, and a 403 from an action names that operation's permission.",
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
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
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
  "overlays": [
   {
    "id": "formAskReportingQuestion",
    "component": "modal",
    "trigger": "Ask reporting question",
    "body": "**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ask reporting question",
     "operation": "askReportingQuestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "question",
      "conversationId",
      "venueId"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask"
   }
  ],
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
  "responds": "Page"
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
    "name": "outletId",
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
    "name": "course",
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
  "responds": "KitchenException"
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
  "responds": "FnbOrder"
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
  "responds": "OrderLabel"
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
 "rebalanceStationLoad": {
  "method": "POST",
  "path": "/kitchen-stations/rebalance",
  "contract": "fnb",
  "summary": "Move work between stations mid-service",
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
  "requestBody": "StationRebalance",
  "responds": "StationRebalance"
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
 "recordDashboardView": {
  "method": "POST",
  "path": "/dashboards/{dashboardId}/views",
  "contract": "reporting",
  "summary": "Record that a dashboard was opened",
  "permission": "REPORT_VIEW_VENUE",
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CourseRules",
  "responds": "CourseRules"
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MenuItem"
 },
 "setKitchenSla": {
  "method": "PUT",
  "path": "/outlets/{outletId}/kitchen-sla",
  "contract": "fnb",
  "summary": "How long a ticket may sit before it is late",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "KitchenSla",
  "responds": "KitchenSla"
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
   },
   {
    "name": "outletId",
    "in": "query",
    "required": true
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
 "CourseRules": {
  "type": "object",
  "x-ticvai-persistence": "fnb.course_rule",
  "description": "**An outlet's coursing default.** It was written to the resolution cache only, which the service model calls losable without consequence — an outlet's default vanished on a cache flush. One row per outlet.\n",
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The outlet in the path."
   },
   "defaultCoursing": {
    "$ref": "#/components/schemas/CoursingPolicy"
   },
   "courseNames": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "autoFireMinutes": {
    "type": "integer",
    "nullable": true
   },
   "serviceModeOverrides": {
    "type": "object",
    "description": "A different default per service mode.",
    "propertyNames": {
     "$ref": "#/components/schemas/ServiceMode"
    },
    "additionalProperties": {
     "$ref": "#/components/schemas/CoursingPolicy"
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `outlet` scope."
   }
  }
 },
 "CoursingPolicy": {
  "type": "string",
  "description": "How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n",
  "enum": [
   "fireAndForget",
   "holdAndFire",
   "phased",
   "timed",
   "delayed"
  ]
 },
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
   },
   "redeemEntitlementId": {
    "type": "string",
    "nullable": true,
    "x-ticvai-references": "access.entitlement",
    "description": "**A meal combo redeemed at the till or by a scan** (29 September, MOB-4; applied 30 September). The entitlement a bundle's `fnbMenuItem` component issued (promotions `BundleComponent.componentKind: fnbMenuItem`, `menuItemId`, `redeemAtOutletIds`). The line is priced at zero against it, `menuItemId` must be the component's menu item and the outlet one of `redeemAtOutletIds` (or any outlet with the item on a live menu when that list is empty), and the entitlement is marked used in the same step through access `validateAccess` at the outlet. An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is refused the same way if it was used meanwhile."
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
     "archivedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"
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
 "EightySixEvent": {
  "type": "object",
  "x-ticvai-persistence": "fnb.sold_out_item",
  "description": "Board 5J. **`setItemAvailability` recorded the current state and not the history.** An item 86'd at 7pm on a Saturday is a lost-sales figure and a prep-planning signal, and the package kept only the flag.\n**`refusedOrderCount` is what makes it worth keeping.** *Off for ninety minutes* is a note; *off for ninety minutes and eleven guests asked for it* is a purchasing decision.\n",
  "required": [
   "id",
   "menuItemId",
   "offAt"
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
   "menuItemId": {
    "type": "string",
    "format": "uuid"
   },
   "offAt": {
    "type": "string",
    "format": "date-time"
   },
   "backAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "enum": [
     "ranOut",
     "qualityIssue",
     "equipmentDown",
     "supplierFailure",
     "seasonal",
     "other"
    ],
    "description": "`other` always carries a `note` (audit R222)."
   },
   "note": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "The note given with the 86. Required where the reason is `other` (audit R222)."
   },
   "calledByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "refusedOrderCount": {
    "type": "integer",
    "default": 0,
    "readOnly": true
   }
  }
 },
 "FnbOrder": {
  "x-ticvai-persistence": "fnb.service_order + fnb.service_order_line",
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
   "salesOrderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "x-ticvai-references": "orders.sales_order",
    "description": "**Retyped 29 September (SD-046)**: `orders.sales_order.id` is a ULID, so a uuid here could never join. **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both offline-sync fields, and no plain updated timestamp.\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "kitchenTicketId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "kitchenTickets": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The kitchen tickets this order created, one per station (SD-046). Returned, not stored here; they are `fnb.kitchen_ticket` rows.",
    "items": {
     "$ref": "#/components/schemas/KitchenTicket"
    }
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
 "GeneratedQuery": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n",
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
   },
   "compiledSql": {
    "type": "string",
    "nullable": true,
    "description": "The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"
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
 "KitchenException": {
  "type": "object",
  "x-ticvai-persistence": "fnb.kitchen_exception",
  "description": "Board 3, 24 August. **Something that cost the kitchen a service and left no other trace** — equipment down, an item run out mid-ticket, a late delivery, a station short.\n`refireItem` covers a dish. **This covers the reasons a venue looking at a bad Saturday needs**, and which currently live in somebody's memory.\n",
  "required": [
   "id",
   "kind",
   "raisedAt"
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
   "stationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ticketId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "equipmentDown",
     "itemRanOut",
     "lateDelivery",
     "staffShort",
     "powerLoss",
     "spillage",
     "chased",
     "other"
    ],
    "description": "`other` always carries a `note` (audit R222)."
   },
   "durationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "KitchenSla": {
  "type": "object",
  "description": "**How long a ticket may sit, per service mode, and what pushes it up the rail** (`setKitchenSla`). The priority weights are the ones `listKitchenTickets` orders the rail by.\n",
  "properties": {
   "targets": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "serviceMode",
      "targetMinutes"
     ],
     "properties": {
      "serviceMode": {
       "$ref": "#/components/schemas/ServiceMode"
      },
      "targetMinutes": {
       "type": "integer",
       "minimum": 1
      },
      "warnAtPercent": {
       "type": "integer",
       "default": 80
      }
     }
    }
   },
   "priorityWeights": {
    "type": "object",
    "description": "The weight of each signal the board names — age, promise time, table stage, a VIP marker.",
    "properties": {
     "age": {
      "type": "integer",
      "minimum": 0
     },
     "targetReadyAt": {
      "type": "integer",
      "minimum": 0,
      "description": "Promise time."
     },
     "tableStage": {
      "type": "integer",
      "minimum": 0
     },
     "vip": {
      "type": "integer",
      "minimum": 0
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
   "displayWorkstationIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**The kitchen displays assigned to this station** (decided 28 September, audit R277), as tenancy `Workstation` ids, primary first and fallbacks after it. Set with `setKitchenStations`. A display reads the rail for the station it is assigned to (`listKitchenTickets`). A workstation is assigned to at most one station; a second assignment is refused `400`.\n"
   },
   "displayEndpoint": {
    "type": "string",
    "nullable": true,
    "description": "The P15 Kitchen Display device this station's tickets go to (19 Sep: the display is TICVAI software on commodity hardware, per station, with a fallback device where the primary is down — 18 Aug minute). Absent where the station has no display assigned.\n"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."
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
    "allOf": [
     {
      "$ref": "#/components/schemas/CoursingPolicy"
     }
    ],
    "nullable": true,
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
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
        "$ref": "#/components/schemas/AllergenCode"
       }
      },
      "refireOfLineId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
       "nullable": true,
       "readOnly": true,
       "description": "**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."
      },
      "refireReason": {
       "allOf": [
        {
         "$ref": "#/components/schemas/RefireReason"
        }
       ],
       "nullable": true,
       "readOnly": true
      },
      "isChargeable": {
       "type": "boolean",
       "nullable": true,
       "readOnly": true,
       "description": "A refire's `chargeable` flag. Null on a line that is not a refire."
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
    "x-ticvai-column": "list_price",
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
   "menuSectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."
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
   "restoreAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."
   },
   "preparationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "allergens": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AllergenCode"
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
   "reliability"
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
    "description": "What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."
   },
   "semanticSpec": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingSemanticQuerySpec"
     }
    ],
    "nullable": true,
    "description": "What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"
   },
   "generatedQuery": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GeneratedQuery"
     }
    ],
    "nullable": true,
    "description": "The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"
   },
   "result": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportResult"
     }
    ],
    "nullable": true,
    "description": "Null when the question is outside the semantic model."
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."
   },
   "reliability": {
    "$ref": "#/components/schemas/ReportingAnswerReliability"
   },
   "unavailableReason": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingUnavailableReason"
     }
    ],
    "nullable": true,
    "description": "Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "deprecated": true,
    "description": "Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."
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
 "OrderLabel": {
  "type": "object",
  "x-ticvai-persistence": "none — rendered from the kitchen ticket and its order",
  "description": "**What goes on the bag** (`printOrderLabel`). Order number, guest name, items and **the allergen flags, which are the reason the label is rendered by the server** from the same source as the order rather than printed from whatever the client has.\n",
  "required": [
   "ticketId",
   "orderNumber",
   "lines",
   "allergens"
  ],
  "properties": {
   "ticketId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderNumber": {
    "type": "string"
   },
   "guestName": {
    "type": "string",
    "nullable": true
   },
   "serviceMode": {
    "$ref": "#/components/schemas/ServiceMode"
   },
   "deliveryLabel": {
    "type": "string",
    "nullable": true,
    "description": "Where it is going, as a runner would read it."
   },
   "buzzerCode": {
    "type": "string",
    "nullable": true
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "name",
      "quantity"
     ],
     "properties": {
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
      "allergens": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/AllergenCode"
       }
      }
     }
    }
   },
   "allergens": {
    "type": "array",
    "description": "Every allergen on the order, together. Present and possibly empty — never omitted.",
    "items": {
     "$ref": "#/components/schemas/AllergenCode"
    }
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
 "RefireReason": {
  "type": "string",
  "description": "Why a line was made again (`refireItem`). The reasons are the data.",
  "enum": [
   "overcooked",
   "undercooked",
   "wrongItem",
   "dropped",
   "cold",
   "allergyRisk",
   "guestChangedMind",
   "lateAdd"
  ]
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
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
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
 "ReportingAnswerReliability": {
  "type": "string",
  "description": "**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n",
  "enum": [
   "grounded",
   "partial",
   "conflictingSources",
   "insufficientEvidence"
  ]
 },
 "ReportingSemanticQuerySpec": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n",
  "required": [
   "metric",
   "period"
  ],
  "properties": {
   "metric": {
    "type": "string",
    "description": "A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."
   },
   "dimensions": {
    "type": "array",
    "maxItems": 5,
    "description": "Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.",
    "items": {
     "type": "string"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "operator"
     ],
     "properties": {
      "field": {
       "type": "string",
       "description": "A `SemanticModel` field code."
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
        "isNull",
        "isNotNull"
       ]
      },
      "values": {
       "type": "array",
       "description": "**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n",
       "items": {}
      }
     }
    }
   },
   "period": {
    "type": "string",
    "description": "ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."
   },
   "comparison": {
    "type": "string",
    "nullable": true,
    "description": "As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.",
    "enum": [
     "previousPeriod",
     "samePeriodLastYear",
     "target",
     "benchmark"
    ]
   },
   "semanticModelVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."
   }
  }
 },
 "ReportingUnavailableReason": {
  "type": "string",
  "description": "Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.",
  "enum": [
   "metricNotModelled",
   "dimensionNotModelled",
   "filterNotModelled",
   "comparisonNotAvailable",
   "periodOutsideHistory"
  ]
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
 "StationRebalance": {
  "type": "object",
  "description": "**A temporary move of work between stations** (`rebalanceStationLoad`). Reverts at `revertAt`, or at close where that is null — a permanent change is `setKitchenStations`.\n",
  "required": [
   "moves"
  ],
  "properties": {
   "moves": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "fromStationId",
      "toStationId"
     ],
     "properties": {
      "fromStationId": {
       "type": "string",
       "format": "uuid"
      },
      "toStationId": {
       "type": "string",
       "format": "uuid"
      },
      "categoryIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "revertAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `setVenueSettings`."
   },
   "calendarDayStartHour": {
    "type": "integer",
    "minimum": 0,
    "maximum": 23,
    "nullable": true,
    "default": 6,
    "description": "**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "readOnly": true,
    "description": "**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "nullable": true,
    "readOnly": true,
    "description": "**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"
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
      "type": "string",
      "description": "IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"
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
         "type": "string",
         "description": "Wall-clock time the desk opens."
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time the desk closes."
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
      "type": "string",
      "description": "Wall-clock time sending stops",
      "in the region's time zone.": null
     },
     "to": {
      "type": "string",
      "description": "Wall-clock time sending resumes",
      "in the region's time zone.": null
     }
    }
   },
   "biometrics": {
    "type": "object",
    "nullable": true,
    "description": "CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false,
      "description": "**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"
     },
     "dpiaReference": {
      "type": "string",
      "nullable": true,
      "maxLength": 200,
      "description": "**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"
     },
     "consentNoticeAcknowledgedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"
     },
     "acknowledgedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "readOnly": true,
      "description": "**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"
     },
     "faceTagPurgeMinutesAfterClose": {
      "type": "integer",
      "nullable": true,
      "default": 0,
      "description": "BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"
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
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
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
       "off",
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": "off",
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
   },
   "displayCurrencies": {
    "type": "array",
    "nullable": true,
    "description": "**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{3}$"
    }
   },
   "cartLeaseSeconds": {
    "type": "integer",
    "nullable": true,
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"
   },
   "cartHoldExtensionMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 30,
    "default": 5,
    "description": "How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."
   },
   "cartMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."
   },
   "resaleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."
   },
   "exchangeCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."
   },
   "rescheduleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."
   },
   "reservationMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."
   },
   "shiftVarianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"
   },
   "catalogue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxVariantsPerProduct": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 2000,
      "default": 200,
      "description": "Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."
     },
     "waitlistOfferHoldMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 1440,
      "default": 30,
      "description": "How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 10,
      "description": "A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationCount": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 50,
      "description": "A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     }
    }
   },
   "inventory": {
    "type": "object",
    "nullable": true,
    "properties": {
     "overReceiptTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 5,
      "description": "Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."
     },
     "countVarianceTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 2,
      "description": "Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."
     },
     "countVarianceApprovalAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"
     }
    }
   },
   "seating": {
    "type": "object",
    "nullable": true,
    "properties": {
     "seatHoldExtensionSeconds": {
      "type": "integer",
      "nullable": true,
      "minimum": 60,
      "maximum": 1800,
      "default": 300,
      "description": "What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."
     },
     "seatHoldMaxExtensions": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 5,
      "default": 2,
      "description": "How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."
     },
     "maxSeatsPerGuestOrder": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 50,
      "default": 10,
      "description": "**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"
     }
    }
   },
   "promotions": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 30,
      "description": "The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."
     },
     "nearZeroLinePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"
     }
    }
   },
   "fnb": {
    "type": "object",
    "nullable": true,
    "properties": {
     "recallWindowMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 60,
      "default": 10,
      "description": "Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."
     },
     "compEscalationAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"
     },
     "foodSafetyLeadPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"
     }
    }
   },
   "queue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "crossQueueLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 10,
      "default": 2,
      "description": "Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "reporting": {
    "type": "object",
    "nullable": true,
    "properties": {
     "inlineRunRowLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1000,
      "maximum": 100000,
      "default": 5000,
      "description": "Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."
     },
     "dashboardRefreshBudgetPerMinute": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 24,
      "description": "Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."
     }
    }
   },
   "marketing": {
    "type": "object",
    "nullable": true,
    "properties": {
     "attributionWindowDays": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 30,
      "default": 7,
      "description": "Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "identity": {
    "type": "object",
    "nullable": true,
    "properties": {
     "guestOtpMaxAttempts": {
      "type": "integer",
      "nullable": true,
      "minimum": 3,
      "maximum": 10,
      "default": 5,
      "description": "Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"
     },
     "guestTwoStep": {
      "type": "object",
      "nullable": true,
      "description": "**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n",
      "properties": {
       "enabled": {
        "type": "boolean",
        "default": false,
        "description": "Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."
       },
       "stepUpActions": {
        "type": "array",
        "uniqueItems": true,
        "description": "The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n",
        "items": {
         "type": "string",
         "enum": [
          "changeContactDetails",
          "changePassword",
          "managePaymentMethods",
          "transferTickets",
          "deleteAccount"
         ]
        },
        "default": [
         "changeContactDetails",
         "changePassword",
         "managePaymentMethods",
         "deleteAccount"
        ]
       }
      }
     }
    }
   }
  }
 }
}
```
