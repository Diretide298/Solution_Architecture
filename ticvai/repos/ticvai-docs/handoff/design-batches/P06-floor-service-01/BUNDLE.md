# P06-floor-service-01 — P06 · Floor Service

**10 screens · 31 operations · 26 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **19 of these operations work offline**: compItem, createFnbOrder, createPayment, fireCourse, getBill, getTableMap, holdCourse, joinRestaurantWaitlist
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-051` | Restaurant Service Command Center | listDetail | 3 | 0 | — |
| `EMP-052` | Floor Plan & Table Map | statusTracker | 2 | 0 | — |
| `EMP-053` | Table & Seating Configuration | configEditor | 1 | 0 | — |
| `EMP-054` | Reservation Calendar & Timeline | listDetail | 1 | 0 | — |
| `EMP-055` | Create / Edit Reservation | configEditor | 2 | 0 | — |
| `EMP-056` | Walk-In & Waitlist Management | configEditor | 1 | 0 | — |
| `EMP-057` | Guest Profile & Dining History | listDetail | 4 | 0 | — |
| `EMP-058` | Live Table & Service Management | configEditor | 16 | 1 | — |
| `EMP-059` | Table Order, Bill & Payment Management | statusTracker | 7 | 1 | — |
| `EMP-060` | Reservation & Table Performance | listDetail | 2 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-051",
  "name": "Restaurant Service Command Center",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/restaurant-service-command-center",
   "component": "apps/venue-staff-app/src/routes/operations/RestaurantServiceCommandCenterDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
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
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4a`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Restaurant Service Command Center* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4a"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTableReservations` reads the population and `getTableMap` reads one of them — list, select, act",
  "purpose": "Restaurant Service Command Center — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "listFnbOrders",
    "why": "**1 declared operation reach no component on this screen**: listFnbOrders. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every restaurant service",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tableIds",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected restaurant service",
       "bindsTo": "TableMap",
       "columns": [
        "TableMap.outletId",
        "TableMap.zones",
        "TableMap.tables"
       ],
       "operation": "getTableMap",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/tables"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search restaurant service command center",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The restaurant service list.",
   "error": "Could not load. Names which read failed and leaves the restaurant service untouched.",
   "emptyFirstRun": "No restaurant service yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the restaurant service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getTableMap",
    "contract": "fnb",
    "purpose": "Table map with live state",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTableReservations",
    "contract": "fnb",
    "purpose": "Bookings for a service period",
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
     "name": "outletId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "TableMap.outletId",
    "TableMap.zones",
    "TableMap.tables"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-051",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "EMP-052",
  "name": "Floor Plan & Table Map",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/floor-plan-table-map",
   "component": "apps/venue-staff-app/src/routes/operations/FloorPlanTableMapDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
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
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Floor Plan &amp; Table Map* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4b"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getTableMap` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Floor Plan & Table Map — from the client design board, 20 August.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected floor plan table",
       "bindsTo": "TableMap",
       "columns": [
        "TableMap.outletId",
        "TableMap.zones",
        "TableMap.tables"
       ],
       "operation": "getTableMap",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/tables"
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
       "operation": "setTableLayout",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search floor plan",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The floor plan table list.",
   "error": "Could not load. Names which read failed and leaves the floor plan table untouched.",
   "emptyFirstRun": "No floor plan table yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the floor plan table are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getTableMap",
    "contract": "fnb",
    "purpose": "Table map with live state",
    "trigger": "onLoad"
   },
   {
    "operationId": "setTableLayout",
    "contract": "fnb",
    "purpose": "Configure the table layout",
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
     "name": "outletId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-052",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "EMP-053",
  "name": "Table & Seating Configuration",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/table-seating-configuration",
   "component": "apps/venue-staff-app/src/routes/operations/TableSeatingConfigurationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
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
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4c`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Table &amp; Seating Configuration* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4c"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setTableLayout`) and no read of a population — it is settings, not a list",
  "purpose": "Table & Seating Configuration — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "TableDefinition.id",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "label",
       "bindsTo": "TableDefinition.label",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "capacity",
       "bindsTo": "TableDefinition.capacity",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "zone",
       "bindsTo": "TableDefinition.zone",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "position",
       "bindsTo": "TableDefinition.position",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "shape",
       "bindsTo": "TableDefinition.shape",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setTableLayout",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search table",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved table seating.",
   "error": "Could not load. Names which read failed and leaves the table seating untouched.",
   "emptyFirstRun": "No table seating configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "setTableLayout",
    "contract": "fnb",
    "purpose": "Configure the table layout",
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
     "name": "outletId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-053",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "EMP-054",
  "name": "Reservation Calendar & Timeline",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/reservation-calendar-timeline",
   "component": "apps/venue-staff-app/src/routes/operations/ReservationCalendarTimelineDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
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
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Reservation Calendar &amp; Timeline* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTableReservations` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Reservation Calendar & Timeline — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every reservation calendar timeline",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tableIds",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reservation calendar timeline",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tableIds",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes",
        "TableReservation.actualPartySize",
        "TableReservation.tableVisitId"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search reservation calendar",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation calendar timeline list.",
   "error": "Could not load. Names which read failed and leaves the reservation calendar timeline untouched.",
   "emptyFirstRun": "No reservation calendar timeline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservation calendar timeline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "listTableReservations",
    "contract": "fnb",
    "purpose": "Bookings for a service period",
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
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "TableReservation.id",
    "TableReservation.outletId",
    "TableReservation.subjectId",
    "TableReservation.guestName",
    "TableReservation.contactPoint"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-054",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "EMP-055",
  "name": "Create / Edit Reservation",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/create-edit-reservation",
   "component": "apps/venue-staff-app/src/routes/operations/CreateEditReservationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
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
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Create / Edit Reservation* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4e"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`createTableReservation`) and no read of a population — it is settings, not a list",
  "purpose": "Create / Edit Reservation — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "TableReservation.id",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "outletId",
       "bindsTo": "TableReservation.outletId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "subjectId",
       "bindsTo": "TableReservation.subjectId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "guestName",
       "bindsTo": "TableReservation.guestName",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "contactPoint",
       "bindsTo": "TableReservation.contactPoint",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "partySize",
       "bindsTo": "TableReservation.partySize",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "startsAt",
       "bindsTo": "TableReservation.startsAt",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "durationMinutes",
       "bindsTo": "TableReservation.durationMinutes",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "tableIds",
       "bindsTo": "TableReservation.tableIds",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "status",
       "bindsTo": "TableReservation.status",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "groupId",
       "bindsTo": "TableReservation.groupId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "notes",
       "bindsTo": "TableReservation.notes",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "actualPartySize",
       "bindsTo": "TableReservation.actualPartySize",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "tableVisitId",
       "bindsTo": "TableReservation.tableVisitId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible existing guest",
       "notes": "**Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.\n"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createTableReservation",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible existing guest",
       "notes": "**Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.\n"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search create / edit reservation",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible existing guest",
       "notes": "**Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.\n"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved create edit reservation.",
   "error": "Could not load. Names which read failed and leaves the create edit reservation untouched.",
   "emptyFirstRun": "No create edit reservation configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "createTableReservation",
    "contract": "fnb",
    "purpose": "Book a table in advance",
    "trigger": "onAction"
   },
   {
    "operationId": "matchGuest",
    "contract": "marketing-crm",
    "purpose": "Propose existing guests who may be the same person, before a second record is created",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-055",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "EMP-056",
  "name": "Walk-In & Waitlist Management",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/walk-in-waitlist-management",
   "component": "apps/venue-staff-app/src/routes/operations/WalkInWaitlistManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
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
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Walk-In &amp; Waitlist Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4f"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`joinRestaurantWaitlist`) and no read of a population — it is settings, not a list",
  "purpose": "Walk-In & Waitlist Management — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "RestaurantWaitlist.id",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "outletId",
       "bindsTo": "RestaurantWaitlist.outletId",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "subjectId",
       "bindsTo": "RestaurantWaitlist.subjectId",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "partySize",
       "bindsTo": "RestaurantWaitlist.partySize",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "quotedWaitMinutes",
       "bindsTo": "RestaurantWaitlist.quotedWaitMinutes",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "seatingPreference",
       "bindsTo": "RestaurantWaitlist.seatingPreference",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "status",
       "bindsTo": "RestaurantWaitlist.status",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "notifiedAt",
       "bindsTo": "RestaurantWaitlist.notifiedAt",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "holdExpiresAt",
       "bindsTo": "RestaurantWaitlist.holdExpiresAt",
       "provenance": "contract fnb.yaml POST /waitlist"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Join",
       "operation": "joinRestaurantWaitlist",
       "provenance": "contract fnb.yaml POST /waitlist"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search walk-in",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved walk-in waitlist.",
   "error": "Could not load. Names which read failed and leaves the walk-in waitlist untouched.",
   "emptyFirstRun": "No walk-in waitlist configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "joinRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Add a party to an outlet's waitlist",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-056",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "EMP-057",
  "name": "Guest Profile & Dining History",
  "module": "Floor Service",
  "requiresModule": "marketing",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/guest-profile-dining-history",
   "component": "apps/venue-staff-app/src/routes/operations/GuestProfileDiningHistoryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
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
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4g`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Guest Profile &amp; Dining History* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4g"
  ],
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getGuestProfile` reads one of them — list, select, act",
  "purpose": "Guest Profile & Dining History — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every guest profile dining",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible duplicates of this guest",
       "permission": "GUEST_MANAGE",
       "notes": "Candidates from `matchGuest`, each with the rule that matched it."
      },
      {
       "kind": "confirmDialog",
       "label": "Merge these two records",
       "permission": "GUEST_MANAGE",
       "notes": "**The consequence, stated before the act.** The losing record is superseded rather than deleted so a year of orders and consents keeps resolving; the merge is reversible for thirty days; and **consent takes the narrower of the two positions**, which is the one thing about a merge that is a regulatory question rather than a data one.\n"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected guest profile dining",
       "bindsTo": "GuestProfileDetail",
       "columns": [
        "GuestProfileDetail.id",
        "GuestProfileDetail.subjectId",
        "GuestProfileDetail.displayName",
        "GuestProfileDetail.email",
        "GuestProfileDetail.phone",
        "GuestProfileDetail.preferredLanguage",
        "GuestProfileDetail.preferredChannel",
        "GuestProfileDetail.guestLinkId",
        "GuestProfileDetail.tags",
        "GuestProfileDetail.engagementScore",
        "GuestProfileDetail.engagementTier",
        "GuestProfileDetail.lifetimeValue",
        "GuestProfileDetail.visitCount",
        "GuestProfileDetail.lastVisitAt",
        "GuestProfileDetail.isActive",
        "GuestProfileDetail.consents"
       ],
       "operation": "getGuestProfile",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible duplicates of this guest",
       "permission": "GUEST_MANAGE",
       "notes": "Candidates from `matchGuest`, each with the rule that matched it."
      },
      {
       "kind": "confirmDialog",
       "label": "Merge these two records",
       "permission": "GUEST_MANAGE",
       "notes": "**The consequence, stated before the act.** The losing record is superseded rather than deleted so a year of orders and consents keeps resolving; the merge is reversible for thirty days; and **consent takes the narrower of the two positions**, which is the one thing about a merge that is a regulatory question rather than a data one.\n"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search guest profile",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible duplicates of this guest",
       "permission": "GUEST_MANAGE",
       "notes": "Candidates from `matchGuest`, each with the rule that matched it."
      },
      {
       "kind": "confirmDialog",
       "label": "Merge these two records",
       "permission": "GUEST_MANAGE",
       "notes": "**The consequence, stated before the act.** The losing record is superseded rather than deleted so a year of orders and consents keeps resolving; the merge is reversible for thirty days; and **consent takes the narrower of the two positions**, which is the one thing about a merge that is a regulatory question rather than a data one.\n"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest profile dining list.",
   "error": "Could not load. Names which read failed and leaves the guest profile dining untouched.",
   "emptyFirstRun": "No guest profile dining yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest profile dining are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Read a guest profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "matchGuest",
    "contract": "marketing-crm",
    "purpose": "Find other records that may be this same person",
    "trigger": "onAction"
   },
   {
    "operationId": "mergeGuests",
    "contract": "marketing-crm",
    "purpose": "Merge a proposed duplicate into this profile, once a person has decided",
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
     "name": "subjectId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "GuestProfileDetail.id",
    "GuestProfileDetail.subjectId",
    "GuestProfileDetail.displayName",
    "GuestProfileDetail.email",
    "GuestProfileDetail.phone"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-057",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "EMP-058",
  "name": "Live Table & Service Management",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/live-table-service-management",
   "component": "apps/venue-staff-app/src/routes/operations/LiveTableServiceManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-059",
    "EMP-060"
   ],
   "transitions": [
    {
     "to": "EMP-059",
     "trigger": "Food is ordered with courses",
     "provenance": "flow F29 step 2→3"
    },
    {
     "to": "EMP-060",
     "trigger": "Reservation & Table Performance",
     "provenance": "flow F80 step 2→3, F94 step 1→2"
    },
    {
     "to": "KIT-002",
     "trigger": "One main comes back wrong",
     "provenance": "flow F29 step 5→6",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Cross-platform navigation removed 24 August**: KIT-002. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4a",
   "FnB Board 4.dc.html#fnb-4b",
   "FnB Board 4.dc.html#fnb-4h"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`openTableVisit`, `updateTableVisit`, `mergeTableVisits`) and no read of a population — it is settings, not a list",
  "purpose": "Live Table & Service Management — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "OpenTableVisitRequest.id",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "tableId",
       "bindsTo": "OpenTableVisitRequest.tableId",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "covers",
       "bindsTo": "OpenTableVisitRequest.covers",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "serverPrincipalId",
       "bindsTo": "OpenTableVisitRequest.serverPrincipalId",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "subjectId",
       "bindsTo": "OpenTableVisitRequest.subjectId",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "recordedAt",
       "bindsTo": "OpenTableVisitRequest.recordedAt",
       "provenance": "contract fnb.yaml POST /table-visits"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Open",
       "operation": "openTableVisit",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateTableVisit",
       "provenance": "contract fnb.yaml PATCH /table-visits/{visitId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Merge",
       "operation": "mergeTableVisits",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/merge"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer",
       "operation": "transferTableVisit",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Seat",
       "operation": "seatTableReservation",
       "provenance": "contract fnb.yaml POST /table-reservations/{reservationId}/seat"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setServiceStage",
       "provenance": "contract fnb.yaml PUT /table-visits/{visitId}/stage"
      },
      {
       "kind": "secondaryButton",
       "label": "Move",
       "operation": "moveTableVisit",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/move"
      },
      {
       "kind": "secondaryButton",
       "label": "Reassign",
       "operation": "reassignServer",
       "provenance": "contract fnb.yaml PUT /table-visits/{visitId}/server"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify",
       "operation": "notifyServer",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/notify-server"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders"
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
       "operation": "setTableCombinations",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/table-combinations"
      },
      {
       "kind": "secondaryButton",
       "label": "Quote",
       "operation": "quoteWaitTime",
       "provenance": "contract fnb.yaml POST /waitlist/{entryId}/quote"
      },
      {
       "kind": "secondaryButton",
       "label": "Join",
       "operation": "joinRestaurantWaitlist",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify",
       "operation": "notifyWaitlistParty",
       "provenance": "contract fnb.yaml POST /waitlist/{entryId}/notify"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search live table",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmMergeTableVisits",
    "component": "confirmDialog",
    "trigger": "Merge",
    "body": "**Names what `mergeTableVisits` changes and what it leaves alone**, in the consequence rather than the verb. A live table service this affects should be identified in the dialog, not just counted.",
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/merge"
   }
  ],
  "states": {
   "loading": "The saved live table service.",
   "error": "Could not load. Names which read failed and leaves the live table service untouched.",
   "emptyFirstRun": "No live table service configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "openTableVisit",
    "contract": "fnb",
    "purpose": "Seat a party and open a visit",
    "trigger": "onAction"
   },
   {
    "operationId": "updateTableVisit",
    "contract": "fnb",
    "purpose": "Amend covers, move table, or reassign server",
    "trigger": "onAction"
   },
   {
    "operationId": "mergeTableVisits",
    "contract": "fnb",
    "purpose": "Merge another visit into this one",
    "trigger": "onAction"
   },
   {
    "operationId": "transferTableVisit",
    "contract": "fnb",
    "purpose": "Move a check to another server",
    "trigger": "onAction"
   },
   {
    "operationId": "seatTableReservation",
    "contract": "fnb",
    "purpose": "The party arrived and has been sat down",
    "trigger": "onAction"
   },
   {
    "operationId": "setServiceStage",
    "contract": "fnb",
    "purpose": "Where this table is in its meal",
    "trigger": "onAction"
   },
   {
    "operationId": "moveTableVisit",
    "contract": "fnb",
    "purpose": "Move a party to a different table, mid-service",
    "trigger": "onAction"
   },
   {
    "operationId": "reassignServer",
    "contract": "fnb",
    "purpose": "Hand a table to another server",
    "trigger": "onAction"
   },
   {
    "operationId": "notifyServer",
    "contract": "fnb",
    "purpose": "The kitchen calls the server to the pass",
    "trigger": "onAction"
   },
   {
    "operationId": "createFnbOrder",
    "contract": "fnb",
    "purpose": "Place an F&B order",
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
    "operationId": "setTableCombinations",
    "contract": "fnb",
    "purpose": "Which tables can be pushed together, and to what capacity",
    "trigger": "onAction"
   },
   {
    "operationId": "quoteWaitTime",
    "contract": "fnb",
    "purpose": "Tell a party how long, and mean it",
    "trigger": "onAction"
   },
   {
    "operationId": "joinRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Add a party to an outlet's waitlist",
    "trigger": "onAction"
   },
   {
    "operationId": "notifyWaitlistParty",
    "contract": "fnb",
    "purpose": "Their table is ready",
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
     "name": "visitId",
     "from": "EMP-003"
    },
    {
     "name": "reservationId",
     "from": "deepLink"
    },
    {
     "name": "entryId",
     "from": "deepLink",
     "optional": true
    },
    {
     "name": "outletId",
     "from": "session",
     "optional": true
    },
    {
     "name": "ticketId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. A booking opened from the timeline. **The host taps a reservation to seat it** — that is the only way in. A waitlist party tapped on the list. Resolves from the shift assignment. A ticket tapped on the rail."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-058",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 16 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "EMP-059",
  "name": "Table Order, Bill & Payment Management",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/table-order-bill-payment-management",
   "component": "apps/venue-staff-app/src/routes/operations/TableOrderBillPaymentManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-058"
   ],
   "transitions": [
    {
     "to": "EMP-058",
     "trigger": "Live Table & Service Management",
     "provenance": "flow F80 step 1→2",
     "operation": "transferOrderItems"
    },
    {
     "to": "KIT-002",
     "trigger": "The kitchen makes the starters and bumps them",
     "provenance": "flow F29 step 3→4",
     "operation": "createFnbOrder",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4j"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getBill` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Table Order, Bill & Payment Management — from the client design board, 20 August.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected table order bill",
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
       "operation": "getBill",
       "provenance": "contract fnb.yaml GET /table-visits/{visitId}/bill"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeTableVisit",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPayment",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Split",
       "operation": "splitBill",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/bill/split"
      },
      {
       "kind": "secondaryButton",
       "label": "Comp",
       "operation": "compItem",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/comp"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer",
       "operation": "transferOrderItems",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/transfer-items"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search table order, bill",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseTableVisit",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeTableVisit` changes and what it leaves alone**, in the consequence rather than the verb. A table order bill this affects should be identified in the dialog, not just counted.",
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/close"
   }
  ],
  "states": {
   "loading": "The table order bill list.",
   "error": "Could not load. Names which read failed and leaves the table order bill untouched.",
   "emptyFirstRun": "No table order bill yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the table order bill are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "closeTableVisit",
    "contract": "fnb",
    "purpose": "Settle and close a visit",
    "trigger": "onAction"
   },
   {
    "operationId": "createPayment",
    "contract": "orders",
    "purpose": "Take a payment against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "createFnbOrder",
    "contract": "fnb",
    "purpose": "Place an F&B order",
    "trigger": "onAction"
   },
   {
    "operationId": "splitBill",
    "contract": "fnb",
    "purpose": "Split a bill",
    "trigger": "onAction"
   },
   {
    "operationId": "getBill",
    "contract": "fnb",
    "purpose": "Bill for a visit",
    "trigger": "onLoad"
   },
   {
    "operationId": "compItem",
    "contract": "fnb",
    "purpose": "Take a line off the bill, with a reason and a name",
    "trigger": "onAction"
   },
   {
    "operationId": "transferOrderItems",
    "contract": "fnb",
    "purpose": "Move items to another table's bill",
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
     "name": "visitId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-059",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "EMP-060",
  "name": "Reservation & Table Performance",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/reservation-table-performance",
   "component": "apps/venue-staff-app/src/routes/operations/ReservationTablePerformanceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003",
    "EMP-058"
   ],
   "exitTo": [
    "EMP-003",
    "EMP-061"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-061",
     "trigger": "Retail Inventory Command Center",
     "provenance": "flow F80 step 3→4, F94 step 2→3"
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
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.**",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTableReservations` reads the population and `getTableMap` reads one of them — list, select, act",
  "purpose": "Reservation & Table Performance — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every reservation table performance",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tableIds",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reservation table performance",
       "bindsTo": "TableMap",
       "columns": [
        "TableMap.outletId",
        "TableMap.zones",
        "TableMap.tables"
       ],
       "operation": "getTableMap",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/tables"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search reservation",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation table performance list.",
   "error": "Could not load. Names which read failed and leaves the reservation table performance untouched.",
   "emptyFirstRun": "No reservation table performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservation table performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "listTableReservations",
    "contract": "fnb",
    "purpose": "Bookings for a service period",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTableMap",
    "contract": "fnb",
    "purpose": "Table map with live state",
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
     "name": "outletId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "TableMap.outletId",
    "TableMap.zones",
    "TableMap.tables"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-060",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "closeTableVisit": {
  "method": "POST",
  "path": "/table-visits/{visitId}/close",
  "contract": "fnb",
  "summary": "Settle and close a visit",
  "permission": "ORDER_CREATE",
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
  "responds": null
 },
 "compItem": {
  "method": "POST",
  "path": "/table-visits/{visitId}/comp",
  "contract": "fnb",
  "summary": "Take a line off the bill, with a reason and a name",
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
  "requestBody": null,
  "responds": "TableVisit"
 },
 "createFnbOrder": {
  "method": "POST",
  "path": "/fnb-orders",
  "contract": "fnb",
  "summary": "Place an F&B order",
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
  "requestBody": "CreateFnbOrderRequest",
  "responds": "FnbOrder"
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
 "getBill": {
  "method": "GET",
  "path": "/table-visits/{visitId}/bill",
  "contract": "fnb",
  "summary": "Bill for a visit",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Bill"
 },
 "getGuestProfile": {
  "method": "GET",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Read a guest profile",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestProfileDetail"
 },
 "getTableMap": {
  "method": "GET",
  "path": "/outlets/{outletId}/tables",
  "contract": "fnb",
  "summary": "Table map with live state",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TableMap"
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
 "listTableReservations": {
  "method": "GET",
  "path": "/table-reservations",
  "contract": "fnb",
  "summary": "Bookings for a service period",
  "permission": "ORDER_MODIFY",
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
    "name": "date",
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
  "responds": "TableReservation"
 },
 "matchGuest": {
  "method": "POST",
  "path": "/guests/match",
  "contract": "marketing-crm",
  "summary": "Is this the same person we already have?",
  "permission": "GUEST_VIEW",
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
 "mergeGuests": {
  "method": "POST",
  "path": "/guests/merge",
  "contract": "marketing-crm",
  "summary": "Two records, one person",
  "permission": "GUEST_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "mergeTableVisits": {
  "method": "POST",
  "path": "/table-visits/{visitId}/merge",
  "contract": "fnb",
  "summary": "Merge another visit into this one",
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
  "responds": "TableVisit"
 },
 "moveTableVisit": {
  "method": "POST",
  "path": "/table-visits/{visitId}/move",
  "contract": "fnb",
  "summary": "Move a party to a different table, mid-service",
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
  "responds": "TableVisit"
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
 "notifyWaitlistParty": {
  "method": "POST",
  "path": "/waitlist/{entryId}/notify",
  "contract": "fnb",
  "summary": "Their table is ready",
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
 "openTableVisit": {
  "method": "POST",
  "path": "/table-visits",
  "contract": "fnb",
  "summary": "Seat a party and open a visit",
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
  "requestBody": "OpenTableVisitRequest",
  "responds": "TableVisit"
 },
 "quoteWaitTime": {
  "method": "POST",
  "path": "/waitlist/{entryId}/quote",
  "contract": "fnb",
  "summary": "Tell a party how long, and mean it",
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
 "reassignServer": {
  "method": "PUT",
  "path": "/table-visits/{visitId}/server",
  "contract": "fnb",
  "summary": "Hand a table to another server",
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
  "responds": "TableVisit"
 },
 "seatTableReservation": {
  "method": "POST",
  "path": "/table-reservations/{reservationId}/seat",
  "contract": "fnb",
  "summary": "The party arrived and has been sat down",
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
  "responds": "TableReservation"
 },
 "setServiceStage": {
  "method": "PUT",
  "path": "/table-visits/{visitId}/stage",
  "contract": "fnb",
  "summary": "Where this table is in its meal",
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
  "responds": "TableVisit"
 },
 "setTableCombinations": {
  "method": "PUT",
  "path": "/outlets/{outletId}/table-combinations",
  "contract": "fnb",
  "summary": "Which tables can be pushed together, and to what capacity",
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
 "setTableLayout": {
  "method": "PUT",
  "path": "/outlets/{outletId}/tables",
  "contract": "fnb",
  "summary": "Configure the table layout",
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
  "responds": "TableMap"
 },
 "splitBill": {
  "method": "POST",
  "path": "/table-visits/{visitId}/bill/split",
  "contract": "fnb",
  "summary": "Split a bill",
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
  "requestBody": "SplitBillRequest",
  "responds": "BillSplit"
 },
 "transferOrderItems": {
  "method": "POST",
  "path": "/table-visits/{visitId}/transfer-items",
  "contract": "fnb",
  "summary": "Move items to another table's bill",
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
  "responds": "TableVisit"
 },
 "transferTableVisit": {
  "method": "POST",
  "path": "/table-visits/{visitId}/transfer",
  "contract": "fnb",
  "summary": "Move a check to another server",
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
  "requestBody": null,
  "responds": null
 },
 "updateTableVisit": {
  "method": "PATCH",
  "path": "/table-visits/{visitId}",
  "contract": "fnb",
  "summary": "Amend covers, move table, or reassign server",
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
  "responds": "TableVisit"
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
 "BillSplit": {
  "x-ticvai-persistence": "fnb.bill_split + fnb.sub_bill",
  "type": "object",
  "required": [
   "visitId",
   "method",
   "subBills"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "visitId": {
    "type": "string"
   },
   "method": {
    "$ref": "#/components/schemas/SplitMethod"
   },
   "subBills": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "subBillId",
      "total",
      "status"
     ],
     "properties": {
      "subBillId": {
       "type": "string"
      },
      "lineIds": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "subtotal": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "taxAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "status": {
       "type": "string",
       "enum": [
        "unpaid",
        "paid"
       ]
      }
     }
    }
   }
  }
 },
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
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
   }
  }
 },
 "CreateFnbOrderRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "outletId",
   "serviceMode",
   "lines",
   "recordedAt"
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
   "serviceMode": {
    "$ref": "#/components/schemas/ServiceMode"
   },
   "tableVisitId": {
    "type": "string",
    "nullable": true,
    "description": "Required for table service. Absent for quick service."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateFnbOrderLine"
    }
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderedAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Cash only. Change is the difference."
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
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
 "GuestProfile": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "type": "object",
  "required": [
   "subjectId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "nullable": true
   },
   "phone": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "preferredChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells. Marketing acts locally."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "engagementScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"
   },
   "engagementTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "new",
     "active",
     "occasional",
     "lapsing",
     "lapsed",
     "dormant"
    ],
    "description": "5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"
   },
   "lifetimeValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "visitCount": {
    "type": "integer"
   },
   "lastVisitAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "GuestProfileDetail": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "allOf": [
   {
    "$ref": "#/components/schemas/GuestProfile"
   },
   {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
     },
     "consents": {
      "$ref": "#/components/schemas/ConsentState"
     },
     "loyalty": {
      "$ref": "#/components/schemas/LoyaltyPosition"
     },
     "openCaseCount": {
      "type": "integer"
     },
     "recentOrderIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "membershipIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "notes": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
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
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "OpenTableVisitRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "tableId",
   "covers",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "tableId": {
    "type": "string",
    "format": "uuid"
   },
   "covers": {
    "type": "integer",
    "minimum": 1,
    "description": "Captured at seating because it drives split-by-covers at close."
   },
   "serverPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
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
 "SplitBillRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "method"
  ],
  "properties": {
   "method": {
    "$ref": "#/components/schemas/SplitMethod"
   },
   "parts": {
    "type": "integer",
    "minimum": 2,
    "description": "For `byCovers` — defaults to the visit's cover count."
   },
   "amounts": {
    "type": "array",
    "description": "For `byAmount`. Must sum to the bill total.",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/Money"
    }
   },
   "lineAssignments": {
    "type": "array",
    "description": "For `byLine` or `bySeat`. Every line must be assigned exactly once.",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "partIndex"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "partIndex": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "categoryAssignments": {
    "type": "array",
    "description": "For `byCategory` — food to one part, beverage to another.",
    "items": {
     "type": "object",
     "required": [
      "categoryCode",
      "partIndex"
     ],
     "properties": {
      "categoryCode": {
       "type": "string"
      },
      "partIndex": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   }
  }
 },
 "SplitMethod": {
  "type": "string",
  "enum": [
   "byAmount",
   "byCovers",
   "byCategory",
   "byLine",
   "bySeat"
  ]
 },
 "TableMap": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "outletId",
   "tables"
  ],
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "zones": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "tables": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/TableState"
    }
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
 "TableState": {
  "x-ticvai-persistence": "none — projection over table and visit",
  "allOf": [
   {
    "$ref": "#/components/schemas/TableDefinition"
   },
   {
    "type": "object",
    "required": [
     "status"
    ],
    "properties": {
     "status": {
      "$ref": "#/components/schemas/TableStatus"
     },
     "visitId": {
      "type": "string",
      "nullable": true
     },
     "covers": {
      "type": "integer",
      "nullable": true
     },
     "seatedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "serverPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "billTotal": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    }
   }
  ]
 },
 "TableVisit": {
  "x-ticvai-persistence": "fnb.table_visit",
  "type": "object",
  "required": [
   "id",
   "tableId",
   "outletId",
   "covers",
   "status",
   "orders",
   "openedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "tableId": {
    "type": "string",
    "format": "uuid"
   },
   "tableLabel": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "covers": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "billRequested",
     "settled",
     "merged",
     "cancelled"
    ]
   },
   "serverPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orders": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FnbOrder"
    }
   },
   "mergedIntoVisitId": {
    "type": "string",
    "nullable": true
   },
   "mergedFromVisitIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "runningTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 }
}
```
